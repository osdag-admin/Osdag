# -*- coding: utf-8 -*-

# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(366, 248)
        Dialog.setMinimumSize(QtCore.QSize(350, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_html = QtWidgets.QLabel(Dialog)
        self.lbl_html.setObjectName("lbl_html")
        self.verticalLayout.addWidget(self.lbl_html)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.le_username = QtWidgets.QLineEdit(Dialog)
        self.le_username.setObjectName("le_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_username)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.le_password = QtWidgets.QLineEdit(Dialog)
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_password.setObjectName("le_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_password)
        self.verticalLayout.addLayout(self.formLayout)
        self.cb_remember = QtWidgets.QCheckBox(Dialog)
        self.cb_remember.setObjectName("cb_remember")
        self.verticalLayout.addWidget(self.cb_remember)
        self.bt_sign_in = QtWidgets.QPushButton(Dialog)
        self.bt_sign_in.setObjectName("bt_sign_in")
        self.verticalLayout.addWidget(self.bt_sign_in)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.verticalLayout.addWidget(self.label_5)

        self.verticalLayout.setSpacing(8)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setStyleSheet("font-size:9pt;font-family:consolas;")

        self.verticalLayout.addWidget(self.label_6)

        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setText("Don't know how to create a Token? "+'<a href=https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>Click here<a/>')
        self.verticalLayout.addWidget(self.label_7)
        self.label_7.setOpenExternalLinks(True)
        self.label_7.setStyleSheet("font-size:8pt;font-family:Arial;")

        self.label_9 = QtWidgets.QLabel(Dialog)
        self.verticalLayout.addWidget(self.label_9)
        self.hl1 = QtWidgets.QFrame(Dialog)
        self.hl1.setFrameShape(QtWidgets.QFrame.HLine)
        self.verticalLayout.addWidget(self.hl1)

        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setStyleSheet("font-size:8pt;font-family:Arial;")
        self.label_8.setText("Make sure token has atleast these two permissions:"+"\n \n"+"1. public_repo (To Access public repositories)"+"\n\n"+"2. gist (To Create gists)")
        self.verticalLayout.addWidget(self.label_8)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sign in to github"))
        self.lbl_html.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><img src=\":/rc/GitHub-Mark.png\"/></p><p align=\"center\">Sign in to GitHub</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Username:"))
        self.label_3.setText(_translate("Dialog", "Password: "))
        self.label_4.setText(_translate("Dialog", "Sign in using Personal Access Token"))
        self.label_5.setText(" ")
        self.label_6.setText(" ")
        self.cb_remember.setText(_translate("Dialog", "Remember me"))
        self.bt_sign_in.setText(_translate("Dialog", "Sign in"))

from . import qcrash_rc
