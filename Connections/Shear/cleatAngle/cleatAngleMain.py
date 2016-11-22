'''
Created on 07-May-2015
comment

@author: aravind
'''
from getpass import getuser
import os.path
import pickle

from OCC import IGESControl
from OCC import VERSION, BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from OCC.IFSelect import IFSelect_RetDone
from OCC.Interface import Interface_Static_SetCVal
from OCC.Quantity import Quantity_NOC_RED, Quantity_NOC_BLUE1, Quantity_NOC_SADDLEBROWN
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.StlAPI import StlAPI_Writer
from OCC.TopoDS import topods, TopoDS_Shape
from OCC.gp import gp_Pnt
from PyQt4.Qt import QPrinter, QDialog
from PyQt4.QtCore import QString, pyqtSignal
from PyQt4.QtGui import QWidget
from PyQt4.QtWebKit import *
import pdfkit
import svgwrite
import shutil
from ui_cleatAngle import Ui_MainWindow
from ISection import ISection
# from OCC.Display.qtDisplay import qtViewer3d
from angle import Angle
from beamWebBeamWebConnectivity import BeamWebBeamWeb
from bolt import Bolt
from cleatCalculation import cleat_connection
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from colWebBeamWebConnectivity import ColWebBeamWeb
from reportGenerator import *
from drawing2D import *
from model import *
from notch import Notch
from nut import Nut
from nutBoltPlacement import NutBoltArray
from ui_popUpWindow import Ui_Capacitydetals
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_HelpOsdag
from ui_tutorial import Ui_Tutorial
from utilities import osdag_display_shape
from Svg_Window import SvgWindow
from OCC.Display import OCCViewer
# from OCC.Display.backend import get_qt_modules
from macpath import basename
# from OCC.Display.backend import get_backend
# get_backend("qt-pyqt4")
# import OCC.Display.qtDisplay
# QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

# import OCC.Display.qtDisplay
# from Connections.Shear.cleatAngle.ui_popUpWindow import Ui_Capacitydetals
# Developed by aravind


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

    def desired_location(self, filename):
        shutil.copyfile(filename, str(self.mainController.folder) + "/images_html/cmpylogoCleat.png")

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
        files_types = "All Files (*))"
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


class myDialog(QtGui.QDialog):
# (Ui_Capacitydetals):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Capacitydetals()
        self.ui.setupUi(self)
        self.setWindowTitle("Capacity Details")
        self.mainController = parent
        # web = QWebView()
        # ui_obj = self.MainController().getuser_inputs()
        ui_obj = self.mainController.getuser_inputs()
        x = cleat_connection(ui_obj)
        # x = MainController().outputdict()
        # x = m.outputdict()

        self.ui.shear_b.setText(str(x['Bolt']['shearcapacity']))
        self.ui.bearing_b.setText(str(x['Bolt']['bearingcapacity']))
        self.ui.capacity_b.setText(str(x['Bolt']['boltcapacity']))
        self.ui.boltGrp_b.setText(str(x['Bolt']['boltgrpcapacity']))
        # Column
        self.ui.shear.setText(str(x['cleat']['shearcapacity']))
        self.ui.bearing.setText(str(x['cleat']['bearingcapacity']))
        self.ui.capacity.setText(str(x['cleat']['boltcapacity']))
        self.ui.boltGrp.setText(str(x['cleat']['boltgrpcapacity']))
        # Cleat
        self.ui.mDemand.setText(str(x['cleat']['externalmoment']))
        self.ui.mCapacity.setText(str(x['cleat']['momentcapacity']))


class MainController(QtGui.QMainWindow):

    closed = pyqtSignal()

    def __init__(self, folder):
        QtGui.QMainWindow.__init__(self)
#         QtGui.QDialog.__init__(self, parent)
#         self.web = web
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder

        self.ui.combo_Beam.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())
        self.ui.comboCleatSection.addItems(get_anglecombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Select Bolt Type': '',
                          'HSFG': [8.8, 10.8],
                          'Black Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 9.8, 12.9]}
        self.ui.comboBoltType.addItems(self.gradeType.keys())
        self.ui.comboBoltType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboBoltType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()
        # Adding GUI changes for beam to beam connection
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convert_col_combo_to_beam)
        #############################################################################################################
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        # self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock)) #USE WHEN ui_cleatAngle.py is used(btnOutput = toolButton)

        self.ui.toolButton.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.btn_front.clicked.connect(lambda: self.call_2d_drawing("Front"))
        self.ui.btn_top.clicked.connect(lambda: self.call_2d_drawing("Top"))
        self.ui.btn_side.clicked.connect(lambda: self.call_2d_drawing("Side"))

        self.ui.btn3D.clicked.connect(lambda: self.call_3d_model(True))
        self.ui.chkBxBeam.clicked.connect(self.call_3d_beam)
        self.ui.chkBxCol.clicked.connect(self.call_3d_column)
        # self.ui.chkBxFinplate.clicked.connect(self.call_3d_cleatangle)
        self.ui.checkBoxCleat.clicked.connect(self.call_3d_cleatangle)

        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)

        dbl_validator = QtGui.QDoubleValidator()
        self.ui.txtInputCleatHeight.setValidator(dbl_validator)
        self.ui.txtInputCleatHeight.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)

        min_fu = 290
        max_fu = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu, self.ui.lbl_fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy, self.ui.lbl_fy, min_fy, max_fy))

        self.ui.actionCreate_design_report.triggered.connect(self.create_design_report)
        self.ui.actionSave_log_message.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialog)
        self.ui.actionZoom_in.triggered.connect(self.call_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.call_zoom_out)
        self.ui.actionSave_3D_model_as.triggered.connect(self.save_3d_cad_images)
        self.ui.actionSave_CAD_image.triggered.connect(self.save_2d_cad_images)
        self.ui.actionSave_Front_View.triggered.connect(lambda: self.call_2d_drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.call_2d_drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.call_2d_drawing("Top"))
        self.ui.actionPan.triggered.connect(self.call_panning)

        self.ui.actionShow_beam.triggered.connect(self.call_3d_beam)
        self.ui.actionShow_column.triggered.connect(self.call_3d_column)
        self.ui.actionShow_cleat_angle.triggered.connect(self.call_3d_cleatangle)
        self.ui.actionShow_all.triggered.connect(lambda: self.call_3d_model(True))
        self.ui.actionChange_background.triggered.connect(self.show_color_dialog)
        # ############################## MARCH_14 #############################
        # populate cleat section and secondary beam according to user input

        self.ui.comboColSec.currentIndexChanged[int].connect(lambda: self.fill_cleatsection_combo())
        self.ui.combo_Beam.currentIndexChanged[str].connect(self.checkbeam_b)
        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkbeam_b)
#         self.ui.txtInputCleatHeight.currentText.connect(self.check_cleat_height())
#         cleatHeight = self.ui.txtInputCleatHeight.currentText()
#         if cleatHeight != 0:
#             self.
        self.ui.txtInputCleatHeight.editingFinished.connect(lambda: self.check_cleat_height(self.ui.txtInputCleatHeight))

        ######################################################################################
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.create_design_report)  # Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        #################################################################
        self.ui.btn_capacity.clicked.connect(self.show_button_clicked)
        # self.ui.actionCreate_design_report.triggered.connect(self.create_design_report)

        #################################################################
        # Saving and Restoring the finPlate window state.
        # self.retrieve_prevstate()
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

# ************************************** Osdag logo for html***************************************************************************************************
        self.ui.btn_Design.clicked.connect(self.osdag_header)

# ************************************ Help button *******************************************************************************
        self.ui.actionAbout_Osdag.triggered.connect(self.open_osdag)
        self.ui.actionVideo_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionSample_Reports.triggered.connect(self.sample_report)
        self.ui.actionSample_Problems.triggered.connect(self.sample_problem)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        self.connectivity = None
        self.fuse_model = None
        self.disable_view_buttons()
        self.result_obj = None
        self.ui_obj = None

    def osdag_header(self):
        image_path = "ResourceFiles/Osdag_header.png"
        self.store_osdagheader(image_path)

    def store_osdagheader(self, image_path):
        shutil.copyfile(image_path, str(self.folder) + "/images_html/Osdag_header.png")

    def show_capacity_dialog(self):
        self.dialog = myDialog(self)
        self.dialog.show()

    def show_button_clicked(self):
        self.show_capacity_dialog()

    def fetch_beam_param(self):
        beam_sec = self.ui.combo_Beam.currentText()
        dict_beam_data = get_beamdata(beam_sec)
        return dict_beam_data

    def fetch_column_param(self):
        column_sec = self.ui.comboColSec.currentText()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            dict_column_data = get_beamdata(column_sec)
        else:
            dict_column_data = get_columndata(column_sec)
        return dict_column_data

    def fetch_angle_param(self):
        angle_sec = self.ui.comboCleatSection.currentText()
        dict_angle_data = get_angledata(angle_sec)
        return dict_angle_data

    def convert_col_combo_to_beam(self):

        loc = self.ui.comboConnLoc.currentText()
        if loc == "Beam-Beam":
            self.ui.beamSection_lbl.setText(" Secondary beam *")
            self.ui.columnSection_lbl.setText("Primary beam *")

            self.ui.chkBxBeam.setText("SBeam")
            self.ui.chkBxBeam.setToolTip("Secondary  beam")
            self.ui.chkBxCol.setText("PBeam")
            self.ui.chkBxCol.setToolTip("Primary beam")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Primary beam")
            self.ui.outputBoltLbl.setText("Secondary beam")
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)

            # self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_beamcombolist())

# ---------------------------------------- Users input-----------------------------------------------------------------------------
            self.ui.comboColSec.setCurrentIndex(0)
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboBoltType.setCurrentIndex(0)
            self.ui.comboBoltGrade.setCurrentIndex(0)
            self.ui.comboCleatSection.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtInputCleatHeight.clear()

# ---------------------------------------- Output-----------------------------------------------------------------------------
            self.ui.txtNoBolts_c.clear()
            self.ui.txt_row_c.clear()
            self.ui.txt_column_c.clear()
            self.ui.txtBeamPitch_c.clear()
            self.ui.txtBeamGuage_c.clear()
            self.ui.txtEndDist_c.clear()
            self.ui.txtEdgeDist_c.clear()
            self.ui.txtNoBolts.clear()
            self.ui.txt_row.clear()
            self.ui.txt_column.clear()
            self.ui.txtBeamPitch.clear()
            self.ui.txtBeamGuage.clear()
            self.ui.txtEndDist.clear()
            self.ui.txtEdgeDist.clear()
            self.ui.outputCleatHeight.clear()

        elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":

            self.ui.columnSection_lbl.setText("Column Section *")
            self.ui.beamSection_lbl.setText("Beam section *")

            self.ui.chkBxBeam.setText("Beam")
            self.ui.chkBxBeam.setToolTip("Beam only")
            self.ui.chkBxCol.setText("Column")
            self.ui.chkBxCol.setToolTip("Column only")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Column")

            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)
            self.ui.outputBoltLbl.setText("Beam")

            # self.ui.comboColSec.clear()
            self.ui.comboColSec.addItems(get_columncombolist())

# ---------------------------------------- Users input-----------------------------------------------------------------------------
            self.ui.comboColSec.setCurrentIndex(0)
            self.ui.combo_Beam.setCurrentIndex(0)
            self.ui.comboDiameter.setCurrentIndex(0)
            self.ui.comboBoltType.setCurrentIndex(0)
            self.ui.comboBoltGrade.setCurrentIndex(0)
            self.ui.comboCleatSection.setCurrentIndex(0)

            self.ui.txtFu.clear()
            self.ui.txtFy.clear()
            self.ui.txtShear.clear()
            self.ui.txtInputCleatHeight.clear()

# ---------------------------------------- Output-----------------------------------------------------------------------------
            self.ui.txtNoBolts_c.clear()
            self.ui.txt_row_c.clear()
            self.ui.txt_column_c.clear()
            self.ui.txtBeamPitch_c.clear()
            self.ui.txtBeamGuage_c.clear()
            self.ui.txtEndDist_c.clear()
            self.ui.txtEdgeDist_c.clear()
            self.ui.txtNoBolts.clear()
            self.ui.txt_row.clear()
            self.ui.txt_column.clear()
            self.ui.txtBeamPitch.clear()
            self.ui.txtBeamGuage.clear()
            self.ui.txtEndDist.clear()
            self.ui.txtEdgeDist.clear()
            self.ui.outputCleatHeight.clear()

    def fill_cleatsection_combo(self):
        '''Populates the cleat section on the basis  beam section and column section
        '''

        if self.ui.combo_Beam.currentText() == "Select Designation" or self.ui.comboColSec.currentText() == "Select Column":
            self.ui.comboCleatSection.setCurrentIndex(0)
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web" or "Column flange-Beam web":
            loc = self.ui.comboConnLoc.currentText()
            dict_beam_data = self.fetch_beam_param()
            dict_column_data = self.fetch_column_param()
            angle_list = get_anglecombolist()
            col_R1 = float(dict_column_data[QString("R1")])
            col_D = float(dict_column_data[QString("D")])
            col_B = float(dict_column_data[QString("B")])
            col_T = float(dict_column_data[QString("T")])
            beam_tw = float(dict_beam_data[QString("tw")])

            if loc == "Column web-Beam web":
                colWeb = col_D - 2 * (col_T + col_R1)
            elif loc == "Column flange-Beam web":
                colWeb = col_B
            newlist = ['Select Cleat']

            for ele in angle_list[1:]:
                angle_sec = QtCore.QString(str(ele))
                dict_angle_data = get_angledata(angle_sec)
                cleat_legsize_b = float(dict_angle_data[QtCore.QString('B')])
                con_legsize = 2 * cleat_legsize_b + beam_tw
                space = colWeb - con_legsize
                if space > 0:
                    newlist.append(str(ele))
                else:
                    break

            self.ui.comboCleatSection.blockSignals(True)

            self.ui.comboCleatSection.clear()
            for i in newlist[:]:
                self.ui.comboCleatSection.addItem(str(i))

            self.ui.comboCleatSection.setCurrentIndex(-1)

            self.ui.comboCleatSection.blockSignals(False)
            self.ui.comboCleatSection.setCurrentIndex(0)
        else:
            pass

    def checkbeam_b(self):
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web":

            column = self.ui.comboColSec.currentText()

            dict_beam_data = self.fetch_beam_param()
            dict_column_data = self.fetch_column_param()
            column_D = float(dict_column_data[QString("D")])
            column_T = float(dict_column_data[QString("T")])
            column_R1 = float(dict_column_data[QString("R1")])
            column_web_depth = column_D - 2.0 * (column_T)

            beam_B = float(dict_beam_data[QString('B')])

            if column_web_depth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information', "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
            else:
                self.ui.btn_Design.setDisabled(False)

        elif loc == "Beam-Beam":

            primaryBeam = self.ui.comboColSec.currentText()
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

    def check_cleat_height(self, widget):
        loc = self.ui.comboConnLoc.currentText()
        cleatHeight = widget.text()
        cleatHeight = float(cleatHeight) 
        if cleatHeight == 0:
            self.ui.btn_Design.setDisabled(False)
        else:

            dict_beam_data = self.fetch_beam_param()
            dictColumnData = self.fetch_column_param()
            col_T = float(dictColumnData[QString('T')])
            col_R1 = float(dictColumnData[QString('R1')])
            beam_D = float(dict_beam_data[QString('D')])
            beam_T = float(dict_beam_data[QString('T')])
            beam_R1 = float(dict_beam_data[QString('R1')])
            clearDepth = 0.0
            minCleatHeight = 0.6 * beam_D
            if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                clearDepth = beam_D - 2 * (beam_T + beam_R1 + 5)
            else:
                clearDepth = beam_D - (beam_R1 + beam_T + col_R1 + col_T)
            if clearDepth < cleatHeight or cleatHeight < minCleatHeight:
                self.ui.btn_Design.setDisabled(True)
                QtGui.QMessageBox.about(self, 'Information',
                                        "Height of the Cleat Angle should be in between %s -%s mm" % (int(minCleatHeight), int(clearDepth)))
            else:
                self.ui.btn_Design.setDisabled(False)

    def show_font_dialog(self):

        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)

    def show_color_dialog(self):

        col = QtGui.QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
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
        fName = str(filename)
        file_extension = fName.split(".")[-1]

        if file_extension == 'png' or file_extension == 'jpg' or file_extension == 'gif':
            self.display.ExportToImage(fName)
            QtGui.QMessageBox.about(self, 'Information', "File saved")

    def disable_view_buttons(self):
        '''
        Disables the all buttons in toolbar
        '''

        # self.ui.actionShow_all.setEnabled(False)
        # self.ui.actionSave_3D_model_as.setEnabled(False)
        # self.ui.actionSave_CAD_image.setEnabled(False)
        # self.ui.actionSave_Front_View.setEnabled(False)
        # self.ui.actionSave_Top_View.setEnabled(False)
        # self.ui.actionSave_Side_View.setEnabled(False)
        # self.ui.actionSave_log_message.setEnabled(False)
        # self.ui.actionCreate_design_report.setEnabled(False)
        # self.ui.actionSave_design.setEnabled(False)
        # self.ui.actionZoom_in.setEnabled(False)
        # self.ui.actionZoom_out.setEnabled(False)
        # self.ui.actionRotate_3D_model.setEnabled(False)
        # self.ui.actionShow_beam.setEnabled(False)
        # self.ui.actionShow_column.setEnabled(False)
        # self.ui.actionShow_cleat_angle.setEnabled(False)
        self.ui.menubar.setEnabled(False)

        self.ui.btn_capacity.setEnabled(False)
        self.ui.btn_SaveMessages.setEnabled(False)
        self.ui.btn_CreateDesign.setEnabled(False)

        self.ui.btn_front.setEnabled(False)

        self.ui.btn_top.setEnabled(False)
        self.ui.btn_side.setEnabled(False)

        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.checkBoxCleat.setEnabled(False)

    def enable_view_buttons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_capacity.setEnabled(True)
        self.ui.btn_SaveMessages.setEnabled(True)
        self.ui.btn_CreateDesign.setEnabled(True)

        self.ui.btn_front.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn_side.setEnabled(True)

        self.ui.menubar.setEnabled(True)

        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.checkBoxCleat.setEnabled(True)

    def unchecked_all_checkbox(self):

        self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
        self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)

    def retrieve_prevstate(self):
        ui_obj = self.get_prevstate()
        if(ui_obj is not None):

            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(ui_obj['Member']['Connectivity'])))

            if ui_obj['Member']['Connectivity'] == 'Beam-Beam':
                self.ui.beamSection_lbl.setText('Secondary beam *')
                self.ui.columnSection_lbl.setText('Primary beam *')
                self.ui.comboColSec.addItems(get_beamcombolist())

            self.ui.combo_Beam.setCurrentIndex(self.ui.combo_Beam.findText(ui_obj['Member']['BeamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(ui_obj['Member']['ColumSection']))

            self.ui.txtFu.setText(str(ui_obj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(ui_obj['Member']['fy (MPa)']))

            self.ui.txtShear.setText(str(ui_obj['Load']['ShearForce (kN)']))

            self.ui.comboDiameter.setCurrentIndex(self.ui.comboDiameter.findText(str(ui_obj['Bolt']['Diameter (mm)'])))
            comboTypeIndex = self.ui.comboBoltType.findText(str(ui_obj['Bolt']['Type']))
            self.ui.comboBoltType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(ui_obj['Bolt']['Type']))

            prevValue = str(ui_obj['Bolt']['Grade'])

            comboGradeIndex = self.ui.comboBoltGrade.findText(prevValue)

            self.ui.comboBoltGrade.setCurrentIndex(comboGradeIndex)

            self.ui.txtInputCleatHeight.setText(str(ui_obj['cleat']['Height (mm)']))
            self.ui.comboCleatSection.setCurrentIndex(self.ui.comboCleatSection.findText(str(ui_obj['cleat']['section'])))

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
        Returns the dictionary object with the user input fields for designing cleat angle connection
        '''
        ui_obj = {}
        ui_obj["Bolt"] = {}
        ui_obj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        ui_obj["Bolt"]["Grade"] = float(self.ui.comboBoltGrade.currentText())
        # ui_obj["Bolt"]["Grade"] = 8.8
        ui_obj["Bolt"]["Type"] = str(self.ui.comboBoltType.currentText())

        ui_obj['Member'] = {}
        ui_obj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        ui_obj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        ui_obj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        ui_obj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        ui_obj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]

        ui_obj['cleat'] = {}
        ui_obj['cleat']['section'] = str(self.ui.comboCleatSection.currentText())
        ui_obj['cleat']['Height (mm)'] = float(self.ui.txtInputCleatHeight.text().toInt()[0])  # changes the label length to height

        ui_obj['Load'] = {}
        # ui_obj['Load']['ShearForce (kN)'] = float(self.ui.txtShear.text().toInt()[0])
        ui_obj['Load']['ShearForce (kN)'] = float(self.ui.txtShear.text())

        return ui_obj

    def save_inputs(self, ui_obj):
        '''
        (Dictionary)--> None
        '''
        inputFile = QtCore.QFile('saveINPUTS.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        # yaml.dump(ui_obj, inputFile,allow_unicode=True, default_flow_style = False)
        pickle.dump(ui_obj, inputFile)

    def get_prevstate(self):
        '''
        '''
        filename = 'saveINPUTS.txt'

        if os.path.isfile(filename):
            fileObject = open(filename, 'r')
            ui_obj = pickle.load(fileObject)
            return ui_obj
        else:
            return None

    def outputdict(self):

        ''' Returns the output of design in dictionary object.
        '''

        ui_obj = self.getuser_inputs()
        output_obj = cleat_connection(ui_obj)
        return output_obj

    def show_dialog(self):

        dialog = MyPopupDialog(self)
        dialog.show()

    def create_design_report(self):

        self.show_dialog()

    def save_design(self, popup_summary):

        # filename, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/", "Html Files (*.html)")
        filename = self.folder + "/images_html/Html_Report.html"
        filename = str(filename)
        self.call_2d_drawing("All")
        # base, base_front, base_top, base_side = self.call_2d_drawing("All")
        # self.outdict = self.result_obj#self.outputdict()

        self.inputdict = self.getuser_inputs()  # self.getuser_inputss()
        self.outdict = cleat_connection(self.inputdict)
        dict_beam_data = self.fetch_beam_param()

        dict_column_data = self.fetch_column_param()
        dict_cleat_data = self.fetch_angle_param()
        save_html(self.outdict, self.inputdict, dict_beam_data, dict_column_data, dict_cleat_data, popup_summary, filename, self.folder)

        # ########################################## Creates pdf: ####################################################################
        path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        options = {
            'margin-bottom': '10mm',
            'footer-right': '[page]'
        }
        #         pdfkit.from_file(filename, filename[:-5] + ".pdf", configuration=config, options=options)
        pdfkit.from_file(filename, str(QtGui.QFileDialog.getSaveFileName(self, "Save File As", self.folder + "/", "PDF (*.pdf)")), configuration=config,
                         options=options)
        QtGui.QMessageBox.about(self, 'Information', "Report Saved")

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def save_log(self):

        filename, pat = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Save File As", str(self.folder) + "/Logmessages", "Text files (*.txt)")
        return self.save_file(filename + ".txt")

    def save_file(self, filename):
        '''(file open for writing)-> boolean
        '''
        fname = QtCore.QFile(filename)

        if not fname.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (filename, fname.errorString()))
            return False

        outf = QtCore.QTextStream(fname)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        # self.setCurrentFile(filename);
        # QtGui.QMessageBox.about(self,'Information',"File saved")

    ###########################################################################################################################
        # def save_yaml(self,outObj,ui_obj):
        #     '''(dictiionary,dictionary) -> NoneType
        #     Saving input and output to file in following format.
        #     Bolt:
        #       diameter: 6
        #       grade: 8.800000190734863
        #       type: HSFG
        #     Load:
        #       shearForce: 100

        #     '''
        #     newDict = {"INPUT": ui_obj, "OUTPUT": outObj}
        #     filename = QtGui.QFileDialog.getSaveFileName(self,"Save File As","output/SaveDesign","Text File (*.txt)")
        #     f = open(filename,'w')
        #     yaml.dump(newDict,f,allow_unicode=True, default_flow_style=False)

        # return self.save_file(filename+".txt")
        # QtGui.QMessageBox.about(self,'Information',"File saved")

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
        self.ui.comboBoltType.setCurrentIndex((0))
        self.ui.comboBoltGrade.setCurrentIndex((0))

        self.ui.comboCleatSection.setCurrentIndex((0))
        self.ui.txtInputCleatHeight.clear()
        # self.ui.txtPlateWidth.clear()
        # self.ui.comboWldSize.setCurrentIndex((0))

        # ----------------------------------------------- Output ------------------------------------------------------------------
        # self.ui.txtShrCapacity.clear()
        # self.ui.txtbearCapacity.clear()
        # self.ui.txtBoltCapacity.clear()
        self.ui.txtNoBolts.clear()
        # self.ui.txtBoltGrpCapacity.clear()
        self.ui.txt_row.clear()
        self.ui.txt_column.clear()
        self.ui.txtBeamPitch.clear()
        self.ui.txtBeamGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()

        # column
        self.ui.txtNoBolts_c.clear()
        self.ui.txt_row_c.clear()
        self.ui.txt_column_c.clear()
        self.ui.txtBeamPitch_c.clear()
        self.ui.txtBeamGuage_c.clear()
        self.ui.txtEndDist_c.clear()
        self.ui.txtEdgeDist_c.clear()

        # self.ui.txtPlateThick.clear()
        self.ui.outputCleatHeight.clear()
        # self.ui.txtplate_width.clear()
        # self.ui.txtExtMomnt.clear()
        # self.ui.txtMomntCapacity.clear()
        # self.ui.txtWeldThick.clear()
        # self.ui.txtResltShr.clear()
        # self.ui.txtWeldStrng.clear()
        self.ui.textEdit.clear()

        # ---------------------------------- Erase Display ------------------------------------------------------------------
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

        self.ui.comboBoltGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))

        self.ui.comboBoltGrade.addItems(strItems)

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

        # self.uiPopUp.lineEdit_companyName.setText(str(shear_capacity))

        bearing_capacity = result_obj['Bolt']['bearingcapacity']
        # self.ui.txtbearCapacity.setText(str(bearing_capacity))

        bolt_capacity = result_obj['Bolt']['boltcapacity']
        # self.ui.txtBoltCapacity.setText(str(bolt_capacity))

        no_ofbolts = result_obj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        # newly added field
        bolt_grp_capacity = result_obj['Bolt']['boltgrpcapacity']
        # self.ui.txtBoltGrpCapacity.setText(str(bolt_grp_capacity))

        no_ofrows = result_obj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))

        no_ofcol = result_obj['Bolt']['numofcol']
        self.ui.txt_column.setText(str(no_ofcol))

        pitch_dist = result_obj['Bolt']['pitch']
        self.ui.txtBeamPitch.setText(str(pitch_dist))

        gauge_dist = result_obj['Bolt']['gauge']
        self.ui.txtBeamGuage.setText(str(gauge_dist))

        end_dist = result_obj['Bolt']['edge']
        self.ui.txtEndDist.setText(str(end_dist))

        edge_dist = result_obj['Bolt']['enddist']
        self.ui.txtEdgeDist.setText(str(edge_dist))
        # column
        c_noOfBolts = result_obj['cleat']['numofbolts']
        self.ui.txtNoBolts_c.setText(str(c_noOfBolts))
        cno_ofrows = result_obj['cleat']['numofrow']
        self.ui.txt_row_c.setText(str(cno_ofrows))

        no_ofcol = result_obj['cleat']['numofcol']
        self.ui.txt_column_c.setText(str(no_ofcol))

        pitch_dist = result_obj['cleat']['pitch']
        self.ui.txtBeamPitch_c.setText(str(pitch_dist))

        gauge_dist = result_obj['cleat']['guage']
        self.ui.txtBeamGuage_c.setText(str(gauge_dist))

        end_dist = result_obj['cleat']['edge']
        self.ui.txtEndDist_c.setText(str(end_dist))

        edge_dist = result_obj['cleat']['end']
        self.ui.txtEdgeDist_c.setText(str(edge_dist))

        # Newly included fields
        cleat_ht = result_obj['cleat']['height']
        self.ui.outputCleatHeight.setText(str(cleat_ht))

        # plate_width = result_obj['Cleat']['width']
        # self.ui.txtplate_width.setText(str(plate_width))

        moment_demand = result_obj['cleat']['externalmoment']
        # self.ui.txtExtMoment.setText(str(moment_demand))

        moment_capacity = result_obj['cleat']['momentcapacity']
        # self.ui.txtMomntCapacity.setText(str(moment_capacity))

    def displaylog_totextedit(self):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''
        afile = QtCore.QFile('Connections/Shear/cleatAngle/fin.log')

        if not afile.open(QtCore.QIODevice.ReadOnly):  # ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())

        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscroll_bar = self.ui.textEdit.verticalScrollBar()
        vscroll_bar.setValue(vscroll_bar.maximum())
        afile.close()

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
            from PyQt4 import QtCore, QtGui
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

            from OCC.Display.backend import get_loaded_backend
            lodedbkend = get_loaded_backend()
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

        self.setWindowTitle("Osdag Cleat Angle")
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

    def display_3d_model(self, component):
        self.display.EraseAll()
        self.display.SetModeShaded()
        display.DisableAntiAliasing()
#         self.display.set_bg_gradient_color(23,1,32,23,1,32)
        self.display.set_bg_gradient_color(51, 51, 102, 150, 150, 170)
#         self.display.set_bg_gradient_color(28,9,99,252,243,235)
        self.display.View_Front()
        self.display.View_Iso()
        self.display.FitAll()
        if component == "Column":
            osdag_display_shape(self.display, self.connectivity.get_column_model(), update=True)
        elif component == "Beam":
            osdag_display_shape(self.display, self.connectivity.get_beam_model(), material=Graphic3d_NOT_2D_ALUMINUM, update=True)
            # osdag_display_shape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif component == "cleatAngle":

            # osdag_display_shape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
            # osdag_display_shape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdag_display_shape(self.display, self.connectivity.angleModel, color='blue', update=True)
            osdag_display_shape(self.display, self.connectivity.angleLeftModel, color='blue', update=True)
            nutboltlist = self.connectivity.nut_bolt_array.get_model()
            for nutbolt in nutboltlist:
                osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
            # self.display.DisplayShape(self.connectivity.nut_bolt_array.get_models(), color = Quantity_NOC_SADDLEBROWN, update=True)
        elif component == "Model":
            osdag_display_shape(self.display, self.connectivity.columnModel, update=True)
            osdag_display_shape(self.display, self.connectivity.beamModel, material=Graphic3d_NOT_2D_ALUMINUM, update=True)
            # osdag_display_shape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
            # osdag_display_shape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdag_display_shape(self.display, self.connectivity.angleModel, color='blue', update=True)
            osdag_display_shape(self.display, self.connectivity.angleLeftModel, color='blue', update=True)
            nutboltlist = self.connectivity.nut_bolt_array.get_model()
            for nutbolt in nutboltlist:
                osdag_display_shape(self.display, nutbolt, color=Quantity_NOC_SADDLEBROWN, update=True)
            # self.display.DisplayShape(self.connectivity.nut_bolt_array.get_models(), color = Quantity_NOC_SADDLEBROWN, update=True)

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

        elif self.ui.comboDiameter.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Diameter of  bolt")

        elif self.ui.comboBoltType.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Type of  bolt")
        elif self.ui.comboCleatSection.currentIndex() == 0:
            QtGui.QMessageBox.about(self, "Information", "Please select Cleat angle")

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
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
        ui_obj = self.getuser_inputs()
        result_obj = cleat_connection(ui_obj)

        # ################################### PRIMARY BEAM PARAMETERS ########################################################

        dict_beam_data = self.fetch_column_param()
        pBeam_D = int(dict_beam_data[QString("D")])
        pBeam_B = int(dict_beam_data[QString("B")])
        pBeam_tw = float(dict_beam_data[QString("tw")])
        pBeam_T = float(dict_beam_data[QString("T")])
        pBeam_alpha = float(dict_beam_data[QString("FlangeSlope")])
        pBeam_R1 = float(dict_beam_data[QString("R1")])
        pBeam_R2 = float(dict_beam_data[QString("R2")])
        pBeam_length = 800.0  # This parameter as per view of 3D cad model

        # beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B=pBeam_B, T=pBeam_T, D=pBeam_D, t=pBeam_tw,
                          R1=pBeam_R1, R2=pBeam_R2, alpha=pBeam_alpha,
                          length=pBeam_length, notch_obj=None)

        # #### SECONDARY BEAM PARAMETERS ######
        dictbeamdata2 = self.fetch_beam_param()

        sBeam_D = int(dictbeamdata2[QString("D")])
        sBeam_B = int(dictbeamdata2[QString("B")])
        sBeam_tw = float(dictbeamdata2[QString("tw")])
        sBeam_T = float(dictbeamdata2[QString("T")])
        sBeam_alpha = float(dictbeamdata2[QString("FlangeSlope")])
        sBeam_R1 = float(dictbeamdata2[QString("R1")])
        sBeam_R2 = float(dictbeamdata2[QString("R2")])

        # ---------------------------- Notch dimensions -----------------------------------------------------------------
        notch_obj = Notch(R1=pBeam_R1, height=(pBeam_T + pBeam_R1), width=((pBeam_B - (pBeam_tw + 40)) / 2.0 + 10), length=sBeam_B)
        # column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B=sBeam_B, T=sBeam_T, D=sBeam_D,
                        t=sBeam_tw, R1=sBeam_R1, R2=sBeam_R2,
                        alpha=sBeam_alpha, length=500, notch_obj=notch_obj)

        # ############################################# WELD,PLATE,BOLT AND NUT PARAMETERS #######################################

        dict_angle_data = self.fetch_angle_param()
        cleat_length = result_obj['cleat']['height']

        cleat_thick = float(dict_angle_data[QString("t")])
        angle_A = int(dict_angle_data[QString("A")])
        angle_B = int(dict_angle_data[QString("B")])
        # cleat_thick = 10
        # angle_A = 120
        # angle_B = 90
        # bolt_dia = ui_obj["Bolt"]["Diameter (mm)"]
        # bolt_r = bolt_dia/2
        # bolt_R = bolt_r + 7
        # nut_R = bolt_R
        # bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3750(1985)
        # nut_T = 12.0 # minimum nut thickness As per Indian Standard
        # nut_Ht = 12.2 #

        bolt_dia = ui_obj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150
        # plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = sBeam_tw + 2 * cleat_thick + nut_T
        cgap = pBeam_tw + cleat_thick + nut_T

        nut_bolt_array = NutBoltArray(result_obj, nut, bolt, gap, cgap)

        beamwebconn = BeamWebBeamWeb(column, beam, notch_obj, angle, nut_bolt_array)
        beamwebconn.create_3dmodel()

        return beamwebconn

    def create_3d_col_web_beam_web(self):
        '''
        creating 3d cad model with column web beam web
        '''
        ui_obj = self.getuser_inputs()
        result_obj = cleat_connection(ui_obj)

        dict_beam_data = self.fetch_beam_param()
        # ################################## BEAM PARAMETERS ####################################################################
        beam_D = int(dict_beam_data[QString("D")])
        beam_B = int(dict_beam_data[QString("B")])
        beam_tw = float(dict_beam_data[QString("tw")])
        beam_T = float(dict_beam_data[QString("T")])
        beam_alpha = float(dict_beam_data[QString("FlangeSlope")])
        beam_R1 = float(dict_beam_data[QString("R1")])
        beam_R2 = float(dict_beam_data[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                        length=beam_length, notch_obj=None)

        # #################################################### COLUMN PARAMETERS #################################################
        dict_column_data = self.fetch_column_param()

        column_D = int(dict_column_data[QString("D")])
        column_B = int(dict_column_data[QString("B")])
        column_tw = float(dict_column_data[QString("tw")])
        column_T = float(dict_column_data[QString("T")])
        column_alpha = float(dict_column_data[QString("FlangeSlope")])
        column_R1 = float(dict_column_data[QString("R1")])
        column_R2 = float(dict_column_data[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notch_obj=None)
        # ########################################## WELD,PLATE,BOLT AND NUT PARAMETERS ############################################
        dict_angle_data = self.fetch_angle_param()
        cleat_length = result_obj['cleat']['height']

        cleat_thick = float(dict_angle_data[QString("t")])
        angle_A = int(dict_angle_data[QString("A")])
        angle_B = int(dict_angle_data[QString("B")])
        # cleat_thick = 10
        # angle_A = 120
        # angle_B = 90
        # bolt_dia = ui_obj["Bolt"]["Diameter (mm)"]
        # bolt_r = bolt_dia/2
        # bolt_R = bolt_r + 7
        # nut_R = bolt_R
        # bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3750(1985)
        # nut_T = 12.0 # minimum nut thickness As per Indian Standard
        # nut_Ht = 12.2 #
        ####################################################################################################################
        bolt_dia = ui_obj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150
        #####################################################################################################################
        # plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = beam_tw + 2 * cleat_thick + nut_T
        cgap = column_tw + cleat_thick + nut_T

        nut_bolt_array = NutBoltArray(result_obj, nut, bolt, gap, cgap)

        colwebconn = ColWebBeamWeb(column, beam, angle, nut_bolt_array)
        colwebconn.create_3dmodel()

        return colwebconn

    def create_3d_col_flange_beam_web(self):
        '''
        Creating 3d cad model with column flange beam web connection
        '''
        ui_obj = self.getuser_inputs()
        result_obj = cleat_connection(ui_obj)

        dict_beam_data = self.fetch_beam_param()
        # #### BEAM PARAMETERS #####
        beam_D = int(dict_beam_data[QString("D")])
        beam_B = int(dict_beam_data[QString("B")])
        beam_tw = float(dict_beam_data[QString("tw")])
        beam_T = float(dict_beam_data[QString("T")])
        beam_alpha = float(dict_beam_data[QString("FlangeSlope")])
        beam_R1 = float(dict_beam_data[QString("R1")])
        beam_R2 = float(dict_beam_data[QString("R2")])
        beam_length = 500.0  # This parameter as per view of 3D cad model

        # beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B=beam_B, T=beam_T, D=beam_D, t=beam_tw,
                        R1=beam_R1, R2=beam_R2, alpha=beam_alpha,
                        length=beam_length, notch_obj=None)

        # ############################################## COLUMN PARAMETERS ##################################################
        dict_column_data = self.fetch_column_param()

        column_D = int(dict_column_data[QString("D")])
        column_B = int(dict_column_data[QString("B")])
        column_tw = float(dict_column_data[QString("tw")])
        column_T = float(dict_column_data[QString("T")])
        column_alpha = float(dict_column_data[QString("FlangeSlope")])
        column_R1 = float(dict_column_data[QString("R1")])
        column_R2 = float(dict_column_data[QString("R2")])

        # column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B=column_B, T=column_T, D=column_D,
                          t=column_tw, R1=column_R1, R2=column_R2, alpha=column_alpha, length=1000, notch_obj=None)

        # ############################### Cleat,BOLT AND NUT PARAMETERS ###########################################################
        dict_angle_data = self.fetch_angle_param()
        cleat_length = result_obj['cleat']['height']

        cleat_thick = float(dict_angle_data[QString("t")])
        angle_A = int(dict_angle_data[QString("A")])
        angle_B = int(dict_angle_data[QString("B")])
#         cleat_thick = 10
#         angle_A = 120
#         angle_B = 90

#         bolt_dia = ui_obj["Bolt"]["Diameter (mm)"]
#         bolt_r = bolt_dia/2
#         bolt_R = bolt_r + 7
#         nut_R = bolt_R
#         bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
#         bolt_Ht = 50.0 # minimum bolt length as per Indian Standard
#         nut_T = 12.0 # minimum nut thickness As per Indian Standard
#         nut_Ht = 12.2
    ######################################################################################################
        bolt_dia = ui_obj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia / 2
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        nut_R = bolt_R
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        # bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        nut_Ht = 12.2  # 150

    ##########################################################################################################

        # plate = Plate(L= 300,W =100, T = 10)
        angle = Angle(L=cleat_length, A=angle_A, B=angle_B, T=cleat_thick)

        # bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R=bolt_R, T=bolt_T, H=bolt_Ht, r=bolt_r)

        # nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R=bolt_R, T=nut_T, H=nut_Ht, innerR1=bolt_r)

        gap = beam_tw + 2 * cleat_thick + nut_T
        cgap = column_T + cleat_thick + nut_T

        nut_bolt_array = NutBoltArray(result_obj, nut, bolt, gap, cgap)

        colflangeconn = ColFlangeBeamWeb(column, beam, angle, nut_bolt_array)
        colflangeconn.create_3dmodel()
        return colflangeconn

    def call_3d_model(self, flag):
        # self.ui.btnSvgSave.setEnabled(True)
        self.ui.btn3D.setChecked(QtCore.Qt.Checked)
        if self.ui.btn3D.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        if flag is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web":
                # self.create_3d_col_web_beam_web()
                self.connectivity = self.create_3d_col_web_beam_web()
                self.fuse_model = None
            elif self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create_3d_col_flange_beam_web()
                self.fuse_model = None

            else:
                self.ui.mytabWidget.setCurrentIndex(0)
                self.connectivity = self.create_3d_beam_web_beam_web()
                self.fuse_model = None

            self.display_3d_model("Model")
            # beamOrigin = self.connectivity.beam.secOrigin + self.connectivity.beam.t/2 * (-self.connectivity.beam.uDir)
            # gpBeamOrigin = getGpPt(beamOrigin)
            # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
            # self.display.DisplayShape(my_sphere2,color = 'red',update = True)
            # beamOrigin = self.connectivity.beam.secOrigin
            # gpBeamOrigin = getGpPt(beamOrigin)
            # my_sphere2 = BRepPrimAPI_MakeSphere(gpBeamOrigin,1).Shape()
            # self.display.DisplayShape(my_sphere2,color = 'blue',update = True)
            # plateOrigin =(self.connectivity.plate.secOrigin + self.connectivity.plate.T/2.0 *(self.connectivity.plate.uDir)+ self.connectivity.weldLeft.L/2.0
            # * (self.connectivity.plate.vDir) + self.connectivity.plate.T * (-self.connectivity.weldLeft.uDir))
            # gpPntplateOrigin=  getGpPt(plateOrigin)
            # my_sphere = BRepPrimAPI_MakeSphere(gpPntplateOrigin,2).Shape()
            # self.display.DisplayShape(my_sphere,update=True)

        else:
            self.display.EraseAll()
            # self.display.DisplayMessage(gp_Pnt(1000,0,400),"Sorry, can not create 3D model",height = 23.0)

    def call_3d_beam(self):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display_3d_model("Beam")

    def call_3d_column(self):
        '''
        '''
        self.ui.chkBxCol.setChecked(QtCore.Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.display_3d_model("Column")

    def call_3d_cleatangle(self):
        '''Displaying FinPlate in 3D
        '''
        self.ui.checkBoxCleat.setChecked(QtCore.Qt.Checked)
        if self.ui.checkBoxCleat.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.btn3D.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.display_3d_model("cleatAngle")

    def design_btnclicked(self):
        '''
        '''
        self.validate_inputs_on_design_button()
        self.ui.outputDock.setFixedSize(310, 710)
        self.enable_view_buttons()
        self. unchecked_all_checkbox()

        # self.set_designlogger()
        # Getting User Inputs.
        self.ui_obj = self.getuser_inputs()
        self.save_inputs(self.ui_obj)

        # FinPlate Design Calculations.
        self.result_obj = cleat_connection(self.ui_obj)
        d = self.result_obj[self.result_obj.keys()[0]]
        if len(str(d[d.keys()[0]])) == 0:
            self.ui.btn_CreateDesign.setEnabled(False)
        # self.outputdict()

        # Displaying Design Calculations To Output Window
        self.display_output(self.result_obj)

        # Displaying Messages related to FinPlate Design.
        self.displaylog_totextedit()

        # Displaying 3D Cad model
        status = self.result_obj['Bolt']['status']
        self.call_3d_model(status)
        self.call_2d_drawing('All')

    def create_2d_cad(self, connectivity):
        ''' Returns the fuse model of cleat angle
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

        file_name = str(filename)
        file_extension = file_name.split(".")[-1]

        if file_extension == 'igs':
            IGESControl.IGESControl_Controller().Init()
            iges_writer = IGESControl.IGESControl_Writer()
            iges_writer.AddShape(shape)
            iges_writer.Write(file_name)

        elif file_extension == 'brep':

            BRepTools.breptools.Write(shape, file_name)

        elif file_extension == 'stp':
            # initialize the STEP exporter
            step_writer = STEPControl_Writer()
            Interface_Static_SetCVal("write.step.schema", "AP203")

            # transfer shapes and write file
            step_writer.Transfer(shape, STEPControl_AsIs)
            status = step_writer.Write(file_name)

            assert(status == IFSelect_RetDone)

        else:
            stl_writer = StlAPI_Writer()
            stl_writer.SetASCIIMode(True)
            stl_writer.Write(shape, file_name)

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

    # def call_desired_view(self, filename, view, base_front, base_top, base_side):

    def call_desired_view(self, filename, view):
        self. unchecked_all_checkbox()

        ui_obj = self.getuser_inputs()
        result_obj = cleat_connection(ui_obj)
        dict_beam_data = self.fetch_beam_param()
        dict_column_data = self.fetch_column_param()
        dict_angle_data = self.fetch_angle_param()
        fin_common_obj = cleatCommonData(ui_obj, result_obj, dict_beam_data, dict_column_data, dict_angle_data, self.folder)
        fin_common_obj.save_to_svg(str(filename), view)
        # base_front, base_top, base_side = fin_common_obj.save_to_svg(str(filename), view, base_front, base_top, base_side)
        # return (base_front, base_top, base_side)

    def call_2d_drawing(self, view):

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from CleatAngle GUI.
        '''
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
#             for n in range(1, 100, 1):
#                 if (os.path.exists(data)):
#                     data = str(self.folder) + "/images_html/3D_Model" + str(n) + ".png"
#                     continue
#             base = os.path.basename(str(data))

        else:
            if view == "Front":
                filename = self.folder + "/images_html/cleatFront.svg"

            elif view == "Side":
                filename = self.folder + "/images_html/cleatSide.svg"

            else:
                filename = self.folder + "/images_html/cleatTop.svg"

            svg_file = SvgWindow()
            svg_file.call_svgwindow(filename, view, self.folder)

#       filename = QtGui.QFileDialog.getSaveFileName(self,
#                                                  "Save SVG", str(self.folder) + '/untitled.svg',
#                                                   "SVG files (*.svg)")
#       f = open(filename, 'w')
#       base1, base2, base3 = self.call_desired_view(filename, view, base_front, base_top, base_side)
#       f.close()
#   return (base, base1, base2, base3)

    def closeEvent(self, event):
        '''
        Closing finPlate window.
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
#         counter = 0
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                os.startfile("%s/%s" % (root_path, pdf_file))
#                 counter = counter + 1

    def sample_problem(self):
        root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Sample_Folder', 'Sample_Report')
        for pdf_file in os.listdir(root_path):
            if pdf_file.endswith('.pdf'):
                os.startfile("%s/%s" % (root_path, pdf_file))

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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/fin.log", mode="a")

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


def launch_cleatangle_controller(osdag_main_window, folder):
    set_osdaglogger()
    raw_logger = logging.getLogger("raw")
    raw_logger.setLevel(logging.INFO)
    fh = logging.FileHandler("Connections/Shear/cleatAngle/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/cleatAngle/log.css"/>''')

    # app = QtGui.QApplication(sys.argv)
    module_setup()
    # web = QWebView()
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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/cleatAngle/log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    module_setup()
    # web = QWebView()
    window = MainController()
    window.show()
    sys.exit(app.exec_())
