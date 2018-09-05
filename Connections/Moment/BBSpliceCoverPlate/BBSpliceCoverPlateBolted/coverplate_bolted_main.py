"""
Created on 7-November-2017

@author: Reshma Konjari
"""

from ui_coverplatebolted import Ui_MainWindow
from ui_flangespliceplate import Ui_Flangespliceplate
from ui_flangespliceplate_inner import Ui_FlangespliceplateInner
from ui_webspliceplate import Ui_Webspliceplate
from svg_window import SvgWindow
from cover_plate_bolted_calc import coverplateboltedconnection
from drawing_2D import CoverEndPlate
from ui_design_preferences import Ui_DesignPreferences
from ui_design_summary import Ui_DesignReport
from ui_ask_question import Ui_AskQuestion
from ui_aboutosdag import Ui_AboutOsdag
from ui_tutorial import Ui_Tutorial
from svg_window import SvgWindow
from reportGenerator import save_html
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFontDialog, QFileDialog, QColorDialog
from PyQt5.Qt import QIntValidator, QDoubleValidator, QFile, Qt, QBrush, QColor, QTextStream, pyqtSignal, QPixmap, QPalette
from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from model import *
from OCC import IGESControl, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Interface import Interface_Static_SetCVal
from OCC.IFSelect import IFSelect_RetDone
from OCC.StlAPI import StlAPI_Writer
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
import cairosvg
import ConfigParser
import json
import os.path
import pickle
import pdfkit
import shutil
import sys
import subprocess
from collections import OrderedDict

from Connections.Component.ISection import ISection
from Connections.Component.nut import Nut
from Connections.Component.bolt import Bolt
from Connections.Component.filletweld import FilletWeld
from Connections.Component.plate import Plate
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.nutBoltPlacement_AF import NutBoltArray_AF
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.nutBoltPlacement_BF import NutBoltArray_BF
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.nutBoltPlacement_Web import NutBoltArray_Web
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
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


class DesignPreferences(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.ui = Ui_DesignPreferences()
		self.ui.setupUi(self)
		self.maincontroller = parent

		self.saved = None
		self.ui.tabWidget.removeTab(1)
		self.ui.combo_design_method.model().item(1).setEnabled(False)
		self.ui.combo_design_method.model().item(2).setEnabled(False)
		self.save_default_para()
		dbl_validator = QDoubleValidator()
		self.ui.txt_boltFu.setValidator(dbl_validator)
		self.ui.txt_boltFu.setMaxLength(7)
		self.ui.txt_weldFu.setValidator(dbl_validator)
		self.ui.txt_weldFu.setMaxLength(7)
		self.ui.txt_detailingGap.setValidator(dbl_validator)
		self.ui.txt_detailingGap.setMaxLength(5)
		self.ui.btn_defaults.clicked.connect(self.save_default_para)
		# self.ui.btn_save.clicked.connect(self.save_designPref_para)
		self.ui.btn_save.hide()
		self.ui.btn_close.clicked.connect(self.close_designPref)
		self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

	def save_designPref_para(self):
		uiObj = self.maincontroller.get_user_inputs()
		self.saved_designPref = {}
		self.saved_designPref["bolt"] = {}
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
		if self.ui.txt_detailingGap.text() == '':

			self.saved_designPref["detailing"]["gap"] = float(5)
		else:
			self.saved_designPref["detailing"]["gap"] = float(self.ui.txt_detailingGap.text())

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
		self.ui.combo_boltHoleType.setCurrentIndex(0)
		designPref = {}
		designPref["bolt"] = {}
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
		self.ui.txt_weldFu.setText(str(410))
		designPref["weld"]["fu_overwrite"] = self.ui.txt_weldFu.text()

		self.ui.combo_detailingEdgeType.setCurrentIndex(0)
		self.ui.txt_detailingGap.setText(str(5))
		designPref["detailing"] = {}
		typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
		designPref["detailing"]["typeof_edge"] = typeOfEdge
		designPref["detailing"]["min_edgend_dist"] = float(1.7)
		designPref["detailing"]["gap"] = int(5)
		self.ui.combo_detailing_memebers.setCurrentIndex(0)
		designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())

		designPref["design"] = {}
		designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
		self.saved = False
		return designPref

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
		boltFu = int(boltGrd) * 100 # Nominal strength of bolt
		return boltFu

	def close_designPref(self):
		self.close()

	def closeEvent(self, QCloseEvent):
		self.save_designPref_para()
		QCloseEvent.accept()


class Flangespliceplate(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.ui = Ui_Flangespliceplate()
		self.ui.setupUi(self)
		self.maincontroller = parent

		uiObj = self.maincontroller.designParameters()
		resultObj_flangeplate = coverplateboltedconnection(uiObj)

		self.ui.txt_plateHeight.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateHeight"]))
		self.ui.txt_plateWidth.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateWidth"]))
		self.ui.txt_plateDemand.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateDemand"]))
		self.ui.txt_plateCapacity.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangeCapacity"]))

class FlangespliceplateInner(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.ui = Ui_FlangespliceplateInner()

		self.ui.setupUi(self)
		self.maincontroller = parent

		uiObj = self.maincontroller.designParameters()
		resultObj_flangeplate = coverplateboltedconnection(uiObj)

		self.ui.txt_outer_plateHeight.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateHeight"]))
		self.ui.txt_outer_plateWidth.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateWidth"]))
		self.ui.txt_inner_plateHeight.setText(str(resultObj_flangeplate["FlangeBolt"]["InnerFlangePlateHeight"]))
		self.ui.txt_inner_plateWidth.setText(str(resultObj_flangeplate["FlangeBolt"]["InnerFlangePlateWidth"]))
		self.ui.txt_plateDemand.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateDemand"]))
		self.ui.txt_plateCapacity.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangeCapacity"]))


class Webspliceplate(QDialog):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.ui = Ui_Webspliceplate()
		self.ui.setupUi(self)
		self.maincontroller = parent

		uiObj = self.maincontroller.designParameters()
		resultObj_webplate = coverplateboltedconnection(uiObj)

		self.ui.txt_plateHeight.setText(str(resultObj_webplate["WebBolt"]["WebPlateHeight"]))
		self.ui.txt_plateWidth.setText(str(resultObj_webplate["WebBolt"]["WebPlateWidth"]))
		self.ui.txt_plateCapacity.setText(str(resultObj_webplate["WebBolt"]["WebPlateCapacity"]))
		self.ui.txt_plateDemand.setText(str(resultObj_webplate["WebBolt"]["webPlateDemand"]))


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
			cairosvg.svg2png(file_obj=filename,
							 write_to=os.path.join(str(self.maincontroller.folder), "images_html", "cmpylogoExtendEndplate.svg"))
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


class MainController(QMainWindow):
	closed = pyqtSignal()

	def __init__(self, folder):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.folder = folder
		self.connection = "Coverplate"
		self.get_beamdata()
		self.designPrefDialog = DesignPreferences(self)
		self.ui.combo_connLoc.model().item(2).setEnabled(False)
		# self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
		# self.ui.combo_beamSec.setCurrentIndex(0)
		self.gradeType = {'Please select type': '', 'Friction Grip Bolt': [8.8, 10.9],
						  'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
		self.ui.combo_type.addItems(self.gradeType.keys())
		self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
		self.ui.combo_type.setCurrentIndex(0)

		self.preference_type = OrderedDict()
		self.preference_type['Cover plate location'] = ''
		self.preference_type['Outside'] = [5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32]
		self.preference_type['Outside + Inside'] = [5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32]

		self.ui.combo_flange_preference.addItems(self.preference_type.keys())
		self.ui.combo_flange_preference.currentIndexChanged[str].connect(self.combopreference_current_index_changed)
		self.ui.combo_flange_preference.setCurrentIndex(0)

		self.retrieve_prevstate()
		self.ui.combo_connLoc.currentIndexChanged[str].connect(self.setimage_connection)

		self.ui.combo_diameter.currentIndexChanged[str].connect(self.bolt_hole_clearance)
		self.ui.combo_grade.currentIndexChanged[str].connect(self.call_bolt_fu)

		self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
		self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
		self.ui.actionDesign_Preferences.triggered.connect(self.design_prefer)
		self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialogue)
		self.ui.action_save_input.triggered.connect(self.save_design_inputs)
		self.ui.action_load_input.triggered.connect(self.load_design_inputs)
		self.ui.actionSave_log_messages.triggered.connect(self.save_log_messages)
		self.ui.actionCreate_design_report.triggered.connect(self.design_report)
		self.ui.actionChange_background.triggered.connect(self.show_color_dialog)
		self.ui.actionSave_Front_View.triggered.connect(lambda: self.call_2D_drawing("Front"))
		self.ui.actionSave_Side_View.triggered.connect(lambda: self.call_2D_drawing("Side"))
		self.ui.actionSave_Top_View.triggered.connect(lambda: self.call_2D_drawing("Top"))
		self.ui.actionShow_all.triggered.connect(lambda: self.call_3DModel("gradient_bg"))
		self.ui.actionShow_beam.triggered.connect(lambda: self.call_3DBeam("gradient_bg"))
		self.ui.actionShow_connector.triggered.connect(lambda: self.call_3DConnector("gradient_bg"))
		self.ui.actionSave_current_image.triggered.connect(self.save_CAD_images)
		self.ui.actionZoom_in.triggered.connect(self.call_zoomin)
		self.ui.actionZoom_out.triggered.connect(self.call_zoomout)
		self.ui.actionPan.triggered.connect(self.call_pannig)
		self.ui.actionRotate_3D_model.triggered.connect(self.call_rotation)
		self.ui.actionClear.triggered.connect(self.clear_log_messages)
		self.ui.actionSample_Tutorials.triggered.connect(self.open_tutorials)
		self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_ask_question)
		self.ui.actionAbout_Osdag_2.triggered.connect(self.open_about_osdag)
		self.ui.actionDesign_examples.triggered.connect(self.design_examples)
		self.ui.actionSave_3D_model.triggered.connect(self.save_3D_CAD_images)

		self.ui.btn_flangePlate.clicked.connect(self.flangesplice_plate)
		self.ui.btn_webPlate.clicked.connect(self.websplice_plate)

		self.ui.btn_Design.clicked.connect(self.design_btnclicked)
		self.ui.btn_Reset.clicked.connect(self.reset_btnclicked)
		self.ui.btn_Design.clicked.connect(self.osdag_header)
		self.ui.btnFront.clicked.connect(lambda: self.call_2D_drawing("Front"))
		self.ui.btnTop.clicked.connect(lambda: self.call_2D_drawing("Top"))
		self.ui.btnSide.clicked.connect(lambda: self.call_2D_drawing("Side"))
		self.ui.btnPlan.clicked.connect(lambda: self.call_2D_drawing("Plan"))
		self.ui.btn3D.clicked.connect(lambda: self.call_3DModel("gradient_bg"))
		self.ui.chkBx_beamSec1.clicked.connect(lambda: self.call_3DBeam("gradient_bg"))
		self.ui.chkBx_extndPlate.clicked.connect(lambda: self.call_3DConnector("gradient_bg"))
		self.ui.btn_CreateDesign.clicked.connect(self.design_report)

		validator = QIntValidator()
		self.ui.txt_flangeplateHeight.setValidator(validator)
		self.ui.txt_flangeplateWidth.setValidator(validator)
		self.ui.txt_webplateHeight.setValidator(validator)
		self.ui.txt_webplateWidth.setValidator(validator)

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

		min_gap = 2
		max_gap = 10
		self.designPrefDialog.ui.txt_detailingGap.editingFinished.connect(
			lambda: self.check_range(self.designPrefDialog.ui.txt_detailingGap, min_gap, max_gap))

		from osdagMainSettings import backend_name
		self.display, _ = self.init_display(backend_str=backend_name())
		self.uiObj = None
		self.resultObj = None
		self.fuse_model = None
		self.disable_buttons()

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

	def get_beamdata(self):
		"""

		Returns: Selects beam data from both Old & Integrated database

		"""
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

		Returns: Differentiate the database by color code

		"""
		for col in old_section:
			if col in intg_section:
				indx = intg_section.index(str(col))
				combo_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

		duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]
		for i in duplicate:
			combo_section.setItemData(i, QBrush(QColor("red")), Qt.TextColorRole)

	def fetchBeamPara(self):
		beamdata_sec = self.ui.combo_beamSec.currentText()
		dictbeamdata = get_beamdata(beamdata_sec)
		return dictbeamdata

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

	def combopreference_current_index_changed(self, index):
		"""

		Args:
			index: Number

		Returns: Types of Preferences

		"""
		items = self.preference_type[str(index)]
		if items != 0:
			self.ui.combo_flangeplateThick.clear()
			stritems = []
			for val in items:
				stritems.append(str(val))

			self.ui.combo_flangeplateThick.addItems(stritems)
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
		text_str = float(text_str)
		if (text_str < min_val or text_str > max_val or text_str == ' '):
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
		self.result = coverplateboltedconnection(self.alist)
		self.beam_data = self.fetchBeamPara()
		save_html(self.result, self.alist, self.beam_data, fileName, report_summary, self.folder)

	def get_user_inputs(self):
		"""

		Returns: User Input dictionary

		"""
		uiObj = {}
		uiObj["Member"] = {}
		uiObj["Member"]["Connectivity"] = str(self.ui.combo_connLoc.currentText())
		uiObj["Member"]["BeamSection"] = str(self.ui.combo_beamSec.currentText())
		uiObj["Member"]["fu (MPa)"] = self.ui.txt_Fu.text()
		uiObj["Member"]["fy (MPa)"] = self.ui.txt_Fy.text()

		uiObj["Load"] = {}
		uiObj["Load"]["ShearForce (kN)"] = self.ui.txt_Shear.text()
		uiObj["Load"]["Moment (kNm)"] = self.ui.txt_Moment.text()
		uiObj["Load"]["AxialForce"] = self.ui.txt_Axial.text()

		uiObj["Bolt"] = {}
		uiObj["Bolt"]["Diameter (mm)"] = self.ui.combo_diameter.currentText()
		uiObj["Bolt"]["Grade"] = self.ui.combo_grade.currentText()
		uiObj["Bolt"]["Type"] = self.ui.combo_type.currentText()

		uiObj["FlangePlate"] = {}
		uiObj['FlangePlate']['Preferences'] = self.ui.combo_flange_preference.currentText()
		uiObj["FlangePlate"]["Thickness (mm)"] = self.ui.combo_flangeplateThick.currentText()
		uiObj["FlangePlate"]["Height (mm)"] = self.ui.txt_flangeplateHeight.text()
		uiObj["FlangePlate"]["Width (mm)"] = self.ui.txt_flangeplateWidth.text()

		uiObj["WebPlate"] = {}
		uiObj["WebPlate"]["Thickness (mm)"] = self.ui.combo_webplateThick.currentText()
		uiObj["WebPlate"]["Height (mm)"] = self.ui.txt_webplateHeight.text()
		uiObj["WebPlate"]["Width (mm)"] = self.ui.txt_webplateWidth.text()
		uiObj["Connection"] = self.connection
		return uiObj

	def osdag_header(self):
		image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
		shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

	def disable_buttons(self):
		self.ui.btn_CreateDesign.setEnabled(False)
		self.ui.btn_SaveMessages.setEnabled(False)
		self.ui.btnFront.setEnabled(False)
		self.ui.btnTop.setEnabled(False)
		self.ui.btnSide.setEnabled(False)
		self.ui.btnPlan.setEnabled(False)
		self.ui.btn3D.setEnabled(False)
		self.ui.chkBx_extndPlate.setEnabled(False)
		self.ui.chkBx_beamSec1.setEnabled(False)
		self.ui.btn_flangePlate.setEnabled(False)
		self.ui.btn_webPlate.setEnabled(False)

		self.ui.action_save_input.setEnabled(False)
		self.ui.actionCreate_design_report.setEnabled(False)
		self.ui.actionSave_3D_model.setEnabled(False)
		self.ui.actionSave_log_messages.setEnabled(False)
		self.ui.actionSave_current_image.setEnabled(False)
		self.ui.actionSave_Front_View.setEnabled(False)
		self.ui.actionSave_Side_View.setEnabled(False)
		self.ui.actionSave_Top_View.setEnabled(False)
		self.ui.menuGraphics.setEnabled(False)

	def enable_buttons(self):
		self.ui.btn_CreateDesign.setEnabled(True)
		self.ui.btn_SaveMessages.setEnabled(True)
		self.ui.btnFront.setEnabled(True)
		self.ui.btnTop.setEnabled(True)
		self.ui.btnPlan.setEnabled(True)
		self.ui.btnSide.setEnabled(True)
		self.ui.btn3D.setEnabled(True)
		self.ui.chkBx_beamSec1.setEnabled(True)
		self.ui.chkBx_extndPlate.setEnabled(True)
		self.ui.btn_flangePlate.setEnabled(True)
		self.ui.btn_webPlate.setEnabled(True)

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
		self.ui.combo_beamSec.setCurrentIndex(0)
		self.ui.combo_connLoc.setCurrentIndex(0)
		self.ui.lbl_connectivity.clear()
		self.ui.txt_Fu.clear()
		self.ui.txt_Fy.clear()
		self.ui.txt_Axial.clear()
		self.ui.txt_Shear.clear()
		self.ui.txt_Moment.clear()
		self.ui.combo_diameter.setCurrentIndex(0)
		self.ui.combo_type.setCurrentIndex(0)
		self.ui.combo_grade.setCurrentIndex(0)
		self.ui.combo_flange_preference.setCurrentIndex(0)
		self.ui.combo_flangeplateThick.setCurrentIndex(0)
		self.ui.txt_flangeplateHeight.clear()
		self.ui.txt_flangeplateWidth.clear()
		self.ui.combo_webplateThick.setCurrentIndex(0)
		self.ui.txt_webplateWidth.clear()
		self.ui.txt_webplateHeight.clear()

		self.ui.txt_shearCapacity.clear()
		self.ui.txt_bearCapacity.clear()
		self.ui.txt_capacityOfbolt.clear()
		self.ui.txt_noBolts.clear()
		self.ui.txt_pitch.clear()
		self.ui.txt_gauge.clear()
		self.ui.txt_edgeDist.clear()
		self.ui.txt_endDist.clear()
		self.ui.txt_shearCapacity_2.clear()
		self.ui.txt_bearCapacity_2.clear()
		self.ui.txt_capacityOfbolt_2.clear()
		self.ui.txt_noBolts_2.clear()
		self.ui.txt_pitch_2.clear()
		self.ui.txt_gauge_2.clear()
		self.ui.txt_endDist_2.clear()
		self.ui.txt_edgeDist_2.clear()

		self.ui.btn_flangePlate.setDisabled(True)
		self.ui.btn_webPlate.setDisabled(True)
		self.disable_buttons()
		self.display.EraseAll()
		self.designPrefDialog.save_default_para()

	def design_prefer(self):
		self.designPrefDialog.show()

	def bolt_hole_clearance(self):
		self.designPrefDialog.get_clearance()

	def call_bolt_fu(self):
		self.designPrefDialog.set_boltFu()

	def closeEvent(self, event):
		"""

		Args:
			event: Yes or No

		Returns: Ask for the confirmation while closing the window

		"""
		# uiInput = self.get_user_inputs()
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
		# input_file = QFile(os.path.join("Connections","Moment","BBSpliceCoverPlate","BBSpliceCoverPlateBolted","saveINPUT.txt"))
		input_file = QFile(os.path.join("saveINPUT.txt"))
		if not input_file.open(QFile.WriteOnly | QFile.Text):
			QMessageBox.warning(self, "Application",
								"Cannot write file %s: \n%s"
								% (input_file.fileName(), input_file.errorString()))
		pickle.dump(uiObj, input_file)

	def get_prevstate(self):
		"""

		Returns: Read for the previous user inputs design

		"""
		# filename = os.path.join("Connections", "Moment", "BBSpliceCoverPlate", "BBSpliceCoverPlateBolted", "saveINPUT.txt")
		filename = os.path.join("saveINPUT.txt")
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
			if uiObj["Connection"] != "Coverplate":
				QMessageBox.information(self, "Information", "You can load this input file only from the corresponding design problem")
				return

			self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(str(uiObj["Member"]["Connectivity"])))
			if uiObj["Member"]["Connectivity"] == "Select Connectivity" or "Bolted" :
				self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(uiObj["Member"]["Connectivity"]))
				self.ui.combo_beamSec.setCurrentIndex(self.ui.combo_beamSec.findText(uiObj["Member"]["BeamSection"]))
				self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
				self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
				self.ui.txt_Shear.setText(str(uiObj["Load"]["ShearForce (kN)"]))
				self.ui.txt_Axial.setText(str(uiObj["Load"]["AxialForce"]))
				self.ui.txt_Moment.setText(str(uiObj["Load"]["Moment (kNm)"]))
				self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
				self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
				self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
				self.ui.combo_flange_preference.setCurrentIndex(self.ui.combo_flange_preference.findText(uiObj["FlangePlate"]['Preferences']))
				self.ui.combo_flangeplateThick.setCurrentIndex(self.ui.combo_flangeplateThick.findText(uiObj["FlangePlate"]["Thickness (mm)"]))
				self.ui.combo_webplateThick.setCurrentIndex(
					self.ui.combo_webplateThick.findText(uiObj["WebPlate"]["Thickness (mm)"]))
				self.ui.txt_flangeplateHeight.setText(str(uiObj["FlangePlate"]["Height (mm)"]))
				self.ui.txt_flangeplateWidth.setText(str(uiObj["FlangePlate"]["Width (mm)"]))
				self.ui.txt_webplateHeight.setText(str(uiObj["WebPlate"]["Height (mm)"]))
				self.ui.txt_webplateWidth.setText(str(uiObj["WebPlate"]["Width (mm)"]))

				self.designPrefDialog.ui.combo_boltHoleType.setCurrentIndex(self.designPrefDialog.ui.combo_boltHoleType.findText(uiObj["bolt"]["bolt_hole_type"]))
				self.designPrefDialog.ui.txt_boltFu.setText(str(uiObj["bolt"]["bolt_fu"]))
				self.designPrefDialog.ui.txt_detailingGap.setText(str(uiObj["detailing"]["gap"]))
				self.designPrefDialog.ui.combo_slipfactor.setCurrentIndex(self.designPrefDialog.ui.combo_slipfactor.findText(str(uiObj["bolt"]["slip_factor"])))
				self.designPrefDialog.ui.combo_detailingEdgeType.setCurrentIndex(self.designPrefDialog.ui.combo_detailingEdgeType.findText(uiObj["detailing"]["typeof_edge"]))
				self.designPrefDialog.ui.combo_detailing_memebers.setCurrentIndex(self.designPrefDialog.ui.combo_detailing_memebers.findText(uiObj["detailing"]["is_env_corrosive"]))
				self.designPrefDialog.ui.combo_design_method.setCurrentIndex(self.designPrefDialog.ui.combo_design_method.findText(uiObj["design"]["design_method"]))

		else:
			pass

	def designParameters(self):
		"""

		Returns: Design preference inputs

		"""
		self.uiObj = self.get_user_inputs()
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
		if loc == "Bolted":
			pixmap = QPixmap(":/newPrefix/images/coverplatewindow.png")
			pixmap.scaledToHeight(60)
			pixmap.scaledToWidth(50)
			self.ui.lbl_connectivity.setPixmap(pixmap)
		else:
			pass

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
			if self.ui.combo_connLoc.currentIndex() == 0:
				incomplete_list.append("Connectivity")
		else:
			pass

		if self.ui.combo_beamSec.currentIndex() == 0:
			incomplete_list.append("Beam section")

		if self.ui.txt_Fu.text() == "":
			incomplete_list.append("Ultimate strength")

		if self.ui.txt_Fy.text() == "":
			incomplete_list.append("Yield strength")

		#if self.ui.txt_Axial.text() == '' or float(self.ui.txt_Axial.text()) == 0:
		#	incomplete_list.append("Axial force")

		if self.ui.txt_Moment.text() == '' or float(self.ui.txt_Moment.text()) == 0:
			incomplete_list.append("Moment")

		if self.ui.txt_Shear.text() == '':
			incomplete_list.append("Shear force")

		if self.ui.combo_diameter.currentIndex() == 0:
			incomplete_list.append("Diameter of bolt")

		if self.ui.combo_type.currentIndex() == 0:
			incomplete_list.append("Type of bolt")

		if self.ui.combo_flange_preference.currentIndex() == 0:
			incomplete_list.append("Flange splice plate thickness")

		if self.ui.combo_webplateThick.currentIndex() == 0:
			incomplete_list.append("Web splice plate thickness")

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

		self.ui.outputDock.setFixedSize(310, 710)
		self.enable_buttons()

		self.outputs = coverplateboltedconnection(self.alist)
		a = self.outputs[self.outputs.keys()[0]]
		self.resultObj = self.outputs
		alist = self.resultObj.values()

		self.display_output(self.outputs)
		self.display_log_to_textedit()
		isempty = [True if val != '' else False for ele in alist for val in ele.values()]
		if self.ui.combo_flange_preference.currentText() == 'Outside':
			self.ui.btnPlan.setEnabled(False)

		if isempty[0] is True:
			status = self.resultObj['Bolt']['status']
			self.call_3DModel("gradient_bg")
			if status is True:
				self.call_2D_drawing("All")
			else:
				self.ui.btn_flangePlate.setDisabled(False)
				self.ui.btn_webPlate.setDisabled(False)
				self.ui.chkBx_extndPlate.setDisabled(True)
				self.ui.chkBx_beamSec1.setDisabled(True)
				self.ui.btn3D.setDisabled(True)

	def display_output(self, outputObj):
		"""

		Args:
			outputObj: Output dictionary from calculation file

		Returns: Design result values to the respective textboxes in the output window

		"""
		for k in outputObj.keys():
			for value in outputObj.values():
				if outputObj.items() == " ":
					# if value == ' ':
					resultObj = outputObj
				else:
					resultObj = outputObj
		print resultObj

		flange_shear_capacity = resultObj["FlangeBolt"]["ShearCapacityF"]
		self.ui.txt_shearCapacity.setText(str(flange_shear_capacity))

		flange_bearing_capacity = resultObj["FlangeBolt"]["BearingCapacityF"]
		self.ui.txt_bearCapacity.setText(str(flange_bearing_capacity))

		flange_capacity_bolt = resultObj["FlangeBolt"]["CapacityBoltF"]
		self.ui.txt_capacityOfbolt.setText(str(flange_capacity_bolt))

		flange_bolt_req = resultObj["FlangeBolt"]["TotalBoltsRequiredF"]
		self.ui.txt_noBolts.setText(str(flange_bolt_req))

		flange_pitch = resultObj["FlangeBolt"]["PitchF"]
		self.ui.txt_pitch.setText(str(flange_pitch))

		flange_gauge = resultObj["FlangeBolt"]["FlangeGauge"]
		self.ui.txt_gauge.setText(str(flange_gauge))

		flange_enddist = resultObj["FlangeBolt"]["EndF"]
		self.ui.txt_endDist.setText(str(flange_enddist))

		flange_edgedist = resultObj["FlangeBolt"]["EdgeF"]
		self.ui.txt_edgeDist.setText(str(flange_edgedist))

		web_shear_capacity = resultObj["WebBolt"]["ShearCapacity"]
		self.ui.txt_shearCapacity_2.setText(str(web_shear_capacity))

		web_bearing_capacity = resultObj["WebBolt"]["BearingCapacity"]
		self.ui.txt_bearCapacity_2.setText(str(web_bearing_capacity))

		web_capacity_bolt = resultObj["WebBolt"]["CapacityBolt"]
		self.ui.txt_capacityOfbolt_2.setText(str(web_capacity_bolt))

		web_bolt_req = resultObj["WebBolt"]["TotalBoltsRequired"]
		self.ui.txt_noBolts_2.setText(str(web_bolt_req))

		web_pitch = resultObj["WebBolt"]["Pitch"]
		self.ui.txt_pitch_2.setText(str(web_pitch))

		web_gauge = resultObj["WebBolt"]["WebGauge"]
		self.ui.txt_gauge_2.setText(str(web_gauge))

		web_enddist = resultObj["WebBolt"]["End"]
		self.ui.txt_endDist_2.setText(str(web_enddist))

		web_edgedist = resultObj["WebBolt"]["Edge"]
		self.ui.txt_edgeDist_2.setText(str(web_edgedist))

	def display_log_to_textedit(self):
		file = QFile(os.path.join('Connections','Moment','BBSpliceCoverPlate','BBSpliceCoverPlateBolted','coverplate.log'))
		if not file.open(QtCore.QIODevice.ReadOnly):
			QMessageBox.information(None, 'info', file.errorString())
		stream = QtCore.QTextStream(file)
		self.ui.textEdit.clear()
		self.ui.textEdit.setHtml(stream.readAll())
		vscroll_bar = self.ui.textEdit.verticalScrollBar()
		vscroll_bar.setValue(vscroll_bar.maximum())
		file.close()

	def call_2D_drawing(self, view):
		"""

		Args:
			view: Front, Side & Top views

		Returns: Saves 2D svg drawings

		"""
		self.alist = self.designParameters()
		self.resultObj = coverplateboltedconnection(self.alist)
		self.beam_data = self.fetchBeamPara()
		beam_beam = CoverEndPlate(self.alist, self.resultObj, self.beam_data, self.folder)
		status = self.resultObj['Bolt']['status']
		if status is True:
			if view != 'All':
				if view == "Front":
					filename = os.path.join(self.folder, "images_html", "coverboltedFront.svg")

				elif view == "Side":
					filename = os.path.join(self.folder, "images_html", "coverboltedSide.svg")

				else:
					filename = os.path.join(self.folder, "images_html", "coverboltedTop.svg")

				beam_beam.save_to_svg(filename, view)
				svg_file = SvgWindow()
				svg_file.call_svgwindow(filename, view, self.folder)
			else:
				fname = ''
				beam_beam.save_to_svg(fname, view)
		else:
			QMessageBox.about(self, 'Information', 'Design Unsafe: %s view cannot be viewed' % (view))

	def flangesplice_plate(self):
		if self.ui.combo_flange_preference.currentText() == 'Outside':
			section = Flangespliceplate(self)
		else:
			section = FlangespliceplateInner(self)
		section.show()

	def websplice_plate(self):
		section = Webspliceplate(self)
		section.show()

	def design_report(self):
		design_report_dialog = DesignReportDialog(self)
		design_report_dialog.show()

	def show_font_dialogue(self):
		font, ok = QFontDialog.getFont()
		if ok:
			self.ui.textEdit.setFont(font)

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

	# ===========================  CAD ===========================
	def show_color_dialog(self):
		col = QColorDialog.getColor()
		colorTup = col.getRgb()
		r = colorTup[0]
		g = colorTup[1]
		b = colorTup[2]
		self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

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

	def create_2D_CAD(self):
		"""

		Returns: The 3D model of coverplate depending upon component selected

		"""
		self.CPBoltedObj = self.createBBCoverPlateBoltedCAD()
		if self.component == "Beam":

			# final_model = [self.CPBoltedObj.get_beamLModel(), self.CPBoltedObj.get_beamRModel()]
			final_model = self.CPBoltedObj.get_beam_models()

		elif self.component == "Connector":
			cadlist = self.CPBoltedObj.get_connector_models()
			print "CADLIST... ", cadlist

			final_model = cadlist[0]
			for model in cadlist[1:]:
				final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

		else:
			cadlist = self.CPBoltedObj.get_models()
			final_model = cadlist[0]
			for model in cadlist[1:]:
				final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

		return final_model

	def save_3D_CAD_images(self):
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

	def createBBCoverPlateBoltedCAD(self):
		'''
		:return: The calculated values/parameters to create 3D CAD model of individual components.
		'''

		beam_data = self.fetchBeamPara()  # Fetches the beam dimensions

		beam_tw = float(beam_data["tw"])
		beam_T = float(beam_data["T"])
		beam_d = float(beam_data["D"])
		beam_B = float(beam_data["B"])
		beam_R1 = float(beam_data["R1"])
		beam_R2 = float(beam_data["R2"])
		beam_alpha = float(beam_data["FlangeSlope"])
		beam_length = 800.0

		beam_Left = ISection(B=beam_B, T=beam_T, D=beam_d, t=beam_tw,
							 R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
							 length=beam_length, notchObj=None)  # Call to ISection in Component repository
		beam_Right = copy.copy(beam_Left)  # Since both the beams are same
		outputobj = self.outputs  # Output dictionary from calculation file
		alist = self.designParameters()  # An object to save all input values entered by user

		plateAbvFlange = Plate(L=outputobj["FlangeBolt"]["FlangePlateWidth"],
							   W=outputobj["FlangeBolt"]["FlangePlateHeight"],
							   T=float(alist["FlangePlate"]["Thickness (mm)"]))  # Call to Plate in Component repository
		plateBelwFlange = copy.copy(plateAbvFlange)  # Since both the flange plates are identical

		innerplateAbvFlangeFront = Plate(L=outputobj["FlangeBolt"]["InnerFlangePlateWidth"],
										 W=outputobj["FlangeBolt"]["InnerFlangePlateHeight"],
										 T=(outputobj["FlangeBolt"]["InnerFlangePlateThickness"]))
		innerplateAbvFlangeBack = copy.copy(innerplateAbvFlangeFront)
		innerplateBelwFlangeFront = copy.copy(innerplateAbvFlangeBack)
		innerplateBelwFlangeBack = copy.copy(innerplateBelwFlangeFront)


		WebPlateLeft = Plate(L=outputobj["WebBolt"]["WebPlateHeight"],
							 W=outputobj["WebBolt"]["WebPlateWidth"],
							 T=float(alist["WebPlate"]["Thickness (mm)"]))  # Call to Plate in Component repository
		WebPlateRight = copy.copy(WebPlateLeft)  # Since both the Web plates are identical

		bolt_d = float(alist["Bolt"]["Diameter (mm)"])  # Bolt diameter (shank part), entered by user
		bolt_r = bolt_d / 2  # Bolt radius (Shank part)
		bolt_T = self.bolt_head_thick_calculation(bolt_d)  # Bolt head thickness
		bolt_R = self.bolt_head_dia_calculation(bolt_d) / 2  # Bolt head diameter (Hexagon)
		bolt_Ht = self.bolt_length_calculation(bolt_d)  # Bolt head height

		bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
		nut_T = self.nut_thick_calculation(bolt_d)  # Nut thickness, usually nut thickness = nut height
		nut_Ht = nut_T
		nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)  # Call to create Nut from Component directory

		numOfBoltsF = 2 * int(outputobj["FlangeBolt"]["BoltsRequiredF"])  # Number of flange bolts for both beams
		nutSpaceF = float(
			alist["FlangePlate"]["Thickness (mm)"]) + beam_T  # Space between bolt head and nut for flange bolts

		numOfBoltsW = 2 * int(outputobj["WebBolt"]["BoltsRequired"])  # Number of web bolts for both beams
		nutSpaceW = 2 * float(
			alist["WebPlate"]["Thickness (mm)"]) + beam_tw  # Space between bolt head and nut for web bolts

		# Bolt placement for Above Flange bolts, call to nutBoltPlacement_AF.py
		bolting_AF = NutBoltArray_AF(alist, beam_data, outputobj, nut, bolt, numOfBoltsF, nutSpaceF)

		# Bolt placement for Below Flange bolts, call to nutBoltPlacement_BF.py
		bolting_BF = NutBoltArray_BF(alist, beam_data, outputobj, nut, bolt, numOfBoltsF, nutSpaceF)

		# Bolt placement for Web Plate bolts, call to nutBoltPlacement_Web.py
		bolting_Web = NutBoltArray_Web(alist, beam_data, outputobj, nut, bolt, numOfBoltsW, nutSpaceW)

		# bbCoverPlateBolted is an object which is passed BBCoverPlateBoltedCAD.py file, which initialized the parameters of each CAD component
		bbCoverPlateBolted = BBCoverPlateBoltedCAD(beam_Left, beam_Right, plateAbvFlange, plateBelwFlange, innerplateAbvFlangeFront,
												   innerplateAbvFlangeBack, innerplateBelwFlangeFront, innerplateBelwFlangeBack,
												   WebPlateLeft, WebPlateRight, bolting_AF, bolting_BF, bolting_Web, alist)

		# bbCoverPlateBolted.create_3DModel() will create the CAD model of each component, debugging this line will give moe clarity
		bbCoverPlateBolted.create_3DModel()

		return bbCoverPlateBolted

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
		bolt_head_thick = {5: 4, 6: 5, 8: 6, 10: 7, 12: 8, 16: 10, 20: 12.5, 22: 14, 24: 15, 27: 17, 30: 18.7, 36: 22.5}
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

	# def bolt_length_calculation(self, bolt_diameter):
	# 	'''
	# 	This routine takes the bolt diameter and return bolt head diameter as per IS:3757(1985)
	#
	#    bolt Head Dia
	# 	<-------->
	# 	__________  ______
	# 	|        |    |
	# 	|________|    |
	# 	   |  |       |
	# 	   |  |       |
	# 	   |  |       |
	# 	   |  |       |
	# 	   |  |       |  l= length
	# 	   |  |       |
	# 	   |  |       |
	# 	   |  |       |
	# 	   |__|    ___|__
	#
	# 	'''
	# 	bolt_head_dia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65, 36: 75}
	#
	# 	return bolt_head_dia[bolt_diameter]

	def nut_thick_calculation(self, bolt_diameter):
		'''
		Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
		'''
		nut_dia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23,
				   30: 25.35, 36: 30.65}
		return nut_dia[bolt_diameter]

	def bolt_length_calculation(self, bolt_diameter):
		'''

		:param self:
		:param bolt_diameter:
		:return:
		'''

		alist = self.designParameters()
		beam_data = self.fetchBeamPara()  # Fetches the beam dimensions
		flangeplatethickness = alist["FlangePlate"]["Thickness (mm)"]
		beam_T = float(beam_data["T"])
		length_required = self.bolt_head_thick_calculation(bolt_diameter) + self.nut_thick_calculation(bolt_diameter) + \
						  2.0 * float(flangeplatethickness) + float(beam_T) + float(self.nut_thick_calculation(bolt_diameter)) + 10.0

		if length_required < 40:
			length_required = 40

		elif length_required > 40 and length_required < 100:
			if length_required % 5 != 0:
				length_required = int(length_required / 5) * 5 + 5
			else:
				length_required = length_required

		elif length_required > 100 and length_required < 300:
			if length_required % 10 != 0:
				length_required = int(length_required / 10) * 10 + 10
			else:
				length_required = length_required

		return length_required

	def call_3DModel(self, bgcolor):
		# Call to calculate/create the BB Cover Plate Bolted CAD model
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.createBBCoverPlateBoltedCAD()
			self.ui.btn3D.setChecked(Qt.Checked)
			if self.ui.btn3D.isChecked():
				self.ui.chkBx_beamSec1.setChecked(Qt.Unchecked)
				self.ui.chkBx_extndPlate.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)

			# Call to display the BB Cover Plate Bolted CAD model
			self.display_3DModel("Model",bgcolor)# "gradient_bg")
		else:
			self.display.EraseAll()

	def call_3DBeam(self, bgcolor):
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.ui.chkBx_beamSec1.setChecked(Qt.Checked)
			if self.ui.chkBx_beamSec1.isChecked():
				self.ui.btn3D.setChecked(Qt.Unchecked)
				self.ui.chkBx_extndPlate.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)
			self.display_3DModel("Beam", bgcolor)

	def call_3DConnector(self, bgcolor):
		status = self.resultObj['Bolt']['status']
		if status is True:
			self.ui.chkBx_extndPlate.setChecked(Qt.Checked)
			if self.ui.chkBx_extndPlate.isChecked():
				self.ui.btn3D.setChecked(Qt.Unchecked)
				self.ui.chkBx_beamSec1.setChecked(Qt.Unchecked)
				self.ui.mytabWidget.setCurrentIndex(0)
			self.display_3DModel("Connector", bgcolor)

	def display_3DModel(self, component, bgcolor):
		self.component = component

		self.display.EraseAll()
		self.display.View_Iso()
		self.display.FitAll()

		self.display.DisableAntiAliasing()
		if bgcolor == "gradient_bg":

			self.display.set_bg_gradient_color(51, 51, 102, 150, 150,
											   170)  # Changes the background color in graphics window iff the design is safe
		else:
			self.display.set_bg_gradient_color(255, 255, 255, 255, 255,
											   255)  # Sets the color of graphics window to dark (black)

		self.CPBoltedObj = self.createBBCoverPlateBoltedCAD()  # CPBoltedObj is an object which gets all the calculated values of CAD models

		if component == "Beam":
			# Displays both beams
			osdag_display_shape(self.display, self.CPBoltedObj.get_beamLModel(), update=True)
			osdag_display_shape(self.display, self.CPBoltedObj.get_beamRModel(), update=True)

		elif component == "Connector":
			# Displays the Flange Plates
			osdag_display_shape(self.display, self.CPBoltedObj.get_plateAbvFlangeModel(), update=True, color='Blue')
			osdag_display_shape(self.display, self.CPBoltedObj.get_plateBelwFlangeModel(), update=True, color='Blue')
			if self.ui.combo_flange_preference.currentText() != 'Outside':
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateAbvFlangeFront(), update=True,color='Blue')
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateAbvFlangeBack(), update=True,color='Blue')
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateBelwFlangeFront(), update=True,color='Blue')
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateBelwFlangeBack(), update=True,color='Blue')

			# Displays the Web Plates
			osdag_display_shape(self.display, self.CPBoltedObj.get_WebPlateLeftModel(), update=True, color='Blue')
			osdag_display_shape(self.display, self.CPBoltedObj.get_WebPlateRightModel(), update=True, color='Blue')

			# Displays the bolts which are above the Flange Plate, debugging will give more clarity
			nutboltlistAF = self.CPBoltedObj.nut_bolt_array_AF.get_modelsAF()
			for nutboltAF in nutboltlistAF:
				osdag_display_shape(self.display, nutboltAF, color=Quantity_NOC_SADDLEBROWN, update=True)

			# Displays the bolts which are below the Flange Plate, debugging will give more clarity
			nutboltlistBF = self.CPBoltedObj.nut_bolt_array_BF.get_modelsBF()
			for nutboltBF in nutboltlistBF:
				osdag_display_shape(self.display, nutboltBF, update=True, color=Quantity_NOC_SADDLEBROWN)

			# Displays the bolts which are on the right side of web plate, debugging will give more clarity
			nutboltlistW = self.CPBoltedObj.nut_bolt_array_Web.get_modelsW()
			for nutboltW in nutboltlistW:
				osdag_display_shape(self.display, nutboltW, update=True, color=Quantity_NOC_SADDLEBROWN)


		elif component == "Model":
			# Displays both beams
			osdag_display_shape(self.display, self.CPBoltedObj.get_beamLModel(), update=True)
			osdag_display_shape(self.display, self.CPBoltedObj.get_beamRModel(), update=True)

			# Displays the Flange Plates
			osdag_display_shape(self.display, self.CPBoltedObj.get_plateAbvFlangeModel(), update=True, color='Blue')
			osdag_display_shape(self.display, self.CPBoltedObj.get_plateBelwFlangeModel(), update=True, color='Blue')
			if self.ui.combo_flange_preference.currentText() != 'Outside':
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateAbvFlangeFront(), update=True,color='Blue')
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateAbvFlangeBack(), update=True,color='Blue')
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateBelwFlangeFront(), update=True,color='Blue')
				osdag_display_shape(self.display, self.CPBoltedObj.get_innerplateBelwFlangeBack(), update=True,color='Blue')

			# Displays the Web Plates
			osdag_display_shape(self.display, self.CPBoltedObj.get_WebPlateLeftModel(), update=True, color='Blue')
			osdag_display_shape(self.display, self.CPBoltedObj.get_WebPlateRightModel(), update=True, color='Blue')

			# Displays the bolts which are above the Flange Plate, debugging will give more clarity
			nutboltlistAF = self.CPBoltedObj.nut_bolt_array_AF.get_modelsAF()
			for nutboltAF in nutboltlistAF:
				osdag_display_shape(self.display, nutboltAF, color=Quantity_NOC_SADDLEBROWN, update=True)

			# Displays the bolts which are below the Flange Plate, debugging will give more clarity
			nutboltlistBF = self.CPBoltedObj.nut_bolt_array_BF.get_modelsBF()
			for nutboltBF in nutboltlistBF:
				osdag_display_shape(self.display, nutboltBF, update=True, color=Quantity_NOC_SADDLEBROWN)

			# Displays the bolts which are on the right side of web plate, debugging will give more clarity
			nutboltlistW = self.CPBoltedObj.nut_bolt_array_Web.get_modelsW()
			for nutboltW in nutboltlistW:
				osdag_display_shape(self.display, nutboltW, update=True, color=Quantity_NOC_SADDLEBROWN)

			# ============================================================================================
	def open_about_osdag(self):
		dialog = MyAboutOsdag(self)
		dialog.show()

	def open_tutorials(self):
		dialog = MyTutorials(self)
		dialog.show()

	def open_ask_question(self):
		dialog = MyAskQuestion(self)
		dialog.show()

	def design_examples(self):
		root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'ResourceFiles', 'design_example', '_build', 'html')
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
	fh = logging.FileHandler(os.path.join('Connections','Moment','BBSpliceCoverPlate','BBSpliceCoverPlateBolted', 'coverplate.log'), mode='a')

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


def launch_coverplate_controller(osdagMainWindow, folder):
	set_osdaglogger()
	# --------------- To display log messages in different colors ---------------
	rawLogger = logging.getLogger("raw")
	rawLogger.setLevel(logging.INFO)
	# fh = logging.FileHandler("Connections\Moment\BBSpliceCoverPlate\BBSpliceCoverPlateBolted\coverplate.log", mode="w")
	file_handler = logging.FileHandler(os.path.join('Connections','Moment','BBSpliceCoverPlate','BBSpliceCoverPlateBolted', 'coverplate.log'), mode='w')
	formatter = logging.Formatter('''%(message)s''')
	file_handler.setFormatter(formatter)
	rawLogger.addHandler(file_handler)
	rawLogger.info(
		'''<link rel="stylesheet" type="text/css" href='''+ os.path.join('Connections','Moment','BBSpliceCoverPlate','BBSpliceCoverPlateBolted', 'log.css') +'''/>''')
	# ----------------------------------------------------------------------------
	module_setup()
	window = MainController(folder)
	osdagMainWindow.hide()
	window.show()
	window.closed.connect(osdagMainWindow.show)


if __name__ == '__main__':
	# --------------- To display log messages in different colors ---------------
	rawLogger = logging.getLogger("raw")
	rawLogger.setLevel(logging.INFO)
	# file_handler = logging.FileHandler(os.path.join('Connections','Moment','BBSpliceCoverPlate','BBSpliceCoverPlateBolted', 'coverplate.log'), mode='w')
	file_handler = logging.FileHandler(os.path.join('..', 'coverplate.log'), mode='w')
	formatter = logging.Formatter('''%(message)s''')
	file_handler.setFormatter(formatter)
	rawLogger.addHandler(file_handler)
	rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')
	app = QApplication(sys.argv)
	module_setup()
	# ----------------------------------------------------------------------------
	folder_path = "/home/reshma/Osdag_workspace/Coverplate"
	if not os.path.exists(folder_path):
		os.mkdir(folder_path, 0755)
	image_folder_path = os.path.join(folder_path, 'images_html')
	if not os.path.exists(image_folder_path):
		os.mkdir(image_folder_path, 0755)
	window = MainController(folder_path)
	window.show()
	sys.exit(app.exec_())
# launch_coverplate_controller()
