'''
Created on 07-May-2015
comment

@author: aravind
'''
from getpass import getuser
import os.path
import pickle

from OCC import IGESControl
from OCC import VERSION, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from OCC.IFSelect import IFSelect_RetDone
from OCC.Interface import Interface_Static_SetCVal
from OCC.Quantity import Quantity_NOC_RED, Quantity_NOC_BLUE1, Quantity_NOC_SADDLEBROWN
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.StlAPI import StlAPI_Writer
from OCC.TopoDS import topods, TopoDS_Shape
from OCC.gp import gp_Pnt
from PyQt4.Qt import QPrinter, QDialog
from PyQt4.QtCore import QString, pyqtSignal
from PyQt4.QtGui import QWidget
from PyQt4.QtWebKit import *
import pdfkit
import svgwrite
import shutil
from ui_cleatAngle import Ui_MainWindow
from ISection import ISection
# from OCC.Display.qtDisplay import qtViewer3d
from angle import Angle
from beamWebBeamWebConnectivity import BeamWebBeamWeb
from bolt import Bolt
from cleatCalculation import cleatAngleConn
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from colWebBeamWebConnectivity import ColWebBeamWeb
from reportGenerator import *
from drawing2D import *
from model import *
from notch import Notch
from nut import Nut
from nutBoltPlacement import NutBoltArray
from ui_popUpWindow import Ui_Capacitydetals
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_HelpOsdag
from ui_tutorial import Ui_Tutorial
from utilities import osdagDisplayShape
from OCC.Display import OCCViewer
# from OCC.Display.backend import get_qt_modules
from macpath import basename
# from OCC.Display.backend import get_backend
# get_backend("qt-pyqt4")
# import OCC.Display.qtDisplay
# QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

# import OCC.Display.qtDisplay
# from Connections.Shear.cleatAngle.ui_popUpWindow import Ui_Capacitydetals
# Developed by aravind


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
        # return input_summary

    def getLogoFilePath(self, lblwidget):

        self.ui.lbl_browse.clear
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', " ", 'Images (*.png *.svg *.jpg)', None, QtGui.QFileDialog.DontUseNativeDialog)

        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

    def desired_location(self, filename):
        shutil.copyfile(filename, str(self.mainController.folder) + "/images_html/cmpylogoCleat.png")

    def saveUserProfile(self):
        inputData = self.getPopUpInputs()

        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Files', str(self.mainController.folder) + "/Profile", '*.txt')

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
        files_types = "All Files (*))"
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


class myDialog(QtGui.QDialog):
# (Ui_Capacitydetals):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Capacitydetals()
        self.ui.setupUi(self)
        self.setWindowTitle("Capacity Details")
        self.mainController = parent
        # web = QWebView()
        # uiObj = self.MainController().getuser_inputs()
        uiObj = self.mainController.getuser_inputs()
        x = cleatAngleConn(uiObj)
        # x = MainController().outputdict()
        # x = m.outputdict()

        self.ui.shear_b.setText(str(x['Bolt']['shearcapacity']))
        self.ui.bearing_b.setText(str(x['Bolt']['bearingcapacity']))
        self.ui.capacity_b.setText(str(x['Bolt']['boltcapacity']))
        self.ui.boltGrp_b.setText(str(x['Bolt']['boltgrpcapacity']))
        # Column
        self.ui.shear.setText(str(x['cleat']['shearcapacity']))
        self.ui.bearing.setText(str(x['cleat']['bearingcapacity']))
        self.ui.capacity.setText(str(x['cleat']['boltcapacity']))
        self.ui.boltGrp.setText(str(x['cleat']['boltgrpcapacity']))
        # Cleat
        self.ui.mDemand.setText(str(x['cleat']['externalmoment']))
        self.ui.mCapacity.setText(str(x['cleat']['momentcapacity']))



class MainController(QtGui.QMainWindow):

    closed = pyqtSignal()

    def __init__(self, folder):
        QtGui.QMainWindow.__init__(self)
#         QtGui.QDialog.__init__(self, parent)
#         self.web = web
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder

        self.ui.combo_Beam.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())
        self.ui.comboCleatSection.addItems(get_anglecombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Select Bolt Type': '',
                          'HSFG': [8.8, 10.8],
                          'Black Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 12.9]}
        self.ui.comboBoltType.addItems(self.gradeType.keys())
        self.ui.comboBoltType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboBoltType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()
        # Adding GUI changes for beam to beam connection
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convertColComboToBeam)
        #############################################################################################################
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        # self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock)) #USE WHEN ui_cleatAngle.py is used(btnOutput = toolButton)

        self.ui.toolButton.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.btn_front.clicked.connect(lambda: self.call_2d_Drawing("Front"))
        self.ui.btn_top.clicked.connect(lambda: self.call_2d_Drawing("Top"))
        self.ui.btn_side.clicked.connect(lambda: self.call_2d_Drawing("Side"))

        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        # self.ui.chkBxFinplate.clicked.connect(self.call_3DCleatAngle)
        self.ui.checkBoxCleat.clicked.connect(self.call_3DCleatAngle)

        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
        self.ui.txtInputCleatHeight.setValidator(dbl_validator)
        self.ui.txtInputCleatHeight.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)

        minfuVal = 290
        maxfuVal = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu, self.ui.lbl_fu, minfuVal, maxfuVal))

        minfyVal = 165
        maxfyVal = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy, self.ui.lbl_fy, minfyVal, maxfyVal))

        self.ui.actionCreate_design_report.triggered.connect(self.createDesignReport)
        self.ui.actionSave_log_message.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_CAD_image.triggered.connect(self.save2DcadImages)
        self.ui.actionSave_Front_View.triggered.connect(lambda: self.call_2d_Drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.call_2d_Drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.call_2d_Drawing("Top"))
        self.ui.actionPan.triggered.connect(self.call_Pannig)

        self.ui.actionShow_beam.triggered.connect(self.call_3DBeam)
        self.ui.actionShow_column.triggered.connect(self.call_3DColumn)
        self.ui.actionShow_cleat_angle.triggered.connect(self.call_3DCleatAngle)
        self.ui.actionShow_all.triggered.connect(lambda: self.call_3DModel(True))
        self.ui.actionChange_background.triggered.connect(self.showColorDialog)
        ############################### MARCH_14 #############################
        # populate cleat section and secondary beam according to user input

        self.ui.comboColSec.currentIndexChanged[int].connect(lambda: self.fillCleatSectionCombo())
        self.ui.combo_Beam.currentIndexChanged[str].connect(self.checkBeam_B)
        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkBeam_B)
#         self.ui.txtInputCleatHeight.currentText.connect(self.checkCleatHeight())
#         cleatHeight = self.ui.txtInputCleatHeight.currentText()
#         if cleatHeight != 0:
#             self.
        self.ui.txtInputCleatHeight.editingFinished.connect(lambda: self.checkCleatHeight(self.ui.txtInputCleatHeight))

        ######################################################################################
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.createDesignReport)  # Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        #################################################################
        self.ui.btn_capacity.clicked.connect(self.showButton_clicked)
        # self.ui.actionCreate_design_report.triggered.connect(self.createDesignReport)

        #################################################################
        # Saving and Restoring the finPlate window state.
        # self.retrieve_prevstate()
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

# ************************************** Osdag logo for html***************************************************************************************************
        self.ui.btn_Design.clicked.connect(self.osdag_header)

# ************************************ Help button *******************************************************************************
        self.ui.actionAbout_Osdag.triggered.connect(self.open_osdag)
        self.ui.actionVideo_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_Reports.triggered.connect(self.sample_report)
        self.ui.actionSample_Problems.triggered.connect(self.sample_problem)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        self.resultObj = None
        self.uiObj = None

    def osdag_header(self):
        image_path = "ResourceFiles/Osdag_header.png"
        self.store_osdagheader(image_path)

    def store_osdagheader(self, image_path):
        shutil.copyfile(image_path, str(self.folder) + "/images_html/Osdag_header.png")

    def show_capacityDialog(self):
        self.dialog = myDialog(self)
        self.dialog.show()

    def showButton_clicked(self):
        self.show_capacityDialog()

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

    def fetchAnglePara(self):
        angle_sec = self.ui.comboCleatSection.currentText()
        dictangledata = get_angledata(angle_sec)
        return dictangledata

    def convertColComboToBeam(self):

        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.beamSection_lbl.setText(" Secondary beam *")
            self.ui.columnSection_lbl.setText("Primary beam *")

            self.ui.chkBxBeam.setText("SBeam")
            self.ui.chkBxBeam.setToolTip("Secondary  beam")
            self.ui.chkBxCol.setText("PBeam")
            self.ui.chkBxCol.setToolTip("Primary beam")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Primary beam")
            self.ui.outputBoltLbl.setText("Secondary beam")
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)

            # self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_beamcombolist())

# ---------------------------------------- Users input-----------------------------------------------------------------------------
            self.ui.comboColSec.setCurrentIndex(0)
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboBoltType.setCurrentIndex(0)
            self.ui.comboBoltGrade.setCurrentIndex(0)
            self.ui.comboCleatSection.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtInputCleatHeight.clear()

# ---------------------------------------- Output-----------------------------------------------------------------------------
            self.ui.txtNoBolts_c.clear()
            self.ui.txt_row_c.clear()
            self.ui.txt_column_c.clear()
            self.ui.txtBeamPitch_c.clear()
            self.ui.txtBeamGuage_c.clear()
            self.ui.txtEndDist_c.clear()
            self.ui.txtEdgeDist_c.clear()
            self.ui.txtNoBolts.clear()
            self.ui.txt_row.clear()
            self.ui.txt_column.clear()
            self.ui.txtBeamPitch.clear()
            self.ui.txtBeamGuage.clear()
            self.ui.txtEndDist.clear()
            self.ui.txtEdgeDist.clear()
            self.ui.outputCleatHeight.clear()

        elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":

            self.ui.columnSection_lbl.setText("Column Section *")
            self.ui.beamSection_lbl.setText("Beam section *")

            self.ui.chkBxBeam.setText("Beam")
            self.ui.chkBxBeam.setToolTip("Beam only")
            self.ui.chkBxCol.setText("Column")
            self.ui.chkBxCol.setToolTip("Column only")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Column")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)
            self.ui.outputBoltLbl.setText("Beam")

            # self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_columncombolist())

# ---------------------------------------- Users input-----------------------------------------------------------------------------
            self.ui.comboColSec.setCurrentIndex(0)
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboBoltType.setCurrentIndex(0)
            self.ui.comboBoltGrade.setCurrentIndex(0)
            self.ui.comboCleatSection.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtInputCleatHeight.clear()

# ---------------------------------------- Output-----------------------------------------------------------------------------
            self.ui.txtNoBolts_c.clear()
            self.ui.txt_row_c.clear()
            self.ui.txt_column_c.clear()
            self.ui.txtBeamPitch_c.clear()
            self.ui.txtBeamGuage_c.clear()
            self.ui.txtEndDist_c.clear()
            self.ui.txtEdgeDist_c.clear()
            self.ui.txtNoBolts.clear()
            self.ui.txt_row.clear()
            self.ui.txt_column.clear()
            self.ui.txtBeamPitch.clear()
            self.ui.txtBeamGuage.clear()
            self.ui.txtEndDist.clear()
            self.ui.txtEdgeDist.clear()
            self.ui.outputCleatHeight.clear()

    def fillCleatSectionCombo(self):
        '''Populates the cleat section on the basis  beam section and column section
        '''

        if self.ui.combo_Beam.currentText() == "Select Designation" or self.ui.comboColSec.currentText() == "Select Column":
            self.ui.comboCleatSection.setCurrentIndex(0)
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web" or "Column flange-Beam web":
            loc = self.ui.comboConnLoc.currentText()
            dictbeamdata = self.fetchBeamPara()
            dictcoldata = self.fetchColumnPara()
            angleList = get_anglecombolist()
            col_R1 = float(dictcoldata[QString("R1")])
            col_D = float(dictcoldata[QString("D")])
            col_B = float(dictcoldata[QString("B")])
            col_T = float(dictcoldata[QString("T")])
            beam_tw = float(dictbeamdata[QString("tw")])

            if loc == "Column web-Beam web":
                colWeb = col_D - 2 * (col_T + col_R1)
            elif loc == "Column flange-Beam web":
                colWeb = col_B
            newlist = ['Select Cleat']

            for ele in angleList[1:]:
                angle_sec = QtCore.QString(str(ele))
                dictAngleData = get_angledata(angle_sec)
                cleatLegsize_B = float(dictAngleData[QtCore.QString('B')])
                conLegsize = 2 * cleatLegsize_B + beam_tw
                space = colWeb - conLegsize
                if space > 0:
                    newlist.append(str(ele))
                else:
                    break

            self.ui.comboCleatSection.blockSignals(True)

            self.ui.comboCleatSection.clear()
            for i in newlist[:]:
                self.ui.comboCleatSection.addItem(str(i))

            self.ui.comboCleatSection.setCurrentIndex(-1)

            self.ui.comboCleatSection.blockSignals(False)
            self.ui.comboCleatSection.setCurrentIndex(0)
        else:
            pass

    def checkBeam_B(self):
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web":

            column = self.ui.comboColSec.currentText()

            dictBeamData = self.fetchBeamPara()
            dictColData = self.fetchColumnPara()
            column_D = float(dictColData[QString("D")])
            column_T = float(dictColData[QString("T")])
            column_R1 = float(dictColData[QString("R1")])
            columnWebDepth = column_D - 2.0 * (column_T)

            beam_B = float(dictBeamData[QString('B')])

            if columnWebDepth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information', "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)

        elif loc == "Beam-Beam":

            primaryBeam = self.ui.comboColSec.currentText()
            dictSBeamData = self.fetchBeamPara()
            dictPBeamData = self.fetchColumnPara()
            PBeam_D = float(dictPBeamData[QString("D")])
            PBeam_T = float(dictPBeamData[QString("T")])
            PBeamWebDepth = PBeam_D - 2.0 * (PBeam_T)

            SBeam_D = float(dictSBeamData[QString("D")])

            if PBeamWebDepth <= SBeam_D:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information',
                                        "Secondary beam depth is higher than clear depth of primary beam web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)

    def checkCleatHeight(self, widget):
        loc = self.ui.comboConnLoc.currentText()
        cleatHeight = widget.text()
        cleatHeight = float(cleatHeight) 
        if cleatHeight == 0:
            self.ui.btn_Design.setDisabled(False)
        else:

            dictBeamData = self.fetchBeamPara()
            dictColumnData = self.fetchColumnPara()
            col_T = float(dictColumnData[QString('T')])
            col_R1 = float(dictColumnData[QString('R1')])
            beam_D = float(dictBeamData[QString('D')])
            beam_T = float(dictBeamData[QString('T')])
            beam_R1 = float(dictBeamData[QString('R1')])
            clearDepth = 0.0
            minCleatHeight = 0.6 * beam_D
            if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                clearDepth = beam_D - 2 * (beam_T + beam_R1 + 5)
            else:
                clearDepth = beam_D - (beam_R1 + beam_T + col_R1 + col_T)
            if clearDepth < cleatHeight or cleatHeight < minCleatHeight:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information',
                                        "Height of the Cleat Angle should be in between %s -%s mm" % (int(minCleatHeight), int(clearDepth)))
            else:
                self.ui.btn_Design.setDisabled(False)

    def showFontDialogue(self):

        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)

    def showColorDialog(self):

        col = QtGui.QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

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

        # self.ui.actionShow_all.setEnabled(False)
        # self.ui.actionSave_3D_model_as.setEnabled(False)
        # self.ui.actionSave_CAD_image.setEnabled(False)
        # self.ui.actionSave_Front_View.setEnabled(False)
        # self.ui.actionSave_Top_View.setEnabled(False)
        # self.ui.actionSave_Side_View.setEnabled(False)
        # self.ui.actionSave_log_message.setEnabled(False)
        # self.ui.actionCreate_design_report.setEnabled(False)
        # self.ui.actionSave_design.setEnabled(False)
        # self.ui.actionZoom_in.setEnabled(False)
        # self.ui.actionZoom_out.setEnabled(False)
        # self.ui.actionRotate_3D_model.setEnabled(False)
        # self.ui.actionShow_beam.setEnabled(False)
        # self.ui.actionShow_column.setEnabled(False)
        # self.ui.actionShow_cleat_angle.setEnabled(False)
        self.ui.menubar.setEnabled(False)

        self.ui.btn_capacity.setEnabled(False)
        self.ui.btn_SaveMessages.setEnabled(False)
        self.ui.btn_CreateDesign.setEnabled(False)

        self.ui.btn_front.setEnabled(False)

        self.ui.btn_top.setEnabled(False)
        self.ui.btn_side.setEnabled(False)

        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.checkBoxCleat.setEnabled(False)

    def enableViewButtons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_capacity.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)

        self.ui.btn_front.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn_side.setEnabled(True)

        self.ui.menubar.setEnabled(True)

        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.checkBoxCleat.setEnabled(True)

    def unchecked_allChkBox(self):

        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)

    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if(uiObj is not None):

            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))

            if uiObj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.beamSection_lbl.setText('Secondary beam *')
                self.ui.columnSection_lbl.setText('Primary beam *')
                self.ui.comboColSec.addItems(get_beamcombolist())

            self.ui.combo_Beam.setCurrentIndex(self.ui.combo_Beam.findText(uiObj['Member']['BeamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['ColumSection']))

            self.ui.txtFu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(uiObj['Member']['fy (MPa)']))

            self.ui.txtShear.setText(str(uiObj['Load']['ShearForce (kN)']))

            self.ui.comboDiameter.setCurrentIndex(self.ui.comboDiameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            comboTypeIndex = self.ui.comboBoltType.findText(str(uiObj['Bolt']['Type']))
            self.ui.comboBoltType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))

            prevValue = str(uiObj['Bolt']['Grade'])

            comboGradeIndex = self.ui.comboBoltGrade.findText(prevValue)

            self.ui.comboBoltGrade.setCurrentIndex(comboGradeIndex)

            self.ui.txtInputCleatHeight.setText(str(uiObj['cleat']['Height (mm)']))
            self.ui.comboCleatSection.setCurrentIndex(self.ui.comboCleatSection.findText(str(uiObj['cleat']['section'])))

    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web":

            # pixmap = QtGui.QPixmap(":/newPrefix/images/beam2.jpg")
            pixmap = QtGui.QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            # self.ui.lbl_connectivity.show()
        elif(loc == "Column web-Beam web"):
            # picmap = QtGui.QPixmap(":/newPrefix/images/beam.jpg")
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
        '''(nothing) -> Dictionary
        Returns the dictionary object with the user input fields for designing cleat angle connection
        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        uiObj["Bolt"]["Grade"] = float(self.ui.comboBoltGrade.currentText())  
        # uiObj["Bolt"]["Grade"] = 8.8
        uiObj["Bolt"]["Type"] = str(self.ui.comboBoltType.currentText())

        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        uiObj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiObj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]

        uiObj['cleat'] = {}
        uiObj['cleat']['section'] = str(self.ui.comboCleatSection.currentText())
        uiObj['cleat']['Height (mm)'] = float(self.ui.txtInputCleatHeight.text().toInt()[0])  # changes the label length to height 

        uiObj['Load'] = {}
        # uiObj['Load']['ShearForce (kN)'] = float(self.ui.txtShear.text().toInt()[0])
        uiObj['Load']['ShearForce (kN)'] = float(self.ui.txtShear.text())

        return uiObj

    def save_inputs(self, uiObj):
        '''
        (Dictionary)--> None
        '''
        inputFile = QtCore.QFile('saveINPUTS.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        # yaml.dump(uiObj, inputFile,allow_unicode=True, default_flow_style = False)
        pickle.dump(uiObj, inputFile)

    def get_prevstate(self):
        '''
        '''
        fileName = 'saveINPUTS.txt'

        if os.path.isfile(fileName):
            fileObject = open(fileName, 'r')
            uiObj = pickle.load(fileObject)
            return uiObj
        else:
            return None

    def outputdict(self):

        ''' Returns the output of design in dictionary object.
        '''

        uiObj = self.getuser_inputs()
        outputobj = cleatAngleConn(uiObj)
        return outputobj

    def show_dialog(self):

        dialog = MyPopupDialog(self)
        dialog.show()

    def createDesignReport(self):

        self.show_dialog()

    def save_design(self, popup_summary):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/", "Html Files (*.html)")
        fileName = str(fileName)
        base, base_front, base_top, base_side = self.call_2d_Drawing("All")
        # self.outdict = self.resultObj#self.outputdict()

        self.inputdict = self.getuser_inputs()  # self.getuser_inputss()
        self.outdict = cleatAngleConn(self.inputdict)
        dictBeamData = self.fetchBeamPara()

        dictColData = self.fetchColumnPara()
        dictCleatData = self.fetchAnglePara()
        save_html(self.outdict, self.inputdict, dictBeamData, dictColData , dictCleatData, popup_summary, fileName, self.folder, base, base_front, base_top, base_side)

        # path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        # options = {
        #             'margin-bottom': '10mm',
        #             'footer-right': '[page]'
        #             }
        # pdfkit.from_file(fileName,'Workspace\css\cleatreport.pdf', configuration=config, options=options) 

        QtGui.QMessageBox.about(self, 'Information', "Report Saved")

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def save_log(self):

        fileName, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/Logmessages", "Text files (*.txt)")
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

        # self.setCurrentFile(fileName);
        # QtGui.QMessageBox.about(self,'Information',"File saved")

    ###########################################################################################################################
        # def save_yaml(self,outObj,uiObj):
        #     '''(dictiionary,dictionary) -> NoneType
        #     Saving input and output to file in following format.
        #     Bolt:
        #       diameter: 6
        #       grade: 8.800000190734863
        #       type: HSFG
        #     Load:
        #       shearForce: 100

        #     '''
        #     newDict = {"INPUT": uiObj, "OUTPUT": outObj}
        #     fileName = QtGui.QFileDialog.getSaveFileName(self,"Save File As","output/SaveDesign","Text File (*.txt)")
        #     f = open(fileName,'w')
        #     yaml.dump(newDict,f,allow_unicode=True, default_flow_style=False)

        # return self.save_file(fileName+".txt")
        # QtGui.QMessageBox.about(self,'Information',"File saved")

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
        self.ui.comboBoltType.setCurrentIndex((0))
        self.ui.comboBoltGrade.setCurrentIndex((0))

        self.ui.comboCleatSection.setCurrentIndex((0))
        self.ui.txtInputCleatHeight.clear()
        # self.ui.txtPlateWidth.clear()
        # self.ui.comboWldSize.setCurrentIndex((0))

        # ----------------------------------------------- Output ------------------------------------------------------------------
        # self.ui.txtShrCapacity.clear()
        # self.ui.txtbearCapacity.clear()
        # self.ui.txtBoltCapacity.clear()
        self.ui.txtNoBolts.clear()
        # self.ui.txtBoltGrpCapacity.clear()
        self.ui.txt_row.clear()
        self.ui.txt_column.clear()
        self.ui.txtBeamPitch.clear()
        self.ui.txtBeamGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()

        # column
        self.ui.txtNoBolts_c.clear()
        self.ui.txt_row_c.clear()
        self.ui.txt_column_c.clear()
        self.ui.txtBeamPitch_c.clear()
        self.ui.txtBeamGuage_c.clear()
        self.ui.txtEndDist_c.clear()
        self.ui.txtEdgeDist_c.clear()

        # self.ui.txtPlateThick.clear()
        self.ui.outputCleatHeight.clear()
        # self.ui.txtplate_width.clear()
        # self.ui.txtExtMomnt.clear()
        # self.ui.txtMomntCapacity.clear()
        # self.ui.txtWeldThick.clear()
        # self.ui.txtResltShr.clear()
        # self.ui.txtWeldStrng.clear()
        self.ui.textEdit.clear()

        # ---------------------------------- Erase Display ------------------------------------------------------------------
        self.display.EraseAll()

    def dockbtn_clicked(self, widget):

        '''(QWidget) -> NoneType
        This method dock and undock widget(QdockWidget)
        '''
        flag = widget.isHidden()
        if(flag):

            widget.show()
        else:
            widget.hide()

    def combotype_currentindexchanged(self, index):

        '''(Number) -> NoneType
        '''
        items = self.gradeType[str(index)]

        self.ui.comboBoltGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))

        self.ui.comboBoltGrade.addItems(strItems)

    def check_range(self, widget, lblwidget, minVal, maxVal):

        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr)
        if(val < minVal or val > maxVal):
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
        shear_capacity = resultObj['Bolt']['shearcapacity']

        # self.uiPopUp.lineEdit_companyName.setText(str(shear_capacity))

        bearing_capacity = resultObj['Bolt']['bearingcapacity']
        # self.ui.txtbearCapacity.setText(str(bearing_capacity))

        bolt_capacity = resultObj['Bolt']['boltcapacity']
        # self.ui.txtBoltCapacity.setText(str(bolt_capacity))

        no_ofbolts = resultObj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        # newly added field
        boltGrp_capacity = resultObj['Bolt']['boltgrpcapacity']
        # self.ui.txtBoltGrpCapacity.setText(str(boltGrp_capacity))

        no_ofrows = resultObj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))

        no_ofcol = resultObj['Bolt']['numofcol']
        self.ui.txt_column.setText(str(no_ofcol))

        pitch_dist = resultObj['Bolt']['pitch']
        self.ui.txtBeamPitch.setText(str(pitch_dist))

        gauge_dist = resultObj['Bolt']['gauge']
        self.ui.txtBeamGuage.setText(str(gauge_dist))

        end_dist = resultObj['Bolt']['edge']
        self.ui.txtEndDist.setText(str(end_dist))

        edge_dist = resultObj['Bolt']['enddist']
        self.ui.txtEdgeDist.setText(str(edge_dist))
        # column
        c_noOfBolts = resultObj['cleat']['numofbolts']
        self.ui.txtNoBolts_c.setText(str(c_noOfBolts))
        cno_ofrows = resultObj['cleat']['numofrow']
        self.ui.txt_row_c.setText(str(cno_ofrows))

        no_ofcol = resultObj['cleat']['numofcol']
        self.ui.txt_column_c.setText(str(no_ofcol))

        pitch_dist = resultObj['cleat']['pitch']
        self.ui.txtBeamPitch_c.setText(str(pitch_dist))

        gauge_dist = resultObj['cleat']['guage']
        self.ui.txtBeamGuage_c.setText(str(gauge_dist))

        end_dist = resultObj['cleat']['edge']
        self.ui.txtEndDist_c.setText(str(end_dist))

        edge_dist = resultObj['cleat']['end']
        self.ui.txtEdgeDist_c.setText(str(edge_dist))

        # Newly included fields
        cleat_ht = resultObj['cleat']['height']
        self.ui.outputCleatHeight.setText(str(cleat_ht))

        # plate_width = resultObj['Cleat']['width']
        # self.ui.txtplate_width.setText(str(plate_width))

        moment_demand = resultObj['cleat']['externalmoment']
        # self.ui.txtExtMoment.setText(str(moment_demand))

        moment_capacity = resultObj['cleat']['momentcapacity']
        # self.ui.txtMomntCapacity.setText(str(moment_capacity))

    def displaylog_totextedit(self):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''
        afile = QtCore.QFile('Connections/Shear/cleatAngle/fin.log')

        if not afile.open(QtCore.QIODevice.ReadOnly):  # ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())

        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscrollBar = self.ui.textEdit.verticalScrollBar()
        vscrollBar.setValue(vscrollBar.maximum())
        afile.close()

    def get_backend(self):
        """
        loads a backend
        backends are loaded in order of preference
        since python comes with Tk included, but that PySide or PyQt4
        is much preferred
        """
        # try:
        #     from PySide import QtCore, QtGui
        #     return 'pyside'
        # except:
        #     pass
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

        self.setWindowTitle("Osdag Cleat Angle")
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")
        # self.ui.mytabWidget.addTab(self.ui.model2dTab,"")

        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display
        # display_2d = self.ui.model2dTab._display
        # background gradient
        display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        # display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        # display black trihedron
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

    def display3Dmodel(self, component):
        self.display.EraseAll()
        self.display.SetModeShaded()
        display.DisableAntiAliasing()
#         self.display.set_bg_gradient_color(23,1,32,23,1,32)
        self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
#         self.display.set_bg_gradient_color(28,9,99,252,243,235)
        self.display.View_Front()
        self.display.View_Iso()
        self.display.FitAll()
        if component == "Column":
            osdagDisplayShape(self.display, self.connectivity.get_columnModel(), update=True)
        elif component == "Beam":
            osdagDisplayShape(self.display, self.connectivity.get_beamModel(), material=Graphic3d_NOT_2D_ALUMINUM, update=True)
            # osdagDisplayShape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif component == "cleatAngle":

        # osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
        # osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
            osdagDisplayShape(self.display, self.connectivity.angleLeftModel, color='blue', update=True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
            # self.display.DisplayShape(self.connectivity.nutBoltArray.getModels(), color = Quantity_NOC_SADDLEBROWN, update=True)
        elif component == "Model":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM, update=True)
            # osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
            # osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivity.angleModel, color='blue', update=True)
            osdagDisplayShape(self.display, self.connectivity.angleLeftModel, color='blue', update=True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
            # self.display.DisplayShape(self.connectivity.nutBoltArray.getModels(), color = Quantity_NOC_SADDLEBROWN, update=True)

    def validateInputsOnDesignBtn(self):

        if self.ui.comboConnLoc.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select connectivity")
        state = self.setimage_connection()
        if state is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web" or self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
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

        elif self.ui.comboBoltType.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Type of  bolt")
        elif self.ui.comboCleatSection.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Cleat angle")

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

    def create3DBeamWebBeamWeb(self):
        '''
        creating 3d cad model with beam web beam web
        '''
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)

        #################################### PRIMARY BEAM PARAMETERS ########################################################

        dictbeamdata = self.fetchColumnPara()
        pBeam_D = int(dictbeamdata[QString("D")])
        pBeam_B = int(dictbeamdata[QString("B")])
        pBeam_tw = float(dictbeamdata[QString("tw")])
        pBeam_T = float(dictbeamdata[QString("T")])
        pBeam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        pBeam_R1 = float(dictbeamdata[QString("R1")])
        pBeam_R2 = float(dictbeamdata[QString("R2")])
        pBeam_length = 800.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B=pBeam_B, T=pBeam_T, D=pBeam_D, t=pBeam_tw,
                          R1=pBeam_R1, R2=pBeam_R2, alpha=pBeam_alpha,
                          length=pBeam_length, notchObj=None)

        ##### SECONDARY BEAM PARAMETERS ######
        dictbeamdata2 = self.fetchBeamPara()

        sBeam_D = int(dictbeamdata2[QString("D")])
        sBeam_B = int(dictbeamdata2[QString("B")])
        sBeam_tw = float(dictbeamdata2[QString("tw")])
        sBeam_T = float(dictbeamdata2[QString("T")])
        sBeam_alpha = float(dictbeamdata2[QString("FlangeSlope")])
        sBeam_R1 = float(dictbeamdata2[QString("R1")])
        sBeam_R2 = float(dictbeamdata2[QString("R2")])

        # ---------------------------- Notch dimensions -----------------------------------------------------------------
        notchObj = Notch(R1=pBeam_R1, height=(pBeam_T + pBeam_R1), width=((pBeam_B - (pBeam_tw + 40)) / 2.0 + 10), length=sBeam_B)
        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B=sBeam_B, T=sBeam_T, D=sBeam_D,
                        t=sBeam_tw, R1=sBeam_R1, R2=sBeam_R2,
                        alpha=sBeam_alpha, length=500, notchObj=notchObj)

        ############################################## WELD,PLATE,BOLT AND NUT PARAMETERS #######################################

        dictAngleData = self.fetchAnglePara()
        cleat_length = resultObj['cleat']['height']

        cleat_thick = float(dictAngleData[QString("t")])
        angle_A = int(dictAngleData[QString("A")])
        angle_B = int(dictAngleData[QString("B")])
        # cleat_thick = 10
        # angle_A = 120
        # angle_B = 90
        # bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        # bolt_r = bolt_dia/2
        # bolt_R = bolt_r + 7
        # nut_R = bolt_R
        # bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3750(1985)
        # nut_T = 12.0 # minimum nut thickness As per Indian Standard
        # nut_Ht = 12.2 #

        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150
        # plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = sBeam_tw + 2 * cleat_thick + nut_T
        cgap = pBeam_tw + cleat_thick + nut_T

        nutBoltArray = NutBoltArray(resultObj, nut, bolt, gap, cgap)

        beamwebconn = BeamWebBeamWeb(column, beam, notchObj, angle, nutBoltArray)
        beamwebconn.create_3dmodel()

        return beamwebconn

    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web
        '''
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)

        dictbeamdata = self.fetchBeamPara()
        ################################### BEAM PARAMETERS ####################################################################
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
                        length=beam_length, notchObj=None)

        ##################################################### COLUMN PARAMETERS #################################################
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
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)
        ########################################### WELD,PLATE,BOLT AND NUT PARAMETERS ############################################
        dictAngleData = self.fetchAnglePara()
        cleat_length = resultObj['cleat']['height']

        cleat_thick = float(dictAngleData[QString("t")])
        angle_A = int(dictAngleData[QString("A")])
        angle_B = int(dictAngleData[QString("B")])
        # cleat_thick = 10
        # angle_A = 120
        # angle_B = 90
        # bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        # bolt_r = bolt_dia/2
        # bolt_R = bolt_r + 7
        # nut_R = bolt_R
        # bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3750(1985)
        # nut_T = 12.0 # minimum nut thickness As per Indian Standard
        # nut_Ht = 12.2 #
        ####################################################################################################################
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150
        #####################################################################################################################
        # plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = beam_tw + 2 * cleat_thick + nut_T
        cgap = column_tw + cleat_thick + nut_T

        nutBoltArray = NutBoltArray(resultObj, nut, bolt, gap, cgap)

        colwebconn = ColWebBeamWeb(column, beam, angle, nutBoltArray)
        colwebconn.create_3dmodel()

        return colwebconn

    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection
        '''
        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)

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
                        length=beam_length, notchObj=None)

        ############################################### COLUMN PARAMETERS ##################################################
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
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notchObj=None)

        ################################ Cleat,BOLT AND NUT PARAMETERS ###########################################################
        dictAngleData = self.fetchAnglePara()
        cleat_length = resultObj['cleat']['height']

        cleat_thick = float(dictAngleData[QString("t")])
        angle_A = int(dictAngleData[QString("A")])
        angle_B = int(dictAngleData[QString("B")])
#         cleat_thick = 10
#         angle_A = 120
#         angle_B = 90

#         bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
#         bolt_r = bolt_dia/2
#         bolt_R = bolt_r + 7
#         nut_R = bolt_R
#         bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
#         bolt_Ht = 50.0 # minimum bolt length as per Indian Standard
#         nut_T = 12.0 # minimum nut thickness As per Indian Standard
#         nut_Ht = 12.2
    ######################################################################################################
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150

    ##########################################################################################################

        # plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = beam_tw + 2 * cleat_thick + nut_T
        cgap = column_T + cleat_thick + nut_T

        nutBoltArray = NutBoltArray(resultObj, nut, bolt, gap, cgap)

        colflangeconn = ColFlangeBeamWeb(column, beam, angle, nutBoltArray)
        colflangeconn.create_3dmodel()
        return colflangeconn

    def call_3DModel(self, flag):
        # self.ui.btnSvgSave.setEnabled(True)
        self.ui.btn3D.setChecked(QtCore.Qt.Checked)
        if self.ui.btn3D.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        if flag is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
                # self.create3DColWebBeamWeb()
                self.connectivity = self.create3DColWebBeamWeb()
                self.fuse_model = None
            elif self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create3DColFlangeBeamWeb()
                self.fuse_model = None

            else:
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create3DBeamWebBeamWeb()
                self.fuse_model = None

            self.display3Dmodel("Model")
            # beamOrigin = self.connectivity.beam.secOrigin + self.connectivity.beam.t/2 * (-self.connectivity.beam.uDir)
            # gpBeamOrigin = getGpPt(beamOrigin)
            # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
            # self.display.DisplayShape(my_sphere2,color = 'red',update = True)
            # beamOrigin = self.connectivity.beam.secOrigin
            # gpBeamOrigin = getGpPt(beamOrigin)
            # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
            # self.display.DisplayShape(my_sphere2,color = 'blue',update = True)
            # plateOrigin =  (self.connectivity.plate.secOrigin + self.connectivity.plate.T/2.0 *(self.connectivity.plate.uDir)+ self.connectivity.weldLeft.L/2.0
            # * (self.connectivity.plate.vDir) + self.connectivity.plate.T * (-self.connectivity.weldLeft.uDir))
            # gpPntplateOrigin=  getGpPt(plateOrigin)
            # my_sphere = BRepPrimAPI_MakeSphere(gpPntplateOrigin,2).Shape()
            # self.display.DisplayShape(my_sphere,update=True)

        else:
            self.display.EraseAll()
            # self.display.DisplayMessage(gp_Pnt(1000,0,400),"Sorry, can not create 3D model",height = 23.0)

    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display3Dmodel("Beam")

    def call_3DColumn(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.display3Dmodel("Column")

    def call_3DCleatAngle(self):
        '''Displaying FinPlate in 3D
        '''
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Checked)
        if self.ui.checkBoxCleat.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display3Dmodel("cleatAngle")

    def design_btnclicked(self):
        '''
        '''
        self.validateInputsOnDesignBtn()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self. unchecked_allChkBox()

        # self.set_designlogger()
        # Getting User Inputs.
        self.uiObj = self.getuser_inputs()
        self.save_inputs(self.uiObj)

        # FinPlate Design Calculations.
        self.resultObj = cleatAngleConn(self.uiObj)
        d = self.resultObj[self.resultObj.keys()[0]]
        if len(str(d[d.keys()[0]])) == 0:
            self.ui.btn_CreateDesign.setEnabled(False)
        # self.outputdict()

        # Displaying Design Calculations To Output Window
        self.display_output(self.resultObj)

        # Displaying Messages related to FinPlate Design.
        self.displaylog_totextedit()

        # Displaying 3D Cad model
        status = self.resultObj['Bolt']['status']
        self.call_3DModel(status)

    def create2Dcad(self, connectivity):
        ''' Returns the fuse model of cleat angle
        '''
        cadlist = self.connectivity.get_models()
        final_model = cadlist[0]
        for model in cadlist[1:]:
            final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        return final_model

    # Export to IGS,STEP,STL,BREP

    def save3DcadImages(self):
        if self.connectivity is None:
            self.connectivity = self.create3DColWebBeamWeb()
        if self.fuse_model is None:
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

            assert(status == IFSelect_RetDone)

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

    def callDesired_View(self, fileName, view, base_front, base_top, base_side):

        self. unchecked_allChkBox()

        uiObj = self.getuser_inputs()
        resultObj = cleatAngleConn(uiObj)
        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        dictangledata = self.fetchAnglePara()
        finCommonObj = cleatCommonData(uiObj, resultObj, dictbeamdata, dictcoldata, dictangledata, self.folder)
        base_front, base_top, base_side = finCommonObj.saveToSvg(str(fileName), view, base_front, base_top, base_side)
        return (base_front, base_top, base_side)

    def call_2d_Drawing(self, view):

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from CleatAngle GUI.
        '''
        base = ''
        loc = self.ui.comboConnLoc.currentText()

        if view == "All":
            fileName = ''
            base_front = ''
            base_side = ''
            base_top = ''
            base1, base2, base3 = self.callDesired_View(fileName, view, base_front, base_top, base_side)

            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
            if loc == "Column flange-Beam web":
                data = str(self.folder) + "/images_html/3D_ModelCleatFB.png"
                for n in range(1, 100, 1):
                    if (os.path.exists(data)):
                        data = str(self.folder) + "/images_html/3D_ModelCleatFB" + str(n) + ".png" 
                        continue
                base = os.path.basename(str(data))

            elif loc == "Column web-Beam web":
                data = str(self.folder) + "/images_html/3D_ModelCleatWB.png"
                for n in range(1, 100, 1):
                    if (os.path.exists(data)):
                        data = str(self.folder) + "/images_html/3D_ModelCleatWB" + str(n) + ".png" 
                        continue
                base = os.path.basename(str(data))

            else:
                data = str(self.folder) + "/images_html/3D_ModelCleatBB.png"
                for n in range(1, 100, 1):
                    if (os.path.exists(data)):
                        data = str(self.folder) + "/images_html/3D_ModelCleatBB" + str(n) + ".png"
                        continue
                base = os.path.basename(str(data))

            self.display.ExportToImage(data)

        else:

            fileName = QtGui.QFileDialog.getSaveFileName(self,
                                                         "Save SVG", str(self.folder) + '/untitled.svg',
                                                         "SVG files (*.svg)")
            f = open(fileName, 'w')

            self.callDesired_View(fileName, view, base_front, base_top, base_side)

            f.close()
        return (base, base1, base2, base3)

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

        root_Path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Report')
#         counter = 0
        for pdf_file in os.listdir(root_Path):
            if pdf_file.endswith('.pdf'):
                os.startfile("%s/%s" % (root_Path, pdf_file))
#                 counter = counter + 1

    def sample_problem(self):
        root_Path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Report')
        for pdf_file in os.listdir(root_Path):
            if pdf_file.endswith('.pdf'):
                os.startfile("%s/%s" % (root_Path, pdf_file))

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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/fin.log", mode="a")

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


def launchCleatAngleController(osdagMainWindow, folder):
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("Connections/Shear/cleatAngle/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/cleatAngle/log.css"/>''')

    # app = QtGui.QApplication(sys.argv)
    module_setup()
    # web = QWebView()
    window = MainController(folder)
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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/cleatAngle/log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    module_setup()
    # web = QWebView()
    window = MainController()
    window.show()
    sys.exit(app.exec_())
