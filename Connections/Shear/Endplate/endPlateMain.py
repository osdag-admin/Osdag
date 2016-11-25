'''
Created on 07-May-2015
comment

@author: deepa
'''
from OCC import IGESControl
from OCC import VERSION, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
# from OCC.Display.qtDisplay import qtViewer3d
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from OCC.IFSelect import IFSelect_RetDone
from OCC.Interface import Interface_Static_SetCVal
from OCC.Quantity import Quantity_NOC_RED, Quantity_NOC_BLUE1, Quantity_NOC_SADDLEBROWN
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.StlAPI import StlAPI_Writer
from OCC.TopoDS import topods, TopoDS_Shape
from OCC.gp import gp_Pnt
from PyQt4.QtCore import QString, pyqtSignal
from PyQt4.QtWebKit import *
from PyQt4.Qt import QPrinter, QDialog
import os.path
import subprocess
import pickle
import svgwrite
# import yaml
import icons_rc
import pdfkit
import shutil
from ui_summary_popup import *
from ui_aboutosdag import Ui_HelpOsdag
from ui_tutorial import Ui_Tutorial
from reportGenerator import *
from ui_design_preferences import Ui_ShearDesignPreferences
from ISection import ISection
from ISectionOld import ISectionOld
from bolt import Bolt
from beamWebBeamWebConnectivity import BeamWebBeamWeb
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from colWebBeamWebConnectivity import ColWebBeamWeb
from filletweld import FilletWeld
from endPlateCalc import end_connection
from model import *
from nut import Nut 
from nutBoltPlacement import NutBoltArray
from plate import Plate
from notch import Notch
from ui_endplate import Ui_MainWindow
from utilities import osdag_display_shape
from weld import Weld
from drawing_2D import EndCommonData
from Connections.Shear.common_logic import CommonDesignLogic
from PyQt4 import QtSvg
from Svg_Window import SvgWindow


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


class DesignPreferences(QtGui.QDialog):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_ShearDesignPreferences()
        self.ui.setupUi(self)
        self.main_controller = parent
        self.saved = None
        #self.set_default_para()
        self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        #self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.set_bolthole_clernce)

    def save_designPref_para(self):
        '''
        This routine is responsible for saving all design preferences selected by the user
        '''
        designPref = {}
        designPref["bolt"] = {}
        designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        designPref["bolt"]["bolt_hole_clrnce"] = float(self.ui.txt_boltHoleClearance.text())
        designPref["bolt"]["bolt_fu"] = int(self.ui.txt_boltFu.text())

        designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        designPref["weld"]["typeof_weld"] = weldType
        if weldType == "Shop weld":
            designPref["weld"]["safety_factor"] = float(1.25)
        else:
            designPref["weld"]["safety_factor"] = float(1.5)

        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        if typeOfEdge == "a - Sheared or hand flame cut":
            designPref["detailing"]["min_edgend_dist"] = float(1.7)
        else:
            designPref["detailing"]["min_edgend_dist"] = float(1.5)
        if self.ui.txt_detailingGap.text().isEmpty():

            designPref["detailing"]["gap"] = int(20)
        else:
            designPref["detailing"]["gap"] = int(self.ui.txt_detailingGap.text())

        self.saved = True

        QtGui.QMessageBox.about(self, 'Information', "Preferences saved")

        return designPref

        #self.main_controller.call_designPref(designPref)

    def set_default_para(self):
        '''
        '''
        uiObj = self.main_controller.getuser_inputs()
        boltDia = int(uiObj["Bolt"]["Diameter (mm)"])
        bolt_grade = float(uiObj["Bolt"]["Grade"])
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

        self.ui.combo_weldType.setCurrentIndex(0)
        designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        designPref["weld"]["typeof_weld"] = weldType
        designPref["weld"]["safety_factor"] = float(1.25)

        self.ui.combo_detailingEdgeType.setCurrentIndex(0)
        self.ui.txt_detailingGap.setText(str(20))
        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        designPref["detailing"]["min_edgend_dist"] = float(1.7)
        designPref["detailing"]["gap"] = int(20)
        self.saved = False

        return designPref

    def set_bolthole_clernce(self):
        uiObj = self.main_controller.getuser_inputs()
        boltDia = int(uiObj["Bolt"]["Diameter (mm)"])
        clearance = self.get_clearance(boltDia)
        self.ui.txt_boltHoleClearance.setText(str(clearance))

    def set_boltFu(self):
        uiObj = self.main_controller.getuser_inputs()
        boltGrade = float(uiObj["Bolt"]["Grade"])
        boltfu = str(self.get_boltFu(boltGrade))
        self.ui.txt_boltFu.setText(boltfu)

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
        boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040, 12.9: 1220}
        return boltFu[boltGrade]

    def close_designPref(self):
        self.close()

                        
class MyPopupDialog(QtGui.QDialog):
    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
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

        self.ui.lbl_browse.clear
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', " ", 'Images (*.png *.svg *.jpg)', None, QtGui.QFileDialog.DontUseNativeDialog)

        base = os.path.basename(str(filename))
        lblwidget.setText(base)
        self.desired_location(filename)

        return str(filename)

    def desired_location(self, filename):
        shutil.copyfile(filename, str(self.mainController.folder) + "/images_html/cmpylogoEnd.png")

    def save_user_profile(self):
        input_data = self.get_design_report_inputs()
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Files', str(self.mainController.folder) + "/Profile", '*.txt')

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
        input_summary["Method"] = str(self.ui.comboBox_method.currentText())

        return input_summary

    def use_user_profile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Files', str(self.mainController.folder) + "/Profile", '*.txt')
        if os.path.isfile(filename):
            outfile = open(filename, 'r')
            reportsummary = pickle.load(outfile)
            self.ui.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
            self.ui.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
            self.ui.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
            self.ui.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])

        else:
            pass


class MainController(QtGui.QMainWindow):

    closed = pyqtSignal()

    def __init__(self, folder):

        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.combo_Beam.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())

        self.ui.inputDock.setFixedSize(310, 710)
        self.folder = folder
        self.gradeType = {'Please Select Type':'',
                         'HSFG': [8.8, 10.9],
                         'Black Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        ###################
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convert_col_combo_to_beam)
        ############
        #self.retrieve_prevstate()
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))

        self.ui.btn_front.clicked.connect(lambda: self.call_2d_drawing("Front"))
        self.ui.btn_top.clicked.connect(lambda: self.call_2d_drawing("Top"))
        self.ui.btn_side.clicked.connect(lambda: self.call_2d_drawing("Side"))

        self.ui.btn3D.clicked.connect(lambda: self.call_3d_model(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3d_beam)
        self.ui.chkBxCol.clicked.connect(self.call_3d_column)
        self.ui.chkBxEndplate.clicked.connect(self.call_3d_endplate)

        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
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
        self.ui.actionQuit_end_plate_design.triggered.connect(QtGui.qApp.quit)

        self.ui.actionCreate_design_report_2.triggered.connect(self.create_design_report)
        self.ui.actionSave_log_messages_2.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialog)
        self.ui.actionZoom_in.triggered.connect(self.call_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.call_zoom_out)
        self.ui.actionSave_3D_model.triggered.connect(self.save_3d_cad_images)
        self.ui.actionSave_CAD_image.triggered.connect(self.save_2d_cad_images)
        self.ui.actionSave_front_view.triggered.connect(lambda: self.call_2d_drawing("Front"))
        self.ui.actionSave_side_view.triggered.connect(lambda: self.call_2d_drawing("Side"))
        self.ui.actionSave_top_view.triggered.connect(lambda: self.call_2d_drawing("Top"))
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
        self.ui.txtPlateLen.editingFinished.connect(lambda: self.check_plate_height(self.ui.txtPlateLen))
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)

        # Saving and Restoring the endPlate window state.

        self.retrieve_prevstate()
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

# ************************************** Osdag logo for html***************************************************************************************************
#         self.ui.btn_Design.clicked.connect(self.osdag_header)
        self.ui.btn_CreateDesign.clicked.connect(self.osdag_header)
        self.ui.btn_CreateDesign.clicked.connect(self.create_design_report)  # Saves the create design report

# ************************************ Help button *******************************************************************************
        self.ui.actionAbout_Osdag.triggered.connect(self.open_osdag)
        self.ui.actionVideo_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_Report.triggered.connect(self.sample_report)
        self.ui.actionSample_Problems.triggered.connect(self.sample_problem)

        # Initialising the qtviewer

        from osdagMainSettings import backend_name

        self.display, _ = self.init_display(backend_str=backend_name())
        # self.ui.btnSvgSave.clicked.connect(self.save_3d_cad_images)
        # self.ui.btnSvgSave.clicked.connect(lambda:self.saveTopng(self.display))

        self.connection = "Endplate"
        self.connectivity = None
        self.fuse_model = None
        self.disable_view_buttons()
        self.result_obj = None
        self.uiobj = None
        self.designPrefDialog = DesignPreferences(self)
#         svgWinObj = Svg_window(filename, view)
#         self.svgWinObj = svgWinObj

    def osdag_header(self):
        image_path = "ResourceFiles/Osdag_header.png"
        shutil.copyfile(image_path, str(self.folder) + "/images_html/Osdag_header.png")

    def show_font_dialog(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)

    def show_color_dialog(self):
        col = QtGui.QColorDialog.getColor()
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

    def save_2d_cad_images(self):
        files_types = "PNG (*.png);;JPG (*.jpg);;GIF (*.gif)"
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Export', str(self.folder) + "/untitled.png", files_types)
        filename = str(filename)
        file_extension = filename.split(".")[-1]

        if file_extension == 'png' or file_extension == 'jpg' or file_extension == 'gif':
            self.display.ExportToImage(filename)
            QtGui.QMessageBox.about(self, 'Information', "File saved")

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
        self.ui.menubar.setEnabled(False)

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
        self.ui.menubar.setEnabled(True)

        self.ui.btn_SaveMessages.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)

    def fill_plate_thick_combo(self):
        '''Populates the plate thickness on the basis of beam web thickness and plate thickness check
        '''
        dict_beam_data = self.fetch_beam_param()
        beam_tw = float(dict_beam_data[QString("tw")])
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
            beam_D = float(dict_beam_data[QString('D')])
            col_T = float(dict_column_data[QString('T')])
            col_R1 = float(dict_column_data[QString('R1')])
            beam_T = float(dict_beam_data[QString('T')])
            beam_R1 = float(dict_beam_data[QString('R1')])
            clear_depth = 0.0
            min_plate_height = 0.6 * beam_D
            if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                clear_depth = beam_D - 2 * (beam_T + beam_R1 + 5)
            else:
                clear_depth = beam_D - (col_R1 + col_T + beam_R1 + beam_T + 5)
            if clear_depth < plate_height or min_plate_height > plate_height:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information', "Height of the end plate should be in between %s-%s mm" % (int(min_plate_height), int(clear_depth)))
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
            col_D = float(dict_column_data[QString('D')])
            col_T = float(dict_column_data[QString('T')])
            col_R1 = float(dict_column_data[QString('R1')])
            clear_depth = 0.0
            if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                clear_depth = col_D - 2 * (col_T + col_R1 + 5)

            if clear_depth < plate_width:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information', "Height of the end plate should be less than %s mm" % (int(clear_depth)))
            else:
                self.ui.btn_Design.setDisabled(False)

    def populate_weld_thick_combo(self):
        '''
        Returns the weld thickness on the basis column flange and plate thickness check
        ThickerPart between column Flange and plate thickness again get checked according to the IS 800 Table 21 (Name of the table :Minimum Size of First Rum 
        or of a Single Run Fillet Weld)
        '''
        if self.ui.comboPlateThick_2.currentText() == "Select plate thickness":
            self.ui.comboPlateThick_2.setCurrentIndex(0)
            self.ui.comboWldSize.setCurrentIndex(0)
            return

        else:
            newlist = ["Select weld thickness"]
            weldlist = [3, 4, 5, 6, 8, 10, 12, 16]
            plate_thickness = [6, 8, 10, 12, 14, 16, 18, 20]

            plate_thickness = self.ui.comboPlateThick_2.currentText()
            plate_thick = plate_thickness.toFloat()
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
    
    #   from shearDP branch
    #     def convertColComboToBeam(self):
    #         loc = self.ui.comboConnLoc.currentText()
    #         if loc == "Beam-Beam":
    #             self.ui.lbl_beam.setText(" Secondary beam *")
    #             self.ui.lbl_column.setText("Primary beam *")
    # 
    #             self.ui.chkBxBeam.setText("SBeam")
    #             self.ui.chkBxBeam.setToolTip("Secondary  beam")
    #             self.ui.chkBxCol.setText("PBeam")
    #             self.ui.chkBxCol.setToolTip("Primary beam")
    # 
    #             self.ui.comboColSec.clear()
    #             self.ui.comboColSec.addItems(get_beamcombolist())
    #             self.ui.combo_Beam.setCurrentIndex(0)
    #             self.ui.comboColSec.setCurrentIndex(0)
    # 
    #             self.ui.txtFu.clear()
    #             self.ui.txtFy.clear()
    #             self.ui.txtShear.clear()
    # 
    #             self.ui.comboDiameter.setCurrentIndex(0)
    #             self.ui.comboType.setCurrentIndex((0))
    #             self.ui.comboGrade.setCurrentIndex((0))
    #             self.ui.comboPlateThick_2.setItemText(0, "Select Plate thickness")
    #             self.ui.comboPlateThick_2.setCurrentIndex((0))
    #             self.ui.txtPlateLen.clear()
    #             self.ui.txtPlateWidth.clear()
    #             self.ui.comboWldSize.setItemText(0, "Select weld thickness")
    #             self.ui.comboWldSize.setCurrentIndex((0))
    # 
    #             self.ui.txtShrCapacity.clear()
    #             self.ui.txtbearCapacity.clear()
    #             self.ui.txtBoltCapacity.clear()
    #             self.ui.txtNoBolts.clear()
    #             self.ui.txtboltgrpcapacity.clear()
    #             self.ui.txt_row.clear()
    #             self.ui.txt_col.clear()
    #             self.ui.txtPitch.clear()
    #             self.ui.txtGuage.clear()
    #             self.ui.txtEndDist.clear()
    #             self.ui.txtEdgeDist.clear()
    #             self.ui.txtplate_ht.clear()
    #             self.ui.txtplate_width.clear()
    #             self.ui.txtExtMomnt.clear()
    #             self.ui.txtMomntCapacity.clear()
    #             self.ui.txtResltShr.clear()
    #             self.ui.txtWeldStrng.clear()
    # 
    #         elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":
    # 
    #             self.ui.lbl_column.setText("Column Section *")
    #             self.ui.lbl_beam.setText("Beam section *")
    #             self.ui.chkBxBeam.setText("Beam")
    #             self.ui.chkBxBeam.setToolTip("Beam only")
    #             self.ui.chkBxCol.setText("Column")
    #             self.ui.chkBxCol.setToolTip("Column only")
    #             self.ui.comboColSec.clear()
    #             self.ui.comboColSec.addItems(get_columncombolist())
    #             self.ui.combo_Beam.setCurrentIndex(0)
    #             self.ui.comboColSec.setCurrentIndex(0)
    # 
    #             self.ui.txtFu.clear()
    #             self.ui.txtFy.clear()
    #             self.ui.txtShear.clear()
    # 
    #             self.ui.comboDiameter.setCurrentIndex(0)
    #             self.ui.comboType.setCurrentIndex((0))
    #             self.ui.comboGrade.setCurrentIndex((0))
    #             self.ui.comboPlateThick_2.setItemText(0, "Select Plate thickness")
    #             self.ui.comboPlateThick_2.setCurrentIndex((0))
    #             self.ui.txtPlateLen.clear()
    #             self.ui.txtPlateWidth.clear()
    #             self.ui.comboWldSize.setItemText(0, "Select weld thickness")
    #             self.ui.comboWldSize.setCurrentIndex((0))
    # 
    #             self.ui.txtShrCapacity.clear()
    #             self.ui.txtbearCapacity.clear()
    #             self.ui.txtBoltCapacity.clear()
    #             self.ui.txtNoBolts.clear()
    #             self.ui.txtboltgrpcapacity.clear()
    #             self.ui.txt_row.clear()
    #             self.ui.txt_col.clear()
    #             self.ui.txtPitch.clear()
    #             self.ui.txtGuage.clear()
    #             self.ui.txtEndDist.clear()
    #             self.ui.txtEdgeDist.clear()
    #             self.ui.txtplate_ht.clear()
    #             self.ui.txtplate_width.clear()
    #             #--------------------------------------- self.ui.txtExtMomnt.clear()
    #             #---------------------------------- self.ui.txtMomntCapacity.clear()
    #             self.ui.txtResltShr.clear()
    #             self.ui.txtWeldStrng.clear()
            
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

#   from cnventionalname branch  

    def convert_col_combo_to_beam(self):# 
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.label_9.setText(" Secondary beam *")
            self.ui.label_3.setText("Primary beam *")
 
            self.ui.chkBxBeam.setText("SBeam")
            self.ui.chkBxBeam.setToolTip("Secondary  beam")
            self.ui.chkBxCol.setText("PBeam")
            self.ui.chkBxCol.setToolTip("Primary beam")
 
            self.ui.comboColSec.clear()
            # self.ui.comboColSec.setObjectName("comboSecondaryBeam")
            # self.ui.comboSecondaryBeam.addItems(get_beamcombolist())
            self.ui.comboColSec.addItems(get_beamcombolist())
 
# ------------------------------------------------- user Inputs-----------------------------------------------------------------------------------------
            self.ui.combo_Beam.setCurrentIndex((0))
            self.ui.comboColSec.setCurrentIndex((0))
#             self.ui.comboConnLoc.setCurrentIndex((0))
            self.ui.comboDaimeter.setCurrentIndex(0)
            self.ui.comboType.setCurrentIndex((0))
            self.ui.comboGrade.setCurrentIndex((0))
            self.ui.comboPlateThick_2.setCurrentIndex((0))
            self.ui.comboWldSize.setCurrentIndex((0))
 
            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtPlateLen.clear()
            self.ui.txtPlateWidth.clear()
 
# ----------------------------------------------Output ----------------------------------------------------------------------------------------------------
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
            self.ui.txtWeldStrng_5.clear()
 
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
# ------------------------------------------------- user Inputs-----------------------------------------------------------------------------------------
            self.ui.combo_Beam.setCurrentIndex((0))
            self.ui.comboColSec.setCurrentIndex((0))
#             self.ui.comboConnLoc.setCurrentIndex((0))
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
 
# ----------------------------------------------Output ----------------------------------------------------------------------------------------------------
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
            column = self.ui.comboColSec.currentText()

            dict_beam_data = self.fetch_beam_param()
            dict_col_data = self.fetch_column_param()
            column_D = float(dict_col_data[QString("D")])
            column_T = float(dict_col_data[QString("T")])
            column_R1 = float(dict_col_data[QString("R1")])
            column_web_depth = column_D - 2.0 * (column_T)

            beam_B = float(dict_beam_data[QString("B")])

            if column_web_depth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information', "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)
        elif loc == "Beam-Beam":
            primary_beam = self.ui.comboColSec.currentText()

            dict_sec_beam_data = self.fetch_beam_param()
            dict_pri_beam_data = self.fetch_column_param()
            pri_beam_D = float(dict_pri_beam_data[QString("D")])
            pri_beam_T = float(dict_pri_beam_data[QString("T")])
            pri_beam_web_depth = pri_beam_D - 2.0 * (pri_beam_T)

            sec_beam_D = float(dict_sec_beam_data[QString("D")])

            if pri_beam_web_depth <= sec_beam_D:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information',
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
                self.ui.label_9.setText('Secondary beam *')
                self.ui.label_3.setText('Primary beam *')
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
        Returns the dictionary object with the user input fields for designing End plate connection
        '''
        uiobj = {}
        uiobj["Bolt"] = {}
        uiobj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        uiobj["Bolt"]["Grade"] = float(self.ui.comboGrade.currentText())
        uiobj["Bolt"]["Type"] = str(self.ui.comboType.currentText())

        uiobj["Weld"] = {}
        uiobj["Weld"]['Size (mm)'] = self.ui.comboWldSize.currentText().toInt()[0]

        uiobj['Member'] = {}
        uiobj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        uiobj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiobj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiobj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiobj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]

        uiobj['Plate'] = {}
        uiobj['Plate']['Thickness (mm)'] = self.ui.comboPlateThick_2.currentText().toInt()[0]
        uiobj['Plate']['Height (mm)'] = self.ui.txtPlateLen.text().toInt()[0]  # changes the label length to height
        uiobj['Plate']['Width (mm)'] = self.ui.txtPlateWidth.text().toInt()[0]

        uiobj['Load'] = {}
        uiobj['Load']['ShearForce (kN)'] = self.ui.txtShear.text().toInt()[0]

        return uiobj

    def save_inputs(self, uiobj):
        '''(Dictionary)--> None
        '''
        input_file = QtCore.QFile('Connections/Shear/Endplate/saveINPUT.txt')
        if not input_file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (input_file, file.errorString()))
        # yaml.dump(uiobj, input_file,allow_unicode=True, default_flow_style = False)
        pickle.dump(uiobj, input_file)

    def get_prevstate(self):
        '''
        '''
        filename = 'Connections/Shear/Endplate/saveINPUT.txt'

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
#         outobj['Plate']["Moment Capacity (kN-m)"] = float(self.ui.txtMomntCapacity.text())

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
        self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)

        commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.display, self.folder)
        if view != 'All':
            fileName = QtGui.QFileDialog.getSaveFileName(self,
                                                         "Save SVG", str(self.folder) + '/untitled.svg',
                                                         "SVG files (*.svg)")
            fname = str(fileName)
        else:
            fname = ''
        commLogicObj.call2D_Drawing(view, fname, self.alist[3], self.folder)
        
    def save_design(self, popup_summary):
        filename = self.folder + "/images_html/Html_Report.html"
        filename = str(filename)
        self.call_end2D_drawing("All")
        commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5],
                                         self.alist[6], self.alist[7], self.alist[8], self.display, self.folder)
        commLogicObj.call_designReport(filename, popup_summary)
      
        path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        options = {
                   'margin-bottom': '10mm',
                   'footer-right': '[page]'
        }
        pdfkit.from_file(filename, str(QtGui.QFileDialog.getSaveFileName(self,"Save File As", self.folder + "/", "PDF (*.pdf)")), configuration=config, options=options)
        QtGui.QMessageBox.about(self, 'Information', "Report Saved")

    def save_log(self):

        filename, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/Logmessages", "Text files (*.txt)")
        return self.save_file(filename)

    def save_file(self, filename):
        '''(file open for writing)-> boolean
        '''
        file_name = QtCore.QFile(filename)

        if not file_name.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (filename, file_name.errorString()))
            return False

        outf = QtCore.QTextStream(file_name)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()
        
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
        self.ui.txtExtMomnt.clear()
        self.ui.txtMomntCapacity.clear()

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
            QtGui.QMessageBox.about(self, 'Error', 'Please Enter a value between %s-%s' % (min_val, max_val))
            widget.clear()
            widget.setFocus()
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QtGui.QPalette()
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
        # newly added field
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

        # resultant_shear = result_obj['Weld']['resultantshear']
        # self.ui.txtResltShr.setText(str(resultant_shear))

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
        afile = QtCore.QFile(fname)
        
        if not afile.open(QtCore.QIODevice.ReadOnly):  # ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())

        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscroll_bar = self.ui.textEdit.verticalScrollBar()
        vscroll_bar.setValue(vscroll_bar.maximum())
        afile.close()

    def validate_inputs_on_design_button(self):

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
            
        elif self.ui.comboDiameter.currentIndex() == 0 :
            QtGui.QMessageBox.about(self, "Information", "Please select Diameter of  bolt")

        elif self.ui.comboType.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Type of  bolt")

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
            from PyQt4 import QtCore, QtGui, QtOpenGL
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

        self.setWindowTitle("Osdag Endplate")
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

        def center_on_screen(self):
                    '''Centers the window on the screen.'''
                    resolution = QtGui.QDesktopWidget().screenGeometry()
                    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                              (resolution.height() / 2) - (self.frameSize().height() / 2))

        def start_display():
            self.ui.modelTab.raise_()
            # self.ui.model2dTab.raise_()   # make the application float to the top

        return display, start_display

#     def display_3d_model(self, component):
#         self.display.EraseAll()
#         self.display.SetModeShaded()
#         display.DisableAntiAliasing()
#         # self.display.set_bg_gradient_color(23,1,32,23,1,32)
#         self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
#         self.display.View_Front()
#         self.display.View_Iso()
#         self.display.FitAll()
#         if component == "Column":
#             osdag_display_shape(self.display, self.connectivity.get_column_model(), update=True)
#         elif component == "Beam":
#             osdag_display_shape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM, update=True)
#             # osdag_display_shape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
#         elif component == "Endplate":
#             osdag_display_shape(self.display, self.connectivity.weldModelLeft, color='red', update=True)
#             osdag_display_shape(self.display, self.connectivity.weldModelRight, color='red', update=True)
#             osdag_display_shape(self.display, self.connectivity.plateModel, color='blue', update=True)
#             nutboltlist = self.connectivity.nut_bolt_array.get_model()
# 
#             for nutbolt in nutboltlist:
#                 osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
#             # self.display.DisplayShape(self.connectivity.nut_bolt_array.get_models(), color = Quantity_NOC_SADDLEBROWN, update=True)
#         elif component == "Model":
#             osdag_display_shape(self.display, self.connectivity.columnModel, update=True)
#             osdag_display_shape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM, update=True)
#             osdag_display_shape(self.display, self.connectivity.weldModelLeft, color='red', update=True)
#             osdag_display_shape(self.display, self.connectivity.weldModelRight, color='red', update=True)
#             osdag_display_shape(self.display, self.connectivity.plateModel, color='blue', update=True)
#             nutboltlist = self.connectivity.nut_bolt_array.get_model()
#             for nutbolt in nutboltlist:
#                 osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
#             # self.display.DisplayShape(self.connectivity.nut_bolt_array.get_models(), color = Quantity_NOC_SADDLEBROWN, update=True)

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

    def create_3d_beam_web_beam_web(self):
        '''
        creating 3d cad model with beam web beam web
        '''
        uiobj = self.getuser_inputs()
        result_obj = end_connection(uiobj)

# ###################### PRIMARY BEAM PARAMETERS #########################

        dict_beam_data = self.fetch_column_param()
        pri_beam_D = int(dict_beam_data[QString("D")])
        pBeam_B = int(dict_beam_data[QString("B")])
        pBeam_tw = float(dict_beam_data[QString("tw")])
        pri_beam_T = float(dict_beam_data[QString("T")])
        pBeam_alpha = float(dict_beam_data[QString("FlangeSlope")])
        pBeam_R1 = float(dict_beam_data[QString("R1")])
        pBeam_R2 = float(dict_beam_data[QString("R2")])
        pBeam_length = 800.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B=pBeam_B, T=pri_beam_T, D=pri_beam_D, t=pBeam_tw,
                          R1=pBeam_R1, R2=pBeam_R2, alpha=pBeam_alpha,
                          length=pBeam_length, notch_obj=None)

# ###################### SECONDARY BEAM PARAMETERS ##########################
        dictbeamdata2 = self.fetch_beam_param()

        sec_beam_D = int(dictbeamdata2[QString("D")])
        sBeam_B = int(dictbeamdata2[QString("B")])
        sBeam_tw = float(dictbeamdata2[QString("tw")])
        sBeam_T = float(dictbeamdata2[QString("T")])
        sBeam_alpha = float(dictbeamdata2[QString("FlangeSlope")])
        sBeam_R1 = float(dictbeamdata2[QString("R1")])
        sBeam_R2 = float(dictbeamdata2[QString("R2")])

        # --Notch dimensions
        notch_obj = Notch(R1=pBeam_R1, height=(pri_beam_T + pBeam_R1), width=((pBeam_B - (pBeam_tw + 40)) / 2.0 + 10), length=sBeam_B)
        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B=sBeam_B, T=sBeam_T, D=sec_beam_D,
                        t=sBeam_tw, R1=sBeam_R1, R2=sBeam_R2,
                        alpha=sBeam_alpha, length=500, notch_obj=notch_obj)

# ########################## WELD,PLATE,BOLT AND NUT PARAMETERS ##########################################################

        fillet_length = result_obj['Plate']['Height']
        fillet_thickness = uiobj["Weld"]['Size (mm)']
        plate_width = result_obj['Plate']['Width']
        plate_thick = uiobj['Plate']['Thickness (mm)']
        bolt_dia = uiobj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  #

        # plate = Plate(L= 300,W =100, T = 10)
        plate = Plate(L=fillet_length, W=plate_width, T=plate_thick)

        # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        Fweld1 = FilletWeld(L=fillet_length, b=fillet_thickness, h=fillet_thickness)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = sBeam_tw + plate_thick + nut_T

        nut_bolt_array = NutBoltArray(result_obj, nut, bolt, gap)

        beamwebconn = BeamWebBeamWeb(column, beam, notch_obj, Fweld1, plate, nut_bolt_array)
        beamwebconn.create_3dmodel()

        return beamwebconn

    def create_3d_col_web_beam_web(self):
        '''
        creating 3d cad model with column web beam web
        '''
        uiobj = self.getuser_inputs()
        result_obj = end_connection(uiobj)

        dict_beam_data = self.fetch_beam_param()
        ##################################### BEAM PARAMETERS ##################################################################
        beam_D = int(dict_beam_data[QString("D")])
        beam_B = int(dict_beam_data[QString("B")])
        beam_tw = float(dict_beam_data[QString("tw")])
        beam_T = float(dict_beam_data[QString("T")])
        beam_alpha = float(dict_beam_data[QString("FlangeSlope")])
        beam_R1 = float(dict_beam_data[QString("R1")])
        beam_R2 = float(dict_beam_data[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISectionOld(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                           R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                           length=beam_length)

# ############################################ COLUMN PARAMETERS ########################################################
        dict_col_data = self.fetch_column_param()

        column_D = int(dict_col_data[QString("D")])
        column_B = int(dict_col_data[QString("B")])
        column_tw = float(dict_col_data[QString("tw")])
        column_T = float(dict_col_data[QString("T")])
        column_alpha = float(dict_col_data[QString("FlangeSlope")])
        column_R1 = float(dict_col_data[QString("R1")])
        column_R2 = float(dict_col_data[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISectionOld(B=column_B, T=column_T, D=column_D,
                             t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000)
# ######################################### WELD,PLATE,BOLT AND NUT PARAMETERS ############################################

        fillet_length = result_obj['Plate']['Height']
        fillet_thickness = uiobj["Weld"]['Size (mm)']
        plate_width = result_obj['Plate']['Width']
        plate_thick = uiobj['Plate']['Thickness (mm)']
        bolt_dia = uiobj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150

        # plate = Plate(L= 300,W =100, T = 10)
        plate = Plate(L=fillet_length, W=plate_width, T=plate_thick)

        # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        Fweld1 = FilletWeld(L=fillet_length, b=fillet_thickness, h=fillet_thickness)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)
        gap = column_tw + plate_thick + nut_T

        nut_bolt_array = NutBoltArray(result_obj, nut, bolt, gap)

        colwebconn = ColWebBeamWeb(column, beam, Fweld1, plate, nut_bolt_array)
        colwebconn.create_3dmodel()

        return colwebconn

#     def create_3d_col_flange_beam_web(self):
#         '''
#         Creating 3d cad model with column flange beam web connection
#         '''
#         uiobj = self.getuser_inputs()
#         result_obj = end_connection(uiobj)
# 
#         dict_beam_data = self.fetch_beam_param()
# # ################################# BEAM PARAMETERS ####################################################################
#         beam_D = int(dict_beam_data[QString("D")])
#         beam_B = int(dict_beam_data[QString("B")])
#         beam_tw = float(dict_beam_data[QString("tw")])
#         beam_T = float(dict_beam_data[QString("T")])
#         beam_alpha = float(dict_beam_data[QString("FlangeSlope")])
#         beam_R1 = float(dict_beam_data[QString("R1")])
#         beam_R2 = float(dict_beam_data[QString("R2")])
#         beam_length = 500.0  # This parameter as per view of 3D cad model
# 
#         # beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
#         beam = ISectionOld(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
#                            R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
#                            length=beam_length)
# 
# # ##################### COLUMN PARAMETERS ####################################
#         dict_col_data = self.fetch_column_param()
# 
#         column_D = int(dict_col_data[QString("D")])
#         column_B = int(dict_col_data[QString("B")])
#         column_tw = float(dict_col_data[QString("tw")])
#         column_T = float(dict_col_data[QString("T")])
#         column_alpha = float(dict_col_data[QString("FlangeSlope")])
#         column_R1 = float(dict_col_data[QString("R1")])
#         column_R2 = float(dict_col_data[QString("R2")])
# 
#         # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
#         column = ISectionOld(B=column_B, T=column_T, D=column_D,
#                              t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000)
# # ########################## WELD,PLATE,BOLT AND NUT PARAMETERS #########################################################
# 
#         fillet_length = result_obj['Plate']['Height']
#         fillet_thickness = uiobj["Weld"]['Size (mm)']
#         plate_width = result_obj['Plate']['Width']
#         plate_thick = uiobj['Plate']['Thickness (mm)']
#         bolt_dia = uiobj["Bolt"]["Diameter (mm)"]
#         bolt_r = bolt_dia / 2
#         bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
#         # bolt_R = bolt_r + 7
#         nut_R = bolt_R
#         bolt_T = self.bolt_head_thick_calculation(bolt_dia)
#         # bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
#         bolt_Ht = self.bolt_length_calculation(bolt_dia)
#         # bolt_Ht =100.0 # minimum bolt length as per Indian Standard
#         nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
#         # nut_T = 12.0 # minimum nut thickness As per Indian Standard
#         nut_Ht = 12.2  #
# 
#         # plate = Plate(L= 300,W =100, T = 10)
#         plate = Plate(L=fillet_length, W=plate_width, T=plate_thick)
# 
#         # Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
#         Fweld1 = FilletWeld(L=fillet_length, b=fillet_thickness, h=fillet_thickness)
# 
#         # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
#         bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)
# 
#         # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
#         nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)
# 
#         gap = column_tw + plate_thick + nut_T
# 
#         nut_bolt_array = NutBoltArray(result_obj, nut, bolt, gap)
# 
#         colflangeconn = ColFlangeBeamWeb(column, beam, Fweld1, plate, nut_bolt_array)
#         colflangeconn.create_3dmodel()
#         return colflangeconn
# 
#     def call_3d_model(self, flag):
# #         self.ui.btnSvgSave.setEnabled(True)
#         self.ui.btn3D.setChecked(QtCore.Qt.Checked)
#         if self.ui.btn3D.isChecked():
#             self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
#             self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
#             self.ui.chkBxEndplate.setChecked(QtCore.Qt.Unchecked)
#             self.ui.mytabWidget.setCurrentIndex(0)
# 
#         if flag is True:
#             if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
#                 # self.create_3d_col_web_beam_web()
#                 self.connectivity = self.create_3d_col_web_beam_web()
#                 self.fuse_model = None
#             elif self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
#                 self.ui.mytabWidget.setCurrentIndex(0)
#                 self.connectivity = self.create_3d_col_flange_beam_web()
#                 self.fuse_model = None
#             else:
#                 self.ui.mytabWidget.setCurrentIndex(0)
#                 self.connectivity = self.create_3d_beam_web_beam_web()
#                 self.fuse_model = None
# 
#             self.display_3d_model("Model")
#             # beamOrigin = self.connectivity.beam.secOrigin + self.connectivity.beam.t/2 * (-self.connectivity.beam.uDir)
#             # gpBeamOrigin = getGpPt(beamOrigin)
#             # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
#             # self.display.DisplayShape(my_sphere2,color = 'red',update = True)
#             # beamOrigin = self.connectivity.beam.secOrigin
#             # gpBeamOrigin = getGpPt(beamOrigin)
#             # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
#             # self.display.DisplayShape(my_sphere2,color = 'blue',update = True)
#             # plateOrigin =  (self.connectivity.plate.secOrigin + self.connectivity.plate.T/2.0 *(self.connectivity.plate.uDir)+ self.connectivity.weldLeft.L/2.0
#             #                 * (self.connectivity.plate.vDir) + self.connectivity.plate.T * (-self.connectivity.weldLeft.uDir))
#             # gpPntplateOrigin=  getGpPt(plateOrigin)
#             # my_sphere = BRepPrimAPI_MakeSphere(gpPntplateOrigin,2).Shape()
#             # self.display.DisplayShape(my_sphere,update=True)
# 
#         else:
#             self.display.EraseAll()
#             # self.display.DisplayMessage(gp_Pnt(1000,0,400),"Sorry, can not create 3D model",height = 23.0)

    def call_3d_beam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxEndplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display_3d_model("Beam")

    def call_3d_column(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxEndplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.display_3d_model("Column")

    def call_3d_endplate(self):
        '''Displaying EndPlate in 3D
        '''
        self.ui.chkBxEndplate.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxEndplate.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display_3d_model("Endplate")

    def unchecked_all_checkbox(self):

        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxEndplate.setChecked(QtCore.Qt.Unchecked)
    
    def call_designPref(self, designPref):
        self.uiobj = self.getuser_inputs()
        
        print"printing designpreferences",self.uiobj
        print designPref
        
    def designParameters(self):
        '''
        This routine returns the neccessary design parameters.
        '''
        self.uiobj = self.getuser_inputs()
        if self.designPrefDialog.saved is not True:
            design_pref = self.designPrefDialog.set_default_para()
        else:
            design_pref = self.designPrefDialog.save_designPref_para()
        self.uiobj.update(design_pref)
        print "printing designprefernces from endPlate", self.uiobj

        dictbeamdata = self.fetch_beam_param()
        dictcoldata = self.fetch_column_param()
        loc = str(self.ui.comboConnLoc.currentText())
        component = "Model"
        bolt_dia = self.uiobj["Bolt"]["Diameter (mm)"]
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        return [self.uiobj, dictbeamdata, dictcoldata, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T]

    def design_btnclicked(self):
        '''
        '''
        self.alist = self.designParameters()

        self.validate_inputs_on_design_button()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enable_view_buttons()
        self.unchecked_all_checkbox()
        connection = "Endplate"

        self.commLogicObj = CommonDesignLogic(self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4], self.alist[5], self.alist[6], self.alist[7], self.alist[8], self.display, self.folder,connection)

        self.result_obj = self.commLogicObj.call_finCalculation()
        d = self.result_obj[self.result_obj.keys()[0]]
        if len(str(d[d.keys()[0]])) == 0:
            self.ui.btn_CreateDesign.setEnabled(False)
        self.display_output(self.result_obj)
        self.displaylog_totextedit(self.commLogicObj)
        status = self.result_obj['Bolt']['status']

        self.commLogicObj.call_3DModel(status)
        
    def create_2d_cad(self, connectivity):
        ''' Returns the fuse model of endplate
        '''
        cadlist = self.connectivity.get_models()
        final_model = cadlist[0]
        for model in cadlist[1:]:
            final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        return final_model

    # Export to IGS,STEP,STL,BREP
    def save_3d_cad_images(self):
        if self.connectivity is None:
            self.connectivity = self.create_3d_col_web_beam_web()
        if self.fuse_model is None:
            self.fuse_model = self.create_2d_cad(self.connectivity)
        shape = self.fuse_model

        files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Export', str(self.folder) + "/untitled.igs", files_types)

        filename = str(filename)
        file_extension = filename.split(".")[-1]

        if file_extension == 'igs':
            IGESControl.IGESControl_Controller().Init()
            iges_writer = IGESControl.IGESControl_Writer()
            iges_writer.AddShape(shape)
            iges_writer.Write(filename)

        elif file_extension == 'brep':

            BRepTools.breptools.Write(shape, filename)

        elif file_extension == 'stp':
            # initialize the STEP exporter
            step_writer = STEPControl_Writer()
            Interface_Static_SetCVal("write.step.schema", "AP203")

            # transfer shapes and write file
            step_writer.Transfer(shape, STEPControl_AsIs)
            status = step_writer.Write(filename)

            assert(status == IFSelect_RetDone)

        else:
            stl_writer = StlAPI_Writer()
            stl_writer.SetASCIIMode(True)
            stl_writer.Write(shape, filename)

        QtGui.QMessageBox.about(self, 'Information', "File saved")

    def display_2d_model_original(self, final_model, view_name):

        self.display, _ = self.init_display()
        self.display.EraseAll()
        # self.display.SetModeWireFrame()

        self.display.DisplayShape(final_model, update=True)
        self.display.SetModeHLR()

        if (view_name == "Front"):
            self.display.View_Front()
        elif (view_name == "Top"):
            self.display.View_Top()
        elif (view_name == "Right"):
            self.display.View_Right()
        else:
            pass
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#     def call_desired_view(self, filename, view, base_front, base_top, base_side):
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def call_desired_view(self, filename, view):
        self. unchecked_all_checkbox()

        uiobj = self.getuser_inputs()
        result_obj = end_connection(uiobj)
        dict_beam_data = self.fetch_beam_param()
        dict_col_data = self.fetch_column_param()
        end_common_obj = EndCommonData(uiobj, result_obj, dict_beam_data, dict_col_data, self.folder)
        end_common_obj.save_to_svg(filename, view)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         base_front, base_top, base_side = end_common_obj.save_to_svg(str(filename), view, base_front, base_top, base_side)
#         return (base_front, base_top, base_side)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def call_2d_drawing(self, view):

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite pacage which takes design INPUT and OUTPUT parameters from Endplate GUI.
        '''
        self.ui.chkBxEndplate.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         base = ''
#         base_front = ''
#         base_side = ''
#         base_top = ''
#         loc = self.ui.comboConnLoc.currentText()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if view == "All":
            filename = ''
            self.call_desired_view(filename, view)
            self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
            data = str(self.folder) + "/images_html/3D_Model.png"
            self.display.ExportToImage(data)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#             base1, base2, base3 = self.call_desired_view(filename, view, base_front, base_top, base_side)
#             for n in range(1, 5, 1):
#                 if (os.path.exists(data)):
#                     data = str(self.folder) + "/images_html/3D_Model" + '(' + str(n) + ')' + ".png"
#                     continue
#             base = os.path.basename(str(data))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        else:
#             self.go_to_open_svg(view)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for opening the window %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            if view == "Front":
                filename = self.folder + "/images_html/endFront.svg"

            elif view == "Side":
                filename = self.folder + "/images_html/endSide.svg"

            else:
                filename = self.folder + "/images_html/endTop.svg"

            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, self.folder)
            # self.save_2d_image_names(view)
#             return self.svgWinObj.call_svgwindow(filename, view)
#             self.svgWidget.setWindowTitle('2D View')
#             self.svgWidget.show()
# #             self.btn_save.clicked.connect(self.save_2d_image_names(view))
# #             self.save_2d_image_names(view)
#             sys.exit(app.exec_())
#         return self.open_new(view)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#             base1, base2, base3 = self.call_desired_view(filename, view, base_front, base_top, base_side)
#         return (base, base1, base2, base3)


#     def open_new(self, view):
#         self.btn_save.clicked.connect(self.save_2d_image_names)
#         return self.save_2d_image_names(view)

#     def save_2d_image_names(self, view):
# #         view = self.go_to_open_svg(view)
#         self.btn_save.clicked.connect(view)
#
#         if view == "Front":
#             png_image_path = self.folder + "/images_html/endFront.png"
#             shutil.copyfile(png_image_path, str(QtGui.QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", "PNG (*.png)")))
#         elif view == "Side":
#             png_image_path = self.folder + "/images_html/endSide.png"
#             shutil.copyfile(png_image_path, str(QtGui.QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", "PNG (*.png)")))
#         else:
#             png_image_path = self.folder + "/images_html/endTop.png"
#             shutil.copyfile(png_image_path, str(QtGui.QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", "PNG (*.png)")))
#
#         QtGui.QMessageBox.about(self, 'Information', "Image Saved")


#     def save_2d_image_names(self, filename, view):
#         filename = filename
#         f = open(filename, 'w')
#         f.write(self.call_desired_view(filename, view))
#         print "saving only imagesssss", filename
#         f.close()

    def closeEvent(self, event):
        '''
        Closing endPlate window.
        '''
        ui_input = self.getuser_inputs()
        self.save_inputs(ui_input)
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

        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Report')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform =="nt":
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

    def sample_problem(self):
        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Problems')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                if sys.platform =="nt":
                    os.startfile("%s/%s" % (root_path, pdf_file))
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, pdf_file)])

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
    fh = logging.FileHandler("Connections/Shear/Endplate/fin.log", mode="a")

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
    fh = logging.FileHandler("Connections/Shear/Endplate/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Endplate/log.css"/>''')

    # app = QtGui.QApplication(sys.argv)
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
#     fh = logging.FileHandler("fin.log", mode="w")
    fh = logging.FileHandler("Connections/Shear/Endplate/fin.log", mode="w")
#     "Connections/Shear/Finplate/fin.log"
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/Endplate/log.css"/>''')
# "Connections/Shear/Finplate/log.css

    app = QtGui.QApplication(sys.argv)
    module_setup()
    window = MainController()
    window.show()
    sys.exit(app.exec_())
