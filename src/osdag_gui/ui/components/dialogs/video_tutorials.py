import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QPixmap, QFont, QCursor, QDesktopServices
from PySide6.QtWidgets import QPushButton

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
import osdag_gui.resources.resources_rc
# from custom_titlebar import CustomTitleBar
# import resources_rc

class TutorialsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("TutorialsDialog")
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        
        # Set fixed size to match the compact design
        self.setFixedSize(320, 140)
        
        # Base stylesheet for the dialog with gradient background
        self.setStyleSheet("""
            #TutorialsDialog {
                background-color: #FFFFFF;
                border: 1px solid #90AF13;
            }
            t#ContentWidget {
                background-color: transparent;
                margin: 2px;
            }
        """)

        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("Video Tutorials")
        mainLayout.addWidget(self.titleBar)

        # Content widget
        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(15, 10, 15, 15)
        contentLayout.setSpacing(8)

        # "Please visit :" label
        visitLabel = QLabel("Please visit :", self)
        visitLabel.setStyleSheet("""
            color: #333333;
            font-size: 13px;
            font-weight: normal;
        """)
        contentLayout.addWidget(visitLabel)

        # YouTube link
        self.youtubeLink = QLabel('<a href="https://www.youtube.com/channel/UCnSZ7EjhDwNi3eCPcSKpgJg" style="color: #1976d2; text-decoration: underline;">https://www.youtube.com/channel</a>', self)
        self.youtubeLink.setStyleSheet("""
            font-size: 12px;
            padding: 2px 0px;
        """)
        self.youtubeLink.setOpenExternalLinks(True)
        self.youtubeLink.setCursor(QCursor(Qt.PointingHandCursor))
        contentLayout.addWidget(self.youtubeLink)

        # Fossee link
        self.fosseeLink = QLabel('<a href="https://osdag.fossee.in/resources/videos" style="color: #1976d2; text-decoration: underline;">https://osdag.fossee.in/resources/videos</a>', self)
        self.fosseeLink.setStyleSheet("""
            font-size: 12px;
            padding: 2px 0px;
        """)
        self.fosseeLink.setOpenExternalLinks(True)
        self.fosseeLink.setCursor(QCursor(Qt.PointingHandCursor))
        contentLayout.addWidget(self.fosseeLink)

        mainLayout.addWidget(contentWidget)

    def showHelp(self):
        """Handle help button click"""
        # You can implement help functionality here
        pass

    def mousePressEvent(self, event):
        """Allow dragging the dialog"""
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle dialog dragging"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'dragPosition'):
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()