'''
Created on 31-Mar-2016

@author: deepa
'''
import sys
from PyQt4 import QtGui
from ui_OsdagMainPage import Ui_MainWindow
# from Connections.Shear.Finplate.finPlateMain import launchFinPlateController
from Connections.Shear.Finplate.finPlateMain import launchFinPlateController
from Connections.Shear.cleatAngle.cleatAngleMain import launchCleatAngleController
from Connections.Shear.Endplate.endPlateMain import launchEndPlateController
from Connections.Shear.SeatedAngle.SeatAngleMain import launchSeatedAngleController

# from os.path import expanduser                       #enters in home folder
import os.path
from PyQt4.QtGui import QFileDialog
import shutil
    
class OsdagMainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        listItems = {'Osdagpage':0,'connectionpage':1,'tensionpage':2,'compressionpage':3,'flexuralpage':4}
        
        self.ui.myStackedWidget.setCurrentIndex(listItems['Osdagpage'])
        self.ui.btn_connection.clicked.connect(lambda:self.changePage(listItems['connectionpage'],listItems['Osdagpage']))
        self.ui.myListWidget.currentItemChanged.connect(self.changePage)
        self.ui.btn_start.clicked.connect(self.showConnection)
        self.ui.btn_beamCol.clicked.connect(self.notavailable)
        self.ui.btn_compression.clicked.connect(self.notavailable)
        self.ui.btn_flexural.clicked.connect(self.notavailable)
        self.ui.btn_gantry.clicked.connect(self.notavailable)
        self.ui.btn_tension.clicked.connect(self.notavailable)
        self.ui.btn_plate.clicked.connect(self.notavailable)
        
#         self.disableDesignButtons()
#         self.ui.cmdlinkbtn_workspace.clicked.connect(self.workspaceLaunch)
        
#     def workspaceLaunch(self):
#         folder = str(QtGui.QFileDialog.getSaveFileName(self, "Select Workspace Directory","Osdag Workspace", "File folder"))
# #         filefolder = QtGui.QFileDialog.getExistingDirectory(self, "Select Workspace Directory","C:\OSDAG ",QtGui.QFileDialog.ShowDirsOnly)
# #         base = os.path.basename(folder)
#         print "reshmmmmmm"
#         print folder
#         if not os.path.exists(folder):
#             os.makedirs(folder, 0755)      
#             self.enableDesignButtons()
#         return folder

#         else:
#             shutil.rmtree(folder)
#     def connect_workspace(self):
#         folder = self.workspaceLaunch()
#         self.showConnection(folder)
         
    def disableDesignButtons(self):
        self.ui.btn_beamCol.setEnabled(False)
        self.ui.btn_compression.setEnabled(False)
        self.ui.btn_connection.setEnabled(False)
        self.ui.btn_flexural.setEnabled(False)
        self.ui.btn_gantry.setEnabled(False)
        self.ui.btn_plate.setEnabled(False)
        self.ui.btn_tension.setEnabled(False)
        self.ui.btn_help.setEnabled(False)
        
    def enableDesignButtons(self):
        self.ui.btn_beamCol.setEnabled(True)
        self.ui.btn_compression.setEnabled(True)
        self.ui.btn_connection.setEnabled(True)
        self.ui.btn_flexural.setEnabled(True)
        self.ui.btn_gantry.setEnabled(True)
        self.ui.btn_plate.setEnabled(True)
        self.ui.btn_tension.setEnabled(True)
        self.ui.btn_help.setEnabled(True)
        
    def changePage(self, current, previous):
        if not current:
            current = previous

        self.ui.myStackedWidget.setCurrentIndex(current)
    
    def showConnection(self):
#         foldernew = self.workspaceLaunch()
        folder = str(QtGui.QFileDialog.getSaveFileName(self, "Select Workspace Directory","Osdag_Workspace", "File folder"))
        if not os.path.exists(folder):
            os.makedirs(folder, 0755)     
            
#         return folder

        root_path = folder 
        print root_path
        css_folder = ['css']
        for create_folder in css_folder:
            os.mkdir(os.path.join(root_path, create_folder))
#             
             
        if self.ui.rdbtn_finplate.isChecked():
            launchFinPlateController(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)
            
        elif self.ui.rdbtn_cleat.isChecked():
            launchCleatAngleController(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)
        
        elif self.ui.rdbtn_endplate.isChecked():
            launchEndPlateController(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)
            # QtGui.QMessageBox.about(self,"INFO","End plate connection design is coming soon!")
        
        elif self.ui.rdbtn_seat.isChecked():
            launchSeatedAngleController(self, folder)
            self.ui.myStackedWidget.setCurrentIndex(0)
            # QtGui.QMessageBox.about(self,"INFO","Seated connection design is coming soon!")
        
        else:
            QtGui.QMessageBox.about(self,"INFO","Please select appropriate connection")
            
    def notavailable(self):    
        QtGui.QMessageBox.about(self,"INFO","This module is not available in this version.")
#         self.ui.btn_beamCol.clicked.connect(lambda:self.changePage(listItems['Osdagpage'], listItems['tensionpage']))
#         self.ui.btn_compression.clicked.connect(lambda:self.changePage(listItems['Osdagpage'], listItems['tensionpage']))
#         self.ui.btn_flexural.clicked.connect(lambda:self.changePage(listItems['Osdagpage'], listItems['tensionpage']))
#         self.ui.btn_gantry.clicked.connect(lambda:self.changePage(listItems['Osdagpage'], listItems['tensionpage']))
#         self.ui.btn_plate.clicked.connect(lambda:self.changePage(listItems['Osdagpage'], listItems['tensionpage']))
#         self.ui.btn_tension.clicked.connect(lambda:self.changePage(listItems['Osdagpage'], listItems['tensionpage']))

    

    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    sys.exit(app.exec_())