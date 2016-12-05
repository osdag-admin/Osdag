'''
Created on 31-Mar-2016

@author: deepa
'''
import sys
from PyQt4 import QtGui
from ui_OsdagMainPage import Ui_MainWindow
from Connections.Shear.Finplate.finPlateMain import launchFinPlateController
from Connections.Shear.cleatAngle.cleatAngleMain import launch_cleatangle_controller
from Connections.Shear.Endplate.endPlateMain import launch_endplate_controller
import os.path


class OsdagMainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        list_of_items = {'Osdagpage': 0, 'connectionpage': 1, 'tensionpage': 2, 'compressionpage': 3, 'flexuralpage': 4}

        self.ui.myStackedWidget.setCurrentIndex(list_of_items['Osdagpage'])
        self.ui.btn_connection.clicked.connect(lambda: self.change_desgin_page(list_of_items['connectionpage'], list_of_items['Osdagpage']))
        self.ui.myListWidget.currentItemChanged.connect(self.change_desgin_page)
        self.ui.btn_start.clicked.connect(self.show_desgin_connection)
        self.ui.btn_beamCol.clicked.connect(self.unavailable)
        self.ui.btn_compression.clicked.connect(self.unavailable)
        self.ui.btn_flexural.clicked.connect(self.unavailable)
        self.ui.btn_gantry.clicked.connect(self.unavailable)
        self.ui.btn_tension.clicked.connect(self.unavailable)
        self.ui.btn_plate.clicked.connect(self.unavailable)

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

    def show_desgin_connection(self):

        folder = QtGui.QFileDialog.getSaveFileName(self, 'Select Workspace Directory', os.path.join('..', '..','OsdagWorkspace', 'Osdag_workspace'), 'All Files (*)')
        folder = str(folder)
        if not os.path.exists(folder):
            os.mkdir(folder)

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
            # QtGui.QMessageBox.about(self,"INFO","End plate connection design is coming soon!")

        elif self.ui.rdbtn_seat.isChecked():
            QtGui.QMessageBox.about(self, "INFO", "Seated connection design is coming soon!")

        else:
            QtGui.QMessageBox.about(self, "INFO", "Please select appropriate connection")

    def unavailable(self):
        QtGui.QMessageBox.about(self, "INFO", "This module is not available in this version.")
        # self.ui.btn_beamCol.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_compression.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_flexural.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_gantry.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_plate.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))
        # self.ui.btn_tension.clicked.connect(lambda:self.change_desgin_page(list_of_items['Osdagpage'], list_of_items['tensionpage']))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    sys.exit(app.exec_())
