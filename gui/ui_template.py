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
from design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
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
from .ui_design_preferences import DesignPreferences
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
from design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.seated_angle_connection import SeatedAngleConnectionInput
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.beam_cover_plate import BeamCoverPlate
from design_type.connection.beam_end_plate import BeamEndPlate
from design_type.connection.column_end_plate import ColumnEndPlate

from cad.cad3dconnection import cadconnection


class Ui_ModuleWindow(QMainWindow):

    closed = pyqtSignal()
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
        self.new_window = QtWidgets.QDialog()
        self.new_ui = Ui_Dialog1()
        self.new_ui.setupUi(self.new_window, main)
        self.new_ui.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.new_window, self.new_ui.lbl_browse))
        self.new_ui.btn_saveProfile.clicked.connect(lambda: self.saveUserProfile(self.new_window))
        self.new_ui.btn_useProfile.clicked.connect(lambda: self.useUserProfile(self.new_window))
        self.new_window.exec()
        # self.new_ui.btn_browse.clicked.connect(lambda: self.getLogoFilePath(self.new_ui.lbl_browse))
        # self.new_ui.btn_saveProfile.clicked.connect(self.saveUserProfile)
        # self.new_ui.btn_useProfile.clicked.connect(self.useUserProfile)

    def getLogoFilePath(self, window, lblwidget):

        self.new_ui.lbl_browse.clear()
        filename, _ = QFileDialog.getOpenFileName(window, "Open Image", os.path.join(str(' '), ''), "InputFiles(*.png *.svg *.jpg)")

        # filename, _ = QFileDialog.getOpenFileName(
        #     self, 'Open File', " ../../",
        #     'Images (*.png *.svg *.jpg)',
        #     None, QFileDialog.DontUseNativeDialog)
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
                             write_to=os.path.join(str(self.folder), "images_html", "cmpylogoFin.png"))
        else:
            shutil.copyfile(filename, os.path.join(str(self.folder), "images_html", "cmpylogoFin.png"))

    def saveUserProfile(self, window):

        flag = True
        inputData = self.getPopUpInputs()
        filename, _ = QFileDialog.getSaveFileName(window, 'Save Files',
                                                  os.path.join(str(self.folder), "Profile"), '*.txt')
        if filename == '':
            flag = False
            return flag
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

        input_summary["ProjectTitle"] = str(self.new_ui.lineEdit_projectTitle.text())
        input_summary["Subtitle"] = str(self.new_ui.lineEdit_subtitle.text())
        input_summary["JobNumber"] = str(self.new_ui.lineEdit_jobNumber.text())
        input_summary["AdditionalComments"] = str(self.new_ui.txt_additionalComments.toPlainText())
        input_summary["Client"] = str(self.new_ui.lineEdit_client.text())

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

    def setupUi(self, MainWindow, main,folder):
        self.folder = folder
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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 412, 111, 51))
        self.pushButton.setObjectName("pushButton")
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

# INPUT DOCK
#############
        # @author : Umair

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
        self.btn3D.setEnabled(False)
        self.chkBxBeam.setEnabled(False)
        self.chkBxCol.setEnabled(False)
        self.chkBxFinplate.setEnabled(False)

        in_widget = QtWidgets.QWidget(self.dockWidgetContents)
        in_widget.setGeometry(QtCore.QRect(0, 0, 325, 600))
        in_layout1 = QtWidgets.QVBoxLayout(in_widget)
        in_scroll = QScrollArea(in_widget)
        in_layout1.addWidget(in_scroll)
        in_scroll.setWidgetResizable(True)
        in_scrollcontent = QtWidgets.QWidget(in_scroll)
        in_layout2 = QtWidgets.QGridLayout(in_scrollcontent)
        in_scrollcontent.setLayout(in_layout2)
        in_scroll.horizontalScrollBar().hide()
        # in_list = main.output_values(main, False)

        option_list = main.input_values(self)
        _translate = QtCore.QCoreApplication.translate

        i = 0
        j = 1
        for option in option_list:
            lable = option[1]
            type = option[2]
            if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE, TYPE_IMAGE_COMPRESSION]:
                l = QtWidgets.QLabel(self.dockWidgetContents)
                if option[0] in [KEY_MOMENT_MAJOR, KEY_MOMENT_MINOR] and module == KEY_DISP_BASE_PLATE:
                    l.setGeometry(QtCore.QRect(16, 10 + i, 120, 25))
                else:
                    l.setGeometry(QtCore.QRect(6, 10 + i, 120, 25))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(option[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setFixedSize(l.size())
                in_layout2.addWidget(l, j, 1, 1, 1)
                print(j, 'label')

            if type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
                combo = QtWidgets.QComboBox(self.dockWidgetContents)
                combo.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(option[0])
                for item in option[4]:
                    combo.addItem(item)
                combo.setFixedSize(combo.size())
                in_layout2.addWidget(combo, j, 2, 1, 1)

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.dockWidgetContents)
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(option[0])
                if option[0] in [KEY_MOMENT_MAJOR, KEY_MOMENT_MINOR] and module == KEY_DISP_BASE_PLATE:
                    r.setGeometry(QtCore.QRect(160, 10 + i, 150, 27))
                    r.setDisabled(True)
                else:
                    r.setGeometry(QtCore.QRect(150, 10 + i, 150, 27))
                r.setFixedSize(r.size())
                in_layout2.addWidget(r, j, 2, 1, 1)

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
                l.setText(option[4])
                l.setReadOnly(True)
                l.setFixedSize(l.size())
                in_layout2.addWidget(l, j, 2, 1, 1)


            if type == TYPE_IMAGE:
                im = QtWidgets.QLabel(self.dockWidgetContents)
                im.setGeometry(QtCore.QRect(190, 10 + i, 70, 57))
                im.setObjectName(option[0])
                im.setScaledContents(True)
                pixmap = QPixmap(option[4])
                im.setPixmap(pixmap)
                i = i + 30
                im.setFixedSize(im.size())
                in_layout2.addWidget(im, j, 2, 1, 1)
                print(j, 'image')

            if type == TYPE_IMAGE_COMPRESSION:
                imc = QtWidgets.QLabel(self.dockWidgetContents)
                imc.setGeometry(QtCore.QRect(130, 10 + i, 160, 150))
                imc.setObjectName(option[0])
                imc.setScaledContents(True)
                pixmapc = QPixmap(option[4])
                imc.setPixmap(pixmapc)
                i = i + 30
                imc.setFixedSize(imc.size())
                in_layout2.addWidget(imc, j, 2, 1, 1)


            if option[0] in [KEY_AXIAL, KEY_SHEAR]:
                key = self.dockWidgetContents.findChild(QtWidgets.QWidget, option[0])
                onlyInt = QIntValidator()
                key.setValidator(onlyInt)

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.dockWidgetContents)
                q.setGeometry(QtCore.QRect(3, 10 + i, 201, 25))
                font = QtGui.QFont()
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))
                q.setFixedSize(q.size())
                in_layout2.addWidget(q, j, 1, 2, 2)
                j = j + 1

            i = i + 30
            j = j + 1
        in_scroll.setWidget(in_scrollcontent)


        for option in option_list:
            key = self.dockWidgetContents.findChild(QtWidgets.QWidget, option[0])

            if option[0] in [KEY_SUPTNGSEC, KEY_SUPTDSEC, KEY_SECSIZE]:
                red_list_set = set(red_list_function())
                current_list_set = set(option[4])
                current_red_list = list(current_list_set.intersection(red_list_set))

                for value in current_red_list:
                    indx = option[4].index(str(value))
                    key.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

    # Customized option in Combobox
    ###############################
    # @author: Amir
        new_list = main.customized_input(main)
        print (new_list)
        data = {}

        for t in new_list:

            if t[0] in [KEY_PLATETHK, KEY_FLANGEPLATE_THICKNESS, KEY_ENDPLATE_THICKNESS, KEY_CLEATSEC, KEY_DIA_ANCHOR]\
                    and (module not in [KEY_DISP_TENSION_WELDED, KEY_DISP_TENSION_BOLTED]):
                key_customized_1 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_1.activated.connect(lambda: popup(key_customized_1, new_list))
                data[t[0] + "_customized"] = t[1]()
            elif t[0] == KEY_GRD and (module not in [KEY_DISP_TENSION_WELDED,KEY_DISP_BEAMCOVERPLATEWELD,KEY_DISP_COLUMNCOVERPLATEWELD]):
                key_customized_2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_2.activated.connect(lambda: popup(key_customized_2, new_list))
                data[t[0] + "_customized"] = t[1]()
            elif t[0] == KEY_D and (module not in [KEY_DISP_TENSION_WELDED,KEY_DISP_BEAMCOVERPLATEWELD,KEY_DISP_COLUMNCOVERPLATEWELD]):
                key_customized_3 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_3.activated.connect(lambda: popup(key_customized_3, new_list))
                data[t[0] + "_customized"] = t[1]()
            elif t[0] == KEY_SECSIZE and (module in [KEY_DISP_COMPRESSION, KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED]):
                key_customized_4 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_4.activated.connect(lambda: popup(key_customized_4, new_list))
                data[t[0] + "_customized"] = t[1](self.dockWidgetContents.findChild(QtWidgets.QWidget,
                                                                                    KEY_SEC_PROFILE).currentText())

            elif t[0] in [KEY_WEBPLATE_THICKNESS] and (module not in [KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED]):
                key_customized_5 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_5.activated.connect(lambda: popup(key_customized_5, new_list))
                data[t[0] + "_customized"] = t[1]()

            elif t[0] == KEY_GRD_ANCHOR and module == KEY_DISP_BASE_PLATE:
                key_customized_6 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_6.activated.connect(lambda: popup(key_customized_6, new_list))
                data[t[0] + "_customized"] = t[1]()

            else:
                pass

            # elif t[0] == KEY_SEC_PROFILE and (module == KEY_DISP_TENSION):
            #     key_customized_6 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
            #     key_customized_6.activated.connect(lambda: popup(key_customized_6, new_list))
            #     data[t[0] + "_customized"] = t[1](self.dockWidgetContents.findChild(QtWidgets.QWidget,
            #                     KEY_SEC_PROFILE).currentText())



        def popup(key, for_custom_list):

            """
            Function for retaining the values in the popup once it is closed.
             """

            # @author: Amir

            for c_tup in for_custom_list:
                if c_tup[0] != key.objectName():
                    continue
                selected = key.currentText()
                f = c_tup[1]
                if c_tup[0] == KEY_SECSIZE and (module in [KEY_DISP_COMPRESSION, KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED]):
                    options = f(self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SEC_PROFILE).currentText())
                    existing_options = data[c_tup[0] + "_customized"]
                    if selected == "Customized":
                        data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options)
                        if data[c_tup[0] + "_customized"] == []:
                            data[c_tup[0] + "_customized"] = f(self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SEC_PROFILE).currentText())
                            key.setCurrentIndex(0)
                    else:
                        data[c_tup[0] + "_customized"] = f(self.dockWidgetContents.findChild(QtWidgets.QWidget,
                            KEY_SEC_PROFILE).currentText())

                        input = f(self.dockWidgetContents.findChild(QtWidgets.QWidget,
                            KEY_SEC_PROFILE).currentText())
                        # input.remove('Select Section')
                        data[c_tup[0] + "_customized"] = input

                        # data[c_tup[0] + "_customized"] = f(self.dockWidgetContents.findChild(QtWidgets.QWidget,
                        #     KEY_SEC_PROFILE).currentText()).remove('Select Section')
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

    # Change in Ui based on Connectivity selection
    ##############################################

        updated_list = main.input_value_changed(main)
        if updated_list is None:
            pass
        else:
            for t in updated_list:
                key_changed = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                self.on_change_connect(key_changed, updated_list, data)

        self.btn_Reset = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_Reset.setGeometry(QtCore.QRect(30, 600, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Reset.setFont(font)
        self.btn_Reset.setAutoDefault(True)
        self.btn_Reset.setObjectName("btn_Reset")

        self.btn_Design = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_Design.setGeometry(QtCore.QRect(140, 600, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Design.setFont(font)
        self.btn_Design.setAutoDefault(True)
        self.btn_Design.setObjectName("btn_Design")
        self.inputDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.inputDock)

        # if module not in [KEY_DISP_BEAMCOVERPLATE, KEY_DISP_COLUMNCOVERPLATE]:
        #     key_changed = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_CONN)
        #     key_changed.currentIndexChanged.connect(lambda: self.validate_beam_beam(key_changed))

# OUTPUT DOCK
#############
        """
        
        @author: Umair 
        
        """

        self.outputDock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
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

        self.dockWidgetContents_out = QtWidgets.QWidget()
        self.dockWidgetContents_out.setObjectName("dockWidgetContents_out")

        out_widget = QtWidgets.QWidget(self.dockWidgetContents_out)
        out_widget.setGeometry(QtCore.QRect(0, 0, 320, 622))
        out_layout1 = QtWidgets.QVBoxLayout(out_widget)
        out_scroll = QScrollArea(out_widget)
        out_layout1.addWidget(out_scroll)
        out_scroll.setWidgetResizable(True)
        out_scrollcontent = QtWidgets.QWidget(out_scroll)
        out_layout2 = QtWidgets.QGridLayout(out_scrollcontent)
        out_scrollcontent.setLayout(out_layout2)
        out_list = main.output_values(main, False)
        _translate = QtCore.QCoreApplication.translate

        i = 0
        j = 1
        button_list = []
        for option in out_list:
            lable = option[1]
            type = option[2]
            if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE]:
                l = QtWidgets.QLabel(self.dockWidgetContents_out)
                l.setGeometry(QtCore.QRect(6, 10 + i, 120, 25))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(option[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                out_layout2.addWidget(l, j, 1, 1, 1)

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.dockWidgetContents_out)
                r.setGeometry(QtCore.QRect(150, 10 + i, 160, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(option[0])
                out_layout2.addWidget(r, j, 2, 1, 1)

            if type == TYPE_OUT_BUTTON:
                v = option[3]
                b = QtWidgets.QPushButton(self.dockWidgetContents_out)
                b.setGeometry(QtCore.QRect(150, 10 + i, 160, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                b.setFont(font)
                b.setObjectName(option[0])
                b.setText(v[0])
                b.setDisabled(True)
                button_list.append(option)
                out_layout2.addWidget(b, j, 2, 1, 1)
                #b.clicked.connect(lambda: self.output_button_dialog(main, out_list))

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.dockWidgetContents_out)
                q.setGeometry(QtCore.QRect(3, 10 + i, 201, 25))
                font = QtGui.QFont()
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))
                out_layout2.addWidget(q, j, 1, 2, 2)
                j = j + 1
            i = i + 30
            j = j + 1
        out_scroll.setWidget(out_scrollcontent)

        # common_button = QtWidgets.QPushButton()
        # d = {
        #     'Button_1': common_button,
        #     'Button_2': common_button,
        #     'Button_3': common_button,
        #     'Button_4': common_button,
        #     'Button_5': common_button,
        #     'Button_6': common_button
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


            # if option[0] == KEY_WEB_SPACING:
            #     d['button_1'] =
            #     button_web_spacing = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0])
            #     print(button_web_spacing)
            #     button_web_spacing.clicked.connect(lambda: self.output_button_dialog(main, button_list, KEY_WEB_SPACING))
            # elif option[0] == KEY_WEB_CAPACITY:
            #     button_web_capacity = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0])
            #     print(button_web_capacity)
            #     button_web_capacity.clicked.connect(lambda: self.output_button_dialog(main, button_list, KEY_WEB_CAPACITY))

        # for i in range(len(button_connect)):
        #     button_connect[i].clicked.connect(lambda: self.output_button_dialog(main, button_list,
        #                                                                         button_connect[i].objectName()))

        # for button in self.dockWidgetContents_out.children():
        #     if button.objectName() == KEY


        self.outputDock.setWidget(self.dockWidgetContents_out)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.outputDock)

        self.btn_CreateDesign = QtWidgets.QPushButton(self.dockWidgetContents_out)
        self.btn_CreateDesign.setGeometry(QtCore.QRect(50, 650, 200, 30))
        self.btn_CreateDesign.setAutoDefault(True)
        self.btn_CreateDesign.setObjectName("btn_CreateDesign")
        # self.btn_CreateDesign.clicked.connect(self.createDesignReport(main))

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
        self.actionDesign_Preferences.triggered.connect(lambda: self.common_function_for_save_and_design(main, data, "Design_Pref"))
        self.actionDesign_Preferences.triggered.connect(lambda: self.combined_design_prefer(module))
        self.actionDesign_Preferences.triggered.connect(self.design_preferences)
        self.designPrefDialog = DesignPreferences(main)
        add_column = self.designPrefDialog.findChild(QtWidgets.QWidget, "pushButton_Add_"+KEY_DISP_COLSEC)
        add_beam = self.designPrefDialog.findChild(QtWidgets.QWidget, "pushButton_Add_"+KEY_DISP_BEAMSEC)

        #
        # if module not in [KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_BEAMCOVERPLATE, KEY_DISP_COLUMNCOVERPLATEWELD,
        #                   KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_COMPRESSION, KEY_DISP_TENSION, KEY_DISP_BASE_PLATE,
        #                   KEY_DISP_COLUMNENDPLATE]:

        if module not in [KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_BEAMCOVERPLATE, KEY_DISP_COLUMNCOVERPLATEWELD,
                          KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_COMPRESSION, KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED,
                          KEY_DISP_BASE_PLATE,KEY_DISP_COLUMNENDPLATE]:
            column_index = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC).currentIndex()
            beam_index = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTDSEC).currentIndex()
            add_column.clicked.connect(lambda: self.refresh_sections(column_index, "Supporting"))
            add_beam.clicked.connect(lambda: self.refresh_sections(beam_index, "Supported"))
        elif module == KEY_DISP_COLUMNCOVERPLATE and module == KEY_DISP_COLUMNCOVERPLATEWELD:
            section_index = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SECSIZE).currentIndex()
            add_column.clicked.connect(lambda: self.refresh_sections(section_index, "Section_col"))

        elif module == KEY_DISP_BEAMCOVERPLATE or module == KEY_DISP_BEAMCOVERPLATEWELD:
            section_index = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SECSIZE).currentIndex()
            add_beam.clicked.connect(lambda: self.refresh_sections(section_index, "Section_bm"))

        elif module == KEY_DISP_COMPRESSION:
            pass
        self.designPrefDialog.rejected.connect(self.design_preferences)

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

        self.retranslateUi()
        self.mytabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.action_save_input.triggered.connect(lambda: self.common_function_for_save_and_design(main, data, "Save"))
        self.btn_Design.clicked.connect(lambda: self.common_function_for_save_and_design(main, data, "Design"))
        self.action_load_input.triggered.connect(lambda: self.loadDesign_inputs(option_list, data, new_list, main))
        # self.action_load_input.triggered.connect(lambda: main.loadDesign_inputs(main, self, option_list, data, new_list))

        self.btn_Reset.clicked.connect(lambda: self.reset_fn(option_list, out_list, new_list, data))
        # self.btn_Reset.clicked.connect(lambda: self.reset_fn(option_list, out_list))
        # self.btn_Reset.clicked.connect(lambda: self.reset_popup(new_list, data))
        # self.btn_Design.clicked.connect(self.osdag_header)
        self.actionShow_beam.triggered.connect(lambda: self.call_3DBeam(self, main, "gradient_bg"))
        self.actionShow_column.triggered.connect(lambda: self.call_3DColumn(self, main, "gradient_bg"))
        self.actionShow_finplate.triggered.connect(lambda: self.call_3DFinplate(self, main, "gradient_bg"))
        self.actionShow_all.triggered.connect(lambda: self.call_3DModel(self, main, "gradient_bg"))
        self.actionChange_background.triggered.connect(lambda: self.showColorDialog(self))
        self.actionSave_3D_model.triggered.connect(self.save3DcadImages)
        self.btn3D.clicked.connect(lambda: self.call_3DModel(self, main, "gradient_bg"))
        self.chkBxBeam.clicked.connect(lambda: self.call_3DBeam(self, main, "gradient_bg"))
        self.chkBxCol.clicked.connect(lambda: self.call_3DColumn(self, main, "gradient_bg"))
        self.chkBxFinplate.clicked.connect(lambda: self.call_3DFinplate(self, main, "gradient_bg"))
        self.btn_CreateDesign.clicked.connect(lambda:self.open_summary_popup(main))
        self.actionSave_current_image.triggered.connect(lambda: self.save_cadImages(main))

        if main.module_name(main) == KEY_DISP_FINPLATE:
            self.chkBxFinplate.setText("Finplate")
            self.actionShow_finplate.setText("Show Finplate")
        elif main.module_name(main) == KEY_DISP_CLEATANGLE:
            self.chkBxFinplate.setText("CleatAngle")
            self.actionShow_finplate.setText("Show CleatAngle")


        from osdagMainSettings import backend_name
        self.display, _ = self.init_display(backend_str=backend_name())

        self.connectivity = None
        self.fuse_model = None
        # self.disableViewButtons()
        # self.resultObj = None
        # self.uiObj = None

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

        display.set_bg_gradient_color([23, 1, 32], [23, 1, 32])
        # # display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        # display.display_trihedron()
        display.display_triedron()
        display.View.SetProj(1, 1, 1)

        def centerOnScreen(self):
            '''Centers the window on the screen.'''
            resolution = QtGui.QDesktopWidget().screenGeometry()
            self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                      (resolution.height() / 2) - (self.frameSize().height() / 2))

        def start_display():
            self.modelTab.raise_()

        return display, start_display

    # def save_cadImages(self,main):
    #     """Save CAD Model in image formats(PNG,JPEG,BMP,TIFF)
    #
    #     Returns:
    #
    #     """
    #
    #     if main.design_status is True:
    #
    #         files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
    #         fileName, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"),
    #                                                   files_types)
    #         fName = str(fileName)
    #         file_extension = fName.split(".")[-1]
    #
    #         if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp' or file_extension == 'tiff':
    #             self.display.ExportToImage(fName)
    #             QMessageBox.about(self, 'Information', "File saved")
    #     else:
    #         self.actionSave_current_image.setEnabled(False)
    #         QMessageBox.about(self, 'Information', 'Design Unsafe: CAD image cannot be saved')


    def save3DcadImages(self):
        status = True
        if status is True:
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
            self.actionSave_3D_model.setEnabled(False)
            QMessageBox.about(self,'Information', 'Design Unsafe: 3D Model cannot be saved')

    # def generate_3D_Cad_image(self,main):
    #
    #     # status = self.resultObj['Bolt']['status']
    #     if main.design_status is True:
    #         main.call_3DModel(main, self,"gradient_bg")
    #         data = os.path.join(str(self.folder), "images_html", "3D_Model.png")
    #         self.display.ExportToImage(data)
    #         self.display.FitAll()
    #     else:
    #         pass
    #
    #     return data

    def on_change_connect(self, key_changed, updated_list, data):
        key_changed.currentIndexChanged.connect(lambda: self.change(key_changed, updated_list, data))

    def change(self, k1, new, data):

        """
        @author: Umair
        """
        for tup in new:
            (object_name, k2_key, typ, f) = tup
            if object_name != k1.objectName():
                continue
            if typ == TYPE_LABEL:
                k2_key = k2_key + "_label"
            if typ == TYPE_NOTE:
                k2_key = k2_key + "_note"
            k2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, k2_key)
            if object_name not in [KEY_END2, KEY_SEC_PROFILE]:
                val = f(k1.currentText())
                k2.clear()
            elif object_name == KEY_SEC_PROFILE:
                val = f(k1.currentText())
                k2.setCurrentIndex(0)
            elif object_name == KEY_END2:
                key_end1 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_END1)
                val = f(k1.currentText(), key_end1.currentText())
                k2.clear()
            if typ == TYPE_COMBOBOX:
                k2.clear()
                for values in val:
                    k2.addItem(values)
                    k2.setCurrentIndex(0)
                if k2_key in [KEY_SUPTNGSEC, KEY_SUPTDSEC, KEY_SECSIZE]:
                    red_list_set = set(red_list_function())
                    current_list_set = set(val)
                    current_red_list = list(current_list_set.intersection(red_list_set))
                    for value in current_red_list:
                        indx = val.index(str(value))
                        k2.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            elif typ == TYPE_COMBOBOX_CUSTOMIZED:
                data[k2_key+"_customized"] = val
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

        # For list in Customized combobox

        for custom_combo in new_list:
            data[custom_combo[0] + "_customized"] = custom_combo[1]()

        # For output dock

        for out in out_list:
            widget = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, out[0])
            if out[2] == TYPE_TEXTBOX:
                widget.setText('')
            else:
                pass

        self.display.EraseAll()

        self.btn3D.setEnabled(False)
        self.chkBxBeam.setEnabled(False)
        self.chkBxCol.setEnabled(False)
        self.chkBxFinplate.setEnabled(False)
        self.btn3D.setChecked(Qt.Unchecked)
        self.chkBxBeam.setChecked(Qt.Unchecked)
        self.chkBxCol.setChecked(Qt.Unchecked)
        self.chkBxFinplate.setChecked(Qt.Unchecked)

# Function for Design Button
    '''
    @author: Umair 
    '''

    def design_fn(self, op_list, data_list):
        design_dictionary = {}
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
                des_val = data_list[op[0]+"_customized"]
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_TEXTBOX:
                des_val = widget.text()
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_NOTE:
                widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0]+"_note")
                des_val = widget.text()
                d1 = {op[0]: des_val}
            else:
                d1 = {}
            design_dictionary.update(d1)

        if self.designPrefDialog.flag:

            if module not in [KEY_DISP_COLUMNCOVERPLATE,KEY_DISP_COLUMNCOVERPLATEWELD, KEY_DISP_BEAMCOVERPLATE,
                              KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_COMPRESSION, KEY_DISP_TENSION_BOLTED,
                              KEY_DISP_TENSION_WELDED, KEY_DISP_BASE_PLATE]:
                tab_Column = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_DISP_COLSEC)
                key_material_column = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_MATERIAL).currentText()
                if key_material_column == "Custom":
                    material_fu_column = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_FU).text()
                    material_fy_column = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_FY).text()
                    material_column = "Custom"+" "+str(material_fu_column)+" "+str(material_fy_column)
                else:
                    material_column = key_material_column
                tab_Beam = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_DISP_BEAMSEC)
                key_material_beam = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_MATERIAL).currentText()
                if key_material_beam == "Custom":
                    material_fu_beam = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_FU).text()
                    material_fy_beam = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_FY).text()
                    material_beam = "Custom"+" "+str(material_fu_beam)+" "+str(material_fy_beam)
                else:
                    material_beam = key_material_beam
                d2 = {KEY_SUPTNGSEC_MATERIAL: material_column, KEY_SUPTDSEC_MATERIAL: material_beam}
                design_dictionary.update(d2)
            elif module == KEY_DISP_COMPRESSION:
                key = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SEC_PROFILE)
                section = key.currentText()
                if section == 'Beams':
                    tab_Beam = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_DISP_BEAMSEC)
                    material_fu_beam = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_FU).text()
                    material_fy_beam = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_FY).text()
                    material_beam = str(material_fu_beam) + "," + str(material_fy_beam)
                    d2 = {KEY_SUPTDSEC_MATERIAL: material_beam}
                    design_dictionary.update(d2)

                elif section == 'Columns':
                    tab_Column = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_DISP_COLSEC)
                    material_fu_column = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_FU).text()
                    material_fy_column = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_FY).text()
                    material_column = str(material_fu_column)+","+str(material_fy_column)
                    d2 = {KEY_SUPTNGSEC_MATERIAL: material_column}
                    design_dictionary.update(d2)

                elif section in ['Angles', 'Back to Back Angles', 'Star Angles', 'Channels', 'Back to Back Channels']:
                    pass
            elif module == KEY_DISP_BASE_PLATE:
                tab_Column = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_DISP_COLSEC)
                typ = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_TYPE).currentText()
                source = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_SOURCE).text()
                material = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_MATERIAL).text()
                material_fu = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_FU).text()
                material_fy = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_FY).text()
                tab_Base_Plate = self.designPrefDialog.findChild(QtWidgets.QWidget, "Base Plate")
                bp_material = tab_Base_Plate.findChild(QtWidgets.QWidget, KEY_BASE_PLATE_MATERIAL).text()
                bp_material_fu = tab_Base_Plate.findChild(QtWidgets.QWidget, KEY_BASE_PLATE_FU).text()
                bp_material_fy = tab_Base_Plate.findChild(QtWidgets.QWidget, KEY_BASE_PLATE_FY).text()
                anchor_dia = data_list[KEY_DIA_ANCHOR+"_customized"]

                d2 = {KEY_SUPTNGSEC_TYPE: typ, KEY_SUPTNGSEC_SOURCE: source, KEY_SUPTNGSEC_MATERIAL: material,
                      KEY_SUPTNGSEC_FU: material_fu, KEY_SUPTNGSEC_FY: material_fy, KEY_BASE_PLATE_MATERIAL: bp_material,
                      KEY_BASE_PLATE_FU: bp_material_fu, KEY_BASE_PLATE_FY: bp_material_fy,
                      KEY_DP_ANCHOR_BOLT_LENGTH: self.designPrefDialog.anchor_bolt_designation(anchor_dia[0])[1],
}
                design_dictionary.update(d2)

        else:
            common_material = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_MATERIAL).currentText()

            if module not in [KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_BEAMCOVERPLATE, KEY_DISP_COMPRESSION,
                              KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED, KEY_DISP_BASE_PLATE]:
                d2 = {KEY_SUPTNGSEC_MATERIAL: common_material, KEY_SUPTDSEC_MATERIAL: common_material}
                design_dictionary.update(d2)
            elif module == KEY_DISP_COMPRESSION:
                key = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SEC_PROFILE)
                section = key.currentText()
                if section == 'Beams':
                    d2 = {KEY_SUPTDSEC_MATERIAL: common_material}
                    design_dictionary.update(d2)
                elif section == 'Columns':
                    d2 = {KEY_SUPTNGSEC_MATERIAL: common_material}
                    design_dictionary.update(d2)
                elif section in ['Angles', 'Back to Back Angles', 'Star Angles', 'Channels', 'Back to Back Channels']:
                    pass
            elif module == KEY_DISP_BASE_PLATE:
                des = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC).currentText()
                anchor_dia = data_list[KEY_DIA_ANCHOR+"_customized"]
                anchor_typ = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_TYP_ANCHOR).currentText()
                if des == 'Select Section':
                    des = connectdb("Columns", "popup")[0]
                col_attributes = Section(des, common_material)
                Section.connect_to_database_update_other_attributes(col_attributes, "Columns", des)
                d2 = {KEY_SUPTNGSEC_TYPE: "Rolled", KEY_SUPTNGSEC_SOURCE: str(col_attributes.source),
                      KEY_SUPTNGSEC_MATERIAL: common_material,
                      KEY_SUPTNGSEC_FU: str(col_attributes.fu), KEY_SUPTNGSEC_FY: str(col_attributes.fy),
                      KEY_BASE_PLATE_MATERIAL: common_material,
                      KEY_BASE_PLATE_FU: str(col_attributes.fu), KEY_BASE_PLATE_FY: str(col_attributes.fy),
                      KEY_DP_ANCHOR_BOLT_DESIGNATION: self.designPrefDialog.anchor_bolt_designation(anchor_dia[0])[0],
                      KEY_DP_ANCHOR_BOLT_TYPE: anchor_typ,
                      KEY_DP_ANCHOR_BOLT_LENGTH: self.designPrefDialog.anchor_bolt_designation(anchor_dia[0])[1],
                      KEY_DP_ANCHOR_BOLT_HOLE_TYPE: 'Standard',
                      KEY_DP_ANCHOR_BOLT_MATERIAL_G_O: str(col_attributes.fu),
                      KEY_DP_ANCHOR_BOLT_FRICTION: str(0.30)
                      }
                design_dictionary.update(d2)

        design_dictionary.update(self.designPrefDialog.save_designPref_para(module))
        self.design_inputs = design_dictionary

    # def pass_d(self, main, design_dictionary):
    #     """
    #     It sets key variable textEdit and passes it to warn text function present in tension_bolted.py for logger
    #      """
    #
    #     # @author Arsil Zunzunia
    #
    #     key = self.centralwidget.findChild(QtWidgets.QWidget, "textEdit")
    #
    #     main.warn_text(main)
        # main.set_input_values(main, design_dictionary)
# Function for saving inputs in a file
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
        elif name == KEY_DISP_COLUMNCOVERPLATE:
            return ColumnCoverPlate
        # elif name == KEY_DISP_COLUMNCOVERPLATEWELD:
        #     return ColumnCoverPlateWeld
        elif name == KEY_DISP_BEAMCOVERPLATE:
            return BeamCoverPlate
        # elif name == KEY_DISP_BEAMCOVERPLATEWELD:
        #     return BeamCoverPlateWeld
        elif name == KEY_DISP_BEAMENDPLATE:
            return BeamEndPlate
        elif name == KEY_DISP_COLUMNENDPLATE:
            return ColumnEndPlate
# Function for getting inputs from a file
    '''
    @author: Umair 
    '''

    def loadDesign_inputs(self, op_list, data, new, main):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Design", os.path.join(str(self.folder)), "InputFiles(*.osi)")
        if not fileName:
            return
        try:
            in_file = str(fileName)
            with open(in_file, 'r') as fileObject:
                uiObj = yaml.load(fileObject)
            module = uiObj[KEY_MODULE]

            # module_class = self.return_class(module)

            selected_module = main.module_name(main)
            if selected_module == module:
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
        for op in op_list:
            key_str = op[0]
            key = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_str)
            if op[2] == TYPE_COMBOBOX:
                if key_str in uiObj.keys():
                    index = key.findText(uiObj[key_str], QtCore.Qt.MatchFixedString)
                    if index >= 0:
                        key.setCurrentIndex(index)
            elif op[2] == TYPE_TEXTBOX:
                key.setText(uiObj[key_str])
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if key_str in uiObj.keys():

                    for n in new:
                        if n[0] == key_str:
                            if uiObj[key_str] != n[1]():
                                data[key_str + "_customized"] = uiObj[key_str]
                                key.setCurrentIndex(1)
                            else:
                                pass
            else:
                pass

# Function for Input Validation
#
#                 for value in red_list:
#                     indx = option[4].index(str(value))
#                     key.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
#
#             elif option[0] == KEY_SUPTDSEC:
#
#                 v = "Beams"
#
#                 red_list = connect_for_red(v)
#
#                 print(red_list)
#
#                 for value in red_list:
#                     indx = option[4].index(str(value))
#
#                     key.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
#
#     def select_workspace_folder(self):
#         # This function prompts the user to select the workspace folder and returns the name of the workspace folder
#         config = configparser.ConfigParser()
#         config.read_file(open(r'Osdag.config'))
#         desktop_path = config.get("desktop_path", "path1")
#         folder = QFileDialog.getExistingDirectory(None, "Select Workspace Folder (Don't use spaces in the folder name)",
#                                                   desktop_path)
#         return folder
    def common_function_for_save_and_design(self, main, data, trigger_type):

        # @author: Amir

        option_list = main.input_values(self)
        self.design_fn(option_list, data)

        if trigger_type == "Save":
            self.saveDesign_inputs()
        elif trigger_type == "Design_Pref":
            pass
        else:
            main.design_button_status = True
            main.func_for_validation(main, self, self.design_inputs)
            status = main.design_status
            print(status)

            # main.set_input_values(main, self.design_inputs, self)
            # DESIGN_FLAG = 'True'

            out_list = main.output_values(main, status)
            for option in out_list:
                if option[2] == TYPE_TEXTBOX:
                    txt = self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0])
                    txt.setText(str(option[3]))
                elif option[2] == TYPE_OUT_BUTTON:
                    self.dockWidgetContents_out.findChild(QtWidgets.QWidget, option[0]).setEnabled(True)

            # if status is True and main.module == "Fin Plate":
            #     self.commLogicObj = cadconnection.commonfile(cadconnection, main.mainmodule, self.display, self.folder,
            #                                                  main.module)
            if self.design_inputs[KEY_MODULE] == KEY_DISP_FINPLATE:
                module_class = FinPlateConnection
            elif self.design_inputs[KEY_MODULE] == KEY_DISP_CLEATANGLE:
                module_class = CleatAngleConnection
            elif self.design_inputs[KEY_MODULE] == KEY_DISP_BEAMCOVERPLATE:
                module_class = BeamCoverPlate

            if status is True and (main.module == KEY_DISP_FINPLATE or main.module == KEY_DISP_BEAMCOVERPLATE or main.module == KEY_DISP_COLUMNCOVERPLATE or main.module == KEY_DISP_CLEATANGLE):
                self.commLogicObj = CommonDesignLogic(self.display, self.folder, main.module, main.mainmodule)
                status = main.design_status
                self.commLogicObj.call_3DModel(status, module_class)
                # self.callFin2D_Drawing("All")
                self.btn3D.setEnabled(True)
                self.chkBxBeam.setEnabled(True)
                self.chkBxCol.setEnabled(True)
                self.chkBxFinplate.setEnabled(True)
                self.actionShow_all.setEnabled(True)
                self.actionShow_beam.setEnabled(True)
                self.actionShow_column.setEnabled(True)
                self.actionShow_finplate.setEnabled(True)
                # image = main.generate_3D_Cad_image(main, self, self.folder)
                fName = str('./ResourceFiles/images/3d.png')
                file_extension = fName.split(".")[-1]
                if file_extension == 'png':
                    self.display.ExportToImage(fName)

            else:
                self.btn3D.setEnabled(False)
                self.chkBxBeam.setEnabled(False)
                self.chkBxCol.setEnabled(False)
                self.chkBxFinplate.setEnabled(False)
                self.actionShow_all.setEnabled(False)
                self.actionShow_beam.setEnabled(False)
                self.actionShow_column.setEnabled(False)
                self.actionShow_finplate.setEnabled(False)


    def osdag_header(self):
        image_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles\images", "OsdagHeader.png")))
        image_path2 = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles\images", "ColumnsBeams.png")))

        shutil.copyfile(image_path, os.path.join(str(self.folder), "images_html", "OsdagHeader.png"))
        shutil.copyfile(image_path2, os.path.join(str(self.folder), "images_html", "ColumnsBeams.png"))

    def output_button_connect(self, main, button_list, b):
        b.clicked.connect(lambda: self.output_button_dialog(main, button_list, b))

    def output_button_dialog(self, main, button_list, button):
        dialog = QtWidgets.QDialog()
        dialog.resize(350, 170)
        dialog.setFixedSize(dialog.size())
        dialog.setObjectName("Dialog")

        layout1 = QtWidgets.QVBoxLayout(dialog)
        scroll = QScrollArea(dialog)
        layout1.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollcontent = QtWidgets.QWidget(scroll)
        layout2 = QtWidgets.QGridLayout(scrollcontent)
        scrollcontent.setLayout(layout2)

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
                    type = option[2]
                    _translate = QtCore.QCoreApplication.translate
                    if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE]:
                        l = QtWidgets.QLabel()
                        l.setGeometry(QtCore.QRect(10, 10 + i, 120, 25))
                        font = QtGui.QFont()
                        font.setPointSize(9)
                        font.setBold(False)
                        font.setWeight(50)
                        l.setFont(font)
                        l.setObjectName(option[0] + "_label")
                        l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                        layout2.addWidget(l, j, 1, 1, 1)

                    if type == TYPE_TEXTBOX:
                        r = QtWidgets.QLineEdit()
                        r.setGeometry(QtCore.QRect(160, 10 + i, 160, 27))
                        font = QtGui.QFont()
                        font.setPointSize(11)
                        font.setBold(False)
                        font.setWeight(50)
                        r.setFont(font)
                        r.setObjectName(option[0])
                        r.setText(str(option[3]))
                        layout2.addWidget(r, j, 2, 1, 1)
                    j = j + 1
                    i = i + 30
                scroll.setWidget(scrollcontent)
                dialog.exec()

    def refresh_sections(self, prev, section):

        connectivity = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_CONN)
        supporting_section = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC)
        supported_section = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTDSEC)
        section_size = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SECSIZE)

        Columns = connectdb("Columns")
        Beams = connectdb("Beams")
        red_list_set = set(red_list_function())

        if section == "Supporting":
            supporting_section.clear()
            if connectivity.currentText() in VALUES_CONN_1:
                for item in Columns:
                    supporting_section.addItem(item)
                current_list_set = set(Columns)
                current_red_list = list(current_list_set.intersection(red_list_set))
                for value in current_red_list:
                    indx = Columns.index(str(value))
                    supporting_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

            elif connectivity.currentText() in VALUES_CONN_2:
                for item in Beams:
                    supporting_section.addItem(item)
                current_list_set = set(Beams)
                current_red_list = list(current_list_set.intersection(red_list_set))
                for value in current_red_list:
                    indx = Beams.index(str(value))
                    supporting_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            text = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_DESIGNATION).text()
            text_index = supporting_section.findText(text, QtCore.Qt.MatchFixedString)
            if text_index:
                supporting_section.setCurrentIndex(text_index)
            else:
                supporting_section.setCurrentIndex(prev)

        if section == "Supported":
            supported_section.clear()

            for item in Beams:
                supported_section.addItem(item)
            current_list_set = set(Beams)
            current_red_list = list(current_list_set.intersection(red_list_set))
            for value in current_red_list:
                indx = Beams.index(str(value))
                supported_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            text = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_DESIGNATION).text()
            text_index = supported_section.findText(text, QtCore.Qt.MatchFixedString)
            if text_index:
                supported_section.setCurrentIndex(text_index)
            else:
                supported_section.setCurrentIndex(prev)

        if section == "Section_col":
            section_size.clear()
            for item in Columns:
                section_size.addItem(item)
            current_list_set = set(Columns)
            current_red_list = list(current_list_set.intersection(red_list_set))
            for value in current_red_list:
                indx = Columns.index(str(value))
                section_size.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            text = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_DESIGNATION).text()
            text_index = section_size.findText(text, QtCore.Qt.MatchFixedString)
            if text_index:
                section_size.setCurrentIndex(text_index)
            else:
                section_size.setCurrentIndex(prev)

        if section == "Section_bm":
            section_size.clear()
            for item in Beams:
                section_size.addItem(item)
            current_list_set = set(Beams)
            current_red_list = list(current_list_set.intersection(red_list_set))
            for value in current_red_list:
                indx = Beams.index(str(value))
                section_size.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            text = self.designPrefDialog.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_DESIGNATION).text()
            text_index = section_size.findText(text, QtCore.Qt.MatchFixedString)
            if text_index:
                section_size.setCurrentIndex(text_index)
            else:
                section_size.setCurrentIndex(prev)




# Function for warning about structure

    # def warning_function(self, main, design_dictionary):
    #     key = self.centralwidget.findChild(QtWidgets.QWidget, "textEdit")
    #     main.warn_text(main, key, design_dictionary)

# Function for error if any field is missing

    def generate_missing_fields_error_string(self, missing_fields_list):


        """

        Args:
            missing_fields_list: list of fields that are not selected or entered

        Returns:
            error string that has to be displayed

        """
        # The base string which should be displayed

        # @author: Amir

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

# Function for validation in beam-beam structure

    def validate_beam_beam(self, key):

        # @author: Arsil

        if key.currentIndex() == 2:
            key2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC)
            key3 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTDSEC)
            key2.currentIndexChanged.connect(lambda: self.primary_secondary_beam_comparison(key, key2, key3))
            key3.currentIndexChanged.connect(lambda: self.primary_secondary_beam_comparison(key, key2, key3))




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
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
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
        print("Done")


    def call_3DModel(self, ui, main, bgcolor):
        '''
        This routine responsible for displaying 3D Cad model
        :param flag: boolean
        :return:
        '''
        if ui.btn3D.isChecked:
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Model", bgcolor)

    def call_3DBeam(self, ui, main, bgcolor):
        '''
        Creating and displaying 3D Beam
        '''
        ui.chkBxBeam.setChecked(Qt.Checked)
        if ui.chkBxBeam.isChecked():
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)

        ui.commLogicObj.display_3DModel("Beam", bgcolor)

    def call_3DColumn(self, ui, main, bgcolor):
        '''
        '''
        ui.chkBxCol.setChecked(Qt.Checked)
        if ui.chkBxCol.isChecked():
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxFinplate.setChecked(Qt.Unchecked)
            ui.btn3D.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def call_3DFinplate(self, ui, main, bgcolor):
        '''
        Displaying FinPlate in 3D
        '''
        ui.chkBxFinplate.setChecked(Qt.Checked)
        if ui.chkBxFinplate.isChecked():
            ui.chkBxBeam.setChecked(Qt.Unchecked)
            ui.chkBxCol.setChecked(Qt.Unchecked)
            ui.mytabWidget.setCurrentIndex(0)
            ui.btn3D.setChecked(Qt.Unchecked)
        if main.module_name(main) == KEY_DISP_FINPLATE:
            ui.commLogicObj.display_3DModel("Plate", bgcolor)
        elif main.module_name(main) == KEY_DISP_CLEATANGLE:
            ui.commLogicObj.display_3DModel("cleatAngle", bgcolor)


    def showColorDialog(self, ui):

        col = QColorDialog.getColor()
        colorTup = col.getRgb()
        r = colorTup[0]
        g = colorTup[1]
        b = colorTup[2]
        ui.display.set_bg_gradient_color([r, g, b], [255, 255, 255])

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

# Function for showing design-preferences popup

    def design_preferences(self):
        self.designPrefDialog.exec()

# Function for getting input for design preferences from input dock
    '''
    @author: Umair 
    '''

    def combined_design_prefer(self, module):
        self.designPrefDialog.flag = True
        key_1 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_CONN)
        key_2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC)
        key_3 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SUPTDSEC)
        key_4 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_MATERIAL)
        key_5 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SECSIZE)
        key_6 = self.dockWidgetContents.findChild(QtWidgets.QWidget, KEY_SEC_PROFILE)

        tab_Column = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, KEY_DISP_COLSEC)
        tab_Beam = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, KEY_DISP_BEAMSEC)
        tab_Angle = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, DISP_TITLE_ANGLE)

        tab_Bolt = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Bolt")
        tab_Weld = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Weld")
        tab_Detailing = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Detailing")
        tab_Design = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Design")
        tab_Connector = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Connector")
        tab_Anchor_Bolt = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Anchor Bolt")
        tab_Base_Plate = self.designPrefDialog.ui.tabWidget.findChild(QtWidgets.QWidget, "Base Plate")

        table_1 = "Columns"
        table_2 = "Beams"
        material_grade = key_4.currentText()
        material = Material(material_grade)
        if module != KEY_DISP_BASE_PLATE:
            tab_Bolt.findChild(QtWidgets.QWidget, KEY_DP_BOLT_MATERIAL_G_O).setText(str(material.fu))
        else:
            tab_Anchor_Bolt.findChild(QtWidgets.QWidget, KEY_DP_ANCHOR_BOLT_MATERIAL_G_O).setText(str(material.fu))
        tab_Weld.findChild(QtWidgets.QWidget, KEY_DP_WELD_MATERIAL_G_O).setText(str(material.fu))

        if module not in [KEY_DISP_BASE_PLATE]:
            material_connector = tab_Connector.findChild(QtWidgets.QWidget, KEY_PLATE_MATERIAL)
            material_connector.setCurrentText(str(material_grade))

            def f(material_g):
                m = Material(material_g)
                tab_Connector.findChild(QtWidgets.QWidget, KEY_PLATE_FU).setText(str(m.fu))
                tab_Connector.findChild(QtWidgets.QWidget, KEY_PLATE_FY).setText(str(m.fy))

            material_connector.currentIndexChanged.connect(lambda: f(material_connector.currentText()))
            tab_Connector.findChild(QtWidgets.QWidget, KEY_PLATE_FU).setText(str(material.fu))
            tab_Connector.findChild(QtWidgets.QWidget, KEY_PLATE_FY).setText(str(material.fy))
        else:
            pass

        if module == KEY_DISP_COLUMNCOVERPLATE:
            designation_col = key_5.currentText()
            if key_5.currentIndex() != 0:
                self.designPrefDialog.column_preferences(designation_col, table_1, material_grade)
        elif module == KEY_DISP_BEAMCOVERPLATE:
            designation_bm = key_5.currentText()
            if key_5.currentIndex() != 0:
                self.designPrefDialog.beam_preferences(designation_bm, material_grade)
        elif module == KEY_DISP_COMPRESSION:
            designation = self.design_inputs[KEY_SECSIZE]
            if key_6.currentIndex() == 0:
                self.designPrefDialog.ui.tabWidget.removeTab(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Column))
                self.designPrefDialog.ui.tabWidget.removeTab(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Angle))
                if tab_Beam is not None:
                    self.designPrefDialog.ui.tabWidget.insertTab(0, tab_Beam, KEY_DISP_BEAMSEC)
                self.designPrefDialog.beam_preferences(designation[0], material_grade)
                designation_list = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC)
                designation_list.setCurrentIndex(0)
                designation_list.clear()
                for item in designation:
                    designation_list.addItem(item)
                designation_list.currentIndexChanged.connect(lambda: self.designPrefDialog.beam_preferences(
                    designation_list.currentText() if designation_list.currentText() else 'JB 150', material_grade))
            elif key_6.currentIndex() == 1:
                self.designPrefDialog.ui.tabWidget.removeTab(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Beam))
                self.designPrefDialog.ui.tabWidget.removeTab(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Angle))
                self.designPrefDialog.column_preferences(designation[0], table_1, material_grade)
                if tab_Column is not None:
                    self.designPrefDialog.ui.tabWidget.insertTab(0, tab_Column, KEY_DISP_COLSEC)
                designation_list = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC)
                designation_list.setCurrentIndex(0)
                designation_list.clear()
                for item in designation:
                    designation_list.addItem(item)
                designation_list.currentIndexChanged.connect(lambda: self.designPrefDialog.column_preferences(
                    designation_list.currentText() if designation_list.currentText() else 'HB 150', table_1, material_grade))
            elif key_6.currentIndex() in [2, 4, 6]:
                self.designPrefDialog.ui.tabWidget.removeTab(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Beam))
                self.designPrefDialog.ui.tabWidget.removeTab(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Column))
                if tab_Angle is not None:
                    self.designPrefDialog.ui.tabWidget.insertTab(0, tab_Angle, DISP_TITLE_ANGLE)
                # self.designPrefDialog.ui.tabWidget.removeTab(
                #     self.designPrefDialog.ui.tabWidget.indexOf(tab_Beam))
                # table_c = "Angles"
            elif key_6.currentIndex() in [3, 5]:
                pass
                # self.designPrefDialog.ui.tabWidget.removeTab(
                #     self.designPrefDialog.ui.tabWidget.indexOf(tab_Beam))
                # table_c = "Channels"

            # designation_col = 'JB 150'
            # designation_col = 'HB 150'
            # designation_col = '20 20 X 3'
            # designation_col = 'JC 100'
            # if key_5.currentIndex() == 0:
            # if designation_col[0] == 'Select Section':
            #     print(designation_col[1])
            # else:
            #     print(designation_col[0])
            # self.designPrefDialog.column_preferences(designation_col[0], table_c, material_grade)

        elif module == KEY_DISP_BASE_PLATE:
            bp_list = []
            anchor_dia = self.design_inputs[KEY_DIA_ANCHOR][0]
            anchor_typ = self.design_inputs[KEY_TYP_ANCHOR]
            designation_col = key_2.currentText()
            self.designPrefDialog.column_preferences(designation_col, table_1, material_grade)
            self.designPrefDialog.anchor_bolt_preferences(anchor_dia, anchor_typ)
            bp_material = tab_Base_Plate.findChild(QtWidgets.QWidget, KEY_BASE_PLATE_MATERIAL)
            bp_material.setText(str(material_grade))
            bp_fu = tab_Base_Plate.findChild(QtWidgets.QWidget, KEY_BASE_PLATE_FU)
            bp_list.append(bp_fu)
            bp_fu.setText(str(material.fu))
            bp_fy = tab_Base_Plate.findChild(QtWidgets.QWidget, KEY_BASE_PLATE_FY)
            bp_list.append(bp_fy)
            bp_fy.setText(str(material.fy))

            for bp in bp_list:
                if bp.text() != "":
                    self.designPrefDialog.fu_fy_validation_connect(bp_list, bp)


        elif module not in [KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_BEAMCOVERPLATE, KEY_DISP_COMPRESSION, KEY_DISP_TENSION,
                            KEY_DISP_BASE_PLATE]:
            conn = key_1.currentText()

            if conn in VALUES_CONN_1:
                self.designPrefDialog.column_preferences(key_2.currentText(), table_1, material_grade)
                self.designPrefDialog.beam_preferences(key_3.currentText(), material_grade)
                column_material = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_MATERIAL)
                column_material.currentIndexChanged.connect(lambda: self.designPrefDialog.column_preferences(
                    key_2.currentText(), table_1, column_material.currentText()))
                beam_material = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_MATERIAL)
                beam_material.currentIndexChanged.connect(lambda: self.designPrefDialog.beam_preferences(
                    key_3.currentText(), beam_material.currentText()))

            elif conn in VALUES_CONN_2:
                self.designPrefDialog.ui.tabWidget.setTabText(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Column), KEY_DISP_PRIBM)
                self.designPrefDialog.ui.tabWidget.setTabText(
                    self.designPrefDialog.ui.tabWidget.indexOf(tab_Beam), KEY_DISP_SECBM)
                self.designPrefDialog.column_preferences(key_2.currentText(), table_2, material_grade)
                self.designPrefDialog.beam_preferences(key_3.currentText(), material_grade)
                column_material = tab_Column.findChild(QtWidgets.QWidget, KEY_SUPTNGSEC_MATERIAL)
                column_material.currentIndexChanged.connect(lambda: self.designPrefDialog.column_preferences(
                    key_2.currentText(), table_2, column_material.currentText()))
                beam_material = tab_Beam.findChild(QtWidgets.QWidget, KEY_SUPTDSEC_MATERIAL)
                beam_material.currentIndexChanged.connect(lambda: self.designPrefDialog.beam_preferences(
                    key_3.currentText(), beam_material.currentText()))

    def create_design_report(self):
        self.create_report.show()

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