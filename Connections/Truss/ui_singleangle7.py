# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_singleangle.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Singleangle_Seven(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(341, 155)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_save = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btn_close.setFont(font)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        self.comboBox_sign_angle = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBox_sign_angle.setFont(font)
        self.comboBox_sign_angle.setObjectName("comboBox_sign_angle")
        self.comboBox_sign_angle.addItem("")
        self.comboBox_sign_angle.addItem("")
        self.comboBox_sign_angle.addItem("")
        self.gridLayout.addWidget(self.comboBox_sign_angle, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.comboBox_sign_selct_section = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBox_sign_selct_section.setFont(font)
        self.comboBox_sign_selct_section.setObjectName("comboBox_sign_selct_section")
        self.gridLayout.addWidget(self.comboBox_sign_selct_section, 1, 1, 1, 1)
        self.comboBox_sign_leg = QtWidgets.QComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBox_sign_leg.setFont(font)
        self.comboBox_sign_leg.setObjectName("comboBox_sign_leg")
        self.comboBox_sign_leg.addItem("")
        self.comboBox_sign_leg.addItem("")
        self.gridLayout.addWidget(self.comboBox_sign_leg, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Single angle"))
        self.btn_save.setText(_translate("Dialog", "Save"))
        self.btn_close.setText(_translate("Dialog", "Close"))
        self.comboBox_sign_angle.setItemText(0, _translate("Dialog", "Angle type"))
        self.comboBox_sign_angle.setItemText(1, _translate("Dialog", "Equal angle"))
        self.comboBox_sign_angle.setItemText(2, _translate("Dialog", "Unequal angle"))
        self.label.setText(_translate("Dialog", "Connectivity with gusset:"))
        self.comboBox_sign_leg.setItemText(0, _translate("Dialog", "Longer leg"))
        self.comboBox_sign_leg.setItemText(1, _translate("Dialog", "Shorter leg"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Singleangle_Seven()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

