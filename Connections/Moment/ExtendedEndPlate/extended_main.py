"""
Created on 24-Aug-2017

@author: Reshma
"""
import json
from ui_extendedendplate import Ui_MainWindow
from ui_design_preferences import Ui_DesignPreference
from ui_plate import Ui_Plate
from ui_stiffener import Ui_Stiffener
# from ui_pitch import Ui_Pitch
from bbExtendedEndPlateSpliceCalc import bbExtendedEndPlateSplice
from drawing_2D import ExtendedEndPlate
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QFontDialog, QFileDialog, QMessageBox
from PyQt5.Qt import QColor, QBrush, Qt, QIntValidator, QDoubleValidator, QFile
from PyQt5 import QtGui, QtCore, QtWidgets, QtOpenGL
from Connections.Component.ISection import ISection
from Connections.Component.plate import Plate
from Connections.Component.bolt import Bolt
from Connections.Component.nut import Nut
from Connections.Component.filletweld import FilletWeld
from model import *
import sys
import os
import pickle
from Connections.Moment.ExtendedEndPlate.bbExtendedEndPlateSpliceCalc import bbExtendedEndPlateSplice
from Connections.Moment.ExtendedEndPlate.extendedBothWays import ExtendedBothWays
from Connections.Moment.ExtendedEndPlate.nutBoltPlacement import NutBoltArray
from Connections.Component.quarterCone import QuarterCone
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from utilities import osdag_display_shape
import copy

class DesignPreference(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_DesignPreference()
        self.ui.setupUi(self)
        self.maincontroller = parent

        self.saved = None
        self.ui.combo_design_method.model().item(1).setEnabled(False)
        self.ui.combo_design_method.model().item(2).setEnabled(False)
        # self.set_default_para()
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_weldFu.setValidator(dbl_validator)
        self.ui.txt_weldFu.setMaxLength(7)
        # self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        # self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

    def save_designPref_para(self):
        uiObj = self.maincontroller.get_user_inputs()
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_type"] = str(self.ui.combo_boltType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
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

        self.saved_designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())
        self.saved_designPref["design"] = {}
        self.saved_designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
        self.saved = True

        QMessageBox.about(self, 'Information', "Preferences saved")

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
        designPref["bolt"]["bolt_type"] = str(self.ui.combo_boltType.currentText())
        designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
        designPref["bolt"]["bolt_fu"] = int(self.ui.txt_boltFu.text())
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
        if boltDia != 'Diameter of Bolt':

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
            boltGrade: HSFG or Bearing Bolt

        Returns: ultimate strength of bolt depending upon grade of bolt chosen

        """
        boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040,
                  12.9: 1220}
        boltGrd = float(boltGrade)
        return boltFu[boltGrd]

    def close_designPref(self):
        self.close()


class plate(QDialog):
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
        self.ui.txt_stiffnrHeight.setText(str(resultObj_plate["Stiffener"]["Height"]))
        self.ui.txt_stiffnrLength.setText(str(resultObj_plate["Stiffener"]["Length"]))
        self.ui.txt_stiffnrThickness.setText(str(resultObj_plate["Stiffener"]["Thickness"]))


class Pitch(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        # self.ui = ui_Pitch()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller.designParameters()
        resultObj_plate = bbExtendedEndPlateSplice(uiObj)
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



class Maincontroller(QMainWindow):
    def __init__(self, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder

        self.get_beamdata()
        # self.resultobj = None

        self.designPrefDialog = DesignPreference(self)
        # self.ui.combo_connLoc.setCurrentIndex(0)
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

        self.gradeType = {'Please select type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)
        self.retrieve_prevstate()

        self.ui.btnFront.clicked.connect(lambda : self.call_2D_drawing("Front"))
        self.ui.btnTop.clicked.connect(lambda : self.call_2D_drawing("Top"))
        self.ui.btnSide.clicked.connect(lambda : self.call_2D_drawing("Side"))
        self.ui.combo_diameter.currentIndexChanged[str].connect(self.bolt_hole_clearance)
        self.ui.combo_grade.currentIndexChanged[str].connect(self.call_bolt_fu)
        self.ui.action_save_input.triggered.connect(self.saveDesign_inputs)
        self.ui.action_load_input.triggered.connect(self.openDesign_inputs)

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        self.ui.btn_Reset.clicked.connect(self.reset_btnclicked)
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.actionDesign_Preferences.triggered.connect(self.design_prefer)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialogue)
        self.ui.btn_pitchDetail.clicked.connect(self.pitch_details)
        self.ui.btn_plateDetail.clicked.connect(self.plate_details)
        self.ui.btn_stiffnrDetail.clicked.connect(self.stiffener_details)

        validator = QIntValidator()
        self.ui.txt_Fu.setValidator(validator)
        self.ui.txt_Fy.setValidator(validator)

        doubl_validator = QDoubleValidator()
        self.ui.txt_Moment.setValidator(doubl_validator)
        self.ui.txt_Shear.setValidator(doubl_validator)
        self.ui.txt_Axial.setValidator(doubl_validator)
        self.ui.txt_plateHeight.setValidator(doubl_validator)
        self.ui.txt_plateWidth.setValidator(doubl_validator)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        min_fu = 290
        max_fu = 590
        self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txt_Fy.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fy, min_fy, max_fy))

        # from osdagMainSettings import backend_name
        # self.display, _ = self.init_display(backend_str=backend_name())
        self.uiObj = None
        self.resultObj = None
        self.designPrefDialog = DesignPreference(self)

    # def init_display(self, backend_str=None, size=(1024, 768)):
    #     from OCC.Display.backend import load_backend, get_qt_modules
    #
    #     used_backend = load_backend(backend_str)
    #
    #     global display, start_display, app, _, USED_BACKEND
    #     if 'qt' in used_backend:
    #         from OCC.Display.qtDisplay import qtViewer3d
    #         QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
    #
    #     from OCC.Display.qtDisplay import qtViewer3d
    #     self.ui.modelTab = qtViewer3d(self)
    #     display = self.ui.modelTab._display
    #
    #     display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
    #     display.View.SetProj(1, 1, 1)

        def centerOnScreen(self):
            resolution = QtGui.QDesktopWidget().screenGeometry()
            self.move((resolution.width()/2) - (self.frameSize().width()/2),
                      (resolution.height()/2) - (self.frameSize().height()/2))

        # def start_display():
        #     self.ui.modelTab.raise_()
        # return display, start_display

    def enableViewButtons(self):
        self.ui.action_save_input.setEnabled(True)

    def disableViewButtons(self):
        self.ui.action_save_input.setEnabled(False)

    def createExtendedBothWays(self):

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

        plate_Left = Plate(L=outputobj["Plate"]["Height"],
                           W=outputobj["Plate"]["Width"],
                           T=outputobj["Plate"]["Thickness"])
        plate_Right = copy.copy(plate_Left)     # Since both the end plates are identical

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

        bbNutBoltArray = NutBoltArray(alist, beam_data, outputobj, nut, bolt, numberOfBolts, nutSpace)

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
        bbWeldBelwFlang_11 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]), h=float(alist["Weld"]["Flange (mm)"]), L=(beam_B - beam_tw) / 2)
        bbWeldBelwFlang_12 = copy.copy(bbWeldBelwFlang_11)
        bbWeldBelwFlang_13 = copy.copy(bbWeldBelwFlang_11)
        bbWeldBelwFlang_14 = copy.copy(bbWeldBelwFlang_11)
        bbWeldBelwFlang_21 = copy.copy(bbWeldBelwFlang_11)
        bbWeldBelwFlang_22 = copy.copy(bbWeldBelwFlang_11)
        bbWeldBelwFlang_23 = copy.copy(bbWeldBelwFlang_11)
        bbWeldBelwFlang_24 = copy.copy(bbWeldBelwFlang_11)

        # Followings welds are welds placed aside beam flange, Qty = 8
        bbWeldSideFlange_11 = FilletWeld(b=float(alist["Weld"]["Flange (mm)"]), h=float(alist["Weld"]["Flange (mm)"]), L=beam_T)
        bbWeldSideFlange_12 = copy.copy(bbWeldSideFlange_11)
        bbWeldSideFlange_13 = copy.copy(bbWeldSideFlange_11)
        bbWeldSideFlange_14 = copy.copy(bbWeldSideFlange_11)
        bbWeldSideFlange_21 = copy.copy(bbWeldSideFlange_11)
        bbWeldSideFlange_22 = copy.copy(bbWeldSideFlange_11)
        bbWeldSideFlange_23 = copy.copy(bbWeldSideFlange_11)
        bbWeldSideFlange_24 = copy.copy(bbWeldSideFlange_11)

        # Followings welds are welds placed aside of beam web, Qty = 4
        bbWeldSideWeb_11 = FilletWeld(b=float(alist["Weld"]["Web (mm)"]), h=float(alist["Weld"]["Web (mm)"]), L=beam_d - 2 * beam_T)
        bbWeldSideWeb_12 = copy.copy(bbWeldSideWeb_11)
        bbWeldSideWeb_21 = copy.copy(bbWeldSideWeb_11)
        bbWeldSideWeb_22 = copy.copy(bbWeldSideWeb_11)

        #######################################
        #       WELD SECTIONS QUARTER CONE    #
        #######################################

        # Following weld cones are placed for Left beam
        weldQtrCone_11 = QuarterCone(b=float(alist["Weld"]["Flange (mm)"]), h=float(alist["Weld"]["Flange (mm)"]), coneAngle=90)
        weldQtrCone_12 = copy.copy(weldQtrCone_11)
        weldQtrCone_13 = copy.copy(weldQtrCone_11)
        weldQtrCone_14 = copy.copy(weldQtrCone_11)
        weldQtrCone_15 = copy.copy(weldQtrCone_11)
        weldQtrCone_16 = copy.copy(weldQtrCone_11)
        weldQtrCone_17 = copy.copy(weldQtrCone_11)
        weldQtrCone_18 = copy.copy(weldQtrCone_11)

        # Following weld cones are placed for Right beam
        weldQtrCone_21 = copy.copy(weldQtrCone_11)
        weldQtrCone_22 = copy.copy(weldQtrCone_11)
        weldQtrCone_23 = copy.copy(weldQtrCone_11)
        weldQtrCone_24 = copy.copy(weldQtrCone_11)
        weldQtrCone_25 = copy.copy(weldQtrCone_11)
        weldQtrCone_26 = copy.copy(weldQtrCone_11)
        weldQtrCone_27 = copy.copy(weldQtrCone_11)
        weldQtrCone_28 = copy.copy(weldQtrCone_11)


        extbothWays = ExtendedBothWays(beam_Left, beam_Right, plate_Left, plate_Right, bbNutBoltArray,
                                       bbWeldAbvFlang_11, bbWeldAbvFlang_12, bbWeldAbvFlang_21, bbWeldAbvFlang_22,
                                       bbWeldBelwFlang_11, bbWeldBelwFlang_12, bbWeldBelwFlang_13, bbWeldBelwFlang_14,
                                       bbWeldBelwFlang_21, bbWeldBelwFlang_22, bbWeldBelwFlang_23, bbWeldBelwFlang_24,
                                       bbWeldSideFlange_11, bbWeldSideFlange_12, bbWeldSideFlange_13, bbWeldSideFlange_14,
                                       bbWeldSideFlange_21, bbWeldSideFlange_22, bbWeldSideFlange_23, bbWeldSideFlange_24,
                                       bbWeldSideWeb_11, bbWeldSideWeb_12, bbWeldSideWeb_21, bbWeldSideWeb_22,
                                       weldQtrCone_11, weldQtrCone_12, weldQtrCone_13, weldQtrCone_14,
                                       weldQtrCone_15, weldQtrCone_16, weldQtrCone_17, weldQtrCone_18,
                                       weldQtrCone_21, weldQtrCone_22, weldQtrCone_23, weldQtrCone_24,
                                       weldQtrCone_25, weldQtrCone_26, weldQtrCone_27, weldQtrCone_28)
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
        uiObj["Weld"]["Flange (mm)"] = str(self.ui.combo_flangeSize.currentText())
        uiObj["Weld"]["Web (mm)"] = str(self.ui.combo_webSize.currentText())
        return uiObj

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
        uiInput = self.get_user_inputs()
        self.save_inputs_totext(uiInput)
        action = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if action == QMessageBox.Yes:
            # self.close.emit()
            self.close()
            event.accept()
        else:
            event.ignore()

    def save_inputs_totext(self, uiObj):
        """

        Args:
            uiObj: User inputs

        Returns: Save the user input to txt format

        """
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
            self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(str(uiObj["Member"]["Connectivity"])))
            if uiObj["Member"]["Connectivity"] == "Flush" or "Extended one way" or "Extended both ways":
                self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(uiObj["Member"]["Connectivity"]))
                self.ui.combo_beamSec.setCurrentIndex(self.ui.combo_beamSec.findText(uiObj["Member"]["BeamSection"]))
                self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
                self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
                self.ui.txt_Shear.setText(str(uiObj["Load"]["ShearForce (kN)"]))
                self.ui.txt_Axial.setText(str(uiObj['Load']['AxialForce (kN)']))
                self.ui.txt_Moment.setText(str(uiObj["Load"]["Moment (kNm)"]))
                self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
                self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
                self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
                self.ui.combo_plateThick.setCurrentIndex(self.ui.combo_plateThick.findText(uiObj["Plate"]["Thickness (mm)"]))
                self.ui.txt_plateHeight.setText(str(uiObj["Plate"]["Height (mm)"]))
                self.ui.txt_plateWidth.setText(str(uiObj["Plate"]["Width (mm)"]))
                self.ui.combo_flangeSize.setCurrentIndex(self.ui.combo_flangeSize.findText(uiObj["Weld"]["Flange (mm)"]))
                self.ui.combo_webSize.setCurrentIndex(self.ui.combo_webSize.findText(uiObj["Weld"]["Web (mm)"]))

        else:
            pass

    def designParameters(self):
        """

        Returns:

        """

        self.uiObj = self.get_user_inputs()
        if self.designPrefDialog.saved is not True:
            design_pref = self.designPrefDialog.save_default_para()
        else:
            design_pref = self.designPrefDialog.saved_designPref
        self.uiObj.update(design_pref)
        return self.uiObj

    def design_btnclicked(self):
        """

        Returns:

        """
        # self.uiObj = self.get_user_inputs()
        # print self.uiObj
        self.display.EraseAll()
        self.alist = self.designParameters()
        self.outputs = bbExtendedEndPlateSplice(self.alist)
        print "output list ", self.outputs
        self.ui.outputDock.setFixedSize(310, 710)
        a = self.outputs[self.outputs.keys()[0]]
        self.display_output(self.outputs)
        self.display_log_to_textedit()
        self.call_3DModel()

    def call_3DModel(self):
        self.createExtendedBothWays()   # Call to calculate/create the Extended Both Way CAD model
        self.display_3DModel("Model", "gradient_bg")     # Call to display the Extended Both Way CAD model

    def display_3DModel(self,component, bgcolor):
        self.component = component

        self.display.EraseAll()
        self.display.View_Iso()
        self.display.FitAll()

        self.display.DisableAntiAliasing()
        if bgcolor == "gradient_bg":

            self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
        else:
            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)

        self.ExtObj = self.createExtendedBothWays()     # ExtObj is an object which gets all the calculated values of CAD models

        # Displays the beams
        osdag_display_shape(self.display, self.ExtObj.get_beamLModel(), update=True)
        osdag_display_shape(self.display, self.ExtObj.get_beamRModel(), update=True)

        # Displays the end plates
        osdag_display_shape(self.display, self.ExtObj.get_plateLModel(), update=True, color='Blue')
        osdag_display_shape(self.display, self.ExtObj.get_plateRModel(), update=True, color='Blue')

        # Display all nut-bolts, call to nutBoltPlacement.py
        nutboltlist = self.ExtObj.nut_bolt_array.get_models()
        for nutbolt in nutboltlist:
            osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)

        # Display all the Welds including the quarter cone
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

        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_11Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_12Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_13Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_14Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_21Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_22Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_23Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideFlange_24Model(), update=True, color='Red')

        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_11Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_12Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_21Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldSideWeb_22Model(), update=True, color='Red')

        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_11Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_12Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_13Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_14Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_15Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_16Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_17Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_18Model(), update=True, color='Red')

        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_21Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_22Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_23Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_24Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_25Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_26Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_27Model(), update=True, color='Red')
        osdag_display_shape(self.display, self.ExtObj.get_bbWeldQtrCone_28Model(), update=True, color='Red')

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

        weld_stress_flange = resultObj["Weld"]["CriticalStressflange"]
        self.ui.txt_criticalFlange.setText(str(weld_stress_flange))

        weld_stress_web = resultObj["Weld"]["CriticalStressWeb"]
        self.ui.txt_criticalWeb.setText(str(weld_stress_web))

    def display_log_to_textedit(self):
        file = QFile('extnd.log')
        if not file.open(QtCore.QIODevice.ReadOnly):
            QMessageBox.information(None, 'info', file.errorString())
        stream = QtCore.QTextStream(file)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscroll_bar = self.ui.textEdit.verticalScrollBar()
        vscroll_bar.setValue(vscroll_bar.maximum())
        file.close()

    def reset_btnclicked(self):
        """

        Returns:

        """
        self.ui.combo_beamSec.setCurrentIndex(0)
        self.ui.combo_connLoc.setCurrentIndex(0)
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

    def combotype_current_index_changed(self, index):
        """

        Args:
            index: Number

        Returns: Types of Grade

        """
        items = self.gradeType[str(index)]
        if items != 0 :
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

    def call_2D_drawing(self, view):
        """

        Args:
            view: Front, Side & Top view of 2D svg drawings

        Returns: SVG image created through svgwrite package which takes design INPUT and OUTPUT
                 parameters from Extended endplate GUI

        """
        # self.resultobj = self.designParameters()
        self.alist = self.designParameters()
        self.resultobj = bbExtendedEndPlateSplice(self.alist)
        self.beam_data = self.fetchBeamPara()
        beam_beam = ExtendedEndPlate(self.alist, self.resultobj, self.beam_data)
        if view != "All":
            if view == "Front":
                filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\ExtendedEndPlate\Front.svg"
                beam_beam.save_to_svg(filename, view)
            elif view == "Side":
                filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\ExtendedEndPlate\Side.svg"
                beam_beam.save_to_svg(filename, view)
            else:
                filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\ExtendedEndPlate\Top.svg"
                beam_beam.save_to_svg(filename, view)

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
        section = Plate(self)
        section.show()

    def stiffener_details(self):
        section = Stiffener(self)
        section.show()

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
        self.set_dict_touser_inputs(uiObj)

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
        QMessageBox.about(self, 'Information', "Input file saved")

        # yaml.dump(self.uiObj,out_file,allow_unicode=True, default_flow_style=False)
        json.dump(self.uiObj, out_file)

        out_file.close()

        pass

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

        # self.setWindowTitle("Osdag Finplate")
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

def set_osdaglogger():
    global logger
    if logger is None:

        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # create the logging file handler
    fh = logging.FileHandler("extnd.log", mode="a")

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


def main():
    set_osdaglogger()
    # --------------- To display log messages in different colors ---------------
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("extnd.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')
    # ----------------------------------------------------------------------------

    app = QApplication(sys.argv)
    module_setup()
    window = Maincontroller(folder="F:\Osdag\Connections\Moment\Moment Workspace")  # TODO Path to my Osdag workspace
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
