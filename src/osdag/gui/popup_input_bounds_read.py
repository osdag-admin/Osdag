from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QFormLayout, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class RangeInputDialogRead(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Range Input")
        self.setFixedSize(350, 230)  # Increased height to accommodate larger inputs
        self.set_styles()

        self.values = []

        self.lower_input = QLineEdit()
        self.upper_input = QLineEdit()
        self.step_input = QLineEdit()

        # Set font and height for better clarity
        for widget in [self.lower_input, self.upper_input, self.step_input]:
            widget.setFont(QFont("Segoe UI", 13))  # Larger font
            widget.setFixedHeight(44)              # Taller input box

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)

        lower_label = QLabel("Lower Bound:")
        upper_label = QLabel("Upper Bound:")
        step_label = QLabel("Step:")

        for label in [lower_label, upper_label, step_label]:
            label.setFont(QFont("Segoe UI", 11))

        form_layout.addRow(lower_label, self.lower_input)
        form_layout.addRow(upper_label, self.upper_input)
        form_layout.addRow(step_label, self.step_input)

        self.setLayout(form_layout)

    def set_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 11pt;
            }
            QLineEdit {
                font-size: 13pt;
                padding: 6px 10px;
                border: 1px solid #aaa;
                border-radius: 4px;
            }
        """)

    def show_error(self, message):
        QMessageBox.warning(self, "Input Error", message)

    def get_values(self):
        return self.values

    def set_read_only_values(self, lower, upper, step):
        """Populates the fields with given values and makes them uneditable."""
        self.lower_input.setText(str(lower))
        self.upper_input.setText(str(upper))
        self.step_input.setText(str(step))

        self.lower_input.setReadOnly(True)
        self.upper_input.setReadOnly(True)
        self.step_input.setReadOnly(True)

    def set_custom_title(self, title):
        """Sets a custom title for the dialog window."""
        self.setWindowTitle(title)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = RangeInputDialogRead()
    dialog.set_custom_title("Display Sensor Range")
    dialog.set_read_only_values(10.0, 100, 10)
    dialog.exec_()