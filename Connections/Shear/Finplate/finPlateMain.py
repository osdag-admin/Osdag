'''
Created on 07-May-2015
comment

@author: deepa
'''
from PyQt4.QtCore import QString, pyqtSignal
from OCC.TopoDS import topods, TopoDS_Shape
from OCC.gp import gp_Pnt
from nutBoltPlacement import NutBoltArray
from OCC import VERSION, BRepTools
from ui_finPlate import Ui_MainWindow
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_HelpOsdag
from ui_tutorial import Ui_Tutorial
from model import *
from finPlateCalc import finConn
import pickle
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from ISection import ISection
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from weld import  Weld
from plate import Plate
from bolt import Bolt
from nut import Nut 
from notch import Notch
import os.path
from utilities import osdagDisplayShape
from colWebBeamWebConnectivity import ColWebBeamWeb
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from beamWebBeamWebConnectivity import BeamWebBeamWeb
from OCC import IGESControl
from filletweld import FilletWeld
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone
from OCC.StlAPI import StlAPI_Writer
from drawing_2D import FinCommonData

from report_generator import * # TODO refactored code in report_generator; old = reportGenerator
from ModelUtils import getGpPt
##### Testing imports
import OCC.V3d
import pdfkit
import shutil
import webbrowser
from commonLogic import CommonDesignLogic


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


class MyPopupDialog(QtGui.QDialog):

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
        filename = QtGui.QFileDialog.getOpenFileName(
            self, 'Open File', " ",
            'Images (*.png *.svg*.jpg)',
            None, QtGui.QFileDialog.DontUseNativeDialog)

        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

        return str(filename)

    def desired_location(self, filename):

        shutil.copyfile(filename, str(self.mainController.folder) +
                        "/images_html/cmpylogoFin.png")

    def saveUserProfile(self):

        inputData = self.getPopUpInputs()
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Files',
                                                     str(self. mainController.folder) + "/Profile", '*.txt')
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

        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Files', str(self.mainController.folder) + "/Profile", "All Files (*)")
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
        self.ui.combo_Beam.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Please Select Type': '', 'HSFG': [8.8, 10.8],
                          'Black Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convertColComboToBeam)

        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        # self.ui.btn_2D.clicked.connect(self.call2D_Drawing)
        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxFinplate.clicked.connect(self.call_3DFinplate)

        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
        self.ui.txtPlateLen.setValidator(dbl_validator)
        self.ui.txtPlateLen.setMaxLength(7)
        self.ui.txtPlateWidth.setValidator(dbl_validator)
        self.ui.txtPlateWidth.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)

        minfuVal = 290
        maxfuVal = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu, self.ui.lbl_fu, minfuVal, maxfuVal))

        minfyVal = 165
        maxfyVal = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy, self.ui.lbl_fy, minfyVal, maxfyVal))

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # File Menu

        self.ui.actionSave_Front_View.triggered.connect(lambda: self.callFin2D_Drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.callFin2D_Drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.callFin2D_Drawing("Top"))
        self.ui.actionQuit_fin_plate_design.setShortcut('Ctrl+Q')
        self.ui.actionQuit_fin_plate_design.setStatusTip('Exit application')
        self.ui.actionQuit_fin_plate_design.triggered.connect(QtGui.qApp.quit)

        self.ui.actionCreate_design_report.triggered.connect(self.createDesignReport)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_curren_image_as.triggered.connect(self.save_cadImages)
        self.ui.actionPan.triggered.connect(self.call_Pannig)
        # graphics
        self.ui.actionBeam_2.triggered.connect(self.call_3DBeam)
        self.ui.actionColumn_2.triggered.connect(self.call_3DColumn)
        self.ui.actionFinplate_2.triggered.connect(self.call_3DFinplate)
        self.ui.actionShow_all.triggered.connect(lambda: self.call_3DModel(True))
        self.ui.actionChange_background.triggered.connect(self.showColorDialog)
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        self.ui.combo_Beam.currentIndexChanged[int].connect(lambda: self.fillPlateThickCombo("combo_Beam"))

        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkBeam_B)
        self.ui.combo_Beam.currentIndexChanged[int].connect(self.checkBeam_B)
        self.ui.comboPlateThick_2.currentIndexChanged[int].connect(lambda: self.populateWeldThickCombo("comboPlateThick_2"))
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.createDesignReport)  # Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        # self.retrieve_prevstate()

        self.ui.btnFront.clicked.connect(lambda: self.callFin2D_Drawing("Front"))
        self.ui.btnSide.clicked.connect(lambda: self.callFin2D_Drawing("Side"))
        self.ui.btnTop.clicked.connect(lambda: self.callFin2D_Drawing("Top"))

        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

# ************************************** Osdag logo for html********************************************************************
        self.ui.btn_Design.clicked.connect(self.osdag_header)

# ************************************ Help button *******************************************************************************
        self.ui.actionAbout_Osdag_2.triggered.connect(self.open_osdag)
        self.ui.actionSample_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_reports.triggered.connect(self.sample_report)
        self.ui.actionSample_Problems.triggered.connect(self.sample_problem)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        self.resultObj = None
        self.uiObj = None
        self.commLogicObj = None

    def osdag_header(self):
        image_path = "ResourceFiles/Osdag_header.png"
        self.store_osdagheader(image_path)

    def store_osdagheader(self, image_path):
        shutil.copyfile(image_path, str(self.folder) + "/images_html/Osdag_header.png")

    def fetchBeamPara(self):
        beam_sec = self.ui.combo_Beam.currentText()
        dictbeamdata = get_beamdata(beam_sec)
        return dictbeamdata

    def fetchColumnPara(self):
        column_sec = self.ui.comboColSec.currentText()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            dictcoldata = get_beamdata(column_sec)
        else:
            dictcoldata = get_columndata(column_sec)
        return dictcoldata

    def convertColComboToBeam(self):
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.lbl_beam.setText(" Secondary beam *")
            self.ui.lbl_column.setText("Primary beam *")

            self.ui.chkBxBeam.setText("SBeam")
            # self.ui.chkBxBeam.setShortcut("MainWindow", "Alt+Shift+B")
            self.ui.chkBxBeam.setToolTip("Secondary  beam")
            self.ui.chkBxCol.setText("PBeam")
            # self.ui.chkBxCol.setShortcut("MainWindow", "Alt+Shift+C")
            self.ui.chkBxCol.setToolTip("Primary beam")

            self.ui.comboColSec.clear()
            # self.ui.comboColSec.setObjectName("comboSecondaryBeam")
            # self.ui.comboSecondaryBeam.addItems(get_beamcombolist())
            self.ui.comboColSec.addItems(get_beamcombolist())
            # self.ui.comboColSec.currentIndex()
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboColSec.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()

            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboType.setCurrentIndex((0))
            self.ui.comboGrade.setCurrentIndex((0))
            self.ui.comboPlateThick_2.setItemText(0, "Select Plate thickness")
            self.ui.comboPlateThick_2.setCurrentIndex((0))
            self.ui.txtPlateLen.clear()
            self.ui.txtPlateWidth.clear()
            self.ui.comboWldSize.setItemText(0, "Select weld thickness")
            self.ui.comboWldSize.setCurrentIndex((0))

            self.ui.txtShrCapacity.clear()
            self.ui.txtbearCapacity.clear()
            self.ui.txtBoltCapacity.clear()
            self.ui.txtNoBolts.clear()
            self.ui.txtboltgrpcapacity.clear()
            self.ui.txt_row.clear()
            self.ui.txt_col.clear()
            self.ui.txtPitch.clear()
            self.ui.txtGuage.clear()
            self.ui.txtEndDist.clear()
            self.ui.txtEdgeDist.clear()
            self.ui.txtplate_ht.clear()
            self.ui.txtplate_width.clear()
            self.ui.txtExtMomnt.clear()
            self.ui.txtMomntCapacity.clear()
            self.ui.txtResltShr.clear()
            self.ui.txtWeldStrng.clear()

        elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":

            self.ui.lbl_column.setText("Column Section *")
            self.ui.lbl_beam.setText("Beam section *")
            self.ui.chkBxBeam.setText("Beam")
            self.ui.chkBxBeam.setToolTip("Beam only")
            self.ui.chkBxCol.setText("Column")
            self.ui.chkBxCol.setToolTip("Column only")
            self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_columncombolist())
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboColSec.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()

            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboType.setCurrentIndex((0))
            self.ui.comboGrade.setCurrentIndex((0))
            self.ui.comboPlateThick_2.setItemText(0, "Select Plate thickness")
            self.ui.comboPlateThick_2.setCurrentIndex((0))
            self.ui.txtPlateLen.clear()
            self.ui.txtPlateWidth.clear()
            self.ui.comboWldSize.setItemText(0, "Select weld thickness")
            self.ui.comboWldSize.setCurrentIndex((0))

            self.ui.txtShrCapacity.clear()
            self.ui.txtbearCapacity.clear()
            self.ui.txtBoltCapacity.clear()
            self.ui.txtNoBolts.clear()
            self.ui.txtboltgrpcapacity.clear()
            self.ui.txt_row.clear()
            self.ui.txt_col.clear()
            self.ui.txtPitch.clear()
            self.ui.txtGuage.clear()
            self.ui.txtEndDist.clear()
            self.ui.txtEdgeDist.clear()
            self.ui.txtplate_ht.clear()
            self.ui.txtplate_width.clear()
            self.ui.txtExtMomnt.clear()
            self.ui.txtMomntCapacity.clear()
            self.ui.txtResltShr.clear()
            self.ui.txtWeldStrng.clear()

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

    def save_cadImages(self):

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
        self.ui.btnFront.setEnabled(False)
        self.ui.btnSide.setEnabled(False)
        self.ui.btnTop.setEnabled(False)
        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.chkBxFinplate.setEnabled(False)
        self.ui.btn_CreateDesign.setEnabled(False)
        self.ui.btn_SaveMessages.setEnabled(False)

        # Disable Menubar 
        self.ui.menubar.setEnabled(False)

    def enableViewButtons(self):
        '''
        Enables the all buttons in toolbar
        '''
        # self.ui.btn_2D.setEnabled(True)
        self.ui.btnFront.setEnabled(True)
        self.ui.btnSide.setEnabled(True)
        self.ui.btnTop.setEnabled(True)
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxFinplate.setEnabled(True)
        self.ui.menubar.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)

    def fillPlateThickCombo(self, culprit):

        '''Populates the plate thickness on the basis of beam web thickness and plate thickness check
        '''
        if self.ui.combo_Beam.currentText() == "Select section":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return
        else:
            dictbeamdata = self.fetchBeamPara()
            beam_tw = float(dictbeamdata[QString("tw")])
            plateThickness = [6, 8, 10, 12, 14, 16, 18, 20]

            newlist = []
            # newlist = ['Select plate thickness']
            for ele in plateThickness[:]:
                item = int(ele)
                if item >= beam_tw:
                    newlist.append(str(item))

            self.ui.comboPlateThick_2.blockSignals(True)
            self.ui.comboPlateThick_2.clear()
            for i in newlist[:]:
                self.ui.comboPlateThick_2.addItem(str(i))

            self.ui.comboPlateThick_2.setCurrentIndex(-1)

            self.ui.comboPlateThick_2.blockSignals(False)
            self.ui.comboPlateThick_2.setCurrentIndex(0)

    def populateWeldThickCombo(self, culprit):
        '''
        Returns the weld thickness on the basis column flange and plate thickness check
        ThickerPart between column Flange and plate thickness again get checked according to the IS 800 Table 21 (Name of the table :Minimum Size of First Rum or of a
        Single Run Fillet Weld)
        '''
        if self.ui.combo_Beam.currentText() == "Select section":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return

        else:
            newlist = []
            weldlist = [3, 4, 5, 6, 8, 10, 12, 16]
            dictbeamdata = self.fetchBeamPara()
            beam_tw = float(dictbeamdata[QString("tw")])
            dictcoldata = self.fetchColumnPara()
            # column_tf = float(dictcoldata[QString("T")])
            # column_tw = float(dictcoldata[QString("tw")])
            plate_thickness = self.ui.comboPlateThick_2.currentText()
            plate_thick = plate_thickness.toFloat()

            if self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
                if self.ui.comboColSec.currentText() == "Select section":
                    self.ui.comboWldSize.clear()
                    return
                else:
                    column_tf = float(dictcoldata[QString("T")])
                    thickerPart = column_tf > plate_thick[0] and column_tf or plate_thick[0]

            elif self.ui.comboConnLoc.currentText() == "Column web-Beam web": 
                if self.ui.comboColSec.currentText() == "Select section":
                    self.ui.comboWldSize.clear()
                    return
                else:
                    column_tw = float(dictcoldata[QString("tw")])
                    thickerPart = column_tw > plate_thick[0] and column_tw or plate_thick[0]
            else:
                PBeam_tw = float(dictcoldata[QString("tw")])
                thickerPart = PBeam_tw > plate_thick[0] and PBeam_tw or plate_thick[0]

            if thickerPart in range(0, 11):
                weld_index = weldlist.index(3)
                newlist.extend(weldlist[weld_index:])
            elif thickerPart in range(11, 21):
                weld_index = weldlist.index(5)
                newlist.extend(weldlist[weld_index:])
            elif thickerPart in range(21, 33):
                weld_index = weldlist.index(6)
                newlist.extend(weldlist[weld_index:])
            else:
                weld_index = weldlist.index(8)
                newlist.extend(weldlist[weld_index:])

            self.ui.comboWldSize.clear()
            for element in newlist[:]:
                self.ui.comboWldSize.addItem(str(element))

    def retrieve_prevstate(self):
        '''
        This routine is responsible for maintaining previous session's  data
        '''
        uiObj = self.get_prevstate()
        self.setDictToUserInputs(uiObj)

    def setDictToUserInputs(self, uiObj):

        if(uiObj is not None):

            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))

            if uiObj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.lbl_beam.setText('Secondary beam *')
                self.ui.lbl_column.setText('Primary beam *')
                self.ui.comboColSec.addItems(get_beamcombolist())

            self.ui.combo_Beam.setCurrentIndex(self.ui.combo_Beam.findText(uiObj['Member']['BeamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['ColumSection']))

            self.ui.txtFu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(uiObj['Member']['fy (MPa)']))

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
        Setting image to connectivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web":
            pixmap = QtGui.QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            # self.ui.lbl_connectivity.show()
        elif(loc == "Column web-Beam web"):
            picmap = QtGui.QPixmap(":/newPrefix/images/colW3.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)
        else:
            picmap = QtGui.QPixmap(":/newPrefix/images/b-b.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)

        return True

    def getuser_inputs(self):
        '''(none) -> Dictionary

        Returns the dictionary object with the user input fields for designing fin plate connection

        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        uiObj["Bolt"]["Grade"] = float(self.ui.comboGrade.currentText())
        uiObj["Bolt"]["Type"] = str(self.ui.comboType.currentText())

        uiObj["Weld"] = {}
        uiObj["Weld"]['Size (mm)'] = self.ui.comboWldSize.currentText().toInt()[0]

        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        uiObj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiObj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]

        uiObj['Plate'] = {}
        uiObj['Plate']['Thickness (mm)'] = self.ui.comboPlateThick_2.currentText().toInt()[0]
        uiObj['Plate']['Height (mm)'] = self.ui.txtPlateLen.text().toInt()[0]  # changes the label length to height 
        uiObj['Plate']['Width (mm)'] = self.ui.txtPlateWidth.text().toInt()[0]

        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = self.ui.txtShear.text().toInt()[0]

        return uiObj

    def save_inputs(self, uiObj):

        '''(Dictionary)--> None

        '''
        inputFile = QtCore.QFile('Connections/Shear/Finplate/saveINPUT.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        pickle.dump(uiObj, inputFile)

    def get_prevstate(self):
        '''
        '''
        fileName = 'Connections/Shear/Finplate/saveINPUT.txt'

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
        outObj['Plate'] = {}
        # outObj['Plate']["Thickness(mm)"] = float(self.ui.txtPlateThick.text())
        outObj['Plate']["External Moment (kN-m)"] = float(self.ui.txtExtMomnt.text())
        outObj['Plate']["Moment Capacity (kN-m)"] = float(self.ui.txtMomntCapacity.text())

        outObj['Weld'] = {}
        # outObj['Weld']["Weld Thickness(mm)"] = float(self.ui.txtWeldThick.text())
        outObj['Weld']["Resultant Shear (kN/mm)"] = float(self.ui.txtResltShr.text())
        outObj['Weld']["Weld Strength (kN/mm)"] = float(self.ui.txtWeldStrng.text())

        outObj['Bolt'] = {}
        outObj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txtShrCapacity.text())
        outObj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txtbearCapacity.text())
        outObj['Bolt']["Capacity Of Bolt (kN)"] = float(self.ui.txtBoltCapacity.text())
        outObj['Bolt']["No Of Bolts"] = float(self.ui.txtNoBolts.text())
        outObj['Bolt']["No.Of Row"] = int(self.ui.txt_row.text())
        outObj['Bolt']["No.Of Column"] = int(self.ui.txt_col.text())
        outObj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txtPitch.text())
        outObj['Bolt']["Guage Distance (mm)"] = float(self.ui.txtGuage.text())
        outObj['Bolt']["End Distance (mm)"] = float(self.ui.txtEndDist.text())
        outObj['Bolt']["Edge Distance (mm)"] = float(self.ui.txtEdgeDist.text())

        return outObj

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def show_dialog(self):
        dialog = MyPopupDialog(self)
        dialog.show()

    def createDesignReport(self):
        self.show_dialog()

    def save_design(self, popup_summary):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/", "Html Files(*.html)")
        fileName = str(fileName + ".html")
        base, base1, base2, base3 = self.callFin2D_Drawing("All")
        commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5],
                                         self.alist[6], self.alist[7], self.alist[8], self.display, self.folder, base, base1, base2, base3)
        commLogicObj.call_designReport(fileName, popup_summary)

        QtGui.QMessageBox.about(self, 'Information', "Report Saved")

    # # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def save_log(self):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/LogMessages", "Text files (*.txt)")
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
        self.ui.combo_Beam.setCurrentIndex((0))
        self.ui.comboColSec.setCurrentIndex((0))
        self.ui.comboConnLoc.setCurrentIndex((0))
        self.ui.txtFu.clear()
        self.ui.txtFy.clear()

        self.ui.txtShear.clear()

        self.ui.comboDiameter.setCurrentIndex(0)
        self.ui.comboType.setCurrentIndex((0))
        self.ui.comboGrade.setCurrentIndex((0))

        self.ui.comboPlateThick_2.setItemText(0, "Select Plate thickness")
        self.ui.comboPlateThick_2.setCurrentIndex((0))
        self.ui.txtPlateLen.clear()
        self.ui.txtPlateWidth.clear()

        self.ui.comboWldSize.setItemText(0, "Select weld thickness")
        self.ui.comboWldSize.setCurrentIndex((0))

        ##### Output #######
        self.ui.txtShrCapacity.clear()
        self.ui.txtbearCapacity.clear()
        self.ui.txtBoltCapacity.clear()
        self.ui.txtNoBolts.clear()
        self.ui.txtboltgrpcapacity.clear()
        self.ui.txt_row.clear()
        self.ui.txt_col.clear()
        self.ui.txtPitch.clear()
        self.ui.txtGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()

        # self.ui.txtPlateThick.clear()
        self.ui.txtplate_ht.clear()
        self.ui.txtplate_width.clear()
        self.ui.txtExtMomnt.clear()
        self.ui.txtMomntCapacity.clear()

        # self.ui.txtWeldThick.clear()
        self.ui.txtResltShr.clear()
        self.ui.txtWeldStrng.clear()
        self.ui.textEdit.clear()

        #------ Erase Display
        self.display.EraseAll()

    def dockbtn_clicked(self, widget):

        '''(QWidget) -> None

        This method dock and undock widget(QdockWidget)
        '''

        flag = widget.isHidden()
        if(flag):

            widget.show()
        else:
            widget.hide()

    def combotype_currentindexchanged(self, index):

        '''(Number) -> None
        '''
        items = self.gradeType[str(index)]

        self.ui.comboGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))

        self.ui.comboGrade.addItems(strItems)

    def check_range(self, widget, lblwidget, minVal, maxVal):

        '''(QlineEdit, QLable, Number, Number)---> None
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr)
        if(val < minVal or val > maxVal):
            QtGui.QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s [cl 2.2.4.2]' % (minVal, maxVal))
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
        shear_capacity = resultObj['Bolt']['shearcapacity']
        self.ui.txtShrCapacity.setText(str(shear_capacity))

        bearing_capacity = resultObj['Bolt']['bearingcapacity']
        self.ui.txtbearCapacity.setText(str(bearing_capacity))

        bolt_capacity = resultObj['Bolt']['boltcapacity']
        self.ui.txtBoltCapacity.setText(str(bolt_capacity))

        no_ofbolts = resultObj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        # newly added field
        boltGrp_capacity = resultObj['Bolt']['boltgrpcapacity']
        self.ui.txtboltgrpcapacity.setText(str(boltGrp_capacity))

        no_ofrows = resultObj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))

        no_ofcol = resultObj['Bolt']['numofcol']
        self.ui.txt_col.setText(str(no_ofcol))

        pitch_dist = resultObj['Bolt']['pitch']
        self.ui.txtPitch.setText(str(pitch_dist))

        gauge_dist = resultObj['Bolt']['gauge']
        self.ui.txtGuage.setText(str(gauge_dist))

        end_dist = resultObj['Bolt']['enddist']
        self.ui.txtEndDist.setText(str(end_dist))

        edge_dist = resultObj['Bolt']['edge']
        self.ui.txtEdgeDist.setText(str(edge_dist))

        resultant_shear = resultObj['Weld']['resultantshear']
        self.ui.txtResltShr.setText(str(resultant_shear))

        weld_strength = resultObj['Weld']['weldstrength']
        self.ui.txtWeldStrng.setText(str(weld_strength))

        # Newly included fields
        plate_ht = resultObj['Plate']['height']
        self.ui.txtplate_ht.setText(str(plate_ht))

        plate_width = resultObj['Plate']['width']
        self.ui.txtplate_width.setText(str(plate_width))

        moment_demand = resultObj['Plate']['externalmoment']
        self.ui.txtExtMomnt.setText(str(moment_demand))

        moment_capacity = resultObj['Plate']['momentcapacity']
        self.ui.txtMomntCapacity.setText(str(moment_capacity))

    def displaylog_totextedit(self, commLogicObj):

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

    # QtViewer
    def init_display(self, backend_str=None, size=(1024, 768)):
        if os.name == 'nt':

            global display, start_display, app, _

            from OCC.Display.backend import get_loaded_backend
            lodedbkend = get_loaded_backend()
            from OCC.Display.backend import get_backend, have_backend
            from osdagMainSettings import backend_name
            if(not have_backend() and backend_name() == "pyqt4"):
                get_backend("qt-pyqt4")
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

        # self.setWindowTitle("Osdag-%s 3d viewer ('%s' backend)" % (VERSION, backend_name()))
        self.setWindowTitle("Osdag Finplate")
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")

        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display

        # background gradient
        display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        # display_2d.set_bg_gradient_color(255,255,255,255,255,255)
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

    def checkBeam_B(self):
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web":
            if self.ui.comboColSec.currentIndex() == 0:
                # QtGui.QMessageBox.about(self,"Information", "Please select column section")
                return
            column = self.ui.comboColSec.currentText()
            dictBeamData = self.fetchBeamPara()
            dictColData = self.fetchColumnPara()
            column_D = float(dictColData[QString("D")])
            column_T = float(dictColData[QString("T")])
            column_R1 = float(dictColData[QString("R1")])
            columnWebDepth = column_D - (2.0 * (column_T) + 2.0 * (10))
            beam_B = float(dictBeamData[QString("B")])

            if columnWebDepth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                self.disableViewButtons()
                QtGui.QMessageBox.about(self, 'Information', "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)
                self.enableViewButtons()
        elif loc == "Beam-Beam":
            dictSBeamData = self.fetchBeamPara()
            dictPBeamData = self.fetchColumnPara()
            PBeam_D = float(dictPBeamData[QString("D")])
            PBeam_T = float(dictPBeamData[QString("T")])
            PBeamWebDepth = PBeam_D - 2.0 * (PBeam_T)

            SBeam_D = float(dictSBeamData[QString("D")])

            if PBeamWebDepth <= SBeam_D:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information', "Secondary beam depth is higher than clear depth of primary beam web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)

    def validateInputsOnDesignBtn(self):

        if self.ui.comboConnLoc.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select connectivity")
        state = self.setimage_connection()
        if state is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web" or self.ui.comboConnLoc.currentText() == "Column flange-Beam web" :
                if self.ui.comboColSec.currentIndex() == 0:
                    QtGui.QMessageBox.about(self, "Information", "Please select column section")
                elif self.ui.combo_Beam.currentIndex() == 0:
                    QtGui.QMessageBox.about(self, "Information", "Please select beam section")
            else:
                if self.ui.comboColSec.currentIndex() == 0:
                    QtGui.QMessageBox.about(self, "Information", "Please select Primary beam  section")
                elif self.ui.combo_Beam.currentIndex() == 0:
                    QtGui.QMessageBox.about(self, "Information", "Please select Secondary beam  section")

        if self.ui.txtFu.text().isEmpty() or float(self.ui.txtFu.text()) == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Ultimate strength of  steel")

        elif self.ui.txtFy.text().isEmpty() or float(self.ui.txtFy.text()) == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Yeild  strength of  steel")

        elif self.ui.txtShear.text().isEmpty() or float(str(self.ui.txtShear.text())) == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Factored shear load")

        elif self.ui.comboDiameter.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Diameter of  bolt")

        elif self.ui.comboType.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Type of  bolt")

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    def boltHeadThick_Calculation(self, boltDia):
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
        boltHeadThick = {5: 4, 6: 5, 8: 6, 10: 7, 12: 8, 16: 10, 20: 12.5, 22: 14, 24: 15, 27: 17, 30: 18.7, 36: 22.5}
        return boltHeadThick[boltDia]

    def boltHeadDia_Calculation(self, boltDia):
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
        boltHeadDia = {5: 7, 6: 8, 8: 10, 10: 15, 12: 20, 16: 27, 20: 34, 22: 36, 24: 41, 27: 46, 30: 50, 36: 60}
        return boltHeadDia[boltDia]

    def boltLength_Calculation(self, boltDia):
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
        boltHeadDia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65, 36: 75}

        return boltHeadDia[boltDia]

    def nutThick_Calculation(self, boltDia):
        '''
        Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
        '''
        nutDia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23, 30: 25.35, 36: 30.65}

        return nutDia[boltDia]

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def call_3DModel(self, flag):
        self.commLogicObj.call_3DModel(flag)

    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam")

    def call_3DColumn(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column")

    def call_3DFinplate(self):
        '''
        Displaying FinPlate in 3D
        '''
        self.ui.chkBxFinplate.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxFinplate.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Finplate")

    def unchecked_allChkBox(self):
        '''
        This routine is responsible for unchecking all checkboxes in GUI
        '''

        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)

    def designParameters(self):
        '''
        This routine returns the neccessary design parameters.
        '''
        self.uiObj = self.getuser_inputs()
        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        loc = str(self.ui.comboConnLoc.currentText())
        component = "Model"
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        return [self.uiObj, dictbeamdata, dictcoldata, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T]

    def design_btnclicked(self):
        '''
        '''
        self.alist = self.designParameters()

        self.validateInputsOnDesignBtn()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self. unchecked_allChkBox()
        base = ''
        base_front = ''
        base_side = ''
        base_top = ''

        self.commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.display, self.folder, base, base_front, base_side, base_top) 

        self.resultObj = self.commLogicObj.call_finCalculation()
        d = self.resultObj[self.resultObj.keys()[0]]
        if len(str(d[d.keys()[0]])) == 0:
            self.ui.btn_CreateDesign.setEnabled(False)
        self.display_output(self.resultObj)
        self.displaylog_totextedit(self.commLogicObj)
        status = self.resultObj['Bolt']['status']

        self.commLogicObj.call_3DModel(status)


        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def create2Dcad(self):
        ''' Returns the 3D model of finplate depending upon component
        '''
        if self.commLogicObj.component == "Beam":
            final_model = self.commLogicObj.connectivityObj.get_beamModel()

        elif self.commLogicObj.component == "Column":
            final_model = self.commLogicObj.connectivityObj.columnModel

        elif self.commLogicObj.component == "Finplate":
            cadlist = [self.commLogicObj.connectivityObj.weldModelLeft,
                       self.commLogicObj.connectivityObj.weldModelRight,
                       self.commLogicObj.connectivityObj.plateModel,
                       self.commLogicObj.connectivityObj.nutBoltArray.getModels()]
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        else:
            cadlist = self.commLogicObj.connectivityObj.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

        return final_model

    # Export to IGS,STEP,STL,BREP

    def save3DcadImages(self):

        if self.fuse_model is None:
            self.fuse_model = self.create2Dcad()
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

            assert(status == IFSelect_RetDone)

        else:
            stl_writer = StlAPI_Writer()
            stl_writer.SetASCIIMode(True)
            stl_writer.Write(shape, fName)

        QtGui.QMessageBox.about(self, 'Information', "File saved")

    def callFin2D_Drawing(self, view):  # call2D_Drawing(self,view)

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        base = ''
        base_front = ''
        base_side = ''
        base_top = ''

        commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.display, self.folder, base, base_front, base_side, base_top)
        if view != 'All':
            fileName = QtGui.QFileDialog.getSaveFileName(self,
                                                         "Save SVG", str(self.folder) + '/untitled.svg',
                                                         "SVG files (*.svg)")
            fname = str(fileName)
        else:
            fname = ''
        base, base1, base2, base3 = commLogicObj.call2D_Drawing(view, fname, self.alist[3], self.folder)
        return base, base1, base2, base3
        # commLogicObj.call2D_Drawing(view,fname)

    def closeEvent(self, event):
        '''
        Closing finPlate window.
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

    def sample_report(self):
        url = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'Sample_Folder', 'Sample_Report', 'The_PyQt4_tutorial.pdf')
        webbrowser.open_new(r'file:///' + url)

    def sample_problem(self):
        webbrowser.open_new(r'file:///D:/EclipseWorkspace/OsdagLIVE/Sample_Folder/Sample_Problems/The_PyQt4_tutorial.pdf')

# ********************************************************************************************************************************************************


def set_osdaglogger():

    global logger
    if logger is None:

        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # create the logging file handler
    fh = logging.FileHandler("Connections/Shear/Finplate/fin.log", mode="a")

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


def launchFinPlateController(osdagMainWindow, folder):
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("Connections/Shear/Finplate/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Finplate/log.css"/>''')

    module_setup()
    window = MainController(folder)
    osdagMainWindow.hide()

    window.show()
    window.closed.connect(osdagMainWindow.show)


if __name__ == '__main__':

    # linking css to log file to display colour logs.
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("Connections/Shear/Finplate/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Finplate/log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    module_setup()
    window = MainController()
    window.show()
    sys.exit(app.exec_())





