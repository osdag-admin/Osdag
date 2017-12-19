#!/home/deepa-c/miniconda2/bin/python
'''
Created on 31-Mar-2016

@author: deepa
'''

import sys
from PyQt5 import Qt

from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication
from ui_OsdagMainPage import Ui_MainWindow
from ui_tutorial import Ui_Tutorial
from ui_aboutosdag import Ui_AboutOsdag
from ui_ask_question import Ui_AskQuestion
from Connections.Shear.Finplate.finPlateMain import launchFinPlateController

import os
from Connections.Shear.SeatedAngle.seat_angle_main import launchSeatedAngleController
from Connections.Shear.cleatAngle.cleatAngleMain import launch_cleatangle_controller
from Connections.Shear.Endplate.endPlateMain import launch_endplate_controller
import os.path
import subprocess
import shutil

import ConfigParser


class MyTutorials(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Tutorial()
        self.ui.setupUi(self)
        self.osdagmainwindow = parent


class MyAboutOsdag(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AboutOsdag()
        self.ui.setupUi(self)
        self.osdagmainwindow = parent

class MyAskQuestion(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AskQuestion()
        self.ui.setupUi(self)
        self.osdagmainwindow = parent

class OsdagMainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        #show_msg = pyqtSignal()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        list_of_items = {'Osdagpage': 0, 'connectionpage': 1, 'tensionpage': 2, 'compressionpage': 3, 'flexuralpage': 4}

        self.ui.myStackedWidget.setCurrentIndex(list_of_items['Osdagpage'])
        self.ui.btn_connection.clicked.connect(lambda: self.change_desgin_page(list_of_items['connectionpage'], list_of_items['Osdagpage']))
        self.ui.myListWidget.currentItemChanged.connect(self.change_desgin_page)
        self.ui.btn_start.clicked.connect(self.show_design_connection)
        self.ui.btn_beamCol.clicked.connect(self.unavailable)
        self.ui.btn_compression.clicked.connect(self.unavailable)
        self.ui.btn_flexural.clicked.connect(self.unavailable)
        self.ui.btn_truss.clicked.connect(self.unavailable)
        self.ui.btn_2dframe.clicked.connect(self.unavailable)
        self.ui.btn_3dframe.clicked.connect(self.unavailable)
        self.ui.btn_groupdesign.clicked.connect(self.unavailable)
        self.ui.btn_tension.clicked.connect(self.unavailable)
        self.ui.btn_plate.clicked.connect(self.unavailable)
        self.ui.comboBox_help.setCurrentIndex(0)
        self.ui.comboBox_help.currentIndexChanged.connect(self.selection_change)

    def selection_change(self):
        loc = self.ui.comboBox_help.currentText()
        if loc == "Design Examples":
            self.design_examples()
        elif loc == "Video Tutorials":
            self.open_tutorials()
        elif loc == "About Osdag":
            self.about_osdag()
        elif loc == "Ask Us a Question":
            self.ask_question()
        # elif loc == "FAQ":
        #     pass

    def disable_desgin_buttons(self):
        self.ui.btn_beamCol.setEnabled(False)
        self.ui.btn_compression.setEnabled(False)
        self.ui.btn_connection.setEnabled(False)
        self.ui.btn_flexural.setEnabled(False)
        self.ui.btn_gantry.setEnabled(False)
        self.ui.btn_plate.setEnabled(False)
        self.ui.btn_tension.setEnabled(False)
        self.ui.btn_help.setEnabled(False)

    def enable_desgin_buttons(self):
        self.ui.btn_beamCol.setEnabled(True)
        self.ui.btn_compression.setEnabled(True)
        self.ui.btn_connection.setEnabled(True)
        self.ui.btn_flexural.setEnabled(True)
        self.ui.btn_gantry.setEnabled(True)
        self.ui.btn_plate.setEnabled(True)
        self.ui.btn_tension.setEnabled(True)
        self.ui.btn_help.setEnabled(True)

    def change_desgin_page(self, current, previous):
        if not current:
            current = previous

        self.ui.myStackedWidget.setCurrentIndex(current)

    def show_design_connection(self):

        # config = ConfigParser.ConfigParser()
        # config.read(open(r'Osdag.config'))
        # default_workspace_path = config.get('default_workspace', 'path1')
        # folder = QFileDialog.getExistingDirectory(self, 'Select Folder', default_workspace_path)
        folder = "F:\Osdag\Osdag_workspace"
        if not os.path.exists(folder):
            if folder == '':
                pass
            else:
                os.mkdir(folder, 0755)

        root_path = folder
        images_html_folder = ['images_html']
        flag = True
        for create_folder in images_html_folder:
            if root_path == '':
                flag = False
                return flag
            else:
                try:
                    os.mkdir(os.path.join(root_path, create_folder))
                except OSError:
                    shutil.rmtree(os.path.join(folder, create_folder))
                    os.mkdir(os.path.join(root_path, create_folder))

        if self.ui.rdbtn_finplate.isChecked():
            launchFinPlateController(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)

        elif self.ui.rdbtn_cleat.isChecked():
            launch_cleatangle_controller(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)

        elif self.ui.rdbtn_endplate.isChecked():
            launch_endplate_controller(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)
            # QMessageBox.about(self,"INFO","End plate connection design is coming soon!")

        elif self.ui.rdbtn_seat.isChecked():
            launchSeatedAngleController(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)

        else:
            QMessageBox.about(self, "INFO", "Please select appropriate connection")

    # ********************************* Help Action *********************************************************************************************

    def about_osdag(self):
        dialog = MyAboutOsdag(self)
        dialog.show()

    def open_osdag(self):
        self.about_osdag()

    def tutorials(self):
        dialog = MyTutorials(self)
        dialog.show()

    def open_tutorials(self):
        self.tutorials()

    def ask_question(self):
        dialog = MyAskQuestion(self)
        dialog.show()

    def open_question(self):
        self.ask_question()

    def design_examples(self):
        root_path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'design_example', '_build', 'html')
        for html_file in os.listdir(root_path):
            if html_file.startswith('index'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, html_file))
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, html_file)])

    def unavailable(self):
        QMessageBox.about(self, "INFO", "This module is not available in the current version.")
        # Following code maintain for future coding.
        # self.ui.btn_beamCol.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_compression.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_flexural.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_gantry.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_plate.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_tension.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))


    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def the_exception_hook(exctype, value, traceback):
        '''Finds the error occurs when Osdag crashes

        Args:
            exctype: type of error
            value: information of the error
            traceback: trace the object

        Returns:
            system exit(1)
        '''
        # Print the error and traceback
        print "Error occurred: ", (exctype, value, traceback)
        # Call the normal Exception hook after
        sys.__excepthook__(exctype, value, traceback)
        sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = the_exception_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print "ERROR"
