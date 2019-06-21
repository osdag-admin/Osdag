# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_weld_details_2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Weld_Details_2(object):
    def setupUi(self, Weld_Details_2):
        Weld_Details_2.setObjectName("Weld_Details_2")
        Weld_Details_2.resize(298, 202)
        self.lineEdit_flange_critical_stress = QtWidgets.QLineEdit(Weld_Details_2)
        self.lineEdit_flange_critical_stress.setGeometry(QtCore.QRect(170, 40, 113, 25))
        self.lineEdit_flange_critical_stress.setObjectName("lineEdit_flange_critical_stress")
        self.lineEdit_flange_strength = QtWidgets.QLineEdit(Weld_Details_2)
        self.lineEdit_flange_strength.setGeometry(QtCore.QRect(170, 70, 113, 25))
        self.lineEdit_flange_strength.setObjectName("lineEdit_flange_strength")
        self.lineEdit_web_critical_stress = QtWidgets.QLineEdit(Weld_Details_2)
        self.lineEdit_web_critical_stress.setGeometry(QtCore.QRect(170, 140, 113, 25))
        self.lineEdit_web_critical_stress.setObjectName("lineEdit_web_critical_stress")
        self.lineEdit_web_strength = QtWidgets.QLineEdit(Weld_Details_2)
        self.lineEdit_web_strength.setGeometry(QtCore.QRect(170, 170, 113, 25))
        self.lineEdit_web_strength.setObjectName("lineEdit_web_strength")
        self.label = QtWidgets.QLabel(Weld_Details_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Weld_Details_2)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 141, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Weld_Details_2)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 111, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Weld_Details_2)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 161, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Weld_Details_2)
        self.label_5.setGeometry(QtCore.QRect(10, 170, 111, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Weld_Details_2)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.line = QtWidgets.QFrame(Weld_Details_2)
        self.line.setGeometry(QtCore.QRect(-33, 93, 351, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(Weld_Details_2)
        QtCore.QMetaObject.connectSlotsByName(Weld_Details_2)

    def retranslateUi(self, Weld_Details_2):
        _translate = QtCore.QCoreApplication.translate
        Weld_Details_2.setWindowTitle(_translate("Weld_Details_2", "Fillet Weld Details"))
        self.label.setText(_translate("Weld_Details_2", "Flange Welds"))
        self.label_2.setText(_translate("Weld_Details_2", "Critical Stress (MPa)"))
        self.label_3.setText(_translate("Weld_Details_2", "Strength (MPa)"))
        self.label_4.setText(_translate("Weld_Details_2", "Critical Stress (MPa)"))
        self.label_5.setText(_translate("Weld_Details_2", "Strength (MPa)"))
        self.label_6.setText(_translate("Weld_Details_2", "Web Welds"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Weld_Details_2 = QtWidgets.QDialog()
    ui = Ui_Weld_Details_2()
    ui.setupUi(Weld_Details_2)
    Weld_Details_2.show()
    sys.exit(app.exec_())

