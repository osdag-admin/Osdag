#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# @author: Amir, Umair, Arsil

import operator
import math


TYPE_COMBOBOX = 'ComboBox'
TYPE_TEXTBOX = 'TextBox'
TYPE_TITLE = 'Title'
TYPE_LABEL = 'Label'
TYPE_IMAGE = 'Image'
TYPE_IMAGE_COMPRESSION = 'Image_compression'
TYPE_COMBOBOX_CUSTOMIZED = 'ComboBox_Customized'
TYPE_OUT_BUTTON = 'Output_dock_Button'
TYPE_OUT_DOCK = 'Output_dock_Item'
TYPE_OUT_LABEL = 'Output_dock_Label'
TYPE_BREAK = 'Break'
TYPE_ENTER = 'Enter'
TYPE_TEXT_BROWSER = 'TextBrowser'
TYPE_NOTE = 'Note'
TYPE_WARNING = 'Warning'
PATH_TO_DATABASE = "ResourceFiles/Database/Intg_osdag.sqlite"
DESIGN_FLAG = 'False'
VALUE_NOT_APPLICABLE = 'N/A'
TYPE_TAB_1 = "TYPE_TAB_1"
TYPE_TAB_2 = "TYPE_TAB_2"
TYPE_TAB_3 = "TYPE_TAB_3"
TYPE_SECTION = 'Popup_Section'


import sqlite3

from utils.common.component import *
from utils.common.component import *

import logging
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
            msg = "<span style='color: yellow;'>"+ msg +"</span>"
        elif record.levelname == 'ERROR':
            msg = "<span style='color: red;'>"+ msg +"</span>"
        elif record.levelname == 'INFO':
            msg = "<span style='color: green;'>" + msg + "</span>"
        self.key.append(msg)
        # self.key.append(record.levelname)

def generate_missing_fields_error_string(missing_fields_list):
    """
    Args:
        missing_fields_list: list of fields that are not selected or entered
    Returns:
        error string that has to be displayed
    """
    # The base string which should be displayed
    information = "Please input the following required field"
    if len(missing_fields_list) > 1:
        # Adds 's' to the above sentence if there are multiple missing input fields
        information += "s"
    information += ": "
    # Loops through the list of the missing fields and adds each field to the above sentence with a comma

    for item in missing_fields_list:
        information = information + item + ", "

    # Removes the last comma
    information = information[:-2]
    information += "."

    return information

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
        cursor = conn.execute("SELECT Diameter_of_bolt FROM Bolt")

    elif table_name == "Material":
        cursor = conn.execute("SELECT Grade FROM Material")

    else:
        cursor = conn.execute("SELECT Designation FROM Columns")
    rows = cursor.fetchall()

    for row in rows:
        lst.append(row)

    final_lst = tuple_to_str(lst,call_type)
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

def tuple_to_str(tl, call_type):
    if call_type is "dropdown":
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


def get_oldcolumncombolist():
    '''(None) -> (List)
    This function returns the list of Indian Standard Column Designation.
    '''

    # @author: Arsil

    conn = sqlite3.connect(PATH_TO_DATABASE)
    old_columnList = []
    # columnQuery = QSqlQuery("SELECT Designation FROM Columns where Source = 'IS808_Old' order by id ASC")
    columnQuery = conn.execute("SELECT Designation FROM Columns WHERE Source = 'IS808_Old'")
    rows = columnQuery.fetchall()
    # a = columnQuery.size()
    # print(a)

    #comboList.append("Select section")
    # while(columnQuery.next()):
    #     old_columnList.append(columnQuery.value(0))
    for row in rows:
        old_columnList.append(row)

    final_lst = tuple_to_str_red(old_columnList)
    return final_lst



    #return old_columnList
def get_oldbeamcombolist():
    '''(None) -> (List)
       This function returns the list of Indian Standard Beams Designation.
       '''

    # @author: Arsil

    conn = sqlite3.connect(PATH_TO_DATABASE)
    old_columnList = []
    # columnQuery = QSqlQuery("SELECT Designation FROM Beams where Source = 'IS808_Old' order by id ASC")
    columnQuery = conn.execute("SELECT Designation FROM Beams WHERE Source = 'IS808_Old'")
    rows = columnQuery.fetchall()
    # a = columnQuery.size()
    # print(a)

    # comboList.append("Select section")
    # while(columnQuery.next()):
    #     old_columnList.append(columnQuery.value(0))
    for row in rows:
        old_columnList.append(row)

    final_lst = tuple_to_str_red(old_columnList)
    return final_lst


########
# Common Display Strings
############
KEY_DISP_SHEAR_YLD= 'Shear yielding Capacity (V_dy) (kN)'
KEY_DISP_BLK_SHEAR = 'Block Shear Capacity'
KEY_DISP_SHEAR_RUP = 'Shear Rupture Capacity (V_dn) (kN)'
KEY_DISP_MOM_DEMAND = 'Moment Demand'
KEY_DISP_MOM_CAPACITY = 'Moment Capacity'
DISP_MIN_PITCH = 'Min. Pitch (mm)'
DISP_MAX_PITCH = 'Max. Pitch (mm)'
DISP_MIN_GAUGE = 'Min. Gauge (mm)'
DISP_MAX_GAUGE = 'Max. Gauge (mm)'
DISP_MIN_EDGE = 'Min. Edge Distance (mm)'
DISP_MAX_EDGE = 'Max. Edge Distance (mm)'
DISP_MIN_END = 'Min. End Distance (mm)'
DISP_MAX_END = 'Max. End Distance (mm)'
DISP_MIN_PLATE_HEIGHT = 'Min. Plate Height (mm)'
DISP_MAX_PLATE_HEIGHT = 'Max. Plate Height (mm)'
DISP_MIN_PLATE_LENGTH = 'Min. Plate Length (mm)'
DISP_MIN_PLATE_THICK = 'Min.Plate Thickness (mm)'

DISP_MIN_PLATE_INNERHEIGHT = 'Min. Inner Plate Height (mm)'
DISP_MAX_PLATE_INNERHEIGHT = 'Max. Inner Plate Height (mm)'
DISP_MIN_PLATE_INNERLENGTH = 'Min. Inner Plate Length (mm)'

KEY_DISP_PLATE_BLK_SHEAR_SHEAR = 'Block Shear Capacity in Shear (V_db) (kN)'
KEY_DISP_PLATE_BLK_SHEAR_TENSION = 'Block Shear Capacity in Tension (T_db) (kN)'
KEY_DISP_SHEAR_CAPACITY = 'Shear Capacity (V_d) (kN)'
KEY_DISP_FU = 'Ultimate strength, fu (MPa)'
KEY_DISP_FY = 'Yield Strength , fy (MPa)'
KEY_DISP_IR = 'Interaction Ratio'
DISP_MIN_WELD_SIZE = 'Min Weld Size (mm)'
DISP_MAX_WELD_SIZE = 'Max Weld Size (mm)'
DISP_THROAT = 'Throat Thickness (mm)'
DISP_EFF = 'Effective Length (mm)'
DISP_WELD_STRENGTH = 'Weld Strength (kN/mm)'
###################################
# Key for Storing Module

KEY_MODULE = 'Module'
KEY_MAIN_MODULE = 'MainModule'
KEY_MODULE_STATUS = 'Module.Status'

TYPE_MODULE = 'Window Title'

KEY_DISP_FINPLATE = 'Fin Plate'
KEY_DISP_ENDPLATE = 'End Plate'
KEY_DISP_CLEATANGLE = 'Cleat Angle'
KEY_DISP_SEATED_ANGLE = 'Seated Angle'
KEY_DISP_BASE_PLATE = 'Base Plate'

KEY_DISP_BEAMCOVERPLATE = 'Beam Coverplate Connection'
KEY_DISP_COLUMNCOVERPLATE = 'Column Coverplate Connection'
KEY_DISP_BEAMCOVERPLATEWELD = 'Beam Coverplate  Weld Connection'
KEY_DISP_COLUMNCOVERPLATEWELD = 'Column Coverplate Weld Connection'
KEY_DISP_BEAMENDPLATE = 'Beam Endplate Connection'
KEY_DISP_COLUMNENDPLATE = 'Column Endplate Connection'

KEY_DISP_TENSION_BOLTED = 'Tension Members Bolted Design'
KEY_DISP_TENSION_WELDED = 'Tension Members Welded Design'
KEY_DISP_COMPRESSION = 'Compression Member'


DISP_TITLE_CM = 'Connecting members'

###################################
# Key for Storing Connectivity

KEY_CONN = 'Connectivity'

KEY_DISP_CONN = 'Connectivity *'

VALUES_CONN = ['Column flange-Beam web', 'Column web-Beam web', 'Beam-Beam']
VALUES_CONN_1 = ['Column flange-Beam web', 'Column web-Beam web']
VALUES_CONN_2 = ['Beam-Beam']
## Column End Plate ##
VALUES_CONN_3 = ['Flush End Plate','Extended Both Ways']
####


# VALUES_CONN_BP = ['Welded-Slab Base', 'Bolted-Slab Base', 'Gusseted Base Plate', 'Hollow Section']
VALUES_CONN_BP = ['Welded Column Base', 'Welded+Bolted Column Base', 'Moment Base Plate', 'Hollow/Tubular Column Base']



KEY_LOCATION = 'Conn_Location'
KEY_DISP_LOCATION = 'Conn_Location *'
VALUES_LOCATION = ['Select Location','Long Leg', 'Short Leg', 'Web']

KEY_IMAGE = 'Image'

KEY_LENGTH = 'Length(mm)'
KEY_DISP_LENGTH = 'Length(mm) *'

###################################
# Key for Storing Supporting_Section sub-key of Member

KEY_SUPTNGSEC = 'Member.Supporting_Section'
KEY_DISP_SUPTNGSEC = 'Supporting Section'
KEY_DISP_COLSEC = 'Column Section *'
VALUES_COLSEC = connectdb("Columns")


KEY_DISP_PRIBM = 'Primary beam *'
VALUES_PRIBM = connectdb("Beams")

###################################
# Key for Storing Supported_Section sub-key of Member

KEY_SUPTDSEC = 'Member.Supported_Section'
KEY_DISP_SUPTDSEC = 'Supported Section'
KEY_DISP_BEAMSEC = 'Beam Section *'
VALUES_BEAMSEC = connectdb("Beams")

KEY_DISP_SECBM = 'Secondary beam *'
VALUES_SECBM = connectdb("Beams")

###################################
# Key for Storing Material sub-key of Member
KEY_MATERIAL = 'Member.Material'
KEY_DISP_MATERIAL = 'Material *'
VALUES_MATERIAL = connectdb("Material")
KEY_SUPTNGSEC_MATERIAL = 'Member.Supporting_Section.Material'
KEY_SUPTDSEC_MATERIAL = 'Member.Supported_Section.Material'


###################################
# Keys for storing Load
DISP_TITLE_FSL = 'Factored load'

# Key for Storing Moment sub-key of Load
KEY_MOMENT = 'Load.Moment'
KEY_DISP_MOMENT = 'Moment(kNm)*'
KEY_MOMENT_MAJOR = 'Load.Moment.Major'
KEY_DISP_MOMENT_MAJOR = ' - Major axis (M<sub>z-z</sub>)'
KEY_MOMENT_MINOR = 'Load.Moment.Minor'
KEY_DISP_MOMENT_MINOR = ' - Minor axis (M<sub>y-y</sub>)'
KEY_DIA_ANCHOR = 'Anchor Bolt.Diameter'
DISP_TITLE_ANCHOR_BOLT = 'Anchor Bolt'
KEY_DISP_DIA_ANCHOR = 'Diameter(mm)*'
VALUES_DIA_ANCHOR = ['All', 'Customized']
KEY_TYP_ANCHOR = 'Anchor Bolt.Type'
KEY_DISP_TYP_ANCHOR = 'Type*'
VALUES_TYP_ANCHOR = ['Select Type', 'End Plate Type', 'L-Type', 'J-Type', 'IS 5624-Type A', 'IS 5624-Type B']
KEY_GRD_ANCHOR = 'Anchor Bolt.Grade'
KEY_DISP_GRD_ANCHOR = 'Grade*'
VALUES_GRD_ANCHOR = ['All', 'Customized']
DISP_TITLE_FOOTING = 'Pedestal/Footing'
KEY_GRD_FOOTING = 'Footing.Grade'
KEY_DISP_GRD_FOOTING = 'Grade*'
VALUES_GRD_FOOTING = ['Select Grade', 'M10', 'M15', 'M20', 'M25', 'M30', 'M35', 'M40', 'M45', 'M50', 'M55']


# Applied load
KEY_DISP_APPLIED_SHEAR_LOAD ='Applied Shear Load (kN)'
KEY_DISP_APPLIED_AXIAL_FORCE='Applied Axial Load (kN)'
KEY_DISP_APPLIED_MOMENT_LOAD='Applied Moment Load (kNm)'
KEY_DISP_AXIAL_FORCE_CON= 'Axial Load Considered (kN)'

# capacity
KEY_OUT_DISP_AXIAL_CAPACITY = "Axial Capacity Member Ac (kN)"
KEY_OUT_DISP_SHEAR_CAPACITY ="Shear Capacity Member Sc (kN)"
KEY_OUT_DISP_MOMENT_CAPACITY ="Moment Capacity Member Mc (kNm)"
KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY  = 'Plastic Moment Capacity Pmc (kNm)'
KEY_OUT_DISP_MOMENT_D_DEFORMATION= 'Moment Deformation Criteria Mdc (kNm)'


KEY_OUT_DIA_ANCHOR = 'Anchor Bolt.Diameter'
KEY_DISP_OUT_DIA_ANCHOR = 'Diameter(mm)'
KEY_OUT_GRD_ANCHOR = 'Anchor Bolt.Grade'
KEY_DISP_OUT_GRD_ANCHOR = 'Grade'
KEY_OUT_ANCHOR_BOLT_LENGTH = 'Anchor Bolt.Length'
KEY_DISP_OUT_ANCHOR_BOLT_LENGTH = 'Total Length'
KEY_OUT_ANCHOR_BOLT_SHEAR = 'Anchor Bolt.Shear'
KEY_OUT_DISP_ANCHOR_BOLT_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_ANCHOR_BOLT_BEARING = 'Anchor Bolt.Bearing'
KEY_OUT_DISP_ANCHOR_BOLT_BEARING = 'Bearing Capacity (kN)'
KEY_OUT_ANCHOR_BOLT_CAPACITY = 'Anchor Bolt.Capacity'
KEY_OUT_DISP_ANCHOR_BOLT_CAPACITY = 'Bolt Capacity'
KEY_OUT_ANCHOR_BOLT_COMBINED = 'Anchor Bolt.Combined'
KEY_OUT_DISP_ANCHOR_BOLT_COMBINED = 'Combined Capacity'
KEY_OUT_ANCHOR_BOLT_TENSION = 'Anchor Bolt.Tension'
KEY_OUT_DISP_ANCHOR_BOLT_TENSION = 'Tension Capacity (kN)'

DISP_TITLE_ANCHOR_BOLT_UPLIFT = 'Anchor Bolt for Uplift'
KEY_OUT_DIA_ANCHOR_UPLIFT = 'Anchor Bolt.Diameter_Uplift'
KEY_DISP_OUT_DIA_ANCHOR_UPLIFT = 'Diameter(mm)'
KEY_OUT_GRD_ANCHOR_UPLIFT = 'Anchor Bolt.Grade_Uplift'
KEY_DISP_OUT_GRD_ANCHOR_UPLIFT = 'Grade'
KEY_OUT_ANCHOR_BOLT_LENGTH_UPLIFT = 'Anchor Bolt.Length_Uplift'
KEY_DISP_OUT_ANCHOR_BOLT_LENGTH_UPLIFT = 'Total Length'
KEY_OUT_ANCHOR_BOLT_TENSION_UPLIFT = 'Anchor Bolt.Tension_Uplift'
KEY_OUT_DISP_ANCHOR_BOLT_TENSION_UPLIFT = 'Tension Capacity (kN)'

# Applied load
KEY_DISP_APPLIED_SHEAR_LOAD ='Shear Load Vu (kN)'
KEY_DISP_APPLIED_AXIAL_FORCE='Axial Load Au (kN)'
KEY_DISP_APPLIED_MOMENT_LOAD='Moment Load Mu (kNm)'

# capacity
DISP_TITLE_MEMBER_CAPACITY ="Member Capacity"
KEY_MEMBER_CAPACITY = "section.memcapacity"
KEY_DISP_MEMBER_CAPACITY = "Member Capacity"
KEY_MEMBER_AXIALCAPACITY='section.MomCapacity'
KEY_OUT_DISP_AXIAL_CAPACITY = "Axial Capacity Ac (kN)"
KEY_MEMBER_SHEAR_CAPACITY='section.MomCapacity'
KEY_OUT_DISP_SHEAR_CAPACITY ="Shear Capacity Sc (kN)"
KEY_MEMBER_MOM_CAPACITY='section.MomCapacity'
KEY_OUT_DISP_MOMENT_CAPACITY ="Moment Capacity Mc (kNm)"
KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY  = 'Plastic Moment Capacity Pmc (kNm)'
KEY_OUT_DISP_MOMENT_D_DEFORMATION= 'Moment Deformation Criteria Mdc (kNm)'

KEY_OUT_BASEPLATE_THICKNNESS = 'Baseplate.Thickness'
KEY_OUT_DISP_BASEPLATE_THICKNNESS = 'Thickness (mm)'
KEY_OUT_BASEPLATE_LENGTH = 'Baseplate.Length'
KEY_OUT_DISP_BASEPLATE_LENGTH = 'Length (mm)'
KEY_OUT_BASEPLATE_WIDTH = 'Baseplate.Width'
KEY_OUT_DISP_BASEPLATE_WIDTH = 'Width (wp)'

DISP_TITLE_DETAILING = 'Detailing'
KEY_OUT_DETAILING_NO_OF_ANCHOR_BOLT = 'Deatiling.No of Anchor bolts'
KEY_OUT_DISP_DETAILING_NO_OF_ANCHOR_BOLT = 'No. of Anchor bolts'
KEY_OUT_DETAILING_PITCH_DISTANCE = 'Detailing.Pitch Distance'
KEY_OUT_DISP_DETAILING_PITCH_DISTANCE = 'Pitch Distance (mm)'
KEY_OUT_DETAILING_GAUGE_DISTANCE = 'Detailing.Gauge Distance'
KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE = 'Gauge Distance (mm)'
KEY_OUT_DETAILING_END_DISTANCE = 'Detailing.End Distance'
KEY_OUT_DISP_DETAILING_END_DISTANCE = 'End Distance (mm)'
KEY_OUT_DETAILING_EDGE_DISTANCE = 'Detailing.Edge Distance'
KEY_OUT_DISP_DETAILING_EDGE_DISTANCE = "Edge Distance (mm)"
KEY_OUT_DETAILING_PROJECTION = 'Detailing.Projection'
KEY_OUT_DISP_DETAILING_PROJECTION = 'Projection (mm)'

# DISP_TITLE_GUSSET_PLATE = 'Gusset Plate'
# KEY_OUT_GUSSET_PLATE_THICKNNESS = 'GussetPlate.Thickness'
# KEY_OUT_DISP_GUSSET_PLATE_THICKNESS = 'Thickness (mm)'
# KEY_OUT_GUSSET_PLATE_SHEAR_DEMAND = 'GussetPlate.Shear_Demand'
# KEY_OUT_DISP_GUSSET_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
# KEY_OUT_GUSSET_PLATE_SHEAR = 'GussetPlate.Shear'
# KEY_OUT_DISP_GUSSET_PLATE_SHEAR = 'Shear Capacity (kN)'
# KEY_OUT_GUSSET_PLATE_MOMENT_DEMAND = 'GussetPlate.Moment_Demand'
# KEY_OUT_DISP_GUSSET_PLATE_MOMENT_DEMAND = 'Moment Demand (kN-m)'
# KEY_OUT_GUSSET_PLATE_MOMENT = 'GussetPlate.Moment'
# KEY_OUT_DISP_GUSSET_PLATE_MOMENT = 'Moment Capacity (kN-m)'

KEY_OUT_STIFFENER_PLATE_FLANGE = 'Stiffener_Plate.Column_flange'
KEY_DISP_OUT_STIFFENER_PLATE_FLANGE = 'Stiffener Plate'
DISP_TITLE_STIFFENER_PLATE_FLANGE = 'Stiffener Plate along Column flange'
KEY_OUT_STIFFENER_PLATE_FLANGE_THICKNNESS = 'Stiffener_Plate_Flange.Thickness'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_THICKNESS = 'Thickness (mm)'
KEY_OUT_STIFFENER_PLATE_FLANGE_SHEAR_DEMAND = 'Stiffener_Plate_Flange.Shear_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_STIFFENER_PLATE_FLANGE_SHEAR = 'Stiffener_Plate_Flange.Shear'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_STIFFENER_PLATE_FLANGE_MOMENT_DEMAND = 'Stiffener_Plate_Flange.Moment_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_MOMENT_DEMAND = 'Moment Demand (kN-m)'
KEY_OUT_STIFFENER_PLATE_FLANGE_MOMENT = 'Stiffener_Plate_Flange.Moment'
KEY_OUT_DISP_STIFFENER_PLATE_FLANGE_MOMENT = 'Moment Capacity (kN-m)'

KEY_OUT_STIFFENER_PLATE_ALONG_WEB = 'Stiffener_Plate.Along_Column_web'
KEY_DISP_OUT_STIFFENER_PLATE_ALONG_WEB = 'Stiffener Plate'
DISP_TITLE_STIFFENER_PLATE_ALONG_WEB = 'Stiffener Plate along Column web'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_THICKNNESS = 'Stiffener_Plate_along_Web.Thickness'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_THICKNESS = 'Thickness (mm)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_SHEAR_DEMAND = 'Stiffener_Plate_along_Web.Shear_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_SHEAR = 'Stiffener_Plate_along_Web.Shear'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_MOMENT_DEMAND = 'Stiffener_Plate_along_Web.Moment_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_MOMENT_DEMAND = 'Moment Demand (kN-m)'
KEY_OUT_STIFFENER_PLATE_ALONG_WEB_MOMENT = 'Stiffener_Plate_along_Web.Moment'
KEY_OUT_DISP_STIFFENER_PLATE_ALONG_WEB_MOMENT = 'Moment Capacity (kN-m)'

KEY_OUT_STIFFENER_PLATE_ACROSS_WEB = 'Stiffener_Plate.Across_Column_web'
KEY_DISP_OUT_STIFFENER_PLATE_ACROSS_WEB = 'Stiffener Plate'
DISP_TITLE_STIFFENER_PLATE_ACROSS_WEB = 'Stiffener Plate across Column web'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_THICKNNESS = 'Stiffener_Plate_across_Web.Thickness'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_THICKNESS = 'Thickness (mm)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_SHEAR_DEMAND = 'Stiffener_Plate_across_Web.Shear_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR_DEMAND = 'Shear Demand (kN)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_SHEAR = 'Stiffener_Plate_across_Web.Shear'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND = 'Stiffener_Plate_across_Web.Moment_Demand'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT_DEMAND = 'Moment Demand (kN-m)'
KEY_OUT_STIFFENER_PLATE_ACROSS_WEB_MOMENT = 'Stiffener_Plate_across_Web.Moment'
KEY_OUT_DISP_STIFFENER_PLATE_ACROSS_WEB_MOMENT = 'Moment Capacity (kN-m)'

#
# DISP_TITLE_STIFFENER_PLATE = 'Stiffener Plate'
# KEY_OUT_STIFFENER_PLATE_THICKNNESS = 'StiffenerPlate.Thickness'
# KEY_OUT_DISP_STIFFENER_PLATE_THICKNESS = 'Thickness (mm)'
# KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND = 'StiffenerPlate.Shear_Demand'
# KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND = 'Shear Demand (kN)'
# KEY_OUT_STIFFENER_PLATE_SHEAR = 'StiffenerPlate.Shear'
# KEY_OUT_DISP_STIFFENER_PLATE_SHEAR = 'Shear Capacity (kN)'
# KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND = 'StiffenerPlate.Moment_Demand'
# KEY_OUT_DISP_STIFFENER_PLATE_MOMENT_DEMAND = 'Moment Demand (kN-m)'
# KEY_OUT_STIFFENER_PLATE_MOMENT = 'StiffenerPlate.Moment'
# KEY_OUT_DISP_STIFFENER_PLATE_MOMENT = 'Moment Capacity (kN-m)'


###################################
# Key for Storing Shear sub-key of Load
KEY_SHEAR = 'Load.Shear'
KEY_DISP_SHEAR = 'Shear(kN)*'

KEY_SHEAR_BP = 'Load.Shear_BP'
KEY_DISP_SHEAR_BP = 'Shear(kN)'
KEY_SHEAR_MAJOR = 'Load.Shear.Major'
KEY_DISP_SHEAR_MAJOR = ' - Along major axis (z-z)'
KEY_SHEAR_MINOR = 'Load.Shear.Minor'
KEY_DISP_SHEAR_MINOR = ' - Along minor axis (y-y)'


###################################
# Key for Storing Axial sub-key of Load
KEY_AXIAL = 'Load.Axial'
KEY_DISP_AXIAL = 'Axial (kN) *'
KEY_AXIAL_BP = 'Load.Axial_Compression'
KEY_DISP_AXIAL_BP = 'Axial Compression (kN) *'
KEY_AXIAL_TENSION_BP = 'Load.Axial_Tension'
KEY_DISP_AXIAL_TENSION_BP = 'Axial Tension/Uplift (kN) *'


###################################
# Keys for Storing Bolt

DISP_TITLE_BOLT = 'Bolt'
DISP_TITLE_BOLT_CAPACITY = 'Bolt Capacity'

DISP_TITLE_WELD = 'Weld'
DISP_TITLE_WELD_CAPACITY = 'Weld Capacity'
DISP_TITLE_END_CONNECTION = 'End Connection'

DISP_TITLE_SECTION = 'SECTION'
DISP_TITLE_TENSION_SECTION = 'Section Capacity'
KEY_BOLT_FU = 'Bolt.fu'
KEY_BOLT_FY = 'Bolt.fy'
# Key for storing Diameter sub-key of Bolt
KEY_D = 'Bolt.Diameter'
KEY_DISP_D = 'Diameter (mm)*'
VALUES_D = ['All', 'Customized']

# Key for storing Type sub-key of Bolt
KEY_TYP = 'Bolt.Type'
KEY_DISP_TYP = 'Type *'
TYP_BEARING = "Bearing Bolt"
TYP_FRICTION_GRIP = "Friction Grip Bolt"
VALUES_TYP = ['Select Type', TYP_FRICTION_GRIP, TYP_BEARING]
VALUES_TYP_1 = ['Friction Grip Bolt']
VALUES_TYP_2 = ['Bearing Bolt']

# Key for storing Grade sub-key of Bolt
KEY_GRD = 'Bolt.Grade'
KEY_DISP_GRD = 'Grade *'
VALUES_GRD = ['All', 'Customized']
VALUES_GRD_CUSTOMIZED = ['3.6', '4.6', '4.8', '5.6', '5.8', '6.8', '8.8', '9.8', '10.9', '12.9']

#################################
# Key for storing Plate
DISP_TITLE_PLATE = 'Plate'
DISP_TITLE_GUSSET_PLATE = 'Gusset Plate'


# Key for storing Thickness sub-key of Plate
KEY_PLATETHK = 'Plate.Thickness'
KEY_PLATE_MATERIAL = 'Plate.Material'
KEY_PLATE_FU = 'Plate.Ultimate_Strength'
KEY_DISP_PLATE_FU = 'Ultimate strength, fu (MPa)'
KEY_PLATE_FY = 'Plate.Yield_Strength'
KEY_DISP_PLATE_FY = 'Yield Strength , fy (MPa)'
KEY_PLATE_MIN_HEIGHT = 'Plate.MinHeight'
KEY_PLATE_MAX_HEIGHT = 'Plate.MaxHeight'
KEY_DISP_PLATETHK = 'Thickness(mm)*'
VALUES_PLATETHK = ['All', 'Customized']
VALUES_PLATETHK_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30']



KEY_LOCATION = 'Conn_Location'
KEY_DISP_LOCATION = 'Conn_Location *'
VALUES_LOCATION = ['Select Location','Long Leg', 'Short Leg','Web']
VALUES_LOCATION_1 = ['Long Leg', 'Short Leg']
VALUES_LOCATION_2 = ["Web"]


KEY_IMAGE = 'Image'

KEY_LENGTH = 'Length(mm)'
KEY_DISP_LENGTH = 'Length (mm) *'

KEY_SLENDER = "Member.Slenderness"
KEY_DISP_SLENDER = 'Slenderness'



DISP_TITLE_TENSION = 'Tension Capacity'








DISP_TITLE_FLANGESPLICEPLATE = 'Flange splice plate '

KEY_FLANGEPLATE_PREFERENCES = 'Flange_Plate.Preferences'
KEY_DISP_FLANGESPLATE_PREFERENCES = 'Preferences'
VALUES_FLANGEPLATE_PREFERENCES = ['Cover plate location', 'Outside','Outside + Inside']

KEY_FLANGEPLATE_THICKNESS = 'flange_plate.thickness_provided'
KEY_DISP_FLANGESPLATE_THICKNESS = 'Thickness (mm)*'
VALUES_FLANGEPLATE_THICKNESS = ['All', 'Customized']

KEY_INNERFLANGEPLATE_THICKNESS = 'flange_plate.innerthickness_provided'
KEY_DISP_INNERFLANGESPLATE_THICKNESS = 'Thickness (mm)'

KEY_FLANGE_PLATE_HEIGHT = 'flange_plate.Height'
KEY_DISP_FLANGE_PLATE_HEIGHT = 'Height (mm)'
KEY_FLANGE_PLATE_LENGTH ='flange_plate.Length'
KEY_DISP_FLANGE_PLATE_LENGTH ='Length (mm)'

KEY_OUT_FLANGE_BOLT_SHEAR ="flange_bolt.shear capacity"


KEY_INNERPLATE= "flange_plate.Inner_plate_details"
KEY_DISP_INNERFLANGESPLICEPLATE = "Inner Plate Detials"
DISP_TITLE_INNERFLANGESPLICEPLATE = 'Inner Flange splice plate'
KEY_INNERFLANGE_PLATE_HEIGHT = 'flange_plate.InnerHeight'
KEY_DISP_INNERFLANGE_PLATE_HEIGHT = 'Height (mm)'
KEY_INNERFLANGE_PLATE_LENGTH ='flange_plate.InnerLength'
KEY_DISP_INNERFLANGE_PLATE_LENGTH ='Length (mm)'

KEY_FLANGE_SPACING ="Flange_plate.spacing"
KEY_DISP_FLANGE_SPACING = 'Spacing (mm)'
KEY_FLANGE_PITCH = 'Flange_plate.pitch_provided'
KEY_DISP_FLANGE_PLATE_PITCH = 'Pitch'
KEY_FLANGE_PLATE_GAUGE = "Flange_plate.gauge_provided "
KEY_DISP_FLANGE_PLATE_GAUGE ="Gauge"
KEY_ENDDIST_FLANGE= 'Flange_plate.end_dist_provided '
KEY_DISP_END_DIST_FLANGE = 'End Distance'
KEY_EDGEDIST_FLANGE= 'Flange_plate.edge_dist_provided'
KEY_DISP_EDGEDIST_FLANGE= 'Edge Distance'

KEY_FLANGE_CAPACITY ="Flange_plate.capacity"
KEY_DISP_FLANGE_CAPACITY= 'Capacity'
KEY_FLANGE_TEN_CAPACITY ="Section.flange_capacity"
KEY_DISP_FLANGE_TEN_CAPACITY ="Flange Tension Capacity (kN)"

KEY_FLANGE_PLATE_TEN_CAP ="Flange_plate.tension_capacity"
KEY_DISP_FLANGE_PLATE_TEN_CAP ="Plate Tension Capacity (kN)"


KEY_BLOCKSHEARCAP_FLANGE='Flange_plate.block_shear_capacity'
KEY_DISP_BLOCKSHEARCAP_FLANGE='Flange Block Shear Capacity (kN)'
KEY_TENSIONYIELDINGCAP_FLANGE = 'Flange_plate.tension_yielding_capacity'
KEY_DISP_TENSIONYIELDINGCAP_FLANGE = 'Flange Tension Yielding Capacity (kN)'
KEY_TENSIONRUPTURECAP_FLANGE= 'Flange_plate.tension_rupture_capacity'
KEY_DISP_TENSIONRUPTURECAP_FLANGE= 'Flange Tension Rupture Capacity (kN)'
KEY_SHEARYIELDINGCAP_FLANGE= 'Flange_plate.shear_yielding_capacity'
KEY_DISP_SHEARYIELDINGCAP_FLANGE= 'Shear Yielding Capacity (kN)'
KEY_SHEARRUPTURECAP_FLANGE= 'Flange_plate.shear_rupture_capacity'
KEY_DISP_SHEARRUPTURECAP_FLANGE= 'Shear Rupture Capacity (kN)'
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

KEY_TENSION_CAPACITY = "Member.tension_capacity"
KEY_DISP_TENSION_CAPACITY = "Tension Capacity (kN)"

KEY_EFFICIENCY = "Member.efficiency"
KEY_DISP_EFFICIENCY = "Utilization Ratio"

DISP_TITLE_BOLTDETAILS ='Bolt Details'
KEY_BOLT_DETAILS ="Bolt.Details"

DISP_TITLE_BOLT_CAPACITIES = 'Bolt Capacities'
KEY_BOLT_CAPACITIES = 'Bolt.Capacities'

KEY_DISP_BOLT_DETAILS = "Bolt Details"
KEY_FLANGE_BOLT_LINE = 'Flange_plate.Bolt_Line'
KEY_FLANGE_DISP_BOLT_LINE = 'Bolt Lines in flange'
KEY_FLANGE_BOLTS_ONE_LINE = 'Flange_plate.Bolt_OneLine'
KEY_FLANGE_DISP_BOLTS_ONE_LINE = 'Bolts in one Line in flange'
KEY_FLANGE_BOLTS_REQ = "Flange_plate.Bolt_required"
KEY_FLANGE_DISP_BOLTS_REQ = "Flange Bolt Required"
KEY_FLANGE_NUM_BOLTS_REQ = "Flange_plate.Bolt_required"


KEY_FLANGE_WELD_DETAILS = "Flange detail"
KEY_DISP_FLANGE_WELD_DETAILS = "Weld Details"

KEY_INNERFLANGE_WELD_DETAILS = "Inner Flange detail"
KEY_DISP_INNERFLANGE_WELD_DETAILS = "Weld Details"

KEY_WELD_TYPE = 'Weld.Type'
KEY_DISP_WELD_TYPE = 'Type'
VALUES_WELD_TYPE = ["Select type", "Fillet Weld", "Butt Weld"]
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
KEY_FLANGE_WELD_HEIGHT ='flange_Weld.height'
KEY_DISP_FLANGE_WELD_HEIGHT = 'Flange Weld Height'

KEY_INNERFLANGE_WELD_LENGTH = 'Flange_Weld.InnerLength'
KEY_DISP_INNERFLANGE_WELD_LENGTH ='Length (mm)'
KEY_INNERFLANGE_WELD_LENGTH_EFF = 'Flange_Weld.InnerEffLength'
KEY_INNERFLANGE_WELD_HEIGHT ='flange_Weld.Innerheight'
KEY_DISP_INNERFLANGE_WELD_HEIGHT = 'Height (mm)'
KEY_INNERFLANGE_WELD_STRESS = 'Inner_Flange_Weld.Stress'
KEY_INNERFLANGE_DISP_WELD_STRESS = 'Flange Weld Stress (N/mm)'
KEY_INNERFLANGE_WELD_STRENGTH = 'Inner_Flange_Weld.Strength'
KEY_INNERFLANGE_DISP_WELD_STRENGTH = 'Flange Weld Strength (N/mm)'

KEY_OUT_FLANGE_BOLT_SHEAR ='flange_bolt.bolt_shear_capacity'
KEY_OUT_DISP_FLANGE_BOLT_SHEAR = "Shear Capacity (kN)"
KEY_OUT_FLANGE_BOLT_BEARING = 'flange_bolt.bolt_bearing_capacity'
KEY_OUT_DISP_FLANGE_BOLT_BEARING = "Bearing Capacity (kN)"
KEY_OUT_FLANGE_BOLT_CAPACITY = 'flange_bolt.bolt_capacity'
KEY_OUT_DISP_FLANGE_BOLT_CAPACITY ="Bolt Capacity (kN)"
KEY_OUT_DISP_FLANGE_BOLT_SLIP= 'Slip Resistance'
KEY_FLANGE_BOLT_GRP_CAPACITY = 'flange_bolt.grp_bolt_capacity'
KEY_OUT_FLANGE_BOLT_GRP_CAPACITY = 'flange bolt grp bolt capacity (kN)'
KEY_OUT_MIN_PITCH= 'Min_pitch'
KEY_OUT_GRD_PROVIDED='flange_bolt.bolt_fu'
KEY_OUT_FLANGE_MIN_PITCH= 'flange_bolt.min_pitch_round'
KEY_OUT_FLANGE_MIN_EDGE_DIST= 'flange_bolt.min_edge_dist_round'
KEY_OUT_FLANGE_MAX_EDGE_DIST='flange_bolt.max_edge_dist_round'

KEY_OUT_DISP_FORCES_FLANGE = 'Forces Carried by Flange'
KEY_OUT_DISP_FORCES_WEB= 'Forces Carried by Web'

KEY_OUT_WEB_BOLT_SHEAR ='web_bolt.bolt_shear_capacity'
KEY_OUT_DISP_WEB_BOLT_SHEAR = "Shear Capacity (kN)"
KEY_OUT_WEB_BOLT_BEARING = 'web_bolt.bolt_bearing_capacity'
KEY_OUT_DISP_WEB_BOLT_BEARING = "Bearing Capacity (kN)"
KEY_OUT_WEB_BOLT_CAPACITY = 'web_bolt.bolt_capacity'
KEY_OUT_DISP_WEB_BOLT_CAPACITY ="Bolt Capacity (kN)"
KEY_OUT_DISP_WEB_BOLT_SLIP= 'Slip Resistance'
KEY_WEB_BOLT_GRP_CAPACITY = 'web_bolt.grp_bolt_capacity'
KEY_OUT_WEB_BOLT_GRP_CAPACITY = 'Web bolt grp bolt capacity (kN)'


DISP_TITLE_WEBSPLICEPLATE = 'Web splice plate'

KEY_WEBPLATE_THICKNESS = 'Web_Plate.thickness_provided'
KEY_DISP_WEBPLATE_THICKNESS = 'Thickness (mm)*'
VALUES_WEBPLATE_THICKNESS = ['All', 'Customized']
VALUES_PLATETHICKNESS_CUSTOMIZED = ['6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30','32','36','40']

KEY_WEB_PLATE_HEIGHT = 'Web_Plate.Height'
KEY_DISP_WEB_PLATE_HEIGHT = 'Height (mm)'
KEY_WEB_PLATE_LENGTH ='Web_Plate.Length'
KEY_DISP_WEB_PLATE_LENGTH ='Length (mm)'
KEY_OUT_WEB_BOLT_SHEAR ="Web_bolt.shear capacity"


KEY_WEB_SPACING ="Web_plate.spacing"
KEY_DISP_WEB_SPACING = 'Spacing (mm)'
KEY_WEB_PITCH = "Web_plate.pitch_provided"
KEY_DISP_WEB_PLATE_PITCH ="Pitch"
KEY_WEB_GAUGE = "Web_plate.gauge_provided "
KEY_DISP_WEB_PLATE_GAUGE ="Gauge"
KEY_ENDDIST_W= 'Web_plate.end_dist_provided '
KEY_DISP_END_DIST_W = 'End Distance'
KEY_EDGEDIST_W = 'Web_plate.edge_dist_provided'
KEY_DISP_EDGEDIST_W = 'Edge Distance'

KEY_WEB_CAPACITY ="Web_plate.capacity"
KEY_DISP_WEB_CAPACITY= 'Capacity'
KEY_WEB_TEN_CAPACITY ="Section.Tension_capacity_web"
KEY_DISP_WEB_TEN_CAPACITY ="Web Tension Capacity (kN)"
KEY_WEBPLATE_SHEAR_CAPACITY ="Section.shear_capacity_web_plate"
KEY_DISP_WEBPLATE_SHEAR_CAPACITY ="Plate Shear Capacity (kN)"
KEY_TEN_CAP_WEB_PLATE ="Web_plate.tension_capacity"
KEY_DISP_TEN_CAP_WEB_PLATE ="Plate Tension Capacity (kN)"


KEY_SHEARYIELDINGCAP_WEB= 'web_plate.shear_yielding_capacity'
KEY_DISP_SHEARYIELDINGCAP_WEB= 'Web Shear Yielding Capacity (kN)'
KEY_BLOCKSHEARCAP_WEB='web_plate.block_shear_capacity'
KEY_DISP_BLOCKSHEARCAP_WEB='Web Block Shear Capacity (kN)'
KEY_SHEARRUPTURECAP_WEB= 'web_plate.shear_rupture_capacity'
KEY_DISP_SHEARRUPTURECAP_WEB= 'Web Shear Rupture Capacity (kN)'
KEY_TENSIONYIELDINGCAP_WEB = "web_plate.tension_yielding_capacity"
KEY_DISP_TENSIONYIELDINGCAP_WEB ='Web Tension Yielding Capacity (kN)'
KEY_TENSIONRUPTURECAP_WEB ='web_plate.shear_rupture_capacity'
KEY_DISP_TENSIONRUPTURECAP_WEB ='Web Tension Rupture Capacity (kN)'
KEY_WEB_PLATE_MOM_DEMAND = 'Web_Plate.MomDemand'
KEY_WEB_DISP_PLATE_MOM_DEMAND = 'Web Moment Demand (kNm)'
KEY_WEB_PLATE_MOM_CAPACITY='Web_plate.MomCapacity'
KEY_WEB_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity (kNm)'
KEY_WEB_BOLT_LINE = 'Web_plate.Bolt_Line'
KEY_WEB_DISP_BOLT_LINE = 'Bolt Lines in web'
KEY_WEB_BOLTS_REQ = "Web_plate.Bolt_required"
KEY_WEB_DISP_BOLTS_REQ = "Web Bolt Required"
KEY_WEB_BOLTS_ONE_LINE = 'Web_plate.Bolt_OneLine'
KEY_WEB_DISP_BOLTS_ONE_LINE = 'Bolts in one Line in web'

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


DISP_TITLE_ENDPLATE = 'End plate'

KEY_ENDPLATE_THICKNESS = 'Plate.end_plate.Thickness'
KEY_DISP_ENDPLATE_THICKNESS = 'Thickness(mm)*'
VALUES_ENDPLATE_THICKNESS = ['All', 'Customized']
VALUES_ENDPLATE_THICKNESS_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30']

VALUES_COLUMN_ENDPLATE_THICKNESS_CUSTOMIZED = VALUES_ENDPLATE_THICKNESS_CUSTOMIZED[3:12] + ['25','28','32','36','40','45','50','56','63','80']

ALL_WELD_SIZES = [3, 4, 5, 6, 8, 10, 12, 14, 16]


KEY_DP_ANCHOR_BOLT_DESIGNATION = 'DesignPreferences.Anchor_Bolt.Designation'
KEY_DP_ANCHOR_BOLT_TYPE = 'DesignPreferences.Anchor_Bolt.Type'
KEY_DISP_DP_ANCHOR_BOLT_TYPE = 'Anchor Bolt type'
KEY_DP_ANCHOR_BOLT_HOLE_TYPE = 'DesignPreferences.Anchor_Bolt.Bolt_Hole_Type'
KEY_DISP_DP_ANCHOR_BOLT_HOLE_TYPE = 'Anchor Bolt hole type'
KEY_DP_ANCHOR_BOLT_MATERIAL_G_O = 'DesignPreferences.Anchor_Bolt.Material_Grade_OverWrite'
KEY_DISP_DP_ANCHOR_BOLT_MATERIAL_G_O = 'Material grade overwrite (MPa) Fu'
KEY_DISP_DP_ANCHOR_BOLT_DESIGN_PARA = 'HSFG bolt design parameters:'
KEY_DP_ANCHOR_BOLT_SLIP_FACTOR = 'DesignPreferences.Anchor_Bolt.Slip_Factor'
KEY_DISP_DP_ANCHOR_BOLT_SLIP_FACTOR = 'Slip factor (µ_f)'
KEY_DP_ANCHOR_BOLT_GALVANIZED = 'DesignPreferences.Anchor_Bolt.Galvanized'
KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED = 'Is galvanized?'
KEY_DP_ANCHOR_BOLT_LENGTH = 'DesignPreferences.Anchor_Bolt.Length'
KEY_DISP_DP_ANCHOR_BOLT_LENGTH = 'Length'
KEY_DP_ANCHOR_BOLT_FRICTION = 'DesignPreferences.Anchor_Bolt.Friction_coefficient'
KEY_DISP_DP_ANCHOR_BOLT_FRICTION = 'Friction coefficient between <br>concrete and anchor bolt'


KEY_DP_BOLT_TYPE = 'DesignPreferences.Bolt.Type'
KEY_DISP_DP_BOLT_TYPE = 'Bolt type'
KEY_DP_BOLT_HOLE_TYPE = 'DesignPreferences.Bolt.Bolt_Hole_Type'
KEY_DISP_DP_BOLT_HOLE_TYPE = 'Bolt hole type'
KEY_DP_BOLT_MATERIAL_G_O = 'DesignPreferences.Bolt.Material_Grade_OverWrite'
KEY_DISP_DP_BOLT_MATERIAL_G_O = 'Material grade overwrite (MPa) Fu'
KEY_DISP_DP_BOLT_DESIGN_PARA = 'HSFG bolt design parameters:'
KEY_DP_BOLT_SLIP_FACTOR = 'DesignPreferences.Bolt.Slip_Factor'
KEY_DISP_DP_BOLT_SLIP_FACTOR = 'Slip factor (µ_f)'
KEY_DP_WELD_FAB = 'DesignPreferences.Weld.Fab'

KEY_DISP_DP_BOLT_FU = 'Bolt Ultimate Strength (N/mm2)'
KEY_DISP_DP_BOLT_FY = 'Bolt Yield Strength (N/mm2)'


KEY_DP_WELD_TYPE = 'Weld.Type'
KEY_DISP_DP_WELD_TYPE ='Weld Type'
KEY_DP_WELD_FAB_SHOP = 'Shop Weld'
KEY_DP_WELD_FAB_FIELD = 'Field weld'
KEY_DP_WELD_FAB_VALUES = [KEY_DP_WELD_FAB_SHOP, KEY_DP_WELD_FAB_FIELD]

KEY_DISP_DP_WELD_FAB = 'Type of weld fabrication'
KEY_DP_WELD_MATERIAL_G_O = 'DesignPreferences.Weld.Material_Grade_OverWrite'
KEY_DISP_DP_WELD_MATERIAL_G_O = 'Material grade overwrite (MPa) Fu'
KEY_DP_DETAILING_EDGE_TYPE = 'DesignPreferences.Detailing.Edge_type'
KEY_DISP_DP_DETAILING_EDGE_TYPE = 'Type of edges'
KEY_DP_DETAILING_GAP = 'DesignPreferences.Detailing.Gap'
KEY_DISP_DP_DETAILING_GAP = 'Gap between beam and <br>support (mm)'
KEY_DP_DETAILING_CORROSIVE_INFLUENCES = 'DesignPreferences.Detailing.Corrosive_Influences'
KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES = 'Are the members exposed to <br>corrosive influences'
KEY_DP_DESIGN_METHOD = 'DesignPreferences.Design.Design_Method'
KEY_DISP_DP_DESIGN_METHOD = 'Design Method'
KEY_DP_DESIGN_BASE_PLATE = 'DesignPreferences.Design.Base_Plate'
KEY_DISP_DP_DESIGN_BASE_PLATE = 'Base Plate'

KEY_SUPTNGSEC_DESIGNATION = 'Supporting_Section.Designation'
KEY_DISP_SUPTNGSEC_DESIGNATION = 'Designation'
KEY_DISP_MECH_PROP = 'Mechanical Properties'
KEY_SUPTNGSEC_FU = 'Supporting_Section.Ultimate_Strength'
KEY_DISP_SUPTNGSEC_FU = 'Ultimate strength, fu (MPa)'
KEY_SUPTNGSEC_FY = 'Supporting_Section.Yield_Strength'
KEY_DISP_SUPTNGSEC_FY = 'Yield Strength , fy (MPa)'
KEY_DISP_DIMENSIONS = 'Dimensions'
KEY_SUPTNGSEC_DEPTH = 'Supporting_Section.Depth'
KEY_DISP_SUPTNGSEC_DEPTH = 'Depth, D (mm)*'
KEY_SUPTNGSEC_FLANGE_W = 'Supporting_Section.Flange_Width'
KEY_DISP_SUPTNGSEC_FLANGE_W = 'Flange width, B (mm)*'
KEY_SUPTNGSEC_FLANGE_T = 'Supporting_Section.Flange_Thickness'
KEY_DISP_SUPTNGSEC_FLANGE_T = 'Flange thickness, T (mm)*'
KEY_SUPTNGSEC_WEB_T = 'Supporting_Section.Web_Thickness'
KEY_DISP_SUPTNGSEC_WEB_T = 'Web thickness, t (mm)*'
KEY_SUPTNGSEC_FLANGE_S = 'Supporting_Section.Flange_Slope'
KEY_DISP_SUPTNGSEC_FLANGE_S = 'Flange Slope, a (deg.)*'
KEY_SUPTNGSEC_ROOT_R = 'Supporting_Section.Root_Radius'
KEY_DISP_SUPTNGSEC_ROOT_R = 'Root radius, R1 (mm)*'
KEY_SUPTNGSEC_TOE_R = 'Supporting_Section.Toe_Radius'
KEY_DISP_SUPTNGSEC_TOE_R = 'Toe radius, R2 (mm)*'


KEY_SUPTNGSEC_TYPE = 'Supporting_Section.Type'
KEY_DISP_SUPTNGSEC_TYPE = 'Type'
KEY_SUPTNGSEC_MOD_OF_ELAST = 'Supporting_Section.Modulus_of_elasticity'
KEY_SUPTNGSEC_DISP_MOD_OF_ELAST = 'Modulus of elasticity, E (GPa)'
KEY_SUPTNGSEC_MOD_OF_RIGID = 'Supporting_Section.Modulus_of_rigidity'
KEY_SUPTNGSEC_DISP_MOD_OF_RIGID = 'Modulus of rifidity, G (GPa)'
KEY_DISP_SEC_PROP = 'Sectional Properties'
KEY_SUPTNGSEC_MASS = 'Supporting_Section.Mass_M'
KEY_DISP_SUPTNGSEC_MASS = 'Mass, M (Kg/m)'
KEY_SUPTNGSEC_SEC_AREA = 'Supporting_Section.Sectional_area_a'
KEY_DISP_SUPTNGSEC_SEC_AREA = 'Sectional area, a (mm<sup>2</sup>)'
KEY_SUPTNGSEC_MOA_LZ = 'Supporting_Section.2nd_Moment_of_area_lz'
KEY_DISP_SUPTNGSEC_MOA_LZ = '2nd Moment of area, l<sub>z</sub> (cm<sup>4</sup>)'
KEY_SUPTNGSEC_MOA_LY = 'Supporting_Section.2nd_Moment_of_area_ly'
KEY_DISP_SUPTNGSEC_MOA_LY = '2nd Moment of area, l<sub>y</sub> (cm<sup>4</sup>)'
KEY_SUPTNGSEC_ROG_RZ = 'Supporting_Section.Radius_of_gyration_rz'
KEY_DISP_SUPTNGSEC_ROG_RZ = 'Radius of gyration, r<sub>z</sub> (cm)'
KEY_SUPTNGSEC_ROG_RY = 'Supporting_Section.Radius_of_gyration_ry'
KEY_DISP_SUPTNGSEC_ROG_RY = 'Radius of gyration, r<sub>y</sub> (cm)'
KEY_SUPTNGSEC_EM_ZZ = 'Supporting_Section.Elastic_modulus_zz'
KEY_DISP_SUPTNGSEC_EM_ZZ = 'Elastic modulus, Z<sub>z</sub> (cm<sup>3</sup>)'
KEY_SUPTNGSEC_EM_ZY = 'Supporting_Section.Elastic_modulus_zy'
KEY_DISP_SUPTNGSEC_EM_ZY = 'Elastic modulus, Z<sub>y</sub> (cm<sup>3</sup>)'
KEY_SUPTNGSEC_PM_ZPZ = 'Supporting_Section.Plastic_modulus_zpz'
KEY_DISP_SUPTNGSEC_PM_ZPZ = 'Plastic modulus, Z<sub>pz</sub> (cm<sup>3</sup>)'
KEY_SUPTNGSEC_PM_ZPY = 'Supporting_Section.Plastic_modulus_zpy'
KEY_DISP_SUPTNGSEC_PM_ZPY = 'Plastic modulus, Z<sub>py</sub> (cm<sup>3</sup>)'


KEY_SUPTNGSEC_SOURCE = 'Supporting_Section.Source'
KEY_DISP_SUPTNGSEC_SOURCE = 'Source'
KEY_SUPTNGSEC_POISSON_RATIO = 'Supporting_Section.Poisson_Ratio'
KEY_DISP_SUPTNGSEC_POISSON_RATIO = 'Poissons ratio, v'
KEY_SUPTNGSEC_THERMAL_EXP = 'Supporting_Section.Thermal_Expansion'
KEY_DISP_SUPTNGSEC_THERMAL_EXP = 'Thermal expansion coeff.a <br>(x10<sup>-6</sup>/ <sup>0</sup>C)'

KEY_SUPTDSEC_DESIGNATION = 'Supported_Section.Designation'
KEY_DISP_SUPTDSEC_DESIGNATION = 'Designation'
KEY_SUPTDSEC_FU = 'Supported_Section.Ultimate_Strength'
KEY_DISP_SUPTDSEC_FU = 'Ultimate strength, fu (MPa)'
KEY_SUPTDSEC_FY = 'Supported_Section.Yield_Strength'
KEY_DISP_SUPTDSEC_FY = 'Yield Strength , fy (MPa)'
KEY_SUPTDSEC_DEPTH = 'Supported_Section.Depth'
KEY_DISP_SUPTDSEC_DEPTH = 'Depth, D (mm)*'
KEY_SUPTDSEC_FLANGE_W = 'Supported_Section.Flange_Width'
KEY_DISP_SUPTDSEC_FLANGE_W = 'Flange width, B (mm)*'
KEY_SUPTDSEC_FLANGE_T = 'Supported_Section.Flange_Thickness'
KEY_DISP_SUPTDSEC_FLANGE_T = 'Flange thickness, T (mm)*'
KEY_SUPTDSEC_WEB_T = 'Supported_Section.Web_Thickness'
KEY_DISP_SUPTDSEC_WEB_T = 'Web thickness, t (mm)*'
KEY_SUPTDSEC_FLANGE_S = 'Supported_Section.Flange_Slope'
KEY_DISP_SUPTDSEC_FLANGE_S = 'Flange Slope, a (deg.)*'
KEY_SUPTDSEC_ROOT_R = 'Supported_Section.Root_Radius'
KEY_DISP_SUPTDSEC_ROOT_R = 'Root radius, R1 (mm)*'
KEY_SUPTDSEC_TOE_R = 'Supported_Section.Toe_Radius'
KEY_DISP_SUPTDSEC_TOE_R = 'Toe radius, R2 (mm)*'


KEY_SUPTDSEC_TYPE = 'Supported_Section.Type'
KEY_DISP_SUPTDSEC_TYPE = 'Type'
KEY_SUPTDSEC_MOD_OF_ELAST = 'Supported_Section.Modulus_of_elasticity'
KEY_SUPTDSEC_DISP_MOD_OF_ELAST = 'Modulus of elasticity, E (GPa)'
KEY_SUPTDSEC_MOD_OF_RIGID = 'Supported_Section.Modulus_of_rigidity'
KEY_SUPTDSEC_DISP_MOD_OF_RIGID = 'Modulus of rifidity, G (GPa)'
KEY_SUPTDSEC_MASS = 'Supported_Section.Mass_M'
KEY_DISP_SUPTDSEC_MASS = 'Mass, M (Kg/m)'
KEY_SUPTDSEC_SEC_AREA = 'Supported_Section.Sectional_area_a'
KEY_DISP_SUPTDSEC_SEC_AREA = 'Sectional area, a (mm<sup>2</sup>)'
KEY_SUPTDSEC_MOA_LZ = 'Supported_Section.2nd_Moment_of_area_lz'
KEY_DISP_SUPTDSEC_MOA_LZ = '2nd Moment of area, l<sub>z</sub> (cm<sup>4</sup>)'
KEY_SUPTDSEC_MOA_LY = 'Supported_Section.2nd_Moment_of_area_ly'
KEY_DISP_SUPTDSEC_MOA_LY = '2nd Moment of area, l<sub>y</sub> (cm<sup>4</sup>)'
KEY_SUPTDSEC_ROG_RZ = 'Supported_Section.Radius_of_gyration_rz'
KEY_DISP_SUPTDSEC_ROG_RZ = 'Radius of gyration, r<sub>z</sub> (cm)'
KEY_SUPTDSEC_ROG_RY = 'Supported_Section.Radius_of_gyration_ry'
KEY_DISP_SUPTDSEC_ROG_RY = 'Radius of gyration, r<sub>y</sub> (cm)'
KEY_SUPTDSEC_EM_ZZ = 'Supported_Section.Elastic_modulus_zz'
KEY_DISP_SUPTDSEC_EM_ZZ = 'Elastic modulus, Z<sub>z</sub> (cm<sup>3</sup>)'
KEY_SUPTDSEC_EM_ZY = 'Supported_Section.Elastic_modulus_zy'
KEY_DISP_SUPTDSEC_EM_ZY = 'Elastic modulus, Z<sub>y</sub> (cm<sup>3</sup>)'
KEY_SUPTDSEC_PM_ZPZ = 'Supported_Section.Plastic_modulus_zpz'
KEY_DISP_SUPTDSEC_PM_ZPZ = 'Plastic modulus, Z<sub>pz</sub> (cm<sup>3</sup>)'
KEY_SUPTDSEC_PM_ZPY = 'Supported_Section.Plastic_modulus_zpy'
KEY_DISP_SUPTDSEC_PM_ZPY = 'Plastic modulus, Z<sub>py</sub> (cm<sup>3</sup>)'


KEY_SUPTDSEC_SOURCE = 'Supported_Section.Source'
KEY_DISP_SUPTDSEC_SOURCE = 'Source'
KEY_SUPTDSEC_POISSON_RATIO = 'Supported_Section.Poisson_Ratio'
KEY_DISP_SUPTDSEC_POISSON_RATIO = 'Poissons ratio, v'
KEY_SUPTDSEC_THERMAL_EXP = 'Supported_Section.Thermal_Expansion'
KEY_DISP_SUPTDSEC_THERMAL_EXP = 'Thermal expansion coeff.a <br>(x10<sup>-6</sup>/ <sup>0</sup>C)'


KEY_BASE_PLATE_MATERIAL = 'Base_Plate.Material'
KEY_DISP_BASE_PLATE_MATERIAL = 'Material'
KEY_BASE_PLATE_FU = 'Base_Plate.Fu'
KEY_DISP_BASE_PLATE_FU = 'Ultimate strength, fu (MPa)'
KEY_DSIP_BASE_PLATE_FY = 'Yield Strength , fy (MPa)'
KEY_BASE_PLATE_FY = 'Base_Plate.Fy'




KEY_ANGLE_DESIGNATION = 'Angle.Designation'
KEY_DISP_ANGLE_DESIGNATION = 'Designation'
KEY_ANGLE_FU = 'Angle.Ultimate_Strength'
KEY_DISP_ANGLE_FU = 'Ultimate strength, fu (MPa)'
KEY_ANGLE_FY = 'Angle.Yield_Strength'
KEY_DISP_ANGLE_FY = 'Yield Strength , fy (MPa)'
KEY_ANGLE_DEPTH = 'Angle.Depth'
KEY_DISP_ANGLE_DEPTH = 'Depth, D (mm)*'
KEY_ANGLE_FLANGE_W = 'Angle.Flange_Width'
KEY_DISP_ANGLE_FLANGE_W = 'Flange width, B (mm)*'
KEY_ANGLE_FLANGE_T = 'Angle.Flange_Thickness'
KEY_DISP_ANGLE_FLANGE_T = 'Flange thickness, T (mm)*'
KEY_ANGLE_WEB_T = 'Angle.Web_Thickness'
KEY_DISP_ANGLE_WEB_T = 'Web thickness, t (mm)*'
KEY_ANGLE_FLANGE_S = 'Angle.Flange_Slope'
KEY_DISP_ANGLE_FLANGE_S = 'Flange Slope, a (deg.)*'
KEY_ANGLE_ROOT_R = 'Angle.Root_Radius'
KEY_DISP_ANGLE_ROOT_R = 'Root radius, R1 (mm)*'
KEY_ANGLE_TOE_R = 'Angle.Toe_Radius'
KEY_DISP_ANGLE_TOE_R = 'Toe radius, R2 (mm)*'


KEY_ANGLE_TYPE = 'Angle.Type'
KEY_DISP_ANGLE_TYPE = 'Type'
KEY_ANGLE_MOD_OF_ELAST = 'Angle.Modulus_of_elasticity'
KEY_ANGLE_DISP_MOD_OF_ELAST = 'Modulus of elasticity, E (GPa)'
KEY_ANGLE_MOD_OF_RIGID = 'Angle.Modulus_of_rigidity'
KEY_ANGLE_DISP_MOD_OF_RIGID = 'Modulus of rifidity, G (GPa)'
KEY_ANGLE_MASS = 'Angle.Mass_M'
KEY_DISP_ANGLE_MASS = 'Mass, M (Kg/m)'
KEY_ANGLE_SEC_AREA = 'Angle.Sectional_area_a'
KEY_DISP_ANGLE_SEC_AREA = 'Sectional area, a (mm<sup>2</sup>)'
KEY_ANGLE_MOA_LZ = 'Angle.2nd_Moment_of_area_lz'
KEY_DISP_ANGLE_MOA_LZ = '2nd Moment of area, l<sub>z</sub> (cm<sup>4</sup>)'
KEY_ANGLE_MOA_LY = 'Angle.2nd_Moment_of_area_ly'
KEY_DISP_ANGLE_MOA_LY = '2nd Moment of area, l<sub>y</sub> (cm<sup>4</sup>)'
KEY_ANGLE_ROG_RZ = 'Angle.Radius_of_gyration_rz'
KEY_DISP_ANGLE_ROG_RZ = 'Radius of gyration, r<sub>z</sub> (cm)'
KEY_ANGLE_ROG_RY = 'Angle.Radius_of_gyration_ry'
KEY_DISP_ANGLE_ROG_RY = 'Radius of gyration, r<sub>y</sub> (cm)'
KEY_ANGLE_EM_ZZ = 'Angle.Elastic_modulus_zz'
KEY_DISP_ANGLE_EM_ZZ = 'Elastic modulus, Z<sub>z</sub> (cm<sup>3</sup>)'
KEY_ANGLE_EM_ZY = 'Angle.Elastic_modulus_zy'
KEY_DISP_ANGLE_EM_ZY = 'Elastic modulus, Z<sub>y</sub> (cm<sup>3</sup>)'
KEY_ANGLE_PM_ZPZ = 'Angle.Plastic_modulus_zpz'
KEY_DISP_ANGLE_PM_ZPZ = 'Plastic modulus, Z<sub>pz</sub> (cm<sup>3</sup>)'
KEY_ANGLE_PM_ZPY = 'Angle.Plastic_modulus_zpy'
KEY_DISP_ANGLE_PM_ZPY = 'Plastic modulus, Z<sub>py</sub> (cm<sup>3</sup>)'

KEY_ANGLE_SOURCE = 'Angle.Source'
KEY_DISP_ANGLE_SOURCE = 'Source'
KEY_ANGLE_POISSON_RATIO = 'Angle.Poisson_Ratio'
KEY_DISP_ANGLE_POISSON_RATIO = 'Poissons ratio, v'
KEY_ANGLE_THERMAL_EXP = 'Angle.Thermal_Expansion'
KEY_DISP_ANGLE_THERMAL_EXP = 'Thermal expansion coeff.a <br>(x10<sup>-6</sup>/ <sup>0</sup>C)'


KEY_BOLT_STATUS = 'Bolt.DesignStatus'
KEY_OUT_D_PROVIDED = 'Bolt.Diameter'
KEY_OUT_DISP_D_PROVIDED = 'Diameter (mm)'
KEY_OUT_GRD_PROVIDED = 'Bolt.Grade'
KEY_OUT_DISP_GRD_PROVIDED = 'Grade'
KEY_OUT_DISP_PC_PROVIDED = 'Property Class'
KEY_OUT_ROW_PROVIDED = 'Bolt.Rows'
KEY_OUT_DISP_ROW_PROVIDED = 'Rows of Bolts'
KEY_OUT_KB = 'Bolt.Kb'
KEY_OUT_BOLT_HOLE = 'Bolt.Hole'
KEY_DISP_BOLT_HOLE = 'Hole Diameter (mm)'
KEY_OUT_BOLT_SHEAR = 'Bolt.Shear'
KEY_OUT_DISP_BOLT_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_BOLT_BEARING = 'Bolt.Bearing'
KEY_OUT_DISP_BOLT_BEARING = 'Bearing Capacity (kN)'
KEY_OUT_DISP_BOLT_SLIP= 'Slip Resistance'
KEY_OUT_BOLT_CAPACITY = 'Bolt.Capacity'
KEY_OUT_DISP_BOLT_CAPACITY = 'Capacity (kN)'
KEY_OUT_DISP_BOLT_VALUE = 'Bolt Value (kN)'
KEY_OUT_BOLT_FORCE = 'Bolt.Force'
KEY_OUT_DISP_BOLT_FORCE = 'Bolt Force (kN)'
KEY_OUT_DISP_BOLT_SHEAR_FORCE = 'Bolt Shear Force (kN)'
KEY_OUT_BOLT_TENSION_FORCE = 'Bolt.TensionForce'
KEY_OUT_DISP_BOLT_TENSION_FORCE = 'Bolt Tension Force (kN)'
KEY_OUT_BOLT_PRYING_FORCE = 'Bolt.PryingForce'
KEY_OUT_DISP_BOLT_PRYING_FORCE = 'Bolt Prying Force (kN)'
KEY_OUT_BOLT_TENSION_CAPACITY = 'Bolt.Tension'
KEY_OUT_DISP_BOLT_TENSION_CAPACITY = 'Bolt Tension Capacity (kN)'
KEY_OUT_BOLT_LINE = 'Bolt.Line'
KEY_OUT_BOLTS_REQUIRED = 'Bolt.Required'
KEY_OUT_LONG_JOINT = 'Long Joint Reduction'
KEY_OUT_BOLT_GRP_CAPACITY = 'Bolt.GroupCapacity'
KEY_OUT_DISP_BOLT_LINE = 'Bolt Lines (nos)'
KEY_OUT_BOLTS_ONE_LINE = 'Bolt.OneLine'
KEY_OUT_DISP_BOLTS_ONE_LINE = 'Bolts in Line (nos)'
KEY_OUT_SPACING = 'spacing'
KEY_OUT_DISP_SPACING = 'Spacing'
KEY_OUT_PITCH = 'Bolt.Pitch'
KEY_OUT_DISP_PITCH = 'Pitch (mm)'

KEY_OUT_MIN_PITCH = 'Bolt.MinPitch'





KEY_OUT_END_DIST = 'Bolt.EndDist'
KEY_OUT_DISP_END_DIST = 'End Distance (mm)'
KEY_OUT_GAUGE = 'Bolt.Gauge'
KEY_OUT_DISP_GAUGE = 'Gauge (mm)'

KEY_OUT_MIN_GAUGE = 'Bolt.MinGauge'
KEY_OUT_MAX_SPACING = 'Bolt.MaxGauge'

KEY_OUT_EDGE_DIST = 'Bolt.EdgeDist'
KEY_OUT_MIN_EDGE_DIST = 'Bolt.MinEdgeDist'
KEY_OUT_MAX_EDGE_DIST = 'Bolt.MaxEdgeDist'


KEY_OUT_DISP_EDGE_DIST = 'Edge Distance (mm)'


KEY_OUT_SPTNG_BOLT_SHEAR = 'Cleat.Sptng_leg.Shear'
KEY_OUT_SPTNG_BOLT_BEARING = 'Cleat.Sptng_leg.Bearing'
KEY_OUT_SPTNG_BOLT_CAPACITY = 'Cleat.Sptng_leg.Capacity'
KEY_OUT_SPTNG_BOLT_FORCE = 'Cleat.Sptng_leg.Force'
KEY_OUT_SPTNG_BOLT_LINE = 'Cleat.Sptng_leg.Line'
KEY_OUT_SPTNG_BOLTS_REQUIRED = 'Cleat.Sptng_leg.Required'

KEY_OUT_SPTNG_BOLT_GRP_CAPACITY = 'Cleat.Sptng_leg.GroupCapacity'

KEY_OUT_SPTNG_BOLTS_ONE_LINE = 'Cleat.Sptng_leg.OneLine'

KEY_OUT_SPTNG_SPACING = 'Cleat.Sptng_leg.spacing'

KEY_OUT_SPTNG_PITCH = 'Cleat.Sptng_leg.Pitch'

KEY_OUT_SPTNG_MIN_PITCH = 'Cleat.Sptng_leg.MinPitch'
KEY_OUT_SPTNG_END_DIST = 'Cleat.Sptng_leg.EndDist'
KEY_OUT_SPTNG_GAUGE = 'Cleat.Sptng_leg.Gauge'
KEY_OUT_SPTNG_MIN_GAUGE = 'Cleat.Sptng_leg.MinGauge'
KEY_OUT_SPTNG_MAX_SPACING = 'Cleat.Sptng_leg.MaxGauge'
KEY_OUT_SPTNG_EDGE_DIST = 'Cleat.Sptng_leg.EdgeDist'
KEY_OUT_SPTNG_MIN_EDGE_DIST = 'Cleat.Sptng_leg.MinEdgeDist'
KEY_OUT_SPTNG_MAX_EDGE_DIST = 'Cleat.Sptng_leg.MaxEdgeDist'


KEY_OUT_DISP_PLATETHK_REP = 'Thickness (tp) (mm)'
KEY_OUT_PLATETHK = 'Plate.Thickness'
KEY_OUT_DISP_PLATETHK = 'Thickness (mm)'
KEY_OUT_PLATE_HEIGHT = 'Plate.Height'
KEY_OUT_DISP_PLATE_HEIGHT = 'Height (mm)'
KEY_OUT_DISP_PLATE_MIN_HEIGHT = 'Min.Height (mm)'
KEY_OUT_PLATE_LENGTH = 'Plate.Length'
KEY_OUT_DISP_PLATE_LENGTH = 'Length (mm)'
KEY_OUT_DISP_PLATE_MIN_LENGTH = 'Min.Length (mm)'
KEY_OUT_PLATE_WIDTH = 'Plate.Width'
KEY_OUT_DISP_PLATE_WIDTH = 'Width (mm)'
c = 'Width (mm)'
KEY_OUT_PLATE_SHEAR = 'Plate.Shear'

KEY_OUT_DISP_PLATE_SHEAR = 'Shear yielding Capacity (kN)'
KEY_OUT_PLATE_YIELD = 'Plate.Yield'
KEY_OUT_DISP_PLATE_YIELD = 'Yield Capacity'
KEY_OUT_PLATE_RUPTURE = 'Plate.Rupture'
KEY_OUT_DISP_PLATE_RUPTURE = 'Rupture Capacity'

KEY_OUT_PLATE_BLK_SHEAR = 'Plate.BlockShear'
KEY_OUT_DISP_PLATE_BLK_SHEAR = 'Block Shear Capacity (kN)'
KEY_OUT_PLATE_MOM_DEMAND = 'Plate.MomDemand'

KEY_OUT_DISP_PLATE_MOM_DEMAND = 'Moment Demand (kN-m)'
KEY_OUT_DISP_PLATE_MOM_DEMAND_SEP = 'Moment Demand per Bolt (kN-m)'
KEY_OUT_PLATE_MOM_CAPACITY = 'Plate.MomCapacity'
KEY_OUT_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity (kN-m)'
KEY_OUT_DISP_PLATE_MOM_CAPACITY_SEP = 'Moment Capacity per Bolt (kN-m)'

KEY_OUT_PLATE_CAPACITIES = 'capacities'
KEY_OUT_DISP_PLATE_CAPACITIES = 'Capacity'

KEY_OUT_WELD_SIZE = 'Weld.Size'
KEY_OUT_DISP_WELD_SIZE = 'Size(mm)'
KEY_OUT_WELD_SIZE_FLANGE = 'Weld.Size_flange'
KEY_OUT_DISP_WELD_SIZE_FLANGE = 'Size at Flange (mm)'
KEY_OUT_WELD_SIZE_WEB = 'Weld.Size_web'
KEY_OUT_DISP_WELD_SIZE_WEB = 'Size at Web (mm)'
KEY_OUT_WELD_SIZE_STIFFENER = 'Weld.Size_stiffener'
KEY_OUT_DISP_WELD_SIZE_STIFFENER = 'Size at Gusset/Stiffener (mm)'
KEY_OUT_WELD_STRENGTH = 'Weld.Strength'
KEY_OUT_DISP_WELD_STRENGTH = 'Strength(N/mm)'
KEY_OUT_WELD_STRESS = 'Weld.Stress'
KEY_OUT_DISP_WELD_STRESS = 'Stress(N/mm)'
KEY_OUT_WELD_LENGTH = 'Weld.Length'
KEY_OUT_DISP_WELD_LENGTH = 'Length (mm)'
KEY_OUT_WELD_LENGTH_EFF = 'Weld.EffLength'
KEY_OUT_DISP_WELD_LENGTH_EFF = 'Eff.Length (mm)'

KEY_OUT_DISP_MEMB_TEN_YIELD = 'Tension Yield Capacity (KN)'
KEY_OUT_DISP_MEMB_TEN_RUPTURE = 'Tension Rupture Capacity'
KEY_OUT_DISP_MEMB_BLK_SHEAR = 'Block Shear Capacity'
KEY_OUT_DISP_MEMB_BLK_SHEAR = 'Block Shear Capacity'


KEY_OUT_NO_BOLTS_FLANGE = 'ColumnEndPlate.nbf'
KEY_OUT_DISP_NO_BOLTS_FLANGE = 'No. of bolts along Flange'
KEY_OUT_NO_BOLTS_WEB = 'ColumnEndPlate.nbw'
KEY_OUT_DISP_NO_BOLTS_WEB = 'No. of bolts along Web'
KEY_OUT_NO_BOLTS = 'ColumnEndPlate.nb'
KEY_OUT_DISP_NO_BOLTS = 'Total no. of Bolts'
KEY_PITCH_2_FLANGE = 'ColumnEndPlate.p2_flange'
KEY_DISP_PITCH_2_FLANGE = 'Pitch2 along Flange'
KEY_PITCH_2_WEB = 'ColumnEndPlate.p2_web'
KEY_DISP_PITCH_2_WEB = 'Pitch2 along Web'
KEY_CONN_PREFERENCE = 'plate.design_method'
KEY_DISP_CONN_PREFERENCE = 'Design Method'
VALUES_CONN_PREFERENCE = ["Select","Plate Oriented", "Bolt Oriented"]


DISP_TITLE_WELD = 'Weld'
KEY_OUT_WELD_SIZE = 'Weld.Size'
KEY_OUT_DISP_WELD_SIZE = 'Size (mm)'
KEY_OUT_WELD_STRENGTH = 'Weld.Strength'
KEY_OUT_DISP_WELD_STRENGTH = 'Strength (N/mm)'
KEY_OUT_WELD_STRESS = 'Weld.Stress'
KEY_OUT_DISP_WELD_STRESS = 'Stress (N/mm)'
KEY_OUT_WELD_LENGTH = 'Weld.Length'
KEY_OUT_DISP_WELD_LENGTH = 'Length (mm)'
KEY_OUT_WELD_LENGTH_EFF = 'Weld.EffLength'
KEY_OUT_DISP_WELD_LENGTH_EFF = 'Eff.Length (mm)'

DISP_OUT_TITLE_SPTDLEG = "Supported Leg"
DISP_OUT_TITLE_SPTNGLEG = "Supporting Leg"
DISP_OUT_TITLE_CLEAT = "Cleat Angle"
KEY_OUT_CLEATTHK = 'Plate.Thickness'
KEY_OUT_DISP_CLEATTHK = 'Thickness (mm)'
KEY_OUT_CLEAT_HEIGHT = 'Plate.Height'
KEY_OUT_DISP_CLEAT_HEIGHT = 'Height (mm)'
KEY_OUT_CLEAT_SPTDLEG = 'Cleat.SupportedLength'
KEY_OUT_DISP_CLEAT_SPTDLEG = 'Length (mm)'
KEY_OUT_CLEAT_SPTNGLEG = 'Cleat.SupportingLength'
KEY_OUT_DISP_CLEAT_SPTNGLEG = 'Length (mm)'

KEY_OUT_CLEAT_SHEAR = 'Cleat.Shear'

KEY_OUT_CLEAT_BLK_SHEAR = 'Cleat.BlockShear'

KEY_OUT_CLEAT_MOM_DEMAND = 'Cleat.MomDemand'

KEY_OUT_CLEAT_MOM_CAPACITY = 'Cleat.MomCapacity'


KEY_SEC_PROFILE = 'Member.Profile'
KEY_DISP_SEC_PROFILE = 'Section Profile'
VALUES_SEC_PROFILE = ['Beams', 'Columns', 'Angles', 'Channels', 'Back to Back Angles', 'Back to Back Channels', 'Star Angles']
VALUES_SEC_PROFILE_2 = ['Angles', 'Back to Back Angles', 'Star Angles', 'Channels', 'Back to Back Channels']

KEY_LENZZ = 'Member.Length_zz'
KEY_DISP_LENZZ = 'Length (z-z)'


KEY_LENYY = 'Member.Length_yy'
KEY_DISP_LENYY = 'Length (y-y)'

DISP_TITLE_SC = 'Supporting Condition'

KEY_END1 = 'End_1'
KEY_DISP_END1 = 'End 1'
VALUES_END1 = ['Fixed', 'Free', 'Hinged', 'Roller']


KEY_END2 = 'End_2'
KEY_DISP_END2 = 'End 2'
VALUES_END2 = ['Fixed', 'Free', 'Hinged', 'Roller']

KEY_END_CONDITION = 'ENd Condition'
KEY_DISP_END_CONDITION = 'End Cndition'

DISP_TITLE_CLEAT = 'Cleat Angle'
DISP_TITLE_ANGLE = 'Angle Section'

KEY_CLEATHT='CleatHt'
KEY_DISP_CLEATHT='Height(mm)'

KEY_CLEATSEC='Cleat Section'
KEY_DISP_CLEATSEC='Cleat Section *'
# VALUES_CLEATSEC=['Select Section','20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5', '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4', '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']

KEY_SEATEDANGLE = 'Seated Angle'
KEY_DISP_SEATEDANGLE = 'Seated Angle *'
# VALUES_SEATEDANGLE=['20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5', '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4', '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']

KEY_TOPANGLE = 'Top Angle'
KEY_DISP_TOPANGLE = 'Top Angle *'
# VALUES_TOPANGLE=[
#     '20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5',
#     '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4',
#     '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']
VALUES_ANGLESEC= ['All', 'Customized']

VALUES_ANGLESEC_CUSTOMIZED= connectdb("Angles", call_type="popup")
# DISPLAY_TITLE_ANGLESEC='Select Sections'

#Design Report Strings
DISP_NUM_OF_BOLTS = 'No of Bolts'
DISP_NUM_OF_ROWS = 'No of Rows'
DISP_NUM_OF_COLUMNS = 'No of Columns'


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

        print(min_leg_length,max_leg_length)
        if operator.le(max(leg_a_length,leg_b_length),max_leg_length_outer) and operator.ge(min(leg_a_length,leg_b_length), min_leg_length_outer) and leg_a_length==leg_b_length:
            print("appended", designation)
            available_angles.append(designation)
        else:
            print("popped",designation)
    return available_angles


def get_leg_lengths(designation):

    """
        Function to fetch designation values from respective Tables.
    """
    conn = sqlite3.connect(PATH_TO_DATABASE)
    db_query = "SELECT AXB, t, R1 FROM Angles WHERE Designation = ?"
    cur = conn.cursor()
    cur.execute(db_query, (designation,))
    row = cur.fetchone()

    axb = row[0]
    t = row[1]
    r_r = row[2]
    axb = axb.lower()
    leg_a_length = float(axb.split("x")[0])
    leg_b_length = float(axb.split("x")[1])
    conn.close()
    return leg_a_length,leg_b_length,t,r_r

all_angles = connectdb("Angles","popup")
VALUES_CLEAT_CUSTOMIZED = get_available_cleat_list(all_angles, 200.0, 50.0)
# print(VALUES_CLEAT_CUSTOMIZED)

DISP_TITLE_COMPMEM='Compression member'

KEY_SECTYPE = 'Section Type'
KEY_DISP_SECTYPE = 'Section Type*'
VALUES_SECTYPE = ['Select Type','Beams','Columns','Angles','Back to Back Angles','Star Angles','Channels','Back to back Channels']


KEY_SECSIZE = 'Section Size'
KEY_DISP_SECSIZE = 'Section Size*'

KEY_LENMEM = 'Length of Member'
KEY_DISP_LENMEM = 'Length of Member'

DISP_TITLE_FL = 'Factored loads'

KEY_AXFOR = 'Axial Force'
KEY_DISP_AXFOR = 'Axial Force (kN)*'

KEY_PLTHK = 'Plate thk'
KEY_DISP_PLTHK = 'Plate thk (mm)'

KEY_PLTHICK = 'Plate thk'
KEY_DISP_PLTHICK = 'Plate Thickness'


KEY_DIAM = 'Diameter'
KEY_DISP_DIAM = 'Diameter (mm)'
VALUES_DIAM = ['Select diameter','12','16','20','24','30','36']

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
VALUES_CONNLOC_BOLT = ['Bolted','Web','Flange','Leg','Back to Back Web','Back to Back Angles','Star Angles']
VALUES_CONNLOC_WELD = ['Welded','Web','Flange','Leg','Back to Back Web','Back to Back Angles','Star Angles']


KEY_LEN_INLINE = 'Total length in line with tension'
KEY_DISP_LEN_INLINE = 'Total Length in line with tension'

KEY_LEN_OPPLINE = 'Total length opp line with tension'
KEY_DISP_LEN_OPPLINE = 'Total Length opp line with tension'


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

DETAILING_DESCRIPTION = str("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
               "p, li { white-space: pre-wrap; }\n"
               "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.7</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[a- sheared or hand flame cut edges] </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">and </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.5 </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[b - Rolled, machine-flame cut, sawn and planed edges]</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> (IS 800 - cl. 10. 2. 4. 2)</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">This gap should include the tolerance value of 5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5 mm{tolerance})</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
               "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3</span></p>\n"
               "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")
