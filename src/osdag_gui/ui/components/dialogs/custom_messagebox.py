import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QSizeGrip
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon, QPixmap

# for standalone testing
# from custom_titlebar import CustomTitleBar
# from resources_rc import *

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.resources.resources_rc import *

class MessageBoxType:
    Information = "Information"
    Warning = "Warning"
    Critical = "Critical"
    Success = "Success"
    About = "About"

class CustomMessageBox(QDialog):
    def __init__(self, title="Message", text="Message", informativeText="", buttons=["OK"], dialogType=MessageBoxType.Information):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("CustomDialog")

        # Base stylesheet for the dialog
        self.setStyleSheet(
            """
            QDialog {
                background-color: #ffffff;
                border: 1px solid #90AF13;
            }
        """
        )

        # Make dialog resizable
        self.setSizeGripEnabled(True)

        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle(title)
        mainLayout.addWidget(self.titleBar)

        # Content widget
        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(20, 20, 20, 20)
        contentLayout.setSpacing(8)

        # Icon and text layout
        contentInnerLayout = QHBoxLayout()
        self.iconLabel = QLabel(self)
        self.setIconForType(dialogType)
        contentInnerLayout.addWidget(self.iconLabel)

        # Text layout
        textLayout = QVBoxLayout()
        self.textLabel = QLabel(text, self)
        self.textLabel.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.textLabel.setAlignment(Qt.AlignLeft)
        textLayout.addWidget(self.textLabel)

        if informativeText:
            self.informativeLabel = QLabel(informativeText, self)
            self.informativeLabel.setStyleSheet("font-size: 12px; color: #555555;")
            self.informativeLabel.setAlignment(Qt.AlignLeft)
            self.informativeLabel.setWordWrap(True)
            textLayout.addWidget(self.informativeLabel)

        contentInnerLayout.addLayout(textLayout)
        contentLayout.addLayout(contentInnerLayout)

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(6)
        buttonLayout.setContentsMargins(0, 8, 0, 0)
        buttonLayout.addStretch()

        # Button styling based on dialog type
        buttonStyle = self.getButtonStyleForType(dialogType)
        self.buttonMap = {}
        for buttonText in buttons:
            button = QPushButton(buttonText, self)
            button.setFixedHeight(30)
            button.setStyleSheet(buttonStyle)
            button.clicked.connect(lambda checked, txt=buttonText: self.buttonClicked(txt))
            buttonLayout.addWidget(button, alignment=Qt.AlignmentFlag.AlignRight)
            self.buttonMap[buttonText] = button

        contentLayout.addLayout(buttonLayout)
        mainLayout.addWidget(contentWidget)

        self.result = None
        self.dialogType = dialogType

    def setIconForType(self, dialogType):
        # Use Qt's standard icons (replace with custom paths if needed)
        icon_map = {
            MessageBoxType.Information: ":/vectors/msg_info.svg",
            MessageBoxType.Warning: ":/vectors/msg_warning.svg",
            MessageBoxType.Success: ":/vectors/msg_success.svg",
            MessageBoxType.Critical: ":/vectors/msg_critical.svg",
            MessageBoxType.About: ":/vectors/msg_about.svg"
        }
        icon_path = icon_map.get(dialogType, icon_map[MessageBoxType.Information])
        self.iconLabel.setPixmap(QIcon(icon_path).pixmap(32, 32))
        self.iconLabel.setFixedSize(34, 34)
        self.iconLabel.setStyleSheet("margin-right: 2px;")

    def getButtonStyleForType(self, dialogType):
        # Define button styles based on dialog type
        style_map = {
            MessageBoxType.Information: """
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1E88E5;
                }
                QPushButton:pressed {
                    background-color: #1976D2;
                }
            """,
            MessageBoxType.Warning: """
                QPushButton {
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #FB8C00;
                }
                QPushButton:pressed {
                    background-color: #F57C00;
                }
            """,
            MessageBoxType.Critical: """
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #E53935;
                }
                QPushButton:pressed {
                    background-color: #D32F2F;
                }
            """,
            MessageBoxType.Success: """
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #45A049;
                }
                QPushButton:pressed {
                    background-color: #3D8B40;
                }
            """,
            MessageBoxType.About: """
                QPushButton {
                    background-color: #64B5F6;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #42A5F5;
                }
                QPushButton:pressed {
                    background-color: #2196F3;
                }
            """
        }
        return style_map.get(dialogType, style_map[MessageBoxType.Information])

    def buttonClicked(self, buttonText):
        self.result = buttonText
        self.accept()

    def exec(self):
        super().exec()
        return self.result


# Test different dialog types
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog_types = [
#         (MessageBoxType.Information, "Information", "This is an information message!", "Additional details here.", ["OK"]),
#         (MessageBoxType.Warning, "Warning", "This is a warning message!", "Proceed with caution.", ["OK", "Cancel"]),
#         (MessageBoxType.Success, "Success", "Successfully build This Application", "Version 1.0, Created by Me", ["OK"]),
#         (MessageBoxType.Critical, "Critical", "A critical error occurred!", "Please check your system.", ["Retry", "Cancel"]),
#         (MessageBoxType.About, "About", "About This Application", "Version 1.0, Created by Me", ["OK"])
#     ]
#     for dialog_type, title, text, informativeText, buttons in dialog_types:
#         msgBox = CustomMessageBox(
#             title=title,
#             text=text,
#             informativeText=informativeText,
#             buttons=buttons,
#             dialogType=dialog_type
#         )
#         result = msgBox.exec()
#         print(f"{dialog_type} Dialog result: {result}")