
# @author: Amir, Umair, Arsil


TYPE_COMBOBOX = 'ComboBox'

TYPE_TEXTBOX = 'TextBox'
TYPE_TITLE = 'Title'
TYPE_LABEL = 'Label'
TYPE_IMAGE = 'Image'
TYPE_COMBOBOX_CUSTOMIZED = 'ComboBox_Customized'
TYPE_OUT_BUTTON = 'Output_dock_Button'
TYPE_BREAK = 'Break'
TYPE_ENTER = 'Enter'
PATH_TO_DATABASE = "ResourceFiles/Database/Intg_osdag.sqlite"
DESIGN_FLAG = 'False'

import sqlite3
from utils.common.component import *
from utils.common.component import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
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


def connectdb(table_name):

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
   
    final_lst = tuple_to_str(lst)
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

def tuple_to_str(tl):
    arr = ['Select Section']
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

KEY_MODULE = 'Module'
KEY_DISP_FINPLATE = 'Fin Plate'
TYPE_MODULE = 'Window Title'

KEY_DISP_BEAMCOVERPLATE = 'Beam Coverplate Connection'
KEY_DISP_COLUMNCOVERPLATE = 'Column Coverplate Connection'
KEY_DISP_BEAMENDPLATE = 'Beam Endplate Connection'
KEY_DISP_COLUMNENDPLATE = 'Column Endplate Connection'

DISP_TITLE_CM = 'Connecting members'

KEY_CONN = 'Connectivity'
KEY_DISP_CONN = 'Connectivity *'
VALUES_CONN = ['Column flange-Beam web', 'Column web-Beam web', 'Beam-Beam']
VALUES_CONN_1 = ['Column flange-Beam web', 'Column web-Beam web']
VALUES_CONN_2 = ['Beam-Beam']


KEY_IMAGE = 'Image'

KEY_SUPTNGSEC = 'Member.Supporting_Section'
KEY_DISP_SUPTNGSEC = 'Supporting Section'
KEY_DISP_COLSEC = 'Column Section *'
VALUES_COLSEC = connectdb("Columns")

KEY_DISP_PRIBM = 'Primary beam *'
VALUES_PRIBM = connectdb("Beams")


KEY_SUPTDSEC = 'Member.Supported_Section'
KEY_DISP_SUPTDSEC = 'Supported Section'
KEY_DISP_BEAMSEC = 'Beam Section *'
VALUES_BEAMSEC = connectdb("Beams")

KEY_DISP_SECBM = 'Secondary beam *'
VALUES_SECBM = connectdb("Beams")

KEY_MATERIAL = 'Member.Material'
KEY_DISP_MATERIAL = 'Material *'
VALUES_MATERIAL = connectdb("Material")

DISP_TITLE_FSL = 'Factored load'

KEY_MOMENT = 'Load.Moment'
KEY_DISP_MOMENT = 'Moment(kNm)*'

KEY_SHEAR = 'Load.Shear'
KEY_DISP_SHEAR = 'Shear(kN)*'

KEY_AXIAL = 'Load.Axial'
KEY_DISP_AXIAL = 'Axial (kN) *'

DISP_TITLE_BOLT = 'Bolt'

KEY_D = 'Bolt.Diameter'
KEY_DISP_D = 'Diameter(mm)*'
VALUES_D = ['All', 'Customized']

KEY_TYP = 'Bolt.Type'
KEY_DISP_TYP = 'Type *'
VALUES_TYP = ['Select Type', 'Friction Grip Bolt', 'Bearing Bolt']
VALUES_TYP_1 = ['Friction Grip Bolt']
VALUES_TYP_2 = ['Bearing Bolt']

KEY_GRD = 'Bolt.Grade'
KEY_DISP_GRD = 'Grade *'

VALUES_GRD = ['All', 'Customized']
VALUES_GRD_CUSTOMIZED = ['3.6', '4.6', '4.8', '5.6', '5.8', '6.8', '8.8', '9.8', '10.9', '12.9']

DISP_TITLE_FLANGESPLICEPLATE = 'Flange splice plate'

KEY_FLANGEPLATE_PREFERENCES = 'Flange_Plate.Preferences'
KEY_DISP_FLANGESPLATE_PREFERENCES = 'Preferences'
VALUES_FLANGEPLATE_PREFERENCES = ['Cover plate location', 'Outside','Outside + Inside']

KEY_FLANGEPLATE_THICKNESS = 'flange_plate.thickness_provided'
KEY_DISP_FLANGESPLATE_THICKNESS = 'Thickness(mm)*'
VALUES_FLANGEPLATE_THICKNESS = ['All', 'Customized']

KEY_FLANGE_PLATE_HEIGHT = 'flange_plate.Height'
KEY_DISP_FLANGE_PLATE_HEIGHT = 'Height(mm)'
KEY_FLANGE_PLATE_LENGTH ='flange_plate.Length'
KEY_DISP_FLANGE_PLATE_LENGTH ='Length'

KEY_FLANGE_SPACING ="Flange_plate.spacing"
KEY_DISP_FLANGE_SPACING = 'Spacing'
KEY_FLANGE_PITCH = 'Flange_plate.pitch_provided'
KEY_DISP_FLANGE_PLATE_PITCH = 'Pitch'
KEY_FLANGE_PLATE_GAUGE = "Flange_plate.gauge_provided "
KEY_DISP_FLANGE_PLATE_GAUGE ="Gauge"
KEY_ENDDIST_FLANGE= 'Flange_plate.end_dist_provided '
KEY_DISP_END_DIST_FLANGE = 'End Distance'
KEY_EDGEDIST_FLANGE= 'Flange_plate.edge_dist_provided'
KEY_DISP_EDGEDIST_FLANGE= 'Edge Distance'

KEY_FLANGE_CAPACITY ="Flange_plate.capacity"
KEY_DISP_FLANGE_CAPACITY= 'capacity'
KEY_BLOCKSHEARCAP_FLANGE='Flange_plate.block_shear_capacity'
KEY_DISP_BLOCKSHEARCAP_FLANGE='Block Shear Capacity'
KEY_SHEARYIELDINGCAP_FLANGE= 'Flange_plate.shear_yielding_capacity'
KEY_DISP_SHEARYIELDINGCAP_FLANGE= 'Shear Yielding Capacity'
KEY_SHEARRUPTURECAP_FLANGE= 'Flange_plate.shear_rupture_capacity'
KEY_DISP_SHEARRUPTURECAP_FLANGE= 'Shear Rupture Capacity'
KEY_FLANGE_PLATE_MOM_DEMAND = 'Flange_Plate.MomDemand'
KEY_FLANGE_DISP_PLATE_MOM_DEMAND = 'Moment Demand'
KEY_FLANGE_PLATE_MOM_CAPACITY='Flange_plate.MomCapacity'
KEY_FLANGE_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity'


DISP_TITLE_WEBSPLICEPLATE = 'Web splice plate'

KEY_WEBPLATE_THICKNESS = 'Web_Plate.thickness_provided'
KEY_DISP_WEBPLATE_THICKNESS = 'Thickness(mm)*'
VALUES_WEBPLATE_THICKNESS = ['All', 'Customized']
VALUES_PLATETHICKNESS_CUSTOMIZED = ['6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30']

KEY_WEB_PLATE_HEIGHT = 'Web_Plate.Height'
KEY_DISP_WEB_PLATE_HEIGHT = 'Height(mm)'
KEY_WEB_PLATE_LENGTH ='Web_Plate.Length'
KEY_DISP_WEB_PLATE_LENGTH ='Length'

KEY_WEB_SPACING ="Web_plate.spacing"
KEY_DISP_WEB_SPACING = 'Spacing'
KEY_WEB_PITCH = "Web_plate.pitch_provided"
KEY_DISP_WEB_PLATE_PITCH ="Pitch"
KEY_WEB_GAUGE = "Web_plate.gauge_provided "
KEY_DISP_WEB_PLATE_GAUGE ="Gauge"
KEY_ENDDIST_W= 'Web_plate.end_dist_provided '
KEY_DISP_END_DIST_W = 'End Distance'
KEY_EDGEDIST_W = 'Web_plate.edge_dist_provided'
KEY_DISP_EDGEDIST_W = 'Edge Distance'

KEY_WEB_CAPACITY ="Web_plate.capacity"
KEY_DISP_WEB_CAPACITY= 'capacity'
KEY_SHEARYIELDINGCAP_WEB= 'web_plate.shear_yielding_capacity'
KEY_DISP_SHEARYIELDINGCAP_WEB= 'Shear Yielding Capacity'
KEY_BLOCKSHEARCAP_WEB='web_plate.block_shear_capacity'
KEY_DISP_BLOCKSHEARCAP_WEB='Block Shear Capacity'
KEY_SHEARRUPTURECAP_WEB= 'web_plate.shear_rupture_capacity'
KEY_DISP_SHEARRUPTURECAP_WEB= 'Shear Rupture Capacity'
KEY_WEB_PLATE_MOM_DEMAND = 'Web_Plate.MomDemand'
KEY_WEB_DISP_PLATE_MOM_DEMAND = 'Moment Demand'
KEY_WEB_PLATE_MOM_CAPACITY='Web_plate.MomCapacity'
KEY_WEB_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity'

DISP_TITLE_ENDPLATE = 'End plate'

KEY_ENDPLATE_THICKNESS = 'Plate.end_plate.Thickness'
KEY_DISP_ENDPLATE_THICKNESS = 'Thickness(mm)*'
VALUES_ENDPLATE_THICKNESS = ['All', 'Customized']
VALUES_ENDPLATE_THICKNESS_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20']

DISP_TITLE_PLATE = 'Plate'

KEY_PLATETHK = 'Plate.Thickness'
KEY_DISP_PLATETHK = 'Thickness(mm)*'
VALUES_PLATETHK = ['All', 'Customized']
VALUES_PLATETHK_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20']

KEY_DP_BOLT_TYPE = 'DesignPreferences.Bolt.Type'
KEY_DISP_DP_BOLT_TYPE = 'Bolt type'
KEY_DP_BOLT_HOLE_TYPE = 'DesignPreferences.Bolt.Bolt_Hole_Type'
KEY_DISP_DP_BOLT_HOLE_TYPE = 'Bolt hole type'
KEY_DP_BOLT_MATERIAL_G_O = 'DesignPreferences.Bolt.Material_Grade_OverWrite'
KEY_DISP_DP_BOLT_MATERIAL_G_O = 'Material grade overwrite (MPa) Fu'
KEY_DISP_DP_BOLT_DESIGN_PARA = 'HSFG bolt design parameters:'
KEY_DP_BOLT_SLIP_FACTOR = 'DesignPreferences.Bolt.Slip_Factor'
KEY_DISP_DP_BOLT_SLIP_FACTOR = 'Slip factor (µ_f)'
KEY_DP_WELD_TYPE = 'DesignPreferences.Weld.Type'
KEY_DISP_DP_WELD_TYPE = 'Type of weld'
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

KEY_OUT_D_PROVIDED = 'Bolt.Diameter'
KEY_OUT_DISP_D_PROVIDED = 'Diameter (mm)'
KEY_OUT_GRD_PROVIDED = 'Bolt.Grade'
KEY_OUT_DISP_GRD_PROVIDED = 'Grade'
KEY_OUT_BOLT_SHEAR = 'Bolt.Shear'
KEY_OUT_DISP_BOLT_SHEAR = 'Shear Capacity'
KEY_OUT_BOLT_BEARING = 'Bolt.Bearing'
KEY_OUT_DISP_BOLT_BEARING = 'Bearing Capacity'
KEY_OUT_BOLT_CAPACITY = 'Bolt.Capacity'
KEY_OUT_BOLT_FORCE = 'Bolt.Force'
KEY_OUT_DISP_BOLT_FORCE = 'Bolt Force'
KEY_OUT_DISP_BOLT_CAPACITY = 'Capacity'
KEY_OUT_BOLT_LINE = 'Bolt.Line'
KEY_OUT_DISP_BOLT_LINE = 'Bolt Lines'
KEY_OUT_BOLTS_ONE_LINE = 'Bolt.OneLine'
KEY_OUT_DISP_BOLTS_ONE_LINE = 'Bolts in Line'
KEY_OUT_SPACING = 'spacing'
KEY_OUT_DISP_SPACING = 'Spacing'
KEY_OUT_PITCH = 'Bolt.Pitch'
KEY_OUT_DISP_PITCH = 'Pitch'
KEY_OUT_END_DIST = 'Bolt.EndDist'
KEY_OUT_DISP_END_DIST = 'End Distance'
KEY_OUT_GAUGE = 'Bolt.Gauge'
KEY_OUT_DISP_GAUGE = 'Gauge'
KEY_OUT_EDGE_DIST = 'Bolt.EdgeDist'
KEY_OUT_DISP_EDGE_DIST = 'Edge Distance'


KEY_OUT_PLATETHK = 'Plate.Thickness'
KEY_OUT_DISP_PLATETHK = 'Thickness (mm)'
KEY_OUT_PLATE_HEIGHT = 'Plate.Height'
KEY_OUT_DISP_PLATE_HEIGHT = 'Height (mm)'
KEY_OUT_PLATE_LENGTH = 'Plate.Length'
KEY_OUT_DISP_PLATE_LENGTH = 'Length (mm)'
KEY_OUT_PLATE_SHEAR = 'Plate.Shear'
KEY_OUT_DISP_PLATE_SHEAR = 'Shear yielding Capacity'
KEY_OUT_PLATE_BLK_SHEAR = 'Plate.BlockShear'
KEY_OUT_DISP_PLATE_BLK_SHEAR = 'Block Shear Capacity'
KEY_OUT_PLATE_MOM_DEMAND = 'Plate.MomDemand'
KEY_OUT_DISP_PLATE_MOM_DEMAND = 'Moment Demand'
KEY_OUT_PLATE_MOM_CAPACITY = 'Plate.MomCapacity'
KEY_OUT_DISP_PLATE_MOM_CAPACITY = 'Moment Capacity'








DISP_TITLE_CLEAT = 'Cleat Angle'
DISP_TITLE_ANGLE = 'Angle Section'

KEY_CLEATHT='CleatHt'
KEY_DISP_CLEATHT='Height(mm)'

KEY_CLEATSEC='Cleat Section'
KEY_DISP_CLEATSEC='Cleat Section *'
# VALUES_CLEATSEC=['Select Section','20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5', '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4', '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']

KEY_SEATEDANGLE='SeatedAngle'
KEY_DISP_SEATEDANGLE='Seated Angle *'
# VALUES_SEATEDANGLE=['20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5', '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4', '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']

KEY_TOPANGLE='TopAngle'
KEY_DISP_TOPANGLE='Top Angle *'
# VALUES_TOPANGLE=[
#     '20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5',
#     '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4',
#     '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']
VALUES_ANGLESEC= connectdb("Angles")
# DISPLAY_TITLE_ANGLESEC='Select Sections'










DISP_TITLE_COMPMEM='Compression member'

KEY_SECTYPE = 'Section Type'
KEY_DISP_SECTYPE = 'Section Type*'
VALUES_SECTYPE = ['Select Type','Beams','Columns','Angles','Back to Back Angles','Star Angles','Channels','Back to back Channels']


KEY_SECSIZE = 'Section Size'
KEY_DISP_SECSIZE = 'Section Size*'
VALUES_SECSIZE_BEAMS = ['Select section','JB 150', 'JB 175', 'JB 200', 'JB 225', 'LB 100', 'LB 125', 'LB 150', 'LB 175', 'LB 200', 'LB 225', 'LB 250', 'LB 275', 'LB 300', 'LB 325', 'LB 350', 'LB 400', 'LB 450', 'LB 500', 'LB 550', 'LB 600', 'LB 75', 'LB(P) 100', 'LB(P) 175', 'LB(P) 200', 'LB(P) 300', 'MB 100', 'MB 125', 'MB 150', 'MB 175', 'MB 200', 'MB 225', 'MB 250', 'MB 300', 'MB 350', 'MB 400', 'MB 450', 'MB 500', 'MB 550', 'MB 600', 'NPB 100x55x8.1', 'NPB 120x60x10.4', 'NPB 140x70x12.9', 'NPB 160x80x15.8', 'NPB 180x90x15.4', 'NPB 180x90x18.8', 'NPB 180x90x21.3', 'NPB 200x100x18.4', 'NPB 200x100x22.4', 'NPB 200x100x25.1', 'NPB 200x130x27.2', 'NPB 200x130x32', 'NPB 220x110x26.2', 'NPB 220x110x29.4', 'NPB 240x120x26.2', 'NPB 240x120x30.7', 'NPB 240x120x34.3', 'NPB 250x125x30.1', 'NPB 250x150x33.9', 'NPB 250x150x39.8', 'NPB 250x150x46', 'NPB 250x175x43.9', 'NPB 270x135x30.7', 'NPB 270x135x36.1', 'NPB 270x135x42.3', 'NPB 300x150x36.5', 'NPB 300x150x42.2', 'NPB 300x150x49.3', 'NPB 300x165x39.9', 'NPB 300x165x45.8', 'NPB 300x165x53.5', 'NPB 300x200x59.6', 'NPB 300x200x66.7', 'NPB 300x200x74.4', 'NPB 330x160x43', 'NPB 330x160x49.1', 'NPB 330x160x57', 'NPB 350x170x50.2', 'NPB 350x170x57.1', 'NPB 350x170x66', 'NPB 350x250x79.2', 'NPB 400x180x57.4', 'NPB 400x180x66.3', 'NPB 450x190x67.2', 'NPB 450x190x77.6', 'NPB 450x190x92.4', 'NPB 500x200x107.3', 'NPB 500x200x79.4', 'NPB 500x200x90.7', 'NPB 550x210x105.5', 'NPB 550x210x122.5', 'NPB 550x210x92.1', 'NPB 600x220x107.6', 'NPB 600x220x122.4', 'NPB 600x220x154.5', 'NPB 750x270x146.9', 'NPB 750x270x174.5', 'NPB 750x270x197.7', 'NPB 750x270x202.5', 'UB 1016 x 305 x 222', 'UB 1016 x 305 x 249', 'UB 1016 x 305 x 272', 'UB 1016 x 305 x 314', 'UB 1016 x 305 x 349', 'UB 1016 x 305 x 393', 'UB 1016 x 305 x 437', 'UB 1016 x 305 x 487', 'UB 127 x 76 x 13', 'UB 152 x 89 x 16', 'UB 178 x 102 x 19', 'UB 203 x 102 x 23', 'UB 203 x 133 x 25', 'UB 203 x 133 x 30', 'UB 254 x 102 x 22', 'UB 254 x 102 x 25', 'UB 254 x 102 x 28', 'UB 254 x 146 x 31', 'UB 254 x 146 x 37', 'UB 254 x 146 x 43', 'UB 305 x 102 x 25', 'UB 305 x 102 x 28', 'UB 305 x 102 x 33', 'UB 305 x 127 x 37', 'UB 305 x 127 x 42', 'UB 305 x 127 x 48', 'UB 305 x 165 x 40', 'UB 305 x 165 x 46', 'UB 305 x 165 x 54', 'UB 356 x 127 x 33', 'UB 356 x 127 x 39', 'UB 356 x 171 x 45', 'UB 356 x 171 x 51', 'UB 356 x 171 x 57', 'UB 356 x 171 x 67', 'UB 406 x 140 x 39', 'UB 406 x 140 x 46', 'UB 406 x 178 x 54', 'UB 406 x 178 x 60', 'UB 406 x 178 x 67', 'UB 406 x 178 x 74', 'UB 457 x 152 x 52', 'UB 457 x 152 x 60', 'UB 457 x 152 x 67', 'UB 457 x 152 x 74', 'UB 457 x 152 x 82', 'UB 457 x 191 x 67', 'UB 457 x 191 x 74', 'UB 457 x 191 x 82', 'UB 457 x 191 x 89', 'UB 457 x 191 x 98', 'UB 533 x 210 x 101', 'UB 533 x 210 x 109', 'UB 533 x 210 x 122', 'UB 533 x 210 x 82', 'UB 533 x 210 x 92', 'UB 610 x 229 x 101', 'UB 610 x 229 x 113', 'UB 610 x 229 x 125', 'UB 610 x 229 x 140', 'UB 610 x 305 x 149', 'UB 610 x 305 x 179', 'UB 610 x 305 x 238', 'UB 686 x 254 x 125', 'UB 686 x 254 x 140', 'UB 686 x 254 x 152', 'UB 686 x 254 x 170', 'UB 762 x 267 x 134', 'UB 762 x 267 x 147', 'UB 762 x 267 x 173', 'UB 762 x 267 x 197', 'UB 914 x 305 x 201', 'UB 914 x 305 x 224', 'UB 914 x 305 x 253', 'UB 914 x 305 x 289', 'UB 914 x 419 x 343', 'UB 914 x 419 x 388', 'WB 150', 'WB 175', 'WB 200', 'WB 200*', 'WB 225', 'WB 250', 'WB 300', 'WB 350', 'WB 400', 'WB 450', 'WB 500', 'WB 550', 'WB 600', 'WB 600', 'WPB 100x100x12.2', 'WPB 100x100x16.7', 'WPB 100x100x20.4', 'WPB 100x100x41.8', 'WPB 120x120x15.5', 'WPB 120x120x19.9', 'WPB 120x120x26.7', 'WPB 120x120x52.1', 'WPB 140x140x18.1', 'WPB 140x140x24.7', 'WPB 140x140x33.7', 'WPB 140x140x63.2', 'WPB 160x160x23.8', 'WPB 160x160x30.4', 'WPB 160x160x42.6', 'WPB 160x160x76.2', 'WPB 180x180x28.7', 'WPB 180x180x35.5', 'WPB 180x180x51.2', 'WPB 180x180x88.9', 'WPB 200x200x101', 'WPB 200x200x103.1', 'WPB 200x200x34.6', 'WPB 200x200x42.3', 'WPB 200x200x50.9', 'WPB 200x200x61.3', 'WPB 200x200x73', 'WPB 200x200x88.2', 'WPB 220x220x117.3', 'WPB 220x220x40.4', 'WPB 220x220x50.5', 'WPB 220x220x71.5', 'WPB 240x240x156.7', 'WPB 240x240x47.4', 'WPB 240x240x60.3', 'WPB 240x240x83.2', 'WPB 250x250x104', 'WPB 250x250x117.6', 'WPB 250x250x133.9', 'WPB 250x250x151.7', 'WPB 250x250x74.5', 'WPB 260x260x172.4', 'WPB 260x260x54.1', 'WPB 260x260x68.2', 'WPB 260x260x93', 'WPB 280x280x103.1', 'WPB 280x280x188.5', 'WPB 280x280x61.2', 'WPB 280x280x76.4', 'WPB 300x300x117', 'WPB 300x300x237.9', 'WPB 300x300x69.8', 'WPB 300x300x88.3', 'WPB 300x300x96.8', 'WPB 320x300x126.7', 'WPB 320x300x245', 'WPB 320x300x74.2', 'WPB 320x300x97.6', 'WPB 340x300x104.8', 'WPB 340x300x134.2', 'WPB 340x300x247.9', 'WPB 340x300x78.9', 'WPB 360x300x112.1', 'WPB 360x300x141.8', 'WPB 360x300x250.3', 'WPB 360x300x83.7', 'WPB 360x370x137.3', 'WPB 360x370x150.9', 'WPB 360x370x165.3', 'WPB 360x370x182.6', 'WPB 360x370x199.9', 'WPB 400x300x124.8', 'WPB 400x300x155.3', 'WPB 400x300x255.7', 'WPB 400x300x92.4', 'WPB 400x400x189.9', 'WPB 400x400x219.7', 'WPB 400x400x239.6', 'WPB 450x300x139.8', 'WPB 450x300x171.1', 'WPB 450x300x263.3', 'WPB 450x300x99.7', 'WPB 500x300x107.4', 'WPB 500x300x128.7', 'WPB 500x300x155.1', 'WPB 500x300x187.3', 'WPB 500x300x270.3', 'WPB 550x300x120', 'WPB 550x300x166.2', 'WPB 550x300x199.4', 'WPB 550x300x278.2', 'WPB 600x300x128.8', 'WPB 600x300x177.8', 'WPB 600x300x211.9', 'WPB 600x300x285.5', 'WPB 650x300x138', 'WPB 650x300x189.7', 'WPB 650x300x224.8', 'WPB 650x300x293.4', 'WPB 700x300x149.9', 'WPB 700x300x204.5', 'WPB 700x300x240.5', 'WPB 700x300x300.7', 'WPB 800x300x171.5', 'WPB 800x300x224.4', 'WPB 800x300x262.3', 'WPB 800x300x317.3', 'WPB 850x300x179.9', 'WPB 850x300x197.5', 'WPB 850x300x214.7', 'WPB 850x300x230.5', 'WPB 850x300x254.5', 'WPB 900x300x198', 'WPB 900x300x251.6', 'WPB 900x300x291.5']
VALUES_SECSIZE_COLUMNS = ['Select section','HB 150','HB 150*','HB 150*','HB 200','HB 200*','HB 225','HB 225*','HB 250','HB 250*','HB 300','HB 300*','HB 350','HB 350*','HB 400','HB 400*','HB 450','HB 450*','PBP 200X43.8','PBP 200X53.5','PBP 220X57.2','PBP 260X75''PBP 260X87.3','PBP 300X110','PBP 300X126.1','PBP 300X149.1','PBP 300X180','PBP 300X186','PBP 300X222.9','PBP 300X78.4','PBP 300X88','PBP 300X94.9','PBP 320X102.8','PBP 320X117.3','PBP 320X146.7','PBP 320X184.1','PBP 320X88.5','PBP 360X108.9','PBP 360X133','PBP 360X152','PBP 360X173.9','PBP 360X180.2','PBP 360X84.3','PBP 400X122.4','PBP 400X140.2','PBP 400X158.1','PBP 400X176.1','PBP 400X194.2','PBP 400X212.5','PBP 400X230.9','SC 100','SC 120','SC 140','SC 150*','SC 160','SC 180','SC 200','SC 220','SC 250','UC 152 x 152 x 23','UC 152 x 152 x 30','UC 152 x 152 x 37','UC 203 x 203 x 46','UC 203 x 203 x 52','UC 203 x 203 x 60','UC 203 x 203 x 71','UC 203 x 203 x 86','UC 254 x 254 x 107','UC 254 x 254 x 132','UC 254 x 254 x 167','UC 254 x 254 x 73','UC 254 x 254 x 89','UC 305 x 305 x 118','UC 305 x 305 x 137','UC 305 x 305 x 158','UC 305 x 305 x 198','UC 305 x 305 x 240','UC 305 x 305 x 283','UC 305 x 305 x 97','UC 356 x 368 x 129','UC 356 x 368 x 153','UC 356 x 368 x 177','UC 356 x 368 x 202','UC 356 x 406 x 235','UC 356 x 406 x 287','UC 356 x 406 x 340','UC 356 x 406 x 393','UC 356 x 406 x 467','UC 356 x 406 x 551','UC 356 x 406 x 634']
VALUES_SECSIZE_ANGLES = ['20 20 X 3', '20 20 X 4', '25 25 x 3', '25 25 x 4', '25 25 x 5', '30 30 x 3', '30 30 x 4', '30 30 x 5', '35 35 x 3', '35 35 x 4', '35 35 x 5', '35 35 x 6', '40 40 x 3', '40 40 x 4', '40 40 x 5', '40 40 x 6', '45 45 x 3', '45 45 x 4', '45 45 x 5', '45 45 x 6', '50 50 x 3', '50 50 x 4', '50 50 x 5', '50 50 x 6', '50 50 x 7', '50 50 x 8', '55 55 x 4', '55 55 x 5', '55 55 x 6', '55 55 x 8', '55 55 x 10', '60 60 x 4', '60 60 x 5', '60 60 x 6', '60 60 x 8', '60 60 x 10', '65 65 x 4', '65 65 x 5', '65 65 x 6', '65 65 x 8', '65 65 x 10', '70 70 x 5', '70 70 x 6', '70 70 x 7', '70 70 x 8', '70 70 x 10', '75 75 x 5', '75 75 x 6', '75 75 x 8', '75 75 x 10', '80 80 x 6', '80 80 x 8', '80 80 x 10', '80 80 x 12', '90 90 x 6', '90 90 x 8', '90 90 x 10', '90 90 x 12', '100 100 x 6', '100 100 x 7', '100 100 x 8', '100 100 x 10', '100 100x 12', '100 100 x 15', '110 110 X 8', '110 110 X 10', '110 110 X 12', '110 110 X 16', '120 120 X 8', '120 120 X 10', '120 120 X 12', '120 120 X 15', '130 130 X 8', '130 130 X 9', '130 130 X 10', '130 130 X 12', '130 130 X 16', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '150 150 X 10', '150 150 X 12', '150 150 X 15', '150 150 X 16', '150 150 X 18', '150 150 X 20', '180 180 X 15', '180 180 X 18', '180 180 X 20', '200 200 X 12', '200 200 X 16', '200 200 X 20', '200 200 X 24', '200 200 X 25', '30 20 X 3', '30 20 X 4', '30 20 X 5', '40 20 X 3', '40 20 X 4', '40 20 X 5', '40 25 X 3', '40 25 X 4', '40 25 X 5', '40 25 X 6', '45 30 X 3', '45 30 X 4', '45 30 X 5', '45 30 X 6', '50 30 X 3', '50 30 X 4', '50 30 X 5', '50 30 X 6', '60 30 X 5', '60 30 X 6', '60 40 X 5', '60 40 X 6', '60 40 X 7', '60 40 X 8', '65 45 X 5', '65 45 X 6', '65 45 X 8', '65 50 X 5', '65 50 X 6', '65 50 X 7', '65 50 X 8', '70 45 X 5', '70 45 X 6', '70 45 X 8', '70 45 X 10', '70 50 X 5', '70 50 X 6', '70 50 X 7', '70 50 X 8', '75 50X 5', '75 50X 6', '75 50X 7', '75 50X 8', '75 50X 10', '80 40 X 5', '80 40 X 6', '80 40 X 7', '80 40 X 8', '80 50 X 5', '80 50 X  6', '80 50 X  8', '80 50 X 10', '80 60 X 6', '80 60 X 7', '80 60 X 8', '90 60 X 6', '90 60 X  8', '90 60 X 10', '90 60 X 12', '90 65 X 6', '90 65 X 7', '90 65 X 8', '90 65 X 10', '100 50 X 6', '100 50 X 7', '100 50 X 8', '100 50 X 10', '100 65 X 6', '100 65 X  7', '100 65 X  8', '100 65 X 10', '100 75 X 6', '100 75 X  8', '100 75 X 10', '100 75 X 12', '120 80 X 8', '120 80 X 10', '120 80 X 12', '125 75 X 6', '125 75 X  8', '125 75 X 10', '125 75 X 12', '125 95 X 6', '125 95 X  8', '125 95 X 10', '125 95 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '135 65 X 8', '135 65 X 10', '135 65 X 12', '150 75 X 8', '150 75 X  9', '150 75 X 10', '150 75 X 12', '150 75 X 15', '150 90 X 10', '150 90 X X 12', '150 90 X X 15', '150 90 X 10', '150 90 X 12', '150 90 X 15', '150 115 X 8', '150 115 X 10', '150 115 X 12', '150 115 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 100 X 10', '200 100 X 12', '200 100 X 15', '200 100 X 16', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20', '200 150 X 10', '200 150 X 12', '200 150 X 15', '200 150 X 16', '200 150 X 18', '200 150 X 20']
VALUES_SECSIZE_CHANNELS = ['JC 100', 'JC 125', 'JC 150', 'JC 175', 'JC 200', 'LC 100', 'LC 125', 'LC 150', 'LC 175', 'LC 200', 'LC 225', 'LC 250', 'LC 300', 'LC 350', 'LC 400', 'LC 75', 'LC(P )150', 'LC(P) 125', 'LC(P) 200', 'LC(P) 300', 'MC 100', 'MC 125', 'MC 125*', 'MC 150', 'MC 150*', 'MC 175', 'MC 175*', 'MC 200', 'MC 200*', 'MC 225', 'MC 225*', 'MC 250', 'MC 250*', 'MC 250*', 'MC 300', 'MC 300*', 'MC 300*', 'MC 350', 'MC 400', 'MC 75  ', 'MCP 100', 'MCP 125', 'MCP 125*', 'MCP 150', 'MCP 150*', 'MCP 175', 'MCP 175*', 'MCP 200', 'MCP 200*', 'MCP 225', 'MCP 225*', 'MCP 250', 'MCP 250*', 'MCP 250*', 'MCP 300', 'MCP 300*', 'MCP 300*', 'MCP 350', 'MCP 400', 'MCP 75']
VALUES_SECSIZE_OTHER = ['Select section']


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


DISP_TITLE_SC = 'Support Condition'


KEY_END1_TRANSLATION = 'End 1'
KEY_END1_ROTATION = 'End 1'
KEY_DISP_END1 = 'End 1'
VALUES_END1_TRANSLATION = ['Translation','Free','Restrained']
VALUES_END1_ROTATION = ['Rotation','Free','Restrained']


KEY_END2_TRANSLATION = 'End 2'
KEY_END2_ROTATION = 'End 2'
KEY_DISP_END2 = 'End 2'
VALUES_END2_TRANSLATION = ['Translation','Free','Restrained']
VALUES_END2_ROTATION = ['Rotation','Free','Restrained']


KEY_LENZZ = 'Member.Length_zz'
KEY_DISP_LENZZ = 'Length (z-z)'


KEY_LENYY = 'Length'
KEY_DISP_LENYY = 'Length (y-y)'


KEY_CONNLOC = 'Conn Location'
KEY_DISP_CONNLOC = 'Conn Location'
VALUES_CONNLOC_BOLT = ['Bolted','Web','Flange','Leg','Back to Back Web','Back to Back Angles','Star Angles']
VALUES_CONNLOC_WELD = ['Welded','Web','Flange','Leg','Back to Back Web','Back to Back Angles','Star Angles']


KEY_LEN_INLINE = 'Total length in line with tension'
KEY_DISP_LEN_INLINE = 'Total Length in line with tension'

KEY_LEN_OPPLINE = 'Total length opp line with tension'
KEY_DISP_LEN_OPPLINE = 'Total Length opp line with tension'
