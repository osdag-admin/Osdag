# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_OsdagSectionModeller.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import math
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Common import *
from gui.ui_section_parameters import Ui_SectionParameters
from gui.ui_SectionModeller_SummaryPopUp import Ui_Dialog1 as SummaryDialog
from SectionModeller_Latex import CreateLatex


class Ui_OsdagSectionModeller(object):
    def setupUi(self,Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(900, 900))
        Dialog.setMaximumSize(QtCore.QSize(906, 900))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.design_section = QtWidgets.QFrame(Dialog)
        self.design_section.setStyleSheet("QFrame{\n"
"background:#ffffff;\n"
"}")
        self.design_section.setFrameShape(QtWidgets.QFrame.Box)
        self.design_section.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.design_section.setLineWidth(3)
        self.design_section.setObjectName("design_section")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.design_section)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label = QtWidgets.QLabel(self.design_section)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setUnderline(False)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
"background:rgb(135, 135, 135);\n"
"color:#ffffff;\n"
"}")
        self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_17.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(75, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_17.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.design_section)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.section_type_combobox = QtWidgets.QComboBox(self.design_section)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.section_type_combobox.setFont(font)
        self.section_type_combobox.setObjectName("section_type_combobox")
        self.section_type_combobox.addItem("")
        self.section_type_combobox.addItem("")
        self.section_type_combobox.addItem("")
        self.section_type_combobox.addItem("")
        self.section_type_combobox.addItem("")
        self.section_type_combobox.addItem("")
        self.horizontalLayout_2.addWidget(self.section_type_combobox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed) 
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.design_section)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.section_template_combobox = QtWidgets.QComboBox(self.design_section)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.section_template_combobox.setFont(font)
        self.section_template_combobox.setObjectName("section_template_combobox")
        self.section_template_combobox.addItem("")
        self.horizontalLayout_3.addWidget(self.section_template_combobox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.design_section)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.section_designation_lineEdit = QtWidgets.QLineEdit(self.design_section)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.section_designation_lineEdit.setFont(font)
        self.section_designation_lineEdit.setInputMask("")
        self.section_designation_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.section_designation_lineEdit.setObjectName("section_designation_lineEdit")
        self.verticalLayout_3.addWidget(self.section_designation_lineEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_17.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_17.addItem(spacerItem3)
        self.horizontalLayout.addWidget(self.design_section)
        self.OCCFrame = QtWidgets.QFrame(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.OCCFrame.setFont(font)
        self.OCCFrame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.OCCFrame.setStyleSheet("QFrame{\n"
"background:#ffffff;\n"
"}")
        self.OCCFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.OCCFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.OCCFrame.setLineWidth(3)
        self.OCCFrame.setObjectName("OCCFrame")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OCCFrame.sizePolicy().hasHeightForWidth())
        self.OCCFrame.setSizePolicy(sizePolicy)
        self.OCCFrame.setMinimumSize(QtCore.QSize(500, 400))
        self.OCCFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout.addWidget(self.OCCFrame)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.section_properties = QtWidgets.QFrame(Dialog)
        self.section_properties.setStyleSheet("QFrame{\n"
"background:#ffffff;\n"
"}")
        self.section_properties.setFrameShape(QtWidgets.QFrame.Box)
        self.section_properties.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.section_properties.setLineWidth(3)
        self.section_properties.setObjectName("section_properties")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.section_properties)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(10)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_5 = QtWidgets.QLabel(self.section_properties)
        self.label_5.setMinimumSize(QtCore.QSize(0, 40))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setUnderline(False)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("QLabel{\n"
"background:rgb(135, 135, 135);\n"
"color:#ffffff;\n"
"}")
        self.label_5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_16.addWidget(self.label_5)
        spacerItem4 = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding) 
        self.verticalLayout_16.addItem(spacerItem4)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_15.setSpacing(15)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.Area = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Area.setFont(font)
        self.Area.setObjectName("Area")
        self.horizontalLayout_9.addWidget(self.Area)
        spacerItem5 = QtWidgets.QSpacerItem(170, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.Area_text = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Area_text.setFont(font)
        self.Area_text.setInputMask("")
        self.Area_text.setAlignment(QtCore.Qt.AlignCenter)
        self.Area_text.setObjectName("Area_text")
        self.horizontalLayout_9.addWidget(self.Area_text)
        self.verticalLayout_14.addLayout(self.horizontalLayout_9)
        self.line_6 = QtWidgets.QFrame(self.section_properties)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_14.addWidget(self.line_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.RG = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.RG.setFont(font)
        self.RG.setObjectName("RG")
        self.horizontalLayout_7.addWidget(self.RG)
        spacerItem6 = QtWidgets.QSpacerItem(24, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setSpacing(22)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.RG_label_1 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.RG_label_1.setFont(font)
        self.RG_label_1.setObjectName("RG_label_1")
        self.verticalLayout_7.addWidget(self.RG_label_1)
        self.RG_label_2 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.RG_label_2.setFont(font)
        self.RG_label_2.setObjectName("RG_label_2")
        self.verticalLayout_7.addWidget(self.RG_label_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RG_text_1 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.RG_text_1.setFont(font)
        self.RG_text_1.setInputMask("")
        self.RG_text_1.setAlignment(QtCore.Qt.AlignCenter)
        self.RG_text_1.setObjectName("RG_text_1")
        self.verticalLayout_4.addWidget(self.RG_text_1)
        self.RG_text_2 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.RG_text_2.setFont(font)
        self.RG_text_2.setInputMask("")
        self.RG_text_2.setAlignment(QtCore.Qt.AlignCenter)
        self.RG_text_2.setObjectName("RG_text_2")
        self.verticalLayout_4.addWidget(self.RG_text_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_4)
        self.verticalLayout_14.addLayout(self.horizontalLayout_7)
        self.line_5 = QtWidgets.QFrame(self.section_properties)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_14.addWidget(self.line_5)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.ESM = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.ESM.setFont(font)
        self.ESM.setObjectName("ESM")
        self.horizontalLayout_8.addWidget(self.ESM)
        spacerItem7 = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ESM_label_1 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ESM_label_1.setFont(font)
        self.ESM_label_1.setObjectName("ESM_label_1")
        self.verticalLayout_8.addWidget(self.ESM_label_1)
        self.ESM_label_2 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ESM_label_2.setFont(font)
        self.ESM_label_2.setObjectName("ESM_label_2")
        self.verticalLayout_8.addWidget(self.ESM_label_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ESM_text_1 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ESM_text_1.setFont(font)
        self.ESM_text_1.setInputMask("")
        self.ESM_text_1.setAlignment(QtCore.Qt.AlignCenter)
        self.ESM_text_1.setObjectName("ESM_text_1")
        self.verticalLayout_5.addWidget(self.ESM_text_1)
        self.ESM_text_2 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ESM_text_2.setFont(font)
        self.ESM_text_2.setInputMask("")
        self.ESM_text_2.setAlignment(QtCore.Qt.AlignCenter)
        self.ESM_text_2.setObjectName("ESM_text_2")
        self.verticalLayout_5.addWidget(self.ESM_text_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_5)
        self.verticalLayout_14.addLayout(self.horizontalLayout_8)
        self.Centroid_box = QtWidgets.QFrame(self.section_properties)
        self.Centroid_box.setStyleSheet(
                '''
                QFrame{
                        border-style:none;
                }
                '''
        )
        self.Centroid_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Centroid_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Centroid_box.setObjectName("Centroid_box")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.Centroid_box)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.line_4 = QtWidgets.QFrame(self.Centroid_box)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_18.addWidget(self.line_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.C = QtWidgets.QLabel(self.Centroid_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.C.setFont(font)
        self.C.setObjectName("C")
        self.horizontalLayout_10.addWidget(self.C)
        spacerItem8 = QtWidgets.QSpacerItem(108, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(22)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setSpacing(30)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(5)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.C_label_1 = QtWidgets.QLabel(self.Centroid_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.C_label_1.setFont(font)
        self.C_label_1.setObjectName("C_label_1")
        self.verticalLayout_9.addWidget(self.C_label_1)
        self.C_label_2 = QtWidgets.QLabel(self.Centroid_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.C_label_2.setFont(font)
        self.C_label_2.setObjectName("C_label_2")
        self.verticalLayout_9.addWidget(self.C_label_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_9)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.C_text_1 = QtWidgets.QLineEdit(self.Centroid_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.C_text_1.setFont(font)
        self.C_text_1.setInputMask("")
        self.C_text_1.setAlignment(QtCore.Qt.AlignCenter)
        self.C_text_1.setObjectName("C_text_1")
        self.verticalLayout_6.addWidget(self.C_text_1)
        self.C_text_2 = QtWidgets.QLineEdit(self.Centroid_box)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.C_text_2.setFont(font)
        self.C_text_2.setInputMask("")
        self.C_text_2.setAlignment(QtCore.Qt.AlignCenter)
        self.C_text_2.setObjectName("C_text_2")
        self.verticalLayout_6.addWidget(self.C_text_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_6)
        self.verticalLayout_18.addLayout(self.horizontalLayout_10)
        self.verticalLayout_14.addWidget(self.Centroid_box)
        self.horizontalLayout_15.addLayout(self.verticalLayout_14)
        self.line = QtWidgets.QFrame(self.section_properties)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_15.addWidget(self.line)
        self.line_2 = QtWidgets.QFrame(self.section_properties)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_15.addWidget(self.line_2)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setSpacing(7)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.MI = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.MI.setFont(font)
        self.MI.setObjectName("MI")
        self.horizontalLayout_14.addWidget(self.MI)
        spacerItem9 = QtWidgets.QSpacerItem(47, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem9)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.MI_label_1 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_label_1.setFont(font)
        self.MI_label_1.setObjectName("MI_label_1")
        self.verticalLayout_12.addWidget(self.MI_label_1)
        self.MI_label_2 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_label_2.setFont(font)
        self.MI_label_2.setObjectName("MI_label_2")
        self.verticalLayout_12.addWidget(self.MI_label_2)
        self.MI_label_3 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_label_3.setFont(font)
        self.MI_label_3.setObjectName("MI_label_3")
        self.verticalLayout_12.addWidget(self.MI_label_3)
        self.MI_label_4 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_label_4.setFont(font)
        self.MI_label_4.setObjectName("MI_label_4")
        self.verticalLayout_12.addWidget(self.MI_label_4)
        self.MI_label_5 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_label_5.setFont(font)
        self.MI_label_5.setObjectName("MI_label_5")
        self.verticalLayout_12.addWidget(self.MI_label_5)
        self.MI_label_6 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_label_6.setFont(font)
        self.MI_label_6.setObjectName("MI_label_6")
        self.verticalLayout_12.addWidget(self.MI_label_6)
        self.horizontalLayout_13.addLayout(self.verticalLayout_12)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.MI_text_1 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_text_1.setFont(font)
        self.MI_text_1.setInputMask("")
        self.MI_text_1.setAlignment(QtCore.Qt.AlignCenter)
        self.MI_text_1.setObjectName("MI_text_1")
        self.verticalLayout_13.addWidget(self.MI_text_1)
        self.MI_text_2 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_text_2.setFont(font)
        self.MI_text_2.setInputMask("")
        self.MI_text_2.setAlignment(QtCore.Qt.AlignCenter)
        self.MI_text_2.setObjectName("MI_text_2")
        self.verticalLayout_13.addWidget(self.MI_text_2)
        self.MI_text_3 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_text_3.setFont(font)
        self.MI_text_3.setInputMask("")
        self.MI_text_3.setAlignment(QtCore.Qt.AlignCenter)
        self.MI_text_3.setObjectName("MI_text_3")
        self.verticalLayout_13.addWidget(self.MI_text_3)
        self.MI_text_4 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_text_4.setFont(font)
        self.MI_text_4.setInputMask("")
        self.MI_text_4.setAlignment(QtCore.Qt.AlignCenter)
        self.MI_text_4.setObjectName("MI_text_4")
        self.verticalLayout_13.addWidget(self.MI_text_4)
        self.MI_text_5 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_text_5.setFont(font)
        self.MI_text_5.setInputMask("")
        self.MI_text_5.setAlignment(QtCore.Qt.AlignCenter)
        self.MI_text_5.setObjectName("MI_text_5")
        self.verticalLayout_13.addWidget(self.MI_text_5)
        self.MI_text_6 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MI_text_6.setFont(font)
        self.MI_text_6.setInputMask("")
        self.MI_text_6.setAlignment(QtCore.Qt.AlignCenter)
        self.MI_text_6.setObjectName("MI_text_6")
        self.verticalLayout_13.addWidget(self.MI_text_6)
        self.horizontalLayout_13.addLayout(self.verticalLayout_13)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_13)
        self.verticalLayout_15.addLayout(self.horizontalLayout_14)
        self.line_3 = QtWidgets.QFrame(self.section_properties)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_15.addWidget(self.line_3)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.PSM = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.PSM.setFont(font)
        self.PSM.setObjectName("PSM")
        self.horizontalLayout_12.addWidget(self.PSM)
        spacerItem10 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.PSM_label_1 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PSM_label_1.setFont(font)
        self.PSM_label_1.setObjectName("PSM_label_1")
        self.verticalLayout_10.addWidget(self.PSM_label_1)
        self.PSM_label_2 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PSM_label_2.setFont(font)
        self.PSM_label_2.setObjectName("PSM_label_2")
        self.verticalLayout_10.addWidget(self.PSM_label_2)
        self.PSM_label_3 = QtWidgets.QLabel(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PSM_label_3.setFont(font)
        self.PSM_label_3.setObjectName("PSM_label_3")
        self.verticalLayout_10.addWidget(self.PSM_label_3)
        self.horizontalLayout_11.addLayout(self.verticalLayout_10)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.PSM_text_1 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PSM_text_1.setFont(font)
        self.PSM_text_1.setInputMask("")
        self.PSM_text_1.setAlignment(QtCore.Qt.AlignCenter)
        self.PSM_text_1.setObjectName("PSM_text_1")
        self.verticalLayout_11.addWidget(self.PSM_text_1)
        self.PSM_text_2 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PSM_text_2.setFont(font)
        self.PSM_text_2.setInputMask("")
        self.PSM_text_2.setAlignment(QtCore.Qt.AlignCenter)
        self.PSM_text_2.setObjectName("PSM_text_2")
        self.verticalLayout_11.addWidget(self.PSM_text_2)
        self.PSM_text_3 = QtWidgets.QLineEdit(self.section_properties)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.PSM_text_3.setFont(font)
        self.PSM_text_3.setInputMask("")
        self.PSM_text_3.setAlignment(QtCore.Qt.AlignCenter)
        self.PSM_text_3.setObjectName("PSM_text_3")
        self.verticalLayout_11.addWidget(self.PSM_text_3)
        self.horizontalLayout_11.addLayout(self.verticalLayout_11)
        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout_15.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_15.addLayout(self.verticalLayout_15)
        self.verticalLayout_16.addLayout(self.horizontalLayout_15)
        spacerItem11 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout_16.addItem(spacerItem11)
        self.verticalLayout.addWidget(self.section_properties)
        spacerItem12 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem12)
        self.HLayout_Buttons = QtWidgets.QHBoxLayout()
        self.HLayout_Buttons.setObjectName("HLayout_Buttons")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HLayout_Buttons.addItem(spacerItem13)
        self.saveBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.saveBtn.setFont(font)
        self.saveBtn.setObjectName("saveBtn")
        self.HLayout_Buttons.addWidget(self.saveBtn)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.HLayout_Buttons.addItem(spacerItem14)
        self.exportBtn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.exportBtn.setFont(font)
        self.exportBtn.setObjectName("exportBtn")
        self.HLayout_Buttons.addWidget(self.exportBtn)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HLayout_Buttons.addItem(spacerItem15)
        self.verticalLayout.addLayout(self.HLayout_Buttons)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.section_type_combobox.currentIndexChanged.connect(self.type_change)
        self.section_template_combobox.activated[int].connect(self.template_change)
        self.section_designation_lineEdit.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[a-zA-Z0-9@_]*"), self.section_designation_lineEdit
        ))
        self.disable_usability(True)
        self.exportBtn.clicked.connect(self.export_to_pdf)
        display,_=self.init_display()
    
    def get_section_properties(self):
            '''
            Method to get the values and names of the Section properties,
            for the currently selected Type and Template,
            in a dictionary
            '''
            Labels=[]
            for child in self.section_properties.findChildren(QtWidgets.QLabel):
                    if(child.isVisible()):
                        Labels.append([child.objectName(),child.text().strip()[:-1]])
            Properties={}
            i=2
            Properties['Area']=self.Area_text.text()
            while(i<len(Labels)):
                Main=Labels[i][0]
                Properties[Labels[i][1]]={}
                for j in range(i+1,len(Labels)):
                        if Main in Labels[j][0]:
                                exec(f"Properties[Labels[i][1]][Labels[j][1]]=self.{Labels[j][0].replace('label','text')}.text()")
                        else:
                                i=j-1
                                break
                i+=1
                if(Labels[i][0][-1].isdigit()):
                        break
            return(Properties)



    def init_display(self):
            from OCC.Display.backend import load_backend, get_qt_modules

            global display
            from OCC.Display.qtDisplay import qtViewer3d
            self.OCCWindow = qtViewer3d(self.OCCFrame)
            self.OCCWindow.InitDriver()
            display = self.OCCWindow._display
            display.set_bg_gradient_color([23, 1, 32], [23, 1, 32])
            display.display_triedron()
            display.View.SetProj(1, 1, 1)
            layout=QtWidgets.QVBoxLayout()
            layout.addWidget(self.OCCWindow)
            layout.setContentsMargins(0, 0, 0, 0)
            self.OCCFrame.setLayout(layout)
            def start_display():
                    self.OCCWindow.raise_()
            return display, start_display       

    def export_to_pdf(self):
            '''
            Method to create and convert information from section modeller into Latex formatted PDF
            '''

            self.summary_dialog=SummaryDialog()
            dialog=QtWidgets.QDialog()
            self.summary_dialog.setupUi(dialog)
            dialog.exec()
            try:
                input_summary=self.summary_dialog.input_summary
                input_summary['Design Section']={
                        'Section Designation':str(self.section_designation_lineEdit.text()),
                        'Section Type':str(self.section_type_combobox.currentText()),
                        'Section Template':str(self.section_template_combobox.currentText()),
                        'Section Parameters':self.Parameters,
                }
                input_summary['Section Properties']=self.get_section_properties()
                rel_path = str(sys.path[0])
                rel_path = rel_path.replace("\\", "/")
                Disp_3D_image = "/ResourceFiles/images/3d.png"
                latex=CreateLatex()
                latex.save_latex(input_summary,input_summary['filename'],rel_path,Disp_3D_image)
            except KeyError:
                pass

    def disable_usability(self,toggle):
            '''
            Method to Disable/Enable Section Properties and Buttons
            '''
            self.section_properties.setDisabled(toggle)
            self.saveBtn.setDisabled(toggle)
            self.exportBtn.setDisabled(toggle)

    def type_change(self):
        '''
        Method to handle Section Type change
        '''
        index_type=self.section_type_combobox.currentIndex()
        self.disable_usability(True)
        if(index_type in [1,4,5]):
                self.Centroid_box.hide()
                self.MI_label_3.hide()
                self.MI_text_3.hide()
                self.MI_label_4.hide()
                self.MI_text_4.hide()
                self.MI_label_5.hide()
                self.MI_text_5.hide()
                self.MI_label_6.hide()
                self.MI_text_6.hide()
                self.PSM_label_3.hide()
                self.PSM_text_3.hide()
        elif(index_type==2):
                self.MI_label_3.show()
                self.MI_text_3.show()
                self.MI_label_4.hide()
                self.MI_text_4.hide()
                self.MI_label_5.hide()
                self.MI_text_5.hide()
                self.MI_label_6.hide()
                self.MI_text_6.hide()
                self.PSM_label_3.show()
                self.PSM_text_3.show()
                self.MI_label_3.setText('Czz(mm⁴):')

        elif(index_type==3):
                self.Centroid_box.show()
                self.MI_label_3.show()
                self.MI_text_3.show()
                self.MI_label_4.show()
                self.MI_text_4.show()
                self.MI_label_5.show()
                self.MI_text_5.show()
                self.MI_label_6.show()
                self.MI_text_6.show()
                self.PSM_label_3.hide()
                self.PSM_text_3.hide()
                self.MI_label_3.setText('Ixy(mm⁴):')
        
        templates={
                0:[],
                1:['I I Side by Side'],
                2:['[ ] Face to Face','] [ Back to Back'],
                3:[
                        u'\u256c'+' Star Angles-4 Angles',
                        u'\u2309'+u'\u2308'+'Star Angles-2 Angles',
                        u'\u230d'+u'\u230e'+'Star Angles-2 Angles',
                        u'\u22a7'+'  Star Angles-2 Angles',
                        u'\u26f6'+' Box Section-4 Angles'
                ],
                4:[
                        u'\u02e1'+'I'+u'\u02e1'+'  I-Section with Stiffening',
                        u'\ua585'+' I-Section from Plates',
                        'Built up SHS/RHS',
                ],
                5:['I & Channel on One Flange'],
        }[index_type]
        self.section_template_combobox.blockSignals(True)
        self.section_template_combobox.clear()
        self.section_template_combobox.addItem('-------Select Template-------')
        self.section_template_combobox.addItems(templates)
        self.section_template_combobox.blockSignals(False)
        self.section_template_combobox.setProperty("lastitem", None)

    def update_section_properties(self,index_type,index_template):
        '''
        Method to fill output parameters to Section Properties
        '''
        conn = sqlite3.connect(PATH_TO_DATABASE)
        if(index_type==1):
                cursor = conn.execute("SELECT Area,B,T,tw,D FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                Area,B,T,t,Di=map(float,cursor.fetchall()[0])
                l=float(self.SectionParameters.parameterText_6.text())
                ti=float(self.SectionParameters.parameterText_7.text())
                S=float(self.SectionParameters.parameterText_3.text())
                A=round((2*Area)+(2*l*ti),4)
                D=round(Di-(2*T),4)
                Ybottom=round((
                        (l*ti*t/2)+
                        (2*B*T*ti*T/2)+
                        (2*((D*t)*((D/2)+T+ti)))+
                        (2*((B*T)*((T/2)+D+T+ti)))+
                        ((l*ti)*((ti/2)+D+ti+(2*T)))
                )/((4*B*T)+(2*l*ti)+(2*D*t)),4)
                Ytop=Ybottom
                Yleft=round((
                        (2*l*ti*l/2)+
                        (2*B*T*B/2)+
                        (D*t*B/2)+
                        (2*((B*T)*(l-S+(B/2))))+
                        ((D*t)*(l-S+(B/2)))
                )/((l*ti)+(4*B*T)+(2*D*t)),4)
                Yright=Yleft
                Izz=round((
                        ((B*(T**3)/12)+((B*T)*((Ybottom-(T/2)-ti)**2)))+
                        ((l*(ti**3)/12)+((l*ti)*((Ybottom-(ti/2))**2)))+
                        (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ybottom-(D/4)-T-ti)**2))))+
                        (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ytop-(D/4)-T-ti)**2))))+
                        (2*((B*(T**3)/12)+((B*T)*((Ytop-(T/2)-ti)**2))))+
                        ((l*(ti**3)/12)+((l*ti)*((Ytop-(ti/2))**2)))
                ),4)
                Iyy=round((
                        (2*(((l/2)*(ti**3)/12)+(((l/2)*ti)*((Yleft-(l/4))**2))))+
                        (2*((B*(T**3)/12)+((B*T)*((Yleft-(B/2))**2))))+
                        ((t*(D**3)/12)+((D*t)*((Yleft-(B/2))**2)))+
                        ((t*(D**3)/12)+((D*t)*((Yright-(B/2))**2)))+
                        (2*((B*(T**3)/12)+((B*T)*((Yright-(B/2))**2))))+
                        (2*(((l/2)*(ti**3)/12)+(((l/2)*ti)*((Yright-(l/4))**2))))
                ),4)
                Rzz=round(math.sqrt(Izz/A),4)
                Ryy=round(math.sqrt(Iyy/A),4)
                Zzz=round((A/2)*(Ytop+Ybottom),4)
                Zyy=round((A/2)*(Yleft+Yright),4)
                self.Area_text.setText(str(A))
                self.MI_text_1.setText(str(Izz))
                self.MI_text_2.setText(str(Iyy))
                self.RG_text_1.setText(str(Rzz))
                self.RG_text_2.setText(str(Ryy))
                self.ESM_text_1.setText(str(Zzz))
                self.ESM_text_2.setText(str(Zyy))
        elif(index_type==2):
                cursor = conn.execute("SELECT Area,B,T,tw,D FROM Channels where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                ChannelArea,B,T,t,Dc=map(float,cursor.fetchall()[0])
                l=float(self.SectionParameters.parameterText_6.text())
                ti=float(self.SectionParameters.parameterText_7.text())
                S=float(self.SectionParameters.parameterText_3.text())
                A=round((2*ChannelArea)+(2*l*ti),4)
                D=round(Dc-(2*T),4)
                if(index_template==1):
                        Yleft=round((
                                (D*t*t/2)+
                                (2*(B*T*B/2))+
                                (2*(l*ti*l/2))+
                                (2*(B*T*(S+t-(B/2))))+
                                (2*(D*t*(S+t+(t/2))))
                        )/((2*D*t)+(B*T)+(2*l*t)),4)
                        Yright=(2*t)+S-Yleft
                        Ybottom=round((
                                (2*(B*T*T+(ti/2)))+
                                (2*(D*t*((D/2)+T+ti)))+
                                (l*ti*(D+(2*T)+ti+(ti/2)))+
                                (2*(l*ti*(ti/2)))+
                                (2*(B*T*(D+T+(T/2))))
                        )/((4*B*T)+(2*D*t)+(2*l*ti)),4)
                        Ytop=D+(2*T)-Ybottom-(2*ti)
                        Izz=round((
                                (2*((B*(T**3)/12)+((B*T)*((Ybottom-(T/2))**2))))+
                                (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ybottom-(D/4)-T-ti)**2))))+
                                (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ytop-(D/4)-T-ti)**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Ytop-(T/2)-ti)**2))))+
                                (2*((l*(ti**3)/12)+((l*ti)*((Ybottom-(ti/2))**2))))
                        ),4)
                        Iyy=round((
                                (((t*(D**3)/12)+((D*t)*((Yleft-(t/2))**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Yleft-(B/2))**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Yright-(B/2))**2))))+
                                (((t*(D**3)/12)+((D*t)*((Yright-(t/2))**2))))+
                                (4*(((l/2)*(ti**3)/12)+(((l/2)*ti)*((Yleft-(l/4))**2))))
                        ),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                elif(index_template==2):
                        Ybottom=round((
                                (l*ti*ti/2)+
                                (2*(B*T*(ti*T/2)))+
                                (2*((D*t)*((D/2)+T+ti)))+
                                (2*((B*T)*((T/2)+D+ti+T)))+
                                ((l*ti)*(D+(2*T)+(ti/2)+t))
                        )/((2*l*ti)+(2*D*t)+(4*B*T)),4)
                        Ytop=Ybottom
                        Yleft=round((
                                (2*(l*ti*l/2))+
                                (2*(B*T*T/2))+
                                ((D*t)*((t/2)+B-(t/2)))+
                                (2*((B*T)*(B+S+(B/2))))+
                                ((D*t)*(B+S+(t/2)))
                        )/((2*l*t)+(4*B*T)+(2*D*t)),4)
                        Yright=Yleft
                        Izz=round((
                                (((l*(ti**3)/12)+((l*ti)*((Ybottom-(ti/2))**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Ybottom-(T/2)-ti)**2))))+
                                (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ybottom-(D/2)-T-ti)**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Ytop-(T/2)-ti)**2))))+
                                (((l*(ti**3)/12)+((l*ti)*((Ytop-(ti/2))**2))))
                        ),4)
                        Iyy=round((
                                (2*(((l/2)*(ti**3)/12)+(((l/2)*ti)*((Yleft-(l/4))**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Yleft-(B/2))**2))))+
                                (((t*(D**3)/12)+((D*T)*((Yleft-(t/2)-B)**2))))+
                                (((t*(D**3)/12)+((D*T)*((Yright-(t/2)-B)**2))))+
                                (2*((B*(T**3)/12)+((B*T)*((Yright-(B/2))**2))))+
                                (2*(((l/2)*(ti**3)/12)+(((l/2)*ti)*((Yright-(l/4))**2))))
                        ),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        Cy=Ybottom
                        Cz=Yleft
                        self.C_text_1.setText(str(Cy))
                        self.C_text_2.setText(str(Cz))
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))

        elif(index_type==3):
                if(index_template==1):
                        cursor = conn.execute("SELECT AXB FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        a,b = map(float,cursor.fetchall()[0][0].split('x'))
                        cursor = conn.execute("SELECT Area,t FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        Area,t=map(float,cursor.fetchall()[0])
                        ti=float(self.SectionParameters.parameterText_7.text())
                        l=float(self.SectionParameters.parameterText_6.text())
                        A=round((4*Area)+(l*ti),4)
                        D=a-t
                        Ybottom=round((
                                (l*ti*l/2)+
                                (2*D*t*D/2)+
                                (2*((b*t)*((t/2)+D)))+
                                (2*((b*t)*((t/2)+t+D)))+
                                (2*((D*t)*((D/2)+D+(2*t))))
                        )/((l*ti)+(4*b*t)+(4*D*t)),4)
                        Ytop=Ybottom
                        Yleft=round((
                                (2*b*t*b/2)+
                                (2*D*t*b/2)+
                                (l*ti*(b+(ti/2)))+
                                (2*((D*t)*(ti+b+(t/2))))+
                                (2*((b*t)*(ti+b+(b/2))))
                        )/((4*b*t)+(4*D*t)+(l*ti)),4)
                        Yright=Yleft
                        Izz=round((
                              (((ti*((l/2)**3)/12)+(((l/2)*ti)*((Ybottom-(l/4))**2))))+  
                              (2*((t*(D**3)/12)+((D*t)*((Ybottom-(D/2))**2))))+
                              (2*((b*(t**3)/12)+((b*t)*((Ybottom-(t/2)-D)**2))))+
                              (2*((t*(D**3)/12)+((D*t)*((Ytop-(D/2))**2))))+
                              (((ti*((l/2)**3)/12)+(((l/2)*ti)*((Ytop-(D/2))**2))))+
                              (2*((b*(t**3)/12)+((b*t)*((Ytop-(t/2)-D)**2))))
                        ),4)
                        Iyy=round((
                                (((b*(t**3)/12)+((b*t)*((Yleft-(b/2))**2))))+
                                (2*((b*(t**3)/12)+((b*t)*((Yright-(b/2))**2))))+
                                (2*((t*(D**3)/12)+((D*t)*((Yleft+(t/2)-b)**2))))+
                                (2*((t*(D**3)/12)+((D*t)*((Yright+(t/2)-b)**2))))+
                                (((l*(ti**3)/12)+((l*ti)*((Yleft-(ti/2)-b)**2))))
                        ),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        Cy=Ybottom
                        Cz=Yleft
                        self.C_text_1.setText(str(Cy))
                        self.C_text_2.setText(str(Cz))
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                elif(index_template==2):
                        cursor = conn.execute("SELECT AXB FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        a,b = map(float,cursor.fetchall()[0][0].split('x'))
                        cursor = conn.execute("SELECT Area,Iy,Cy,t FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        Area,Iy,Cy,t=map(float,cursor.fetchall()[0])
                        ti=float(self.SectionParameters.parameterText_7.text())
                        l=float(self.SectionParameters.parameterText_6.text())
                        D=a-t
                        A=round((2*Area)+(l*ti),4)
                        Ybottom=round((
                                (2*D*t*D/2)+
                                (2*((b*t)*(D+(t/2))))+
                                (l*ti*l/2)
                        )/((2*D*t)+(2*b*t)+(l*ti)),4)
                        Ytop=D+t-Ybottom
                        Yleft=round((
                                (b*t*b/2)+
                                (D*t*(b-(t/2)))+
                                (l*ti*(b+(ti/2)))+
                                (D*t*(b+ti+(t/2)))+
                                (b*t*(b+ti+(b/2)))
                        )/((2*b*t)+(2*D*t)+(l*ti)),4)
                        Yright=Yleft
                        Izz=round((
                                (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ybottom-(D/4))**2))))+
                                (((ti*(l/2))+(((l/2)*ti)*((Ybottom-(l/4))**2))))+
                                (2*((t*((D/2)**3)/12)+(((D/2)*t)*((Ytop-(D/4)-t)**2))))+
                                (((ti*(l/2))+(((l/2)*ti)*((Ytop-(l/4))**2))))+
                                (2*((b*(t**3)/12)+((b*t)*((Ytop-(t/2))**2))))
                        ),4)
                        Iyy=round( 2*(Iy+(A*((Cy+(t/2))**2))),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        Cy=Ybottom
                        Cz=Yleft
                        self.C_text_1.setText(str(Cy))
                        self.C_text_2.setText(str(Cz))
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                
                elif(index_template==3):
                        cursor = conn.execute("SELECT AXB FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        a,b = map(float,cursor.fetchall()[0][0].split('x'))
                        cursor = conn.execute("SELECT Area,t FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        Area,t=map(float,cursor.fetchall()[0])
                        ti=float(self.SectionParameters.parameterText_7.text())
                        l=float(self.SectionParameters.parameterText_6.text())
                        A=round((2*Area)+(l*ti),4)
                        D=a-t
                        Ybottom=round((
                                (l*ti*l/2)+
                                (D*t*D/2)+
                                (b*t*(D+(t/2)))+
                                (b*t*(t+D+(t/2)))+
                                (D*t*((2*t)+(D/2)+D))
                        )/((l*ti)+(2*D*t)+(2*b*t)),4)
                        Ytop=Ybottom
                        Yleft=round((
                                (b*t*b/2)+
                                (D*t*b/2)+
                                (l*ti*(b+(ti/2)))+
                                (D*t*(ti+b+(t/2)))+
                                (b*t*(ti+b+(b/2)))
                        )/((2*b*t)+(2*D*t)+(l*ti)),4)
                        Yright=Yleft
                        Izz=round((
                                (((ti*((l/2)**3)/12)+(((l/2)*ti)*((Ybottom-(l/4))**2))))+
                                (((t*(D**3)/12)+((D*t)*((Ybottom-(D/2))**2))))+
                                (((b*(t**3)/12)+((b*t)*((Ybottom-(t/2)-D)**2))))+
                                (((b*(t**3)/12)+((b*t)*((Ytop-(t/2)-D)**2))))+
                                (((t*(D**3)/12)+((D*t)*((Ytop-(D/2))**2))))+
                                (((ti*((l/2)**3)/12)+(((l/2)*ti)*((Ytop-(l/4))**2))))

                        ),4)
                        Iyy=round((
                                (((b*(t**3)/12)+((b*t)*((Yleft-(b/2))**2))))+
                                (((t*(D**3)/12)+((D*t)*((Yleft+(t/2)-b)**2))))+
                                (((ti*(l**3)/12)+((l*t)*((Yleft-(t/2)-b)**2))))+                        
                                (((t*(D**3)/12)+((D*t)*((Yright+(t/2)-b)**2))))+
                                (((b*(t**3)/12)+((b*t)*((Yleft-(b/2))**2))))
                        ),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        Cy=Ybottom
                        Cz=Yleft
                        self.C_text_1.setText(str(Cy))
                        self.C_text_2.setText(str(Cz))
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
        
                elif(index_template==4):
                        cursor = conn.execute("SELECT AXB FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        a,b = map(float,cursor.fetchall()[0][0].split('x'))
                        cursor = conn.execute("SELECT Area,Iy,t FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        Area,Iy,t=map(float,cursor.fetchall()[0])
                        ti=float(self.SectionParameters.parameterText_7.text())
                        l=float(self.SectionParameters.parameterText_6.text())
                        A=round((2*Area)+(l*ti),4)
                        D=a-t
                        Ybottom=round((
                                (l*ti+l/2)+
                                (D*t*D/2)+
                                (b*t*(D+(t/2)))+
                                ((b*t)*(D+t+(t/2)))+
                                ((D*t)*(D+t+t+(D/2)))
                        )/((l*t)+(2*D*t)+(2*b*t)),4)
                        Ytop=Ybottom
                        Yleft=round((
                                (l*t*ti/2)+
                                (2*((D*t)*(ti+(t/2))))+
                                (2*((b*t)*(ti+(b/2))))
                        )/((l+ti)+(2*b*t)+(2*D*t)),4)
                        Yright=ti+b-Yleft
                        Izz=round((
                                (((ti*((l**3)/2)/12)+(((l/2)*ti)*((Ybottom-(l/4))**2))))+
                                (((t*(D**3)/12)+((D*t)*((Ybottom-(D/2))**2))))+
                                (((b*(t**3)/12)+((b*t)*((Ybottom-(t/2)-D)**2))))+
                                (((b*(t**3)/12)+((b*t)*((Ytop-(t/2))**2))))+
                                (((t*(D**3)/12)+((D*t)*((Ytop-(D/2)-t)**2))))+
                                (((ti*((l/2)**3)/12)+(((l/2)*t)*((Ytop-(l/4))**2))))

                        ),4)
                        Ryy=round(math.sqrt(Iy/A),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        Cy=Ybottom
                        Cz=Yleft
                        self.C_text_1.setText(str(Cy))
                        self.C_text_2.setText(str(Cz))
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                elif(index_template==5):
                       cursor = conn.execute("SELECT AXB FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                       a,b = map(float,cursor.fetchall()[0][0].split('x'))
                       cursor = conn.execute("SELECT Area,t FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                       Area,t=map(float,cursor.fetchall()[0])
                       ti=float(self.SectionParameters.parameterText_7.text())
                       S=float(self.SectionParameters.parameterText_3.text())
                       l=float(self.SectionParameters.parameterText_5.text())
                       lv=float(self.SectionParameters.parameterText_6.text())
                       A=round((4*Area)+(2*l*ti)+(2*lv*ti),4)
                       D=a-t 
                       Ybottom=round((
                               (l*ti*ti/2)+
                               (2*b*t*(ti*t/2))+
                               (2*((D*t)*(t+ti+(D/2))))+
                               (2*((D*t)*(D+t+ti+(D/2))))+
                               (2*((b*t)*(D+D+t+ti+(t/2))))+
                               ((l*ti)*(ti+D+t+t+D+(ti/2)))+
                               (2*((lv*ti)*(lv/2)))
                       )/((2*l*ti)+(2*lv*ti)+(4*D*t)+(4*b*t)),4)
                       Ytop=Ybottom
                       Yleft=round((
                               (lv*ti*ti/2)+
                               (2*((D*t)*(ti+(t/2))))+
                               (2*((b*t)*(ti+(b/2))))+
                               (2*((b*t)*(ti+t+S+t-(b/2))))+
                               (2*((D*t)*(ti+t+S+(t/2))))+
                               ((lv*ti)*(t+S+t+ti+(ti/2)))+
                               (2*((l*t)*(ti+(l/2))))
                       )/((4*b*t)+(2*l*t)+(2*lv*ti)+(D*t)),4)
                       Yright=Yleft
                       Izz=round((
                             ((l*(ti**3)/12)+(l*ti)*((Ybottom-(ti/2))**2))+  
                             (2*((b*(t**3)/12)+(b*t)*((Ybottom-(t/2)-ti)**2)))+
                             (2*((t*(D**3)/12)+(D*t)*((Ybottom-(D/2)-ti-t)**2)))+
                             (2*((t*(D**3)/12)+(D*t)*((Ytop-(D/2)-ti-t)**2)))+
                             ((b*(t**3)/12)+(b*t)*((Ytop-(t/2)-ti)**2))+
                             ((l*(ti**3)/12)+(l*ti)*((Ybottom-(ti/2))**2))+  
                             (2*((ti*((lv**3)/2)/12)+(((lv/2)*ti)*((Ybottom-(l/4))**2))))+
                             (2*((ti*((lv**3)/2)/12)+(((lv/2)*ti)*((Ytop-(l/4))**2))))

                       ),4)
                       Iyy=round((
                               ((lv*(ti**3)/12)+(lv*ti)*((Yleft-(ti/2))**2))+
                               (2*((t*(D**3)/12)+(D*t)*((Yleft-(t/2)-ti)**2)))+
                               (2*((b*(t**3)/12)+(b*t)*((Yleft-(b/2)-ti)**2)))+
                               ((l*(ti**3)/12)+(l*ti)*((Yleft-(l/2))**2))+  
                               (2*((b*(t**3)/12)+(b*t)*((Yright-(b/2)-ti-t)**2)))+
                               (2*((t*(D**3)/12)+(D*t)*((Yright-(t/2)-ti)**2)))+
                               ((lv*(ti**3)/12)+(lv*ti)*((Yright-(ti/2))**2))
                       ),4)
                       Ryy=round(math.sqrt(Iyy/A),4)
                       Rzz=round(math.sqrt(Izz/A),4)
                       Zzz=round((A/2)*(Ytop+Ybottom),4)
                       Zyy=round((A/2)*(Yleft+Yright),4)
                       Cy=Ybottom
                       Cz=Yleft
                       self.C_text_1.setText(str(Cy))
                       self.C_text_2.setText(str(Cz))
                       self.Area_text.setText(str(A))
                       self.MI_text_1.setText(str(Izz))
                       self.MI_text_2.setText(str(Iyy))
                       self.RG_text_1.setText(str(Rzz))
                       self.RG_text_2.setText(str(Ryy))
                       self.ESM_text_1.setText(str(Zzz))
                       self.ESM_text_2.setText(str(Zyy))
        elif(index_type==4):
                if(index_template==1):
                        cursor = conn.execute("SELECT Area,B,T,tw,D FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        ISectionArea,B,T,t,Di=map(float,cursor.fetchall()[0])
                        D=Di-(2*T)
                        P,Q=float(self.SectionParameters.parameterText_6.text()),float(self.SectionParameters.parameterText_7.text())
                        A=ISectionArea+(2*P*Q)
                        Ybottom=(
                                (B*T*T/2)+
                                (t*D*(D/2)*t)+
                                (B*T*(B+T+(T/2)))+
                                (2*Q*P*((2*T)+D-(P/2)))
                        )/((B*T)+(t*D)+(B*T)+(2*Q*P))
                        Ytop=((2*T)+D-Ybottom)
                        Yleft=(
                                ((P**3)*Q*Q/2)+
                                (2*(B/2)*T*((B/4)+Q))+
                                (D*(t/2)*((t/2)+(B/2)+Q))
                        )/(P*Q*2*(B/2)*T*D*(t/2))
                        Yright=Yleft
                        Izz=round((
                                ((B*(T**3)/12)+(B*T)*((Ybottom-(T/2))**2))+
                                ((t*(D**3)/12)+(D*T)*((D-(D/2)-Ybottom)**2))+
                                ((B*(T**3)/12)+(B*T)*((Ytop-(T/2))**2))+
                                (2*((Q*(P**3)/12)+(Q*P)*((Ytop-(P/2))**2)))),4)
                        Iyy=round((
                                ((Q*(P**3)/12)+(P*Q)*((Yleft-(Q/2))**2))+
                                (((B/2)*(T**3)/12)+((B/2)*T)*((Yleft-(B/4))**2))+
                                (((t/2)*(D**3)/12)+(D*t/2)*((Yleft-Q-(B/2)+(t/4))**2))),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                elif(index_template==2):
                        cursor = conn.execute("SELECT Area,D,tw,B,T FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        Area,Dc,t,B,T=map(float,cursor.fetchall()[0])
                        D=Dc-(2*T)
                        d=round(((D-(2*T))/2)-t,4)
                        A=round((2*Area)-(t**2),4)
                        Ybottom=round((
                                (B*T*T/2)+
                                (D*t*((D/2)+T))+
                                (2*(D*T*((D/2)+T)))+
                                (2*(d*t*((D/2)+T)))+
                                (B*T*(D+T+(T/2)))
                        )/((2*B*T)+(D*t)+(D*T)+(D*T)+(2*d*t)),4)
                        Ytop=Ybottom
                        Yleft=round((
                                (D*T*T/2)+
                                (B*T*B)+
                                (d*t*((d/2)+T))+
                                (D*t*(d+T+(t/2)))+
                                (d*t*(T+d+t+(d/2)))+
                                (D*T*(d+t+d+T+(T/2)))
                        )/((2*D*T)+(D*t)+(2*B*T)+(2*d*T)),4)
                        Yright=Yleft
                        Izz=round((
                                ((B*(T**3)/12)+(B*T)*((Ybottom-(T/2))**2))+
                                (2*((T*((D/2)**3)/12)+((D/2)*T)*((Ybottom-(D/4)-T)**2)))+
                                ((t*((D/2)**3)/12)+((D/2)*t)*((Ybottom-(D/4)-T)**2))+
                                (2*((d*((t/2)**3)/12)+((t/2)*d)*((Ybottom-(D/2)-T)**2)))+
                                (2*((d*((t/2)**3)/12)+((t/2)*d)*((Ytop-(D/2)-T)**2)))+
                                (2*((T*((D/2)**3)/12)+((D/2)*T)*((Ytop-(D/4)-T)**2)))+
                                ((T*((D/2)**3)/12)+((D/2)*T)*((Ytop-(D/4)-T)**2))+
                                ((B*(T**3)/12)+(B*T)*((Ytop-(T/2))**2))
                        ),4)
                        Iyy=round((
                                ((T*(D**3)/12)+(D*T)*((Yleft-(T/2))**2))+
                                (2*(((B/2)*(T**3)/12)+((B/2)*T)*((Yleft-(B/4))**2)))+
                                (2*(((B/2)*(T**3)/12)+((B/2)*T)*((Yright-(B/4))**2)))+
                                ((d*(t**3)/12)+((T*d)*((Yleft-(d/2)-T)**2)))+
                                ((d*(t**3)/12)+((t*d)*((Yright-(d/2)-T)**2)))+
                                (((t/2)*(D**3)/12)+((t/2)*D)*((Yleft-(t/4)-T-d)**2))+
                                (((t/2)*(D**3)/12)+((t/2)*D)*((Yright-(t/4)-T-d)**2))+
                                ((T*(D**3)/12)+(D*T)*((Yright-(T/2))**2))
                        ),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                elif(index_template==3):
                        cursor = conn.execute("SELECT B,T FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        B,T=map(float,cursor.fetchall()[0])
                        A=4*B*T
                        Ybottom=round((
                                (B*T*T/2)+
                                (2*(B/2)*T*(B/4))
                        )/((B*T)+((B/2)*T)),4)
                        Ytop=Ybottom
                        Yleft=round((
                                (B*T*T/2)+
                                (2*(B/2)*T*(B/4))
                        )/((B*T)+(2*(B/2)*T)),4)
                        Yright=Yleft
                        Izz=round((
                                (B*(T**3)/12)+
                                ((B*T)*((Ybottom-(T/2))**2))+
                                (2*((((B/2)**3)*T/12))+(((B/2)*T)*((Ybottom-T-(B/4))**2)))
                        ),4)
                        Iyy=round((
                                (B*(T**3)/12)+
                                ((B*T)*((Ytop-(T/2))**2))+
                                (2*(((((B/2)**3)+T)/12))+(((B/2)*T)*((Yleft-T-(B/4))**2)))
                        ),4)
                        Rzz=round(math.sqrt(Izz/A),4)
                        Ryy=round(math.sqrt(Iyy/A),4)
                        Zzz=round((A/2)*(Ytop+Ybottom),4)
                        Zyy=round((A/2)*(Yleft+Yright),4)
                        self.Area_text.setText(str(A))
                        self.MI_text_1.setText(str(Izz))
                        self.MI_text_2.setText(str(Iyy))
                        self.RG_text_1.setText(str(Rzz))
                        self.RG_text_2.setText(str(Ryy))
                        self.ESM_text_1.setText(str(Zzz))
                        self.ESM_text_2.setText(str(Zyy))
                        
        elif(index_type==5):
                cursor = conn.execute("SELECT Area,B,T,tw,D FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                ISectionArea,B,T,t,Di=map(float,cursor.fetchall()[0])
                D=Di-(2*T)
                cursor = conn.execute("SELECT Area,B,T,tw,D FROM Channels where Designation="+repr(self.SectionParameters.parameterText_2.currentText()))
                ChannelArea,R,P,U,Dc = map(float,cursor.fetchall()[0])
                Q=Dc-(2*P)
                S=float(self.SectionParameters.parameterText_3.text())
                A = ISectionArea+ChannelArea
                Ybottom=round((
                        (B*T*T/2)+
                        ((T*D)*((D/2)+T))+
                        (B*T*(D+T+(T/2)))+
                        (Q*U*(D+T+T+(U/2)))+
                        (2*P*R*(T+D+T+U-(R/2)))
                )/((2*B*T)+(D*t)+(U*Q)+(2*P*R)),4)
                Ytop=((2*T)+D+U)-Ybottom
                Yleft=round((
                        (R*P*P/2)+
                        ((Q/2)*U*(Q/4)*U)+
                        (2*(B/2)*T*(S+P+(t/2)-(B/4)))+
                        (D*t/2*(S+P+(t/4)))
                )/((R*P)+((Q/2)*U)+(2*(B/2)*T)+(D*(t/2))),4)
                Yright=(P+S+t+S+P)-Yleft
                Izz=round((
                        ((B*(T**3)/12)+((B*T)*((Ybottom-((T/3)**2)))))+
                        ((t*(D**3)/12)+(t*D)+(((D/2)+T-Ybottom)**2))+
                        ((B*(T**3)/12)+(B*T)*((Ytop-U-(T/2))**2))+
                        ((Q*(U**3)/12)+(Q*U)*((Ytop-(U/2))**2))+
                        (((P*(R**3)/12)+(P*R)*((Ytop-R+(R/2))**2))/2)
                ),4)
                Iyy=round((
                        ((P*(R**3)/12)+(R*P)*((Yleft-P)**2))+
                        (((Q/2)*(U**3))+((Q/2)*U)*((Yleft-(U/4)-P)**2))+
                        (2*(((B/2)*(T**3))+((B/2)*T)*((Yleft-(B/4)-S-P)**2)))+
                        (((t/2)*(D**3))+((t/2)*D)*((Yleft-(t/4)-S-P)**2))
                ),4)
                Rzz=round(math.sqrt(Izz/A),4)
                Ryy=round(math.sqrt(Iyy/A),4)
                Zzy=round(A*(Yleft+Yright)/2,4)
                Zzz=round(A*(Ytop+Ybottom)/2,4)
                self.Area_text.setText(str(A))
                self.MI_text_1.setText(str(Izz))
                self.MI_text_2.setText(str(Iyy))
                self.RG_text_1.setText(str(Rzz))
                self.RG_text_2.setText(str(Ryy))
                self.ESM_text_1.setText(str(Zzy))
                self.ESM_text_2.setText(str(Zzz))



    def template_change(self,new_index):
        '''
        Method to handle Section Template change
        and retrieve saved values for section parameters
        '''
        last_index=self.section_template_combobox.property("lastitem")
        index_type=self.section_type_combobox.currentIndex()
        index_template=self.section_template_combobox.currentIndex()
        if(index_template==0):
                self.disable_usability(True)
                return
        else:
                self.SectionParameters=Ui_SectionParameters(index_type,index_template)
                if(index_type in [1,4,5]):
                        self.SectionParameters.parameterText_1.clear()
                        self.SectionParameters.parameterText_1.addItems(connectdb('Columns'))
                        if(index_type==5):
                                self.SectionParameters.parameterText_2.clear()
                                self.SectionParameters.parameterText_2.addItems(connectdb('Channels'))
                elif(index_type==2):
                        self.SectionParameters.parameterText_1.clear()
                        self.SectionParameters.parameterText_1.addItems(connectdb('Channels'))
                elif(index_type==3):
                        self.SectionParameters.parameterText_1.clear()
                        self.SectionParameters.parameterText_1.addItems(connectdb('Angles'))
        

                if(last_index==new_index and self.Parameters!={}):
                        for child in self.Parameters:
                                self.SectionParameters.textBoxVisible[child]=self.Parameters[child]
                                if(child=='parameterText_1' or child=='parameterText_2'):
                                        exec('self.SectionParameters.'+child+'.setCurrentText('+repr(self.Parameters[child][1])+')')
                                else:
                                        exec('self.SectionParameters.'+child+'.setText('+repr(self.Parameters[child][1])+')')
                self.SectionParameters.exec()
                self.Parameters=self.SectionParameters.textBoxVisible
                if(self.Parameters=={}):
                        self.disable_usability(True)
                else:
                        self.disable_usability(False)
                        self.update_section_properties(index_type,index_template)

        if(index_type==2):
                if(index_template==1):
                                self.Centroid_box.hide()                        
                elif(index_template==2):
                                self.Centroid_box.show()
        self.section_template_combobox.setProperty("lastitem",new_index)


    def retranslateUi(self,Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Osdag Section Modeller"))
        self.label.setText(_translate("Dialog", "Design Section"))
        self.label_2.setText(_translate("Dialog", "Section Type:"))
        self.section_type_combobox.setItemText(0, _translate("Dialog", "---------Select Type---------"))
        self.section_type_combobox.setItemText(1, _translate("Dialog", "I-Section"))
        self.section_type_combobox.setItemText(2, _translate("Dialog", "Channel Section"))
        self.section_type_combobox.setItemText(3, _translate("Dialog", "Angle Section"))
        self.section_type_combobox.setItemText(4, _translate("Dialog", "Built-Up Section"))
        self.section_type_combobox.setItemText(5, _translate("Dialog", "Compound Section"))
        self.label_3.setText(_translate("Dialog", "Section Template:"))
        self.section_template_combobox.setItemText(0, _translate("Dialog", "-------Select Template-------"))
        self.label_4.setText(_translate("Dialog", "Section Designation:"))
        self.label_5.setText(_translate("Dialog", "Section Properties"))
        self.Area.setText(_translate("Dialog", "Area(mm²):"))
        self.RG.setText(_translate("Dialog", "Radius of Gyration:"))
        self.RG_label_1.setText(_translate("Dialog", "Rzz(mm):"))
        self.RG_label_2.setText(_translate("Dialog", "Ryy(mm):"))
        self.ESM.setText(_translate("Dialog", "Elastic Section Moduli:"))
        self.ESM_label_1.setText(_translate("Dialog", "Zzz(mm³):"))
        self.ESM_label_2.setText(_translate("Dialog", "Zyy(mm³):"))
        self.C.setText(_translate("Dialog", "Centroid:"))
        self.C_label_1.setText(_translate("Dialog", "Cy(mm):"))
        self.C_label_2.setText(_translate("Dialog", "Cz(mm):"))
        self.MI.setText(_translate("Dialog", "Moment of Inertia:"))
        self.MI_label_1.setText(_translate("Dialog", "Izz(mm⁴):"))
        self.MI_label_2.setText(_translate("Dialog", "Iyy(mm⁴):"))
        self.MI_label_3.setText(_translate("Dialog", "Ixy(mm⁴):"))
        self.MI_label_4.setText(_translate("Dialog", "𝛼(°):"))
        self.MI_label_5.setText(_translate("Dialog", "Iu(mm⁴):"))
        self.MI_label_6.setText(_translate("Dialog", "Iv(mm⁴):"))
        self.PSM.setText(_translate("Dialog", "Plastic Section Moduli:"))
        self.PSM_label_1.setText(_translate("Dialog", "Zpy(mm³):"))
        self.PSM_label_2.setText(_translate("Dialog", "Zpz(mm³):"))
        self.PSM_label_3.setText(_translate("Dialog", "Czp(mm³):"))
        self.saveBtn.setText(_translate("Dialog", "Save"))
        self.exportBtn.setText(_translate("Dialog", "Export"))


