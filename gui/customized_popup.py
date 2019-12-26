# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newnew.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

#from .ui_template import *

class Ui_Popup(object):


    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(607, 598)
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(20, 50, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(370, 50, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.listWidget = QtWidgets.QListWidget(MainWindow)

        self.listWidget.setGeometry(QtCore.QRect(20, 80, 211, 271))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_2 = QtWidgets.QListWidget(MainWindow)
        self.listWidget_2.setGeometry(QtCore.QRect(370, 80, 211, 271))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setSortingEnabled(True)
        self.listWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(265, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(265, 180, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(265, 230, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(265, 280, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_5.setGeometry(QtCore.QRect(225, 400, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(14)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        #self.pushButton_5.clicked.connect(self.close_on_submit)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.update_buttons_status()
        self.connections()
        # self.KEY_EXISTINGVAL = self.get_right_elements()
        # print(self.KEY_EXISTINGVAL)
        #test_list = self.get_right_elements()

        # for i in range(0, len(test_list)):
        #     test_list[i] = int(test_list[i])
        # test_list.sort()
        # print(test_list)
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

    def connections(self):
        self.listWidget.itemSelectionChanged.connect(self.update_buttons_status)
        self.listWidget_2.itemSelectionChanged.connect(self.update_buttons_status)
        self.pushButton_2.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.pushButton_3.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.pushButton_4.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.pushButton.clicked.connect(self.on_mButtonToSelected_clicked)
        self.pushButton_5.clicked.connect(self.get_right_elements)
        #self.pushButton_5.clicked.connect(self.get_updated_list)


    def update_buttons_status(self):
        self.pushButton_2.setDisabled(not bool(self.listWidget.selectedItems()))
        self.pushButton_3.setDisabled(not bool(self.listWidget_2.selectedItems()))

    # def on_mBtnMoveToAvailable_clicked(self):
    #     self.listWidget_2.addItem(self.listWidget.takeItem(self.listWidget.currentRow()))
    #     # x = []
    #     # for i in range(len(items)):
    #     #     self.listWidget_2.addItem(self.listWidget.selectedItems()[i].text())
    #
    # def on_mBtnMoveToSelected_clicked(self):
    #     self.listWidget.addItem(self.listWidget_2.takeItem(self.listWidget_2.currentRow()))

    def on_mBtnMoveToAvailable_clicked(self):
        items = self.listWidget.selectedItems()
        for i in range(len(items)):
            self.listWidget_2.addItem(self.listWidget.selectedItems()[i].text())
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

    def on_mBtnMoveToSelected_clicked(self):
        items = self.listWidget_2.selectedItems()
        for i in range(len(items)):
            self.listWidget.addItem(self.listWidget_2.selectedItems()[i].text())
        for item in self.listWidget_2.selectedItems():
            self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def on_mButtonToAvailable_clicked(self):
        while self.listWidget_2.count() > 0:
            self.listWidget.addItem(self.listWidget_2.takeItem(0))
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))


    def on_mButtonToSelected_clicked(self):
        while self.listWidget.count() > 0:
            self.listWidget_2.addItem(self.listWidget.takeItem(0))


    def addAvailableItems(self,items,KEY_EXISTINGVAL_CUSTOMIZED):
        self.listWidget_2.clear()
        #self.listWidget_2.addItems(items)
        if items not in KEY_EXISTINGVAL_CUSTOMIZED:
            self.listWidget_2.addItems(KEY_EXISTINGVAL_CUSTOMIZED)
            a = list(set(items) - set(KEY_EXISTINGVAL_CUSTOMIZED))
            self.listWidget.addItems(a)
        else:
            self.listWidget_2.addItems(items)
    # def addAvailableItems1(self,items1,KEY_EXISTINGVAL_CUSTOMIZED):
    #     self.listWidget_2.clear()
    #     if items1 != KEY_EXISTINGVAL_CUSTOMIZED and KEY_EXISTINGVAL_CUSTOMIZED != []:
    #         self.listWidget_2.addItems(KEY_EXISTINGVAL_CUSTOMIZED)
    #     else:
    #         self.listWidget_2.addItems(items1)

    # def get_left_elements(self):
    #     r = []
    #     for i in range(self.listWidget.count()):
    #         it = self.listWidget.item(i)
    #
    #         r.append(it.text())
    #         r[i] = int(r[i])
    #     r.sort()
    #     return r

    def get_right_elements(self):
        r = []
        for i in range(self.listWidget_2.count()):
            it = self.listWidget_2.item(i)
            r.append(it.text())
        return r

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    # def on_pushButton_clicked():
    #     Mainwindow.exec_()
    ui = Ui_Popup()
    ui.setupUi(MainWindow)
    print(MainWindow.exec())
    print(ui.get_right_elements())
    print(1)
    sys.exit(app.exec_())
