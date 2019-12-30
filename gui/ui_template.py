# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/gui/ui_template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWidgets import QMessageBox, qApp
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice,pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import os
import json
import logging
from drawing_2D.Svg_Window import SvgWindow
import sys
import sqlite3
import shutil
import openpyxl

from Common import *
from utils.common.component import Section,I_sectional_Properties
from utils.common.component import *
from .customized_popup import Ui_Popup
from .ui_design_preferences import Ui_Dialog


class Ui_ModuleWindow(QMainWindow):

    closed = pyqtSignal()
    def open_popup(self, op,  KEYEXISTING_CUSTOMIZED):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Popup()
        self.ui.setupUi(self.window)
        self.ui.addAvailableItems(op, KEYEXISTING_CUSTOMIZED)
        self.ui.pushButton_5.clicked.connect(self.window.close)
        self.window.exec()
        return self.ui.get_right_elements()

    # def close(self):
    #     self.window.close()
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

        option_list = main.input_values(self)
        _translate = QtCore.QCoreApplication.translate

        i = 0
        for option in option_list:
            lable = option[1]
            type = option[2]
            # value = option[4]
            if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE]:
                l = QtWidgets.QLabel(self.dockWidgetContents)
                l.setGeometry(QtCore.QRect(6, 10 + i, 120, 25))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(option[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))

            if type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
                combo = QtWidgets.QComboBox(self.dockWidgetContents)
                combo.setGeometry(QtCore.QRect(150, 10 + i, 160, 27))
                # combo.setMaxVisibleItems(5)
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setObjectName(option[0])
                for item in option[4]:
                    combo.addItem(item)
                # combo.setMaxVisibleItems(int(5))

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.dockWidgetContents)
                r.setGeometry(QtCore.QRect(150,10 + i, 160, 27))
                font = QtGui.QFont()
                font.setPointSize(11)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(option[0])

            if type == TYPE_MODULE:
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", option[1]))
                i = i - 30

            if type == TYPE_IMAGE:
                im = QtWidgets.QLabel(self.dockWidgetContents)
                im.setGeometry(QtCore.QRect(190, 10 + i, 70, 57))
                im.setObjectName(option[0])
                im.setScaledContents(True)
                pixmap = QPixmap("./ResourceFiles/images/fin_cf_bw.png")
                im.setPixmap(pixmap)
                i = i + 30

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.dockWidgetContents)
                q.setGeometry(QtCore.QRect(3, 10 + i, 201, 25))
                font = QtGui.QFont()
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))

            i = i + 30


        new_list = main.customized_input(main)

        data = {}

        for t in new_list:
            if t[0] == KEY_PLATETHK:
                key_customized_1 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_1.activated.connect(lambda: popup(key_customized_1, new_list))
                data[t[0] + "_customized"] = t[1]()
            elif t[0] == KEY_GRD:
                key_customized_2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_2.activated.connect(lambda: popup(key_customized_2, new_list))
                data[t[0] + "_customized"] = t[1]()
            elif t[0] == KEY_D:
                key_customized_3 = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
                key_customized_3.activated.connect(lambda: popup(key_customized_3, new_list))
                data[t[0] + "_customized"] = t[1]()
            else:
                pass

        def popup(key, for_custom_list):
            for c_tup in for_custom_list:
                if c_tup[0] != key.objectName():
                    continue
                selected = key.currentText()
                f = c_tup[1]
                options = f()
                existing_options = data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    data[c_tup[0] + "_customized"] = self.open_popup(options, existing_options)
                else:
                    data[c_tup[0] + "_customized"] = f()

        updated_list = main.input_value_changed(main)

        for t in updated_list:
            key_changed = self.dockWidgetContents.findChild(QtWidgets.QWidget, t[0])
            key_changed.currentIndexChanged.connect(lambda: change(key_changed, updated_list))

        def change(k1, new):

            for tup in new:
                (object_name, k2_key, typ, f) = tup
                if object_name != k1.objectName():
                    continue
                if typ == TYPE_LABEL:
                    k2_key = k2_key + "_label"
                k2 = self.dockWidgetContents.findChild(QtWidgets.QWidget, k2_key)
                val = f(k1.currentText())
                k2.clear()
                if typ == TYPE_COMBOBOX:
                    for values in val:
                        k2.addItem(values)
                elif typ == TYPE_LABEL:
                    k2.setText(val)
                elif typ == TYPE_IMAGE:
                    pixmap1 = QPixmap(val)
                    k2.setPixmap(pixmap1)
                else:
                    pass

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
        self.actionDesign_Preferences.triggered.connect(self.design_preferences)
        self.actionDesign_Preferences.triggered.connect(self.column_design_prefer)
        self.actionDesign_Preferences.triggered.connect(self.beam_design_prefer)
        self.designPrefDialog = DesignPreferences(self)
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

        self.retranslateUi(MainWindow)
        self.mytabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.action_save_input.triggered.connect(lambda: self.design_fn(option_list, main, data))
        self.action_save_input.triggered.connect(lambda: self.saveDesign_inputs(option_list, data))
        self.action_load_input.triggered.connect(lambda: self.loadDesign_inputs(option_list, data, new_list))
        self.btn_Reset.clicked.connect(lambda: self.reset_fn(option_list))
        self.btn_Design.clicked.connect(lambda: self.design_fn(option_list, main, data))
        self.btn_Reset.clicked.connect(lambda: self.reset_popup(new_list, data))

    def reset_popup(self, new_list, data):
        for custom_combo in new_list:
            data[custom_combo[0] + "_customized"] = custom_combo[1]()

    def reset_fn(self, op_list):
        for op in op_list:
            widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0])
            if op[2] == TYPE_COMBOBOX or op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                widget.setCurrentIndex(0)
            elif op[2] == TYPE_TEXTBOX:
                widget.setText('')
            else:
                pass

    def design_fn(self, op_list, main, data_list):
        design_dictionary = {}

        for op in op_list:
            widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0])
            if op[2] == TYPE_COMBOBOX:
                des_val = widget.currentText()
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_MODULE:
                des_val = op[1]
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                des_val = data_list[op[0]+"_customized"]
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_TEXTBOX:
                des_val = widget.text()
                d1 = {op[0]: des_val}
            else:
                d1 = {}
            design_dictionary.update(d1)
        design_dictionary.update(self.designPrefDialog.save_designPref_para())
        main.to_get_d(design_dictionary)
        self.design_inputs = design_dictionary

    def saveDesign_inputs(self, op_list, data_list):
        path = r'C:\Users\Win10\Desktop'
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Design", os.path.join(str(path), "untitled.osi"),
                                                  "Input Files(*.osi)")
        # design_dictionary = {}
        # for op in op_list:
        #     widget = self.dockWidgetContents.findChild(QtWidgets.QWidget, op[0])
        #     if op[2] == TYPE_COMBOBOX:
        #         des_val = widget.currentText()
        #         d1 = {op[0]: des_val}
        #     elif op[2] == TYPE_MODULE:
        #         des_val = op[1]
        #         d1 = {op[0]: des_val}
        #     elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
        #         des_val = data_list[op[0]+"_customized"]
        #         d1 = {op[0]: des_val}
        #     elif op[2] == TYPE_TEXTBOX:
        #         des_val = widget.text()
        #         d1 = {op[0]: des_val}
        #     else:
        #         d1 = {}
        #     design_dictionary.update(d1)
        # design_dictionary.update(self.designPrefDialog.save_designPref_para())
        if not fileName:
            return
        try:
            with open(fileName, 'w') as input_file:
                json.dump(self.design_inputs, input_file)
        except Exception as e:
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s" % (fileName, str(e)))
            return

    def loadDesign_inputs(self, op_list, data, new):
        path = r'C:\Users\Win10\Desktop'
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Design", str(path), "InputFiles(*.osi)")
        if not fileName:
            return
        try:
            in_file = str(fileName)
            with open(in_file, 'r') as fileObject:
                uiObj = json.load(fileObject)
            self.setDictToUserInputs(uiObj, op_list, data, new)

        except IOError:
            QMessageBox.information(self, "Unable to open file",
                                    "There was an error opening \"%s\"" % fileName)
            return

    def setDictToUserInputs(self, uiObj, op_list, data, new):
        for op in op_list:
            key_str = op[0]
            key = self.dockWidgetContents.findChild(QtWidgets.QWidget, key_str)
            if op[2] == TYPE_COMBOBOX:
                index = key.findText(uiObj[key_str], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    key.setCurrentIndex(index)
            elif op[2] == TYPE_TEXTBOX:
                key.setText(uiObj[key_str])
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                for n in new:
                    if n[0] == key_str:
                        if uiObj[key_str] != n[1]():
                            data[key_str + "_customized"] = uiObj[key_str]
                            key.setCurrentIndex(1)
                        else:
                            pass
            else:
                pass



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        #MainWindow.setWindowTitle(_translate("MainWindow", "Fin Plate"))
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

    def dockbtn_clicked(self, widget):

        '''(QWidget) -> None
        This method dock and undock widget(QdockWidget)
        '''

        flag = widget.isHidden()
        if (flag):
            widget.show()
        else:
            widget.hide()

    def design_preferences(self):
        self.designPrefDialog.exec()

    def column_design_prefer(self):
        # designation = str(self.ui.combo_columnSec.currentText())
        #TODO:ADD FUNCTION TO GET designation, FY,FU
        designation = "HB 150"
        ultimateStrength_Column = "410"
        yieldStrength_Column = "250"
        self.designPrefDialog.column_preferences(designation, ultimateStrength_Column, yieldStrength_Column)

    def beam_design_prefer(self):
        # designation = str(self.ui.combo_beamSec.currentText())
        #TODO:ADD FUNCTION TO GET designation, FY,FU
        designation = "JB 150"
        ultimateStrength_Column = "410"
        yieldStrength_Column = "250"
        self.designPrefDialog.beam_preferences(designation, ultimateStrength_Column, yieldStrength_Column)

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
        # self.save_default_para()
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_weldFu.setValidator(dbl_validator)
        self.ui.txt_weldFu.setMaxLength(7)
        # self.ui.btn_defaults.clicked.connect(self.save_default_para)
        # self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_save.hide()
        self.ui.btn_close.clicked.connect(self.close_designPref)
        # self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)
        self.ui.pushButton_Import_Column.setDisabled(True)
        self.ui.pushButton_Import_Beam.setDisabled(True)
        self.ui.pushButton_Add_Column.clicked.connect(self.add_ColumnPref)
        self.ui.pushButton_Add_Beam.clicked.connect(self.add_BeamPref)
        self.ui.pushButton_Clear_Column.clicked.connect(self.clear_ColumnPref)
        self.ui.pushButton_Clear_Beam.clicked.connect(self.clear_BeamPref)
        self.ui.pushButton_Download_Column.clicked.connect(self.download_Database_Column)
        self.ui.pushButton_Download_Beam.clicked.connect(self.download_Database_Beam)

        self.ui.pushButton_Import_Column.clicked.connect(self.import_ColumnPref)
        self.ui.pushButton_Import_Beam.clicked.connect(self.import_BeamPref)
        #self.ui.btn_save.clicked.connect(Ui_ModuleWindow.design_preferences(Ui_ModuleWindow()))
        #self.ui.combo_boltHoleType.currentIndexChanged.connect(my_fn)
        #self.ui.btn_save.clicked.connect(self.save_fn)
        self.ui.btn_defaults.clicked.connect(self.default_fn)

    def default_fn(self):
        for children in self.ui.tab_Bolt.children():
            if children.objectName() == 'combo_boltHoleType':
                children.setCurrentIndex(0)
            elif children.objectName() == 'txt_boltFu':
                children.setText('800')
            elif children.objectName() == 'combo_slipfactor':
                children.setCurrentIndex(8)
            else:
                pass
        for children in self.ui.tab_Weld.children():
            if children.objectName() == 'combo_weldType':
                children.setCurrentIndex(0)
            elif children.objectName() == 'txt_weldFu':
                children.setText('410')
            else:
                pass
        for children in self.ui.tab_Detailing.children():
            if children.objectName() == 'combo_detailingEdgeType':
                children.setCurrentIndex(0)
            elif children.objectName() == 'txt_detailingGap':
                children.setText('10')
            elif children.objectName() == 'combo_detailing_memebers':
                children.setCurrentIndex(0)
            else:
                pass
        for children in self.ui.tab_Design.children():
            if children.objectName() == 'combo_design_method':
                children.setCurrentIndex(0)
            else:
                pass

    # def save_fn(self):
    #     for children in self.ui.tab_Bolt.children():
    #         if isinstance(children, QtWidgets.QComboBox):
    #             children.setCurrentIndex(children.currentIndex())
    #             print('check')

    def save_designPref_para(self):
        """This routine is responsible for saving all design preferences selected by the user
        """
        key_boltHoleType = self.ui.tab_Bolt.findChild(QtWidgets.QWidget, "combo_boltHoleType")
        combo_boltHoleType = key_boltHoleType.currentText()
        key_boltFu = self.ui.tab_Bolt.findChild(QtWidgets.QWidget, "txt_boltFu")
        line_boltFu = key_boltFu.text()
        key_slipfactor = self.ui.tab_Bolt.findChild(QtWidgets.QWidget, "combo_slipfactor")
        combo_slipfactor = key_slipfactor.currentText()
        key_weldType = self.ui.tab_Weld.findChild(QtWidgets.QWidget, "combo_weldType")
        combo_weldType = key_weldType.currentText()
        key_weldFu = self.ui.tab_Weld.findChild(QtWidgets.QWidget, "txt_weldFu")
        line_weldFu = key_weldFu.text()
        key_detailingEdgeType = self.ui.tab_Detailing.findChild(QtWidgets.QWidget, "combo_detailingEdgeType")
        combo_detailingEdgeType = key_detailingEdgeType.currentText()
        key_detailingGap = self.ui.tab_Detailing.findChild(QtWidgets.QWidget, "txt_detailingGap")
        line_detailingGap = key_detailingGap.text()
        key_detailing_memebers = self.ui.tab_Detailing.findChild(QtWidgets.QWidget, "combo_detailing_memebers")
        combo_detailing_memebers = key_detailing_memebers.currentText()
        key_design_method = self.ui.tab_Design.findChild(QtWidgets.QWidget, "combo_design_method")
        combo_design_method = key_design_method.currentText()
        d1 = {KEY_DP_BOLT_HOLE_TYPE: combo_boltHoleType,
              KEY_DP_BOLT_MATERIAL_G_O: line_boltFu,
              KEY_DP_BOLT_SLIP_FACTOR: combo_slipfactor,
              KEY_DP_WELD_TYPE: combo_weldType,
              KEY_DP_WELD_MATERIAL_G_O: line_weldFu,
              KEY_DP_DETAILING_EDGE_TYPE: combo_detailingEdgeType,
              KEY_DP_GAP: line_detailingGap,
              KEY_DP_DETAILING_CORROSIVE_INFLUENCES: combo_detailing_memebers, KEY_DP_DESIGN_METHOD: combo_design_method}
        return d1

    def highlight_slipfactor_description(self):
        """Highlight the description of currosponding slipfactor on selection of inputs
        Note : This routine is not in use in current version
        :return:
        """
        slip_factor = str(self.ui.combo_slipfactor.currentText())
        self.textCursor = QTextCursor(self.ui.textBrowser.document())
        cursor = self.textCursor
        # Setup the desired format for matches
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("red")))
        # Setup the regex engine
        pattern = str(slip_factor)
        regex = QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.ui.textBrowser.toPlainText(), pos)
        while (index != -1):
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfLine, 1)
            # cursor.movePosition(QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.ui.textBrowser.toPlainText(), pos)

    # def connect_to_database_update_other_attributes(self, table, designation):
    #     self.path_to_database = "ResourceFiles/Database/Intg_osdag.sqlite"
    #     conn = sqlite3.connect(self.path_to_database)
    #     db_query = "SELECT * FROM " + table + " WHERE Designation = ?"
    #     cur = conn.cursor()
    #     cur.execute(db_query, (designation,))
    #     row = cur.fetchone()
    #     self.mass = row[2]
    #     self.area = row[3]
    #     self.depth = row[4]
    #     self.flange_width = row[5]
    #     self.web_thickness = row[6]
    #     self.flange_thickness = row[7]
    #     self.flange_slope = row[8]
    #     self.root_radius = row[9]
    #     self.toe_radius = row[10]
    #     self.mom_inertia_z = row[11]
    #     self.mom_inertia_y = row[12]
    #     self.rad_of_gy_z = row[13]
    #     self.rad_of_gy_y = row[14]
    #     self.elast_sec_mod_z = row[15]
    #     self.elast_sec_mod_y = row[16]
    #     self.plast_sec_mod_z = row[17]
    #     self.plast_sec_mod_y = row[18]
    #     self.source = row[19]
    #
    #     conn.close()
    def column_preferences(self, designation, ultimateStrength_Column, yieldStrength_Column):
        col_attributes = Section(designation)
        Section.connect_to_database_update_other_attributes(col_attributes,"Columns", designation)
        self.ui.lineEdit_Designation_Column.setText(designation)
        self.ui.lineEdit_Source_Column.setText(col_attributes.source)
        self.ui.lineEdit_UltimateStrength_Column.setText(str(ultimateStrength_Column))
        self.ui.lineEdit_YieldStrength_Column.setText(str(yieldStrength_Column))
        self.ui.lineEdit_Depth_Column.setText(str(col_attributes.depth))
        self.ui.lineEdit_FlangeWidth_Column.setText(str(col_attributes.flange_width))
        self.ui.lineEdit_FlangeThickness_Column.setText(str(col_attributes.flange_thickness))
        self.ui.lineEdit_WeBThickness_Column.setText(str(col_attributes.web_thickness))
        self.ui.lineEdit_FlangeSlope_Column.setText(str(col_attributes.flange_slope))
        self.ui.lineEdit_RootRadius_Column.setText(str(col_attributes.root_radius))
        self.ui.lineEdit_ToeRadius_Column.setText(str(col_attributes.toe_radius))
        self.ui.lineEdit_ModElasticity_Column.setText("200")
        self.ui.lineEdit_ModElasticity_Column.setDisabled(True)
        self.ui.lineEdit_ModulusOfRigidity_Column.setText("76.9")
        self.ui.lineEdit_ModulusOfRigidity_Column.setDisabled(True)
        self.ui.lineEdit_PoissionsRatio_Column.setText("0.3")
        self.ui.lineEdit_PoissionsRatio_Column.setDisabled(True)
        self.ui.lineEdit_ThermalExpansion_Column.setText("12")
        self.ui.lineEdit_ThermalExpansion_Column.setDisabled(True)
        self.ui.lineEdit_Mass_Column.setText(str(col_attributes.mass))
        self.ui.lineEdit_SectionalArea_Column.setText(str(col_attributes.area))
        self.ui.lineEdit_MomentOfAreaZ_Column.setText(str(col_attributes.mom_inertia_z))
        self.ui.lineEdit_MomentOfAreaY_Column.setText(str(col_attributes.mom_inertia_y))
        self.ui.lineEdit_RogZ_Column.setText(str(col_attributes.rad_of_gy_z))
        self.ui.lineEdit_RogY_Column.setText(str(col_attributes.rad_of_gy_y))
        self.ui.lineEdit_ElasticModZ_Column.setText(str(col_attributes.elast_sec_mod_z))
        self.ui.lineEdit_ElasticModY_Column.setText(str(col_attributes.elast_sec_mod_y))
        self.ui.lineEdit_ElasticModPZ_Column.setText(str(col_attributes.plast_sec_mod_z))
        self.ui.lineEdit_ElasticModPY_Column.setText(str(col_attributes.plast_sec_mod_y))
        self.ui.pushButton_Add_Column.setEnabled(True)

        if (
                self.ui.lineEdit_Depth_Column.text() != "" and self.ui.lineEdit_FlangeWidth_Column.text() != "" and self.ui.lineEdit_FlangeThickness_Column.text() != ""
                and self.ui.lineEdit_WeBThickness_Column.text() != ""):
            self.ui.lineEdit_Depth_Column.textChanged.connect(self.new_sectionalprop_Column)
            self.ui.lineEdit_FlangeWidth_Column.textChanged.connect(self.new_sectionalprop_Column)
            self.ui.lineEdit_FlangeThickness_Column.textChanged.connect(self.new_sectionalprop_Column)
            self.ui.lineEdit_WeBThickness_Column.textChanged.connect(self.new_sectionalprop_Column)

    def beam_preferences(self, designation, ultimateStrength_Beam, yieldStrength_Beam):
        beam_attributes = Section(designation)
        Section.connect_to_database_update_other_attributes(beam_attributes, "Beams", designation)
        self.ui.lineEdit_Designation_Beam.setText(designation)
        self.ui.lineEdit_Source_Beam.setText(str(beam_attributes.source))
        self.ui.lineEdit_UltimateStrength_Beam.setText(ultimateStrength_Beam)
        self.ui.lineEdit_YieldStrength_Beam.setText(yieldStrength_Beam)
        self.ui.lineEdit_Depth_Beam.setText(str(beam_attributes.depth))
        self.ui.lineEdit_FlangeWidth_Beam.setText(str(beam_attributes.flange_width))
        self.ui.lineEdit_FlangeThickness_Beam.setText(str(beam_attributes.flange_thickness))
        self.ui.lineEdit_WeBThickness_Beam.setText(str(beam_attributes.web_thickness))
        self.ui.lineEdit_FlangeSlope_Beam.setText(str(beam_attributes.flange_slope))
        self.ui.lineEdit_RootRadius_Beam.setText(str(beam_attributes.root_radius))
        self.ui.lineEdit_ToeRadius_Beam.setText(str(beam_attributes.toe_radius))
        self.ui.lineEdit_ModElasticity_Beam.setText("200")
        self.ui.lineEdit_ModElasticity_Beam.setDisabled(True)
        self.ui.lineEdit_ModulusOfRigidity_Beam.setText("76.9")
        self.ui.lineEdit_ModulusOfRigidity_Beam.setDisabled(True)
        self.ui.lineEdit_PoissonsRatio_Beam.setText("0.3")
        self.ui.lineEdit_PoissonsRatio_Beam.setDisabled(True)
        self.ui.lineEdit_ThermalExpansion_Beam.setText("12")
        self.ui.lineEdit_ThermalExpansion_Beam.setDisabled(True)
        self.ui.lineEdit_Mass_Beam.setText(str(beam_attributes.mass))
        self.ui.lineEdit_SectionalArea_Beam.setText(str(beam_attributes.area))
        self.ui.lineEdit_MomentOfAreaZ_Beam.setText(str(beam_attributes.mom_inertia_z))
        self.ui.lineEdit_MomentOfAreaY_Beam.setText(str(beam_attributes.mom_inertia_y))
        self.ui.lineEdit_RogZ_Beam.setText(str(beam_attributes.rad_of_gy_z))
        self.ui.lineEdit_RogY_Beam.setText(str(beam_attributes.rad_of_gy_y))
        self.ui.lineEdit_ElasticModZ_Beam.setText(str(beam_attributes.elast_sec_mod_z))
        self.ui.lineEdit_ElasticModY_Beam.setText(str(beam_attributes.elast_sec_mod_y))
        self.ui.lineEdit_ElasticModPZ_Beam.setText(str(beam_attributes.plast_sec_mod_z))
        self.ui.lineEdit_ElasticModPY_Beam.setText(str(beam_attributes.plast_sec_mod_y))
        self.ui.pushButton_Add_Beam.setEnabled(True)

        if (
                self.ui.lineEdit_Depth_Beam.text() != "" and self.ui.lineEdit_FlangeWidth_Beam.text() != "" and self.ui.lineEdit_FlangeThickness_Beam.text() != ""
                and self.ui.lineEdit_WeBThickness_Beam.text() != ""):
            self.ui.lineEdit_Depth_Beam.textChanged.connect(self.new_sectionalprop_Beam)
            self.ui.lineEdit_FlangeWidth_Beam.textChanged.connect(self.new_sectionalprop_Beam)
            self.ui.lineEdit_FlangeThickness_Beam.textChanged.connect(self.new_sectionalprop_Beam)
            self.ui.lineEdit_WeBThickness_Beam.textChanged.connect(self.new_sectionalprop_Beam)

    def new_sectionalprop_Column(self):
        if self.ui.lineEdit_Depth_Column.text() == "":
            return
        else:
            D = float(self.ui.lineEdit_Depth_Column.text())

        if self.ui.lineEdit_FlangeWidth_Column.text() == "":
            return
        else:
            B = float(self.ui.lineEdit_FlangeWidth_Column.text())

        if self.ui.lineEdit_FlangeThickness_Column.text() == "":
            return
        else:
            t_w = float(self.ui.lineEdit_FlangeThickness_Column.text())

        if self.ui.lineEdit_WeBThickness_Column.text() == "":
            return
        else:
            t_f = float(self.ui.lineEdit_WeBThickness_Column.text())

        self.sectionalprop = I_sectional_Properties()
        self.ui.lineEdit_Mass_Column.setText(str(self.sectionalprop.calc_Mass(D, B, t_w, t_f)))
        self.ui.lineEdit_SectionalArea_Column.setText(str(self.sectionalprop.calc_Area(D, B, t_w, t_f)))
        self.ui.lineEdit_MomentOfAreaZ_Column.setText(str(self.sectionalprop.calc_MomentOfAreaZ(D, B, t_w, t_f)))
        self.ui.lineEdit_MomentOfAreaY_Column.setText(str(self.sectionalprop.calc_MomentOfAreaY(D, B, t_w, t_f)))
        self.ui.lineEdit_RogZ_Column.setText(str(self.sectionalprop.calc_RogZ(D, B, t_w, t_f)))
        self.ui.lineEdit_RogY_Column.setText(str(self.sectionalprop.calc_RogY(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModZ_Column.setText(str(self.sectionalprop.calc_ElasticModulusZz(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModY_Column.setText(str(self.sectionalprop.calc_ElasticModulusZy(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModPZ_Column.setText(str(self.sectionalprop.calc_PlasticModulusZpz(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModPY_Column.setText(str(self.sectionalprop.calc_PlasticModulusZpy(D, B, t_w, t_f)))

        self.ui.pushButton_Add_Column.setEnabled(True)

    def new_sectionalprop_Beam(self):
        if self.ui.lineEdit_Depth_Beam.text() == "":
            return
        else:
            D = float(self.ui.lineEdit_Depth_Beam.text())

        if self.ui.lineEdit_FlangeWidth_Beam.text() == "":
            return
        else:
            B = float(self.ui.lineEdit_FlangeWidth_Beam.text())

        if self.ui.lineEdit_FlangeThickness_Beam.text() == "":
            return
        else:
            t_w = float(self.ui.lineEdit_FlangeThickness_Beam.text())

        if self.ui.lineEdit_WeBThickness_Beam.text() == "":
            return
        else:
            t_f = float(self.ui.lineEdit_WeBThickness_Beam.text())

        self.sectionalprop = I_sectional_Properties()
        self.ui.lineEdit_Mass_Beam.setText(str(self.sectionalprop.calc_Mass(D, B, t_w, t_f)))
        self.ui.lineEdit_SectionalArea_Beam.setText(str(self.sectionalprop.calc_Area(D, B, t_w, t_f)))
        self.ui.lineEdit_MomentOfAreaZ_Beam.setText(str(self.sectionalprop.calc_MomentOfAreaZ(D, B, t_w, t_f)))
        self.ui.lineEdit_MomentOfAreaY_Beam.setText(str(self.sectionalprop.calc_MomentOfAreaY(D, B, t_w, t_f)))
        self.ui.lineEdit_RogZ_Beam.setText(str(self.sectionalprop.calc_RogZ(D, B, t_w, t_f)))
        self.ui.lineEdit_RogY_Beam.setText(str(self.sectionalprop.calc_RogY(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModZ_Beam.setText(str(self.sectionalprop.calc_ElasticModulusZz(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModY_Beam.setText(str(self.sectionalprop.calc_ElasticModulusZy(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModPZ_Beam.setText(str(self.sectionalprop.calc_PlasticModulusZpz(D, B, t_w, t_f)))
        self.ui.lineEdit_ElasticModPY_Beam.setText(str(self.sectionalprop.calc_PlasticModulusZpy(D, B, t_w, t_f)))
        self.ui.pushButton_Add_Beam.setEnabled(True)

    def add_ColumnPref(self):

        if (
                self.ui.lineEdit_Designation_Column.text() == "" or self.ui.lineEdit_Mass_Column.text() == "" or self.ui.lineEdit_SectionalArea_Column.text() == "" or self.ui.lineEdit_Depth_Column.text() == ""
                or self.ui.lineEdit_FlangeWidth_Column.text() == "" or self.ui.lineEdit_WeBThickness_Column.text() == "" or self.ui.lineEdit_FlangeThickness_Column.text() == "" or self.ui.lineEdit_FlangeSlope_Column.text() == ""
                or self.ui.lineEdit_RootRadius_Column.text() == "" or self.ui.lineEdit_ToeRadius_Column.text() == "" or self.ui.lineEdit_MomentOfAreaZ_Column.text() == "" or self.ui.lineEdit_MomentOfAreaY_Column.text() == ""
                or self.ui.lineEdit_RogZ_Column.text() == "" or self.ui.lineEdit_RogY_Column.text() == "" or self.ui.lineEdit_ElasticModZ_Column.text() == "" or self.ui.lineEdit_ElasticModY_Column.text() == ""
                or self.ui.lineEdit_Source_Column.text() == ""):
            QMessageBox.information(QMessageBox(), 'Warning', 'Please Fill all missing parameters!')
            self.ui.pushButton_Add_Column.setDisabled(True)


        else:
            self.ui.pushButton_Add_Column.setEnabled(True)
            Designation_c = self.ui.lineEdit_Designation_Column.text()
            Mass_c = float(self.ui.lineEdit_Mass_Column.text())
            Area_c = float(self.ui.lineEdit_SectionalArea_Column.text())
            D_c = float(self.ui.lineEdit_Depth_Column.text())
            B_c = float(self.ui.lineEdit_FlangeWidth_Column.text())
            tw_c = float(self.ui.lineEdit_WeBThickness_Column.text())
            T_c = float(self.ui.lineEdit_FlangeThickness_Column.text())
            FlangeSlope_c = int(self.ui.lineEdit_FlangeSlope_Column.text())
            R1_c = float(self.ui.lineEdit_RootRadius_Column.text())
            R2_c = float(self.ui.lineEdit_ToeRadius_Column.text())
            Iz_c = float(self.ui.lineEdit_MomentOfAreaZ_Column.text())
            Iy_c = float(self.ui.lineEdit_MomentOfAreaY_Column.text())
            rz_c = float(self.ui.lineEdit_RogZ_Column.text())
            ry_c = float(self.ui.lineEdit_RogY_Column.text())
            Zz_c = float(self.ui.lineEdit_ElasticModZ_Column.text())
            Zy_c = float(self.ui.lineEdit_ElasticModY_Column.text())
            if (self.ui.lineEdit_ElasticModPZ_Column.text() == "" or self.ui.lineEdit_ElasticModPY_Column.text() == ""):
                self.ui.lineEdit_ElasticModPZ_Column.setText("0")
                self.ui.lineEdit_ElasticModPY_Column.setText("0")
            Zpz_c = float(self.ui.lineEdit_ElasticModPZ_Column.text())
            Zpy_c = float(self.ui.lineEdit_ElasticModPY_Column.text())
            Source_c = self.ui.lineEdit_Source_Column.text()

            conn = sqlite3.connect(Component().path_to_database)

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Columns WHERE Designation = ?", (Designation_c,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Columns (Designation,Mass,Area,D,B,tw,T,R1,R2,Iz,Iy,rz,ry,
    				                                               Zz,zy,Zpz,Zpy,FlangeSlope,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (Designation_c, Mass_c, Area_c,
                           D_c, B_c, tw_c, T_c,
                           R1_c, R2_c, Iz_c, Iy_c, rz_c,
                           ry_c, Zz_c, Zy_c,
                           Zpz_c, Zpy_c, FlangeSlope_c, Source_c))
                conn.commit()
                c.close()
                conn.close()
                QMessageBox.information(QMessageBox(), 'Information', 'Data is added successfully to the database!')
            else:
                QMessageBox.information(QMessageBox(), 'Warning', 'Designation is already exist in Database!')
                self.clear_ColumnPref()

    def add_BeamPref(self):

        if (
                self.ui.lineEdit_Designation_Beam.text() == "" or self.ui.lineEdit_Mass_Beam.text() == "" or self.ui.lineEdit_SectionalArea_Beam.text() == "" or self.ui.lineEdit_Depth_Beam.text() == ""
                or self.ui.lineEdit_FlangeWidth_Beam.text() == "" or self.ui.lineEdit_WeBThickness_Beam.text() == "" or self.ui.lineEdit_FlangeThickness_Beam.text() == "" or self.ui.lineEdit_FlangeSlope_Beam.text() == ""
                or self.ui.lineEdit_RootRadius_Beam.text() == "" or self.ui.lineEdit_ToeRadius_Beam.text() == "" or self.ui.lineEdit_MomentOfAreaZ_Beam.text() == "" or self.ui.lineEdit_MomentOfAreaY_Beam.text() == ""
                or self.ui.lineEdit_RogZ_Beam.text() == "" or self.ui.lineEdit_RogY_Beam.text() == "" or self.ui.lineEdit_ElasticModZ_Beam.text() == "" or self.ui.lineEdit_ElasticModY_Beam.text() == ""
                or self.ui.lineEdit_Source_Beam.text() == ""):
            QMessageBox.information(QMessageBox(), 'Warning', 'Please Fill all missing parameters!')
            self.ui.pushButton_Add_Beam.setDisabled(True)

        else:
            self.ui.pushButton_Add_Beam.setEnabled(True)
            Designation_b = self.ui.lineEdit_Designation_Beam.text()
            Mass_b = float(self.ui.lineEdit_Mass_Beam.text())
            Area_b = float(self.ui.lineEdit_SectionalArea_Beam.text())
            D_b = float(self.ui.lineEdit_Depth_Beam.text())
            B_b = float(self.ui.lineEdit_FlangeWidth_Beam.text())
            tw_b = float(self.ui.lineEdit_WeBThickness_Beam.text())
            T_b = float(self.ui.lineEdit_FlangeThickness_Beam.text())
            FlangeSlope_b = int(self.ui.lineEdit_FlangeSlope_Beam.text())
            R1_b = float(self.ui.lineEdit_RootRadius_Beam.text())
            R2_b = float(self.ui.lineEdit_ToeRadius_Beam.text())
            Iz_b = float(self.ui.lineEdit_MomentOfAreaZ_Beam.text())
            Iy_b = float(self.ui.lineEdit_MomentOfAreaY_Beam.text())
            rz_b = float(self.ui.lineEdit_RogZ_Beam.text())
            ry_b = float(self.ui.lineEdit_RogY_Beam.text())
            Zz_b = float(self.ui.lineEdit_ElasticModZ_Beam.text())
            Zy_b = float(self.ui.lineEdit_ElasticModY_Beam.text())
            if (self.ui.lineEdit_ElasticModPZ_Beam.text() == "" or self.ui.lineEdit_ElasticModPY_Beam.text() == ""):
                self.ui.lineEdit_ElasticModPZ_Beam.setText("0")
                self.ui.lineEdit_ElasticModPY_Beam.setText("0")
            Zpz_b = float(self.ui.lineEdit_ElasticModPZ_Beam.text())
            Zpy_b = float(self.ui.lineEdit_ElasticModPY_Beam.text())
            Source_b = self.ui.lineEdit_Source_Beam.text()

            conn = sqlite3.connect(Component().path_to_database)

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_b,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,FlangeSlope,R1,R2,Iz,Iy,rz,ry,
    				                                                Zz,zy,Zpz,Zpy,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (Designation_b, Mass_b, Area_b,
                           D_b, B_b, tw_b, T_b, FlangeSlope_b,
                           R1_b, R2_b, Iz_b, Iy_b, rz_b,
                           ry_b, Zz_b, Zy_b,
                           Zpz_b, Zpy_b, Source_b))
                conn.commit()
                c.close()
                conn.close()
                QMessageBox.information(QMessageBox(), 'Information', 'Data is added successfully to the database.')
            else:
                QMessageBox.information(QMessageBox(), 'Warning', 'Designation is already exist in Database!')
                self.clear_BeamPref()

    def clear_ColumnPref(self):
        self.ui.lineEdit_Designation_Column.clear()
        self.ui.lineEdit_Source_Column.clear()
        self.ui.lineEdit_UltimateStrength_Column.clear()
        self.ui.lineEdit_YieldStrength_Column.clear()
        self.ui.lineEdit_Depth_Column.clear()
        self.ui.lineEdit_FlangeWidth_Column.clear()
        self.ui.lineEdit_FlangeThickness_Column.clear()
        self.ui.lineEdit_WeBThickness_Column.clear()
        self.ui.lineEdit_FlangeSlope_Column.clear()
        self.ui.lineEdit_RootRadius_Column.clear()
        self.ui.lineEdit_ToeRadius_Column.clear()
        self.ui.lineEdit_Mass_Column.clear()
        self.ui.lineEdit_SectionalArea_Column.clear()
        self.ui.lineEdit_MomentOfAreaZ_Column.clear()
        self.ui.lineEdit_MomentOfAreaY_Column.clear()
        self.ui.lineEdit_RogZ_Column.clear()
        self.ui.lineEdit_RogY_Column.clear()
        self.ui.lineEdit_ElasticModZ_Column.clear()
        self.ui.lineEdit_ElasticModY_Column.clear()
        self.ui.lineEdit_ElasticModPZ_Column.clear()
        self.ui.lineEdit_ElasticModPY_Column.clear()
        self.ui.pushButton_Add_Column.setDisabled(True)

    def clear_BeamPref(self):
        self.ui.lineEdit_Designation_Beam.clear()
        self.ui.lineEdit_Source_Beam.clear()
        self.ui.lineEdit_UltimateStrength_Beam.clear()
        self.ui.lineEdit_YieldStrength_Beam.clear()
        self.ui.lineEdit_Depth_Beam.clear()
        self.ui.lineEdit_FlangeWidth_Beam.clear()
        self.ui.lineEdit_FlangeThickness_Beam.clear()
        self.ui.lineEdit_WeBThickness_Beam.clear()
        self.ui.lineEdit_FlangeSlope_Beam.clear()
        self.ui.lineEdit_RootRadius_Beam.clear()
        self.ui.lineEdit_ToeRadius_Beam.clear()
        self.ui.lineEdit_Mass_Beam.clear()
        self.ui.lineEdit_SectionalArea_Beam.clear()
        self.ui.lineEdit_MomentOfAreaZ_Beam.clear()
        self.ui.lineEdit_MomentOfAreaY_Beam.clear()
        self.ui.lineEdit_RogZ_Beam.clear()
        self.ui.lineEdit_RogY_Beam.clear()
        self.ui.lineEdit_ElasticModZ_Beam.clear()
        self.ui.lineEdit_ElasticModY_Beam.clear()
        self.ui.lineEdit_ElasticModPZ_Beam.clear()
        self.ui.lineEdit_ElasticModPY_Beam.clear()
        self.ui.pushButton_Add_Beam.setDisabled(True)

    def download_Database_Column(self):
        file_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "add_sections.xlsx")))
        shutil.copyfile(file_path, os.path.join(str(self.folder), "images_html", "add_sections.xlsx"))
        QMessageBox.information(QMessageBox(), 'Information', 'Your File is Downloaded in your selected workspace')
        self.ui.pushButton_Import_Column.setEnabled(True)

    def download_Database_Beam(self):
        file_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "add_sections.xlsx")))
        shutil.copyfile(file_path, os.path.join(str(self.folder), "images_html", "add_sections.xlsx"))
        QMessageBox.information(QMessageBox(), 'Information', 'Your File is Downloaded in your selected workspace')
        self.ui.pushButton_Import_Beam.setEnabled(True)

    def import_ColumnPref(self):
        wb = openpyxl.load_workbook(os.path.join(str(self.folder), "images_html", "add_sections.xlsx"))
        sheet = wb['First Sheet']
        conn = sqlite3.connect('ResourceFiles/Database/Intg_osdag.sqlite')

        for rowNum in range(2, sheet.max_row + 1):
            designation = sheet.cell(row=rowNum, column=2).value
            mass = sheet.cell(row=rowNum, column=3).value
            area = sheet.cell(row=rowNum, column=4).value
            d = sheet.cell(row=rowNum, column=5).value
            b = sheet.cell(row=rowNum, column=6).value
            tw = sheet.cell(row=rowNum, column=7).value
            t = sheet.cell(row=rowNum, column=8).value
            flangeSlope = sheet.cell(row=rowNum, column=9).value
            r1 = sheet.cell(row=rowNum, column=10).value
            r2 = sheet.cell(row=rowNum, column=11).value
            iz = sheet.cell(row=rowNum, column=12).value
            iy = sheet.cell(row=rowNum, column=13).value
            rz = sheet.cell(row=rowNum, column=14).value
            ry = sheet.cell(row=rowNum, column=15).value
            zz = sheet.cell(row=rowNum, column=16).value
            zy = sheet.cell(row=rowNum, column=17).value
            zpz = sheet.cell(row=rowNum, column=18).value
            zpy = sheet.cell(row=rowNum, column=19).value
            source = sheet.cell(row=rowNum, column=20).value
            c = conn.cursor()
            c.execute("SELECT count(*) FROM Columns WHERE Designation = ?", (designation,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Columns (Designation,Mass,Area,D,B,tw,T,R1,R2,Iz,Iy,rz,ry,
    				                           Zz,zy,Zpz,Zpy,FlangeSlope,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (designation, mass, area,
                           d, b, tw, t,
                           r1, r2, iz, iy, rz, ry,
                           zz, zy
                           ,
                           zpz, zpy, flangeSlope, source))
                conn.commit()
                c.close()

        conn.close()
        QMessageBox.information(QMessageBox(), 'Successful', ' File data is imported successfully to the database.')
        self.ui.pushButton_Import_Column.setDisabled(True)

    def import_BeamPref(self):
        wb = openpyxl.load_workbook(os.path.join(str(self.folder), "images_html", "add_sections.xlsx"))
        sheet = wb['First Sheet']
        conn = sqlite3.connect('ResourceFiles/Database/Intg_osdag.sqlite')

        for rowNum in range(2, sheet.max_row + 1):
            designation = sheet.cell(row=rowNum, column=2).value
            mass = sheet.cell(row=rowNum, column=3).value
            area = sheet.cell(row=rowNum, column=4).value
            d = sheet.cell(row=rowNum, column=5).value
            b = sheet.cell(row=rowNum, column=6).value
            tw = sheet.cell(row=rowNum, column=7).value
            t = sheet.cell(row=rowNum, column=8).value
            flangeSlope = sheet.cell(row=rowNum, column=9).value
            r1 = sheet.cell(row=rowNum, column=10).value
            r2 = sheet.cell(row=rowNum, column=11).value
            iz = sheet.cell(row=rowNum, column=12).value
            iy = sheet.cell(row=rowNum, column=13).value
            rz = sheet.cell(row=rowNum, column=14).value
            ry = sheet.cell(row=rowNum, column=15).value
            zz = sheet.cell(row=rowNum, column=16).value
            zy = sheet.cell(row=rowNum, column=17).value
            zpz = sheet.cell(row=rowNum, column=18).value
            zpy = sheet.cell(row=rowNum, column=19).value
            source = sheet.cell(row=rowNum, column=20).value

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (designation,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,FlangeSlope,R1,R2,Iz,Iy,rz,ry,
            				                           Zz,zy,Zpz,Zpy,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (designation, mass, area,
                           d, b, tw, t,
                           flangeSlope, r1
                           ,
                           r2, iz, iy, rz, ry,
                           zz, zy
                           ,
                           zpz, zpy, source))
                conn.commit()
                c.close()

        conn.close()
        QMessageBox.information(QMessageBox(), 'Successful', ' File data is imported successfully to the database.')
        self.ui.pushButton_Import_Beam.setDisabled(True)

    def close_designPref(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        self.save_designPref_para()
        QCloseEvent.accept()

from . import icons_rc
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ModuleWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())