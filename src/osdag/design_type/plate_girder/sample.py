from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFormLayout,
    QApplication, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

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


# Run for test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = RangeInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        print("Returned values:", dialog.get_values())
    sys.exit(app.exec_())
