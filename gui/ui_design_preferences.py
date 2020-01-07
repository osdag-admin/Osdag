# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from Common import *
from utils.common.component import Section,I_sectional_Properties
from utils.common.component import *
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.shear_connection import ShearConnection

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
from PyQt5.QtGui import QStandardItem
import os
import json
import logging
from drawing_2D.Svg_Window import SvgWindow
import sys
import sqlite3
import shutil
import openpyxl


class Ui_Dialog(object):
    def setupUi(self, DesignPreferences):
        DesignPreferences.setObjectName("DesignPreferences")
        DesignPreferences.resize(969, 624)
        self.gridLayout_5 = QtWidgets.QGridLayout(DesignPreferences)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_defaults = QtWidgets.QPushButton(DesignPreferences)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_defaults.setFont(font)
        self.btn_defaults.setObjectName("btn_defaults")
        self.gridLayout_2.addWidget(self.btn_defaults, 0, 1, 1, 1)
        self.btn_save = QtWidgets.QPushButton(DesignPreferences)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout_2.addWidget(self.btn_save, 0, 2, 1, 1)
        self.btn_close = QtWidgets.QPushButton(DesignPreferences)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_close.setFont(font)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout_2.addWidget(self.btn_close, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 4, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(DesignPreferences)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Column = QtWidgets.QWidget()
        self.tab_Column.setObjectName("tab_Column")

        supporting_section_list = ShearConnection.supporting_section_values(self)
        _translate = QtCore.QCoreApplication.translate
        i = 0
        j = 6
        for element in supporting_section_list:
            lable = element[1]
            type = element[2]
            # value = option[4]
            if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                l = QtWidgets.QLabel(self.tab_Column)
                if lable in [KEY_DISP_SUPTNGSEC_THERMAL_EXP]:
                    l.setGeometry(QtCore.QRect(3 + j, 10 + i, 165, 28))
                else:
                    l.setGeometry(QtCore.QRect(3 + j, 10 + i, 165, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                if lable in [KEY_DISP_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_SOURCE]:
                    font.setWeight(75)
                else:
                    font.setWeight(50)
                l.setFont(font)
                l.setObjectName(element[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setAlignment(QtCore.Qt.AlignCenter)

            if type == TYPE_COMBOBOX:
                combo = QtWidgets.QComboBox(self.tab_Column)
                combo.setGeometry(QtCore.QRect(170 + j, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(element[0])
                for item in element[3]:
                    combo.addItem(item)

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.tab_Column)
                q.setGeometry(QtCore.QRect(j, 10 + i, 155, 35))
                font = QtGui.QFont()
                font.setPointSize(10)
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.tab_Column)
                r.setGeometry(QtCore.QRect(170 + j, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(element[0])
                if element[0] in [KEY_SUPTNGSEC_DEPTH, KEY_SUPTNGSEC_FLANGE_W, KEY_SUPTNGSEC_FLANGE_T, KEY_SUPTNGSEC_WEB_T]:
                    r.setValidator(QDoubleValidator())

            if type == TYPE_BREAK:
                j = j + 310
                i = -30

            if type == TYPE_ENTER:
                pass

            i = i + 30
        pushButton_Add_Column = QtWidgets.QPushButton(self.tab_Column)
        pushButton_Add_Column.setObjectName("pushButton_Add_Column")
        pushButton_Add_Column.setGeometry(QtCore.QRect(6, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Add_Column.setFont(font)
        pushButton_Add_Column.setText("Add")

        pushButton_Clear_Column = QtWidgets.QPushButton(self.tab_Column)
        pushButton_Clear_Column.setObjectName("pushButton_Clear_Column")
        pushButton_Clear_Column.setGeometry(QtCore.QRect(180, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Clear_Column.setFont(font)
        pushButton_Clear_Column.setText("Clear")

        pushButton_Import_Column = QtWidgets.QPushButton(self.tab_Column)
        pushButton_Import_Column.setObjectName("pushButton_Import_Column")
        pushButton_Import_Column.setGeometry(QtCore.QRect(770, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Import_Column.setFont(font)
        pushButton_Import_Column.setText("Import xlsx file")

        pushButton_Download_Column = QtWidgets.QPushButton(self.tab_Column)
        pushButton_Download_Column.setObjectName("pushButton_Download_Column")
        pushButton_Download_Column.setGeometry(QtCore.QRect(600, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Download_Column.setFont(font)
        pushButton_Download_Column.setText("Download xlsx file")

        self.tabWidget.addTab(self.tab_Column, "")
        self.tab_Beam = QtWidgets.QWidget()
        self.tab_Beam.setObjectName("tab_Beam")

        supported_section_list = ShearConnection.supported_section_values(self)
        _translate = QtCore.QCoreApplication.translate
        i = 0
        j = 6
        for element in supported_section_list:
            lable = element[1]
            type = element[2]
            # value = option[4]
            if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                l = QtWidgets.QLabel(self.tab_Beam)
                if lable in [KEY_DISP_SUPTNGSEC_THERMAL_EXP]:
                    l.setGeometry(QtCore.QRect(3 + j, 10 + i, 165, 28))
                else:
                    l.setGeometry(QtCore.QRect(3 + j, 10 + i, 165, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                if lable in [KEY_DISP_SUPTNGSEC_DESIGNATION, KEY_DISP_SUPTNGSEC_TYPE, KEY_DISP_SUPTNGSEC_SOURCE]:
                    font.setWeight(75)
                else:
                    font.setWeight(50)
                l.setFont(font)
                l.setObjectName(element[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setAlignment(QtCore.Qt.AlignCenter)

            if type == TYPE_COMBOBOX:
                combo = QtWidgets.QComboBox(self.tab_Beam)
                combo.setGeometry(QtCore.QRect(170 + j, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(element[0])
                for item in element[3]:
                    combo.addItem(item)

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.tab_Beam)
                q.setGeometry(QtCore.QRect(j, 10 + i, 155, 35))
                font = QtGui.QFont()
                font.setPointSize(10)
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.tab_Beam)
                r.setGeometry(QtCore.QRect(170 + j, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(element[0])
                if element[0] in [KEY_SUPTDSEC_DEPTH, KEY_SUPTDSEC_FLANGE_W, KEY_SUPTDSEC_FLANGE_T,
                               KEY_SUPTDSEC_WEB_T]:
                    r.setValidator(QDoubleValidator())

            if type == TYPE_BREAK:
                j = j + 310
                i = -30

            if type == TYPE_ENTER:
                pass

            i = i + 30
        pushButton_Add_Beam = QtWidgets.QPushButton(self.tab_Beam)
        pushButton_Add_Beam.setObjectName("pushButton_Add_Beam")
        pushButton_Add_Beam.setGeometry(QtCore.QRect(6, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Add_Beam.setFont(font)
        pushButton_Add_Beam.setText("Add")

        pushButton_Clear_Beam = QtWidgets.QPushButton(self.tab_Beam)
        pushButton_Clear_Beam.setObjectName("pushButton_Clear_Beam")
        pushButton_Clear_Beam.setGeometry(QtCore.QRect(180, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Clear_Beam.setFont(font)
        pushButton_Clear_Beam.setText("Clear")

        pushButton_Import_Beam = QtWidgets.QPushButton(self.tab_Beam)
        pushButton_Import_Beam.setObjectName("pushButton_Import_Beam")
        pushButton_Import_Beam.setGeometry(QtCore.QRect(770, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Import_Beam.setFont(font)
        pushButton_Import_Beam.setText("Import xlsx file")

        pushButton_Download_Beam = QtWidgets.QPushButton(self.tab_Beam)
        pushButton_Download_Beam.setObjectName("pushButton_Download_Beam")
        pushButton_Download_Beam.setGeometry(QtCore.QRect(600, 500, 160, 27))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        pushButton_Download_Beam.setFont(font)
        pushButton_Download_Beam.setText("Download xlsx file")

        self.tabWidget.addTab(self.tab_Beam, "")
        self.tab_Bolt = QtWidgets.QWidget()
        self.tab_Bolt.setObjectName("tab_Bolt")

        label_1 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        label_1.setFont(font)
        label_1.setObjectName("label_1")
        label_1.setGeometry(QtCore.QRect(10, 10, 130, 22))
        label_1.setText("Inputs")
        label_3 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setGeometry(QtCore.QRect(400, 10, 130, 22))
        label_3.setText("Description")
        textBrowser = QtWidgets.QTextBrowser(self.tab_Bolt)
        textBrowser.setMinimumSize(QtCore.QSize(210, 320))
        textBrowser.setObjectName("textBrowser")
        textBrowser.setGeometry(QtCore.QRect(400, 40, 520, 450))
        textBrowser.setHtml(_translate("DesignPreferences",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                            "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
                                            "<tr>\n"
                                            "<td colspan=\"3\">\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">IS 800 Table 20 Typical Average Values for Coefficient of Friction (</span><span style=\" font-family:\'Calibri,sans-serif\'; font-size:9pt;\">µ</span><span style=\" font-family:\'Calibri,sans-serif\'; font-size:9pt; vertical-align:sub;\">f</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">)</span></p></td></tr></table>\n"
                                            "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
                                            "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
                                            "<tr>\n"
                                            "<td width=\"26\"></td>\n"
                                            "<td width=\"383\">\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Treatment of Surfaces</span></p></td>\n"
                                            "<td width=\"78\">\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  µ_f</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">i)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces not treated</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.2</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">ii)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit with any loose rust removed, no pitting</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.5</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">iii)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit and hot-dip galvanized</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.1</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">iv)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit and spray - metallized with zinc (thickness 50-70 µm)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.25</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">v)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with ethylzinc silicate coat (thickness 30-60 µm)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">vi)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sand blasted surface, after light rusting</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.52</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">vii)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with ethylzinc silicate coat (thickness 60-80 µm)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">viii)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with alcalizinc silicate coat (thickness 60-80 µm)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">ix)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and spray metallized with aluminium (thickness &gt;50 µm)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.5</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">x)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Clean mill scale</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.33</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">xi)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sand blasted surface</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.48</span></p></td></tr>\n"
                                            "<tr>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">xii)</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Red lead painted surface</span></p></td>\n"
                                            "<td>\n"
                                            "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.1</span></p>\n"
                                            "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></td></tr></table></body></html>"))

        bolt_list = ShearConnection.bolt_values(self)
        _translate = QtCore.QCoreApplication.translate
        i = 40
        for element in bolt_list:
            lable = element[1]
            type = element[2]
            # value = option[4]
            if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                l = QtWidgets.QLabel(self.tab_Bolt)
                l.setGeometry(QtCore.QRect(6, 10 + i, 185, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(element[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setAlignment(QtCore.Qt.AlignCenter)

            if type == TYPE_COMBOBOX:
                combo = QtWidgets.QComboBox(self.tab_Bolt)
                combo.setGeometry(QtCore.QRect(230, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(element[0])
                for item in element[3]:
                    combo.addItem(item)
                if element[0] == KEY_DP_BOLT_SLIP_FACTOR:
                    combo.setCurrentIndex(4)

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.tab_Bolt)
                q.setGeometry(QtCore.QRect(3, 10 + i, 300, 35))
                font = QtGui.QFont()
                font.setPointSize(9)
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.tab_Bolt)
                r.setGeometry(QtCore.QRect(230, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(element[0])
                if element[3]:
                    r.setText(element[3])
                dbl_validator = QDoubleValidator()
                if element[0] == KEY_DP_BOLT_MATERIAL_G_O:
                    r.setValidator(dbl_validator)
                    r.setMaxLength(7)

            if type == TYPE_ENTER:
                i = i + 100

            i = i + 30

        self.tabWidget.addTab(self.tab_Bolt, "")
        self.tab_Weld = QtWidgets.QWidget()
        self.tab_Weld.setObjectName("tab_Weld")

        label_1 = QtWidgets.QLabel(self.tab_Weld)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        label_1.setFont(font)
        label_1.setObjectName("label_1")
        label_1.setGeometry(QtCore.QRect(10, 10, 130, 22))
        label_1.setText("Inputs")
        label_3 = QtWidgets.QLabel(self.tab_Weld)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setGeometry(QtCore.QRect(400, 10, 130, 22))
        label_3.setText("Description")
        textBrowser = QtWidgets.QTextBrowser(self.tab_Weld)
        textBrowser.setMinimumSize(QtCore.QSize(210, 320))
        textBrowser.setObjectName("textBrowser")
        textBrowser.setGeometry(QtCore.QRect(400, 40, 520, 450))
        textBrowser.setHtml(_translate("DesignPreferences",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                       "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Shop weld takes a material safety factor of 1.25</span></p>\n"
                                       "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Field weld takes a material safety factor of 1.5</span></p>\n"
                                       "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">(IS 800 - cl. 5. 4. 1 or Table 5)</span></p></body></html>"))
        weld_list = ShearConnection.weld_values(self)
        _translate = QtCore.QCoreApplication.translate
        i = 40
        for element in weld_list:
            lable = element[1]
            type = element[2]
            # value = option[4]
            if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                l = QtWidgets.QLabel(self.tab_Weld)
                l.setGeometry(QtCore.QRect(6, 10 + i, 185, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(element[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setAlignment(QtCore.Qt.AlignCenter)

            if type == TYPE_COMBOBOX :
                combo = QtWidgets.QComboBox(self.tab_Weld)
                combo.setGeometry(QtCore.QRect(230, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(element[0])
                for item in element[3]:
                    combo.addItem(item)

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.tab_Weld)
                r.setGeometry(QtCore.QRect(230, 10 + i, 130, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(element[0])
                if element[3]:
                    r.setText(element[3])
                dbl_validator = QDoubleValidator()
                if element[0] == KEY_DP_WELD_MATERIAL_G_O:
                    r.setValidator(dbl_validator)
                    r.setMaxLength(7)

            i = i + 40
        self.tabWidget.addTab(self.tab_Weld, "")
        self.tab_Detailing = QtWidgets.QWidget()
        self.tab_Detailing.setObjectName("tab_Detailing")

        label_1 = QtWidgets.QLabel(self.tab_Detailing)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        label_1.setFont(font)
        label_1.setObjectName("label_1")
        label_1.setGeometry(QtCore.QRect(10, 10, 130, 22))
        label_1.setText("Inputs")
        label_3 = QtWidgets.QLabel(self.tab_Detailing)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setGeometry(QtCore.QRect(470, 10, 130, 22))
        label_3.setText("Description")
        textBrowser = QtWidgets.QTextBrowser(self.tab_Detailing)
        textBrowser.setMinimumSize(QtCore.QSize(210, 320))
        textBrowser.setObjectName("textBrowser")
        textBrowser.setGeometry(QtCore.QRect(470, 40, 450, 450))
        textBrowser.setHtml(_translate("DesignPreferences",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                       "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.7</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[a- sheared or hand flame cut edges] </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">and </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.5 </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[b - Rolled, machine-flame cut, sawn and planed edges]</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> (IS 800 - cl. 10. 2. 4. 2)</span></p>\n"
                                       "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
                                       "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">This gap should include the tolerance value of 5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5 mm{tolerance})</span></p>\n"
                                       "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
                                       "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3</span></p>\n"
                                       "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>"))

        detailing_list = ShearConnection.detailing_values(self)
        _translate = QtCore.QCoreApplication.translate
        i = 40
        for element in detailing_list:
            lable = element[1]
            type = element[2]
            # value = option[4]
            if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                l = QtWidgets.QLabel(self.tab_Detailing)
                l.setGeometry(QtCore.QRect(6, 10 + i, 174, 30))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(element[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setAlignment(QtCore.Qt.AlignCenter)

            if type == TYPE_COMBOBOX:
                combo = QtWidgets.QComboBox(self.tab_Detailing)
                combo.setGeometry(QtCore.QRect(180, 10 + i, 270, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(element[0])
                for item in element[3]:
                    combo.addItem(item)

            if type == TYPE_TITLE:
                q = QtWidgets.QLabel(self.tab_Detailing)
                q.setGeometry(QtCore.QRect(3, 10 + i, 300, 35))
                font = QtGui.QFont()
                font.setPointSize(9)
                q.setFont(font)
                q.setObjectName("_title")
                q.setText(_translate("MainWindow",
                                     "<html><head/><body><p><span style=\" font-weight:600;\">" + lable + "</span></p></body></html>"))

            if type == TYPE_TEXTBOX:
                r = QtWidgets.QLineEdit(self.tab_Detailing)
                r.setGeometry(QtCore.QRect(180, 10 + i, 270, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(element[0])
                if element[3]:
                    r.setText(element[3])

            i = i + 40


        # self.gridLayout_18 = QtWidgets.QGridLayout(self.tab_Detailing)
        # self.gridLayout_18.setObjectName("gridLayout_18")
        # self.gridLayout_17 = QtWidgets.QGridLayout()
        # self.gridLayout_17.setObjectName("gridLayout_17")
        # self.gridLayout_6 = QtWidgets.QGridLayout()
        # self.gridLayout_6.setObjectName("gridLayout_6")
        # self.label_38 = QtWidgets.QLabel(self.tab_Detailing)
        # self.label_38.setObjectName("label_38")
        # self.gridLayout_6.addWidget(self.label_38, 0, 0, 1, 1)
        # self.line_11 = QtWidgets.QFrame(self.tab_Detailing)
        # self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line_11.setObjectName("line_11")
        # self.gridLayout_6.addWidget(self.line_11, 1, 0, 1, 1)
        # self.gridLayout_17.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        # self.gridLayout_4 = QtWidgets.QGridLayout()
        # self.gridLayout_4.setObjectName("gridLayout_4")
        # self.label_39 = QtWidgets.QLabel(self.tab_Detailing)
        # self.label_39.setObjectName("label_39")
        # self.gridLayout_4.addWidget(self.label_39, 0, 0, 1, 1)
        # self.combo_detailingEdgeType = QtWidgets.QComboBox(self.tab_Detailing)
        # self.combo_detailingEdgeType.setObjectName("combo_detailingEdgeType")
        # self.combo_detailingEdgeType.addItem("")
        # self.combo_detailingEdgeType.addItem("")
        # self.gridLayout_4.addWidget(self.combo_detailingEdgeType, 0, 1, 1, 1)
        # self.label_12 = QtWidgets.QLabel(self.tab_Detailing)
        # self.label_12.setObjectName("label_30")
        # self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        # self.txt_detailingGap = QtWidgets.QLineEdit(self.tab_Detailing)
        # self.txt_detailingGap.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # self.txt_detailingGap.setObjectName("txt_detailingGap")
        # self.gridLayout_4.addWidget(self.txt_detailingGap, 1, 1, 1, 1)
        # self.label_40 = QtWidgets.QLabel(self.tab_Detailing)
        # self.label_40.setObjectName("label_40")
        # self.gridLayout_4.addWidget(self.label_40, 2, 0, 1, 1)
        # self.combo_detailing_memebers = QtWidgets.QComboBox(self.tab_Detailing)
        # self.combo_detailing_memebers.setObjectName("combo_detailing_memebers")
        # self.combo_detailing_memebers.addItem("")
        # self.combo_detailing_memebers.addItem("")
        # self.gridLayout_4.addWidget(self.combo_detailing_memebers, 2, 1, 1, 1)
        # self.gridLayout_17.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        # self.gridLayout_18.addLayout(self.gridLayout_17, 0, 0, 1, 1)
        # self.gridLayout_10 = QtWidgets.QGridLayout()
        # self.gridLayout_10.setObjectName("gridLayout_10")
        # self.line_6 = QtWidgets.QFrame(self.tab_Detailing)
        # self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line_6.setObjectName("line_6")
        # self.gridLayout_10.addWidget(self.line_6, 1, 0, 1, 1)
        # self.label_18 = QtWidgets.QLabel(self.tab_Detailing)
        # self.label_18.setObjectName("label_18")
        # self.gridLayout_10.addWidget(self.label_18, 0, 0, 1, 1)
        # self.textBrowser_detailingDescription = QtWidgets.QTextBrowser(self.tab_Detailing)
        # self.textBrowser_detailingDescription.setMinimumSize(QtCore.QSize(210, 0))
        # self.textBrowser_detailingDescription.setObjectName("textBrowser_detailingDescription")
        # self.gridLayout_10.addWidget(self.textBrowser_detailingDescription, 2, 0, 1, 1)
        # self.gridLayout_18.addLayout(self.gridLayout_10, 0, 1, 2, 1)
        # spacerItem7 = QtWidgets.QSpacerItem(20, 255, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridLayout_18.addItem(spacerItem7, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_Detailing, "")
        self.tab_Design = QtWidgets.QWidget()
        self.tab_Design.setObjectName("tab_Design")

        design_list = ShearConnection.design_values(self)
        _translate = QtCore.QCoreApplication.translate
        i = 40
        for element in design_list:
            lable = element[1]
            type = element[2]
            # value = option[4]
            if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                l = QtWidgets.QLabel(self.tab_Design)
                l.setGeometry(QtCore.QRect(6, 10 + i, 174, 30))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setWeight(50)
                l.setFont(font)
                l.setObjectName(element[0] + "_label")
                l.setText(_translate("MainWindow", "<html><head/><body><p>" + lable + "</p></body></html>"))
                l.setAlignment(QtCore.Qt.AlignCenter)

            if type == TYPE_COMBOBOX:
                combo = QtWidgets.QComboBox(self.tab_Design)
                combo.setGeometry(QtCore.QRect(180, 10 + i, 270, 22))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                combo.setFont(font)
                combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                combo.setMaxVisibleItems(5)
                combo.setObjectName(element[0])
                for item in element[3]:
                    combo.addItem(item)
                if element[0] == KEY_DP_DESIGN_METHOD:
                    combo.model().item(1).setEnabled(False)
                    combo.model().item(2).setEnabled(False)

        # self.label_19 = QtWidgets.QLabel(self.tab_Design)
        # self.label_19.setGeometry(QtCore.QRect(21, 31, 101, 16))
        # self.label_19.setObjectName("label_19")
        # self.combo_design_method = QtWidgets.QComboBox(self.tab_Design)
        # self.combo_design_method.setGeometry(QtCore.QRect(160, 31, 227, 22))
        # self.combo_design_method.setObjectName("combo_design_method")
        # self.combo_design_method.addItem("")
        # self.combo_design_method.addItem("")
        # self.combo_design_method.addItem("")
        self.tabWidget.addTab(self.tab_Design, "")
        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(DesignPreferences)
        self.tabWidget.setCurrentIndex(2)
        #self.combo_slipfactor.setCurrentIndex(8)
        QtCore.QMetaObject.connectSlotsByName(DesignPreferences)
        DesignPreferences.setTabOrder(self.btn_close, self.tab_Column)
        # DesignPreferences.setTabOrder(self.tab_Column, self.lineEdit_Designation_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_Designation_Column, self.lineEdit_UltimateStrength_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_UltimateStrength_Column, self.lineEdit_YieldStrength_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_YieldStrength_Column, self.lineEdit_Depth_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_Depth_Column, self.lineEdit_FlangeWidth_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_FlangeWidth_Column, self.lineEdit_FlangeThickness_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_FlangeThickness_Column, self.lineEdit_WeBThickness_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_WeBThickness_Column, self.lineEdit_FlangeSlope_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_FlangeSlope_Column, self.lineEdit_RootRadius_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_RootRadius_Column, self.lineEdit_ToeRadius_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ToeRadius_Column, self.comboBox_Column)
        # DesignPreferences.setTabOrder(self.comboBox_Column, self.lineEdit_ModElasticity_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ModElasticity_Column, self.lineEdit_ModulusOfRigidity_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ModulusOfRigidity_Column, self.lineEdit_Mass_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_Mass_Column, self.lineEdit_SectionalArea_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_SectionalArea_Column, self.lineEdit_MomentOfAreaZ_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_MomentOfAreaZ_Column, self.lineEdit_MomentOfAreaY_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_MomentOfAreaY_Column, self.lineEdit_RogZ_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_RogZ_Column, self.lineEdit_RogY_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_RogY_Column, self.lineEdit_ElasticModZ_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModZ_Column, self.lineEdit_ElasticModY_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModY_Column, self.lineEdit_ElasticModPZ_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModPZ_Column, self.lineEdit_ElasticModPY_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModPY_Column, self.lineEdit_Source_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_Source_Column, self.lineEdit_PoissionsRatio_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_PoissionsRatio_Column, self.lineEdit_ThermalExpansion_Column)
        # DesignPreferences.setTabOrder(self.lineEdit_ThermalExpansion_Column, self.pushButton_Clear_Column)
        # DesignPreferences.setTabOrder(self.pushButton_Clear_Column, self.pushButton_Add_Column)
        # DesignPreferences.setTabOrder(self.pushButton_Add_Column, self.pushButton_Download_Column)
        # DesignPreferences.setTabOrder(self.pushButton_Download_Column, self.btn_save)
        # DesignPreferences.setTabOrder(self.btn_save, self.btn_defaults)
        # DesignPreferences.setTabOrder(self.btn_defaults, self.btn_close)
        DesignPreferences.setTabOrder(self.btn_close, self.tab_Column)

        DesignPreferences.setTabOrder(self.btn_close, self.tab_Beam)
        # DesignPreferences.setTabOrder(self.tab_Beam, self.lineEdit_Designation_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_Designation_Beam, self.lineEdit_UltimateStrength_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_UltimateStrength_Beam, self.lineEdit_YieldStrength_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_YieldStrength_Beam, self.lineEdit_Depth_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_Depth_Beam, self.lineEdit_FlangeWidth_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_FlangeWidth_Beam, self.lineEdit_FlangeThickness_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_FlangeThickness_Beam, self.lineEdit_WeBThickness_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_WeBThickness_Beam, self.lineEdit_FlangeSlope_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_FlangeSlope_Beam, self.lineEdit_RootRadius_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_RootRadius_Beam, self.lineEdit_ToeRadius_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ToeRadius_Beam, self.comboBox_Beam)
        # DesignPreferences.setTabOrder(self.comboBox_Beam, self.lineEdit_ModElasticity_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ModElasticity_Beam, self.lineEdit_ModulusOfRigidity_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ModulusOfRigidity_Beam, self.lineEdit_Mass_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_Mass_Beam, self.lineEdit_SectionalArea_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_SectionalArea_Beam, self.lineEdit_MomentOfAreaZ_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_MomentOfAreaZ_Beam, self.lineEdit_MomentOfAreaY_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_MomentOfAreaY_Beam, self.lineEdit_RogZ_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_RogZ_Beam, self.lineEdit_RogY_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_RogY_Beam, self.lineEdit_ElasticModZ_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModZ_Beam, self.lineEdit_ElasticModY_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModY_Beam, self.lineEdit_ElasticModPZ_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModPZ_Beam, self.lineEdit_ElasticModPY_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ElasticModPY_Beam, self.lineEdit_Source_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_Source_Beam, self.lineEdit_PoissonsRatio_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_PoissonsRatio_Beam, self.lineEdit_ThermalExpansion_Beam)
        # DesignPreferences.setTabOrder(self.lineEdit_ThermalExpansion_Beam, self.pushButton_Clear_Beam)
        # DesignPreferences.setTabOrder(self.pushButton_Clear_Beam, self.pushButton_Add_Beam)
        # DesignPreferences.setTabOrder(self.pushButton_Add_Beam, self.pushButton_Download_Beam)
        # DesignPreferences.setTabOrder(self.pushButton_Download_Beam, self.btn_save)
        DesignPreferences.setTabOrder(self.btn_save, self.btn_defaults)
        DesignPreferences.setTabOrder(self.btn_defaults, self.btn_close)
        DesignPreferences.setTabOrder(self.btn_close, self.tab_Beam)

        pushButton_Clear_Column.clicked.connect(lambda: self.clear_tab("Column"))
        pushButton_Clear_Beam.clicked.connect(lambda: self.clear_tab("Beam"))

        pushButton_Add_Column.clicked.connect(self.add_tab_column)
        pushButton_Add_Beam.clicked.connect(self.add_tab_beam)

    def clear_tab(self, tab_name):
        if tab_name == "Column":
            tab = self.tab_Column
        elif tab_name == "Beam":
            tab = self.tab_Beam
        for c in tab.children():
            if isinstance(c, QtWidgets.QComboBox):
                c.setCurrentIndex(0)
            elif isinstance(c, QtWidgets.QLineEdit):
                c.clear()

    def add_tab_column(self):

        name = self.tabWidget.tabText(self.tabWidget.indexOf(self.tab_Column))
        if name == KEY_DISP_COLSEC:
            table = "Columns"
        elif name == KEY_DISP_PRIBM:
            table = "Beams"
        else:
            pass

        for ch in self.tab_Column.children():
            if isinstance(ch, QtWidgets.QLineEdit) and ch.text() == "":
                QMessageBox.information(QMessageBox(), 'Warning', 'Please Fill all missing parameters!')
                add_col = self.tab_Column.findChild(QtWidgets.QWidget, 'pushButton_Add_Column')
                add_col.setDisabled(True)
                break
            elif isinstance(ch, QtWidgets.QLineEdit) and ch.text() != "":
                if ch.objectName() == KEY_SUPTNGSEC_DESIGNATION:
                    Designation_c = ch.text()
                elif ch.objectName() == KEY_SUPTNGSEC_SOURCE:
                    Source_c = ch.text()
                elif ch.objectName() == KEY_SUPTNGSEC_DEPTH:
                    D_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_FLANGE_W:
                    B_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_FLANGE_T:
                    T_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_WEB_T:
                    tw_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_FLANGE_S:
                    FlangeSlope_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_ROOT_R:
                    R1_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_TOE_R:
                    R2_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_MASS:
                    Mass_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_SEC_AREA:
                    Area_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_MOA_LZ:
                    Iz_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_MOA_LY:
                    Iy_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_ROG_RZ:
                    rz_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_ROG_RY:
                    ry_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_EM_ZZ:
                    Zz_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_EM_ZY:
                    Zy_c = float(ch.text())
                elif ch.objectName() == KEY_SUPTNGSEC_PM_ZPZ:
                    if ch.text() == "":
                        ch.setText("0")
                    Zpz_c = ch.text()
                elif ch.objectName() == KEY_SUPTNGSEC_PM_ZPY:
                    if ch.text() == "":
                        ch.setText("0")
                    Zpy_c = ch.text()
                else:
                    pass

        if ch == self.tab_Column.children()[len(self.tab_Column.children())-1]:
            conn = sqlite3.connect(PATH_TO_DATABASE)
            c = conn.cursor()
            if table == "Beams":
                c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_c,))
                data = c.fetchone()[0]
            else:
                c.execute("SELECT count(*) FROM Columns WHERE Designation = ?", (Designation_c,))
                data = c.fetchone()[0]
            if data == 0:
                if table == "Beams":
                    c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,R1,R2,Iz,Iy,rz,ry,
                        Zz,zy,Zpz,Zpy,FlangeSlope,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (Designation_c, Mass_c, Area_c,
                               D_c, B_c, tw_c, T_c,
                               R1_c, R2_c, Iz_c, Iy_c, rz_c,
                               ry_c, Zz_c, Zy_c,
                               Zpz_c, Zpy_c, FlangeSlope_c, Source_c))
                    conn.commit()
                else:
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
                self.clear_tab("Column")

    def add_tab_beam(self):

        for ch in self.tab_Beam.children():

            if isinstance(ch, QtWidgets.QLineEdit) and ch.text() == "":
                QMessageBox.information(QMessageBox(), 'Warning', 'Please Fill all missing parameters!')
                add_bm = self.tab_Beam.findChild(QtWidgets.QWidget, 'pushButton_Add_Beam')
                add_bm.setDisabled(True)
                break

            elif isinstance(ch, QtWidgets.QLineEdit) and ch.text() != "":

                if ch.objectName() == KEY_SUPTDSEC_DESIGNATION:
                    Designation_b = ch.text()
                elif ch.objectName() == KEY_SUPTDSEC_SOURCE:
                    Source_b = ch.text()
                elif ch.objectName() == KEY_SUPTDSEC_DEPTH:
                    D_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_FLANGE_W:
                    B_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_FLANGE_T:
                    T_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_WEB_T:
                    tw_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_FLANGE_S:
                    FlangeSlope_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_ROOT_R:
                    R1_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_TOE_R:
                    R2_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_MASS:
                    Mass_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_SEC_AREA:
                    Area_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_MOA_LZ:
                    Iz_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_MOA_LY:
                    Iy_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_ROG_RZ:
                    rz_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_ROG_RY:
                    ry_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_EM_ZZ:
                    Zz_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_EM_ZY:
                    Zy_b = float(ch.text())
                elif ch.objectName() == KEY_SUPTDSEC_PM_ZPZ:
                    if ch.text() == "":
                        ch.setText("0")
                    Zpz_b = ch.text()
                elif ch.objectName() == KEY_SUPTDSEC_PM_ZPY:
                    if ch.text() == "":
                        ch.setText("0")
                    Zpy_b = ch.text()
                else:
                    pass

        if ch == self.tab_Beam.children()[len(self.tab_Beam.children())-1]:

            conn = sqlite3.connect(PATH_TO_DATABASE)

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_b,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,R1,R2,Iz,Iy,rz,ry,Zz,zy,Zpz,Zpy,
                    FlangeSlope,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
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
                self.clear_tab("Beam")

    def retranslateUi(self, DesignPreferences):
        _translate = QtCore.QCoreApplication.translate
        DesignPreferences.setWindowTitle(_translate("DesignPreferences", "Design preferences"))
        self.btn_defaults.setText(_translate("DesignPreferences", "Defaults"))
        self.btn_save.setText(_translate("DesignPreferences", "Save"))
        self.btn_close.setText(_translate("DesignPreferences", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Column), _translate("DesignPreferences", "Column"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Beam), _translate("DesignPreferences", "Beam"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Bolt), _translate("DesignPreferences", "Bolt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Weld), _translate("DesignPreferences", "Weld"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Detailing), _translate("DesignPreferences", "Detailing"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Design), _translate("DesignPreferences", "Design"))


class DesignPreferences(QDialog):

    def __init__(self, main, parent=None):

        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.main_controller = parent
        #self.uiobj = self.main_controller.uiObj
        self.saved = None
        self.sectionalprop = I_sectional_Properties()
        # self.ui.combo_design_method.model().item(1).setEnabled(False)
        # self.ui.combo_design_method.model().item(2).setEnabled(False)
        # self.save_default_para()
        # self.ui.txt_boltFu.setValidator(dbl_validator)
        # self.ui.txt_boltFu.setMaxLength(7)
        # self.ui.txt_weldFu.setValidator(dbl_validator)
        # self.ui.txt_weldFu.setMaxLength(7)
        # self.ui.btn_defaults.clicked.connect(self.save_default_para)
        # self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_save.hide()
        self.ui.btn_close.clicked.connect(self.close_designPref)
        # self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)
        # self.ui.pushButton_Import_Column.setDisabled(True)
        #self.ui.pushButton_Import_Beam.setDisabled(True)
        # self.ui.pushButton_Add_Column.clicked.connect(self.add_ColumnPref)
        # self.ui.pushButton_Add_Beam.clicked.connect(self.add_BeamPref)
        # self.ui.pushButton_Clear_Column.clicked.connect(self.clear_ColumnPref)
        #self.ui.pushButton_Clear_Beam.clicked.connect(self.clear_BeamPref)
        # pushButton_Download_Column = self.ui.tab_Column.findChild(QtWidgets.QWidget, 'pushButton_Download_Column')
        # pushButton_Download_Column.clicked.connect(self.download_Database_Column)
        # pushButton_Download_Beam = self.ui.tab_Beam.findChild(QtWidgets.QWidget, 'pushButton_Download_Beam')
        # pushButton_Download_Beam.clicked.connect(self.download_Database_Beam)
        #
        # pushButton_Import_Column = self.ui.tab_Column.findChild(QtWidgets.QWidget, 'pushButton_Import_Column')
        # pushButton_Import_Column.clicked.connect(self.import_ColumnPref)
        # pushButton_Import_Beam = self.ui.tab_Beam.findChild(QtWidgets.QWidget, 'pushButton_Import_Beam')
        # pushButton_Import_Beam.clicked.connect(self.import_BeamPref)
        #self.ui.btn_save.clicked.connect(Ui_ModuleWindow.design_preferences(Ui_ModuleWindow()))
        #self.ui.combo_boltHoleType.currentIndexChanged.connect(my_fn)
        #self.ui.btn_save.clicked.connect(self.save_fn)
        self.ui.btn_defaults.clicked.connect(self.default_fn)

    def default_fn(self):
        for children in self.ui.tab_Bolt.children():
            if children.objectName() == KEY_DP_BOLT_TYPE:
                children.setCurrentIndex(0)
            elif children.objectName() == KEY_DP_BOLT_HOLE_TYPE:
                children.setCurrentIndex(0)
            elif children.objectName() == KEY_DP_BOLT_MATERIAL_G_O:
                children.setText('410')
            elif children.objectName() == KEY_DP_BOLT_SLIP_FACTOR:
                children.setCurrentIndex(4)
            else:
                pass
        for children in self.ui.tab_Weld.children():
            if children.objectName() == KEY_DP_WELD_TYPE:
                children.setCurrentIndex(0)
            elif children.objectName() == KEY_DP_WELD_MATERIAL_G_O:
                children.setText('410')
            else:
                pass
        for children in self.ui.tab_Detailing.children():
            if children.objectName() == KEY_DP_DETAILING_EDGE_TYPE:
                children.setCurrentIndex(0)
            elif children.objectName() == KEY_DP_DETAILING_GAP:
                children.setText('10')
            elif children.objectName() == KEY_DP_DETAILING_CORROSIVE_INFLUENCES:
                children.setCurrentIndex(0)
            else:
                pass
        for children in self.ui.tab_Design.children():
            if children.objectName() == KEY_DP_DESIGN_METHOD:
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
        key_boltHoleType = self.ui.tab_Bolt.findChild(QtWidgets.QWidget, KEY_DP_BOLT_HOLE_TYPE)
        combo_boltHoleType = key_boltHoleType.currentText()
        key_boltFu = self.ui.tab_Bolt.findChild(QtWidgets.QWidget, KEY_DP_BOLT_MATERIAL_G_O)
        line_boltFu = key_boltFu.text()
        key_slipfactor = self.ui.tab_Bolt.findChild(QtWidgets.QWidget, KEY_DP_BOLT_SLIP_FACTOR)
        combo_slipfactor = key_slipfactor.currentText()
        key_weldType = self.ui.tab_Weld.findChild(QtWidgets.QWidget, KEY_DP_WELD_TYPE)
        combo_weldType = key_weldType.currentText()
        key_weldFu = self.ui.tab_Weld.findChild(QtWidgets.QWidget, KEY_DP_WELD_MATERIAL_G_O)
        line_weldFu = key_weldFu.text()
        key_detailingEdgeType = self.ui.tab_Detailing.findChild(QtWidgets.QWidget, KEY_DP_DETAILING_EDGE_TYPE)
        combo_detailingEdgeType = key_detailingEdgeType.currentText()
        key_detailingGap = self.ui.tab_Detailing.findChild(QtWidgets.QWidget, KEY_DP_DETAILING_GAP)
        line_detailingGap = key_detailingGap.text()
        key_detailing_memebers = self.ui.tab_Detailing.findChild(QtWidgets.QWidget, KEY_DP_DETAILING_CORROSIVE_INFLUENCES)
        combo_detailing_memebers = key_detailing_memebers.currentText()
        key_design_method = self.ui.tab_Design.findChild(QtWidgets.QWidget, KEY_DP_DESIGN_METHOD)
        combo_design_method = key_design_method.currentText()
        d1 = {KEY_DP_BOLT_HOLE_TYPE: combo_boltHoleType,
              KEY_DP_BOLT_MATERIAL_G_O: line_boltFu,
              KEY_DP_BOLT_SLIP_FACTOR: combo_slipfactor,
              KEY_DP_WELD_TYPE: combo_weldType,
              KEY_DP_WELD_MATERIAL_G_O: line_weldFu,
              KEY_DP_DETAILING_EDGE_TYPE: combo_detailingEdgeType,
              KEY_DP_DETAILING_GAP: line_detailingGap,
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
    def column_preferences(self, designation, table, material_grade):
        col_list = []
        col_attributes = Section(designation, material_grade)
        Section.connect_to_database_update_other_attributes(col_attributes, table, designation)
        if table == "Beams":
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_Column), KEY_DISP_PRIBM)
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_Beam), KEY_DISP_SECBM)
        else:
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_Column), KEY_DISP_COLSEC)
            self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_Beam), KEY_DISP_BEAMSEC)
        for ch in self.ui.tab_Column.children():
            if ch.objectName() == KEY_SUPTNGSEC_DESIGNATION:
                ch.setText(designation)
            elif ch.objectName() == KEY_SUPTNGSEC_SOURCE:
                ch.setText(col_attributes.source)
            elif ch.objectName() == KEY_SUPTNGSEC_FU:
                ch.setText(str(col_attributes.fu))
            elif ch.objectName() == KEY_SUPTNGSEC_FY:
                ch.setText(str(col_attributes.fy))
            elif ch.objectName() == KEY_SUPTNGSEC_DEPTH:
                ch.setText(str(col_attributes.depth))
                col_list.append(ch)
            elif ch.objectName() == KEY_SUPTNGSEC_FLANGE_W:
                ch.setText(str(col_attributes.flange_width))
                col_list.append(ch)
            elif ch.objectName() == KEY_SUPTNGSEC_FLANGE_T:
                ch.setText(str(col_attributes.flange_thickness))
                col_list.append(ch)
            elif ch.objectName() == KEY_SUPTNGSEC_WEB_T:
                ch.setText(str(col_attributes.web_thickness))
                col_list.append(ch)
            elif ch.objectName() == KEY_SUPTNGSEC_FLANGE_S:
                ch.setText(str(col_attributes.flange_slope))
            elif ch.objectName() == KEY_SUPTNGSEC_ROOT_R:
                ch.setText(str(col_attributes.root_radius))
            elif ch.objectName() == KEY_SUPTNGSEC_TOE_R:
                ch.setText(str(col_attributes.toe_radius))
            elif ch.objectName() == KEY_SUPTNGSEC_MOD_OF_ELAST:
                ch.setText("200")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTNGSEC_MOD_OF_RIGID:
                ch.setText("76.9")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTNGSEC_POISSON_RATIO:
                ch.setText("0.3")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTNGSEC_THERMAL_EXP:
                ch.setText("12")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTNGSEC_MASS:
                ch.setText(str(col_attributes.mass))
            elif ch.objectName() == KEY_SUPTNGSEC_SEC_AREA:
                ch.setText(str(col_attributes.area))
            elif ch.objectName() == KEY_SUPTNGSEC_MOA_LZ:
                ch.setText(str(col_attributes.mom_inertia_z))
            elif ch.objectName() == KEY_SUPTNGSEC_MOA_LY:
                ch.setText(str(col_attributes.mom_inertia_y))
            elif ch.objectName() == KEY_SUPTNGSEC_ROG_RZ:
                ch.setText(str(col_attributes.rad_of_gy_z))
            elif ch.objectName() == KEY_SUPTNGSEC_ROG_RY:
                ch.setText(str(col_attributes.rad_of_gy_y))
            elif ch.objectName() == KEY_SUPTNGSEC_EM_ZZ:
                ch.setText(str(col_attributes.elast_sec_mod_z))
            elif ch.objectName() == KEY_SUPTNGSEC_EM_ZY:
                ch.setText(str(col_attributes.elast_sec_mod_y))
            elif ch.objectName() == KEY_SUPTNGSEC_PM_ZPZ:
                ch.setText(str(col_attributes.plast_sec_mod_z))
            elif ch.objectName() == KEY_SUPTNGSEC_PM_ZPY:
                ch.setText(str(col_attributes.plast_sec_mod_y))
            elif ch.objectName() == 'pushButton_Add_Column':
                ch.setEnabled(True)
            else:
                pass

        for e in col_list:
            if e.text() != "":
                e.textChanged.connect(lambda: self.new_sectionalprop_Column(col_list))

        # self.ui.lineEdit_Designation_Column.setText(designation)
        # self.ui.lineEdit_Source_Column.setText(col_attributes.source)
        # self.ui.lineEdit_UltimateStrength_Column.setText(str(col_attributes.fu))
        # self.ui.lineEdit_YieldStrength_Column.setText(str(col_attributes.fy))
        # self.ui.lineEdit_Depth_Column.setText(str(col_attributes.depth))
        # self.ui.lineEdit_FlangeWidth_Column.setText(str(col_attributes.flange_width))
        # self.ui.lineEdit_FlangeThickness_Column.setText(str(col_attributes.flange_thickness))
        # self.ui.lineEdit_WeBThickness_Column.setText(str(col_attributes.web_thickness))
        # self.ui.lineEdit_FlangeSlope_Column.setText(str(col_attributes.flange_slope))
        # self.ui.lineEdit_RootRadius_Column.setText(str(col_attributes.root_radius))
        # self.ui.lineEdit_ToeRadius_Column.setText(str(col_attributes.toe_radius))
        # self.ui.lineEdit_ModElasticity_Column.setText("200")
        # self.ui.lineEdit_ModElasticity_Column.setDisabled(True)
        # self.ui.lineEdit_ModulusOfRigidity_Column.setText("76.9")
        # self.ui.lineEdit_ModulusOfRigidity_Column.setDisabled(True)
        # self.ui.lineEdit_PoissionsRatio_Column.setText("0.3")
        # self.ui.lineEdit_PoissionsRatio_Column.setDisabled(True)
        # self.ui.lineEdit_ThermalExpansion_Column.setText("12")
        # self.ui.lineEdit_ThermalExpansion_Column.setDisabled(True)
        # self.ui.lineEdit_Mass_Column.setText(str(col_attributes.mass))
        # self.ui.lineEdit_SectionalArea_Column.setText(str(col_attributes.area))
        # self.ui.lineEdit_MomentOfAreaZ_Column.setText(str(col_attributes.mom_inertia_z))
        # self.ui.lineEdit_MomentOfAreaY_Column.setText(str(col_attributes.mom_inertia_y))
        # self.ui.lineEdit_RogZ_Column.setText(str(col_attributes.rad_of_gy_z))
        # self.ui.lineEdit_RogY_Column.setText(str(col_attributes.rad_of_gy_y))
        # self.ui.lineEdit_ElasticModZ_Column.setText(str(col_attributes.elast_sec_mod_z))
        # self.ui.lineEdit_ElasticModY_Column.setText(str(col_attributes.elast_sec_mod_y))
        # self.ui.lineEdit_ElasticModPZ_Column.setText(str(col_attributes.plast_sec_mod_z))
        # self.ui.lineEdit_ElasticModPY_Column.setText(str(col_attributes.plast_sec_mod_y))
        # self.ui.pushButton_Add_Column.setEnabled(True)
        # self.ui.pushButton_Add_Column.clicked.connect(lambda: self.add_ColumnPref(table))
        #
        # if (
        #         self.ui.lineEdit_Depth_Column.text() != "" and self.ui.lineEdit_FlangeWidth_Column.text() != "" and self.ui.lineEdit_FlangeThickness_Column.text() != ""
        #         and self.ui.lineEdit_WeBThickness_Column.text() != ""):
        #     self.ui.lineEdit_Depth_Column.textChanged.connect(self.new_sectionalprop_Column)
        #     self.ui.lineEdit_FlangeWidth_Column.textChanged.connect(self.new_sectionalprop_Column)
        #     self.ui.lineEdit_FlangeThickness_Column.textChanged.connect(self.new_sectionalprop_Column)
        #     self.ui.lineEdit_WeBThickness_Column.textChanged.connect(self.new_sectionalprop_Column)

    def beam_preferences(self, designation, material_grade):
        beam_attributes = Section(designation, material_grade)
        Section.connect_to_database_update_other_attributes(beam_attributes, "Beams", designation)
        beam_list = []
        for ch in self.ui.tab_Beam.children():
            if ch.objectName() == KEY_SUPTDSEC_DESIGNATION:
                ch.setText(designation)
            elif ch.objectName() == KEY_SUPTDSEC_SOURCE:
                ch.setText(beam_attributes.source)
            elif ch.objectName() == KEY_SUPTDSEC_FU:
                ch.setText(str(beam_attributes.fu))
            elif ch.objectName() == KEY_SUPTDSEC_FY:
                ch.setText(str(beam_attributes.fy))
            elif ch.objectName() == KEY_SUPTDSEC_DEPTH:
                ch.setText(str(beam_attributes.depth))
                beam_list.append(ch)
            elif ch.objectName() == KEY_SUPTDSEC_FLANGE_W:
                ch.setText(str(beam_attributes.flange_width))
                beam_list.append(ch)
            elif ch.objectName() == KEY_SUPTDSEC_FLANGE_T:
                ch.setText(str(beam_attributes.flange_thickness))
                beam_list.append(ch)
            elif ch.objectName() == KEY_SUPTDSEC_WEB_T:
                ch.setText(str(beam_attributes.web_thickness))
                beam_list.append(ch)
            elif ch.objectName() == KEY_SUPTDSEC_FLANGE_S:
                ch.setText(str(beam_attributes.flange_slope))
            elif ch.objectName() == KEY_SUPTDSEC_ROOT_R:
                ch.setText(str(beam_attributes.root_radius))
            elif ch.objectName() == KEY_SUPTDSEC_TOE_R:
                ch.setText(str(beam_attributes.toe_radius))
            elif ch.objectName() == KEY_SUPTDSEC_MOD_OF_ELAST:
                ch.setText("200")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTDSEC_MOD_OF_RIGID:
                ch.setText("76.9")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTDSEC_POISSON_RATIO:
                ch.setText("0.3")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTDSEC_THERMAL_EXP:
                ch.setText("12")
                ch.setDisabled(True)
            elif ch.objectName() == KEY_SUPTDSEC_MASS:
                ch.setText(str(beam_attributes.mass))
            elif ch.objectName() == KEY_SUPTDSEC_SEC_AREA:
                ch.setText(str(beam_attributes.area))
            elif ch.objectName() == KEY_SUPTDSEC_MOA_LZ:
                ch.setText(str(beam_attributes.mom_inertia_z))
            elif ch.objectName() == KEY_SUPTDSEC_MOA_LY:
                ch.setText(str(beam_attributes.mom_inertia_y))
            elif ch.objectName() == KEY_SUPTDSEC_ROG_RZ:
                ch.setText(str(beam_attributes.rad_of_gy_z))
            elif ch.objectName() == KEY_SUPTDSEC_ROG_RY:
                ch.setText(str(beam_attributes.rad_of_gy_y))
            elif ch.objectName() == KEY_SUPTDSEC_EM_ZZ:
                ch.setText(str(beam_attributes.elast_sec_mod_z))
            elif ch.objectName() == KEY_SUPTDSEC_EM_ZY:
                ch.setText(str(beam_attributes.elast_sec_mod_y))
            elif ch.objectName() == KEY_SUPTDSEC_PM_ZPZ:
                ch.setText(str(beam_attributes.plast_sec_mod_z))
            elif ch.objectName() == KEY_SUPTDSEC_PM_ZPY:
                ch.setText(str(beam_attributes.plast_sec_mod_y))
            elif ch.objectName() == 'pushButton_Add_Beam':
                ch.setEnabled(True)
            else:
                pass

        for e in beam_list:
            if e.text() != "":
                e.textChanged.connect(lambda: self.new_sectionalprop_Beam(beam_list))
        # self.ui.lineEdit_Designation_Beam.setText(designation)
        # self.ui.lineEdit_Source_Beam.setText(str(beam_attributes.source))
        # self.ui.lineEdit_UltimateStrength_Beam.setText(str(beam_attributes.fu))
        # self.ui.lineEdit_YieldStrength_Beam.setText(str(beam_attributes.fy))
        # self.ui.lineEdit_Depth_Beam.setText(str(beam_attributes.depth))
        # self.ui.lineEdit_FlangeWidth_Beam.setText(str(beam_attributes.flange_width))
        # self.ui.lineEdit_FlangeThickness_Beam.setText(str(beam_attributes.flange_thickness))
        # self.ui.lineEdit_WeBThickness_Beam.setText(str(beam_attributes.web_thickness))
        # self.ui.lineEdit_FlangeSlope_Beam.setText(str(beam_attributes.flange_slope))
        # self.ui.lineEdit_RootRadius_Beam.setText(str(beam_attributes.root_radius))
        # self.ui.lineEdit_ToeRadius_Beam.setText(str(beam_attributes.toe_radius))
        # self.ui.lineEdit_ModElasticity_Beam.setText("200")
        # self.ui.lineEdit_ModElasticity_Beam.setDisabled(True)
        # self.ui.lineEdit_ModulusOfRigidity_Beam.setText("76.9")
        # self.ui.lineEdit_ModulusOfRigidity_Beam.setDisabled(True)
        # self.ui.lineEdit_PoissonsRatio_Beam.setText("0.3")
        # self.ui.lineEdit_PoissonsRatio_Beam.setDisabled(True)
        # self.ui.lineEdit_ThermalExpansion_Beam.setText("12")
        # self.ui.lineEdit_ThermalExpansion_Beam.setDisabled(True)
        # self.ui.lineEdit_Mass_Beam.setText(str(beam_attributes.mass))
        # self.ui.lineEdit_SectionalArea_Beam.setText(str(beam_attributes.area))
        # self.ui.lineEdit_MomentOfAreaZ_Beam.setText(str(beam_attributes.mom_inertia_z))
        # self.ui.lineEdit_MomentOfAreaY_Beam.setText(str(beam_attributes.mom_inertia_y))
        # self.ui.lineEdit_RogZ_Beam.setText(str(beam_attributes.rad_of_gy_z))
        # self.ui.lineEdit_RogY_Beam.setText(str(beam_attributes.rad_of_gy_y))
        # self.ui.lineEdit_ElasticModZ_Beam.setText(str(beam_attributes.elast_sec_mod_z))
        # self.ui.lineEdit_ElasticModY_Beam.setText(str(beam_attributes.elast_sec_mod_y))
        # self.ui.lineEdit_ElasticModPZ_Beam.setText(str(beam_attributes.plast_sec_mod_z))
        # self.ui.lineEdit_ElasticModPY_Beam.setText(str(beam_attributes.plast_sec_mod_y))
        # self.ui.pushButton_Add_Beam.setEnabled(True)
        # self.ui.pushButton_Add_Beam.clicked.connect(self.add_BeamPref)
        #
        #
        # if (
        #         self.ui.lineEdit_Depth_Beam.text() != "" and self.ui.lineEdit_FlangeWidth_Beam.text() != "" and self.ui.lineEdit_FlangeThickness_Beam.text() != ""
        #         and self.ui.lineEdit_WeBThickness_Beam.text() != ""):
        #     self.ui.lineEdit_Depth_Beam.textChanged.connect(self.new_sectionalprop_Beam)
        #     self.ui.lineEdit_FlangeWidth_Beam.textChanged.connect(self.new_sectionalprop_Beam)
        #     self.ui.lineEdit_FlangeThickness_Beam.textChanged.connect(self.new_sectionalprop_Beam)
        #     self.ui.lineEdit_WeBThickness_Beam.textChanged.connect(self.new_sectionalprop_Beam)

    def new_sectionalprop_Column(self, col_list):

        for e in col_list:
            if e.text() != "":
                if e.objectName() == KEY_SUPTNGSEC_DEPTH:
                    D = float(e.text())
                elif e.objectName() == KEY_SUPTNGSEC_FLANGE_W:
                    B = float(e.text())
                elif e.objectName() == KEY_SUPTNGSEC_FLANGE_T:
                    t_w = float(e.text())
                elif e.objectName() == KEY_SUPTNGSEC_WEB_T:
                    t_f = float(e.text())
                else:
                    pass
            else:
                return
        if col_list:
            for c in self.ui.tab_Column.children():
                if c.objectName() == KEY_SUPTNGSEC_MASS:
                    c.setText(str(self.sectionalprop.calc_Mass(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_SEC_AREA:
                    c.setText(str(self.sectionalprop.calc_Area(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_MOA_LZ:
                    c.setText(str(self.sectionalprop.calc_MomentOfAreaZ(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_MOA_LY:
                    c.setText(str(self.sectionalprop.calc_MomentOfAreaY(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_ROG_RZ:
                    c.setText(str(self.sectionalprop.calc_RogZ(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_ROG_RY:
                    c.setText(str(self.sectionalprop.calc_RogY(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_EM_ZZ:
                    c.setText(str(self.sectionalprop.calc_ElasticModulusZz(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_EM_ZY:
                    c.setText(str(self.sectionalprop.calc_ElasticModulusZy(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_PM_ZPZ:
                    c.setText(str(self.sectionalprop.calc_PlasticModulusZpz(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTNGSEC_PM_ZPY:
                    c.setText(str(self.sectionalprop.calc_PlasticModulusZpy(D, B, t_w, t_f)))
                elif c.objectName() == 'pushButton_Add_Column':
                    c.setEnabled(True)
                else:
                    pass



        # if self.ui.lineEdit_Depth_Column.text() == "":
        #     return
        # else:
        #     D = float(self.ui.lineEdit_Depth_Column.text())
        #
        # if self.ui.lineEdit_FlangeWidth_Column.text() == "":
        #     return
        # else:
        #     B = float(self.ui.lineEdit_FlangeWidth_Column.text())
        #
        # if self.ui.lineEdit_FlangeThickness_Column.text() == "":
        #     return
        # else:
        #     t_w = float(self.ui.lineEdit_FlangeThickness_Column.text())
        #
        # if self.ui.lineEdit_WeBThickness_Column.text() == "":
        #     return
        # else:
        #     t_f = float(self.ui.lineEdit_WeBThickness_Column.text())
        #
        # self.sectionalprop = I_sectional_Properties()
        # self.ui.lineEdit_Mass_Column.setText(str(self.sectionalprop.calc_Mass(D, B, t_w, t_f)))
        # self.ui.lineEdit_SectionalArea_Column.setText(str(self.sectionalprop.calc_Area(D, B, t_w, t_f)))
        # self.ui.lineEdit_MomentOfAreaZ_Column.setText(str(self.sectionalprop.calc_MomentOfAreaZ(D, B, t_w, t_f)))
        # self.ui.lineEdit_MomentOfAreaY_Column.setText(str(self.sectionalprop.calc_MomentOfAreaY(D, B, t_w, t_f)))
        # self.ui.lineEdit_RogZ_Column.setText(str(self.sectionalprop.calc_RogZ(D, B, t_w, t_f)))
        # self.ui.lineEdit_RogY_Column.setText(str(self.sectionalprop.calc_RogY(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModZ_Column.setText(str(self.sectionalprop.calc_ElasticModulusZz(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModY_Column.setText(str(self.sectionalprop.calc_ElasticModulusZy(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModPZ_Column.setText(str(self.sectionalprop.calc_PlasticModulusZpz(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModPY_Column.setText(str(self.sectionalprop.calc_PlasticModulusZpy(D, B, t_w, t_f)))
        #
        # self.ui.pushButton_Add_Column.setEnabled(True)

    def new_sectionalprop_Beam(self, beam_list):

        for e in beam_list:
            if e.text() != "":
                if e.objectName() == KEY_SUPTDSEC_DEPTH:
                    D = float(e.text())
                elif e.objectName() == KEY_SUPTDSEC_FLANGE_W:
                    B = float(e.text())
                elif e.objectName() == KEY_SUPTDSEC_FLANGE_T:
                    t_w = float(e.text())
                elif e.objectName() == KEY_SUPTDSEC_WEB_T:
                    t_f = float(e.text())
                else:
                    pass
            else:
                return
        if beam_list:
            for c in self.ui.tab_Beam.children():
                if c.objectName() == KEY_SUPTDSEC_MASS:
                    c.setText(str(self.sectionalprop.calc_Mass(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_SEC_AREA:
                    c.setText(str(self.sectionalprop.calc_Area(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_MOA_LZ:
                    c.setText(str(self.sectionalprop.calc_MomentOfAreaZ(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_MOA_LY:
                    c.setText(str(self.sectionalprop.calc_MomentOfAreaY(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_ROG_RZ:
                    c.setText(str(self.sectionalprop.calc_RogZ(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_ROG_RY:
                    c.setText(str(self.sectionalprop.calc_RogY(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_EM_ZZ:
                    c.setText(str(self.sectionalprop.calc_ElasticModulusZz(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_EM_ZY:
                    c.setText(str(self.sectionalprop.calc_ElasticModulusZy(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_PM_ZPZ:
                    c.setText(str(self.sectionalprop.calc_PlasticModulusZpz(D, B, t_w, t_f)))
                elif c.objectName() == KEY_SUPTDSEC_PM_ZPY:
                    c.setText(str(self.sectionalprop.calc_PlasticModulusZpy(D, B, t_w, t_f)))
                elif c.objectName() == 'pushButton_Add_Beam':
                    c.setEnabled(True)
                else:
                    pass
        # if self.ui.lineEdit_Depth_Beam.text() == "":
        #     return
        # else:
        #     D = float(self.ui.lineEdit_Depth_Beam.text())
        #
        # if self.ui.lineEdit_FlangeWidth_Beam.text() == "":
        #     return
        # else:
        #     B = float(self.ui.lineEdit_FlangeWidth_Beam.text())
        #
        # if self.ui.lineEdit_FlangeThickness_Beam.text() == "":
        #     return
        # else:
        #     t_w = float(self.ui.lineEdit_FlangeThickness_Beam.text())
        #
        # if self.ui.lineEdit_WeBThickness_Beam.text() == "":
        #     return
        # else:
        #     t_f = float(self.ui.lineEdit_WeBThickness_Beam.text())
        #
        # self.sectionalprop = I_sectional_Properties()
        # self.ui.lineEdit_Mass_Beam.setText(str(self.sectionalprop.calc_Mass(D, B, t_w, t_f)))
        # self.ui.lineEdit_SectionalArea_Beam.setText(str(self.sectionalprop.calc_Area(D, B, t_w, t_f)))
        # self.ui.lineEdit_MomentOfAreaZ_Beam.setText(str(self.sectionalprop.calc_MomentOfAreaZ(D, B, t_w, t_f)))
        # self.ui.lineEdit_MomentOfAreaY_Beam.setText(str(self.sectionalprop.calc_MomentOfAreaY(D, B, t_w, t_f)))
        # self.ui.lineEdit_RogZ_Beam.setText(str(self.sectionalprop.calc_RogZ(D, B, t_w, t_f)))
        # self.ui.lineEdit_RogY_Beam.setText(str(self.sectionalprop.calc_RogY(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModZ_Beam.setText(str(self.sectionalprop.calc_ElasticModulusZz(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModY_Beam.setText(str(self.sectionalprop.calc_ElasticModulusZy(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModPZ_Beam.setText(str(self.sectionalprop.calc_PlasticModulusZpz(D, B, t_w, t_f)))
        # self.ui.lineEdit_ElasticModPY_Beam.setText(str(self.sectionalprop.calc_PlasticModulusZpy(D, B, t_w, t_f)))
        # self.ui.pushButton_Add_Beam.setEnabled(True)

    def add_ColumnPref(self, table):

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
            FlangeSlope_c = float(self.ui.lineEdit_FlangeSlope_Column.text())
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
            Zpz_c = self.ui.lineEdit_ElasticModPZ_Column.text()
            Zpy_c = self.ui.lineEdit_ElasticModPY_Column.text()
            Source_c = self.ui.lineEdit_Source_Column.text()

            conn = sqlite3.connect(PATH_TO_DATABASE)

            c = conn.cursor()
            if table == "Beams":
                c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_c,))
                data = c.fetchone()[0]
            else:
                c.execute("SELECT count(*) FROM Columns WHERE Designation = ?", (Designation_c,))
                data = c.fetchone()[0]
            if data == 0:
                if table == "Beams":
                    c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,R1,R2,Iz,Iy,rz,ry,
                                                                                                               Zz,zy,Zpz,Zpy,FlangeSlope,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (Designation_c, Mass_c, Area_c,
                               D_c, B_c, tw_c, T_c,
                               R1_c, R2_c, Iz_c, Iy_c, rz_c,
                               ry_c, Zz_c, Zy_c,
                               Zpz_c, Zpy_c, FlangeSlope_c, Source_c))
                    conn.commit()
                else:
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
            FlangeSlope_b = float(self.ui.lineEdit_FlangeSlope_Beam.text())
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
            Zpz_b = self.ui.lineEdit_ElasticModPZ_Beam.text()
            Zpy_b = self.ui.lineEdit_ElasticModPY_Beam.text()
            Source_b = self.ui.lineEdit_Source_Beam.text()

            conn = sqlite3.connect(PATH_TO_DATABASE)

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_b,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,R1,R2,Iz,Iy,rz,ry,Zz,zy,Zpz,Zpy,
    				                                                FlangeSlope,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
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
        #self.ui.pushButton_Import_Column.setEnabled(True)

    def download_Database_Beam(self):
        file_path = os.path.abspath(os.path.join(os.getcwd(), os.path.join("ResourceFiles", "add_sections.xlsx")))
        shutil.copyfile(file_path, os.path.join(str(self.folder), "images_html", "add_sections.xlsx"))
        QMessageBox.information(QMessageBox(), 'Information', 'Your File is Downloaded in your selected workspace')
        #self.ui.pushButton_Import_Beam.setEnabled(True)

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

    # def closeEvent(self, QCloseEvent):
    #     self.save_designPref_para()
    #     QCloseEvent.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DesignPreferences = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(DesignPreferences)
    DesignPreferences.exec()
    sys.exit(app.exec_())

