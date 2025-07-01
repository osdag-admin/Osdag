from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


class AvailableThicknessDialog(QDialog):
    def __init__(self, thickness_list):
        super().__init__()
        self.setWindowTitle("Available Thicknesses")
        self.setFixedSize(1000, 200)  # Wider dialog box
        self.init_ui(thickness_list)
        self.set_styles()

    def init_ui(self, thickness_list):
        layout = QVBoxLayout()

        message = f"Available thicknesses by default - {thickness_list}"
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12pt;
                color: #333;
                padding: 10px;
            }
        """)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    default_thicknesses = ['8', '10', '12', '14', '16', '18', '20', '22', '25', '28', '32', '36', '40', '45', '50', '56', '63', '75', '80', '90', '100',
                        '110', '120']
    dialog = AvailableThicknessDialog(default_thicknesses)
    dialog.exec_()
