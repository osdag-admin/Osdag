'''
Created on 07-May-2015
@author: deepa

Updated 23-Aug-2016
@author: jayant
'''

import os.path

from PyQt4.QtCore import pyqtSignal
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
from filletweld import FilletWeld
from bolt import Bolt
from nut import Nut
from SeatAngleCalc import SeatAngleConn
from nutBoltPlacement import NutBoltArray

from colWebBeamWebConnectivity import ColWebBeamWeb
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
# from beamWebBeamWebConnectivity import BeamWebBeamWeb

from reportGenerator import *
from ui_seat_angle import Ui_MainWindow # ui_seat_angle is the revised ui (~23 Aug 2016)
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_HelpOsdag
from ui_tutorial import Ui_Tutorial


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
        input_summary = self.getPopUpInputs()
        self.mainController.save_design(input_summary)

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
        inputData = self.getPopUpInputs()
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Files', str(self.mainController.folder) + "/Profile",
                                                     '*.txt')
        infile = open(filename, 'w')
        pickle.dump(inputData, infile)
        infile.close()

    def getPopUpInputs(self):
        input_summary = {}
        input_summary["ProfileSummary"] = {}
        input_summary["ProfileSummary"]["CompanyName"] = str(self.ui.lineEdit_companyName.text())
        input_summary["ProfileSummary"]["CompanyLogo"] = str(self.ui.lbl_browse.text())
        input_summary["ProfileSummary"]["Group/TeamName"] = str(self.ui.lineEdit_groupName.text())
        input_summary["ProfileSummary"]["Designer"] = str(self.ui.lineEdit_designer.text())

        input_summary["ProjectTitle"] = str(self.ui.lineEdit_projectTitle.text())
        input_summary["Subtitle"] = str(self.ui.lineEdit_subtitle.text())
        input_summary["JobNumber"] = str(self.ui.lineEdit_jobNumber.text())
        input_summary["AdditionalComments"] = str(self.ui.txt_additionalComments.toPlainText())
        input_summary["Method"] = str(self.ui.comboBox_method.currentText())

        return input_summary

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

        # self.ui.btn_front.clicked.connect(self.call_Frontview)
        # self.ui.btn_front.clicked.connect(self.call_Frontview)
        # self.ui.btn_top.clicked.connect(self.call_Topview)
        # self.ui.btn_side.clicked.connect(self.call_Sideview)

        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxSeatAngle.clicked.connect(self.call_3DSeatAngle)

        validator = QtGui.QIntValidator()
        self.ui.txt_fu.setValidator(validator)
        self.ui.txt_fy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
        #TODO add exhaustive validators
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

        self.ui.actionSave_front_view.triggered.connect(lambda:self.call2D_Drawing("Front"))
        self.ui.actionSave_side_view.triggered.connect(lambda: self.call2D_Drawing("Side"))
        self.ui.actionSave_top_view.triggered.connect(lambda: self.call2D_Drawing("Top"))
        #TODO update ui variables with appropiate names and code below
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

        # self.ui.combo_beam_section.currentIndexChanged[int].connect(lambda: self.fillPlateThickCombo("combo_Beam"))

        # TODO checkBeam_B is incomplete
        # self.ui.comboColSec.currentIndexChanged[str].connect(self.checkBeam_B)
        # self.ui.combo_Beam.currentIndexChanged[int].connect(self.checkBeam_B)
        # self.ui.comboPlateThick_2.currentIndexChanged[int].connect(
        #     lambda: self.populateWeldThickCombo("comboPlateThick_2"))

        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.create_design_report)  # Saves the design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)

        self.ui.btn_front.clicked.connect(lambda: self.call2D_Drawing("Front"))
        self.ui.btn_side.clicked.connect(lambda: self.call2D_Drawing("Side"))
        self.ui.btn_top.clicked.connect(lambda: self.call2D_Drawing("Top"))

        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

        # Osdag logo for html
        self.ui.btn_Design.clicked.connect(self.osdag_header)

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

    def osdag_header(self):
        # osdag_header() and store_osdagheader(str) functions are combined here
        image_path = os.path.dirname(os.path.abspath(__file__))+os.path.join("..","..","..","ResourceFiles","Osdag_header.png")
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
                self.ui.comboColSec.addItems(get_beamcombolist())

            self.ui.combo_beam_section.setCurrentIndex(self.ui.combo_beam_section.findText(uiObj['Member']['BeamSection']))
            self.ui.combo_column_section.setCurrentIndex(self.ui.combo_column_section.findText(uiObj['Member']['ColumnSection']))

            self.ui.txt_fu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txt_fy.setText(str(uiObj['Member']['fy (MPa)']))

            self.ui.txt_shear_force.setText(str(uiObj['Load']['ShearForce (kN)']))

            self.ui.combo_bolt_diameter.setCurrentIndex(self.ui.combo_bolt_diameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            comboTypeIndex = self.ui.combo_bolt_type.findText(str(uiObj['Bolt']['Type']))
            self.ui.combo_bolt_type.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))
            comboGradeIndex = self.ui.combo_bolt_grade.findText(str(uiObj['Bolt']['Grade']))
            self.ui.combo_bolt_grade.setCurrentIndex(comboGradeIndex)

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
        outObj['SeatAngle']["Moment Demand (kNm)"] = float(self.ui.txt_moment_demand.text())
        outObj['SeatAngle']["Moment Capacity (kNm)"] = float(self.ui.txt_moment_capacity.text())
        outObj['SeatAngle']["Shear Demand (kN/mm)"] = float(self.ui.txt_seat_shear_demand.text())
        outObj['SeatAngle']["Shear Capacity (kN/mm)"] = float(self.ui.txt_seat_shear_capacity.text())
        # TODO confirm after checking UI: beam shear strength (mostly) vs seat shear strength(?)
        outObj['SeatAngle']["Beam Shear Strength (kN/mm)"] = float(self.ui.txt_seat_shear_strength.text())

        outObj['Bolt'] = {}
        outObj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txt_bolt_shear_capacity.text())
        outObj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txt_bolt_bearing_capacity.text())
        outObj['Bolt']["Capacity of Bolt (kN)"] = float(self.ui.txt_bolt_capacity.text())
        outObj['Bolt']["Bolt group capacity (kN)"] = float(self.ui.txt_bolt_group_capacity.text())
        outObj['Bolt']["No. of Bolts"] = float(self.ui.txt_no_bolts.text())
        outObj['Bolt']["No. of Row"] = int(self.ui.txt_bolt_rows.text())
        outObj['Bolt']["No. of Column"] = int(self.ui.txt_bolt_cols.text())
        outObj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txt_bolt_pitch.text())
        outObj['Bolt']["Guage Distance (mm)"] = float(self.ui.txt_bolt_gauge.text())
        outObj['Bolt']["End Distance (mm)"] = float(self.ui.txt_end_distance.text())
        outObj['Bolt']["Edge Distance (mm)"] = float(self.ui.txt_edge_distance.text())

        return outObj

    def show_design_report_dialog(self):
        design_report_dialog = DesignReportDialog(self)
        design_report_dialog.show()

    def create_design_report(self):
        self.show_design_report_dialog()
        # function name changed from createDesignReport

    def save_design(self):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/",
                                                                   "Html Files (*.html)")
        fileName = str(fileName)
        base, base_front, base_top, base_side = self.call2D_Drawing("All")
        inputdict = self.uiObj
        outdict = self.resultObj

        dictBeamData = self.fetchBeamPara()
        dictColData = self.fetchColumnPara()
        save_html(outdict, inputdict, dictBeamData, dictColData, popup_summary, fileName, self.folder, base,
                  base_front, base_top, base_side)

        QtGui.QMessageBox.about(self, 'Information', "Report Saved")

    def save_log(self):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.foler)+"/LogMessages",
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
        # TODO check seat OR beam shear strength
        self.ui.txt_seat_shear_strength.clear()

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
        self.ui.txt_bolt_cols.setText(str(no_of_col))

        pitch_dist = resultObj['Bolt']['Pitch Distance (mm)']
        self.ui.txtPitch.setText(str(pitch_dist))

        gauge_dist = resultObj['Bolt']['Gauge Distance (mm)']
        self.ui.txt_bolt_gauge.setText(str(gauge_dist))

        end_dist = resultObj['Bolt']['End Distance (mm)']
        self.ui.txt_end_distance.setText(str(end_dist))
        #
        edge_dist = resultObj['Bolt']['Edge Distance (mm)']
        self.ui.txt_edge_distance.setText(str(edge_dist))

        angle_length = resultObj['SeatAngle']['Length (mm)']
        self.ui.txt_seat_length.setText(str(angle_length))

        moment_demand = resultObj['SeatAngle']['Moment Demand (kNm)']
        self.ui.txt_moment_demand.setText(str(moment_demand))

        moment_capacity = resultObj['SeatAngle']['Moment Capacity (kNm)']
        self.ui.txt_moment_capacity.setText(str(moment_capacity))

        shear_demand = resultObj['SeatAngle']['Shear Demand (kN/mm)']
        self.ui.txt_seat_shear_demand.setText(str(shear_demand))

        angle_shear_capacity = resultObj['SeatAngle']['Shear Capacity (kN/mm)']
        self.ui.txt_seat_shear_capacity.setText(str(angle_shear_capacity))

        #TODO check seat or beam shear strength
        beam_shear_strength = resultObj['SeatAngle']['Beam Shear Strength (kN/mm)']
        self.ui.txt_seat_shear_strength.setText(str(beam_shear_strength))

    def displaylog_totextedit(self):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''

        afile = QtCore.QFile('./seatangle.log')

        if not afile.open(QtCore.QIODevice.ReadOnly):  # ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())

        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscrollBar = self.ui.textEdit.verticalScrollBar();
        vscrollBar.setValue(vscrollBar.maximum());
        afile.close()

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
        else:
            global display, start_display, app, USED_BACKEND

            if not backend_str:
                USED_BACKEND = self.get_backend()
            elif backend_str in ['pyside', 'pyqt4']:
                USED_BACKEND = backend_str
            else:
                raise ValueError("You should pass either 'qt' or 'tkinter' to the init_display function.")
                sys.exit(1)

            # Qt based simple GUI
            if USED_BACKEND in ['pyqt4', 'pyside']:
                if USED_BACKEND == 'pyqt4':
                    import OCC.Display.qtDisplay
                    from OCC.Display.qtDisplay import qtViewer3d
                    from PyQt4 import QtCore, QtGui, QtOpenGL

        from OCC.Display.qtDisplay import qtViewer3d

        self.ui.modelTab = qtViewer3d(self)

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

    def display3Dmodel(self, component):
        # TODO check display initialisation in other modules
        self.display, _ = self.init_display()

        self.display.EraseAll()
        self.display.SetModeShaded()
        display.DisableAntiAliasing()
        self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)

        loc = self.ui.combo_connectivity.currentText()
        if loc == "Column flange-Beam web":
            self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
        else:
            self.display.View_Iso()
            self.display.FitAll()

        if component == "Column":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
        elif component == "Beam":
            osdagDisplayShape(self.display, self.connectivity.get_beamModel(), material=Graphic3d_NOT_2D_ALUMINUM,
                              update=True)
        elif component == "SeatAngle":
            osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
        elif component == "Model":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM,
                              update=True)
            osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
            osdagDisplayShape(self.display, self.connectivity.topclipangleModel, color='blue', update=True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

# -------------------------------------------------------------------------
# TODO check the 3D drawing generating functions below

    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web
        '''
        uiObj = self.getuser_inputs()
        resultObj = SeatAngleConn(uiObj)

        dictbeamdata = self.fetchBeamPara()
        ##### BEAM PARAMETERS #####
        beam_D = int(dictbeamdata[QString("D")])
        beam_B = int(dictbeamdata[QString("B")])
        beam_tw = float(dictbeamdata[QString("tw")])
        beam_T = float(dictbeamdata[QString("T")])
        beam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(dictbeamdata[QString("R1")])
        beam_R2 = float(dictbeamdata[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                        length=beam_length)

        ##### COLUMN PARAMETERS ######
        dictcoldata = self.fetchColumnPara()

        column_D = int(dictcoldata[QString("D")])
        column_B = int(dictcoldata[QString("B")])
        column_tw = float(dictcoldata[QString("tw")])
        column_T = float(dictcoldata[QString("T")])
        column_alpha = float(dictcoldata[QString("FlangeSlope")])
        column_R1 = float(dictcoldata[QString("R1")])
        column_R2 = float(dictcoldata[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000)

        ##### ANGLE PARAMETERS ######
        dictangledata = self.fetchAnglePara()

        angle_l = resultObj['SeatAngle']["Length (mm)"]
        angle_a = int(dictangledata[QString("A")])
        angle_b = int(dictangledata[QString("B")])
        angle_t = float(dictangledata[QString("t")])
        angle_r1 = float(dictangledata[QString("R1")])
        angle_r2 = float(dictangledata[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        angle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2)
        #         topclipangle = Angle(L = angle_l, A = 60, B = 60,T = 6, R1 =6.5, R2 = 0)
        topclipangle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2)

        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####

        #         fillet_length = resultObj['Plate']['height']
        #         fillet_thickness =  resultObj['Weld']['thickness']
        #         plate_width = resultObj['Plate']['width']
        #         plate_thick = uiObj['Plate']['Thickness (mm)']
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = 10.0  # minimum bolt thickness As per Indian Standard
        bolt_Ht = 50.0  # minimum bolt length as per Indian Standard IS 3750(1985)
        nut_T = 12.0  # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2  #

        # plate = Plate(L= 300,W =100, T = 10)
        #         angle = Angle(L = angle_l, A = angle_a, B = angle_b,T = angle_t, R1 = angle_r1, R2 = angle_r2)

        # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        #         Fweld1 = FilletWeld(L= fillet_length,b = fillet_thickness, h = fillet_thickness)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = beam_tw + angle_t + nut_T

        nutBoltArray = NutBoltArray(resultObj, nut, bolt, gap)
        #         topclipnutboltArray = NutBoltArray(resultObj,nut,bolt,gap)

        colwebconn = ColWebBeamWeb(column, beam, angle, topclipangle, nutBoltArray)
        colwebconn.create_3dmodel()

        return colwebconn

    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection
        
        '''
        uiObj = self.getuser_inputs()
        resultObj = SeatAngleConn(uiObj)

        dictbeamdata = self.fetchBeamPara()
        #         fillet_length = resultObj['Plate']['height']
        #         fillet_thickness =  resultObj['Weld']['thickness']
        #         plate_width = resultObj['Plate']['width']
        #         plate_thick = uiObj['Plate']['Thickness (mm)']
        ##### BEAM PARAMETERS #####
        beam_D = int(dictbeamdata[QString("D")])
        beam_B = int(dictbeamdata[QString("B")])
        beam_tw = float(dictbeamdata[QString("tw")])
        beam_T = float(dictbeamdata[QString("T")])
        beam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(dictbeamdata[QString("R1")])
        beam_R2 = float(dictbeamdata[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                        length=beam_length)

        ##### COLUMN PARAMETERS ######
        dictcoldata = self.fetchColumnPara()

        column_D = int(dictcoldata[QString("D")])
        column_B = int(dictcoldata[QString("B")])
        column_tw = float(dictcoldata[QString("tw")])
        column_T = float(dictcoldata[QString("T")])
        column_alpha = float(dictcoldata[QString("FlangeSlope")])
        column_R1 = float(dictcoldata[QString("R1")])
        column_R2 = float(dictcoldata[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000)

        ##### ANGLE PARAMETERS ######
        dictangledata = self.fetchAnglePara()

        angle_l = resultObj['SeatAngle']["Length (mm)"]
        angle_a = int(dictangledata[QString("A")])
        angle_b = int(dictangledata[QString("B")])
        angle_t = float(dictangledata[QString("t")])
        angle_r1 = float(dictangledata[QString("R1")])
        angle_r2 = float(dictangledata[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        angle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2)

        topclipangle = Angle(L=angle_l, A=angle_a, B=angle_b, T=angle_t, R1=angle_r1, R2=angle_r2)

        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####

        #         fillet_length = resultObj['Plate']['height']
        #         fillet_thickness =  resultObj['Weld']['thickness']
        #         plate_width = resultObj['Plate']['width']
        #         plate_thick = uiObj['Plate']['Thickness (mm)']
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = 10.0  # minimum bolt thickness As per Indian Standard
        bolt_Ht = 50.0  # minimum bolt length as per Indian Standard
        nut_T = 12.0  # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2  #

        # plate = Plate(L= 300,W =100, T = 10)
        #         angle = Angle(L = angle_l, A = angle_a, B = angle_b,T = angle_t, R1 = angle_r1, R2 = angle_r2)

        # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        #         Fweld1 = FilletWeld(L= fillet_length,b = fillet_thickness, h = fillet_thickness)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = beam_tw + angle_t + nut_T

        nutBoltArray = NutBoltArray(resultObj, nut, bolt, gap)

        colflangeconn = ColFlangeBeamWeb(column, beam, angle, topclipangle, nutBoltArray)
        colflangeconn.create_3dmodel()
        return colflangeconn
# TODO check 3D drawing generating functions above
#-------------------------------------------------------------------------------
    def call_3DModel(self, flag):
        # self.ui.btnSvgSave.setEnabled(True)
        self.ui.btn3D.setChecked(QtCore.Qt.Checked)
        if self.ui.btn3D.isEnabled():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        if flag == True:
            if self.ui.combo_connectivity.currentText() == "Column web-Beam web":
                # self.create3DColWebBeamWeb()
                self.connectivity = self.create3DColWebBeamWeb()
                self.fuse_model = None

            elif self.ui.combo_connectivity.currentText() == "Column flange-Beam web":
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create3DColFlangeBeamWeb()
                self.fuse_model = None

            else:
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create3DBeamWebBeamWeb()
                self.fuse_model = None

            self.display3Dmodel("Model")

        else:
            self.display.EraseAll()

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

        self.display3Dmodel("Beam")

    def call_3DColumn(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.display3Dmodel("Column")

    def call_3DSeatAngle(self):
        '''Displaying Seat Angle in 3D
        '''
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxSeatAngle.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        # TODO uncomment display3D model after debugging
        # self.display3Dmodel("SeatAngle")

    def unchecked_allChkBox(self):

        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)

    def design_btnclicked(self):
        '''
        '''
        # TODO input validation
        # self.validateInputsOnDesignBtn()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self.unchecked_allChkBox()

        # Getting User Inputs.
        self.uiObj = self.getuser_inputs()

        # Seated Angle Design Calculations.
        self.resultObj = SeatAngleConn(self.uiObj)
        d = self.resultObj[self.resultObj.keys()[0]]
        if len(str(d[d.keys()[0]])) == 0:
            self.ui.btn_CreateDesign.setEnabled(False)

        # Displaying Design Calculations To Output Window
        self.display_output(resultObj)

        # Displaying Messages related to Seated Angle Design.
        self.displaylog_totextedit()

        # Displaying 3D Cad model
        status = resultObj['Bolt']['status']
        self.call_3DModel(status)

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

    def display2DModelOriginal(self, final_model, viewName):

        self.display, _ = self.init_display()
        self.display.EraseAll()
        # self.display.SetModeWireFrame()

        self.display.DisplayShape(final_model, update=True)
        self.display.SetModeHLR()

        if (viewName == "Front"):
            self.display.View_Front()
        elif (viewName == "Top"):
            self.display.View_Top()
        elif (viewName == "Right"):
            self.display.View_Right()
        else:
            pass

    # def display2DModel(self, final_model, viewName):
    #
    #     # display, start_display, _, _ = self.simpleGUI()
    #     # self.display2d,_,_ = self.init_display(backend_str="pyqt4")
    #     self.display.EraseAll()
    #
    #     self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
    #
    #     self.display.SetModeHLR()
    #     # self.display.SetModeShaded()
    #     # Get Context
    #     ais_context = self.display.GetContext().GetObject()
    #
    #     # Get Prs3d_drawer from previous context
    #     drawer_handle = ais_context.DefaultDrawer()
    #     drawer = drawer_handle.GetObject()
    #     drawer.EnableDrawHiddenLine()
    #
    #     hla = drawer.HiddenLineAspect().GetObject()
    #     hla.SetWidth(2)
    #     hla.SetColor(Quantity_NOC_RED)
    #
    #     # increase line width in the current viewer
    #     # This is only viewed in the HLR mode (hit 'e' key for instance)
    #
    #     line_aspect = drawer.SeenLineAspect().GetObject()
    #     line_aspect.SetWidth(2.8)
    #     line_aspect.SetColor(Quantity_NOC_BLUE1)
    #
    #     self.display.DisplayShape(final_model, update=False)
    #
    #     if (viewName == "Front"):
    #         self.display.View_Front()
    #     elif (viewName == "Top"):
    #         self.display.View_Top()
    #     elif (viewName == "Right"):
    #         self.display.View_Right()
    #     elif (viewName == "Left"):
    #         self.display.View_Left()
    #     else:
    #         pass
    #
    #         # start_display()

    def call2D_Drawing(view):
        ''' This routine saves the 2D SVG image as per the connectivity selected
            SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
            '''
        base = ''

        loc = self.ui.combo_connectivity.currentText()
        if view == "All":
            fileName = ''
            base_front = ''
            base_side = ''
            base_top = ''

            base1, base2, base3 = self.callDesired_View(fileName, view, base_front, base_top, base_side)
            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

            if loc == "Column flange-Beam web":

                data = str(self.folder) + "/css/3D_ModelSeatFB.png"
                for n in range(1, 100, 1):
                    if (os.path.exists(data)):
                        data = str(self.folder) + "/css/3D_ModelSeatFB" + str(n) + ".png"
                        continue
                base = os.path.basename(str(data))
                print "basenameee", base

            elif loc == "Column web-Beam web":
                data = str(self.folder) + "/css/3D_ModelSeatWB.png"
                for n in range(1, 100, 1):
                    if (os.path.exists(data)):
                        data = str(self.folder) + "/css/3D_ModelSeatWB" + str(n) + ".png"
                        continue
                base = os.path.basename(str(data))


            else:
                data = str(self.folder) + "/css/3D_ModelSeatBB.png"
                for n in range(1, 100, 1):
                    if (os.path.exists(data)):
                        data = str(self.folder) + "/css/3D_ModelSeatBB" + str(n) + ".png"
                        continue
                base = os.path.basename(str(data))

            self.display.ExportToImage(data)


        else:
            #             fileName = webbrowser.open_new(r'file:///untitled.svg')

            fileName = QtGui.QFileDialog.getSaveFileName(self,
                                                         "Save SVG", str(self.folder) + '/untitled.svg',
                                                         "SVG files (*.svg)")
            f = open(fileName, 'w')

            self.callDesired_View(fileName, view, base_front, base_top, base_side)
            # f.close() #TODO check with fin plate module

        print "basenameee", base
        print "base front", base1
        print "base side", base2
        print "base top", base3
        return (base, base1, base2, base3)

    def callDesired_View(self, fileName, view, base_front, base_top, base_side):

        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)

        #TODO update for common logic. Won't work currently
        uiObj = self.uiObj
        resultObj = self.resultObj
        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        seatCommonObj = SeatCommonData(uiObj, resultObj, dictbeamdata, dictcoldata, self.folder)
        base_front, base_top, base_side = seatCommonObj.saveToSvg(str(fileName), view, base_front, base_top,
                                                                 base_side)
        return (base_front, base_top, base_side)
        print"sucessfully worked"

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
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="./Connections/Shear/SeatedAngle/log.css"/>''')
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
    fh = logging.FileHandler("./Connections/Shear/SeatAngle/seatangle.log", mode="w")
    # while launching from Seated Angle folder
    # fh = logging.FileHandler("./seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    # while launching from Osdag Main:
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="./Connections/Shear/SeatedAngle/log.css"/>''')
    # while launching from Seated Angle folder:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href=".//log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    module_setup()
    window = MainController()
    window.show()
    sys.exit(app.exec_())

#TODO : connect to osdag main window