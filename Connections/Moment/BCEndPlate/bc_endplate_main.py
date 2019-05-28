"""
Started on 22nd April, 2019.

@author: ajmalbabums


Module: Beam to column end plate moment connection
"""

# UI files
from ui_bc_endplate import Ui_MainWindow
from ui_design_preferences import Ui_DesignPreferences
from ui_design_summary import Ui_DesignReport
from ui_plate import Ui_Plate
from ui_stiffener import Ui_Stiffener
from ui_pitch import Ui_Pitch

from svg_window import SvgWindow
from ui_tutorial import Ui_Tutorial
from ui_aboutosdag import Ui_AboutOsdag
from ui_ask_question import Ui_AskQuestion
from bc_endplate_calc import bc_endplate_design
from reportGenerator import save_html
from drawing_2D import ExtendedEndPlate
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from drawing2D_bothway import ExtendedEndPlate
from drawing2D_oneway import OnewayEndPlate
from drawing2D_flush import FlushEndPlate
from drawing2D_WWbothway import ExtendedEndPlate_WW
from drawing2D_WWoneway import OnewayEndPlate_WW
from drawing2D_WWflush import FlushEndPlate_WW

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFontDialog, QFileDialog
from PyQt5.Qt import QColor, QBrush, Qt, QIntValidator, QDoubleValidator, QFile, QTextStream, pyqtSignal, QColorDialog, \
    QPixmap, QPalette
from PyQt5 import QtGui, QtCore, QtWidgets, QtOpenGL
from model import *
import sys
import os
import pickle
import pdfkit
import json
import ConfigParser
import cairosvg
import shutil
import subprocess

from Connections.Component.ISection import ISection
from Connections.Component.nut import Nut
from Connections.Component.bolt import Bolt
from Connections.Component.filletweld import FilletWeld
from Connections.Component.groove_weld import GrooveWeld
from Connections.Component.plate import Plate
from Connections.Component.stiffener_plate import StiffenerPlate

from Connections.Moment.BCEndPlate.extendedBothWays import CADFillet
from Connections.Moment.BCEndPlate.extendedBothWays import CADGroove
from Connections.Moment.BCEndPlate.extendedBothWays import CADColWebFillet
from Connections.Moment.BCEndPlate.extendedBothWays import CADcolwebGroove
from Connections.Moment.BCEndPlate.nutBoltPlacement import NutBoltArray

from Connections.Component.quarterCone import QuarterCone
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from OCC import IGESControl, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone
from OCC.StlAPI import StlAPI_Writer
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs

from utilities import osdag_display_shape
import copy


class MyTutorials(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Tutorial()
        self.ui.setupUi(self)
        self.mainController = parent


class MyAskQuestion(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AskQuestion()
        self.ui.setupUi(self)
        self.mainController = parent


class MyAboutOsdag(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AboutOsdag()
        self.ui.setupUi(self)
        self.mainController = parent


class DesignPreference(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_DesignPreferences()
        self.ui.setupUi(self)
        self.maincontroller = parent

        self.saved = None
        self.ui.combo_design_method.model().item(1).setEnabled(False)
        self.ui.combo_design_method.model().item(2).setEnabled(False)
        self.save_default_para()
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_weldFu.setValidator(dbl_validator)
        self.ui.txt_weldFu.setMaxLength(7)
        self.ui.btn_defaults.clicked.connect(self.save_default_para)
        # self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_save.hide()
        self.ui.btn_close.clicked.connect(self.close_designPref)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

    def save_designPref_para(self):
        uiObj = self.maincontroller.get_user_inputs()
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_type"] = str(self.ui.combo_boltType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
        self.saved_designPref["bolt"]["bolt_fu"] = float(str(self.ui.txt_boltFu.text()))
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

        self.saved_designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())
        self.saved_designPref["design"] = {}
        self.saved_designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
        self.saved = True

        # QMessageBox.about(self, 'Information', "Preferences saved")

        return self.saved_designPref

    def save_default_para(self):
        uiObj = self.maincontroller.get_user_inputs()
        if uiObj["Bolt"]["Grade"] == '':
            pass
        else:
            bolt_grade = float(uiObj["Bolt"]["Grade"])
            bolt_fu = str(self.get_boltFu(bolt_grade))
            self.ui.txt_boltFu.setText(bolt_fu)
        self.ui.combo_boltType.setCurrentIndex(1)
        self.ui.combo_boltHoleType.setCurrentIndex(0)
        designPref = {}
        designPref["bolt"] = {}
        designPref["bolt"]["bolt_type"] = str(self.ui.combo_boltType.currentText())
        designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
        designPref["bolt"]["bolt_fu"] = float(self.ui.txt_boltFu.text())
        self.ui.combo_slipfactor.setCurrentIndex(4)
        designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        self.ui.combo_weldType.setCurrentIndex(0)
        designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        designPref["weld"]["typeof_weld"] = weldType
        designPref["weld"]["safety_factor"] = float(1.25)
        Fu = str(uiObj["Member"]["fu (MPa)"])
        self.ui.txt_weldFu.setText(Fu)
        designPref["weld"]["fu_overwrite"] = self.ui.txt_weldFu.text()
        self.ui.combo_detailingEdgeType.setCurrentIndex(0)
        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        designPref["detailing"]["min_edgend_dist"] = float(1.7)
        self.ui.combo_detailing_memebers.setCurrentIndex(0)
        designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())

        designPref["design"] = {}
        designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
        self.saved = False
        return designPref

    def set_weldFu(self):
        """

		Returns: Set weld Fu based on member fu

		"""
        uiObj = self.maincontroller.get_user_inputs()
        Fu = str(uiObj["Member"]["fu (MPa)"])
        self.ui.txt_weldFu.setText(Fu)

    def set_boltFu(self):
        uiObj = self.maincontroller.get_user_inputs()
        boltGrade = str(uiObj["Bolt"]["Grade"])
        if boltGrade != '':
            boltfu = str(self.get_boltFu(boltGrade))
            self.ui.txt_boltFu.setText(boltfu)
        else:
            pass

    def get_clearance(self):

        uiObj = self.maincontroller.get_user_inputs()
        boltDia = str(uiObj["Bolt"]["Diameter (mm)"])
        if boltDia != 'Select diameter':

            standard_clrnce = {12: 1, 14: 1, 16: 2, 18: 2, 20: 2, 22: 2, 24: 2, 30: 3, 34: 3, 36: 3}
            overhead_clrnce = {12: 3, 14: 3, 16: 4, 18: 4, 20: 4, 22: 4, 24: 6, 30: 8, 34: 8, 36: 8}
            boltHoleType = str(self.ui.combo_boltHoleType.currentText())
            if boltHoleType == "Standard":
                clearance = standard_clrnce[int(boltDia)]
            else:
                clearance = overhead_clrnce[int(boltDia)]

            return clearance
        else:
            pass

    def get_boltFu(self, boltGrade):
        """

		Args:
			boltGrade: Friction Grip Bolt or Bearing Bolt

		Returns: ultimate strength of bolt depending upon grade of bolt chosen

		"""
        # boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040,
        # 		  12.9: 1220}
        boltGrd = float(boltGrade)
        boltFu = int(boltGrd) * 100  # Nominal strength of bolt
        return boltFu

    def close_designPref(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        self.save_designPref_para()
        QCloseEvent.accept()


class PlateDetails(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Plate()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller.designParameters()
        resultObj_plate = bc_endplate_design(uiObj)
        self.ui.txt_plateWidth.setText(str(resultObj_plate["Plate"]["Width"]))
        self.ui.txt_plateHeight.setText(str(resultObj_plate["Plate"]["Height"]))
    # self.ui.txt_plateDemand.setText(str(resultObj_plate["Plate"]["MomentDemand"]))
    # self.ui.txt_plateCapacity.setText(str(resultObj_plate["Plate"]["MomentCapacity"]))


class Stiffener(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Stiffener()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller.designParameters()
        resultObj_plate = bc_endplate_design(uiObj)
        self.ui.txt_stiffnrHeight.setText(str(resultObj_plate["Stiffener"]["Height"]))
        self.ui.txt_stiffnrLength.setText(str(resultObj_plate["Stiffener"]["Length"]))
        self.ui.txt_stiffnrThickness.setText(str(resultObj_plate["Stiffener"]["Thickness"]))


class Pitch(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Pitch()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller.designParameters()
        resultObj_plate = bc_endplate_design(uiObj)
        print "result plate", resultObj_plate
        no_of_bolts = resultObj_plate['Bolt']['NumberOfBolts']
        if no_of_bolts == 8:
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch']))
            self.ui.lbl_1.setText('Pitch')
            self.ui.lbl_mem2.hide()
            self.ui.lbl_mem3.hide()
            self.ui.lbl_mem4.hide()
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lbl_2.hide()
            self.ui.lbl_3.hide()
            self.ui.lbl_4.hide()
            self.ui.lbl_5.hide()
            self.ui.lbl_6.hide()
            self.ui.lbl_7.hide()
            self.ui.lineEdit_pitch2.hide()
            self.ui.lineEdit_pitch3.hide()
            self.ui.lineEdit_pitch4.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
        elif no_of_bolts == 12:
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lbl_1.setText('Pitch_2_3')
            self.ui.lbl_2.setText('Pitch_3_4')
            self.ui.lbl_3.setText('Pitch_4_5')
            self.ui.lbl_mem4.hide()
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lbl_4.hide()
            self.ui.lbl_5.hide()
            self.ui.lbl_6.hide()
            self.ui.lbl_7.hide()
            self.ui.lineEdit_pitch4.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
        elif no_of_bolts == 16:
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lineEdit_pitch4.setText(str(resultObj_plate['Bolt']['Pitch56']))
            self.ui.lineEdit_pitch5.setText(str(resultObj_plate['Bolt']['Pitch67']))
            self.ui.lbl_1.setText('Pitch_2_3')
            self.ui.lbl_2.setText('Pitch_3_4')
            self.ui.lbl_3.setText('Pitch_4_5')
            self.ui.lbl_4.setText('Pitch_5_6')
            self.ui.lbl_5.setText('Pitch_6_7')
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lbl_6.hide()
            self.ui.lbl_7.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
        elif no_of_bolts == 20:
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch12']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lineEdit_pitch4.setText(str(resultObj_plate['Bolt']['Pitch56']))
            self.ui.lineEdit_pitch5.setText(str(resultObj_plate['Bolt']['Pitch67']))
            self.ui.lineEdit_pitch6.setText(str(resultObj_plate['Bolt']['Pitch78']))
            self.ui.lineEdit_pitch7.setText(str(resultObj_plate['Bolt']['Pitch910']))
            self.ui.lbl_1.setText('Pitch_1_2')
            self.ui.lbl_2.setText('Pitch_3_4')
            self.ui.lbl_3.setText('Pitch_4_5')
            self.ui.lbl_4.setText('Pitch_5_6')
            self.ui.lbl_5.setText('Pitch_6_7')
            self.ui.lbl_6.setText('Pitch_7_8')
            self.ui.lbl_7.setText('Pitch_9_10')


class DesignReportDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_DesignReport()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.setWindowTitle("Design Profile")
        self.ui.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.ui.lbl_browse))
        self.ui.btn_saveProfile.clicked.connect(self.saveUserProfile)
        self.ui.btn_useProfile.clicked.connect(self.useUserProfile)
        self.accepted.connect(self.save_inputSummary)

    def save_inputSummary(self):
        report_summary = self.get_report_summary()
        self.maincontroller.save_design(report_summary)

    def getLogoFilePath(self, lblwidget):
        self.ui.lbl_browse.clear()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', "../../ ", 'Images (*.png *.svg *.jpg)', None,
                                                  QFileDialog.DontUseNativeDialog)
        flag = True
        if filename == '':
            flag = False
            return flag
        else:
            base = os.path.basename(str(filename))
            lblwidget.setText(base)
            base_type = base[-4:]
            self.desired_location(filename, base_type)

        return str(filename)

    def desired_location(self, filename, base_type):
        if base_type == ".svg":
            cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.maincontroller.folder), "images_html",
                                                                      "cmpylogoExtendEndplate.svg"))
        else:
            shutil.copyfile(filename,
                            os.path.join(str(self.maincontroller.folder), "images_html", "cmpylogoExtendEndplate.png"))

    def saveUserProfile(self):
        inputData = self.get_report_summary()
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Files',
                                                  os.path.join(str(self.maincontroller.folder), "Profile"), '*.txt')
        if filename == '':
            flag = False
            return flag
        else:
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
                                                  os.path.join(str(self.maincontroller.folder), "Profile"),
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


class Maincontroller(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder
        self.connection = "BCEndPlate"
        self.get_columndata()
        self.get_beamdata()
        self.result_obj = None

        self.designPrefDialog = DesignPreference(self)
        # self.ui.combo_connLoc.model().item(1).setEnabled(False)
        # self.ui.combo_connLoc.model().item(2).setEnabled(False)
        # self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
        # self.ui.combo_beamSec.setCurrentIndex(0)

        # import math
        # beam_section = self.fetchBeamPara()
        # t_w = float(beam_section["tw"])
        # t_f = float(beam_section["T"])
        # print t_w, t_f
        # t_thicker = math.ceil(max(t_w, t_f))
        # t_thicker = (t_thicker / 2.) * 2
        #
        # self.plate_thickness = {'Select plate thickness':[t_thicker, t_thicker+2]}

        self.gradeType = {'Please select type': '', 'Friction Grip Bolt': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)
        self.retrieve_prevstate()
        self.ui.combo_connLoc.currentIndexChanged[str].connect(self.setimage_connection)

        self.ui.btnFront.clicked.connect(lambda: self.call_2D_drawing("Front"))
        self.ui.btnTop.clicked.connect(lambda: self.call_2D_drawing("Top"))
        self.ui.btnSide.clicked.connect(lambda: self.call_2D_drawing("Side"))
        self.ui.combo_diameter.currentIndexChanged[str].connect(self.bolt_hole_clearance)
        self.ui.combo_grade.currentIndexChanged[str].connect(self.call_bolt_fu)
        self.ui.txt_Fu.textChanged.connect(self.call_weld_fu)

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        self.ui.btn_Design.clicked.connect(self.osdag_header)
        self.ui.btn_Reset.clicked.connect(self.reset_btnclicked)
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.actionDesign_Preferences.triggered.connect(self.design_prefer)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialogue)
        self.ui.action_save_input.triggered.connect(self.save_design_inputs)
        self.ui.action_load_input.triggered.connect(self.load_design_inputs)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log_messages)
        self.ui.actionSave_3D_model.triggered.connect(self.save_3D_cad_images)
        self.ui.actionCreate_design_report.triggered.connect(self.design_report)
        self.ui.actionChange_background.triggered.connect(self.show_color_dialog)
        self.ui.actionSave_Front_View.triggered.connect(lambda: self.call_2D_drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.call_2D_drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.call_2D_drawing("Top"))
        self.ui.actionShow_all.triggered.connect(lambda: self.call_3DModel("gradient_bg"))
        self.ui.actionShow_column.triggered.connect(lambda: self.call_3DColumn("gradient_bg"))
        self.ui.actionShow_beam.triggered.connect(lambda: self.call_3DBeam("gradient_bg"))
        self.ui.actionShow_connector.triggered.connect(lambda: self.call_3DConnector("gradient_bg"))
        self.ui.actionSave_current_image.triggered.connect(self.save_CAD_images)
        self.ui.actionZoom_in.triggered.connect(self.call_zoomin)
        self.ui.actionZoom_out.triggered.connect(self.call_zoomout)
        self.ui.actionPan.triggered.connect(self.call_pannig)
        self.ui.actionRotate_3D_model.triggered.connect(self.call_rotation)
        self.ui.actionClear.triggered.connect(self.clear_log_messages)
        self.ui.actionAbout_Osdag_2.triggered.connect(self.open_about_osdag)
        self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_ask_question)
        self.ui.actionSample_Tutorials.triggered.connect(self.open_tutorials)
        self.ui.actionDesign_examples.triggered.connect(self.design_examples)

        self.ui.btn_pitchDetail.clicked.connect(self.pitch_details)
        self.ui.btn_plateDetail.clicked.connect(self.plate_details)
        self.ui.btn_stiffnrDetail.clicked.connect(self.stiffener_details)
        self.ui.btn_CreateDesign.clicked.connect(self.design_report)

        self.ui.btn3D.clicked.connect(lambda: self.call_3DModel("gradient_bg"))
        self.ui.chkBx_columnSec.clicked.connect(lambda: self.call_3DColumn("gradient_bg"))
        self.ui.chkBx_beamSec.clicked.connect(lambda: self.call_3DBeam("gradient_bg"))
        self.ui.chkBx_connector.clicked.connect(lambda: self.call_3DConnector("gradient_bg"))

        validator = QIntValidator()

        doubl_validator = QDoubleValidator()
        self.ui.txt_Fu.setValidator(doubl_validator)
        self.ui.txt_Fy.setValidator(doubl_validator)
        self.ui.txt_Moment.setValidator(doubl_validator)
        self.ui.txt_Shear.setValidator(doubl_validator)
        self.ui.txt_Axial.setValidator(doubl_validator)

        min_fu = 290
        max_fu = 780
        self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))
        self.ui.txt_Fu.editingFinished.connect(
            lambda: self.validate_fu_fy(self.ui.txt_Fu, self.ui.txt_Fy, self.ui.txt_Fu, self.ui.lbl_fu))

        min_fy = 165
        max_fy = 650
        self.ui.txt_Fy.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fy, min_fy, max_fy))
        self.ui.txt_Fy.editingFinished.connect(
            lambda: self.validate_fu_fy(self.ui.txt_Fu, self.ui.txt_Fy, self.ui.txt_Fy, self.ui.lbl_fy))

        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())
        self.uiObj = None
        self.fuse_model = None
        self.resultObj = None
        self.disable_buttons()

	def on_change(self, newIndex):
			if newIndex == "Groove Weld (CJP)":
				self.ui.combo_flangeSize.setEnabled(False)
				self.ui.combo_webSize.setEnabled(False)
    def init_display(self, backend_str=None, size=(1024, 768)):
        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        from OCC.Display.qtDisplay import qtViewer3d
        self.ui.modelTab = qtViewer3d(self)

        # ========================  CAD ========================
        # self.setWindowTitle("Osdag Finplate")
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")
        self.ui.modelTab.InitDriver()
        # ===========================================================
        display = self.ui.modelTab._display
        display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        # ========================  CAD ========================
        display.display_trihedron()
        # ===========================================================
        display.View.SetProj(1, 1, 1)

        def centerOnScreen(self):
            '''Centers the window on the screen.'''
            resolution = QtGui.QDesktopWidget().screenGeometry()
            self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                      (resolution.height() / 2) - (self.frameSize().height() / 2))

        def start_display():
            self.ui.modelTab.raise_()

        return display, start_display

    def save_design_inputs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Design", os.path.join(str(self.folder), "untitled.osi"),
                                                  "Input Files(*.osi)")
        if not filename:
            return
        try:
            out_file = open(str(filename), 'wb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % filename)
            return
        json.dump(self.uiObj, out_file)
        out_file.close()
        pass

    def load_design_inputs(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Design", str(self.folder), "(*.osi)")
        if not filename:
            return
        try:
            in_file = open(str(filename), 'rb')
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % filename)
            return
        ui_obj = json.load(in_file)
        self.set_dict_touser_inputs(ui_obj)

    def save_log_messages(self):
        filename, pat = QFileDialog.getSaveFileName(self, "Save File As", os.path.join(str(self.folder), "LogMessages"),
                                                    "Text files (*.txt)")
        return self.save_file(filename + ".txt")

    def save_file(self, filename):
        """

		Args:
			filename: file name

		Returns: open file for writing

		"""
        fname = QFile(filename)
        if not fname.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (filename, fname.errorString()))
            return
        outf = QTextStream(fname)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

    def save_design(self, report_summary):
        status = self.resultObj['Bolt']['status']
        if status is True:
            self.call_3DModel("white_bg")
            data = os.path.join(str(self.folder), "images_html", "3D_Model.png")
            self.display.ExportToImage(data)
            self.display.FitAll()
        else:
            pass

        filename = os.path.join(str(self.folder), "images_html", "Html_Report.html")
        file_name = str(filename)
        self.call_designreport(file_name, report_summary)

        # Creates PDF
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'Osdag.config'))
        wkhtmltopdf_path = config.get('wkhtml_path', 'path1')

        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        file_type = "PDF(*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", file_type)
        fname = str(fname)
        flag = True
        if fname == '':
            flag = False
            return flag
        else:
            pdfkit.from_file(filename, fname, configuration=config, options=options)
            QMessageBox.about(self, 'Information', "Report Saved")

    def call_designreport(self, fileName, report_summary):
        self.alist = self.designParameters()
        self.result = bc_endplate_design(self.alist)
        print "resultobj", self.result
        self.column_data = self.fetchColumnPara()
        self.beam_data = self.fetchBeamPara()
        save_html(self.result, self.alist, self.column_data, self.beam_data, fileName, report_summary, self.folder)

    def get_user_inputs(self):
        uiObj = {}
        uiObj["Member"] = {}
        uiObj["Member"]["Connectivity"] = str(self.ui.combo_connect.currentText())
        uiObj["Member"]["EndPlate_type"] = str(self.ui.combo_connLoc.currentText())
        uiObj["Member"]["ColumnSection"] = str(self.ui.combo_columnSec.currentText())
        uiObj["Member"]["BeamSection"] = str(self.ui.combo_beamSec.currentText())
        uiObj["Member"]["fu (MPa)"] = self.ui.txt_Fu.text()
        uiObj["Member"]["fy (MPa)"] = self.ui.txt_Fy.text()

        uiObj["Load"] = {}
        uiObj["Load"]["ShearForce (kN)"] = self.ui.txt_Shear.text()
        uiObj["Load"]["Moment (kNm)"] = self.ui.txt_Moment.text()
        uiObj["Load"]["AxialForce (kN)"] = self.ui.txt_Axial.text()

        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.combo_diameter.currentText()
        uiObj["Bolt"]["Grade"] = self.ui.combo_grade.currentText()
        uiObj["Bolt"]["Type"] = self.ui.combo_type.currentText()

        uiObj["Plate"] = {}
        uiObj["Plate"]["Thickness (mm)"] = str(self.ui.combo_plateThick.currentText())

        uiObj["Weld"] = {}


        uiObj["Weld"]["Flange (mm)"] = str(self.ui.combo_flangeSize.currentText())
        uiObj["Weld"]["Web (mm)"] = str(self.ui.combo_webSize.currentText())

        uiObj["Connection"] = self.connection

        return uiObj


    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

    def design_prefer(self):
        self.designPrefDialog.show()

    def bolt_hole_clearance(self):
        self.designPrefDialog.get_clearance()

    def call_bolt_fu(self):
        self.designPrefDialog.set_boltFu()

    def call_weld_fu(self):
        self.designPrefDialog.set_weldFu()

    def closeEvent(self, event):
        """

		Args:
			event: Yes or No

		Returns: Ask for the confirmation while closing the window

		"""
        uiInput = self.designParameters()
        self.save_inputs_totext(uiInput)
        action = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if action == QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()

    def save_inputs_totext(self, uiObj):
        """

		Args:
			uiObj: User inputs

		Returns: Save the user input to txt format

		"""
        input_file = QFile(os.path.join("Connections", "Moment", "BCEndPlate", "saveINPUT.txt"))
        if not input_file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s: \n%s"
                                % (input_file.fileName(), input_file.errorString()))
        pickle.dump(uiObj, input_file)

    def get_prevstate(self):
        """

		Returns: Read for the previous user inputs design

		"""
        filename = os.path.join("Connections", "Moment", "BCEndPlate", "saveINPUT.txt")
        if os.path.isfile(filename):
            file_object = open(filename, 'r')
            uiObj = pickle.load(file_object)
            return uiObj
        else:
            return None

    def retrieve_prevstate(self):
        """

		Returns: Retrieve the previous user inputs

		"""
        uiObj = self.get_prevstate()
        self.set_dict_touser_inputs(uiObj)

    def set_dict_touser_inputs(self, uiObj):
        """

		Args:
			uiObj: User inputs

		Returns: Set the dictionary to user inputs

		"""

        if uiObj is not None:
            if uiObj["Connection"] != "BCEndPlate":
                QMessageBox.information(self, "Information",
                                        "You can load this input file only from the corresponding design problem")
                return

            self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connect.findText(uiObj["Member"]["Connectivity"]))
            self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(str(uiObj["Member"]["EndPlate_type"])))
            if uiObj["Member"]["EndPlate_type"] == "Flush" or "Extended one way" or "Extended both ways":
                # self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connect.findText(uiObj["Member"]["Connectivity"]))
                self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(uiObj["Member"]["EndPlate_type"]))
                self.ui.combo_columnSec.setCurrentIndex(
                    self.ui.combo_columnSec.findText(uiObj["Member"]["ColumnSection"]))
                self.ui.combo_beamSec.setCurrentIndex(self.ui.combo_beamSec.findText(uiObj["Member"]["BeamSection"]))
                self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
                self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
                self.ui.txt_Shear.setText(str(uiObj["Load"]["ShearForce (kN)"]))
                self.ui.txt_Axial.setText(str(uiObj["Load"]["AxialForce (kN)"]))
                self.ui.txt_Moment.setText(str(uiObj["Load"]["Moment (kNm)"]))
                self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
                self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
                self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
                self.ui.combo_plateThick.setCurrentIndex(
                    self.ui.combo_plateThick.findText(uiObj["Plate"]["Thickness (mm)"]))
                self.ui.combo_weld_method.setCurrentIndex(self.ui.combo_weld_method.findText(uiObj["Weld"]["Method"]))
                self.ui.combo_flangeSize.setCurrentIndex(
                    self.ui.combo_flangeSize.findText(uiObj["Weld"]["Flange (mm)"]))
                self.ui.combo_webSize.setCurrentIndex(self.ui.combo_webSize.findText(uiObj["Weld"]["Web (mm)"]))

                self.designPrefDialog.ui.combo_boltType.setCurrentIndex(
                    self.designPrefDialog.ui.combo_boltType.findText(uiObj["bolt"]["bolt_type"]))
                self.designPrefDialog.ui.combo_boltHoleType.setCurrentIndex(
                    self.designPrefDialog.ui.combo_boltHoleType.findText(uiObj["bolt"]["bolt_hole_type"]))
                self.designPrefDialog.ui.txt_boltFu.setText(str(uiObj["bolt"]["bolt_fu"]))
                self.designPrefDialog.ui.combo_slipfactor.setCurrentIndex(
                    self.designPrefDialog.ui.combo_slipfactor.findText(str(uiObj["bolt"]["slip_factor"])))
                self.designPrefDialog.ui.combo_weldType.setCurrentIndex(
                    self.designPrefDialog.ui.combo_weldType.findText(uiObj["weld"]["typeof_weld"]))
                self.designPrefDialog.ui.txt_weldFu.setText(str(uiObj["weld"]["fu_overwrite"]))
                self.designPrefDialog.ui.combo_detailingEdgeType.setCurrentIndex(
                    self.designPrefDialog.ui.combo_detailingEdgeType.findText(uiObj["detailing"]["typeof_edge"]))
                self.designPrefDialog.ui.combo_detailing_memebers.setCurrentIndex(
                    self.designPrefDialog.ui.combo_detailing_memebers.findText(uiObj["detailing"]["is_env_corrosive"]))
                self.designPrefDialog.ui.combo_design_method.setCurrentIndex(
                    self.designPrefDialog.ui.combo_design_method.findText(uiObj["design"]["design_method"]))

        else:
            pass

    def designParameters(self):
        """

		Returns: Design preference inputs

		"""
        self.uiObj = self.get_user_inputs()
	self.ui.combo_weld_method.currentTextChanged.connect(self.on_change)
        # if self.designPrefDialog.saved is not True:
        # 	design_pref = self.designPrefDialog.save_default_para()
        # else:
        design_pref = self.designPrefDialog.save_designPref_para()
        self.uiObj.update(design_pref)
        return self.uiObj

    def setimage_connection(self):
        '''
		Setting image to connectivity.
		'''
        self.ui.lbl_connectivity.show()
        loc = self.ui.combo_connLoc.currentText()
        loc2 = self.ui.combo_connect.currentText()

        if loc == "Extended both ways" and loc2 == "Column flange-Beam web":
            pixmap = QPixmap(":/newPrefix/images/webextnboth.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        elif loc == "Flush end plate" and loc2 == "Column flange-Beam web":
            pixmap = QPixmap(":/newPrefix/images/webflush.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        elif loc == "Extended one way" and loc2 == "Column flange-Beam web":
            pixmap = QPixmap(":/newPrefix/images/webextnone.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        elif loc == "Extended both ways" and loc2 == "Column web-Beam web":
            pixmap = QPixmap(":/newPrefix/images/fextnboth.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        elif loc == "Flush end plate" and loc2 == "Column web-Beam web":
            pixmap = QPixmap(":/newPrefix/images/ff.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        else:
            pixmap = QPixmap(":/newPrefix/images/fextnone.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)

        return True

    def generate_incomplete_string(self, incomplete_list):
        """

		Args:
			incomplete_list: list of fields that are not selected or entered

		Returns:
			error string that has to be displayed

		"""

        # The base string which should be displayed
        information = "Please input the following required field"
        if len(incomplete_list) > 1:
            # Adds 's' to the above sentence if there are multiple missing input fields
            information += "s"
        information += ": "

        # Loops through the list of the missing fields and adds each field to the above sentence with a comma
        for item in incomplete_list:
            information = information + item + ", "

        # Removes the last comma
        information = information[:-2]
        information += "."

        return information

    def validate_inputs_on_design_btn(self):
        flag = True
        incomplete_list = []
        state = self.setimage_connection()
        if state is True:
            if self.ui.combo_connect.currentIndex() == 0:
                incomplete_list.append("Connectivity")
        else:
            pass

        if self.ui.combo_connLoc.currentIndex() == 0:
            incomplete_list.append("EndPlate_type")

        if self.ui.combo_columnSec.currentIndex() == 0:
            incomplete_list.append("Column section")

        if self.ui.combo_beamSec.currentIndex() == 0:
            incomplete_list.append("Beam section")

        if self.ui.txt_Fu.text() == "":
            incomplete_list.append("Ultimate strength")

        if self.ui.txt_Fy.text() == "":
            incomplete_list.append("Yield strength")

        # if self.ui.txt_Axial.text() == '' or float(self.ui.txt_Axial.text()) == 0:
        #	incomplete_list.append("Axial force")

        if self.ui.txt_Moment.text() == '' or float(self.ui.txt_Moment.text()) == 0:
            incomplete_list.append("Moment")

        if self.ui.txt_Shear.text() == '':
            incomplete_list.append("Shear force")

        if self.ui.combo_diameter.currentIndex() == 0:
            incomplete_list.append("Diameter of bolt")

        if self.ui.combo_type.currentIndex() == 0:
            incomplete_list.append("Type of bolt")

        if self.ui.combo_plateThick.currentIndex() == 0:
            incomplete_list.append("Flange splice plate thickness")

        if self.ui.combo_webSize.currentIndex() == 0:
            incomplete_list.append("Web weld thickness")


        if self.ui.combo_flangeSize.currentIndex() == 0:
            incomplete_list.append("Flange weld thickness")

        if len(incomplete_list) > 0:
            flag = False
            QMessageBox.information(self, "Information", self.generate_incomplete_string(incomplete_list))

        return flag

    def design_btnclicked(self):
        """

		Returns:

		"""
        if self.validate_inputs_on_design_btn() is not True:
            return
        self.alist = self.designParameters()
        self.outputs = bc_endplate_design(self.alist)
        print "output list ", self.outputs

        self.ui.outputDock.setFixedSize(310, 710)
        self.enable_buttons()

        a = self.outputs[self.outputs.keys()[0]]
        self.resultObj = self.outputs
        alist = self.resultObj.values()

        self.display_output(self.outputs)
        self.display_log_to_textedit()
        isempty = [True if val != '' else False for ele in alist for val in ele.values()]

        if isempty[0] == True:
            status = self.resultObj['Bolt']['status']
            self.call_3DModel("gradient_bg")
            if status is True:
                self.call_2D_drawing("All")
            else:
                self.ui.btn_pitchDetail.setDisabled(False)
                self.ui.btn_plateDetail.setDisabled(False)
                self.ui.btn_stiffnrDetail.setDisabled(False)
                self.ui.chkBx_connector.setDisabled(True)
                self.ui.chkBx_columnSec.setDisabled(True)
                self.ui.chkBx_beamSec.setDisabled(True)
                self.ui.btn3D.setDisabled(True)

    def display_output(self, outputObj):
        for k in outputObj.keys():
            for value in outputObj.values():
                if outputObj.items() == " ":
                    resultObj = outputObj
                else:
                    resultObj = outputObj
        print resultObj

        critical_tension = resultObj["Bolt"]["TensionBolt"]
        self.ui.txt_tensionCritical.setText(str(critical_tension))

        tension_capacity = resultObj["Bolt"]["TensionCapacity"]
        self.ui.txt_tensionCapacity.setText(str(tension_capacity))

        shear_capacity = resultObj["Bolt"]["ShearCapacity"]
        self.ui.txt_shearCapacity.setText(str(shear_capacity))

        bearing_capacity = resultObj["Bolt"]["BearingCapacity"]
        self.ui.txt_bearCapacity.setText(str(bearing_capacity))

        combined_capacity = resultObj["Bolt"]["CombinedCapacity"]
        self.ui.txt_boltgrpcapacity.setText(str(combined_capacity))

        bolt_capacity = resultObj["Bolt"]["BoltCapacity"]
        self.ui.txt_boltcapacity.setText(str(bolt_capacity))

        bolts_required = resultObj["Bolt"]["NumberOfBolts"]
        self.ui.txt_noBolts.setText(str(bolts_required))

        # bolts_in_rows = resultObj["Bolt"]["NumberOfRows"]
        bolts_in_rows = 1
        self.ui.txt_rowBolts.setText(str(bolts_in_rows))

        # pitch = resultObj["Bolt"]["Pitch"]
        # self.ui.txt_pitch.setText(str(pitch))

        # gauge = resultObj["Bolt"]["Gauge"]
        gauge = 0.0
        self.ui.txt_gauge.setText(str(gauge))

        cross_centre_gauge = resultObj["Bolt"]["CrossCentreGauge"]
        self.ui.txt_crossGauge.setText(str(cross_centre_gauge))

        end_distance = resultObj["Bolt"]["End"]
        self.ui.txt_endDist.setText(str(end_distance))

        edge_distance = resultObj["Bolt"]["Edge"]
        self.ui.txt_edgeDist.setText(str(edge_distance))

        # weld_stress_flange = resultObj["Weld"]["FlangeStress"]
        weld_stress_flange = 0.0
        self.ui.txt_criticalFlange.setText(str(weld_stress_flange))

        # weld_stress_web = resultObj["Weld"]["WebStress"]
        weld_stress_web = 0.0
        self.ui.txt_criticalWeb.setText(str(weld_stress_web))

    def display_log_to_textedit(self):
        file = QFile(os.path.join('Connections', 'Moment', 'BCEndPlate', 'extnd.log'))
        if not file.open(QtCore.QIODevice.ReadOnly):
            QMessageBox.information(None, 'info', file.errorString())
        stream = QtCore.QTextStream(file)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscroll_bar = self.ui.textEdit.verticalScrollBar()
        vscroll_bar.setValue(vscroll_bar.maximum())
        file.close()

    def disable_buttons(self):
        self.ui.btn_CreateDesign.setEnabled(False)
        self.ui.btn_SaveMessages.setEnabled(False)
        self.ui.btnFront.setEnabled(False)
        self.ui.btnTop.setEnabled(False)
        self.ui.btnSide.setEnabled(False)
        self.ui.btn3D.setEnabled(False)
        self.ui.chkBx_columnSec.setEnabled(False)
        self.ui.chkBx_beamSec.setEnabled(False)
        self.ui.chkBx_connector.setEnabled(False)
        self.ui.btn_pitchDetail.setEnabled(False)
        self.ui.btn_plateDetail.setEnabled(False)
        self.ui.btn_stiffnrDetail.setEnabled(False)

        self.ui.action_save_input.setEnabled(False)
        self.ui.actionCreate_design_report.setEnabled(False)
        self.ui.actionSave_3D_model.setEnabled(False)
        self.ui.actionSave_log_messages.setEnabled(False)
        self.ui.actionSave_current_image.setEnabled(False)
        self.ui.actionSave_Front_View.setEnabled(False)
        self.ui.actionSave_Side_View.setEnabled(False)
        self.ui.actionSave_Top_View.setEnabled(False)
        self.ui.menuGraphics.setEnabled(True)

    def enable_buttons(self):
        self.ui.btn_CreateDesign.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)
        self.ui.btnFront.setEnabled(True)
        self.ui.btnTop.setEnabled(True)
        self.ui.btnSide.setEnabled(True)
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBx_columnSec.setEnabled(True)
        self.ui.chkBx_beamSec.setEnabled(True)
        self.ui.chkBx_connector.setEnabled(True)
        self.ui.btn_pitchDetail.setEnabled(True)
        self.ui.btn_plateDetail.setEnabled(True)
        self.ui.btn_stiffnrDetail.setEnabled(True)

        self.ui.action_save_input.setEnabled(True)
        self.ui.actionCreate_design_report.setEnabled(True)
        self.ui.actionSave_3D_model.setEnabled(True)
        self.ui.actionSave_log_messages.setEnabled(True)
        self.ui.actionSave_current_image.setEnabled(True)
        self.ui.actionSave_Front_View.setEnabled(True)
        self.ui.actionSave_Side_View.setEnabled(True)
        self.ui.actionSave_Top_View.setEnabled(True)
        self.ui.menuGraphics.setEnabled(True)

    def reset_btnclicked(self):
        """

		Returns:

		"""
        self.ui.combo_connect.setCurrentIndex(0)
        self.ui.combo_connLoc.setCurrentIndex(0)
        self.ui.combo_columnSec.setCurrentIndex(0)
        self.ui.combo_beamSec.setCurrentIndex(0)
        self.ui.lbl_connectivity.clear()
        self.ui.txt_Fu.clear()
        self.ui.txt_Fy.clear()
        self.ui.txt_Axial.clear()
        self.ui.txt_Shear.clear()
        self.ui.txt_Moment.clear()
        self.ui.combo_diameter.setCurrentIndex(0)
        self.ui.combo_type.setCurrentIndex(0)
        self.ui.combo_grade.setCurrentIndex(0)
        self.ui.combo_plateThick.setCurrentIndex(0)
        self.ui.combo_flangeSize.setCurrentIndex(0)
        self.ui.combo_webSize.setCurrentIndex(0)

        self.ui.txt_tensionCritical.clear()
        self.ui.txt_tensionCapacity.clear()
        self.ui.txt_shearCapacity.clear()
        self.ui.txt_bearCapacity.clear()
        self.ui.txt_boltcapacity.clear()
        self.ui.txt_boltgrpcapacity.clear()
        self.ui.txt_noBolts.clear()
        self.ui.txt_rowBolts.clear()
        self.ui.txt_gauge.clear()
        self.ui.txt_crossGauge.clear()
        self.ui.txt_endDist.clear()
        self.ui.txt_edgeDist.clear()
        self.ui.txt_criticalFlange.clear()
        self.ui.txt_criticalWeb.clear()

        self.ui.btn_pitchDetail.setDisabled(True)
        self.ui.btn_plateDetail.setDisabled(True)
        self.ui.btn_stiffnrDetail.setDisabled(True)

        self.display.EraseAll()
        self.designPrefDialog.save_default_para()

    def get_columndata(self):
        """Fetch  old and new column sections from "Intg_osdag" database.
		Returns:
        	"""
        columndata = get_columncombolist()
        old_colList = get_oldcolumncombolist()

        self.ui.combo_columnSec.addItems(columndata)
        combo_section = self.ui.combo_columnSec
        self.color_oldDatabase_section(old_colList, columndata, combo_section)

    def get_beamdata(self):
        loc = self.ui.combo_connLoc.currentText()
        beamdata = get_beamcombolist()
        old_beamdata = get_oldbeamcombolist()
        combo_section = ''
        self.ui.combo_beamSec.addItems(beamdata)
        combo_section = self.ui.combo_beamSec
        self.color_oldDatabase_section(old_beamdata, beamdata, combo_section)

    def color_oldDatabase_section(self, old_section, intg_section, combo_section):
        """

		Args:
			old_section: Old database
			intg_section: Integrated database
			combo_section: Contents of database

		Returns: Differentiate the database by color code

		"""
        for col in old_section:
            if col in intg_section:
                indx = intg_section.index(str(col))
                combo_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

        duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]
        for i in duplicate:
            combo_section.setItemData(i, QBrush(QColor("red")), Qt.TextColorRole)

    def fetchColumnPara(self):
        columndata_sec = self.ui.combo_columnSec.currentText()
        dictcolumndata = get_columndata(columndata_sec)
        return dictcolumndata

    def fetchBeamPara(self):
        beamdata_sec = self.ui.combo_beamSec.currentText()
        dictbeamdata = get_beamdata(beamdata_sec)
        return dictbeamdata

    def populate_weld_thk_flange(self):
        """

		Returns: The list of weld thickness in Gui

		"""
        if str(self.ui.combo_beamSec.currentText()) == "Select section":
            self.ui.combo_plateThick.setCurrentIndex(0)
            self.ui.combo_flangeSize.setCurrentIndex(0)
            return

        else:
            newlist = []
            newlist.append("Select thickness")
            weldlist = [3, 4, 5, 6, 8, 10, 12, 16, 18, 20]
            dictbeamdata = self.fetchBeamPara()
            beam_tw = float(dictbeamdata["tw"])
            plate_thickness = str(self.ui.combo_plateThick.currentText())

            if plate_thickness != "Select plate thickness":
                plate_thick = float(plate_thickness)

                if str(self.ui.combo_connLoc.currentText()) == "Extended both ways":
                    if str(self.ui.combo_beamSec.currentText()) == "Select section":
                        self.ui.combo_flangeSize.clear()
                        return
                    else:
                        beam_tf = float(dictbeamdata["T"])
                        beam_tw = float(dictbeamdata["tw"])
                        # column_tf = float(dictbeamdata["T"])
                        thicker_part = max(beam_tf, beam_tw, plate_thick)

                if thicker_part in range(0, 11):
                    weld_index = weldlist.index(3)
                    newlist.extend(weldlist[weld_index:])
                elif thicker_part in range(11, 21):
                    weld_index = weldlist.index(5)
                    newlist.extend(weldlist[weld_index:])
                elif thicker_part in range(21, 33):
                    weld_index = weldlist.index(6)
                    newlist.extend(weldlist[weld_index:])
                else:
                    weld_index = weldlist.index(8)
                    newlist.extend(weldlist[weld_index:])

                self.ui.combo_flangeSize.clear()
                for element in newlist[:]:
                    self.ui.combo_flangeSize.addItem(str(element))
            else:
                pass

    def combotype_current_index_changed(self, index):
        """

		Args:
			index: Number

		Returns: Types of Grade

		"""
        items = self.gradeType[str(index)]
        if items != 0:
            self.ui.combo_grade.clear()
            stritems = []
            for val in items:
                stritems.append(str(val))

            self.ui.combo_grade.addItems(stritems)
        else:
            pass

    def check_range(self, widget, min_val, max_val):
        """

		Args:
			widget: Fu , Fy lineedit
			min_val: min value
			max_val: max value

		Returns: Check for the value mentioned for the given range

		"""
        text_str = widget.text()
        text_str = int(text_str)
        if (text_str < min_val or text_str > max_val or text_str == ''):
            QMessageBox.about(self, "Error", "Please enter a value between %s-%s" % (min_val, max_val))
            widget.clear()
            widget.setFocus()

    def validate_fu_fy(self, fu_widget, fy_widget, current_widget, lblwidget):
        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) greater than F_y (Yeild Strength) textfields
        '''
        try:
            fu_value = float(fu_widget.text())
        except ValueError:
            fu_value = 0.0

        try:
            fy_value = float(fy_widget.text())
        except ValueError:
            fy_value = 0.0

        if fy_value > fu_value:
            QMessageBox.about(self, 'Error', 'Yield strength (fy) cannot be greater than ultimate strength (fu)')
            current_widget.clear()
            current_widget.setFocus()
            palette = QPalette()
            palette.setColor(QPalette.Foreground, Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QPalette()
            lblwidget.setPalette(palette)

    def call_2D_drawing(self, view):
        """

		Args:
			view: Front, Side & Top view of 2D svg drawings

		Returns: SVG image created through svgwrite package which takes design INPUT and OUTPUT
				 parameters from Extended endplate GUI

		"""
        self.alist = self.designParameters()
        self.result_obj = bc_endplate_design(self.alist)
        self.column_data = self.fetchColumnPara()
        self.beam_data = self.fetchBeamPara()

        # TODO added endplate_type here, find new way to redue this lines

        if self.alist['Member']['Connectivity'] == "Column web-Beam web":
            # conn_type = 'col_web_connectivity'
            if self.alist['Member']['EndPlate_type'] == "Extended both ways":
                self.endplate_type = "both_way"
                beam_beam = ExtendedEndPlate_WW(self.alist, self.result_obj, self.column_data, self.beam_data,
                                                self.folder)
            elif self.alist['Member']['EndPlate_type'] == "Extended one way":
                self.endplate_type = "one_way"
                beam_beam = OnewayEndPlate_WW(self.alist, self.result_obj, self.column_data, self.beam_data,
                                              self.folder)
            else:
                self.endplate_type = "flush"
                beam_beam = FlushEndPlate_WW(self.alist, self.result_obj, self.column_data, self.beam_data, self.folder)
        else:  # "Column flange-Beam web"
            # conn_type = 'col_flange_connectivity'
            if self.alist['Member']['EndPlate_type'] == "Extended one way":
                self.endplate_type = "one_way"
                beam_beam = OnewayEndPlate(self.alist, self.result_obj, self.column_data, self.beam_data, self.folder)
            elif self.alist['Member']['EndPlate_type'] == "Flush end plate":
                self.endplate_type = "flush"
                beam_beam = FlushEndPlate(self.alist, self.result_obj, self.column_data, self.beam_data, self.folder)
            else:  # uiObj['Member']['EndPlate_type'] == "Extended both ways":
                self.endplate_type = "both_way"
                beam_beam = ExtendedEndPlate(self.alist, self.result_obj, self.column_data, self.beam_data, self.folder)

        # beam_beam = ExtendedEndPlate(self.alist, self.result_obj, self.column_data, self.beam_data, self.folder)
        status = self.resultObj['Bolt']['status']
        if status is True:
            if view != "All":
                if view == "Front":
                    filename = os.path.join(self.folder, "images_html", "extendFront.svg")

                elif view == "Side":
                    filename = os.path.join(self.folder, "images_html", "extendSide.svg")

                else:
                    filename = os.path.join(self.folder, "images_html", "extendTop.svg")

                beam_beam.save_to_svg(filename, view)
                svg_file = SvgWindow()
                svg_file.call_svgwindow(filename, view, self.folder)
            else:
                fname = ''
                beam_beam.save_to_svg(fname, view)
        else:
            QMessageBox.about(self, 'Information', 'Design Unsafe: %s view cannot be viewed' % (view))

    def dockbtn_clicked(self, widgets):
        """

		Args:
			widgets: Input , Output dock

		Returns: Dock & undock the widgets

		"""
        flag = widgets.isHidden()
        if flag:
            widgets.show()
        else:
            widgets.hide()

    def show_font_dialogue(self):
        font, ok = QFontDialog.getFont()
        if ok:
            # self.ui.textEdit.setFont()
            self.ui.textEdit.setFont(font)

    def pitch_details(self):
        section = Pitch(self)
        section.show()

    def plate_details(self):
        section = PlateDetails(self)
        section.show()

    def stiffener_details(self):
        section = Stiffener(self)
        section.show()

    def design_report(self):
        design_report_dialog = DesignReportDialog(self)
        design_report_dialog.show()

    # fileName = ("Connections\Moment\BCEndPlate\Html_Report.html")
    # fileName = str(fileName)
    # self.alist = self.designParameters()
    # self.result = bc_endplate_design(self.alist)
    # print "result_obj", self.result
    # self.beam_data = self.fetchBeamPara()
    # save_html(self.result, self.alist, self.beam_data, fileName)

    # ===========================  CAD ===========================
    def show_color_dialog(self):

        col = QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

    def create_2D_CAD(self):
        '''

		Returns: The 3D model of extendedplate depending upon component selected

		'''
        self.ExtObj = self.create_extended_both_ways()
        if self.component == "Column":
            final_model = self.ExtObj.get_column_models()

        elif self.component == "Beam":
            final_model = self.ExtObj.get_beam_models()

        elif self.component == "Connector":
            cadlist = self.ExtObj.get_connector_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        else:
            cadlist = self.ExtObj.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

        return final_model

    def save_3D_cad_images(self):
        '''

		Returns: Save 3D CAD images in *igs, *step, *stl, *brep format

		'''
        status = self.resultObj['Bolt']['status']
        if status is True:
            if self.fuse_model is None:
                self.fuse_model = self.create_2D_CAD()
            shape = self.fuse_model

            files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"

            fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"),
                                                      files_types)
            fName = str(fileName)

            flag = True
            if fName == '':
                flag = False
                return flag
            else:
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
        else:
            self.ui.actionSave_3D_model.setEnabled(False)
            QMessageBox.about(self, 'Information', 'Design Unsafe: 3D Model cannot be saved')

    def save_CAD_images(self):
        status = self.resultObj['Bolt']['status']
        if status is True:

            files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
            fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"),
                                                      files_types)
            fName = str(fileName)
            file_extension = fName.split(".")[-1]

            if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp' or file_extension == 'tiff':
                self.display.ExportToImage(fName)
                QMessageBox.about(self, 'Information', "File saved")
        else:
            self.ui.actionSave_current_image.setEnabled(False)
            QMessageBox.about(self, 'Information', 'Design Unsafe: CAD image cannot be saved')

    def call_zoomin(self):
        self.display.ZoomFactor(2)

    def call_zoomout(self):
        self.display.ZoomFactor(0.5)

    def call_rotation(self):
        self.display.Rotation(15, 0)

    def call_pannig(self):
        self.display.Pan(50, 0)

    def clear_log_messages(self):
        self.ui.textEdit.clear()

    def create_extended_both_ways(self):

        column_data = self.fetchColumnPara()
        beam_data = self.fetchBeamPara()

        # TODO check if column data is working

        column_tw = float(column_data["tw"])
        column_T = float(column_data["T"])
        column_d = float(column_data["D"])
        column_B = float(column_data["B"])
        column_R1 = float(column_data["R1"])
        column_R2 = float(column_data["R2"])
        column_alpha = float(column_data["FlangeSlope"])
        column_length = 1600.0

        beam_tw = float(beam_data["tw"])
        beam_T = float(beam_data["T"])
        beam_d = float(beam_data["D"])
        beam_B = float(beam_data["B"])
        beam_R1 = float(beam_data["R1"])
        beam_R2 = float(beam_data["R2"])
        beam_alpha = float(beam_data["FlangeSlope"])
        beam_length = 1600.0

        beam_Left = ISection(B=column_B, T=column_T, D=column_d, t=column_tw,
                             R1=column_R1, R2=column_R2, alpha=column_alpha,
                             length=column_length, notchObj=None)

        beam_Right = ISection(B=beam_B, T=beam_T, D=beam_d, t=beam_tw,
                              R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                              length=beam_length, notchObj=None)  # Since both the beams are same

        outputobj = self.outputs  # Save all the claculated/displayed out in outputobj

        plate_Right = Plate(W=outputobj["Plate"]["Width"],
                            L=outputobj["Plate"]["Height"],
                            T=outputobj["Plate"]["Thickness"])

        alist = self.designParameters()  # An object to save all input values entered by user

        # TODO make dictionary for the contPlates
        # TODO adding enpplate type and check if code is working
        # TODO added connectivity type here

        if alist['Member']['Connectivity'] == "Column web-Beam web":
            conn_type = 'col_web_connectivity'
        else:  # "Column flange-Beam web"
            conn_type = 'col_flange_connectivity'

        # endplate_type = alist['Member']['EndPlate_type']
        if alist['Member']['EndPlate_type'] == "Extended one way":
            endplate_type = "one_way"
        elif alist['Member']['EndPlate_type'] == "Flush end plate":
            endplate_type = "flush"
        else:  # uiObj['Member']['EndPlate_type'] == "Extended both ways":
            endplate_type = "both_way"

        contPlate_L1 = StiffenerPlate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
                                      L=float(column_data["D"]) - 2 * float(column_data["T"]),
                                      T=outputobj['ContPlateComp']['Thickness'])

        contPlate_L2 = StiffenerPlate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
                                      L=float(column_data["D"]) - 2 * float(column_data["T"]),
                                      T=outputobj['ContPlateTens']['Thickness'])
        contPlate_R1 = copy.copy(contPlate_L1)
        contPlate_R2 = copy.copy(contPlate_L2)

        beam_stiffener_1 = StiffenerPlate(W=outputobj['Stiffener']['Height'], L=outputobj['Stiffener']['Length'],
                                          T=outputobj['Stiffener']['Thickness'], R11=outputobj['Stiffener']['NotchTop'],
                                          R12=outputobj['Stiffener']['NotchTop'],
                                          L21=outputobj['Stiffener']['NotchBottom'],
                                          L22=outputobj['Stiffener']['NotchBottom'])

        beam_stiffener_2 = copy.copy(beam_stiffener_1)

        # contPlate_L1 = Plate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
        # L=float(column_data["D"]) - 2 * float(column_data["T"]), T=float(column_data["T"]))
        # contPlate_L2 = Plate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
        # 					 L=float(column_data["D"]) - 2 * float(column_data["T"]), T=float(column_data["T"]))
        # contPlate_R1 = Plate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
        # 					 L=float(column_data["D"]) - 2 * float(column_data["T"]), T=float(column_data["T"]))
        # contPlate_R2 = Plate(W=(float(column_data["B"]) - float(column_data["tw"])) / 2,
        # 					 L=float(column_data["D"]) - 2 * float(column_data["T"]), T=float(column_data["T"]))

        bolt_d = float(alist["Bolt"]["Diameter (mm)"])  # Bolt diameter, entered by user
        bolt_r = bolt_d / 2
        bolt_T = self.bolt_head_thick_calculation(bolt_d)
        bolt_R = self.bolt_head_dia_calculation(bolt_d) / 2
        bolt_Ht = self.bolt_length_calculation(bolt_d)

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component repo
        nut_T = self.nut_thick_calculation(bolt_d)
        nut_Ht = nut_T
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        numberOfBolts = int(outputobj["Bolt"]["NumberOfBolts"])

        # TODO remove all the clutter later

        # nutSpace = 2 * float(outputobj["Plate"]["Thickness"]) + nut_T   # Space between bolt head and nut
        if conn_type == 'col_flange_connectivity':
            nutSpace = float(column_data["T"]) + float(
                outputobj["Plate"]["Thickness"]) + nut_T / 2 + bolt_T / 2  # Space between bolt head and nut
        else:
            nutSpace = float(column_data["tw"]) + float(
                outputobj["Plate"]["Thickness"]) + nut_T / 2 + bolt_T / 2  # Space between bolt head and nut

        bbNutBoltArray = NutBoltArray(alist, beam_data, outputobj, nut, bolt, numberOfBolts, nutSpace, endplate_type)

        ###########################
        #       WELD SECTIONS     #
        ###########################
        '''
		Following sections are for creating Fillet Welds and Groove Welds
		Welds are numbered from Top to Bottom in Z-axis, Front to Back in Y axis and Left to Right in X axis. 
		'''
        if conn_type == 'col_flange_connectivity':

            if alist["Weld"]["Method"] == "Fillet Weld":

                # Followings welds are welds above beam flange, Qty = 4
                bbWeldAbvFlang_21 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
                                               h=float(alist["Weld"]["Flange (mm)"]),
                                               L=beam_B)
                bbWeldAbvFlang_22 = copy.copy(bbWeldAbvFlang_21)

                # Followings welds are welds below beam flange, Qty = 8
                bbWeldBelwFlang_21 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
                                                h=float(alist["Weld"]["Flange (mm)"]), L=(beam_B - beam_tw) / 2)
                bbWeldBelwFlang_22 = copy.copy(bbWeldBelwFlang_21)
                bbWeldBelwFlang_23 = copy.copy(bbWeldBelwFlang_21)
                bbWeldBelwFlang_24 = copy.copy(bbWeldBelwFlang_21)

                # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
                bbWeldSideWeb_21 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                                              L=beam_d - 2 * beam_T - 40)
                bbWeldSideWeb_22 = copy.copy(bbWeldSideWeb_21)

                #######################################
                #       WELD SECTIONS QUARTER CONE    #
                #######################################

                extbothWays = CADFillet(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bbWeldAbvFlang_21,
                                        bbWeldAbvFlang_22,
                                        bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23,
                                        bbWeldBelwFlang_24,
                                        bbWeldSideWeb_21, bbWeldSideWeb_22,
                                        contPlate_L1, contPlate_L2, contPlate_R1,
                                        contPlate_R2, beam_stiffener_1, beam_stiffener_2, endplate_type, conn_type,
                                        outputobj)
                extbothWays.create_3DModel()

                return extbothWays

            else:  # Groove Weld
                bcWeldFlang_1 = GrooveWeld(b=outputobj["Weld"]["Size"], h=float(beam_data["T"]),
                                           L=beam_B)
                bcWeldFlang_2 = copy.copy(bcWeldFlang_1)

                # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
                bcWeldWeb_3 = GrooveWeld(b=outputobj["Weld"]["Size"], h=float(beam_data["tw"]),
                                         L=beam_d - 2 * beam_T)

                #######################################
                #       WELD SECTIONS QUARTER CONE    #
                #######################################

                extbothWays = CADGroove(beam_Left, beam_Right, plate_Right, bbNutBoltArray,
                                        bcWeldFlang_1, bcWeldFlang_2, bcWeldWeb_3,
                                        contPlate_L1, contPlate_L2, contPlate_R1,
                                        contPlate_R2, beam_stiffener_1, beam_stiffener_2, endplate_type, outputobj)
                extbothWays.create_3DModel()

                return extbothWays

        else:  # conn_type = 'col_web_connectivity'
            if alist["Weld"]["Method"] == "Fillet Weld":
                # Followings welds are welds above beam flange, Qty = 4
                bbWeldAbvFlang_21 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
                                               h=float(alist["Weld"]["Flange (mm)"]),
                                               L=beam_B)
                bbWeldAbvFlang_22 = copy.copy(bbWeldAbvFlang_21)

                # Followings welds are welds below beam flange, Qty = 8
                bbWeldBelwFlang_21 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]),
                                                h=float(alist["Weld"]["Flange (mm)"]), L=(beam_B - beam_tw) / 2)
                bbWeldBelwFlang_22 = copy.copy(bbWeldBelwFlang_21)
                bbWeldBelwFlang_23 = copy.copy(bbWeldBelwFlang_21)
                bbWeldBelwFlang_24 = copy.copy(bbWeldBelwFlang_21)

                # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
                bbWeldSideWeb_21 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                                              L=beam_d - 2 * beam_T - 40)
                bbWeldSideWeb_22 = copy.copy(bbWeldSideWeb_21)

                #######################################
                #       WELD SECTIONS QUARTER CONE    #
                #######################################

                # extbothWays = CADFillet(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bbWeldAbvFlang_21,
                # 						bbWeldAbvFlang_22,
                # 						bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23,
                # 						bbWeldBelwFlang_24,
                # 						bbWeldSideWeb_21, bbWeldSideWeb_22,
                # 						contPlate_L1, contPlate_L2, contPlate_R1,
                # 						contPlate_R2, endplate_type, conn_type)

                col_web_connectivity = CADColWebFillet(beam_Left, beam_Right, plate_Right, bbNutBoltArray,
                                                       bbWeldAbvFlang_21,
                                                       bbWeldAbvFlang_22,
                                                       bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23,
                                                       bbWeldBelwFlang_24,
                                                       bbWeldSideWeb_21, bbWeldSideWeb_22,
                                                       contPlate_L1, contPlate_L2, contPlate_R1,
                                                       contPlate_R2, beam_stiffener_1, beam_stiffener_2, endplate_type,
                                                       conn_type, outputobj)

                col_web_connectivity.create_3DModel()

                return col_web_connectivity

            else:  # Groove Weld

                # else:
                bcWeldFlang_1 = GrooveWeld(b=outputobj["Weld"]["Size"], h=float(beam_data["T"]),
                                           L=beam_B)
                bcWeldFlang_2 = copy.copy(bcWeldFlang_1)

                # Followings welds are welds placed aside of beam web, Qty = 4 			# edited length value by Anand Swaroop
                bcWeldWeb_3 = GrooveWeld(b=outputobj["Weld"]["Size"], h=float(beam_data["tw"]),
                                         L=beam_d - 2 * beam_T)

                #######################################
                #       WELD SECTIONS QUARTER CONE    #
                #######################################

                col_web_connectivity = CADcolwebGroove(beam_Left, beam_Right, plate_Right, bbNutBoltArray,
                                                       bcWeldFlang_1, bcWeldFlang_2, bcWeldWeb_3,
                                                       contPlate_L1, contPlate_L2, contPlate_R1,
                                                       contPlate_R2, beam_stiffener_1, beam_stiffener_2, endplate_type,
                                                       outputobj)

                col_web_connectivity.create_3DModel()

                return col_web_connectivity

    #######################################
    #       WELD SECTIONS QUARTER CONE    #
    #######################################

    # # Following weld cones are placed for Left beam

    # extbothWays = CADFillet(beam_Left, beam_Right, plate_Right, bbNutBoltArray, bbWeldAbvFlang_21,
    # 							   bbWeldAbvFlang_22,
    # 							   bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23,
    # 							   bbWeldBelwFlang_24,
    # 							   bbWeldSideWeb_21, bbWeldSideWeb_22, bcWeldFlang_1, bcWeldFlang_2, bcWeldWeb_3, contPlate_L1, contPlate_L2, contPlate_R1,
    # 							   contPlate_R2, endplate_type, weld_method)
    # extbothWays.create_3DModel()
    #
    # return extbothWays

    def bolt_head_thick_calculation(self, bolt_diameter):
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
        bolt_head_thick = {5: 4, 6: 5, 8: 6, 10: 7, 12: 8, 16: 10, 20: 12.5, 22: 14, 24: 15, 27: 17, 30: 18.7,
                           36: 22.5}
        return bolt_head_thick[bolt_diameter]

    def bolt_head_dia_calculation(self, bolt_diameter):
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
        bolt_head_dia = {5: 7, 6: 8, 8: 10, 10: 15, 12: 20, 16: 27, 20: 34, 22: 36, 24: 41, 27: 46, 30: 50, 36: 60}
        return bolt_head_dia[bolt_diameter]

    def bolt_length_calculation(self, bolt_diameter):
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
        bolt_head_dia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65,
                         36: 75}

        return bolt_head_dia[bolt_diameter]

    def nut_thick_calculation(self, bolt_diameter):
        '''
		Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
		'''
    
		nut_dia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23,
				   30: 25.35, 36: 30.65}
		return nut_dia[bolt_diameter]

	def call_3DModel(self, bgcolor):
		# Call to calculate/create the Extended Both Way CAD model
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.create_extended_both_ways()
			self.ui.btn3D.setChecked(Qt.Checked)
			if self.ui.btn3D.isChecked():
				self.ui.chkBx_columnSec.setChecked(Qt.Unchecked)
				self.ui.chkBx_beamSec.setChecked(Qt.Unchecked)
				self.ui.chkBx_connector.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)

			# Call to display the Extended Both Way CAD model
			self.display_3DModel("Model", bgcolor)
		else:
			self.display.EraseAll()

	def call_3DColumn(self, bgcolor):
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.ui.chkBx_columnSec.setChecked(Qt.Checked)
			if self.ui.chkBx_columnSec.isChecked():
				self.ui.btn3D.setChecked(Qt.Unchecked)
				self.ui.chkBx_connector.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)
			self.display_3DModel("Column", bgcolor)

	def call_3DBeam(self, bgcolor):
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.ui.chkBx_beamSec.setChecked(Qt.Checked)
			if self.ui.chkBx_beamSec.isChecked():
				self.ui.btn3D.setChecked(Qt.Unchecked)
				self.ui.chkBx_connector.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)
			self.display_3DModel("Beam", bgcolor)

	def call_3DConnector(self, bgcolor):
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.ui.chkBx_connector.setChecked(Qt.Checked)
			if self.ui.chkBx_connector.isChecked():
				self.ui.btn3D.setChecked(Qt.Unchecked)
				self.ui.chkBx_columnSec.setChecked(Qt.Unchecked)
				self.ui.chkBx_beamSec.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)
			self.display_3DModel("Connector", bgcolor)

	def display_3DModel(self, component, bgcolor):
		self.component = component

		self.display.EraseAll()
		# self.display.View_Iso()
		# self.display.StartRotation(2000,0)
		self.display.FitAll()
		# self.display.Rotation(2000, 0)
		alist = self.designParameters()
		outputobj = self.outputs
		numberOfBolts = int(outputobj["Bolt"]["NumberOfBolts"])

		if alist['Member']['Connectivity'] == "Column web-Beam web":
			conn_type = 'col_web_connectivity'
		else:  # "Column flange-Beam web"
			conn_type = 'col_flange_connectivity'

		self.display.DisableAntiAliasing()
		if bgcolor == "gradient_bg":

			self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
		else:
			self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

		# ExtObj is an object which gets all the calculated values of CAD models
		self.ExtObj = self.create_extended_both_ways()


		# Displays the beams #TODO ANAND
		if component == "Column":
			self.display.View_Iso()
			osdag_display_shape(self.display, self.ExtObj.get_beamLModel(), update=True)
			# osdag_display_shape(self.display, self.ExtObj.get_beamRModel(), update=True)  # , color = 'Dark Gray'

		elif component == "Beam":
			self.display.View_Iso()
			# osdag_display_shape(self.display, self.ExtObj.get_beamLModel(), update=True)
			osdag_display_shape(self.display, self.ExtObj.get_beamRModel(), update=True)  # , color = 'Dark Gray'

		elif component == "Connector":
			self.display.View_Iso()
			# Displays the end plates
			# osdag_display_shape(self.display, self.ExtObj.get_plateLModel(), update=True, color='Blue')
			osdag_display_shape(self.display, self.ExtObj.get_plateRModel(), update=True, color='Blue')

			if conn_type == 'col_flange_connectivity':
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L1Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L2Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_R1Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_R2Model(), update=True, color='Blue')



			else:		#col_web_connectivity"
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L1Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L2Model(), update=True, color='Blue')

			# TODO: add if else statement for the type of endplate and also the number of bolts

			if alist['Member']['EndPlate_type'] == "Extended both ways":
				if numberOfBolts == 20:
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_1Model(), update=True,
										color='Blue')
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_2Model(), update=True,
										color='Blue')
			elif alist['Member']['EndPlate_type'] == "Extended one way":
				if numberOfBolts == 12:
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_1Model(), update=True,
										color='Blue')
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_2Model(), update=True,
										color='Blue')
			else:  # alist['Member']['EndPlate_type'] == "Flush end plate":
				pass



			# Display all nut-bolts, call to nutBoltPlacement.py
			nutboltlist = self.ExtObj.nut_bolt_array.get_models()
			for nutbolt in nutboltlist:
				osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
			# Display all the Welds including the quarter cone
			  # An object to save all input values entered by user
			if alist["Weld"]["Method"] == "Fillet Weld":
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_21Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_22Model(), update=True, color='Red')

				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_21Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_22Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_23Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_24Model(), update=True, color='Red')

				osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_21Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_22Model(), update=True, color='Red')

			else:  # Groove weld

				osdag_display_shape(self.display, self.ExtObj.get_bcWeldFlang_1Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bcWeldFlang_2Model(), update=True, color='Red')

				osdag_display_shape(self.display, self.ExtObj.get_bcWeldWeb_3Model(), update=True, color='Red')


		elif component == "Model":
			osdag_display_shape(self.display, self.ExtObj.get_beamLModel(), update=True)
			osdag_display_shape(self.display, self.ExtObj.get_beamRModel(), update=True, material=Graphic3d_NOT_2D_ALUMINUM)
			# Displays the end plates
			# osdag_display_shape(self.display, self.ExtObj.get_plateLModel(), update=True, color='Blue')
			osdag_display_shape(self.display, self.ExtObj.get_plateRModel(), update=True, color='Blue')

			if conn_type == 'col_flange_connectivity':
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L1Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L2Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_R1Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_R2Model(), update=True, color='Blue')



			else:
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L1Model(), update=True, color='Blue')
				osdag_display_shape(self.display, self.ExtObj.get_contPlate_L2Model(), update=True, color='Blue')

			# TODO: add if else statement for the type of endplate and also the number of bolts

			if alist['Member']['EndPlate_type'] == "Extended both ways":
				if numberOfBolts == 20:
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_1Model(), update=True,
										color='Blue')
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_2Model(), update=True,
										color='Blue')
			elif alist['Member']['EndPlate_type'] == "Extended one way":
				if numberOfBolts == 12:
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_1Model(), update=True,
										color='Blue')
					osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_2Model(), update=True,
										color='Blue')
			else:  # alist['Member']['EndPlate_type'] == "Flush end plate":
				pass

			# Display all nut-bolts, call to nutBoltPlacement.py
			nutboltlist = self.ExtObj.nut_bolt_array.get_models()
			for nutbolt in nutboltlist:
				osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

			# Display all the Welds including the quarter cone

			  # An object to save all input values entered by user
			if alist["Weld"]["Method"] == "Fillet Weld":
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_21Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_22Model(), update=True, color='Red')

				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_21Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_22Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_23Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_24Model(), update=True, color='Red')

				osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_21Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_22Model(), update=True, color='Red')

			else:  #Groove weld

				osdag_display_shape(self.display, self.ExtObj.get_bcWeldFlang_1Model(), update=True, color='Red')
				osdag_display_shape(self.display, self.ExtObj.get_bcWeldFlang_2Model(), update=True, color='Red')

				osdag_display_shape(self.display, self.ExtObj.get_bcWeldWeb_3Model(), update=True, color='Red')

	# =================================================================================
	def open_about_osdag(self):
		dialog = MyAboutOsdag(self)
		dialog.show()

	def open_tutorials(self):
		dialog = MyTutorials(self)
		dialog.show()

	def open_ask_question(self):
		dialog =  MyAskQuestion(self)
		dialog.show()

	def design_examples(self):
		root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ResourceFiles', 'design_example', '_build', 'html')
		for html_file in os.listdir(root_path):
			if html_file.startswith('index'):
				if sys.platform == ("win32" or "win64"):
					os.startfile("%s/%s" % (root_path, html_file))
				else:
					opener = "open" if sys.platform == "darwin" else "xdg-open"
					subprocess.call([opener, "%s/%s" % (root_path, html_file)])

def set_osdaglogger():
    global logger
    if logger is None:

        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # create the logging file handler
    fh = logging.FileHandler(os.path.join('Connections', 'Moment', 'BCEndPlate', 'extnd.log'), mode='a')

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


def launch_bc_endplate_controller(osdagMainWindow, folder):
    set_osdaglogger()
    # --------------- To display log messages in different colors ---------------
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    # file_handler = logging.FileHandler(os.path.join('Connections','Moment','BCEndPlate','extnd.log'), mode='w')
    file_handler = logging.FileHandler(os.path.join('..', 'extnd.log'), mode='w')
    formatter = logging.Formatter('''%(message)s''')
    file_handler.setFormatter(formatter)
    rawLogger.addHandler(file_handler)
    rawLogger.info(
        '''<link rel="stylesheet" type="text/css" href=''' + os.path.join('Connections', 'Moment', 'BCEndPlate',
                                                                          'log.css') + '''/>''')
    # ----------------------------------------------------------------------------
    module_setup()
    window = Maincontroller(folder)
    osdagMainWindow.hide()
    window.show()
    window.closed.connect(osdagMainWindow.show)


if __name__ == "__main__":
    # --------------- To display log messages in different colors ---------------
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    # fh = logging.FileHandler(os.path.join('Connections','Moment','BCEndPlate','extnd.log'), mode="w")
    fh = logging.FileHandler(os.path.join('..', 'extnd.log'), mode='w')

    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections\Moment\BCEndPlate\log.css"/>''')
    # ----------------------------------------------------------------------------
    # folder_path = "D:\Osdag_Workspace\extendedendplate"
    app = QApplication(sys.argv)
    module_setup()
    folder_path = "C:\Users\User\Desktop\Osdag IITB\Cloned\osdag_workspace"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path, 0755)
    image_folder_path = os.path.join(folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0755)

    window = Maincontroller(folder_path)
    window.show()
    sys.exit(app.exec_())
