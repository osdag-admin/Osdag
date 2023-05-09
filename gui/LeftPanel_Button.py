# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LeftPanel_Button.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LPButton(object):
    def setupUi(self, Form,scale):
        Form.setObjectName("Form")
        Form.resize(scale*300, 30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(scale*300, 30))
        Form.setMaximumSize(QtCore.QSize(16777215, 30))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.LP_Button = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LP_Button.sizePolicy().hasHeightForWidth())
        self.LP_Button.setSizePolicy(sizePolicy)
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(11)
        # font.setBold(True)
        # font.setWeight(75)
        # self.LP_Button.setFont(font)
        self.LP_Button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.LP_Button.setMouseTracking(False)
        self.LP_Button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.LP_Button.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.LP_Button.setToolTip("")
        self.LP_Button.setAutoFillBackground(False)

        self.LP_Button.setAutoDefault(True)
        self.LP_Button.setDefault(False)
        self.LP_Button.setFlat(False)
        self.LP_Button.setObjectName("LP_Button")
        self.gridLayout.addWidget(self.LP_Button, 0, 0, 1, 1)
        QtCore.QMetaObject.connectSlotsByName(Form)
