"""
Control Button Position Selector Dialog
Allows user to choose where window control buttons appear
"""
import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QRadioButton, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
import osdag_gui.resources.resources_rc


class ControlButtonPositionDialog(QDialog):
    def __init__(self, current_position="right", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName("ControlButtonPositionDialog")
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.old_pos = current_position
        self.setObjectName("win_control_btn_dialog")
        
        # Get theme manager from app
        app = QApplication.instance()
        self.theme = app.theme_manager
        
        # Set fixed size for the dialog
        self.setFixedSize(360, 200)
        
        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("Control Button Position")
        mainLayout.addWidget(self.titleBar)

        # Content widget
        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(20, 20, 20, 20)
        contentLayout.setSpacing(16)

        # Description label
        descLabel = QLabel("Choose where to display window control buttons:")
        descLabel.setWordWrap(True)
        contentLayout.addWidget(descLabel)

        # Radio button group
        radioLayout = QVBoxLayout()
        radioLayout.setSpacing(12)
        
        self.leftRadio = QRadioButton("Left side (macOS style)")
        self.leftRadio.setObjectName("LeftPositionRadio")
        radioLayout.addWidget(self.leftRadio)
        
        self.rightRadio = QRadioButton("Right side (Windows style)")
        self.rightRadio.setObjectName("RightPositionRadio")
        radioLayout.addWidget(self.rightRadio)
        
        # Set current selection
        if current_position == "left":
            self.leftRadio.setChecked(True)
        else:
            self.rightRadio.setChecked(True)
        
        contentLayout.addLayout(radioLayout)
        contentLayout.addStretch()

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(8)
        buttonLayout.setContentsMargins(0, 8, 0, 0)
        buttonLayout.addStretch()

        # Cancel button
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedHeight(32)
        self.cancelButton.setFixedWidth(80)
        self.cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.cancelButton)

        # Apply button
        self.applyButton = QPushButton("Apply")
        self.applyButton.setFixedHeight(32)
        self.applyButton.setFixedWidth(80)
        self.applyButton.clicked.connect(self.accept)
        buttonLayout.addWidget(self.applyButton)

        contentLayout.addLayout(buttonLayout)
        mainLayout.addWidget(contentWidget)

    def accept(self):
        """Override accept to update theme manager setting"""
        new_position = "left" if self.leftRadio.isChecked() else "right"
        self.theme.set_control_btn_pos(new_position)
        if self.old_pos != new_position:
            CustomMessageBox(
                title="Info",
                text="Restart the software to see the effect of setting.\n"
            ).exec()
        super().accept()