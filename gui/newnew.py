# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newnew.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from Common import *

class Ui_Form(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(607, 598)
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(30, 30, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(330, 30, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.listWidget = QtWidgets.QListWidget(MainWindow)
        self.listWidget.setGeometry(QtCore.QRect(20, 80, 211, 271))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(MainWindow)
        self.listWidget_2.setGeometry(QtCore.QRect(330, 80, 211, 271))
        self.listWidget_2.setObjectName("listWidget_2")
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(240, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 180, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 230, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 280, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 400, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.update_buttons_status()
        self.connections()
        # def plt_thk():
        #     self.addAvailableItems(VALUES_PLATETHK_CUSTOMIZED)
        #
        # def diam_bolt():
        #     lst = self.connectdb1()
        #     self.addAvailableItems(lst)
        #

        self.lst = self.connectdb1()
        self.addAvailableItems(self.lst)



    def all_list(self):
        self.lst = self.connectdb1()
        return self.lst
    def connections(self):
        self.listWidget.itemSelectionChanged.connect(self.update_buttons_status)
        self.listWidget_2.itemSelectionChanged.connect(self.update_buttons_status)
        self.pushButton_2.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.pushButton_3.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.pushButton_4.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.pushButton.clicked.connect(self.on_mButtonToSelected_clicked)
        self.pushButton_5.clicked.connect(self.get_right_elements)

    def connectdb1(self):
        lst = []
        conn = sqlite3.connect('C:/Users/pc/Desktop/demo database/DBbolt.db')
        cursor = conn.execute("SELECT Bolt_diameter FROM Bolt")
        rows = cursor.fetchall()
        for row in rows:
            lst.append(row)
        l2 = self.convert_list(lst)
        return l2

    def convert_list(self, tl):
        arr = []
        for v in tl:
            val = ''.join(v)
            arr.append(val)
        return arr

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Available:"))
        self.label_2.setText(_translate("MainWindow", "Selected:"))
        self.pushButton.setText(_translate("MainWindow", ">>"))
        self.pushButton_2.setText(_translate("MainWindow", ">"))
        self.pushButton_3.setText(_translate("MainWindow", "<"))
        self.pushButton_4.setText(_translate("MainWindow", "<<"))
        self.pushButton_5.setText(_translate("MainWindow", "Submit"))

    def update_buttons_status(self):
        self.pushButton_2.setDisabled(not bool(self.listWidget.selectedItems()) or self.listWidget_2.currentRow() == 0)
        self.pushButton_3.setDisabled(not bool(self.listWidget_2.selectedItems()))

    def on_mBtnMoveToAvailable_clicked(self):
        self.listWidget_2.addItem(self.listWidget.takeItem(self.listWidget.currentRow()))

    def on_mBtnMoveToSelected_clicked(self):
        self.listWidget.addItem(self.listWidget_2.takeItem(self.listWidget_2.currentRow()))

    def on_mButtonToAvailable_clicked(self):
        while self.listWidget_2.count() > 0:
            self.listWidget.addItem(self.listWidget_2.takeItem(0))

    def on_mButtonToSelected_clicked(self):
        while self.listWidget.count() > 0:
            self.listWidget_2.addItem(self.listWidget.takeItem(0))

    def addAvailableItems(self, items):
        self.listWidget.addItems(items)

    def get_left_elements(self):
        r = []
        for i in range(self.listWidget.count()):
            it = self.listWidget.item(i)
            r.append(it.text())
        return r

    def get_right_elements(self):
        r = []
        for i in range(self.listWidget_2.count()):
            it = self.listWidget_2.item(i)
            r.append(it.text())
        print(r)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWidow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWidow)
    MainWidow.show()
    sys.exit(app.exec_())
