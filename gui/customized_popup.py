# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_customized_popup.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, qApp, QListWidget, QListWidgetItem, QApplication
import sys
import sqlite3
from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from get_DPI_scale import scale
#from .ui_template import *


class My_ListWidget(QListWidget):

    def addItems(self, Iterable, p_str=None):
        QListWidget.addItems(self, Iterable)

    def addItem(self, *__args):
        QListWidget.addItem(self, My_ListWidgetItem(__args[0]))


class My_ListWidgetItem(QListWidgetItem):

    def __lt__(self, other):
        try:
            import re
            self_text = str(re.sub("[^0-9]", "", self.text()))
            other_text = str(re.sub("[^0-9]", "", other.text()))
            return float(self_text) < float(other_text)
        except Exception:
            return QListWidgetItem.__lt__(self, other)


class Ui_Popup(object):


    def setupUi(self, MainWindow, disabled_values, note):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(scale*540, scale*470)
        self.disabled_values = disabled_values
        self.note = note
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(20, 20, 150, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(scale*320, 20, 150, 30))
        self.label_2.setObjectName("label_2")
        # self.listWidget = QtWidgets.QListWidget(MainWindow)
        self.listWidget = My_ListWidget(MainWindow)
        self.listWidget.setGeometry(QtCore.QRect(20, 50, scale*180, scale*300))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.itemDoubleClicked.connect(self.move_to_selected)
        # self.listWidget_2 = QtWidgets.QListWidget(MainWindow)
        self.listWidget_2 = My_ListWidget(MainWindow)

        self.listWidget_2.setGeometry(QtCore.QRect(scale*320, 50, scale*180, scale*300))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setSortingEnabled(True)
        self.listWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_2.itemDoubleClicked.connect(self.move_to_available)
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QtCore.QRect(scale*225, scale*140, scale*70, scale*30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setAutoDefault(False)
        self.pushButton_2 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(scale*225, scale*180, scale*70, scale*30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_3 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(scale*225, scale*220, scale*70, scale*30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_4 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(scale*225, scale*260, scale*70, scale*30))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_5 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_5.setGeometry(QtCore.QRect(scale*190, scale*400, scale*140, scale*35))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setDefault(True)
        if self.note != "":
            self.note_label = QtWidgets.QLabel(MainWindow)
            self.note_label.setGeometry(QtCore.QRect(20, scale * 450, scale * 320, scale * 150))
            self.note_label.setObjectName("note_label")
            self.note_label.setText("<b>Note</b>: "+self.note)
            self.note_label.setStyleSheet("background-color: white;")
            self.note_label.resize(QtCore.QSize(self.note_label.sizeHint()))
            MainWindow.resize(scale * 540, scale * 550)
        self.connections(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.update_buttons_status()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "Customized"))
        self.label.setText(_translate("MainWindow", "Available:"))
        self.label_2.setText(_translate("MainWindow", "Selected:"))
        self.pushButton.setText(_translate("MainWindow", ">>"))
        self.pushButton_2.setText(_translate("MainWindow", ">"))
        self.pushButton_3.setText(_translate("MainWindow", "<"))
        self.pushButton_4.setText(_translate("MainWindow", "<<"))
        self.pushButton_5.setText(_translate("MainWindow", "Submit"))

    def connections(self,MainWindow):
        self.listWidget.itemSelectionChanged.connect(self.update_buttons_status)
        self.listWidget_2.itemSelectionChanged.connect(self.update_buttons_status)
        self.pushButton_2.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.pushButton_3.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.pushButton_4.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.pushButton.clicked.connect(self.on_mButtonToSelected_clicked)
        self.pushButton_5.clicked.connect(self.get_right_elements)
        self.pushButton_5.clicked.connect(lambda: self.is_empty(MainWindow))

    def is_empty(self,MainWindow):

        # Function to check whether values are selected or not.
        # @author: Amir

        if len(self.get_right_elements()) == 0:
            self.error_message = QtWidgets.QMessageBox()
            self.error_message.setWindowTitle('Information')
            self.error_message.setIcon(QtWidgets.QMessageBox.Critical)
            self.error_message.setText('Please Select some values.')
            self.error_message.exec()
        else:
            MainWindow.close()


    def update_buttons_status(self):
        self.pushButton_2.setDisabled(not bool(self.listWidget.selectedItems()))
        self.pushButton_3.setDisabled(not bool(self.listWidget_2.selectedItems()))

    def on_mBtnMoveToAvailable_clicked(self):
        """
        Functions to move Values from Availabe listWidget to Selected ListWidget and vice versa on clicking the respective buttons
        """
        # @author : Arsil
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

    def on_mButtonToSelected_clicked(self):
        while self.listWidget.count() > 0:
            self.listWidget_2.addItem(self.listWidget.takeItem(0))


    def addAvailableItems(self,items,KEY_EXISTINGVAL_CUSTOMIZED):
        # Function to addItems from one listWidget to another

        # @author : Amir

        self.listWidget_2.clear()
        #self.listWidget_2.addItems(items)
        if items not in KEY_EXISTINGVAL_CUSTOMIZED:
            for item in KEY_EXISTINGVAL_CUSTOMIZED:
                # self.listWidget_2.addItems(KEY_EXISTINGVAL_CUSTOMIZED)
                if item in self.disabled_values:
                    continue
                self.listWidget_2.addItem(item)

            a = list(set(items) - set(KEY_EXISTINGVAL_CUSTOMIZED))
            for item_a in list(set(a + self.disabled_values)):
                self.listWidget.addItem(item_a)
            # self.listWidget.addItems(a)
        else:
            for it in items:
                self.listWidget_2.addItem(it)

        for all_items in [self.listWidget.item(i) for i in range(self.listWidget.count())]:
            if all_items.text() in self.disabled_values:
                all_items.setFlags(QtCore.Qt.NoItemFlags)

            # self.listWidget_2.addItems(items)
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

        # Function to get the selected (i.e. thr right elements) elements

        # @author: Amir




        r = []
        for i in range(self.listWidget_2.count()):
            it = self.listWidget_2.item(i)
            r.append(it.text())
        return r

    def move_to_selected(self, item):
        self.listWidget_2.addItem(item.text())
        self.listWidget.takeItem(self.listWidget.row(item))

    def move_to_available(self, item):
        self.listWidget.addItem(item.text())
        self.listWidget_2.takeItem(self.listWidget_2.row(item))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    # def on_pushButton_clicked():
    #     Mainwindow.exec_()
    ui = Ui_Popup()
    ui.setupUi(MainWindow)
    print(MainWindow.exec())
    sys.exit(app.exec_())
