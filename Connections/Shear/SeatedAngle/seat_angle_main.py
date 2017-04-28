import os.path
import sys
import subprocess
import pdfkit

from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import shutil
import pickle

from OCC import BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC import IGESControl
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone
from OCC.StlAPI import StlAPI_Writer

from model import *

from svg_window import SvgWindow
import report_generator
from ui_design_preferences import Ui_ShearDesignPreferences
from ui_seat_angle import Ui_MainWindow
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_AboutOsdag
from ui_tutorial import Ui_Tutorial
from ui_ask_question import Ui_AskQuestion
from Connections.Shear.common_logic import CommonDesignLogic
import seat_angle_calc


class DesignPreferences(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_ShearDesignPreferences()
        self.ui.setupUi(self)
        self.main_controller = parent
        self.saved = None
        self.ui.combo_design_method.model().item(1).setEnabled(False)
        self.ui.combo_design_method.model().item(2).setEnabled(False)
        self.ui.tabWidget.removeTab(1)
        self.set_default_para()
        self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.set_bolthole_clearance)

    def save_designPref_para(self):
        """
        This routine is responsible for saving all design preferences selected by the user
        """
        self.saved_designPref = {"bolt": {}}
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_clrnce"] = float(self.ui.txt_boltHoleClearance.text())
        self.saved_designPref["bolt"]["bolt_fu"] = int(self.ui.txt_boltFu.text())
        self.saved_designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))
        self.saved_designPref["bolt"]["ultimate_load"] = str(self.ui.combo_ultimat_load.currentText())

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
        self.ui.combo_design_method.setCurrentIndex(0)
        self.saved_designPre["design"]["design_method"] = self.ui.combo_design_method.currentText()
        self.saved = True
        QMessageBox.about(self, 'Information', "Preferences saved")

        return self.saved_designPref

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
        designPref = {"bolt": {}}
        designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        designPref["bolt"]["bolt_hole_clrnce"] = float(self.ui.txt_boltHoleClearance.text())
        designPref["bolt"]["bolt_fu"] = int(self.ui.txt_boltFu.text())
        self.ui.combo_slipfactor.setCurrentIndex(8)
        designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        self.ui.combo_detailingEdgeType.setCurrentIndex(0)
        self.ui.txt_detailingGap.setText(str(20))
        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        designPref["detailing"]["min_edgend_dist"] = float(1.7)
        designPref["detailing"]["gap"] = int(20)
        self.ui.combo_detailing_memebers.setCurrentIndex(0)
        designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())

        self.ui.combo_design_method.setCurrentIndex(0)
        designPref["design"] = {}
        designPref["design"]["design_method"] = self.ui.combo_design_method.currentText()
        self.saved = False

        return designPref

    def set_bolthole_clearance(self):
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
        """
        This routine returns ultimate strength of bolt depending upon grade of bolt chosen
        """
        # TODO : change grade to 10.9; also update UI
        boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.8: 1040,
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


# below class was previously MyPopupDialog in the other modules
class DesignReportDialog(QDialog):
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
        report_summary = self.get_report_summary()
        self.mainController.save_design(report_summary)

    def getLogoFilePath(self, lblwidget):
        self.ui.lbl_browse.clear()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', " ", 'Images (*.png *.svg *.jpg)', None,
                                                  QFileDialog.DontUseNativeDialog)
        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

        return str(filename)

    def desired_location(self, filename):
        shutil.copyfile(filename, os.path.join(str(self.mainController.folder), "images_html", "cmpylogoFin.png"))

    def saveUserProfile(self):
        inputData = self.get_report_summary()
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Files',
                                                  os.path.join(str(self.mainController.folder), "Profile"), '*.txt')
        infile = open(filename, 'w')
        pickle.dump(inputData, infile)
        infile.close()

    def get_report_summary(self):
        report_summary = {"ProfileSummary": {}}
        report_summary["ProfileSummary"]["CompanyName"] = str(self.ui.lineEdit_companyName.text())
        report_summary["ProfileSummary"]["CompanyLogo"] = str(self.ui.lbl_browse.text())
        report_summary["ProfileSummary"]["Group/TeamName"] = str(self.ui.lineEdit_groupName.text())
        report_summary["ProfileSummary"]["Designer"] = str(self.ui.lineEdit_designer.text())

        report_summary["ProjectTitle"] = str(self.ui.lineEdit_projectTitle.text())
        report_summary["Subtitle"] = str(self.ui.lineEdit_subtitle.text())
        report_summary["JobNumber"] = str(self.ui.lineEdit_jobNumber.text())
        report_summary["Client"] = str(self.ui.lineEdit_client.text())
        report_summary["AdditionalComments"] = str(self.ui.txt_additionalComments.toPlainText())

        return report_summary

    def useUserProfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Files',
                                                  os.path.join(str(self.mainController.folder), "Profile"),
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


class MainController(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder

        self.ui.combo_beam_section.addItems(get_beamcombolist())
        self.ui.combo_column_section.addItems(get_columncombolist())
        self.ui.combo_angle_section.addItems(get_anglecombolist())
        self.ui.combo_topangle_section.addItems(get_anglecombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.grade_type = {'Please Select Type': '',  # TODO HSFG 10.9
                           'HSFG': [8.8, 10.8],
                           'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_bolt_type.addItems(self.grade_type.keys())
        self.ui.combo_bolt_type.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.combo_bolt_type.setCurrentIndex(0)

        self.ui.combo_connectivity.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()

        self.ui.combo_connectivity.currentIndexChanged[str].connect(self.convert_col_combo_to_beam)

        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        self.ui.btn3D.clicked.connect(self.call_3DModel)
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxSeatAngle.clicked.connect(self.call_3DSeatAngle)

        validator = QIntValidator()
        self.ui.txt_fu.setValidator(validator)
        self.ui.txt_fy.setValidator(validator)

        dbl_validator = QDoubleValidator()
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

        # Menu Bar and File Menu
        self.ui.actionSave_front_view.triggered.connect(lambda: self.call_seatangle2D_Drawing("Front"))
        self.ui.actionSave_side_view.triggered.connect(lambda: self.call_seatangle2D_Drawing("Side"))
        self.ui.actionSave_top_view.triggered.connect(lambda: self.call_seatangle2D_Drawing("Top"))

        self.ui.actionQuit_fin_plate_design.setShortcut('Ctrl+Q')
        self.ui.actionQuit_fin_plate_design.setStatusTip('Exit application')
        self.ui.actionQuit_fin_plate_design.triggered.connect(qApp.quit)

        self.ui.actionCreate_design_report.triggered.connect(self.create_design_report)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
        self.ui.actionZoom_in.triggered.connect(self.callZoomin)
        self.ui.actionZoom_out.triggered.connect(self.callZoomout)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_current_2D_image_as.triggered.connect(self.save_cadImages)
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
        self.ui.btn_Design.clicked.connect(self.osdag_header)

        # Help button
        self.ui.actionAbout_Osdag.triggered.connect(self.open_osdag)
        self.ui.actionVideo_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_Reports.triggered.connect(self.sample_report)
        self.ui.actionSampe_Problems.triggered.connect(self.sample_problem)
        self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_question)

        from osdagMainSettings import backend_name

        self.display, _ = self.init_display(backend_str=backend_name())
        self.ui.actionDesign_preferences.triggered.connect(self.design_preferences)

        # self.ui.btnSvgSave.clicked.connect(self.save3DcadImages)

        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        self.resultObj = None
        self.uiObj = None
        self.connection = "SeatedAngle"
        self.sa_calc_object = seat_angle_calc.SeatAngleCalculation()
        self.designPrefDialog = DesignPreferences(self)

    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

    def fetchBeamPara(self):
        beam_sec = self.ui.combo_beam_section.currentText()
        dict_beam_data = get_beamdata(beam_sec)
        return dict_beam_data

    def fetchColumnPara(self):
        column_sec = self.ui.combo_column_section.currentText()
        loc = self.ui.combo_connectivity.currentText()
        if loc == "Beam-Beam":
            dict_col_data = get_beamdata(column_sec)
        else:
            dict_col_data = get_columndata(column_sec)
        return dict_col_data

    def fetch_angle_para(self):
        angle_sec = self.ui.combo_angle_section.currentText()
        dict_angle_data = get_angledata(angle_sec)
        return dict_angle_data

    def fetch_top_angle_para(self):
        if self.ui.combo_topangle_section.currentText() is not None:
            angle_sec = self.ui.combo_topangle_section.currentText()
            dict_top_angle = get_angledata(angle_sec)
        else:
            dict_top_angle = {}
        return dict_top_angle

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
        files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
        fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"),
                                                  files_types)
        fName = str(fileName)
        file_extension = fName.split(".")[-1]

        if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp' or file_extension == 'tiff':
            self.display.ExportToImage(fName)
            QMessageBox.about(self, 'Information', "File saved")

    def disableViewButtons(self):
        """
        Disables the all buttons in toolbar
        """
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
        self.ui.menuFile.setEnabled(False)
        self.ui.menuGraphics.setEnabled(False)
        self.ui.menuView.setEnabled(False)
        self.ui.menuEdit.setEnabled(False)

    def enableViewButtons(self):
        """
        Enables the all buttons in toolbar
        """
        self.ui.btn_front.setEnabled(True)
        self.ui.btn_side.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxSeatAngle.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)

        self.ui.menuFile.setEnabled(True)
        self.ui.menuGraphics.setEnabled(True)
        self.ui.menuView.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)

    def convert_col_combo_to_beam(self):
        loc = self.ui.combo_connectivity.currentText()
        if loc == "Column flange-Beam flange":
            self.ui.combo_beam_section.setCurrentIndex(0)
            self.ui.combo_column_section.setCurrentIndex(0)
            self.ui.combo_bolt_diameter.setCurrentIndex(0)
            self.ui.combo_angle_section.setCurrentIndex(0)
            self.ui.combo_bolt_type.setCurrentIndex(0)
            self.ui.combo_bolt_grade.setCurrentIndex(0)
            self.ui.txt_fu.clear()
            self.ui.txt_fy.clear()
            self.ui.txt_shear_force.clear()

            self.ui.combo_topangle_section.setCurrentIndex(0)

            self.ui.txt_bolt_shear_capacity.clear()
            self.ui.txt_bolt_bearing_capacity.clear()
            self.ui.txt_bolt_capacity.clear()
            self.ui.txt_no_bolts.clear()
            self.ui.txt_bolt_group_capacity.clear()
            self.ui.txt_bolt_rows.clear()
            self.ui.txt_bolt_cols.clear()
            self.ui.txt_bolt_pitch.clear()
            self.ui.txt_bolt_gauge.clear()
            self.ui.txt_end_distance.clear()
            self.ui.txt_edge_distance.clear()
            self.ui.txt_seat_length.clear()
            self.ui.txt_moment_capacity.clear()
            self.ui.txt_moment_demand.clear()
            self.ui.txt_seat_shear_capacity.clear()
            self.ui.txt_seat_shear_demand.clear()
            self.ui.txt_beam_shear_strength.clear()
            self.ui.txt_top_angle.clear()
        else:
            self.ui.combo_beam_section.setCurrentIndex(0)
            self.ui.combo_column_section.setCurrentIndex(0)
            self.ui.combo_bolt_diameter.setCurrentIndex(0)
            self.ui.combo_angle_section.setCurrentIndex(0)
            self.ui.combo_bolt_type.setCurrentIndex(0)
            self.ui.combo_bolt_grade.setCurrentIndex(0)
            self.ui.txt_fu.clear()
            self.ui.txt_fy.clear()
            self.ui.txt_shear_force.clear()

            self.ui.combo_topangle_section.setCurrentIndex(0)

            self.ui.txt_bolt_shear_capacity.clear()
            self.ui.txt_bolt_bearing_capacity.clear()
            self.ui.txt_bolt_capacity.clear()
            self.ui.txt_no_bolts.clear()
            self.ui.txt_bolt_group_capacity.clear()
            self.ui.txt_bolt_rows.clear()
            self.ui.txt_bolt_cols.clear()
            self.ui.txt_bolt_pitch.clear()
            self.ui.txt_bolt_gauge.clear()
            self.ui.txt_end_distance.clear()
            self.ui.txt_edge_distance.clear()
            self.ui.txt_seat_length.clear()
            self.ui.txt_moment_capacity.clear()
            self.ui.txt_moment_demand.clear()
            self.ui.txt_seat_shear_capacity.clear()
            self.ui.txt_seat_shear_demand.clear()
            self.ui.txt_beam_shear_strength.clear()
            self.ui.txt_top_angle.clear()

    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if uiObj != None:
            self.ui.combo_connectivity.setCurrentIndex(
                self.ui.combo_connectivity.findText(str(uiObj['Member']['Connectivity'])))

            if uiObj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.lbl_beam.setText('Secondary beam *')
                self.ui.lbl_column.setText('Primary beam *')
                self.ui.combo_column_section.addItems(get_beamcombolist())

            self.ui.combo_beam_section.setCurrentIndex(
                self.ui.combo_beam_section.findText(uiObj['Member']['BeamSection']))
            self.ui.combo_column_section.setCurrentIndex(
                self.ui.combo_column_section.findText(uiObj['Member']['ColumnSection']))

            self.ui.txt_fu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txt_fy.setText(str(uiObj['Member']['fy (MPa)']))

            self.ui.txt_shear_force.setText(str(uiObj['Load']['ShearForce (kN)']))

            self.ui.combo_bolt_diameter.setCurrentIndex(
                self.ui.combo_bolt_diameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            combo_type_index = self.ui.combo_bolt_type.findText(str(uiObj['Bolt']['Type']))
            self.ui.combo_bolt_type.setCurrentIndex(combo_type_index)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))
            combo_grade_index = self.ui.combo_bolt_grade.findText(str(uiObj['Bolt']['Grade']))
            self.ui.combo_bolt_grade.setCurrentIndex(combo_grade_index)
            combo_seat_angle_index = self.ui.combo_angle_section.findText(str(uiObj['Angle']['AngleSection']))
            self.ui.combo_angle_section.setCurrentIndex(combo_seat_angle_index)
            combo_top_angle_index = self.ui.combo_topangle_section.findText(str(uiObj['Angle']['TopAngleSection']))
            self.ui.combo_topangle_section.setCurrentIndex(combo_top_angle_index)

    def setimage_connection(self):
        """
        Setting image to connectivity.
        """
        self.ui.lbl_connectivity.show()
        loc = self.ui.combo_connectivity.currentText()
        if loc == "Column flange-Beam web":
            pixmap = QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        elif loc == "Column web-Beam flange":
            picmap = QPixmap(":/newPrefix/images/colW3.png")
            picmap.scaledToHeight(60)
            picmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(picmap)
        elif loc == "Column flange-Beam flange":
            pixmap = QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        else:
            self.ui.lbl_connectivity.hide()

        return True

    def getuser_inputs(self):
        """(nothing) -> Dictionary

        Returns the dictionary object with the user input fields for designing fin plate connection

        """
        uiObj = {"Bolt": {}}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.combo_bolt_diameter.currentText()
        uiObj["Bolt"]["Grade"] = self.ui.combo_bolt_grade.currentText()
        uiObj["Bolt"]["Type"] = str(self.ui.combo_bolt_type.currentText())

        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.combo_beam_section.currentText())
        uiObj['Member']['ColumnSection'] = str(self.ui.combo_column_section.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.combo_connectivity.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txt_fu.text()
        uiObj['Member']['fy (MPa)'] = self.ui.txt_fy.text()

        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = (self.ui.txt_shear_force.text())

        uiObj['Angle'] = {}
        uiObj['Angle']['AngleSection'] = str(self.ui.combo_angle_section.currentText())

        uiObj['Angle']['TopAngleSection'] = str(self.ui.combo_topangle_section.currentText())

        return uiObj

    def save_inputs(self, uiObj):
        """(Dictionary)--> None

        """
        file_name = os.path.join("Connections", "Shear", "SeatedAngle", "saveINPUT.txt")
        inputFile = QFile(file_name)
        if not inputFile.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        pickle.dump(uiObj, inputFile)

    def get_prevstate(self):
        """
        
        Returns:

        """
        file_name = os.path.join("Connections", "Shear", "SeatedAngle", "saveINPUT.txt")

        if os.path.isfile(file_name):
            fileObject = open(file_name, 'r')
            uiObj = pickle.load(fileObject)
            return uiObj
        else:
            return None

    def outputdict(self):
        """Returns the output of design in dictionary object.
        """
        outObj = {'SeatAngle': {}}
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
        outObj['Bolt']["No. of Bolts Provided"] = float(self.ui.txt_no_bolts.text())
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

    def save_design(self, report_summary):
        filename = os.path.join(str(self.folder), "images_html", "Html_Report.html")
        file_name = str(filename)
        self.call_seatangle2D_Drawing("All")

        report_generator_instance = report_generator.ReportGenerator(self.sa_calc_object)
        report_generator_instance.save_html(report_summary, file_name, self.folder)

        # Creates PDF
        if sys.platform == ("win32" or "win64"):
            path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        else:
            path_wkhtmltopdf = r'/usr/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        file_type = "PDF(*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", file_type)
        pdfkit.from_file(filename, fname, configuration=config, options=options)
        QMessageBox.about(self, 'Information', "Report Saved")

    def save_log(self):

        fileName, pat = QFileDialog.getSaveFileName(self, "Save File As", os.path.join(str(self.folder), "LogMessages"),
                                                    "Text files (*.txt)")
        return self.save_file(fileName + ".txt")

    def save_file(self, fileName):
        """(file open for writing)-> boolean
        """
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
        """(NoneType) -> NoneType
        
        Resets all fields in input as well as output window        
        """
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
        """(QWidget) -> NoneType

        This method dock and undock widget(QdockWidget)
        """
        flag = widget.isHidden()
        if flag:
            widget.show()
        else:
            widget.hide()

    def combotype_currentindexchanged(self, index):
        """(Number) -> NoneType
        """
        items = self.grade_type[str(index)]

        self.ui.combo_bolt_grade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))

        self.ui.combo_bolt_grade.addItems(strItems)

    def check_range(self, widget, lblwidget, min_value, max_value):
        """(QlineEdit, QLabel, Number, Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yield Strength) textfields
        """
        textStr = widget.text()
        val = int(textStr)
        if val < min_value or val > max_value:
            QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s' % (min_value, max_value))
            widget.clear()
            widget.setFocus()
            palette = QPalette()
            palette.setColor(QPalette.Foreground, Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QPalette()
            lblwidget.setPalette(palette)

    def display_output(self, outputObj):
        """(dictionary) --> NoneType
        Setting design result values to the respective textboxes in the output window
        """
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                if outputObj[k][key] == "":
                    resultObj = outputObj
                else:
                    resultObj = outputObj

        bolt_shear_capacity = resultObj['Bolt']['Shear Capacity (kN)']
        self.ui.txt_bolt_shear_capacity.setText(str(bolt_shear_capacity))

        bolt_bearing_capacity = resultObj['Bolt']['Bearing Capacity (kN)']
        self.ui.txt_bolt_bearing_capacity.setText(str(bolt_bearing_capacity))

        bolt_capacity = resultObj['Bolt']['Capacity of Bolt (kN)']
        self.ui.txt_bolt_capacity.setText(str(bolt_capacity))

        no_of_bolts = resultObj['Bolt']['No. of Bolts Provided']
        self.ui.txt_no_bolts.setText(str(no_of_bolts))
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

    def displaylog_totextedit(self, commLogicObj):
        """
        This method displaying Design messages(log messages)to textedit widget.
        """
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

    def boltHeadThick_Calculation(self, boltDia):
        """
        This routine takes the bolt diameter and return bolt head thickness as per IS:3757(1989)
       
       bolt Head Dia
        <-------->
        __________
        |        | | T = Thickness
        |________| |
           |  |
           |  |
           |  |
        
        """
        boltHeadThick = {5: 4, 6: 5, 8: 6, 10: 7, 12: 8, 16: 10, 20: 12.5, 22: 14, 24: 15, 27: 17, 30: 18.7, 36: 22.5}
        return boltHeadThick[boltDia]

    def boltHeadDia_Calculation(self, boltDia):
        """
        This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1989)
       
       bolt Head Dia
        <-------->
        __________
        |        |
        |________|
           |  |
           |  |
           |  |
        
        """
        boltHeadDia = {5: 7, 6: 8, 8: 10, 10: 15, 12: 20, 16: 27, 20: 34, 22: 36, 24: 41, 27: 46, 30: 50, 36: 60}
        return boltHeadDia[boltDia]

    def boltLength_Calculation(self, boltDia):
        """
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
        
        """
        boltHeadDia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65, 36: 75}

        return boltHeadDia[boltDia]

    def nutThick_Calculation(self, boltDia):
        """
        Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
        """
        nutDia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23, 30: 25.35,
                  36: 30.65}

        return nutDia[boltDia]

    def init_display(self, backend_str=None, size=(1024, 768)):

        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        from OCC.Display.qtDisplay import qtViewer3d
        self.ui.modelTab = qtViewer3d(self)

        self.setWindowTitle("Seated Angle Connection")
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
            """Centers the window on the screen."""
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

    def call_3DModel(self):
        """
        This routine responsible for displaying 3D Cad model
        :param: boolean
        :return:
        """
        if self.ui.btn3D.isChecked:
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(Qt.Unchecked)
        self.commLogicObj.display_3DModel("Model")

    def call_3DBeam(self):
        """
        Creating and displaying 3D Beam
        """
        self.ui.chkBxBeam.setChecked(Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam")

    def call_3DColumn(self):
        """
        """
        self.ui.chkBxCol.setChecked(Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxSeatAngle.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column")

    def call_3DSeatAngle(self):
        """Displaying Seat Angle in 3D
        """
        self.ui.chkBxSeatAngle.setChecked(Qt.Checked)
        if self.ui.chkBxSeatAngle.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("SeatAngle")

    def unchecked_allChkBox(self):

        self.ui.btn3D.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.chkBxSeatAngle.setChecked(Qt.Unchecked)

    def designParameters(self):
        """
        This routine returns the necessary design parameters.
        """
        self.uiObj = self.getuser_inputs()
        if self.designPrefDialog.saved is not True:
            design_pref = self.designPrefDialog.set_default_para()
        else:
            design_pref = self.designPrefDialog.saved_designPref  # self.designPrefDialog.save_designPref_para()
        self.uiObj.update(design_pref)

        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        dict_angledata = self.fetch_angle_para()
        dict_topangledata = self.fetch_top_angle_para()

        loc = str(self.ui.combo_connectivity.currentText())
        component = "Model"
        bolt_dia = int(self.uiObj["Bolt"]["Diameter (mm)"])

        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        return [self.uiObj, dictbeamdata, dictcoldata, dict_angledata,
                dict_topangledata, loc, component, bolt_R, bolt_T,
                bolt_Ht, nut_T]

    def design_btnclicked(self):
        """
        """
        # TODO input validation
        self.display.EraseAll()
        self.alist = self.designParameters()
        # self.validateInputsOnDesignBtn()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self.unchecked_allChkBox()
        self.commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3],
                                              self.alist[4], self.alist[5], self.alist[6], self.alist[7],
                                              self.alist[8], self.alist[9], self.alist[10], self.display,
                                              self.folder, self.connection)

        self.resultObj = self.commLogicObj.resultObj
        alist = self.resultObj.values()
        self.display_output(self.resultObj)
        self.displaylog_totextedit(self.commLogicObj)
        isempty = [True if val != '' else False for ele in alist for val in ele.values()]

        if isempty[0] is True:
            status = self.resultObj['SeatAngle']['status']
            self.commLogicObj.call_3DModel(status)
            # self.call_seatangle2D_Drawing("All")
        else:
            pass

    def create2Dcad(self, connectivity):
        """ Returns the fuse model of finplate
        """
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
        fileName = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"),
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

        QMessageBox.about(self, 'Information', "File saved")

    def call_seatangle2D_Drawing(self, view):
        """ This routine saves the 2D SVG image as per the connectivity selected
            SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        """
        self.ui.chkBxSeatAngle.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.btn3D.setChecked(Qt.Unchecked)

        if view != 'All':

            if view == "Front":
                filename = os.path.join(self.folder, "images_html", "seatFront.svg")

            elif view == "Side":
                filename = os.path.join(self.folder, "images_html", "seatSide.svg")

            else:
                filename = os.path.join(self.folder, "images_html", "seatTop.svg")

            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, self.folder)

        else:
            fname = ''
            self.commLogicObj.call2D_Drawing(view, fname, self.folder)

    def closeEvent(self, event):
        """
        Closing Seated angle window
        :param event:
        :return:
        """
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()

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

    def ask_questions(self):
        dialog = MyAskQuestion(self)
        dialog.show()

    def open_question(self):
        self.ask_questions()

    def sample_report(self):
        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Report')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == "nt":
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def sample_problem(self):
        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Problems')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == "nt":
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def design_preferences(self):
        self.designPrefDialog.show()

    def bolt_hole_clearance(self):
        self.designPrefDialog.set_bolthole_clearance()

    def call_boltFu(self):
        self.designPrefDialog.set_boltFu()


def set_osdaglogger():
    global logger
    if logger == None:
        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("./Connections/Shear/SeatedAngle/seatangle.log", mode="a")

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
    # For the following to work, set the working directory of seat_angle_main.py to the root Osdag folder
    fh = logging.FileHandler("./Connections/Shear/SeatedAngle/seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/SeatedAngle/log.css"/>''')
    module_setup()

    window = MainController(folder)
    osdagMainWindow.hide()
    window.show()
    window.closed.connect(osdagMainWindow.show)


if __name__ == '__main__':
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    # For the following to work, set the working directory of seat_angle_main.py to the root Osdag folder
    # TODO make paths platform agnostic
    fh = logging.FileHandler("./Connections/Shear/SeatedAngle/seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/SeatedAngle/log.css"/>''')
    app = QApplication(sys.argv)
    module_setup()
    # workspace_folder_path, _ = QFileDialog.getSaveFileName('Select Workspace Directory', "F:\Osdag_workspace")
    workspace_folder_path = 'F:\Osdag_workspace\seated_angle'
    if not os.path.exists(workspace_folder_path):
        os.mkdir(workspace_folder_path, 0755)
    image_folder_path = os.path.join(workspace_folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0755)
    window = MainController(workspace_folder_path)
    window.show()
    sys.exit(app.exec_())
