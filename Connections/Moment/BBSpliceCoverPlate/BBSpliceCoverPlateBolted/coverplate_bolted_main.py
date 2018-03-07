"""
Created on 7-November-2017

@author: Reshma Konjari
"""

from ui_coverplatebolted import Ui_MainWindow
from ui_flangespliceplate import Ui_Flangespliceplate
from ui_webspliceplate import Ui_Webspliceplate
from svg_window import SvgWindow
from cover_plate_bolted_calc import coverplateboltedconnection
from drawing_2D import CoverEndPlate
from ui_design_preferences import Ui_DesignPreference
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFontDialog
from PyQt5.Qt import QIntValidator, QDoubleValidator, QFile, Qt, QBrush, QColor
from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from model import *

from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.BBCoverPlateBoltedCAD import BBCoverPlateBoltedCAD
from Connections.Component.ISection import ISection
from Connections.Component.plate import Plate
from Connections.Component.nut import Nut
from Connections.Component.bolt import Bolt
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.nutBoltPlacement_AF import NutBoltArray_AF
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.nutBoltPlacement_BF import NutBoltArray_BF
from Connections.Moment.BBSpliceCoverPlate.BBSpliceCoverPlateBolted.nutBoltPlacement_Web import NutBoltArray_Web
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from utilities import osdag_display_shape
import copy

import sys
import os.path
import pickle

class DesignPreferences(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_DesignPreference()
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
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

    def save_designPref_para(self):
        uiObj = self.maincontroller.get_user_inputs()
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        # self.saved_designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
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

            self.saved_designPref["detailing"]["gap"] = float(5)
        else:
            self.saved_designPref["detailing"]["gap"] = float(self.ui.txt_detailingGap.text())

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
        designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
        designPref["bolt"]["bolt_fu"] = int(self.ui.txt_boltFu.text())
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
            boltGrade: HSFG or Bearing Bolt

        Returns: ultimate strength of bolt depending upon grade of bolt chosen

        """
        boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040,
                  12.9: 1220}
        boltGrd = float(boltGrade)
        return boltFu[boltGrd]

    def close_designPref(self):
        self.close()


class Flangespliceplate(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Flangespliceplate()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller.designParameters()
        resultObj_flangeplate = coverplateboltedconnection(uiObj)
        print "flange ", resultObj_flangeplate

        self.ui.txt_plateHeight.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateHeight"]))
        self.ui.txt_plateWidth.setText(str(resultObj_flangeplate["FlangeBolt"]["FlangePlateWidth"]))
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

class MainController(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.get_beamdata()
          # self.ui.combo_connLoc.setCurrentIndex(0)
        # self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
        # self.ui.combo_beamSec.setCurrentIndex(0)
        self.gradeType = {'Please select type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)
        self.retrieve_prevstate()

        self.ui.btnFront.clicked.connect(lambda: self.call_2D_drawing("Front"))
        self.ui.btnTop.clicked.connect(lambda: self.call_2D_drawing("Top"))
        self.ui.btnSide.clicked.connect(lambda: self.call_2D_drawing("Side"))
        self.ui.combo_diameter.currentIndexChanged[str].connect(self.bolt_hole_clearance)
        self.ui.combo_grade.currentIndexChanged[str].connect(self.call_bolt_fu)

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.actionDesign_Preferences.triggered.connect(self.design_prefer)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialogue)
        self.ui.btn_flangePlate.clicked.connect(self.flangesplice_plate)
        self.ui.btn_webPlate.clicked.connect(self.websplice_plate)

        validator = QIntValidator()
        self.ui.txt_Fu.setValidator(validator)
        self.ui.txt_Fy.setValidator(validator)

        doubl_validator = QDoubleValidator()
        self.ui.txt_Moment.setValidator(doubl_validator)
        self.ui.txt_Shear.setValidator(doubl_validator)
        self.ui.txt_Axial.setValidator(doubl_validator)
        self.ui.txt_flangeplateHeight.setValidator(doubl_validator)
        self.ui.txt_flangeplateWidth.setValidator(doubl_validator)
        self.ui.txt_webplateHeight.setValidator(doubl_validator)
        self.ui.txt_webplateWidth.setValidator(doubl_validator)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        min_fu = 290
        max_fu = 590
        self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txt_Fy.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fy, min_fy, max_fy))

        self.uiObj = None
        self.resultObj = None
        self.designPrefDialog = DesignPreferences(self)

        def centerOnScreen(self):
            resolution = QtGui.QDesktopWidget().screenGeometry()
            self.move((resolution.width()/2) - (self.frameSize().width()/2),
                      (resolution.height()/2) - (self.frameSize().height()/2))

        # def start_display():
        #     self.ui.modelTab.raise_()
        # return display, start_display

    def showColorDialog(self):

        col = QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

    def createBBCoverPlateBoltedCAD(self):
        '''
        :return: The calculated values/parameters to create 3D CAD model of individual components.   
        '''

        beam_data = self.fetchBeamPara()        # Fetches the beam dimensions

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
                             length=beam_length, notchObj=None)         # Call to ISection in Component repository
        beam_Right = copy.copy(beam_Left)  # Since both the beams are same
        outputobj = self.outputs  # Output dictionary from calculation file
        alist = self.designParameters()  # An object to save all input values entered by user

        plateAbvFlange = Plate(L=outputobj["FlangeBolt"]["FlangePlateWidth"],
                           W=outputobj["FlangeBolt"]["FlangePlateHeight"],
                           T=float(alist["FlangePlate"]["Thickness (mm)"]))     # Call to Plate in Component repository
        plateBelwFlange = copy.copy(plateAbvFlange)  # Since both the flange plates are identical

        WebPlateLeft = Plate(L=outputobj["WebBolt"]["WebPlateHeight"],
                             W=outputobj["WebBolt"]["WebPlateWidth"],
                             T=float(alist["WebPlate"]["Thickness (mm)"]))      # Call to Plate in Component repository
        WebPlateRight = copy.copy(WebPlateLeft)  # Since both the Web plates are identical

        bolt_d = float(alist["Bolt"]["Diameter (mm)"])  # Bolt diameter (shank part), entered by user
        bolt_r = bolt_d / 2     # Bolt radius (Shank part)
        bolt_T = self.bolt_head_thick_calculation(bolt_d)   # Bolt head thickness
        bolt_R = self.bolt_head_dia_calculation(bolt_d) / 2     # Bolt head diameter (Hexagon)
        bolt_Ht = self.bolt_length_calculation(bolt_d)          # Bolt head height

        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)  # Call to create Bolt from Component directory
        nut_T = self.nut_thick_calculation(bolt_d)      # Nut thickness, usually nut thickness = nut height
        nut_Ht = nut_T
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)  # Call to create Nut from Component directory

        numOfBoltsF = 2 * int(outputobj["FlangeBolt"]["BoltsRequiredF"])    # Number of flange bolts for both beams
        nutSpaceF = float(alist["FlangePlate"]["Thickness (mm)"]) + beam_T  # Space between bolt head and nut for flange bolts

        numOfBoltsW = 2 * int(outputobj["WebBolt"]["BoltsRequired"])        # Number of web bolts for both beams
        nutSpaceW = 2 * float(alist["WebPlate"]["Thickness (mm)"]) + beam_tw    # Space between bolt head and nut for web bolts

        # Bolt placement for Above Flange bolts, call to nutBoltPlacement_AF.py
        bolting_AF = NutBoltArray_AF(alist, beam_data, outputobj, nut, bolt, numOfBoltsF, nutSpaceF)

        # Bolt placement for Below Flange bolts, call to nutBoltPlacement_BF.py
        bolting_BF = NutBoltArray_BF(alist, beam_data, outputobj, nut, bolt, numOfBoltsF, nutSpaceF)

        # Bolt placement for Web Plate bolts, call to nutBoltPlacement_Web.py
        bolting_Web = NutBoltArray_Web(alist, beam_data, outputobj, nut, bolt, numOfBoltsW, nutSpaceW)

        # bbCoverPlateBolted is an object which is passed BBCoverPlateBoltedCAD.py file, which initialized the parameters of each CAD component
        bbCoverPlateBolted = BBCoverPlateBoltedCAD(beam_Left, beam_Right, plateAbvFlange, plateBelwFlange,
                                                   WebPlateLeft, WebPlateRight, bolting_AF, bolting_BF, bolting_Web)

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
        return  dictbeamdata

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
        if (text_str < min_val or text_str > max_val or text_str == ' '):
            QMessageBox.about(self, "Error", "Please enter a value between %s-%s"%(min_val, max_val))
            widget.clear()
            widget.setFocus()

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
        uiObj["FlangePlate"]["Thickness (mm)"] = self.ui.combo_flangeplateThick.currentText()
        uiObj["FlangePlate"]["Height (mm)"] = self.ui.txt_flangeplateHeight.text()
        uiObj["FlangePlate"]["Width (mm)"] = self.ui.txt_flangeplateWidth.text()

        uiObj["WebPlate"] = {}
        uiObj["WebPlate"]["Thickness (mm)"] = self.ui.combo_webplateThick.currentText()
        uiObj["WebPlate"]["Height (mm)"] = self.ui.txt_webplateHeight.text()
        uiObj["WebPlate"]["Width (mm)"] = self.ui.txt_webplateWidth.text()
        return uiObj


    def reset_btnclicked(self):
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
        self.ui.combo_flangeplateThick.setCurrentIndex(0)
        self.ui.txt_flangeplateHeight.clear()
        self.ui.txt_flangeplateWidth.clear()
        self.ui.combo_webplateThick.setCurrentIndex(0)
        self.ui.txt_webplateWidth.clear()
        self.ui.txt_webplateHeight.clear()


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
            if uiObj["Member"]["Connectivity"] == "Beam-Beam" or "Select Connectivity":
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
                self.ui.combo_flangeplateThick.setCurrentIndex(self.ui.combo_flangeplateThick.findText(uiObj["FlangePlate"]["Thickness (mm)"]))
                self.ui.combo_webplateThick.setCurrentIndex(self.ui.combo_webplateThick.findText(uiObj["WebPlate"]["Thickness (mm)"]))
                self.ui.txt_flangeplateHeight.setText(str(uiObj["FlangePlate"]["Height (mm)"]))
                self.ui.txt_flangeplateWidth.setText(str(uiObj["FlangePlate"]["Width (mm)"]))
                self.ui.txt_webplateHeight.setText(str(uiObj["WebPlate"]["Height (mm)"]))
                self.ui.txt_webplateWidth.setText(str(uiObj["WebPlate"]["Width (mm)"]))

        else:
            pass

    def design_prefer(self):
        self.designPrefDialog.show()

    def bolt_hole_clearance(self):
        self.designPrefDialog.get_clearance()

    def call_bolt_fu(self):
        self.designPrefDialog.set_boltFu()

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
        self.alist = self.designParameters()
        print "alist printing", self.alist
        self.outputs = coverplateboltedconnection(self.alist)
        a = self.outputs[self.outputs.keys()[0]]
        # if len(str(a[a.keys()[0]])) == 0:
        #     self.ui.btn_Design.setEnabled(False)
        self.display_output(self.outputs)
        self.display_log_to_textedit()
        self.call_3DModel()

    def call_3DModel(self):
        # self.createBBCoverPlateBoltedCAD()  # Call to calculate/create the BB Cover Plate Bolted CAD model
        self.display_3DModel("Model", "gradient_bg")  # Call to display the BB Cover Plate Bolted CAD model

    def display_3DModel(self, component, bgcolor):
        self.component = component

        self.display.EraseAll()
        self.display.View_Iso()
        self.display.FitAll()

        self.display.DisableAntiAliasing()
        if bgcolor == "gradient_bg":

            self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)  # Changes the background color in graphics window iff the design is safe
        else:
            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)    # Sets the color of graphics window to dark (black)

        self.CPBoltedObj = self.createBBCoverPlateBoltedCAD()   # CPBoltedObj is an object which gets all the calculated values of CAD models

        # Displays both beams
        osdag_display_shape(self.display, self.CPBoltedObj.get_beamLModel(), update=True)
        osdag_display_shape(self.display, self.CPBoltedObj.get_beamRModel(), update=True)

        # Displays the Flange Plates
        osdag_display_shape(self.display, self.CPBoltedObj.get_plateAbvFlangeModel(), update=True, color='Blue')
        osdag_display_shape(self.display, self.CPBoltedObj.get_plateBelwFlangeModel(), update=True, color='Blue')

        # Displays the Web Plates
        osdag_display_shape(self.display, self.CPBoltedObj.get_WebPlateLeftModel(), update=True, color='Blue')
        osdag_display_shape(self.display, self.CPBoltedObj.get_WebPlateRightModel(), update=True, color='Blue')

        # Displays the bolts which are above the Flange Plate, debugging will give more clarity
        nutboltlistAF = self.CPBoltedObj.nut_bolt_array_AF.get_modelsAF()
        for nutboltAF in nutboltlistAF:
            osdag_display_shape(self.display, nutboltAF, update=True, color=Quantity_NOC_SADDLEBROWN)

        # Displays the bolts which are below the Flange Plate, debugging will give more clarity
        nutboltlistBF = self.CPBoltedObj.nut_bolt_array_BF.get_modelsBF()
        for nutboltBF in nutboltlistBF:
            osdag_display_shape(self.display, nutboltBF, update=True, color=Quantity_NOC_SADDLEBROWN)

        # Displays the bolts which are on the right side of web plate, debugging will give more clarity
        nutboltlistW = self.CPBoltedObj.nut_bolt_array_Web.get_modelsW()
        for nutboltW in nutboltlistW:
            osdag_display_shape(self.display, nutboltW, update=True, color=Quantity_NOC_SADDLEBROWN)

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

        flange_bearing_capacity =resultObj["FlangeBolt"]["BearingCapacityF"]
        self.ui.txt_bearCapacity.setText(str(flange_bearing_capacity))

        flange_capacity_bolt = resultObj["FlangeBolt"]["CapacityBoltF"]
        self.ui.txt_capacityOfbolt.setText(str(flange_capacity_bolt))

        flange_bolt_req = resultObj["FlangeBolt"]["BoltsRequiredF"]
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

        web_bearing_capacity =resultObj["WebBolt"]["BearingCapacity"]
        self.ui.txt_bearCapacity_2.setText(str(web_bearing_capacity))

        web_capacity_bolt = resultObj["WebBolt"]["CapacityBolt"]
        self.ui.txt_capacityOfbolt_2.setText(str(web_capacity_bolt))

        web_bolt_req = resultObj["WebBolt"]["BoltsRequired"]
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
        file = QFile('coverplate.log')
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
        self.resultObj = self.call_calculation()
        beam_beam = CoverEndPlate(self.resultObj)
        if view != 'All':
            if view == "Front":
                filename = "F:\drawing\Front.svg"
                beam_beam.save_to_svg(filename, view)
            elif view == "Side":
                filename = "F:\drawing\Side.svg"
                beam_beam.save_to_svg(filename, view)
            else:
                filename = "F:\drawing\Top.svg"
                beam_beam.save_to_svg(filename, view)

    def flangesplice_plate(self):
        section = Flangespliceplate(self)
        section.show()

    def websplice_plate(self):
        section = Webspliceplate(self)
        section.show()

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


def set_osdaglogger():
    global logger
    if logger is None:

        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # create the logging file handler
    fh = logging.FileHandler("coverplate.log", mode="a")

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
    fh = logging.FileHandler("coverplate.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')
    # ----------------------------------------------------------------------------
    app = QApplication(sys.argv)
    module_setup()
    window = MainController()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
