'''
Section Type and Template Description:
1) I-Section
        1.1) Side by Side
2) Channels Section
        2.1) Face to Face
        2.2) Back to Back
3) Angles Section
        3.1) Star Configuration with 4 Angles
        3.2) Star Configuration with 2 Angles
        3.3) Two angles on same side
        3.4) Two angles on opposite sides
        3.5) Box with 4 Angles
4) Built-up Section
        4.1) I-Section with stiffening
        4.2) I-Section from Plates
        4.3) Built-up SHS.RHS
5) Compound Section
        5.1) I-Section on one flange

# Integers are Section Types
# Floating-Points are Section Templates
#For Example:
Two angles on opposite side will be:
-Section_Type_Index =3
-Section_Template_Index =4

'''


import math
import numpy
import sys
import os
import pprint
from PyQt5 import QtCore, QtGui, QtWidgets
from Common import *
from gui.ui_section_parameters import Ui_SectionParameters
from gui.ui_SectionModeller_SummaryPopUp import Ui_Dialog1 as SummaryDialog
from SectionModeller_Latex import CreateLatex
from cad.cadfiles.isection_coverplate import IsectionCoverPlate
from cad.cadfiles.isection_channel import ISectionChannel
from cad.cadfiles.star_angle2 import StarAngle2
from cad.cadfiles.star_angle4 import StarAngle4
from cad.cadfiles.star_angle_opp import StarAngleOpposite
from cad.cadfiles.star_angle_same import StarAngleSame
from cad.cadfiles.TIsection import TISection
from cad.cadfiles.channel_section import ChannelSection
from cad.cadfiles.channel_section_opp import ChannelSectionOpposite
from cad.cadfiles.box import Box
from cad.cadfiles.box_angle import BoxAngle
from cad.cadfiles.cross_isection import cross_isection


class Ui_OsdagSectionModeller(object):

        def setupUi(self,Dialog):
                super().__init__()
                Dialog.setObjectName("Dialog")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
                Dialog.setSizePolicy(sizePolicy)
                #self.setMinimumSize(QtCore.QSize(700, 500))
                #self.setMaximumSize(QtCore.QSize(906, 800))
                Dialog.setSizeGripEnabled(False)
                #self.setModal(True)
                self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
                self.verticalLayout.setContentsMargins(11, 11, 11, 11)
                self.verticalLayout.setSpacing(0)
                self.verticalLayout.setObjectName("verticalLayout")
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
                self.horizontalLayout.setSpacing(0)
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.design_section = QtWidgets.QFrame(Dialog)

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

                self.OCCFrame.setFrameShape(QtWidgets.QFrame.Box)
                self.OCCFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.OCCFrame.setLineWidth(3)
                self.OCCFrame.setObjectName("OCCFrame")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.OCCFrame.sizePolicy().hasHeightForWidth())
                self.OCCFrame.setSizePolicy(sizePolicy)
                #self.OCCFrame.setMinimumSize(QtCore.QSize(300, 200))
                self.OCCFrame.setMaximumSize(QtCore.QSize(500, 400))
                self.horizontalLayout.addWidget(self.OCCFrame)
                self.horizontalLayout.setStretch(0, 1)
                self.horizontalLayout.setStretch(1, 1)
                self.verticalLayout.addLayout(self.horizontalLayout)
                self.section_properties = QtWidgets.QFrame(Dialog)

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
                spacerItem8 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
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
                display=self.init_display()
                Dialog.setFixedSize(Dialog.sizeHint())

        def set_validations(self):
                '''
                Mehtod to set Validations for Section Properties and Section Designation
                '''
                self.section_designation_lineEdit.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[a-zA-Z0-9@_]*"), self.section_designation_lineEdit
        ))
                self.Area_text.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.Area_text
        ))
                self.MI_text1.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.MI_text1
        ))
                self.MI_text2.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.MI_text2
        ))
                self.RG_text1.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.RG_text1
        ))
                self.RG_text2.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.RG_text2
        ))
                self.C_text1.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.C_text1
        ))
                self.C_text2.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.C_text2
        ))
                self.ESM_text1.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.ESM_text1
        ))
                self.ESM_text2.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.ESM_text2
        ))
                self.PSM_text1.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.PSM_text1
        ))
                self.PSM_text1.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.PSM_text2
        ))

        def clear_properties(self):
                '''
                Method to clear all Section Properties text boxes
                '''
                self.Area_text.clear()
                self.RG_text1.clear()
                self.RG_text2.clear()
                self.MI_text1.clear()
                self.MI_text2.clear()
                self.C_text1.clear()
                self.C_text2.clear()
                self.ESM_text1.clear()
                self.ESM_text2.clear()
                self.PSM_text1.clear()
                self.PSM_text2.clear()
        
        def disable_usability(self,toggle):
                '''
                Method to Disable/Enable Section Properties and Save and Export Buttons
                '''
                self.section_properties.setDisabled(toggle)
                self.saveBtn.setDisabled(toggle)
                self.exportBtn.setDisabled(toggle)
        
        def template_change(self):
                '''
                Method to handle Section Template change
                and retrieve saved values for section parameters
                '''
                self.Parameters={}
                self.section_designation_lineEdit.clear()
                self.clear_properties()
                display.EraseAll()
                self.disable_usability(True)
        
        def type_change(self):
                '''
                Method to handle Section Type change 
                and change Section Template Combobox accordingly
                '''
                index_type=self.section_type_combobox.currentIndex()
                self.section_designation_lineEdit.clear()
                self.clear_properties()
                display.EraseAll()
                self.disable_usability(True)                
                templates={
                        0:[],
                        1:['Side by Side'],
                        2:['Face to Face','Back to Back'],
                        3:[
                                'Star Angles-4 Angles',
                                'Star Angles-2 Angles',
                                '2 Angles on same side',
                                '2 Angles on opposite sides',
                                'Box Section-4 Angles'
                        ],
                        4:[
                                'I-Section with Stiffening',
                                'I-Section from Plates',
                                'Built up SHS/RHS',
                        ],
                        5:['I & Channel on One Flange'],
                }[index_type]
                self.section_template_combobox.blockSignals(True)
                self.section_template_combobox.clear()
                self.section_template_combobox.addItem('--------Select Template--------')
                self.section_template_combobox.addItems(templates)

                ########################## Loading Tooltip on hover over template ####################################
                if(index_type==1):
                        self.section_template_combobox.setItemData(1, "<img src='./ResourceFiles/images/SectionModeller/Main/1.1.png'>",QtCore.Qt.ToolTipRole)
                elif(index_type==2):
                        self.section_template_combobox.setItemData(1, "<img src='./ResourceFiles/images/SectionModeller/Main/2.1.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(2, "<img src='./ResourceFiles/images/SectionModeller/Main/2.2.png'>",QtCore.Qt.ToolTipRole)
                elif(index_type==3):
                        self.section_template_combobox.setItemData(1, "<img src='./ResourceFiles/images/SectionModeller/Main/3.1.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(2, "<img src='./ResourceFiles/images/SectionModeller/Main/3.2.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(3, "<img src='./ResourceFiles/images/SectionModeller/Main/3.3.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(4, "<img src='./ResourceFiles/images/SectionModeller/Main/3.4.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(5, "<img src='./ResourceFiles/images/SectionModeller/Main/3.5.png'>",QtCore.Qt.ToolTipRole)
                elif(index_type==4):
                        self.section_template_combobox.setItemData(1, "<img src='./ResourceFiles/images/SectionModeller/Main/4.1.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(2, "<img src='./ResourceFiles/images/SectionModeller/Main/4.2.png'>",QtCore.Qt.ToolTipRole)
                        self.section_template_combobox.setItemData(3, "<img src='./ResourceFiles/images/SectionModeller/Main/4.3.png'>",QtCore.Qt.ToolTipRole)
                elif(index_type==5):
                        self.section_template_combobox.setItemData(1, "<img src='./ResourceFiles/images/SectionModeller/Main/5.1.png'>",QtCore.Qt.ToolTipRole)
                ##########################################################################################################
                self.section_template_combobox.blockSignals(False)
        
        def open_section_parameters(self):
                '''
                Method to handle Enter/Edit Parameters button
                '''
                index_type=self.section_type_combobox.currentIndex()
                index_template=self.section_template_combobox.currentIndex()
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


                ########################## Retrieving Section Parameters on Dialog close and reopen ###################
                if(self.Parameters!={}):
                        for child in self.Parameters:
                                self.SectionParameters.textBoxVisible[child]=self.Parameters[child]
                                if(child=='parameterText_1' or child=='parameterText_2'):
                                        exec('self.SectionParameters.'+child+'.setCurrentText('+repr(self.Parameters[child][1])+')')
                                else:
                                        exec('self.SectionParameters.'+child+'.setText('+repr(self.Parameters[child][1])+')')
                
                #############################################################################################################
                if(index_type!=0 and index_template!=0):
                        self.SectionParameters.exec()
                        self.Parameters=self.SectionParameters.textBoxVisible
                else:
                        return
                if(self.Parameters=={}):
                        self.disable_usability(True)
                else:
                        self.disable_usability(False)
                        self.update_section_properties(index_type,index_template)

        def create_cad_model(self,index_type,index_template,parameters):
                '''
                Method to Specify and create CAD model template-wise
                '''
                origin = numpy.array([0.,0.,0.])
                uDir = numpy.array([1.,0.,0.])
                shaftDir = wDir = numpy.array([0.,0.,1.])
                if(index_type==1):                        
                        ISecPlate = IsectionCoverPlate(*parameters)
                        ISecPlate.place(origin, uDir, shaftDir)
                        prism = ISecPlate.create_model()
                        display.DisplayShape(prism, update=True)
                elif(index_type==2):
                        if(index_template==1):
                                channel_section = ChannelSection(*parameters)
                                _place = channel_section.place(origin, uDir, shaftDir)
                                point = channel_section.compute_params()
                                prism = channel_section.create_model()
                                display.DisplayShape(prism, update=True)
                        elif(index_template==2):
                                channel_section = ChannelSectionOpposite(*parameters)
                                _place = channel_section.place(origin, uDir, shaftDir)
                                point = channel_section.compute_params()
                                prism = channel_section.create_model()
                                display.DisplayShape(prism, update=True)
                elif(index_type==3):
                        if(index_template==1):
                                star_angle = StarAngle4(*parameters)
                                _place = star_angle.place(origin, uDir, wDir)
                                point = star_angle.compute_params()
                                prism = star_angle.create_model()
                                display.DisplayShape(prism, update=True)
                        
                        elif(index_template==2):
                                star_angle = StarAngle2(*parameters)
                                _place = star_angle.place(origin, uDir, wDir)
                                point = star_angle.compute_params()
                                prism = star_angle.create_model()
                                display.DisplayShape(prism, update=True)

                        elif(index_template==3):
                                star_angle_same = StarAngleSame(*parameters)
                                _place = star_angle_same.place(origin, uDir, wDir)
                                point = star_angle_same.compute_params()
                                prism = star_angle_same.create_model()
                                display.DisplayShape(prism, update=True)

                        elif(index_template==4):
                                star_angle_opposite = StarAngleOpposite(*parameters)
                                _place = star_angle_opposite.place(origin, uDir, wDir)
                                point = star_angle_opposite.compute_params()
                                prism = star_angle_opposite.create_model()
                                display.DisplayShape(prism, update=True)
                        
                        elif(index_template==5):
                                l = 40
                                l1 = 50
                                a = 15
                                b = 15
                                t = 2
                                t1 = 2
                                s = l  - 2*t1
                                s1 = l1 - 2*t1 - 2*t
                                H = 50
                                box_angle = BoxAngle(*parameters)
                                _place = box_angle.place(origin, uDir, wDir)
                                point = box_angle.compute_params()
                                prism = box_angle.create_model()
                                display.DisplayShape(prism, update=True)
                                
                elif(index_type==4):
                        if(index_template==1):
                                B = 40
                                T = 3
                                D = 50
                                t = 2
                                P = 8
                                Q = 4
                                H = 100
                                TISec = TISection(D, B, T, t, P, Q, H)
                                _place = TISec.place(origin, uDir, shaftDir)
                                point = TISec.compute_params()
                                prism = TISec.create_model()
                                display.DisplayShape(prism, update=True)
                        elif(index_template==2):
                                B = 50
                                T = 3
                                D = 70
                                t = 2
                                H = 100
                                d = (B - 2*T - t)/2
                                s = (D - t)/2
                                CrossISec = cross_isection(D, B, T, t, H, s, d)
                                CrossISec.place(origin, uDir, shaftDir)
                                CrossISec.compute_params()
                                prism = CrossISec.create_model()
                                display.DisplayShape(prism, update=True)
                        elif(index_template==3):
                                A = 50
                                B = 30
                                H = 50
                                t = 2
                                s = 30
                                s1 = 50
                                box = Box(A, B, t, H, s, s1)
                                _place = box.place(origin, uDir, wDir)
                                point = box.compute_params()
                                prism = box.create_model()
                                display.DisplayShape(prism, update=True)
                elif(index_type==5):
                        B = 20
                        T = 2
                        D = 40
                        t = 1.5
                        T1 = 2
                        t1 = 2
                        H = 60
                        b = 20
                        d = 50
                        s = 15
                        isection_channel = ISectionChannel(D, B, T, t, T1, t1, d, b, H, s)
                        _place = isection_channel.place(origin, uDir, shaftDir)
                        point = isection_channel.compute_params()
                        prism = isection_channel.create_model()
                        display.DisplayShape(prism, update=True)
                display.ExportToImage("./ResourceFiles/images/3DSectionfromSectionModeller.png")
        
        def update_section_properties(self,index_type,index_template):
                '''
                Method to fill output parameters to Section Properties
                '''
                conn = sqlite3.connect(PATH_TO_DATABASE)
                if(index_type==1):                                              # I-Section Side-by-Side
                        cursor = conn.execute("SELECT D,B,T,tw,Area FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        D,B,T,t,A=map(float,cursor.fetchall()[0])
                        s=float(self.SectionParameters.parameterText_3.text())/10
                        l=float(self.SectionParameters.parameterText_6.text())/10
                        ti=float(self.SectionParameters.parameterText_7.text())/10
                        D/=10
                        B/=10
                        T/=10
                        t/=10
                        Di=D-(2*T)
                        Ai=(2*A)+(2*l*ti)
                        Ytop=Ybottom=(D+(2*ti))/2
                        Yleft=Yright=l/2
                        Zzz=(Ai/2)+(Ytop+Ybottom)
                        Zyy=(Ai/2)+(Yleft+Yright)
                        Izz=(
                                (2*(((B*(T**3))/12)+(B*T*((Ybottom-ti-(T/2))**2))))+
                                (((l*(ti**3))/12)+(l*ti*((Ybottom-(ti/2))**2)))+
                                (2*(((t*((Di/2)**3))/12)+((Di/2)*t*((Ytop-T-ti-(T/2))**2))))+
                                (2*(((B*(T**3))/12)+(B*T*((Ytop-ti-(T/2))**2))))+
                                (((l*(ti**3))/12)+(l*ti*((Ytop-(ti/2))**2)))
                        )
                        Iyy=(
                                (((ti*((l/2)**3))/6)+((l/2)*ti*((Yleft-(l/2))**2)))+
                                (2*(((T*(B**3))/12)+(B*T*((Yleft-(B/2))**2))))+
                                (((Di*(t**3))/12)+(Di*t*((Yleft-(B/2))**2)))+
                                (((Di*(t**3))/12)+(Di*t*((Yright-(B/2))**2)))+
                                (2*(((T*(B**3))/12)+(B*T*((Yright-(B/2))**2))))+
                                (2*(((ti*((l/2)**3))/12)+((l/2)*ti*((Yright-(l/4))**2))))
                        )
                        Rzz=math.sqrt(Izz/Ai)
                        Ryy=math.sqrt(Iyy/Ai)
                        Zpz=(
                                (2*l*t*(Ytop-(ti/2)))+
                                (4*B*T*(Ytop-ti-(T/2)))+
                                (4*(Di/2)*t*(Ytop-T-ti-(Di/4)))
                        )
                        Zpy=(
                                (4*(l/2)*ti*(Yleft-(l/4)))+
                                (4*B*T*(Yleft-(B/2)))+
                                (2*Di*t*(Yleft*(B/2)))
                        )
                        self.Area_text.setText(str(round(Ai,4)))
                        parameters=[D,B,T,t,s,l,ti,50]
                                        
                        
                elif(index_type==2):                                                      # Channel Section
                        cursor = conn.execute("SELECT D,B,Area,T,tw FROM Channels where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        D,B,A,T,t=map(float,cursor.fetchall()[0])
                        s=float(self.SectionParameters.parameterText_3.text())/10
                        l=float(self.SectionParameters.parameterText_6.text())/10
                        tc=float(self.SectionParameters.parameterText_7.text())/10
                        D/=10
                        B/=10
                        T/=10
                        t/=10
                        Dc=D-(2*T)
                        Ac=(2*A)+(2*l*tc)
                        Ytop=Ybottom=(D+(2*tc))/2
                        Yleft=Yright=l/2
                        Zpz=(
                                (2*l*tc*(Ybottom-(tc/2)))+
                                (4*B*T*(Ybottom-tc-(T/2)))+
                                (4*(Dc/2)*t*(Ybottom-tc-T-(Dc/4)))
                        )
                        Zzz=(Ac/2)*(Ytop+Ybottom)
                        Zyy=(Ac/2)*(Yleft+Yright)

                        if(index_template==1):                                            # Face to Face
                                Izz=(
                                        (2*(((B*(T**3))/12)+(B*T*((Ybottom-(T/2)-tc)**2))))+
                                        (2*(((t*((Dc/2)**3))/12)+((Dc/2)*t*((Ybottom-T-tc-(Dc/4))**2))))+
                                        (2*(((t*((Dc/2)**3))/12)+((Dc/2)*t*((Ytop-T-tc-(T/2))**2))))+
                                        (2*(((B*(T**3))/12)+(B*T*((Ytop-tc-(T/2))**2))))+
                                        (((l*(tc**3))/12)+(l*tc*((Ybottom-(tc/2))**2)))+
                                        (((l*(tc**3))/12)+(l*tc*((Ytop-(tc/2))**2)))
                                )
                                Iyy=(
                                        (((Dc*(t**3))/12)+(Dc*t*((Yleft-(t/2))**2)))+
                                        (2*(((T*(B**3))/12)+(B*T*((Yleft-(B/2))**2))))+
                                        (2*(((T*(B**3))/12)+(B*T*((Yright-(B/2))**2))))+
                                        (2*(((Dc*(t**3))/12)+(Dc*t*((Yright-(t/2))**2))))+
                                        (2*(((tc*((l/2)**3))/12)+((l/2)*tc*((Yleft-(l/4))**2))))+
                                        (2*(((tc*((l/2)**3))/12)+((l/2)*tc*((Yright-(l/4))**2))))
                                )
                                Zpy=(
                                        (2*Dc*t*(Yleft-(t/2)))+
                                        (4*B*T*(Yleft-(B/2)))+
                                        (4*(l/2)*tc*(Yleft-(l/4)))
                                )
                                
                        elif(index_template==2):                                            # Back to Back
                                Izz=(
                                        (((l*(tc**3))/12)+(l*tc*((Ybottom-(tc/2))**2)))+
                                        (2*(((B*(T**3))/12)+(B*T*((Ybottom-(T/2)-tc)**2))))+
                                        (2*(((t*((Dc/2)**3))/12)+((Dc/2)*t*((Ybottom-(D/4)-T-tc)**2))))+
                                        (2*(((B*(T**3))/12)+(B*T*((Ytop-(T/2)-tc)**2))))+
                                        (((l*(tc**3))/12)+(l*tc*((Ytop-(tc/2))**2)))
                                )
                                Iyy=(
                                        (2*(((tc*((l/2)**3))/12)+((l/2)*tc*((Yleft-(l/4))**2))))+
                                        (2*(((T*(B**3))/12)+(B*T*((Yleft-(B/2))**2))))+
                                        (((Dc*(t**3))/12)+(Dc*t*((Yleft-(t/2)-B)**2)))+
                                        (((Dc*(t**3))/12)+(Dc*t*((Yright-(t/2)-B)**2)))+
                                        (2*(((T*(B**3))/12)+(B*T*((Yright-(B/2))**2))))+
                                        (2*(((tc*((l/2)**3))/12)+((l/2)*tc*((Yright-(l/4))**2))))
                                )
                                Zpy=(
                                        (4*(l/2)*tc*(Yleft-(l/4)))+
                                        (4*B*T*(Yleft-(B/2)))+
                                        (2*Dc*t*(Yleft-B+(t/2)))
                                )
                        
                        parameters=[D,B,T,t,s,l,tc,50]
                        Rzz=math.sqrt(Izz/Ac)
                        Ryy=math.sqrt(Iyy/Ac)
                        self.Area_text.setText(str(round(Ac,4)))


                elif(index_type==3):                                                         # Angle Section
                        if(index_template==1):                                                       #Star Configuration 4 Angles
                                cursor = conn.execute("SELECT a,b,t,Area FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                a,b,t,A = map(float,cursor.fetchall()[0])
                                ta=float(self.SectionParameters.parameterText_7.text())/10
                                l=float(self.SectionParameters.parameterText_6.text())/10
                                a/=10
                                b/=10
                                t/=10
                                l=2*a
                                Da=a-t                                
                                Aa=(4*A)+(l*ta)
                                Yleft=Yright=((2*b)+ta)/2
                                Ytop=Ybottom=l/2
                                Izz=(
                                (((ta*((l/2)**3))/12)+((l/2)*ta*((Ybottom-(l/4))**2)))+  
                                (2*(((t*(Da**3))/12)+(Da*t*((Ybottom-(Da/2))**2))))+
                                (2*(((b*(t**3))/12)+(b*t*((Ybottom-(t/2)-Da)**2))))+
                                (2*(((b*(t**3))/12)+(b*t*((Ytop-(t/2)-Da)**2))))+
                                (2*(((t*(Da**3))/12)+(Da*t*((Ytop-(Da/2))**2))))+
                                (((ta*((l/2)**3))/12)+((l/2)*ta*((Ytop-(l/4))**2)))
                                )
                                Iyy=(
                                        (2*(((t*(b**3))/12)+(b*t*((Yleft-(b/2))**2))))+
                                        (2*(((t*(b**3))/12)+(b*t*((Yright-(b/2))**2))))+
                                        (2*(((Da*(t**3))/12)+(Da*t*((Yleft+(t/2)-b)**2))))+
                                        (2*(((Da*(t**3))/12)+(Da*t*((Yright+(t/2)-b)**2))))+
                                        (((l*((ta/2)**3))/12)+(l*(ta/2)*((Yleft-(t/4))**2)))+
                                        (((l*((ta/2)**3))/12)+(l*(ta/2)*((Yright-(t/4))**2)))
                                )
                                Rzz=math.sqrt(Izz/Aa)
                                Ryy=math.sqrt(Iyy/Aa)
                                Zzz=(Aa/2)*(Ytop+Ybottom)
                                Zyy=(Aa/2)*(Yleft+Yright)
                                Zpz=(
                                        (2*(l/2)*ta*(Ybottom-(l/4)))+
                                        (4*b*t*(Ybottom-Da-(ta/2)))+
                                        (4*Da*t*(Ybottom-(Da/2)))
                                )
                                Zpy=(
                                        (2*(ta/2)*l*(Yleft-b-(ta/4)))+
                                        (4*b*t*(Yleft-(b/2)))+
                                        (4*Da*t*(Yleft-b+(t/2)))
                                )
                                parameters=[a,b,t,l,ta,50]
                                
                        elif(index_template==2):                                                   #Star Configuration 2 Angles
                                cursor = conn.execute("SELECT a,b,t,Area FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                a,b,t,A = map(float,cursor.fetchall()[0])
                                ta=float(self.SectionParameters.parameterText_7.text())/10
                                l=float(self.SectionParameters.parameterText_6.text())/10
                                a/=10
                                b/=10
                                t/=10
                                Da=a-t
                                Aa=(2*A)+(l*ta)
                                Ytop=Ybottom=l/2
                                Yleft=Yright=((2*b)+ta)/2
                                Izz=(
                                        (((ta*((l/2))**3)+(((l/2)*ta)*((Ybottom-(l/4))**2))))+
                                        ((t*(Da**3)/12)+((Da*t)*((Ybottom-(Da/2))**2)))+
                                        ((b*(t**3)/12)+((b*t)*((Ybottom-(t/2)-Da)**2)))+
                                        ((b*(t**3)/12)+((b*t)*((Ytop-(t/2)-Da)**2)))+
                                        ((t*(Da**3)/12)+((Da*t)*((Ytop-Da-(t/2))**2)))+
                                        (((ta*((l/2))**3)+(((l/2)*ta)*((Ytop-(l/4))**2))))
                                )
                                Iyy=(
                                        (((t*(b**3)/12)+((b*t)*((Yleft-(b/2))**2))))+
                                        (((Da*(t**3)/12)+((Da*t)*((Yleft+(t/2)-b)**2))))+
                                        (((l*((ta/2)**3)/12)+(((ta/2)*l)*((Yleft-(t/4)-b)**2))))+
                                        (((l*((ta/2)**3)/12)+(((ta/2)*l)*((Yright-(t/4)-b)**2))))+
                                        (((Da*(t**3)/12)+((Da*t)*((Yright+(t/2)-b)**2))))+
                                        (((t*(b**3)/12)+((b*t)*((Yright-(b/2))**2))))
                                )                                
                                Zpz=(
                                        (2*Da*t*(Ybottom-(Da/2)))+
                                        (2*b*t*(Ybottom-Da-(t/2)))+
                                        (2*(l/2)*ta*(Ybottom-(l/4)))
                                )
                                Zpy=(
                                        (2*b*t*(Yleft-(b/2)))+
                                        (2*l*(ta/2)*(Yleft-b-(ta/4)))+
                                        (2*Da*t*(Yleft-b+(t/2)))
                                )
                                parameters=[a,b,t,l,ta,50]
                        
                        elif(index_template==3):                                                        # 2 Angles on Same side
                                cursor = conn.execute("SELECT a,b,t,Area,Iy,Cy FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                a,b,t,A,Iy,Cy = map(float,cursor.fetchall()[0])
                                ta=float(self.SectionParameters.parameterText_7.text())/10
                                l=float(self.SectionParameters.parameterText_6.text())/10
                                a/=10
                                b/=10
                                t/=10
                                Da=a-t
                                Aa=(2*A)+(l*ta)
                                Ytop=Ybottom=l/2
                                Yleft=((
                                        (l*ta*-(ta/2))+
                                        (2*(Da*t*(ta+(t/2))))+
                                        (2*(b*t*(ta+(b/2))))
                                )/((l*ta)+(2*b*t)+(2*Da*t)))
                                Yright=(2*b)+ta-Yleft
                                Izz=(
                                        (((ta*((l/2)**3)/12)+(((l/2)*ta)*((Ybottom-(l/4))**2))))+  
                                        (((t*(Da**3)/12)+((Da*t)*((Ybottom+(Da/2))**2))))+
                                        (((b*(t**3)/12)+((b*t)*((Ybottom-(t/2)-Da)**2))))+
                                        (((b*(t**3)/12)+((b*t)*((Ybottom-(t/2)-Da)**2))))+
                                        (((t*(Da**3)/12)+((Da*t)*((Ybottom+(Da/2))**2))))+
                                        (((ta*((l/2)**3)/12)+(((l/2)*ta)*((Ybottom-(l/4))**2))))
                                )
                                Iyy=2*(Iy+(Aa*((Cy+(ta/2))**2)))
                                Zpz=(
                                        (2*(l/2)*ta*(Ybottom-(l/4)))+
                                        (2*b*t*(Ybottom-Da-(t/2)))+
                                        (2*Da*t*(Ybottom-(Da/4)))
                                )
                                Zpy=(
                                        (2*(ta/2)*l*(Yright-b-(ta/4)))+
                                        (2*b*t*(Yright-(b/2)))+
                                        (2*Da*t*(Yright-b+(t/2)))
                                )
                                parameters=[a,b,t,l,ta,50]              
                        elif(index_template==4):                                                        # 2 Angles on opposite side
                                cursor = conn.execute("SELECT a,b,t,Area,Iz,Cz FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                a,b,t,A,Iz,Cz = map(float,cursor.fetchall()[0])
                                ta=float(self.SectionParameters.parameterText_7.text())/10
                                l=float(self.SectionParameters.parameterText_6.text())/10
                                a/=10
                                b/=10
                                t/=10
                                Da=a-t
                                Aa=(2*A)+(l*ta)
                                Ybottom=((
                                        (2*Da*t*(Da/2))+
                                        (2*b*t*(Da+(t/2)))+
                                        (l*ta*(l/2))
                                )/((2*Da*t)+(2*b*t)+(l*ta)))
                                Ytop=Da+t-Ybottom
                                Yleft=Yright=((2*b)+ta)/2
                                Izz=2*(Iz+(Aa*((Cz+(ta/2))**2)))
                                Iyy=(
                                        (((t*(b**3)/12)+((b*t)*((Yleft-(b/2))**2))))+
                                        (((Da*(t**3)/12)+((Da*t)*((Yleft+(t/2)-b)**2))))+
                                        (((l*((ta/2)**3)/12)+(((ta/2)*l)*((Yleft-(ta/4)-b)**2))))+
                                        (((l*((ta/2)**3)/12)+(((ta/2)*l)*((Yright-(t/4)-b)**2))))+
                                        (((Da*(t**3)/12)+((Da*t)*((Yright+(t/2)-b)**2))))+
                                        (((t*(b**3)/12)+((b*t)*((Yright-(b/2))**2))))
                                )
                                Zpz=(
                                        (2*(l/2)*ta*(Ytop-(l/4)))+
                                        (2*b*t*(Ytop-(t/2)))+
                                        (2*(Da/2)*t*(Ybottom-(Da/4)))
                                )
                                Zpy=(
                                        (2*(ta/2)*l*(Yleft-b-(t/4)))+
                                        (2*b*t*(Yleft-(b/2)))+
                                        (2*Da*t*(Yleft-b+(t/2)))
                                )
                                parameters=[a,b,t,l,ta,50]
                        elif(index_template==5):                                                        # Box Angle
                                cursor = conn.execute("SELECT a,b,t,Area FROM Angles where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                a,b,t,A = map(float,cursor.fetchall()[0])  
                                s=float(self.SectionParameters.parameterText_3.text())/10
                                sa=float(self.SectionParameters.parameterText_4.text())/10
                                ta=float(self.SectionParameters.parameterText_7.text())/10
                                l=float(self.SectionParameters.parameterText_5.text())/10
                                la=float(self.SectionParameters.parameterText_6.text())/10
                                a/=10
                                b/=10
                                t/=10
                                Da=a-t
                                Aa=(4*A)+(l*ta)+(la*ta)
                                Ytop=Ybottom=((2*a)+(2*ta))/2
                                Yleft=Yright=l/2                                
                                Izz=(
                                        ((l*(ta**3)/12)+(l*t)*((Ybottom-(ta/2))**2))+  
                                        (2*((b*(t**3)/12)+(b*t)*((Ybottom-(t/2)-ta)**2)))+
                                        (2*((t*(Da**3)/12)+(Da*t)*((Ybottom-(Da/2)-ta-t)**2)))+
                                        (2*((t*(Da**3)/12)+(Da*t)*((Ytop-(Da/2)-ta-t)**2)))+
                                        (2*((b*(t**3)/12)+(b*t)*((Ytop-(t/2)-ta)**2)))+
                                        ((l*(ta**3)/12)+(l*ta)*((Ytop-(ta/2))**2))+  
                                        (2*((ta*(((la/2)**3)/12))+(((la/2)*ta)*((Ybottom-(l/4))**2))))+
                                        (2*((ta*(((la/2)**3)/12))+(((la/2)*ta)*((Ybottom-(l/4))**2))))

                                )
                                Iyy=(
                                        ((la*(ta**3)/12)+(la*ta)*((Yleft-(ta/2))**2))+
                                        (2*((Da*(t**3)/12)+(Da*t)*((Yleft-(t/2)-ta)**2)))+
                                        (2*((t*(b**3)/12)+(b*t)*((Yleft-(b/2)-ta)**2)))+
                                        (2*((ta*((l/2)**3)/12)+((l/2)*ta)*((Yleft-(l/4))**2)))+  
                                        (2*((t*(b**3)/12)+(b*t)*((Yright-(b/2)-ta)**2)))+
                                        (2*((Da*(t**3)/12)+(Da*t)*((Yright-(t/2)-ta)**2)))+
                                        (2*((ta*((l/2)**3)/12)+((l/2)*ta)*((Yright-(l/4))**2)))+ 
                                        ((la*(ta**3)/12)+(la*ta)*((Yright-(ta/2))**2))
                                )
                                Zpz=(
                                        (4*(la/2)*ta*(Ybottom-(l/4)))+
                                        (2*l*ta*(Ybottom-(ta/2)))+
                                        (4*Da*t*(Ybottom-t-ta-(Da/2)))+
                                        (4*b*t*(Ybottom-ta-(t/2)))
                                )
                                Zpy=(
                                        (4*(l/2)*ta*(Yleft-(l/4)))+
                                        (4*b*t*(Yleft-ta-(b/2)))+
                                        (4*Da*t*(Yleft-ta-(t/2)))+
                                        (2*la*ta*(Yleft-(ta/2)))
                                )
                                parameters=[a,b,t,l,ta,la,50,s,sa]
                        Ryy=math.sqrt(Iyy/Aa)
                        Rzz=math.sqrt(Izz/Aa)
                        Zzz=(Aa/2)*(Ytop+Ybottom)
                        Zyy=(Aa/2)*(Yleft+Yright)
                        self.Area_text.setText(str(round(Aa,4)))
                                
                elif(index_type==4):                                                    # Built-up Section
                        if(index_template==1):                                                # I-Section with stiffening
                                cursor = conn.execute("SELECT D,B,T,tw,Area FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                D,B,T,t,A=map(float,cursor.fetchall()[0])
                                P,Q=float(self.SectionParameters.parameterText_6.text())/10,float(self.SectionParameters.parameterText_7.text())/10
                                D/=10
                                B/=10
                                T/=10
                                t/=10
                                Db=D-(2*T)                                
                                Ab=A+(2*P*Q)
                                Ybottom=(
                                        (B*T*T/2)+
                                        (t*D*(D/2)*t)+
                                        (B*T*(B+T+(T/2)))+
                                        (2*Q*P*((2*T)+D-(P/2)))
                                )/((B*T)+(t*D)+(B*T)+(2*Q*P))
                                Yleft=Yright=B/2
                                Ybottom=(
                                        (B*T*(T/2))+
                                        (t*Db*((Db/2)+T))+
                                        (B*T*(Db+T+(T/2)))+
                                        (2*T*P*(T+Db+T-(P/2)))
                                ) 
                                Ytop=D-Ybottom
                                Izz=(
                                        ((B*(T**3)/12)+(B*T)*((Ybottom-(T/2))**2))+
                                        (2*((t*(Db**3)/12)+(Db*T)*((Db-(Db/2)-Ybottom)**2)))+
                                        ((B*(T**3)/12)+(B*T)*((Ytop-(T/2))**2))+
                                        (2*((Q*(P**3)/12)+(Q*P)*((Ytop-(P/2))**2)))
                                        )
                                Iyy=(
                                        ((P*(Q**3)/12)+(P*Q)*((Yleft-(Q/2))**2))+
                                        (2*((T*((B/2)**3)/12)+((B/2)*T)*((Yleft-(B/4))**2)))+
                                        (2*((T*((B/2)**3)/12)+((B/2)*T)*((Yright-(B/4))**2)))+
                                        ((Db*((t/2)**3)/12)+(Db*t/2)*((Yleft-(B/2)+(t/4))**2))+
                                        ((Db*((t/2)**3)/12)+(Db*t/2)*((Yright-(B/2)+(t/4))**2))+
                                        ((P*(Q**3)/12)+(P*Q)*((Yright-(Q/2))**2))
                                )
                                Zpz=(
                                        (B*T*(Ybottom-(T/2)))+
                                        (t*(Db/2))*(Ybottom-T-(Db/4))+
                                        (t*(Db/2)*(Ytop-T-(Db/4)))+
                                        (B*T*(Ytop-(T/2)))+
                                        (P*T*(Ytop-(P/2)))
                                )
                                Zpy=(
                                        (P*Q*(Yleft-(Q/2)))+
                                        (2*B*T*(Yleft-Q-(B/2)))+
                                        (Db*t*(Yleft-(B/2)))
                                )
                                parameters=[D,B,T,t,P,Q,50]
                        elif(index_template==2):                                                # I-Section from plates
                                cursor = conn.execute("SELECT D,B,T,tw,Area FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                D,B,T,t,A=map(float,cursor.fetchall()[0])
                                s=float(self.SectionParameters.parameterText_3.text())/10
                                da=float(self.SectionParameters.parameterText_6.text())/10
                                D/=10
                                t/=10
                                B/=10
                                T/=10
                                d=(B-(2*T)-t)/2
                                Db=D-(2*T)
                                Ab=(2*A)-(t**2)
                                Ytop=Ybottom=D/2
                                Yleft=Yright=B/2
                                Izz=(
                                        ((B*(T**3)/12)+(B*T)*((Ybottom-(T/2))**2))+
                                        (2*((T*((Db/2)**3)/12)+((Db/2)*T)*((Ybottom-(Db/4)-T)**2)))+
                                        ((t*((Db/2)**3)/12)+((Db/2)*t)*((Ybottom-(Db/4)-T)**2))+
                                        (2*((d*((t/2)**3)/12)+((t/2)*d)*((Ybottom-(Db/2)-T+(t/4))**2)))+
                                        (2*((d*((t/2)**3)/12)+((t/2)*d)*((Ytop-(Db/2)-T+(t/4))**2)))+
                                        (2*((T*((Db/2)**3)/12)+((Db/2)*T)*((Ytop-(Db/4)-T)**2)))+
                                        ((t*((Db/2)**3)/12)+((Db/2)*t)*((Ytop-(Db/2)-T)**2))+
                                        ((B*(T**3)/12)+(B*T)*((Ytop-(T/2))**2))
                                )
                                Iyy=(
                                        ((Db*(T**3)/12)+(Db*T)*((Yleft-(T/2))**2))+
                                        (2*((T*((B/2)**3)/12)+((B/2)*T)*((Yleft-(B/4))**2)))+
                                        (2*((T*((B/2)**3)/12)+((B/2)*T)*((Yright-(B/4))**2)))+
                                        ((t*(d**3)/12)+((t*d)*((Yleft-(d/2)-T)**2)))+
                                        ((t*(d**3)/12)+((t*d)*((Yright-(d/2)-T)**2)))+
                                        ((Db*((t/2)**3)/12)+((t/2)*Db)*((Yleft-(t/4)-T-d)**2))+
                                        ((Db*((t/2)**3)/12)+((t/2)*Db)*((Yright-(t/4)-T-d)**2))+
                                        ((Db*(T**3)/12)+(Db*T)*((Yright-(T/2))**2))
                                )                        
                                Zpz=(
                                        (2*B*T*(Ybottom-(T/2)))+
                                        (4*T*(Db/2)*(Ybottom-T-(Db/4)))+
                                        (2*t*(Db/2)*(Ybottom-T-(Db/4)))+
                                        (d*(t/2)*(Ybottom-(Db/2)))
                                )
                                Zpy=(
                                        (2*Db*T*(Yleft-(T/2)))+
                                        (2*d*t*(Yleft-T-(d/2)))+
                                        (2*Db*(t/2)*(Yleft-d-T-(t/4)))+
                                        (4*T*(B/2)*(Yleft-(B/4)))
                                )
                                parameters=[D, B, T, t,50, s, da]

                        elif(index_template==3):                                              # Built-up Box Section
                                cursor = conn.execute("SELECT B,tw FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                                B,t=map(float,cursor.fetchall()[0])
                                s=float(self.SectionParameters.parameterText_3.text())/10
                                sa=float(self.SectionParameters.parameterText_4.text())/10
                                B/=10
                                t/=10
                                A=Ab=4*B*t
                                Ytop=Ybottom=Yright=Yleft=B/2
                                Izz=(
                                        ((B*(t**3)/12)+(B*t*((Ybottom-(t/2))**2)))+
                                        ((B*(t**3)/12)+(B*t*((Ytop-(t/2))**2)))+
                                        (2*(((((B/2)**3)*t/12))+(((B/2)*t)*((Ybottom-t-(B/4))**2))))+
                                        (2*(((((B/2)**3)*t/12))+(((B/2)*t)*((Ytop-t-(B/4))**2))))
                                )
                                Iyy=(
                                        ((B*(t**3)/12)+(B*t*((Yleft-(t/2))**2)))+
                                        ((B*(t**3)/12)+(B*t*((Yright-(t/2))**2)))+
                                        (2*(((((B/2)**3)+t)/12)+(((B/2)*t)*((Yleft-t-(B/4))**2))))+
                                        (2*(((((B/2)**3)+t)/12)+(((B/2)*t)*((Yright-t-(B/4))**2))))
                                )
                                Zpz=(
                                        (2*B*t*(Ybottom-(t/2)))+
                                        (4*t*(B/2)*(Ybottom-(B/4)))
                                )
                                Zpy=(
                                        (2*t*(B/2)*(Yleft-(B/4)))+
                                        (2*B*t*(Yleft-(t/2)))
                                )
                                parameters=[A, B, t, 50, s, sa]
                        Rzz=math.sqrt(Izz/Ab)
                        Ryy=math.sqrt(Iyy/Ab)
                        Zzz=(Ab/2)*(Ytop+Ybottom)
                        Zyy=(Ab/2)*(Yleft+Yright)
                        self.Area_text.setText(str(round(Ab,4)))
                                
                elif(index_type==5):                                            #Compound Section
                        cursor = conn.execute("SELECT D,B,T,tw,Area FROM Columns where Designation="+repr(self.SectionParameters.parameterText_1.currentText()))
                        D,B,T,t,Ai=map(float,cursor.fetchall()[0])
                        s=float(self.SectionParameters.parameterText_3.text())/10
                        B/=10
                        T/=10
                        t/=10
                        D/=10
                        Di=D-(2*T)
                        cursor = conn.execute("SELECT D,B,Area,T,tw FROM Channels where Designation="+repr(self.SectionParameters.parameterText_2.currentText()))
                        d,b,a,Tc,tc = map(float,cursor.fetchall()[0])
                        b/=10
                        Tc/=10
                        tc/=10
                        d/=10
                        dc=d-(2*Tc)
                        A = Ai+a
                        Ybottom=((
                                (B*T*T/2)+
                                ((t*Di)*((Di/2)+T))+
                                (B*T*(Di+T+(T/2)))+
                                (dc*tc*(Di+(2*T)+(tc/2)))+
                                (b*Tc*(D+tc))
                        )/((2*B*T)+(2*b*Tc)+(dc*tc)+(Di*t)))
                        Ytop=(D+tc)-Ybottom
                        Yleft=Yright=d/2
                        Izz=(
                                ((B*(T**3)/12)+((B*T)*((Ybottom-((T/2)**2)))))+
                                ((t*((Di/2)**3)/12)+(t*(Di/2))+((Ybottom-T-(Di/4))**2))+
                                ((t*((Di/2)**3)/12)+(t*(Di/2))+((Ytop-T-(Di/4))**2))+
                                ((B*(T**3)/12)+(B*T)*((Ytop-tc-(T/2))**2))+
                                ((dc*(tc**3)/12)+(dc*tc)*((Ytop-(tc/2))**2))+
                                (2*((Tc*(b**3)/12)+((b*Tc)*((Ytop-(b/2))**2))))
                        )
                        Iyy=(
                                ((b*(Tc**3)/12)+(b*Tc*((Yleft-(Tc/2))**2)))+
                                ((tc*((dc/2)**3)/12)+((dc/2)*tc*((Yleft-T-(dc/4))**2)))+
                                (2*((T*((B/2)**3)/12)+((B/2)*T*((Yleft-T-(B/4))**2))))+
                                ((Di*((tc/2)**3)/12)+((tc/2)*Di*((Yleft-(t/4)-(d/2))**2)))+
                                ((Di*((tc/2)**3)/12)+((tc/2)*Di*((Yright-(t/4)-(d/2))**2)))+
                                (2*((T*((B/2)**3)/12)+((B/2)*T*((Yright-T-(B/4))**2))))+
                                ((tc*((dc/2)**3)/12)+((dc/2)*tc*((Yright-T-(dc/4))**2)))+
                                ((b*(Tc**3)/12)+(b*Tc*((Yright-(Tc/2))**2)))


                        )
                        Rzz=math.sqrt(Izz/A)
                        Ryy=math.sqrt(Iyy/A)
                        Zyy=A*(Yleft+Yright)/2
                        Zzz=A*(Ytop+Ybottom)/2
                        
                        Zpz=(
                                (B*T*(Ybottom-(T/2)))+
                                (t*(D/2)*(Ybottom-T-(D/4)))+
                                (t*(D/2)*(Ytop-T-tc-(D/4)))+
                                (d*t*(Ytop-(tc/2)))+
                                (2*b*T*(Ytop-(b/2)))
                        )
                        Zpy=(
                                (2*D*T*(Yleft-(T/2)))+
                                (2*d*t*(Yleft-T-(d/2)))+
                                (2*D*(t/20)*(Yleft-d-T-(t/4)))+
                                (4*T*(B/2)*(Yleft-(B/4)))
                        )
                        self.Area_text.setText(str(round(A,4)))
                        parameters=[D, B, T, t, Tc, tc, d, b, 50, s]

                Cy=Ybottom
                Cz=Yleft    
                self.PSM_text1.setText(str(round(Zpz,4)))
                self.PSM_text2.setText(str(round(Zpy,4)))
                self.C_text1.setText(str(round(Cz,4)))
                self.C_text2.setText(str(round(Cy,4)))
                self.MI_text1.setText(str(round(Izz,4)))
                self.MI_text2.setText(str(round(Iyy,4)))
                self.RG_text1.setText(str(round(Rzz,4)))
                self.RG_text2.setText(str(round(Ryy,4)))
                self.ESM_text1.setText(str(round(Zzz,4)))
                self.ESM_text2.setText(str(round(Zyy,4)))
                display.EraseAll()
                self.create_cad_model(index_type,index_template,parameters)

        def init_display(self):
                '''
                Method to initialize the OCC Display
                '''
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
                return display
        
        def get_section_properties(self):
                '''
                Method to get the values and names of the Section properties,
                for the currently selected Type and Template,
                in a dictionary
                '''
                symbols=['A','Izz','Iyy','Rzz','Ryy','Cz','Cy','Zpz','Zpy','Zzz','Zyy']
                Properties={}
                
                for child,symbol in zip(self.section_properties.findChildren(QtWidgets.QLineEdit),symbols):
                        Properties[symbol]=child.text()                
                return(Properties) 
        
        def import_to_modeller(self):
                '''
                Method to Handle Import button click. 
                This file helps select .osm files in the system and import them directly into the 
                modeller and automatically creates run all processes from the .osm file.
                '''
                fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Section Design",None, "InputFiles(*.osm)")
                if(fileName==''):
                        return
                reply=QtWidgets.QMessageBox.question(QtWidgets.QMessageBox(),'Alert!','Further proceedings will lead to a loss of the current unsaved data. Do you wish to continue?',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
                if(reply==QtWidgets.QMessageBox.No):
                        return
                with open(fileName,'r') as file:
                        parameters=eval(file.read())
                index_type,index_template=parameters['Section_Type'],parameters['Section_Template']
                self.section_type_combobox.setCurrentIndex(index_type)
                self.section_template_combobox.setCurrentIndex(index_template)
                self.section_designation_lineEdit.setText(parameters['Section_Designation'])
                self.Parameters=parameters['Section_Parameters']
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

                for child in self.Parameters:
                        self.SectionParameters.textBoxVisible[child]=self.Parameters[child]                        
                        if(child=='parameterText_1' or child=='parameterText_2'):
                                exec('self.SectionParameters.'+child+'.setCurrentText('+repr(self.Parameters[child][1])+')')
                        else:
                                exec('self.SectionParameters.'+child+'.setText('+repr(self.Parameters[child][1])+')')

                self.update_section_properties(index_type,index_template)
                self.disable_usability(False)

        def save_to_osm(self):
                '''
                Method to save Section Modeller Design data to .osm file 
                of desired location.
                '''
                designation=str(self.section_designation_lineEdit.text())
                if(designation==''):
                        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(),'Error','Please provide a Section Designation for the designed section and try again.')
                        return
                else:
                        reply=QtWidgets.QMessageBox.question(QtWidgets.QMessageBox(),'INFO','The File saves by the same name as the Section Designation.Click Yes to Continue or No and change the Section Designation.',QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
                if(reply==QtWidgets.QMessageBox.No):
                        return
                else:
                        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a Folder")
                        if(os.path.isfile(folder+'/'+designation+'.osm')):
                                QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(),'Error','A file with the same name exists in the provided folder.')
                                return
                        else:
                                parameters={}
                                parameters['Section_Type']=self.section_type_combobox.currentIndex()
                                parameters['Section_Template']=self.section_template_combobox.currentIndex()
                                parameters['Section_Parameters']=self.Parameters
                                parameters['Section_Designation']=designation
                                parameters['Section_Properties']=self.get_section_properties()
                                
                                with open(folder+'/'+designation+'.osm','w') as file:
                                        file.write(pprint.pformat(parameters))    
                                QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'INFO','File Succesfully saved.')

        def export_to_pdf(self):
                '''
                Method to send information from section modeller into Latex creator
                '''
                designation=str(self.section_designation_lineEdit.text())
                if(designation==''):
                        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(),'Error','Please provide a Section Designation for the designed section and try again.')
                        return
                self.summary_dialog=SummaryDialog()
                dialog=QtWidgets.QDialog()
                self.summary_dialog.setupUi(dialog)
                dialog.exec()
                try:
                        input_summary=self.summary_dialog.input_summary
                        input_summary['Define Section']={
                                'Section Designation':designation,
                                'Section Type':str(self.section_type_combobox.currentText()),
                                'Section Template':str(self.section_template_combobox.currentText()),
                                'Section Parameters':self.Parameters,
                        }
                        input_summary['Section Properties']=self.get_section_properties()
                        rel_path = str(sys.path[0])
                        rel_path = rel_path.replace("\\", "/")
                        Disp_3D_image = "/ResourceFiles/images/3DSectionfromSectionModeller.png"
                        latex=CreateLatex()
                        latex.save_latex(input_summary,input_summary['filename'],rel_path,Disp_3D_image)
                        if os.path.isfile(str(input_summary['filename']+'.pdf')) and not os.path.isfile(input_summary['filename']+'.log'):
                                QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(), 'Information', 'Design report saved!')            
                        else:
                                logfile=open(input_summary['filename']+'.log','r')
                                logs=logfile.read()
                                if('! I can\'t write on file' in logs):
                                        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), 'Error', 'Please make sure no PDF is open with same name and try again.')
                                else:
                                        print(logs)
                                        QtWidgets.QMessageBox.critical(QtWidgets.QMessageBox(), 'Error', 'Latex Creation Error. If this error persists send us the log file created in the same folder choosen for the Design Report.')
                                logfile.close()            
                except KeyError:
                        pass

        def retranslateUi(self, Dialog):
                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
                self.label_14.setText(_translate("Dialog", "Define Section"))
                self.label_15.setText(_translate("Dialog", "Section Type:"))
                self.label_16.setText(_translate("Dialog", "Section Template:"))
                self.label_17.setText(_translate("Dialog", "Section Parameters:"))
                self.label_18.setText(_translate("Dialog", "Section Designation:"))
                self.section_type_combobox.setItemText(0, _translate("Dialog", "----------Select Type----------"))
                self.section_type_combobox.setItemText(1, _translate("Dialog", "I-Section"))
                self.section_type_combobox.setItemText(2, _translate("Dialog", "Channel Section"))
                self.section_type_combobox.setItemText(3, _translate("Dialog", "Angle Section"))
                self.section_type_combobox.setItemText(4, _translate("Dialog", "Built-Up Section"))
                self.section_type_combobox.setItemText(5, _translate("Dialog", "Compound Section"))
                self.parametersBtn.setText(_translate("Dialog", "Enter/Edit Parameters"))
                self.label_13.setText(_translate("Dialog", "Section Properties"))
                self.Area_label.setText(_translate("Dialog", "<html><head/><body><p>Area, a(cm<span style=\" vertical-align:super;\">2</span>):</p></body></html>"))
                self.MI_label1.setText(_translate("Dialog", "<html><head/><body><p>Moment of Inertia, I_zz(cm<span style=\" vertical-align:super;\">4</span>):</p></body></html>"))
                self.MI_label2.setText(_translate("Dialog", "<html><head/><body><p>Moment of Inertia, I_yy(cm<span style=\" vertical-align:super;\">4</span>):</p></body></html>"))
                self.RG_label1.setText(_translate("Dialog", "Radius of Gyration, r_zz(cm):"))
                self.RG_label2.setText(_translate("Dialog", "Radius of Gyration, r_yy(cm):"))
                self.C_label1.setText(_translate("Dialog", "Centriod, c_z(cm):"))
                self.C_label2.setText(_translate("Dialog", "Centriod, c_y(cm):"))
                self.PSM_label1.setText(_translate("Dialog", "<html><head/><body><p>Plastic Section modulus, Z_pz(cm<span style=\" vertical-align:super;\">3</span>):</p></body></html>"))
                self.PSM_label2.setText(_translate("Dialog", "<html><head/><body><p>Plastic Section modulus, Z_py(cm<span style=\" vertical-align:super;\">3</span>):</p></body></html>"))
                self.ESM_label1.setText(_translate("Dialog", "<html><head/><body><p>Elastic Section modulus, Z_zz(cm<span style=\" vertical-align:super;\">3</span>):</p></body></html>"))
                self.ESM_label2.setText(_translate("Dialog", "<html><head/><body><p>Elastic Section modulus, Z_yy(cm<span style=\" vertical-align:super;\">3</span>):</p></body></html>"))
                self.importBtn.setText(_translate("Dialog","Import"))
                self.saveBtn.setText(_translate("Dialog", "Save"))
                self.exportBtn.setText(_translate("Dialog", "Export"))

if __name__ == "__main__":
        import sys
        app =QtWidgets.QApplication(sys.argv)
        ui=Ui_OsdagSectionModeller()
        screen_resolution=app.desktop().screenGeometry()
        dialog=QtWidgets.QDialog()
        ui.setupUi(dialog)
        dialog.resize(900,780)
        if(screen_resolution.width()<1025):
                measure=screen_resolution.height()-120
                dialog.resize(measure*45//39,measure)
        dialog.exec_()
        app.exec_()
