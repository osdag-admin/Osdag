'''
Created on 07-May-2015
comment

@author: aravind
'''
import ConfigParser
import json
import os.path
import pickle
import subprocess

from PyQt5.QtCore import QFile,pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator,QPixmap, QPalette
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QDesktopWidget
from OCC import IGESControl,BRepTools
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.IFSelect import IFSelect_RetDone
from OCC.Interface import Interface_Static_SetCVal
from OCC.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.StlAPI import StlAPI_Writer
from cleatCalculation import cleat_connection
from drawing2D import *
from model import *
from ui_design_preferences import Ui_ShearDesignPreferences
from ui_cleatAngle import Ui_MainWindow
from ui_popUpWindow import Ui_Capacitydetals
from ui_summary_popup import Ui_Dialog
from ui_aboutosdag import Ui_AboutOsdag
from ui_tutorial import Ui_Tutorial
from ui_ask_question import Ui_AskQuestion
from Svg_Window import SvgWindow
from Connections.Shear.common_logic import CommonDesignLogic
import shutil
import pdfkit
import cairosvg

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
        int_validator = QIntValidator()
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_detailingGap.setValidator(dbl_validator)
        self.ui.txt_detailingGap.setMaxLength(5)
        self.set_default_para()
        self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

    def save_designPref_para(self):
        '''
        This routine is responsible for saving all design preferences selected by the user
        '''
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())

        self.saved_designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
        self.saved_designPref["bolt"]["bolt_fu"] = float(self.ui.txt_boltFu.text())
        self.saved_designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        self.saved_designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        self.saved_designPref["weld"]["typeof_weld"] = weldType
        if weldType == "Shop weld":
            self.saved_designPref["weld"]["safety_factor"] = float(1.25)
        else:
            self.saved_designPref["weld"]["safety_factor"] = float(1.5)

        self.saved_designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        self.saved_designPref["detailing"]["typeof_edge"] = typeOfEdge
        if typeOfEdge == "a - Sheared or hand flame cut":
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.7)
        else:
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.5)
        if self.ui.txt_detailingGap.text() == '':

            self.saved_designPref["detailing"]["gap"] = float(10)
        else:
            self.saved_designPref["detailing"]["gap"] = float(self.ui.txt_detailingGap.text())
        self.saved_designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())

        self.saved_designPref["design"] = {}
        self.ui.combo_design_method.setCurrentIndex(0)
        self.saved_designPref["design"]["design_method"] = self.ui.combo_design_method.currentText()

        self.saved = True

        # QMessageBox.about(self, 'Information', "Preferences saved")

        return self.saved_designPref


    def set_default_para(self):
        '''
        '''

        uiObj = self.main_controller.getuser_inputs()

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

        designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()#float
        designPref["bolt"]["bolt_fu"] = float(self.ui.txt_boltFu.text())#float
        self.ui.combo_slipfactor.setCurrentIndex(4)
        designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        # self.ui.combo_weldType.setCurrentIndex(0)
        # designPref["weld"] = {}
        # weldType = str(self.ui.combo_weldType.currentText())
        # designPref["weld"]["typeof_weld"] = weldType
        # designPref["weld"]["safety_factor"] = float(1.25)

        self.ui.combo_detailingEdgeType.setCurrentIndex(0)
        self.ui.txt_detailingGap.setText(str(10))
        designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        designPref["detailing"]["typeof_edge"] = typeOfEdge
        designPref["detailing"]["min_edgend_dist"] = float(1.7)
        designPref["detailing"]["gap"] = float(10)
        self.ui.combo_detailing_memebers.setCurrentIndex(0)
        designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())

        self.ui.combo_design_method.setCurrentIndex(0)
        designPref["design"] = {}
        designPref["design"]["design_method"] = self.ui.combo_design_method.currentText()
        self.saved = False
        return designPref

    def set_bolthole_clernce(self):
        uiObj = self.main_controller.getuser_inputs()
        boltDia = str(uiObj["Bolt"]["Diameter (mm)"])
        if boltDia != "Diameter of Bolt":
            clearance = self.get_clearance(int(boltDia))
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

    def get_clearance(self):

        uiObj = self.main_controller.getuser_inputs()
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
        '''
        This routine returns ultimate strength of bolt depending upon grade of bolt chosen
        '''
        if boltGrade != '':
            # Nominal tensile strength (Table 3, IS 1367(part 3):2002) should be taken for calculations
            # boltFu = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 8.8: 800, 9.8: 900, 10.9: 1040,
            #           12.9: 1220}
            boltGrd = float(boltGrade)
            boltFu = int(boltGrd) * 100
            return boltFu
        else:
            pass

    def close_designPref(self):
        self.close()



class MyAskQuestion(QDialog):
    """

    """
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
        """

        :return:
        """

        input_summary = self.get_design_report_inputs()
        self.mainController.save_design(input_summary)

    def get_logo_file_path(self, lblwidget):

        self.ui.lbl_browse.clear()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', "../../ ", 'Images (*.png *.svg *.jpg)', None, QFileDialog.DontUseNativeDialog)
        flag = True
        if filename == '':
            flag = False
            return flag
        else:
            base = os.path.basename(str(filename))
            lblwidget.setText(base)
            base_type = base[-4:]
            self.desired_location(filename, base_type)

    def desired_location(self, filename, base_type):
        if base_type == ".svg":
            cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.mainController.folder), "images_html", "cmpylogoCleat.png"))
        else:
            shutil.copyfile(filename, os.path.join(str(self.mainController.folder), "images_html", "cmpylogoCleat.png"))

    def save_user_profile(self):
        input_data = self.get_design_report_inputs()

        filename, _ = QFileDialog.getSaveFileName(self, 'Save Files', os.path.join(str(self.mainController.folder), "Profile"), '*.txt')

        if filename == '':
            flag = False
            return flag
        else:
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
        files_types = "All Files (*))"
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


class myDialog(QDialog):
# (Ui_Capacitydetals):

    def __init__(self, parent=None):

        QDialog.__init__(self, parent)
        self.ui = Ui_Capacitydetals()
        self.ui.setupUi(self)
        self.setWindowTitle("Capacity Details")
        self.mainController = parent
        ui_obj = self.mainController.alist[0]
        #ui_obj = self.mainController.getuser_inputs()
        print "ui_obj form capacity deatials",ui_obj
        x = cleat_connection(ui_obj)

        # Column - Supporting member
        self.ui.shear.setText(str(x['cleat']['shearcapacity']))
        self.ui.bearing.setText(str(x['cleat']['bearingcapacity']))
        self.ui.capacity.setText(str(x['cleat']['boltcapacity']))
        self.ui.boltGrp.setText(str(x['cleat']['boltgrpcapacity']))

        # Beam - Supported member
        self.ui.shear_b.setText(str(x['Bolt']['shearcapacity']))
        self.ui.bearing_b.setText(str(x['Bolt']['bearingcapacity']))
        self.ui.capacity_b.setText(str(x['Bolt']['boltcapacity']))
        self.ui.boltGrp_b.setText(str(x['Bolt']['boltgrpcapacity']))

        # Cleat
        self.ui.mDemand.setText(str(x['cleat']['externalmoment']))
        self.ui.mCapacity.setText(str(x['cleat']['momentcapacity']))


class MainController(QMainWindow):

    closed = pyqtSignal()

    def __init__(self, folder):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.folder = folder
        self.connection = "cleatAngle"

        self.get_columndata()
        self.get_beamdata()
        self.designPrefDialog = DesignPreferences(self)
        self.ui.comboCleatSection.addItems(get_anglecombolist())

        self.ui.inputDock.setFixedSize(310, 710)

        self.gradeType = {'Please Select Type': '', 'Friction Grip Bolt': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.comboBoltType.addItems(self.gradeType.keys())
        self.ui.comboBoltType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboBoltType.setCurrentIndex(0)

        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        self.retrieve_prevstate()
        # Adding GUI changes for beam to beam connection
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.convert_col_combo_to_beam)
        #############################################################################################################
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))

        self.ui.toolButton.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.btn_front.clicked.connect(lambda: self.callCleat2D_drawing("Front"))
        self.ui.btn_top.clicked.connect(lambda: self.callCleat2D_drawing("Top"))
        self.ui.btn_side.clicked.connect(lambda: self.callCleat2D_drawing("Side"))

        self.ui.btn3D.clicked.connect(lambda:self.call_3d_model("gradient_bg"))
        self.ui.chkBxBeam.clicked.connect(lambda:self.call_3d_beam("gradient_bg"))
        self.ui.chkBxCol.clicked.connect(lambda:self.call_3d_column("gradient_bg"))
        self.ui.checkBoxCleat.clicked.connect(lambda:self.call_3d_cleatangle("gradient_bg"))

        # validator = QIntValidator()
        # self.ui.txtFu.setValidator(validator)
        # self.ui.txtFy.setValidator(validator)

        dbl_validator = QDoubleValidator()
        self.ui.txtFu.setValidator(dbl_validator)
        self.ui.txtFu.setMaxLength(6)
        self.ui.txtFy.setValidator(dbl_validator)
        self.ui.txtFy.setMaxLength(6)

        self.ui.txtInputCleatHeight.setValidator(dbl_validator)
        self.ui.txtInputCleatHeight.setMaxLength(7)
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

        self.ui.actionCreate_design_report.triggered.connect(self.create_design_report)
        self.ui.actionSave_log_message.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.show_font_dialog)
        self.ui.actionZoom_in.triggered.connect(self.call_zoom_in)
        self.ui.actionZoom_out.triggered.connect(self.call_zoom_out)
        self.ui.actionPan.triggered.connect(self.call_panning)
        self.ui.actionSave_3D_model.triggered.connect(self.save_3d_cad_images)
        self.ui.actionSave_CAD_image.triggered.connect(self.save_cadImages)
        self.ui.actionCleat_quit.setStatusTip('Exit application')
        self.ui.actionCleat_quit.triggered.connect(qApp.quit)
        self.ui.actionSave_input.triggered.connect(self.saveDesign_inputs)
        self.ui.actionLoad_input.triggered.connect(self.openDesign_inputs)

        self.ui.actionSave_Front_View.triggered.connect(lambda: self.callCleat2D_drawing("Front"))
        self.ui.actionSave_Side_View.triggered.connect(lambda: self.callCleat2D_drawing("Side"))
        self.ui.actionSave_Top_View.triggered.connect(lambda: self.callCleat2D_drawing("Top"))

        self.ui.actionShow_beam.triggered.connect(lambda:self.call_3d_beam("gradient_bg"))
        self.ui.actionShow_column.triggered.connect(lambda:self.call_3d_column("gradient_bg"))
        self.ui.actionShow_cleat_angle.triggered.connect(lambda:self.call_3d_cleatangle("gradient_bg"))
        self.ui.actionShow_all.triggered.connect(lambda: self.call_3d_model("gradient_bg"))
        self.ui.actionChange_background.triggered.connect(self.show_color_dialog)

        # populate cleat section and secondary beam according to user input
        self.ui.comboColSec.currentIndexChanged[int].connect(self.fill_cleatsection_combo)
        self.ui.combo_Beam.currentIndexChanged[str].connect(self.checkbeam_b)
        self.ui.comboColSec.currentIndexChanged[str].connect(self.checkbeam_b)
        self.ui.txtInputCleatHeight.editingFinished.connect(lambda: self.check_cleat_height(
            self.ui.txtInputCleatHeight, self.ui.cleatLength_lbl))
        self.ui.comboBoltGrade.currentIndexChanged[str].connect(self.call_boltFu)
        ######################################################################################
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.create_design_report)  # Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        #################################################################
        self.ui.btn_capacity.clicked.connect(self.show_button_clicked)

        #################################################################
        # Saving and Restoring the finPlate window state.
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

        self.ui.btn_Design.clicked.connect(self.osdag_header)

# ************************************ Help button *******************************************************************************
        self.ui.actionAbout_Osdag.triggered.connect(self.open_osdag)
        self.ui.actionVideo_Tutorials.triggered.connect(self.tutorials)
        self.ui.actionDesign_examples.triggered.connect(self.design_examples)
        # self.ui.actionSample_Reports.triggered.connect(self.sample_report)
        # self.ui.actionSample_Problems.triggered.connect(self.sample_problem)
        self.ui.actionAsk_Us_a_Question.triggered.connect(self.open_question)
        self.ui.actionDesign_preferences.triggered.connect(self.design_preferences)

        # Initialising the qtviewer
        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        self.connectivity = None
        self.fuse_model = None
        self.disable_view_buttons()
        self.result_obj = None
        self.ui_obj = None
        self.commLogicObj = None

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
        loc = self.ui.comboConnLoc.currentText()
        beamdata = get_beamcombolist()
        old_beamList = get_oldbeamcombolist()
        combo_section = ''
        if loc == "Beam-Beam":
            self.ui.comboColSec.addItems(beamdata)
            combo_section = self.ui.comboColSec
        else:
            self.ui.combo_Beam.addItems(beamdata)
            combo_section = self.ui.combo_Beam

        self.color_oldDB_sections(old_beamList, beamdata, combo_section)


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
        duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]
        for i in duplicate:
            combo_section.setItemData(i, QBrush(QColor("red")), Qt.TextColorRole)


    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join( "ResourceFiles", "Osdag_header.png")))
        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "Osdag_header.png"))

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
        """
        :return:
        """
        self.display.EraseAll()
        loc = str(self.ui.comboConnLoc.currentText())
        if loc == "Beam-Beam":
            self.ui.beamSection_lbl.setText("Secondary beam *")
            self.ui.actionShow_beam.setText("Show SBeam")
            self.ui.columnSection_lbl.setText("Primary beam *")
            self.ui.actionShow_column.setText("Show PBeam")

            self.ui.chkBxBeam.setText("SBeam")
            self.ui.chkBxBeam.setToolTip("Secondary beam")
            self.ui.chkBxCol.setText("PBeam")
            self.ui.chkBxCol.setToolTip("Primary beam")
            self.ui.comboColSec.blockSignals(True)
            self.ui.comboColSec.clear()
            self.get_beamdata()
            self.ui.combo_Beam.setCurrentIndex(0)

            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Primary beam")
            self.ui.outputBoltLbl.setText("Secondary beam")
            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)

            self.ui.comboColSec.addItems(get_beamcombolist())

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
            self.display.EraseAll()
            self.disable_view_buttons()

        elif loc == "Column web-Beam web" or loc == "Column flange-Beam web":

            self.ui.columnSection_lbl.setText("Column Section *")
            self.ui.actionShow_column.setText("Show column")
            self.ui.beamSection_lbl.setText("Beam section *")
            self.ui.actionShow_beam.setText("Show beam")

            self.ui.chkBxBeam.setText("Beam")
            self.ui.chkBxBeam.setToolTip("Beam only")
            self.ui.chkBxCol.setText("Column")
            self.ui.chkBxCol.setToolTip("Column only")

            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl_3.setFont(font)
            self.ui.outputBoltLbl_3.setText("Column")

            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            self.ui.outputBoltLbl.setFont(font)
            self.ui.outputBoltLbl.setText("Beam")
            self.ui.comboColSec.clear()
            self.get_columndata()
            self.ui.comboColSec.currentText()

            # self.ui.comboColSec.addItems(get_columncombolist())

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
            self.display.EraseAll()
            self.disable_view_buttons()

    def fill_cleatsection_combo(self):
        '''Populates the cleat section on the basis  beam section and column section
        '''
        self.ui.combo_Beam.currentText()
        self.ui.comboColSec.currentText()
        if str(self.ui.combo_Beam.currentText()) == "Select section" or str(self.ui.comboColSec.currentText()) == "Select section" or str(self.ui.comboColSec.currentText()) == '':
            return
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web" or loc == "Column web-Beam web":

            dict_beam_data = self.fetch_beam_param()
            dict_column_data = self.fetch_column_param()
            angle_list = get_anglecombolist()
            col_R1 = float(dict_column_data["R1"])
            col_D = float(dict_column_data["D"])
            col_B = float(dict_column_data["B"])
            col_T = float(dict_column_data["T"])
            beam_tw = float(dict_beam_data["tw"])

            if loc == "Column web-Beam web":
                colWeb = col_D - (2 * (col_T + col_R1))
            elif loc == "Column flange-Beam web":
                colWeb = col_B
            newlist = ['Select Cleat']

            for ele in angle_list[1:]:
                angle_sec = str(ele)
                dict_angle_data = get_angledata(angle_sec)
                cleat_legsizes = str(dict_angle_data["AXB"])
                cleat_legsize_A = int(cleat_legsizes.split('x')[0])
                cleat_legsize_B = int(cleat_legsizes.split('x')[1])
                cleat_legsize_b = float(cleat_legsize_B)
                con_legsize = (2 * cleat_legsize_b) + beam_tw
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
        check = True
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column web-Beam web":
            if self.ui.comboColSec.currentIndex() == -1 or str(self.ui.combo_Beam.currentText()) == 'Select section' or str(self.ui.comboColSec.currentText()) == 'Select section':
                return

            column = self.ui.comboColSec.currentText()

            dict_beam_data = self.fetch_beam_param()
            dict_column_data = self.fetch_column_param()
            column_D = float(dict_column_data["D"])
            column_T = float(dict_column_data["T"])
            column_R1 = float(dict_column_data["R1"])
            column_web_depth = column_D - 2.0 * (column_T)

            beam_B = float(dict_beam_data['B'])

            if column_web_depth <= beam_B:
                self.ui.btn_Design.setDisabled(True)
                QMessageBox.about(self, 'Information', "Beam flange is wider than clear depth of column web (No provision in Osdag till now)")
                check = False
            else:
                self.ui.btn_Design.setDisabled(False)

        elif loc == "Beam-Beam":
            if self.ui.comboColSec.currentIndex() == 0 or self.ui.combo_Beam.currentIndex() == 0:
                return

            primaryBeam = self.ui.comboColSec.currentText()
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
                check = False
            else:
                self.ui.btn_Design.setDisabled(False)
        return check

    def check_cleat_height(self, widget, lblwidget):
        '''

        Args:
            widget: QlineEdit
            lblwidget: QLabel

        Returns:
            range of cleat height

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

                cleatHeight = widget.text()
                cleatHeight = float(cleatHeight)
                if cleatHeight == 0:
                    self.ui.btn_Design.setDisabled(False)
                else:

                    dict_beam_data = self.fetch_beam_param()
                    dictColumnData = self.fetch_column_param()
                    col_T = float(dictColumnData['T'])
                    col_R1 = float(dictColumnData['R1'])
                    beam_D = float(dict_beam_data['D'])
                    beam_T = float(dict_beam_data['T'])
                    beam_R1 = float(dict_beam_data['R1'])
                    clearDepth = 0.0
                    minCleatHeight = 0.6 * beam_D
                    if loc == "Column web-Beam web" or loc == "Column flange-Beam web":
                        clearDepth = beam_D - 2 * (beam_T + beam_R1 + 5)
                    else:
                        clearDepth = beam_D - (beam_R1 + beam_T + col_R1 + col_T)
                    if clearDepth < cleatHeight or cleatHeight < minCleatHeight:
                        #self.ui.btn_Design.setDisabled(True)
                        QMessageBox.warning(self, 'Warning', "Height of the Cleat Angle should be in between %s -%s mm" % (int(minCleatHeight), int(clearDepth)))
                        widget.clear()
                        widget.setFocus()
                        palette = QPalette()
                        palette.setColor(QPalette.Foreground, Qt.red)
                        lblwidget.setPalette(palette)
                        return
                    else:
                        self.ui.btn_Design.setDisabled(False)
                        palette = QPalette()
                        lblwidget.setPalette(palette)

    def show_font_dialog(self):

        font, ok = QFontDialog.getFont()
        if ok:
            # self.ui.inputDock.setFont(font)
            # self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)

    def show_color_dialog(self):

        col = QColorDialog.getColor()
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

    def save_cadImages(self):
        status = self.resultObj['Bolt']['status']
        if status is True:

            files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
            fileName,_ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"), files_types)
            fName = str(fileName)
            file_extension = fName.split(".")[-1]

            if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp'or file_extension == 'tiff' :
                self.display.ExportToImage(fName)
                QMessageBox.about(self, 'Information', "File saved")
        else:
            self.ui.actionSave_CAD_image.setEnabled(False)

            QMessageBox.about(self,'Information', 'Design Unsafe: CAD image cannot be viewed')


    def disable_view_buttons(self):
        '''
        Disables the all buttons in toolbar
        '''
        self.ui.actionSave_input.setEnabled(False)
        self.ui.actionSave_log_message.setEnabled(False)
        self.ui.actionCreate_design_report.setEnabled(False)
        self.ui.actionSave_3D_model.setEnabled(False)
        self.ui.actionSave_CAD_image.setEnabled(False)
        self.ui.actionSave_Front_View.setEnabled(False)
        self.ui.actionSave_Top_View.setEnabled(False)
        self.ui.actionSave_Side_View.setEnabled(False)
        self.ui.menuGraphics.setEnabled(False)

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

        # self.ui.menubar.setEnabled(True)
        self.ui.menuFile.setEnabled(True)
        self.ui.actionSave_input.setEnabled(True)
        self.ui.actionSave_log_message.setEnabled(True)
        self.ui.actionCreate_design_report.setEnabled(True)
        self.ui.actionSave_3D_model.setEnabled(True)
        self.ui.actionSave_CAD_image.setEnabled(True)
        self.ui.actionSave_Front_View.setEnabled(True)
        self.ui.actionSave_Top_View.setEnabled(True)
        self.ui.actionSave_Side_View.setEnabled(True)

        self.ui.menuEdit.setEnabled(True)
        self.ui.menuView.setEnabled(True)
        self.ui.menuGraphics.setEnabled(True)

        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.checkBoxCleat.setEnabled(True)

    def unchecked_all_checkbox(self):

        self.ui.btn3D.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.checkBoxCleat.setChecked(Qt.Unchecked)

    def retrieve_prevstate(self):
        ui_obj = self.get_prevstate()
        self.setDictToUserInputs(ui_obj)

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

        # yaml.dump(self.uiObj,out_file,allow_unicode=True, default_flow_style=False)
        json.dump(self.uiObj, out_file)

        out_file.close()

        pass

    def openDesign_inputs(self):

        fileName, _ = QFileDialog.getOpenFileName(self, "Open Design", str(self.folder), "(*.osi)")
        if not fileName:
            return
        try:
            in_file = open(str(fileName), 'rb')

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return
        uiObj = json.load(in_file)
        self.setDictToUserInputs(uiObj)


    def setDictToUserInputs(self, uiObj):

        if (uiObj is not None):

            if uiObj["Connection"] != "cleatAngle":
                QMessageBox.information(self, "Information", "You can load this input file only from the corresponding design problem")
                return

            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))

            if uiObj['Member']['Connectivity'] == 'Beam-Beam':

                self.ui.beamSection_lbl.setText('Secondary beam *')
                self.ui.columnSection_lbl.setText('Primary beam *')
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
            comboTypeIndex = self.ui.comboBoltType.findText(str(uiObj['Bolt']['Type']))
            self.ui.comboBoltType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))

            prevValue = str(uiObj['Bolt']['Grade'])

            comboGradeIndex = self.ui.comboBoltGrade.findText(prevValue)

            self.ui.comboBoltGrade.setCurrentIndex(comboGradeIndex)

            selection = str(uiObj['cleat']['Height (mm)'])
            self.ui.txtInputCleatHeight.setText(selection)
            cleat_section = str(uiObj['cleat']['section'])
            self.ui.comboCleatSection.setCurrentIndex(self.ui.comboCleatSection.findText(cleat_section))

            self.designPrefDialog.ui.combo_boltHoleType.setCurrentIndex(self.designPrefDialog.ui.combo_boltHoleType.findText(uiObj["bolt"]["bolt_hole_type"]))
            self.designPrefDialog.ui.txt_boltFu.setText(str(uiObj["bolt"]["bolt_fu"]))
            self.designPrefDialog.ui.combo_slipfactor.setCurrentIndex(self.designPrefDialog.ui.combo_slipfactor.findText(str(uiObj["bolt"]["slip_factor"])))
            self.designPrefDialog.ui.combo_weldType.setCurrentIndex(self.designPrefDialog.ui.combo_weldType.findText(uiObj["weld"]["typeof_weld"]))
            self.designPrefDialog.ui.combo_detailingEdgeType.setCurrentIndex(self.designPrefDialog.ui.combo_detailingEdgeType.findText(uiObj["detailing"]["typeof_edge"]))
            self.designPrefDialog.ui.combo_detailing_memebers.setCurrentIndex(self.designPrefDialog.ui.combo_detailing_memebers.findText(uiObj["detailing"]["is_env_corrosive"]))
            self.designPrefDialog.ui.txt_detailingGap.setText(str(uiObj["detailing"]["gap"]))

        else:
            pass

    def getuser_inputs(self):
        '''(nothing) -> Dictionary
        Returns the dictionary object with the user input fields for designing cleat angle connection
        '''
        ui_obj = {}
        ui_obj["Bolt"] = {}
        ui_obj["Bolt"]["Diameter (mm)"] = str(self.ui.comboDiameter.currentText())
        ui_obj["Bolt"]["Grade"] = (self.ui.comboBoltGrade.currentText())
        ui_obj["Bolt"]["Type"] = str(self.ui.comboBoltType.currentText())

        ui_obj['Member'] = {}
        ui_obj['Member']['BeamSection'] = str(self.ui.combo_Beam.currentText())
        ui_obj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        ui_obj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        ui_obj['Member']['fu (MPa)'] = self.ui.txtFu.text()
        ui_obj['Member']['fy (MPa)'] = self.ui.txtFy.text()

        ui_obj['cleat'] = {}
        ui_obj['cleat']['section'] = str(self.ui.comboCleatSection.currentText())
        ui_obj['cleat']['Height (mm)'] = str(self.ui.txtInputCleatHeight.text())  # changes the label length to height

        ui_obj['Load'] = {}
        ui_obj['Load']['ShearForce (kN)'] = (self.ui.txtShear.text())
        ui_obj["Connection"] = self.connection

        return ui_obj

    def save_inputs(self, ui_obj):
        '''
        (Dictionary)--> None
        '''
        inputFile = QFile(os.path.join("Connections", "Shear","cleatAngle", "saveINPUT.txt"))
        if not inputFile.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        pickle.dump(ui_obj, inputFile)

    def get_prevstate(self):
        '''
        '''
        filename = os.path.join("Connections", "Shear", "cleatAngle", "saveINPUT.txt")
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

        status = self.resultObj['Bolt']['status']
        if status is True:
            self.call_3d_model("white_bg")
            data = os.path.join(str(self.folder), "images_html", "3D_Model.png")
            self.display.ExportToImage(data)
            self.display.FitAll()
        else:
            pass

        fileName = os.path.join(self.folder, "images_html","Html_Report.html")
        fileName = str(fileName)
        self.commLogicObj.call_designReport(fileName, popup_summary)
        # Creates pdf

        config = ConfigParser.ConfigParser()
        config.readfp(open(r'Osdag.config'))
        wkhtmltopdf_path = config.get('wkhtml_path', 'path1')

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
        """
        Save log messages in user prefered text file at user prefered location.
        Returns: (File) save_file

        """
        filename, pat = QFileDialog.getSaveFileName(self, "Save File As", os.path.join(str(self.folder),  "Logmessages"), "Text files (*.txt)")
        return self.save_file(filename + ".txt")


    def save_file(self, filename):
        '''(file open for writing)-> boolean
        '''
        fname = QFile(filename)

        if not fname.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                      "Cannot write file %s:\n%s." % (filename, fname.errorString()))
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
        self.ui.comboBoltType.setCurrentIndex((0))
        self.ui.comboBoltGrade.setCurrentIndex((0))

        self.ui.comboCleatSection.setCurrentIndex((0))
        self.ui.txtInputCleatHeight.clear()

        self.ui.txtNoBolts.clear()
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

        self.ui.outputCleatHeight.clear()
        self.ui.textEdit.clear()

        self.display.EraseAll()
        self.designPrefDialog.set_default_para()
        self.disable_view_buttons()


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

        '''(QlineEdit,QLabel,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        text_str = widget.text()

        val = float(text_str)
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

        shear_capacity = result_obj['Bolt']['shearcapacity']


        bearing_capacity = result_obj['Bolt']['bearingcapacity']

        bolt_capacity = result_obj['Bolt']['boltcapacity']

        no_ofbolts = result_obj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        # newly added field
        bolt_grp_capacity = result_obj['Bolt']['boltgrpcapacity']

        no_ofrows = result_obj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))

        no_ofcol = result_obj['Bolt']['numofcol']
        self.ui.txt_column.setText(str(no_ofcol))

        pitch_dist = result_obj['Bolt']['pitch']
        self.ui.txtBeamPitch.setText(str(pitch_dist))

        gauge_dist = result_obj['Bolt']['gauge']
        self.ui.txtBeamGuage.setText(str(gauge_dist))

        edge_dist = result_obj['Bolt']['edge']
        self.ui.txtEdgeDist.setText(str(edge_dist))

        end_dist = result_obj['Bolt']['enddist']
        self.ui.txtEndDist.setText(str(end_dist))

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

        edge_dist = result_obj['cleat']['edge']
        self.ui.txtEdgeDist_c.setText(str(edge_dist))

        end_dist = result_obj['cleat']['end']
        self.ui.txtEndDist_c.setText(str(end_dist))

        cleat_ht = result_obj['cleat']['height']
        self.ui.outputCleatHeight.setText(str(cleat_ht))


        moment_demand = result_obj['cleat']['externalmoment']

        moment_capacity = result_obj['cleat']['momentcapacity']

    def displaylog_totextedit(self,commLogicObj):
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

    # QtViewer
    def init_display(self, backend_str=None, size=(1024, 768)):
        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        from OCC.Display.qtDisplay import qtViewer3d
        self.ui.modelTab = qtViewer3d(self)

        self.setWindowTitle("Osdag Cleat Angle")
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab, "")

        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display
        # background gradient
        display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        display.display_trihedron()
        display.View.SetProj(1, 1, 1)

        def center_on_screen(self):
                    '''Centers the window on the screen.'''
                    resolution = QDesktopWidget().screenGeometry()
                    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                              (resolution.height() / 2) - (self.frameSize().height() / 2))

        def start_display():

            self.ui.modelTab.raise_()

        return display, start_display

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

    def validate_inputs_on_design_button(self):
        flag = True
        incomplete_list = []

        if self.ui.comboConnLoc.currentIndex() == 0:
            incomplete_list.append("Connectivity")
            flag = False
            QMessageBox.information(self, "Information", self.generate_incomplete_string(incomplete_list))
            return flag

        state = self.setimage_connection()
        if state is True:
            if self.ui.comboConnLoc.currentText() == "Column web-Beam web" or self.ui.comboConnLoc.currentText() == "Column flange-Beam web":
                if self.ui.comboColSec.currentIndex() == 0:
                    incomplete_list.append("Column section")
                    # QMessageBox.information(self, "Information", "Please select column section")
                    # flag = False

                if self.ui.combo_Beam.currentIndex() == 0:
                    incomplete_list.append("Beam section")
                    # QMessageBox.information(self, "Information", "Please select beam section")
                    # flag = False
            else:
                if self.ui.comboColSec.currentIndex() == 0:
                    incomplete_list.append("Primary beam section")
                    # QMessageBox.information(self, "Information", "Please select Primary beam  section")
                    # flag = False
                if self.ui.combo_Beam.currentIndex() == 0:
                    incomplete_list.append("Secondary beam section")
                    # QMessageBox.information(self, "Information", "Please select Secondary beam  section")
                    # flag = False
        if self.ui.txtFu.text()== '' or float(self.ui.txtFu.text()) == 0:
            incomplete_list.append("Ultimate strength of steel")
            # QMessageBox.information(self, "Information", "Please select Ultimate strength of  steel")
            # flag = False

        if self.ui.txtFy.text()== '' or float(self.ui.txtFy.text()) == 0:
            incomplete_list.append("Yield strength of steel")
            # QMessageBox.information(self, "Information", "Please select Yeild  strength of  steel")
            # flag = False

        if self.ui.txtShear.text()== '' or str(self.ui.txtShear.text())== 0:
            incomplete_list.append("Factored shear load")
            # reply = QMessageBox.information(self, "Information", "Please select Factored shear load")
            # flag = False

        if self.ui.comboDiameter.currentIndex() == 0:
            incomplete_list.append("Diameter of bolt")
            # QMessageBox.information(self, "Information", "Please select Diameter of  bolt")
            # flag = False

        if self.ui.comboBoltType.currentIndex() == 0:
            incomplete_list.append("Type of bolt")
            # QMessageBox.information(self, "Information", "Please select Type of  bolt")
            # flag = False
        if self.ui.comboCleatSection.currentIndex() == 0:
            incomplete_list.append("Cleat angle")
            # QMessageBox.information(self, "Information", "Please select Cleat angle")
            # flag = False

        if len(incomplete_list) > 0:
            flag = False
            QMessageBox.information(self, "Information", self.generate_incomplete_string(incomplete_list))

        if flag:
            flag = self.checkbeam_b()

        return flag

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


    def call_3d_model(self,bgcolor):
        """

        :return:
        """
        self.ui.btn3D.setChecked(Qt.Checked)
        if self.ui.btn3D.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(Qt.Unchecked)
        self.commLogicObj.display_3DModel("Model",bgcolor)


    def call_3d_beam(self,bgcolor):
        '''
        Creating and displaying 3D Beam
        '''
        self.ui.chkBxBeam.setChecked(Qt.Checked)
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)

        self.commLogicObj.display_3DModel("Beam",bgcolor)



    def call_3d_column(self,bgcolor):
        """

        :return:
        """
        self.ui.chkBxCol.setChecked(Qt.Checked)
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.checkBoxCleat.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("Column",bgcolor)


    def call_3d_cleatangle(self,bgcolor):
        '''Displaying FinPlate in 3D
        '''
        self.ui.checkBoxCleat.setChecked(Qt.Checked)
        if self.ui.checkBoxCleat.isChecked():
            self.ui.chkBxBeam.setChecked(Qt.Unchecked)
            self.ui.chkBxCol.setChecked(Qt.Unchecked)
            self.ui.btn3D.setChecked(Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
        self.commLogicObj.display_3DModel("cleatAngle",bgcolor)


    def designParameters(self):
        '''
        This routine returns the neccessary design parameters.
        '''
        self.uiObj = self.getuser_inputs()
        # if self.designPrefDialog.saved is not True:
        #     design_pref = self.designPrefDialog.set_default_para()
        # else:
        design_pref = self.designPrefDialog.save_designPref_para()
        self.uiObj.update(design_pref)
        return self.uiObj

    def parameters(self):
        self.uiObj = self.getuser_inputs()

        dictbeamdata = self.fetch_beam_param()
        dictcoldata = self.fetch_column_param()
        dictangledata = self.fetch_angle_param()
        dict_topangledata = {}

        loc = str(self.ui.comboConnLoc.currentText())
        component = "Model"
        bolt_dia = int(self.uiObj["Bolt"]["Diameter (mm)"])
        bolt_R = self.bolt_head_dia_calculation(bolt_dia) / 2
        bolt_T = self.bolt_head_thick_calculation(bolt_dia)
        bolt_Ht = self.bolt_length_calculation(bolt_dia)
        nut_T = self.nut_thick_calculation(bolt_dia)  # bolt_dia = nut_dia
        return [dictbeamdata, dictcoldata,dictangledata, dict_topangledata, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T]

    def design_btnclicked(self):
        '''
        '''

        self.display.EraseAll()

        if self.validate_inputs_on_design_button() is not True:
            return
        self.alist = self.parameters()
        designpreference = self.designParameters()
        print "uiobj=:",self.alist[0]

        self.ui.outputDock.setFixedSize(310, 710)
        self.enable_view_buttons()
        self.unchecked_all_checkbox()
        self.commLogicObj = CommonDesignLogic(designpreference, self.alist[0], self.alist[1], self.alist[2], self.alist[3], self.alist[4],
                                              self.alist[5], self.alist[6],self.alist[7], self.alist[8], self.alist[9],
                                              self.display, self.folder, self.connection)

        self.resultObj = self.commLogicObj.resultObj
        alist = self.resultObj.values()
        self.display_output(self.resultObj)
        self.displaylog_totextedit(self.commLogicObj)
        isempty = [True if val != '' else False for ele in alist for val in ele.values()]

        if isempty[0] == True:
            status = self.resultObj['Bolt']['status']
            self.commLogicObj.call_3DModel(status)
            if status is True:
                self.callCleat2D_drawing("All")
                self.ui.actionShow_all.setEnabled(True)
                self.ui.actionShow_beam.setEnabled(True)
                self.ui.actionShow_column.setEnabled(True)
                self.ui.actionShow_cleat_angle.setEnabled(True)
            else:
                self.ui.btn3D.setEnabled(False)
                self.ui.chkBxBeam.setEnabled(False)
                self.ui.chkBxCol.setEnabled(False)
                self.ui.checkBoxCleat.setEnabled(False)
                self.ui.actionShow_all.setEnabled(False)
                self.ui.actionShow_beam.setEnabled(False)
                self.ui.actionShow_column.setEnabled(False)
                self.ui.actionShow_cleat_angle.setEnabled(False)

        else:
            pass

        self.designPrefDialog.saved = False
    def create2Dcad(self):
        ''' Returns the 3D model of finplate depending upon component
        '''
        if self.commLogicObj.component == "Beam":
            final_model = self.commLogicObj.connectivityObj.get_beamModel()

        elif self.commLogicObj.component == "Column":
            final_model = self.commLogicObj.connectivityObj.get_columnModel()

        elif self.commLogicObj.component == "cleatAngle":
            cadlist = [self.commLogicObj.connectivityObj.angleModel,
                       self.commLogicObj.connectivityObj.angleLeftModel] + self.commLogicObj.connectivityObj.nut_bolt_array.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()
        else:
            cadlist = self.commLogicObj.connectivityObj.get_models()
            # cadlist = [self.commLogicObj.connectivityObj.angleModel,
            #            self.commLogicObj.connectivityObj.angleLeftModel] + self.commLogicObj.connectivityObj.nut_bolt_array.get_models()
            final_model = cadlist[0]
            for model in cadlist[1:]:
                final_model = BRepAlgoAPI_Fuse(model, final_model).Shape()

        return final_model


    def save_3d_cad_images(self):
        """
        Export to IGS,STEP,STL,BREP
        """
        status = self.resultObj['Bolt']['status']
        if status is True:

            if self.fuse_model is None:
                self.fuse_model = self.create2Dcad()
            shape = self.fuse_model

            files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"

            fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"), files_types)
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

    def call_desired_view(self, filename, view):
        """

        :param filename: string
        :param view:
        :return:
        """

        self. unchecked_all_checkbox()

        ui_obj = self.getuser_inputs()
        result_obj = cleat_connection(ui_obj)
        dict_beam_data = self.fetch_beam_param()
        dict_column_data = self.fetch_column_param()
        dict_angle_data = self.fetch_angle_param()
        fin_common_obj = cleatCommonData(ui_obj, result_obj, dict_beam_data, dict_column_data, dict_angle_data, self.folder)
        fin_common_obj.save_to_svg(str(filename), view)

    def callCleat2D_drawing(self, view):

        ''' This routine saves the 2D SVG image as per the connectivity selected
        SVG image created through svgwrite package which takes design INPUT and OUTPUT parameters from CleatAngle GUI.
        '''
        self.ui.checkBoxCleat.setChecked(Qt.Unchecked)
        self.ui.chkBxBeam.setChecked(Qt.Unchecked)
        self.ui.chkBxCol.setChecked(Qt.Unchecked)
        self.ui.btn3D.setChecked(Qt.Unchecked)
        status = self.resultObj['Bolt']['status']
        if status is True:

            if view != 'All':

                if view == "Front":
                    filename = os.path.join(self.folder, "images_html", "cleatFront.svg")

                elif view == "Side":
                    filename = os.path.join(self.folder, "images_html", "cleatSide.svg")

                else:
                    filename = os.path.join(self.folder, "images_html", "cleatTop.svg")

                svg_file = SvgWindow()
                svg_file.call_svgwindow(filename, view, self.folder)

            else:
                fname = ''
                self.commLogicObj.call2D_Drawing(view, fname, self.folder)
        else:
            QMessageBox.about(self,'Information', 'Design Unsafe: %s view cannot be saved' %(view))


    def closeEvent(self, event):
        '''
        Closing finPlate window.
        '''
        # ui_input = self.getuser_inputs()
        ui_input = self.designParameters()
        self.save_inputs(ui_input)
        reply = QMessageBox.question(self, 'Message',
                                           "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

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
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, "%s/%s" % (root_path, html_file)])

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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/cleat.log", mode="a")

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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/cleat.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/cleatAngle/log.css"/>''')

    # app = QApplication(sys.argv)
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
    fh = logging.FileHandler("Connections/Shear/cleatAngle/cleat.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    raw_logger.addHandler(fh)
    raw_logger.info('''<link rel="stylesheet" type="text/css" href="Connections/Shear/cleatAngle/log.css"/>''')

    app = QApplication(sys.argv)
    module_setup()
    ########################################
    workspace_folder_path = "D:\Osdag_Workspace\Cleatangle"
    if not os.path.exists(workspace_folder_path):
        os.mkdir(workspace_folder_path, 0755)
    image_folder_path = os.path.join(workspace_folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0755)
    window = MainController(workspace_folder_path)
    ########################################
    window = MainController(workspace_folder_path)
    window.show()
    sys.exit(app.exec_())
