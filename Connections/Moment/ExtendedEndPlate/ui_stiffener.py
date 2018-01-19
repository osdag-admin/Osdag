# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_stiffener.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Stiffener(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(246, 171)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.txt_stiffnrHeight = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txt_stiffnrHeight.setFont(font)
        self.txt_stiffnrHeight.setReadOnly(True)
        self.txt_stiffnrHeight.setObjectName("txt_stiffnrHeight")
        self.gridLayout.addWidget(self.txt_stiffnrHeight, 0, 1, 1, 1)
        self.plateHeight = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.plateHeight.setFont(font)
        self.plateHeight.setObjectName("plateHeight")
        self.gridLayout.addWidget(self.plateHeight, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txt_stiffnrLength = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txt_stiffnrLength.setFont(font)
        self.txt_stiffnrLength.setReadOnly(True)
        self.txt_stiffnrLength.setObjectName("txt_stiffnrLength")
        self.gridLayout.addWidget(self.txt_stiffnrLength, 1, 1, 1, 1)
        self.label_163 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_163.setFont(font)
        self.label_163.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_163.setObjectName("label_163")
        self.gridLayout.addWidget(self.label_163, 2, 0, 1, 1)
        self.txt_stiffnrThickness = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txt_stiffnrThickness.setFont(font)
        self.txt_stiffnrThickness.setReadOnly(True)
        self.txt_stiffnrThickness.setObjectName("txt_stiffnrThickness")
        self.gridLayout.addWidget(self.txt_stiffnrThickness, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Stiffener"))
        self.plateHeight.setText(_translate("Dialog", "Height (mm)"))
        self.label_2.setText(_translate("Dialog", "Length (mm)"))
        self.label_163.setText(_translate("Dialog", "<html><head/><body><p>Thickness (mm)</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Stiffener()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

