'''
Created on 07-May-2015
@author: deepa

Updated 23-Aug-2016
@author: jayant
'''

import os.path
import sys

from PyQt4.QtCore import pyqtSignal
from PyQt4 import QtCore
from PyQt4 import QtGui
import shutil
import webbrowser
import pickle

from OCC.gp import gp_Pnt
from OCC import VERSION, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from OCC import IGESControl
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone
from OCC.StlAPI import StlAPI_Writer
import OCC.V3d

from model import *
from utilities import osdagDisplayShape
# from drawing_2D import FinCommonData

from ISection import ISection
from angle import Angle
from fillet_weld import FilletWeld
from bolt import Bolt
from nut import Nut
from seat_angle_calc import SeatAngleCalculation
from nut_bolt_placement import NutBoltArray

from col_web_beam_web_connectivity import ColWebBeamWeb
from col_flange_beam_web_connectivity import ColFlangeBeamWeb
# from beamWebBeamWebConnectivity import BeamWebBeamWeb

from report_generator import *
from ui_seat_angle import Ui_MainWindow # ui_seat_angle is the revised ui (~23 Aug 2016)
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_HelpOsdag
from ui_tutorial import Ui_Tutorial
# You can delete ite
from ModelUtils import getGpPt
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from apt.auth import update
from Connections.Shear.SeatedAngle.common_logic import CommonDesignLogic

class MyTutorials(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Tutorial()
        self.ui.setupUi(self)
        self.mainController = parent


class MyAboutOsdag(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_HelpOsdag()
        self.ui.setupUi(self)
        self.mainController = parent


# below class was previously MyPopupDialog in the other modules
class DesignReportDialog(QtGui.QDialog):
    print "Design Report - Dseign Profile dialog box"
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.mainController = parent
        self.setWindowTitle("Design Profile")
        self.ui.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.ui.lbl_browse))
        self.ui.btn_saveProfile.clicked.connect(self.saveUserProfile)
        self.ui.btn_useProfile.clicked.connect(self.useUserProfile)
        self.accepted.connect(self.save_inputSummary)

    # noinspection PyPep8Naming
    def save_inputSummary(self):
        report_summary = self.get_report_summary()
        self.mainController.save_design(report_summary)

    def getLogoFilePath(self, lblwidget):
        self.ui.lbl_browse.clear
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', " ", 'Images (*.png *.svg *.jpg)', None,
                                                     QtGui.QFileDialog.DontUseNativeDialog)
        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

        return str(filename)

    def desired_location(self, filename):
        shutil.copyfile(filename, str(self.mainController.folder) + "/images_html/cmpylogoFin.png")

    def saveUserProfile(self):
        inputData = self.get_report_summary()
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Files', str(self.mainController.folder) + "/Profile",
                                                     '*.txt')
        infile = open(filename, 'w')
        pickle.dump(inputData, infile)
        infile.close()

    def get_report_summary(self):
        report_summary = {}
        report_summary["ProfileSummary"] = {}
        report_summary["ProfileSummary"]["CompanyName"] = str(self.ui.lineEdit_companyName.text())
        report_summary["ProfileSummary"]["CompanyLogo"] = str(self.ui.lbl_browse.text())
        report_summary["ProfileSummary"]["Group/TeamName"] = str(self.ui.lineEdit_groupName.text())
        report_summary["ProfileSummary"]["Designer"] = str(self.ui.lineEdit_designer.text())

        report_summary["ProjectTitle"] = str(self.ui.lineEdit_projectTitle.text())
        report_summary["Subtitle"] = str(self.ui.lineEdit_subtitle.text())
        report_summary["JobNumber"] = str(self.ui.lineEdit_jobNumber.text())
        report_summary["AdditionalComments"] = str(self.ui.txt_additionalComments.toPlainText())
        report_summary["Method"] = str(self.ui.comboBox_method.currentText())

        return report_summary

    def useUserProfile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Files', str(self.mainController.folder) + "/Profile",
                                                     "All Files (*)")
        if os.path.isfile(filename):
            outfile = open(filename, 'r')
            reportsummary = pickle.load(outfile)
            self.ui.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
            self.ui.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
            self.ui.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
            self.ui.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])
        else:
            pass


class MainController(QtGui.QMainWindow):

    closed = pyqtSignal()

    def __init__(self, folder):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder

        self.ui.combo_beam_section.addItems(get_beamcombolist())
        self.ui.combo_column_section.addItems(get_columncombolist())
        self.ui.combo_angle_section.addItems(get_anglecombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.grade_type = {'Please Select Type': '',
                          'HSFG': [8.8, 10.8],
                          'Black Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 12.9]}
        self.ui.combo_bolt_type.addItems(self.grade_type.keys())
        self.ui.combo_bolt_type.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.combo_bolt_type.setCurrentIndex(0)

        #comboConnLoc renamed to combo_connectivity
        self.ui.combo_connectivity.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()

        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxSeatAngle.clicked.connect(self.call_3DSeatAngle)

        validator = QtGui.QIntValidator()
        self.ui.txt_fu.setValidator(validator)
        self.ui.txt_fy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
        #TODO add input validations
        self.ui.txt_shear_force.setValidator(dbl_validator)
        self.ui.txt_shear_force.setMaxLength(7)

        min_fu_value = 290
        max_fu_value = 590
        self.ui.txt_fu.editingFinished.connect(
            lambda: self.check_range(self.ui.txt_fu, self.ui.lbl_fu, min_fu_value, max_fu_value))

        min_fy_value = 165
        max_fy_value = 450
        self.ui.txt_fy.editingFinished.connect(
            lambda: self.check_range(self.ui.txt_fy, self.ui.lbl_fy, min_fy_value, max_fy_value))

        # Menu Bar
        # File Menu

        self.ui.actionSave_front_view.triggered.connect(lambda:self.call_seatangle2D_Drawing("Front"))
        self.ui.actionSave_side_view.triggered.connect(lambda: self.call_seatangle2D_Drawing("Side"))
        self.ui.actionSave_top_view.triggered.connect(lambda: self.call_seatangle2D_Drawing("Top"))
        self.ui.actionQuit_fin_plate_design.setShortcut('Ctrl+Q')
        self.ui.actionQuit_fin_plate_design.setStatusTip('Exit application')
        self.ui.actionQuit_fin_plate_design.triggered.connect(QtGui.qApp.quit)

        self.ui.actionCreate_design_report.triggered.connect(self.create_design_report)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_current_2D_image_as.triggered.connect(self.save2DcadImages)
        self.ui.actionPan.triggered.connect(self.call_Pannig)

        # Graphics menu
        self.ui.actionBeam_2.triggered.connect(self.call_3DBeam)
        self.ui.actionColumn_2.triggered.connect(self.call_3DColumn)
        self.ui.actionSeatAngle_2.triggered.connect(self.call_3DSeatAngle)
        self.ui.actionShow_All.triggered.connect(lambda: self.call_3DModel(True))
        self.ui.actionChange_Background.triggered.connect(self.showColorDialog)

        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.create_design_report)  # Saves the design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)

        self.ui.btn_front.clicked.connect(lambda: self.call_seatangle2D_Drawing("Front"))
        self.ui.btn_side.clicked.connect(lambda: self.call_seatangle2D_Drawing("Side"))
        self.ui.btn_top.clicked.connect(lambda: self.call_seatangle2D_Drawing("Top"))

        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

        # Osdag logo for html
        # self.ui.btn_Design.clicked.connect(self.osdag_header)

        # Help button
        self.ui.actionAbout_Osdag.triggered.connect(self.open_osdag)
        # TODO update UI for actionSample_Tutorials
        # self.ui.actionSample_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_Reports.triggered.connect(self.sample_report)
        # TODO update UI actionSample_Problems
        self.ui.actionSampe_Problems.triggered.connect(self.sample_problem)

        from osdagMainSettings import backend_name

        self.display, self.start_display = self.init_display(backend_str=backend_name())

        # self.ui.btnSvgSave.clicked.connect(self.save3DcadImages)

        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        self.resultObj = None
        self.uiObj = None
        self.sa_calc_object = SeatAngleCalculation()

    def osdag_header(self):
        # osdag_header() and store_osdagheader(str) functions are combined here
        image_path = os.path.dirname(os.path.abspath(__file__))+os.path+os.path.join("..","..","..","ResourceFiles","Osdag_header.png")
        print str(image_path)
        print str(os.path.join("images_html","Osdag_header.png"))
        shutil.copyfile(image_path, str(self.folder) + os.path.join("images_html","Osdag_header.png"))

    # noinspection PyPep8Naming
    def fetchBeamPara(self):
        beam_sec = self.ui.combo_beam_section.currentText()
        dictbeamdata = get_beamdata(beam_sec)
        return dictbeamdata

    def fetchColumnPara(self):
        column_sec = self.ui.combo_column_section.currentText()
        loc = self.ui.combo_connectivity.currentText()
        if loc == "Beam-Beam":
            dictcoldata = get_beamdata(column_sec)
        else:
            dictcoldata = get_columndata(column_sec)
        return dictcoldata
    
    def fetchAnglePara(self):
        angle_sec = self.ui.combo_angle_section.currentText()
        dictangledata = get_angledata(angle_sec)
        return dictangledata

    
    def showFontDialogue(self):

        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)

    def callZoomin(self):
        self.display.ZoomFactor(2)

    def callZoomout(self):
        self.display.ZoomFactor(0.5)

    def callRotation(self):
        self.display.Rotation(15, 0)

    def call_Pannig(self):
        self.display.Pan(50, 0)

    def save2DcadImages(self):
        files_types = "PNG (*.png);;JPG (*.jpg);;GIF (*.gif)"
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Export', str(self.folder) + "/untitled.png", files_types)
        fName = str(fileName)
        file_extension = fName.split(".")[-1]

        if file_extension == 'png' or file_extension == 'jpg' or file_extension == 'gif':
            self.display.ExportToImage(fName)
            QtGui.QMessageBox.about(self, 'Information', "File saved")

    def disableViewButtons(self):
        '''
        Disables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(False)
        self.ui.btn_side.setEnabled(False)
        self.ui.btn_top.setEnabled(False)
        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.chkBxSeatAngle.setEnabled(False)
        self.ui.btn_CreateDesign.setEnabled(False)
        self.ui.btn_SaveMessages.setEnabled(False)

        # Disable Menubar
        self.ui.menubar.setEnabled(False)

    def enableViewButtons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(True)
        self.ui.btn_side.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxSeatAngle.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)

        self.ui.menubar.setEnabled(True)

    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if (uiObj is not None):

            self.ui.combo_connectivity.setCurrentIndex(self.ui.combo_connectivity.findText(str(uiObj['Member']['Connectivity'])))

            if uiObj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.lbl_beam.setText('Secondary beam *')
                self.ui.lbl_column.setText('Primary beam *')
                self.ui.combo_column_section.addItems(get_beamcombolist())

            self.ui.combo_beam_section.setCurrentIndex(self.ui.combo_beam_section.findText(uiObj['Member']['BeamSection']))
            print uiObj
            self.ui.combo_column_section.setCurrentIndex(self.ui.combo_column_section.findText(uiObj['Member']['ColumnSection']))

            self.ui.txt_fu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txt_fy.setText(str(uiObj['Member']['fy (MPa)']))

            self.ui.txt_shear_force.setText(str(uiObj['Load']['ShearForce (kN)']))

            self.ui.combo_bolt_diameter.setCurrentIndex(self.ui.combo_bolt_diameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            combo_type_index = self.ui.combo_bolt_type.findText(str(uiObj['Bolt']['Type']))
            self.ui.combo_bolt_type.setCurrentIndex(combo_type_index)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))
            combo_grade_index = self.ui.combo_bolt_grade.findText(str(uiObj['Bolt']['Grade']))
            self.ui.combo_bolt_grade.setCurrentIndex(combo_grade_index)
            combo_angle_index = self.ui.combo_angle_section.findText(str(uiObj['Angle']['AngleSection']))
            self.ui.combo_angle_section.setCurrentIndex(combo_angle_index)
            self.ui.txt_angle_thickness.setText(str(uiObj['Angle']['Thickness']))

    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.combo_connectivity.currentText()
        if loc == "Column flange-Beam web":
            pixmap = QtGui.QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            # self.ui.lbl_connectivity.show()
        elif (loc == "Column web-Beam web"):
            picmap = QtGui.QPixmap(":/newPrefix/images/colW3.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)
        else:
            self.ui.lbl_connectivity.hide()

        return True

    def getuser_inputs(self):
        '''(nothing) -> Dictionary
        
        Returns the dictionary object with the user input fields for designing fin plate connection
        
        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.combo_bolt_diameter.currentText().toInt()[0]
        uiObj["Bolt"]["Grade"] = float(self.ui.combo_bolt_grade.currentText())
        uiObj["Bolt"]["Type"] = str(self.ui.combo_bolt_type.currentText())

        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.combo_beam_section.currentText())
        uiObj['Member']['ColumnSection'] = str(self.ui.combo_column_section.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.combo_connectivity.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txt_fu.text().toInt()[0]
        uiObj['Member']['fy (MPa)'] = self.ui.txt_fy.text().toInt()[0]

        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = float(self.ui.txt_shear_force.text())

        uiObj['Angle'] = {}
        uiObj['Angle']['AngleSection'] = str(self.ui.combo_angle_section.currentText())
        uiObj['Angle']['Thickness'] = str(self.ui.txt_angle_thickness.text())
        #TODO delete angle - thickness input from UI

        return uiObj

    def save_inputs(self, uiObj):

        '''(Dictionary)--> None
         
        '''
        inputFile = QtCore.QFile('saveINPUT.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        pickle.dump(uiObj, inputFile)

    def get_prevstate(self):
        '''
        '''
        fileName = 'saveINPUT.txt'

        if os.path.isfile(fileName):
            fileObject = open(fileName, 'r')
            uiObj = pickle.load(fileObject)
            return uiObj
        else:
            return None

    def outputdict(self):

        ''' Returns the output of design in dictionary object.
        '''
        outObj = {}
        outObj['SeatAngle'] = {}
        outObj['SeatAngle']["Length (mm)"] = float(self.ui.txt_seat_length.text())
        outObj['SeatAngle']["Moment Demand (kN-mm)"] = float(self.ui.txt_moment_demand.text())
        outObj['SeatAngle']["Moment Capacity (kN-mm)"] = float(self.ui.txt_moment_capacity.text())
        outObj['SeatAngle']["Shear Demand (kN)"] = float(self.ui.txt_seat_shear_demand.text())
        outObj['SeatAngle']["Shear Capacity (kN)"] = float(self.ui.txt_seat_shear_capacity.text())
        outObj['SeatAngle']["Beam Shear Strength (kN)"] = float(self.ui.txt_beam_shear_strength.text())
        outObj['SeatAngle']["Top Angle"] = float(self.ui.txt_top_angle.text())

        outObj['Bolt'] = {}
        outObj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txt_bolt_shear_capacity.text())
        outObj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txt_bolt_bearing_capacity.text())
        outObj['Bolt']["Capacity of Bolt (kN)"] = float(self.ui.txt_bolt_capacity.text())
        outObj['Bolt']["Bolt group capacity (kN)"] = float(self.ui.txt_bolt_group_capacity.text())
        outObj['Bolt']["No. of Bolts"] = float(self.ui.txt_no_bolts.text())
        outObj['Bolt']["No. of Row"] = int(self.ui.txt_bolt_rows.text())
        outObj['Bolt']["No. of Column"] = int(self.ui.txt_bolt_cols.text())
        outObj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txt_bolt_pitch.text())
        outObj['Bolt']["Gauge Distance (mm)"] = float(self.ui.txt_bolt_gauge.text())
        outObj['Bolt']["End Distance (mm)"] = float(self.ui.txt_end_distance.text())
        outObj['Bolt']["Edge Distance (mm)"] = float(self.ui.txt_edge_distance.text())

        return outObj

    def show_design_report_dialog(self):
        design_report_dialog = DesignReportDialog(self)
        design_report_dialog.show()

    def create_design_report(self):
        self.show_design_report_dialog()
        # function name changed from createDesignReport

    def save_design(self, report_summary):

        file_name, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/",
                                                                   "Html Files (*.html)")
        file_name = str(file_name)
        base, base_front, base_top, base_side = self.call2D_Drawing("All")
        inputdict = self.uiObj
        outdict = self.resultObj

        report_generator_instance = ReportGenerator(self.sa_calc_object)
        report_generator_instance.save_html(outdict, inputdict, report_summary, file_name, self.folder, base,
                  base_front, base_top, base_side)

        QtGui.QMessageBox.about(self, 'Information', "Report Saved")

    def save_log(self):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder)+"/LogMessages",
                                                                   "Text files (*.txt)")
        return self.save_file(fileName + ".txt")

    def save_file(self, fileName):
        '''(file open for writing)-> boolean
        '''
        fname = QtCore.QFile(fileName)

        if not fname.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (fileName, fname.errorString()))
            return False

        outf = QtCore.QTextStream(fname)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

    def resetbtn_clicked(self):
        '''(NoneType) -> NoneType
        
        Resets all fields in input as well as output window
    
        '''
        # Input

        self.ui.combo_beam_section.setCurrentIndex(0)
        self.ui.combo_column_section.setCurrentIndex(0)
        self.ui.combo_connectivity.setCurrentIndex(0)
        self.ui.txt_fu.clear()
        self.ui.txt_fy.clear()

        self.ui.txt_shear_force.clear()

        self.ui.combo_bolt_diameter.setCurrentIndex(0)
        self.ui.combo_bolt_grade.setCurrentIndex(0)
        self.ui.combo_bolt_type.setCurrentIndex(0)

        self.ui.combo_angle_section.setCurrentIndex(0)

        # Output

        self.ui.txt_seat_length.clear()
        self.ui.txt_moment_demand.clear()
        self.ui.txt_moment_capacity.clear()
        self.ui.txt_seat_shear_demand.clear()
        self.ui.txt_seat_shear_capacity.clear()
        self.ui.txt_beam_shear_strength.clear()
        self.ui.txt_top_angle.clear()

        self.ui.txt_bolt_shear_capacity.clear()
        self.ui.txt_bolt_bearing_capacity.clear()
        self.ui.txt_bolt_capacity.clear()
        self.ui.txt_bolt_group_capacity.clear()
        self.ui.txt_no_bolts.clear()
        self.ui.txt_bolt_rows.clear()
        self.ui.txt_bolt_cols.clear()
        self.ui.txt_bolt_pitch.clear()
        self.ui.txt_bolt_gauge.clear()
        self.ui.txt_end_distance.clear()
        self.ui.txt_edge_distance.clear()

        # ------ Erase Display
        self.display.EraseAll()

    def dockbtn_clicked(self, widget):

        '''(QWidget) -> NoneType
        
        This method dock and undock widget(QdockWidget)
        '''

        flag = widget.isHidden()
        if (flag):
            widget.show()
        else:
            widget.hide()

    def combotype_currentindexchanged(self, index):

        '''(Number) -> NoneType
        '''
        items = self.grade_type[str(index)]

        self.ui.combo_bolt_grade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))

        self.ui.combo_bolt_grade.addItems(strItems)

    def check_range(self, widget, lblwidget, min_value, max_value):

        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yield Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr)
        if (val < min_value or val > max_value):
            QtGui.QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s' % (min_value, max_value))
            widget.clear()
            widget.setFocus()
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QtGui.QPalette()
            lblwidget.setPalette(palette)

    def display_output(self, outputObj):
        '''(dictionary) --> NoneType
        Setting design result values to the respective textboxes in the output window
        '''
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                if (outputObj[k][key] == ""):
                    resultObj = outputObj
                else:
                    resultObj = outputObj

        # resultObj['Bolt']
        bolt_shear_capacity = resultObj['Bolt']['Shear Capacity (kN)']
        self.ui.txt_bolt_shear_capacity.setText(str(bolt_shear_capacity))

        bolt_bearing_capacity = resultObj['Bolt']['Bearing Capacity (kN)']
        self.ui.txt_bolt_bearing_capacity.setText(str(bolt_bearing_capacity))

        bolt_capacity = resultObj['Bolt']['Capacity of Bolt (kN)']
        self.ui.txt_bolt_capacity.setText(str(bolt_capacity))

        no_of_bolts = resultObj['Bolt']['No. of Bolts']
        self.ui.txt_no_bolts.setText(str(no_of_bolts))
        # newly added field
        bolt_grp_capacity = resultObj['Bolt']['Bolt group capacity (kN)']
        self.ui.txt_bolt_group_capacity.setText(str(bolt_grp_capacity))

        no_of_rows = resultObj['Bolt']['No. of Row']
        self.ui.txt_bolt_rows.setText(str(no_of_rows))

        no_of_cols = resultObj['Bolt']['No. of Column']
        self.ui.txt_bolt_cols.setText(str(no_of_cols))

        pitch_dist = resultObj['Bolt']['Pitch Distance (mm)']
        self.ui.txt_bolt_pitch.setText(str(pitch_dist))

        gauge_dist = resultObj['Bolt']['Gauge Distance (mm)']
        self.ui.txt_bolt_gauge.setText(str(gauge_dist))

        end_dist = resultObj['Bolt']['End Distance (mm)']
        self.ui.txt_end_distance.setText(str(end_dist))
        #
        edge_dist = resultObj['Bolt']['Edge Distance (mm)']
        self.ui.txt_edge_distance.setText(str(edge_dist))

        angle_length = resultObj['SeatAngle']['Length (mm)']
        self.ui.txt_seat_length.setText(str(angle_length))

        moment_demand = resultObj['SeatAngle']['Moment Demand (kN-mm)']
        self.ui.txt_moment_demand.setText(str(moment_demand))

        moment_capacity = resultObj['SeatAngle']['Moment Capacity (kN-mm)']
        self.ui.txt_moment_capacity.setText(str(moment_capacity))

        shear_demand = resultObj['SeatAngle']['Shear Demand (kN)']
        self.ui.txt_seat_shear_demand.setText(str(shear_demand))

        angle_shear_capacity = resultObj['SeatAngle']['Shear Capacity (kN)']
        self.ui.txt_seat_shear_capacity.setText(str(angle_shear_capacity))

        beam_shear_strength = resultObj['SeatAngle']['Beam Shear Strength (kN)']
        self.ui.txt_beam_shear_strength.setText(str(beam_shear_strength))

        top_angle = resultObj['SeatAngle']['Top Angle']
        self.ui.txt_top_angle.setText(str(top_angle))

    def displaylog_totextedit(self,commLogicObj):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''
        
        fname = str(commLogicObj.call_saveMessages())
        afile = QtCore.QFile(fname)
     
        if not afile.open(QtCore.QIODevice.ReadOnly):  # ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())
     
        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscrollBar = self.ui.textEdit.verticalScrollBar()
        vscrollBar.setValue(vscrollBar.maximum())
        afile.close()
    
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    def boltHeadThick_Calculation(self,boltDia):
        '''
        This routine takes the bolt diameter and return bolt head thickness as per IS:3757(1989)
       
       bolt Head Dia
        <-------->
        __________
        |        | | T = Thickness
        |________| |
           |  |
           |  |
           |  |
        
        '''
        boltHeadThick = {5:4, 6:5, 8:6, 10:7, 12:8, 16:10, 20:12.5, 22:14, 24:15, 27:17, 30:18.7, 36:22.5 }
        return boltHeadThick[boltDia]
        
        
    def boltHeadDia_Calculation(self,boltDia):
        '''
        This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1989)
       
       bolt Head Dia
        <-------->
        __________
        |        |
        |________|
           |  |
           |  |
           |  |
        
        '''
        boltHeadDia = {5:7, 6:8, 8:10, 10:15, 12:20, 16:27, 20:34, 22:36, 24:41, 27:46, 30:50, 36:60 }
        return boltHeadDia[boltDia]
    
    def boltLength_Calculation(self,boltDia):
        '''
        This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1985)
       
       bolt Head Dia
        <-------->
        __________  ______
        |        |    |
        |________|    | 
           |  |       |
           |  |       |
           |  |       |
           |  |       | 
           |  |       |  l= length
           |  |       |
           |  |       |
           |  |       |
           |__|    ___|__ 
        
        '''
        boltHeadDia = {5:40, 6:40, 8:40, 10:40, 12:40, 16:50, 20:50, 22:50, 24:50, 27:60, 30:65, 36:75 }
       
        return boltHeadDia[boltDia]
    
    def nutThick_Calculation(self,boltDia):
        '''
        Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
        '''
        nutDia = {5:5, 6:5.65, 8:7.15, 10:8.75, 12:11.3, 16:15, 20:17.95, 22:19.0, 24:21.25, 27:23, 30:25.35, 36:30.65 }
        
        return nutDia[boltDia]
    
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def get_backend(self):
        """
        loads a backend
        backends are loaded in order of preference
        since python comes with Tk included, but that PySide or PyQt4
        is much preferred
        """
#         try:
#             from PySide import QtCore, QtGui
#             return 'pyside'
#         except:
#             pass
        try:
            from PyQt4 import QtCore, QtGui
            return 'pyqt4'
        except:
            pass
        # Check wxPython
        try:
            import wx
            return 'wx'
        except:
            raise ImportError("No compliant GUI library found. You must have either PySide, PyQt4 or wxPython installed.")
            sys.exit(1)

    # QtViewer
    def init_display(self, backend_str=None, size=(1024, 768)):
        if os.name == 'nt':

            global display, start_display, app

            from OCC.Display.backend import get_loaded_backend
            lodedbkend = get_loaded_backend()
            from OCC.Display.backend import get_backend, have_backend
            from osdagMainSettings import backend_name
            if (not have_backend() and backend_name() == "pyqt4"):
                get_backend("qt-pyqt4")
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        else:
            global display, start_display, app, _, USED_BACKEND

            if not backend_str:
                USED_BACKEND = self.get_backend()
            elif backend_str in [ 'pyside', 'pyqt4']:
                USED_BACKEND = backend_str
            else:
                raise ValueError("You should pass either 'qt' or 'tkinter' to the init_display function.")
                sys.exit(1)

            # Qt based simple GUI
            if USED_BACKEND in ['pyqt4', 'pyside']:
                if USED_BACKEND == 'pyqt4':
                    import OCC.Display.qtDisplay
                    from PyQt4 import QtCore, QtGui, QtOpenGL

        from OCC.Display.qtDisplay import qtViewer3d
        self.ui.modelTab = qtViewer3d(self)
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


        self.setWindowTitle("Osdag Seated Angle Connection")
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")

        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display

        display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        display.display_trihedron()
        display.View.SetProj(1, 1, 1)

        def centerOnScreen(self):
            '''Centers the window on the screen.'''
            resolution = QtGui.QDesktopWidget().screenGeometry()
            self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                      (resolution.height() / 2) - (self.frameSize().height() / 2))
        def start_display():

            self.ui.modelTab.raise_()

        return display, start_display

    def showColorDialog(self):

        col = QtGui.QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

    # def display3Dmodel(self, component):
    # 
    #     self.display.EraseAll()
    #     self.display.SetModeShaded()
    #     display.DisableAntiAliasing()
    #     self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
    # 
    #     loc = self.ui.combo_connectivity.currentText()
    #     if loc == "Column flange-Beam web":
    #         self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
    #     else:
    #         self.display.View_Iso()
    #         self.display.FitAll()
    # 
    #     if component == "Column":
    #         osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
    #     elif component == "Beam":
    #         osdagDisplayShape(self.display, self.connectivity.get_beamModel(), material=Graphic3d_NOT_2D_ALUMINUM,
    #                           update=True)
    #     elif component == "SeatAngle":
    #         osdagDisplayShape(self.display, self.connectivity.topclipangleModel, color='blue', update=True)
    #         osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
    #         nutboltlist = self.connectivity.nutBoltArray.getModels()
    #         for nutbolt in nutboltlist:
    #             osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
    #     elif component == "Model":
    #         osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
    #         osdagDisplayShape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM,
    #                           update=True)
    #         osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
    #         osdagDisplayShape(self.display, self.connectivity.topclipangleModel, color='blue', update=True)
    #         nutboltlist = self.connectivity.nutBoltArray.getModels()
    #         for nutbolt in nutboltlist:
    #             osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)


#-------------------------------------------------------------------------------
    # def call_3DModel(self, flag):
    #     # self.ui.btnSvgSave.setEnabled(True)
    #     self.ui.btn3D.setChecked(QtCore.Qt.Checked)
    #     if self.ui.btn3D.isEnabled():
    #         self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
    #         self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
    #         self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
    #         self.ui.mytabWidget.setCurrentIndex(0)
    # 
    #     if flag == True:
    #         if self.ui.combo_connectivity.currentText() == "Column web-Beam web":
    #             # self.create3DColWebBeamWeb()
    #             self.connectivity = self.create3DColWebBeamWeb()
    #             self.fuse_model = None
    # 
    #         elif self.ui.combo_connectivity.currentText() == "Column flange-Beam web":
    #             self.ui.mytabWidget.setCurrentIndex(0)
    #             self.connectivity = self.create3DColFlangeBeamWeb()
    #             self.fuse_model = None
    # 
    #         else:
    #             self.ui.mytabWidget.setCurrentIndex(0)
    #             self.connectivity = self.create3DBeamWebBeamWeb()
    #             self.fuse_model = None
    # 
    #         self.display3Dmodel("Model")
    #         nutboltArrayOrigin = self.connectivity.angle.secOrigin 
    #         nutboltArrayOrigin = nutboltArrayOrigin + self.connectivity.angle.L/4 * self.connectivity.angle.wDir  
    #         nutboltArrayOrigin = nutboltArrayOrigin + self.connectivity.angle.T * self.connectivity.angle.uDir  
    #         nutboltArrayOrigin = nutboltArrayOrigin + self.connectivity.angle.A * self.connectivity.angle.vDir
    #         firstnutboltArrayOrigin = getGpPt(nutboltArrayOrigin)
    #         my_sphere1 = BRepPrimAPI_MakeSphere(firstnutboltArrayOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere1,color = 'red',update = True)
    #         
    #         bnutboltArrayOrigin = self.connectivity.angle.secOrigin 
    #         bnutboltArrayOrigin = bnutboltArrayOrigin + self.connectivity.angle.L/4 * self.connectivity.angle.wDir  
    #         bnutboltArrayOrigin = bnutboltArrayOrigin + self.connectivity.angle.T * self.connectivity.angle.vDir  
    #         bnutboltArrayOrigin = bnutboltArrayOrigin + (self.connectivity.angle.B) * self.connectivity.angle.uDir
    #         secondtnutboltArrayOrigin = getGpPt(bnutboltArrayOrigin)
    #         my_sphere2 = BRepPrimAPI_MakeSphere(secondtnutboltArrayOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere2,color = 'red',update = True)
    #         
    #         topclipnutboltArrayOrigin = self.connectivity.topclipangle.secOrigin 
    #         topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.connectivity.topclipangle.L/4 * self.connectivity.topclipangle.wDir  
    #         topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.connectivity.topclipangle.T * self.connectivity.topclipangle.uDir  
    #         topclipnutboltArrayOrigin = topclipnutboltArrayOrigin + self.connectivity.topclipangle.A * self.connectivity.topclipangle.vDir
    #         thirdtopclipnutboltArrayOrigin = getGpPt(topclipnutboltArrayOrigin)
    #         my_sphere3 = BRepPrimAPI_MakeSphere(thirdtopclipnutboltArrayOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere3,color = 'red',update = True)
    #         
    #         topclipbnutboltArrayOrigin = self.connectivity.topclipangle.secOrigin 
    #         topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.connectivity.topclipangle.L/4 * self.connectivity.topclipangle.wDir  
    #         topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + self.connectivity.topclipangle.T * self.connectivity.topclipangle.vDir  
    #         topclipbnutboltArrayOrigin = topclipbnutboltArrayOrigin + (self.connectivity.topclipangle.B) * self.connectivity.topclipangle.uDir
    #         fourthtopclipbnutboltArrayOrigin = getGpPt(topclipbnutboltArrayOrigin)
    #         my_sphere4 = BRepPrimAPI_MakeSphere(fourthtopclipbnutboltArrayOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere4,color = 'red',update = True)
    #         
    #         angle_origin =((self.connectivity.column.secOrigin + self.connectivity.column.D/2) * (-self.connectivity.column.vDir)) + ((self.connectivity.column.length/2-self.connectivity.beam.D/2) * self.connectivity.column.wDir)+(self.connectivity.angle.L/2 * (-self.connectivity.column.uDir))
    #         angleRealOrigin = getGpPt(angle_origin)
    #         my_sphere5 = BRepPrimAPI_MakeSphere(angleRealOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere5,color = 'yellow',update = True)
    #         
    #         root2 = math.sqrt(2)
    #         #angle_Rorigin =self.connectivity.angle.secOrigin  + self.connectivity.angle.T * self.connectivity.angle.uDir + (self.connectivity.angle.T + (self.connectivity.angle.R2 + self.connectivity.angle.R2/root2))* self.connectivity.angle.vDir
    #         angle_Rorigin =self.connectivity.angle.secOrigin  + self.connectivity.angle.A * self.connectivity.angle.vDir + self.connectivity.angle.T * self.connectivity.angle.uDir + self.connectivity.angle.R2*(1-1/root2) * self.connectivity.angle.uDir - self.connectivity.angle.R2/root2*self.connectivity.angle.vDir
    #         angleRealOrigin = getGpPt(angle_Rorigin)
    #         my_sphere6 = BRepPrimAPI_MakeSphere(angleRealOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere6,color = 'green',update = True)
    #         
    #         root2 = math.sqrt(2)
    #         angle_Rorigin =self.connectivity.angle.secOrigin  + self.connectivity.angle.B * self.connectivity.angle.uDir + self.connectivity.angle.T * self.connectivity.angle.vDir + self.connectivity.angle.R2*(1-1/root2) * self.connectivity.angle.vDir - self.connectivity.angle.R2/root2*self.connectivity.angle.uDir
    #         angleRealOrigin = getGpPt(angle_Rorigin)
    #         my_sphere6 = BRepPrimAPI_MakeSphere(angleRealOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere6,color = 'green',update = True)
    #         
    #         topclip_nutboltArrayOrigin = self.connectivity.topclipangle.secOrigin  + self.connectivity.topclipangle.B * self.connectivity.topclipangle.uDir + self.connectivity.topclipangle.T * self.connectivity.topclipangle.vDir -self.connectivity.topclipangle.R2/root2 * self.connectivity.topclipangle.uDir + self.connectivity.topclipangle.R2*(1-1/root2)*self.connectivity.topclipangle.vDir + self.connectivity.topclipangle.L * self.connectivity.topclipangle.wDir
    #         
    #         angletopRealOrigin = getGpPt(topclip_nutboltArrayOrigin)
    #         my_sphere7 = BRepPrimAPI_MakeSphere(angletopRealOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere7,color = 'green',update = True)
    # 
    #         
    #         topclipB_nutboltArrayOrigin = self.connectivity.topclipangle.secOrigin  + self.connectivity.topclipangle.A * self.connectivity.topclipangle.vDir + self.connectivity.topclipangle.T * self.connectivity.topclipangle.uDir -self.connectivity.topclipangle.R2/root2 * self.connectivity.topclipangle.vDir + self.connectivity.topclipangle.R2*(1-1/root2)*self.connectivity.topclipangle.uDir + self.connectivity.topclipangle.L * self.connectivity.topclipangle.wDir
    #         
    #         angletopRealOrigin = getGpPt(topclipB_nutboltArrayOrigin)
    #         my_sphere7 = BRepPrimAPI_MakeSphere(angletopRealOrigin,2.5).Shape()
    #         self.display.DisplayShape(my_sphere7,color = 'green',update = True)
    #         positions = self.connectivity.nutBoltArray.positions
    #         
    #         for pos in positions:
    #             loc = getGpPt(pos)
    #             sphere = BRepPrimAPI_MakeSphere(loc,2.0).Shape()
    #             self.display.DisplayShape(sphere, color = 'red',update = True)
    #         clipPositions = self.connectivity.nutBoltArray.topclippositions
    #         for pos in clipPositions:
    #             loc = getGpPt(pos)
    #             sphere = BRepPrimAPI_MakeSphere(loc,2.0).Shape()
    #             self.display.DisplayShape(sphere, color = 'red',update = True)
    # 
    #     else:
    #         self.display.EraseAll()
    
    def call_3DModel(self, flag):
        self.commLogicObj.call_3DModel(flag)

    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam")

    def call_3DColumn(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column")

    def call_3DSeatAngle(self):
        '''Displaying Seat Angle in 3D
        '''
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxSeatAngle.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("SeatAngle")

        # TODO uncomment display3D model after debugging
        # self.display3Dmodel("SeatAngle")

    def unchecked_allChkBox(self):

        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
        
    def designParameters(self):
        '''
        This routine returns the neccessary design parameters.
        '''
        self.uiObj = self.getuser_inputs()
        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        dictangledata = self.fetchAnglePara()
        loc = str(self.ui.combo_connectivity.currentText())
        component = "Model"
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        return [self.uiObj, dictbeamdata, dictcoldata, dictangledata, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T]
    
    def design_btnclicked(self):
        '''
        '''
        # TODO input validation
        # self.validateInputsOnDesignBtn()
        self.alist = self.designParameters()
        
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self.unchecked_allChkBox()

        # Getting User Inputs.
        #self.uiObj = self.getuser_inputs()
        
        self.commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.alist[9], self.display, self.folder)
        # Seated Angle Design Calculations.
        self.resultObj = self.commLogicObj.call_finCalculation()
        d = self.resultObj[self.resultObj.keys()[0]]
        if len(str(d[d.keys()[0]])) == 0:
            self.ui.btn_CreateDesign.setEnabled(False)

        # Displaying Design Calculations To Output Window
        self.display_output(self.resultObj)

        # Displaying Messages related to Seated Angle Design.
        self.displaylog_totextedit(self.commLogicObj)

        # Displaying 3D Cad model
        status = self.resultObj['SeatAngle']['status']
        #self.call_3DModel(status)
        self.commLogicObj.call_3DModel(status)

    def create2Dcad(self, connectivity):
        ''' Returns the fuse model of finplate
        '''
        cadlist = self.connectivity.get_models()
        final_model = cadlist[0]
        for model in cadlist[1:]:
            final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        return final_model

        # Export to IGS,STEP,STL,BREP

    def save3DcadImages(self):
        if self.connectivity == None:
            self.connectivity = self.create3DColWebBeamWeb()
        if self.fuse_model == None:
            self.fuse_model = self.create2Dcad(self.connectivity)
        shape = self.fuse_model

        files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Export', str(self.folder) + "/untitled.igs", files_types)

        fName = str(fileName)
        file_extension = fName.split(".")[-1]

        if file_extension == 'igs':
            IGESControl.IGESControl_Controller().Init()
            iges_writer = IGESControl.IGESControl_Writer()
            iges_writer.AddShape(shape)
            iges_writer.Write(fName)

        elif file_extension == 'brep':
            BRepTools.breptools.Write(shape, fName)

        elif file_extension == 'stp':
            # initialize the STEP exporter
            step_writer = STEPControl_Writer()
            Interface_Static_SetCVal("write.step.schema", "AP203")

            # transfer shapes and write file
            step_writer.Transfer(shape, STEPControl_AsIs)
            status = step_writer.Write(fName)

            assert (status == IFSelect_RetDone)

        else:
            stl_writer = StlAPI_Writer()
            stl_writer.SetASCIIMode(True)
            stl_writer.Write(shape, fName)

        QtGui.QMessageBox.about(self, 'Information', "File saved")

    def call_seatangle2D_Drawing(self, view):  # call2D_Drawing(self,view)

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)

        commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.alist[9], self.display, self.folder)
        if view != 'All':
            fileName = QtGui.QFileDialog.getSaveFileName(self,
                                                         "Save SVG", str(self.folder) + '/untitled.svg',
                                                         "SVG files (*.svg)")
            fname = str(fileName)
        else:
            fname = ''
        base, base1, base2, base3 = commLogicObj.call2D_Drawing(view, fname, self.alist[3], self.folder)
        return base, base1, base2, base3
    

    def closeEvent(self, event):
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()

    # Following functions are trimmed in Seated angle module
        # about_osdag(), MyAboutOsdag(), tutorials(), MyTutorials(), open_tutorials()
    # open_osdag() also calls about_osdag()
    def open_osdag(self):
        # dialog=MyAboutOsdag(self)
        # dialog.show()
        pass

    def sample_report(self):
        #TODO: update path below
        # url = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'Sample_Folder',
        #                    'Sample_Report', 'The_PyQt4_tutorial.pdf')
        # webbrowser.open_new(r'file:///' + url)
        pass

    def sample_problem(self):
        # webbrowser.open_new(
        #     r'file:///D:/EclipseWorkspace/OsdagLIVE/Sample_Folder/Sample_Problems/The_PyQt4_tutorial.pdf')
        pass

def set_osdaglogger():
    global logger
    if logger == None:

        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # while launching from Osdag Main:
    # fh = logging.FileHandler("./Connections/Shear/SeatedAngle/seatangle.log", mode="a")
    # while launching from Seated angle folder
    fh = logging.FileHandler("./seatangle.log", mode="a")

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

def launchSeatedAngleController(osdagMainWindow, folder):
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    # while launching from Osdag Main:
    fh = logging.FileHandler("./Connections/Shear/SeatedAngle/seatangle.log", mode="w")
    #while launching from Seated Angle folder
    # fh = logging.FileHandler("./seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    # while launching from Osdag Main:
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/SeatedAngle/log.css"/>''')
    # while launching from Seated Angle folder:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href=".//log.css"/>''')

    module_setup()

    window = MainController(folder)
    osdagMainWindow.hide()

    window.show()
    window.closed.connect(osdagMainWindow.show)

if __name__ == '__main__':
    # launchSeatAngleController(None)

    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    # while launching from Osdag Main:
    fh = logging.FileHandler("./seatangle.log", mode="w")
    # while launching from Seated Angle folder
    # fh = logging.FileHandler("./seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    # while launching from Osdag Main:
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/SeatedAngle/log.css"/>''')
    # while launching from Seated Angle folder:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href=".//log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    module_setup()
    folder = None
    window = MainController(folder)
    window.show()
    sys.exit(app.exec_())
