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
        pass

    def module_name(self):
        return KEY_DISP_GUSSET

    def input_values(self, existingvalues={}):
        pass

    def customized_input(self):
        pass

    def input_value_changed(self):
        pass


class MainController(QMainWindow):
    # closed = pyqtSignal()
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
