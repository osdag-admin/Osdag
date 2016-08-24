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
from ui_SeatAngle import Ui_MainWindow
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
    # print"my popup window"

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
        shutil.copyfile(filename, str(self.mainController.folder) + "/css/cmpylogoFin.png")

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

        self.ui.comboBeamSec.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())
        self.ui.comboAngleSec.addItems(get_anglecombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Please Select Type': '',
                          'HSFG': [8.8, 10.8],
                          'Black Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()

        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        # self.ui.btn_front.clicked.connect(self.call_Frontview)
        # self.ui.btn_top.clicked.connect(self.call_Topview)
        # self.ui.btn_side.clicked.connect(self.call_Sideview)

        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxSeatAngle.clicked.connect(self.call_3DSeatAngle)

        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
        #TODO add exhaustive validators
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)

        minfuVal = 290
        maxfuVal = 590
        self.ui.txtFu.editingFinished.connect(
            lambda: self.check_range(self.ui.txtFu, self.ui.lbl_fu, minfuVal, maxfuVal))

        minfyVal = 165
        maxfyVal = 450
        self.ui.txtFy.editingFinished.connect(
            lambda: self.check_range(self.ui.txtFy, self.ui.lbl_fy, minfyVal, maxfyVal))

        #-------------------------------------------------
        # Menu Bar
        # File Menu
        self.ui.actionSave_Front_View.triggered.connect(lambda: self.call2D_Drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.call2D_Drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.call2D_Drawing("Top"))
        self.ui.actionQuit_fin_plate_design.setShortcut('Ctrl+Q')
        self.ui.actionQuit_fin_plate_design.setStatusTip('Exit application')
        self.ui.actionQuit_fin_plate_design.triggered.connect(QtGui.qApp.quit)

        self.ui.actionCreate_design_report.triggered.connect(self.createDesignReport)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_current_2D_image_as.triggered.connect(self.save2DcadImages)
        self.ui.actionView_2D_on_ZX.triggered.connect(self.call_Frontview)
        self.ui.actionView_2D_on_XY.triggered.connect(self.call_Topview)
        self.ui.actionView_2D_on_YZ.triggered.connect(self.call_Sideview)
        self.ui.actionPan.triggered.connect(self.call_Pannig)

        # self.ui.comboBeamSec.addItems(get_beamcombolist())
        # self.ui.comboColSec.addItems(get_columncombolist())
        #         self.ui.comboBeamSec.currentIndexChanged[str].connect(self.fillPlateThickCombo)
        #         self.ui.comboColSec.currentIndexChanged[str].connect(self.populateWeldThickCombo)
        #         self.ui.comboConnLoc.currentIndexChanged[str].connect(self.populateWeldThickCombo)
        #         self.ui.comboPlateThick_2.currentIndexChanged[str].connect(self.populateWeldThickCombo)
        #

        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.createDesignReport)  # Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)

        # Saving and Restoring the finPlate window state.
        # self.retrieve_prevstate()

        self.ui.btnZmIn.clicked.connect(self.callZoomin)
        self.ui.btnZmOut.clicked.connect(self.callZoomout)
        self.ui.btnRotatCw.clicked.connect(self.callRotation)
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

        # Initialising the qtviewer
        self.display, _ = self.init_display(backend_str="pyqt4")

        self.ui.btnSvgSave.clicked.connect(self.save3DcadImages)
        # self.ui.btnSvgSave.clicked.connect(lambda:self.saveTopng(self.display))

        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()

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
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Export', "/home/jeffy/Cadfiles/untitled.png", files_types)
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
        self.ui.btn_top.setEnabled(False)
        self.ui.btn_side.setEnabled(False)

        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.chkBxSeatAngle.setEnabled(False)

    def enableViewButtons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn_side.setEnabled(True)

        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxSeatAngle.setEnabled(True)

    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if (uiObj != None):
            self.ui.comboBeamSec.setCurrentIndex(self.ui.comboBeamSec.findText(uiObj['Member']['BeamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['ColumSection']))

            self.ui.txtFu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(uiObj['Member']['fy (MPa)']))

            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))

            self.ui.txtShear.setText(str(uiObj['Load']['ShearForce (kN)']))

            self.ui.comboDiameter.setCurrentIndex(self.ui.comboDiameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            comboTypeIndex = self.ui.comboType.findText(str(uiObj['Bolt']['Type']))
            self.ui.comboType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))

            prevValue = str(uiObj['Bolt']['Grade'])

            comboGradeIndex = self.ui.comboGrade.findText(prevValue)

            self.ui.comboGrade.setCurrentIndex(comboGradeIndex)

            selection = str(uiObj['Plate']['Thickness (mm)'])
            selectionIndex = self.ui.comboPlateThick_2.findText(selection)
            self.ui.comboPlateThick_2.setCurrentIndex(selectionIndex)
            self.ui.txtPlateLen.setText(str(uiObj['Plate']['Height (mm)']))
            self.ui.txtPlateWidth.setText(str(uiObj['Plate']['Width (mm)']))

            self.ui.comboWldSize.setCurrentIndex(self.ui.comboWldSize.findText(str(uiObj['Weld']['Size (mm)'])))

    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
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
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        uiObj["Bolt"]["Grade"] = float(self.ui.comboGrade.currentText())
        uiObj["Bolt"]["Type"] = str(self.ui.comboType.currentText())

        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.comboBeamSec.currentText())
        uiObj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiObj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]

        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = self.ui.txtShear.text().toInt()[0]

        uiObj['Angle'] = {}
        uiObj['Angle']['AngleSection'] = str(self.ui.comboAngleSec.currentText())

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
        outObj['SeatAngle']["Length (mm)"] = float(self.ui.txtSeatLength.text())
        outObj['SeatAngle']["Moment Demand (kNm)"] = float(self.ui.txtExtMomnt.text())
        outObj['SeatAngle']["Moment Capacity (kNm)"] = float(self.ui.txtMomntCapacity.text())
        outObj['SeatAngle']["Shear Demand (kN/mm)"] = float(self.ui.txtShearDemand.text())
        outObj['SeatAngle']["Shear Capacity (kN/mm)"] = float(self.ui.txtShearCapacity_2.text())
        outObj['SeatAngle']["Beam Shear Strength (kN/mm)"] = float(self.ui.txtBeamShearStrength.text())

        outObj['Bolt'] = {}
        outObj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txtShearCapacity.text())
        outObj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txtBearingCapacity.text())
        outObj['Bolt']["Capacity Of Bolt (kN)"] = float(self.ui.txtBoltCapacity.text())
        outObj['Bolt']["Bolt group capacity (kN)"] = float(self.ui.txtBoltGroupCapacity.text())
        outObj['Bolt']["No Of Bolts"] = float(self.ui.txtNoBolts.text())
        outObj['Bolt']["No.Of Row"] = int(self.ui.txt_row.text())
        outObj['Bolt']["No.Of Column"] = int(self.ui.txt_col.text())
        outObj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txtPitch.text())
        outObj['Bolt']["Guage Distance (mm)"] = float(self.ui.txtGuage.text())
        outObj['Bolt']["End Distance (mm)"] = float(self.ui.txtEndDist.text())
        outObj['Bolt']["Edge Distance (mm)"] = float(self.ui.txtEdgeDist.text())

        return outObj

    def create_design_report(self):
        design_report_dialog = DesignReportDialog(self)
        design_report_dialog.show()

    def save_design(self):
        self.outdict = self.outputdict()
        self.inputdict = self.getuser_inputs()
        self.save_yaml(self.outdict, self.inputdict)

        # self.save(self.outdict,self.inputdict)

    def save_log(self):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", "/home/jeffy/SaveMessages",
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
        # user Inputs

        self.ui.comboDiameter.setCurrentIndex(0)
        self.ui.comboGrade.setCurrentIndex(0)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboBeamSec.setCurrentIndex(0)
        self.ui.comboColSec.setCurrentIndex(0)
        self.ui.comboConnLoc.setCurrentIndex(0)
        self.ui.txtFu.clear()
        self.ui.txtFy.clear()

        self.ui.txtShear.clear()

        self.ui.comboAngleSec.setCurrentIndex(0)

        # ----Output

        self.ui.txtSeatLength.clear()
        self.ui.txtExtMomnt.clear()
        self.ui.txtMomntCapacity.clear()
        self.ui.txtShearDemand.clear()
        self.ui.txtShearCapacity.clear()
        self.ui.txtBeamShearStrength.clear()

        self.ui.txtShrCapacity_2.clear()
        self.ui.txtBearingCapacity.clear()
        self.ui.txtBoltCapacity.clear()
        self.ui.txtBoltGroupCapacity.clear()
        self.ui.txtNoBolts.clear()
        self.ui.txt_row.clear()
        self.ui.txt_col.clear()
        self.ui.txtPitch.clear()
        self.ui.txtGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()

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
        items = self.gradeType[str(index)]

        self.ui.comboGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))

        self.ui.comboGrade.addItems(strItems)

    def check_range(self, widget, lblwidget, minVal, maxVal):

        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yield Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr)
        if (val < minVal or val > maxVal):
            QtGui.QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s' % (minVal, maxVal))
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
        self.ui.txtShearCapacity.setText(str(bolt_shear_capacity))

        bearing_capacity = resultObj['Bolt']['Bearing Capacity (kN)']
        self.ui.txtBearingCapacity.setText(str(bearing_capacity))

        bolt_capacity = resultObj['Bolt']['Capacity Of Bolt (kN)']
        self.ui.txtBoltCapacity.setText(str(bolt_capacity))

        no_ofbolts = resultObj['Bolt']['No Of Bolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        # newly added field
        boltGrp_capacity = resultObj['Bolt']['Bolt group capacity (kN)']
        self.ui.txtBoltGroupCapacity.setText(str(boltGrp_capacity))

        no_ofrows = resultObj['Bolt']['No.Of Row']
        self.ui.txt_row.setText(str(no_ofrows))

        no_ofcol = resultObj['Bolt']['No.Of Column']
        self.ui.txt_col.setText(str(no_ofcol))

        pitch_dist = resultObj['Bolt']['Pitch Distance (mm)']
        self.ui.txtPitch.setText(str(pitch_dist))

        gauge_dist = resultObj['Bolt']['Gauge Distance (mm)']
        self.ui.txtGuage.setText(str(gauge_dist))

        end_dist = resultObj['Bolt']['End Distance (mm)']
        self.ui.txtEndDist.setText(str(end_dist))
        #
        edge_dist = resultObj['Bolt']['Edge Distance (mm)']
        self.ui.txtEdgeDist.setText(str(edge_dist))

        angle_length = resultObj['SeatAngle']['Length (mm)']
        self.ui.txtSeatLength.setText(str(angle_length))

        moment_demand = resultObj['SeatAngle']['Moment Demand (kNm)']
        self.ui.txtExtMomnt.setText(str(moment_demand))

        moment_capacity = resultObj['SeatAngle']['Moment Capacity (kNm)']
        self.ui.txtMomntCapacity.setText(str(moment_capacity))

        shear_demand = resultObj['SeatAngle']['Shear Demand (kN/mm)']
        self.ui.txtShearDemand.setText(str(shear_demand))

        angle_shear_capacity = resultObj['SeatAngle']['Shear Capacity (kN/mm)']
        self.ui.txtShearCapacity_2.setText(str(angle_shear_capacity))

        beam_shear_strength = resultObj['SeatAngle']['Beam Shear Strength (kN/mm)']
        self.ui.txtBeamShearStrength.setText(str(beam_shear_strength))

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
            raise ImportError(
                "No compliant GUI library found. You must have either PySide, PyQt4 or wxPython installed.")
            sys.exit(1)

    # QtViewer
    def init_display(self, backend_str=None, size=(1024, 768)):
        if os.name == 'nt':

            global display, start_display, app, _

            from OCC.Display.backend import get_loaded_backend
            lodedbkend = get_loaded_backend()
            from OCC.Display.backend import get_backend, have_backend
            from osdagMainSettings import backend_name
            if (not have_backend() and backend_name() == "pyqt4"):
                get_backend("qt-pyqt4")
        else:
            global display, start_display, app, _, USED_BACKEND

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
        # self.ui.model2dTab = qtViewer3d(self)

        self.setWindowTitle("Osdag-%s 3d viewer ('%s' backend)" % (VERSION, backend_name))
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")
        # self.ui.mytabWidget.addTab(self.ui.model2dTab,"")

        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display
        # display_2d = self.ui.model2dTab._display

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
            # self.ui.model2dTab.raise_()   # make the application float to the top

        return display, start_display

    def showColorDialog(self):

        col = QtGui.QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

    def display3Dmodel(self, component):
        self.display.EraseAll()
        self.display.SetModeShaded()
        display.DisableAntiAliasing()
        self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
        self.display.View_Front()
        self.display.View_Iso()
        self.display.FitAll()
        if component == "Column":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
        elif component == "Beam":
            osdagDisplayShape(self.display, self.connectivity.get_beamModel(), material=Graphic3d_NOT_2D_ALUMINUM,
                              update=True)
            # osdagDisplayShape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif component == "SeatAngle":
            #             osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
                # self.display.DisplayShape(self.connectivity.nutBoltArray.getModels(), color = Quantity_NOC_SADDLEBROWN, update=True)
        elif component == "Model":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM,
                              update=True)
            #             osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
            #             osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
            osdagDisplayShape(self.display, self.connectivity.topclipangleModel, color='blue', update=True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
                # self.display.DisplayShape(self.connectivity.nutBoltArray.getModels(), color = Quantity_NOC_SADDLEBROWN, update=True)

    def fetchBeamPara(self):
        beam_sec = self.ui.comboBeamSec.currentText()
        dictbeamdata = get_beamdata(beam_sec)
        return dictbeamdata

    def fetchColumnPara(self):
        column_sec = self.ui.comboColSec.currentText()
        dictcoldata = get_columndata(column_sec)
        return dictcoldata

    def fetchAnglePara(self):
        angle_sec = self.ui.comboAngleSec.currentText()
        dictangledata = get_angledata(angle_sec)
        return dictangledata

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

    def call_3DModel(self, flag):
        self.ui.btnSvgSave.setEnabled(True)
        if self.ui.btn3D.isEnabled():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        if flag == True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
                # self.create3DColWebBeamWeb()
                self.connectivity = self.create3DColWebBeamWeb()
                self.fuse_model = None
            else:
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create3DColFlangeBeamWeb()
                self.fuse_model = None

            self.display3Dmodel("Model")


        else:
            self.display.EraseAll()
            self.display.DisplayMessage(gp_Pnt(1000, 0, 400), "Sorry, can not create 3D model", height=23.0)

    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display3Dmodel("Beam")

    def call_3DColumn(self):
        '''
        '''
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.display3Dmodel("Column")

    def call_3DSeatAngle(self):
        '''Displaying Seat Angle in 3D
        '''
        if self.ui.chkBxSeatAngle.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display3Dmodel("SeatAngle")

    def design_btnclicked(self):
        '''
        '''
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()

        # self.set_designlogger()
        # Getting User Inputs.
        uiObj = self.getuser_inputs()

        # FinPlate Design Calculations. 
        resultObj = SeatAngleConn(uiObj)

        # Displaying Design Calculations To Output Window
        self.display_output(resultObj)

        # Displaying Messages related to FinPlate Design.
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
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Export', "/home/jeffy/Cadfiles/untitled.igs", files_types)

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

    def display2DModel(self, final_model, viewName):

        # display, start_display, _, _ = self.simpleGUI()
        # self.display2d,_,_ = self.init_display(backend_str="pyqt4")
        self.display.EraseAll()

        self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

        self.display.SetModeHLR()
        # self.display.SetModeShaded()
        # Get Context
        ais_context = self.display.GetContext().GetObject()

        # Get Prs3d_drawer from previous context
        drawer_handle = ais_context.DefaultDrawer()
        drawer = drawer_handle.GetObject()
        drawer.EnableDrawHiddenLine()

        hla = drawer.HiddenLineAspect().GetObject()
        hla.SetWidth(2)
        hla.SetColor(Quantity_NOC_RED)

        # increase line width in the current viewer
        # This is only viewed in the HLR mode (hit 'e' key for instance)

        line_aspect = drawer.SeenLineAspect().GetObject()
        line_aspect.SetWidth(2.8)
        line_aspect.SetColor(Quantity_NOC_BLUE1)

        self.display.DisplayShape(final_model, update=False)

        if (viewName == "Front"):
            self.display.View_Front()
        elif (viewName == "Top"):
            self.display.View_Top()
        elif (viewName == "Right"):
            self.display.View_Right()
        elif (viewName == "Left"):
            self.display.View_Left()
        else:
            pass

            # start_display()

    def call_Frontview(self):

        '''Displays front view of 2Dmodel
        '''
        self.ui.btnSvgSave.setEnabled(False)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)
        if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(1)
            if self.connectivity == None:
                self.connectivity = self.create3DColWebBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel(self.fuse_model, "Front")

            self.call2D_Drawing()
        else:
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(0)
            if self.connectivity == None:
                self.connectivity = self.create3DColFlangeBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel(self.fuse_model, "Left")
            self.call2D_Drawing()

    def call2D_Drawing(self):
        uiObj = self.getuser_inputs()

        resultObj = SeatAngleConn(uiObj)
        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        fin2DFront = Fin2DCreatorFront(uiObj, resultObj, dictbeamdata, dictcoldata)
        fin2DFront.saveToSvg()

    def call_Topview(self):

        '''Displays Top view of 2Dmodel
        '''
        self.ui.btnSvgSave.setEnabled(False)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)

        if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(1)

            if self.connectivity == None:
                self.connectivity = self.create3DColWebBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel(self.fuse_model, "Top")
        else:
            self.display.EraseAll()
            self.ui.mytabWidget.setCurrentIndex(0)

            if self.connectivity == None:
                self.connectivity = self.create3DColFlangeBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel(self.fuse_model, "Top")

    def call_Sideview(self):

        '''Displays Side view of the 2Dmodel'
        '''
        self.ui.btnSvgSave.setEnabled(False)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxSeatAngle.setChecked(QtCore.Qt.Unchecked)

        if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
            self.ui.mytabWidget.setCurrentIndex(1)

            if self.connectivity == None:
                self.connectivity = self.create3DColWebBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel(self.fuse_model, "Right")
        else:
            self.ui.mytabWidget.setCurrentIndex(0)

            if self.connectivity == None:
                self.connectivity = self.create3DColFlangeBeamWeb()
            if self.fuse_model == None:
                self.fuse_model = self.create2Dcad(self.connectivity)
            self.display2DModel(self.fuse_model, "Front")

    def closeEvent(self, event):
        '''
        Closing Seat Angle window.
        '''
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()


def set_osdaglogger():
    logger = logging.getLogger("osdag")
    logger.setLevel(logging.DEBUG)

    # create the logging file handler
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

    # add handler to logger object
    logger.addHandler(fh)


def launchSeatedAngleController(osdagMainWindow):
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("./Connections/Shear/SeatAngle/seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="./Connections/Shear/SeatAngle/log.css"/>''')

    # app = QtGui.QApplication(sys.argv)
    window = MainController()
    osdagMainWindow.hide()

    window.show()
    window.closed.connect(osdagMainWindow.show)

    # sys.exit(app.exec_())


if __name__ == '__main__':
    # launchFinPlateController(None)

    # linking css to log file to display colour logs.
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())
