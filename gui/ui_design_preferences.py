# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from Common import *
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.shear_connection import ShearConnection

from PyQt5 import QtCore, QtGui, QtWidgets


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
            if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE, TYPE_BREAK, TYPE_ENTER]:
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

            if type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
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
            if type not in [TYPE_TITLE, TYPE_IMAGE, TYPE_MODULE, TYPE_BREAK, TYPE_ENTER]:
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

            if type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
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
            if type not in [TYPE_TITLE, TYPE_ENTER]:
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
                if element[3] != None:
                    r.setText(element[3])

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
            if type not in [TYPE_TITLE, TYPE_ENTER]:
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
                if element[3] != None:
                    r.setText(element[3])

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
        label_3.setGeometry(QtCore.QRect(400, 10, 130, 22))
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
            if type not in [TYPE_TITLE, TYPE_ENTER]:
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
                combo.setGeometry(QtCore.QRect(180, 10 + i, 270, 30))
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
                r.setGeometry(QtCore.QRect(180, 10 + i, 270, 30))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(False)
                font.setWeight(50)
                r.setFont(font)
                r.setObjectName(element[0])
                if element[3] != None:
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
        self.label_19 = QtWidgets.QLabel(self.tab_Design)
        self.label_19.setGeometry(QtCore.QRect(21, 31, 101, 16))
        self.label_19.setObjectName("label_19")
        self.combo_design_method = QtWidgets.QComboBox(self.tab_Design)
        self.combo_design_method.setGeometry(QtCore.QRect(160, 31, 227, 22))
        self.combo_design_method.setObjectName("combo_design_method")
        self.combo_design_method.addItem("")
        self.combo_design_method.addItem("")
        self.combo_design_method.addItem("")
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


    def retranslateUi(self, DesignPreferences):
        _translate = QtCore.QCoreApplication.translate
        DesignPreferences.setWindowTitle(_translate("DesignPreferences", "Design preferences"))
        self.btn_defaults.setText(_translate("DesignPreferences", "Defaults"))
        self.btn_save.setText(_translate("DesignPreferences", "Save"))
        self.btn_close.setText(_translate("DesignPreferences", "Save"))
        # self.label_49.setText(_translate("DesignPreferences", "Web thickness, t (mm)*"))
        # self.label_50.setText(_translate("DesignPreferences", "Root radius, R1 (mm)*"))
        # self.label_36.setText(_translate("DesignPreferences", "Toe radius, R2 (mm)*"))
        # self.label_45.setText(_translate("DesignPreferences", "Dimensions"))
        # self.label_28.setText(_translate("DesignPreferences", "Flange width, B (mm)*"))
        # self.label_48.setText(_translate("DesignPreferences", "Flange thickness, T (mm)*"))
        # self.label_47.setText(_translate("DesignPreferences", "<html><head/><body><p>Flange Slope, <span style=\" font-family:\'Symbol\'; font-size:large;\">a </span>(deg.)*</p></body></html>"))
        # self.label_54.setText(_translate("DesignPreferences", "Depth, D (mm)*"))
        # self.label_85.setText(_translate("DesignPreferences", "Poissons ratio, v"))
        # self.comboBox_Column.setItemText(0, _translate("DesignPreferences", "Rolled"))
        # self.comboBox_Column.setItemText(1, _translate("DesignPreferences", "Welded"))
        # self.label_43.setText(_translate("DesignPreferences", "<html><head/><body><p>Plastic modulus, Z<span style=\" vertical-align:sub;\">pz</span> (cm<span style=\" vertical-align:super;\">3</span> )</p></body></html>"))
        # self.label_46.setText(_translate("DesignPreferences", "Ultimate strength, fu (MPa)"))
        # self.label_31.setText(_translate("DesignPreferences", "Modulus of elasticity, E (GPa)"))
        # self.label_32.setText(_translate("DesignPreferences", "Mechanical Properties"))
        # self.label_30.setText(_translate("DesignPreferences", "<html><head/><body><p><span style=\" font-size:10pt;\">Designation</span></p></body></html>"))
        # self.label_35.setText(_translate("DesignPreferences", "<html><head/><body><p><span style=\" font-size:10pt;\">Source</span></p></body></html>"))
        # self.label_41.setText(_translate("DesignPreferences", "<html><head/><body><p><span style=\" font-size:10pt;\">Type</span></p></body></html>"))
        # self.label_34.setText(_translate("DesignPreferences", "<html><head/><body><p>2nd Moment of area, I<span style=\" vertical-align:sub;\">z</span>(cm<span style=\" vertical-align:super;\">4</span>)</p></body></html>"))
        # self.label_53.setText(_translate("DesignPreferences", "Mass, M (kg/m)"))
        # self.label_42.setText(_translate("DesignPreferences", "<html><head/><body><p>Elastic modulus, Z<span style=\" vertical-align:sub;\">z</span> (cm<span style=\" vertical-align:super;\">3</span>)</p></body></html>"))
        # self.label_52.setText(_translate("DesignPreferences", "Sectional Properties"))
        # self.label_51.setText(_translate("DesignPreferences", "<html><head/><body><p>Radius of gyration, r<span style=\" vertical-align:sub;\">z</span> (cm)</p></body></html>"))
        # self.label_33.setText(_translate("DesignPreferences", "<html><head/><body><p>Radius of gyration, r<span style=\" vertical-align:sub;\">y</span> (cm)</p></body></html>"))
        # self.label_44.setText(_translate("DesignPreferences", "<html><head/><body><p>Elastic modulus, Z<span style=\" vertical-align:sub;\">y</span> (cm<span style=\" vertical-align:super;\">3</span>)</p></body></html>"))
        # self.label_29.setText(_translate("DesignPreferences", "<html><head/><body><p>2nd Moment of area,I<span style=\" vertical-align:sub;\">y</span> (cm<span style=\" vertical-align:super;\">4</span>)</p></body></html>"))
        # self.label_57.setText(_translate("DesignPreferences", "<html><head/><body><p>Sectional area, a (mm<span style=\" vertical-align:super;\">2</span>)</p></body></html>"))
        # self.label_56.setText(_translate("DesignPreferences", "<html><head/><body><p>Plastic modulus, Z<span style=\" vertical-align:sub;\">py</span> (cm<span style=\" vertical-align:super;\">3</span> )</p></body></html>"))
        # self.label_86.setText(_translate("DesignPreferences", "<html><head/><body><p>Thermal expansion </p><p>coeff.<span style=\" font-family:\'Symbol\'; font-size:large;\">a </span>(x10<span style=\" vertical-align:super;\">-6</span>/<span style=\" vertical-align:super;\">0</span>C)</p></body></html>"))
        # self.label_55.setText(_translate("DesignPreferences", "Yield Strength , fy (MPa)"))
        # self.label_37.setText(_translate("DesignPreferences", "Modulus of rigidity, G (GPa)"))
        # self.pushButton_Clear_Column.setText(_translate("DesignPreferences", "Clear"))
        # self.pushButton_Add_Column.setText(_translate("DesignPreferences", "Add"))
        # self.pushButton_Download_Column.setText(_translate("DesignPreferences", "Download xlsx format"))
        # self.pushButton_Import_Column.setText(_translate("DesignPreferences", "Import xlsx file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Column), _translate("DesignPreferences", "Column"))
        # self.pushButton_Download_Beam.setText(_translate("DesignPreferences", "Download xlsx format"))
        # self.pushButton_Import_Beam.setText(_translate("DesignPreferences", "Import xlsx file"))
        # self.label_74.setText(_translate("DesignPreferences", "<html><head/><body><p><span style=\" font-size:10pt;\">Source</span></p></body></html>"))
        # self.pushButton_Clear_Beam.setText(_translate("DesignPreferences", "Clear"))
        # self.pushButton_Add_Beam.setText(_translate("DesignPreferences", "Add"))
        # self.label_75.setText(_translate("DesignPreferences", "Sectional Properties"))
        # self.label_77.setText(_translate("DesignPreferences", "Dimensions"))
        # self.label_58.setText(_translate("DesignPreferences", "Modulus of elasticity, E (GPa)"))
        # self.comboBox_Beam.setItemText(0, _translate("DesignPreferences", "Rolled"))
        # self.comboBox_Beam.setItemText(1, _translate("DesignPreferences", "Welded"))
        # self.label_66.setText(_translate("DesignPreferences", "Modulus of rigidity, G (GPa)"))
        # self.label_79.setText(_translate("DesignPreferences", "Ultimate strength, fu (MPa)"))
        # self.label_81.setText(_translate("DesignPreferences", "Mechanical Properties"))
        # self.label_88.setText(_translate("DesignPreferences", "Poissons ratio, v"))
        # self.label_89.setText(_translate("DesignPreferences", "<html><head/><body><p>Thermal expansion </p><p>coeff.<span style=\" font-family:\'Symbol\'; font-size:large;\">a </span>(x10<span style=\" vertical-align:super;\">-6</span>/<span style=\" vertical-align:super;\">0</span>C)</p></body></html>"))
        # self.label_80.setText(_translate("DesignPreferences", "Depth, D (mm)*"))
        # self.label_64.setText(_translate("DesignPreferences", "<html><head/><body><p><span style=\" font-size:10pt;\">Designation</span></p></body></html>"))
        # self.label_63.setText(_translate("DesignPreferences", "<html><head/><body><p><span style=\" font-size:10pt;\">Type</span></p></body></html>"))
        # self.label_150.setText(_translate("DesignPreferences", "<html><head/><body><p>Radius of gyration, r<span style=\" vertical-align:sub;\">z</span> (cm)</p></body></html>"))
        # self.label_145.setText(_translate("DesignPreferences", "<html><head/><body><p>Elastic modulus, Z<span style=\" vertical-align:sub;\">y</span> (cm<span style=\" vertical-align:super;\">3</span>)</p></body></html>"))
        # self.label_78.setText(_translate("DesignPreferences", "Toe radius, R2 (mm)*"))
        # self.label_147.setText(_translate("DesignPreferences", "<html><head/><body><p>Sectional area, a (mm<span style=\" vertical-align:super;\">2</span>)</p></body></html>"))
        # self.label_152.setText(_translate("DesignPreferences", "<html><head/><body><p>Plastic modulus, Z<span style=\" vertical-align:sub;\">pz</span> (cm<span style=\" vertical-align:super;\">3</span> )</p></body></html>"))
        # self.label_153.setText(_translate("DesignPreferences", "<html><head/><body><p>Radius of gyration, r<span style=\" vertical-align:sub;\">y</span> (cm)</p></body></html>"))
        # self.label_82.setText(_translate("DesignPreferences", "Yield Strength , fy (MPa)"))
        # self.label_72.setText(_translate("DesignPreferences", "<html><head/><body><p>Flange Slope, <span style=\" font-family:\'Symbol\'; font-size:large;\">a </span>(deg.)*</p></body></html>"))
        # self.label_73.setText(_translate("DesignPreferences", "Root radius, R1 (mm)*"))
        # self.label_151.setText(_translate("DesignPreferences", "<html><head/><body><p>Elastic modulus, Z<span style=\" vertical-align:sub;\">z</span> (cm<span style=\" vertical-align:super;\">3</span>)</p></body></html>"))
        # self.label_61.setText(_translate("DesignPreferences", "Flange thickness, T (mm)*"))
        # self.label_62.setText(_translate("DesignPreferences", "Mass, M (kg/m)"))
        # self.label_146.setText(_translate("DesignPreferences", "<html><head/><body><p>2nd Moment of area, I<span style=\" vertical-align:sub;\">z</span>(cm<span style=\" vertical-align:super;\">4</span>)</p></body></html>"))
        # self.label_59.setText(_translate("DesignPreferences", "Flange width, B (mm)*"))
        # self.label_149.setText(_translate("DesignPreferences", "<html><head/><body><p>2nd Moment of area,I<span style=\" vertical-align:sub;\">y</span> (cm<span style=\" vertical-align:super;\">4</span>)</p></body></html>"))
        # self.label_69.setText(_translate("DesignPreferences", "Web thickness, t (mm)*"))
        # self.label_148.setText(_translate("DesignPreferences", "<html><head/><body><p>Plastic modulus, Z<span style=\" vertical-align:sub;\">py</span> (cm<span style=\" vertical-align:super;\">3</span> )</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Beam), _translate("DesignPreferences", "Beam"))
#         self.label_note.setText(_translate("DesignPreferences", "NOTE : If slip is permitted under the design load, design the bolt as a bearing\n"
# "bolt and select corresponding bolt grade."))
#         self.label.setText(_translate("DesignPreferences", "Bolt type"))
#         self.label_4.setText(_translate("DesignPreferences", "Material grade overwrite (MPa)"))
#         self.label_2.setText(_translate("DesignPreferences", "Bolt hole type"))
#         self.combo_boltHoleType.setItemText(0, _translate("DesignPreferences", "Standard"))
#         self.combo_boltHoleType.setItemText(1, _translate("DesignPreferences", "Over-sized"))
#         self.label_8.setText(_translate("DesignPreferences", "Fu"))
#         self.txt_boltFu.setText(_translate("DesignPreferences", "800"))
#         self.combo_boltType.setItemText(0, _translate("DesignPreferences", "Pretensioned"))
#         self.combo_boltType.setItemText(1, _translate("DesignPreferences", "Non-pretensioned"))
#         self.label_7.setText(_translate("DesignPreferences", "HSFG bolt design parameters:"))
#         self.label_15.setText(_translate("DesignPreferences", "Slip factor (µ_f)"))
#         self.combo_slipfactor.setItemText(0, _translate("DesignPreferences", "0.2"))
#         self.combo_slipfactor.setItemText(1, _translate("DesignPreferences", "0.5"))
#         self.combo_slipfactor.setItemText(2, _translate("DesignPreferences", "0.1"))
#         self.combo_slipfactor.setItemText(3, _translate("DesignPreferences", "0.25"))
#         self.combo_slipfactor.setItemText(4, _translate("DesignPreferences", "0.3"))
#         self.combo_slipfactor.setItemText(5, _translate("DesignPreferences", "0.33"))
#         self.combo_slipfactor.setItemText(6, _translate("DesignPreferences", "0.48"))
#         self.combo_slipfactor.setItemText(7, _translate("DesignPreferences", "0.52"))
#         self.combo_slipfactor.setItemText(8, _translate("DesignPreferences", "0.55"))
#         self.label_5.setText(_translate("DesignPreferences", "Inputs"))
#         self.label_3.setText(_translate("DesignPreferences", "Description"))
#         self.textBrowser.setHtml(_translate("DesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
# "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
# "<tr>\n"
# "<td colspan=\"3\">\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">IS 800 Table 20 Typical Average Values for Coefficient of Friction (</span><span style=\" font-family:\'Calibri,sans-serif\'; font-size:9pt;\">µ</span><span style=\" font-family:\'Calibri,sans-serif\'; font-size:9pt; vertical-align:sub;\">f</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">)</span></p></td></tr></table>\n"
# "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
# "<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
# "<tr>\n"
# "<td width=\"26\"></td>\n"
# "<td width=\"383\">\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Treatment of Surfaces</span></p></td>\n"
# "<td width=\"78\">\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  µ_f</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">i)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces not treated</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.2</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">ii)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit with any loose rust removed, no pitting</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.5</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">iii)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit and hot-dip galvanized</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.1</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">iv)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with short or grit and spray - metallized with zinc (thickness 50-70 µm)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.25</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">v)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with ethylzinc silicate coat (thickness 30-60 µm)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">vi)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sand blasted surface, after light rusting</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.52</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">vii)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with ethylzinc silicate coat (thickness 60-80 µm)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">viii)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and painted with alcalizinc silicate coat (thickness 60-80 µm)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.3</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">ix)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Surfaces blasted with shot or grit and spray metallized with aluminium (thickness &gt;50 µm)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.5</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">x)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Clean mill scale</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.33</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">xi)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Sand blasted surface</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.48</span></p></td></tr>\n"
# "<tr>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">xii)</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Red lead painted surface</span></p></td>\n"
# "<td>\n"
# "<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">  0.1</span></p>\n"
# "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></td></tr></table></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Bolt), _translate("DesignPreferences", "Bolt"))
#         self.label_16.setText(_translate("DesignPreferences", "Inputs"))
#         self.label_17.setText(_translate("DesignPreferences", "Description"))
#         self.textBrowser_weldDescription.setHtml(_translate("DesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Shop weld takes a material safety factor of 1.25</span></p>\n"
# "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Field weld takes a material safety factor of 1.5</span></p>\n"
# "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">(IS 800 - cl. 5. 4. 1 or Table 5)</span></p></body></html>"))
#         self.label_6.setText(_translate("DesignPreferences", "Material grade overwrite (MPa)"))
#         self.combo_weldType.setItemText(0, _translate("DesignPreferences", "Shop weld"))
#         self.combo_weldType.setItemText(1, _translate("DesignPreferences", "Field weld"))
#         self.label_22.setText(_translate("DesignPreferences", "Type of weld"))
#         self.txt_weldFu.setText(_translate("DesignPreferences", "410"))
#         self.label_10.setText(_translate("DesignPreferences", "Fu"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Weld), _translate("DesignPreferences", "Weld"))
#         self.label_38.setText(_translate("DesignPreferences", "Inputs"))
#         self.label_39.setText(_translate("DesignPreferences", "Type of edges"))
#         self.combo_detailingEdgeType.setItemText(0, _translate("DesignPreferences", "a - Sheared or hand flame cut"))
#         self.combo_detailingEdgeType.setItemText(1, _translate("DesignPreferences", "b - Rolled, machine-flame cut, sawn and planed"))
#         self.label_40.setText(_translate("DesignPreferences", "Are the members exposed to\n"
# "corrosive influences?"))
#         self.combo_detailing_memebers.setItemText(0, _translate("DesignPreferences", "No"))
#         self.combo_detailing_memebers.setItemText(1, _translate("DesignPreferences", "Yes"))
#         self.label_12.setText(_translate("Dialog", "Gap between beam & support (mm)"))
#         self.label_18.setText(_translate("DesignPreferences", "Description"))
#         self.textBrowser_detailingDescription.setHtml(_translate("DesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'Arial\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.7</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[a- sheared or hand flame cut edges] </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">and </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.5 </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[b - Rolled, machine-flame cut, sawn and planed edges]</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> (IS 800 - cl. 10. 2. 4. 2)</span></p>\n"
# "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
# "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">This gap should include the tolerance value of 5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5 mm{tolerance})</span></p>\n"
# "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
# "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3</span></p>\n"
# "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Detailing), _translate("DesignPreferences", "Detailing"))
        self.label_19.setText(_translate("DesignPreferences", "Design Method"))
        self.combo_design_method.setItemText(0, _translate("DesignPreferences", "Limit State Design"))
        self.combo_design_method.setItemText(1, _translate("DesignPreferences", "Limit State (Capacity based) Design"))
        self.combo_design_method.setItemText(2, _translate("DesignPreferences", "Working Stress Design"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Design), _translate("DesignPreferences", "Design"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DesignPreferences = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(DesignPreferences)
    DesignPreferences.show()
    sys.exit(app.exec_())

