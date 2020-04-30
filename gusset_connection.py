from design_type.connection.connection import Connection
# from Common import *
import sqlite3
import logging
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import sys
from gui.ui_template import Ui_ModuleWindow

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

    def input_values(self, existingvalues={}):

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

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_COMBOBOX_CUSTOMIZED, None, VALUES_AXIAL)
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


