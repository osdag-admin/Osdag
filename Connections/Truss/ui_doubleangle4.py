# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_Doubleangle_Four.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Doubleangle_Four(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(345, 193)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_doub_leg = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBox_doub_leg.setFont(font)
        self.comboBox_doub_leg.setObjectName("comboBox_doub_leg")
        self.comboBox_doub_leg.addItem("")
        self.comboBox_doub_leg.addItem("")
        self.gridLayout.addWidget(self.comboBox_doub_leg, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.comboBx_doub_sides = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBx_doub_sides.setFont(font)
        self.comboBx_doub_sides.setObjectName("comboBx_doub_sides")
        self.comboBx_doub_sides.addItem("")
        self.comboBx_doub_sides.addItem("")
        self.gridLayout.addWidget(self.comboBx_doub_sides, 2, 2, 1, 1)
        self.comboBox_doub_selct_section = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBox_doub_selct_section.setFont(font)
        self.comboBox_doub_selct_section.setObjectName("comboBox_doub_selct_section")
        self.gridLayout.addWidget(self.comboBox_doub_selct_section, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.comboBox_doub_angle = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBox_doub_angle.setFont(font)
        self.comboBox_doub_angle.setObjectName("comboBox_doub_angle")
        self.comboBox_doub_angle.addItem("")
        self.comboBox_doub_angle.addItem("")
        self.comboBox_doub_angle.addItem("")
        self.gridLayout.addWidget(self.comboBox_doub_angle, 0, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Double angle"))
        self.comboBox_doub_leg.setItemText(0, _translate("Dialog", "Longer leg"))
        self.comboBox_doub_leg.setItemText(1, _translate("Dialog", "Shorter leg"))
        self.label.setText(_translate("Dialog", "Connectivity with gusset:"))
        self.comboBx_doub_sides.setItemText(0, _translate("Dialog", "Opposite sides"))
        self.comboBx_doub_sides.setItemText(1, _translate("Dialog", "Same side"))
        self.comboBox_doub_angle.setItemText(0, _translate("Dialog", "Angle type"))
        self.comboBox_doub_angle.setItemText(1, _translate("Dialog", "Equal angle"))
        self.comboBox_doub_angle.setItemText(2, _translate("Dialog", "Unequal angle"))
        self.btn_save.setText(_translate("Dialog", "Save"))
        self.btn_close.setText(_translate("Dialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Doubleangle_Four()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

