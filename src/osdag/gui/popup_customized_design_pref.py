
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFormLayout,
    QApplication, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import re
import sys
scale = 1  # For resizing components
class My_ListWidget(QListWidget):
    def addItems(self, Iterable, p_str=None):
        super().addItems(Iterable)
        self.sortItems()

    def addItem(self, *__args):
        super().addItem(My_ListWidgetItem(__args[0]))
        self.sortItems()

class My_ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        try:
            self_text = str(re.sub("[^0-9.]", "", self.text()))
            other_text = str(re.sub("[^0-9.]", "", other.text()))
            return float(self_text) < float(other_text)
        except Exception:
            return super().__lt__(other)

class PopupDialog(QDialog):
    def __init__(self, disabled_values=[], note="", parent=None):
        super().__init__(parent)
        self.disabled_values = disabled_values
        self.note = note
        self.setWindowTitle("Customized")
        self.resize(int(scale*540), int(scale*470))
        self.init_ui()
        self.set_styles()

    def init_ui(self):
        self.label = QtWidgets.QLabel("Available:", self)
        self.label.setGeometry(QtCore.QRect(20, 20, 150, 30))

        self.label_2 = QtWidgets.QLabel("Selected:", self)
        self.label_2.setGeometry(QtCore.QRect(int(scale * 320), 20, 150, 30))

        self.listWidget = My_ListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(20, 50, int(scale*180), int(scale*300)))
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.itemDoubleClicked.connect(self.move_to_selected)

        self.listWidget_2 = My_ListWidget(self)
        self.listWidget_2.setGeometry(QtCore.QRect(int(scale*320), 50, int(scale*180), int(scale*300)))
        self.listWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_2.itemDoubleClicked.connect(self.move_to_available)

        self.pushButton = QtWidgets.QPushButton(">>", self)
        self.pushButton.setGeometry(QtCore.QRect(int(scale*225), int(scale*140), int(scale*70), int(scale*30)))

        self.pushButton_2 = QtWidgets.QPushButton(">", self)
        self.pushButton_2.setGeometry(QtCore.QRect(int(scale*225), int(scale*180), int(scale*70), int(scale*30)))

        self.pushButton_3 = QtWidgets.QPushButton("<", self)
        self.pushButton_3.setGeometry(QtCore.QRect(int(scale*225), int(scale*220), int(scale*70), int(scale*30)))

        self.pushButton_4 = QtWidgets.QPushButton("<<", self)
        self.pushButton_4.setGeometry(QtCore.QRect(int(scale*225), int(scale*260), int(scale*70), int(scale*30)))

        self.pushButton_5 = QtWidgets.QPushButton("Submit", self)
        self.pushButton_5.setGeometry(QtCore.QRect(int(scale*190), int(scale*400), int(scale*140), int(scale*35)))
        self.pushButton_5.setDefault(True)

        self.pushButton.clicked.connect(self.move_all_to_selected)
        self.pushButton_2.clicked.connect(self.move_selected_to_selected)
        self.pushButton_3.clicked.connect(self.move_selected_to_available)
        self.pushButton_4.clicked.connect(self.move_all_to_available)
        self.pushButton_5.clicked.connect(self.accept)

        self.listWidget.itemSelectionChanged.connect(self.update_buttons_status)
        self.listWidget_2.itemSelectionChanged.connect(self.update_buttons_status)

        self.update_buttons_status()

    def update_buttons_status(self):
        self.pushButton_2.setDisabled(not bool(self.listWidget.selectedItems()))
        self.pushButton_3.setDisabled(not bool(self.listWidget_2.selectedItems()))

    def move_selected_to_selected(self):
        for item in self.listWidget.selectedItems():
            self.listWidget_2.addItem(item.text())
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

    def move_selected_to_available(self):
        for item in self.listWidget_2.selectedItems():
            self.listWidget.addItem(item.text())
        for item in self.listWidget_2.selectedItems():
            self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def move_all_to_selected(self):
        while self.listWidget.count() > 0:
            self.listWidget_2.addItem(self.listWidget.takeItem(0).text())

    def move_all_to_available(self):
        while self.listWidget_2.count() > 0:
            self.listWidget.addItem(self.listWidget_2.takeItem(0).text())

    def move_to_selected(self, item):
        self.listWidget_2.addItem(item.text())
        self.listWidget.takeItem(self.listWidget.row(item))

    def move_to_available(self, item):
        self.listWidget.addItem(item.text())
        self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def get_selected_items(self):
        return [self.listWidget_2.item(i).text() for i in range(self.listWidget_2.count())]

    def set_styles(self):
        brown = "#925a5b"
        grey = "#8e8e8e"
        white = "#ffffff"

        button_style = f"""
        QPushButton {{
            background-color: {brown};
            color: {white};
            border-radius: 6px;
            font-size: 22px;
            padding: 6px 18px;
            border: none;
        }}
        QPushButton:disabled {{
            background-color: {grey};
            color: {white};
        }}
        """
        for btn in [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.pushButton_5]:
            btn.setStyleSheet(button_style)

        list_item_style = """
        QListWidget::item {
            font-size: 24px;
            color: black;
            margin: 2px 0px;
        }
        """
        scrollbar_style = f"""
        QScrollBar:vertical {{
            border: none;
            background: #f5f5f5;
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {grey};
            min-height: 20px;
            border-radius: 6px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            background: none;
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollBar:horizontal {{
            height: 0px;
        }}
        """
        self.listWidget.setStyleSheet(list_item_style + scrollbar_style)
        self.listWidget_2.setStyleSheet(list_item_style + scrollbar_style)