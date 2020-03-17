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


    def set_osdaglogger(key):
        """
        Set logger for Base Plate Module.
        """
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = OurLog(key)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def module_name(self):
        """
        Call the Base Plate Module key for displaying the module name.
        """
        return KEY_DISP_BASE_PLATE

    def input_values(self, existingvalues={}):
        """
        Return a-list of tuple, used to create the Input Dock U.I in Osdag design window.
        """
        self.module = KEY_DISP_BASE_PLATE

        options_list = []

        if KEY_DISP_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_DISP_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SUPTNGSEC in existingvalues:  # this might not be required
            existingvalue_key_suptngsec = existingvalues[KEY_SUPTNGSEC]
        else:
            existingvalue_key_suptngsec = ''

        if KEY_SUPTDSEC in existingvalues:
            existingvalue_key_suptdsec = existingvalues[KEY_SUPTDSEC]
        else:
            existingvalue_key_suptdsec = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_MOMENT in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_MOMENT]
        else:
            existingvalue_key_versh = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
        else:
            existingvalue_key_versh = ''

        if KEY_DIA_ANCHOR in existingvalues:
            existingvalue_key_d = existingvalues[KEY_DIA_ANCHOR]
        else:
            existingvalue_key_d = ''

        # if KEY_TYP in existingvalues:
        #     existingvalue_key_typ = existingvalues[KEY_TYP]
        # else:
        #     existingvalue_key_typ = ''

        # if KEY_GRD in existingvalues:
        #     existingvalue_key_grd = existingvalues[KEY_GRD]
        # else:
        #     existingvalue_key_grd = ''

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None)
        options_list.append(t1)

        t16 = (KEY_MODULE, KEY_DISP_BASE_PLATE, TYPE_MODULE, None, None)
        options_list.append(t16)

        t2 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_BP)
        options_list.append(t2)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/base_plate.png")
        options_list.append(t15)

        t3 = (KEY_SUPTNGSEC, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec, connectdb("Columns"))  # this might not be required
        options_list.append(t3)

        # t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, connectdb("Columns"))
        # options_list.append(t4)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL)
        options_list.append(t5)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None)
        options_list.append(t6)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None)
        options_list.append(t8)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None)
        options_list.append(t7)

        t17 = (None, DISP_TITLE_MOMENT, TYPE_TITLE, existingvalue_key_axial, None)
        options_list.append(t17)

        t18 = (KEY_MOMENT_MAJOR, KEY_DISP_MOMENT_MAJOR, TYPE_TEXTBOX, existingvalue_key_conn, None)
        options_list.append(t18)

        t19 = (KEY_MOMENT_MINOR, KEY_DISP_MOMENT_MINOR, TYPE_TEXTBOX, existingvalue_key_conn, None)
        options_list.append(t19)

        t9 = (None, DISP_TITLE_ANCHOR_BOLT, TYPE_TITLE, None, None)
        options_list.append(t9)

        t10 = (KEY_DIA_ANCHOR, KEY_DISP_DIA_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_DIA_ANCHOR)
        options_list.append(t10)

        # t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        # options_list.append(t11)

        # t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        # options_list.append(t12)

        # t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        # options_list.append(t13)

        # t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        # options_list.append(t14)

        return options_list

    def output_values(self, flag):
        return []

    def fn(self):
        if self in ['Gusseted Base Plate', 'Base Plate with Cleat Angles', 'Hollow Sections']:
            return True
        else:
            return False

    def input_value_changed(self):

        lst = []

        t1 = (KEY_CONN, KEY_MOMENT_MAJOR, TYPE_TEXTBOX, self.fn)
        lst.append(t1)

        t2 = (KEY_CONN, KEY_MOMENT_MINOR, TYPE_TEXTBOX, self.fn)
        lst.append(t2)

        return lst

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_DIA_ANCHOR, self.diam_bolt_customized)
        list1.append(t1)

        return list1

    def func_for_validation(self, window, design_dictionary):
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        if design_dictionary[KEY_CONN] == 'Pinned Base Plate':
            design_dictionary[KEY_MOMENT_MAJOR] = 'Ignore'
            design_dictionary[KEY_MOMENT_MINOR] = 'Ignore'
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:
            QMessageBox.information(window, "Information",
                                    generate_missing_fields_error_string(missing_fields_list))
            # flag = False
        else:
            flag = True

        if flag:
            print(design_dictionary)
            # self.set_input_values(self, design_dictionary)
        else:
            pass





