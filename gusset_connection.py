from design_type.connection.connection import Connection
from Common import *
import logging
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import sys
from gui.ui_template import Ui_ModuleWindow


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
