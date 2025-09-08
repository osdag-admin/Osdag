"""
Additional Inputs button for Osdag GUI.
Simple clickable button with clean styling.
"""
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal

class AdditionalInputsButton(QPushButton):
    button_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__("Additional Inputs", parent)
        
        # Connect click signal
        self.clicked.connect(self.button_clicked.emit)
        
        # Styling
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-weight: bold; 
                border-radius: 5px;
                border: 1px solid black;
                padding: 5px 14px;
                text-align: center;
                # font-family: "Calibri";
            }
            QPushButton:hover {
                background-color: #90AF13;
                border: 1px solid #90AF13;
                color: white;
            }
            QPushButton:pressed {
                color: black;
                background-color: white;
                border: 1px solid black;
            }
        """)

