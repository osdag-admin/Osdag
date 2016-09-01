# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design Preferences Window - v2.9.6.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ShearDesignPreferences(object):
    def setupUi(self, ShearDesignPreferences):
        ShearDesignPreferences.setObjectName(_fromUtf8("ShearDesignPreferences"))
        ShearDesignPreferences.resize(651, 500)
        ShearDesignPreferences.setMinimumSize(QtCore.QSize(651, 500))
        ShearDesignPreferences.setAutoFillBackground(True)
        self.BoltTab = QtGui.QWidget()
        self.BoltTab.setAutoFillBackground(True)
        self.BoltTab.setObjectName(_fromUtf8("BoltTab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.BoltTab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_5 = QtGui.QLabel(self.BoltTab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.BoltTab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_5.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_8 = QtGui.QLabel(self.BoltTab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 5, 1, 1, 1)
        self.lineEdit_boltFu = QtGui.QLineEdit(self.BoltTab)
        self.lineEdit_boltFu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_boltFu.setObjectName(_fromUtf8("lineEdit_boltFu"))
        self.gridLayout_4.addWidget(self.lineEdit_boltFu, 5, 2, 1, 1)
        self.label_11 = QtGui.QLabel(self.BoltTab)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 5, 3, 1, 1)
        self.lbl_hgfg = QtGui.QLabel(self.BoltTab)
        self.lbl_hgfg.setObjectName(_fromUtf8("lbl_hgfg"))
        self.gridLayout_4.addWidget(self.lbl_hgfg, 0, 0, 1, 1)
        self.lineEdit_boltSlipFactor = QtGui.QLineEdit(self.BoltTab)
        self.lineEdit_boltSlipFactor.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_boltSlipFactor.setObjectName(_fromUtf8("lineEdit_boltSlipFactor"))
        self.gridLayout_4.addWidget(self.lineEdit_boltSlipFactor, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.BoltTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox_boltHoleType = QtGui.QComboBox(self.BoltTab)
        self.comboBox_boltHoleType.setFocusPolicy(QtCore.Qt.TabFocus)
        self.comboBox_boltHoleType.setObjectName(_fromUtf8("comboBox_boltHoleType"))
        self.comboBox_boltHoleType.addItem(_fromUtf8(""))
        self.comboBox_boltHoleType.addItem(_fromUtf8(""))
        self.gridLayout_4.addWidget(self.comboBox_boltHoleType, 1, 2, 1, 1)
        self.lineEdit_boltHoleDiaClearance = QtGui.QLineEdit(self.BoltTab)
        self.lineEdit_boltHoleDiaClearance.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_boltHoleDiaClearance.setObjectName(_fromUtf8("lineEdit_boltHoleDiaClearance"))
        self.gridLayout_4.addWidget(self.lineEdit_boltHoleDiaClearance, 2, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.BoltTab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 2, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.BoltTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 2)
        self.label_6 = QtGui.QLabel(self.BoltTab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 4, 1, 1, 1)
        self.lineEdit_boltFy = QtGui.QLineEdit(self.BoltTab)
        self.lineEdit_boltFy.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_boltFy.setObjectName(_fromUtf8("lineEdit_boltFy"))
        self.gridLayout_4.addWidget(self.lineEdit_boltFy, 4, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.BoltTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.BoltTab)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 4, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 2, 4, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.line_2 = QtGui.QFrame(self.BoltTab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.BoltTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.textBrowser_boltDescription = QtGui.QTextBrowser(self.BoltTab)
        self.textBrowser_boltDescription.setObjectName(_fromUtf8("textBrowser_boltDescription"))
        self.gridLayout_2.addWidget(self.textBrowser_boltDescription, 2, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 1, 2, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 241, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_boltdefaults = QtGui.QPushButton(self.BoltTab)
        self.btn_boltdefaults.setObjectName(_fromUtf8("btn_boltdefaults"))
        self.horizontalLayout.addWidget(self.btn_boltdefaults)
        self.btn_boltsave = QtGui.QPushButton(self.BoltTab)
        self.btn_boltsave.setObjectName(_fromUtf8("btn_boltsave"))
        self.horizontalLayout.addWidget(self.btn_boltsave)
        self.btn_boltclose = QtGui.QPushButton(self.BoltTab)
        self.btn_boltclose.setObjectName(_fromUtf8("btn_boltclose"))
        self.horizontalLayout.addWidget(self.btn_boltclose)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_6.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        ShearDesignPreferences.addTab(self.BoltTab, _fromUtf8(""))
        self.WeldTab = QtGui.QWidget()
        self.WeldTab.setAutoFillBackground(True)
        self.WeldTab.setObjectName(_fromUtf8("WeldTab"))
        self.gridLayout_8 = QtGui.QGridLayout(self.WeldTab)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_16 = QtGui.QLabel(self.WeldTab)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout.addWidget(self.label_16)
        self.line_8 = QtGui.QFrame(self.WeldTab)
        self.line_8.setFrameShape(QtGui.QFrame.HLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.verticalLayout.addWidget(self.line_8)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_22 = QtGui.QLabel(self.WeldTab)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.horizontalLayout_5.addWidget(self.label_22)
        self.comboBox_weldType = QtGui.QComboBox(self.WeldTab)
        self.comboBox_weldType.setObjectName(_fromUtf8("comboBox_weldType"))
        self.comboBox_weldType.addItem(_fromUtf8(""))
        self.comboBox_weldType.addItem(_fromUtf8(""))
        self.horizontalLayout_5.addWidget(self.comboBox_weldType)
        spacerItem4 = QtGui.QSpacerItem(238, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout_8.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.textBrowser_weldDescription = QtGui.QTextBrowser(self.WeldTab)
        self.textBrowser_weldDescription.setObjectName(_fromUtf8("textBrowser_weldDescription"))
        self.gridLayout_7.addWidget(self.textBrowser_weldDescription, 2, 0, 1, 1)
        self.line_4 = QtGui.QFrame(self.WeldTab)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout_7.addWidget(self.line_4, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.WeldTab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_7.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 1, 2, 1)
        spacerItem5 = QtGui.QSpacerItem(20, 364, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem5, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.btn_welddefaults = QtGui.QPushButton(self.WeldTab)
        self.btn_welddefaults.setObjectName(_fromUtf8("btn_welddefaults"))
        self.horizontalLayout_4.addWidget(self.btn_welddefaults)
        self.btn_weldsave = QtGui.QPushButton(self.WeldTab)
        self.btn_weldsave.setObjectName(_fromUtf8("btn_weldsave"))
        self.horizontalLayout_4.addWidget(self.btn_weldsave)
        self.btn_weldclose = QtGui.QPushButton(self.WeldTab)
        self.btn_weldclose.setObjectName(_fromUtf8("btn_weldclose"))
        self.horizontalLayout_4.addWidget(self.btn_weldclose)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.gridLayout_8.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)
        ShearDesignPreferences.addTab(self.WeldTab, _fromUtf8(""))
        self.DetailingTab = QtGui.QWidget()
        self.DetailingTab.setAutoFillBackground(True)
        self.DetailingTab.setObjectName(_fromUtf8("DetailingTab"))
        self.gridLayout_16 = QtGui.QGridLayout(self.DetailingTab)
        self.gridLayout_16.setObjectName(_fromUtf8("gridLayout_16"))
        self.label_38 = QtGui.QLabel(self.DetailingTab)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.gridLayout_16.addWidget(self.label_38, 0, 0, 1, 1)
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.textBrowser_detailingDescription = QtGui.QTextBrowser(self.DetailingTab)
        self.textBrowser_detailingDescription.setObjectName(_fromUtf8("textBrowser_detailingDescription"))
        self.gridLayout_9.addWidget(self.textBrowser_detailingDescription, 2, 1, 1, 1)
        self.line_5 = QtGui.QFrame(self.DetailingTab)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.gridLayout_9.addWidget(self.line_5, 1, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.DetailingTab)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_9.addWidget(self.label_12, 0, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_9, 0, 1, 4, 1)
        self.line_11 = QtGui.QFrame(self.DetailingTab)
        self.line_11.setFrameShape(QtGui.QFrame.HLine)
        self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_11.setObjectName(_fromUtf8("line_11"))
        self.gridLayout_16.addWidget(self.line_11, 1, 0, 1, 1)
        self.gridLayout_15 = QtGui.QGridLayout()
        self.gridLayout_15.setObjectName(_fromUtf8("gridLayout_15"))
        self.lineEdit_detailingGap = QtGui.QLineEdit(self.DetailingTab)
        self.lineEdit_detailingGap.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_detailingGap.setObjectName(_fromUtf8("lineEdit_detailingGap"))
        self.gridLayout_15.addWidget(self.lineEdit_detailingGap, 1, 1, 1, 1)
        self.label_40 = QtGui.QLabel(self.DetailingTab)
        self.label_40.setText(_fromUtf8(""))
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.gridLayout_15.addWidget(self.label_40, 0, 2, 1, 1)
        self.label_36 = QtGui.QLabel(self.DetailingTab)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.gridLayout_15.addWidget(self.label_36, 1, 2, 1, 1)
        self.label_29 = QtGui.QLabel(self.DetailingTab)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.gridLayout_15.addWidget(self.label_29, 1, 0, 1, 1)
        self.label_39 = QtGui.QLabel(self.DetailingTab)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.gridLayout_15.addWidget(self.label_39, 0, 0, 1, 1)
        self.comboBox_detailingEdgeType = QtGui.QComboBox(self.DetailingTab)
        self.comboBox_detailingEdgeType.setObjectName(_fromUtf8("comboBox_detailingEdgeType"))
        self.comboBox_detailingEdgeType.addItem(_fromUtf8(""))
        self.comboBox_detailingEdgeType.addItem(_fromUtf8(""))
        self.gridLayout_15.addWidget(self.comboBox_detailingEdgeType, 0, 1, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_15.addItem(spacerItem8, 1, 3, 1, 1)
        self.gridLayout_15.setColumnMinimumWidth(1, 100)
        self.gridLayout_15.setColumnStretch(1, 12)
        self.gridLayout_16.addLayout(self.gridLayout_15, 2, 0, 1, 1)
        spacerItem9 = QtGui.QSpacerItem(20, 340, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_16.addItem(spacerItem9, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem10 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.btn_detailingdefaults = QtGui.QPushButton(self.DetailingTab)
        self.btn_detailingdefaults.setObjectName(_fromUtf8("btn_detailingdefaults"))
        self.horizontalLayout_2.addWidget(self.btn_detailingdefaults)
        self.btn_detailingsave = QtGui.QPushButton(self.DetailingTab)
        self.btn_detailingsave.setObjectName(_fromUtf8("btn_detailingsave"))
        self.horizontalLayout_2.addWidget(self.btn_detailingsave)
        self.btn_detailingclose = QtGui.QPushButton(self.DetailingTab)
        self.btn_detailingclose.setObjectName(_fromUtf8("btn_detailingclose"))
        self.horizontalLayout_2.addWidget(self.btn_detailingclose)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem11)
        self.gridLayout_16.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)
        self.line_11.raise_()
        self.label_38.raise_()
        ShearDesignPreferences.addTab(self.DetailingTab, _fromUtf8(""))
        self.DesignTab = QtGui.QWidget()
        self.DesignTab.setEnabled(False)
        self.DesignTab.setAutoFillBackground(True)
        self.DesignTab.setObjectName(_fromUtf8("DesignTab"))
        self.gridLayout_17 = QtGui.QGridLayout(self.DesignTab)
        self.gridLayout_17.setObjectName(_fromUtf8("gridLayout_17"))
        self.label_34 = QtGui.QLabel(self.DesignTab)
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.gridLayout_17.addWidget(self.label_34, 0, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_35 = QtGui.QLabel(self.DesignTab)
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.gridLayout_3.addWidget(self.label_35, 0, 0, 1, 1)
        self.line_3 = QtGui.QFrame(self.DesignTab)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_3.addWidget(self.line_3, 1, 0, 1, 1)
        self.textBrowser_designDescription = QtGui.QTextBrowser(self.DesignTab)
        self.textBrowser_designDescription.setObjectName(_fromUtf8("textBrowser_designDescription"))
        self.gridLayout_3.addWidget(self.textBrowser_designDescription, 2, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_3, 0, 2, 5, 1)
        self.line_9 = QtGui.QFrame(self.DesignTab)
        self.line_9.setFrameShape(QtGui.QFrame.HLine)
        self.line_9.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_9.setObjectName(_fromUtf8("line_9"))
        self.gridLayout_17.addWidget(self.line_9, 1, 0, 1, 2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem12 = QtGui.QSpacerItem(53, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem12, 0, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout, 3, 0, 1, 2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem13 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem13)
        self.btn_designdefaults = QtGui.QPushButton(self.DesignTab)
        self.btn_designdefaults.setObjectName(_fromUtf8("btn_designdefaults"))
        self.horizontalLayout_3.addWidget(self.btn_designdefaults)
        self.btn_designsave = QtGui.QPushButton(self.DesignTab)
        self.btn_designsave.setObjectName(_fromUtf8("btn_designsave"))
        self.horizontalLayout_3.addWidget(self.btn_designsave)
        self.btn_designclose = QtGui.QPushButton(self.DesignTab)
        self.btn_designclose.setObjectName(_fromUtf8("btn_designclose"))
        self.horizontalLayout_3.addWidget(self.btn_designclose)
        spacerItem14 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem14)
        self.gridLayout_17.addLayout(self.horizontalLayout_3, 5, 0, 1, 3)
        spacerItem15 = QtGui.QSpacerItem(328, 363, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_17.addItem(spacerItem15, 2, 0, 1, 2)
        ShearDesignPreferences.addTab(self.DesignTab, _fromUtf8(""))

        self.retranslateUi(ShearDesignPreferences)
        ShearDesignPreferences.setCurrentIndex(0)
        QtCore.QObject.connect(self.btn_boltclose, QtCore.SIGNAL(_fromUtf8("clicked()")), ShearDesignPreferences.close)
        QtCore.QObject.connect(self.btn_detailingclose, QtCore.SIGNAL(_fromUtf8("clicked()")), ShearDesignPreferences.close)
        QtCore.QObject.connect(self.btn_weldclose, QtCore.SIGNAL(_fromUtf8("clicked()")), ShearDesignPreferences.close)
        QtCore.QObject.connect(self.btn_designclose, QtCore.SIGNAL(_fromUtf8("clicked()")), ShearDesignPreferences.close)
        QtCore.QObject.connect(self.lineEdit_boltSlipFactor, QtCore.SIGNAL(_fromUtf8("editingFinished()")), self.textBrowser_boltDescription.hide)
        QtCore.QMetaObject.connectSlotsByName(ShearDesignPreferences)
        ShearDesignPreferences.setTabOrder(self.lineEdit_boltSlipFactor, self.comboBox_boltHoleType)
        ShearDesignPreferences.setTabOrder(self.comboBox_boltHoleType, self.lineEdit_boltHoleDiaClearance)
        ShearDesignPreferences.setTabOrder(self.lineEdit_boltHoleDiaClearance, self.lineEdit_boltFy)
        ShearDesignPreferences.setTabOrder(self.lineEdit_boltFy, self.lineEdit_boltFu)
        ShearDesignPreferences.setTabOrder(self.lineEdit_boltFu, self.btn_boltdefaults)
        ShearDesignPreferences.setTabOrder(self.btn_boltdefaults, self.btn_boltsave)
        ShearDesignPreferences.setTabOrder(self.btn_boltsave, self.btn_boltclose)
        ShearDesignPreferences.setTabOrder(self.btn_boltclose, self.comboBox_weldType)
        ShearDesignPreferences.setTabOrder(self.comboBox_weldType, self.btn_welddefaults)
        ShearDesignPreferences.setTabOrder(self.btn_welddefaults, self.btn_weldsave)
        ShearDesignPreferences.setTabOrder(self.btn_weldsave, self.btn_weldclose)
        ShearDesignPreferences.setTabOrder(self.btn_weldclose, self.comboBox_detailingEdgeType)
        ShearDesignPreferences.setTabOrder(self.comboBox_detailingEdgeType, self.lineEdit_detailingGap)
        ShearDesignPreferences.setTabOrder(self.lineEdit_detailingGap, self.btn_detailingdefaults)
        ShearDesignPreferences.setTabOrder(self.btn_detailingdefaults, self.btn_detailingsave)
        ShearDesignPreferences.setTabOrder(self.btn_detailingsave, self.btn_detailingclose)
        ShearDesignPreferences.setTabOrder(self.btn_detailingclose, self.btn_designdefaults)
        ShearDesignPreferences.setTabOrder(self.btn_designdefaults, self.btn_designsave)
        ShearDesignPreferences.setTabOrder(self.btn_designsave, self.btn_designclose)
        ShearDesignPreferences.setTabOrder(self.btn_designclose, self.textBrowser_boltDescription)
        ShearDesignPreferences.setTabOrder(self.textBrowser_boltDescription, self.textBrowser_weldDescription)
        ShearDesignPreferences.setTabOrder(self.textBrowser_weldDescription, self.textBrowser_detailingDescription)
        ShearDesignPreferences.setTabOrder(self.textBrowser_detailingDescription, self.textBrowser_designDescription)

    def retranslateUi(self, ShearDesignPreferences):
        ShearDesignPreferences.setWindowTitle(_translate("ShearDesignPreferences", "Shear Connections - Design Preferences", None))
        self.label_5.setText(_translate("ShearDesignPreferences", "Inputs", None))
        self.label_8.setText(_translate("ShearDesignPreferences", "Fu", None))
        self.lineEdit_boltFu.setText(_translate("ShearDesignPreferences", "800", None))
        self.label_11.setText(_translate("ShearDesignPreferences", "MPa", None))
        self.lbl_hgfg.setText(_translate("ShearDesignPreferences", "HSFG - slip factor", None))
        self.lineEdit_boltSlipFactor.setText(_translate("ShearDesignPreferences", "0.2", None))
        self.label.setText(_translate("ShearDesignPreferences", "Bolt hole type", None))
        self.comboBox_boltHoleType.setItemText(0, _translate("ShearDesignPreferences", "Standard", None))
        self.comboBox_boltHoleType.setItemText(1, _translate("ShearDesignPreferences", "Over-sized", None))
        self.lineEdit_boltHoleDiaClearance.setText(_translate("ShearDesignPreferences", "2", None))
        self.label_9.setText(_translate("ShearDesignPreferences", "mm", None))
        self.label_2.setText(_translate("ShearDesignPreferences", "Bolt hole clearance", None))
        self.label_6.setText(_translate("ShearDesignPreferences", "Fy", None))
        self.lineEdit_boltFy.setText(_translate("ShearDesignPreferences", "640", None))
        self.label_4.setText(_translate("ShearDesignPreferences", "Material grade overwrite", None))
        self.label_10.setText(_translate("ShearDesignPreferences", "MPa", None))
        self.label_3.setText(_translate("ShearDesignPreferences", "Description", None))
        self.textBrowser_boltDescription.setHtml(_translate("ShearDesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">IS 4000: 1992 - Annex C recommended slip factors:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<table border=\"0\" style=\" border-color:#a3a3a3; border-style:solid; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"0\" cellpadding=\"0\">\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Treatment of surface</span><span style=\" font-size:8pt;\">                 </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Slip factor </span><span style=\" font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Surface not treated</span><span style=\" font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.2</span><span style=\" font-size:8pt;\"> </span></p></td></tr></table>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">Surface blasted with shot or grit </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:10pt;\"><br /></p>\n"
"<table border=\"0\" style=\" border-color:#a3a3a3; border-style:solid; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"0\" cellpadding=\"0\">\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">with any loose rust removed, no pitting</span><span style=\" font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.5</span><span style=\" font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and hot-dip galvanized</span><span style=\" font-size:8pt;\">                 </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.1</span><span style=\" font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and spray-metallized with zinc (thickness 50-70 micro-m</span><span style=\" font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.25</span><span style=\" font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and painted with ethyl-zinc silicate coat (thickness 30-80  micro-m)</span><span style=\" font-size:8pt;\"> </span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.30</span><span style=\" font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and painted with alkali-zinc silicate coat (thickness 60-80  micro-m)</span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.30</span><span style=\" font-size:8pt;\"> </span></p></td></tr>\n"
"<tr>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">and spray metallized with aluminium (thickness &gt; 50  micro-m)</span></p></td>\n"
"<td style=\" vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">0.5</span><span style=\" font-size:8pt;\"> </span></p></td></tr></table></body></html>", None))
        self.btn_boltdefaults.setText(_translate("ShearDesignPreferences", "Defaults", None))
        self.btn_boltsave.setText(_translate("ShearDesignPreferences", "Save", None))
        self.btn_boltclose.setText(_translate("ShearDesignPreferences", "Close", None))
        ShearDesignPreferences.setTabText(ShearDesignPreferences.indexOf(self.BoltTab), _translate("ShearDesignPreferences", "Bolt", None))
        self.label_16.setText(_translate("ShearDesignPreferences", "Inputs", None))
        self.label_22.setText(_translate("ShearDesignPreferences", "Type of weld", None))
        self.comboBox_weldType.setItemText(0, _translate("ShearDesignPreferences", "Shop weld", None))
        self.comboBox_weldType.setItemText(1, _translate("ShearDesignPreferences", "Field weld", None))
        self.textBrowser_weldDescription.setHtml(_translate("ShearDesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Shop weld takes a material safety factor of 1.25</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Field weld takes a material safety factor of 1.5</span></p></body></html>", None))
        self.label_7.setText(_translate("ShearDesignPreferences", "Description", None))
        self.btn_welddefaults.setText(_translate("ShearDesignPreferences", "Defaults", None))
        self.btn_weldsave.setText(_translate("ShearDesignPreferences", "Save", None))
        self.btn_weldclose.setText(_translate("ShearDesignPreferences", "Close", None))
        ShearDesignPreferences.setTabText(ShearDesignPreferences.indexOf(self.WeldTab), _translate("ShearDesignPreferences", "Weld", None))
        self.label_38.setText(_translate("ShearDesignPreferences", "Inputs", None))
        self.textBrowser_detailingDescription.setHtml(_translate("ShearDesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">The minimum edge and end distances from the centre of any hole to the nearest edge of a plate shall not be less than </span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">1.7 </span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">times the hole diameter in case of [</span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">a - sheared or hand flame cut edges</span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">] and </span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">1.5 </span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">times the hole diameter in case of [</span><span style=\" font-family:\'Calibri\'; font-size:10pt; font-weight:600; vertical-align:middle;\">b - Rolled, machine-flame cut, sawn and planed edges</span><span style=\" font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\">] (IS 800 - Cl. 10.2.4.2)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:10pt; vertical-align:middle;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:10pt;\">This gap should include the tolerance value of 5 mm. So if the assumed clearance is 5 mm, then the gap should be = 10 mm ( = 5 mm {clearance} + 5 mm {tolerance} )</span></p></body></html>", None))
        self.label_12.setText(_translate("ShearDesignPreferences", "Description", None))
        self.lineEdit_detailingGap.setText(_translate("ShearDesignPreferences", "10", None))
        self.label_36.setText(_translate("ShearDesignPreferences", "mm", None))
        self.label_29.setText(_translate("ShearDesignPreferences", "Gap between beam & support", None))
        self.label_39.setText(_translate("ShearDesignPreferences", "Type of edges", None))
        self.comboBox_detailingEdgeType.setItemText(0, _translate("ShearDesignPreferences", "a - Sheared or hand flame cut", None))
        self.comboBox_detailingEdgeType.setItemText(1, _translate("ShearDesignPreferences", "b - Rolled, machine-flame cut, sawn and planed", None))
        self.btn_detailingdefaults.setText(_translate("ShearDesignPreferences", "Defaults", None))
        self.btn_detailingsave.setText(_translate("ShearDesignPreferences", "Save", None))
        self.btn_detailingclose.setText(_translate("ShearDesignPreferences", "Close", None))
        ShearDesignPreferences.setTabText(ShearDesignPreferences.indexOf(self.DetailingTab), _translate("ShearDesignPreferences", "Detailing", None))
        self.label_34.setText(_translate("ShearDesignPreferences", "Inputs", None))
        self.label_35.setText(_translate("ShearDesignPreferences", "Description", None))
        self.textBrowser_designDescription.setHtml(_translate("ShearDesignPreferences", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.btn_designdefaults.setText(_translate("ShearDesignPreferences", "Defaults", None))
        self.btn_designsave.setText(_translate("ShearDesignPreferences", "Save", None))
        self.btn_designclose.setText(_translate("ShearDesignPreferences", "Close", None))
        ShearDesignPreferences.setTabText(ShearDesignPreferences.indexOf(self.DesignTab), _translate("ShearDesignPreferences", "Design", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ShearDesignPreferences = QtGui.QTabWidget()
    ui = Ui_ShearDesignPreferences()
    ui.setupUi(ShearDesignPreferences)
    ShearDesignPreferences.show()
    sys.exit(app.exec_())

