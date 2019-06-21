"""
Created on 24-Aug-2017

@author: Reshma
"""

from ui_extendedendplate import Ui_MainWindow
from ui_design_preferences import Ui_DesignPreferences
from ui_design_summary import Ui_DesignReport
from ui_plate import Ui_Plate
from ui_stiffener import Ui_Stiffener
from ui_pitch import Ui_Pitch
from ui_weld_details import Ui_Weld_Details
from ui_weld_details_2 import Ui_Weld_Details_2
from svg_window import SvgWindow
from ui_tutorial import Ui_Tutorial
from ui_aboutosdag import Ui_AboutOsdag
from ui_ask_question import Ui_AskQuestion
from bbExtendedEndPlateSpliceCalc import bbExtendedEndPlateSplice
import bbExtendedEndPlateSpliceCalc as db_value
from reportGenerator import save_html
from drawing_2D_ExtendedBothways import ExtendedEndPlate
from drawing_2D_Extendedoneway import OnewayEndPlate
from drawing_2D_BBFlush import FlushEndPlate


from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFontDialog, QFileDialog
from PyQt5.Qt import QColor, QBrush, Qt, QIntValidator, QDoubleValidator, QFile, QTextStream, pyqtSignal, QColorDialog, QPixmap, QPalette
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
from Connections.Moment.ExtendedEndPlate.bbExtendedEndPlateSpliceCalc import bbExtendedEndPlateSplice
from Connections.Moment.ExtendedEndPlate.extendedBothWays import CADFillet
from Connections.Moment.ExtendedEndPlate.extendedBothWays import CADGroove
from Connections.Moment.ExtendedEndPlate.nutBoltPlacement import NutBoltArray
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
		boltFu = int(boltGrd) * 100 # Nominal strength of bolt
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
		resultObj_plate = bbExtendedEndPlateSplice(uiObj)
		self.ui.txt_plateWidth.setText(str(resultObj_plate["Plate"]["Width"]))
		self.ui.txt_plateHeight.setText(str(resultObj_plate["Plate"]["Height"]))
		self.ui.txt_plateDemand.setText(str(resultObj_plate["Plate"]["MomentDemand"]))
		self.ui.txt_plateCapacity.setText(str(resultObj_plate["Plate"]["MomentCapacity"]))


class Stiffener(QDialog):
   def __init__(self, parent=None):
      QDialog.__init__(self, parent)
      self.ui = Ui_Stiffener()
      self.ui.setupUi(self)
      self.maincontroller = parent
      uiObj = self.maincontroller.designParameters()
      resultObj_plate = bbExtendedEndPlateSplice(uiObj)

      # loc = self.ui.plateHeight.currentText()

      if uiObj["Member"]["Connectivity"] == "Flush":
         self.ui.plateHeight.setText("Width (mm)")
         self.ui.widget.setPixmap(QtGui.QPixmap(":/newPrefix/images/flush_stiffener.png"))
         self.ui.txt_stiffnrHeight.setText(str(resultObj_plate['Stiffener']['Height']))
         self.ui.txt_stiffnrLength.setText(str(resultObj_plate["Stiffener"]["Length"]))
         self.ui.txt_stiffnrThickness.setText(str(resultObj_plate["Stiffener"]["Thickness"]))
         self.ui.txt_stiffnrThickness_2.setText(str(resultObj_plate['Stiffener']['Moment']))
         self.ui.txt_stiffnrThickness_3.setText(str(resultObj_plate['Stiffener']['MomentCapacity']))

      else:
         self.ui.plateHeight.setText("Height (mm)")
         self.ui.widget.setPixmap(QtGui.QPixmap(":/newPrefix/images/eep_stiffener.png"))
         self.ui.txt_stiffnrHeight.setText(str(resultObj_plate["Stiffener"]["Height"]))
         self.ui.txt_stiffnrLength.setText(str(resultObj_plate["Stiffener"]["Length"]))
         self.ui.txt_stiffnrThickness.setText(str(resultObj_plate["Stiffener"]["Thickness"]))
         self.ui.txt_stiffnrThickness_2.setText(str(resultObj_plate['Stiffener']['Moment']))
         self.ui.txt_stiffnrThickness_3.setText(str(resultObj_plate['Stiffener']['MomentCapacity']))
class Weld_Details(QDialog):
   def __init__(self, parent = None):
      QDialog.__init__(self, parent)
      self.maincontroller = parent
      if self.maincontroller.ui.combo_weld_method.currentText() == "Groove Weld (CJP)":
         self.ui = Ui_Weld_Details()
         self.ui.setupUi(self)
      else :
         self.ui = Ui_Weld_Details_2()
         self.ui.setupUi(self)

      uiObj = self.maincontroller.designParameters()
      self.resultObj_plate = bbExtendedEndPlateSplice(uiObj)

      if self.maincontroller.ui.combo_weld_method.currentText() == "Groove Weld (CJP)":
         self.groove_details()
      else :
         self.fillet_details()

   def groove_details(self):
      self.ui.label_note_1.setText("All dimensions are in mm")
      if db_value.beam_tf <= 12:
         self.ui.label_picture_1.setPixmap(QtGui.QPixmap(":/newPrefix/images/Butt_weld_single_bevel_flange.png"))
         self.ui.label_note_2.setText("As flange thickness, tf (%d mm) <= 12 mm, single bevel butt welding is provided [Reference: IS 9595:1996]." % int(db_value.beam_tf))
      else :
         self.ui.label_picture_1.setPixmap(QtGui.QPixmap(":/newPrefix/images/Butt_weld_double_bevel_flange.png"))
         self.ui.label_note_2.setText("As flange thickness, tf (%d mm) > 12 mm, double bevel butt welding is provided [Reference: IS 9595:1996]." % int(db_value.beam_tf))
      if db_value.beam_tw <= 12:
         self.ui.label_picture_2.setPixmap(QtGui.QPixmap(":/newPrefix/images/Butt_weld_single_bevel_web.png"))
         self.ui.label_note_3.setText("As web thickness, tw (%d mm) <= 12 mm, single bevel butt welding is provided [Reference: IS 9595:1996]." % int(db_value.beam_tw))
      else :
         self.ui.label_picture_2.setPixmap(QtGui.QPixmap(":/newPrefix/images/Butt_weld_double_bevel_web.png"))
         self.ui.label_note_3.setText("As web thickness, tw (%d mm) > 12 mm, double bevel butt welding is provided [Reference: IS 9595:1996]." % int(db_value.beam_tw))
   def fillet_details(self):
      self.ui.lineEdit_flange_critical_stress.setText(str(self.resultObj_plate["Weld"]["CriticalStressflange"]))
      self.ui.lineEdit_flange_strength.setText(str(self.resultObj_plate["Weld"]["WeldStrength"]))
      self.ui.lineEdit_web_critical_stress.setText(str(self.resultObj_plate["Weld"]["CriticalStressWeb"]))
      self.ui.lineEdit_web_strength.setText(str(self.resultObj_plate["Weld"]["WeldStrength"]))


class Pitch(QDialog):
   def __init__(self, parent=None):
      QDialog.__init__(self, parent)
      self.ui = Ui_Pitch()
      self.ui.setupUi(self)
      self.maincontroller = parent

      uiObj = self.maincontroller.designParameters()
      resultObj_plate = bbExtendedEndPlateSplice(uiObj)
      print "result plate", resultObj_plate
      no_of_bolts = resultObj_plate['Bolt']['NumberOfBolts']

      if uiObj["Member"]["Connectivity"] == "Flush":

         if no_of_bolts == 4:
            pixmap = QPixmap(":/newPrefix/images/Flush/Flush_4.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
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



         elif no_of_bolts == 6:
            pixmap = QPixmap(":/newPrefix/images/Flush/Flush_6.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch12']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lbl_1.setText('Pitch 1-2')
            self.ui.lbl_2.setText('Pitch 2-3')
            self.ui.lbl_mem3.hide()
            self.ui.lbl_mem4.hide()
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lbl_3.hide()
            self.ui.lbl_4.hide()
            self.ui.lbl_5.hide()
            self.ui.lbl_6.hide()
            self.ui.lbl_7.hide()
            self.ui.lineEdit_pitch3.hide()
            self.ui.lineEdit_pitch4.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()


      elif uiObj["Member"]["Connectivity"] == "Extended one way":

         if no_of_bolts == 6:
            pixmap = QPixmap(":/newPrefix/images/One_way/OWE_6.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lbl_1.setText('Pitch 2-3')
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

         elif no_of_bolts == 8:
            pixmap = QPixmap(":/newPrefix/images/One_way/OWE_8.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lbl_1.setText('Pitch 2-3')
            self.ui.lbl_2.setText('Pitch 3-4')
            self.ui.lbl_mem3.hide()
            self.ui.lbl_mem4.hide()
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lbl_3.hide()
            self.ui.lbl_4.hide()
            self.ui.lbl_5.hide()
            self.ui.lbl_6.hide()
            self.ui.lbl_7.hide()
            self.ui.lineEdit_pitch3.hide()
            self.ui.lineEdit_pitch4.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()

         elif no_of_bolts == 10:
            pixmap = QPixmap(":/newPrefix/images/One_way/OWE_10.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch12']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lbl_1.setText('Pitch 1-2')
            self.ui.lbl_2.setText('Pitch 3-4')
            self.ui.lbl_3.setText('Pitch 4-5')
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
      else:

         if no_of_bolts == 8:
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch']))
            pixmap = QPixmap(":/newPrefix/images/Both_way/BW_8.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
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
            pixmap = QPixmap(":/newPrefix/images/Both_way/BW_12.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lbl_1.setText('Pitch 2-3')
            self.ui.lbl_2.setText('Pitch 3-4')
            self.ui.lbl_3.setText('Pitch 4-5')
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
            pixmap = QPixmap(":/newPrefix/images/Both_way/BW_16.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch23']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lineEdit_pitch4.setText(str(resultObj_plate['Bolt']['Pitch56']))
            self.ui.lineEdit_pitch5.setText(str(resultObj_plate['Bolt']['Pitch67']))
            self.ui.lbl_1.setText('Pitch 2-3')
            self.ui.lbl_2.setText('Pitch 3-4')
            self.ui.lbl_3.setText('Pitch 4-5')
            self.ui.lbl_4.setText('Pitch 5-6')
            self.ui.lbl_5.setText('Pitch 6-7')
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lbl_6.hide()
            self.ui.lbl_7.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
         elif no_of_bolts == 20:
            pixmap = QPixmap(":/newPrefix/images/Both_way/BW_20.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.label_3.setPixmap(pixmap)
            self.ui.lineEdit_pitch.setText(str(resultObj_plate['Bolt']['Pitch12']))
            self.ui.lineEdit_pitch2.setText(str(resultObj_plate['Bolt']['Pitch34']))
            self.ui.lineEdit_pitch3.setText(str(resultObj_plate['Bolt']['Pitch45']))
            self.ui.lineEdit_pitch4.setText(str(resultObj_plate['Bolt']['Pitch56']))
            self.ui.lineEdit_pitch5.setText(str(resultObj_plate['Bolt']['Pitch67']))
            self.ui.lineEdit_pitch6.setText(str(resultObj_plate['Bolt']['Pitch78']))
            self.ui.lineEdit_pitch7.setText(str(resultObj_plate['Bolt']['Pitch910']))
            self.ui.lbl_1.setText('Pitch 1-2')
            self.ui.lbl_2.setText('Pitch 3-4')
            self.ui.lbl_3.setText('Pitch 4-5')
            self.ui.lbl_4.setText('Pitch 5-6')
            self.ui.lbl_5.setText('Pitch 6-7')
            self.ui.lbl_6.setText('Pitch 7-8')
            self.ui.lbl_7.setText('Pitch 9-10')

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
			cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.maincontroller.folder), "images_html", "cmpylogoExtendEndplate.svg"))
		else:
			shutil.copyfile(filename, os.path.join(str(self.maincontroller.folder), "images_html", "cmpylogoExtendEndplate.png"))

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
      self.connection = "Extended"
      self.get_beamdata()
      self.result_obj = None
      self.ui.combo_weld_method.currentTextChanged.connect(self.on_change)

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

      self.ui.btnFront.clicked.connect(lambda : self.call_2D_drawing("Front"))
      self.ui.btnTop.clicked.connect(lambda : self.call_2D_drawing("Top"))
      self.ui.btnSide.clicked.connect(lambda : self.call_2D_drawing("Side"))
      self.ui.actionfinPlate_quit.setShortcut('Ctrl+Q')
      self.ui.actionfinPlate_quit.setStatusTip('Exit application')
      self.ui.actionfinPlate_quit.triggered.connect(qApp.quit)

      self.ui.combo_diameter.currentIndexChanged[str].connect(self.bolt_hole_clearance)
      self.ui.combo_grade.currentIndexChanged[str].connect(self.call_bolt_fu)
      self.ui.txt_Fu.textChanged.connect(self.call_weld_fu)

      self.ui.btn_Design.clicked.connect(self.design_btnclicked)
      self.ui.btn_Design.clicked.connect(self.osdag_header)
      self.ui.btn_Design.clicked.connect(self.osdag_image1)
      self.ui.btn_Design.clicked.connect(self.osdag_image2)
      self.ui.btn_Design.clicked.connect(self.osdag_image3)
      self.ui.btn_Design.clicked.connect(self.osdag_image4)
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
      self.ui.actionSave_Front_View.triggered.connect(lambda : self.call_2D_drawing("Front"))
      self.ui.actionSave_Side_View.triggered.connect(lambda : self.call_2D_drawing("Side"))
      self.ui.actionSave_Top_View.triggered.connect(lambda : self.call_2D_drawing("Top"))
      self.ui.actionShow_all.triggered.connect(lambda: self.call_3DModel("gradient_bg"))
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
      self.ui.btn_weldDetails.clicked.connect(self.weld_details)
      self.ui.btn_CreateDesign.clicked.connect(self.design_report)
      self.ui.btn_SaveMessages.clicked.connect(self.save_log_messages)

      self.ui.btn3D.clicked.connect(lambda : self.call_3DModel("gradient_bg"))
      self.ui.chkBx_beamSec.clicked.connect(lambda : self.call_3DBeam("gradient_bg"))
      self.ui.chkBx_connector.clicked.connect(lambda :self.call_3DConnector("gradient_bg"))

      validator = QIntValidator()

      doubl_validator = QDoubleValidator()
      self.ui.txt_Fu.setValidator(doubl_validator)
      self.ui.txt_Fy.setValidator(doubl_validator)
      self.ui.txt_Moment.setValidator(doubl_validator)
      self.ui.txt_Shear.setValidator(doubl_validator)
      self.ui.txt_Axial.setValidator(doubl_validator)
      self.ui.txt_plateHeight.setValidator(doubl_validator)
      self.ui.txt_plateWidth.setValidator(doubl_validator)

      min_fu = 410  # The values of ultimate strength have been referred from IS 2062:2011
      max_fu = 780
      self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))
      self.ui.txt_Fu.editingFinished.connect(lambda: self.validate_fu_fy(self.ui.txt_Fu, self.ui.txt_Fy, self.ui.txt_Fu, self.ui.lbl_fu))

      min_fy = 230  # The values of yield strength have been referred from IS 2062:2011
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

   def on_change(self):
      if self.ui.combo_weld_method.currentText() == "Groove Weld (CJP)":
         self.ui.combo_webSize.setCurrentIndex(1)
         self.ui.combo_flangeSize.setCurrentIndex(1)
         self.ui.combo_flangeSize.setDisabled(True)
         self.ui.combo_webSize.setDisabled(True)
      else:
         self.ui.combo_webSize.setCurrentIndex(0)
         self.ui.combo_flangeSize.setCurrentIndex(0)
         self.ui.combo_flangeSize.setEnabled(True)
         self.ui.combo_webSize.setEnabled(True)

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
         self.move((resolution.width()/2) - (self.frameSize().width()/2),
                 (resolution.height()/2) - (self.frameSize().height()/2))

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

   def save_file(self,filename):
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

      config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path )

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
      self.result = bbExtendedEndPlateSplice(self.alist)
      print "resultobj", self.result
      self.beam_data = self.fetchBeamPara()
      save_html(self.result, self.alist, self.beam_data, fileName, report_summary, self.folder)

   def get_user_inputs(self):
      uiObj = {}
      uiObj["Member"] = {}
      uiObj["Member"]["Connectivity"] = str(self.ui.combo_connLoc.currentText())
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
      uiObj["Plate"]["Height (mm)"] = str(self.ui.txt_plateHeight.text())
      uiObj["Plate"]["Width (mm)"] = str(self.ui.txt_plateWidth.text())

      uiObj["Weld"] = {}
      uiObj["Weld"]["Type"] = str(self.ui.combo_weld_method.currentText())
      uiObj["Weld"]["Flange (mm)"] = str(self.ui.combo_flangeSize.currentText())
      uiObj["Weld"]["Web (mm)"] = str(self.ui.combo_webSize.currentText())
      uiObj["Connection"] = self.connection
      return uiObj

   def osdag_header(self):
      image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
      shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

   def osdag_image1(self):  # This function is created for calling the single butt weld (flange) image in design report
      image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("Connections/Moment/ExtendedEndPlate/ResourceFiles/images", "Butt_weld_single_bevel_flange.png")))
      shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Butt_weld_single_bevel_flange.png"))

   def osdag_image2(self):  # This function is created for calling the double butt weld (flange) image in design report
      image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("Connections/Moment/ExtendedEndPlate/ResourceFiles/images", "Butt_weld_double_bevel_flange.png")))
      shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Butt_weld_double_bevel_flange.png"))

   def osdag_image3(self):  # This function is created for calling the single butt weld (web) image in design report
      image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("Connections/Moment/ExtendedEndPlate/ResourceFiles/images", "Butt_weld_single_bevel_web.png")))
      shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Butt_weld_single_bevel_web.png"))

   def osdag_image4(self):  # This function is created for calling the single butt weld (web) image in design report
      image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("Connections/Moment/ExtendedEndPlate/ResourceFiles/images", "Butt_weld_double_bevel_web.png")))
      shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Butt_weld_double_bevel_web.png"))


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
      input_file = QFile(os.path.join("Connections","Moment","ExtendedEndPlate","saveINPUT.txt"))
      if not input_file.open(QFile.WriteOnly | QFile.Text):
         QMessageBox.warning(self, "Application",
                        "Cannot write file %s: \n%s"
                        % (input_file.fileName(), input_file.errorString()))
      pickle.dump(uiObj, input_file)

   def get_prevstate(self):
      """

      Returns: Read for the previous user inputs design

      """
      filename = os.path.join("Connections","Moment","ExtendedEndPlate","saveINPUT.txt")
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
         if uiObj["Connection"] != "Extended":
            QMessageBox.information(self, "Information", "You can load this input file only from the corresponding design problem")
            return

         self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(str(uiObj["Member"]["Connectivity"])))
         if uiObj["Member"]["Connectivity"] == "Flush" or "Extended one way" or "Extended both ways":
            self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(uiObj["Member"]["Connectivity"]))
            self.ui.combo_beamSec.setCurrentIndex(self.ui.combo_beamSec.findText(uiObj["Member"]["BeamSection"]))
            self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
            self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
            self.ui.txt_Shear.setText(str(uiObj["Load"]["ShearForce (kN)"]))
            self.ui.txt_Axial.setText(str(uiObj["Load"]["AxialForce (kN)"]))
            self.ui.txt_Moment.setText(str(uiObj["Load"]["Moment (kNm)"]))
            self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
            self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
            self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
            self.ui.combo_plateThick.setCurrentIndex(self.ui.combo_plateThick.findText(uiObj["Plate"]["Thickness (mm)"]))
            self.ui.txt_plateHeight.setText(str(uiObj["Plate"]["Height (mm)"]))
            self.ui.txt_plateWidth.setText(str(uiObj["Plate"]["Width (mm)"]))
            self.ui.combo_weld_method.setCurrentIndex(self.ui.combo_weld_method.findText(uiObj["Weld"]["Type"]))

            self.ui.combo_flangeSize.setCurrentIndex(self.ui.combo_flangeSize.findText(uiObj["Weld"]["Flange (mm)"]))
            self.ui.combo_webSize.setCurrentIndex(self.ui.combo_webSize.findText(uiObj["Weld"]["Web (mm)"]))

            self.designPrefDialog.ui.combo_boltType.setCurrentIndex(self.designPrefDialog.ui.combo_boltType.findText(uiObj["bolt"]["bolt_type"]))
            self.designPrefDialog.ui.combo_boltHoleType.setCurrentIndex(self.designPrefDialog.ui.combo_boltHoleType.findText(uiObj["bolt"]["bolt_hole_type"]))
            self.designPrefDialog.ui.txt_boltFu.setText(str(uiObj["bolt"]["bolt_fu"]))
            self.designPrefDialog.ui.combo_slipfactor.setCurrentIndex(self.designPrefDialog.ui.combo_slipfactor.findText(str(uiObj["bolt"]["slip_factor"])))
            self.designPrefDialog.ui.combo_weldType.setCurrentIndex(
               self.designPrefDialog.ui.combo_weldType.findText(uiObj["weld"]["typeof_weld"]))
            self.designPrefDialog.ui.txt_weldFu.setText(str(uiObj["weld"]["fu_overwrite"]))
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
      #  design_pref = self.designPrefDialog.save_default_para()
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
      if loc == "Extended both ways":
         pixmap = QPixmap(":/newPrefix/images/ebw_ep.png")
         pixmap.scaledToHeight(60)
         pixmap.scaledToWidth(50)
         self.ui.lbl_connectivity.setPixmap(pixmap)
      elif loc == "Extended one way":
         pixmap = QPixmap(":/newPrefix/images/owe_ep.png")
         pixmap.scaledToHeight(60)
         pixmap.scaledToWidth(50)
         self.ui.lbl_connectivity.setPixmap(pixmap)
      elif loc == "Flush":
         pixmap = QPixmap(":/newPrefix/images/flush_ep.png")
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
      #  incomplete_list.append("Axial force")

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

      if self.ui.combo_webSize.currentIndex() == 0 and self.ui.combo_weld_method.currentIndex() == 1:
         incomplete_list.append("Web weld thickness")

      if self.ui.combo_flangeSize.currentIndex() == 0 and self.ui.combo_weld_method.currentIndex() == 1:
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
      self.outputs = bbExtendedEndPlateSplice(self.alist)
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

      critical_tension = resultObj["Bolt"]["CriticalTension"]
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

      bolts_in_rows = resultObj["Bolt"]["NumberOfRows"]
      self.ui.txt_rowBolts.setText(str(bolts_in_rows))

      # pitch = resultObj["Bolt"]["Pitch"]
      # self.ui.txt_pitch.setText(str(pitch))

      gauge = resultObj["Bolt"]["Gauge"]
      self.ui.txt_gauge.setText(str(gauge))

      cross_centre_gauge = resultObj["Bolt"]["CrossCentreGauge"]
      self.ui.txt_crossGauge.setText(str(cross_centre_gauge))

      end_distance = resultObj["Bolt"]["End"]
      self.ui.txt_endDist.setText(str(end_distance))

      edge_distance = resultObj["Bolt"]["Edge"]
      self.ui.txt_edgeDist.setText(str(edge_distance))


   def display_log_to_textedit(self):
      file = QFile(os.path.join('Connections','Moment','ExtendedEndPlate','extnd.log'))
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
      self.ui.chkBx_beamSec.setEnabled(False)
      self.ui.chkBx_connector.setEnabled(False)
      self.ui.btn_pitchDetail.setEnabled(False)
      self.ui.btn_plateDetail.setEnabled(False)
      self.ui.btn_stiffnrDetail.setEnabled(False)
      self.ui.btn_weldDetails.setEnabled(False)

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
      self.ui.btnSide.setEnabled(True)
      self.ui.btn3D.setEnabled(True)
      self.ui.chkBx_beamSec.setEnabled(True)
      self.ui.chkBx_connector.setEnabled(True)
      self.ui.btn_pitchDetail.setEnabled(True)
      self.ui.btn_plateDetail.setEnabled(True)
      self.ui.btn_stiffnrDetail.setEnabled(True)
      self.ui.btn_weldDetails.setEnabled(True)

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
      self.ui.combo_plateThick.setCurrentIndex(0)
      self.ui.txt_plateHeight.clear()
      self.ui.txt_plateWidth.clear()
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

      self.ui.btn_pitchDetail.setDisabled(True)
      self.ui.btn_plateDetail.setDisabled(True)
      self.ui.btn_stiffnrDetail.setDisabled(True)
      self.ui.btn_weldDetails.setDisabled(True)

      self.display.EraseAll()
      self.designPrefDialog.save_default_para()

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

            if str(self.ui.combo_connLoc.currentText()) == "Extended both ways" or "Flush" or "Extended one way":
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
      self.result_obj = bbExtendedEndPlateSplice(self.alist)
      self.beam_data = self.fetchBeamPara()

      if self.alist["Member"]["Connectivity"] == "Extended both ways":
         beam_beam = ExtendedEndPlate(self.alist, self.result_obj, self.beam_data, self.folder)
      elif self.alist["Member"]["Connectivity"] == "Extended one way":
         beam_beam = OnewayEndPlate(self.alist, self.result_obj, self.beam_data, self.folder)
      elif self.alist["Member"]["Connectivity"] == "Flush":
         beam_beam = FlushEndPlate(self.alist, self.result_obj, self.beam_data, self.folder)


      status = self.resultObj['Bolt']['status']
      if status is True:
         if view != "All":
            if view == "Front":
               filename = os.path.join(str(self.folder), "images_html", "extendFront.svg")

            elif view == "Side":
               filename = os.path.join(str(self.folder), "images_html", "extendSide.svg")

            else:
               filename = os.path.join(str(self.folder), "images_html", "extendTop.svg")

            beam_beam.save_to_svg(filename, view)
            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, str(self.folder))
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

   def weld_details(self):
      section = Weld_Details(self)
      section.show()

   def design_report(self):
      design_report_dialog = DesignReportDialog(self)
      design_report_dialog.show()

      # fileName = ("Connections\Moment\ExtendedEndPlate\Html_Report.html")
      # fileName = str(fileName)
      # self.alist = self.designParameters()
      # self.result = bbExtendedEndPlateSplice(self.alist)
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
      if self.component == "Beam":
         cadlist = self.ExtObj.get_beam_models()
         final_model = cadlist[0]
         for model in cadlist[1:]:
             final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

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
         fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"), files_types)
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

      beam_data = self.fetchBeamPara()

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
                    length=beam_length, notchObj=None)
      beam_Right = copy.copy(beam_Left)   # Since both the beams are same

      outputobj = self.outputs    # Save all the claculated/displayed out in outputobj

      plate_Left = Plate(W=outputobj["Plate"]["Width"],
                     L=outputobj["Plate"]["Height"],
                     T=outputobj["Plate"]["Thickness"])
      plate_Right = copy.copy(plate_Left)     # Since both the end plates are identical

      #Beam stiffeners 4 if extended both ways, only 1 and 3 if extended oneway and non for flus type
      beam_stiffener_1 = StiffenerPlate(W=outputobj['Stiffener']['Height'], L=outputobj['Stiffener']['Length'],
                                T=outputobj['Stiffener']['Thickness'], R11=outputobj['Stiffener']['Length'] - 25,
                                R12=outputobj['Stiffener']['Height']-25,
                                L21=outputobj['Stiffener']['NotchSize'],L22 =outputobj['Stiffener']['NotchSize'])       #TODO: given hard inputs to L21 and L22

      beam_stiffener_2 = copy.copy(beam_stiffener_1)
      beam_stiffener_3 = copy.copy(beam_stiffener_1)
      beam_stiffener_4 = copy.copy(beam_stiffener_1)


      #Beam stiffeners for the flush type endplate
      beam_stiffener_F1 =  StiffenerPlate(W=outputobj['Stiffener']['Height'], L=outputobj['Stiffener']['Length'],
                                T=outputobj['Stiffener']['Thickness'],
                                L21=outputobj['Stiffener']['NotchSize'],L22 =outputobj['Stiffener']['NotchSize'])

      beam_stiffener_F2 = copy.copy(beam_stiffener_F1)
      beam_stiffener_F3 = copy.copy(beam_stiffener_F1)
      beam_stiffener_F4 = copy.copy(beam_stiffener_F1)


      alist = self.designParameters()         # An object to save all input values entered by user

      bolt_d = float(alist["Bolt"]["Diameter (mm)"])      # Bolt diameter, entered by user
      bolt_r = bolt_d/2
      bolt_T = self.bolt_head_thick_calculation(bolt_d)
      bolt_R = self.bolt_head_dia_calculation(bolt_d) / 2
      bolt_Ht = self.bolt_length_calculation(bolt_d)

      bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)    # Call to create Bolt from Component repo
      nut_T = self.nut_thick_calculation(bolt_d)
      nut_Ht = nut_T
      nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

      numberOfBolts = int(outputobj["Bolt"]["NumberOfBolts"])

      nutSpace = 2 * float(outputobj["Plate"]["Thickness"]) + nut_T   # Space between bolt head and nut

      bbNutBoltArray = NutBoltArray(alist, beam_data, outputobj, nut, bolt, numberOfBolts, nutSpace, alist)

      # Following welds are for to weld stiffeners for extended bothways and ext4ended oneway
      # bbWeld for stiffener hight on left side
      bbWeldStiffHL_1 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                            L=outputobj['Stiffener'][
                                 'Height'] - outputobj['Stiffener'][
                                 'NotchSize'])  # outputobj['Stiffener']['Length'] - 25
      bbWeldStiffHL_2 = copy.copy(bbWeldStiffHL_1)
      bbWeldStiffHL_3 = copy.copy(bbWeldStiffHL_1)
      bbWeldStiffHL_4 = copy.copy(bbWeldStiffHL_1)

      # bbWeld for stiffener length on left side
      bbWeldStiffLL_1 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                            L=outputobj['Stiffener']['Length'] - outputobj['Stiffener']['NotchSize'])
      bbWeldStiffLL_2 = copy.copy(bbWeldStiffLL_1)
      bbWeldStiffLL_3 = copy.copy(bbWeldStiffLL_1)
      bbWeldStiffLL_4 = copy.copy(bbWeldStiffLL_1)

      # bbWeld for stiffener hight on Right side
      bbWeldStiffHR_1 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                            L=outputobj['Stiffener'][
                                 'Height'] - outputobj['Stiffener'][
                                 'NotchSize'])  # outputobj['Stiffener']['Length'] - 25
      bbWeldStiffHR_2 = copy.copy(bbWeldStiffHR_1)
      bbWeldStiffHR_3 = copy.copy(bbWeldStiffHR_1)
      bbWeldStiffHR_4 = copy.copy(bbWeldStiffHR_1)

      # bbWeld for stiffener length on right side
      bbWeldStiffLR_1 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                            L=outputobj['Stiffener']['Length'] - outputobj['Stiffener']['NotchSize'])
      bbWeldStiffLR_2 = copy.copy(bbWeldStiffLR_1)
      bbWeldStiffLR_3 = copy.copy(bbWeldStiffLR_1)
      bbWeldStiffLR_4 = copy.copy(bbWeldStiffLR_1)


      #following welds are fillet welds for the flush endplate stiffeners
      bbWeldstiff1_u1 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                            L=outputobj['Stiffener']['Height'] - outputobj['Stiffener']['NotchSize'])
      bbWeldstiff1_l1 = copy.copy(bbWeldstiff1_u1)
      bbWeldstiff2_u1 = copy.copy(bbWeldstiff1_u1)
      bbWeldstiff2_l1 = copy.copy(bbWeldstiff1_u1)
      bbWeldstiff3_u1 = copy.copy(bbWeldstiff1_u1)
      bbWeldstiff3_l1 = copy.copy(bbWeldstiff1_u1)
      bbWeldstiff4_u1 = copy.copy(bbWeldstiff1_u1)
      bbWeldstiff4_l1 = copy.copy(bbWeldstiff1_u1)

      bbWeldstiff1_u2 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]),
                            L=outputobj['Stiffener']['Length'] - outputobj['Stiffener']['NotchSize'])
      bbWeldstiff1_l2 = copy.copy(bbWeldstiff1_u2)
      bbWeldstiff2_u2 = copy.copy(bbWeldstiff1_u2)
      bbWeldstiff2_l2 = copy.copy(bbWeldstiff1_u2)
      bbWeldstiff3_u2 = copy.copy(bbWeldstiff1_u2)
      bbWeldstiff3_l2 = copy.copy(bbWeldstiff1_u2)
      bbWeldstiff4_u2 = copy.copy(bbWeldstiff1_u2)
      bbWeldstiff4_l2 = copy.copy(bbWeldstiff1_u2)


      if alist["Weld"]["Type"] == "Fillet Weld":

         ###########################
         #       WELD SECTIONS     #
         ###########################
         '''
         Following sections are for creating Fillet Welds. 
         Welds are numbered from Top to Bottom in Z-axis, Front to Back in Y axis and Left to Right in X axis. 
         '''

         # Followings welds are welds above beam flange, Qty = 4
         bbWeldAbvFlang_11 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]), h=float(alist["Weld"]["Flange (mm)"]), L=beam_B)
         bbWeldAbvFlang_12 = copy.copy(bbWeldAbvFlang_11)
         bbWeldAbvFlang_21 = copy.copy(bbWeldAbvFlang_11)
         bbWeldAbvFlang_22 = copy.copy(bbWeldAbvFlang_11)

         # Followings welds are welds below beam flange, Qty = 8
         bbWeldBelwFlang_11 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]), h=float(alist["Weld"]["Flange (mm)"]), L=(beam_B - beam_tw )/ 2- beam_R1-beam_R2)
         bbWeldBelwFlang_12 = copy.copy(bbWeldBelwFlang_11)
         bbWeldBelwFlang_13 = copy.copy(bbWeldBelwFlang_11)
         bbWeldBelwFlang_14 = copy.copy(bbWeldBelwFlang_11)
         bbWeldBelwFlang_21 = copy.copy(bbWeldBelwFlang_11)
         bbWeldBelwFlang_22 = copy.copy(bbWeldBelwFlang_11)
         bbWeldBelwFlang_23 = copy.copy(bbWeldBelwFlang_11)
         bbWeldBelwFlang_24 = copy.copy(bbWeldBelwFlang_11)

         # Followings welds are welds placed aside of beam web, Qty = 4
         bbWeldSideWeb_11 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]), L=beam_d - 2 * (beam_T+beam_R1) - (2*5))
         bbWeldSideWeb_12 = copy.copy(bbWeldSideWeb_11)
         bbWeldSideWeb_21 = copy.copy(bbWeldSideWeb_11)
         bbWeldSideWeb_22 = copy.copy(bbWeldSideWeb_11)


         extbothWays = CADFillet(beam_Left, beam_Right, plate_Left, plate_Right, bbNutBoltArray,
                                 bbWeldAbvFlang_11, bbWeldAbvFlang_12, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                                 bbWeldBelwFlang_11, bbWeldBelwFlang_12, bbWeldBelwFlang_13, bbWeldBelwFlang_14,
                                 bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24,
                                 bbWeldSideWeb_11, bbWeldSideWeb_12, bbWeldSideWeb_21, bbWeldSideWeb_22,
                              bbWeldstiff1_u1,bbWeldstiff1_u2,bbWeldstiff2_u1,bbWeldstiff2_u2,bbWeldstiff3_u1,
                              bbWeldstiff3_u2,bbWeldstiff4_u1,bbWeldstiff4_u2,
                           bbWeldstiff1_l1, bbWeldstiff1_l2, bbWeldstiff2_l1, bbWeldstiff2_l2, bbWeldstiff3_l1,
                           bbWeldstiff3_l2, bbWeldstiff4_l1, bbWeldstiff4_l2,
                              bbWeldStiffHL_1, bbWeldStiffHL_2, bbWeldStiffHL_3, bbWeldStiffHL_4,
                              bbWeldStiffLL_1, bbWeldStiffLL_2, bbWeldStiffLL_3, bbWeldStiffLL_4,
                              bbWeldStiffHR_1, bbWeldStiffHR_2, bbWeldStiffHR_3, bbWeldStiffHR_4,
                              bbWeldStiffLR_1, bbWeldStiffLR_2, bbWeldStiffLR_3, bbWeldStiffLR_4,
                                 beam_stiffener_1,beam_stiffener_2,beam_stiffener_3,beam_stiffener_4,
                           beam_stiffener_F1,beam_stiffener_F2,beam_stiffener_F3,beam_stiffener_F4, alist, outputobj)
         extbothWays.create_3DModel()

         return extbothWays

      else:  # Groove Weld
         bbWeldFlang_R1 = GrooveWeld(b=outputobj['Stiffener']['WeldSize'], h=float(beam_data["T"]),
                              L=beam_B)         #outputobj["Weld"]["Size"]
         bbWeldFlang_R2 = copy.copy(bbWeldFlang_R1)

         bbWeldFlang_L1 = copy.copy(bbWeldFlang_R1)
         bbWeldFlang_L2 = copy.copy(bbWeldFlang_R1)

         # Followings welds are welds placed aside of beam web, Qty = 4           # edited length value by Anand Swaroop
         bbWeldWeb_R3 = GrooveWeld(b=outputobj['Stiffener']['WeldSize'], h=float(beam_data["tw"]),
                            L=beam_d - 2 * beam_T)       #outputobj["Weld"]["Size"]

         bbWeldWeb_L3 = copy.copy(bbWeldWeb_R3)

         #Following welds are to join beam stiffeners to the beam
         bbWeldStiffH_1 = GrooveWeld(b=outputobj['Stiffener']['WeldSize'], h= outputobj['Stiffener']['Thickness'], L= outputobj['Stiffener']['Height']-outputobj['Stiffener']['NotchSize'])    #outputobj['Stiffener']['Length'] - 25
         bbWeldStiffH_2 = copy.copy(bbWeldStiffH_1)
         bbWeldStiffH_3 = copy.copy(bbWeldStiffH_1)
         bbWeldStiffH_4 = copy.copy(bbWeldStiffH_1)

         bbWeldStiffL_1 = GrooveWeld(b=outputobj['Stiffener']['WeldSize'], h= outputobj['Stiffener']['Thickness'], L= outputobj['Stiffener']['Length']-outputobj['Stiffener']['NotchSize'])
         bbWeldStiffL_2 = copy.copy(bbWeldStiffL_1)
         bbWeldStiffL_3 = copy.copy(bbWeldStiffL_1)
         bbWeldStiffL_4 = copy.copy(bbWeldStiffL_1)


         #######################################
         #       WELD SECTIONS QUARTER CONE    #
         #######################################

         extbothWays = CADGroove(beam_Left, beam_Right,plate_Left, plate_Right, bbNutBoltArray,
                           bbWeldFlang_R1, bbWeldFlang_R2, bbWeldWeb_R3,bbWeldFlang_L1, bbWeldFlang_L2, bbWeldWeb_L3,
                           bbWeldStiffHL_1, bbWeldStiffHL_2, bbWeldStiffHL_3, bbWeldStiffHL_4,
                           bbWeldStiffLL_1, bbWeldStiffLL_2, bbWeldStiffLL_3, bbWeldStiffLL_4,
                           bbWeldStiffHR_1, bbWeldStiffHR_2, bbWeldStiffHR_3, bbWeldStiffHR_4,
                           bbWeldStiffLR_1, bbWeldStiffLR_2, bbWeldStiffLR_3, bbWeldStiffLR_4,
                           bbWeldstiff1_u1, bbWeldstiff1_u2, bbWeldstiff2_u1, bbWeldstiff2_u2, bbWeldstiff3_u1,
                           bbWeldstiff3_u2, bbWeldstiff4_u1, bbWeldstiff4_u2,
                           bbWeldstiff1_l1, bbWeldstiff1_l2, bbWeldstiff2_l1, bbWeldstiff2_l2, bbWeldstiff3_l1,
                           bbWeldstiff3_l2, bbWeldstiff4_l1, bbWeldstiff4_l2,
                           beam_stiffener_1, beam_stiffener_2,beam_stiffener_3, beam_stiffener_4,
                           beam_stiffener_F1,beam_stiffener_F2,beam_stiffener_F3,beam_stiffener_F4,alist, outputobj)
         extbothWays.create_3DModel()

         return extbothWays


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
      bolt_head_dia = {5: 40, 6: 40, 8: 40, 10: 40, 12: 40, 16: 50, 20: 50, 22: 50, 24: 50, 27: 60, 30: 65, 36: 75}

      return bolt_head_dia[bolt_diameter]

   def nut_thick_calculation(self, bolt_diameter):
      '''
      Returns the thickness of the nut depending upon the nut diameter as per IS1363-3(2002)
      '''
      nut_dia = {5: 5, 6: 5.65, 8: 7.15, 10: 8.75, 12: 11.3, 16: 15, 20: 17.95, 22: 19.0, 24: 21.25, 27: 23, 30: 25.35, 36: 30.65}
      return nut_dia[bolt_diameter]

   def call_3DModel(self, bgcolor):
      # Call to calculate/create the Extended Both Way CAD model
      status = self.resultObj['Bolt']['status']
      if status is True:
         self.create_extended_both_ways()
         self.ui.btn3D.setChecked(Qt.Checked)
         if self.ui.btn3D.isChecked():
            self.ui.chkBx_beamSec.setChecked(Qt.Unchecked)
            self.ui.chkBx_connector.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

      # Call to display the Extended Both Way CAD model
         self.display_3DModel("Model", bgcolor)
      else:
         self.display.EraseAll()

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
            self.ui.chkBx_beamSec.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
         self.display_3DModel("Connector", bgcolor)

   def display_3DModel(self,component, bgcolor):
      self.component = component

      self.display.EraseAll()
      self.display.View_Iso()
      self.display.FitAll()

      alist = self.designParameters()

      self.display.DisableAntiAliasing()
      if bgcolor == "gradient_bg":

         self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
      else:
         self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

      # ExtObj is an object which gets all the calculated values of CAD models
      self.ExtObj = self.create_extended_both_ways()

      # Displays the beams
      if component == "Beam":
         osdag_display_shape(self.display, self.ExtObj.get_beamLModel(), update=True)
         osdag_display_shape(self.display, self.ExtObj.get_beamRModel(), update=True)

      elif component == "Connector":
         # Displays the end plates
         osdag_display_shape(self.display, self.ExtObj.get_plateLModel(), update=True, color='Blue')
         osdag_display_shape(self.display, self.ExtObj.get_plateRModel(), update=True, color='Blue')\

         #Adding stiffeners along with the weld
         if self.alist["Member"]["Connectivity"] == "Extended both ways" or self.alist["Member"][
            "Connectivity"] == "Extended one way":
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_1Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_3Model(), update=True, color='Blue')

            # Fillet Welds
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_3Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_3Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_3Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_3Model(), update=True, color='Red')

         if self.alist["Member"]["Connectivity"] == "Extended both ways":
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_2Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_4Model(), update=True, color='Blue')

            # Fillet Welds
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_4Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_4Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_4Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_4Model(), update=True, color='Red')

         if self.alist["Member"]["Connectivity"] == "Flush":
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F1Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F2Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F3Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F4Model(), update=True, color='Blue')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_l2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_l2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_l2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_l2Model(), update=True, color='Red')

         # Display all nut-bolts, call to nutBoltPlacement.py
         nutboltlist = self.ExtObj.nut_bolt_array.get_models()
         for nutbolt in nutboltlist:
            osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

         # Display all the Welds including the quarter cone

         if alist["Weld"]["Type"] == "Fillet Weld":
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_11Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_12Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_21Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_22Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_11Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_12Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_13Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_14Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_21Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_22Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_23Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_24Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_11Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_12Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_21Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_22Model(), update=True, color='Red')



         else:      #Groove weld
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_R1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_R2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_L1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_L2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldWeb_R3Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldWeb_L3Model(), update=True, color='Red')

            #TODO: This is the groove weld for the beam stiffenres
            ## osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_1Model(), update=True, color='Red')
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_2Model(), update=True, color='Red')
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_3Model(), update=True, color='Red')
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_4Model(), update=True, color='Red')
            #
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_1Model(), update=True, color='Red')
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_2Model(), update=True, color='Red')
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_3Model(), update=True, color='Red')
            # osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_4Model(), update=True, color='Red')


      elif component == "Model":
         osdag_display_shape(self.display, self.ExtObj.get_beamLModel(), update=True)
         osdag_display_shape(self.display, self.ExtObj.get_beamRModel(), update=True)
         # Displays the end plates
         osdag_display_shape(self.display, self.ExtObj.get_plateLModel(), update=True, color='Blue')
         osdag_display_shape(self.display, self.ExtObj.get_plateRModel(), update=True, color='Blue')

         if self.alist["Member"]["Connectivity"] == "Extended both ways" or self.alist["Member"][
            "Connectivity"] == "Extended one way":
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_1Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_3Model(), update=True, color='Blue')

            #Fillet Welds
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_3Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_3Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_3Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_3Model(), update=True, color='Red')

         if self.alist["Member"]["Connectivity"] == "Extended both ways":
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_2Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_4Model(), update=True, color='Blue')

            #Fillet Welds
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHL_4Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLL_4Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffHR_4Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffLR_4Model(), update=True, color='Red')

         if self.alist["Member"]["Connectivity"] == "Flush":
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F1Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F2Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F3Model(), update=True, color='Blue')
            osdag_display_shape(self.display, self.ExtObj.get_beam_stiffener_F4Model(), update=True, color='Blue')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff1_l2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff2_l2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff3_l2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_u1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_u2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_l1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldstiff4_l2Model(), update=True, color='Red')

         # Display all nut-bolts, call to nutBoltPlacement.py
         nutboltlist = self.ExtObj.nut_bolt_array.get_models()
         for nutbolt in nutboltlist:
            osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)


         # Display all the Welds including the quarter cone
         if alist["Weld"]["Type"] == "Fillet Weld":
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_11Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_12Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_21Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldAbvFlang_22Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_11Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_12Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_13Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_14Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_21Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_22Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_23Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldBelwFlang_24Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_11Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_12Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_21Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_22Model(), update=True, color='Red')


         else:   #Groove weld
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_R1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_R2Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_L1Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldFlang_L2Model(), update=True, color='Red')

            osdag_display_shape(self.display, self.ExtObj.get_bbWeldWeb_R3Model(), update=True, color='Red')
            osdag_display_shape(self.display, self.ExtObj.get_bbWeldWeb_L3Model(), update=True, color='Red')

            #TODO: Thid is the groove weld fot the  beam stiffeners
            ## if self.alist["Member"]["Connectivity"] == "Extended both ways" or self.alist["Member"][
            #  "Connectivity"] == "Extended one way":
            #
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_1Model(), update=True, color='Red')
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_1Model(), update=True, color='Red')
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_3Model(), update=True, color='Red')
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_3Model(), update=True, color='Red')
            #
            # if self.alist["Member"]["Connectivity"] == "Extended both ways":
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_2Model(), update=True, color='Red')
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_2Model(), update=True, color='Red')
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffH_4Model(), update=True, color='Red')
            #  osdag_display_shape(self.display, self.ExtObj.get_bbWeldStiffL_4Model(), update=True, color='Red')


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
	fh = logging.FileHandler("Connections/Moment/ExtendedEndPlate/extnd.log", mode='a')

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


def launch_extendedendplate_controller(osdagMainWindow, folder):
	set_osdaglogger()
	# --------------- To display log messages in different colors ---------------
	rawLogger = logging.getLogger("raw")
	rawLogger.setLevel(logging.INFO)
	# file_handler = logging.FileHandler(os.path.join('Connections','Moment','ExtendedEndPlate','extnd.log'), mode='w')
	file_handler = logging.FileHandler("Connections/Moment/ExtendedEndPlate/extnd.log", mode='w')
	formatter = logging.Formatter('''%(message)s''')
	file_handler.setFormatter(formatter)
	rawLogger.addHandler(file_handler)
	rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Moment/BCEndPlate/log.css"/>''')
	# ----------------------------------------------------------------------------
	module_setup()
	window = Maincontroller(folder)
	osdagMainWindow.hide()
	window.show()
	window.closed.connect(osdagMainWindow.show)


if __name__ == "__main__":
	# --------------- To display log messages in different colors ---------------
	set_osdaglogger()
	rawLogger = logging.getLogger("raw")
	rawLogger.setLevel(logging.INFO)
	# fh = logging.FileHandler(os.path.join('Connections','Moment','ExtendedEndPlate','extnd.log'), mode="w")
	fh = logging.FileHandler("Connections/Moment/ExtendedEndPlate/extnd.log", mode='w')

	formatter = logging.Formatter('''%(message)s''')
	fh.setFormatter(formatter)
	rawLogger.addHandler(fh)
	rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Moment/ExtendedEndPlate/log.css"/>''')
	# ----------------------------------------------------------------------------
	# folder_path = "D:\Osdag_Workspace\extendedendplate"
	app = QApplication(sys.argv)
	module_setup()
	folder_path = ""
	if not os.path.exists(folder_path):
		os.mkdir(folder_path, 0755)
	image_folder_path = os.path.join(folder_path, 'images_html')
	if not os.path.exists(image_folder_path):
		os.mkdir(image_folder_path, 0755)

	window = Maincontroller(folder_path)
	window.show()
	sys.exit(app.exec_())
