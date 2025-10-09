import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QTextBrowser, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QIcon

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
import osdag_gui.resources.resources_rc
from osdag_gui.__config__ import VERSION

# For testing purposes - replace with actual import
# VERSION = "V2025.01.a.2"
# from custom_titlebar import CustomTitleBar
# import resources_rc

class AboutOsdagDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("AboutOsdagDialog")
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        
        # Set size to match original dialog
        self.setFixedSize(580, 450)
        
        # Base stylesheet for the dialog
        self.setStyleSheet("""
            QDialog#AboutOsdagDialog {
                background-color: #ffffff;
                border: 1px solid #90AF13;
            }
            QWidget#ContentWidget {
                background-color: #ffffff;
            }
            QTextBrowser {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                font-family: 'Arial', sans-serif;
                font-size: 8pt;
                padding: 8px;
            }
        """)

        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("About Osdag")
        mainLayout.addWidget(self.titleBar)

        # Content widget
        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        contentLayout.setSpacing(10)

        self.logoLabel = QSvgWidget(":/vectors/Osdag.svg", self)
        self.logoLabel.setObjectName("LogoLabel")
        self.logoLabel.setFixedHeight(106) # calculated wrt original 1001x234
        self.logoLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        contentLayout.addWidget(self.logoLabel, 0, Qt.AlignCenter)

        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.setAboutContent()
        
        contentLayout.addWidget(self.textBrowser)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        
        okButton = QPushButton("OK", self)
        okButton.setFixedHeight(30)
        okButton.setStyleSheet("""
            QPushButton {
                background-color: #90AF13;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7A9611;
            }
            QPushButton:pressed {
                background-color: #6B850F;
            }
        """)
        okButton.clicked.connect(self.accept)
        buttonLayout.addWidget(okButton)
        
        contentLayout.addLayout(buttonLayout)
        mainLayout.addWidget(contentWidget)

    def setAboutContent(self):
        """Set the HTML content for the about dialog"""
        html_content = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li {{ white-space: pre-wrap; }}
</style></head><body style=" font-family:'Arial'; font-size:7.8pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'monospace, monospace'; font-size:8pt;">Osdag© </span></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;">Version: {VERSION}</span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'monospace, monospace'; font-size:8pt;">Osdag is a cross-platform, free, and open-source software for the design and detailing of steel structures, following the Indian Standard IS 800:2007. Osdag is primarily built using Python other Python-based FOSS tools, such as, PyQt, OpenCascade, PythonOCC, SQLite. It allows the user to design steel connections, members and systems using a graphical user interface. The interactive GUI provides a 3D visualisation of the designed component and an option to export the CAD model to any drafting software for the creation of construction/fabrication drawings. The design is typically optimised following industry best practices. Osdag is developed by the Osdag team at IIT Bombay under the initiative of FOSSEE funded by the Ministry of Education (MoE), Government of India. </span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'monospace, monospace'; font-size:8pt;">This version of Osdag contains the Shear Connection modules, Moment Connection modules and the Tension Member modules.</span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;">© Copyright Osdag contributors 2017.</span></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;">This program comes with ABSOLUTELY NO WARRANTY. This is a free software, and you are welcome to redistribute it under certain conditions. See the License.txt file for details regarding the license.</span></p>
<p align="justify" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8pt;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;">Authors: Osdag Team </span><a href="https://osdag.fossee.in/team"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt; text-decoration: underline; color:#0000ff;">https://osdag.fossee.in/team</span></a></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;">Visit </span><a href="https://osdag.fossee.in/"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt; text-decoration: underline; color:#0000ff;">https://osdag.fossee.in</span></a><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;"> for more information.</span></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt;">----------------------------------------------------</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; text-decoration: underline; color:#0000ff;"><br /></p>
<p align="justify" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt; color:#8a8a8a;">Osdag</span><span style=" font-family:'arial,sans-serif'; font-size:8pt; color:#8a8a8a;">®</span><span style=" font-family:'MS Shell Dlg 2'; font-size:8pt; color:#8a8a8a;"> and the Osdag logo are registered trademarks of Indian Institute of Technology Bombay (IIT Bombay).</span></p></body></html>"""
        
        self.textBrowser.setHtml(html_content)

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


# Test the dialog
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialog = AboutOsdagDialog()
#     result = dialog.exec()
#     sys.exit(app.exec())