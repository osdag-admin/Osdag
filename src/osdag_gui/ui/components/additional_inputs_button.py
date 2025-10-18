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
        self.setObjectName("additional_input_btn")
