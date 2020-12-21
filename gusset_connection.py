from design_type.connection.connection import Connection
from design_type.member import Member
from Common import *
import sqlite3
import logging
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog, QMessageBox
import sys

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


# Keys for output_dock
KEY_OUT_D_PROVIDED = 'Bolt.Diameter'
KEY_OUT_DISP_D_PROVIDED = 'Diameter (mm)'
KEY_OUT_GRD_PROVIDED = 'Bolt.Grade_Provided'
KEY_OUT_DISP_GRD_PROVIDED = 'Grade'
KEY_OUT_BOLT_SHEAR = 'Bolt.Shear'
KEY_OUT_DISP_BOLT_SHEAR = 'Shear Capacity (kN)'
KEY_OUT_BOLT_BEARING = 'Bolt.Bearing'
KEY_OUT_DISP_BOLT_BEARING = 'Bearing Capacity (kN)'
KEY_OUT_BOLT_CAPACITY = 'Bolt.Capacity'
KEY_OUT_DISP_BOLT_CAPACITY = 'Capacity (kN)'
VALUE_NOT_APPLICABLE = 'N/A'


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

class GussetConnection(Connection,Member):

    def __init__(self):
        super(GussetConnection, self).__init__()

    ###############################################
    # Design Preference Functions Start
    ###############################################

    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """
        tabs = []

        t1 = (DISP_TITLE_ANGLE, TYPE_TAB_1, self.tab_angle_section)
        tabs.append(t1)

        t2 = (DISP_TITLE_CHANNEL, TYPE_TAB_1, self.tab_channel_section)
        tabs.append(t2)

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t3 = ("Bolt", TYPE_TAB_2, self.bolt_values)
        tabs.append(t3)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):
        """

        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
         It returns list of tuple which contains, tab name, keys whose values will be changed,
         function to change the values and arguments for the function.

         [Tab Name, [Argument list], [list of keys to be updated], input widget type of keys, change_function]

         Here Argument list should have only one element.
         Changing of this element,(either changing index or text depending on widget type),
         will update the list of keys (this can be more than one).
         TODO: input widget type of keys (3rd element) is no longer required. needs to be removed

         """
        change_tab = []

        t1 = (DISP_TITLE_ANGLE, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5',
               'Label_7', 'Label_8', 'Label_9',
               'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17',
               'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23', 'Label_24', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_new_angle_section_properties)
        change_tab.append(t1)

        t2 = (DISP_TITLE_ANGLE, ['Label_1', 'Label_2', 'Label_3', 'Label_0'],
              ['Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_13', 'Label_14',
               'Label_15',
               'Label_16', 'Label_17', 'Label_18', 'Label_19', 'Label_20', 'Label_21', 'Label_22', 'Label_23',
               KEY_IMAGE],
              TYPE_TEXTBOX, self.get_Angle_sec_properties)
        change_tab.append(t2)

        t3 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE, KEY_SEC_MATERIAL, 'Label_0'],
              [KEY_SECSIZE_SELECTED, KEY_SEC_FY, KEY_SEC_FU, 'Label_1', 'Label_2', 'Label_3', 'Label_13',
               'Label_14',
               'Label_4', 'Label_5',
               'Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17',
               'Label_19', 'Label_20', 'Label_21',
               'Label_22', 'Label_23', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_new_channel_section_properties)
        change_tab.append(t3)

        t4 = (DISP_TITLE_CHANNEL, ['Label_1', 'Label_2', 'Label_3', 'Label_13', 'Label_14'],
              ['Label_9', 'Label_10', 'Label_11', 'Label_12', 'Label_15', 'Label_16', 'Label_17', 'Label_19',
               'Label_20', 'Label_21', 'Label_22', 'Label_26', 'Label_27', KEY_IMAGE], TYPE_TEXTBOX,
              self.get_Channel_sec_properties)

        change_tab.append(t4)

        t5 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)

        change_tab.append(t5)

        t6 = (DISP_TITLE_ANGLE, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t6)

        t7 = (DISP_TITLE_CHANNEL, [KEY_SECSIZE_SELECTED], [KEY_SOURCE], TYPE_TEXTBOX, self.change_source)
        change_tab.append(t7)

        return change_tab

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (DISP_TITLE_ANGLE, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        t2 = (DISP_TITLE_CHANNEL, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        t3 = ("Bolt", TYPE_COMBOBOX, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR])
        design_input.append(t3)

        # t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        # design_input.append(t4)
        #
        # t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        # design_input.append(t4)
        #
        # t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        # design_input.append(t5)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DETAILING_EDGE_TYPE])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

        :return: Returns list of tuples which have the design preference keys to be stored if user does not open
        design preference (since deisgn preference values are saved on click of 'save' this function is necessary'

        ([Key need to get default values, list of design prefernce values, source of key])

        TODO: list of design preference values are sufficient in this function
         since whole of input dock design dictionary is being passed anyway in ui template
        """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_BOLT_TYPE, KEY_DP_BOLT_HOLE_TYPE, KEY_DP_BOLT_SLIP_FACTOR,
                     KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_EDGE_TYPE,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

         :return: This function returns list of tuples which has keys that needs to be updated,
          on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

          [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
         """

        add_buttons = []

        t2 = (DISP_TITLE_ANGLE, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Angles', 'Back to Back Angles', 'Star Angles'], "Angles")
        add_buttons.append(t2)

        t2 = (DISP_TITLE_CHANNEL, KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, KEY_SECSIZE_SELECTED, KEY_SEC_PROFILE,
              ['Channels', 'Back to Back Channels'], "Channels")
        add_buttons.append(t2)

        return add_buttons

    ####################################
    # Design Preference Functions End
    ####################################

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

        t16 = (KEY_MODULE, KEY_DISP_GUSSET, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_MEMBER_COUNT, KEY_DISP_MEMBER_COUNT, TYPE_COMBOBOX, VALUES_MEM_COUNT, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_IMAGE, None, TYPE_IMAGE, "./ResourceFiles/images/sample_gusset.png", True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_SEC_PROFILE, KEY_DISP_SEC_PROFILE, TYPE_COMBOBOX, VALUES_SEC_PROFILE, True, 'No Validator')
        options_list.append(t4)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, VALUES_SECSIZE, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t6 = (None, DISP_TITLE_LOADS, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, VALUES_AXIAL, True, 'Int Validator')
        options_list.append(t8)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
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

        t2 = ([KEY_SEC_PROFILE], KEY_SECSIZE, TYPE_COMBOBOX_CUSTOMIZED, self.fn_profile_section)
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


    def set_input_values(self, design_dictionary):
        self.section = design_dictionary[KEY_SECSIZE][0]
        self.membercount = design_dictionary[KEY_MEMBER_COUNT]
        self.load = design_dictionary[KEY_AXIAL]
        self.bolt = Bolt(grade=[8.8], diameter=design_dictionary[KEY_D],
                         bolt_type='Bearing Bolt')
        self.bolt_details = {
            'diameter':self.bolt.bolt_diameter[0],
            'grade': 8.8,
            'number of bolts': 4}

    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []

        t1 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (
        KEY_OUT_D_PROVIDED, KEY_OUT_DISP_D_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_diameter_provided if flag else '',
        True)
        out_list.append(t2)

        t3 = (
        KEY_OUT_GRD_PROVIDED, KEY_OUT_DISP_GRD_PROVIDED, TYPE_TEXTBOX, self.bolt.bolt_grade_provided if flag else '',
        True)

        out_list.append(t3)

        t4 = (KEY_OUT_BOLT_SHEAR, KEY_OUT_DISP_BOLT_SHEAR, TYPE_TEXTBOX,
              round(self.bolt.bolt_shear_capacity / 1000, 2) if flag else '', True)
        out_list.append(t4)

        bolt_bearing_capacity_disp = ''
        if flag is True:
            if self.bolt.bolt_bearing_capacity is not VALUE_NOT_APPLICABLE:
                bolt_bearing_capacity_disp = round(self.bolt.bolt_bearing_capacity / 1000, 2)

        t5 = (
        KEY_OUT_BOLT_BEARING, KEY_OUT_DISP_BOLT_BEARING, TYPE_TEXTBOX, bolt_bearing_capacity_disp if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_BOLT_CAPACITY, KEY_OUT_DISP_BOLT_CAPACITY, TYPE_TEXTBOX,
              round(self.bolt.bolt_capacity / 1000, 2) if flag else '', True)
        out_list.append(t6)

        return out_list

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
                               rel_path, Disp_3D_image, module=self.module)

    def show_error_message(self):
        QMessageBox.about(self, 'information', "Your message!")

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('End Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'End Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Plate", bgcolor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    from gui.ui_template import Ui_ModuleWindow
    window = Ui_ModuleWindow(GussetConnection,'')
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("ERROR")