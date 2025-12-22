from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from .widgets import My_ListWidget

scale = 1  # For resizing components

class RangeInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Range Input")
        self.setFixedSize(350, 200)
        self.set_styles()

        self.values = []

        self.lower_input = QLineEdit()
        self.upper_input = QLineEdit()
        self.step_input = QLineEdit()

        for widget in [self.lower_input, self.upper_input, self.step_input]:
            widget.setFont(QFont("Segoe UI", 11))  # Slightly larger font
            widget.setFixedHeight(32)              # Increased height

        # Form layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)

        lower_label = QLabel("Lower Bound:")
        upper_label = QLabel("Upper Bound:")
        step_label = QLabel("Step:")

        for label in [lower_label, upper_label, step_label]:
            label.setFont(QFont("Segoe UI", 10))

        form_layout.addRow(lower_label, self.lower_input)
        form_layout.addRow(upper_label, self.upper_input)
        form_layout.addRow(step_label, self.step_input)

        self.submit_button = QPushButton("Add")
        self.submit_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.submit_button.clicked.connect(self.validate_and_submit)

        form_layout.addRow(self.submit_button)
        self.setLayout(form_layout)

    def set_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 10pt;
            }
            QLineEdit {
                font-size: 11pt;
                padding: 4px 6px;
                border: 1px solid #aaa;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #814c4c;
                color: white;
                font-size: 10pt;
                font-weight: bold;
                height: 28px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #a05c5c;
            }
        """)

    def validate_and_submit(self):
        lower_text = self.lower_input.text().strip()
        upper_text = self.upper_input.text().strip()
        step_text = self.step_input.text().strip()

        if not lower_text or not upper_text or not step_text:
            self.show_error("All fields must be filled.")
            return

        try:
            lower = float(lower_text)
            upper = float(upper_text)
            step = float(step_text)

            if step <= 0:
                self.show_error("Step must be greater than 0.")
                return

            self.values = [lower, upper, step]
            self.accept()

        except ValueError:
            self.show_error("Please enter valid numeric values.")

    def show_error(self, message):
        QMessageBox.warning(self, "Input Error", message)

    def get_values(self):
        return self.values

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
