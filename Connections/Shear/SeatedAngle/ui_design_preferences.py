# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ShearDesignPreferences(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(822, 462)
        self.gridLayout_5 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout_2.addWidget(self.btn_save, 0, 2, 1, 1)
        self.btn_defaults = QtWidgets.QPushButton(Dialog)
        self.btn_defaults.setObjectName("btn_defaults")
        self.gridLayout_2.addWidget(self.btn_defaults, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 4, 1, 1)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout_2.addWidget(self.btn_close, 0, 3, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 5, 1, 1)
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 5)
        self.line_4 = QtWidgets.QFrame(self.tab)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 1, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.combo_boltHoleType = QtWidgets.QComboBox(self.tab)
        self.combo_boltHoleType.setFocusPolicy(QtCore.Qt.TabFocus)
        self.combo_boltHoleType.setObjectName("combo_boltHoleType")
        self.combo_boltHoleType.addItem("")
        self.combo_boltHoleType.addItem("")
        self.gridLayout.addWidget(self.combo_boltHoleType, 2, 2, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setMinimumSize(QtCore.QSize(210, 320))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 5, 5, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.txt_boltHoleClearance = QtWidgets.QLineEdit(self.tab)
        self.txt_boltHoleClearance.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_boltHoleClearance.setObjectName("txt_boltHoleClearance")
        self.gridLayout.addWidget(self.txt_boltHoleClearance, 3, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 5, 1, 1, 1)
        self.txt_boltFu = QtWidgets.QLineEdit(self.tab)
        self.txt_boltFu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_boltFu.setObjectName("txt_boltFu")
        self.gridLayout.addWidget(self.txt_boltFu, 5, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 5, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 201, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 0, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setObjectName("label_17")
        self.gridLayout_7.addWidget(self.label_17, 0, 0, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.tab_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_7.addWidget(self.line_5, 1, 0, 1, 1)
        self.textBrowser_weldDescription = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_weldDescription.setMinimumSize(QtCore.QSize(210, 320))
        self.textBrowser_weldDescription.setObjectName("textBrowser_weldDescription")
        self.gridLayout_7.addWidget(self.textBrowser_weldDescription, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 4, 6, 1)
        self.line_8 = QtWidgets.QFrame(self.tab_2)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_3.addWidget(self.line_8, 1, 0, 1, 4)
        self.label_22 = QtWidgets.QLabel(self.tab_2)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 2, 0, 1, 1)
        self.combo_weldType = QtWidgets.QComboBox(self.tab_2)
        self.combo_weldType.setObjectName("combo_weldType")
        self.combo_weldType.addItem("")
        self.combo_weldType.addItem("")
        self.gridLayout_3.addWidget(self.combo_weldType, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 4, 1, 1, 1)
        self.txt_weldFu = QtWidgets.QLineEdit(self.tab_2)
        self.txt_weldFu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_weldFu.setObjectName("txt_weldFu")
        self.gridLayout_3.addWidget(self.txt_weldFu, 4, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 4, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 288, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 5, 2, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_38 = QtWidgets.QLabel(self.tab_5)
        self.label_38.setObjectName("label_38")
        self.gridLayout_9.addWidget(self.label_38, 0, 0, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.tab_5)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout_9.addWidget(self.line_11, 1, 0, 1, 4)
        self.label_39 = QtWidgets.QLabel(self.tab_5)
        self.label_39.setObjectName("label_39")
        self.gridLayout_9.addWidget(self.label_39, 2, 0, 1, 1)
        self.combo_detailingEdgeType = QtWidgets.QComboBox(self.tab_5)
        self.combo_detailingEdgeType.setObjectName("combo_detailingEdgeType")
        self.combo_detailingEdgeType.addItem("")
        self.combo_detailingEdgeType.addItem("")
        self.gridLayout_9.addWidget(self.combo_detailingEdgeType, 2, 1, 1, 2)
        self.label_29 = QtWidgets.QLabel(self.tab_5)
        self.label_29.setObjectName("label_29")
        self.gridLayout_9.addWidget(self.label_29, 3, 0, 1, 1)
        self.txt_detailingGap = QtWidgets.QLineEdit(self.tab_5)
        self.txt_detailingGap.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txt_detailingGap.setObjectName("txt_detailingGap")
        self.gridLayout_9.addWidget(self.txt_detailingGap, 3, 1, 1, 1)
        self.label_36 = QtWidgets.QLabel(self.tab_5)
        self.label_36.setObjectName("label_36")
        self.gridLayout_9.addWidget(self.label_36, 3, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem4, 3, 3, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.line_6 = QtWidgets.QFrame(self.tab_5)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_10.addWidget(self.line_6, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.tab_5)
        self.label_18.setObjectName("label_18")
        self.gridLayout_10.addWidget(self.label_18, 0, 0, 1, 1)
        self.textBrowser_detailingDescription = QtWidgets.QTextBrowser(self.tab_5)
        self.textBrowser_detailingDescription.setMinimumSize(QtCore.QSize(210, 0))
        self.textBrowser_detailingDescription.setObjectName("textBrowser_detailingDescription")
        self.gridLayout_10.addWidget(self.textBrowser_detailingDescription, 2, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 1, 2, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 255, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_11.addItem(spacerItem5, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")
        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Design preferences"))
        self.btn_save.setText(_translate("Dialog", "Save"))
        self.btn_defaults.setText(_translate("Dialog", "Defaults"))
        self.btn_close.setText(_translate("Dialog", "Close"))
        self.label_5.setText(_translate("Dialog", "Inputs"))
        self.label_3.setText(_translate("Dialog", "Description"))
        self.label.setText(_translate("Dialog", "Bolt hole type"))
        self.combo_boltHoleType.setItemText(0, _translate("Dialog", "Standard"))
        self.combo_boltHoleType.setItemText(1, _translate("Dialog", "Over-sized"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">IS 4000: 1992 - Annex C recommended slip factors:</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p>\n"
"<table border=\"0\" style=\" border-color:#a3a3a3; border-style:solid; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"0\" cellpadding=\"0\">\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Treatment of surface</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\';\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Slip factor </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Surface not treated</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.2</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Surface blasted with shot or grit </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\"> </span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">with any loose rust removed, no pitting</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.5</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and hot-dip galvanized</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.1</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and spray-metallized with zinc (thickness 50-70 micro-m</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.25</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and painted with ethyl-zinc silicate coat (thickness 30-80  micro-m)</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.30</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and painted with alkali-zinc silicate coat (thickness 60-80  micro-m</span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.30</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and spray metallized with aluminium (thickness &gt; 50  micro-m)</span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.5</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"> </span></p></td></tr></table></body></html>"))
        self.label_2.setText(_translate("Dialog", "Bolt hole clearance"))
        self.txt_boltHoleClearance.setText(_translate("Dialog", "2"))
        self.label_9.setText(_translate("Dialog", "mm"))
        self.label_4.setText(_translate("Dialog", "Material grade overwrite"))
        self.label_8.setText(_translate("Dialog", "Fu"))
        self.txt_boltFu.setText(_translate("Dialog", "800"))
        self.label_11.setText(_translate("Dialog", "MPa"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Bolt"))
        self.label_16.setText(_translate("Dialog", "Inputs"))
        self.label_17.setText(_translate("Dialog", "Description"))
        self.textBrowser_weldDescription.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Shop weld takes a material safety factor of 1.25</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Field weld takes a material safety factor of 1.5</span></p></body></html>"))
        self.label_22.setText(_translate("Dialog", "Type of weld"))
        self.combo_weldType.setItemText(0, _translate("Dialog", "Shop weld"))
        self.combo_weldType.setItemText(1, _translate("Dialog", "Field weld"))
        self.label_6.setText(_translate("Dialog", "Material grade overwrite"))
        self.label_10.setText(_translate("Dialog", "Fu"))
        self.txt_weldFu.setText(_translate("Dialog", "410"))
        self.label_12.setText(_translate("Dialog", "MPa"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Weld"))
        self.label_38.setText(_translate("Dialog", "Inputs"))
        self.label_39.setText(_translate("Dialog", "Type of edges"))
        self.combo_detailingEdgeType.setItemText(0, _translate("Dialog", "a - Sheared or hand flame cut"))
        self.combo_detailingEdgeType.setItemText(1, _translate("Dialog", "b - Rolled, machine-flame cut, sawn and planed"))
        self.label_29.setText(_translate("Dialog", "Gap between beam & support"))
        self.txt_detailingGap.setText(_translate("Dialog", "10"))
        self.label_36.setText(_translate("Dialog", "mm"))
        self.label_18.setText(_translate("Dialog", "Description"))
        self.textBrowser_detailingDescription.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">1.7 </span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">times the hole diameter in case of [</span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">a - sheared or hand flame cut edges</span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">] and </span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">1.5 </span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">times the hole diameter in case of [</span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">b - Rolled, machine-flame cut, sawn and planed edges</span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">] (IS 800 - Cl. 10.2.4.2)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">This gap should include the tolerance value of 5 mm. So if the assumed clearance is 5 mm, then the gap should be = 10 mm ( = 5 mm {clearance} + 5 mm {tolerance} )</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "Detailing"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", "Design"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_ShearDesignPreferences()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

