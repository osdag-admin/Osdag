from design_type.connection.connection import Connection
# from Common import *
import sqlite3
import logging
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import sys
from gui.ui_template import Ui_ModuleWindow
from utils.common.component import Bolt
from design_report.reportGenerator_latex import CreateLatex

PATH_TO_DATABASE = "ResourceFiles/Database/Intg_osdag.sqlite"

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

    final_lst = tuple_to_str(lst, call_type)
    return final_lst

def tuple_to_str(tl, call_type):
    if call_type is "dropdown":
        arr = ['Select Section']
    else:
        arr = []
    for v in tl:
        val = ''.join(v)
        arr.append(val)
    return arr

def tuple_to_str_popup(tl):

    # @author: Amir

    arr = []
    for v in tl:
        val = ''.join(v)
        arr.append(val)
    return arr
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

######### Just FOR Documentation ########
KEY_DISP_GUSSET = 'Gusset Connection'

KEY_MODULE = 'Module'
TYPE_MODULE = 'Window Title'

KEY_IMAGE = 'Image'

DISP_TITLE_CM = 'Connecting members'

KEY_MEMBER_COUNT = 'Member.Count'
KEY_DISP_MEMBER_COUNT = 'Member Count'
VALUES_MEM_COUNT = ['1','2','3','4','5','6','7']

KEY_SEC_PROFILE = 'Member.Profile'
KEY_DISP_SEC_PROFILE = 'Section Profile'
VALUES_SEC_PROFILE = ['Angles', 'Channels']

KEY_SECSIZE = 'Member.Designation'
KEY_DISP_SECSIZE = 'Section Size*'
VALUES_SECSIZE = ['All', 'Customized']

KEY_MATERIAL = 'Member.Material'
KEY_DISP_MATERIAL = 'Material *'
VALUES_MATERIAL = connectdb("Material")

DISP_TITLE_LOADS = 'Factored load'
KEY_AXIAL = 'Load.Axial'
KEY_DISP_AXIAL = 'Axial (kN) *'
VALUES_AXIAL = ['Minimum','Customized']

# Key for storing Diameter sub-key of Bolt
DISP_TITLE_BOLT = 'Bolt'
KEY_D = 'Bolt.Diameter'
KEY_DISP_D = 'Diameter(mm)*'
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


DISP_TITLE_PLATE = 'Plate'
KEY_PLATETHK = 'Plate.Thickness'
VALUES_PLATETHK = ['All', 'Customized']
VALUES_PLATETHK_CUSTOMIZED = ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30']

# Keys for design_pref
KEY_SUPTNGSEC_DESIGNATION = 'Supporting_Section.Designation'
KEY_DISP_SUPTNGSEC_DESIGNATION = 'Designation'
KEY_DISP_MECH_PROP = 'Mechanical Properties'
KEY_SUPTNGSEC_FU = 'Supporting_Section.Ultimate_Strength'
KEY_DISP_SUPTNGSEC_FU = 'Ultimate strength, fu (MPa)'
KEY_SUPTNGSEC_FY = 'Supporting_Section.Yield_Strength'
KEY_DISP_SUPTNGSEC_FY = 'Yield Strength , fy (MPa)'
KEY_PLATE_MATERIAL = 'Plate.Material'
KEY_PLATE_FU = 'Plate.Ultimate_Strength'
KEY_DISP_PLATE_FU = 'Ultimate strength, fu (MPa)'
KEY_PLATE_FY = 'Plate.Yield_Strength'
KEY_DISP_PLATE_FY = 'Yield Strength , fy (MPa)'


TYPE_COMBOBOX = 'ComboBox'
TYPE_TEXTBOX = 'TextBox'
TYPE_TITLE = 'Title'
TYPE_LABEL = 'Label'
TYPE_IMAGE = 'Image'
TYPE_IMAGE_COMPRESSION = 'Image_compression'
TYPE_COMBOBOX_CUSTOMIZED = 'ComboBox_Customized'
TYPE_OUT_BUTTON = 'Output_dock_Button'
TYPE_BREAK = 'Break'
TYPE_ENTER = 'Enter'
TYPE_TEXT_BROWSER = 'TextBrowser'
TYPE_NOTE = 'Note'
TYPE_TAB_1 = "TYPE_TAB_1"
TYPE_TAB_2 = "TYPE_TAB_2"


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

class GussetConnection(Connection):

    def __init__(self):
        super(GussetConnection, self).__init__()

    def set_osdaglogger(key):

        """
        Function to set Logger for FinPlate Module
        """

        # @author Arsil Zunzunia
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
        return KEY_DISP_GUSSET

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)
        '''
        # @author: Amir, Umair
        self.module = KEY_DISP_GUSSET

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_GUSSET, TYPE_MODULE, None, None)
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t2 = (KEY_MEMBER_COUNT, KEY_DISP_MEMBER_COUNT, TYPE_COMBOBOX, None, VALUES_MEM_COUNT)
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/sample_gusset.png")
        options_list.append(t3)

        t4 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, None, VALUES_SEC_PROFILE)
        options_list.append(t4)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, None, VALUES_SECSIZE)
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, None, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_LOADS, TYPE_TITLE, None, None)
        options_list.append(t6)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, None, VALUES_AXIAL)
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, None, VALUES_D)
        options_list.append(t10)


        return options_list

    def customized_input(self):

        list1 = []
        t1 = (KEY_SECSIZE, self.fn_profile_section)
        list1.append(t1)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        return list1

    def fn_profile_section(self):

        "Function to populate combobox based on the section type selected"

        # print(self,"2")
        if self == 'Beams':
            return connectdb("Beams", call_type="popup")
        elif self == 'Columns':
            return connectdb("Columns", call_type= "popup")
        elif self in ['Angles', 'Back to Back Angles', 'Star Angles']:
            return connectdb("Angles", call_type= "popup")
        elif self in ['Channels', 'Back to Back Channels']:
            return connectdb("Channels", call_type= "popup")

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    def input_value_changed(self):

        lst = []

        t2 = (KEY_SEC_PROFILE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
        lst.append(t2)

        return lst

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        option_list = self.input_values(self)
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    all_errors.append('Please input '+option[1])
            # Since all COMBO BOX have default value except material, we can check only for Material.
            if option[0] == KEY_MATERIAL:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    all_errors.append('Please input '+option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    all_errors.append('Please input '+option[1])

        if all_errors == []:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors

    def tab_list(self):
        tabs = []

        t1 = ("Column", TYPE_TAB_1, self.tab_column_section)
        tabs.append(t1)

        t7 = ("Connector", TYPE_TAB_2, self.connector_values)
        tabs.append(t7)

        return tabs

    @staticmethod
    def tab_column_section():
        supporting_section = []
        t1 = (KEY_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_DESIGNATION, TYPE_TEXTBOX, None)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None)
        supporting_section.append(t2)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_SUPTNGSEC_FU, TYPE_TEXTBOX, None)
        supporting_section.append(t3)

        return supporting_section

    @staticmethod
    def connector_values():
        connector = []

        material = connectdb("Material", call_type="popup")
        material.append('Custom')
        t1 = (KEY_PLATE_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material)
        connector.append(t1)

        t2 = (KEY_PLATE_FU, KEY_DISP_PLATE_FU, TYPE_TEXTBOX, None)
        connector.append(t2)

        t3 = (KEY_PLATE_FY, KEY_DISP_PLATE_FY, TYPE_TEXTBOX, None)
        connector.append(t3)

        return connector

    def set_input_values(self, design_dictionary):
        self.section = design_dictionary[KEY_SECSIZE][0]
        self.membercount = design_dictionary[KEY_MEMBER_COUNT]
        self.load = design_dictionary[KEY_AXIAL]
        self.bolt = Bolt(grade=[8.8], diameter=design_dictionary[KEY_D],
                         bolt_type='Bearing Bolt',
                         material_grade=design_dictionary[KEY_MATERIAL])
        self.bolt_details = {
            'diameter':self.bolt.bolt_diameter[0],
            'grade': 8.8,
            'number of bolts': 4}

    def save_design(self,popup_summary):

        self.report_input = \
            {KEY_MODULE: self.module,
             'Num of Members':self.membercount,
             'Load': self.load,
             KEY_DISP_D: str(self.bolt.bolt_diameter),
             KEY_DISP_GRD: str(self.bolt.bolt_grade),
             KEY_DISP_TYP: self.bolt.bolt_type}

        self.report_check = []

        t1 = ('SubSection', 'Bolt Design Checks','|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)

        if self.bolt.bolt_type == TYP_BEARING:
            t1 = ('Bolt Shear Capacity', '', '50', '')
            self.report_check.append(t1)
            t2 = ('Bolt Bearing Capacity', '', '40', '')
            self.report_check.append(t2)
            t3 = ('Bolt capacity', '35','40','Pass')
            self.report_check.append(t3)
        else:

            t4 = ('Bolt slip capacity', '60','70','Pass')
            self.report_check.append(t4)


        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")

        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                               rel_path, Disp_3D_image)

class MainController(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, Ui_ModuleWindow, main):
        super(MainController,self).__init__()
        QMainWindow.__init__(self)
        self.ui = Ui_ModuleWindow()
        self.ui.setupUi(self, main, '')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainController(Ui_ModuleWindow,GussetConnection)
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("ERROR")
