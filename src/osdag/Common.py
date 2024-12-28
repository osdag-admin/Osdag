#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Amir, Umair, Arsil

# FIXME: Keeping os even if not used here.
import os
import operator
import math
import logging
from importlib.resources import files

PATH_TO_DATABASE = files("osdag.data.ResourceFiles.Database").joinpath("Intg_osdag.sqlite")

import sqlite3

from .utils.common.other_standards import *
from .utils.common.component import *
# from design_type.connection.fin_plate_connection import FinPlateConnection
# from design_type.connection.column_cover_plate import ColumnCoverPlate

class OurLog(logging.Handler):

    def __init__(self, key):
        logging.Handler.__init__(self)

        self.key = key
        # self.key.setText("<h1>Welcome to Osdag</h1>")

    def handle(self, record):
        msg = self.format(record)
        if record.levelname == 'WARNING':
            msg = "<span style='color: blue;'>"+ msg +"</span>"
        elif record.levelname == 'ERROR':
            msg = "<span style='color: red;'>"+ msg +"</span>"
        elif record.levelname == 'INFO':
            msg = "<span style='color: green;'>" + msg + "</span>"
        self.key.append(msg)


def connectdb1():
    """
    Function to fetch diameter values from Bolt Table
     """
    # @author: Amir

    lst = []
    conn = sqlite3.connect(PATH_TO_DATABASE)
    cursor = conn.execute("SELECT Bolt_diameter FROM Bolt")
    rows = cursor.fetchall()
    for row in rows:
        lst.append(row)
    l2 = tuple_to_str_popup(lst)
    return l2

def connectdb2():
    """
    Function to fetch diameter values from Bolt Table
     """
    # @author: Amir

    lst = []
    conn = sqlite3.connect(PATH_TO_DATABASE)
    cursor = conn.execute("SELECT Diameter FROM Anchor_Bolt")
    rows = cursor.fetchall()
    for row in rows:
        lst.append(row)
    l2 = tuple_to_str_popup(lst)
    return l2


def connectdb(table_name, call_type="dropdown"):

    """
        Function to fetch designation values from respective Tables.
         """

    # @author: Amir
    conn = sqlite3.connect(PATH_TO_DATABASE)
    lst = []
    if table_name == "Angles":
        cursor = conn.execute("SELECT Designation FROM Angles")

    elif table_name == "Channels":
        cursor = conn.execute("SELECT Designation FROM Channels")

    elif table_name == "Beams":
        cursor = conn.execute("SELECT Designation FROM Beams")

    elif table_name == "Bolt":
        cursor = conn.execute("SELECT Bolt_diameter FROM Bolt")

    elif table_name == "Material":
        cursor = conn.execute("SELECT Grade FROM Material")

    elif table_name == "RHS":
        cursor = conn.execute("SELECT Designation FROM RHS")

    elif table_name == "SHS":
        cursor = conn.execute("SELECT Designation FROM SHS")

    elif table_name == "CHS":
        cursor = conn.execute("SELECT Designation FROM CHS")

    else:
        cursor = conn.execute("SELECT Designation FROM Columns")
    rows = cursor.fetchall()

    for row in rows:
        lst.append(row)

    final_lst = tuple_to_str(lst,call_type,table_name)
    if table_name == "Material" and call_type == "dropdown":
        final_lst.append("Custom")

    return final_lst


def connect_for_red(table_name):

    """
        Function to fetch designation values from various Tables where source is IS808_Old
    """

    # @author: Arsil
    conn = sqlite3.connect(PATH_TO_DATABASE)
    lst = []
    if table_name == "Angles":
        cursor = conn.execute("SELECT Designation FROM Angles WHERE Source = 'IS808_Old'")

    elif table_name == "Channels":
        cursor = conn.execute("SELECT Designation FROM Channels WHERE Source = 'IS808_Old'")

    elif table_name == "Beams":
        cursor = conn.execute("SELECT Designation FROM Beams WHERE Source = 'IS808_Old'")

    elif table_name == "Columns":
        cursor = conn.execute("SELECT Designation FROM Columns WHERE Source = 'IS808_Old'")

    else:
        return []
    rows = cursor.fetchall()

    for row in rows:
        lst.append(row)

    final_lst = tuple_to_str_red(lst)
    return final_lst


def red_list_function():

    """
        Function to form a list for old values from Columns and Beams table.
     """

    # @author: Arsil

    red_list = []
    red_list_columns = connect_for_red("Columns")
    red_list_beams = connect_for_red("Beams")
    red_list.extend(red_list_beams)
    red_list.extend(red_list_columns)
    return red_list


def tuple_to_str_popup(tl):

    # @author: Amir

    arr = []
    for v in tl:
        val = ''.join(v)
        arr.append(val)
    return arr

def tuple_to_str(tl, call_type,table_name=None):

    if call_type is "dropdown" and table_name != 'Material' and table_name != 'Bolt':
        arr = ['Select Section']
    else:
        arr = []
    for v in tl:
        val = ''.join(v)
        arr.append(val)
    return arr


def tuple_to_str_red(tl):
    arr = []
    for v in tl:
        val = ''.join(v)
        arr.append(val)
    return arr

def get_db_header(table_name):

    conn = sqlite3.connect(PATH_TO_DATABASE)

    if table_name == "Angles":
        cursor = conn.execute("SELECT * FROM Angles")

    elif table_name == "Channels":
        cursor = conn.execute("SELECT * FROM Channels")

    elif table_name == "Beams":
        cursor = conn.execute("SELECT * FROM Beams")

    else:
        cursor = conn.execute("SELECT * FROM Columns")

    header = [description[0] for description in cursor.description]

    return header

def get_source(table_name, designation):

    conn = sqlite3.connect(PATH_TO_DATABASE)

    if table_name == "Angles":
        cursor = conn.execute("SELECT Source FROM Angles WHERE Designation = ?", (designation,))

    elif table_name == "Channels":
        cursor = conn.execute("SELECT Source FROM Channels WHERE Designation = ?", (designation,))

    elif table_name == "Beams":
        cursor = conn.execute("SELECT Source FROM Beams WHERE Designation = ?", (designation,))

    else:
        cursor = conn.execute("SELECT Source FROM Columns WHERE Designation = ?", (designation,))

    source = cursor.fetchone()[0]
    return str(source)


class MaterialValidator(object):
    def __init__(self, material):
        self.material = str(material)
        self.typ = "Unknown"
        self.fy_20 = 0
        self.fy_20_40 = 0
        self.fy_40 = 0
        self.fu = 0
        self.custom_format_flag = False
        self.invalid_value = ""
        self.notations = ["Fy_20", "Fy_20_40", "Fy_40", "Fu"]
        material = self.material.split("_")
        if len(material) == 5:
            self.typ = material[0]
            self.fy_20 = material[1]
            self.fy_20_40 = material[2]
            self.fy_40 = material[3]
            self.fu = material[4]
        self.values = [self.fy_20, self.fy_20_40, self.fy_40, self.fu]
        if self.typ == "Cus":
            for i in self.values:
                if str(i) != "" and str(i).isdigit():
                    self.custom_format_flag = True
                else:
                    self.custom_format_flag = False
                    break

    def is_already_in_db(self):
        if self.material in connectdb("Material", call_type="popup"):
            return True
        else:
            return False

    def is_format_custom(self):
        return self.custom_format_flag

    def is_valid_custom(self):

        min_allowed = [165, 165, 165, 165]
        max_allowed = [1500, 1500, 1500, 1500]
        for i in range(4):
            if self.values[i] == "":
                continue
            if min_allowed[i] <= int(self.values[i]) <= max_allowed[i]:
                pass
            else:
                self.invalid_value = self.notations[i]
                break

        if self.invalid_value:
            return False
        else:
            return self.custom_format_flag

##########################
# Type Keys (Type of input field, tab type etc.)
###########################
TYPE_COMBOBOX = 'ComboBox'
TYPE_COMBOBOX_FREEZE = 'Disable_ComboBoc'
TYPE_TABLE_IN = 'Table_Input'
TYPE_TABLE_OU = 'Table_Output'
TYPE_TABLE_GUS = 'Gusset_Table'
TYPE_TEXTBOX = 'TextBox'
TYPE_TITLE = 'Title'
TYPE_LABEL = 'Label'
TYPE_IMAGE = 'Image'
TYPE_IMAGE_COMPRESSION = 'Image_compression'
TYPE_COMBOBOX_CUSTOMIZED = 'ComboBox_Customized'
TYPE_IN_BUTTON = 'Input_dock_Button'
TYPE_OUT_BUTTON = 'Output_dock_Button'
TYPE_OUT_DOCK = 'Output_dock_Item'
TYPE_OUT_LABEL = 'Output_dock_Label'
TYPE_BREAK = 'Break'
TYPE_ENTER = 'Enter'
TYPE_TEXT_BROWSER = 'TextBrowser'
TYPE_NOTE = 'Note'
TYPE_WARNING = 'Warning'
DESIGN_FLAG = 'False'
VALUE_NOT_APPLICABLE = 'N/A'
TYPE_TAB_1 = "TYPE_TAB_1"
TYPE_TAB_2 = "TYPE_TAB_2"
TYPE_TAB_3 = "TYPE_TAB_3"
TYPE_SECTION = 'Popup_Section'
TYPE_CUSTOM_MATERIAL = 'New_Material_Popup'
TYPE_CUSTOM_SECTION = 'New_Section_Popup'
TYPE_ENABLE_DISABLE = 'Enable/Disable'
TYPE_CHANGE_TAB_NAME = 'Change tab_name'
TYPE_REMOVE_TAB = 'Remove tab'
TYPE_OVERWRITE_VALIDATION = 'Overwrite_validation'
KEY_IMAGE = 'Image'
KEY_IMAGE_Y = 'Image_Y'
KEY_IMAGE_two = 'Imagetwo'
TYP_BEARING = "Bearing Bolt"
TYP_FRICTION_GRIP = "Friction Grip Bolt"

###################################
# Module Keys DONOT CHANGE THESE
###################################
KEY_MAIN_MODULE = 'Main Module'
KEY_MODULE_STATUS = 'Module.Status'

TYPE_MODULE = 'Window Title'

KEY_DISP_FINPLATE = 'Fin Plate Connection'
KEY_DISP_ENDPLATE = 'End Plate Connection'
KEY_DISP_CLEATANGLE = 'Cleat Angle Connection'
KEY_DISP_SEATED_ANGLE = 'Seated Angle Connection'
KEY_DISP_BASE_PLATE = 'Base Plate Connection'
KEY_DISP_TRUSS_BOLTED = 'Truss Connection Bolted'

KEY_DISP_BEAMCOVERPLATE = 'Beam-to-Beam Cover Plate Bolted Connection'
KEY_DISP_COLUMNCOVERPLATE = 'Column-to-Column Cover Plate Bolted Connection'
KEY_DISP_BEAMCOVERPLATEWELD = 'Beam-to-Beam Cover Plate Welded Connection'
KEY_DISP_COLUMNCOVERPLATEWELD = 'Column-to-Column Cover Plate Welded Connection'
# KEY_DISP_BEAMENDPLATE = 'Beam End Plate Connection'
KEY_DISP_COLUMNENDPLATE = 'Column-to-Column End Plate Connection'
KEY_DISP_BCENDPLATE = 'Beam-to-Column End Plate Connection'
KEY_DISP_TENSION_BOLTED = 'Tension Member Design - Bolted to End Gusset'
KEY_DISP_TENSION_WELDED = 'Tension Member Design - Welded to End Gusset'
KEY_DISP_BB_EP_SPLICE = 'Beam-to-Beam End Plate Connection'
KEY_DISP_COMPRESSION = 'Compression Member'
KEY_DISP_COMPRESSION_STRUT = 'Compression Member Design - Strut Design'

DISP_TITLE_CM = 'Connecting Members'

# Compression Members
KEY_DISP_COMPRESSION_COLUMN = 'Columns with known support conditions'
KEY_DISP_COMPRESSION_Strut = 'Struts in Trusses'
KEY_SECTION_PROPERTY = 'Section Property'
KEY_SECTION_DATA = 'Section Data'
KEY_MEMBER_PROPERTY = 'Member Property'
KEY_MEMBER_DATA = 'Member.Data'
KEY_SECTION_PROFILE = 'Section.Profile'
KEY_DISP_SECTION_PROFILE = 'Section Profile *'
VALUES_SEC_PROFILE_COLUMN = ['Beams', 'Columns', 'RHS', 'SHS', 'CHS', 'Angles']
KEY_SECTION_DEFINITION = 'SectionDefinition'
KEY_DISP_SECTION_DEFINITION = 'Section Definition*'
KEY_DISP_MEMBER_DATA = 'Member Data'
KEY_ACTUAL_LENGTH = 'Length.Actual'
KEY_DISP_ACTUAL_LENGTH = 'Actual Length'
KEY_COLUMN_DESIGN = 'Column Design'
KEY_COLUMN_CAPACITY = 'Column.Capacity'
KEY_DISP_COLUMN_CAPACITY = 'Column Capacity (kN)'
KEY_ACTUAL_LEN_ZZ = 'Actual.Length_zz'
KEY_DISP_ACTUAL_LEN_ZZ = 'Actual Length (z-z), mm'
KEY_ACTUAL_LEN_YY = 'Actual.Length_yy'
KEY_DISP_ACTUAL_LEN_YY = 'Actual Length (y-y), mm'
KEY_UNSUPPORTED_LEN_ZZ = 'Unsupported.Length_zz'
KEY_DISP_UNSUPPORTED_LEN_ZZ = 'Unsupported Length (z-z), mm'
KEY_UNSUPPORTED_LEN_YY = 'Unsupported.Length_yy'
KEY_DISP_UNSUPPORTED_LEN_YY = 'Unsupported Length (y-y), mm'
KEY_DESIGN_COMPRESSION = 'Design Results'
KEY_DESIGN_STRENGTH_COMPRESSION = 'Design.Strength'
KEY_MIN_DESIGN_COMP_STRESS = 'MinCompStress'
KEY_MIN_DESIGN_COMP_STRESS_VAL = 'Min. Design Comp.Stress (MPa)'
KEY_MAT_STRESS = 'MaterialStress'
KEY_DISP_MAT_STRESS = 'fy/gamma_m0'
KEY_FCD = 'Fcd'
KEY_DISP_FCD = 'f_cd'
KEY_DISP_DESIGN_STRENGTH_COMPRESSION = 'Design Strength (kN)'
DISP_TITLE_OPTIMUM_SECTION = 'Optimum Section'
KEY_TITLE_OPTIMUM_DESIGNATION = 'Optimum.Designation'
KEY_DISP_TITLE_OPTIMUM_DESIGNATION = 'Designation'
KEY_OPTIMUM_UR_COMPRESSION = 'Optimum.UR'
KEY_DISP_OPTIMUM_UR_COMPRESSION = 'Utilization Ratio'
KEY_OPTIMUM_SC = 'Optimum.SectionClassification'
KEY_DISP_OPTIMUM_SC = 'Section Classification'
DISP_TITLE_ZZ = 'Major Axis (z-z)'
DISP_TITLE_YY = 'Minor Axis (y-y)'
KEY_EFF_LEN_ZZ = 'Major.Effective_Length'
KEY_DISP_EFF_LEN_ZZ = 'Effective Length (m)'
KEY_EFF_LEN_YY = 'MinorEffLen'
KEY_DISP_EFF_LEN_YY = 'Effective Length (m)'
KEY_EULER_BUCKLING_STRESS_ZZ = 'MajorBucklingStress'
KEY_DISP_EULER_BUCKLING_STRESS_ZZ = 'Euler Buckling Stress (MPa)'
KEY_EULER_BUCKLING_STRESS_YY = 'MinorBucklingStress'
KEY_DISP_EULER_BUCKLING_STRESS_YY = 'Euler Buckling Stress (MPa)'
KEY_BUCKLING_CURVE_ZZ = 'MajorBC'
KEY_DISP_BUCKLING_CURVE_ZZ = 'Buckling Curve Classification'
KEY_BUCKLING_CURVE_YY = 'MinorBC'
KEY_DISP_BUCKLING_CURVE_YY = 'Buckling Curve Classification'
KEY_IMPERFECTION_FACTOR_ZZ = 'MajorIF'
KEY_DISP_IMPERFECTION_FACTOR_ZZ = 'Imperfection Factor'
KEY_IMPERFECTION_FACTOR_YY = 'MinorIF'
KEY_DISP_IMPERFECTION_FACTOR_YY = 'Imperfection Factor'
KEY_SR_FACTOR_ZZ = 'MajorSRF'
KEY_DISP_SR_FACTOR_ZZ = 'Stress Reduction Factor'
KEY_SR_FACTOR_YY = 'MinorSRF'
KEY_DISP_SR_FACTOR_YY = 'Stress Reduction Factor'
KEY_NON_DIM_ESR_ZZ = 'MajorNDESR'
KEY_DISP_NON_DIM_ESR_ZZ = 'Non-dimensional Effective SR (z-z)'
KEY_NON_DIM_ESR_YY = 'MinorNDESR'
KEY_DISP_NON_DIM_ESR_YY = 'Non-dimensional Effective SR (y-y)'
KEY_EFF_SEC_AREA_ZZ = 'MajorEffSecArea'
KEY_DISP_EFF_SEC_AREA_ZZ = 'Effective Sectional Area (mm2)'
KEY_EFF_SEC_AREA_YY = 'MinorEffSecArea'
KEY_DISP_EFF_SEC_AREA_YY = 'Effective Sectional Area (mm2)'
KEY_COMP_STRESS_ZZ = 'MajorDCS'
KEY_DISP_COMP_STRESS_ZZ = 'Design Compressive Stress (MPa)'
KEY_COMP_STRESS_YY = 'MinorDCS'
KEY_DISP_COMP_STRESS_YY = 'Design Compressive Stress (MPa)'
KEY_DISP_DESIGN_STRENGTH_YY = 'Pd (kN)'
KEY_DISP_DESIGN_STRENGTH_ZZ = 'Pd (kN)'
KEY_DESIGN_STRENGTH_YY = 'DesignStrength.y-y'
KEY_DESIGN_STRENGTH_ZZ = 'DesignStrength.z-z'
##Strut Design
###################################
KEY_SHEAR_STRENGTH = 'Shear.Strength'
KEY_SHEAR_STRENGTH_YY = 'Shear.Strength_YY'
KEY_SHEAR_STRENGTH_ZZ = 'Shear.Strength_ZZ'
KEY_MOMENT_STRENGTH = 'Moment.Strength'
KEY_MOMENT_STRENGTH_YY = 'Moment.Strength_YY'
KEY_MOMENT_STRENGTH_ZZ = 'Moment.Strength_ZZ'
KEY_DISP_HIGH_SHEAR= 'High Shear Check'
KEY_DISP_HIGH_SHEAR_YY= 'High Shear Check (y-y)'
KEY_DISP_HIGH_SHEAR_ZZ= 'High Shear Check (z-z)'
KEY_HIGH_SHEAR = 'Shear.High'
KEY_HIGH_SHEAR_YY = 'Shear.High_YY'
KEY_HIGH_SHEAR_ZZ = 'Shear.High_ZZ'
KEY_DISP_DESIGN_STRENGTH_SHEAR = 'Shear Strength (kN)' # Design 
KEY_DISP_DESIGN_STRENGTH_SHEAR_YY = 'Shear Strength (y-y) (kN)'
KEY_DISP_DESIGN_STRENGTH_SHEAR_ZZ = 'Shear Strength (z-z) (kN)'
KEY_DISP_DESIGN_STRENGTH_MOMENT = 'Moment Strength (kNm)' # Design
KEY_DISP_DESIGN_STRENGTH_MOMENT_YY = 'Moment Strength (y-y) (kNm)'
KEY_DISP_DESIGN_STRENGTH_MOMENT_ZZ = 'Moment Strength (z-z) (kNm)'
KEY_DISP_REDUCE_STRENGTH_MOMENT = 'Reduced Moment Strength (kNm)'
KEY_EULER_BUCKLING_STRESS = 'MajorBucklingStress'
KEY_DISP_EULER_BUCKLING_STRESS = 'Buckling Stress (MPa)' # Euler 
KEY_EFF_SEC_AREA = 'MajorEffSecArea'
KEY_DISP_EFF_SEC_AREA = 'Eff. Sectional Area (mm<sup>2</sup>)' # ective
KEY_EFF_LEN = 'Major.Effective_Length'
KEY_DISP_EFF_LEN = 'Eff. Length (m)' # ective
KEY_BUCKLING_CURVE = 'BucklingCurve'
KEY_DISP_BUCKLING_CURVE = 'Buckling Curve' #  Classification
KEY_IMPERFECTION_FACTOR = 'ImperfectionFactor'
KEY_DISP_IMPERFECTION_FACTOR = 'Imperfection' # Factor
KEY_SR_FACTOR = 'StressReductionFactor'
KEY_DISP_SR_FACTOR = 'Stress Reduction' # Factor
KEY_NON_DIM_ESR = 'NDESR'
KEY_DISP_NON_DIM_ESR = 'ND Eff. Senderness'
KEY_ALLOW_CLASS = 'Optimum.Class'
KEY_DISP_CLASS = 'Semi-compact sections'
DISP_TITLE_STRUT_SECTION = 'Section Details'
KEY_ALLOW_LOAD = 'Load.Type'
KEY_DISP_LOAD = 'Type of Load'
KEY_DISP_ESR = 'Effective SR'
KEY_ESR = 'ESR'
KEY_SR_lambdavv = 'ESRLambdavv'
KEY_DISP_SR_lambdavv = 'Lambda v-v'
KEY_SR_lambdapsi = 'ESRLambdapsi'
KEY_DISP_SR_lambdapsi = 'Lambda psi'
Buckling_Type = 'Type of Buckling'
End_Connection_title = 'End Connection Details'
KEY_COMP_STRESS = 'MinorDCS'
KEY_DISP_COMP_STRESS = 'Compressive Stress (MPa)'

KEY_Buckling_Out_plane = ' Out_of_Plane'
KEY_Buckling_In_plane =  ' In_Plane'
Buckling_Out_plane = ' Out of Plane'
Buckling_In_plane =  ' In Plane'
Load_type1 = 'Concentric Load'
Load_type2 = 'Leg Load'
Strut_load = list((Load_type1, Load_type2))
IMG_STRUT_1 = str(files("osdag.data.ResourceFiles.images").joinpath("bA.png"))
IMG_STRUT_2 = str(files("osdag.data.ResourceFiles.images").joinpath("bBBA.png"))
IMG_STRUT_3 = str(files("osdag.data.ResourceFiles.images").joinpath("back_back_same_side_angles.png"))
VALUES_IMG_STRUT = list(( IMG_STRUT_1, IMG_STRUT_2, IMG_STRUT_3))
KEY_BOLT_Number = 'Bolt.Number'
Strut_Bolt_Number = 'Number of Bolts'
Profile_name_1 = 'Angles'
Profile_name_2 = 'Back to Back Angles - Same side of gusset'
Profile_name_3 = 'Back to Back Angles - Opposite side of gusset'
loc_type1 = 'Long Leg'
loc_type2 = 'Short Leg'
VALUES_SEC_PROFILE_Compression_Strut = list((Profile_name_1, Profile_name_2, Profile_name_3)) #other sections can be added later the elements and not before 'Star Angles', 'Channels', 'Back to Back Channels'
Profile_2_img1 = str(files("osdag.data.ResourceFiles.images").joinpath("bblssg_eq.png")) # Back to back Long leg on same side of gusset for equal angle
Profile_2_img2 = str(files("osdag.data.ResourceFiles.images").joinpath("bbsssg_eq.png"))# Back to back short leg on same side of gusset for equal angle
Profile_2_img3 = str(files("osdag.data.ResourceFiles.images").joinpath("bblssg_ueq.png"))# Back to back Long leg on same side of gusset for unequal angle
Profile_2_img4 = str(files("osdag.data.ResourceFiles.images").joinpath("bbsssg_ueq.png"))# Back to back short leg on same side of gusset for unequal angle

KEY_ALLOW_CLASS1 = 'Optimum.Class1'
KEY_DISP_CLASS1 = 'Choose Plastic sections'
KEY_ALLOW_CLASS2 = 'Optimum.Class2'
KEY_DISP_CLASS2 = 'Choose Compact sections'
KEY_ALLOW_CLASS3 = 'Optimum.Class3'
KEY_DISP_CLASS3 = 'Choose Semi-compact sections'
KEY_ALLOW_CLASS4 = 'Optimum.Class4'
KEY_DISP_CLASS4 = 'Choose Slender sections'
KEY_ALLOW_UR = 'Optimum.AllowUR'
KEY_DISP_UR = 'Allowable Utilization Ratio (UR)'
KEY_OPTIMIZATION_PARA = 'Optimum.Para'
KEY_DISP_OPTIMIZATION_PARA = 'Optimization Parameter'
KEY_EFFECTIVE_AREA_PARA = 'Effective.Area_Para'
KEY_DISP_EFFECTIVE_AREA_PARA = 'Effective Area Parameter'
KEY_DISP_SECTION_DEFINITION_DP = 'Section Definition (Table 2)'
KEY_DISP_OPTIMIZATION_STEEL_COST = 'Cost'
KEY_STEEL_COST = 'Steel.Cost'
KEY_DISP_STEEL_COST = 'Steel cost (INR / per kg)'

###################################
#Flexure Members
###################################
KEY_Plastic = "Plastic"
KEY_Compact = "Compact"
KEY_SemiCompact = "Semi-Compact"
KEY_Flexure_Member_MAIN_MODULE = 'Flexure Member'
KEY_DISP_FLEXURE = 'Flexural Members - Simply Supported'
KEY_DISP_FLEXURE2 = 'Flexural Members - Cantilever'
KEY_DISP_FLEXURE3 = 'Flexural Members'
KEY_DISP_FLEXURE4 = 'Flexural Members - Purlins'

KEY_DISP_PLASTIC_STRENGTH_MOMENT = 'Plastic Strength (kNm)'
KEY_DISP_Bending_STRENGTH_MOMENT = 'Bending Strength (kNm)'
KEY_DISP_LTB_Bending_STRENGTH_MOMENT = 'Lateral Torsional Buckling Strength (kNm)'

KEY_DISP_betab_constatnt= 'Beta<sub>b</sub>'
KEY_betab_constatnt= 'Beta.Constant'
KEY_BUCKLING_STRENGTH= 'Buckling.Strength'
KEY_DISP_BUCKLING_STRENGTH= 'Buckling Strength (kN)'
KEY_WEB_CRIPPLING= 'Crippling.Strength'
KEY_DISP_CRIPPLING_STRENGTH = 'Crippling Strength (kN)'
KEY_DISP_LTB= 'Lateral Torsional Buckling Details'
KEY_DISP_Elastic_CM= 'Critical Moment (M<sub>cr</sub>)'# Elastic
KEY_DISP_Elastic_CM_YY= 'Critical Moment (y-y) (M<sub>cr</sub>)'
KEY_DISP_Elastic_CM_ZZ= 'Critical Moment (z-z) (M<sub>cr</sub>)'
KEY_DISP_Elastic_CM_latex= 'Elastic Critical Moment(kNm)' #
KEY_DISP_T_constatnt= 'Torsional Constant (mm<sup>4</sup>)' #  (I<sub>t</sub>)
KEY_DISP_W_constatnt= 'Warping Constant (mm<sup>6</sup>)' # (I<sub>w</sub>)
KEY_LTB= 'L.T.B.Details'
KEY_Elastic_CM= 'Elastic.Moment'
KEY_Elastic_CM_YY = 'Elastic.Moment_YY'
KEY_Elastic_CM_ZZ = 'Elastic.Moment_ZZ'
KEY_T_constatnt= 'T.Constant'
KEY_W_constatnt= 'W.Constant'
KEY_IMPERFECTION_FACTOR_LTB = 'Imperfection.LTB'
KEY_SR_FACTOR_LTB = 'SR.LTB'
KEY_NON_DIM_ESR_LTB = 'NDESR.LTB'
# KEY_LTB= 'Lateral Torsional Buckling Details'
KEY_WEB_BUCKLING= 'Web Buckling Details'
KEY_WEB_RESISTANCE= 'Web Resistance Details'
KEY_BEARING_LENGTH = 'Bearing.Length'
Simply_Supported_img = str(files("osdag.data.ResourceFiles.images").joinpath("ss_beam.png"))
Cantilever_img = str(files("osdag.data.ResourceFiles.images").joinpath("c_beam.png"))
Purlin_img = str(files("osdag.data.ResourceFiles.images").joinpath("purlin.jpg"))
KEY_LENGTH_OVERWRITE = 'Length.Overwrite'
KEY_DISPP_LENGTH_OVERWRITE = 'Effective Length Parameter'
KEY_DISP_BEAM_MOMENT = 'Bending Moment (kNm)(M<sub>z-z</sub>)'
KEY_DISP_BEAM_MOMENT_Latex = 'Bending Moment (kNm)' # ($M_{z-z}$)
KEY_SUPP_TYPE = 'Member.Type'
DISP_TITLE_ISECTION = 'I Sections'
KEY_DISP_CLADDING = 'Cladding (For Deflection)'

#Web Resistance Values
KEY_BENDING_COMPRESSIVE_STRESS_YY = 'Resistance.Bending_Cmp_Stress_yy'
KEY_BENDING_COMPRESSIVE_STRESS_ZZ = 'Resistance.Bending_Cmp_Stress_zz'
KEY_DISP_BENDING_COMPRESSIVE_STRESS_YY = 'Bending Compressive Stress (y-y)'
KEY_DISP_BENDING_COMPRESSIVE_STRESS_ZZ = 'Bending Compressive Stress (z-z)'
KEY_BENDING_STRESS_RF_YY = 'Resistance.Bending_Stress_RF_yy'
KEY_BENDING_STRESS_RF_ZZ = 'Resistance.Bending_Stress_RF_zz'
KEY_DISP_BENDING_STRESS_RF_YY = 'Bending Stress Reduction Factor (y-y)'
KEY_DISP_BENDING_STRESS_RF_ZZ = 'Bending Stress Reduction Factor (z-z)'
KEY_RESISTANCE_MOMENT_YY = 'Resistance.Moment_YY'
KEY_RESISTANCE_MOMENT_ZZ = 'Resistance.Moment_ZZ'
KEY_DISP_RESISTANCE_MOMENT_YY = 'Moment (y-y)'
KEY_DISP_RESISTANCE_MOMENT_ZZ = 'Moment (z-z)'
KEY_BUCKLING_CLASS = "Buckling Class"
KEY_DISP_BUCKLING_CLASS = "Buckling Class"

KEY_DISP_DESIGN_TYPE_FLEXURE = 'Laterally Supported'
KEY_DESIGN_TYPE_FLEXURE = 'Flexure.Type'
KEY_BEAM_SUPP_TYPE = 'Support Type'
KEY_BEAM_SUPP_TYPE_DESIGN = 'Design Support Type'
KEY_DISP_DESIGN_TYPE2_FLEXURE = 'Laterally Unsupported'
KEY_DESIGN_TYPE2_FLEXURE = 'Laterally.Unsupported'
KEY_DISP_BENDING = 'Axis of Bending'
KEY_DISP_BENDING1 = 'Major'
KEY_DISP_BENDING2 = 'Minor'
VALUES_BENDING_TYPE = list((KEY_DISP_BENDING2, KEY_DISP_BENDING1))
VALUES_SUPP_TYPE = list((KEY_DISP_DESIGN_TYPE_FLEXURE, KEY_DISP_DESIGN_TYPE2_FLEXURE)) #[KEY_DISP_DESIGN_TYPE_FLEXURE, KEY_DISP_DESIGN_TYPE2_FLEXURE]
VALUES_SUPP_TYPE_temp = list((KEY_DISP_BENDING1 + " " + KEY_DISP_DESIGN_TYPE_FLEXURE, KEY_DISP_BENDING2 + " " + KEY_DISP_DESIGN_TYPE2_FLEXURE, KEY_DISP_BENDING1 + " " + KEY_DISP_DESIGN_TYPE2_FLEXURE)) #[KEY_DISP_DESIGN_TYPE_FLEXURE, KEY_DISP_DESIGN_TYPE2_FLEXURE]
KEY_BENDING = 'Bending.type'
KEY_SUPPORT = 'Flexure.Support'
KEY_DISP_SUPPORT = 'End Conditions'
KEY_DISP_SUPPORT1 = 'Simply Supported'
KEY_DISP_SUPPORT2 = 'Cantilever'
KEY_DISP_SUPPORT3 = 'Purlins'
KEY_DISP_SUPPORT_LIST = list((KEY_DISP_SUPPORT1, KEY_DISP_SUPPORT2, KEY_DISP_SUPPORT3)) #[KEY_DISP_SUPPORT1, KEY_DISP_SUPPORT2]
# KEY_SUPPORT1 = 'SimpSupport.Torsional'
# KEY_SUPPORT2 = 'SimpSupport.Warping'
KEY_CLADDING_TYPE1 = 'Brittle Cladding'
KEY_CLADDING_TYPE2 = 'Elastic Cladding'
KEY_CLADDING = 'Cladding.type'
VALUES_CLADDING = list((KEY_CLADDING_TYPE1, KEY_CLADDING_TYPE2))
KEY_DISP_LENGTH_BEAM = 'Effective Span (m)*'
KEY_LOAD = 'Loading.Condition'
KEY_DISP_LOAD = 'Loading Condition'
KEY_DISP_LOAD1 ='Normal'
KEY_DISP_LOAD2 = 'Destabilizing'
KEY_DISP_LOAD_list = list((KEY_DISP_LOAD1, KEY_DISP_LOAD2))
KEY_TORSIONAL_RES = 'Torsion.restraint'
DISP_TORSIONAL_RES = 'Torsional restraint'
Torsion_Restraint1 = 'Fully Restrained'
Torsion_Restraint2 = 'Partially Restrained-support connection'
Torsion_Restraint3 = 'Partially Restrained-bearing support'
Torsion_Restraint_list = list(( Torsion_Restraint1, Torsion_Restraint2, Torsion_Restraint3))
KEY_WARPING_RES = 'Warping.restraint'
DISP_WARPING_RES = 'Warping restraint'
Warping_Restraint1 = 'Both flanges fully restrained'
Warping_Restraint2 = 'Compression flange fully restrained'
# Warping_Restraint3 = 'Both flanges fully restrained'
Warping_Restraint4 = 'Compressicm flange partially restrained'
Warping_Restraint5 = 'Warping not restrained in both flanges'
Warping_Restraint_list = list(( Warping_Restraint1, Warping_Restraint2, Warping_Restraint4, Warping_Restraint5))
DISP_SUPPORT_RES = 'Support restraint'
KEY_SUPPORT_TYPE = 'Cantilever.Support'
Support1 = 'Continous, with lateral restraint to top flange'
Support2 = 'Continous, with partial torsional restraint'
Support3 = 'Continous, with lateral and torsional restraint'
Support4 = 'Restrained laterally, torsionally and against rotation on flange'
Supprt_Restraint_list = list(( Support1, Support2, Support3, Support4))
DISP_TOP_RES = 'Top restraint'
KEY_SUPPORT_TYPE2 = 'Cantilever.Top'
Top1 = 'Free'
Top2 = 'Lateral restraint to top flange'
Top3 = 'Torsional rwstraint'
Top4 = 'Lateral and Torsional restraint'
Top_Restraint_list = list(( Top1, Top2, Top3, Top4))
KEY_WEB_BUCKLING_option = ['Method A','Method B']
KEY_BUCKLING_METHOD = 'Buckling.Method'
KEY_ShearBuckling = 'Shear Buckling Design Method '
KEY_ShearBucklingOption = 'S.B.Methods'
KEY_DISP_SB_Option = ['Simple Post Critical', 'Tension Field Test']
KEY_DISP_TENSION_HOLES = 'Tension Zone'
KEY_DISP_Web_Buckling = 'Web Buckling'
KEY_DISP_Utilization_Ratio = 'Utilization Ratio'
KEY_DISP_Web_Buckling_Support = 'Web Buckling @Support'
KEY_DISP_I_eff_latex = '$I_{eff}$web'
KEY_DISP_A_eff_latex = '$A_{eff}$web'
KEY_DISP_r_eff_latex = '$r_{eff}$web'
KEY_DISP_K_v_latex = '$K_{v}$'
KEY_DISP_Elastic_Critical_shear_stress_web = 'Elastic Critical Shear Stress Web($N/mm^2$)' #(\tau_{crc})
KEY_DISP_Transverse_Stiffener_spacing = 'Spacing of Transverse Stiffeners(c)(mm)'
KEY_DISP_slenderness_ratio_web = 'Web Slenderness ratio($\lambda_w$)'
KEY_DISP_BUCKLING_STRENGTH= 'Buckling Resistance (kN)'
KEY_DISP_reduced_moment= 'Reduced moment (Nmm)'
# KEY_DISP_reduced_moment= 'Reduced moment (N_f)'
KEY_DISP_tension_field_incline= 'Tension field inclination($\phi$)'
KEY_DISP_Yield_Strength_Tension_field = 'Yield Strength of Tension field(f_v)($N/mm^2$)'
KEY_DISP_AnchoragelengthTensionField= 'Anchorage length of Tension Field(s)(mm)'
KEY_DISP_WidthTensionField= 'Width of Tension Field($w_{tf}$)'

###################################
# Plate Girder
###################################
KEY_PLATE_GIRDER_MAIN_MODULE = 'PLATE GIRDER'
KEY_DISP_PLATE_GIRDER_WELDED = 'PLATE GIRDER - WELDED'
KEY_tf = 'TF.Data'
KEY_tw = 'TW.Data'
KEY_dw = 'DW.Data'
KEY_bf = 'BF.Data'
KEY_DISP_tf = 'Flange Thickness(mm)'
KEY_DISP_tw = 'Web Thickness(mm)'
KEY_DISP_dw = 'Web Depth(mm)'
KEY_DISP_bf = 'Flange Width(mm)'
KEY_IntermediateStiffener = 'IntermediateStiffener.Data'
KEY_DISP_IntermediateStiffener = 'Intermediate Stiffener'
KEY_DISP_Plate_Girder_PROFILE = 'Section Profile'
KEY_IntermediateStiffener_spacing = 'IntermediateStiffener.Spacing'
KEY_DISP_IntermediateStiffener_spacing = 'Intermediate Stiffener Spacing'
###################################
# All Input Keys
###################################
KEY_MODULE = 'Module'
KEY_CONN = 'Connectivity'
KEY_TABLE = 'Table'
KEY_MEMBERS = 'No of Members'
KEY_LOCATION = 'Conn_Location'
KEY_ENDPLATE_TYPE = 'EndPlateType'
KEY_MATERIAL = 'Material'
KEY_MATERIAL_ST_SK = 'Material'
KEY_MATERIAL_FU = 'Material.Fu'
KEY_MATERIAL_FY = 'Material.Fy'


KEY_SEC_MATERIAL = 'Member.Material'
KEY_SEC_FU = 'Member.Fu'    #Extra Keys
KEY_SEC_FY = 'Member.Fy'    #Extra Keys

KEY_SECSIZE = 'Member.Designation'
KEY_SECSIZE_DP = 'Member.Designation_dp'
KEY_SECSIZE_SELECTED = 'Member.Designation_Selected'        #Extra Keys for Display
KEY_SUPTNGSEC = 'Member.Supporting_Section.Designation'
KEY_COLUMN_SECTION = 'Member.Column_Section.Designation'
KEY_SUPTNGSEC_MATERIAL = 'Member.Supporting_Section.Material'
KEY_A = 'Member.A'
KEY_B = 'Member.B'


KEY_SUPTDSEC_FU = 'Member.Supported_Section.Fu'     #Extra Keys for DP Display
KEY_SUPTDSEC_FY = 'Member.Supported_Section.Fy'     #Extra Keys for DP Display

KEY_SUPTDSEC = 'Member.Supported_Section.Designation'
KEY_SUPTDSEC_MATERIAL = 'Member.Supported_Section.Material'
KEY_SUPTNGSEC_FU = 'Member.Supporting_Section.Fu'   #Extra Keys for DP Display
KEY_SUPTNGSEC_FY = 'Member.Supporting.Section.Fy'   #Extra Keys for DP Display

KEY_LENGTH = 'Member.Length'
KEY_SEC_PROFILE = 'Member.Profile'
KEY_SEC_TYPE = 'Member.Type'

KEY_SHEAR = 'Load.Shear'
KEY_SHEAR_YY = 'Load.Shear.YY'
KEY_SHEAR_ZZ = 'Load.Shear.ZZ'
KEY_AXIAL = 'Load.Axial'
KEY_MOMENT = 'Load.Moment'
KEY_MOMENT_YY = 'Load.Moment_YY'
KEY_MOMENT_ZZ = 'Load.Moment_ZZ'

KEY_D = 'Bolt.Diameter'
KEY_TYP = 'Bolt.Type'
KEY_COF = 'Bolt.Coefficient'
KEY_GRD = 'Bolt.Grade'

# KEY_DP_BOLT_MATERIAL_G_O = 'Bolt.Material_Grade_OverWrite'
KEY_DP_BOLT_HOLE_TYPE = 'Bolt.Bolt_Hole_Type'
KEY_DP_BOLT_TYPE = 'Bolt.TensionType'
KEY_DP_BOLT_SLIP_FACTOR = 'Bolt.Slip_Factor'

KEY_CONNECTOR_MATERIAL = 'Connector.Material'
KEY_CONNECTOR_FU = 'Connector.Fu'               #Extra Keys for DP Display
KEY_CONNECTOR_FY = 'Connector.Fy'               #Extra Keys for DP Display
KEY_CONNECTOR_FY_20 = 'Connector.Fy_20'         #Extra Keys for DP Display
KEY_CONNECTOR_FY_20_40 = 'Connector.Fy_20_40'   #Extra Keys for DP Display
KEY_CONNECTOR_FY_40 = 'Connector.Fy_40'         #Extra Keys for DP Display
KEY_CONNECTOR_GUSSET = 'Connector.GUSSET'         #Extra Keys for DP Display


KEY_PLATETHK = 'Connector.Plate.Thickness_List'
KEY_FLANGEPLATE_PREFERENCES = 'Connector.Flange_Plate.Preferences'
KEY_FLANGEPLATE_THICKNESS = 'Connector.Flange_Plate.Thickness_list'
KEY_WEBPLATE_THICKNESS = 'Connector.Web_Plate.Thickness_List'
KEY_ANGLE_LIST='Connector.Angle_List'
KEY_ANGLE_SELECTED = 'Connector.Angle_Selected'
KEY_SEATEDANGLE = 'Connector.Seated_Angle_List'
KEY_TOPANGLE = 'Connector.Top_Angle'
KEY_DISP_ANGLE_LIST = 'Seated Angle List'
KEY_DISP_CLEAT_ANGLE_LIST = 'Cleat Angle List'
KEY_DISP_TOPANGLE_LIST = 'Top Angle List'

KEY_MOMENT_MAJOR = 'Load.Moment.Major'
KEY_MOMENT_MINOR = 'Load.Moment.Minor'
KEY_ANCHOR_OCF = 'Anchor Bolt.OCF'
KEY_DISP_ANCHOR_OCF = 'Anchor Bolt Outside Column Flange'
KEY_ANCHOR_ICF = 'Anchor Bolt.ICF'
KEY_DISP_ANCHOR_ICF = 'Anchor Bolt Inside Column Flange'
KEY_DISP_ANCHOR_GENERAL = 'General'
KEY_DIA_ANCHOR_OCF = 'Anchor Bolt.OCF.Diameter'
KEY_DIA_ANCHOR_ICF = 'Anchor Bolt.ICF.Diameter'
KEY_TYP_ANCHOR = 'Anchor Bolt.Type'
KEY_GRD_ANCHOR_OCF = 'Anchor Bolt.OCF.Grade'
KEY_GRD_ANCHOR_ICF = 'Anchor Bolt.ICF.Grade'
KEY_GRD_FOOTING = 'Footing.Grade'


KEY_DP_WELD_FAB = 'Weld.Fab'
KEY_DP_WELD_MATERIAL_G_O = 'Weld.Material_Grade_OverWrite'
KEY_DP_WELD_TYPE = 'Weld.Type'

KEY_DP_DETAILING_EDGE_TYPE = 'Detailing.Edge_type'
KEY_DP_DETAILING_GAP = 'Detailing.Gap'
KEY_DP_DETAILING_CORROSIVE_INFLUENCES = 'Detailing.Corrosive_Influences'

KEY_DP_DESIGN_METHOD = 'Design.Design_Method'

###################
# Value Keys
###################

RED_LIST = [KEY_SUPTNGSEC, KEY_SUPTDSEC, KEY_SECSIZE]
VALUES_CONN_SPLICE = ['Coplanar Tension-Compression Flange', 'Coplanar Tension Flange', 'Coplanar Compression Flange']
CONN_CFBW = 'Column Flange-Beam Web'
CONN_CWBW = 'Column Web-Beam Web'
VALUES_CONN_1 = [CONN_CFBW, CONN_CWBW]
VALUES_CONN_2 = ['Beam-Beam']
VALUES_CONN_3 = ['Flush End Plate', 'Extended Both Ways']
VALUES_CONN = VALUES_CONN_1 + VALUES_CONN_2
VALUES_ENDPLATE_TYPE = ['Flushed - Reversible Moment', 'Extended One Way - Irreversible Moment', 'Extended Both Ways - Reversible Moment']
# VALUES_CONN_BP = ['Welded Column Base', 'Welded+Bolted Column Base', 'Moment Base Plate', 'Hollow/Tubular Column Base']
VALUES_CONN_BP = ['Welded Column Base', 'Moment Base Plate', 'Hollow/Tubular Column Base']
VALUES_LOCATION = ['Select Location','Long Leg', 'Short Leg', 'Web']

# TODO: Every one is requested to use VALUES_ALL_CUSTOMIZED key instead of all other keys
VALUES_ALL_CUSTOMIZED = ['All', 'Customized']
VALUES_ENDPLATE_THICKNESS = ['All', 'Customized']
VALUES_DIA_ANCHOR = ['All', 'Customized']
VALUES_GRD_ANCHOR = ['All', 'Customized']
VALUES_D = ['All', 'Customized']
VALUES_GRD = ['All', 'Customized']
VALUES_PLATETHK = ['All', 'Customized']
VALUES_FLANGEPLATE_THICKNESS = ['All', 'Customized']
VALUES_WEBPLATE_THICKNESS = ['All', 'Customized']
VALUES_ANGLESEC= ['All', 'Customized']
VALUES_TRUSSBOLT_THK = ['8', '10', '12', '14', '16']

VALUES_MEMBERS = ['2', '3', '4', '5', '6', '7', '8']
ALL_WELD_SIZES = [3, 4, 5, 6, 8, 10, 12, 14, 16]
VALUES_TYP_ANCHOR = ['End Plate Type', 'IS 5624-Type A', 'IS 5624-Type B']
VALUES_GRD_FOOTING = ['Select Grade', 'M10', 'M15', 'M20', 'M25', 'M30', 'M35', 'M40', 'M45', 'M50', 'M55']
VALUES_TYP = [TYP_BEARING, TYP_FRICTION_GRIP]
TYP_FRICTION_GRIP = 'Friction Grip Bolt'
TYP_BEARING = 'Bearing Bolt'

# VALUES_GRD_CUSTOMIZED = ['3.6', '4.6', '4.8', '5.6', '5.8', '6.8', '8.8', '9.8', '10.9', '12.9']
VALUES_GRD_CUSTOMIZED = IS1367_Part3_2002.get_bolt_PC()

# standard as per IS 1730:1989
PLATE_THICKNESS_IS_1730_1989 = ['5', '6', '7', '8', '10', '12', '14', '16', '18', '20', '22', '25', '28', '32', '36', '40', '45', '50', '56', '63']
# standard as per SAIL's product brochure
PLATE_THICKNESS_SAIL = ['8', '10', '12', '14', '16', '18', '20', '22', '25', '28', '32', '36', '40', '45', '50', '56', '63', '75', '80', '90', '100',
                        '110', '120']

VALUES_PLATETHICKNESS_CUSTOMIZED = PLATE_THICKNESS_SAIL
VALUES_PLATETHK_CUSTOMIZED = PLATE_THICKNESS_SAIL
VALUES_ENDPLATE_THICKNESS_CUSTOMIZED = PLATE_THICKNESS_SAIL
VALUES_COLUMN_ENDPLATE_THICKNESS_CUSTOMIZED = PLATE_THICKNESS_SAIL

# TODO: delete the below list (commented) after verification
# VALUES_PLATETHK_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24','25', '26', '28', '30','32','36','40','45','50','56','63','80']
# VALUES_ENDPLATE_THICKNESS_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30']
# VALUES_COLUMN_ENDPLATE_THICKNESS_CUSTOMIZED = VALUES_ENDPLATE_THICKNESS_CUSTOMIZED[3:12] + ['25','28','32','36','40','45','50','56','63','80']



VALUES_FLANGEPLATE_PREFERENCES = ['Outside','Outside + Inside']
VALUES_LOCATION_1 = ['Long Leg', 'Short Leg']
VALUES_LOCATION_2 = ["Web"]
VALUES_SECTYPE = ['Select Type','Beams and Columns','Columns','Angles','Back to Back Angles','Star Angles','Channels','Back to back Channels']

VALUES_CONNLOC_BOLT = ['Bolted','Web','Flange','Leg','Back to Back Web','Back to Back Angles','Star Angles']
VALUES_CONNLOC_WELD = ['Welded','Web','Flange','Leg','Back to Back Web','Back to Back Angles','Star Angles']
VALUES_DIAM = connectdb("Bolt")
# VALUES_DIAM = ['Select diameter','12','16','20','24','30','36']


VALUES_IMG_TENSIONBOLTED = [str(files("osdag.data.ResourceFiles.images").joinpath("bA.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bBBA.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bSA.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bC.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bBBC.png"))]
VALUES_IMG_TENSIONWELDED = [str(files("osdag.data.ResourceFiles.images").joinpath("wA.png")),str(files("osdag.data.ResourceFiles.images").joinpath("wBBA.png")),str(files("osdag.data.ResourceFiles.images").joinpath("wSA.png")),str(files("osdag.data.ResourceFiles.images").joinpath("wC.png")),str(files("osdag.data.ResourceFiles.images").joinpath("wBBC.png"))]
VALUES_IMG_TENSIONBOLTED_DF01 = [str(files("osdag.data.ResourceFiles.images").joinpath("equaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bblequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bbsequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("salequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("sasequaldp.png"))]
VALUES_IMG_TENSIONBOLTED_DF02 = [str(files("osdag.data.ResourceFiles.images").joinpath("unequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bblunequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("bbsunequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("salunequaldp.png")),str(files("osdag.data.ResourceFiles.images").joinpath("sasunequaldp.png"))]

VALUES_IMG_TENSIONBOLTED_DF03 = [str(files("osdag.data.ResourceFiles.images").joinpath("Slope_Channel.png")),str(files("osdag.data.ResourceFiles.images").joinpath("Parallel_Channel.png")),str(files("osdag.data.ResourceFiles.images").joinpath("Slope_BBChannel.png")),str(files("osdag.data.ResourceFiles.images").joinpath("Parallel_BBChannel.png"))]

VALUES_IMG_BEAM = [str(files("osdag.data.ResourceFiles.images").joinpath("Slope_Beam.png")),str(files("osdag.data.ResourceFiles.images").joinpath("Parallel_Beam.png"))]
VALUES_IMG_HOLLOWSECTION = [str(files("osdag.data.ResourceFiles.images").joinpath("SHS.png")),str(files("osdag.data.ResourceFiles.images").joinpath("RHS.png")),str(files("osdag.data.ResourceFiles.images").joinpath("CHS.png"))]

VALUES_BEAMSEC = connectdb("Beams")
VALUES_SECBM = connectdb("Beams")
VALUES_COLSEC = connectdb("Columns")
VALUES_MATERIAL = connectdb("Material")
VALUES_MATERIAL_SELECTED = "E 250 (Fe 410 W)A"
VALUES_PRIBM = connectdb("Beams")


############################
# Display Keys (Input Dock, Output Dock, Design preference, Design report)
############################

KEY_DISP_SHEAR_YLD = 'Shear Yielding Capacity (kN)'
KEY_DISP_SHEAR_RUP = 'Shear Rupture Capacity (kN)'
KEY_DISP_PLATE_BLK_SHEAR_SHEAR = 'Block Shear Capacity in Shear (kN)'
KEY_DISP_PLATE_BLK_SHEAR_TENSION = 'Block Shear Capacity in Tension (kN)'
KEY_DISP_SHEAR_CAPACITY = 'Shear Capacity (kN)'
KEY_DISP_BEARING_LENGTH = 'Bearing Length'
KEY_DISP_ALLOW_SHEAR = 'Allowable Shear Capacity (kN)'
DISP_LOWSHEAR = 'Limited to low shear capacity'

KEY_DISP_BLK_SHEAR = 'Block Shear Capacity (kN)'
KEY_DISP_MOM_DEMAND = 'Moment Demand (kNm)'
KEY_DISP_MOM_CAPACITY = 'Moment Capacity (kNm)'
DISP_MIN_PITCH = 'Min. Pitch Distance (mm)'
DISP_MAX_PITCH = 'Max. Pitch Distance (mm)'
DISP_MIN_GAUGE = 'Min. Gauge Distance (mm)'
DISP_MAX_GAUGE = 'Max. Gauge Distance (mm)'
DISP_CS_GAUGE = 'Cross-centre Gauge Distance (mm)'
DISP_MIN_EDGE = 'Min. Edge Distance (mm)'
KEY_SPACING = "Spacing Check"
DISP_MAX_EDGE = 'Max. Edge Distance (mm)'
DISP_MIN_END = 'Min. End Distance (mm)'
DISP_MAX_END = 'Max. End Distance (mm)'
DISP_MIN_PLATE_HEIGHT = 'Min. Plate Height (mm)'
DISP_MAX_PLATE_HEIGHT = 'Max. Plate Height (mm)'
DISP_MIN_PLATE_LENGTH = 'Min. Plate Length (mm)'
DISP_MAX_PLATE_WIDTH = 'Max. Plate Width (mm)'
DISP_MIN_PLATE_WIDTH = 'Min. Plate Width (mm)'
DISP_MIN_LEG_LENGTH = 'Min. Leg Length (mm)'
DISP_MIN_CLEAT_HEIGHT = 'Min. Cleat Angle Height'
DISP_MAX_CLEAT_HEIGHT = 'Max. Cleat Angle Height'
DISP_MIN_CLEAT_THK = 'Min. Cleat Angle Thickness (mm)'
DISP_MIN_WIDTH = 'Minimum Width (mm)'
DISP_MIN_PLATE_THICK = 'Min. Plate Thickness (mm)'

######### Minimun for Flange####
DISP_MIN_FLANGE_PLATE_HEIGHT = 'Min. Flange Plate Width (mm)'
DISP_MAX_FLANGE_PLATE_HEIGHT = 'Max. Flange Plate Width (mm)'
DISP_MIN_FLANGE_PLATE_LENGTH = 'Min. Flange Plate Length (mm)'
DISP_MIN_FLANGE_PLATE_THICK = 'Min. Flange Plate Thickness (mm)'

######### Minimun for Flange####
DISP_MIN_WEB_PLATE_HEIGHT = 'Min. Web Plate Height (mm)'
DISP_MAX_WEB_PLATE_HEIGHT = 'Max. Web Plate Height (mm)'
DISP_MIN_WEB_PLATE_LENGTH = 'Min. Web Plate Width (mm)'
DISP_MIN_WEB_PLATE_THICK = 'Min. Web Plate Thickness (mm)'




DISP_MIN_PLATE_INNERHEIGHT = 'Min. Inner Plate Width (mm)'
DISP_MAX_PLATE_INNERHEIGHT = 'Max. Inner Plate Width (mm)'
DISP_MIN_PLATE_INNERLENGTH = 'Min. Inner Plate Length (mm)'


KEY_DISP_FU = 'Ultimate Strength, Fu (MPa)'
KEY_DISP_FY = 'Yield Strength, Fy (MPa)'
KEY_DISP_IR = 'Interaction Ratio'
DISP_WELD_SIZE = 'Weld Size (mm)'
DISP_MIN_WELD_SIZE = 'Min. Weld Size (mm)'
DISP_MAX_WELD_SIZE = 'Max. Weld Size (mm)'
DISP_THROAT = 'Throat Thickness (mm)'
DISP_WEB_WELD_SIZE_REQ = 'Web Weld Size Required (mm)'

DISP_WELD_STRENGTH = 'Weld Strength (N/mm)'
DISP_WELD_STRENGTH_MPA = 'Weld Strength (N/mm2)'
KEY_DISP_FY_20 = 'Yield Strength, Fy (MPa) (0-20mm)'
KEY_DISP_FY_20_40 = 'Yield Strength, Fy (MPa) (20-40mm)'
KEY_DISP_FY_40 = 'Yield Strength, Fy (MPa) (>40mm)'
KEY_DISP_GUSSET = 'Gusset Plate'
KEY_GUSSET = 'Thickness (mm)'


DISP_TITLE_ANCHOR_BOLT = 'Anchor Bolt'
DISP_TITLE_ANCHOR_BOLT_OUTSIDE_CF = 'Anchor Bolt - Outside Column Flange'
DISP_TITLE_ANCHOR_BOLT = 'Anchor Bolt'
DISP_TITLE_FOOTING = 'Pedestal/Footing'

KEY_DISP_CONN = 'Connectivity'

KEY_DISP_ENDPLATE_TYPE = 'End Plate Type'
KEY_DISP_MEMBERS = 'No of Members'


# VALUES_CONN_BP = ['Welded-Slab Base', 'Bolted-Slab Base', 'Gusseted Base Plate', 'Hollow Section']

KEY_DISP_LENGTH = 'Length (mm) *'
KEY_DISP_LOCATION = 'Conn_Location *'
KEY_DISP_LOCATION_STRUT = 'Connection'
KEY_DISP_MATERIAL = 'Material'
KEY_DISP_SUPTNGSEC = 'Supporting Section'
KEY_DISP_SUPTNGSEC_REPORT = 'Supporting Section - Mechanical Properties'
KEY_DISP_COLSEC = 'Column Section *'
KEY_DISP_COLSEC_REPORT = 'Column Section'
KEY_DISP_PRIBM = 'Primary Beam *'
KEY_DISP_SUPTDSEC = 'Supported Section'
KEY_DISP_SUPTDSEC_REPORT = 'Supported Section - Mechanical Properties'
KEY_DISP_BEAMSEC = 'Beam Section *'
KEY_DISP_BEAMSEC_REPORT = 'Beam Section'
KEY_DISP_SECBM = 'Secondary Beam *'
DISP_TITLE_FSL = 'Factored Loads'
KEY_DISP_MOMENT = 'Bending Moment (kNm)'
KEY_DISP_MOMENT_ZZ = 'Bending Moment (z-z) (kNm)'
KEY_DISP_MOMENT_YY = 'Bending Moment (y-y) (kNm)'

KEY_DISP_TOP_ANGLE = 'Top Angle'

KEY_DISP_DIA_ANCHOR = 'Diameter(mm)'
DISP_TITLE_BOLT = 'Bolt'
DISP_TITLE_CRITICAL_BOLT = 'Critical Bolt Design'
DISP_TITLE_CRITICAL_BOLT_SHEAR = 'Critical Bolt - Shear Design'
DISP_TITLE_BOLT_CAPACITY = 'Bolt Capacity'

DISP_TITLE_FLANGESPLICEPLATE = 'Flange Splice Plate '
DISP_TITLE_FLANGESPLICEPLATE_OUTER = 'Outer Plate '
DISP_TITLE_FLANGESPLICEPLATE_INNER = 'Inner Plate '
KEY_DISP_SLENDER = 'Slenderness ratio'


KEY_DISP_PLATETHK = 'Thickness (mm)'
KEY_DISP_DPPLATETHK = 'Endplate thickness, T (mm)'
KEY_DISP_DPPLATETHK01 = 'Endplate thickness, Tp (mm)'

DISP_TITLE_TENSION = 'Tension Capacity'
KEY_DISP_FLANGESPLATE_PREFERENCES = 'Preference'
KEY_DISP_FLANGESPLATE_THICKNESS = 'Thickness (mm)'
KEY_DISP_INNERFLANGESPLATE_THICKNESS = 'Thickness (mm)'

DISP_TITLE_WELD = 'Weld'
DISP_TITLE_WELD_CAPACITY = 'Weld Capacity'
DISP_TITLE_END_CONNECTION = 'End Connection'
DISP_TITLE_WELD_DETAILS = 'Weld Details'
DISP_TITLE_CONN_DETAILS = 'Connection Details'


KEY_DISP_FLANGE_CAPACITY= 'Capacity'
KEY_DISP_FLANGE_PLATE_GAUGE ="Gauge Distance (mm)"
KEY_DISP_FLANGE_SPACING = 'Spacing (mm)'
KEY_DISP_END_DIST_FLANGE = 'End Distance'
KEY_DISP_EDGEDIST_FLANGE= 'Edge Distance (mm)'
KEY_DISP_FLANGE_PLATE_PITCH = 'Pitch Distance (mm)'

KEY_DISP_FLANGE_PLATE_TEN_CAP ="Flange Plate Tension Capacity (kN)"
DISP_TITLE_SECTION = 'Section Details'
DISP_TITLE_TENSION_SECTION = 'Section Details'
SECTION_CLASSIFICATION = "Section Classification"

KEY_DISP_D = 'Diameter (mm)'
KEY_DISP_SHEAR = 'Shear Force (kN)'
KEY_DISP_SHEAR_YY = 'Shear Force (y-y) (kN)'
KEY_DISP_SHEAR_ZZ = 'Shear Force (z-z) (kN)'
KEY_DISP_AXIAL = 'Axial Force (kN)'
KEY_DISP_AXIAL_STAR = 'Axial (kN)* '
DISP_TITLE_PLATE = 'Plate'
KEY_DISP_TYP = 'Type'
KEY_DISP_COF = 'Coefficient of friction'
KEY_DISP_TYP_ANCHOR = 'Anchor Type'
KEY_DISP_GRD_ANCHOR = 'Property Class'
KEY_DISP_GRD_FOOTING = 'Grade*'
KEY_DISP_GRD = 'Property Class'
KEY_DISP_BOLT_PRE_TENSIONING = 'Bolt Tension'

KEY_DISP_MOMENT_MAJOR = ' - Major axis (M<sub>z-z</sub>)'
KEY_DISP_MOMENT_MINOR = ' - Minor axis (M<sub>y-y</sub>)'

# Applied load
KEY_INTERACTION_RATIO ="Interaction Ratio"
MIN_LOADS_REQUIRED ="Minimum Required Load"
KEY_DISP_APPLIED_SHEAR_LOAD = 'Applied Shear Force (kN)'
KEY_DISP_APPLIED_AXIAL_FORCE = 'Applied Axial Force (kN)'
KEY_DISP_APPLIED_MOMENT_LOAD = 'Applied Moment (kNm)'
KEY_DISP_AXIAL_FORCE_CON = 'Axial Load Considered (kN)'


# capacity

KEY_OUT_DISP_AXIAL_CAPACITY = "Axial Capacity Member (kN)"
KEY_OUT_DISP_SHEAR_CAPACITY = "Shear Capacity Member (kN)"
KEY_OUT_DISP_MOMENT_CAPACITY = "Moment Capacity Member (kNm)"
KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY = 'Plastic Moment Capacity (kNm)'
KEY_OUT_DISP_MOMENT_D_DEFORMATION= 'Moment Deformation Criteria (kNm)'
KEY_OUT_DISP_SHEAR_CAPACITY_M = "Shear Capacity (kN)"


KEY_OUT_DIA_ANCHOR = 'Anchor Bolt.Diameter'
KEY_DISP_OUT_DIA_ANCHOR = 'Diameter (mm)'
KEY_OUT_GRD_ANCHOR = 'Anchor Bolt.Grade'
KEY_DISP_OUT_GRD_ANCHOR = 'Property Class'
KEY_OUT_ANCHOR_BOLT_LENGTH = 'Anchor Bolt.Length'
KEY_DISP_OUT_ANCHOR_BOLT_LENGTH = 'Anchor Length (mm)'
KEY_OUT_ANCHOR_BOLT_NO = 'Anchor Bolt.No of Anchor Bolts'
KEY_DISP_OUT_ANCHOR_BOLT_NO = 'No. of Anchors'


KEY_OUT_DISP_ANCHOR_BOLT_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_DISP_ANCHOR_BOLT_BEARING = 'Bearing Capacity (kN)'
KEY_OUT_DISP_ANCHOR_BOLT_CAPACITY = 'Bolt Capacity (kN)'
KEY_OUT_DISP_ANCHOR_BOLT_COMBINED = 'Combined Capacity (kN)'
KEY_OUT_DISP_ANCHOR_BOLT_TENSION_DEMAND = 'Tension Demand (kN)'
KEY_OUT_DISP_ANCHOR_BOLT_TENSION = 'Tension Capacity (kN)'


DISP_TITLE_ANCHOR_BOLT_UPLIFT = 'Anchor Bolt - Inside Column Flange'
KEY_OUT_DIA_ANCHOR_UPLIFT = 'Anchor Bolt.Diameter_Uplift'
KEY_DISP_OUT_DIA_ANCHOR_UPLIFT = 'Diameter (mm)'
KEY_OUT_GRD_ANCHOR_UPLIFT = 'Anchor Bolt.Grade_Uplift'
KEY_DISP_OUT_GRD_ANCHOR_UPLIFT = 'Property Class'
KEY_OUT_ANCHOR_UPLIFT_BOLT_NO = 'Anchor Bolt.No of Anchor Bolts_Uplift'
KEY_DISP_OUT_ANCHOR_UPLIFT_BOLT_NO = 'No. of Anchor Bolts'
KEY_OUT_ANCHOR_BOLT_LENGTH_UPLIFT = 'Anchor Bolt.Length_Uplift'
KEY_DISP_OUT_ANCHOR_BOLT_LENGTH_UPLIFT = 'Anchor Length (mm)'
KEY_OUT_ANCHOR_BOLT_TENSION_UPLIFT = 'Anchor Bolt.Tension_Uplift'
KEY_OUT_DISP_ANCHOR_BOLT_TENSION_UPLIFT = 'Tension Capacity (kN)'
KEY_OUT_ANCHOR_BOLT_TENSION_DEMAND_UPLIFT = 'Anchor Bolt.Tension_Demand_Uplift'
KEY_OUT_DISP_ANCHOR_BOLT_TENSION_DEMAND_UPLIFT = 'Tension Demand (kN)'

DISP_TITLE_MEMBER_CAPACITY ="Member Capacity"
KEY_DISP_MEMBER_CAPACITY = "Member Capacity"


KEY_OUT_DISP_BASEPLATE_WIDTH = 'Width (mm)'
KEY_OUT_DISP_BASEPLATE_LENGTH = 'Length (mm)'
KEY_OUT_DISP_BASEPLATE_THICKNNESS = 'Thickness (mm)'
DISP_TITLE_DETAILING = 'Detailing'
DISP_TITLE_TYPICAL_DETAILING = 'Typical Detailing'
DISP_TITLE_DETAILING_OCF = 'Detailing - Outside Column Flange'
DISP_TITLE_DETAILING_ICF = 'Detailing - Inside Column Flange'

KEY_OUT_DISP_DETAILING_NO_OF_ANCHOR_BOLT = 'Total No. of Anchor Bolts'

KEY_OUT_DISP_DETAILING_PITCH_DISTANCE = 'Pitch Distance (mm)'
KEY_IN_DISP_DETAILING_PITCH_DISTANCE = 'Pitch Distance (mm)'

KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE = 'Gauge Distance (mm)'
KEY_IN_DISP_DETAILING_GAUGE_DISTANCE = 'Gauge Distance (mm)'
KEY_OUT_DISP_DETAILING_CS_GAUGE_DISTANCE = 'Cross-centre Gauge (mm)'
KEY_OUT_DETAILING_END_DISTANCE = 'Detailing.EndDistanceOut'
KEY_IN_DETAILING_END_DISTANCE = 'Detailing.EndDistanceIn'

KEY_OUT_DISP_DETAILING_END_DISTANCE = 'End Distance (mm)'
KEY_IN_DISP_DETAILING_END_DISTANCE = 'End Distance (mm)'

KEY_OUT_DISP_DETAILING_EDGE_DISTANCE = "Edge Distance (mm)"
KEY_IN_DISP_DETAILING_EDGE_DISTANCE = "Edge Distance (mm)"

KEY_OUT_DISP_DETAILING_PROJECTION = 'Effective Projection (mm)'
DISP_TITLE_STIFFENER_PLATE = 'Stiffener Plate'
DISP_OUT_TITLE_STIFFENER_PLATE = 'Stiffener.StiffenerPlate'
DISP_OUT_TITLE_CHS_STIFFENER_PLATE = 'Stiffener.StiffenerPlate'
DISP_TITLE_CONTINUITY_PLATE = 'Continuity Plate'
DISP_TITLE_COL_WEB_STIFFENER_PLATE = 'Column Web Stiffener Plate'
KEY_OUT_DISP_STIFFENER_PLATE_THICKNESS = 'Thickness (mm)'
KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_DISP_STIFFENER_PLATE_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_DISP_STIFFENER_PLATE_MOMENT_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_DISP_STIFFENER_PLATE_MOMENT = 'Moment Capacity (kNm)'
KEY_OUT_DISP_GUSSET_PLATE_MOMENT = 'Moment Capacity (kNm)'
KEY_OUT_DISP_GUSSET_PLATE_MOMENT_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_DISP_GUSSET_PLATE_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_DISP_GUSSET_PLATE_THICKNESS = 'Thickness (mm)'
KEY_OUT_DISP_GUSSET_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
DISP_TITLE_GUSSET_PLATE = 'Gusset Plate Details'
KEY_DISP_FLANGE_PLATE_LENGTH = 'Length (mm)'
KEY_DISP_FLANGE_PLATE_HEIGHT = 'Width (mm)'
KEY_DISP_INNERFLANGESPLICEPLATE = "Inner Plate Details"
DISP_TITLE_INNERFLANGESPLICEPLATE = 'Inner Flange splice plate'
KEY_DISP_INNERFLANGE_PLATE_HEIGHT = 'Width (mm)'
KEY_DISP_INNERFLANGE_PLATE_LENGTH = 'Length (mm)'




# DISP_TITLE_GUSSET_PLATE = 'Gusset Plate'
# KEY_OUT_GUSSET_PLATE_THICKNNESS = 'GussetPlate.Thickness'
# KEY_OUT_DISP_GUSSET_PLATE_THICKNESS = 'Thickness (mm)'
# KEY_OUT_GUSSET_PLATE_SHEAR_DEMAND = 'GussetPlate.Shear_Demand'
# KEY_OUT_DISP_GUSSET_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
# KEY_OUT_GUSSET_PLATE_SHEAR = 'GussetPlate.Shear'
# KEY_OUT_DISP_GUSSET_PLATE_SHEAR = 'Shear Capacity (kN)'
# KEY_OUT_GUSSET_PLATE_MOMENT_DEMAND = 'GussetPlate.Moment_Demand'
# KEY_OUT_DISP_GUSSET_PLATE_MOMENT_DEMAND = 'Moment Demand (kNm)'
# KEY_OUT_GUSSET_PLATE_MOMENT = 'GussetPlate.Moment'
# KEY_OUT_DISP_GUSSET_PLATE_MOMENT = 'Moment Capacity (kNm)'

KEY_OUT_STIFFENER_PLATE_FLANGE = 'Stiffener_Plate.Column_flange'
KEY_DISP_OUT_STIFFENER_PLATE_FLANGE = 'Stiffener Plate'
DISP_TITLE_STIFFENER_PLATE_FLANGE = 'Stiffener Plate along Column flange'
KEY_OUT_STIFFENER_PLATE_FLANGE_LENGTH = 'Stiffener_Plate_Flange.Length'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_LENGTH = 'Length (mm)'
KEY_OUT_STIFFENER_PLATE_FLANGE_HEIGHT = 'Stiffener_Plate_Flange.Height'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_HEIGHT = 'Height (mm)'
KEY_OUT_STIFFENER_PLATE_FLANGE_THICKNNESS = 'Stiffener_Plate_Flange.Thickness'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_THICKNESS = 'Thickness (mm)'
KEY_OUT_STIFFENER_PLATE_FLANGE_SHEAR_DEMAND = 'Stiffener_Plate_Flange.Shear_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_STIFFENER_PLATE_FLANGE_SHEAR = 'Stiffener_Plate_Flange.Shear'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_STIFFENER_PLATE_FLANGE_MOMENT_DEMAND = 'Stiffener_Plate_Flange.Moment_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_MOMENT_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_STIFFENER_PLATE_FLANGE_MOMENT = 'Stiffener_Plate_Flange.Moment'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_MOMENT = 'Moment Capacity (kNm)'

KEY_OUT_STIFFENER_PLATE_ALONG_WEB = 'Stiffener_Plate.Along_Column_web'
KEY_DISP_OUT_STIFFENER_PLATE_ALONG_WEB = 'Stiffener Plate'
DISP_TITLE_STIFFENER_PLATE_ALONG_WEB = 'Stiffener Plate along Column web'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_LENGTH = 'Stiffener_Plate_along_Web.Length'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_LENGTH = 'Length (mm)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_HEIGHT = 'Stiffener_Plate_along_Web.Height'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_HEIGHT = 'Height (mm)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_THICKNNESS = 'Stiffener_Plate_along_Web.Thickness'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_THICKNESS = 'Thickness (mm)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_SHEAR_DEMAND = 'Stiffener_Plate_along_Web.Shear_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_SHEAR = 'Stiffener_Plate_along_Web.Shear'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_MOMENT_DEMAND = 'Stiffener_Plate_along_Web.Moment_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_MOMENT_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_MOMENT = 'Stiffener_Plate_along_Web.Moment'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_MOMENT = 'Moment Capacity (kNm)'

KEY_OUT_STIFFENER_PLATE_ACROSS_WEB = 'Stiffener_Plate.Across_Column_web'
KEY_DISP_OUT_STIFFENER_PLATE_ACROSS_WEB = 'Stiffener Plate'
DISP_TITLE_STIFFENER_PLATE_ACROSS_WEB = 'Stiffener Plate across Column web'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_LENGTH = 'Stiffener_Plate_across_Web.Length'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_LENGTH = 'Length (mm)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_HEIGHT = 'Stiffener_Plate_across_Web.Height'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_HEIGHT = 'Height (mm)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_THICKNNESS = 'Stiffener_Plate_across_Web.Thickness'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_THICKNESS = 'Thickness (mm)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_SHEAR_DEMAND = 'Stiffener_Plate_across_Web.Shear_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_SHEAR = 'Stiffener_Plate_across_Web.Shear'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND = 'Stiffener_Plate_across_Web.Moment_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_MOMENT = 'Stiffener_Plate_across_Web.Moment'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT = 'Moment Capacity (kNm)'


KEY_OUT_SHEAR_KEY = 'Shear Key.Along_both_direction'
KEY_OUT_SHEAR_KEY_TYPICAL_DETAILS = 'Shear Key.TypicalDetails'
KEY_DISP_OUT_SHEAR_KEY = 'Shear Key'
KEY_DISP_OUT_SHEAR_KEY_TYPICAL_DETAILS = 'Typical Details'
DISP_TITLE_SHEAR_KEY = 'Shear Design'
KEY_OUT_SHEAR_RESISTANCE = 'ShearDesign.Resistance'
KEY_OUT_DISP_SHEAR_RESISTANCE = 'Shear Resistance (kN)'
KEY_OUT_SHEAR_KEY_REQ = 'Shear_key.Required'
KEY_OUT_DISP_SHEAR_KEY_REQ = 'Key Required?'
KEY_OUT_SHEAR_KEY_LENGTH = 'Shear_key.Length'
KEY_OUT_DISP_SHEAR_KEY_LENGTH = 'Length (mm)'
KEY_OUT_SHEAR_KEY_DEPTH = 'Shear_key.Depth'
KEY_OUT_DISP_SHEAR_KEY_DEPTH = 'Depth (mm)'
KEY_OUT_SHEAR_KEY_THICKNESS = 'Shear_key.Thickness'
KEY_OUT_DISP_SHEAR_KEY_THICKNESS = 'Thickness (mm)'
KEY_OUT_SHEAR_KEY_STRESS = 'Shear_key.Stress'
KEY_OUT_DISP_SHEAR_KEY_STRESS = 'Bearing Stress (N/mm2)'
KEY_OUT_SHEAR_KEY_MOM_DEMAND = 'Shear_key.MomentDemand'
KEY_OUT_DISP_SHEAR_KEY_MOM_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_SHEAR_KEY_MOM_CAPACITY = 'Shear_key.MomentCapacity'
KEY_OUT_DISP_SHEAR_KEY_MOM_CAPACITY = 'Moment Capacity (kNm)'

#
# DISP_TITLE_STIFFENER_PLATE = 'Stiffener Plate'
# KEY_OUT_STIFFENER_PLATE_THICKNNESS = 'StiffenerPlate.Thickness'
# KEY_OUT_DISP_STIFFENER_PLATE_THICKNESS = 'Thickness (mm)'
# KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND = 'StiffenerPlate.Shear_Demand'
# KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
# KEY_OUT_STIFFENER_PLATE_SHEAR = 'StiffenerPlate.Shear'
# KEY_OUT_DISP_STIFFENER_PLATE_SHEAR = 'Shear Capacity (kN)'
# KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND = 'StiffenerPlate.Moment_Demand'
# KEY_OUT_DISP_STIFFENER_PLATE_MOMENT_DEMAND = 'Moment Demand (kNm)'
# KEY_OUT_STIFFENER_PLATE_MOMENT = 'StiffenerPlate.Moment'
# KEY_OUT_DISP_STIFFENER_PLATE_MOMENT = 'Moment Capacity (kNm)'


KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF = 'DesignPreferences.Anchor_Bolt.OCF.Designation'
KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF = 'DesignPreferences.Anchor_Bolt.ICF.Designation'
KEY_DP_ANCHOR_BOLT_TYPE_OCF = 'DesignPreferences.Anchor_Bolt.OCF.Type'
KEY_DP_ANCHOR_BOLT_TYPE_ICF = 'DesignPreferences.Anchor_Bolt.ICF.Type'
KEY_DISP_DP_ANCHOR_BOLT_TYPE = 'Anchor Bolt Type'
KEY_DP_ANCHOR_BOLT_HOLE_TYPE_OCF = 'DesignPreferences.Anchor_Bolt.OCF.Bolt_Hole_Type'
KEY_DP_ANCHOR_BOLT_HOLE_TYPE_ICF = 'DesignPreferences.Anchor_Bolt.ICF.Bolt_Hole_Type'
KEY_DISP_DP_ANCHOR_BOLT_HOLE_TYPE = 'Anchor Bolt Hole Type'
KEY_DISP_REPORT_HOLE_TYPE = 'Hole Type'
KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF = 'DesignPreferences.Anchor_Bolt.OCF.Material_Grade_OverWrite'
KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF = 'DesignPreferences.Anchor_Bolt.ICF.Material_Grade_OverWrite'
KEY_DISP_DP_ANCHOR_BOLT_MATERIAL_G_O = 'Material Grade, Fu (MPa)'
KEY_DISP_DP_ANCHOR_BOLT_DESIGN_PARA = 'HSFG bolt design parameters:'
KEY_DP_ANCHOR_BOLT_SLIP_FACTOR = 'DesignPreferences.Anchor_Bolt.Slip_Factor'
KEY_DISP_DP_ANCHOR_BOLT_SLIP_FACTOR = 'Slip factor (µ_f)'
KEY_DP_ANCHOR_BOLT_GALVANIZED_OCF = 'DesignPreferences.Anchor_Bolt.OCF.Galvanized'
KEY_DP_ANCHOR_BOLT_GALVANIZED_ICF = 'DesignPreferences.Anchor_Bolt.ICF.Galvanized'
KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED = 'Anchor Bolt Galvanized?'
KEY_DP_ANCHOR_BOLT_LENGTH_OCF = 'DesignPreferences.Anchor_Bolt.OCF.Length'
KEY_DP_ANCHOR_BOLT_LENGTH_ICF = 'DesignPreferences.Anchor_Bolt.ICF.Length'
KEY_DISP_DP_ANCHOR_BOLT_LENGTH = 'Total Length (mm)'
KEY_DP_ANCHOR_BOLT_FRICTION = 'DesignPreferences.Anchor_Bolt.Friction_coefficient'
KEY_DISP_DP_ANCHOR_BOLT_FRICTION = 'Friction Coefficient <br>(between concrete and anchor bolt)'


KEY_DISP_DP_BOLT_TYPE = 'Bolt tensioning type'

###################################
# Key for Storing Shear sub-key of Load


KEY_SHEAR_BP = 'Load.Shear_BP'
KEY_DISP_SHEAR_BP = 'Shear Force (kN)'
KEY_SHEAR_MAJOR = 'Load.Shear.Major'
KEY_DISP_SHEAR_MAJOR = ' - Along major axis (z-z)'
KEY_SHEAR_MINOR = 'Load.Shear.Minor'
KEY_DISP_SHEAR_MINOR = ' - Along minor axis (y-y)'


###################################
# Key for Storing Axial sub-key of Load
KEY_AXIAL_BP = 'Load.Axial_Compression'
KEY_DISP_AXIAL_BP = 'Axial Compression (kN)'
KEY_AXIAL_TENSION_BP = 'Load.Axial_Tension'
KEY_DISP_AXIAL_TENSION_BP = 'Axial Tension/Uplift (kN)'
KEY_DISP_DP_BOLT_HOLE_TYPE = 'Hole Type'

# KEY_PC = 'Bolt.PC'
KEY_DISP_PC = 'Property Class'
KEY_DISP_DP_BOLT_MATERIAL_G_O = 'Material grade overwrite (MPa) Fu'
KEY_DISP_DP_BOLT_DESIGN_PARA = 'HSFG Bolt:'


KEY_DISP_DP_BOLT_SLIP_FACTOR = 'Slip Factor, (mu<sub>f</sub>)'
KEY_DISP_DP_BOLT_SLIP_FACTOR_REPORT = 'Slip Factor, ($\mu_{f}$)'
KEY_DISP_DP_BOLT_FU = 'Bolt Ultimate Strength (N/mm2)'
KEY_DISP_DP_BOLT_FY = 'Bolt Yield Strength (N/mm2)'
KEY_DISP_GAMMA_M0 = "Governed by Yielding"
KEY_DISP_GAMMA_M1 = "Governed by Ultimate Stress"
KEY_DISP_GAMMA_MB = "Connection Bolts - Bearing Type"
KEY_DISP_GAMMA_MF = "Connection Bolts - Friction Type"
KEY_DISP_GAMMA_MW = "Connection Weld"


KEY_DISP_DP_WELD_TYPE = 'Weld Type'
KEY_DISP_BEAM_FLANGE_WELD_TYPE = 'Beam Flange to End Plate'
KEY_DISP_BEAM_WEB_WELD_TYPE = 'Beam Web to End Plate'
KEY_DISP_STIFFENER_WELD_TYPE = "Stiffener"
KEY_DISP_CONTINUITY_PLATE_WELD_TYPE = "Continuity Plate"
KEY_DP_WELD_TYPE_FILLET = 'Fillet Weld'
KEY_DP_WELD_TYPE_GROOVE = 'Groove Weld'
KEY_DP_WELD_TYPE_VALUES = [KEY_DP_WELD_TYPE_FILLET, KEY_DP_WELD_TYPE_GROOVE]

KEY_DISP_DP_WELD_FAB = 'Type of Weld Fabrication'
KEY_DP_FAB_SHOP = 'Shop Weld'
KEY_DP_FAB_FIELD = 'Field weld'
KEY_DP_WELD_FAB_VALUES = [KEY_DP_FAB_SHOP, KEY_DP_FAB_FIELD]

KEY_DISP_DP_WELD_MATERIAL_G_O = 'Material Grade Overwrite, Fu (MPa)'
KEY_DISP_DP_WELD_MATERIAL_G_O_REPORT = 'Material Grade Overwrite, $F_{u}$ (MPa)'
KEY_DP_DESIGN_BASE_PLATE = 'DesignPreferences.Design.Base_Plate'
# KEY_DISP_DP_DETAILING_EDGE_TYPE = 'Type of edge'
KEY_DISP_DP_DETAILING_EDGE_TYPE = 'Edge Preparation Method'  # added by Danish Ansari

DISP_TITLE_INTERMITTENT = 'Intermittent Connection'
DISP_TITLE_BOLTD = 'Bolt Details'
DISP_TITLE_PLATED = 'Plate Details'

KEY_DISP_DP_DETAILING_GAP = 'Gap Between Beam and <br>Support (mm)'
KEY_DISP_DP_DETAILING_GAP_BEAM = 'Gap Between Beams (mm)'
KEY_DISP_DP_DETAILING_GAP_COL = 'Gap Between Columns (mm)'
KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES = 'Are the Members Exposed to <br> Corrosive Influences?'
KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES_BEAM = 'Are the Members Exposed to Corrosive Influences?'
KEY_DISP_CORR_INFLUENCES = 'Members exposed to corrosive influences?'
KEY_DISP_DP_DESIGN_METHOD = 'Design Method'

KEY_DISP_DP_DESIGN_BASE_PLATE = 'Base Plate Analysis'
KEY_DISP_GAP = 'Gap Between Members (mm)'


KEY_DISP_MECH_PROP = 'Mechanical Properties'
KEY_DISP_DIMENSIONS = 'Dimensions'
KEY_DISP_DEPTH = 'Depth, D (mm)*'
KEY_DISP_WIDTH = 'Width, B (mm)*'
KEY_DISP_THICKNESS = 'Thickness, T (mm)*'
KEY_DISP_NB = 'Nominal Bore, NB (mm)*'
KEY_DISP_OD = 'Outside Diameter, OD (mm)*'
KEY_DISP_FLANGE_W = 'Flange Width, B (mm)*'
KEY_DISP_FLANGE_T = 'Flange Thickness, T (mm)*'
KEY_DISP_WEB_HEIGHT = 'Web Height, D (mm*)'
KEY_DISP_WEB_T = 'Web Thickness, t (mm)*'
KEY_DISP_FLANGE_S = 'Flange Slope, α (deg.)*'
KEY_DISP_FLANGE_S_REPORT = 'Flange Slope'
KEY_DISP_ROOT_R = 'Root Radius, R1 (mm)*'
KEY_DISP_TOE_R = 'Toe Radius, R2 (mm)*'
KEY_DISP_TYPE = 'Type'
KEY_DISP_MOD_OF_ELAST = 'Modulus of Elasticity, E (GPa)'
KEY_DISP_MOD_OF_RIGID = 'Modulus of Rigidity, G (GPa)'
KEY_DISP_SEC_PROP = 'Section Properties'
KEY_DISP_MASS = 'Mass, M (Kg/m)'
KEY_DISP_Cz = 'Cz (cm)'
KEY_DISP_Cy = 'Cy (cm)'
KEY_DISP_AREA = 'Sectional Area, a (cm<sup>2</sup>)'
KEY_DISP_MOA = '2nd Moment of Area, I (cm<sup>4</sup>/m)*'
KEY_DISP_MOA_IZ = '2nd Moment of Area, I<sub>z</sub> (cm<sup>4</sup>)'
KEY_DISP_MOA_IY = '2nd Moment of Area, I<sub>y</sub> (cm<sup>4</sup>)'
KEY_DISP_MOA_IU = '2nd Moment of Area, I<sub>u</sub> (cm<sup>4</sup>)'
KEY_DISP_MOA_IV = '2nd Moment of Area, I<sub>v</sub> (cm<sup>4</sup>)'
KEY_DISP_ROG = 'Radius of Gyration, r (cm)*'
KEY_DISP_ROG_RZ = 'Radius of Gyration, r<sub>z</sub> (cm)'
KEY_DISP_ROG_RY = 'Radius of Gyration, r<sub>y</sub> (cm)'
KEY_DISP_ROG_RU = 'Radius of Gyration, r<sub>u</sub> (cm)'
KEY_DISP_ROG_RV = 'Radius of Gyration, r<sub>v</sub> (cm)'
KEY_DISP_SM = 'Section Modulus, Z (cm<sup>3</sup>)*'
KEY_DISP_EM_ZZ = 'Elastic Modulus, Z<sub>z</sub> (cm<sup>3</sup>)'
KEY_DISP_EM_ZY = 'Elastic Modulus, Z<sub>y</sub> (ccm<sup>3</sup>)'
KEY_DISP_PM_ZPZ = 'Plastic Modulus, Z<sub>pz</sub> (cm<sup>3</sup>)'
KEY_DISP_PM_ZPY = 'Plastic Modulus, Z<sub>py</sub> (cm<sup>3</sup>)'
KEY_DISP_It = 'Torsion Constant, I<sub>t</sub> (cm<sup>4</sup>)'
KEY_DISP_Iw = 'Warping Constant, I<sub>w</sub> (cm<sup>6</sup>)'
KEY_DISP_IV = 'Internal Volume (cm<sup>3</sup>/m)*'

KEY_SOURCE = 'Section.Source'
KEY_DISP_SOURCE = 'Source'
KEY_DISP_POISSON_RATIO = 'Poisson\'s Ratio, v'
KEY_DISP_THERMAL_EXP = 'Thermal Expansion Coefficient, <br>(x10<sup>-6</sup>/ <sup>0</sup>C)'
KEY_DISP_A= 'Long Leg, A (mm)*'
KEY_DISP_B= 'Short Leg, B (mm)*'
KEY_DISP_LEG_THK = 'Leg Thickness, t (mm)*'
KEY_DISP_BASE_PLATE_MATERIAL = 'Material'
KEY_DISP_ST_SK_MATERIAL = 'Material '
KEY_DISP_REPORT_MATERIAL_GRADE = 'Material Grade, $F_{u}$ (MPa)'
KEY_DISP_BASE_PLATE_FU = 'Ultimate Strength, Fu (MPa)'
KEY_DSIP_BASE_PLATE_FY = 'Yield Strength , Fy (MPa)'
KEY_DISP_ST_SK_FU = 'Ultimate Strength, Fu (MPa)'
KEY_DSIP_ST_SK_FY = 'Yield Strength , Fy (MPa)'
KEY_DISP_ULTIMATE_STRENGTH_REPORT = 'Ultimate Strength, $F_u$ (MPa)'
KEY_DISP_YIELD_STRENGTH_REPORT = 'Yield Strength, $F_y$ (MPa)'

# Common keys for design report

# section properties (In the form of LaTeX equations)
KEY_REPORT_MASS = 'Mass, $m$ (kg/m)'
KEY_REPORT_AREA = 'Area, $A$ (cm$^2$)'
KEY_REPORT_DEPTH = '$D$ (mm)'
KEY_REPORT_WIDTH = '$B$ (mm)'
KEY_REPORT_MAX_LEG_SIZE = '$A$ (mm)'
KEY_REPORT_MIN_LEG_SIZE = '$B$ (mm)'
KEY_REPORT_FLANGE_THK = '$T$ (mm)'
KEY_REPORT_WEB_THK = '$t$ (mm)'
KEY_REPORT_ANGLE_THK = '$t$ (mm)'
KEY_REPORT_R1 = '$R_1$ (mm)'
KEY_REPORT_R2 = '$R_2$ (mm)'
KEY_REPORT_CY = '$C_y$ (mm)'
KEY_REPORT_CZ = '$C_z$ (mm)'
KEY_REPORT_IZ = '$I_z$ (cm$^4$)'
KEY_REPORT_IY = '$I_y$(cm$^4$)'
KEY_REPORT_IU = '$I_u$ (cm$^4$)'
KEY_REPORT_IV = '$I_v$(cm$^4$)'
KEY_REPORT_RZ = '$r_z$ (cm)'
KEY_REPORT_RY = '$r_y$ (cm)'
KEY_REPORT_RU = '$r_u$ (cm)'
KEY_REPORT_RV = '$r_v$ (cm)'
KEY_REPORT_ZEZ = '$Z_z$ (cm$^3$)'
KEY_REPORT_ZEY = '$Z_y$ (cm$^3$)'
KEY_REPORT_ZPZ = '$Z_{pz}$ (cm$^3$)'
KEY_REPORT_ZPY = '$Z_{py}$ (cm$^3$)'
KEY_REPORT_2ND_MOM = '2nd Moment of area, I ($cm^{4}/m$)'
KEY_REPORT_RADIUS_GYRATION = 'Radius of gyration, r ($cm$)'
KEY_REPORT_SECTION_MODULUS = 'Modulus of section, Z ($cm^{3}$)'
KEY_REPORT_NB = 'Nominal bore, NB (mm)'
KEY_REPORT_OD = 'Out diameter, OD (mm)'

# Design cheks
KEY_REPORT_DIAMETER = 'Diameter $(mm)$'
KEY_REPORT_BOLT_NOS = 'Number of Bolts'
KEY_REPORT_PROPERTY_CLASS = 'Property Class'
KEY_REPORT_MIN_END = 'Min. End Distance $(mm)$'
KEY_REPORT_MAX_END = 'Max. End Distance $(mm)$'
KEY_REPORT_MIN_EDGE = 'Min. Edge Distance $(mm)$'
KEY_REPORT_MAX_EDGE = 'Max. Edge Distance $(mm)$'
KEY_REPORT_MIN_PITCH = 'Min. Pitch Distance $(mm)$'
KEY_REPORT_MAX_PITCH = 'Max. Pitch Distance $(mm)$'
KEY_REPORT_MIN_GAUGE = 'Min. Gauge Distance $(mm)$'
KEY_REPORT_MAX_GAUGE = 'Max. Gauge Distance $(mm)$'

KEY_REPORT_PLATE_LENGTH = 'Length $(mm)$'
KEY_REPORT_PLATE_WIDTH = 'Width $(mm)$'
KEY_REPORT_PLATE_HEIGHT = 'Height $(mm)$'

KEY_REPORT_SHEAR_CAPA = 'Shear Capacity $(kN)$'
KEY_REPORT_BEARING_CAPA = 'Bearing Capacity $(kN)$'
KEY_REPORT_BOLT_CAPA = 'Bolt Capacity $(kN)$'
KEY_REPORT_TENSION_CAPA = 'Tension Capacity $(kN)$'
KEY_REPORT_TENSION_DEMAND = 'Tension Demand $(kN)$'

########################
# Output Keys
########################
KEY_OUT_ANCHOR_BOLT_SHEAR = 'Anchor Bolt.Shear'
KEY_OUT_ANCHOR_BOLT_BEARING = 'Anchor Bolt.Bearing'
KEY_OUT_ANCHOR_BOLT_CAPACITY = 'Anchor Bolt.Capacity'
KEY_OUT_ANCHOR_BOLT_COMBINED = 'Anchor Bolt.Combined'
KEY_OUT_ANCHOR_BOLT_TENSION_DEMAND = 'Anchor Bolt.Tension_Demand'
KEY_OUT_ANCHOR_BOLT_TENSION = 'Anchor Bolt.Tension'
KEY_MEMBER_CAPACITY = "section.memcapacity"
KEY_MEMBER_AXIALCAPACITY='Section.AxialCapacity'
KEY_MEMBER_SHEAR_CAPACITY='Section.ShearCapacity'
KEY_MEMBER_MOM_CAPACITY='Section.MomCapacity'
KEY_OUT_BASEPLATE_THICKNNESS = 'Baseplate.Thickness'
KEY_OUT_BASEPLATE_LENGTH = 'Baseplate.Length'
KEY_OUT_BASEPLATE_WIDTH = 'Baseplate.Width'
KEY_OUT_BASEPLATE_BEARING_STRESS = 'Baseplate.BearingStress'
KEY_OUT_BASEPLATE_MOMENT_DEMAND = 'Baseplate.MomentDemand'
KEY_OUT_DISP_BASEPLATE_MOMENT_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_BASEPLATE_MOMENT_CAPACITY = 'Baseplate.MomentCapacity'
KEY_OUT_DISP_BASEPLATE_MOMENT_CAPACITY = 'Moment Capacity (kNm)'
# KEY_OUT_DISP_BASEPLATE_BEARING_STRESS = 'Bearing Stress (N/mm<sup>2</sup>)'
KEY_OUT_DISP_BASEPLATE_BEARING_STRESS = 'Bearing Stress (MPa)'
KEY_OUT_DETAILING_PROJECTION = 'Detailing.Projection'
KEY_OUT_DETAILING_NO_OF_ANCHOR_BOLT = 'Detailing.No of Anchor bolts'
KEY_OUT_DETAILING_EDGE_DISTANCE = 'Detailing.EdgeDistanceOut'
KEY_IN_DETAILING_EDGE_DISTANCE = 'Detailing.EdgeDistanceIn'
KEY_OUT_DETAILING_GAUGE_DISTANCE = 'Detailing.GaugeDistanceOut'
KEY_IN_DETAILING_GAUGE_DISTANCE = 'Detailing.GaugeDistanceIn'
KEY_OUT_DETAILING_CS_GAUGE_DISTANCE = 'Detailing.Cross-centre Gauge Distance'
KEY_OUT_DETAILING_PITCH_DISTANCE = 'Detailing.PitchDistanceOut'
KEY_IN_DETAILING_PITCH_DISTANCE = 'Detailing.PitchDistanceIn'
KEY_BOLT_FU = 'Bolt.fu'
KEY_BOLT_FY = 'Bolt.fy'

KEY_OUT_DISP_DETAILING_BOLT_COLUMNS = 'Detailing.No. of Columns'
KEY_OUT_DISP_DETAILING_BOLT_COLUMNS_EP = 'No. of Columns'
KEY_OUT_DISP_DETAILING_BOLT_ROWS = 'Detailing.No. of Rows'
KEY_OUT_DISP_DETAILING_BOLT_ROWS_EP = 'No. of Rows'
KEY_OUT_DISP_DETAILING_BOLT_NUMBERS = 'Detailing.No. of Bolts'
KEY_OUT_DISP_DETAILING_BOLT_NUMBERS_EP = 'No. of Bolts'


KEY_OUT_GUSSET_PLATE_THICKNNESS = 'GussetPlate.Thickness'
KEY_OUT_GUSSET_PLATE_SHEAR_DEMAND = 'GussetPlate.Shear_Demand'
KEY_OUT_GUSSET_PLATE_SHEAR = 'GussetPlate.Shear'
KEY_OUT_GUSSET_PLATE_MOMENT_DEMAND = 'GussetPlate.Moment_Demand'
KEY_OUT_GUSSET_PLATE_MOMENT = 'GussetPlate.Moment'
KEY_OUT_STIFFENER_PLATE_THICKNNESS = 'StiffenerPlate.Thickness'

KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND = 'StiffenerPlate.Shear_Demand'
KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND_CHS = 'StiffenerPlate.Shear_Demand'
KEY_OUT_STIFFENER_PLATE_SHEAR_CAPACITY = 'StiffenerPlate.Shear_Capacity'
KEY_OUT_STIFFENER_PLATE_SHEAR_CAPACITY_CHS = 'StiffenerPlate.Shear_Capacity'
KEY_OUT_STIFFENER_PLATE_SHEAR = 'StiffenerPlate.Shear'
KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND = 'StiffenerPlate.Moment_Demand'
KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND_CHS = 'StiffenerPlate.Moment_Demand'
KEY_OUT_STIFFENER_PLATE_MOMENT_CAPACITY = 'StiffenerPlate.Moment_Capacity'
KEY_OUT_STIFFENER_PLATE_MOMENT_CAPACITY_CHS = 'StiffenerPlate.Moment_Capacity'
KEY_OUT_STIFFENER_PLATE_MOMENT = 'StiffenerPlate.Moment'

KEY_PLATE_MIN_HEIGHT = 'Plate.MinHeight'
KEY_PLATE_MAX_HEIGHT = 'Plate.MaxHeight'
KEY_SLENDER = "Member.Slenderness"

KEY_INNERFLANGEPLATE_THICKNESS = 'flange_plate.innerthickness_provided'
KEY_FLANGE_PLATE_HEIGHT = 'Flange_Plate.Width (mm)'
KEY_OUT_FLANGESPLATE_THICKNESS = 'flange_plate.Thickness'
KEY_DISP_FLANGESPLATE_THICKNESS = 'Thickness (mm)'
KEY_FLANGE_PLATE_LENGTH ='flange_plate.Length'
KEY_OUT_FLANGE_BOLT_SHEAR ="flange_bolt.shear capacity"

KEY_INNERPLATE= "flange_plate.Inner_plate_details"

KEY_INNERFLANGE_PLATE_HEIGHT = 'Flange_Plate.InnerWidth'
KEY_INNERFLANGE_PLATE_LENGTH ='flange_plate.InnerLength'

KEY_DISP_AREA_CHECK ="Plate Area Check (mm2)"


KEY_FLANGE_SPACING ="Flange_plate.spacing"

KEY_FLANGE_PITCH = 'Flange_plate.pitch_provided'
KEY_FLANGE_PLATE_GAUGE = "Flange_plate.gauge_provided "
KEY_ENDDIST_FLANGE= 'Flange_plate.end_dist_provided '
KEY_EDGEDIST_FLANGE= 'Flange_plate.edge_dist_provided'

KEY_FLANGE_CAPACITY ='section.flange_capacity'

# flange
KEY_FLANGE_TEN_CAPACITY ="Section.flange_capacity"
KEY_DISP_FLANGE_TEN_CAPACITY ="Flange Tension Capacity (kN)"
KEY_TENSIONYIELDINGCAP_FLANGE = 'section.tension_yielding_capacity'
KEY_DISP_TENSIONYIELDINGCAP_FLANGE = 'Flange Tension Yielding Capacity (kN)'
KEY_TENSIONRUPTURECAP_FLANGE='section.tension_rupture_capacity '
KEY_DISP_TENSIONRUPTURECAP_FLANGE= 'Flange Tension Rupture Capacity (kN)'
KEY_BLOCKSHEARCAP_FLANGE='section.block_shear_capacity'
KEY_DISP_BLOCKSHEARCAP_FLANGE='Flange Block Shear Capacity (kN)'
# flange plate
KEY_TENSIONYIELDINGCAP_FLANGE_PLATE = 'Flange_plate.tension_yielding_capacity (kN)'
KEY_DISP_TENSIONYIELDINGCAP_FLANGE_PLATE ='Tension Yielding Capacity (kN)'
KEY_TENSIONRUPTURECAP_FLANGE_PLATE= 'Flange_plate.tension_rupture_capacity (kN)'
KEY_DISP_TENSIONRUPTURECAP_FLANGE_PLATE ='Tension Rupture Capacity (kN)'
KEY_BLOCKSHEARCAP_FLANGE_PLATE = 'flange_plate.block_shear_capacity '
KEY_DISP_BLOCKSHEARCAP_FLANGE_PLATE ='Block Shear Capacity (kN)'
KEY_FLANGE_PLATE_TEN_CAP ="flange_plate.tension_capacity_flange_plate"



# KEY_TENSIONRUPTURECAP_FLANGE= 'Flange_plate.tension_rupture_capacity'
# KEY_DISP_TENSIONRUPTURECAP_FLANGE= 'Flange Tension Rupture Capacity (kN)'
# KEY_SHEARYIELDINGCAP_FLANGE= 'Flange_plate.shear_yielding_capacity'
# KEY_DISP_SHEARYIELDINGCAP_FLANGE= 'Shear Yielding Capacity (kN)'
# KEY_SHEARRUPTURECAP_FLANGE= 'Flange_plate.shear_rupture_capacity'
# KEY_DISP_SHEARRUPTURECAP_FLANGE= 'Shear Rupture Capacity (kN)'
KEY_FLANGE_PLATE_MOM_DEMAND = 'Flange_Plate.MomDemand'
KEY_FLANGE_DISP_PLATE_MOM_DEMAND = 'Flange Moment Demand (kNm)'
KEY_FLANGE_PLATE_MOM_CAPACITY='Flange_plate.MomCapacity'
KEY_FLANGE_DISP_PLATE_MOM_CAPACITY = 'Flange Moment Capacity (kNm)'
KEY_DESIGNATION = "section_size.designation"
KEY_DISP_DESIGNATION = "Designation"


KEY_TENSION_YIELDCAPACITY = "Member.tension_yielding"
KEY_DISP_TENSION_YIELDCAPACITY = 'Tension Yielding Capacity (kN)'
KEY_TENSION_RUPTURECAPACITY = "Member.tension_rupture"
KEY_DISP_TENSION_RUPTURECAPACITY = 'Tension Rupture Capacity (kN)'
KEY_TENSION_BLOCKSHEARCAPACITY = "Member.tension_blockshear"
KEY_DISP_TENSION_BLOCKSHEARCAPACITY = 'Block Shear Capacity (kN)'

KEY_SHEAR_YIELDCAPACITY = "Member.shear_yielding"
KEY_SHEAR_RUPTURECAPACITY = "Member.shear_rupture"
KEY_SHEAR_BLOCKSHEARCAPACITY = "Member.shear_blockshear"



KEY_TENSION_CAPACITY = "Member.tension_capacity"
KEY_DISP_TENSION_CAPACITY = "Tension Capacity (kN)"

KEY_EFFICIENCY = "Member.efficiency"
KEY_DISP_EFFICIENCY = "Utilization Ratio"

DISP_TITLE_BOLTDETAILS ='Bolt Details'
KEY_BOLT_DETAILS ="Bolt.Details"

DISP_TITLE_BOLT_CAPACITIES = 'Bolt Capacities'
KEY_BOLT_CAPACITIES = 'Bolt.Capacities'
DISP_THROAT_THICKNESS = "Throat Thickness"
DISP_TITLE_BOLT_CAPACITY_FLANGE= 'Flange Bolt Capacity'
KEY_DISP_BOLT_DETAILS = "Bolt Details"
KEY_FLANGE_BOLT_LINE = 'Flange_plate.Bolt_Line'
KEY_FLANGE_DISP_BOLT_LINE = 'Bolt Lines '
KEY_FLANGE_BOLTS_ONE_LINE = 'Flange_plate.Bolt_OneLine'
KEY_FLANGE_DISP_BOLTS_ONE_LINE = 'Bolts in One Line '
KEY_FLANGE_BOLTS_REQ = "Flange_plate.Bolt_required"
KEY_FLANGE_DISP_BOLTS_REQ = "Bolts Required"
KEY_FLANGE_NUM_BOLTS_REQ = "Flange_plate.Bolt_required"


KEY_FLANGE_WELD_DETAILS = "Flange detail"
KEY_DISP_FLANGE_WELD_DETAILS = "Weld Details"

KEY_INNERFLANGE_WELD_DETAILS = "Inner Flange detail"
KEY_DISP_INNERFLANGE_WELD_DETAILS = "Weld Details"

KEY_WELD_TYPE = 'Weld.Type'
KEY_DISP_WELD_TYPE = 'Type'
VALUES_WELD_TYPE = ["Fillet Weld", "Groove Weld"]
VALUES_WELD_TYPE_EP = ["Groove Weld", "Fillet Weld"]
VALUES_WELD_TYPE_BB_FLUSH = ["Groove Weld"]
DISP_FLANGE_TITLE_WELD = 'Flange Weld'
KEY_FLANGE_WELD_SIZE = 'Flange_Weld.Size'
KEY_FLANGE_DISP_WELD_SIZE = 'Flange Weld Size (mm)'
KEY_FLANGE_WELD_STRENGTH = 'Flange_Weld.Strength'
KEY_FLANGE_DISP_WELD_STRENGTH = 'Flange Weld Strength (N/mm)'
KEY_FLANGE_WELD_STRESS = 'Flange_Weld.Stress'
KEY_FLANGE_DISP_WELD_STRESS = 'Flange Weld Stress (N/mm)'
KEY_FLANGE_WELD_LENGTH = 'Flange_Weld.Length'
KEY_DISP_FLANGE_WELD_LENGTH ='Flange Weld Length'
KEY_FLANGE_WELD_LENGTH_EFF = 'Flange_Weld.EffLength'

KEY_DISP_WELD_LEN_EFF_OUTSIDE = 'EffLength. Outer+Inner flange'
KEY_DISP_CLEARANCE = "Clearance (mm)"
KEY_FLANGE_WELD_HEIGHT ='flange_Weld.height'
KEY_DISP_FLANGE_WELD_HEIGHT = 'Flange Weld Height'
DISP_EFF = "Effective Length (mm)"
KEY_INNERFLANGE_WELD_LENGTH = 'Flange_Weld.InnerLength'
KEY_DISP_INNERFLANGE_WELD_LENGTH ='Length (mm)'
KEY_INNERFLANGE_WELD_LENGTH_EFF = 'Flange_Weld.InnerEffLength'
KEY_INNERFLANGE_WELD_HEIGHT ='flange_Weld.Innerheight'
KEY_DISP_INNERFLANGE_WELD_HEIGHT = 'Height (mm)'
KEY_INNERFLANGE_WELD_STRESS = 'Inner_Flange_Weld.Stress'
KEY_INNERFLANGE_DISP_WELD_STRESS = 'Flange Weld Stress (N/mm)'
KEY_INNERFLANGE_WELD_STRENGTH = 'Inner_Flange_Weld.Strength'
KEY_INNERFLANGE_DISP_WELD_STRENGTH = 'Flange Weld Strength (N/mm)'

# FLANGE AND WEB -REDUCTION FACTOR
KEY_REDUCTION_FACTOR_LONG_FLANGE ='flange_plate.red,factor'
KEY_DISP_REDUCTION_FACTOR_FLANGE ="Long Joint Red.Factor"

KEY_REDUCTION_FACTOR_LONG_WEB ='web_plate.red,factor'
KEY_DISP_REDUCTION_FACTOR_LONG_WEB ="Long Joint Red.Factor"

KEY_REDUCTION_LARGE_GRIP_WEB = 'web_bolt.large_grip'
KEY_DISP_REDUCTION_LARGE_GRIP_WEB = "Large Grip Red.Factor"

KEY_REDUCTION_LARGE_GRIP_FLANGE = 'flange_bolt.large_grip'
KEY_DISP_REDUCTION_LARGE_GRIP_FLANGE = "Large Grip Red.Factor"

# COMMON -REDUCTION FACTOR
KEY_REDUCTION_LONG_JOINT ="bolt.long_joint"
KEY_DISP_REDUCTION_LONG_JOINT ="Long Joint Red.Factor"

KEY_REDUCTION_LARGE_GRIP ="bolt.large_grip"
KEY_DISP_REDUCTION_LARGE_GRIP ="Large Grip Red.Factor"



KEY_DISP_REDUCTION ="Strength Red.Factor"
KEY_OUT_FLANGE_BOLT_SHEAR ='flange_bolt.bolt_shear_capacity'
KEY_OUT_DISP_FLANGE_BOLT_SHEAR = "Shear Capacity (kN)"
KEY_OUT_FLANGE_BOLT_BEARING = 'flange_bolt.bolt_bearing_capacity'
KEY_OUT_DISP_FLANGE_BOLT_BEARING = "Bearing Capacity (kN)"
KEY_OUT_FLANGE_BOLT_CAPACITY = 'flange_bolt.bolt_capacity'
KEY_OUT_DISP_FLANGE_BOLT_CAPACITY ="Bolt Capacity (kN)"
KEY_OUT_DISP_FLANGE_BOLT_SLIP= 'Slip Resistance (kN)'
KEY_FLANGE_BOLT_GRP_CAPACITY = 'flange_bolt.grp_bolt_capacity'
KEY_OUT_FLANGE_BOLT_GRP_CAPACITY = 'flange bolt grp bolt capacity (kN)'
KEY_OUT_MIN_PITCH= 'Min_pitch'

KEY_OUT_FLANGE_MIN_PITCH= 'flange_bolt.min_pitch_round'
KEY_OUT_FLANGE_MIN_EDGE_DIST= 'flange_bolt.min_edge_dist_round'
KEY_OUT_FLANGE_MAX_EDGE_DIST='flange_bolt.max_edge_dist_round'

KEY_OUT_DISP_FORCES_FLANGE = 'Force Carried by Flange'
KEY_OUT_DISP_FORCES_WEB= 'Force Carried by Web'
KEY_OUT_WEB_BOLT_SHEAR ='web_bolt.bolt_shear_capacity'
KEY_OUT_DISP_WEB_BOLT_SHEAR = "Shear Capacity (kN)"
KEY_OUT_WEB_BOLT_BEARING = 'web_bolt.bolt_bearing_capacity'
KEY_OUT_DISP_WEB_BOLT_BEARING = "Bearing Capacity (kN)"
KEY_OUT_WEB_BOLT_CAPACITY = 'web_bolt.bolt_capacity'
KEY_OUT_DISP_WEB_BOLT_CAPACITY ="Bolt Capacity (kN)"
KEY_OUT_DISP_WEB_BOLT_SLIP= 'Slip Resistance (kN)'
KEY_WEB_BOLT_GRP_CAPACITY = 'web_bolt.grp_bolt_capacity'
KEY_OUT_WEB_BOLT_GRP_CAPACITY = 'Web bolt grp bolt capacity (kN)'
KEY_OUT_REQ_MOMENT_DEMAND_BOLT = "Moment Demand (kNm)"
KEY_OUT_REQ_PARA_BOLT = "Bolt Force Parameter(s) (mm)"
DISP_TITLE_WEBSPLICEPLATE = 'Web Splice Plate'
KEY_DISP_WEBPLATE_THICKNESS = 'Thickness (mm)*'




KEY_WEB_PLATE_HEIGHT = 'Web_Plate.Height (mm)'
KEY_DISP_WEB_PLATE_HEIGHT = 'Height (mm)'
KEY_WEB_PLATE_LENGTH ='Web_Plate.Width'
KEY_OUT_WEBPLATE_THICKNESS = 'Web_Plate.Thickness'
KEY_DISP_WEBPLATE_THICKNESS = 'Thickness (mm)'
KEY_DISP_WEB_PLATE_LENGTH ='Width (mm)'
DISP_TITLE_BOLT_CAPACITY_WEB = 'Web Bolt Capacity'
KEY_BOLT_CAPACITIES_WEB = 'Web Bolt.Capacities'

KEY_WEB_SPACING ="Web_plate.spacing"
KEY_DISP_WEB_SPACING = 'Spacing (mm)'
KEY_WEB_PITCH = "Web_plate.pitch_provided"
KEY_DISP_WEB_PLATE_PITCH ="Pitch Distance (mm)"
KEY_WEB_GAUGE = "Web_plate.gauge_provided "
KEY_DISP_WEB_PLATE_GAUGE ="Gauge Distance (mm)"
KEY_ENDDIST_W= 'Web_plate.end_dist_provided '
KEY_DISP_END_DIST_W = 'End Distance (mm)'
KEY_EDGEDIST_W = 'Web_plate.edge_dist_provided'
KEY_DISP_EDGEDIST_W = 'Edge Distance (mm)'

KEY_WEB_CAPACITY ='section.web_capacities'
KEY_DISP_WEB_CAPACITY ='Capacity'

# Web plate
KEY_REDUCTION_FACTOR_WEB ='web_plate.red,factor'
KEY_DISP_REDUCTION_FACTOR_WEB ="Red. Factor"
KEY_WEB_PLATE_CAPACITY ="Web_plate.capacity"
KEY_DISP_WEB_PLATE_CAPACITY= 'Web Plate Tension Capacity (kN)'
KEY_TEN_YIELDCAPACITY_WEB_PLATE = "Web_plate.tension_yielding"
KEY_DISP_TENSION_YIELDCAPACITY_WEB_PLATE = 'Tension Yielding Capacity (kN)'
KEY_TENSION_RUPTURECAPACITY_WEB_PLATE = "Web_plate.tension_rupture"
KEY_DISP_TENSION_RUPTURECAPACITY_WEB_PLATE= 'Tension Rupture Capacity (kN)'
KEY_TENSION_BLOCKSHEARCAPACITY_WEB_PLATE = "Web_plate.tension_blockshear"
KEY_DISP_TENSION_BLOCKSHEARCAPACITY_WEB_PLATE = 'Block Shear Capacity (kN)'
# Web
KEY_TENSIONYIELDINGCAP_WEB = "section.tension_yielding_capacity_web"
KEY_DISP_TENSIONYIELDINGCAP_WEB ='Web Tension Yielding Capacity (kN)'
KEY_TENSIONRUPTURECAP_WEB ='section.tension_rupture_capacity_web'
KEY_DISP_TENSIONRUPTURECAP_WEB ='Web Tension Rupture Capacity (kN)'
KEY_TENSIONBLOCK_WEB ='section.block_shear_capacity_web'
KEY_DISP_BLOCKSHEARCAP_WEB ='Web Block Shear Capacity (kN)'
KEY_WEB_TEN_CAPACITY ="section.Tension_capacity_web"
KEY_DISP_WEB_TEN_CAPACITY ="Web Tension Capacity (kN)"
# web in shear
KEY_SHEARYIELDINGCAP_WEB_PLATE= 'web_plate.shear_yielding_capacity'
KEY_DISP_SHEARYIELDINGCAP_WEB_PLATE= 'Shear Yielding Capacity (kN)'
KEY_BLOCKSHEARCAP_WEB_PLATE='web_plate.block_shear_capacity'
KEY_DISP_BLOCKSHEARCAP_WEB_PLATE='Block Shear Capacity (kN)'
KEY_SHEARRUPTURECAP_WEB_PLATE= 'web_plate.shear_rupture_capacity'
KEY_DISP_SHEARRUPTURECAP_WEB_PLATE= 'Shear Rupture Capacity (kN)'
KEY_WEBPLATE_SHEAR_CAPACITY_PLATE ="web_plate.shear_capacity_web_plate"
KEY_DISP_WEBPLATE_SHEAR_CAPACITY_PLATE ="Web Plate Shear Capacity (kN)"
KEY_WEB_PLATE_MOM_DEMAND = 'Web_Plate.MomDemand'
KEY_WEB_DISP_PLATE_MOM_DEMAND = 'Web Moment Demand (kNm)'
KEY_WEB_PLATE_MOM_CAPACITY='Web_plate.MomCapacity'
KEY_WEB_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity (kNm)'
KEY_WEB_BOLT_LINE = 'Web_plate.Bolt_Line'
KEY_WEB_DISP_BOLT_LINE = 'Bolt Lines'
KEY_WEB_BOLTS_REQ = "Web_plate.Bolt_required"
KEY_WEB_DISP_BOLTS_REQ = "Bolt Required"
KEY_WEB_BOLTS_ONE_LINE = 'Web_plate.Bolt_OneLine'
KEY_WEB_DISP_BOLTS_ONE_LINE = 'Bolts in One Line'

KEY_WEB_WELD_DETAILS = "Web detail"
KEY_DISP_WEB_WELD_DETAILS = "Weld Details"
DISP_WEB_TITLE_WELD = 'Web Weld'
KEY_WEB_WELD_SIZE = 'Web_Weld.Size'
KEY_WEB_DISP_WELD_SIZE = 'Web Weld Size (mm)'
KEY_WEB_WELD_STRENGTH = 'Web_Weld.Strength'
KEY_WEB_DISP_WELD_STRENGTH = 'Web Weld Strength (N/mm)'
KEY_WEB_WELD_STRESS = 'Web_Weld.Stress'
KEY_WEB_DISP_WELD_STRESS = 'Web Weld Stress (N/mm)'
KEY_WEB_WELD_LENGTH = 'Web_Weld.Length'
KEY_DISP_WEB_WELD_LENGTH = 'Web Weld Length'
KEY_WEB_WELD_LENGTH_EFF = 'Web_Weld.EffLength'
KEY_WEB_WELD_HEIGHT ='Web_Weld.height'
KEY_DISP_WEB_WELD_HEIGHT = 'Web Weld Height'
KEY_OUT_LONG_JOINT_WELD = 'Weld Strength (post long joint) (N/mm)'
KEY_OUT_DISP_RED_WELD_STRENGTH = 'Weld Strength (N/mm)'


DISP_TITLE_ENDPLATE = 'End Plate'

KEY_ENDPLATE_THICKNESS = 'Plate.end_plate.Thickness'
KEY_DISP_ENDPLATE_THICKNESS = 'Thickness (mm)'

KEY_BASE_PLATE_MATERIAL = 'Base_Plate.Material'
KEY_ST_KEY_MATERIAL = 'Stiffener_Key.Material'
KEY_BASE_PLATE_FU = 'Base_Plate.Fu'
KEY_BASE_PLATE_FY = 'Base_Plate.Fy'
KEY_ST_KEY_FU = 'Stiffener_Key.Fu'
KEY_ST_KEY_FY = 'Stiffener_Key.Fy'

KEY_DISP_LEVER_ARM = "Lever Arm (mm)"
KEY_DISP_REQ_PARA= "Parameters"
KEY_BOLT_STATUS = 'Bolt.DesignStatus'
KEY_OUT_D_PROVIDED = 'Bolt.Diameter'
KEY_OUT_DISP_D_PROVIDED = 'Diameter (mm)'
KEY_OUT_DISP_D_MIN= 'Min. Diameter (mm)'
KEY_OUT_INTER_D_PROVIDED = 'Bolt.InterDiameter'
KEY_OUT_DISP_INTER_D_PROVIDED = 'Diameter (mm)'




KEY_OUT_GRD_PROVIDED = 'Bolt.Grade_Provided'
KEY_OUT_DISP_GRD_PROVIDED = 'Property Class'
KEY_OUT_INTER_GRD_PROVIDED = 'Bolt.InterGrade'
KEY_OUT_DISP_INTER_GRD_PROVIDED = 'Grade'




KEY_OUT_DISP_PC_PROVIDED = 'Property Class'
KEY_OUT_ROW_PROVIDED = 'Bolt.Rows'
KEY_OUT_DISP_ROW_PROVIDED = 'Rows of Bolts'
KEY_OUT_COL_PROVIDED = 'Bolt.Cols'
KEY_OUT_DISP_COL_PROVIDED = 'Columns of Bolts'
KEY_OUT_TOT_NO_BOLTS = 'Bolt.number'
KEY_OUT_DISP_TOT_NO_BOLTS = 'Number of Bolts'
KEY_OUT_KB = 'Bolt.Kb'
KEY_OUT_BOLT_HOLE = 'Bolt.Hole'
KEY_DISP_BOLT_HOLE = 'Hole Diameter (mm)'
KEY_DISP_MIN_BOLT = 'Minimum Bolts (nos)'

KEY_DISP_BOLT_AREA = 'Nominal Stress Area (mm2)'
KEY_DISP_KB = 'Kb'

KEY_OUT_BOLT_IR_DETAILS = 'Bolt.IRDetails'
KEY_OUT_BOLT_IR_DETAILS_SPTD = 'Bolt.IRDetails_sptd'
KEY_OUT_BOLT_IR_DETAILS_SPTING = 'Bolt.IRDetails_spting'
KEY_OUT_DISP_BOLT_IR_DETAILS = 'Capacity Details'
KEY_OUT_BOLT_SHEAR = 'Bolt.Shear'
KEY_OUT_DISP_BOLT_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_BOLT_BEARING = 'Bolt.Bearing'
KEY_OUT_DISP_BOLT_BEARING = 'Bearing Capacity (kN)'
KEY_OUT_BETA_LJ = 'Bolt.Betalj'
KEY_OUT_DISP_BETA_LJ = 'β<sub>lj</sub>'
KEY_OUT_BETA_LG = 'Bolt.Betalg'
KEY_OUT_DISP_BETA_LG = 'β<sub>lg</sub>'
KEY_OUT_BETA_PK = 'Bolt.Betapk'
KEY_OUT_DISP_BETA_PK = 'β<sub>pk</sub>'
KEY_OUT_DISP_BOLT_SLIP= 'Slip Resistance'
KEY_OUT_DISP_BOLT_SLIP_DR = 'Slip Resistance (kN)'
KEY_OUT_BOLT_CAPACITY = 'Bolt.Capacity'
KEY_OUT_BOLT_CAPACITY_SPTD = 'Bolt.Capacity_sptd'
KEY_OUT_BOLT_CAPACITY_SPTING = 'Bolt.Capacity_spting'
KEY_OUT_DISP_BOLT_CAPACITY = 'Capacity (kN)'
KEY_OUT_DISP_BOLT_VALUE = 'Bolt Value (kN)'
KEY_OUT_BOLT_FORCE = 'Bolt.Force (kN)'
KEY_OUT_DISP_BOLT_FORCE = 'Bolt Force (kN)'
KEY_OUT_DISP_BOLT_SHEAR_FORCE = 'Bolt Shear Force (kN)'
KEY_OUT_BOLT_TENSION_FORCE = 'Bolt.TensionForce'
KEY_OUT_DISP_BOLT_TENSION_FORCE = 'Bolt Tension Force (kN)'
KEY_OUT_DISP_CRITICAL_BOLT_TENSION = 'Tension Due to Moment (kN)'
KEY_OUT_DISP_BOLT_TENSION_AXIAL = 'Tension due to Moment and Axial Force (kN)'
KEY_OUT_BOLT_PRYING_FORCE = 'Bolt.PryingForce'
KEY_OUT_DISP_BOLT_PRYING_FORCE = 'Bolt Prying Force (kN)'
KEY_OUT_DISP_BOLT_PRYING_FORCE_EP = 'Prying Force (kN)'
KEY_OUT_BOLT_TENSION_TOTAL = 'Bolt.TensionTotal'
KEY_OUT_DISP_BOLT_TENSION_TOTAL = 'Total Bolt Tension (kN)'
KEY_OUT_DISP_BOLT_TENSION_DEMAND = 'Tension Demand (kN)'
KEY_OUT_DISP_BOLT_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_BOLT_TENSION_CAPACITY = 'Bolt.Tension'
KEY_OUT_BOLT_TENSION_CAPACITY1 = 'Bolt Tension Capacity (kN)'
KEY_OUT_DISP_BOLT_TENSION_CAPACITY = 'Bolt Tension Capacity (kN)'
KEY_OUT_CRITICAL_BOLT_TENSION_CAPACITY = 'Tension Capacity (kN)'
KEY_OUT_BOLTS_REQUIRED = 'Bolt.Required'
KEY_OUT_LONG_JOINT = 'Long Joint Reduction Factor'
KEY_OUT_LARGE_GRIP = 'Large Grip Length Reduction Factor'
KEY_OUT_PACKING_PLATE = 'Packing Plate Reduction Factor'
KEY_OUT_BOLT_CAPACITY_REDUCED = 'Bolt Capacity (post reduction factor) (kN)'
KEY_OUT_BOLT_GRP_CAPACITY = 'Bolt.GroupCapacity'
KEY_OUT_BOLT_LINE = 'Bolt.Line'
KEY_OUT_DISP_BOLT_LINE = 'Bolt Columns (nos)'
KEY_OUT_INTER_BOLT_LINE = 'Bolt.InterLine'
KEY_OUT_DISP_INTER_BOLT_LINE = 'Columns (nos)'
KEY_OUT_BOLT_IR = 'Bolt.IR'
KEY_OUT_DISP_BOLT_IR = 'Interaction Ratio'
KEY_OUT_DISP_BOLT_COMBINED_CAPACITY = 'Combined Capacity, I.R'


KEY_OUT_BOLTS_ONE_LINE = 'Bolt.OneLine'
KEY_OUT_DISP_BOLTS_ONE_LINE = 'Bolt Rows (nos)'
KEY_OUT_BOLTS_ONE_LINE_S = 'Bolt.OneLineT'
KEY_OUT_DISP_BOLTS_ONE_LINE_S = 'Rows per Angle(nos)'

KEY_OUT_INTER_BOLTS_ONE_LINE = 'Bolt.InterOneLine'
KEY_OUT_DISP_INTER_BOLTS_ONE_LINE = 'Rows (nos)'


KEY_OUT_SPACING = 'spacing'
KEY_OUT_DISP_SPACING = 'Spacing'
KEY_OUT_DISP_PATTERN = 'Pattern'
KEY_OUT_PITCH = 'Bolt.Pitch'
KEY_OUT_DISP_PITCH = 'Pitch Distance (mm)'
KEY_OUT_PATTERN_1 = 'pattern1'
KEY_OUT_PATTERN_2 = 'pattern2'

KEY_OUT_Lw = 'Weld.Lw'
KEY_OUT_DISP_Lw = 'Lw (mm)'
KEY_OUT_Hw = 'Weld.Hw'
KEY_OUT_DISP_Hw = 'Hw (mm)'


KEY_OUT_END_DIST = 'Bolt.EndDist'
KEY_OUT_DISP_END_DIST = 'End Distance (mm)'
KEY_OUT_GAUGE = 'Bolt.Gauge'
KEY_OUT_DISP_GAUGE = 'Gauge Distance (mm)'
KEY_OUT_GAUGE1 = 'Bolt.Gauge1'
KEY_OUT_DISP_GAUGE1 = 'Gauge Distance 1 (mm)'
KEY_OUT_GAUGE2 = 'Bolt.Gauge2'
KEY_OUT_DISP_GAUGE2 = 'Gauge Distance 2 (mm)'
KEY_OUT_GAUGE_CENTRAL = 'Bolt.GaugeCentral'
KEY_OUT_DISP_GAUGE_CENTRAL = 'Central Gauge (mm)'

KEY_OUT_MIN_GAUGE = 'Bolt.MinGauge'
KEY_OUT_MAX_SPACING = 'Bolt.MaxGauge'

KEY_OUT_EDGE_DIST = 'Bolt.EdgeDist'
KEY_OUT_MIN_EDGE_DIST = 'Bolt.MinEdgeDist'
KEY_OUT_MAX_EDGE_DIST = 'Bolt.MaxEdgeDist'


KEY_OUT_DISP_EDGE_DIST = 'Edge Distance (mm)'


KEY_OUT_SPTING_BOLT_SHEAR = 'Cleat.Spting_leg.Shear'
KEY_OUT_SPTING_BOLT_BEARING = 'Cleat.Spting_leg.Bearing'
KEY_OUT_SPTING_BOLT_CAPACITY = 'Cleat.Spting_leg.Capacity'
KEY_OUT_SPTING_BOLT_FORCE = 'Cleat.Spting_leg.Force'
KEY_OUT_SPTING_BOLT_LINE = 'Cleat.Spting_leg.Line'
KEY_OUT_SPTING_BOLTS_REQUIRED = 'Cleat.Spting_leg.Required'

KEY_OUT_SPTING_BOLT_GRP_CAPACITY = 'Cleat.Spting_leg.GroupCapacity'

KEY_OUT_SPTING_BOLTS_ONE_LINE = 'Cleat.Spting_leg.OneLine'

KEY_OUT_SPTING_SPACING = 'Cleat.Spting_leg.spacing'

KEY_OUT_SPTING_PITCH = 'Cleat.Spting_leg.Pitch'

KEY_OUT_SPTING_MIN_PITCH = 'Cleat.Spting_leg.MinPitch'
KEY_OUT_SPTING_END_DIST = 'Cleat.Spting_leg.EndDist'
KEY_OUT_SPTING_GAUGE = 'Cleat.Spting_leg.Gauge'
KEY_OUT_SPTING_MIN_GAUGE = 'Cleat.Spting_leg.MinGauge'
KEY_OUT_SPTING_MAX_SPACING = 'Cleat.Spting_leg.MaxGauge'
KEY_OUT_SPTING_EDGE_DIST = 'Cleat.Spting_leg.EdgeDist'
KEY_OUT_SPTING_MIN_EDGE_DIST = 'Cleat.Spting_leg.MinEdgeDist'
KEY_OUT_SPTING_MAX_EDGE_DIST = 'Cleat.Spting_leg.MaxEdgeDist'


KEY_OUT_DISP_PLATETHK_REP = 'Thickness (mm)'
KEY_OUT_PLATETHK = 'Plate.Thickness'
KEY_OUT_DISP_PLATETHK = 'Thickness (mm)'
KEY_OUT_PLATE_HEIGHT = 'Plate.Height'
KEY_OUT_DISP_PLATE_HEIGHT = 'Height (mm)'
KEY_OUT_DISP_PLATE_MIN_HEIGHT = 'Min.Height (mm)'

KEY_OUT_INTER_PLATE_HEIGHT = 'Plate.InterHeight'
KEY_OUT_DISP_INTER_PLATE_HEIGHT = 'Height (mm)'


KEY_OUT_INTER_PLATE_LENGTH = 'Plate.InterLength'
KEY_OUT_DISP_INTER_PLATE_LENGTH = 'Length (mm)'


KEY_OUT_INTERCONNECTION = 'Intermittent.Connection'
KEY_OUT_DISP_INTERCONNECTION = 'Connection (nos)'

KEY_OUT_INTERSPACING = 'Intermittent.Spacing'
KEY_OUT_DISP_INTERSPACING = 'Spacing (mm)'


KEY_OUT_PLATE_CAPACITY = 'Plate.Capacity'
KEY_OUT_PLATE_LENGTH = 'Plate.Length'
KEY_OUT_DISP_PLATE_LENGTH = 'Length (mm)'
KEY_OUT_DISP_PLATE_MIN_LENGTH = 'Min.Plate Length (mm)'
KEY_OUT_DISP_MEMB_MIN_LENGTH = 'Min.Member Length (mm)'

KEY_OUT_PLATE_WIDTH = 'Plate.Width'
KEY_OUT_DISP_PLATE_WIDTH = 'Width (mm)'
c = 'Width (mm)'

KEY_OUT_SEATED_ANGLE_DESIGNATION = "SeatedAngle.Designation"
KEY_OUT_DISP_ANGLE_DESIGNATION = "Designation"
KEY_OUT_SEATED_ANGLE_THICKNESS = "SeatedAngle.Thickness"
KEY_OUT_DISP_SEATED_ANGLE_THICKNESS = "Leg Thickness (mm)"
KEY_OUT_SEATED_ANGLE_LEGLENGTH = "SeatedAngle.LegLength"
KEY_OUT_DISP_SEATED_ANGLE_LEGLENGTH = "Leg Length (mm)"
KEY_OUT_SEATED_ANGLE_WIDTH = "SeatedAngle.Width"
KEY_OUT_DISP_ANGLE_WIDTH = "Width (mm)"
KEY_OUT_SEATED_ANGLE_BOLT_COL = "SeatedAngle.Bolt_Spacing_col"
KEY_OUT_DISP_SEATED_ANGLE_BOLT_COL = "Bolt Spacing Details"
KEY_OUT_SEATED_ANGLE_BOLT_BEAM = "SeatedAngle.Bolt_Spacing_beam"
KEY_OUT_DISP_SEATED_ANGLE_BOLT_BEAM = "Bolt Spacing Details"

KEY_OUT_TOP_ANGLE_DESIGNATION = "TopAngle.Designation"
# KEY_OUT_DISP_TOP_ANGLE_DESIGNATION = "Designation"
KEY_OUT_TOP_ANGLE_WIDTH = "TopAngle.Width"
# KEY_OUT_DISP_TOP_ANGLE_WIDTH = "Width (mm)"
KEY_OUT_TOP_ANGLE_BOLT_COL = "TopAngle.Bolt_Spacing_col"
KEY_OUT_DISP_TOP_ANGLE_BOLT_COL = "Bolt Spacing Details"
KEY_OUT_TOP_ANGLE_BOLT_BEAM = "TopAngle.Bolt_Spacing_beam"
KEY_OUT_DISP_TOP_ANGLE_BOLT_BEAM = "Bolt Spacing Details"

KEY_OUT_PLATE_SHEAR_DEMAND = 'Plate.ShearDemand'
KEY_OUT_DISP_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_PLATE_SHEAR = 'Plate.Shear'
KEY_OUT_DISP_PLATE_SHEAR = 'Shear Yielding Capacity (kN)'
KEY_OUT_PLATE_YIELD = 'Plate.Yield'
KEY_OUT_DISP_PLATE_YIELD = 'Yield Capacity'
KEY_OUT_PLATE_RUPTURE = 'Plate.Rupture'
KEY_OUT_DISP_PLATE_RUPTURE = 'Rupture Capacity (kN)'

KEY_OUT_PLATE_BLK_SHEAR = 'Plate.BlockShear'
KEY_OUT_DISP_PLATE_BLK_SHEAR = 'Block Shear Capacity (kN)'
KEY_OUT_PLATE_MOM_DEMAND = 'Plate.MomDemand'
KEY_OUT_DISP_PLATE_MOM_DEMAND = 'Moment Demand (kNm)'
KEY_OUT_DISP_PLATE_MOM_DEMAND_SEP = 'Moment Demand per Bolt (kNm)'
KEY_OUT_PLATE_MOM_CAPACITY = 'Plate.MomCapacity'
KEY_OUT_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity (kNm)'
KEY_OUT_DISP_PLATE_MOM_CAPACITY_SEP = 'Moment Capacity per Bolt (kNm)'
KEY_OUT_EP_MOM_CAPACITY = 'Plate.MomentCapacity'
KEY_OUT_DISP_EP_MOM_CAPACITY = 'Moment Capacity (kNm)'

KEY_OUT_PLATE_TENSION = 'Plate.TensionYield'

KEY_OUT_DISP_PLATE_TENSION = 'Tension Yielding Capacity (kN)'

KEY_OUT_PLATE_TENSION_RUP = 'Plate.TensionRupture'
KEY_OUT_DISP_PLATE_TENSION_RUP = 'Tension Rupture Capacity (kN)'

KEY_OUT_PLATE_BLK_SHEAR_AXIAL = 'Plate.BlockShearAxial'
KEY_OUT_DISP_PLATE_BLK_SHEAR_AXIAL = 'Axial Block Shear Capacity (kN)'

KEY_OUT_PLATE_CAPACITIES = 'capacities'
KEY_OUT_DISP_PLATE_CAPACITIES = 'Capacity'

KEY_OUT_WELD_SIZE = 'Weld.Size'
KEY_OUT_DISP_WELD_SIZE = 'Size (mm)'

KEY_OUT_INTER_WELD_SIZE = 'InterWeld.Size'
KEY_OUT_DISP_INTER_WELD_SIZE = 'Size (mm)'

KEY_OUT_WELD_SIZE_FLANGE = 'Weld.Size_flange'
KEY_OUT_DISP_WELD_SIZE_FLANGE = 'Size at Flange (mm)'
KEY_OUT_WELD_SIZE_WEB = 'Weld.Size_web'
KEY_OUT_DISP_WELD_SIZE_WEB = 'Size at Web (mm)'
KEY_OUT_WELD_SIZE_STIFFENER = 'Weld.Size_stiffener'
KEY_OUT_DISP_WELD_SIZE_STIFFENER = 'Size at Stiffener (mm)'
KEY_OUT_DISP_WELD_SIZE_STIFFENER1 = 'Weld Size at Stiffener (mm)'
KEY_OUT_WELD_STRENGTH = 'Weld.Strength'
KEY_OUT_DISP_WELD_STRENGTH = 'Strength (N/mm)'
KEY_OUT_WELD_STRESS = 'Weld.Stress'
KEY_OUT_DISP_WELD_STRESS = 'Stress (N/mm)'
KEY_OUT_WELD_LENGTH = 'Weld.Length'
KEY_OUT_DISP_WELD_LENGTH = 'Length (mm)'
KEY_OUT_WELD_LENGTH_EFF = 'Weld.EffLength'
KEY_OUT_DISP_WELD_LENGTH_EFF = 'Eff.Length (mm)'

KEY_OUT_DISP_MEMB_TEN_YIELD = 'Tension Yield Capacity (KN)'
KEY_OUT_DISP_MEMB_TEN_RUPTURE = 'Tension Rupture Capacity'
KEY_OUT_DISP_MEMB_BLK_SHEAR = 'Block Shear Capacity'


KEY_OUT_NO_BOLTS_FLANGE = 'ColumnEndPlate.nbf'
KEY_OUT_NO_BOLTS_FLANGE_TOTAL = 'ColumnEndPlate.nbftotal'
KEY_OUT_DISP_NO_BOLTS_FLANGE = 'No. of Bolts (along one side of the flange overhang) (n)'
KEY_OUT_DISP_NO_BOLTS_FLANGE_TOTAL = 'No. of Bolts (along flange)'
KEY_OUT_NO_BOLTS_WEB = 'ColumnEndPlate.nbw'
KEY_OUT_NO_BOLTS_WEB_TOTAL = 'ColumnEndPlate.nbwtotal'

KEY_OUT_DISP_NO_BOLTS_WEB = 'No. of Bolts (along one side of the web) (n)'
KEY_OUT_DISP_NO_BOLTS_WEB_TOTAL = 'No. of Bolts (along web)'

KEY_OUT_NO_BOLTS = 'ColumnEndPlate.nb'
KEY_OUT_DISP_NO_BOLTS = 'Total No. of Bolts'
KEY_PITCH_2_FLANGE = 'ColumnEndPlate.p2_flange'
KEY_DISP_PITCH_2_FLANGE = 'Pitch2 along Flange'
KEY_PITCH_2_WEB = 'ColumnEndPlate.p2_web'
KEY_DISP_PITCH_2_WEB = 'Pitch2 along Web'

KEY_PITCH_2_FLANGE1 = 'ColumnEndPlate.p2_flange'
KEY_DISP_PITCH_2_FLANGE1 = 'Pitch (bolts along centre) (p2)'
KEY_PITCH_2_WEB1 = 'ColumnEndPlate.p2_web'
KEY_DISP_PITCH_2_WEB1 = 'Pitch along centre bolt (p2)'
KEY_BOLT_FLANGE_SPACING = 'Bolt.flange_bolts'
KEY_DISP_BOLT_FLANGE_SPACING = 'Flange Bolts Spacing'
KEY_BOLT_WEB_SPACING = 'Bolt.web_bolts'
KEY_DISP_BOLT_WEB_SPACING = 'Web Bolts Spacing'



KEY_CONN_PREFERENCE = 'plate.design_method'
KEY_DISP_CONN_PREFERENCE = 'Design Method'
VALUES_CONN_PREFERENCE = ["Select","Plate Oriented", "Bolt Oriented"]
KEY_OUT_STIFFENER_HEIGHT = 'Stiffener.height'
KEY_OUT_DISP_STIFFENER_HEIGHT = 'Stiffener Height'
KEY_OUT_STIFFENER_WIDTH = 'Stiffener.width'
KEY_OUT_DISP_STIFFENER_WIDTH = 'Stiffener Width'
KEY_OUT_STIFFENER_THICKNESS = 'Stiffener.thickness'
KEY_OUT_DISP_STIFFENER_THICKNESS = 'Stiffener Thickness'
KEY_OUT_WELD_TYPE = 'Stiffener.weld'
KEY_OUT_WELD_TYPE1 = 'Stiffener.weld_flange'
KEY_OUT_DISP_WELD_TYPE = 'Weld Between Stiffener and Column flange'
KEY_OUT_DISP_WELD_TYPE1 = 'Weld Between Stiffener and End plate'
KEY_OUT_STIFFENER_DETAILS = 'Stiffener.Details'
KEY_OUT_STIFFENER_SKETCH = 'Stiffener.Sketch'
KEY_OUT_BP_TYPICAL_SKETCH = 'BasePlate.Sketch'
KEY_OUT_BP_TYPICAL_DETAILING = 'BasePlate.Detailing'
KEY_OUT_DISP_BP_DETAILING = 'Typical Detailing'
KEY_OUT_DISP_BP_DETAILING_SKETCH = 'Detailing'
KEY_OUT_CONTINUITY_DETAILS = 'ContinuityPlate.Details'
KEY_OUT_COL_WEB_STIFFENER_DETAILS = 'ColWebStiffenerPlate.Details'
KEY_OUT_DISP_STIFFENER_DETAILS = 'Stiffener Plate'
KEY_OUT_DISP_STIFFENER_DIMENSIONS = 'Dimensions'
KEY_OUT_DISP_STIFFENER_SKETCH = 'Typical Sketch'
KEY_OUT_DISP_CONTINUITY_PLATE_DETAILS = 'Continuity Plate'
KEY_OUT_DISP_WEB_STIFFENER_PLATE_DETAILS = 'Web Stiffener Plate'
KEY_OUT_STIFFENER_TITLE = 'Stiffener.Title'
KEY_P2_WEB = 'Bolt.pitch2_web'
KEY_P2_FLANGE = 'Bolt.pitch2_flange'
KEY_Y_SQR = 'Bolt.y_sqr'
KEY_BOLT_TENSION = 'Bolt.t_b'
KEY_BOLT_SHEAR = 'Bolt.v_sb'
KEY_PLATE_MOMENT = 'Plate.m_ep'
KEY_OUT_STIFFENER_LENGTH = 'Stiffener.Length'
KEY_OUT_STIFFENER_LENGTH_CHS = 'Stiffener.Length'
KEY_OUT_CONTINUITY_PLATE_NOS = 'ContinuityPlate.Number'
KEY_OUT_CONTINUITY_PLATE_LENGTH = 'ContinuityPlate.Length'
KEY_OUT_CONTINUITY_PLATE_WIDTH = 'ContinuityPlate.Width'
KEY_OUT_CONTINUITY_PLATE_THK = 'ContinuityPlate.Thickness'
KEY_OUT_WEB_STIFFENER_PLATE_NOS = 'WebStiffener.Number'
KEY_OUT_WEB_STIFFENER_PLATE_LENGTH = 'WebStiffener.Length'
KEY_OUT_WEB_STIFFENER_PLATE_WIDTH = 'WebStiffener.Width'
KEY_OUT_WEB_STIFFENER_PLATE_THK = 'WebStiffener.Thickness'
KEY_OUT_DISP_STIFFENER_LENGTH = 'Length (mm)'
KEY_OUT_DISP_CONTINUITY_PLATE_NUMBER = 'Number of Continuity Plate(s)'
KEY_OUT_DISP_WEB_STIFFENER_PLATE_NUMBER = 'Number of Stiffener(s)'
KEY_OUT_DISP_CONTINUITY_PLATE_LENGTH = 'Length (mm)'
KEY_OUT_DISP_WEB_PLATE_PLATE_DEPTH = 'Depth (mm)'
KEY_OUT_DISP_CONTINUITY_PLATE_WIDTH = 'Width (mm)'
KEY_OUT_DISP_CONTINUITY_PLATE_THK = 'Thickness (mm)'
KEY_OUT_STIFFENER_HEIGHT = 'Stiffener.Height'
KEY_OUT_STIFFENER_HEIGHT_CHS = 'Stiffener.Height'
KEY_OUT_STIFFENER_WIDTH = 'Stiffener.Width'
KEY_OUT_DISP_STIFFENER_HEIGHT = 'Height (mm)'
KEY_OUT_DISP_STIFFENER_WIDTH = 'Width (mm)'
KEY_OUT_STIFFENER_THICKNESS = 'Stiffener.Thickness'
KEY_OUT_STIFFENER_THICKNESS_CHS = 'Stiffener.Thickness'
KEY_OUT_DISP_STIFFENER_THICKNESS = 'Thickness (mm)'

KEY_OUT_DISP_LOCAL_WEB_YIELDING = 'Local Web Yielding'
KEY_OUT_DISP_COMP_BUCKLING_WEB = 'Compression Buckling of Web'
KEY_OUT_DISP_WEB_CRIPPLING = 'Web Crippling'
KEY_OUT_DISP_COMP_STRENGTH = 'Compression Strength (kN)'
#Continuity Plate
KEY_OUT_DISP_CONT_PLATE_REQ = 'Continuity Plate Required?'
KEY_OUT_DISP_DIAG_PLATE_REQ = 'Web Stiffener Plate Required?'
KEY_OUT_DISP_AREA_REQ= "Area Required (mm2)"
KEY_OUT_DISP_NOTCH_SIZE ="Notch Size (mm)"
KEY_OUT_DISP_DIAG_LOAD_STIFF="Load taken by Stiffener"
KEY_OUT_DISP_DIAGONAL_PLATE_DEPTH = 'Depth (mm)'
KEY_OUT_DISP_DIAGONAL_PLATE_WIDTH = 'Width (mm)'
# KEY_OUT_DISP_WEB_PLATE_CONT_T



KEY_OUT_WELD_DETAILS = 'Weld.Details'
DISP_TITLE_WELD = 'Weld'
DISP_TITLE_WELD_FLANGE = 'Weld at Flange'
DISP_TITLE_WELD_TYPICAL_DETAIL = 'Typical Sketch'
DISP_TITLE_WELD_WEB = 'Weld at Web'
KEY_OUT_WELD_SIZE = 'Weld.Size'
KEY_OUT_WELD_DETAILS = 'Weld.Details'
KEY_OUT_WELD_TYPE = 'Weld.Type'
KEY_OUT_DISP_WELD_SIZE = 'Size (mm)'
KEY_OUT_DISP_WELD_SIZE_EP = 'Size (mm)'
KEY_OUT_DISP_WELD_TYPE = 'Type'
KEY_OUT_WELD_STRENGTH = 'Weld.Strength'
KEY_OUT_DISP_WELD_STRENGTH = 'Strength (N/mm2)'

KEY_OUT_WELD_STRESS = 'Weld.Stress'
KEY_OUT_WELD_STRESS_NORMAL = 'Weld.NormalStress'
KEY_OUT_WELD_STRESS_SHEAR = 'Weld.ShearStress'
KEY_OUT_WELD_STRESS_COMBINED = 'Weld.StressCombined'
KEY_OUT_DISP_WELD_STRESS_COMBINED = 'Combined Stress (N/mm2)'
KEY_OUT_DISP_WELD_STRESS_EQUIVALENT = 'Equivalent Stress (N/mm2)'
KEY_OUT_DISP_WELD_STRESS = 'Stress (N/mm)'
KEY_OUT_DISP_WELD_NORMAL_STRESS = 'Normal Stress (N/mm2)'
KEY_OUT_DISP_WELD_SHEAR_STRESS = 'Shear Stress (N/mm2)'
KEY_OUT_DISP_WELD_STRESS_AXIAL = 'Weld.Stress due to axial force'
KEY_OUT_DISP_WELD_STRESS_SHEAR = 'Weld.Stress due to shear force'
KEY_OUT_DISP_WEB_WELD_LENGTH = 'Web Weld Length (mm)'
KEY_OUT_WELD_LENGTH = 'Weld.Length'
KEY_OUT_DISP_WELD_LENGTH = 'Total Length (mm)'
KEY_OUT_WELD_LENGTH_EFF = 'Weld.EffLength'
KEY_OUT_DISP_WELD_LENGTH_EFF = 'Eff.Length (mm)'
KEY_OUT_WELD_STRENGTH_RED = 'Weld.Strength_red'
KEY_OUT_DISP_WELD_STRENGTH_RED = 'Red.Strength (N/mm)'

DISP_OUT_TITLE_SPTDLEG = "Bolts on Supported Leg"
DISP_OUT_TITLE_SPTINGLEG = "Bolts on Supporting Leg"
DISP_OUT_TITLE_CLEAT = "Cleat Angle"
KEY_OUT_CLEAT_SECTION = "Cleat.Angle"
KEY_OUT_DISP_CLEAT_SECTION = "Cleat Angle Designation"
KEY_OUT_CLEATTHK = 'Plate.Thickness'
KEY_OUT_DISP_CLEATTHK = 'Thickness (mm)'
KEY_OUT_CLEAT_HEIGHT = 'Plate.Height'
KEY_OUT_DISP_CLEAT_HEIGHT = 'Height (mm)'
KEY_OUT_CLEAT_SPTDLEG = 'Cleat.SupportedLength'
KEY_OUT_DISP_CLEAT_SPTDLEG = 'Length (mm)'
KEY_OUT_CLEAT_SPTINGLEG = 'Cleat.SupportingLength'
KEY_OUT_DISP_CLEAT_SPTINGLEG = 'Length (mm)'

KEY_OUT_CLEAT_SHEAR = 'Cleat.Shear'
KEY_OUT_DISP_CLEAT_SHEAR = 'Shear '
KEY_OUT_CLEAT_BLK_SHEAR = 'Cleat.BlockShear'

KEY_OUT_CLEAT_MOM_DEMAND = 'Cleat.MomDemand'

KEY_OUT_CLEAT_MOM_CAPACITY = 'Cleat.MomCapacity'



KEY_DISP_SEC_PROFILE = 'Section Profile*'
KEY_DISP_SEC_TYPE = 'Section Type'
VALUES_SEC_PROFILE = ['Beams and Columns', 'RHS and SHS', 'CHS'] #,'Channels', 'Back to Back Channels'
VALUES_SEC_PROFILE_2 = ['Angles', 'Back to Back Angles', 'Star Angles', 'Channels', 'Back to Back Channels']
#, 'Channels', 'Back to Back Channels'
VALUES_SEC_PROFILE3 = ['Beams and Columns'] #,'Channels', 'Back to Back Channels'
VALUES_SEC_PROFILE4 = ['Channels']
KEY_LENZZ = 'Member.Length_zz'
KEY_DISP_LENZZ = 'Length (z-z)(mm)*'


KEY_LENYY = 'Member.Length_yy'
KEY_DISP_LENYY = 'Length (y-y)(mm)*'

DISP_TITLE_SC = 'Supporting Condition'
DISP_TITLE_STRUT = 'End Condition'
KEY_END1 = 'End_1'
KEY_END1_Y = 'End_1_Y'
KEY_DISP_END1 = 'End 1'
KEY_DISP_END1_Y = 'End 1'
VALUES_END1 = ['Fixed', 'Free', 'Hinged', 'Roller']
VALUES_STRUT_END1 = ['Fixed', 'Hinged']
VALUES_END1_Y = ['Fixed', 'Free', 'Hinged', 'Roller']
VALUES_STRUT_END1_Y = ['Fixed', 'Hinged']

KEY_END2 = 'End_2'
KEY_END2_Y = 'End_2_Y'
KEY_DISP_END2 = 'End 2'
KEY_DISP_END2_Y = 'End 2'
VALUES_END2 = ['Fixed', 'Free', 'Hinged', 'Roller']
VALUES_STRUT_END2 = ['Fixed', 'Hinged']
VALUES_END2_Y = ['Fixed', 'Free', 'Hinged', 'Roller']
VALUES_STRUT_END2_Y = ['Fixed', 'Hinged']

KEY_END_CONDITION = 'End Condition'
KEY_DISP_END_CONDITION = 'End Condition (about z-z axis)'
KEY_DISP_END_CONDITION_2 = 'End Condition (about y-y axis)'
DISP_TITLE_CLEAT = 'Cleat Angle'
DISP_TITLE_ANGLE = 'Angle Section'
DISP_TITLE_CHANNEL = 'Channel Section'
KEY_CLEATHT='CleatHt'
KEY_DISP_CLEATHT='Height(mm)'
KEY_DISP_CLEATSEC='Cleat Section *'
KEY_DISP_SEATEDANGLE = 'Seated Angle *'
KEY_DISP_TOPANGLE = 'Top Angle *'
#Design Report Strings
DISP_NUM_OF_BOLTS = 'No. of Bolts'
DISP_NUM_OF_ROWS = 'No. of Bolt Rows'
DISP_NUM_OF_COLUMNS = 'No. of Bolt Columns'
DISP_TITLE_COMPMEM='Compression member'
KEY_SECTYPE = 'Section Type'
KEY_DISP_SECTYPE = 'Section Type*'
KEY_DISP_SECSIZE = 'Section Size*'
KEY_DISP_SECSIZE_REPORT = 'Section Size'
KEY_LENMEM = 'Length of Member'
KEY_DISP_LENMEM = 'Length of Member'
DISP_TITLE_FL = 'Factored loads'
KEY_AXFOR = 'Axial Force'
KEY_DISP_AXFOR = 'Axial Force (kN)*'
KEY_PLTHK = 'Plate thk'
KEY_DISP_PLTHK = 'Plate thk (mm)'
KEY_PLTHICK = 'Plate thk'
KEY_DISP_PLTHICK = 'Plate Thickness (mm)'
KEY_DISP_PLATE_THICK = 'Plate Thickness (mm)'
KEY_DIAM = 'Diameter'
KEY_DISP_DIAM = 'Diameter (mm)'
KEY_NOROWS = 'No of Rows of Bolts'
KEY_DISP_NOROWS = 'No of Rows of Bolts'
KEY_NOCOLS = 'No of Column of Bolts'
KEY_DISP_NOCOLS = 'No of Column of Bolts'
KEY_ROWPI = 'Row Pitch'
KEY_DISP_ROWPI = 'Row Pitch'
KEY_COLPI = 'Column Pitch'
KEY_DISP_COLPI = 'Column Pitch'
KEY_ENDDIST = 'End Distance'
KEY_DISP_ENDDIST = 'End Distance'
KEY_EDGEDIST = 'Edge Distance'
KEY_DISP_EDGEDIST = 'Edge Distance'
KEY_CONNLOC = 'Conn Location'
KEY_DISP_CONNLOC = 'Conn Location'
KEY_LEN_INLINE = 'Total length in line with tension'
KEY_DISP_LEN_INLINE = 'Total Length in line with tension'
KEY_LEN_OPPLINE = 'Total length opp line with tension'
KEY_DISP_LEN_OPPLINE = 'Total Length opp line with tension'


VALUES_ANGLESEC_CUSTOMIZED= connectdb("Angles", call_type="popup")

def get_available_cleat_list(input_angle_list, max_leg_length=math.inf, min_leg_length=0.0, position="outer"):

    available_angles = []
    for designation in input_angle_list:
        leg_a_length,leg_b_length,t,r_r = get_leg_lengths(designation)
        if position == "inner":
            min_leg_length_outer = min_leg_length + t + r_r
            max_leg_length_outer = max_leg_length + t + r_r
        else:
            min_leg_length_outer = min_leg_length
            max_leg_length_outer = max_leg_length

        # print(min_leg_length,max_leg_length)
        if operator.le(max(leg_a_length,leg_b_length),max_leg_length_outer) and operator.ge(min(leg_a_length,leg_b_length), min_leg_length_outer) and leg_a_length==leg_b_length:
            # print("appended", designation)
            available_angles.append(designation)
        # else:
            # print("popped",designation)
    return available_angles


def get_leg_lengths(designation):

    """
        Function to fetch designation values from respective Tables.
    """
    conn = sqlite3.connect(PATH_TO_DATABASE)
    db_query = "SELECT a, b, t, R1 FROM Angles WHERE Designation = ?"
    cur = conn.cursor()
    cur.execute(db_query, (designation,))
    row = cur.fetchone()

    a = row[0]
    b = row[1]
    t = row[2]
    r_r = row[3]
    # axb = axb.lower()
    leg_a_length = float(a)
    leg_b_length = float(b)
    conn.close()
    return leg_a_length,leg_b_length,t,r_r

all_angles = connectdb("Angles","popup")
VALUES_CLEAT_CUSTOMIZED = get_available_cleat_list(all_angles, 200.0, 50.0)
print(all_angles)
print("customised")
print(VALUES_CLEAT_CUSTOMIZED)

BOLT_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
                "<tr>\n"
                "<td colspan=\"3\">\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">IS 800 Table 20 Typical Average Values for Coefficient of Friction (</span><span style=\" font-family:\'Calibri,sans-serif\'; font-size:9pt;\">µ</span><span style=\" font-family:\'Calibri,sans-serif\'; font-size:9pt; vertical-align:sub;\">f</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">)</span></p></td></tr></table>\n"
                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
                "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
                "<tr>\n"
                "<td width=\"26\"></td>\n"
                "<td width=\"383\">\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Treatment of Surfaces</span></p></td>\n"
                "<td width=\"78\">\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  µ_f</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">i)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces not treated</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.2</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">ii)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit with any loose rust removed, no pitting</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.5</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">iii)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit and hot-dip galvanized</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.1</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">iv)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit and spray - metallized with zinc (thickness 50-70 µm)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.25</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">v)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with ethylzinc silicate coat (thickness 30-60 µm)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">vi)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sand blasted surface, after light rusting</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.52</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">vii)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with ethylzinc silicate coat (thickness 60-80 µm)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">viii)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with alcalizinc silicate coat (thickness 60-80 µm)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">ix)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and spray metallized with aluminium (thickness &gt;50 µm)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.5</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">x)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Clean mill scale</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.33</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">xi)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sand blasted surface</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.48</span></p></td></tr>\n"
                "<tr>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">xii)</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Red lead painted surface</span></p></td>\n"
                "<td>\n"
                "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.1</span></p>\n"
                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></td></tr></table></body></html>")

WELD_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Shop weld takes a material safety factor of 1.25</span></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Field weld takes a material safety factor of 1.5</span></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">(IS 800 - cl. 5. 4. 1 or Table 5)</span></p></body></html>")

# DETAILING_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
#                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
#                "p, li { white-space: pre-wrap; }\n"
#                "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
#                "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.7</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[sheared or hand flame cut edges] </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">and </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.5 </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[Rolled, machine-flame cut, sawn and planed edges]</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> (IS 800 - cl. 10. 2. 4. 2)</span></p>\n"
#                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
#                "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">This gap should include the tolerance value of 5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5 mm{tolerance})</span></p>\n"
#                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
#                "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3</span></p>\n"
#                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")



DETAILING_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.7</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[sheared or hand flame cut edges] </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">and </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.5 </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[Rolled, machine-flame cut, sawn and planed edges]</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> (IS 800 - cl. 10. 2. 4. 2)</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">This gap should include the tolerance value of 5mm or 1.5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5mm {tolerance} or if the assumed clearance is 1.5mm, then the gap should be = 3mm (= 1.5mm {clearance} + 1.5mm {tolerance}. These are the default gap values based on the site practice for convenience of erection and IS 7215,Clause 2.3.1. The gap value can also be zero based on the nature of connection where clearance is not required.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")


COLUMN_OPTIMIZATION_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Allowable Utilization Ratio (UR)</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the maximum allowable value of the demand to capacity ratio for performing the design. The default value of this ratio is set at </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.0</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. The UR can be re-defined for any particular design session with a maximum allowable value of 1.0 and a minimum of 0.1.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Optimization Parameter</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the parameter used for selecting the most optimum section as the design output. The default parameter is set as the </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Utilization Ratio (UR)</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. Optimum sections can be selected based on the cost plus UR by choosing the '</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Cost</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">' parameter from the drop-down list.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Effective Area Parameter</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the parameter used to define the reduction in the area of the section due to connection detailing and other such requirements. The default value of this parameter is set at 1.0, which means that the effective area is 100% of the gross area for Plastic, Compact and Semi-compact sections. For Slender sections, the initial area will be computed based on the recommendations in Fig.2B of The National Building Code (2016). The value of the parameter should be defined in terms of the effective area to be considered for design simulation after deducting the area lost. The maximum value of the parameter is 1.0 (effective area is 100% of the gross area) with a minimum value of 0.1.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Section Definition</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> preference allows to choose the type of section to be considered in the design as per the classification listed in Table 2 (Cl.3.7.2 and Cl.3.7.4) of IS 800:2007. Choosing 'Yes' for a particular section type will allow the solver to choose that section when it performs the design checks. Choosing 'No' will simply discard the section from the list of sections as a possible output.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Optimum_Para = str("<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Optimization Parameter</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the parameter used for selecting the most optimum section as the design output. The default parameter is set as the </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Utilization Ratio (UR)</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. Optimum sections can be selected based on the cost plus UR by choosing the '</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Cost</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">' parameter from the drop-down list.</span></p>\n"
                    "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
                   )

Allowable_Utilization_Para = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Allowable Utilization Ratio (UR)</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the maximum allowable value of the demand to capacity ratio for performing the design. The default value of this ratio is set at </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.0</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. The UR can be re-defined for any particular design session with a maximum allowable value of 1.0 and a minimum of 0.1.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n")

Effective_Area_Para = str("<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Effective Area Parameter</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the parameter used to define the reduction in the area of the section due to connection detailing and other such requirements. The default value of this parameter is set at 1.0, which means that the effective area is 100% of the gross area for Plastic, Compact and Semi-compact sections. For Slender sections, the initial area will be computed based on the recommendations in Fig.2B of The National Building Code (2016). The value of the parameter should be defined in terms of the effective area to be considered for design simulation after deducting the area lost. The maximum value of the parameter is 1.0 (effective area is 100% of the gross area) with a minimum value of 0.1.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n")


Type_Load_Para = str("<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Type of Load</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the parameter used to define how the load maybe transferred in a Single Angle section. By default the Section will transfer the load concentrically through end gusset represented by </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Concentric Load</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. Type of Load can be selected based on the Concentric Load plus Leg Load by choosing the '</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Leg Load</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">' parameter from the drop-down list. </span></p>\n"                          
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n")

Section_Definition_Para = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                               "The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                               "Section Definition</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                               "preference allows to choose the type of section to be considered in the design as per the classification listed in Table 2 (Cl.3.7.2 and Cl.3.7.4) of IS 800:2007. Choosing 'Yes' for a particular section type will allow the solver to choose that section when it performs the design checks. Choosing 'No' will simply discard the section from the list of sections as a possible output.</span></p>\n"
                                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Single_Angle_Out_Plane = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                              "In the case of members of trusses, buckling in the plane perpendicular to the plane of the truss, </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                              "Out of Plane</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                              ", the effective length, KL shall be taken as the distance between the centres of intersection (Cl.7.2.4) of IS 800:2007.</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>"
                              )
Single_Angle_In_Plane = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                              "In the case of members of trusses, buckling in the plane of the truss, </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                              "In Plane</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                              ", the effective length, KL shall be taken as 0.7 to 1.0 times the distance between the centres of connections, depending on the degree of end restraint provided (Cl.7.2.4) of IS 800:2007.</span></p>\n"
                              "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Double_angle_opposite_gusset = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                                    "</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                                    "Double Angle Struts connected back to back, on opposite sides of the gusset</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                                    "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Double_angle_same_gusset = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                                "</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                                "Double Angle Struts connected back to back on one side of a gusset or section</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                                "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Opposite_Side_of_Gusset_Out_Plane = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                              "The effective length, KL, in the plane perpendicular to that of the end gusset,, </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                              "Out of Plane</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                              ",shall be taken as equal to the distance between centres of intersections (Cl.7.5.2.1) of IS 800:2007.</span></p>\n"
                              "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Opposite_Side_of_Gusset_In_Plane = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                              "The effective length, KL, in the plane of end gusset, </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                              "In Plane</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                              ", shall be taken as between 0.7 and 0.85 times the distance between intersections, depending on the degree of the restraint provided  (Cl.7.5.2.1) of IS 800:2007.</span></p>\n"
                              "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Same_Side_of_Gusset_Out_Plane = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                              "The effective length, KL, in the plane perpendicular to that of the end gusset,, </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                              "Out of Plane</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                              ",shall be taken as equal to the distance between centres of intersections (Cl.7.5.2.1) of IS 800:2007.</span></p>\n"
                              "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")

Same_Side_of_Gusset_In_Plane = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">"
                              "The effective length, KL, in the plane of end gusset, </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">"
                              "In Plane</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> "
                              ", shall be taken as between 0.7 and 0.85 times the distance between intersections, depending on the degree of the restraint provided  (Cl.7.5.2.1) of IS 800:2007.</span></p>\n"
                              "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")


STRUT_OPTIMIZATION_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               ) + Allowable_Utilization_Para + Effective_Area_Para
Effective_Length_Para = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Effective Length</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the parameter to </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Overwrite</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> the Length multiplyer. The default value of this ratio is set at </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">NA</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. The value can be re-defined for any particular design session with a minimum of 0.1. If invalid value given then it is set to NA or 1.0.</span></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">For simply supported beams of overall depth D and span length L, the effective length L<sub>LT</sub> is given by below Table</span></p>\n"             
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n")
Bearing_Length_Para = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Bearing Length Parameter</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is the length of Bearing stiffener provided for webs. The default value of this parameter is set at </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">NA</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. If invalid value given then it is set to NA.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n")
Shear_Buckling_Para = str( "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Shear Buckling</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> is only applicable when the input sections are susceptible to shear buckling.. The default value of this parameter is set at </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Simple Post Critical Method</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">. Refer</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Clause IS 8.4.2.2</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">for understanding which method is applicable in your case.</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n")

OPTIMIZATION_TABLE_UI = str("""
<div style="width:100%;" style="overflow-x:auto;">
    <table style="width:100%;" border="1">
      <tr>
      <th colspan="5" style="text-align:center;">Effective Length for Cantilever Beams </th>
    </tr>
    <tr>
        <th>Sl No.</th>
        <th colspan="2" style="text-align:center;">Conditions of Restraint</th>
        <th colspan="2" style="text-align:center;">Loading Condition</th>
      </tr>
      <tr >
        <th> </th>
        <th>Support</th>
        <th>Top</th>
        <th>Normal</th>
        <th>Destabilizing</th>
      </tr>
      <tr style="text-align:center;">
        <td rowspan="4">(i)</td>
        <td rowspan="4">Continous, with lateral restraint to top flange</td>
        <td>Free</td>
        <td>3.0 L</td>
        <td>7.5 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral restraint to top flange</td>
        <td>2.7 L</td>
        <td>7.5 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Torsional restraint</td>
        <td>2.4 L</td>
        <td>4.5 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral and Torsional restraint</td>
        <td>2.1 L</td>
        <td>3.6 L</td>
      </tr>
      <tr style="text-align:center;">
        <td rowspan="4">(ii)</td>
        <td rowspan="4">Continous, with partial torsional restraint</td>
        <td>Free</td>
        <td>2.0 L</td>
        <td>5.0 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral restraint to top flange</td>
        <td>1.8 L</td>
        <td>5.0 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Torsional restraint</td>
        <td>1.6 L</td>
        <td>3.0 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral and Torsional restraint</td>
        <td>1.4 L</td>
        <td>2.4 L</td>
      </tr>
      <tr style="text-align:center;">
        <td rowspan="4">(iii)</td>
        <td rowspan="4">Continous, with lateral and torsional restraint</td>
        <td>Free</td>
        <td>1.0 L</td>
        <td>2.5 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral restraint to top flange</td>
        <td>0.9 L</td>
        <td>2.5 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Torsional restraint</td>
        <td>0.8 L</td>
        <td>1.5 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral and Torsional restraint</td>
        <td>0.7 L</td>
        <td>1.2 L</td>
      </tr>
      <tr style="text-align:center;">
        <td rowspan="4">(iv)</td>
        <td rowspan="4">Restrained laterally, torsionally and against rotation</td>
        <td>Free</td>
        <td>0.8 L</td>
        <td>1.4 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral restraint to top flange</td>
        <td>0.7 L</td>
        <td>1.4 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Torsional restraint</td>
        <td>0.6 L</td>
        <td>0.6 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>Lateral and Torsional restraint</td>
        <td>0.5 L</td>
        <td>0.5 L</td>
      </tr>
        <!-- Add more rows as needed -->
</table>
</div>
</body></html>
""")

STRUT_OPTIMIZATION_DESCRIPTION = (
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
    '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
    'p, li { white-space: pre-wrap; }\n'
    '</style></head><body style="font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;">\n'
) + Allowable_Utilization_Para + Effective_Area_Para # + OPTIMIZATION_TABLE_UI

OPTIMIZATION_TABLE_UI2 = str("""
<div style="width:100%;" style="overflow-x:auto;">
    <table style="width:100%;" border="1">
      <tr>
        <th colspan="5" style="text-align:center;">Effective Length for Simply Supported Beams </th>
    </tr>
    <tr>
        <th>Sl No.</th>
        <th colspan="2" style="text-align:center;">Conditions of Restraint Supports</th>
        <th colspan="2" style="text-align:center;">Loading Condition</th>
      </tr>
      <tr style="text-align:center;">
        <th> </th>
        <th>Torsional Restraint</th>
        <th>Warping Restraint</th>
        <th>Normal</th>
        <th>Destabilizing</th>
      </tr>
      <tr style="text-align:center;">
        <td>(i)</td>
        <td>Fully restrained</td>
        <td>Both flanges fully restrained</td>
        <td>0.7 L</td>
        <td>0.85 L</td>
      </tr>
      <tr style="text-align:center;">
        <td>(ii)</td>
        <td>Fully restrained</td>
        <td>Compression flange fully restrained</td>
        <td>0.75 L</td>
        <td>0.9 L</td>        
      </tr>
      <tr style="text-align:center;">
        <td>(iii)</td>
        <td>Fully restrained</td>
        <td>Both flanges fully restrained</td>
        <td>0.8 L</td>
        <td>0.95 L</td>  
      </tr>
      <tr style="text-align:center;">
        <td>(iv)</td>
        <td>Fully restrained</td>
        <td>Both flanges fully restrained</td>
        <td>0.85 L</td>
        <td>1.0 L</td>  
      </tr>
      <tr style="text-align:center;">
        <td>(v)</td>
        <td>Fully restrained</td>
        <td>Warping not restrained in both flanges</td>
        <td>1.0 L</td>
        <td>1.2 L</td>  
      </tr>
      <tr style="text-align:center;">
        <td>(vi)</td>
        <td>Partially restrained by bottom flange support connection</td>
        <td>Warping not restrained in both flanges</td>
        <td>1.0 + 2 D</td>
        <td>1.2 L + 2 D</td>  
      </tr>
      <tr style="text-align:center;">
        <td>(vii)</td>
        <td>Partially restrained by bottom flange bearing support</td>
        <td>Warping not restrained in both flanges</td>
        <td>1.2 L + 2 D</td>
        <td>1.4 L + 2 D</td>  
      </tr>
        <!-- Add more rows as needed -->
</table>
</div>
""")+str("<p>\n</p>")
# </body></html>
FLEXURE_OPTIMIZATION_DESCRIPTION_SimplySupp = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               ) + Allowable_Utilization_Para + Effective_Area_Para + Effective_Length_Para + OPTIMIZATION_TABLE_UI2 + Bearing_Length_Para

FLEXURE_OPTIMIZATION_DESCRIPTION_Canti = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               ) + Allowable_Utilization_Para + Effective_Area_Para + Effective_Length_Para + OPTIMIZATION_TABLE_UI + Bearing_Length_Para
