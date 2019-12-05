# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/gui/ui_template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import QMessageBox, qApp
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
from .ui_design_preferences import Ui_Dialog
import os
import json
import logging
from drawing_2D.Svg_Window import SvgWindow
import sys

from OCC.Core import BRepTools
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core import IGESControl
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.StlAPI import StlAPI_Writer

import pdfkit
import subprocess
import os.path
import pickle
import shutil
import cairosvg
import configparser

class DesignPreferences(QDialog):
    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.main_controller = parent
        #self.uiobj = self.main_controller.uiObj
        self.saved = None
        self.ui.combo_design_method.model().item(1).setEnabled(False)
        self.ui.combo_design_method.model().item(2).setEnabled(False)
        # self.set_default_para()
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_weldFu.setValidator(dbl_validator)
        self.ui.txt_weldFu.setMaxLength(7)
        self.ui.txt_detailingGap.setValidator(dbl_validator)
        self.ui.txt_detailingGap.setMaxLength(5)
        # self.ui.btn_defaults.clicked.connect(self.set_default_para)
        # self.ui.btn_save.clicked.connect(self.save_designPref_para)
        # self.ui.btn_close.clicked.connect(self.close_designPref)
        # self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

class MainController(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, main, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_ModuleWindow()
        self.ui.setupUi(self,main)
        self.folder = folder
        self.connection = "Finplate"

        # self.get_columndata()
        # self.get_beamdata()

        self.designPrefDialog = DesignPreferences(self)
        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Please Select Type': '', 'Friction Grip Bolt': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()

        # self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convertColComboToBeam)
        # self.retrieve_prevstate()

        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        # self.ui.btn_2D.clicked.connect(self.call2D_Drawing)
        #self.ui.btn3D.clicked.connect(self.call_3DModel)
        self.ui.btn3D.clicked.connect(lambda:self.call_3DModel("gradient_bg"))
        self.ui.chkBxBeam.clicked.connect(lambda: self.call_3DBeam("gradient_bg"))
        self.ui.chkBxCol.clicked.connect(lambda:self.call_3DColumn("gradient_bg"))
        self.ui.chkBxFinplate.clicked.connect(lambda:self.call_3DFinplate("gradient_bg"))

        # validator = QIntValidator()
        # self.ui.txtFu.setValidator(validator)
        # self.ui.txtFy.setValidator(validator)

        dbl_validator = QDoubleValidator()
        self.ui.txtFu.setValidator(dbl_validator)
        self.ui.txtFu.setMaxLength(6)
        self.ui.txtFy.setValidator(dbl_validator)
        self.ui.txtFy.setMaxLength(6)

        self.ui.txtPlateLen.setValidator(dbl_validator)
        self.ui.txtPlateLen.setMaxLength(7)
        self.ui.txtPlateWidth.setValidator(dbl_validator)
        self.ui.txtPlateWidth.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)

        min_fu = 290
        max_fu = 780
        self.ui.txtFu.editingFinished.connect(
            lambda: self.check_range(self.ui.txtFu, self.ui.lbl_fu, min_fu, max_fu))
        self.ui.txtFu.editingFinished.connect(
            lambda: self.validate_fu_fy(self.ui.txtFu, self.ui.txtFy, self.ui.txtFu, self.ui.lbl_fu))

        min_fy = 165
        max_fy = 650
        self.ui.txtFy.editingFinished.connect(
            lambda: self.check_range(self.ui.txtFy, self.ui.lbl_fy, min_fy, max_fy))
        self.ui.txtFy.editingFinished.connect(
            lambda: self.validate_fu_fy(self.ui.txtFu, self.ui.txtFy, self.ui.txtFy, self.ui.lbl_fy))

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
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
        self.ui.actionSave_3D_model.triggered.connect(self.save3DcadImages)
        self.ui.actionSave_current_image.triggered.connect(self.save_cadImages)
        self.ui.actionPan.triggered.connect(self.call_Pannig)
        self.ui.action_save_input.triggered.connect(self.saveDesign_inputs)
        self.ui.action_load_input.triggered.connect(self.openDesign_inputs)
        # graphics
        self.ui.actionShow_beam.triggered.connect(lambda:self.call_3DBeam("gradient_bg"))
        self.ui.actionShow_column.triggered.connect(lambda:self.call_3DColumn("gradient_bg"))
        self.ui.actionShow_finplate.triggered.connect(lambda:self.call_3DFinplate("gradient_bg"))
        self.ui.actionShow_all.triggered.connect(lambda:self.call_3DModel("gradient_bg"))
        self.ui.actionChange_background.triggered.connect(self.showColorDialog)
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        self.ui.combo_Beam.currentIndexChanged[int].connect(self.fillPlateThickCombo)


        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkBeam_B)
        self.ui.combo_Beam.currentIndexChanged[int].connect(self.checkBeam_B)
        self.ui.comboPlateThick_2.currentIndexChanged[int].connect(self.populateWeldThickCombo)
        self.ui.comboDiameter.currentIndexChanged[str].connect(self.bolt_hole_clearace)
        self.ui.comboGrade.currentIndexChanged[str].connect(self.call_boltFu)
        self.ui.txtFu.textChanged.connect(self.call_weld_fu)

        self.ui.txtPlateLen.editingFinished.connect(lambda: self.check_plate_height(self.ui.txtPlateLen, self.ui.lbl_len_2))
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.createDesignReport)  # Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)


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
        self.ui.actionDesign_examples.triggered.connect(self.design_examples)
        self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_question)
        self.ui.actionDesign_Preferences.triggered.connect(self.design_preferences)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        self.resultObj = None
        self.uiObj = None

    # def get_columndata(self):
    #     """Fetch  old and new column sections from "Intg_osdag" database.
    #     Returns:
    #
    #     """
    #     columndata = get_columncombolist()
    #     old_colList = get_oldcolumncombolist()
    #     self.ui.comboColSec.addItems(columndata)
    #     self.color_oldDB_sections(old_colList, columndata, self.ui.comboColSec)
    #
    # def get_beamdata(self):
    #     """Fetch old and new beam sections from "Intg_osdag" database
    #
    #     Returns:
    #
    #     """
    #
    #     loc = self.ui.comboConnLoc.currentText()
    #     beamdata = get_beamcombolist()
    #     old_beamList = get_oldbeamcombolist()
    #     combo_section = ''
    #     if loc == "Beam-Beam":
    #         self.ui.comboColSec.addItems(beamdata)
    #         combo_section = self.ui.comboColSec
    #     else:
    #         self.ui.combo_Beam.addItems(beamdata)
    #         combo_section = self.ui.combo_Beam
    #
    #     self.color_oldDB_sections(old_beamList, beamdata,combo_section )
    #
    # def color_oldDB_sections(self, old_section, intg_section, combo_section):
    #     """display old sections in red color.
    #
    #     Args:
    #         old_section(str): Old sections from IS 808 1984
    #         intg_section(str): Revised sections from IS 808 2007
    #         combo_section(QcomboBox): Beam/Column dropdown list
    #
    #     Returns:
    #
    #     """
    #     for col in old_section:
    #         if col in intg_section:
    #             indx = intg_section.index(str(col))
    #             combo_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
    #
    #     duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]
    #     for i in duplicate:
    #         combo_section.setItemData(i, QBrush(QColor("red")), Qt.TextColorRole)
    #
    #
    # def osdag_header(self):
    #     image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
    #     shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))
    #
    # def fetchBeamPara(self):
    #     beam_sec = self.ui.combo_Beam.currentText()
    #     dictbeamdata = get_beamdata(beam_sec)
    #     return dictbeamdata
    #
    # def fetchColumnPara(self):
    #     """Return  sectional properties of selected column section
    #     Returns:
    #         dictcoldata(dict): Sectional properties of column
    #
    #     """
    #     column_sec = str(self.ui.comboColSec.currentText())
    #     if column_sec == 'Select section':
    #         return
    #     loc = self.ui.comboConnLoc.currentText()
    #     if loc == "Beam-Beam":
    #         dictcoldata = get_beamdata(column_sec)
    #     else:
    #         dictcoldata = get_columndata(column_sec)
    #     return dictcoldata
    #
    # def convertColComboToBeam(self):
    #     """Replace colulmn cobobox to Primary beam sections and change text of column section(label) to primary beam.
    #     Returns:
    #
    #     """
    #
    #     self.display.EraseAll()
    #     self.designPrefDialog.set_default_para()
    #     loc = self.ui.comboConnLoc.currentText()
    #     if loc == "Beam-Beam":
    #         self.ui.lbl_beam.setText("Secondary beam *")
    #         self.ui.lbl_column.setText("Primary beam *")
    #
    #         self.ui.chkBxBeam.setText("SBeam")
    #         self.ui.chkBxBeam.setToolTip("Secondary beam")
    #         self.ui.chkBxCol.setText("PBeam")
    #         self.ui.chkBxCol.setToolTip("Primary beam")
    #         self.ui.actionShow_beam.setText("Show SBeam")
    #         self.ui.actionShow_column.setText("Show PBeam")
    #         self.ui.comboColSec.blockSignals(True)
    #         self.ui.comboColSec.clear()
    #         self.get_beamdata()
    #         self.ui.combo_Beam.setCurrentIndex(0)
    #
    #         self.ui.txtFu.clear()
    #         self.ui.txtFy.clear()
    #         self.ui.txtShear.clear()
    #
    #         self.ui.comboDiameter.blockSignals(True)
    #         self.ui.comboDiameter.setCurrentIndex(0)
    #         self.ui.comboType.setCurrentIndex((0))
    #         self.ui.comboGrade.blockSignals(True)
    #         self.ui.comboGrade.setCurrentIndex((0))
    #         self.ui.comboPlateThick_2.setItemText(0, "Select plate thickness")
    #         self.ui.comboPlateThick_2.setCurrentIndex((0))
    #         self.ui.txtPlateLen.clear()
    #         self.ui.txtPlateWidth.clear()
    #         self.ui.comboWldSize.setItemText(0, "Select weld thickness")
    #         self.ui.comboWldSize.setCurrentIndex((0))
    #
    #         self.ui.txtShrCapacity.clear()
    #         self.ui.txtbearCapacity.clear()
    #         self.ui.txtBoltCapacity.clear()
    #         self.ui.txtNoBolts.clear()
    #         self.ui.txtboltgrpcapacity.clear()
    #         self.ui.txt_row.clear()
    #         self.ui.txt_col.clear()
    #         self.ui.txtPitch.clear()
    #         self.ui.txtGuage.clear()
    #         self.ui.txtEndDist.clear()
    #         self.ui.txtEdgeDist.clear()
    #         self.ui.txtplate_ht.clear()
    #         self.ui.txtplate_width.clear()
    #         self.ui.txtExtMomnt.clear()
    #         self.ui.txtMomntCapacity.clear()
    #         self.ui.txtResltShr.clear()
    #         self.ui.txtWeldStrng.clear()
    #         self.display.EraseAll()
    #         self.disableViewButtons()
    #
    #     elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":
    #
    #         self.ui.lbl_column.setText("Column Section *")
    #         self.ui.lbl_beam.setText("Beam section *")
    #         self.ui.chkBxBeam.setText("Beam")
    #         self.ui.actionShow_beam.setText("Show beam")
    #         self.ui.chkBxBeam.setToolTip("Beam only")
    #         self.ui.chkBxCol.setText("Column")
    #         self.ui.actionShow_column.setText("Show column")
    #         self.ui.chkBxCol.setToolTip("Column only")
    #         self.ui.comboColSec.clear()
    #         self.get_columndata()
    #         self.ui.comboColSec.setCurrentIndex(0)
    #         self.ui.combo_Beam.setCurrentIndex(0)
    #
    #         self.ui.txtFu.clear()
    #         self.ui.txtFy.clear()
    #         self.ui.txtShear.clear()
    #
    #         self.ui.comboDiameter.setCurrentIndex(0)
    #         self.ui.comboType.setCurrentIndex((0))
    #         self.ui.comboGrade.setCurrentIndex((0))
    #         self.ui.comboPlateThick_2.setItemText(0, "Select plate thickness")
    #         self.ui.comboPlateThick_2.setCurrentIndex((0))
    #         self.ui.txtPlateLen.clear()
    #         self.ui.txtPlateWidth.clear()
    #         self.ui.comboWldSize.setItemText(0, "Select weld thickness")
    #         self.ui.comboWldSize.setCurrentIndex((0))
    #
    #         self.ui.txtShrCapacity.clear()
    #         self.ui.txtbearCapacity.clear()
    #         self.ui.txtBoltCapacity.clear()
    #         self.ui.txtNoBolts.clear()
    #         self.ui.txtboltgrpcapacity.clear()
    #         self.ui.txt_row.clear()
    #         self.ui.txt_col.clear()
    #         self.ui.txtPitch.clear()
    #         self.ui.txtGuage.clear()
    #         self.ui.txtEndDist.clear()
    #         self.ui.txtEdgeDist.clear()
    #         self.ui.txtplate_ht.clear()
    #         self.ui.txtplate_width.clear()
    #         self.ui.txtExtMomnt.clear()
    #         self.ui.txtMomntCapacity.clear()
    #         self.ui.txtResltShr.clear()
    #         self.ui.txtWeldStrng.clear()
    #         self.display.EraseAll()
    #         self.disableViewButtons()

    def showFontDialogue(self):

        font, ok = QFontDialog.getFont()
        if ok:
            # self.ui.inputDock.setFont(font)
            # self.ui.outputDock.setFont(font)
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
            QMessageBox.about(self,'Information', 'Design Unsafe: CAD image cannot be saved')


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
        self.ui.action_save_input.setEnabled(False)
        self.ui.actionSave_log_messages.setEnabled(False)
        self.ui.actionCreate_design_report.setEnabled(False)
        self.ui.actionSave_3D_model.setEnabled(False)
        self.ui.actionSave_current_image.setEnabled(False)
        self.ui.actionSave_Front_View.setEnabled(False)
        self.ui.actionSave_Top_View.setEnabled(False)
        self.ui.actionSave_Side_View.setEnabled(False)
        self.ui.menuGraphics.setEnabled(False)

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
        self.ui.action_save_input.setEnabled(True)
        self.ui.actionSave_log_messages.setEnabled(True)
        self.ui.actionCreate_design_report.setEnabled(True)
        self.ui.actionSave_3D_model.setEnabled(True)
        self.ui.actionSave_current_image.setEnabled(True)
        self.ui.actionSave_Front_View.setEnabled(True)
        self.ui.actionSave_Top_View.setEnabled(True)
        self.ui.actionSave_Side_View.setEnabled(True)
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
            newlist.append("Select plate thickness")
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


    def check_plate_height(self, widget, lblwidget):
        '''

        Args:
            widget: QlineEdit
            lblwidget: QLabel

        Returns:
        range of plate height

        '''
        def clear_widget():
            ''' Clear the widget and change the label colour in to red '''
            widget.clear()
            widget.setFocus()
            palette = QPalette()
            palette.setColor(QPalette.Foreground, Qt.red)
            lblwidget.setPalette(palette)
            pass

        loc = self.ui.comboConnLoc.currentText()
        if loc == "Select Connectivity":
            QMessageBox.about(self, 'Information', "Please select the Connectivity")
            clear_widget()

        else:

            if loc == "Beam-Beam":
                select_col = "Please select the primary beam"
                select_beam = "Please select the secondary beam"
            else:
                select_col = "Please select the column section"
                select_beam = "Please select the beam section"

            if self.ui.comboColSec.currentText() == "Select section":
                QMessageBox.about(self, 'Information', select_col)
                clear_widget()

            elif self.ui.combo_Beam.currentText() == "Select section":
                QMessageBox.about(self, 'Information', select_beam)
                clear_widget()

            else:

                plate_height = widget.text()
                plate_height = float(plate_height)
                if plate_height == 0:
                    self.ui.btn_Design.setDisabled(False)
                else:

                    dict_beam_data = self.fetchBeamPara()
                    dict_column_data = self.fetchColumnPara()
                    beam_D = float(dict_beam_data['D'])
                    col_T = float(dict_column_data['T'])
                    col_R1 = float(dict_column_data['R1'])
                    beam_T = float(dict_beam_data['T'])
                    beam_R1 = float(dict_beam_data['R1'])
                    clear_depth = 0.0
                    min_plate_height = 0.6 * beam_D
                    if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                        clear_depth = beam_D - 2 * (beam_T + beam_R1 + 5)
                    else:
                        clear_depth = beam_D - (col_R1 + col_T + beam_R1 + beam_T + 10)
                    if clear_depth < plate_height or min_plate_height > plate_height:
                        QMessageBox.about(self, 'Warning', "Height of the fin plate should be in between %s-%s mm" % (int(min_plate_height), int(clear_depth)))
                        clear_widget()
                    else:
                        self.ui.btn_Design.setDisabled(False)
                        palette = QPalette()
                        lblwidget.setPalette(palette)

    def check_plate_width(self, widget):
        loc = self.ui.comboConnLoc.currentText()
        plate_width = widget.text()
        plate_width = float(plate_width)
        if plate_width == 0:
            self.ui.btn_Design.setDisabled(False)
        else:

            dict_column_data = self.fetchColumnPara()
            col_D = float(dict_column_data['D'])
            col_T = float(dict_column_data['T'])
            col_R1 = float(dict_column_data['R1'])
            clear_depth = 0.0
            if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                clear_depth = col_D - 2 * (col_T + col_R1 + 5)

            if clear_depth < plate_width:

                QMessageBox.about(self, 'Information', "Height of the fin plate should be less than %s mm" % (int(clear_depth)))
            else:
                self.ui.btn_Design.setDisabled(False)

    def populateWeldThickCombo(self):
        """Return weld thickness on the basis column flange and plate thickness check
        ThickerPart between column Flange and plate thickness again get checked according to the IS 800 Table 21
        (Name of the table :Minimum Size of First Rum or of a Single Run Fillet Weld)

        Returns:

        """

        if self.ui.comboPlateThick_2.currentText() == "Select plate thickness":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return

        else:
            newlist = ["Select weld thickness"]
            weldlist = [3, 4, 5, 6, 8, 10, 12, 16]
            # dictbeamdata = self.fetchBeamPara()
            # beam_tw = float(dictbeamdata["tw"])
            column_sec = str(self.ui.comboColSec.currentText())
            if column_sec == 'Select section':
                return
            dict_column_data = self.fetchColumnPara()
            plate_thickness = str(self.ui.comboPlateThick_2.currentText())

            try:
                plate_thick = float(plate_thickness)
            except ValueError:
                return

            if str(self.ui.comboConnLoc.currentText()) == "Column flange-Beam web":
                column_tf = float(dict_column_data["T"])
                thicker_part = max(column_tf, plate_thick)

            elif str(self.ui.comboConnLoc.currentText()) == "Column web-Beam web":
                column_tw = float(dict_column_data["tw"])
                thicker_part = max(column_tw, plate_thick)

            elif str(self.ui.comboConnLoc.currentText()) == "Beam-Beam":
                PBeam_tw = float(dict_column_data["tw"])
                thicker_part = max(PBeam_tw, plate_thick)

            else:
                    self.ui.comboWldSize.clear()
                    return

            if thicker_part <= 10:
                weld_index = weldlist.index(3)
                newlist.extend(weldlist[weld_index:])
            elif thicker_part <= 20 and thicker_part > 10:
                weld_index = weldlist.index(5)
                newlist.extend(weldlist[weld_index:])
            elif thicker_part <= 32 and thicker_part > 20:
                weld_index = weldlist.index(6)
                newlist.extend(weldlist[weld_index:])
            else:
                weld_index = weldlist.index(10)
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

    def setDictToUserInputs(self,uiObj):

        if uiObj is not None:
            if uiObj['Connection'] != 'Finplate':
                QMessageBox.information(self, "Information", "You can load this input file only from the corresponding design problem")
                return

            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))

            if uiObj['Member']['Connectivity'] == 'Beam-Beam':

                self.ui.lbl_beam.setText('Secondary beam *')
                self.ui.lbl_column.setText('Primary beam *')
                self.ui.comboColSec.clear()
                self.get_beamdata()
                #self.ui.comboColSec.addItems(get_beamcombolist())
                self.ui.chkBxBeam.setText("SBeam")
                self.ui.chkBxBeam.setToolTip("Secondary  beam")
                self.ui.chkBxCol.setText("PBeam")
                self.ui.chkBxCol.setToolTip("Primary beam")
                self.ui.actionShow_beam.setText("Show SBeam")
                self.ui.actionShow_column.setText("Show PBeam")

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

            self.designPrefDialog.ui.combo_boltHoleType.setCurrentIndex(self.designPrefDialog.ui.combo_boltHoleType.findText(uiObj["bolt"]["bolt_hole_type"]))
            self.designPrefDialog.ui.txt_boltFu.setText(str(uiObj["bolt"]["bolt_fu"]))
            self.designPrefDialog.ui.combo_slipfactor.setCurrentIndex(self.designPrefDialog.ui.combo_slipfactor.findText(str(uiObj["bolt"]["slip_factor"])))
            self.designPrefDialog.ui.combo_weldType.setCurrentIndex(self.designPrefDialog.ui.combo_weldType.findText(uiObj["weld"]["typeof_weld"]))
            self.designPrefDialog.ui.txt_weldFu.setText(str(uiObj["weld"]["fu_overwrite"]))
            self.designPrefDialog.ui.combo_detailingEdgeType.setCurrentIndex(self.designPrefDialog.ui.combo_detailingEdgeType.findText(uiObj["detailing"]["typeof_edge"]))
            self.designPrefDialog.ui.txt_detailingGap.setText(str(uiObj["detailing"]["gap"]))
            self.designPrefDialog.ui.combo_detailing_memebers.setCurrentIndex(self.designPrefDialog.ui.combo_detailing_memebers.findText(uiObj["detailing"]["is_env_corrosive"]))

        else:
            pass

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

        uiObj["Connection"] = self.connection

        return uiObj

    def saveDesign_inputs(self):

        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Design", os.path.join(str(self.folder), "untitled.osi"),
                                                  "Input Files(*.osi)")

        if not fileName:
            return
        try:
            with open(str(fileName), 'w') as out_file:
                json.dump(self.uiObj, out_file)
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return

        # yaml.dump(self.uiObj,out_file,allow_unicode=True, default_flow_style=False)

        pass

    def openDesign_inputs(self):

        fileName, _ = QFileDialog.getOpenFileName(self, "Open Design", str(self.folder), "InputFiles(*.osi)")
        if not fileName:
            return
        try:
            in_file = str(fileName)
            with open(in_file, 'r') as fileObject:
                uiObj = json.load(fileObject)
            self.setDictToUserInputs(uiObj)

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return


    def save_inputs(self, uiObj):
        '''Save the user inputs in text format

        Args:
            :param uiObj: User inputs
            :type uiObj:Dictionary
        '''
        inputFile = os.path.join("Connections", "Shear", "Finplate", "saveINPUT.txt")
        try:
            with open(inputFile, 'w') as input_file:
                json.dump(uiObj, input_file)
        except Exception as e:
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s" % (inputFile, str(e)))

    def get_prevstate(self):
        '''
        '''
        fileName = os.path.join("Connections", "Shear", "Finplate", "saveINPUT.txt")

        if os.path.isfile(fileName):
            with open(fileName, 'r') as fileObject:
                uiObj = json.load(fileObject)
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
        status = self.resultObj['Bolt']['status']
        if status is True:
            self.call_3DModel("white_bg")
            data = os.path.join(str(self.folder), "images_html", "3D_Model.png")
            self.display.ExportToImage(data)
            self.display.FitAll()
        else:
            pass

        fileName = os.path.join(self.folder, "images_html", "Html_Report.html")
        fileName = str(fileName)
        self.commLogicObj.call_designReport(fileName, popup_summary)

        config = configparser.ConfigParser()
        config.read_file(open(r'Osdag.config'))
        wkhtmltopdf_path = config.get('wkhtml_path', 'path1')
        # Creates pdf

        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path )

        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        file_type = "PDF (*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", file_type)
        fname = str(fname)
        flag = True
        if fname == '':
            flag = False
            return flag
        else:
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

        self.ui.comboPlateThick_2.setItemText(0, "Select plate thickness")
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
        self.disableViewButtons()
        self.designPrefDialog.set_default_para()

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
        val = float(textStr)
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

        self.setWindowTitle("Osdag Fin Plate")
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")

        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display

        # background gradient
        display.set_bg_gradient_color([23, 1, 32], [23, 1, 32])
        # display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        display.display_triedron()
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
        check = True
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
                check = False
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
                check = False
            else:
                self.ui.btn_Design.setDisabled(False)
        return check

    def generate_missing_fields_error_string(self, missing_fields_list):
        """

        Args:
            missing_fields_list: list of fields that are not selected or entered

        Returns:
            error string that has to be displayed

        """

        # The base string which should be displayed
        information = "Please input the following required field"
        if len(missing_fields_list) > 1:
            # Adds 's' to the above sentence if there are multiple missing input fields
            information += "s"
        information += ": "

        # Loops through the list of the missing fields and adds each field to the above sentence with a comma
        for item in missing_fields_list:
            information = information + item + ", "

        # Removes the last comma
        information = information[:-2]
        information += "."

        return information

    def validateInputsOnDesignBtn(self):

        flag = True
        missing_fields_list = []

        if self.ui.comboConnLoc.currentIndex() == 0:
            missing_fields_list.append("Connectivity")
            flag = False
            QMessageBox.information(self, "Information", self.generate_missing_fields_error_string(missing_fields_list))
            return flag

        state = self.setimage_connection()
        if state is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web" or self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
                if self.ui.comboColSec.currentIndex() == 0:
                    missing_fields_list.append("Column section")

                if self.ui.combo_Beam.currentIndex() == 0:
                    missing_fields_list.append("Beam section")

            else:
                if self.ui.comboColSec.currentIndex() == 0:
                    missing_fields_list.append("Primary beam section")

                if self.ui.combo_Beam.currentIndex() == 0:
                    missing_fields_list.append("Secondary beam section")

        if self.ui.txtFu.text() == '' or float(self.ui.txtFu.text()) == 0:
            missing_fields_list.append("Ultimate strength of steel")

        if self.ui.txtFy.text() == '' or float(self.ui.txtFy.text()) == 0:
            missing_fields_list.append("Yield strength of steel")

        if self.ui.txtShear.text() == '' or str(self.ui.txtShear.text()) == 0:
            missing_fields_list.append("Factored shear load")

        if self.ui.comboDiameter.currentIndex() == 0:
            missing_fields_list.append("Diameter of bolt")

        if self.ui.comboType.currentIndex() == 0:
            missing_fields_list.append("Type of bolt")

        if self.ui.comboPlateThick_2.currentIndex() == 0:
            missing_fields_list.append("Plate thickness")

        if self.ui.comboWldSize.currentIndex() == 0:
            missing_fields_list.append("Weld thickness")

        if len(missing_fields_list) > 0:
            flag = False
            QMessageBox.information(self, "Information", self.generate_missing_fields_error_string(missing_fields_list))

        if flag:
            flag = self.checkBeam_B()

        return flag


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


    def call_3DModel(self, bgcolor):
        '''

        This routine responsible for displaying 3D Cad model
        :param flag: boolean
        :return:
        '''
        if self.ui.btn3D.isChecked:
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
        self.commLogicObj.display_3DModel("Model",bgcolor)

    def call_3DBeam(self,bgcolor):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam",bgcolor)

    def call_3DColumn(self,bgcolor):
        '''
        '''
        self.ui.chkBxCol.setChecked(Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column",bgcolor)

    def call_3DFinplate(self,bgcolor):
        '''
        Displaying FinPlate in 3D
        '''
        self.ui.chkBxFinplate.setChecked(Qt.Checked)
        if self.ui.chkBxFinplate.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            self.ui.btn3D.setChecked(Qt.Unchecked)

        self.commLogicObj.display_3DModel("Plate",bgcolor)

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

        # if self.designPrefDialog.saved is not True:
        #     design_pref = self.designPrefDialog.set_default_para()
        #     print "default_design_pref=",design_pref
        # else:
        design_pref = self.designPrefDialog.save_designPref_para()  # self.designPrefDialog.save_designPref_para()
        self.uiObj.update(design_pref)
        print ("saved_design_pref = ", self.uiObj)
        return self.uiObj


    def parameters(self):
        self.uiObj = self.getuser_inputs()

        dictbeamdata = self.fetchBeamPara()
        dictcoldata = self.fetchColumnPara()
        dict_angle_data = {}
        dict_topangledata = {}
        loc = str(self.ui.comboConnLoc.currentText())
        component = "Model"
        bolt_dia = int(self.uiObj["Bolt"]["Diameter (mm)"])
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) / 2
        bolt_T = self.boltHeadThick_Calculation(bolt_dia)
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        nut_T = self.nutThick_Calculation(bolt_dia)  # bolt_dia = nut_dia
        return [dictbeamdata, dictcoldata, dict_angle_data, dict_topangledata, loc, component, bolt_R,
                bolt_T, bolt_Ht, nut_T]

    def design_btnclicked(self):
        '''
        '''
        self.display.EraseAll()
        if self.validateInputsOnDesignBtn() is not True:
            return
        self.alist = self.parameters()
        designpreference = self.designParameters()

        print ("uiobj =", self.alist[0])

        self.ui.outputDock.setFixedSize(310, 710)
        self.enableViewButtons()
        self.unchecked_allChkBox()
        self.commLogicObj = CommonDesignLogic(designpreference, self.alist[0], self.alist[1], self.alist[2], self.alist[3],
                                              self.alist[4], self.alist[5], self.alist[6], self.alist[7],
                                              self.alist[8], self.alist[9], self.display, self.folder,
                                              self.connection)

        self.resultObj = self.commLogicObj.resultObj
        alist = self.resultObj.values()
        self.display_output(self.resultObj)
        self.displaylog_totextedit(self.commLogicObj)
        isempty = [True if val != '' else False for ele in alist for val in ele.values()]

        if isempty[0] is True:
            status = self.resultObj['Bolt']['status']
            self.commLogicObj.call_3DModel(status)
            if status is True:
                self.callFin2D_Drawing("All")
                self.ui.actionShow_all.setEnabled(True)
                self.ui.actionShow_beam.setEnabled(True)
                self.ui.actionShow_column.setEnabled(True)
                self.ui.actionShow_finplate.setEnabled(True)
            else:
                self.ui.btn3D.setEnabled(False)
                self.ui.chkBxBeam.setEnabled(False)
                self.ui.chkBxCol.setEnabled(False)
                self.ui.chkBxFinplate.setEnabled(False)
                self.ui.actionShow_all.setEnabled(False)
                self.ui.actionShow_beam.setEnabled(False)
                self.ui.actionShow_column.setEnabled(False)
                self.ui.actionShow_finplate.setEnabled(False)
        else:
            pass
        self.designPrefDialog.saved = False

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
        status = self.resultObj['Bolt']['status']
        if status is True:
            if self.fuse_model is None:
                self.fuse_model = self.create2Dcad()
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
            QMessageBox.about(self,'Information', 'Design Unsafe: 3D Model cannot be saved')

    def callFin2D_Drawing(self, view):  # call2D_Drawing(self,view)

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        self.ui.chkBxFinplate.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.btn3D.setChecked(Qt.Unchecked)
        status = self.resultObj['Bolt']['status']
        if status is True:
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

        else:

            QMessageBox.about(self,'Information', 'Design Unsafe: %s view cannot be viewed' %(view))


    def closeEvent(self, event):
        '''
        Closing finPlate window.
        '''

        # uiInput = self.getuser_inputs()
        uiInput = self.designParameters()
        self.save_inputs(uiInput)
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

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

    def design_examples(self):

        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ResourceFiles', 'design_example', '_build', 'html')
        for html_file in os.listdir(root_path):
            if html_file.startswith('index'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, html_file))
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, html_file)])

    def design_preferences(self):
        self.designPrefDialog.show()

    def bolt_hole_clearace(self):
        self.designPrefDialog.get_clearance()

    def call_boltFu(self):
        self.designPrefDialog.set_boltFu()

    def call_weld_fu(self):
        self.designPrefDialog.set_weldFu()

    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "Osdag_header.png")))
        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

class Ui_ModuleWindow(QMainWindow):
    def launchwindow(self, osdagMainWindow, folder):
        Ui_ModuleWindow.set_osdaglogger(self)
        rawLogger = logging.getLogger("raw")
        rawLogger.setLevel(logging.INFO)
        fh = logging.FileHandler("design_type/connection/fin.log", mode="w")
        formatter = logging.Formatter('''%(message)s''')
        fh.setFormatter(formatter)
        rawLogger.addHandler(fh)
        rawLogger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Finplate/log.css"/>''')

        Ui_ModuleWindow.module_setup(self)
        window = MainController(osdagMainWindow, folder)
        self.hide()

        window.show()
        window.closed.connect(osdagMainWindow.show)

    def set_osdaglogger(self):
        global logger
        logger = None
        if logger is None:
            logger = logging.getLogger("osdag")
        else:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

        logger.setLevel(logging.DEBUG)

        # create the logging file handler
        fh = logging.FileHandler("design_type/connection/fin.log", mode="a")

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

    def module_setup(self):
        global logger
        logger = logging.getLogger("osdag.model")

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
        folder_path = r'D:\Osdag_Workspace\\Finplate'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path, 0o755)
        image_folder_path = os.path.join(folder_path, 'images_html')
        if not os.path.exists(image_folder_path):
            os.mkdir(image_folder_path, 0o755)
        window = MainController(folder_path)
        ########################################
        # folder = None
        window = MainController(folder_path)
        window.show()
        sys.exit(app.exec_())

    def setupUi(self, MainWindow, main):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1328, 769)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/finwindow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(20, 2))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 28))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 28))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btnInput = QtWidgets.QToolButton(self.frame)
        self.btnInput.setGeometry(QtCore.QRect(0, 0, 28, 28))
        self.btnInput.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btnInput.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/images/input.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnInput.setIcon(icon1)
        self.btnInput.setIconSize(QtCore.QSize(18, 18))
        self.btnInput.setObjectName("btnInput")
        self.btnOutput = QtWidgets.QToolButton(self.frame)
        self.btnOutput.setGeometry(QtCore.QRect(30, 0, 28, 28))
        self.btnOutput.setFocusPolicy(QtCore.Qt.TabFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/images/output.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOutput.setIcon(icon2)
        self.btnOutput.setIconSize(QtCore.QSize(18, 18))
        self.btnOutput.setObjectName("btnOutput")
        self.btnTop = QtWidgets.QToolButton(self.frame)
        self.btnTop.setGeometry(QtCore.QRect(160, 0, 28, 28))
        self.btnTop.setFocusPolicy(QtCore.Qt.TabFocus)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/images/X-Y.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTop.setIcon(icon3)
        self.btnTop.setIconSize(QtCore.QSize(22, 22))
        self.btnTop.setObjectName("btnTop")
        self.btnFront = QtWidgets.QToolButton(self.frame)
        self.btnFront.setGeometry(QtCore.QRect(100, 0, 28, 28))
        self.btnFront.setFocusPolicy(QtCore.Qt.TabFocus)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/images/Z-X.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFront.setIcon(icon4)
        self.btnFront.setIconSize(QtCore.QSize(22, 22))
        self.btnFront.setObjectName("btnFront")
        self.btnSide = QtWidgets.QToolButton(self.frame)
        self.btnSide.setGeometry(QtCore.QRect(130, 0, 28, 28))
        self.btnSide.setFocusPolicy(QtCore.Qt.TabFocus)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/images/Z-Y.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSide.setIcon(icon5)
        self.btnSide.setIconSize(QtCore.QSize(22, 22))
        self.btnSide.setObjectName("btnSide")
        self.btn3D = QtWidgets.QCheckBox(self.frame)
        self.btn3D.setGeometry(QtCore.QRect(230, 0, 90, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.btn3D.setFont(font)
        self.btn3D.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn3D.setObjectName("btn3D")
        self.chkBxBeam = QtWidgets.QCheckBox(self.frame)
        self.chkBxBeam.setGeometry(QtCore.QRect(325, 0, 90, 29))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.chkBxBeam.setFont(font)
        self.chkBxBeam.setFocusPolicy(QtCore.Qt.TabFocus)
        self.chkBxBeam.setObjectName("chkBxBeam")
        self.chkBxCol = QtWidgets.QCheckBox(self.frame)
        self.chkBxCol.setGeometry(QtCore.QRect(420, 0, 101, 29))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.chkBxCol.setFont(font)
        self.chkBxCol.setFocusPolicy(QtCore.Qt.TabFocus)
        self.chkBxCol.setObjectName("chkBxCol")
        self.chkBxFinplate = QtWidgets.QCheckBox(self.frame)
        self.chkBxFinplate.setGeometry(QtCore.QRect(530, 0, 101, 29))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.chkBxFinplate.setFont(font)
        self.chkBxFinplate.setFocusPolicy(QtCore.Qt.TabFocus)
        self.chkBxFinplate.setObjectName("chkBxFinplate")
        self.verticalLayout_2.addWidget(self.frame)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.frame_2 = QtWidgets.QFrame(self.splitter)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mytabWidget = QtWidgets.QTabWidget(self.frame_2)
        self.mytabWidget.setMinimumSize(QtCore.QSize(0, 450))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.mytabWidget.setFont(font)
        self.mytabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mytabWidget.setStyleSheet("QTabBar::tab { height: 75px; width: 1px;  }")
        self.mytabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.mytabWidget.setObjectName("mytabWidget")
        self.verticalLayout.addWidget(self.mytabWidget)
        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 125))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit.setReadOnly(True)
        self.textEdit.setOverwriteMode(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1328, 21))
        self.menubar.setStyleSheet("")
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setStyleSheet("QMenu {\n"
"    background-color:#b2bd84;\n"
"    border-color: black;\n"
"    border: 1px solid;\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    color: black;\n"
"    padding: 2px 20px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"   color:white;\n"
"    border-color: darkblue;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"")
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setStyleSheet("QMenu {\n"
"    background-color:#b2bd84;\n"
"    border-color: black;\n"
"    border: 1px solid;\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    color: black;\n"
"    padding: 2px 20px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"   color:white;\n"
"    border-color: darkblue;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"")
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setStyleSheet("QMenu {\n"
"    background-color:#b2bd84;\n"
"    border-color: black;\n"
"    border: 1px solid;\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    color: black;\n"
"    padding: 2px 20px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"   color:white;\n"
"    border-color: darkblue;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"")
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setStyleSheet("QMenu {\n"
"    background-color:#b2bd84;\n"
"    border-color: black;\n"
"    border: 1px solid;\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    color: black;\n"
"    padding: 2px 20px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"   color:white;\n"
"    border-color: darkblue;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"")
        self.menuHelp.setObjectName("menuHelp")
        self.menuGraphics = QtWidgets.QMenu(self.menubar)
        self.menuGraphics.setStyleSheet("QMenu {\n"
"    background-color:#b2bd84;\n"
"    border-color: black;\n"
"    border: 1px solid;\n"
"    margin: 2px; /* some spacing around the menu */\n"
"}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    color: black;\n"
"    padding: 2px 20px 2px 20px;\n"
"    border: 1px solid transparent; /* reserve space for selection border */\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"   color:white;\n"
"    border-color: darkblue;\n"
"    background: #825051;\n"
"    margin-left: 5px;\n"
"    margin-right: 5px;\n"
"}")
        self.menuGraphics.setObjectName("menuGraphics")
        MainWindow.setMenuBar(self.menubar)
        self.inputDock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputDock.sizePolicy().hasHeightForWidth())
        self.inputDock.setSizePolicy(sizePolicy)
        self.inputDock.setMinimumSize(QtCore.QSize(320, 710))
        self.inputDock.setMaximumSize(QtCore.QSize(310, 710))
        self.inputDock.setBaseSize(QtCore.QSize(310, 710))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.inputDock.setFont(font)
        self.inputDock.setFloating(False)
        self.inputDock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.inputDock.setObjectName("inputDock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.txtFy = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.txtFy.setGeometry(QtCore.QRect(150, 217, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txtFy.setFont(font)
        self.txtFy.setObjectName("txtFy")
        self.lbl_column = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_column.setGeometry(QtCore.QRect(6, 127, 151, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_column.setFont(font)
        self.lbl_column.setObjectName("lbl_column")
        self.comboConnLoc = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboConnLoc.setGeometry(QtCore.QRect(150, 40, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.comboConnLoc.setFont(font)
        self.comboConnLoc.setObjectName("comboConnLoc")
        self.comboConnLoc.addItem("")
        self.comboConnLoc.addItem("")
        self.comboConnLoc.addItem("")
        self.comboConnLoc.addItem("")
        self.txtFu = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.txtFu.setGeometry(QtCore.QRect(150, 187, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txtFu.setFont(font)
        self.txtFu.setObjectName("txtFu")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(3, 15, 221, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Link, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Link, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Link, brush)
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        option_list = main.input_values(self)
        _translate = QtCore.QCoreApplication.translate
        for option in option_list:
            lable = option[1]
            l = QtWidgets.QLabel(self.dockWidgetContents)
            l.setGeometry(QtCore.QRect(6, 40, 120, 25))
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(False)
            font.setWeight(50)
            l.setFont(font)
            l.setObjectName("label_4")
            l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))

            type = option[2]
            if type == "combo_box":
                e = QtWidgets.QComboBox(self.dockWidgetContents)
                e.setGeometry(QtCore.QRect(150, 40, 160, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                e.setFont(font)
                e.setObjectName("comboConnLoc")
                for item in option[4]:
                    e.addItem(item)
        # self.label_4 = QtWidgets.QLabel(self.dockWidgetContents)
        # self.label_4.setGeometry(QtCore.QRect(6, 40, 120, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(False)
        # font.setWeight(50)
        # self.label_4.setFont(font)
        # self.label_4.setObjectName("label_4")
        self.lbl_fu = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_fu.setGeometry(QtCore.QRect(6, 187, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_fu.setFont(font)
        self.lbl_fu.setObjectName("lbl_fu")
        self.comboColSec = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboColSec.setGeometry(QtCore.QRect(150, 127, 160, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.comboColSec.setFont(font)
        self.comboColSec.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.comboColSec.setMaxVisibleItems(5)
        self.comboColSec.setObjectName("comboColSec")
        self.lbl_fy = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_fy.setGeometry(QtCore.QRect(6, 212, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_fy.setFont(font)
        self.lbl_fy.setObjectName("lbl_fy")
        self.label_18 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_18.setGeometry(QtCore.QRect(3, 250, 201, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.lbl_shear = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_shear.setGeometry(QtCore.QRect(6, 280, 151, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_shear.setFont(font)
        self.lbl_shear.setObjectName("lbl_shear")
        self.txtShear = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.txtShear.setGeometry(QtCore.QRect(150, 277, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txtShear.setFont(font)
        self.txtShear.setObjectName("txtShear")
        self.label_5 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(3, 310, 150, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.comboType = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboType.setGeometry(QtCore.QRect(150, 370, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.comboType.setFont(font)
        self.comboType.setMaxVisibleItems(10)
        self.comboType.setObjectName("comboType")
        self.label_6 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_6.setGeometry(QtCore.QRect(6, 400, 100, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.comboGrade = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboGrade.setGeometry(QtCore.QRect(150, 400, 160, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.comboGrade.setFont(font)
        self.comboGrade.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.comboGrade.setMaxVisibleItems(6)
        self.comboGrade.setObjectName("comboGrade")
        self.label_7 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_7.setGeometry(QtCore.QRect(6, 340, 131, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_8.setGeometry(QtCore.QRect(6, 370, 100, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.comboDiameter = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboDiameter.setGeometry(QtCore.QRect(150, 340, 160, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.comboDiameter.setFont(font)
        self.comboDiameter.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.comboDiameter.setMaxVisibleItems(5)
        self.comboDiameter.setObjectName("comboDiameter")
        self.comboDiameter.addItem("")
        self.comboDiameter.addItem("")
        self.comboDiameter.addItem("")
        self.comboDiameter.addItem("")
        self.comboDiameter.addItem("")
        self.comboDiameter.addItem("")
        self.comboDiameter.addItem("")
        self.lbl_width_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_width_2.setGeometry(QtCore.QRect(6, 520, 111, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_width_2.setFont(font)
        self.lbl_width_2.setObjectName("lbl_width_2")
        self.label_40 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_40.setGeometry(QtCore.QRect(3, 430, 100, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_41.setGeometry(QtCore.QRect(6, 460, 141, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_41.setFont(font)
        self.label_41.setObjectName("label_41")
        self.txtPlateLen = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.txtPlateLen.setGeometry(QtCore.QRect(150, 490, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txtPlateLen.setFont(font)
        self.txtPlateLen.setText("")
        self.txtPlateLen.setObjectName("txtPlateLen")
        self.lbl_len_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_len_2.setGeometry(QtCore.QRect(6, 490, 111, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_len_2.setFont(font)
        self.lbl_len_2.setObjectName("lbl_len_2")
        self.comboPlateThick_2 = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboPlateThick_2.setGeometry(QtCore.QRect(150, 460, 160, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.comboPlateThick_2.setFont(font)
        self.comboPlateThick_2.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.comboPlateThick_2.setMaxVisibleItems(5)
        self.comboPlateThick_2.setObjectName("comboPlateThick_2")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.comboPlateThick_2.addItem("")
        self.label_42 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_42.setGeometry(QtCore.QRect(3, 550, 66, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_42.setFont(font)
        self.label_42.setObjectName("label_42")
        self.label_43 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_43.setGeometry(QtCore.QRect(6, 580, 151, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_43.setFont(font)
        self.label_43.setObjectName("label_43")
        self.outputFrame_2 = QtWidgets.QFrame(self.dockWidgetContents)
        self.outputFrame_2.setGeometry(QtCore.QRect(988, 620, 320, 690))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFrame_2.sizePolicy().hasHeightForWidth())
        self.outputFrame_2.setSizePolicy(sizePolicy)
        self.outputFrame_2.setMinimumSize(QtCore.QSize(320, 690))
        self.outputFrame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outputFrame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outputFrame_2.setObjectName("outputFrame_2")
        self.txtShrCapacity_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtShrCapacity_2.setGeometry(QtCore.QRect(181, 50, 130, 25))
        self.txtShrCapacity_2.setText("")
        self.txtShrCapacity_2.setReadOnly(True)
        self.txtShrCapacity_2.setObjectName("txtShrCapacity_2")
        self.txtbearCapacity_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtbearCapacity_2.setGeometry(QtCore.QRect(181, 80, 130, 25))
        self.txtbearCapacity_2.setReadOnly(True)
        self.txtbearCapacity_2.setObjectName("txtbearCapacity_2")
        self.txtBoltCapacity_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtBoltCapacity_2.setGeometry(QtCore.QRect(181, 110, 130, 25))
        self.txtBoltCapacity_2.setReadOnly(True)
        self.txtBoltCapacity_2.setObjectName("txtBoltCapacity_2")
        self.txtNoBolts_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtNoBolts_2.setGeometry(QtCore.QRect(181, 140, 130, 25))
        self.txtNoBolts_2.setReadOnly(True)
        self.txtNoBolts_2.setObjectName("txtNoBolts_2")
        self.txtPitch_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtPitch_2.setGeometry(QtCore.QRect(181, 230, 130, 25))
        self.txtPitch_2.setReadOnly(True)
        self.txtPitch_2.setObjectName("txtPitch_2")
        self.txtGuage_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtGuage_2.setGeometry(QtCore.QRect(181, 260, 130, 25))
        self.txtGuage_2.setReadOnly(True)
        self.txtGuage_2.setObjectName("txtGuage_2")
        self.txtEndDist_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtEndDist_2.setGeometry(QtCore.QRect(181, 290, 130, 25))
        self.txtEndDist_2.setReadOnly(True)
        self.txtEndDist_2.setObjectName("txtEndDist_2")
        self.txtEdgeDist_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtEdgeDist_2.setGeometry(QtCore.QRect(181, 320, 130, 25))
        self.txtEdgeDist_2.setReadOnly(True)
        self.txtEdgeDist_2.setObjectName("txtEdgeDist_2")
        self.txtWeldThick_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtWeldThick_2.setGeometry(QtCore.QRect(181, 380, 130, 25))
        self.txtWeldThick_2.setReadOnly(True)
        self.txtWeldThick_2.setObjectName("txtWeldThick_2")
        self.txtResltShr_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtResltShr_2.setGeometry(QtCore.QRect(181, 410, 130, 25))
        self.txtResltShr_2.setReadOnly(True)
        self.txtResltShr_2.setObjectName("txtResltShr_2")
        self.txtWeldStrng_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtWeldStrng_2.setGeometry(QtCore.QRect(181, 440, 130, 25))
        self.txtWeldStrng_2.setReadOnly(True)
        self.txtWeldStrng_2.setObjectName("txtWeldStrng_2")
        self.txtPlateThick_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtPlateThick_2.setGeometry(QtCore.QRect(181, 510, 130, 25))
        self.txtPlateThick_2.setReadOnly(True)
        self.txtPlateThick_2.setObjectName("txtPlateThick_2")
        self.label_44 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_44.setGeometry(QtCore.QRect(4, 30, 66, 17))
        self.label_44.setObjectName("label_44")
        self.label_45 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_45.setGeometry(QtCore.QRect(10, 50, 170, 25))
        self.label_45.setObjectName("label_45")
        self.label_46 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_46.setGeometry(QtCore.QRect(10, 80, 150, 25))
        self.label_46.setObjectName("label_46")
        self.labl123_2 = QtWidgets.QLabel(self.outputFrame_2)
        self.labl123_2.setGeometry(QtCore.QRect(10, 110, 150, 25))
        self.labl123_2.setObjectName("labl123_2")
        self.t_2 = QtWidgets.QLabel(self.outputFrame_2)
        self.t_2.setGeometry(QtCore.QRect(10, 140, 130, 25))
        self.t_2.setObjectName("t_2")
        self.label_47 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_47.setGeometry(QtCore.QRect(10, 230, 130, 25))
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_48.setGeometry(QtCore.QRect(10, 290, 130, 25))
        self.label_48.setObjectName("label_48")
        self.label_49 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_49.setGeometry(QtCore.QRect(10, 380, 130, 25))
        self.label_49.setObjectName("label_49")
        self.label_50 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_50.setGeometry(QtCore.QRect(10, 440, 160, 25))
        self.label_50.setObjectName("label_50")
        self.label_51 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_51.setGeometry(QtCore.QRect(10, 260, 130, 25))
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_52.setGeometry(QtCore.QRect(4, 350, 130, 25))
        self.label_52.setObjectName("label_52")
        self.label_53 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_53.setGeometry(QtCore.QRect(10, 320, 140, 25))
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_54.setGeometry(QtCore.QRect(10, 510, 130, 25))
        self.label_54.setObjectName("label_54")
        self.label_55 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_55.setGeometry(QtCore.QRect(10, 410, 170, 25))
        self.label_55.setObjectName("label_55")
        self.label_56 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_56.setGeometry(QtCore.QRect(10, 540, 160, 25))
        self.label_56.setObjectName("label_56")
        self.label_57 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_57.setGeometry(QtCore.QRect(4, 480, 130, 25))
        self.label_57.setObjectName("label_57")
        self.txtExtMomnt_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtExtMomnt_2.setGeometry(QtCore.QRect(180, 540, 130, 25))
        self.txtExtMomnt_2.setReadOnly(True)
        self.txtExtMomnt_2.setObjectName("txtExtMomnt_2")
        self.txtMomntCapacity_2 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.txtMomntCapacity_2.setGeometry(QtCore.QRect(180, 570, 130, 25))
        self.txtMomntCapacity_2.setReadOnly(True)
        self.txtMomntCapacity_2.setObjectName("txtMomntCapacity_2")
        self.label_58 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_58.setGeometry(QtCore.QRect(10, 570, 170, 25))
        self.label_58.setObjectName("label_58")
        self.lbl_col_2 = QtWidgets.QLabel(self.outputFrame_2)
        self.lbl_col_2.setGeometry(QtCore.QRect(10, 200, 130, 25))
        self.lbl_col_2.setObjectName("lbl_col_2")
        self.lbl_row_2 = QtWidgets.QLabel(self.outputFrame_2)
        self.lbl_row_2.setGeometry(QtCore.QRect(10, 170, 130, 25))
        self.lbl_row_2.setObjectName("lbl_row_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 170, 130, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.outputFrame_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 200, 130, 25))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_59 = QtWidgets.QLabel(self.outputFrame_2)
        self.label_59.setGeometry(QtCore.QRect(120, 0, 60, 31))
        self.label_59.setObjectName("label_59")
        self.pushButton_2 = QtWidgets.QPushButton(self.outputFrame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 620, 40, 50))
        self.pushButton_2.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon6)
        self.pushButton_2.setIconSize(QtCore.QSize(40, 50))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.btnReset_2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnReset_2.setGeometry(QtCore.QRect(30, 1249, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnReset_2.setFont(font)
        self.btnReset_2.setObjectName("btnReset_2")
        self.btnDesign_2 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnDesign_2.setGeometry(QtCore.QRect(150, 1249, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnDesign_2.setFont(font)
        self.btnDesign_2.setAutoDefault(False)
        self.btnDesign_2.setDefault(False)
        self.btnDesign_2.setFlat(False)
        self.btnDesign_2.setObjectName("btnDesign_2")
        self.outputFrame_3 = QtWidgets.QFrame(self.dockWidgetContents)
        self.outputFrame_3.setGeometry(QtCore.QRect(1088, 610, 320, 690))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFrame_3.sizePolicy().hasHeightForWidth())
        self.outputFrame_3.setSizePolicy(sizePolicy)
        self.outputFrame_3.setMinimumSize(QtCore.QSize(320, 690))
        self.outputFrame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outputFrame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outputFrame_3.setObjectName("outputFrame_3")
        self.txtShrCapacity_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtShrCapacity_3.setGeometry(QtCore.QRect(181, 50, 130, 25))
        self.txtShrCapacity_3.setText("")
        self.txtShrCapacity_3.setReadOnly(True)
        self.txtShrCapacity_3.setObjectName("txtShrCapacity_3")
        self.txtbearCapacity_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtbearCapacity_3.setGeometry(QtCore.QRect(181, 80, 130, 25))
        self.txtbearCapacity_3.setReadOnly(True)
        self.txtbearCapacity_3.setObjectName("txtbearCapacity_3")
        self.txtBoltCapacity_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtBoltCapacity_3.setGeometry(QtCore.QRect(181, 110, 130, 25))
        self.txtBoltCapacity_3.setReadOnly(True)
        self.txtBoltCapacity_3.setObjectName("txtBoltCapacity_3")
        self.txtNoBolts_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtNoBolts_3.setGeometry(QtCore.QRect(181, 140, 130, 25))
        self.txtNoBolts_3.setReadOnly(True)
        self.txtNoBolts_3.setObjectName("txtNoBolts_3")
        self.txtPitch_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtPitch_3.setGeometry(QtCore.QRect(181, 230, 130, 25))
        self.txtPitch_3.setReadOnly(True)
        self.txtPitch_3.setObjectName("txtPitch_3")
        self.txtGuage_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtGuage_3.setGeometry(QtCore.QRect(181, 260, 130, 25))
        self.txtGuage_3.setReadOnly(True)
        self.txtGuage_3.setObjectName("txtGuage_3")
        self.txtEndDist_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtEndDist_3.setGeometry(QtCore.QRect(181, 290, 130, 25))
        self.txtEndDist_3.setReadOnly(True)
        self.txtEndDist_3.setObjectName("txtEndDist_3")
        self.txtEdgeDist_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtEdgeDist_3.setGeometry(QtCore.QRect(181, 320, 130, 25))
        self.txtEdgeDist_3.setReadOnly(True)
        self.txtEdgeDist_3.setObjectName("txtEdgeDist_3")
        self.txtWeldThick_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtWeldThick_3.setGeometry(QtCore.QRect(181, 380, 130, 25))
        self.txtWeldThick_3.setReadOnly(True)
        self.txtWeldThick_3.setObjectName("txtWeldThick_3")
        self.txtResltShr_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtResltShr_3.setGeometry(QtCore.QRect(181, 410, 130, 25))
        self.txtResltShr_3.setReadOnly(True)
        self.txtResltShr_3.setObjectName("txtResltShr_3")
        self.txtWeldStrng_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtWeldStrng_3.setGeometry(QtCore.QRect(181, 440, 130, 25))
        self.txtWeldStrng_3.setReadOnly(True)
        self.txtWeldStrng_3.setObjectName("txtWeldStrng_3")
        self.txtPlateThick_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtPlateThick_3.setGeometry(QtCore.QRect(181, 510, 130, 25))
        self.txtPlateThick_3.setReadOnly(True)
        self.txtPlateThick_3.setObjectName("txtPlateThick_3")
        self.label_60 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_60.setGeometry(QtCore.QRect(4, 30, 66, 17))
        self.label_60.setObjectName("label_60")
        self.label_61 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_61.setGeometry(QtCore.QRect(10, 50, 170, 25))
        self.label_61.setObjectName("label_61")
        self.label_62 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_62.setGeometry(QtCore.QRect(10, 80, 150, 25))
        self.label_62.setObjectName("label_62")
        self.labl123_3 = QtWidgets.QLabel(self.outputFrame_3)
        self.labl123_3.setGeometry(QtCore.QRect(10, 110, 150, 25))
        self.labl123_3.setObjectName("labl123_3")
        self.t_3 = QtWidgets.QLabel(self.outputFrame_3)
        self.t_3.setGeometry(QtCore.QRect(10, 140, 130, 25))
        self.t_3.setObjectName("t_3")
        self.label_63 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_63.setGeometry(QtCore.QRect(10, 230, 130, 25))
        self.label_63.setObjectName("label_63")
        self.label_64 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_64.setGeometry(QtCore.QRect(10, 290, 130, 25))
        self.label_64.setObjectName("label_64")
        self.label_65 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_65.setGeometry(QtCore.QRect(10, 380, 130, 25))
        self.label_65.setObjectName("label_65")
        self.label_66 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_66.setGeometry(QtCore.QRect(10, 440, 160, 25))
        self.label_66.setObjectName("label_66")
        self.label_67 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_67.setGeometry(QtCore.QRect(10, 260, 130, 25))
        self.label_67.setObjectName("label_67")
        self.label_68 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_68.setGeometry(QtCore.QRect(4, 350, 130, 25))
        self.label_68.setObjectName("label_68")
        self.label_69 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_69.setGeometry(QtCore.QRect(10, 320, 140, 25))
        self.label_69.setObjectName("label_69")
        self.label_70 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_70.setGeometry(QtCore.QRect(10, 510, 130, 25))
        self.label_70.setObjectName("label_70")
        self.label_71 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_71.setGeometry(QtCore.QRect(10, 410, 170, 25))
        self.label_71.setObjectName("label_71")
        self.label_72 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_72.setGeometry(QtCore.QRect(10, 540, 160, 25))
        self.label_72.setObjectName("label_72")
        self.label_73 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_73.setGeometry(QtCore.QRect(4, 480, 130, 25))
        self.label_73.setObjectName("label_73")
        self.txtExtMomnt_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtExtMomnt_3.setGeometry(QtCore.QRect(180, 540, 130, 25))
        self.txtExtMomnt_3.setReadOnly(True)
        self.txtExtMomnt_3.setObjectName("txtExtMomnt_3")
        self.txtMomntCapacity_3 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.txtMomntCapacity_3.setGeometry(QtCore.QRect(180, 570, 130, 25))
        self.txtMomntCapacity_3.setReadOnly(True)
        self.txtMomntCapacity_3.setObjectName("txtMomntCapacity_3")
        self.label_74 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_74.setGeometry(QtCore.QRect(10, 570, 170, 25))
        self.label_74.setObjectName("label_74")
        self.lbl_col_3 = QtWidgets.QLabel(self.outputFrame_3)
        self.lbl_col_3.setGeometry(QtCore.QRect(10, 200, 130, 25))
        self.lbl_col_3.setObjectName("lbl_col_3")
        self.lbl_row_3 = QtWidgets.QLabel(self.outputFrame_3)
        self.lbl_row_3.setGeometry(QtCore.QRect(10, 170, 130, 25))
        self.lbl_row_3.setObjectName("lbl_row_3")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(180, 170, 130, 25))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.outputFrame_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(180, 200, 130, 25))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_75 = QtWidgets.QLabel(self.outputFrame_3)
        self.label_75.setGeometry(QtCore.QRect(120, 0, 60, 31))
        self.label_75.setObjectName("label_75")
        self.pushButton_3 = QtWidgets.QPushButton(self.outputFrame_3)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 620, 40, 50))
        self.pushButton_3.setText("")
        self.pushButton_3.setIcon(icon6)
        self.pushButton_3.setIconSize(QtCore.QSize(40, 50))
        self.pushButton_3.setCheckable(False)
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setDefault(False)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.btnReset_3 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnReset_3.setGeometry(QtCore.QRect(130, 1239, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnReset_3.setFont(font)
        self.btnReset_3.setObjectName("btnReset_3")
        self.btnDesign_3 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnDesign_3.setGeometry(QtCore.QRect(250, 1239, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnDesign_3.setFont(font)
        self.btnDesign_3.setAutoDefault(False)
        self.btnDesign_3.setDefault(False)
        self.btnDesign_3.setFlat(False)
        self.btnDesign_3.setObjectName("btnDesign_3")
        self.outputFrame_4 = QtWidgets.QFrame(self.dockWidgetContents)
        self.outputFrame_4.setGeometry(QtCore.QRect(1048, 580, 320, 690))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFrame_4.sizePolicy().hasHeightForWidth())
        self.outputFrame_4.setSizePolicy(sizePolicy)
        self.outputFrame_4.setMinimumSize(QtCore.QSize(320, 690))
        self.outputFrame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outputFrame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outputFrame_4.setObjectName("outputFrame_4")
        self.txtShrCapacity_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtShrCapacity_4.setGeometry(QtCore.QRect(181, 50, 130, 25))
        self.txtShrCapacity_4.setText("")
        self.txtShrCapacity_4.setReadOnly(True)
        self.txtShrCapacity_4.setObjectName("txtShrCapacity_4")
        self.txtbearCapacity_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtbearCapacity_4.setGeometry(QtCore.QRect(181, 80, 130, 25))
        self.txtbearCapacity_4.setReadOnly(True)
        self.txtbearCapacity_4.setObjectName("txtbearCapacity_4")
        self.txtBoltCapacity_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtBoltCapacity_4.setGeometry(QtCore.QRect(181, 110, 130, 25))
        self.txtBoltCapacity_4.setReadOnly(True)
        self.txtBoltCapacity_4.setObjectName("txtBoltCapacity_4")
        self.txtNoBolts_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtNoBolts_4.setGeometry(QtCore.QRect(181, 140, 130, 25))
        self.txtNoBolts_4.setReadOnly(True)
        self.txtNoBolts_4.setObjectName("txtNoBolts_4")
        self.txtPitch_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtPitch_4.setGeometry(QtCore.QRect(181, 230, 130, 25))
        self.txtPitch_4.setReadOnly(True)
        self.txtPitch_4.setObjectName("txtPitch_4")
        self.txtGuage_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtGuage_4.setGeometry(QtCore.QRect(181, 260, 130, 25))
        self.txtGuage_4.setReadOnly(True)
        self.txtGuage_4.setObjectName("txtGuage_4")
        self.txtEndDist_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtEndDist_4.setGeometry(QtCore.QRect(181, 290, 130, 25))
        self.txtEndDist_4.setReadOnly(True)
        self.txtEndDist_4.setObjectName("txtEndDist_4")
        self.txtEdgeDist_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtEdgeDist_4.setGeometry(QtCore.QRect(181, 320, 130, 25))
        self.txtEdgeDist_4.setReadOnly(True)
        self.txtEdgeDist_4.setObjectName("txtEdgeDist_4")
        self.txtWeldThick_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtWeldThick_4.setGeometry(QtCore.QRect(181, 380, 130, 25))
        self.txtWeldThick_4.setReadOnly(True)
        self.txtWeldThick_4.setObjectName("txtWeldThick_4")
        self.txtResltShr_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtResltShr_4.setGeometry(QtCore.QRect(181, 410, 130, 25))
        self.txtResltShr_4.setReadOnly(True)
        self.txtResltShr_4.setObjectName("txtResltShr_4")
        self.txtWeldStrng_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtWeldStrng_4.setGeometry(QtCore.QRect(181, 440, 130, 25))
        self.txtWeldStrng_4.setReadOnly(True)
        self.txtWeldStrng_4.setObjectName("txtWeldStrng_4")
        self.txtPlateThick_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtPlateThick_4.setGeometry(QtCore.QRect(181, 510, 130, 25))
        self.txtPlateThick_4.setReadOnly(True)
        self.txtPlateThick_4.setObjectName("txtPlateThick_4")
        self.label_76 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_76.setGeometry(QtCore.QRect(4, 30, 66, 17))
        self.label_76.setObjectName("label_76")
        self.label_77 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_77.setGeometry(QtCore.QRect(10, 50, 170, 25))
        self.label_77.setObjectName("label_77")
        self.label_78 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_78.setGeometry(QtCore.QRect(10, 80, 150, 25))
        self.label_78.setObjectName("label_78")
        self.labl123_4 = QtWidgets.QLabel(self.outputFrame_4)
        self.labl123_4.setGeometry(QtCore.QRect(10, 110, 150, 25))
        self.labl123_4.setObjectName("labl123_4")
        self.t_4 = QtWidgets.QLabel(self.outputFrame_4)
        self.t_4.setGeometry(QtCore.QRect(10, 140, 130, 25))
        self.t_4.setObjectName("t_4")
        self.label_79 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_79.setGeometry(QtCore.QRect(10, 230, 130, 25))
        self.label_79.setObjectName("label_79")
        self.label_80 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_80.setGeometry(QtCore.QRect(10, 290, 130, 25))
        self.label_80.setObjectName("label_80")
        self.label_81 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_81.setGeometry(QtCore.QRect(10, 380, 130, 25))
        self.label_81.setObjectName("label_81")
        self.label_82 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_82.setGeometry(QtCore.QRect(10, 440, 160, 25))
        self.label_82.setObjectName("label_82")
        self.label_83 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_83.setGeometry(QtCore.QRect(10, 260, 130, 25))
        self.label_83.setObjectName("label_83")
        self.label_84 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_84.setGeometry(QtCore.QRect(4, 350, 130, 25))
        self.label_84.setObjectName("label_84")
        self.label_85 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_85.setGeometry(QtCore.QRect(10, 320, 140, 25))
        self.label_85.setObjectName("label_85")
        self.label_86 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_86.setGeometry(QtCore.QRect(10, 510, 130, 25))
        self.label_86.setObjectName("label_86")
        self.label_87 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_87.setGeometry(QtCore.QRect(10, 410, 170, 25))
        self.label_87.setObjectName("label_87")
        self.label_88 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_88.setGeometry(QtCore.QRect(10, 540, 160, 25))
        self.label_88.setObjectName("label_88")
        self.label_89 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_89.setGeometry(QtCore.QRect(4, 480, 130, 25))
        self.label_89.setObjectName("label_89")
        self.txtExtMomnt_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtExtMomnt_4.setGeometry(QtCore.QRect(180, 540, 130, 25))
        self.txtExtMomnt_4.setReadOnly(True)
        self.txtExtMomnt_4.setObjectName("txtExtMomnt_4")
        self.txtMomntCapacity_4 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.txtMomntCapacity_4.setGeometry(QtCore.QRect(180, 570, 130, 25))
        self.txtMomntCapacity_4.setReadOnly(True)
        self.txtMomntCapacity_4.setObjectName("txtMomntCapacity_4")
        self.label_90 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_90.setGeometry(QtCore.QRect(10, 570, 170, 25))
        self.label_90.setObjectName("label_90")
        self.lbl_col_4 = QtWidgets.QLabel(self.outputFrame_4)
        self.lbl_col_4.setGeometry(QtCore.QRect(10, 200, 130, 25))
        self.lbl_col_4.setObjectName("lbl_col_4")
        self.lbl_row_4 = QtWidgets.QLabel(self.outputFrame_4)
        self.lbl_row_4.setGeometry(QtCore.QRect(10, 170, 130, 25))
        self.lbl_row_4.setObjectName("lbl_row_4")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.lineEdit_7.setGeometry(QtCore.QRect(180, 170, 130, 25))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.outputFrame_4)
        self.lineEdit_8.setGeometry(QtCore.QRect(180, 200, 130, 25))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_91 = QtWidgets.QLabel(self.outputFrame_4)
        self.label_91.setGeometry(QtCore.QRect(120, 0, 60, 31))
        self.label_91.setObjectName("label_91")
        self.pushButton_4 = QtWidgets.QPushButton(self.outputFrame_4)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 620, 40, 50))
        self.pushButton_4.setText("")
        self.pushButton_4.setIcon(icon6)
        self.pushButton_4.setIconSize(QtCore.QSize(40, 50))
        self.pushButton_4.setCheckable(False)
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.btnReset_4 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnReset_4.setGeometry(QtCore.QRect(90, 1209, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnReset_4.setFont(font)
        self.btnReset_4.setObjectName("btnReset_4")
        self.btnDesign_4 = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnDesign_4.setGeometry(QtCore.QRect(210, 1209, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnDesign_4.setFont(font)
        self.btnDesign_4.setAutoDefault(False)
        self.btnDesign_4.setDefault(False)
        self.btnDesign_4.setFlat(False)
        self.btnDesign_4.setObjectName("btnDesign_4")
        self.txtPlateWidth = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.txtPlateWidth.setGeometry(QtCore.QRect(150, 520, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.txtPlateWidth.setFont(font)
        self.txtPlateWidth.setObjectName("txtPlateWidth")
        self.btn_Reset = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_Reset.setGeometry(QtCore.QRect(30, 620, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Reset.setFont(font)
        self.btn_Reset.setAutoDefault(True)
        self.btn_Reset.setObjectName("btn_Reset")
        self.btn_Design = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_Design.setGeometry(QtCore.QRect(140, 620, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Design.setFont(font)
        self.btn_Design.setAutoDefault(True)
        self.btn_Design.setObjectName("btn_Design")
        self.combo_Beam = QtWidgets.QComboBox(self.dockWidgetContents)
        self.combo_Beam.setGeometry(QtCore.QRect(150, 157, 160, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.combo_Beam.setFont(font)
        self.combo_Beam.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.combo_Beam.setMaxVisibleItems(5)
        self.combo_Beam.setObjectName("combo_Beam")
        self.comboWldSize = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboWldSize.setGeometry(QtCore.QRect(150, 580, 160, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.comboWldSize.setFont(font)
        self.comboWldSize.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.comboWldSize.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.comboWldSize.setMaxVisibleItems(5)
        self.comboWldSize.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.comboWldSize.setObjectName("comboWldSize")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.comboWldSize.addItem("")
        self.lbl_connectivity = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_connectivity.setGeometry(QtCore.QRect(190, 70, 81, 51))
        self.lbl_connectivity.setScaledContents(True)
        self.lbl_connectivity.setObjectName("lbl_connectivity")
        self.lbl_beam = QtWidgets.QLabel(self.dockWidgetContents)
        self.lbl_beam.setGeometry(QtCore.QRect(6, 157, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_beam.setFont(font)
        self.lbl_beam.setObjectName("lbl_beam")
        self.inputDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.inputDock)
        self.outputDock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputDock.sizePolicy().hasHeightForWidth())
        self.outputDock.setSizePolicy(sizePolicy)
        self.outputDock.setMinimumSize(QtCore.QSize(320, 710))
        self.outputDock.setMaximumSize(QtCore.QSize(310, 710))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.outputDock.setFont(font)
        self.outputDock.setObjectName("outputDock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.txtNoBolts = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtNoBolts.setGeometry(QtCore.QRect(200, 120, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtNoBolts.setFont(font)
        self.txtNoBolts.setReadOnly(True)
        self.txtNoBolts.setObjectName("txtNoBolts")
        self.t_7 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.t_7.setGeometry(QtCore.QRect(2, 120, 191, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.t_7.setFont(font)
        self.t_7.setObjectName("t_7")
        self.txtShrCapacity = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtShrCapacity.setGeometry(QtCore.QRect(200, 30, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtShrCapacity.setFont(font)
        self.txtShrCapacity.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.txtShrCapacity.setText("")
        self.txtShrCapacity.setReadOnly(True)
        self.txtShrCapacity.setObjectName("txtShrCapacity")
        self.txtPitch = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtPitch.setGeometry(QtCore.QRect(200, 240, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtPitch.setFont(font)
        self.txtPitch.setReadOnly(True)
        self.txtPitch.setObjectName("txtPitch")
        self.txtGuage = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtGuage.setGeometry(QtCore.QRect(200, 270, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtGuage.setFont(font)
        self.txtGuage.setReadOnly(True)
        self.txtGuage.setObjectName("txtGuage")
        self.txtBoltCapacity = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtBoltCapacity.setGeometry(QtCore.QRect(200, 90, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtBoltCapacity.setFont(font)
        self.txtBoltCapacity.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.txtBoltCapacity.setReadOnly(True)
        self.txtBoltCapacity.setObjectName("txtBoltCapacity")
        self.txt_col = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txt_col.setGeometry(QtCore.QRect(200, 210, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_col.setFont(font)
        self.txt_col.setReadOnly(True)
        self.txt_col.setObjectName("txt_col")
        self.txt_row = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txt_row.setGeometry(QtCore.QRect(200, 180, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txt_row.setFont(font)
        self.txt_row.setReadOnly(True)
        self.txt_row.setObjectName("txt_row")
        self.label_152 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_152.setGeometry(QtCore.QRect(2, 270, 130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_152.setFont(font)
        self.label_152.setObjectName("label_152")
        self.labl123_7 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.labl123_7.setGeometry(QtCore.QRect(2, 90, 179, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.labl123_7.setFont(font)
        self.labl123_7.setObjectName("labl123_7")
        self.txtbearCapacity = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtbearCapacity.setGeometry(QtCore.QRect(200, 60, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtbearCapacity.setFont(font)
        self.txtbearCapacity.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.txtbearCapacity.setReadOnly(True)
        self.txtbearCapacity.setObjectName("txtbearCapacity")
        self.label_153 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_153.setGeometry(QtCore.QRect(2, 300, 179, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_153.setFont(font)
        self.label_153.setObjectName("label_153")
        self.lbl_col_7 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.lbl_col_7.setGeometry(QtCore.QRect(2, 210, 130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_col_7.setFont(font)
        self.lbl_col_7.setObjectName("lbl_col_7")
        self.label_154 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_154.setGeometry(QtCore.QRect(2, 240, 130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_154.setFont(font)
        self.label_154.setObjectName("label_154")
        self.txtEdgeDist = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtEdgeDist.setGeometry(QtCore.QRect(200, 330, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtEdgeDist.setFont(font)
        self.txtEdgeDist.setReadOnly(True)
        self.txtEdgeDist.setObjectName("txtEdgeDist")
        self.lbl_row_7 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.lbl_row_7.setGeometry(QtCore.QRect(2, 180, 130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_row_7.setFont(font)
        self.lbl_row_7.setObjectName("lbl_row_7")
        self.label_155 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_155.setGeometry(QtCore.QRect(2, 330, 179, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_155.setFont(font)
        self.label_155.setObjectName("label_155")
        self.label_156 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_156.setGeometry(QtCore.QRect(2, 30, 161, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_156.setFont(font)
        self.label_156.setObjectName("label_156")
        self.txtEndDist = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtEndDist.setGeometry(QtCore.QRect(200, 300, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtEndDist.setFont(font)
        self.txtEndDist.setReadOnly(True)
        self.txtEndDist.setObjectName("txtEndDist")
        self.label_157 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_157.setGeometry(QtCore.QRect(-1, 10, 66, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(False)
        self.label_157.setFont(font)
        self.label_157.setObjectName("label_157")
        self.label_158 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_158.setGeometry(QtCore.QRect(2, 60, 179, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_158.setFont(font)
        self.label_158.setObjectName("label_158")
        self.label_160 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_160.setGeometry(QtCore.QRect(2, 480, 191, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_160.setFont(font)
        self.label_160.setObjectName("label_160")
        self.txtMomntCapacity = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtMomntCapacity.setGeometry(QtCore.QRect(200, 480, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMomntCapacity.setFont(font)
        self.txtMomntCapacity.setReadOnly(True)
        self.txtMomntCapacity.setObjectName("txtMomntCapacity")
        self.label_161 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_161.setGeometry(QtCore.QRect(-1, 360, 130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_161.setFont(font)
        self.label_161.setObjectName("label_161")
        self.txtExtMomnt = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtExtMomnt.setGeometry(QtCore.QRect(200, 450, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtExtMomnt.setFont(font)
        self.txtExtMomnt.setReadOnly(True)
        self.txtExtMomnt.setObjectName("txtExtMomnt")
        self.label_162 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_162.setGeometry(QtCore.QRect(2, 450, 191, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_162.setFont(font)
        self.label_162.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_162.setObjectName("label_162")
        self.txtWeldStrng = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtWeldStrng.setGeometry(QtCore.QRect(200, 570, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtWeldStrng.setFont(font)
        self.txtWeldStrng.setReadOnly(True)
        self.txtWeldStrng.setObjectName("txtWeldStrng")
        self.label_163 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_163.setGeometry(QtCore.QRect(2, 540, 191, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_163.setFont(font)
        self.label_163.setObjectName("label_163")
        self.label_164 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_164.setGeometry(QtCore.QRect(2, 570, 191, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_164.setFont(font)
        self.label_164.setObjectName("label_164")
        self.txtResltShr = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtResltShr.setGeometry(QtCore.QRect(200, 540, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtResltShr.setFont(font)
        self.txtResltShr.setReadOnly(True)
        self.txtResltShr.setObjectName("txtResltShr")
        self.label_166 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_166.setGeometry(QtCore.QRect(-1, 510, 130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_166.setFont(font)
        self.label_166.setObjectName("label_166")
        self.btn_SaveMessages = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.btn_SaveMessages.setGeometry(QtCore.QRect(50, 600, 200, 30))
        self.btn_SaveMessages.setAutoDefault(True)
        self.btn_SaveMessages.setObjectName("btn_SaveMessages")
        self.btn_CreateDesign = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.btn_CreateDesign.setGeometry(QtCore.QRect(50, 630, 200, 30))
        self.btn_CreateDesign.setAutoDefault(True)
        self.btn_CreateDesign.setObjectName("btn_CreateDesign")
        self.plateHeight = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.plateHeight.setGeometry(QtCore.QRect(2, 390, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.plateHeight.setFont(font)
        self.plateHeight.setObjectName("plateHeight")
        self.txtplate_ht = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtplate_ht.setGeometry(QtCore.QRect(200, 390, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtplate_ht.setFont(font)
        self.txtplate_ht.setReadOnly(True)
        self.txtplate_ht.setObjectName("txtplate_ht")
        self.txtplate_width = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtplate_width.setGeometry(QtCore.QRect(200, 420, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtplate_width.setFont(font)
        self.txtplate_width.setReadOnly(True)
        self.txtplate_width.setObjectName("txtplate_width")
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_2.setGeometry(QtCore.QRect(2, 420, 100, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_10 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_10.setGeometry(QtCore.QRect(2, 150, 200, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.txtboltgrpcapacity = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.txtboltgrpcapacity.setGeometry(QtCore.QRect(200, 150, 100, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtboltgrpcapacity.setFont(font)
        self.txtboltgrpcapacity.setReadOnly(True)
        self.txtboltgrpcapacity.setObjectName("txtboltgrpcapacity")
        self.outputDock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.outputDock)
        self.actionInput = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/input.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInput.setIcon(icon7)
        self.actionInput.setObjectName("actionInput")
        self.actionInputwindow = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/inputview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInputwindow.setIcon(icon8)
        self.actionInputwindow.setObjectName("actionInputwindow")
        self.actionNew = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.actionNew.setFont(font)
        self.actionNew.setObjectName("actionNew")
        self.action_load_input = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setItalic(False)
        self.action_load_input.setFont(font)
        self.action_load_input.setObjectName("action_load_input")
        self.action_save_input = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.action_save_input.setFont(font)
        self.action_save_input.setObjectName("action_save_input")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.actionCut = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionCut.setFont(font)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionCopy.setFont(font)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionPaste.setFont(font)
        self.actionPaste.setObjectName("actionPaste")
        self.actionInput_Browser = QtWidgets.QAction(MainWindow)
        self.actionInput_Browser.setObjectName("actionInput_Browser")
        self.actionOutput_Browser = QtWidgets.QAction(MainWindow)
        self.actionOutput_Browser.setObjectName("actionOutput_Browser")
        self.actionAbout_Osdag = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionAbout_Osdag.setFont(font)
        self.actionAbout_Osdag.setObjectName("actionAbout_Osdag")
        self.actionBeam = QtWidgets.QAction(MainWindow)
        self.actionBeam.setObjectName("actionBeam")
        self.actionColumn = QtWidgets.QAction(MainWindow)
        self.actionColumn.setObjectName("actionColumn")
        self.actionFinplate = QtWidgets.QAction(MainWindow)
        self.actionFinplate.setObjectName("actionFinplate")
        self.actionBolt = QtWidgets.QAction(MainWindow)
        self.actionBolt.setObjectName("actionBolt")
        self.action2D_view = QtWidgets.QAction(MainWindow)
        self.action2D_view.setObjectName("action2D_view")
        self.actionZoom_in = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionZoom_in.setFont(font)
        self.actionZoom_in.setObjectName("actionZoom_in")
        self.actionZoom_out = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionZoom_out.setFont(font)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.actionPan = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionPan.setFont(font)
        self.actionPan.setObjectName("actionPan")
        self.actionRotate_3D_model = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionRotate_3D_model.setFont(font)
        self.actionRotate_3D_model.setObjectName("actionRotate_3D_model")
        self.actionView_2D_on_XY = QtWidgets.QAction(MainWindow)
        self.actionView_2D_on_XY.setObjectName("actionView_2D_on_XY")
        self.actionView_2D_on_YZ = QtWidgets.QAction(MainWindow)
        self.actionView_2D_on_YZ.setObjectName("actionView_2D_on_YZ")
        self.actionView_2D_on_ZX = QtWidgets.QAction(MainWindow)
        self.actionView_2D_on_ZX.setObjectName("actionView_2D_on_ZX")
        self.actionModel = QtWidgets.QAction(MainWindow)
        self.actionModel.setObjectName("actionModel")
        self.actionEnlarge_font_size = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionEnlarge_font_size.setFont(font)
        self.actionEnlarge_font_size.setObjectName("actionEnlarge_font_size")
        self.actionReduce_font_size = QtWidgets.QAction(MainWindow)
        self.actionReduce_font_size.setObjectName("actionReduce_font_size")
        self.actionSave_3D_model = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_3D_model.setFont(font)
        self.actionSave_3D_model.setObjectName("actionSave_3D_model")
        self.actionSave_current_image = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_current_image.setFont(font)
        self.actionSave_current_image.setObjectName("actionSave_current_image")
        self.actionSave_log_messages = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_log_messages.setFont(font)
        self.actionSave_log_messages.setObjectName("actionSave_log_messages")
        self.actionCreate_design_report = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionCreate_design_report.setFont(font)
        self.actionCreate_design_report.setObjectName("actionCreate_design_report")
        self.actionQuit_fin_plate_design = QtWidgets.QAction(MainWindow)
        self.actionQuit_fin_plate_design.setObjectName("actionQuit_fin_plate_design")
        self.actionSave_Front_View = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_Front_View.setFont(font)
        self.actionSave_Front_View.setObjectName("actionSave_Front_View")
        self.actionSave_Top_View = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_Top_View.setFont(font)
        self.actionSave_Top_View.setObjectName("actionSave_Top_View")
        self.actionSave_Side_View = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_Side_View.setFont(font)
        self.actionSave_Side_View.setObjectName("actionSave_Side_View")
        self.actionChange_bg_color = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.actionChange_bg_color.setFont(font)
        self.actionChange_bg_color.setObjectName("actionChange_bg_color")
        self.actionShow_beam = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setItalic(False)
        self.actionShow_beam.setFont(font)
        self.actionShow_beam.setObjectName("actionShow_beam")
        self.actionShow_column = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionShow_column.setFont(font)
        self.actionShow_column.setObjectName("actionShow_column")
        self.actionShow_finplate = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionShow_finplate.setFont(font)
        self.actionShow_finplate.setObjectName("actionShow_finplate")
        self.actionChange_background = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionChange_background.setFont(font)
        self.actionChange_background.setObjectName("actionChange_background")
        self.actionShow_all = QtWidgets.QAction(MainWindow)
        self.actionShow_all.setObjectName("actionShow_all")
        self.actionDesign_examples = QtWidgets.QAction(MainWindow)
        self.actionDesign_examples.setObjectName("actionDesign_examples")
        self.actionSample_Problems = QtWidgets.QAction(MainWindow)
        self.actionSample_Problems.setObjectName("actionSample_Problems")
        self.actionSample_Tutorials = QtWidgets.QAction(MainWindow)
        self.actionSample_Tutorials.setObjectName("actionSample_Tutorials")
        self.actionAbout_Osdag_2 = QtWidgets.QAction(MainWindow)
        self.actionAbout_Osdag_2.setObjectName("actionAbout_Osdag_2")
        self.actionOsdag_Manual = QtWidgets.QAction(MainWindow)
        self.actionOsdag_Manual.setObjectName("actionOsdag_Manual")
        self.actionAsk_Us_a_Question = QtWidgets.QAction(MainWindow)
        self.actionAsk_Us_a_Question.setObjectName("actionAsk_Us_a_Question")
        self.actionFAQ = QtWidgets.QAction(MainWindow)
        self.actionFAQ.setObjectName("actionFAQ")
        self.actionDesign_Preferences = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Serif")
        self.actionDesign_Preferences.setFont(font)
        self.actionDesign_Preferences.setObjectName("actionDesign_Preferences")
        self.actionfinPlate_quit = QtWidgets.QAction(MainWindow)
        self.actionfinPlate_quit.setObjectName("actionfinPlate_quit")
        self.actio_load_input = QtWidgets.QAction(MainWindow)
        self.actio_load_input.setObjectName("actio_load_input")
        self.menuFile.addAction(self.action_load_input)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_save_input)
        self.menuFile.addAction(self.actionSave_log_messages)
        self.menuFile.addAction(self.actionCreate_design_report)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_3D_model)
        self.menuFile.addAction(self.actionSave_current_image)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Front_View)
        self.menuFile.addAction(self.actionSave_Top_View)
        self.menuFile.addAction(self.actionSave_Side_View)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionfinPlate_quit)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDesign_Preferences)
        self.menuView.addAction(self.actionEnlarge_font_size)
        self.menuView.addSeparator()
        self.menuHelp.addAction(self.actionSample_Tutorials)
        self.menuHelp.addAction(self.actionDesign_examples)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAsk_Us_a_Question)
        self.menuHelp.addAction(self.actionAbout_Osdag_2)
        self.menuGraphics.addSeparator()
        self.menuGraphics.addAction(self.actionZoom_in)
        self.menuGraphics.addAction(self.actionZoom_out)
        self.menuGraphics.addAction(self.actionPan)
        self.menuGraphics.addAction(self.actionRotate_3D_model)
        self.menuGraphics.addSeparator()
        self.menuGraphics.addAction(self.actionShow_beam)
        self.menuGraphics.addAction(self.actionShow_column)
        self.menuGraphics.addAction(self.actionShow_finplate)
        self.menuGraphics.addAction(self.actionShow_all)
        self.menuGraphics.addSeparator()
        self.menuGraphics.addAction(self.actionChange_background)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuGraphics.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.mytabWidget.setCurrentIndex(-1)
        self.comboColSec.setCurrentIndex(-1)
        self.comboPlateThick_2.setCurrentIndex(0)
        self.combo_Beam.setCurrentIndex(-1)
        self.comboWldSize.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.comboConnLoc, self.comboColSec)
        MainWindow.setTabOrder(self.comboColSec, self.combo_Beam)
        MainWindow.setTabOrder(self.combo_Beam, self.txtFu)
        MainWindow.setTabOrder(self.txtFu, self.txtFy)
        MainWindow.setTabOrder(self.txtFy, self.txtShear)
        MainWindow.setTabOrder(self.txtShear, self.comboDiameter)
        MainWindow.setTabOrder(self.comboDiameter, self.comboType)
        MainWindow.setTabOrder(self.comboType, self.comboGrade)
        MainWindow.setTabOrder(self.comboGrade, self.comboPlateThick_2)
        MainWindow.setTabOrder(self.comboPlateThick_2, self.txtPlateLen)
        MainWindow.setTabOrder(self.txtPlateLen, self.txtPlateWidth)
        MainWindow.setTabOrder(self.txtPlateWidth, self.comboWldSize)
        MainWindow.setTabOrder(self.comboWldSize, self.btn_Design)
        MainWindow.setTabOrder(self.btn_Design, self.btn_Reset)
        MainWindow.setTabOrder(self.btn_Reset, self.btn_SaveMessages)
        MainWindow.setTabOrder(self.btn_SaveMessages, self.btn_CreateDesign)
        MainWindow.setTabOrder(self.btn_CreateDesign, self.btnInput)
        MainWindow.setTabOrder(self.btnInput, self.btnOutput)
        MainWindow.setTabOrder(self.btnOutput, self.btnFront)
        MainWindow.setTabOrder(self.btnFront, self.btnSide)
        MainWindow.setTabOrder(self.btnSide, self.btnTop)
        MainWindow.setTabOrder(self.btnTop, self.btn3D)
        MainWindow.setTabOrder(self.btn3D, self.chkBxBeam)
        MainWindow.setTabOrder(self.chkBxBeam, self.chkBxCol)
        MainWindow.setTabOrder(self.chkBxCol, self.chkBxFinplate)
        MainWindow.setTabOrder(self.chkBxFinplate, self.lineEdit_4)
        MainWindow.setTabOrder(self.lineEdit_4, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.btnReset_2)
        MainWindow.setTabOrder(self.btnReset_2, self.btnDesign_2)
        MainWindow.setTabOrder(self.btnDesign_2, self.txtGuage_2)
        MainWindow.setTabOrder(self.txtGuage_2, self.txtbearCapacity_3)
        MainWindow.setTabOrder(self.txtbearCapacity_3, self.txtBoltCapacity_3)
        MainWindow.setTabOrder(self.txtBoltCapacity_3, self.txtNoBolts_3)
        MainWindow.setTabOrder(self.txtNoBolts_3, self.txtPitch_3)
        MainWindow.setTabOrder(self.txtPitch_3, self.txtGuage_3)
        MainWindow.setTabOrder(self.txtGuage_3, self.txtEndDist_3)
        MainWindow.setTabOrder(self.txtEndDist_3, self.txtEdgeDist_3)
        MainWindow.setTabOrder(self.txtEdgeDist_3, self.txtWeldThick_3)
        MainWindow.setTabOrder(self.txtWeldThick_3, self.txtResltShr_3)
        MainWindow.setTabOrder(self.txtResltShr_3, self.txtWeldStrng_3)
        MainWindow.setTabOrder(self.txtWeldStrng_3, self.txtPlateThick_3)
        MainWindow.setTabOrder(self.txtPlateThick_3, self.txtExtMomnt_3)
        MainWindow.setTabOrder(self.txtExtMomnt_3, self.txtMomntCapacity_3)
        MainWindow.setTabOrder(self.txtMomntCapacity_3, self.lineEdit_5)
        MainWindow.setTabOrder(self.lineEdit_5, self.lineEdit_6)
        MainWindow.setTabOrder(self.lineEdit_6, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.btnReset_3)
        MainWindow.setTabOrder(self.btnReset_3, self.btnDesign_3)
        MainWindow.setTabOrder(self.btnDesign_3, self.txtShrCapacity_4)
        MainWindow.setTabOrder(self.txtShrCapacity_4, self.txtbearCapacity_4)
        MainWindow.setTabOrder(self.txtbearCapacity_4, self.txtBoltCapacity_4)
        MainWindow.setTabOrder(self.txtBoltCapacity_4, self.txtNoBolts_4)
        MainWindow.setTabOrder(self.txtNoBolts_4, self.txtPitch_4)
        MainWindow.setTabOrder(self.txtPitch_4, self.txtGuage_4)
        MainWindow.setTabOrder(self.txtGuage_4, self.txtEndDist_4)
        MainWindow.setTabOrder(self.txtEndDist_4, self.txtEdgeDist_4)
        MainWindow.setTabOrder(self.txtEdgeDist_4, self.txtWeldThick_4)
        MainWindow.setTabOrder(self.txtWeldThick_4, self.txtResltShr_4)
        MainWindow.setTabOrder(self.txtResltShr_4, self.txtWeldStrng_4)
        MainWindow.setTabOrder(self.txtWeldStrng_4, self.txtPlateThick_4)
        MainWindow.setTabOrder(self.txtPlateThick_4, self.txtExtMomnt_4)
        MainWindow.setTabOrder(self.txtExtMomnt_4, self.txtMomntCapacity_4)
        MainWindow.setTabOrder(self.txtMomntCapacity_4, self.lineEdit_7)
        MainWindow.setTabOrder(self.lineEdit_7, self.lineEdit_8)
        MainWindow.setTabOrder(self.lineEdit_8, self.pushButton_4)
        MainWindow.setTabOrder(self.pushButton_4, self.btnReset_4)
        MainWindow.setTabOrder(self.btnReset_4, self.btnDesign_4)
        MainWindow.setTabOrder(self.btnDesign_4, self.txtShrCapacity_2)
        MainWindow.setTabOrder(self.txtShrCapacity_2, self.txtNoBolts_2)
        MainWindow.setTabOrder(self.txtNoBolts_2, self.txtBoltCapacity_2)
        MainWindow.setTabOrder(self.txtBoltCapacity_2, self.textEdit)
        MainWindow.setTabOrder(self.textEdit, self.txtbearCapacity_2)
        MainWindow.setTabOrder(self.txtbearCapacity_2, self.txtNoBolts)
        MainWindow.setTabOrder(self.txtNoBolts, self.txtShrCapacity)
        MainWindow.setTabOrder(self.txtShrCapacity, self.txtPitch)
        MainWindow.setTabOrder(self.txtPitch, self.txtGuage)
        MainWindow.setTabOrder(self.txtGuage, self.txtBoltCapacity)
        MainWindow.setTabOrder(self.txtBoltCapacity, self.txt_col)
        MainWindow.setTabOrder(self.txt_col, self.txt_row)
        MainWindow.setTabOrder(self.txt_row, self.txtbearCapacity)
        MainWindow.setTabOrder(self.txtbearCapacity, self.txtEdgeDist)
        MainWindow.setTabOrder(self.txtEdgeDist, self.txtEndDist)
        MainWindow.setTabOrder(self.txtEndDist, self.txtMomntCapacity)
        MainWindow.setTabOrder(self.txtMomntCapacity, self.txtExtMomnt)
        MainWindow.setTabOrder(self.txtExtMomnt, self.txtWeldStrng)
        MainWindow.setTabOrder(self.txtWeldStrng, self.txtResltShr)
        MainWindow.setTabOrder(self.txtResltShr, self.txtPitch_2)
        MainWindow.setTabOrder(self.txtPitch_2, self.txtShrCapacity_3)
        MainWindow.setTabOrder(self.txtShrCapacity_3, self.txtplate_ht)
        MainWindow.setTabOrder(self.txtplate_ht, self.txtplate_width)
        MainWindow.setTabOrder(self.txtplate_width, self.txtboltgrpcapacity)
        MainWindow.setTabOrder(self.txtboltgrpcapacity, self.txtEndDist_2)
        MainWindow.setTabOrder(self.txtEndDist_2, self.txtEdgeDist_2)
        MainWindow.setTabOrder(self.txtEdgeDist_2, self.txtWeldStrng_2)
        MainWindow.setTabOrder(self.txtWeldStrng_2, self.txtWeldThick_2)
        MainWindow.setTabOrder(self.txtWeldThick_2, self.txtResltShr_2)
        MainWindow.setTabOrder(self.txtResltShr_2, self.txtPlateThick_2)
        MainWindow.setTabOrder(self.txtPlateThick_2, self.txtExtMomnt_2)
        MainWindow.setTabOrder(self.txtExtMomnt_2, self.txtMomntCapacity_2)
        MainWindow.setTabOrder(self.txtMomntCapacity_2, self.lineEdit_3)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fin Plate"))
        self.btnInput.setToolTip(_translate("MainWindow", "Left Dock"))
        self.btnInput.setText(_translate("MainWindow", "input"))
        self.btnOutput.setToolTip(_translate("MainWindow", "Right Dock"))
        self.btnOutput.setText(_translate("MainWindow", "..."))
        self.btnTop.setToolTip(_translate("MainWindow", "Top View"))
        self.btnTop.setText(_translate("MainWindow", "..."))
        self.btnFront.setToolTip(_translate("MainWindow", "Front View"))
        self.btnFront.setText(_translate("MainWindow", "..."))
        self.btnSide.setToolTip(_translate("MainWindow", "Side View"))
        self.btnSide.setText(_translate("MainWindow", "..."))
        self.btn3D.setToolTip(_translate("MainWindow", "3D Model"))
        self.btn3D.setText(_translate("MainWindow", "Model"))
        self.chkBxBeam.setToolTip(_translate("MainWindow", "Beam only"))
        self.chkBxBeam.setText(_translate("MainWindow", "Beam"))
        self.chkBxCol.setToolTip(_translate("MainWindow", "Column only"))
        self.chkBxCol.setText(_translate("MainWindow", "Column"))
        self.chkBxFinplate.setToolTip(_translate("MainWindow", "Finplate only"))
        self.chkBxFinplate.setText(_translate("MainWindow", "Fin Plate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuGraphics.setTitle(_translate("MainWindow", "Graphics"))
        self.inputDock.setWindowTitle(_translate("MainWindow", "Input dock"))
        self.txtFy.setPlaceholderText(_translate("MainWindow", "000.0"))
        self.lbl_column.setText(_translate("MainWindow", "<html><head/><body><p>Column section *</p></body></html>"))
        # self.comboConnLoc.setItemText(0, _translate("MainWindow", "Select Connectivity"))
        # self.comboConnLoc.setItemText(1, _translate("MainWindow", "Column flange-Beam web"))
        # self.comboConnLoc.setItemText(2, _translate("MainWindow", "Column web-Beam web"))
        # self.comboConnLoc.setItemText(3, _translate("MainWindow", "Beam-Beam"))
        self.txtFu.setPlaceholderText(_translate("MainWindow", "000.0"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>Connecting members</p></body></html>"))
        # self.label_4.setText(_translate("MainWindow", "<html><head/><body><p>Connectivity *</p></body></html>"))
        self.lbl_fu.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-style:italic;\">f</span><span style=\" font-style:italic; vertical-align:sub;\">u </span>(MPa) * </p></body></html>"))
        self.lbl_fy.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-style:italic;\">f</span><span style=\" vertical-align:sub;\">y </span>(MPa) *</p></body></html>"))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Factored shear load</span></p></body></html>"))
        self.lbl_shear.setText(_translate("MainWindow", "Vert. Shear (kN) *"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Bolt</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Grade *"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p>Diameter (mm) <span style=\" color:#555500;\">*</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "Type *"))
        self.comboDiameter.setItemText(0, _translate("MainWindow", "Diameter of Bolt"))
        self.comboDiameter.setItemText(1, _translate("MainWindow", "12"))
        self.comboDiameter.setItemText(2, _translate("MainWindow", "16"))
        self.comboDiameter.setItemText(3, _translate("MainWindow", "20"))
        self.comboDiameter.setItemText(4, _translate("MainWindow", "24"))
        self.comboDiameter.setItemText(5, _translate("MainWindow", "30"))
        self.comboDiameter.setItemText(6, _translate("MainWindow", "36"))
        self.lbl_width_2.setText(_translate("MainWindow", "Width (mm)"))
        self.label_40.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Plate</span></p></body></html>"))
        self.label_41.setText(_translate("MainWindow", "<html><head/><body><p>Thickness (mm) *</p></body></html>"))
        self.txtPlateLen.setPlaceholderText(_translate("MainWindow", "0"))
        self.lbl_len_2.setText(_translate("MainWindow", "Height (mm)"))
        self.comboPlateThick_2.setItemText(0, _translate("MainWindow", "Select plate thickness"))
        self.comboPlateThick_2.setItemText(1, _translate("MainWindow", "6"))
        self.comboPlateThick_2.setItemText(2, _translate("MainWindow", "8"))
        self.comboPlateThick_2.setItemText(3, _translate("MainWindow", "10"))
        self.comboPlateThick_2.setItemText(4, _translate("MainWindow", "12"))
        self.comboPlateThick_2.setItemText(5, _translate("MainWindow", "14"))
        self.comboPlateThick_2.setItemText(6, _translate("MainWindow", "16"))
        self.comboPlateThick_2.setItemText(7, _translate("MainWindow", "18"))
        self.comboPlateThick_2.setItemText(8, _translate("MainWindow", "20"))
        self.label_42.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Weld</span></p></body></html>"))
        self.label_43.setText(_translate("MainWindow", "<html><head/><body><p>Thickness (mm) *</p></body></html>"))
        self.label_44.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Bolt</span></p></body></html>"))
        self.label_45.setText(_translate("MainWindow", "Shear Capacity (kN)"))
        self.label_46.setText(_translate("MainWindow", "<html><head/><body><p>Bearing Capacity (kN)</p></body></html>"))
        self.labl123_2.setText(_translate("MainWindow", "<html><head/><body><p>Capacity of Bolt (kN)</p></body></html>"))
        self.t_2.setText(_translate("MainWindow", "No. of Bolts"))
        self.label_47.setText(_translate("MainWindow", "Pitch (mm)"))
        self.label_48.setText(_translate("MainWindow", "End Distance (mm)"))
        self.label_49.setText(_translate("MainWindow", "Thickness (mm)"))
        self.label_50.setText(_translate("MainWindow", "Weld Strength (kN/mm)"))
        self.label_51.setText(_translate("MainWindow", "Gauge (mm)"))
        self.label_52.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Weld</span></p></body></html>"))
        self.label_53.setText(_translate("MainWindow", "Edge Distance (mm)"))
        self.label_54.setText(_translate("MainWindow", "Thickness (mm)"))
        self.label_55.setText(_translate("MainWindow", "<html><head/><body><p>Resultant Shear (kN/mm)</p></body></html>"))
        self.label_56.setText(_translate("MainWindow", "External Moment (kNm)"))
        self.label_57.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Plate</span></p></body></html>"))
        self.label_58.setText(_translate("MainWindow", "Moment Capacity (KNm)"))
        self.lbl_col_2.setText(_translate("MainWindow", "No. of Column"))
        self.lbl_row_2.setText(_translate("MainWindow", "No. of Row"))
        self.label_59.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">OUTPUT</span></p></body></html>"))
        self.btnReset_2.setText(_translate("MainWindow", "Reset"))
        self.btnDesign_2.setText(_translate("MainWindow", "Design"))
        self.label_60.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Bolt</span></p></body></html>"))
        self.label_61.setText(_translate("MainWindow", "Shear Capacity (kN)"))
        self.label_62.setText(_translate("MainWindow", "<html><head/><body><p>Bearing Capacity (kN)</p></body></html>"))
        self.labl123_3.setText(_translate("MainWindow", "<html><head/><body><p>Capacity of Bolt (kN)</p></body></html>"))
        self.t_3.setText(_translate("MainWindow", "No. of Bolts"))
        self.label_63.setText(_translate("MainWindow", "Pitch (mm)"))
        self.label_64.setText(_translate("MainWindow", "End Distance (mm)"))
        self.label_65.setText(_translate("MainWindow", "Thickness (mm)"))
        self.label_66.setText(_translate("MainWindow", "Weld Strength (kN/mm)"))
        self.label_67.setText(_translate("MainWindow", "Gauge (mm)"))
        self.label_68.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Weld</span></p></body></html>"))
        self.label_69.setText(_translate("MainWindow", "Edge Distance (mm)"))
        self.label_70.setText(_translate("MainWindow", "Thickness (mm)"))
        self.label_71.setText(_translate("MainWindow", "<html><head/><body><p>Resultant Shear (kN/mm)</p></body></html>"))
        self.label_72.setText(_translate("MainWindow", "External Moment (kNm)"))
        self.label_73.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Plate</span></p></body></html>"))
        self.label_74.setText(_translate("MainWindow", "Moment Capacity (KNm)"))
        self.lbl_col_3.setText(_translate("MainWindow", "No. of Column"))
        self.lbl_row_3.setText(_translate("MainWindow", "No. of Row"))
        self.label_75.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">OUTPUT</span></p></body></html>"))
        self.btnReset_3.setText(_translate("MainWindow", "Reset"))
        self.btnDesign_3.setText(_translate("MainWindow", "Design"))
        self.label_76.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Bolt</span></p></body></html>"))
        self.label_77.setText(_translate("MainWindow", "Shear Capacity (kN)"))
        self.label_78.setText(_translate("MainWindow", "<html><head/><body><p>Bearing Capacity (kN)</p></body></html>"))
        self.labl123_4.setText(_translate("MainWindow", "<html><head/><body><p>Capacity of Bolt (kN)</p></body></html>"))
        self.t_4.setText(_translate("MainWindow", "No. of Bolts"))
        self.label_79.setText(_translate("MainWindow", "Pitch (mm)"))
        self.label_80.setText(_translate("MainWindow", "End Distance (mm)"))
        self.label_81.setText(_translate("MainWindow", "Thickness (mm)"))
        self.label_82.setText(_translate("MainWindow", "Weld Strength (kN/mm)"))
        self.label_83.setText(_translate("MainWindow", "Gauge (mm)"))
        self.label_84.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Weld</span></p></body></html>"))
        self.label_85.setText(_translate("MainWindow", "Edge Distance (mm)"))
        self.label_86.setText(_translate("MainWindow", "Thickness (mm)"))
        self.label_87.setText(_translate("MainWindow", "<html><head/><body><p>Resultant Shear (kN/mm)</p></body></html>"))
        self.label_88.setText(_translate("MainWindow", "External Moment (kNm)"))
        self.label_89.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Plate</span></p></body></html>"))
        self.label_90.setText(_translate("MainWindow", "Moment Capacity (KNm)"))
        self.lbl_col_4.setText(_translate("MainWindow", "No. of Column"))
        self.lbl_row_4.setText(_translate("MainWindow", "No. of Row"))
        self.label_91.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#00007f;\">OUTPUT</span></p></body></html>"))
        self.btnReset_4.setText(_translate("MainWindow", "Reset"))
        self.btnDesign_4.setText(_translate("MainWindow", "Design"))
        self.txtPlateWidth.setPlaceholderText(_translate("MainWindow", "0"))
        self.btn_Reset.setToolTip(_translate("MainWindow", "Alt+R"))
        self.btn_Reset.setText(_translate("MainWindow", "Reset"))
        self.btn_Reset.setShortcut(_translate("MainWindow", "Alt+R"))
        self.btn_Design.setToolTip(_translate("MainWindow", "Alt+D"))
        self.btn_Design.setText(_translate("MainWindow", "Design"))
        self.btn_Design.setShortcut(_translate("MainWindow", "Alt+D"))
        self.comboWldSize.setItemText(0, _translate("MainWindow", "Select weld thickness"))
        self.comboWldSize.setItemText(1, _translate("MainWindow", "3"))
        self.comboWldSize.setItemText(2, _translate("MainWindow", "4"))
        self.comboWldSize.setItemText(3, _translate("MainWindow", "5"))
        self.comboWldSize.setItemText(4, _translate("MainWindow", "6"))
        self.comboWldSize.setItemText(5, _translate("MainWindow", "8"))
        self.comboWldSize.setItemText(6, _translate("MainWindow", "10"))
        self.comboWldSize.setItemText(7, _translate("MainWindow", "12"))
        self.comboWldSize.setItemText(8, _translate("MainWindow", "14"))
        self.comboWldSize.setItemText(9, _translate("MainWindow", "16"))
        self.lbl_beam.setText(_translate("MainWindow", "Beam section *"))
        self.outputDock.setWindowTitle(_translate("MainWindow", "Output dock"))
        self.t_7.setText(_translate("MainWindow", "No. of bolts required"))
        self.label_152.setText(_translate("MainWindow", "Gauge (mm)"))
        self.labl123_7.setText(_translate("MainWindow", "<html><head/><body><p>Capacity of bolt (kN)</p></body></html>"))
        self.label_153.setText(_translate("MainWindow", "End distance (mm)"))
        self.lbl_col_7.setText(_translate("MainWindow", "No. of columns"))
        self.label_154.setText(_translate("MainWindow", "Pitch (mm)"))
        self.lbl_row_7.setText(_translate("MainWindow", "No. of rows"))
        self.label_155.setText(_translate("MainWindow", "Edge distance (mm)"))
        self.label_156.setText(_translate("MainWindow", "Shear capacity (kN)"))
        self.label_157.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Bolt</span></p></body></html>"))
        self.label_158.setText(_translate("MainWindow", "<html><head/><body><p>Bearing capacity (kN)</p></body></html>"))
        self.label_160.setText(_translate("MainWindow", "Moment capacity (kNm)"))
        self.label_161.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Plate</span></p></body></html>"))
        self.label_162.setText(_translate("MainWindow", "<html><head/><body><p>Moment demand (kNm)</p></body></html>"))
        self.label_163.setText(_translate("MainWindow", "<html><head/><body><p>Shear demand (kN/mm)</p></body></html>"))
        self.label_164.setText(_translate("MainWindow", "Weld strength (kN/mm)"))
        self.label_166.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">Weld</span></p></body></html>"))
        self.btn_SaveMessages.setToolTip(_translate("MainWindow", "Save log messages"))
        self.btn_SaveMessages.setText(_translate("MainWindow", "Save messages"))
        self.btn_CreateDesign.setToolTip(_translate("MainWindow", "Create design report"))
        self.btn_CreateDesign.setText(_translate("MainWindow", "Create design report"))
        self.plateHeight.setText(_translate("MainWindow", "Height (mm)"))
        self.label_2.setText(_translate("MainWindow", "Width (mm)"))
        self.label_10.setText(_translate("MainWindow", "Bolt group capacity (kN)"))
        self.actionInput.setText(_translate("MainWindow", "Input"))
        self.actionInput.setToolTip(_translate("MainWindow", "Input browser"))
        self.actionInputwindow.setText(_translate("MainWindow", "inputwindow"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_load_input.setText(_translate("MainWindow", "Load input"))
        self.action_load_input.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.action_save_input.setText(_translate("MainWindow", "Save input"))
        self.action_save_input.setIconText(_translate("MainWindow", "Save input"))
        self.action_save_input.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionPrint.setText(_translate("MainWindow", "Print"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionInput_Browser.setText(_translate("MainWindow", "Input Browser"))
        self.actionOutput_Browser.setText(_translate("MainWindow", "Output Browser"))
        self.actionAbout_Osdag.setText(_translate("MainWindow", "About Osdag"))
        self.actionBeam.setText(_translate("MainWindow", "Beam"))
        self.actionColumn.setText(_translate("MainWindow", "Column"))
        self.actionFinplate.setText(_translate("MainWindow", "Finplate"))
        self.actionBolt.setText(_translate("MainWindow", "Bolt"))
        self.action2D_view.setText(_translate("MainWindow", "2D view"))
        self.actionZoom_in.setText(_translate("MainWindow", "Zoom in"))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out"))
        self.actionPan.setText(_translate("MainWindow", "Pan"))
        self.actionRotate_3D_model.setText(_translate("MainWindow", "Rotate 3D model"))
        self.actionView_2D_on_XY.setText(_translate("MainWindow", "View 2D on XY"))
        self.actionView_2D_on_YZ.setText(_translate("MainWindow", "View 2D on YZ"))
        self.actionView_2D_on_ZX.setText(_translate("MainWindow", "View 2D on ZX"))
        self.actionModel.setText(_translate("MainWindow", "Model"))
        self.actionEnlarge_font_size.setText(_translate("MainWindow", "Font"))
        self.actionReduce_font_size.setText(_translate("MainWindow", "Reduce font size"))
        self.actionSave_3D_model.setText(_translate("MainWindow", "Save 3D model "))
        self.actionSave_3D_model.setShortcut(_translate("MainWindow", "Alt+3"))
        self.actionSave_current_image.setText(_translate("MainWindow", "Save CAD image "))
        self.actionSave_current_image.setShortcut(_translate("MainWindow", "Alt+I"))
        self.actionSave_log_messages.setText(_translate("MainWindow", "Save log messages"))
        self.actionSave_log_messages.setShortcut(_translate("MainWindow", "Alt+M"))
        self.actionCreate_design_report.setText(_translate("MainWindow", "Create design report"))
        self.actionCreate_design_report.setShortcut(_translate("MainWindow", "Alt+C"))
        self.actionQuit_fin_plate_design.setText(_translate("MainWindow", "Quit fin plate design"))
        self.actionSave_Front_View.setText(_translate("MainWindow", "Save front view"))
        self.actionSave_Front_View.setShortcut(_translate("MainWindow", "Alt+Shift+F"))
        self.actionSave_Top_View.setText(_translate("MainWindow", "Save top view"))
        self.actionSave_Top_View.setShortcut(_translate("MainWindow", "Alt+Shift+T"))
        self.actionSave_Side_View.setText(_translate("MainWindow", "Save side view"))
        self.actionSave_Side_View.setShortcut(_translate("MainWindow", "Alt+Shift+S"))
        self.actionChange_bg_color.setText(_translate("MainWindow", "Change bg color"))
        self.actionShow_beam.setText(_translate("MainWindow", "Show beam"))
        self.actionShow_beam.setShortcut(_translate("MainWindow", "Alt+Shift+B"))
        self.actionShow_column.setText(_translate("MainWindow", "Show column"))
        self.actionShow_column.setShortcut(_translate("MainWindow", "Alt+Shift+C"))
        self.actionShow_finplate.setText(_translate("MainWindow", "Show finplate"))
        self.actionShow_finplate.setShortcut(_translate("MainWindow", "Alt+Shift+A"))
        self.actionChange_background.setText(_translate("MainWindow", "Change background"))
        self.actionShow_all.setText(_translate("MainWindow", "Show all"))
        self.actionShow_all.setShortcut(_translate("MainWindow", "Alt+Shift+M"))
        self.actionDesign_examples.setText(_translate("MainWindow", "Design Examples"))
        self.actionSample_Problems.setText(_translate("MainWindow", "Sample Problems"))
        self.actionSample_Tutorials.setText(_translate("MainWindow", "Video Tutorials"))
        self.actionAbout_Osdag_2.setText(_translate("MainWindow", "About Osdag"))
        self.actionOsdag_Manual.setText(_translate("MainWindow", "Osdag Manual"))
        self.actionAsk_Us_a_Question.setText(_translate("MainWindow", "Ask Us a Question"))
        self.actionFAQ.setText(_translate("MainWindow", "FAQ"))
        self.actionDesign_Preferences.setText(_translate("MainWindow", "Design Preferences"))
        self.actionDesign_Preferences.setShortcut(_translate("MainWindow", "Alt+P"))
        self.actionfinPlate_quit.setText(_translate("MainWindow", "Quit"))
        self.actionfinPlate_quit.setShortcut(_translate("MainWindow", "Shift+Q"))
        self.actio_load_input.setText(_translate("MainWindow", "Load input"))
        self.actio_load_input.setShortcut(_translate("MainWindow", "Ctrl+L"))

from . import icons_rc
