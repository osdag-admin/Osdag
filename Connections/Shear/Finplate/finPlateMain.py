"""
Created on 07-May-2015
comment

@author: deepa
"""
import json

from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
from ui_finPlate import Ui_MainWindow
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_AboutOsdag
from ui_tutorial import Ui_Tutorial
from ui_ask_question import Ui_AskQuestion
from ui_design_preferences import Ui_ShearDesignPreferences
from model import *
from Connections.Shear.common_logic import CommonDesignLogic
# from Connections.Shear.commonlogic import CommonDesignLogic
from Svg_Window import SvgWindow
from OCC import BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC import IGESControl
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone
from OCC.StlAPI import StlAPI_Writer
import pdfkit
import subprocess
import os.path
import pickle
import shutil


class DesignPreferences(QDialog):
    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        self.ui = Ui_ShearDesignPreferences()
        self.ui.setupUi(self)
        self.main_controller = parent
        self.saved = None
        self.ui.combo_design_method.model().item(1).setEnabled(False)
        self.ui.combo_design_method.model().item(2).setEnabled(False)
        self.set_default_para()
        int_validator = QIntValidator()
        self.ui.txt_boltHoleClearance.setValidator(int_validator)
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_weldFu.setValidator(dbl_validator)
        self.ui.txt_weldFu.setMaxLength(7)
        self.ui.txt_detailingGap.setValidator(dbl_validator)
        self.ui.txt_detailingGap.setMaxLength(5)
        self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.set_bolthole_clernce)

    def highlight_slipfactor_description(self):
        """Highlight the description of currosponding slipfactor on selection of inputs
        Note : This routine is not in use in current version
        :return:
        """
        slip_factor = str(self.ui.combo_slipfactor.currentText())
        self.textCursor = QTextCursor(self.ui.textBrowser.document())
        cursor = self.textCursor
        # Setup the desired format for matches
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("red")))
        # Setup the regex engine
        pattern = str(slip_factor)
        regex = QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.ui.textBrowser.toPlainText(), pos)
        while (index != -1):
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfLine, 1)
            # cursor.movePosition(QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.ui.textBrowser.toPlainText(), pos)

    def save_designPref_para(self):
        """This routine is responsible for saving all design preferences selected by the user
        """
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_clrnce"] = float(str(self.ui.txt_boltHoleClearance.text()))
        self.saved_designPref["bolt"]["bolt_fu"] = int(str(self.ui.txt_boltFu.text()))
        self.saved_designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        self.saved_designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        self.saved_designPref["weld"]["typeof_weld"] = weldType
        if weldType == "Shop weld":
            self.saved_designPref["weld"]["safety_factor"] = float(1.25)
        else:
            self.saved_designPref["weld"]["safety_factor"] = float(1.5)
        self.saved_designPref["weld"]["fu_overwrite"] = self.ui.txt_weldFu.text()

        self.saved_designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        self.saved_designPref["detailing"]["typeof_edge"] = typeOfEdge
        if typeOfEdge == "a - Sheared or hand flame cut":
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.7)
        else:
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.5)
        if self.ui.txt_detailingGap.text() == '':

            self.saved_designPref["detailing"]["gap"] = int(20)
        else:
            self.saved_designPref["detailing"]["gap"] = int(self.ui.txt_detailingGap.text())

        self.saved_designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())
        self.saved_designPref["design"] = {}
        self.saved_designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
        self.saved = True

        QMessageBox.about(self, 'Information', "Preferences saved")

        return self.saved_designPref


        # self.main_controller.call_designPref(designPref)

    def set_default_para(self):
        """

        Returns:

        """
        uiObj = self.main_controller.getuser_inputs()
        if uiObj["Bolt"]["Diameter (mm)"] == 'Diameter of Bolt':
            pass
        else:
            boltDia = int(uiObj["Bolt"]["Diameter (mm)"])
            clearance = str(self.get_clearance(boltDia))
            self.ui.txt_boltHoleClearance.setText(clearance)
        if uiObj["Bolt"]["Grade"] == '':
            pass
        else:
            bolt_grade = float(uiObj["Bolt"]["Grade"])
            bolt_fu = str(self.get_boltFu(bolt_grade))
            self.ui.txt_boltFu.setText(bolt_fu)

        self.ui.combo_boltHoleType.setCurrentIndex(0)
        designPref = {}
        designPref["bolt"] = {}
        designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        designPref["bolt"]["bolt_hole_clrnce"] = float(self.ui.txt_boltHoleClearance.text())
        designPref["bolt"]["bolt_fu"] = int(self.ui.txt_boltFu.text())
        self.ui.combo_slipfactor.setCurrentIndex(8)
        designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        self.ui.combo_weldType.setCurrentIndex(0)
        designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        designPref["weld"]["typeof_weld"] = weldType
        designPref["weld"]["safety_factor"] = float(1.25)
        self.ui.txt_weldFu.setText(str(410))
        designPref["weld"]["fu_overwrite"] = self.ui.txt_weldFu.text()

        self.ui.combo_detailingEdgeType.setCurrentIndex(0)
        self.ui.txt_detailingGap.setText(str(20))
        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        designPref["detailing"]["min_edgend_dist"] = float(1.7)
        designPref["detailing"]["gap"] = int(20)

        self.ui.combo_detailing_memebers.setCurrentIndex(0)
        designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())

        designPref["design"] = {}
        designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
        self.saved = False

        return designPref

    def set_bolthole_clernce(self):
        uiObj = self.main_controller.getuser_inputs()
        boltDia = str(uiObj["Bolt"]["Diameter (mm)"])
        if boltDia != "Diameter of Bolt":
            clearance = self.get_clearance(int(boltDia))
            self.ui.txt_boltHoleClearance.setText(str(clearance))
        else:
            pass

    def set_boltFu(self):
        uiObj = self.main_controller.getuser_inputs()
        boltGrade = str(uiObj["Bolt"]["Grade"])
        if boltGrade != '':
            boltfu = str(self.get_boltFu(boltGrade))
            self.ui.txt_boltFu.setText(boltfu)
        else:
            pass

    def get_clearance(self, boltDia):

        standard_clrnce = {12: 1, 14: 1, 16: 2, 18: 2, 20: 2, 22: 2, 24: 2, 30: 3, 34: 3, 36: 3}
        overhead_clrnce = {12: 3, 14: 3, 16: 4, 18: 4, 20: 4, 22: 4, 24: 6, 30: 8, 34: 8, 36: 8}

        if self.ui.combo_boltHoleType.currentText() == "Standard":
            clearance = standard_clrnce[boltDia]
        else:
            clearance = overhead_clrnce[boltDia]

        return clearance

    def get_boltFu(self, boltGrade):
        '''
        This routine returns ultimate strength of bolt depending upon grade of bolt chosen
        '''
        boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040,
                  12.9: 1220}
        boltGrd = float(boltGrade)
        return boltFu[boltGrd]

    def close_designPref(self):
        self.close()


class MyAskQuestion(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AskQuestion()
        self.ui.setupUi(self)
        self.mainController = parent


class MyTutorials(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Tutorial()
        self.ui.setupUi(self)
        self.mainController = parent


class MyAboutOsdag(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AboutOsdag()
        self.ui.setupUi(self)
        self.mainController = parent


class MyPopupDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
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

        self.ui.lbl_browse.clear()
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open File', " ",
            'Images (*.png *.svg*.jpg)',
            None, QFileDialog.DontUseNativeDialog)

        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

        return str(filename)

    def desired_location(self, filename):

        shutil.copyfile(filename, os.path.join(str(self.mainController.folder), "images_html", "cmpylogoFin.png"))

    def saveUserProfile(self):

        inputData = self.getPopUpInputs()
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Files',
                                                  os.path.join(str(self.mainController.folder), "Profile"), '*.txt')
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
        input_summary["Client"] = str(self.ui.lineEdit_client.text())

        return input_summary

    def useUserProfile(self):

        filename, _ = QFileDialog.getOpenFileName(self, 'Open Files',
                                                  os.path.join(str(self.mainController.folder), "Profile"),
                                                  '*.txt')
        if os.path.isfile(filename):
            outfile = open(filename, 'r')
            reportsummary = pickle.load(outfile)
            self.ui.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
            self.ui.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
            self.ui.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
            self.ui.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])

        else:
            pass


class MainController(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder

        self.get_columndata()
        self.get_beamdata()

        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Please Select Type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convertColComboToBeam)
        # self.retrieve_prevstate()

        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        # self.ui.btn_2D.clicked.connect(self.call2D_Drawing)
        self.ui.btn3D.clicked.connect(self.call_3DModel)
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxFinplate.clicked.connect(self.call_3DFinplate)

        validator = QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)

        dbl_validator = QDoubleValidator()
        self.ui.txtPlateLen.setValidator(dbl_validator)
        self.ui.txtPlateLen.setMaxLength(7)
        self.ui.txtPlateWidth.setValidator(dbl_validator)
        self.ui.txtPlateWidth.setMaxLength(7)
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

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # File Menu

        self.ui.actionSave_Front_View.triggered.connect(lambda: self.callFin2D_Drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.callFin2D_Drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.callFin2D_Drawing("Top"))
        self.ui.actionfinPlate_quit.setShortcut('Ctrl+Q')
        self.ui.actionfinPlate_quit.setStatusTip('Exit application')
        self.ui.actionfinPlate_quit.triggered.connect(qApp.quit)

        self.ui.actionCreate_design_report.triggered.connect(self.createDesignReport)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_curren_image_as.triggered.connect(self.save_cadImages)
        self.ui.actionPan.triggered.connect(self.call_Pannig)
        self.ui.action_savedesign.triggered.connect(self.saveDesign_inputs)
        self.ui.action_open_design.triggered.connect(self.openDesign_inputs)
        # graphics
        self.ui.actionBeam_2.triggered.connect(self.call_3DBeam)
        self.ui.actionColumn_2.triggered.connect(self.call_3DColumn)
        self.ui.actionFinplate_2.triggered.connect(self.call_3DFinplate)
        self.ui.actionShow_all.triggered.connect(self.call_3DModel)
        self.ui.actionChange_background.triggered.connect(self.showColorDialog)
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        #self.ui.combo_Beam.currentIndexChanged[int].connect(lambda: self.fillPlateThickCombo("combo_Beam"))
        self.ui.combo_Beam.currentIndexChanged[int].connect(lambda: self.fillPlateThickCombo)

        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkBeam_B)
        self.ui.combo_Beam.currentIndexChanged[int].connect(self.checkBeam_B)
        self.ui.comboPlateThick_2.currentIndexChanged[int].connect(
            lambda: self.populateWeldThickCombo)
        self.ui.comboDiameter.currentIndexChanged[str].connect(self.bolt_hole_clearace)
        self.ui.comboGrade.currentIndexChanged[str].connect(self.call_boltFu)

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
        self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_question)

        self.ui.actionDesign_Preferences.triggered.connect(self.design_preferences)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())
        self.connection = "Finplate"
        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        self.resultObj = None
        self.uiObj = None
        self.designPrefDialog = DesignPreferences(self)

    def get_columndata(self):
        """Fetch  old and new column sections from "Intg_osdag" database.
        Returns:

        """
        columndata = get_columncombolist()
        old_colList = get_oldcolumncombolist()
        self.ui.comboColSec.addItems(columndata)
        self.color_oldDB_sections(old_colList, columndata, self.ui.comboColSec)

    def get_beamdata(self):
        """Fetch old and new beam sections from "Intg_osdag" database
        Returns:

        """
        beamdata = get_beamcombolist()
        old_beamList = get_oldbeamcombolist()
        self.ui.combo_Beam.addItems(beamdata)
        self.color_oldDB_sections(old_beamList, beamdata, self.ui.combo_Beam)

    def color_oldDB_sections(self, old_section, intg_section, combo_section):
        """display old sections in red color.

        Args:
            old_section(str): Old sections from IS 808 1984
            intg_section(str): Revised sections from IS 808 2007
            combo_section(QcomboBox): Beam/Column dropdown list

        Returns:

        """
        print "old section",old_section
        print "form intg",intg_section
        indx = 0
        # duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]

        for col in old_section:
            if col in intg_section:

                indx = intg_section.index(str(col))
                combo_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
                indx += 1

    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

    def fetchBeamPara(self):
        beam_sec = self.ui.combo_Beam.currentText()
        dictbeamdata = get_beamdata(beam_sec)
        return dictbeamdata

    def fetchColumnPara(self):
        """Return  sectional properties of selected column section
        Returns:
            dictcoldata(dict): Sectional properties of column

        """
        column_sec = str(self.ui.comboColSec.currentText())
        if column_sec == 'Select section':
            return
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            dictcoldata = get_beamdata(column_sec)
        else:
            dictcoldata = get_columndata(column_sec)
        return dictcoldata

    def convertColComboToBeam(self):
        """Replace colulmn cobobox to Primary beam sections and change text of column section(label) to primary beam.
        Returns:

        """

        self.display.EraseAll()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.lbl_beam.setText(" Secondary beam *")
            self.ui.lbl_column.setText("Primary beam *")

            self.ui.chkBxBeam.setText("SBeam")
            self.ui.chkBxBeam.setToolTip("Secondary  beam")
            self.ui.chkBxCol.setText("PBeam")
            self.ui.chkBxCol.setToolTip("Primary beam")
            self.ui.comboColSec.blockSignals(True)
            self.ui.comboColSec.clear()
            self.get_columndata()
            #self.ui.comboColSec.addItems(get_beamcombolist())
            self.ui.combo_Beam.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()

            self.ui.comboDiameter.blockSignals(True)
            self.ui.comboDiameter.setCurrentIndex(0)
            # self.ui.comboType.blockSignals(True)
            self.ui.comboType.setCurrentIndex((0))
            self.ui.comboGrade.blockSignals(True)
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
            self.get_columndata()
            #self.ui.comboColSec.addItems(get_columncombolist())
            self.ui.comboColSec.setCurrentIndex(0)
            self.ui.combo_Beam.setCurrentIndex(0)

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

        font, ok = QFontDialog.getFont()
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
        """Save CAD Model in image formats(PNG,JPEG,BMP,TIFF)

        Returns:

        """
        files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
        fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"),
                                                  files_types)
        fName = str(fileName)
        file_extension = fName.split(".")[-1]

        if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp' or file_extension == 'tiff':
            self.display.ExportToImage(fName)
            QMessageBox.about(self, 'Information', "File saved")

    def disableViewButtons(self):
        """Disable all tool buttons on Toolbar.

        Returns:

        """
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
        # self.ui.menubar.setEnabled(False)
        self.ui.menuFile.setEnabled(False)
        self.ui.menuEdit.setEnabled(False)
        self.ui.menuView.setEnabled(False)
        self.ui.menuGraphics.setEnabled(False)

        # self.ui.menuHelp.setEnabled(False)

    def enableViewButtons(self):
        """Enable the all buttons in toolbar

        Returns:

        """
        self.ui.btnFront.setEnabled(True)
        self.ui.btnSide.setEnabled(True)
        self.ui.btnTop.setEnabled(True)
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxFinplate.setEnabled(True)
        # self.ui.menubar.setEnabled(True)
        self.ui.menuFile.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuView.setEnabled(True)
        self.ui.menuGraphics.setEnabled(True)

        self.ui.btn_CreateDesign.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)

    def fillPlateThickCombo(self):
        """Populates the plate thickness on the basis of beam web thickness and plate thickness check

        Returns:

        """

        if self.ui.combo_Beam.currentText() == "Select section":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return
        else:
            dictbeamdata = self.fetchBeamPara()
            beam_tw = float(dictbeamdata["tw"])
            plateThickness = [6, 8, 10, 12, 14, 16, 18, 20]

            newlist = []
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

    def populateWeldThickCombo(self):
        """Return weld thickness on the basis column flange and plate thickness check
        ThickerPart between column Flange and plate thickness again get checked according to the IS 800 Table 21
        (Name of the table :Minimum Size of First Rum or of a Single Run Fillet Weld)

        Returns:

        """
        if str(self.ui.combo_Beam.currentText()) == "Select section":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return

        else:
            newlist = []
            weldlist = [3, 4, 5, 6, 8, 10, 12, 16]
            dictbeamdata = self.fetchBeamPara()
            beam_tw = float(dictbeamdata["tw"])
            column_sec = str(self.ui.comboColSec.currentText())
            if column_sec == 'Select section':
                return
            dictcoldata = self.fetchColumnPara()
            plate_thickness = self.ui.comboPlateThick_2.currentText()
            plate_thick = float(plate_thickness)

            if str(self.ui.comboConnLoc.currentText()) == "Column flange-Beam web":
                if str(self.ui.comboColSec.currentText()) == "Select section":
                    self.ui.comboWldSize.clear()
                    return
                else:
                    column_tf = float(dictcoldata["T"])
                    thickerPart = column_tf > plate_thick and column_tf or plate_thick

            elif str(self.ui.comboConnLoc.currentText()) == "Column web-Beam web":
                if str(self.ui.comboColSec.currentText()) == "Select section":
                    self.ui.comboWldSize.clear()
                    return
                else:
                    column_tw = float(dictcoldata["tw"])
                    thickerPart = column_tw > plate_thick and column_tw or plate_thick
            else:
                PBeam_tw = float(dictcoldata["tw"])
                thickerPart = PBeam_tw > plate_thick and PBeam_tw or plate_thick

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
        """Maintain previous session's data.
        Returns:

        """

        uiObj = self.get_prevstate()
        self.setDictToUserInputs(uiObj)

    def setDictToUserInputs(self, uiObj):

        if (uiObj is not None):

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
            pixmap = QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            # self.ui.lbl_connectivity.show()
        elif (loc == "Column web-Beam web"):
            picmap = QPixmap(":/newPrefix/images/colW3.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)
        else:
            picmap = QPixmap(":/newPrefix/images/b-b.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)

        return True

    def getuser_inputs(self):
        '''
        keyword arguments: None

        Returns the dictionary object with the user input fields for designing fin plate connection

        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText()
        uiObj["Bolt"]["Grade"] = (self.ui.comboGrade.currentText())
        uiObj["Bolt"]["Type"] = str(self.ui.comboType.currentText())

        uiObj["Weld"] = {}
        uiObj["Weld"]['Size (mm)'] = self.ui.comboWldSize.currentText()

        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        uiObj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txtFu.text()
        uiObj['Member']['fy (MPa)'] = self.ui.txtFy.text()

        uiObj['Plate'] = {}
        uiObj['Plate']['Thickness (mm)'] = self.ui.comboPlateThick_2.currentText()
        uiObj['Plate']['Height (mm)'] = self.ui.txtPlateLen.text()  # changes the label length to height
        uiObj['Plate']['Width (mm)'] = self.ui.txtPlateWidth.text()

        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = self.ui.txtShear.text()

        return uiObj

    def saveDesign_inputs(self):

        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Design", os.path.join(str(self.folder), "untitled.osi"),
                                                  "Input Files(*.osi)")

        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return

        # yaml.dump(self.uiObj,out_file,allow_unicode=True, default_flow_style=False)
        json.dump(self.uiObj, out_file)

        out_file.close()

        pass

    def openDesign_inputs(self):

        fileName, _ = QFileDialog.getOpenFileName(self, "Open Design", str(self.folder), "All Files(*)")
        if not fileName:
            return
        try:
            in_file = open(str(fileName), 'rb')

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return
        uiObj = json.load(in_file)
        self.setDictToUserInputs(uiObj)

    def save_inputs(self, uiObj):
        '''Save the user inputs in text format

        Args:
            :param uiObj: User inputs
            :type uiObj:Dictionary
        '''
        inputFile = QFile(os.path.join("Connections", "Shear", "Finplate", "saveINPUT.txt"))
        if not inputFile.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        pickle.dump(uiObj, inputFile)

    def get_prevstate(self):
        '''
        '''
        fileName = os.path.join("Connections", "Shear", "Finplate", "saveINPUT.txt")

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

        fileName = os.path.join(self.folder, "images_html", "Html_Report.html")
        fileName = str(fileName)
        self.callFin2D_Drawing("All")

        self.commLogicObj.call_designReport(fileName, popup_summary)

        # Creates pdf
        if sys.platform == ("win32" or "win64"):
            path_wkthmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        else:
            path_wkthmltopdf = r'/usr/bin/wkhtmltopdf'
            # path_wkthmltopdf = r'/home/deepa-c/miniconda2/pkgs/wkhtmltopdf-0.12.3-0/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        file_type = "PDF (*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", file_type)
        pdfkit.from_file(fileName, fname, configuration=config, options=options)

        QMessageBox.about(self, 'Information', "Report Saved")

    def save_log(self):

        fileName, pat = QFileDialog.getSaveFileName(self, "Save File As",
                                                    os.path.join(str(self.folder), "LogMessages"),
                                                    "Text files (*.txt)")
        return self.save_file(fileName + ".txt")

    def save_file(self, fileName):
        '''(file open for writing)-> boolean
        '''
        fname = QFile(fileName)

        if not fname.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (fileName, fname.errorString()))
            return False

        outf = QTextStream(fname)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

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

        # ------ Erase Display
        self.display.EraseAll()

    def dockbtn_clicked(self, widget):

        '''(QWidget) -> None

        This method dock and undock widget(QdockWidget)
        '''

        flag = widget.isHidden()
        if (flag):

            widget.show()
        else:
            widget.hide()

    def combotype_currentindexchanged(self, index):

        '''(Number) -> None
        '''
        items = self.gradeType[str(index)]
        if items != 0:

            self.ui.comboGrade.clear()
            strItems = []
            for val in items:
                strItems.append(str(val))

            self.ui.comboGrade.addItems(strItems)
        else:
            pass

    def check_range(self, widget, lblwidget, minVal, maxVal):

        '''(QlineEdit, QLable, Number, Number)---> None
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr)
        if (val < minVal or val > maxVal):
            QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s [cl 2.2.4.2]' % (minVal, maxVal))
            widget.clear()
            widget.setFocus()
            palette = QPalette()
            palette.setColor(QPalette.Foreground, Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QPalette()
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
        afile = QFile(fname)

        if not afile.open(QIODevice.ReadOnly):  # ReadOnly
            QMessageBox.information(None, 'info', afile.errorString())

        stream = QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscrollBar = self.ui.textEdit.verticalScrollBar()
        vscrollBar.setValue(vscrollBar.maximum())
        afile.close()

    # QtViewer
    def init_display(self, backend_str=None, size=(1024, 768)):

        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        # from OCC.Display.pyqt4Display import qtViewer3d
        from OCC.Display.qtDisplay import qtViewer3d
        self.ui.modelTab = qtViewer3d(self)

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

        col = QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

    def checkBeam_B(self):
        loc = str(self.ui.comboConnLoc.currentText())
        if loc == "Column web-Beam web":
            if self.ui.comboColSec.currentIndex() == -1 or str(
                    self.ui.combo_Beam.currentText()) == 'Select section' or str(
                self.ui.comboColSec.currentText()) == 'Select section':
                return
            column = self.ui.comboColSec.currentText()
            beam_index = self.ui.combo_Beam.currentIndex()
            dictBeamData = self.fetchBeamPara()
            dictColData = self.fetchColumnPara()
            column_D = float(dictColData["D"])
            column_T = float(dictColData["T"])
            column_R1 = float(dictColData["R1"])
            columnWebDepth = column_D - (2.0 * (column_T) + 2.0 * (10))
            beam_B = float(dictBeamData["B"])

            if columnWebDepth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                self.disableViewButtons()
                QMessageBox.about(self, 'Information',
                                  "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)
                self.enableViewButtons()
        elif loc == "Beam-Beam":

            if self.ui.comboColSec.currentIndex() == 0 or self.ui.combo_Beam.currentIndex() == 0:
                return

            dictSBeamData = self.fetchBeamPara()
            dictPBeamData = self.fetchColumnPara()

            PBeam_D = float(dictPBeamData["D"])
            PBeam_T = float(dictPBeamData["T"])
            PBeamWebDepth = PBeam_D - 2.0 * (PBeam_T)

            SBeam_D = float(dictSBeamData["D"])

            if PBeamWebDepth <= SBeam_D:
                self.ui.btn_Design.setDisabled(True)
                QMessageBox.about(self, 'Information',
                                  "Secondary beam depth is higher than clear depth of primary beam web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)

    def validateInputsOnDesignBtn(self):

        if self.ui.comboConnLoc.currentIndex() == 0:
            QMessageBox.about(self, "Information", "Please select connectivity")
        state = self.setimage_connection()
        if state is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web" or self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
                if self.ui.comboColSec.currentIndex() == 0:
                    QMessageBox.about(self, "Information", "Please select column section")
                elif self.ui.combo_Beam.currentIndex() == 0:
                    QMessageBox.about(self, "Information", "Please select beam section")
            else:
                if self.ui.comboColSec.currentIndex() == 0:
                    QMessageBox.about(self, "Information", "Please select Primary beam  section")
                elif self.ui.combo_Beam.currentIndex() == 0:
                    QMessageBox.about(self, "Information", "Please select Secondary beam  section")

        if self.ui.txtFu.text() == '' or float(self.ui.txtFu.text()) == 0:
            QMessageBox.about(self, "Information", "Please select Ultimate strength of  steel")

        elif self.ui.txtFy.text() == '' or float(self.ui.txtFy.text()) == 0:
            QMessageBox.about(self, "Information", "Please select Yeild  strength of  steel")

        elif self.ui.txtShear.text() == '' or float(str(self.ui.txtShear.text())) == str(0):
            QMessageBox.about(self, "Information", "Please select Factored shear load")

        elif self.ui.comboDiameter.currentIndex() == 0:
            QMessageBox.about(self, "Information", "Please select Diameter of  bolt")

        elif self.ui.comboType.currentIndex() == 0:
            QMessageBox.about(self, "Information", "Please select Type of  bolt")

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
        nutDia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23, 30: 25.35,
                  36: 30.65}

        return nutDia[boltDia]

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def call_3DModel(self):
        '''
        This routine responsible for diasplaying 3D Cad model
        :param flag: boolean
        :return:
        '''
        if self.ui.btn3D.isChecked:
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
        self.commLogicObj.display_3DModel("Model")

    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam")

    def call_3DColumn(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column")

    def call_3DFinplate(self):
        '''
        Displaying FinPlate in 3D
        '''
        self.ui.chkBxFinplate.setChecked(Qt.Checked)
        if self.ui.chkBxFinplate.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            self.ui.btn3D.setChecked(Qt.Unchecked)

        self.commLogicObj.display_3DModel("Plate")

    def unchecked_allChkBox(self):
        '''
        This routine is responsible for unchecking all checkboxes in GUI
        '''

        self.ui.btn3D.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.chkBxFinplate.setChecked(Qt.Unchecked)

    def call_designPref(self, designPref):
        self.uiObj = self.getuser_inputs()
        self.uiObj

    def designParameters(self):
        '''
        This routine returns the neccessary design parameters.
        '''
        self.uiObj = self.getuser_inputs()
        if self.designPrefDialog.saved is not True:
            design_pref = self.designPrefDialog.set_default_para()
        else:
            design_pref = self.designPrefDialog.saved_designPref  # self.designPrefDialog.save_designPref_para()
        self.uiObj.update(design_pref)
        print "design_pref = ", self.uiObj

        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        dict_angle_data = {}
        dict_topangledata = {}
        dict_topangledata = {}
        loc = str(self.ui.comboConnLoc.currentText())
        component = "Model"
        bolt_dia = int(self.uiObj["Bolt"]["Diameter (mm)"])
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        return [self.uiObj, dictbeamdata, dictcoldata, dict_angle_data, dict_topangledata, loc, component, bolt_R,
                bolt_T, bolt_Ht, nut_T]

    def design_btnclicked(self):
        '''
        '''
        self.display.EraseAll()
        self.alist = self.designParameters()
        print "printing design para with DP =", self.alist[0]

        self.validateInputsOnDesignBtn()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self.unchecked_allChkBox()
        self.commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3],
                                              self.alist[4], self.alist[5], self.alist[6], self.alist[7],
                                              self.alist[8], self.alist[9], self.alist[10], self.display, self.folder,
                                              self.connection)

        self.resultObj = self.commLogicObj.resultObj
        alist = self.resultObj.values()
        self.display_output(self.resultObj)
        self.displaylog_totextedit(self.commLogicObj)
        isempty = [True if val != '' else False for ele in alist for val in ele.values()]

        if isempty[0] == True:
            status = self.resultObj['Bolt']['status']
            self.commLogicObj.call_3DModel(status)
            self.callFin2D_Drawing("All")
        else:
            pass
            # self.display.EraseAll()

    def create2Dcad(self):
        ''' Returns the 3D model of finplate depending upon component
        '''
        if self.commLogicObj.component == "Beam":
            final_model = self.commLogicObj.connectivityObj.get_beamModel()

        elif self.commLogicObj.component == "Column":
            final_model = self.commLogicObj.connectivityObj.columnModel

        elif self.commLogicObj.component == "Plate":
            cadlist = [self.commLogicObj.connectivityObj.weldModelLeft,
                       self.commLogicObj.connectivityObj.weldModelRight,
                       self.commLogicObj.connectivityObj.plateModel] + self.commLogicObj.connectivityObj.nut_bolt_array.get_models()
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

        fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"),
                                                  files_types)
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

        self.fuse_model = None

        QMessageBox.about(self, 'Information', "File saved")

    def callFin2D_Drawing(self, view):  # call2D_Drawing(self,view)

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.btn3D.setChecked(Qt.Unchecked)
        # commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4],
        #                                  self.alist[5], self.alist[6], self.alist[7],
        #                                  self.alist[8],self.alist[9], self.display, self.folder, self.connection)
        if view != 'All':

            if view == "Front":
                filename = os.path.join(self.folder, "images_html", "finFront.svg")

            elif view == "Side":
                filename = os.path.join(self.folder, "images_html", "finSide.svg")

            else:
                filename = os.path.join(self.folder, "images_html", "finTop.svg")

            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, self.folder)

        else:
            fname = ''
            self.commLogicObj.call2D_Drawing(view, fname, self.folder)

    # def save_2D_images(self, view):
    #
    #     fileName = QFileDialog.getSaveFileName(self,
    #                                                  "Save as PNG", str(self.folder) + '/untitled.png',
    #                                                  "PNG files (*.png)")
    #     f = open(self.callFin2D_Drawing(view), 'w')
    #     f.close()
    #     QMessageBox.about(self, 'Information', "Image Saved")

    def closeEvent(self, event):
        '''
        Closing finPlate window.
        '''
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()

            # Help Action

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

    def sample_report(self):

        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Report')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def sample_problem(self):
        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Problems')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def design_preferences(self):
        self.designPrefDialog.show()

    def bolt_hole_clearace(self):
        self.designPrefDialog.set_bolthole_clernce()

    def call_boltFu(self):
        self.designPrefDialog.set_boltFu()


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

    app = QApplication(sys.argv)
    module_setup()
    ########################################
    folder_path = "/home/deepa-c/Osdag_workspace"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path, 0755)
    image_folder_path = os.path.join(folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0755)
    window = MainController(folder_path)
    ########################################
    # folder = None
    window = MainController(folder_path)
    window.show()
    sys.exit(app.exec_())
