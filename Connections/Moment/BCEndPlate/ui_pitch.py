# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_pitch.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Pitch(object):
    def setupUi(self, Pitch):
        Pitch.setObjectName("Pitch")
        Pitch.resize(332, 393)
        Pitch.setMinimumSize(QtCore.QSize(300, 200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        Pitch.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Pitch)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Pitch)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 299, 383))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 0, 1, 10, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_2.addWidget(self.line_6, 0, 3, 10, 1)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 4, 1, 1)
        self.lbl_mem = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem.setFont(font)
        self.lbl_mem.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem.setObjectName("lbl_mem")
        self.gridLayout_2.addWidget(self.lbl_mem, 1, 0, 1, 1)
        self.lbl_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_1.setFont(font)
        self.lbl_1.setObjectName("lbl_1")
        self.gridLayout_2.addWidget(self.lbl_1, 1, 2, 1, 1)
        self.lineEdit_pitch = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch.setFont(font)
        self.lineEdit_pitch.setReadOnly(True)
        self.lineEdit_pitch.setObjectName("lineEdit_pitch")
        self.gridLayout_2.addWidget(self.lineEdit_pitch, 1, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 5, 1, 1)
        self.lbl_mem2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem2.setFont(font)
        self.lbl_mem2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem2.setObjectName("lbl_mem2")
        self.gridLayout_2.addWidget(self.lbl_mem2, 2, 0, 1, 1)
        self.lbl_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_2.setFont(font)
        self.lbl_2.setObjectName("lbl_2")
        self.gridLayout_2.addWidget(self.lbl_2, 2, 2, 1, 1)
        self.lineEdit_pitch2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch2.setFont(font)
        self.lineEdit_pitch2.setReadOnly(True)
        self.lineEdit_pitch2.setObjectName("lineEdit_pitch2")
        self.gridLayout_2.addWidget(self.lineEdit_pitch2, 2, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 5, 1, 1)
        self.lbl_mem3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lbl_mem3.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem3.setFont(font)
        self.lbl_mem3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem3.setObjectName("lbl_mem3")
        self.gridLayout_2.addWidget(self.lbl_mem3, 3, 0, 1, 1)
        self.lbl_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_3.setFont(font)
        self.lbl_3.setObjectName("lbl_3")
        self.gridLayout_2.addWidget(self.lbl_3, 3, 2, 1, 1)
        self.lineEdit_pitch3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch3.setFont(font)
        self.lineEdit_pitch3.setReadOnly(True)
        self.lineEdit_pitch3.setObjectName("lineEdit_pitch3")
        self.gridLayout_2.addWidget(self.lineEdit_pitch3, 3, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 3, 5, 1, 1)
        self.lbl_mem4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem4.setFont(font)
        self.lbl_mem4.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem4.setObjectName("lbl_mem4")
        self.gridLayout_2.addWidget(self.lbl_mem4, 4, 0, 1, 1)
        self.lbl_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_4.setFont(font)
        self.lbl_4.setObjectName("lbl_4")
        self.gridLayout_2.addWidget(self.lbl_4, 4, 2, 1, 1)
        self.lineEdit_pitch4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch4.setFont(font)
        self.lineEdit_pitch4.setReadOnly(True)
        self.lineEdit_pitch4.setObjectName("lineEdit_pitch4")
        self.gridLayout_2.addWidget(self.lineEdit_pitch4, 4, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 4, 5, 1, 1)
        self.lbl_mem5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem5.setFont(font)
        self.lbl_mem5.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem5.setObjectName("lbl_mem5")
        self.gridLayout_2.addWidget(self.lbl_mem5, 5, 0, 1, 1)
        self.lbl_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_5.setFont(font)
        self.lbl_5.setObjectName("lbl_5")
        self.gridLayout_2.addWidget(self.lbl_5, 5, 2, 1, 1)
        self.lineEdit_pitch5 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch5.setFont(font)
        self.lineEdit_pitch5.setReadOnly(True)
        self.lineEdit_pitch5.setObjectName("lineEdit_pitch5")
        self.gridLayout_2.addWidget(self.lineEdit_pitch5, 5, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 5, 5, 1, 1)
        self.lbl_mem6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem6.setFont(font)
        self.lbl_mem6.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem6.setObjectName("lbl_mem6")
        self.gridLayout_2.addWidget(self.lbl_mem6, 6, 0, 1, 1)
        self.lbl_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_6.setFont(font)
        self.lbl_6.setObjectName("lbl_6")
        self.gridLayout_2.addWidget(self.lbl_6, 6, 2, 1, 1)
        self.lineEdit_pitch6 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch6.setFont(font)
        self.lineEdit_pitch6.setReadOnly(True)
        self.lineEdit_pitch6.setObjectName("lineEdit_pitch6")
        self.gridLayout_2.addWidget(self.lineEdit_pitch6, 6, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 6, 5, 1, 1)
        self.lbl_mem7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem7.setFont(font)
        self.lbl_mem7.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem7.setObjectName("lbl_mem7")
        self.gridLayout_2.addWidget(self.lbl_mem7, 7, 0, 1, 1)
        self.lbl_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_7.setFont(font)
        self.lbl_7.setObjectName("lbl_7")
        self.gridLayout_2.addWidget(self.lbl_7, 7, 2, 1, 1)
        self.lineEdit_pitch7 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch7.setFont(font)
        self.lineEdit_pitch7.setReadOnly(True)
        self.lineEdit_pitch7.setObjectName("lineEdit_pitch7")
        self.gridLayout_2.addWidget(self.lineEdit_pitch7, 7, 4, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 7, 5, 1, 1)
        self.lbl_mem7_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem7_2.setFont(font)
        self.lbl_mem7_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem7_2.setObjectName("lbl_mem7_2")
        self.gridLayout_2.addWidget(self.lbl_mem7_2, 8, 0, 1, 1)
        self.lbl_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_8.setFont(font)
        self.lbl_8.setObjectName("lbl_8")
        self.gridLayout_2.addWidget(self.lbl_8, 8, 2, 1, 1)
        self.lineEdit_pitch8 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch8.setFont(font)
        self.lineEdit_pitch8.setReadOnly(True)
        self.lineEdit_pitch8.setObjectName("lineEdit_pitch8")
        self.gridLayout_2.addWidget(self.lineEdit_pitch8, 8, 4, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 8, 5, 1, 1)
        self.lbl_mem7_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lbl_mem7_3.setFont(font)
        self.lbl_mem7_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_mem7_3.setObjectName("lbl_mem7_3")
        self.gridLayout_2.addWidget(self.lbl_mem7_3, 9, 0, 1, 1)
        self.lbl_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lbl_9.setFont(font)
        self.lbl_9.setObjectName("lbl_9")
        self.gridLayout_2.addWidget(self.lbl_9, 9, 2, 1, 1)
        self.lineEdit_pitch9 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.lineEdit_pitch9.setFont(font)
        self.lineEdit_pitch9.setReadOnly(True)
        self.lineEdit_pitch9.setObjectName("lineEdit_pitch9")
        self.gridLayout_2.addWidget(self.lineEdit_pitch9, 9, 4, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 9, 5, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 10, 0, 1, 6)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Pitch)
        QtCore.QMetaObject.connectSlotsByName(Pitch)

    def retranslateUi(self, Pitch):
        _translate = QtCore.QCoreApplication.translate
        Pitch.setWindowTitle(_translate("Pitch", "Pitch Details"))
        self.label.setText(_translate("Pitch", "Sr. No."))
        self.label_2.setText(_translate("Pitch", "Designation"))
        self.label_5.setText(_translate("Pitch", "Pitch (mm)"))
        self.lbl_mem.setText(_translate("Pitch", "1"))
        self.lbl_1.setText(_translate("Pitch", "Pitch 1-2"))
        self.lbl_mem2.setText(_translate("Pitch", "2"))
        self.lbl_2.setText(_translate("Pitch", "Pitch 2-3"))
        self.lbl_mem3.setText(_translate("Pitch", "3"))
        self.lbl_3.setText(_translate("Pitch", "Pitch 3-4"))
        self.lbl_mem4.setText(_translate("Pitch", "4"))
        self.lbl_4.setText(_translate("Pitch", "Pitch 4-5"))
        self.lbl_mem5.setText(_translate("Pitch", "5"))
        self.lbl_5.setText(_translate("Pitch", "Pitch 5-6"))
        self.lbl_mem6.setText(_translate("Pitch", "6"))
        self.lbl_6.setText(_translate("Pitch", "Pitch 6-7"))
        self.lbl_mem7.setText(_translate("Pitch", "7"))
        self.lbl_7.setText(_translate("Pitch", "Pitch 7-8"))
        self.lbl_mem7_2.setText(_translate("Pitch", "8"))
        self.lbl_8.setText(_translate("Pitch", "Pitch 8-9"))
        self.lbl_mem7_3.setText(_translate("Pitch", "9"))
        self.lbl_9.setText(_translate("Pitch", "Pitch 9-10"))
        self.textEdit.setHtml(_translate("Pitch", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Note:</span> \'Pitch i-j\' stands for vertical pitch distance between centre lines of i<span style=\" vertical-align:super;\">th</span> and j<span style=\" vertical-align:super;\">th</span> rows of bolts numbered from top.</p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Pitch = QtWidgets.QDialog()
    ui = Ui_Pitch()
    ui.setupUi(Pitch)
    Pitch.show()
    sys.exit(app.exec_())
