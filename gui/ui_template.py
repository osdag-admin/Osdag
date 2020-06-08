# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/gui/ui_template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!\
from PyQt5.QtWidgets import QMessageBox, qApp, QScrollArea
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice,pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from design_report import reportGenerator
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush, QImage
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QDialogButtonBox
from design_type.connection.column_cover_plate import ColumnCoverPlate
from PyQt5.QtGui import QStandardItem
import os
import yaml
import json
import logging
from drawing_2D.Svg_Window import SvgWindow
import sys
import sqlite3
import shutil
import openpyxl
import pdfkit
import configparser
import pickle
import cairosvg


from Common import *
from utils.common.component import Section,I_sectional_Properties
from utils.common.component import *
from .customized_popup import Ui_Popup
# from .ui_summary_popup import Ui_Dialog1
from .ui_design_preferences import Ui_Dialog

from gui.ui_summary_popup import Ui_Dialog1
from design_report.reportGenerator import save_html
#from .ui_design_preferences import DesignPreferences
from .UI_DESIGN_PREFERENCE import DesignPreferences
from design_type.connection.shear_connection import ShearConnection
from cad.common_logic import CommonDesignLogic
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core import BRepTools
from OCC.Core import IGESControl
from cad.cad3dconnection import cadconnection
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.column_cover_plate import ColumnCoverPlate
from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.seated_angle_connection import SeatedAngleConnection
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.beam_cover_plate import BeamCoverPlate
from design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from design_type.connection.beam_end_plate import BeamEndPlate
from design_type.connection.column_end_plate import ColumnEndPlate
from design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from design_type.connection.base_plate_connection import BasePlateConnection
from design_type.tension_member.tension_bolted import Tension_bolted
from design_type.tension_member.tension_welded import Tension_welded

from cad.cad3dconnection import cadconnection

class Ui_ModuleWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    closed = pyqtSignal()
    def  __init__(self, main,folder,parent=None):
        super(Ui_ModuleWindow, self).__init__(parent=parent)
        self.ui = Window()
        self.ui.setupUi(self,main,folder)
        #self.showMaximized()
        self.resized.connect(self.resize_dockComponents)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Ui_ModuleWindow, self).resizeEvent(event)

    def resize_dockComponents(self):

        posi = (3/4)*(self.height())

        # Input Dock
        width = self.ui.inputDock.width()
        self.ui.inputDock.resize(width,self.height())
        self.ui.in_widget.resize(width,posi)

        self.ui.btn_Reset.move((width/2)-110,posi+8)
        self.ui.btn_Design.move((width/2)+17,posi+8)
        #self.ui.btn_Design.move(,posi+10)

        # Output Dock
        width = self.ui.outputDock.width()
        self.ui.outputDock.resize(width,self.height())
        self.ui.out_widget.resize(width,posi)
        self.ui.btn_CreateDesign.move((width/2)-168,posi+8)
        self.ui.save_outputDock.move((width/2)+28,posi+8)

    def closeEvent(self, event):
        '''
        Closing module window.
        '''
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore()

class Window(QMainWindow):
    #closed = pyqtSignal()

    def open_customized_popup(self, op, KEYEXISTING_CUSTOMIZED):
        """
        Function to connect the customized_popup with the ui_template file
        on clicking the customized option
        """

        # @author : Amir


        self.window = QtWidgets.QDialog()
        self.ui = Ui_Popup()
        self.ui.setupUi(self.window)
        self.ui.addAvailableItems(op, KEYEXISTING_CUSTOMIZED)
        self.window.exec()
        return self.ui.get_right_elements()

    def open_summary_popup(self, main):

        if not main.design_button_status:
            QMessageBox.warning(QMessageBox(), 'Warning', 'No design created!')
            return

        self.new_window = QtWidgets.QDialog()
        self.new_ui = Ui_Dialog1(self.design_exist)
        self.new_ui.setupUi(self.new_window, main)
        self.new_ui.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.new_window, self.new_ui.lbl_browse))
        self.new_ui.btn_saveProfile.clicked.connect(lambda: self.saveUserProfile(self.new_window))
        self.new_ui.btn_useProfile.clicked.connect(lambda: self.useUserProfile(self.new_window))
        self.new_window.exec()
        # self.new_ui.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.new_ui.lbl_browse))
        # self.new_ui.btn_saveProfile.clicked.connect(self.saveUserProfile)
        # self.new_ui.btn_useProfile.clicked.connect(self.useUserProfile)

    def getLogoFilePath(self, window, lblwidget):

        filename, _ = QFileDialog.getOpenFileName(window, "Open Image", os.path.join(str(' '), ''), "InputFiles(*.png *.svg *.jpg)")

        # filename, _ = QFileDialog.getOpenFileName(
        #     self, 'Open File', " ../../",
        #     'Images (*.png *.svg *.jpg)',
        #     None, QFileDialog.DontUseNativeDialog)
        if filename == '':
            return False
        else:
            # base = os.path.basename(str(filename))
            lblwidget.setText(str(filename))
            # base_type = base[-4:]
            # self.desired_location(filename, base_type)

        return str(filename)

    def desired_location(self, filename, base_type):
        if base_type == ".svg":
            cairosvg.svg2png(file_obj=filename,
                             write_to=os.path.join(str(self.folder), "images_html", "cmpylogoFin.png"))
        else:
            shutil.copyfile(filename, os.path.join(str(self.folder), "images_html", "cmpylogoFin.png"))

    def saveUserProfile(self, window):

        inputData = self.getPopUpInputs()
        filename, _ = QFileDialog.getSaveFileName(window, 'Save Files',
                                                  os.path.join(str(self.folder), "Profile"), '*.txt')
        if filename == '':
            return False
        else:
            infile = open(filename, 'w')
            yaml.dump(inputData, infile)
            infile.close()

    def getPopUpInputs(self):
        input_summary = {}
        input_summary["ProfileSummary"] = {}
        input_summary["ProfileSummary"]["CompanyName"] = str(self.new_ui.lineEdit_companyName.text())
        input_summary["ProfileSummary"]["CompanyLogo"] = str(self.new_ui.lbl_browse.text())
        input_summary["ProfileSummary"]["Group/TeamName"] = str(self.new_ui.lineEdit_groupName.text())
        input_summary["ProfileSummary"]["Designer"] = str(self.new_ui.lineEdit_designer.text())

        # input_summary["ProjectTitle"] = str(self.new_ui.lineEdit_projectTitle.text())
        # input_summary["Subtitle"] = str(self.new_ui.lineEdit_subtitle.text())
        # input_summary["JobNumber"] = str(self.new_ui.lineEdit_jobNumber.text())
        # input_summary["AdditionalComments"] = str(self.new_ui.txt_additionalComments.toPlainText())
        # input_summary["Client"] = str(self.new_ui.lineEdit_client.text())

        return input_summary

    def useUserProfile(self, window):

        filename, _ = QFileDialog.getOpenFileName(window, 'Open Files',
                                                  os.path.join(str(self.folder), "Profile"),
                                                  '*.txt')
        if os.path.isfile(filename):
            outfile = open(filename, 'r')
            reportsummary = yaml.load(outfile)
            self.new_ui.lineEdit_companyName.setText(reportsummary["ProfileSummary"]['CompanyName'])
            self.new_ui.lbl_browse.setText(reportsummary["ProfileSummary"]['CompanyLogo'])
            self.new_ui.lineEdit_groupName.setText(reportsummary["ProfileSummary"]['Group/TeamName'])
            self.new_ui.lineEdit_designer.setText(reportsummary["ProfileSummary"]['Designer'])

        else:
            pass

    def zoom_model(self, zoom_type="in"):
        if zoom_type == "in":
            self.display.ZoomFactor(3)
        elif zoom_type == "out":
            self.display.ZoomFactor(1/3)
        else:
            self.display.ZoomFactor(0)


    def get_validator(self, validator):
        if validator == 'Int Validator':
            return QIntValidator()
        elif validator == 'Double Validator':
            return QDoubleValidator()
        else:
            return None

    def setupUi(self, MainWindow, main,folder):
        self.design_inputs = {}
        self.prev_inputs = {}
        self.input_dock_inputs = {}
        self.design_pref_inputs = {}
        self.folder = folder
        main.design_status = False
        main.design_button_status = False
        MainWindow.setObjectName("MainWindow")

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
        self.frame.setObjectName("frame_")

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
        #self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        #self.pushButton.setGeometry(QtCore.QRect(440, 412, 111, 51))
        #self.pushButton.setObjectName("pushButton")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/images/output.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOutput.setIcon(icon2)
        self.btnOutput.setIconSize(QtCore.QSize(18, 18))
        self.btnOutput.setObjectName("btnOutput")

        self.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.inputDock))
        self.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.outputDock))

        self.btnTop = QtWidgets.QToolButton(self.frame)
        self.btnTop.setGeometry(QtCore.QRect(160, 0, 28, 28))
        self.btnTop.setFocusPolicy(QtCore.Qt.TabFocus)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/images/X-Y.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTop.setIcon(icon3)
        self.btnTop.setIconSize(QtCore.QSize(22, 22))
        self.btnTop.setObjectName("btnTop")
        self.btnTop.setEnabled(False)
        self.btnFront = QtWidgets.QToolButton(self.frame)
        self.btnFront.setGeometry(QtCore.QRect(100, 0, 28, 28))
        self.btnFront.setFocusPolicy(QtCore.Qt.TabFocus)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/images/Z-X.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFront.setIcon(icon4)
        self.btnFront.setIconSize(QtCore.QSize(22, 22))
        self.btnFront.setObjectName("btnFront")
        self.btnFront.setEnabled(False)
        self.btnSide = QtWidgets.QToolButton(self.frame)
        self.btnSide.setGeometry(QtCore.QRect(130, 0, 28, 28))
        self.btnSide.setFocusPolicy(QtCore.Qt.TabFocus)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/images/Z-Y.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSide.setIcon(icon5)
        self.btnSide.setIconSize(QtCore.QSize(22, 22))
        self.btnSide.setObjectName("btnSide")
        self.btnSide.setEnabled(False)
        """
            To get 3d component checkbox details from modules
        """
        i = 0
        for component in main.get_3d_components(main):
            checkBox = QtWidgets.QCheckBox(self.frame)
            checkBox.setGeometry(QtCore.QRect(230 + i, 0, 110, 29))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            checkBox.setFont(font)
            checkBox.setFocusPolicy(QtCore.Qt.TabFocus)
            checkBox.setObjectName(component[0])
            checkBox.setText(component[0])
            checkBox.setDisabled(True)
            function_name = component[1]
            self.chkbox_connect(main, checkBox, function_name)
            checkBox.resize(checkBox.sizeHint())
            i += (checkBox.sizeHint().width() + 5)

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
        self.mytabWidget.setTabPosition(QtWidgets.QTabWidget.East)
        self.mytabWidget.setObjectName("mytabWidget")
        self.verticalLayout.addWidget(self.mytabWidget)
        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 125))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit.setReadOnly(True)
        self.textEdit.setOverwriteMode(True)
        self.textEdit.setObjectName("textEdit")

        main.set_osdaglogger(self.textEdit)
        # self.textEdit.setStyleSheet("QTextEdit {color:red}")
        self.verticalLayout_2.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1328, 21))
        self.menubar.setStyleSheet("")
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)

        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)

        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)

        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)

        self.menuHelp.setObjectName("menuHelp")
        self.menuGraphics = QtWidgets.QMenu(self.menubar)

        self.menuGraphics.setObjectName("menuGraphics")
        MainWindow.setMenuBar(self.menubar)

        ####################################################################
        # INPUT DOCK
        #####################################################################
        # @author : Umair

        self.inputDock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputDock.sizePolicy().hasHeightForWidth())
        #self.inputDock.setSizePolicy(sizePolicy)
        #self.inputDock.setMinimumSize(QtCore.QSize(320, 710))
        #self.inputDock.setMaximumSize(QtCore.QSize(310, 710))
        #self.inputDock.setBaseSize(QtCore.QSize(310, 710))
        #self.inputDock.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
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

        self.in_widget = QtWidgets.QWidget(self.dockWidgetContents)
        #sself.in_widget.setGeometry(QtCore.QRect(0, 0, 325, 600))
        in_layout1 = QtWidgets.QVBoxLayout(self.in_widget)
        in_scroll = QScrollArea(self.in_widget)
        in_layout1.addWidget(in_scroll)
        in_scroll.setWidgetResizable(True)
        in_scrollcontent = QtWidgets.QWidget(in_scroll)
        in_layout2 = QtWidgets.QGridLayout(in_scrollcontent)
        in_scrollcontent.setLayout(in_layout2)
        #in_scroll.horizontalScrollBar().hide()
        in_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        in_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)


        """
        This routine takes the returned list from input_values function of corresponding module
        and creates the specified QT widgets, [Ref input_values function is any module for details]
        """
        option_list = main.input_values(self)
        _translate = QtCore.QCoreApplication.translate

        i = 0
        j = 1
        maxi_width_left, maxi_width_right = -1, -1
        for option in option_list:
            lable = option[1]
            type = option[2]
            if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE, TYPE_IMAGE_COMPRESSION]:
                l = QtWidgets.QLabel(self.dockWidgetContents)

                # if option[0] in [KEY_MOMENT_MAJOR, KEY_MOMENT_MINOR] and module == KEY_DISP_BASE_PLATE:
                #     l.setGeometry(QtCore.QRect(16, 10 + i, 120, 25))
                # else:
                #l.setGeometry(QtCore.QRect(6, 10 + i, 120, 25))

                #l.setGeometry(QtCore.QRect(6, 10 + i, 120, 25))

                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(option[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                #l.setFixedSize(l.size())
                in_layout2.addWidget(l, j, 1, 1, 1)
                metrices = QtGui.QFontMetrics(font)
                maxi_width_left = max(maxi_width_left, metrices.boundingRect(lable).width() + 8)


            if type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
                combo = QtWidgets.QComboBox(self.dockWidgetContents)
                #combo.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(option[0])

                metrices = QtGui.QFontMetrics(font)
                item_width = 10

                for item in option[3]:

                    combo.addItem(item)
                    item_width = max(item_width, metrices.boundingRect(item).width())
                in_layout2.addWidget(combo, j, 2, 1, 1)

                if lable == 'Material *':
                    maxi_width_right = max(maxi_width_right, item_width+5)
                else:
                    combo.view().setMinimumWidth(item_width + 25)

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.dockWidgetContents)
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(option[0])
                # if option[0] in [KEY_MOMENT_MAJOR, KEY_MOMENT_MINOR] and module == KEY_DISP_BASE_PLATE:
                #     r.setGeometry(QtCore.QRect(160, 10 + i, 150, 27))
                #     r.setDisabled(True)
                # else:

                #r.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                r.setEnabled(True if option[4] else False)
                if option[5] != 'No Validator':
                    r.setValidator(self.get_validator(option[5]))
                #r.setFixedSize(r.size())

                # if option[0] in [KEY_MOMENT_MAJOR, KEY_MOMENT_MINOR, KEY_AXIAL_TENSION_BP] and module == KEY_DISP_BASE_PLATE:
                #     r.setGeometry(QtCore.QRect(160, 10 + i, 150, 27))
                #     r.setDisabled(True)
                # else:
                #     r.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                # r.setFixedSize(r.size())

                in_layout2.addWidget(r, j, 2, 1, 1)
                #maxi_width_right = max(maxi_width_right, 120)

            if type == TYPE_MODULE:
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", option[1]))
                i = i - 30
                module = lable
                j = j - 1

            if type == TYPE_NOTE:
                l = QtWidgets.QLineEdit(self.dockWidgetContents)
                l.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(True)
                font.setWeight(50)
                l.setFont(font)
                l.setAlignment(Qt.AlignHCenter)
                l.setObjectName(option[0] + "_note")
                # l.setText(_translate("MainWindow", "<html><head/><body><p>" + option[4] + "</p></body></html>"))
                l.setText(option[3])
                l.setReadOnly(True)
                l.setFixedSize(l.size())
                in_layout2.addWidget(l, j, 2, 1, 1)

            if type == TYPE_IMAGE:
                im = QtWidgets.QLabel(self.dockWidgetContents)
                im.setGeometry(QtCore.QRect(190, 10 + i, 70, 57))
                im.setObjectName(option[0])
                im.setScaledContents(True)
                pixmap = QPixmap(option[3])
                im.setPixmap(pixmap)
                i = i + 30
                im.setFixedSize(im.size())
                in_layout2.addWidget(im, j, 2, 1, 1)

            if type == TYPE_IMAGE_COMPRESSION:
                imc = QtWidgets.QLabel(self.dockWidgetContents)
                imc.setGeometry(QtCore.QRect(130, 10 + i, 160, 150))
                imc.setObjectName(option[0])
                imc.setScaledContents(True)
                pixmapc = QPixmap(option[3])
                imc.setPixmap(pixmapc)
                i = i + 30
                imc.setFixedSize(imc.size())
                in_layout2.addWidget(imc, j, 2, 1, 1)

# <<<<<<< HEAD
# =======
#             if option[0] in [KEY_AXIAL, KEY_AXIAL_BP, KEY_SHEAR]:
#                 key = self.dockWidgetContents.findChild(QtWidgets.QWidget, option[0])
#                 onlyInt = QIntValidator()
#                 key.setValidator(onlyInt)
#
# >>>>>>> 436f627ed59112463791456e6d1eceb9749f6d4c
            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.dockWidgetContents)
                #q.setGeometry(QtCore.QRect(3, 10 + i, 201, 25))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setWeight(65)
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))
                q.setFixedSize(q.sizeHint().width(), q.sizeHint().height())
                in_layout2.addWidget(q, j, 1, 2, 2)
                j = j + 1

            i = i + 30
            j = j + 1
        in_layout2.setRowStretch(j+1, 10)
        in_scroll.setWidget(in_scrollcontent)

        maxi_width = maxi_width_left + maxi_width_right
        print(maxi_width)
        in_scrollcontent.setMinimumSize(maxi_width,in_scrollcontent.sizeHint().height())
        maxi_width += 82
        maxi_width = max(maxi_width, 350)    # In case there is no widget
        self.inputDock.setFixedWidth(maxi_width)
        self.in_widget.setFixedWidth( maxi_width)
        for option in option_list:
            key = self.dockWidgetContents.findChild(QtWidgets.QWidget, option[0])

            if option[0] in RED_LIST:
                red_list_set = set(red_list_function())
                current_list_set = set(option[3])
                current_red_list = list(current_list_set.intersection(red_list_set))

                for value in current_red_list:
                    indx = option[3].index(str(value))
                    key.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

        ###############################
        # Customized option in Combobox
        ###############################
        # @author: Amir
        """
        This routine takes both customized_input list and input_value_changed list.
        Customized input list is the list displayed in popup, when "Customized" option is clicked.
        input_value_Changed is the list of keys whose values depend on values of other keys in input dock.
        The function which returns customized_input values takes no arguments.
        But if a key is common in both customized input and input value changed, it takes argument as specified in
         input value changed.
        Here, on_change_key_popup gives list of keys which are common in both and needs an input argument.
        Since, we don't know how may customized popups can be used in a module we have provided,
         "triggered.connect" for up to 10 customized popups
        """

        new_list = main.customized_input(main)
        updated_list = main.input_value_changed(main)
        data = {}

        d = {}
        if new_list != []:
            for t in new_list:
                Combobox_key = t[0]
                d[Combobox_key] = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                if updated_list != None:
                    onchange_key_popup = [item for item in updated_list if item[1] == t[0]]
                    arg_list = []
                    if onchange_key_popup != []:
                        for change_key in onchange_key_popup[0][0]:
                            arg_list.append(self.dockWidgetContents.findChild(QtWidgets.QWidget, change_key).currentText())
                        data[t[0] + "_customized"] = t[1](arg_list)
                    else:
                        data[t[0] + "_customized"] = t[1]()
                else:
                    data[t[0] + "_customized"] = t[1]()
            try:
                d.get(new_list[0][0]).activated.connect(lambda: self.popup(d.get(new_list[0][0]), new_list,updated_list,data))
                d.get(new_list[1][0]).activated.connect(lambda: self.popup(d.get(new_list[1][0]), new_list,updated_list,data))
                d.get(new_list[2][0]).activated.connect(lambda: self.popup(d.get(new_list[2][0]), new_list,updated_list,data))
                d.get(new_list[3][0]).activated.connect(lambda: self.popup(d.get(new_list[3][0]), new_list,updated_list,data))
                d.get(new_list[4][0]).activated.connect(lambda: self.popup(d.get(new_list[4][0]), new_list,updated_list,data))
                d.get(new_list[5][0]).activated.connect(lambda: self.popup(d.get(new_list[5][0]), new_list,updated_list,data))
                d.get(new_list[6][0]).activated.connect(lambda: self.popup(d.get(new_list[6][0]), new_list,updated_list,data))
                d.get(new_list[7][0]).activated.connect(lambda: self.popup(d.get(new_list[7][0]), new_list,updated_list,data))
                d.get(new_list[8][0]).activated.connect(lambda: self.popup(d.get(new_list[8][0]), new_list,updated_list,data))
                d.get(new_list[9][0]).activated.connect(lambda: self.popup(d.get(new_list[9][0]), new_list,updated_list,data))
                d.get(new_list[10][0]).activated.connect(lambda: self.popup(d.get(new_list[10][0]), new_list,updated_list,data))
            except IndexError:
                pass

        # Change in Ui based on Connectivity selection
        ##############################################
        """ This routine is for "on change" feature. When ever base key is changed all their corresponding
        on_change keys should change. input_value_changed written for each module gives this information in form of list
         of tuples [ref input_value_Changed in any module for detailed description]"""
        if updated_list is None:
            pass
        else:
            for t in updated_list:
                for key_name in t[0]:
                    key_changed = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_name)
                    self.on_change_connect(key_changed, updated_list, data)

        self.btn_Reset = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_Reset.setGeometry(QtCore.QRect((maxi_width/2)-110, 650, 100, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(65)
        self.btn_Reset.setFont(font)
        self.btn_Reset.setAutoDefault(True)
        self.btn_Reset.setObjectName("btn_Reset")

        self.btn_Design = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_Design.setGeometry(QtCore.QRect((maxi_width/2)+10, 650, 100, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(65)
        self.btn_Design.setFont(font)
        self.btn_Design.setAutoDefault(True)
        self.btn_Design.setObjectName("btn_Design")
        self.inputDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.inputDock)

        ##############################################
        # OUTPUT DOCK
        ##############################################
        """

        @author: Umair

        """
        out_list = main.output_values(main, False)

        #maxi_width = max([QtGui.QFontMetrics(font).boundingRect(option[1]).width() for option in out_list if option[2] not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE]])
        self.outputDock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputDock.sizePolicy().hasHeightForWidth())
        self.outputDock.setSizePolicy(sizePolicy)
        #self.outputDock.setMinimumSize(QtCore.QSize(400, 710))
        #self.outputDock.setMaximumSize(QtCore.QSize(maxi_width+220, 710))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.outputDock.setFont(font)
        self.outputDock.setObjectName("outputDock")

        self.dockWidgetContents_out = QtWidgets.QWidget()
        self.dockWidgetContents_out.setObjectName("dockWidgetContents_out")

        self.out_widget = QtWidgets.QWidget(self.dockWidgetContents_out)
        #self.out_widget.setGeometry(QtCore.QRect(0, 0, 400, 600))
        out_layout1 = QtWidgets.QVBoxLayout(self.out_widget)
        out_scroll = QScrollArea(self.out_widget)
        out_layout1.addWidget(out_scroll)
        out_scroll.setWidgetResizable(True)
        out_scroll.horizontalScrollBar().hide()
        out_scrollcontent = QtWidgets.QWidget(out_scroll)
        out_layout2 = QtWidgets.QGridLayout(out_scrollcontent)
        out_scrollcontent.setLayout(out_layout2)
        #out_scroll.horizontalScrollBar().hide()
        _translate = QtCore.QCoreApplication.translate

        """
        This routine takes the inputs from output_values function from the corresponding module file
         and create specified QT widgets
        """

        i = 0
        j = 1
        button_list = []
        maxi_width_left, maxi_width_right = -1, -1
        for option in out_list:
            lable = option[1]
            output_type = option[2]
            if output_type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE]:
                l = QtWidgets.QLabel(self.dockWidgetContents_out)
                #l.setGeometry(QtCore.QRect(6, 10 + i, maxi_width , 25))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(option[0] + "_label")
                l.resize(l.sizeHint().width(), l.sizeHint().height())
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                out_layout2.addWidget(l, j, 1, 1, 1)
                l.setVisible(True if option[4] else False)
                metrices = QtGui.QFontMetrics(font)
                maxi_width_left = max(metrices.boundingRect(lable).width() + 8, maxi_width_left)
                #l.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
                # if option[0] == KEY_OUT_ANCHOR_BOLT_TENSION and module == KEY_DISP_BASE_PLATE:
                #     l.setVisible(False)

            if output_type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.dockWidgetContents_out)

                #r.setGeometry(QtCore.QRect(100, 10 + i, 150, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(option[0])
                r.setReadOnly(True)

                #r.setFixedSize(r.size())
                out_layout2.addWidget(r, j, 2, 1, 1)
                r.setVisible(True if option[4] else False)
                maxi_width_right = max(maxi_width_right, 100)    # predefined minimum width of 110 for textboxes
                #r.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
                # if option[0] == KEY_OUT_ANCHOR_BOLT_TENSION and module == KEY_DISP_BASE_PLATE:
                #     r.setVisible(False)

            if output_type == TYPE_OUT_BUTTON:
                v = option[3]
                b = QtWidgets.QPushButton(self.dockWidgetContents_out)

                #b.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                b.setFont(font)
                b.setObjectName(option[0])
                #b.setFixedSize(b.size())
                b.resize(b.sizeHint().width(), b.sizeHint().height())
                b.setText(v[0])
                b.setDisabled(True)
                #b.setFixedSize(b.size())
                button_list.append(option)
                out_layout2.addWidget(b, j, 2, 1, 1)
                maxi_width_right = max(maxi_width_right, b.sizeHint().width())
                #b.clicked.connect(lambda: self.output_button_dialog(main, out_list))

            if output_type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.dockWidgetContents_out)

                #q.setGeometry(QtCore.QRect(3, 10 + i, 201, 25))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setWeight(65)
                q.setFont(font)
                q.setObjectName("_title")

                #q.setFixedSize(q.size())
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))
                q.resize(q.sizeHint().width(), q.sizeHint().height())
                out_layout2.addWidget(q, j, 1, 2, 2)
                j = j + 1
            i = i + 30
            j = j + 1
        out_layout2.setRowStretch(j+1, 10)
        out_scroll.setWidget(out_scrollcontent)
        maxi_width = maxi_width_left + maxi_width_right

        maxi_width += 80    # +73 coz of whitespaces
        maxi_width = max(maxi_width, 350) # in case no widget
        out_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        out_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.outputDock.setFixedWidth(maxi_width)
        self.out_widget.setFixedWidth(maxi_width)
        self.outputDock.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
        self.out_widget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
        # common_button = QtWidgets.QPushButton()
        # d = {
        #     'Button_1': common_button,
        #     'Button_2': common_button,
        #     'Button_3': common_button,
        #     'Button_4': common_button,
        #     'Button_5': common_button,
        #     'Button_6':  common_button
        # }
        #
        # print(button_list)

        # Case_1

        # for option in button_list:
        #     for i in d.keys():
        #         button = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0])
        #         if button not in d.values() and d[i] not in self.dockWidgetContents_out.children():
        #             d[i] = button
        # d['Button_1'].clicked.connect(lambda: self.output_button_dialog(main, button_list, d['Button_1']))
        # d['Button_2'].clicked.connect(lambda: self.output_button_dialog(main, button_list, d['Button_2']))
        # d['Button_3'].clicked.connect(lambda: self.output_button_dialog(main, button_list, d['Button_3']))
        # d['Button_4'].clicked.connect(lambda: self.output_button_dialog(main, button_list, d['Button_4']))
        # d['Button_5'].clicked.connect(lambda: self.output_button_dialog(main, button_list, d['Button_5']))
        # d['Button_6'].clicked.connect(lambda: self.output_button_dialog(main, button_list, d['Button_6']))

        # Case_2


        if button_list:
            for button_key in button_list:
                button = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, button_key[0])
                self.output_button_connect(main, button_list, button)

        """ UI code for other output dock widgets like create design report button etc."""
        self.outputDock.setWidget(self.dockWidgetContents_out)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.outputDock)
        self.btn_CreateDesign = QtWidgets.QPushButton(self.dockWidgetContents_out)
        self.save_outputDock = QtWidgets.QPushButton(self.dockWidgetContents_out)
        self.btn_CreateDesign.setFixedSize(185, 35)
        self.save_outputDock.setFixedSize(140, 35)
        self.btn_CreateDesign.setAutoDefault(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(65)
        self.btn_CreateDesign.setFont(font)
        self.btn_CreateDesign.setObjectName("btn_CreateDesign")
        self.save_outputDock.setFont(font)
        self.save_outputDock.setObjectName("save_outputDock")
        self.save_outputDock.setText("Save Output")
        self.save_outputDock.clicked.connect(self.save_output_to_txt(main))
        # self.btn_CreateDesign.clicked.connect(self.createDesignReport(main))

        ##################################
        # Menu UI
        ##################################
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
        self.actionSave_Front_View.setEnabled(False)
        self.actionSave_Top_View = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_Top_View.setFont(font)
        self.actionSave_Top_View.setObjectName("actionSave_Top_View")
        self.actionSave_Top_View.setEnabled(False)
        self.actionSave_Side_View = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionSave_Side_View.setFont(font)
        self.actionSave_Side_View.setObjectName("actionSave_Side_View")
        self.actionSave_Side_View.setEnabled(False)
        self.actionChange_bg_color = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.actionChange_bg_color.setFont(font)
        self.actionChange_bg_color.setObjectName("actionChange_bg_color")

        self.menugraphics_component_list = []
        """
        This routine take the list of separate 3D components checkboxes to be displayed in the ribbon from
        the corresponding module file
        """
        for component in main.get_3d_components(main):
            actionShow_component = QtWidgets.QAction(MainWindow)
            font = QtGui.QFont()
            font.setFamily("DejaVu Sans")
            font.setItalic(False)
            actionShow_component.setFont(font)
            actionShow_component.setObjectName(component[0])
            actionShow_component.setText(component[0])
            actionShow_component.setEnabled(False)
            self.action_connect(main, actionShow_component, component[1])
            self.menugraphics_component_list.append(actionShow_component)

        self.actionChange_background = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        self.actionChange_background.setFont(font)
        self.actionChange_background.setObjectName("actionChange_background")
        # self.actionShow_all = QtWidgets.QAction(MainWindow)
        # self.actionShow_all.setObjectName("actionShow_all")
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
        self.actionDesign_Preferences.triggered.connect(lambda: self.common_function_for_save_and_design(main, data, "Design_Pref"))
        self.actionDesign_Preferences.triggered.connect(lambda: self.combined_design_prefer(data,main))
        self.actionDesign_Preferences.triggered.connect(self.design_preferences)
        self.designPrefDialog = DesignPreferences(self, main, input_dictionary=self.input_dock_inputs)

        # self.designPrefDialog.rejected.connect(lambda: self.design_preferences('rejected'))
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
        # self.menuEdit.addAction(self.actionCut)
        # self.menuEdit.addAction(self.actionCopy)
        # self.menuEdit.addAction(self.actionPaste)
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
        # self.menuGraphics.addAction(self.actionShow_beam)
        # self.menuGraphics.addAction(self.actionShow_column)
        # self.menuGraphics.addAction(self.actionShow_finplate)
        # self.menuGraphics.addAction(self.actionShow_all)
        for action in self.menugraphics_component_list:
            self.menuGraphics.addAction(action)
        self.menuGraphics.addSeparator()
        self.menuGraphics.addAction(self.actionChange_background)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuGraphics.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi()
        self.mytabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.action_save_input.triggered.connect(lambda: self.common_function_for_save_and_design(main, data, "Save"))
        self.btn_Design.clicked.connect(lambda: self.common_function_for_save_and_design(main, data, "Design"))
        self.action_load_input.triggered.connect(lambda: self.loadDesign_inputs(option_list, data, new_list, main))
        self.btn_Reset.clicked.connect(lambda: self.reset_fn(option_list, out_list, new_list, data))
        self.actionChange_background.triggered.connect(lambda: main.showColorDialog(self))
        self.actionSave_3D_model.triggered.connect(lambda: self.save3DcadImages(main))
        self.btn_CreateDesign.clicked.connect(lambda:self.open_summary_popup(main))
        self.actionSave_current_image.triggered.connect(lambda: self.save_cadImages(main))
        self.actionCreate_design_report.triggered.connect(lambda:self.open_summary_popup(main))
        self.actionZoom_out.triggered.connect(lambda: self.zoom_model(zoom_type="out"))
        self.actionZoom_in.triggered.connect(lambda: self.zoom_model(zoom_type="in"))

        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())
        self.connectivity = None
        self.fuse_model = None

    def save_output_to_txt(self, main):
        def save_fun():
            status = main.design_status
            out_list = main.output_values(main, status)
            to_Save = {}
            flag = 0
            for option in out_list:
                if option[0] is not None and option[2] == TYPE_TEXTBOX:
                    to_Save[option[0]] = str(option[3])
                    if str(option[3]):
                        flag = 1
            if not flag:
                QMessageBox.information(self, "Information",
                                        "Nothing to Save.")
            else:
                fileName, _ = QFileDialog.getSaveFileName(self,
                                                          "Save Output", os.path.join(self.folder, "untitled.txt"),
                                                          "Input Files(*.txt)")
                if fileName:
                    with open(fileName, 'w') as outfile:
                        yaml.dump(to_Save, outfile, default_flow_style=False)
                    QMessageBox.information(self, "Information",
                                            "Saved successfully.")
        return save_fun

    def popup(self,key, for_custom_list,updated_list,data):

        """
        Function for retaining the values in the popup once it is closed.
        """

        # @author: Amir

        for c_tup in for_custom_list:
            if c_tup[0] != key.objectName():
                continue
            selected = key.currentText()
            f = c_tup[1]
            if updated_list != None:
                onchange_key_popup = [item for item in updated_list if item[1] == c_tup[0]]
            else:
                onchange_key_popup = []
            if onchange_key_popup != []:
                arg_list = []
                for change_key in onchange_key_popup[0][0]:
                    arg_list.append(
                        self.dockWidgetContents.findChild(QtWidgets.QWidget, change_key).currentText())
                options = f(arg_list)
                existing_options = data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options)
                    if data[c_tup[0] + "_customized"] == []:
                        data[c_tup[0] + "_customized"] = f(arg_list)
                        key.setCurrentIndex(0)
                else:
                    data[c_tup[0] + "_customized"] = f(arg_list)

                    input = f(arg_list)
                    data[c_tup[0] + "_customized"] = input
            else:
                options = f()
                existing_options = data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options)
                    if data[c_tup[0] + "_customized"] == []:
                        data[c_tup[0] + "_customized"] = f()
                        key.setCurrentIndex(0)
                else:
                    data[c_tup[0] + "_customized"] = f()

    def on_change_connect(self, key_changed, updated_list, data):
        key_changed.currentIndexChanged.connect(lambda: self.change(key_changed, updated_list, data))

    def change(self, k1, new, data):

        """
        @author: Umair
        """
        for tup in new:
            (object_name, k2_key, typ, f) = tup
            if k1.objectName() not in object_name:
                continue
            if typ in [TYPE_LABEL, TYPE_OUT_LABEL]:
                k2_key = k2_key + "_label"
            if typ == TYPE_NOTE:
                k2_key = k2_key + "_note"

            if typ in [TYPE_OUT_DOCK, TYPE_OUT_LABEL]:
                k2 = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, k2_key)
            elif typ == TYPE_WARNING:
                k2 = str(k2_key)
            else:
                k2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, k2_key)


            arg_list = []
            for ob_name in object_name:
                key = self.dockWidgetContents.findChild(QtWidgets.QWidget, ob_name)
                arg_list.append(key.currentText())

            val = f(arg_list)

            if typ == TYPE_COMBOBOX:
                k2.clear()
                for values in val:
                    k2.addItem(values)
                    k2.setCurrentIndex(0)
                if k2_key in RED_LIST:
                    red_list_set = set(red_list_function())
                    current_list_set = set(val)
                    current_red_list = list(current_list_set.intersection(red_list_set))
                    for value in current_red_list:
                        indx = val.index(str(value))
                        k2.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            elif typ == TYPE_COMBOBOX_CUSTOMIZED:
                k2.setCurrentIndex(0)
                data[k2_key + "_customized"] = val
            elif typ == TYPE_CUSTOM_MATERIAL:
                if val:
                    self.new_material_dialog()

            elif typ == TYPE_LABEL:
                k2.setText(val)
            elif typ == TYPE_NOTE:
                k2.setText(val)
            elif typ == TYPE_IMAGE:
                pixmap1 = QPixmap(val)
                k2.setPixmap(pixmap1)
            elif typ == TYPE_TEXTBOX:
                if val:
                    k2.setEnabled(True)
                else:
                    k2.setDisabled(True)
            elif typ == TYPE_WARNING:
                if val:
                    QMessageBox.warning(self, "Application", k2)
            elif typ in [TYPE_OUT_DOCK, TYPE_OUT_LABEL]:
                if val:
                    k2.setVisible(False)
                else:
                    k2.setVisible(True)
            else:
                pass

    # Function for Reset Button
    '''
    @author: Umair, Amir
    '''

    def reset_fn(self, op_list, out_list, new_list, data):

        # For input dock

        for op in op_list:
            widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0])
            if op[2] == TYPE_COMBOBOX or op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                widget.setCurrentIndex(0)
            elif op[2] == TYPE_TEXTBOX:
                widget.setText('')
            else:
                pass

        for out in out_list:
            widget = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, out[0])
            if out[2] == TYPE_TEXTBOX:
                widget.setText('')
            else:
                pass

        self.display.EraseAll()

    # Function for Design Button
    '''
    @author: Umair
    '''

    def design_fn(self, op_list, data_list, main):
        design_dictionary = {}
        self.input_dock_inputs = {}
        for op in op_list:
            widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0])
            if op[2] == TYPE_COMBOBOX:
                des_val = widget.currentText()
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_MODULE:
                des_val = op[1]
                module = op[1]
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                des_val = data_list[op[0] + "_customized"]
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_TEXTBOX:
                des_val = widget.text()
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_NOTE:
                widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0] + "_note")
                des_val = widget.text()
                d1 = {op[0]: des_val}
            else:
                d1 = {}
            design_dictionary.update(d1)
            self.input_dock_inputs.update(d1)

        for design_pref_key in self.design_pref_inputs.keys():
            if design_pref_key not in self.input_dock_inputs.keys():
                self.input_dock_inputs.update({design_pref_key: self.design_pref_inputs[design_pref_key]})
        if self.designPrefDialog.flag:
            print('flag true')

            des_pref_input_list = main.input_dictionary_design_pref(main)
            edit_tabs_list = main.edit_tabs(main)
            edit_tabs_remove = list(filter(lambda x: x[2] == TYPE_REMOVE_TAB,edit_tabs_list))
            remove_tab_name = [x[0] for x in edit_tabs_remove]
            # remove_tabs = list(filter(lambda x: x[0] in remove_tab_name, des_pref_input_list))
            #
            # remove_func_name = edit_tabs_remove[3]
            result = None
            for edit in main.edit_tabs(main):
                (tab_name, input_dock_key_name, change_typ, f) = edit
                remove_tabs = list(filter(lambda x: x[0] in remove_tab_name,des_pref_input_list))

                input_dock_key = self.dockWidgetContents.findChild(QtWidgets.QWidget, input_dock_key_name)
                result = list(filter(lambda get_tab:
                                     self.designPrefDialog.ui.findChild(QtWidgets.QWidget, get_tab[0]).objectName() !=
                                     f(input_dock_key.currentText()), remove_tabs))

            if result is not None:
                des_pref_input_list_updated = [i for i in des_pref_input_list if i not in result]
            else:
                des_pref_input_list_updated = des_pref_input_list

            for des_pref in des_pref_input_list_updated:
                tab_name = des_pref[0]
                input_type = des_pref[1]
                input_list = des_pref[2]
                tab = self.designPrefDialog.ui.findChild(QtWidgets.QWidget, tab_name)
                for key_name in input_list:
                    key = tab.findChild(QtWidgets.QWidget, key_name)
                    if input_type == TYPE_TEXTBOX:
                        val = key.text()
                        design_dictionary.update({key_name: val})
                    elif input_type == TYPE_COMBOBOX:
                        val = key.currentText()
                        design_dictionary.update({key_name: val})

        else:
            print('flag false')

            for without_des_pref in main.input_dictionary_without_design_pref(main):
                input_dock_key = without_des_pref[0]
                input_list = without_des_pref[1]
                input_source = without_des_pref[2]
                for key_name in input_list:
                    if input_source == 'Input Dock':
                        design_dictionary.update({key_name: design_dictionary[input_dock_key]})
                    else:
                        val = main.get_values_for_design_pref(main, key_name, design_dictionary)
                        design_dictionary.update({key_name: val})

            for dp_key in self.design_pref_inputs.keys():
                design_dictionary[dp_key] = self.design_pref_inputs[dp_key]

        self.design_inputs = design_dictionary

    '''
    @author: Umair
    '''
    def saveDesign_inputs(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Design", os.path.join(self.folder, "untitled.osi"),
                                                  "Input Files(*.osi)")
        if not fileName:
            return
        try:
            with open(fileName, 'w') as input_file:
                yaml.dump(self.design_inputs, input_file)
        except Exception as e:
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s" % (fileName, str(e)))
            return

    def return_class(self,name):
        if name == KEY_DISP_FINPLATE:
            return FinPlateConnection
        elif name == KEY_DISP_ENDPLATE:
            return EndPlateConnection
        elif name == KEY_DISP_CLEATANGLE:
            return CleatAngleConnection
        elif name == KEY_DISP_SEATED_ANGLE:
            return SeatedAngleConnection
        elif name == KEY_DISP_COLUMNCOVERPLATE:
            return ColumnCoverPlate
        elif name == KEY_DISP_COLUMNCOVERPLATEWELD:
            return ColumnCoverPlateWeld
        elif name == KEY_DISP_BEAMCOVERPLATE:
            return BeamCoverPlate
        elif name == KEY_DISP_BEAMCOVERPLATEWELD:
            return BeamCoverPlateWeld
        elif name == KEY_DISP_BEAMENDPLATE:
            return BeamEndPlate
        elif name == KEY_DISP_COLUMNENDPLATE:
            return ColumnEndPlate
        elif name == KEY_DISP_BASE_PLATE:
            return BasePlateConnection
        elif name == KEY_DISP_TENSION_BOLTED:
            return Tension_bolted
        elif name == KEY_DISP_TENSION_WELDED:
            return Tension_welded
# Function for getting inputs from a file
    '''
    @author: Umair
    '''

    def loadDesign_inputs(self, op_list, data, new, main):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Design", os.path.join(str(self.folder)),
                                                  "InputFiles(*.osi)")
        if not fileName:
            return
        try:
            in_file = str(fileName)
            with open(in_file, 'r') as fileObject:
                uiObj = yaml.load(fileObject)
            module = uiObj[KEY_MODULE]

            # module_class = self.return_class(module)
            # print('loading inputs',uiObj, op_list, data, new)
            selected_module = main.module_name(main)
            if selected_module == module:
                # print(uiObj, op_list, data, new)
                self.setDictToUserInputs(uiObj, op_list, data, new)
            else:
                QMessageBox.information(self, "Information",
                                        "Please load the appropriate Input")

                return
        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return

    # Function for loading inputs from a file to Ui
    '''
    @author: Umair
    '''

    def setDictToUserInputs(self, uiObj, op_list, data, new):

        for uiObj_key in uiObj.keys():
            if uiObj_key not in [i[0] for i in op_list]:
                self.design_pref_inputs.update({uiObj_key: uiObj[uiObj_key]})

        for op in op_list:
            key_str = op[0]
            key = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_str)
            if op[2] == TYPE_COMBOBOX:
                if key_str in uiObj.keys():
                    index = key.findText(uiObj[key_str], QtCore.Qt.MatchFixedString)
                    if index >= 0:
                        key.setCurrentIndex(index)
            elif op[2] == TYPE_TEXTBOX:
                if key_str in uiObj.keys():
                    key.setText(uiObj[key_str])
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if key_str in uiObj.keys():
                    for n in new:

                        if n[0] == key_str and n[0] == KEY_SECSIZE:
                            if uiObj[key_str] != n[1](self.dockWidgetContents.findChild(QtWidgets.QWidget,
                                                          KEY_SEC_PROFILE).currentText()):
                                data[key_str + "_customized"] = uiObj[key_str]
                                key.setCurrentIndex(1)
                            else:
                                pass
                        elif n[0] == key_str and n[0] != KEY_SECSIZE:
                            if uiObj[key_str] != n[1]():
                                data[key_str + "_customized"] = uiObj[key_str]
                                key.setCurrentIndex(1)
                            else:
                                pass
            else:
                pass

    def common_function_for_save_and_design(self, main, data, trigger_type):

        # @author: Amir

        option_list = main.input_values(self)
        self.design_fn(option_list, data, main)

        if trigger_type == "Save":
            self.saveDesign_inputs()
        elif trigger_type == "Design_Pref":

            if self.prev_inputs != self.input_dock_inputs:
                self.designPrefDialog = DesignPreferences(self, main, input_dictionary=self.input_dock_inputs)

                if 'Select Section' in self.input_dock_inputs.values():
                    self.designPrefDialog.flag = False
                else:
                    self.designPrefDialog.flag = True

        else:
            main.design_button_status = True
            error = main.func_for_validation(main, self.design_inputs)
            status = main.design_status
            print(status)

            if error is not None:
                self.show_error_msg(error)

            out_list = main.output_values(main, status)
            for option in out_list:
                if option[2] == TYPE_TEXTBOX:
                    txt = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0])
                    txt.setText(str(option[3]))
                    if status:
                        txt.setVisible(True if option[3] else False)
                        txt_label = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0]+"_label")
                        txt_label.setVisible(True if option[3] else False)

                elif option[2] == TYPE_OUT_BUTTON:
                    self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0]).setEnabled(True)


            self.design_exist = False

            if status is True and main.module in [KEY_DISP_FINPLATE, KEY_DISP_BEAMCOVERPLATE,
                                                  KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_CLEATANGLE,
                                                  KEY_DISP_ENDPLATE, KEY_DISP_BASE_PLATE, KEY_DISP_SEATED_ANGLE,
                                                  KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED,
                                                  KEY_DISP_COLUMNCOVERPLATEWELD, KEY_DISP_COLUMNENDPLATE]:
                self.commLogicObj = CommonDesignLogic(self.display, self.folder, main.module, main.mainmodule)
                status = main.design_status
                module_class = self.return_class(main.module)
                self.commLogicObj.call_3DModel(status, module_class)
                for chkbox in main.get_3d_components(main):
                    self.frame.findChild(QtWidgets.QCheckBox, chkbox[0]).setEnabled(True)
                for action in self.menugraphics_component_list:
                    action.setEnabled(True)
                fName = str('./ResourceFiles/images/3d.png')
                file_extension = fName.split(".")[-1]
                if file_extension == 'png':
                    self.display.ExportToImage(fName)
                self.design_exist = True

            else:
                for chkbox in main.get_3d_components(main):
                    self.frame.findChild(QtWidgets.QCheckBox, chkbox[0]).setEnabled(False)
                for action in self.menugraphics_component_list:
                    action.setEnabled(False)

    def show_error_msg(self, error):
        QMessageBox.about(self,'information',error[0])  # show only first error message.

    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles\images", "OsdagHeader.png")))
        image_path2 = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles\images", "ColumnsBeams.png")))

        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "OsdagHeader.png"))
        shutil.copyfile(image_path2, os.path.join(str(self.folder), "images_html", "ColumnsBeams.png"))

    def output_button_connect(self, main, button_list, b):
        b.clicked.connect(lambda: self.output_button_dialog(main, button_list, b))

    def output_button_dialog(self, main, button_list, button):

        dialog = QtWidgets.QDialog()
        #dialog.resize(470, 300)

        dialog.setObjectName("Dialog")
        #q.sizeHint().width(), q.sizeHint().height()
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        #dialog.setSizePolicy(sizePolicy)
        layout1 = QtWidgets.QVBoxLayout(dialog)
        scroll = QScrollArea(dialog)
        layout1.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scroll.horizontalScrollBar().setVisible(False)
        scrollcontent = QtWidgets.QWidget(scroll)
        outer_grid_layout = QtWidgets.QGridLayout(scrollcontent)
        inner_grid_widget = QtWidgets.QWidget(scrollcontent)
        image_widget = QtWidgets.QWidget(scrollcontent)
        image_layout = QtWidgets.QVBoxLayout(image_widget)
        image_widget.setLayout(image_layout)
        inner_grid_layout = QtWidgets.QGridLayout(inner_grid_widget)
        inner_grid_widget.setLayout(inner_grid_layout)
        scrollcontent.setLayout(outer_grid_layout)
        section = 0
        maxi_width = -1
        for op in button_list:

            if op[0] == button.objectName():
                tup = op[3]
                title = tup[0]
                fn = tup[1]
                dialog.setWindowTitle(title)
                i = 0
                j = 1
                for option in fn(main, main.design_status):
                    lable = option[1]
                    out_but_type = option[2]
                    _translate = QtCore.QCoreApplication.translate
                    if out_but_type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE, TYPE_SECTION]:
                        l = QtWidgets.QLabel(inner_grid_widget)
                        #l.setGeometry(QtCore.QRect(10, 10 + i, 120, 25))

                        font = QtGui.QFont()
                        font.setPointSize(9)
                        font.setBold(False)
                        font.setWeight(50)
                        l.setFont(font)
                        #l.setFixedSize(l.size())
                        l.setObjectName(option[0] + "_label")
                        l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                        inner_grid_layout.addWidget(l, j, 1, 1, 1)
                        #l.resize(l.sizeHint().width() + 8, l.sizeHint().height())
                        metrices = QtGui.QFontMetrics(font)
                        l.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
                        maxi_width = max(maxi_width, metrices.boundingRect(lable).width() + 8)



                    if out_but_type == TYPE_SECTION:
                        if section != 0:
                            outer_grid_layout.addWidget(inner_grid_widget, j, 1, 1, 1)
                            outer_grid_layout.addWidget(image_widget, j, 2, 1, 1)
                            hl1 = QtWidgets.QFrame()
                            hl1.setFrameShape(QtWidgets.QFrame.HLine)
                            j += 1
                            outer_grid_layout.addWidget(hl1, j, 1, 1, 2)

                        inner_grid_widget = QtWidgets.QWidget(scrollcontent)
                        image_widget = QtWidgets.QWidget(scrollcontent)
                        image_layout = QtWidgets.QVBoxLayout(image_widget)
                        image_widget.setLayout(image_layout)
                        inner_grid_layout = QtWidgets.QGridLayout(inner_grid_widget)
                        inner_grid_widget.setLayout(inner_grid_layout)
                        im = QtWidgets.QLabel(image_widget)
                        #im.setGeometry(QtCore.QRect(330, 10, 150, 150))
                        #im.setFixedSize(im.size())
                        # im.setGeometry(QtCore.QRect(330, 10, 100, 100))
                        # im.setScaledContents(True)
                        # im.setFixedSize(im.size())

                        pmap = QPixmap(option[3])
                        #im.setScaledContents(1)
                        im.setPixmap(pmap.scaled(170,340,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
                        #im.setPixmap(pmap)
                        image_layout.addWidget(im)
                        j += 1
                        #maxi_width = max(maxi_width, im.width())
                        #im.resize(im.sizeHint().width(), im.sizeHint().height())

                        q = QtWidgets.QLabel(scrollcontent)
                        #q.setGeometry(QtCore.QRect(30, 10, 201, 30))

                        font = QtGui.QFont()
                        font.setWeight(600)
                        font.setPointSize(11)
                        q.setFont(font)
                        q.setObjectName("_title")
                        q.setText(lable)
                        q.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum))
                        #q.setFixedSize(q.size())
                        #q.resize(q.sizeHint().width(), q.sizeHint().height())
                        outer_grid_layout.addWidget(q, j, 1, 1, 2)

                        section += 1

                    if out_but_type == TYPE_TEXTBOX:
                        r = QtWidgets.QLineEdit(inner_grid_widget)
                        #r.setGeometry(QtCore.QRect(160, 10 + i, 160, 27))
                        font = QtGui.QFont()
                        font.setPointSize(11)
                        font.setBold(False)
                        font.setWeight(50)
                        r.setFont(font)
                        #r.setFixedSize(r.size())
                        r.setObjectName(option[0])
                        r.setText(str(option[3]))
                        inner_grid_layout.addWidget(r, j, 2, 1, 1)

                    if out_but_type == TYPE_IMAGE:
                        im = QtWidgets.QLabel(image_widget)
                        #im.setGeometry(QtCore.QRect(330, 10, 100, 100))
                        #im.setScaledContents(True)
                        #im.setFixedSize(im.size())
                        pmap = QPixmap(option[3])
                        im.setPixmap(pmap.scaled(170,340,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
                        image_layout.addWidget(im)

                    j = j + 1
                    i = i + 30

                if inner_grid_layout.count() > 0:
                    outer_grid_layout.addWidget(inner_grid_widget, j, 1, 1, 1)
                if image_layout.count() > 0:
                    outer_grid_layout.addWidget(image_widget, j, 2, 1, 1)
                scroll.setWidget(scrollcontent)
                if section == 0:
                    dialog.resize(350, 300)
                #dialog.setFixedSize(dialog.size())
                dialog.exec()

    def new_material_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle('Custom Material')
        layout = QtWidgets.QGridLayout(dialog)
        widget = QtWidgets.QWidget(dialog)
        widget.setLayout(layout)
        _translate = QtCore.QCoreApplication.translate
        textbox_list = ['Grade', 'Fy_20', 'Fy_20_40', 'Fy_40', 'Fu']
        i = 0
        for textbox_name in textbox_list:
            label = QtWidgets.QLabel(widget)
            label.setObjectName(textbox_name+"_label")
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setBold(False)
            font.setWeight(50)
            label.setFont(font)
            label.setText(_translate("MainWindow", "<html><body><p>" + textbox_name + "</p></body></html>"))
            # label.resize(120, 30)
            label.setFixedSize(100, 30)
            layout.addWidget(label, i, 1, 1, 1)

            textbox = QtWidgets.QLineEdit(widget)
            textbox.setObjectName(textbox_name)
            font = QtGui.QFont()
            font.setPointSize(11)
            font.setBold(False)
            font.setWeight(50)
            textbox.setFont(font)
            # textbox.resize(120, 30)
            textbox.setFixedSize(200, 24)
            if textbox_name == 'Grade':
                textbox.setText('Cus____')
                textbox.setReadOnly(True)
            else:
                textbox.setValidator(QtGui.QIntValidator())

            self.connect_change_popup_material(textbox, widget)
            layout.addWidget(textbox, i, 2, 1, 1)

            i += 1

        add_button = QtWidgets.QPushButton(widget)
        add_button.setObjectName("material_add")
        add_button.setText("Add")
        add_button.clicked.connect(lambda: self.update_material_db(widget))
        layout.addWidget(add_button, i, 1, 1, 2)

        dialog.setFixedSize(350, 250)
        closed = dialog.exec()
        if closed is not None:
            input_dock_material = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_MATERIAL)
            input_dock_material.clear()
            for item in connectdb("Material"):
                input_dock_material.addItem(item)

    def update_material_db(self, widget):

        material = widget.findChild(QtWidgets.QLineEdit, 'Grade').text()
        values = material.split("_")

        fy_20 = values[1]
        fy_20_40 = values[2]
        fy_40 = values[3]
        fu = values[4]
        elongation = 0

        if "" in [fy_20, fy_40, fy_20_40, fu]:
            QMessageBox.information(QMessageBox(), 'Warning', 'Please Fill all missing parameters!')
            return

        fy_20 = int(fy_20)
        fy_20_40 = int(fy_20_40)
        fy_40 = int(fy_40)
        fu = int(fu)

        if not 0 <= fy_20 <= 1000:
            QMessageBox.information(QMessageBox(), 'Warning', 'Please select Fy_20 in valid range!')
            return
        elif not 0 <= fy_20_40 <= 1000:
            QMessageBox.information(QMessageBox(), 'Warning', 'Please select Fy_20_40 in valid range!')
            return
        elif not 0 <= fy_40 <= 1000:
            QMessageBox.information(QMessageBox(), 'Warning', 'Please select Fy_40 in valid range!')
            return
        elif not 0 <= fu <= 1000:
            QMessageBox.information(QMessageBox(), 'Warning', 'Please select Fu in valid range!')
            return

        if fy_20 > 350:
            elongation = 20
        elif 250 < fy_20 <= 350:
            elongation = 22
        elif fy_20 <= 250:
            elongation = 23

        conn = sqlite3.connect(PATH_TO_DATABASE)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM Material WHERE Grade = ?", (material,))
        data = c.fetchone()[0]

        if data == 0:
            c.execute('''INSERT INTO Material (Grade,[Yield Stress (< 20)],[Yield Stress (20 -40)],
            [Yield Stress (> 40)],[Ultimate Tensile Stress],[Elongation ]) VALUES (?,?,?,?,?,?)''',
                      (material, fy_20, fy_20_40, fy_40, fu, elongation))
            conn.commit()
            c.close()
            conn.close()
            QMessageBox.information(QMessageBox(), 'Information', 'Data is added successfully to the database.')

        else:
            QMessageBox.information(QMessageBox(), 'Warning', 'Material already exists in Database!')

    def connect_change_popup_material(self, textbox, widget):
        textbox.textChanged.connect(lambda: self.change_popup_material(widget))

    def change_popup_material(self, widget):

        grade = widget.findChild(QtWidgets.QLineEdit, 'Grade')
        fy_20 = widget.findChild(QtWidgets.QLineEdit, 'Fy_20').text()
        fy_20_40 = widget.findChild(QtWidgets.QLineEdit, 'Fy_20_40').text()
        fy_40 = widget.findChild(QtWidgets.QLineEdit, 'Fy_40').text()
        fu = widget.findChild(QtWidgets.QLineEdit, 'Fu').text()
        material = str("Cus_"+fy_20+"_"+fy_20_40+"_"+fy_40+"_"+fu)
        grade.setText(material)

    # Function for showing design-preferences popup

    def design_preferences(self):
        #print(self.designPrefDialog.module_window.input_dock_inputs)
        self.designPrefDialog.show()

    # Function for getting input for design preferences from input dock
    '''
    @author: Umair
    '''
    def combined_design_prefer(self, data, main):

        on_change_tab_list = main.tab_value_changed(main)
        for new_values in on_change_tab_list:
            (tab_name, key_list, key_to_change, key_type, f) = new_values
            tab = self.designPrefDialog.ui.tabWidget.tabs.findChild(QtWidgets.QWidget, tab_name)
            for key_name in key_list:
                key = tab.findChild(QtWidgets.QWidget, key_name)
                if isinstance(key, QtWidgets.QComboBox):
                    self.connect_combobox_for_tab(key, tab, on_change_tab_list)
                elif isinstance(key, QtWidgets.QLineEdit):
                    self.connect_textbox_for_tab(key, tab, on_change_tab_list)

        # for fu_fy in main.list_for_fu_fy_validation(main):
        #
        #     material_key_name = fu_fy[0]
        #     fu_key_name = fu_fy[1]
        #     fy_key_name = fu_fy[2]
        #     material_key = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, material_key_name)
        #     fu_key = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, fu_key_name)
        #     fy_key = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, fy_key_name)
        #
        #     for validation_key in [fu_key, fy_key]:
        #         if validation_key.text() != "":
        #             self.designPrefDialog.fu_fy_validation_connect([fu_key, fy_key], validation_key, material_key)

        for edit in main.edit_tabs(main):
            (tab_name, input_dock_key_name, change_typ, f) = edit
            tab = self.designPrefDialog.ui.tabWidget.tabs.findChild(QtWidgets.QWidget, tab_name)
            input_dock_key = self.dockWidgetContents.findChild(QtWidgets.QWidget, input_dock_key_name)
            if change_typ == TYPE_CHANGE_TAB_NAME:
                self.designPrefDialog.ui.tabWidget.tabs.setTabText(
                    self.designPrefDialog.ui.tabWidget.tabs.indexOf(tab), f(input_dock_key.currentText()))
            elif change_typ == TYPE_REMOVE_TAB:

                if tab.objectName() != f(input_dock_key.currentText()):
                    self.designPrefDialog.ui.tabWidget.tabs.removeTab(
                        self.designPrefDialog.ui.tabWidget.tabs.indexOf(tab))
                # if tab:
                #     self.designPrefDialog.ui.tabWidget.insertTab(0, tab, tab_name)

        for refresh in main.refresh_input_dock(main):
            (tab_name, key_name, key_type, tab_key, master_key, value, database_arg) = refresh
            tab = self.designPrefDialog.ui.tabWidget.tabs.findChild(QtWidgets.QWidget, tab_name)
            if tab:
                add_button = tab.findChild(QtWidgets.QWidget, "pushButton_Add_"+tab_name)
                key = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_name)
                selected = key.currentText()


                if master_key:
                    val = self.dockWidgetContents.findChild(QtWidgets.QWidget, master_key).currentText()
                    if val not in value:
                        continue
                self.refresh_section_connect(add_button, selected, key_name, key_type, tab_key, database_arg,data)

    def connect_textbox_for_tab(self, key, tab, new):
        key.textChanged.connect(lambda: self.tab_change(key, tab, new))

    def connect_combobox_for_tab(self, key, tab, new):
        key.currentIndexChanged.connect(lambda: self.tab_change(key, tab, new))

    def tab_change(self, key, tab, new):

        for tup in new:
            (tab_name, key_list, k2_key_list, typ, f) = tup
            if tab_name != tab.objectName() or key.objectName() not in key_list:
                continue
            arg_list = []
            for key_name in key_list:
                # if object_name != key.objectName():
                #     continue
                key = tab.findChild(QtWidgets.QWidget, key_name)
                if isinstance(key, QtWidgets.QComboBox):
                    arg_list.append(key.currentText())
                elif isinstance(key, QtWidgets.QLineEdit):
                    arg_list.append(key.text())

            arg_list.append(self.input_dock_inputs)
            try:
                tab1 = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, tab_name)
                key1 = tab.findChild(QtWidgets.QWidget, KEY_SECSIZE_SELECTED)
                value1 = key1.text()
                arg_list.append({KEY_SECSIZE_SELECTED: value1})
            except:
                pass
            val = f(arg_list)

            for k2_key_name in k2_key_list:
                k2 = tab.findChild(QtWidgets.QWidget, k2_key_name)
                if typ == TYPE_COMBOBOX:
                    k2.clear()
                    for values in val[k2_key_name]:
                        k2.addItem(str(values))
                elif typ == TYPE_TEXTBOX:
                    k2.setText(str(val[k2_key_name]))

    def refresh_section_connect(self, add_button, prev, key_name, key_type, tab_key, arg,data):
        add_button.clicked.connect(lambda: self.refresh_section(prev, key_name, key_type, tab_key, arg,data))

    def refresh_section(self, prev, key_name, key_type, tab_key, arg,data):

        if key_type == TYPE_COMBOBOX_CUSTOMIZED:
            current_list = connectdb(arg,"popup")
        else:
            current_list = connectdb(arg)
        text = self.designPrefDialog.ui.findChild(QtWidgets.QWidget, tab_key).text()
        key = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_name)

        if key_type == TYPE_COMBOBOX:
            if text == "":
                return
            key.clear()
            for item in current_list:
                key.addItem(item)
            current_list_set = set(current_list)
            red_list_set = set(red_list_function())
            current_red_list = list(current_list_set.intersection(red_list_set))
            for value in current_red_list:
                indx = current_list.index(str(value))
                key.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            text_index = key.findText(text, QtCore.Qt.MatchFixedString)
            # key.setCurrentIndex(current_list.index(prev))

            if text_index >= 0:
                key.setCurrentIndex(text_index)
            else:
                key.setCurrentIndex(current_list.index(prev))
        elif key_type == TYPE_COMBOBOX_CUSTOMIZED:
            master_list = ['All','Customized']
            data[key_name + "_customized"] = current_list
            key.setCurrentIndex(master_list.index(prev))

    def create_design_report(self):
        self.create_report.show()

    def chkbox_connect(self, main, chkbox, f):
        chkbox.clicked.connect(lambda: f(main, self, "gradient_bg"))

    def action_connect(self, main, action, f):
        action.triggered.connect(lambda: f(main, self, "gradient_bg"))

    def showColorDialog(self):

        col = QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        self.display.set_bg_gradient_color([r, g, b], [255, 255, 255])

    def init_display(self, backend_str=None, size=(1024, 768)):

        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        # from OCC.Display.pyqt4Display import qtViewer3d
        from OCC.Display.qtDisplay import qtViewer3d
        self.modelTab = qtViewer3d(self)

        # self.setWindowTitle("Osdag Fin Plate")
        self.mytabWidget.resize(size[0], size[1])
        self.mytabWidget.addTab(self.modelTab, "")

        self.modelTab.InitDriver()
        display = self.modelTab._display

        # background gradient
        # display.set_bg_gradient_color(23, 1, 32, 23, 1, 32)
        display.set_bg_gradient_color([23, 1, 32], [23, 1, 32])
        # # display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        display.display_triedron()
        # display.display_triedron()
        display.View.SetProj(1, 1, 1)

        def centerOnScreen(self):
            '''Centers the window on the screen.'''
            resolution = QtGui.QDesktopWidget().screenGeometry()
            self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                      (resolution.height() / 2) - (self.frameSize().height() / 2))

        def start_display():
            self.modelTab.raise_()

        return display, start_display

    def save_cadImages(self,main):
        """Save CAD Model in image formats(PNG,JPEG,BMP,TIFF)

        Returns:

        """

        if main.design_status:

            files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
            fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"),
                                                      files_types)
            fName = str(fileName)
            file_extension = fName.split(".")[-1]

            if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp' or file_extension == 'tiff':
                self.display.ExportToImage(fName)
                QMessageBox.about(self, 'Information', "File saved")
        else:
            # self.actionSave_current_image.setEnabled(False)
            QMessageBox.about(self, 'Information', 'Design Unsafe: CAD image cannot be saved')

    def save3DcadImages(self, main):

        if main.design_status:
            if self.fuse_model is None:
                self.fuse_model = CommonDesignLogic.create2Dcad(self.commLogicObj)
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
            # self.actionSave_3D_model.setEnabled(False)
            QMessageBox.about(self,'Information', 'Design Unsafe: 3D Model cannot be saved')

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
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
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuGraphics.setTitle(_translate("MainWindow", "Graphics"))
        self.inputDock.setWindowTitle(_translate("MainWindow", "Input dock"))
        #self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.btn_Reset.setToolTip(_translate("MainWindow", "Alt+R"))
        self.btn_Reset.setText(_translate("MainWindow", "Reset"))
        self.btn_Reset.setShortcut(_translate("MainWindow", "Alt+R"))
        self.btn_Design.setToolTip(_translate("MainWindow", "Alt+D"))
        self.btn_Design.setText(_translate("MainWindow", "Design"))
        self.btn_Design.setShortcut(_translate("MainWindow", "Alt+D"))
        self.outputDock.setWindowTitle(_translate("MainWindow", "Output dock"))
        self.btn_CreateDesign.setText(_translate("MainWindow", "Create design report"))
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
        self.actionZoom_in.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out"))
        self.actionZoom_out.setShortcut(_translate("MainWindow", "Ctrl+O"))
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
        self.actionChange_background.setText(_translate("MainWindow", "Change background"))
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
        print("Done")

    # Function for hiding and showing input and output dock
    def dockbtn_clicked(self, widget):

        '''(QWidget) -> None
        This method dock and undock widget(QdockWidget)
        '''

        flag = widget.isHidden()
        if (flag):
            widget.show()
        else:
            widget.hide()





from . import icons_rc
if __name__ == '__main__':
    # set_osdaglogger()

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ModuleWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
