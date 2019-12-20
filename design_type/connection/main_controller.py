import sys
# from PyQt5 import Qt
# from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication
from gui.ui_OsdagMainPage import Ui_MainWindow
from gui.ui_tutorial import Ui_Tutorial
from gui.ui_aboutosdag import Ui_AboutOsdag
from gui.ui_ask_question import Ui_AskQuestion
from design_type.connection.fin_plate_connection import FinPlateConnection
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


class MainController(QMainWindow):
    # closed = pyqtSignal()
    def __init__(self, Ui_ModuleWindow, main, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_ModuleWindow()
        self.ui.setupUi(self, main)
        self.folder = folder
        self.connection = "Finplate"
        # MainController.set_osdaglogger(self)
        # rawLogger = logging.getLogger("raw")
        # rawLogger.setLevel(logging.INFO)
        # fh = logging.FileHandler("design_type/connection/fin.log", mode="w")
        # formatter = logging.Formatter('''%(message)s''')
        # fh.setFormatter(formatter)
        # rawLogger.addHandler(fh)
        # rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Finplate/log.css"/>''')
        # MainController.module_setup(self)
        # ########################################
        # folder_path = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
        # if not os.path.exists(folder_path):
        #     os.mkdir(folder_path, 0o755)
        # image_folder_path = os.path.join(folder_path, 'images_html')
        # if not os.path.exists(image_folder_path):
        #     os.mkdir(image_folder_path, 0o755)
        #
        # # window = MainController(Ui_ModuleWindow, FinPlateConnection, folder_path)
        # # MainController.hide(self)
        # self.ui.show()
        # window.closed.connect(Ui_ModuleWindow.show)

    def launchwindow(self, modulewindow, main, folder):
        try:
            self.set_osdaglogger()
            rawLogger = logging.getLogger("raw")
            rawLogger.setLevel(logging.INFO)
            fh = logging.FileHandler("design_type/connection/fin.log", mode="w")
            formatter = logging.Formatter('''%(message)s''')
            fh.setFormatter(formatter)
            rawLogger.addHandler(fh)
            rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Finplate/log.css"/>''')
            self.module_setup()
            print(self, modulewindow, main, folder)
            window = MainController(modulewindow, main, folder)
            print (window)
            self.hide()
            window.show()
            window.closed.connect(self.show)
        except BaseException as e:
            print("ERROR1", str(e))

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # folder_path = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
    folder_path = r'C:\Users\Win10\Desktop'
    # folder_path = r'C:\Users\pc\Desktop'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path, 0o755)
    image_folder_path = os.path.join(folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0o755)
    print(Ui_ModuleWindow,FinPlateConnection,folder_path)
    window = MainController(Ui_ModuleWindow,FinPlateConnection,folder_path)
    print(window)
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("ERROR")