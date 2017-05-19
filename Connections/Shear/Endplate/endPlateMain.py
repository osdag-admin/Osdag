'''
Created on 07-May-2015
comment

@author: deepa
'''
import json

from PyQt5.QtCore import QFile,pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator,QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget,QDialog, QMessageBox, QFontDialog, QApplication, QFileDialog, QColorDialog, qApp
from OCC import IGESControl
from OCC import BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.IFSelect import IFSelect_RetDone
from OCC.Interface import Interface_Static_SetCVal
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.StlAPI import StlAPI_Writer
import os.path
import subprocess
import pickle
import icons_rc
import pdfkit
import shutil
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_AboutOsdag
from ui_tutorial import Ui_Tutorial
from ui_ask_question import  Ui_AskQuestion
# from ui_ask_a_question import Ui_AskQuestion
from reportGenerator import *
from ui_design_preferences import Ui_ShearDesignPreferences
from endPlateCalc import end_connection
from model import *
from ui_endplate import Ui_MainWindow
from drawing_2D import EndCommonData
from Connections.Shear.common_logic import CommonDesignLogic
# from Connections.Shear.common_logic import CommonDesignLogic
#from Connections.Shear.commonlogic import CommonDesignLogic
from Svg_Window import SvgWindow


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
        self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.set_bolthole_clernce)

    def save_designPref_para(self):
        '''
        This routine is responsible for saving all design preferences selected by the user
        '''
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_clrnce"] = float(self.ui.txt_boltHoleClearance.text())
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
        self.saved_designPref["weld"]["weld_fu"] = str(self.ui.txt_weldFu.text())

        self.saved_designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        self.saved_designPref["detailing"]["typeof_edge"] = typeOfEdge
        if typeOfEdge == "a - Sheared or hand flame cut":
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.7)
        else:
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.5)
        # if self.ui.txt_detailingGap.text() == '':
        #
        #     designPref["detailing"]["gap"] = int(20)
        # else:
        #     designPref["detailing"]["gap"] = int(self.ui.txt_detailingGap.text())
        self.saved_designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())
        self.saved_designPref["detailing"]["gap"] = int(20)

        self.saved_designPref["design"] = {}
        self.saved_designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())

        self.saved = True

        QMessageBox.about(self, 'Information', "Preferences saved")

        return self.saved_designPref

        #self.main_controller.call_designPref(designPref)

    def set_default_para(self):
        '''
        '''
        uiObj = self.main_controller.getuser_inputs()

        # if uiObj ["Bolt"]["Diameter (mm)"] == 'Diameter of Bolt':
        #     pass
        # else:
        #     boltDia = str(uiObj["Bolt"]["Diameter (mm)"])
        #     clearance = str(self.get_clearance(boltDia))
        #     self.ui.txt_boltHoleClearance.setText(clearance)
        # if uiObj ["Bolt"]["Grade"] == '':
        #     pass
        # else:
        #     bolt_grade = float(uiObj["Bolt"]["Grade"])
        #     bolt_fu = str(self.get_boltFu(bolt_grade))
        #     self.ui.txt_boltFu.setText(bolt_fu)

        boltDia = str(uiObj["Bolt"]["Diameter (mm)"])
        bolt_grade = (uiObj["Bolt"]["Grade"])
        clearance = str(self.get_clearance(boltDia))
        bolt_fu = str(self.get_boltFu(bolt_grade))

        self.ui.combo_boltHoleType.setCurrentIndex(0)
        self.ui.txt_boltHoleClearance.setText(clearance)
        self.ui.txt_boltFu.setText(bolt_fu)
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
        #self.ui.txt_detailingGap.setText(str(20))
        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        if typeOfEdge == "a - Sheared or hand flame cut":
            designPref["detailing"]["min_edgend_dist"] = float(1.7)
        else:
            designPref["detailing"]["min_edgend_dist"] = float(1.5)
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
            clearance = self.get_clearance(boltDia)
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
            clearance = standard_clrnce[float(str(boltDia))]
        else:
            clearance = overhead_clrnce[boltDia]
        
        return clearance

    def get_boltFu(self, boltGrade):
        '''
        This routine returns ultimate strength of bolt depending upon grade of bolt chosen
        '''
        boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040, 12.9: 1220}
        return boltFu[float(boltGrade)]

    def close_designPref(self):
        self.close()

                        
class MyPopupDialog(QDialog):
    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.mainController = parent
        self.setWindowTitle("Design Profile")
        self.ui.btn_browse.clicked.connect(lambda: self.get_logo_file_path(self.ui.lbl_browse))
        self.ui.btn_saveProfile.clicked.connect(self.save_user_profile)
        self.ui.btn_useProfile.clicked.connect(self.use_user_profile)
        self.accepted.connect(self.save_input_summary)

    def save_input_summary(self):
        input_summary = self.get_design_report_inputs()
        self.mainController.save_design(input_summary)
        # return input_summary

    def get_logo_file_path(self, lblwidget):

        self.ui.lbl_browse.clear()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', " ", 'Images (*.png *.svg *.jpg)', None, QFileDialog.DontUseNativeDialog)
        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

        return str(filename)

    def desired_location(self, filename):
        shutil.copyfile(filename, os.path.join(str(self.mainController.folder), "images_html", "cmpylogoEnd.png"))

    def save_user_profile(self):
        input_data = self.get_design_report_inputs()
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Files', os.path.join(str(self.mainController.folder), "Profile"), '*.txt')

        infile = open(filename, 'w')
        pickle.dump(input_data, infile)
        infile.close()

    def get_design_report_inputs(self):

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

    def use_user_profile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Files', os.path.join(str(self.mainController.folder), "Profile"), '*.txt')
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

        self.get_columndata()
        self.get_beamdata()

        self.ui.inputDock.setFixedSize(310, 710)
        self.folder = folder


        self.gradeType = {'Please Select Type':'',
                         'HSFG': [8.8, 10.9],
                         'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 10.9, 12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()
        ###################
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convert_col_combo_to_beam)
        ############
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        self.ui.btn_front.clicked.connect(lambda: self.callend2D_Drawing("Front"))
        self.ui.btn_top.clicked.connect(lambda: self.callend2D_Drawing("Top"))
        self.ui.btn_side.clicked.connect(lambda: self.callend2D_Drawing("Side"))

        self.ui.btn3D.clicked.connect(lambda: self.call_3d_model(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3d_beam)
        self.ui.chkBxCol.clicked.connect(self.call_3d_column)
        self.ui.chkBxEndplate.clicked.connect(self.call_3d_endplate)

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

        min_fu = 290
        max_fu = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu, self.ui.lbl_fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy, self.ui.lbl_fy, min_fy, max_fy))

        ##### MenuBar #####
        self.ui.actionQuit_end_plate_design.setShortcut('Ctrl+Q')
        self.ui.actionQuit_end_plate_design.setStatusTip('Exit application')
        self.ui.actionQuit_end_plate_design.triggered.connect(qApp.quit)

        self.ui.actionCreate_design_report_2.triggered.connect(self.create_design_report)
        self.ui.actionSave_log_messages_2.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialog)
        self.ui.actionZoom_in.triggered.connect(self.call_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.call_zoom_out)
        self.ui.actionSave_3D_model.triggered.connect(self.save_3d_cad_images)
        self.ui.actionSave_CAD_image.triggered.connect(self.save_cadImages)
        self.ui.actionSave_front_view.triggered.connect(lambda: self.callend2D_Drawing("Front"))
        self.ui.actionSave_side_view.triggered.connect(lambda: self.callend2D_Drawing("Side"))
        self.ui.actionSave_top_view.triggered.connect(lambda: self.callend2D_Drawing("Top"))
        self.ui.actionSave_design.triggered.connect(self.saveDesign_inputs)
        self.ui.actionOpen_design.triggered.connect(self.openDesign_inputs)
        self.ui.actionPan.triggered.connect(self.call_panning)

        self.ui.actionShow_beam.triggered.connect(self.call_3d_beam)
        self.ui.actionShow_column.triggered.connect(self.call_3d_column)
        self.ui.actionShoe_end_plate.triggered.connect(self.call_3d_endplate)
        self.ui.actionShow_all.triggered.connect(lambda: self.call_3d_model(True))
        self.ui.actionChange_background.triggered.connect(self.show_color_dialog)

        # self.ui.combo_Beam.addItems(get_beamcombolist())
        # self.ui.comboColSec.addItems(get_columncombolist())

        self.ui.combo_Beam.currentIndexChanged[int].connect(lambda: self.fill_plate_thick_combo())
        self.ui.combo_Beam.currentIndexChanged[str].connect(self.checkbeam_b)
        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkbeam_b)
        self.ui.comboPlateThick_2.currentIndexChanged[int].connect(lambda: self.populate_weld_thick_combo())
        self.ui.comboDiameter.currentIndexChanged[str].connect(self.bolt_hole_clearace)
        self.ui.comboGrade.currentIndexChanged[str].connect(self.call_boltFu)
        self.ui.txtPlateLen.editingFinished.connect(lambda: self.check_plate_height(self.ui.txtPlateLen))
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)

        # Saving and Restoring the endPlate window state.

        #self.retrieve_prevstate()
        self.designPrefDialog = DesignPreferences(self)
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

        self.ui.btn_CreateDesign.clicked.connect(self.osdag_header)
        self.ui.btn_CreateDesign.clicked.connect(self.create_design_report)  # Saves the create design report

        # ************************************ Help button *******************************************************************************
        self.ui.actionAbout_Osdag_2.triggered.connect(self.open_osdag)
        self.ui.actionVideo_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_Report.triggered.connect(self.sample_report)
        self.ui.actionSample_Problems.triggered.connect(self.sample_problem)
        self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_question)

        self.ui.actionDesign_Preferences.triggered.connect(self.design_preferences)
        # Initialising the qtviewer

        from osdagMainSettings import backend_name

        self.display, _ = self.init_display(backend_str=backend_name())

        self.connection = "Endplate"
        self.connectivity = None
        self.fuse_model = None
        self.disable_view_buttons()
        self.result_obj = None
        self.uiobj = None
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
        for col in old_section:
            if col in intg_section:
                indx = intg_section.index(str(col))
                combo_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)


    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join( "ResourceFiles", "Osdag_header.png")))
        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

    def show_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)

    def show_color_dialog(self):
        col = QColorDialog.getColor()
        color_tuple = col.getRgb()
        r = color_tuple[0]
        g = color_tuple[1]
        b = color_tuple[2]
        self.display.set_bg_gradient_color(r, g, b, 255, 255, 255)

    def call_zoom_in(self):
        self.display.ZoomFactor(2)

    def call_zoom_out(self):
        self.display.ZoomFactor(0.5)

    def call_rotation(self):
        self.display.Rotation(15, 0)

    def call_panning(self):
        self.display.Pan(50, 0)

    def save_cadImages(self):

        files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
        fileName,_ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"), files_types)
        fName = str(fileName)
        file_extension = fName.split(".")[-1]

        if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp'or file_extension == 'tiff' :
            self.display.ExportToImage(fName)
            QMessageBox.about(self, 'Information', "File saved")


    def disable_view_buttons(self):
        '''
        Disables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(False)
        self.ui.btn_top.setEnabled(False)
        self.ui.btn_side.setEnabled(False)

        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.chkBxEndplate.setEnabled(False)
        # self.ui.menubar.setEnabled(False)
        self.ui.menuFile.setEnabled(False)
        self.ui.menuEdit.setEnabled(False)
        self.ui.menuView.setEnabled(False)
        self.ui.menuGraphics.setEnabled(False)

        self.ui.btn_SaveMessages.setEnabled(False)
        self.ui.btn_CreateDesign.setEnabled(False)

    def enable_view_buttons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn_side.setEnabled(True)

        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxEndplate.setEnabled(True)
        # self.ui.menubar.setEnabled(True)
        self.ui.menuFile.setEnabled(True)
        self.ui.menuEdit.setEnabled(True)
        self.ui.menuView.setEnabled(True)
        self.ui.menuGraphics.setEnabled(True)

        self.ui.btn_SaveMessages.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)

    def fill_plate_thick_combo(self):
        '''Populates the plate thickness on the basis of beam web thickness and plate thickness check
        '''
        print" combo_beam text:", self.ui.combo_Beam.currentText()
        if str(self.ui.combo_Beam.currentText()) == 'Select section':
            return
        dict_beam_data = self.fetch_beam_param()
        beam_tw = float(dict_beam_data["tw"])
        plate_thickness = [6, 8, 10, 12, 14, 16, 18, 20]
        newlist = ['Select plate thickness']
        for ele in plate_thickness[1:]:
            item = int(ele)
            if item >= beam_tw:
                newlist.append(str(item))
        self.ui.comboPlateThick_2.clear()
        for i in newlist[:]:
            self.ui.comboPlateThick_2.addItem(str(i))
        self.ui.comboPlateThick_2.setCurrentIndex(1)

    def check_plate_height(self, widget):
        loc = self.ui.comboConnLoc.currentText()
        plate_height = widget.text()
        plate_height = float(plate_height)
        if plate_height == 0:
            self.ui.btn_Design.setDisabled(False)
        else:

            dict_beam_data = self.fetch_beam_param()
            dict_column_data = self.fetch_column_param()
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
                clear_depth = beam_D - (col_R1 + col_T + beam_R1 + beam_T + 5)
            if clear_depth < plate_height or min_plate_height > plate_height:
                self.ui.btn_Design.setDisabled(True)
                QMessageBox.about(self, 'Information', "Height of the end plate should be in between %s-%s mm" % (int(min_plate_height), int(clear_depth)))
            else:
                self.ui.btn_Design.setDisabled(False)

    def check_plate_width(self, widget):
        loc = self.ui.comboConnLoc.currentText()
        plate_width = widget.text()
        plate_width = float(plate_width)
        if plate_width == 0:
            self.ui.btn_Design.setDisabled(False)
        else:

            dict_column_data = self.fetch_column_param()
            col_D = float(dict_column_data['D'])
            col_T = float(dict_column_data['T'])
            col_R1 = float(dict_column_data['R1'])
            clear_depth = 0.0
            if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                clear_depth = col_D - 2 * (col_T + col_R1 + 5)

            if clear_depth < plate_width:
                self.ui.btn_Design.setDisabled(True)
                QMessageBox.about(self, 'Information', "Height of the end plate should be less than %s mm" % (int(clear_depth)))
            else:
                self.ui.btn_Design.setDisabled(False)

    def populate_weld_thick_combo(self):
        '''
        Returns the weld thickness on the basis column flange and plate thickness check
        ThickerPart between column Flange and plate thickness again get checked according to the IS 800 Table 21 (Name of the table :Minimum Size of First Rum 
        or of a Single Run Fillet Weld)
        '''
        if str(self.ui.comboPlateThick_2.currentText()) == "Select plate thickness":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return

        else:
            newlist = ["Select weld thickness"]
            weldlist = [3, 4, 5, 6, 8, 10, 12, 16]
            plate_thickness = [6, 8, 10, 12, 14, 16, 18, 20]

            plate_thickness = self.ui.comboPlateThick_2.currentText()
            plate_thick = plate_thickness
            if plate_thick <= 10:

                for i in weldlist[:]:
                    newlist.append(str(i))
            elif plate_thick <= 20 and plate_thick > 10:

                for i in weldlist[2:]:
                    newlist.append(str(i))
            elif plate_thick <= 32 and plate_thick > 20:

                for i in weldlist[3:]:
                    newlist.append(str(i))
            else:

                for i in weldlist[5:]:
                    newlist.append(str(i))

            self.ui.comboWldSize.clear()
            for element in newlist[:]:
                self.ui.comboWldSize.addItem(str(element))
    
    def fetch_beam_param(self):
        beam_sec = self.ui.combo_Beam.currentText()
        dict_beam_data = get_beamdata(beam_sec)
        return dict_beam_data

    def fetch_column_param(self):
        column_sec = self.ui.comboColSec.currentText()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            dict_col_data = get_beamdata(column_sec)
        else:
            dict_col_data = get_columndata(column_sec)
        return dict_col_data


    def convert_col_combo_to_beam(self):# 
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.lbl_beam.setText(" Secondary beam *")
            self.ui.lbl_column.setText("Primary beam *")
 
            self.ui.chkBxBeam.setText("SBeam")
            self.ui.chkBxBeam.setToolTip("Secondary  beam")
            self.ui.chkBxCol.setText("PBeam")
            self.ui.chkBxCol.setToolTip("Primary beam")
 
            self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_beamcombolist())
 
            self.ui.combo_Beam.setCurrentIndex((0))
            self.ui.comboColSec.setCurrentIndex((0))
            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboType.setCurrentIndex((0))
            self.ui.comboGrade.setCurrentIndex((0))
            self.ui.comboPlateThick_2.setCurrentIndex((0))
            self.ui.comboWldSize.setCurrentIndex((0))
 
            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtPlateLen.clear()
            self.ui.txtPlateWidth.clear()
 
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
            self.ui.combo_Beam.setCurrentIndex((0))
            self.ui.comboColSec.setCurrentIndex((0))
            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboType.setCurrentIndex((0))
            self.ui.comboGrade.setCurrentIndex((0))
            self.ui.comboPlateThick_2.setCurrentIndex((0))
            self.ui.comboWldSize.setCurrentIndex((0))
 
            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtPlateLen.clear()
            self.ui.txtPlateWidth.clear()
 
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
            self.ui.txtResltShr.clear()
            self.ui.txtWeldStrng.clear()
            self.ui.txtWeld_length.clear()

    def checkbeam_b(self):
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web":

            if self.ui.combo_Beam.currentText()== "Select section" or self.ui.comboColSec.currentIndex() == -1 or self.ui.comboColSec.currentText()=='Select section':
                return
            dict_beam_data = self.fetch_beam_param()
            dict_col_data = self.fetch_column_param()
            column_D = float(dict_col_data["D"])
            column_T = float(dict_col_data["T"])
            column_R1 = float(dict_col_data["R1"])
            column_web_depth = column_D - 2.0 * (column_T)

            beam_B = float(dict_beam_data["B"])

            if column_web_depth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                QMessageBox.about(self, 'Information', "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)
        elif loc == "Beam-Beam":

            if self.ui.comboColSec.currentIndex() == -1 or self.ui.comboColSec.currentIndex() == 0 or self.ui.combo_Beam.currentIndex() == 0:
                return

            dict_sec_beam_data = self.fetch_beam_param()
            dict_pri_beam_data = self.fetch_column_param()
            pri_beam_D = float(dict_pri_beam_data["D"])
            pri_beam_T = float(dict_pri_beam_data["T"])
            pri_beam_web_depth = pri_beam_D - 2.0 * (pri_beam_T)

            sec_beam_D = float(dict_sec_beam_data["D"])

            if pri_beam_web_depth <= sec_beam_D:
                self.ui.btn_Design.setDisabled(True)
                QMessageBox.about(self, 'Information',
                                        "Secondary beam depth is higher than clear depth of primary beam web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)

         
    def retrieve_prevstate(self):
        '''
        This routine is responsible for maintaining previous session's  data
        '''
        uiObj = self.get_prevstate()
        self.setDictToUserInputs(uiObj)
    
    
    def setDictToUserInputs(self,uiobj):
        if(uiobj is not None):
            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiobj['Member']['Connectivity'])))

            if uiobj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.lbl_beam.setText('Secondary beam *')
                self.ui.lbl_column.setText('Primary beam *')
                self.ui.comboColSec.addItems(get_beamcombolist())

            self.ui.combo_Beam.setCurrentIndex(self.ui.combo_Beam.findText(uiobj['Member']['BeamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiobj['Member']['ColumSection']))

            self.ui.txtFu.setText(str(uiobj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(uiobj['Member']['fy (MPa)']))

            self.ui.txtShear.setText(str(uiobj['Load']['ShearForce (kN)']))

            self.ui.comboDiameter.setCurrentIndex(self.ui.comboDiameter.findText(str(uiobj['Bolt']['Diameter (mm)'])))
            combo_type_index = self.ui.comboType.findText(str(uiobj['Bolt']['Type']))
            self.ui.comboType.setCurrentIndex(combo_type_index)
            self.combotype_currentindexchanged(str(uiobj['Bolt']['Type']))

            prevValue = str(uiobj['Bolt']['Grade'])

            combo_grade_index = self.ui.comboGrade.findText(prevValue)

            self.ui.comboGrade.setCurrentIndex(combo_grade_index)

            selection = str(uiobj['Plate']['Thickness (mm)'])
            selection_index = self.ui.comboPlateThick_2.findText(selection)
            self.ui.comboPlateThick_2.setCurrentIndex(selection_index)
            self.ui.txtPlateLen.setText(str(uiobj['Plate']['Height (mm)']))
            self.ui.txtPlateWidth.setText(str(uiobj['Plate']['Width (mm)']))

            self.ui.comboWldSize.setCurrentIndex(self.ui.comboWldSize.findText(str(uiobj['Weld']['Size (mm)'])))


    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web":

            pixmap = QPixmap(":/newPrefix/images/colF2.png")
            pixmap.scaledToHeight(60)
            pixmap.scaledToWidth(50)
            self.ui.lbl_connectivity.setPixmap(pixmap)
        elif(loc == "Column web-Beam web"):
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
        '''(nothing) -> Dictionary
        Returns the dictionary object with the user input fields for designing End plate connection
        '''
        uiobj = {}
        uiobj["Bolt"] = {}
        uiobj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText()
        uiobj["Bolt"]["Grade"] = (self.ui.comboGrade.currentText())
        uiobj["Bolt"]["Type"] = str(self.ui.comboType.currentText())

        uiobj["Weld"] = {}
        uiobj["Weld"]['Size (mm)'] = str(self.ui.comboWldSize.currentText())

        uiobj['Member'] = {}
        uiobj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        uiobj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiobj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiobj['Member']['fu (MPa)'] = self.ui.txtFu.text()
        uiobj['Member']['fy (MPa)'] = self.ui.txtFy.text()

        uiobj['Plate'] = {}
        uiobj['Plate']['Thickness (mm)'] = str(self.ui.comboPlateThick_2.currentText())
        uiobj['Plate']['Height (mm)'] = str(self.ui.txtPlateLen.text())  # changes the label length to height
        uiobj['Plate']['Width (mm)'] = str(self.ui.txtPlateWidth.text())

        uiobj['Load'] = {}
        uiobj['Load']['ShearForce (kN)'] = self.ui.txtShear.text()

        return uiobj

    def saveDesign_inputs(self):

        fileName,_ = QFileDialog.getSaveFileName(self,"Save Design", os.path.join(str(self.folder), "untitled.osi"),"Input Files(*.osi)")
        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                          "There was an error opening \"%s\"" % fileName)
            return

        # yaml.dump(self.uiObj,out_file,allow_unicode=True, default_flow_style=False)
        json.dump(self.uiobj, out_file)

        out_file.close()

    def openDesign_inputs(self):

        fileName,_ = QFileDialog.getOpenFileName(self, "Open Design", str(self.folder), "All Files(*)")
        if not fileName:
            return
        try:
            in_file = open(str(fileName), 'rb')

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                          "There was an error opening \"%s\"" % fileName)
            return

        uiobj = json.load(in_file)
        self.setDictToUserInputs(uiobj)

    def save_inputs(self, uiobj):
        '''(Dictionary)--> None
        '''
        input_file = QFile(os.path.join("Connections", "Shear", "Endplate", "saveINPUT.txt"))
        if not input_file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (input_file, file.errorString()))
        pickle.dump(uiobj, input_file)

    def get_prevstate(self):
        '''
        '''
        filename = os.path.join("Connections", "Shear", "Endplate", "saveINPUT.txt")

        if os.path.isfile(filename):
            file_object = open(filename, 'r')
            uiobj = pickle.load(file_object)
            return uiobj
        else:
            return None

    def outputdict(self):
        ''' Returns the output of design in dictionary object.
        '''
        outobj = {}
        outobj['Plate'] = {}
        outobj['Plate']["Height(mm)"] = float(self.ui.txtplate_ht.text())
        outobj['Plate']["Width(mm)"] = float(self.ui.txtplate_width.text())

        outobj['Weld'] = {}
        outobj['Weld']["Weld Length(mm)"] = float(self.ui.txtWeldStrng_5.text())
        outobj['Weld']["Resultant Shear (kN/mm)"] = float(self.ui.txtResltShr.text())
        outobj['Weld']["Weld Strength (kN/mm)"] = float(self.ui.txtWeldStrng.text())

        outobj['Bolt'] = {}
        outobj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txtShrCapacity.text())
        outobj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txtbearCapacity.text())
        outobj['Bolt']["Capacity Of Bolt (kN)"] = float(self.ui.txtBoltCapacity.text())
        outobj['Bolt']["No Of Bolts"] = float(self.ui.txtNoBolts.text())
        outobj['Bolt']["No.Of Row"] = float(self.ui.txt_row.text())
        outobj['Bolt']["No.Of Column"] = int(self.ui.txt_col.text())
        outobj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txtPitch.text())
        outobj['Bolt']["Guage Distance (mm)"] = float(self.ui.txtGuage.text())
        outobj['Bolt']["End Distance (mm)"] = float(self.ui.txtEndDist.text())
        outobj['Bolt']["Edge Distance (mm)"] = float(self.ui.txtEdgeDist.text())

        return outobj

    def show_dialog(self):

        dialog = MyPopupDialog(self)
        dialog.show()

    def create_design_report(self, report_index):

        self.show_dialog()

    def call_end2D_drawing(self, view):  # call2D_Drawing(self,view)

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.btn3D.setChecked(Qt.Unchecked)

        if view != 'All':

            if view == "Front":
                filename = os.path.join(self.folder, "images_html", "endFront.svg")

            elif view == "Side":
                filename = os.path.join(self.folder, "images_html", "endSide.svg")

            else:
                filename = os.path.join(self.folder, "images_html", "endTop.svg")

            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, self.folder)

        else:
            fname = ''
            self.commLogicObj.call2D_Drawing(view, fname,  self.folder)
        
    def save_design(self, popup_summary):
        filename = os.path.join(self.folder, "images_html", "Html_Report.html")
        filename = str(filename)
        self.call_end2D_drawing("All")

        self.commLogicObj.call_designReport(filename, popup_summary)

        if sys.platform == ("win32" or "win64"):
            path_wkthmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        else:
            #path_wkthmltopdf = r'/usr/bin/wkhtmltopdf'
            path_wkthmltopdf = r'/home/deepa-c/miniconda2/pkgs/wkhtmltopdf-0.12.3-0/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        options = {
                   'margin-bottom': '10mm',
                   'footer-right': '[page]'
        }
        file_type = "PDF (*.pdf)"
        fname, _ = QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", file_type)
        pdfkit.from_file(filename, fname, configuration=config, options=options)

        #pdfkit.from_file(filename, str(QFileDialog.getSaveFileName(self,"Save File As", self.folder + "/", "PDF (*.pdf)")), configuration=config, options=options)
        QMessageBox.about(self, 'Information', "Report Saved")

    def save_log(self):

        fileName, pat = QFileDialog.getSaveFileName(self, "Save File As",
                                                    os.path.join(str(self.folder), "LogMessages"),
                                                    "Text files (*.txt)")
        return self.save_file(fileName + ".txt")

        if filename == "":
            return

    def save_file(self, filename):
        '''(file open for writing)-> boolean
        '''
        file_name = QFile(filename)

        if not file_name.open(QFile.WriteOnly | QFile.Text):
            return False

        outf = QTextStream(file_name)
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

        # ----------------------- Output ----------------------------------------------------------------------------------
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
        # self.ui.txtExtMomnt.clear()
        # self.ui.txtMomntCapacity.clear()

        # self.ui.txtWeldThick.clear()
        self.ui.txtResltShr.clear()
        self.ui.txtWeldStrng.clear()
        self.ui.textEdit.clear()

        # ------------------------------------ Erase Display -----------------------------------------------------------------
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

        self.ui.comboGrade.clear()
        str_items = []
        for val in items:
            str_items.append(str(val))

        self.ui.comboGrade.addItems(str_items)

    def check_range(self, widget, lblwidget, min_val, max_val):

        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        text_str = widget.text()
        val = int(text_str)
        if(val < min_val or val > max_val):
            QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s' % (min_val, max_val))
            widget.clear()
            widget.setFocus()
            palette = QPalette()
            palette.setColor(QPalette.Foreground, Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QPalette()
            lblwidget.setPalette(palette)

    def display_output(self, output_obj):
        '''(dictionary) --> NoneType
        Setting design result values to the respective textboxes in the output window
        '''
        for k in output_obj.keys():
            for key in output_obj[k].keys():
                if (output_obj[k][key] == ""):
                    result_obj = output_obj
                else:
                    result_obj = output_obj

        # result_obj['Bolt']
        shear_capacity = result_obj['Bolt']['shearcapacity']
        self.ui.txtShrCapacity.setText(str(shear_capacity))

        bearing_capacity = result_obj['Bolt']['bearingcapacity']
        self.ui.txtbearCapacity.setText(str(bearing_capacity))

        bolt_capacity = result_obj['Bolt']['boltcapacity']
        self.ui.txtBoltCapacity.setText(str(bolt_capacity))

        no_ofbolts = result_obj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        
        bolt_grp_capacity = result_obj['Bolt']['boltgrpcapacity']
        self.ui.txtboltgrpcapacity.setText(str(bolt_grp_capacity))

        no_ofrows = result_obj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))

        no_ofcol = result_obj['Bolt']['numofcol']
        self.ui.txt_col.setText(str(no_ofcol))

        pitch_dist = result_obj['Bolt']['pitch']
        self.ui.txtPitch.setText(str(pitch_dist))

        gauge_dist = result_obj['Bolt']['gauge']
        self.ui.txtGuage.setText(str(gauge_dist))

        end_dist = result_obj['Bolt']['enddist']
        self.ui.txtEndDist.setText(str(end_dist))

        edge_dist = result_obj['Bolt']['edge']
        self.ui.txtEdgeDist.setText(str(edge_dist))

        weld_strength = result_obj['Weld']['weldstrength']
        self.ui.txtWeldStrng.setText(str(weld_strength))

        weld_shear = result_obj['Weld']['weldshear']
        self.ui.txtResltShr.setText(str(weld_shear))

        weld_length = result_obj['Weld']['weldlength']
        self.ui.txtWeld_length.setText(str(weld_length))

        # Newly included fields
        plate_ht = result_obj['Plate']['height']
        self.ui.txtplate_ht.setText(str(plate_ht))

        plate_width = result_obj['Plate']['width']
        self.ui.txtplate_width.setText(str(plate_width))
        

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
        vscroll_bar = self.ui.textEdit.verticalScrollBar()
        vscroll_bar.setValue(vscroll_bar.maximum())
        afile.close()

    def validate_inputs_on_design_button(self):

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

        if self.ui.txtFu.text() == ' ' or float(self.ui.txtFu.text()) == 0:
            QMessageBox.about(self, "Information", "Please select Ultimate strength of  steel")

        elif self.ui.txtFy.text() == ' ' or float(self.ui.txtFy.text()) == 0:
            QMessageBox.about(self, "Information", "Please select Yeild  strength of  steel")

        elif self.ui.txtShear.text() == ' ' or float(str(self.ui.txtShear.text())) == 0:
            QMessageBox.about(self, "Information", "Please select Factored shear load")
            
        elif self.ui.comboDiameter.currentIndex() == 0 :
            QMessageBox.about(self, "Information", "Please select Diameter of  bolt")

        elif self.ui.comboType.currentIndex() == 0:
            QMessageBox.about(self, "Information", "Please select Type of  bolt")

    # QtViewer
    def init_display(self, backend_str=None, size=(1024, 768)):

        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)

        # if os.name == 'nt':
        #
        #     global display, start_display, app, _
        #
        #     from OCC.Display.backend import get_loaded_backend
        #     lodedbkend = get_loaded_backend()
        #     from OCC.Display.backend import get_backend, have_backend
        #     from osdagMainSettings import backend_name
        #     if (not have_backend() and backend_name() == "pyqt5"):
        #         get_backend("qt-pyqt5")
        # else:

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        # from OCC.Display.pyqt4Display import qtViewer3d
        from OCC.Display.qtDisplay import qtViewer3d
        self.ui.modelTab = qtViewer3d(self)

        # self.setWindowTitle("Osdag-%s 3d viewer ('%s' backend)" % (VERSION, backend_name()))
        self.setWindowTitle("Osdag Endplate")
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





        # if os.name == 'nt':
        #
        #     global display, start_display, app, _
        #
        #     from OCC.Display.backend import get_backend, have_backend
        #     from osdagMainSettings import backend_name
        #     if(not have_backend() and backend_name() == "pyqt5"):
        #         get_backend("qt-pyqt5")
        #
        # else:
        #     global display, start_display, app, _, USED_BACKEND
        #
        #     if not backend_str:
        #         USED_BACKEND = self.get_backend()
        #     elif backend_str in ['pyside', 'pyqt5']:
        #         USED_BACKEND = backend_str
        #     else:
        #         raise ValueError("You should pass either 'qt' or 'tkinter' to the init_display function.")
        #         sys.exit(1)
        #
        #     # Qt based simple GUI
        #     if USED_BACKEND in ['pyqt4', 'pyside']:
        #         if USED_BACKEND == 'pyqt4':
        #             import OCC.Display.pyqt4Display
        #             from OCC.Display.qtDisplay import qtViewer3d
        #             #from PyQt4 import QtCore, QtGui, QtOpenGL
        #
        # from OCC.Display.qtDisplay import qtViewer3d
        #
        # self.ui.modelTab = qtViewer3d(self)
        #
        #
        # self.setWindowTitle("Osdag Endplate")
        # self.ui.mytabWidget.resize(size[0], size[1])
        # self.ui.mytabWidget.addTab(self.ui.modelTab, "")
        #
        # self.ui.modelTab.InitDriver()
        # display = self.ui.modelTab._display
        #
        # # background gradient
        # display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        # # display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        # # display black trihedron
        # display.display_trihedron()
        # display.View.SetProj(1, 1, 1)
        #
        # def center_on_screen(self):
        #             '''Centers the window on the screen.'''
        #             resolution = QDesktopWidget().screenGeometry()
        #             self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        #                       (resolution.height() / 2) - (self.frameSize().height() / 2))
        #
        # def start_display():
        #     self.ui.modelTab.raise_()
        #     # self.ui.model2dTab.raise_()   # make the application float to the top
        #
        # return display, start_display


# #################################################################################################################################################

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

    
    def call_3d_model(self, flag):
        self.ui.btn3D.setChecked(Qt.Checked)
        if self.ui.btn3D.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.commLogicObj.display_3DModel("Model")
        
    def call_3d_beam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam")

    def call_3d_column(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column")

    def call_3d_endplate(self):
        '''Displaying EndPlate in 3D
        '''
        self.ui.chkBxEndplate.setChecked(Qt.Checked)
        if self.ui.chkBxEndplate.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Plate")

    def unchecked_all_checkbox(self):

        self.ui.btn3D.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
    
    def call_designPref(self, designPref):
        self.uiobj = self.getuser_inputs()
        
    def designParameters(self):
        '''
        This routine returns the neccessary design parameters.
        '''
        # self.designPrefDialog.saved = False
        self.uiobj = self.getuser_inputs()
        if self.designPrefDialog.saved is not True:
            design_pref = self.designPrefDialog.set_default_para()
        else:
            design_pref = self.designPrefDialog.saved_designPref
        self.uiobj.update(design_pref)

        dictbeamdata = self.fetch_beam_param()
        dictcoldata = self.fetch_column_param()
        dict_angle_data = {}
        dict_topangle_data = {}
        loc = str(self.ui.comboConnLoc.currentText())
        component = "Model"
        bolt_dia = int(self.uiobj["Bolt"]["Diameter (mm)"])
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        return [self.uiobj, dictbeamdata, dictcoldata, dict_angle_data, dict_topangle_data, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T]

    def design_btnclicked(self):
        """

        Returns:

        """
        self.display.EraseAll()
        self.alist = self.designParameters()
        print "design preference printing", self.alist[0]

        self.validate_inputs_on_design_button()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enable_view_buttons()
        self.unchecked_all_checkbox()
        connection = "Endplate"

        self.commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3],
                                              self.alist[4], self.alist[5], self.alist[6], self.alist[7],
                                              self.alist[8], self.alist[9],self.alist[10], self.display,
                                              self.folder,connection)

        self.resultObj = self.commLogicObj.resultObj
        alist = self.resultObj.values()

        self.displaylog_totextedit(self.commLogicObj)
        self.display_output(self.resultObj)
        isempty = [True if val != '' else False for ele in alist for val in ele.values()]
        if isempty[0] == True:
            status = self.resultObj['Bolt']['status']
            self.commLogicObj.call_3DModel(status)
            self.callend2D_Drawing("All")
        else:
            pass
            # self.display.EraseAll()


    def create2Dcad(self):
        ''' Returns the 3D model of finplate depending upon component
        '''
        if self.commLogicObj.component == "Beam":
            final_model = self.commLogicObj.connectivityObj.get_beamModel()

        elif self.commLogicObj.component == "Column":
            final_model = self.commLogicObj.connectivityObj.get_column_model()

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
        
    # def create_2d_cad(self, connectivity):
    #     ''' Returns the fuse model of endplate
    #     '''
    #     cadlist = self.connectivity.get_models()
    #     final_model = cadlist[0]
    #     for model in cadlist[1:]:
    #         final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
    #     return final_model

    # Export to IGS,STEP,STL,BREP
    def save_3d_cad_images(self):

        if self.fuse_model is None:
            self.fuse_model = self.create2Dcad()
        shape = self.fuse_model

        files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"

        fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"), files_types)
        fName = str(fileName)

        # if self.connectivity is None:
        #     self.connectivity = self.create_3d_col_web_beam_web()
        # if self.fuse_model is None:
        #     self.fuse_model = self.create_2d_cad(self.connectivity)
        # shape = self.fuse_model
        #
        # files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"
        # filename = QFileDialog.getSaveFileName(self, 'Export', str(self.folder) + "/untitled.igs", files_types)
        #
        # filename = str(filename)

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

        self.fuse_model = None
        QMessageBox.about(self, 'Information', "File saved")


    def call_desired_view(self, filename, view):
        self. unchecked_all_checkbox()

        uiobj = self.getuser_inputs()
        result_obj = end_connection(uiobj)
        dict_beam_data = self.fetch_beam_param()
        dict_col_data = self.fetch_column_param()
        end_common_obj = EndCommonData(uiobj, result_obj, dict_beam_data, dict_col_data, self.folder)
        end_common_obj.save_to_svg(filename, view)

    def callend2D_Drawing(self, view):  # call2D_Drawing(self,view)

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from Finplate GUI.
        '''
        self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.btn3D.setChecked(Qt.Unchecked)


        if view != 'All':

            if view == "Front":
                filename = os.path.join(self.folder, "images_html", "endFront.svg")

            elif view == "Side":
                filename = os.path.join(self.folder, "images_html",  "endSide.svg")

            else:
                filename = os.path.join(self.folder, "images_html", "endTop.svg")

            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, self.folder)

        else:
            fname = ''
            self.commLogicObj.call2D_Drawing(view, fname, self.folder)

    # def call_2d_drawing(self, view):
    #
    #     ''' This routine saves the 2D SVG image as per the connectivity selected
    #     SVG image created through svgwrite pacage which takes design INPUT and OUTPUT parameters from Endplate GUI.
    #     '''
    #     self.ui.chkBxEndplate.setChecked(Qt.Unchecked)
    #     self.ui.chkBxBeam.setChecked(Qt.Unchecked)
    #     self.ui.chkBxCol.setChecked(Qt.Unchecked)
    #     self.ui.btn3D.setChecked(Qt.Unchecked)
    #
    #     if view == "All":
    #         filename = ''
    #         self.call_desired_view(filename, view)
    #         self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
    #         data = os.path.join(str(self.folder), "images_html", "3D_Model.png")
    #         self.display.ExportToImage(data)
    #
    #     else:
    #
    #         if view == "Front":
    #             filename = os.path.join(self.folder, "images_html", "endFront.svg")
    #
    #         elif view == "Side":
    #             filename = os.path.join(self.folder, "images_html", "endSide.svg")
    #
    #         else:
    #             filename = os.path.join(self.folder, "images_html", "endTop.svg")
    #
    #         svg_file = SvgWindow()
    #         svg_file.call_svgwindow(filename, view, self.folder)

    def closeEvent(self, event):
        '''
        Closing endPlate window.
        '''
        ui_input = self.getuser_inputs()
        self.save_inputs(ui_input)
        reply = QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
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
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def sample_problem(self):
        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Problems')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform == ("win32" or "win64"):
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

# ********************************************************************************************************************************************************
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
    fh = logging.FileHandler("Connections/Shear/Endplate/end.log", mode="a")

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


def launch_endplate_controller(osdag_main_window, folder):
    set_osdaglogger()
    raw_logger = logging.getLogger("raw")
    raw_logger.setLevel(logging.INFO)
    fh = logging.FileHandler("Connections/Shear/Endplate/end.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Endplate/log.css"/>''')

    # app = QApplication(sys.argv)
    module_setup()
#     web = QWebView()
    window = MainController(folder)
    osdag_main_window.hide()

    window.show()
    window.closed.connect(osdag_main_window.show)

    # sys.exit(app.exec_())


if __name__ == '__main__':
    # launchFinPlateController(None)

    # linking css to log file to display colour logs.
    set_osdaglogger()
    raw_logger = logging.getLogger("raw")
    raw_logger.setLevel(logging.INFO)
    fh = logging.FileHandler("Connections/Shear/Endplate/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Endplate/log.css"/>''')

    app = QApplication(sys.argv)
    module_setup()
    # workspace_folder_path, _ = QFileDialog.getSaveFileName(caption='Select Workspace Directory', directory="F:\Osdag_workspace")
    workspace_folder_path = "Z:\Osdag_workspace\end_plate"
    if not os.path.exists(workspace_folder_path):
        os.mkdir(workspace_folder_path, 0755)
    image_folder_path = os.path.join(workspace_folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0755)
    window = MainController(workspace_folder_path)
    window.show()
    sys.exit(app.exec_())
