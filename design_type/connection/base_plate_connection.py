"""

@Author:    Danish Ansari - Osdag Team, IIT Bombay
@Co-author: Aditya Pawar, Project Intern, MIT College (Aurangabad)


@Module - Base Plate Connection
           - Pinned Base Plate [Axial + Shear]
           - Gusseted Base Plate [Moment (major and minor axis) + Axial + Shear]
           - Base Plate with Cleat Angle


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               3) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

     other     4)  Column Bases - Omer Blodgett (chapter 3)
  references   5) AISC Design Guide 1 - Base Plate and Anchor Rod Design

"""

# Importing modules from the project directory

from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from utils.common.material import *
from Common import *
from utils.common.load import Load
import yaml
from design_report.reportGenerator import save_html

import time
import os
import shutil
import logging
import pickle
import pdfkit
import configparser
import cairosvg
from io import StringIO

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap, QPalette
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog,QMessageBox


class BasePlateConnection(MomentConnection):
    """
    Perform stress analyses --> design base plate and anchor bolt--> provide connection detailing.

    Attributes:
                gamma_mb (float): partial safety factor for material - resistance of connection - bolts
                gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling
                gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress

    """

    def __init__(self):
        """
        Initialize all attributes.
        """
        super(BasePlateConnection, self).__init__()
        self.gamma_mb = 0.0
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0

