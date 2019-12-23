#!/home/deepa-c/miniconda2/bin/python
'''
Created on 31-Mar-2016

@author: darshan
'''

import sys
# from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication
from gui.ui_OsdagMainPage import Ui_MainWindow
from gui.ui_tutorial import Ui_Tutorial
from gui.ui_aboutosdag import Ui_AboutOsdag
from gui.ui_ask_question import Ui_AskQuestion
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.main_controller import launchwindow
from gui.ui_template import Ui_ModuleWindow

from design_type.connection import main_controller
import os
import os.path
import subprocess
import shutil
import configparser
from PyQt5.QtWidgets import QMessageBox, qApp
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
from gui.ui_design_preferences import Ui_Dialog
import os
import json
import logging
from drawing_2D.Svg_Window import SvgWindow
import sys

from OCC.Core import BRepTools
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core import IGESControl
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.StlAPI import StlAPI_Writer

import pdfkit
import subprocess
import os.path
import pickle
import shutil
import cairosvg
import configparser
from gui.ui_OsdagMainPage import Ui_MainWindow
from gui.ui_template import Ui_ModuleWindow
# from design_type.connection.main_controller import MainController


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
        self.showMaximized()
        list_of_items = {'Osdagpage': 0, 'connectionpage': 1, 'Tension': 2,'Compression': 3, 'beamtocolumnpage': 4,'flexuralpage': 5}
        self.ui.myStackedWidget.setCurrentIndex(list_of_items['Osdagpage'])
        self.ui.btn_connection.clicked.connect(lambda: self.change_desgin_page(list_of_items['connectionpage'], list_of_items['Osdagpage']))
       # self.ui.myListWidget.currentItemChanged.connect(self.change_desgin_page)
        self.ui.btn_start.clicked.connect(self.show_shear_connection)
        self.ui.btn_start_2.clicked.connect(self.unavailable)
        self.ui.btn_start_3.clicked.connect(self.unavailable)
        self.ui.Tension_Start.clicked.connect(self.unavailable)
        self.ui.Compression_Start.clicked.connect(self.unavailable)
        self.ui.cc_Start.clicked.connect(self.unavailable)

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
        #self.ui.rdbtn_beamtobeam.clicked.connect(lambda: self.change_desgin_page(list_of_items['beamtobeampage'], list_of_items['Osdagpage']))
        #self.ui.rdbtn_beamcolumn.clicked.connect(lambda: self.change_desgin_page(list_of_items['beamtocolumnpage'], list_of_items['Osdagpage']))
        #self.ui.rdbtn_peb.setDisabled(True)
        #self.ui.rdbtn_colcol.setDisabled(True)

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

    def select_workspace_folder(self):
        # This function prompts the user to select the workspace folder and returns the name of the workspace folder
        config = configparser.ConfigParser()
        config.read_file(open(r'Osdag.config'))
        desktop_path = config.get("desktop_path", "path1")
        folder = QFileDialog.getExistingDirectory(self, "Select Workspace Folder (Don't use spaces in the folder name)", desktop_path)
        return folder

    # @pyqtSlot
    def show_shear_connection(self):
        folder = self.select_workspace_folder()
        folder = str(folder)
        if not os.path.exists(folder):
            if folder == '':
                pass
            else:
                os.mkdir(folder, 0o755)

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
            # window = Ui_ModuleWindow(FinPlateConnection,folder)
            # window.show()
            launchwindow(self,Ui_ModuleWindow,FinPlateConnection,folder)
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

# class MainController(QMainWindow):
#     # closed = pyqtSignal()
#     def __init__(self, Ui_ModuleWindow, main, folder):
#         QMainWindow.__init__(self)
#         self.ui = Ui_ModuleWindow()
#         self.ui.setupUi(self, main)
#         self.folder = folder
#         self.connection = "Finplate"
#
#     def launchwindow(self, modulewindow, main, folder):
#         try:
#             print(self, modulewindow, main, folder)
#             # MainController.set_osdaglogger(self)
#             rawLogger = logging.getLogger("raw")
#             rawLogger.setLevel(logging.INFO)
#             fh = logging.FileHandler("design_type/connection/fin.log", mode="w")
#             formatter = logging.Formatter('''%(message)s''')
#             fh.setFormatter(formatter)
#             rawLogger.addHandler(fh)
#             rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Finplate/log.css"/>''')
#             MainController.module_setup(self)
#             print(self, modulewindow, main, folder)
#             window = MainController(modulewindow, main, folder)
#             print(window)
#             OsdagMainWindow.hide(self)
#             window.show()
#             window.closed.connect(OsdagMainWindow.show)
#         except BaseException as e:
#             print("ERROR1", str(e))

    def set_osdaglogger(self):
        global logger
        logger = None
        if logger is None:
            logger = logging.getLogger("osdag")
        else:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

        logger.setLevel(logging.DEBUG)

        # create the logging file handler
        fh = logging.FileHandler("design_type/connection/fin.log", mode="a")

        # ,datefmt='%a, %d %b %Y %H:%M:%S'
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        formatter = logging.Formatter('''
        <div  class="LOG %(levelname)s">
            <span class="DATE">%(asctime)s</span>
            <span class="LEVEL">%(levelname)s</span>
            <span class="MSG">%(message)s</span>
        </div>''')
        formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    def module_setup(self):
        global logger
        logger = logging.getLogger("osdag.model")

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
    print("Error occurred: ", (exctype, value, traceback))
    # Call the normal Exception hook after
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = the_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    # app.exec_()
    # sys.exit(app.exec_())
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print("ERROR", e)
