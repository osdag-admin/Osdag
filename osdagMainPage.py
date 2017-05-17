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
        self.ui.btn_gantry.clicked.connect(self.unavailable)
        self.ui.btn_tension.clicked.connect(self.unavailable)
        self.ui.btn_plate.clicked.connect(self.unavailable)
        self.ui.comboBox_help.setCurrentIndex(0)
        self.ui.comboBox_help.currentIndexChanged.connect(self.selection_change)



    def selection_change(self):
        loc = self.ui.comboBox_help.currentText()
        if loc == "Sample Design Report":
            self.sample_report()
        elif loc == "Sample Problems":
            self.sample_problem()
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

        options = QFileDialog.Options()
        folder, _ = QFileDialog.getSaveFileName(self, 'Select Workspace Directory', os.path.join('..','..','Osdag_workspace'),"All Files (*)", options=options)
        folder = str(folder)
        if not os.path.exists(folder):
            os.mkdir(folder, 0755)

        root_path = folder
        images_html_folder = ['images_html']
        for create_folder in images_html_folder:
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

    def sample_report(self):

        root_path = os.path.join(os.path.dirname(__file__), 'Sample_Folder', 'Sample_Report')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def sample_problem(self):
        root_path = os.path.join(os.path.dirname(__file__), 'Sample_Folder', 'Sample_Problems')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])



    def unavailable(self):
        QMessageBox.about(self, "INFO", "This module is not available in the current version.")
        # Following code maintain for future coding.
        # self.ui.btn_beamCol.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_compression.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_flexural.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_gantry.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_plate.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_tension.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    sys.exit(app.exec_())
