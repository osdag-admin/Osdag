# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_design_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DesignPreferences(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(808, 519)
        self.gridLayout_5 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout_2.addWidget(self.btn_save, 0, 2, 1, 1)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_close.setFont(font)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout_2.addWidget(self.btn_close, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.btn_defaults = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.btn_defaults.setFont(font)
        self.btn_defaults.setObjectName("btn_defaults")
        self.gridLayout_2.addWidget(self.btn_defaults, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_Bolt = QtWidgets.QWidget()
        self.tab_Bolt.setObjectName("tab_Bolt")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.tab_Bolt)
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.label_9 = QtWidgets.QLabel(self.tab_Bolt)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.gridLayout_22.addWidget(self.label_9, 0, 2, 1, 1)
        self.gridLayout_21 = QtWidgets.QGridLayout()
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_9.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.combo_boltHoleType = QtWidgets.QComboBox(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.combo_boltHoleType.setFont(font)
        self.combo_boltHoleType.setFocusPolicy(QtCore.Qt.TabFocus)
        self.combo_boltHoleType.setObjectName("combo_boltHoleType")
        self.combo_boltHoleType.addItem("")
        self.combo_boltHoleType.addItem("")
        self.gridLayout.addWidget(self.combo_boltHoleType, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_Bolt)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.txt_boltFu = QtWidgets.QLineEdit(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.txt_boltFu.setFont(font)
        self.txt_boltFu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_boltFu.setReadOnly(False)
        self.txt_boltFu.setObjectName("txt_boltFu")
        self.gridLayout.addWidget(self.txt_boltFu, 2, 1, 1, 1)
        self.combo_boltType = QtWidgets.QComboBox(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.combo_boltType.setFont(font)
        self.combo_boltType.setObjectName("combo_boltType")
        self.combo_boltType.addItem("")
        self.combo_boltType.addItem("")
        self.gridLayout.addWidget(self.combo_boltType, 0, 1, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout, 0, 1, 3, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_9.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_9.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_9, 0, 0, 1, 2)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem2 = QtWidgets.QSpacerItem(168, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem2, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_12.addWidget(self.label_7, 1, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_12.addWidget(self.label_15, 2, 0, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_12, 1, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        spacerItem3 = QtWidgets.QSpacerItem(128, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem3, 0, 0, 1, 1)
        self.combo_slipfactor = QtWidgets.QComboBox(self.tab_Bolt)
        self.combo_slipfactor.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_slipfactor.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.combo_slipfactor.setFont(font)
        self.combo_slipfactor.setObjectName("combo_slipfactor")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.combo_slipfactor.addItem("")
        self.gridLayout_11.addWidget(self.combo_slipfactor, 1, 0, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_11, 1, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_14, 1, 0, 1, 1)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.label_5 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_15.addWidget(self.label_5, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.tab_Bolt)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_15.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_15, 0, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_16, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(17, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_21.addItem(spacerItem4, 1, 0, 1, 1)
        self.gridLayout_20 = QtWidgets.QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.label_note = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_note.setFont(font)
        self.label_note.setObjectName("label_note")
        self.gridLayout_20.addWidget(self.label_note, 0, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_20.addItem(spacerItem5, 1, 0, 1, 1)
        self.gridLayout_21.addLayout(self.gridLayout_20, 2, 0, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_21, 1, 0, 2, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_3 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 0, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.tab_Bolt)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_8.addWidget(self.line_4, 1, 0, 1, 1)
        self.gridLayout_19.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_Bolt)
        self.textBrowser.setMinimumSize(QtCore.QSize(210, 320))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_19.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.gridLayout_22.addLayout(self.gridLayout_19, 1, 1, 2, 2)
        self.label_11 = QtWidgets.QLabel(self.tab_Bolt)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_11.setFont(font)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.gridLayout_22.addWidget(self.label_11, 2, 2, 1, 1)
        self.tabWidget.addTab(self.tab_Bolt, "")
        self.tab_Weld = QtWidgets.QWidget()
        self.tab_Weld.setObjectName("tab_Weld")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_Weld)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_16 = QtWidgets.QLabel(self.tab_Weld)
        self.label_16.setObjectName("label_16")
        self.gridLayout_13.addWidget(self.label_16, 0, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_17 = QtWidgets.QLabel(self.tab_Weld)
        self.label_17.setObjectName("label_17")
        self.gridLayout_7.addWidget(self.label_17, 0, 0, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.tab_Weld)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_7.addWidget(self.line_5, 1, 0, 1, 1)
        self.textBrowser_weldDescription = QtWidgets.QTextBrowser(self.tab_Weld)
        self.textBrowser_weldDescription.setMinimumSize(QtCore.QSize(210, 320))
        self.textBrowser_weldDescription.setObjectName("textBrowser_weldDescription")
        self.gridLayout_7.addWidget(self.textBrowser_weldDescription, 2, 0, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_7, 0, 2, 4, 1)
        self.line_8 = QtWidgets.QFrame(self.tab_Weld)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_13.addWidget(self.line_8, 1, 0, 1, 2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.tab_Weld)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.combo_weldType = QtWidgets.QComboBox(self.tab_Weld)
        self.combo_weldType.setObjectName("combo_weldType")
        self.combo_weldType.addItem("")
        self.combo_weldType.addItem("")
        self.gridLayout_3.addWidget(self.combo_weldType, 0, 2, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.tab_Weld)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 0, 0, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.tab_Weld)
        self.label_27.setText("")
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 1, 0, 1, 1)
        self.txt_weldFu = QtWidgets.QLineEdit(self.tab_Weld)
        self.txt_weldFu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_weldFu.setObjectName("txt_weldFu")
        self.gridLayout_3.addWidget(self.txt_weldFu, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab_Weld)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 2, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_3, 2, 0, 1, 2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 288, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_13.addItem(spacerItem6, 3, 1, 1, 1)
        self.tabWidget.addTab(self.tab_Weld, "")
        self.tab_Detailing = QtWidgets.QWidget()
        self.tab_Detailing.setObjectName("tab_Detailing")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.tab_Detailing)
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_38 = QtWidgets.QLabel(self.tab_Detailing)
        self.label_38.setObjectName("label_38")
        self.gridLayout_6.addWidget(self.label_38, 0, 0, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.tab_Detailing)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout_6.addWidget(self.line_11, 1, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_39 = QtWidgets.QLabel(self.tab_Detailing)
        self.label_39.setObjectName("label_39")
        self.gridLayout_4.addWidget(self.label_39, 0, 0, 1, 1)
        self.combo_detailingEdgeType = QtWidgets.QComboBox(self.tab_Detailing)
        self.combo_detailingEdgeType.setObjectName("combo_detailingEdgeType")
        self.combo_detailingEdgeType.addItem("")
        self.combo_detailingEdgeType.addItem("")
        self.gridLayout_4.addWidget(self.combo_detailingEdgeType, 0, 1, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.tab_Detailing)
        self.label_40.setObjectName("label_40")
        self.gridLayout_4.addWidget(self.label_40, 1, 0, 1, 1)
        self.combo_detailing_memebers = QtWidgets.QComboBox(self.tab_Detailing)
        self.combo_detailing_memebers.setObjectName("combo_detailing_memebers")
        self.combo_detailing_memebers.addItem("")
        self.combo_detailing_memebers.addItem("")
        self.gridLayout_4.addWidget(self.combo_detailing_memebers, 1, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_17, 0, 0, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.line_6 = QtWidgets.QFrame(self.tab_Detailing)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_10.addWidget(self.line_6, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.tab_Detailing)
        self.label_18.setObjectName("label_18")
        self.gridLayout_10.addWidget(self.label_18, 0, 0, 1, 1)
        self.textBrowser_detailingDescription = QtWidgets.QTextBrowser(self.tab_Detailing)
        self.textBrowser_detailingDescription.setMinimumSize(QtCore.QSize(210, 0))
        self.textBrowser_detailingDescription.setObjectName("textBrowser_detailingDescription")
        self.gridLayout_10.addWidget(self.textBrowser_detailingDescription, 2, 0, 1, 1)
        self.gridLayout_18.addLayout(self.gridLayout_10, 0, 1, 2, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 255, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_18.addItem(spacerItem7, 1, 0, 1, 1)
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

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.combo_slipfactor.setCurrentIndex(8)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Design preferences"))
        self.btn_save.setText(_translate("Dialog", "Save"))
        self.btn_close.setText(_translate("Dialog", "Save"))
        self.btn_defaults.setText(_translate("Dialog", "Defaults"))
        self.label.setText(_translate("Dialog", "Bolt type"))
        self.combo_boltHoleType.setItemText(0, _translate("Dialog", "Standard"))
        self.combo_boltHoleType.setItemText(1, _translate("Dialog", "Over-sized"))
        self.label_8.setText(_translate("Dialog", "Fu"))
        self.txt_boltFu.setText(_translate("Dialog", "800"))
        self.combo_boltType.setItemText(0, _translate("Dialog", "Pretensioned"))
        self.combo_boltType.setItemText(1, _translate("Dialog", "Non-pretensioned"))
        self.label_4.setText(_translate("Dialog", "Material grade overwrite (MPa)"))
        self.label_2.setText(_translate("Dialog", "Bolt hole type"))
        self.label_7.setText(_translate("Dialog", "HSFG bolt design parameters:"))
        self.label_15.setText(_translate("Dialog", "Slip factor (µ_f)"))
        self.combo_slipfactor.setItemText(0, _translate("Dialog", "0.2"))
        self.combo_slipfactor.setItemText(1, _translate("Dialog", "0.5"))
        self.combo_slipfactor.setItemText(2, _translate("Dialog", "0.1"))
        self.combo_slipfactor.setItemText(3, _translate("Dialog", "0.25"))
        self.combo_slipfactor.setItemText(4, _translate("Dialog", "0.3"))
        self.combo_slipfactor.setItemText(5, _translate("Dialog", "0.33"))
        self.combo_slipfactor.setItemText(6, _translate("Dialog", "0.48"))
        self.combo_slipfactor.setItemText(7, _translate("Dialog", "0.52"))
        self.combo_slipfactor.setItemText(8, _translate("Dialog", "0.55"))
        self.label_5.setText(_translate("Dialog", "Inputs"))
        self.label_note.setText(_translate("Dialog", "NOTE : If slip is permitted under the design load, design the bolt as a bearing\n"
"bolt and select corresponding bolt grade."))
        self.label_3.setText(_translate("Dialog", "Description"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td colspan=\"3\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">IS 800 Table 20 Typical Average Values for Coefficient of Friction (</span><span style=\" font-family:\'Calibri,sans-serif\';\">µ</span><span style=\" font-family:\'Calibri,sans-serif\'; vertical-align:sub;\">f</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">)</span></p></td></tr></table>\n"
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Bolt), _translate("Dialog", "Bolt"))
        self.label_16.setText(_translate("Dialog", "Inputs"))
        self.label_17.setText(_translate("Dialog", "Description"))
        self.textBrowser_weldDescription.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Shop weld takes a material safety factor of 1.25</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Field weld takes a material safety factor of 1.5</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">(IS 800 - cl. 5. 4. 1 or Table 5)</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog", "Material grade overwrite (MPa)"))
        self.combo_weldType.setItemText(0, _translate("Dialog", "Shop weld"))
        self.combo_weldType.setItemText(1, _translate("Dialog", "Field weld"))
        self.label_22.setText(_translate("Dialog", "Type of weld"))
        self.txt_weldFu.setText(_translate("Dialog", "410"))
        self.label_10.setText(_translate("Dialog", "Fu"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Weld), _translate("Dialog", "Weld"))
        self.label_38.setText(_translate("Dialog", "Inputs"))
        self.label_39.setText(_translate("Dialog", "Type of edges"))
        self.combo_detailingEdgeType.setItemText(0, _translate("Dialog", "a - Sheared or hand flame cut"))
        self.combo_detailingEdgeType.setItemText(1, _translate("Dialog", "b - Rolled, machine-flame cut, sawn and planed"))
        self.label_40.setText(_translate("Dialog", "Are the members exposed to\n"
"corrosive influences?"))
        self.combo_detailing_memebers.setItemText(0, _translate("Dialog", "No"))
        self.combo_detailing_memebers.setItemText(1, _translate("Dialog", "Yes"))
        self.label_18.setText(_translate("Dialog", "Description"))
        self.textBrowser_detailingDescription.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.7</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[a- sheared or hand flame cut edges] </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">and </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">1.5 </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">times the hole diameter in case of </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">[b - Rolled, machine-flame cut, sawn and planed edges]</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> (IS 800 - cl. 10. 2. 4. 2)</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt; vertical-align:middle;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">This gap should include the tolerance value of 5mm. So if the assumed clearance is 5mm, then the gap should be = 10mm (= 5mm {clearance} + 5 mm{tolerance})</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:8pt;\"><br /></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\">Specifying whether the members are exposed to corrosive influences, here, only affects the calculation of the maximum edge distance as per cl. 10.2.4.3</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Detailing), _translate("Dialog", "Detailing"))
        self.label_19.setText(_translate("Dialog", "Design Method"))
        self.combo_design_method.setItemText(0, _translate("Dialog", "Limit State Design"))
        self.combo_design_method.setItemText(1, _translate("Dialog", "Limit State (Capacity based) Design"))
        self.combo_design_method.setItemText(2, _translate("Dialog", "Working Stress Design"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Design), _translate("Dialog", "Design"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_DesignPreferences()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

