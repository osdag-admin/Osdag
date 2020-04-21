#!/home/deepa-c/miniconda2/bin/python
'''
Created on 31-Mar-2016

@author: darshan
'''
#testing 
import sys
# from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication
from gui.ui_OsdagMainPage import Ui_MainWindow
from gui.ui_tutorial import Ui_Tutorial
from gui.ui_aboutosdag import Ui_AboutOsdag
from gui.ui_ask_question import Ui_AskQuestion
# from design_type.connection.fin_plate_connection import design_report_show
# from design_type.connection.fin_plate_connection import DesignReportDialog
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.seated_angle_connection import SeatedAngleConnectionInput
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.base_plate_connection import BasePlateConnection

from design_type.connection.beam_cover_plate import BeamCoverPlate
from design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld

from design_type.tension_member.tension_bolted import Tension_bolted
from design_type.tension_member.tension_welded import Tension_welded
from design_type.connection.beam_end_plate import BeamEndPlate
from design_type.connection.column_cover_plate import ColumnCoverPlate
from design_type.connection.column_end_plate import ColumnEndPlate
from design_type.compression_member.compression import Compression
#from design_type.tension_member.tension import Tension
# from cad.cad_common import call_3DBeam
from gui.ui_template import Ui_ModuleWindow

# from design_type.connection.main_controller import MainController
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
from gui.ui_design_summary import Ui_DesignReport
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
        self.ui.btn_compression.clicked.connect(
            lambda: self.change_desgin_page(list_of_items['Compression'], list_of_items['Osdagpage']))
        self.ui.btn_tension.clicked.connect(
            lambda: self.change_desgin_page(list_of_items['Tension'], list_of_items['Osdagpage']))
       # self.ui.myListWidget.currentItemChanged.connect(self.change_desgin_page)
        self.ui.btn_shearconnection_start.clicked.connect(self.show_shear_connection)
        self.ui.btn_momentconnection_bb_start.clicked.connect(self.show_moment_connection)
        self.ui.btn_momentconnection_bc_start.clicked.connect(self.unavailable)
        self.ui.btn_momentconnection_cc_start.clicked.connect(self.show_moment_connection_cc)
        self.ui.btn_baseplate_start.clicked.connect(self.show_base_plate)

        self.ui.Tension_Start.clicked.connect(self.show_tension_module)
        self.ui.Compression_Start.clicked.connect(self.show_compression_module)

        self.ui.btn_beamCol.clicked.connect(self.unavailable)
        # self.ui.btn_compression.clicked.connect(self.unavailable)
        self.ui.btn_flexural.clicked.connect(self.unavailable)
        self.ui.btn_truss.clicked.connect(self.unavailable)
        self.ui.btn_2dframe.clicked.connect(self.unavailable)
        self.ui.btn_3dframe.clicked.connect(self.unavailable)
        self.ui.btn_groupdesign.clicked.connect(self.unavailable)
        # self.ui.btn_tension.clicked.connect(self.unavailable)
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
        self.ui.btn_plate.setEnabled(False)
        self.ui.btn_tension.setEnabled(False)

    def enable_desgin_buttons(self):
        self.ui.btn_beamCol.setEnabled(True)
        self.ui.btn_compression.setEnabled(True)
        self.ui.btn_connection.setEnabled(True)
        self.ui.btn_flexural.setEnabled(True)
        self.ui.btn_plate.setEnabled(True)
        self.ui.btn_tension.setEnabled(True)

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

    @pyqtSlot()
    def show_shear_connection(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.ui.rdbtn_finplate.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, FinPlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.ui.rdbtn_cleat.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, CleatAngleConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.ui.rdbtn_seat.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2,SeatedAngleConnectionInput)
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.ui.rdbtn_endplate.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, EndPlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        else:
            QMessageBox.about(self, "INFO", "Please select appropriate connection")
    #
    # def show_compression_module(self):
    #     folder = self.select_workspace_folder()
    #     folder = str(folder)
    #     if not os.path.exists(folder):
    #         if folder == '':
    #             pass
    #         else:
    #             os.mkdir(folder, 0o755)
    #
    #     root_path = folder
    #     images_html_folder = ['images_html']
    #     flag = True
    #     for create_folder in images_html_folder:
    #         if root_path == '':
    #             flag = False
    #             return flag
    #         else:
    #             try:
    #                 os.mkdir(os.path.join(root_path, create_folder))
    #             except OSError:
    #                 shutil.rmtree(os.path.join(folder, create_folder))
    #                 os.mkdir(os.path.join(root_path, create_folder))
    #     self.hide()
    #     self.ui3 = Ui_ModuleWindow()
    #     self.ui3.setupUi(self.ui3, Compression, folder)
    #     self.ui3.show()
    #     self.ui3.closed.connect(self.show)


    def show_moment_connection(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.ui.rdbtn_bb_coverplate_bolted.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, BeamCoverPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.ui.rdbtn_bb_coverplate_welded.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, BeamCoverPlateWeld, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.ui.rdbtn_bb_endplate.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2,BeamEndPlate)
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)


    def show_base_plate(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        self.hide()
        self.ui2 = Ui_ModuleWindow()
        self.ui2.setupUi(self.ui2, BasePlateConnection, ' ')
        self.ui2.show()
        self.ui2.closed.connect(self.show)

    def show_moment_connection_cc(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.ui.rdbtn_cc_coverplate_bolted.isChecked() :
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, ColumnCoverPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.ui.rdbtn_cc_coverplate_welded.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, ColumnCoverPlateWeld, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.ui.rdbtn_cc_endplate.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, ColumnEndPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_compression_module(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))
        if self.ui.rdbtn_compression_bolted.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, Compression, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.ui.rdbtn_compression_welded.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, Compression)
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_tension_module(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.ui.rdbtn_tension_bolted.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2,Tension_bolted, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.ui.rdbtn_tension_welded.isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, Tension_welded, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

class MainController(QMainWindow):
    closed = pyqtSignal()
    def __init__(self, Ui_ModuleWindow, main, folder):
        super(MainController,self).__init__()
        QMainWindow.__init__(self)
        self.ui = Ui_ModuleWindow()
        self.ui.setupUi(self, main, folder)
        self.folder = folder
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        # self.ui.btn_CreateDesign.clicked.connect(design_report(Ui_DesignReport))
        # self.design_report = DesignReportDialog(self)
        # self.ui.actionCreate_design_report.triggered.connect(DesignReportDialog.exec)


    def dockbtn_clicked(self, widget):

        '''(QWidget) -> None

        This method dock and undock widget(QdockWidget)
        '''

        flag = widget.isHidden()
        if (flag):

            widget.show()
        else:
            widget.hide()

    def closeEvent(self, event):
        '''
        Closing finPlate window.
        '''
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()

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
    # folder_path = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
    # # folder_path = r'C:\Users\Win10\Desktop'
    #folder_path = r'C:\Users\pc\Desktop'
    # window = MainController(Ui_ModuleWindow, FinPlateConnection, folder_path)
    window = OsdagMainWindow()
    window.show()
    # app.exec_()
    # sys.exit(app.exec_())
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print("ERROR", e)
