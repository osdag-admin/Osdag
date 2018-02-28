"""
Created on 27-Sept-2017

@author: Reshma Konjari
"""
from ui_boltedconnection import Ui_MainWindow
from ui_selection import Ui_Selection
from ui_singleangle import Ui_Singleangle
from ui_singleangle2 import Ui_Singleangle_Two
from ui_singleangle3 import Ui_Singleangle_Three
from ui_singleangle4 import Ui_Singleangle_Four
from ui_singleangle5 import Ui_Singleangle_Five
from ui_singleangle6 import Ui_Singleangle_Six
from ui_singleangle7 import Ui_Singleangle_Seven
from ui_doubleangle import Ui_Doubleangle
from ui_doubleangle2 import Ui_Doubleangle_Two
from ui_doubleangle3 import Ui_Doubleangle_Three
from ui_doubleangle4 import Ui_Doubleangle_Four
from ui_doubleangle5 import Ui_Doubleangle_Five
from ui_doubleangle6 import Ui_Doubleangle_Six
from ui_doubleangle7 import Ui_Doubleangle_Seven
from ui_channel import Ui_Channel
from ui_channel2 import Ui_Channel_Two
from ui_channel3 import Ui_Channel_Three
from ui_channel4 import Ui_Channel_Four
from ui_channel5 import Ui_Channel_Five
from ui_channel6 import Ui_Channel_Six
from ui_channel7 import Ui_Channel_Seven
from ui_output import Ui_BoltOutput
from drawing_2D import TrussBoltedConnection
from truss_bolted_conn_calc import trussboltedconnection
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIntValidator, QPalette, QDoubleValidator
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal, QFile
from model import *
import pickle
import sys
import os


class SingleAngleSelection(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None

        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        # self.ui.btn_save.clicked.connect(self.save_singledata_para)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved =True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):
        if self.sectionselection.ui.comboBx_selection.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class SingleAngleSelectionTwo(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle_Two()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None
        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved =True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_2.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class SingleAngleSelectionThree(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle_Three()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None
        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(
            self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved = True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_3.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class SingleAngleSelectionFour(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle_Four()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None
        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved =True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_4.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_4.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection_4.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class SingleAngleSelectionFive(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle_Five()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None
        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved =True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_5.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_5.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection_5.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class SingleAngleSelectionSix(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle_Six()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None
        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved =True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_6.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_6.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection_6.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class SingleAngleSelectionSeven(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle_Seven()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved = None
        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):
        """

        Returns: Single angle dictionary

        """
        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        self.saved =True
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_7.currentText() == "Select type":
            pass
        else:
            ui_sing_obj = self.save_singledata_para()
            type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
            section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
            leg = ui_sing_obj["SingleAngle"]["leg"]
            print ui_sing_obj, type, section, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_7.setText(type + ' ' + section)
            else:
                self.sectionselection.ui.lbl_sectionSelection_7.setText(type + ' ' + section + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of  angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_sign_angle.currentText()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_sign_selct_section.clear()
            self.ui.comboBox_sign_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_sign_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):
        equalangle_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_sign_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelection(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelectionTwo(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle_Two()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_2.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelectionThree(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle_Three()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_3.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelectionFour(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle_Four()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_4.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_4.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection_4.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelectionFive(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle_Five()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_5.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_5.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection_5.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelectionSix(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle_Six()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_6.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_6.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection_6.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class DoubleAngleSelectionSeven(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Doubleangle_Seven()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):
        """

        Returns: Double angle dictionary

        """
        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["side"] = str(self.ui.comboBx_doub_sides.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        """

        Returns: Close the window

        """
        self.close()

    def lbl_section(self):

        if self.sectionselection.ui.comboBx_selection_7.currentText() == "Select type":
            pass
        else:
            ui_doubl_obj = self.save_doubledata_para()
            type = ui_doubl_obj["DoubleAngle"]["angle_type"]["type"]
            section = ui_doubl_obj["DoubleAngle"]["angle_type"]["section"]
            side = ui_doubl_obj["DoubleAngle"]["side"]
            leg = ui_doubl_obj["DoubleAngle"]["leg"]
            print ui_doubl_obj, type, section, side, leg
            if type == "Equal angle":
                self.sectionselection.ui.lbl_sectionSelection_7.setText(type + ' ' + section + ' ' + side)
            else:
                self.sectionselection.ui.lbl_sectionSelection_7.setText(type + ' ' + section + ' ' + side + ' ' + leg)

    def get_angledata(self):
        """

        Returns: The type of angle selected - Equal or Unequal

        """
        angle_type = self.ui.comboBox_doub_angle.currentText()
        self.ui.comboBox_doub_selct_section.clearFocus()
        print angle_type
        if angle_type == "Equal angle":
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(False)
            equalangledata = get_equalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(equalangledata)

        else:
            self.ui.comboBox_doub_selct_section.clear()
            self.ui.comboBox_doub_leg.setEnabled(True)
            unequalangledata = get_unequalanglecombolist()
            self.ui.comboBox_doub_selct_section.addItems(unequalangledata)

    def fetchEqualAnglePara(self):

        equalangle_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictequalangledata = get_equalangledata(equalangle_sec)
        return dictequalangledata

    def fetchUnequalAnglePara(self):
        unequal_sec = self.ui.comboBox_doub_selct_section.currentText()
        dictunequaldata = get_unequalangledata(unequal_sec)
        return dictunequaldata


class ChannelSelection(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class ChannelSelectionTwo(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel_Two()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class ChannelSelectionThree(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel_Three()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class ChannelSelectionFour(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel_Four()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection_4.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class ChannelSelectionFive(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel_Five()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection_5.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class ChannelSelectionSix(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel_Six()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection_6.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class ChannelSelectionSeven(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Channel_Seven()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent

        self.ui.comboBox_channel.setCurrentIndex(0)
        if self.ui.comboBox_channel.currentText() == "Channel":
            self.get_channeldata()
            print self.ui.comboBox_channel.currentText(), "yes"
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"] = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentText())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def lbl_section(self):
        ui_chanl_obj = self.save_channel_para()
        type = ui_chanl_obj["Channel"]["type"]
        section = ui_chanl_obj["Channel"]["section"]
        print ui_chanl_obj, type, section
        self.sectionselection.ui.lbl_sectionSelection_7.setText(type + ' ' + section)

    def get_channeldata(self):
        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class SectionSelection(QDialog):
    def __init__(self, parent=None):
        # super(SectionSelection, self).__init__(parent)
        QDialog.__init__(self, parent)
        self.ui = Ui_Selection()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.saved = None

        self.singledataparams = SingleAngleSelection(self)
        self.doubledataparams = DoubleAngleSelection(self)
        self.channeldataparams = ChannelSelection(self)
        self.ui.btn_save.clicked.connect(self.save_user_inputs)
        self.ui.btn_reset.clicked.connect(self.reset_btnclicked)
        self.ui.btn_close.clicked.connect(self.close_definemembrs_para)
        self.retrieve_prevstate()

        self.ui.comboBx_selection.setCurrentIndex(0)
        self.ui.comboBx_selection_2.setCurrentIndex(0)
        self.ui.comboBx_selection_3.setCurrentIndex(0)
        self.ui.comboBx_selection_4.setCurrentIndex(0)
        self.ui.comboBx_selection_5.setCurrentIndex(0)
        self.ui.comboBx_selection_6.setCurrentIndex(0)
        self.ui.comboBx_selection_7.setCurrentIndex(0)


        self.ui.comboBx_selection.currentIndexChanged.connect(self.single_angle_selection1)
        self.ui.comboBx_selection_2.currentIndexChanged.connect(self.single_angle_selection2)
        self.ui.comboBx_selection_3.currentIndexChanged.connect(self.single_angle_selection3)
        self.ui.comboBx_selection_4.currentIndexChanged.connect(self.single_angle_selection4)
        self.ui.comboBx_selection_5.currentIndexChanged.connect(self.single_angle_selection5)
        self.ui.comboBx_selection_6.currentIndexChanged.connect(self.single_angle_selection6)
        self.ui.comboBx_selection_7.currentIndexChanged.connect(self.single_angle_selection7)

        min_angle = 0
        max_angle = 360
        self.ui.lineEdit_angle.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle, min_angle, max_angle))
        self.ui.lineEdit_angle_2.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle_2, min_angle, max_angle))
        self.ui.lineEdit_angle_3.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle_3, min_angle, max_angle))
        self.ui.lineEdit_angle_4.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle_4, min_angle, max_angle))
        self.ui.lineEdit_angle_5.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle_5, min_angle, max_angle))
        self.ui.lineEdit_angle_6.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle_6, min_angle, max_angle))
        self.ui.lineEdit_angle_7.editingFinished.connect(lambda : self.check_range(self.ui.lineEdit_angle_7, min_angle, max_angle))

        validator = QIntValidator()
        self.ui.lineEdit_no_of_member.setValidator(validator)
        self.ui.lineEdit_angle.setValidator(validator)
        self.ui.lineEdit_angle_2.setValidator(validator)
        self.ui.lineEdit_angle_3.setValidator(validator)
        self.ui.lineEdit_angle_4.setValidator(validator)
        self.ui.lineEdit_angle_5.setValidator(validator)
        self.ui.lineEdit_angle_6.setValidator(validator)
        self.ui.lineEdit_angle_7.setValidator(validator)

        self.ui.lineEdit_loads.setValidator(validator)
        self.ui.lineEdit_loads_2.setValidator(validator)
        self.ui.lineEdit_loads_3.setValidator(validator)
        self.ui.lineEdit_loads_4.setValidator(validator)
        self.ui.lineEdit_loads_5.setValidator(validator)
        self.ui.lineEdit_loads_6.setValidator(validator)
        self.ui.lineEdit_loads_7.setValidator(validator)

        self.ui.lineEdit_loads.setValidator(QDoubleValidator( 0.00, 10000.00, 3))
        self.ui.lineEdit_loads_2.setValidator(QDoubleValidator(0.00, 10000.00, 3))
        self.ui.lineEdit_loads_3.setValidator(QDoubleValidator(0.00, 10000.00, 3))
        self.ui.lineEdit_loads_4.setValidator(QDoubleValidator(0.00, 10000.00, 3))
        self.ui.lineEdit_loads_5.setValidator(QDoubleValidator(0.00, 10000.00, 3))
        self.ui.lineEdit_loads_6.setValidator(QDoubleValidator(0.00, 10000.00, 3))
        self.ui.lineEdit_loads_7.setValidator(QDoubleValidator(0.00, 10000.00, 3))


        # ui_obj = self.maincontroller.get_user_inputs(["Member"]["No. of members"] )
        # no_of_member = ui_obj["Member"]["No. of members"]
        ui_obj = self.maincontroller.no_of_members()
        no_of_member = ui_obj
        print no_of_member, "no_of_member"

        # self.hide_section(no_of_member)
        # def hide_section(no_of_member):


        if no_of_member == '2':
            no_member_display = str(no_of_member)
            # self.ui.lineEdit_no_of_member.setText(no_member_display)
            self.ui.lineEdit_no_of_member_3.hide()
            self.ui.lineEdit_no_of_member_4.hide()
            self.ui.lineEdit_no_of_member_5.hide()
            self.ui.lineEdit_no_of_member_6.hide()
            self.ui.lineEdit_no_of_member_7.hide()
            self.ui.lineEdit_angle_3.hide()
            self.ui.lineEdit_angle_4.hide()
            self.ui.lineEdit_angle_5.hide()
            self.ui.lineEdit_angle_6.hide()
            self.ui.lineEdit_angle_7.hide()
            self.ui.comboBx_selection_3.hide()
            self.ui.comboBx_selection_4.hide()
            self.ui.comboBx_selection_5.hide()
            self.ui.comboBx_selection_6.hide()
            self.ui.comboBx_selection_7.hide()
            self.ui.lineEdit_loads_3.hide()
            self.ui.lineEdit_loads_4.hide()
            self.ui.lineEdit_loads_5.hide()
            self.ui.lineEdit_loads_6.hide()
            self.ui.lineEdit_loads_7.hide()

            self.ui.lbl_sectionSelection.clear()
            self.ui.lbl_sectionSelection_2.clear()
            self.ui.lbl_sectionSelection_3.clear()
            self.ui.lbl_sectionSelection_4.clear()
            self.ui.lbl_sectionSelection_5.clear()
            self.ui.lbl_sectionSelection_6.clear()
            self.ui.lbl_sectionSelection_7.clear()

        elif no_of_member == '3':
            no_member_display = str(no_of_member)
            # self.ui.lineEdit_no_of_member.setText(no_member_display)
            self.ui.lineEdit_no_of_member_4.hide()
            self.ui.lineEdit_no_of_member_5.hide()
            self.ui.lineEdit_no_of_member_6.hide()
            self.ui.lineEdit_no_of_member_7.hide()
            self.ui.lineEdit_angle_4.hide()
            self.ui.lineEdit_angle_5.hide()
            self.ui.lineEdit_angle_6.hide()
            self.ui.lineEdit_angle_7.hide()
            self.ui.comboBx_selection_4.hide()
            self.ui.comboBx_selection_5.hide()
            self.ui.comboBx_selection_6.hide()
            self.ui.comboBx_selection_7.hide()
            self.ui.lineEdit_loads_4.hide()
            self.ui.lineEdit_loads_5.hide()
            self.ui.lineEdit_loads_6.hide()
            self.ui.lineEdit_loads_7.hide()

        elif no_of_member == '4':
            no_member_display = str(no_of_member)
            # self.ui.lineEdit_no_of_member.setText(no_member_display)
            self.ui.lineEdit_no_of_member_5.hide()
            self.ui.lineEdit_no_of_member_6.hide()
            self.ui.lineEdit_no_of_member_7.hide()
            self.ui.lineEdit_angle_5.hide()
            self.ui.lineEdit_angle_6.hide()
            self.ui.lineEdit_angle_7.hide()
            self.ui.comboBx_selection_5.hide()
            self.ui.comboBx_selection_6.hide()
            self.ui.comboBx_selection_7.hide()
            self.ui.lineEdit_loads_5.hide()
            self.ui.lineEdit_loads_6.hide()
            self.ui.lineEdit_loads_7.hide()

        elif no_of_member == '5':
            no_member_display = str(no_of_member)
            # self.ui.lineEdit_no_of_member.setText(no_member_display)
            self.ui.lineEdit_no_of_member_6.hide()
            self.ui.lineEdit_no_of_member_7.hide()
            self.ui.lineEdit_angle_6.hide()
            self.ui.lineEdit_angle_7.hide()
            self.ui.comboBx_selection_6.hide()
            self.ui.comboBx_selection_7.hide()
            self.ui.lineEdit_loads_6.hide()
            self.ui.lineEdit_loads_7.hide()

        elif no_of_member == '6':
            no_member_display = str(no_of_member)
            # self.ui.lineEdit_no_of_member.setText(no_member_display)
            self.ui.lineEdit_no_of_member_7.hide()
            self.ui.lineEdit_angle_7.hide()
            self.ui.comboBx_selection_7.hide()
            self.ui.lineEdit_loads_7.hide()


        # QMessageBox.about(self, 'Information', 'Define members saved')

    def save_user_inputs(self):
        # pass
        # ui_Obj = self.maincontroller.get_user_inputs()
        self.save_section = {}
        self.save_section["member"] = {}
        self.save_section["member"]["member_one"] = str(self.ui.lineEdit_no_of_member.text())
        self.save_section["member"]["member_two"] = str(self.ui.lineEdit_no_of_member_2.text())
        self.save_section["member"]["member_three"] = str(self.ui.lineEdit_no_of_member_3.text())
        self.save_section["member"]["member_four"] = str(self.ui.lineEdit_no_of_member_4.text())
        self.save_section["member"]["member_five"] = str(self.ui.lineEdit_no_of_member_5.text())
        self.save_section["member"]["member_six"] = str(self.ui.lineEdit_no_of_member_6.text())
        self.save_section["member"]["member_seven"] = str(self.ui.lineEdit_no_of_member_7.text())
        self.save_section["inclination"] = {}
        self.save_section["inclination"]["angle_one"] = str(self.ui.lineEdit_angle.text())
        self.save_section["inclination"]["angle_two"] = str(self.ui.lineEdit_angle_2.text())
        self.save_section["inclination"]["angle_three"] = str(self.ui.lineEdit_angle_3.text())
        self.save_section["inclination"]["angle_four"] = str(self.ui.lineEdit_angle_4.text())
        self.save_section["inclination"]["angle_five"] = str(self.ui.lineEdit_angle_5.text())
        self.save_section["inclination"]["angle_six"] = str(self.ui.lineEdit_angle_6.text())
        self.save_section["inclination"]["angle_seven"] = str(self.ui.lineEdit_angle_7.text())
        self.save_section["force"]={}
        self.save_section["force"]["force_one"] = str(self.ui.lineEdit_loads.text())
        self.save_section["force"]["force_two"] = str(self.ui.lineEdit_loads_2.text())
        self.save_section["force"]["force_three"] = str(self.ui.lineEdit_loads_3.text())
        self.save_section["force"]["force_four"] = str(self.ui.lineEdit_loads_4.text())
        self.save_section["force"]["force_fivr"] = str(self.ui.lineEdit_loads_5.text())
        self.save_section["force"]["force_six"] = str(self.ui.lineEdit_loads_6.text())
        self.save_section["force"]["force_seven"] = str(self.ui.lineEdit_loads_7.text())
        self.save_section["type"] = {}
        self.save_section["type"]["type_one"] = (self.ui.comboBx_selection.currentText())
        self.save_section["type"]["type_two"] = (self.ui.comboBx_selection_2.currentText())
        self.save_section["type"]["type_three"] = (self.ui.comboBx_selection_3.currentText())
        self.save_section["type"]["type_four"] = str(self.ui.comboBx_selection_4.currentText())
        self.save_section["type"]["type_five"] = str(self.ui.comboBx_selection_5.currentText())
        self.save_section["type"]["type_six"] = str(self.ui.comboBx_selection_6.currentText())
        self.save_section["type"]["type_seven"] = str(self.ui.comboBx_selection_7.currentText())
        self.save_section["section"] = {}
        self.save_section["section"]["sec_one"] = str(self.ui.lbl_sectionSelection.text())
        self.save_section["section"]["sec_two"] = str(self.ui.lbl_sectionSelection_2.text())
        self.save_section["section"]["sec_three"] = str(self.ui.lbl_sectionSelection_3.text())
        self.save_section["section"]["sec_four"] = str(self.ui.lbl_sectionSelection_4.text())
        self.save_section["section"]["sec_five"] = str(self.ui.lbl_sectionSelection_5.text())
        self.save_section["section"]["sec_six"] = str(self.ui.lbl_sectionSelection_6.text())
        self.save_section["section"]["sec_seven"] = str(self.ui.lbl_sectionSelection_7.text())
        self.saved = True
        print self.save_section, "inputs"
        QMessageBox.about(self, 'Information', "Define members data saved")

        return self.save_section

    def reset_btnclicked(self):

        self.ui.comboBx_selection.setCurrentIndex(0)
        self.ui.comboBx_selection_2.setCurrentIndex(0)
        self.ui.comboBx_selection_3.setCurrentIndex(0)
        self.ui.comboBx_selection_4.setCurrentIndex(0)
        self.ui.comboBx_selection_5.setCurrentIndex(0)
        self.ui.comboBx_selection_6.setCurrentIndex(0)
        self.ui.comboBx_selection_7.setCurrentIndex(0)

        self.ui.lineEdit_loads.clear()
        self.ui.lineEdit_loads_2.clear()
        self.ui.lineEdit_loads_3.clear()
        self.ui.lineEdit_loads_4.clear()
        self.ui.lineEdit_loads_5.clear()
        self.ui.lineEdit_loads_6.clear()
        self.ui.lineEdit_loads_7.clear()

        self.ui.lineEdit_angle.clear()
        self.ui.lineEdit_angle_2.clear()
        self.ui.lineEdit_angle_3.clear()
        self.ui.lineEdit_angle_4.clear()
        self.ui.lineEdit_angle_5.clear()
        self.ui.lineEdit_angle_6.clear()
        self.ui.lineEdit_angle_7.clear()

        self.ui.lbl_sectionSelection.clear()
        self.ui.lbl_sectionSelection_2.clear()
        self.ui.lbl_sectionSelection_3.clear()
        self.ui.lbl_sectionSelection_4.clear()
        self.ui.lbl_sectionSelection_5.clear()
        self.ui.lbl_sectionSelection_6.clear()
        self.ui.lbl_sectionSelection_7.clear()

    def single_angle_selection1(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc = self.ui.comboBx_selection.currentText()
        if loc == "Single Angle":
            section = SingleAngleSelection(self)
            section.show()
        elif loc == "Double Angle":
            section = DoubleAngleSelection(self)
            section.show()
        elif loc == "Select type":
            pass
        else:
            section = ChannelSelection(self)
            section.show()

    def single_angle_selection2(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc1 = self.ui.comboBx_selection_2.currentText()
        if loc1 =="Single Angle":
            section = SingleAngleSelectionTwo(self)
            section.show()
        elif loc1 == "Double Angle":
            section = DoubleAngleSelectionTwo(self)
            section.show()
        elif loc1 == "Select type":
            pass
        else:
            section = ChannelSelectionTwo(self)
            section.show()

    def single_angle_selection3(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc2 = self.ui.comboBx_selection_3.currentText()
        if loc2 == "Single Angle":
            section = SingleAngleSelectionThree(self)
            section.show()
        elif loc2 == "Double Angle":
            section = DoubleAngleSelectionThree(self)
            section.show()
        elif loc2 == "Select type":
            pass
        else:
            section = ChannelSelectionThree(self)
            section.show()

    def single_angle_selection4(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc3 = self.ui.comboBx_selection_4.currentText()
        if loc3 == "Single Angle":
            section = SingleAngleSelectionFour(self)
            section.show()
        elif loc3 == "Double Angle":
            section = DoubleAngleSelectionFour(self)
            section.show()
        elif loc3 == "Select type":
            pass
        else:
            section = ChannelSelectionFour(self)
            section.show()

    def single_angle_selection5(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc4 = self.ui.comboBx_selection_5.currentText()
        if loc4 == "Single Angle":
            section = SingleAngleSelectionFive(self)
            section.show()
        elif loc4 == "Double Angle":
            section = DoubleAngleSelectionFive(self)
            section.show()
        elif loc4 == "Select type":
            pass
        else:
            section = ChannelSelectionFive(self)
            section.show()

    def single_angle_selection6(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc5 = self.ui.comboBx_selection_6.currentText()
        if loc5 == "Single Angle":
            section = SingleAngleSelectionSix(self)
            section.show()
        elif loc5 == "Double Angle":
            section = DoubleAngleSelectionSix(self)
            section.show()
        elif loc5 == "Select type":
            pass
        else:
            section = ChannelSelectionSix(self)
            section.show()

    def single_angle_selection7(self):
        """

        Returns: Select type of Angles or Channel

        """
        loc6 = self.ui.comboBx_selection_7.currentText()
        if loc6 == "Single Angle":
            section = SingleAngleSelectionSeven(self)
            section.show()
        elif loc6 == "Double Angle":
            section = DoubleAngleSelectionSeven(self)
            section.show()
        elif loc6 == "Select type":
            pass
        else:
            section = ChannelSelectionSeven(self)
            section.show()

    def check_range(self, widget, min_angle, max_angle):
        """

        Args:
            widget: Text entered for Angle
            min_angle:  Min angle of inclination
            max_angle: Max angle of Inclination

        Returns: Check for range of angle of Inclination

        """
        text_str = widget.text()
        text_str = int(text_str)
        if (text_str < min_angle or text_str > max_angle or text_str == ' '):
            QMessageBox.about(self, 'Error', 'Please enter a value between %s-%s' %(min_angle, max_angle))
            widget.clear()
            widget.setFocus()

    def save_definemembrs_para(self):
        pass

    def close_definemembrs_para(self):
        self.close()

    def closeEvent(self, event):
        """

        Args:
            event: Yes or No

        Returns: Ask for the confirmation while closing the window

        """
        uiInput = self.save_user_inputs()
        self.save_inputs_totext(uiInput)
        action = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if action == QMessageBox.Yes:
            # self.close.emit()
            self.close()
            event.accept()
        else:
            event.ignore()

    def save_inputs_totext(self, uiObj):
        """

        Args:
            uiObj: User inputs

        Returns: Save the user input to txt format

        """
        input_file = QFile(os.path.join("saveINPUT1.txt"))
        if not input_file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s: \n%s"
                                % (input_file.fileName(), input_file.errorString()))
        pickle.dump(uiObj, input_file)

    def get_prevstate(self):
        """

        Returns: Read for the previous user inputs design

        """
        filename = os.path.join("saveINPUT1.txt")
        if os.path.isfile(filename):
            file_object = open(filename, 'r')
            uiObj = pickle.load(file_object)
            return uiObj
        else:
            return None

    def retrieve_prevstate(self):
        """

        Returns: Retrieve the previous design parameters done by user

        """
        uiObj = self.get_prevstate()
        self.set_dict_touser_inputs(uiObj)

    def set_dict_touser_inputs(self, uiObj):

        if uiObj is not None:
            self.ui.lineEdit_angle.setText(str(uiObj["inclination"]["angle_one"]))
            self.ui.lineEdit_angle_2.setText(str(uiObj["inclination"]["angle_two"]))
            self.ui.lineEdit_angle_3.setText(str(uiObj["inclination"]["angle_three"]))
            self.ui.lineEdit_angle_4.setText(str(uiObj["inclination"]["angle_four"]))
            self.ui.lineEdit_angle_5.setText(str(uiObj["inclination"]["angle_five"]))
            self.ui.lineEdit_angle_6.setText(str(uiObj["inclination"]["angle_six"]))
            self.ui.lineEdit_angle_7.setText(str(uiObj["inclination"]["angle_seven"]))
            self.ui.lineEdit_loads.setText(str(uiObj["force"]["force_one"]))
            self.ui.lineEdit_loads_2.setText(str(uiObj["force"]["force_two"]))
            self.ui.lineEdit_loads_3.setText(str(uiObj["force"]["force_three"]))
            self.ui.lineEdit_loads_4.setText(str(uiObj["force"]["force_four"]))
            self.ui.lineEdit_loads_5.setText(str(uiObj["force"]["force_fivr"]))
            self.ui.lineEdit_loads_6.setText(str(uiObj["force"]["force_six"]))
            self.ui.lineEdit_loads_7.setText(str(uiObj["force"]["force_seven"]))

            self.ui.lbl_sectionSelection.setText(str(uiObj["section"]["sec_one"]))
            self.ui.lbl_sectionSelection_2.setText(str(uiObj["section"]["sec_two"]))
            self.ui.lbl_sectionSelection_3.setText(str(uiObj["section"]["sec_three"]))
            self.ui.lbl_sectionSelection_4.setText(str(uiObj["section"]["sec_four"]))
            self.ui.lbl_sectionSelection_5.setText(str(uiObj["section"]["sec_five"]))
            self.ui.lbl_sectionSelection_6.setText(str(uiObj["section"]["sec_six"]))
            self.ui.lbl_sectionSelection_7.setText(str(uiObj["section"]["sec_seven"]))

            self.ui.comboBx_selection.setCurrentIndex(self.ui.comboBx_selection.findText(uiObj["type"]["type_one"]))
            self.ui.comboBx_selection_2.setCurrentIndex(self.ui.comboBx_selection_2.findText(uiObj["type"]["type_one"]))
            self.ui.comboBx_selection_3.setCurrentIndex(self.ui.comboBx_selection_3.findText(uiObj["type"]["type_one"]))
            self.ui.comboBx_selection_4.setCurrentIndex(self.ui.comboBx_selection_4.findText(uiObj["type"]["type_one"]))
            self.ui.comboBx_selection_5.setCurrentIndex(self.ui.comboBx_selection_5.findText(uiObj["type"]["type_one"]))
            self.ui.comboBx_selection_6.setCurrentIndex(self.ui.comboBx_selection_6.findText(uiObj["type"]["type_one"]))
            self.ui.comboBx_selection_7.setCurrentIndex(self.ui.comboBx_selection_7.findText(uiObj["type"]["type_one"]))


class BoltOutput(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_BoltOutput()
        self.ui.setupUi(self)
        self.maincontroller = parent

        dbl_validator = QDoubleValidator()
        self.ui.lineEdit_shr.setValidator(dbl_validator)
        self.ui.lineEdit_shr2.setValidator(dbl_validator)
        self.ui.lineEdit_shr3.setValidator(dbl_validator)
        self.ui.lineEdit_shr4.setValidator(dbl_validator)
        self.ui.lineEdit_shr5.setValidator(dbl_validator)
        self.ui.lineEdit_shr6.setValidator(dbl_validator)
        self.ui.lineEdit_shr7.setValidator(dbl_validator)

        members = self.maincontroller.no_of_members()
        no_of_member = members
        print no_of_member, "no of members"
        if no_of_member == '2':
            self.ui.lbl_mem3.hide()
            self.ui.lbl_mem4.hide()
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lineEdit_shr3.hide()
            self.ui.lineEdit_shr4.hide()
            self.ui.lineEdit_shr5.hide()
            self.ui.lineEdit_shr6.hide()
            self.ui.lineEdit_shr7.hide()
            self.ui.lineEdit_ber3.hide()
            self.ui.lineEdit_ber4.hide()
            self.ui.lineEdit_ber5.hide()
            self.ui.lineEdit_ber6.hide()
            self.ui.lineEdit_ber7.hide()
            self.ui.lineEdit_req3.hide()
            self.ui.lineEdit_req4.hide()
            self.ui.lineEdit_req5.hide()
            self.ui.lineEdit_req6.hide()
            self.ui.lineEdit_req7.hide()
            self.ui.lineEdit_blt_cap3.hide()
            self.ui.lineEdit_blt_cap4.hide()
            self.ui.lineEdit_blt_cap5.hide()
            self.ui.lineEdit_blt_cap6.hide()
            self.ui.lineEdit_blt_cap7.hide()
            self.ui.lineEdit_col3.hide()
            self.ui.lineEdit_col4.hide()
            self.ui.lineEdit_col5.hide()
            self.ui.lineEdit_col6.hide()
            self.ui.lineEdit_col7.hide()
            self.ui.lineEdit_row3.hide()
            self.ui.lineEdit_row4.hide()
            self.ui.lineEdit_row5.hide()
            self.ui.lineEdit_row6.hide()
            self.ui.lineEdit_row7.hide()
            self.ui.lineEdit_pitch3.hide()
            self.ui.lineEdit_pitch4.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
            self.ui.lineEdit_gauge3.hide()
            self.ui.lineEdit_gauge4.hide()
            self.ui.lineEdit_gauge5.hide()
            self.ui.lineEdit_gauge6.hide()
            self.ui.lineEdit_gauge7.hide()
            self.ui.lineEdit_end3.hide()
            self.ui.lineEdit_end4.hide()
            self.ui.lineEdit_end5.hide()
            self.ui.lineEdit_end6.hide()
            self.ui.lineEdit_end7.hide()
            self.ui.lineEdit_edge3.hide()
            self.ui.lineEdit_edge4.hide()
            self.ui.lineEdit_edge5.hide()
            self.ui.lineEdit_edge6.hide()
            self.ui.lineEdit_edge7.hide()
            self.ui.lineEdit_tens3.hide()
            self.ui.lineEdit_tens4.hide()
            self.ui.lineEdit_tens5.hide()
            self.ui.lineEdit_tens6.hide()
            self.ui.lineEdit_tens7.hide()
            self.ui.lineEdit_block3.hide()
            self.ui.lineEdit_block4.hide()
            self.ui.lineEdit_block5.hide()
            self.ui.lineEdit_block6.hide()
            self.ui.lineEdit_block7.hide()

        elif no_of_member == '3':
            self.ui.lbl_mem4.hide()
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lineEdit_shr4.hide()
            self.ui.lineEdit_shr5.hide()
            self.ui.lineEdit_shr6.hide()
            self.ui.lineEdit_shr7.hide()
            self.ui.lineEdit_ber4.hide()
            self.ui.lineEdit_ber5.hide()
            self.ui.lineEdit_ber6.hide()
            self.ui.lineEdit_ber7.hide()
            self.ui.lineEdit_req4.hide()
            self.ui.lineEdit_req5.hide()
            self.ui.lineEdit_req6.hide()
            self.ui.lineEdit_req7.hide()
            self.ui.lineEdit_blt_cap4.hide()
            self.ui.lineEdit_blt_cap5.hide()
            self.ui.lineEdit_blt_cap6.hide()
            self.ui.lineEdit_blt_cap7.hide()
            self.ui.lineEdit_col4.hide()
            self.ui.lineEdit_col5.hide()
            self.ui.lineEdit_col6.hide()
            self.ui.lineEdit_col7.hide()
            self.ui.lineEdit_row4.hide()
            self.ui.lineEdit_row5.hide()
            self.ui.lineEdit_row6.hide()
            self.ui.lineEdit_row7.hide()
            self.ui.lineEdit_pitch4.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
            self.ui.lineEdit_gauge4.hide()
            self.ui.lineEdit_gauge5.hide()
            self.ui.lineEdit_gauge6.hide()
            self.ui.lineEdit_gauge7.hide()
            self.ui.lineEdit_end4.hide()
            self.ui.lineEdit_end5.hide()
            self.ui.lineEdit_end6.hide()
            self.ui.lineEdit_end7.hide()
            self.ui.lineEdit_edge4.hide()
            self.ui.lineEdit_edge5.hide()
            self.ui.lineEdit_edge6.hide()
            self.ui.lineEdit_edge7.hide()
            self.ui.lineEdit_tens4.hide()
            self.ui.lineEdit_tens5.hide()
            self.ui.lineEdit_tens6.hide()
            self.ui.lineEdit_tens7.hide()
            self.ui.lineEdit_block4.hide()
            self.ui.lineEdit_block5.hide()
            self.ui.lineEdit_block6.hide()
            self.ui.lineEdit_block7.hide()

        elif no_of_member == '4':
            self.ui.lbl_mem5.hide()
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lineEdit_shr5.hide()
            self.ui.lineEdit_shr6.hide()
            self.ui.lineEdit_shr7.hide()
            self.ui.lineEdit_ber5.hide()
            self.ui.lineEdit_ber6.hide()
            self.ui.lineEdit_ber7.hide()
            self.ui.lineEdit_req5.hide()
            self.ui.lineEdit_req6.hide()
            self.ui.lineEdit_req7.hide()
            self.ui.lineEdit_blt_cap5.hide()
            self.ui.lineEdit_blt_cap6.hide()
            self.ui.lineEdit_blt_cap7.hide()
            self.ui.lineEdit_col5.hide()
            self.ui.lineEdit_col6.hide()
            self.ui.lineEdit_col7.hide()
            self.ui.lineEdit_row5.hide()
            self.ui.lineEdit_row6.hide()
            self.ui.lineEdit_row7.hide()
            self.ui.lineEdit_pitch5.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
            self.ui.lineEdit_gauge5.hide()
            self.ui.lineEdit_gauge6.hide()
            self.ui.lineEdit_gauge7.hide()
            self.ui.lineEdit_end5.hide()
            self.ui.lineEdit_end6.hide()
            self.ui.lineEdit_end7.hide()
            self.ui.lineEdit_edge5.hide()
            self.ui.lineEdit_edge6.hide()
            self.ui.lineEdit_edge7.hide()
            self.ui.lineEdit_tens5.hide()
            self.ui.lineEdit_tens6.hide()
            self.ui.lineEdit_tens7.hide()
            self.ui.lineEdit_block5.hide()
            self.ui.lineEdit_block6.hide()
            self.ui.lineEdit_block7.hide()

        elif no_of_member == '5':
            self.ui.lbl_mem6.hide()
            self.ui.lbl_mem7.hide()
            self.ui.lineEdit_shr6.hide()
            self.ui.lineEdit_shr7.hide()
            self.ui.lineEdit_ber6.hide()
            self.ui.lineEdit_ber7.hide()
            self.ui.lineEdit_req6.hide()
            self.ui.lineEdit_req7.hide()
            self.ui.lineEdit_blt_cap6.hide()
            self.ui.lineEdit_blt_cap7.hide()
            self.ui.lineEdit_col6.hide()
            self.ui.lineEdit_col7.hide()
            self.ui.lineEdit_row6.hide()
            self.ui.lineEdit_row7.hide()
            self.ui.lineEdit_pitch6.hide()
            self.ui.lineEdit_pitch7.hide()
            self.ui.lineEdit_gauge6.hide()
            self.ui.lineEdit_gauge7.hide()
            self.ui.lineEdit_end6.hide()
            self.ui.lineEdit_end7.hide()
            self.ui.lineEdit_edge6.hide()
            self.ui.lineEdit_edge7.hide()
            self.ui.lineEdit_tens6.hide()
            self.ui.lineEdit_tens7.hide()
            self.ui.lineEdit_block6.hide()
            self.ui.lineEdit_block7.hide()

        elif no_of_member == '6':
            self.ui.lbl_mem7.hide()
            self.ui.lineEdit_shr7.hide()
            self.ui.lineEdit_ber7.hide()
            self.ui.lineEdit_req7.hide()
            self.ui.lineEdit_blt_cap7.hide()
            self.ui.lineEdit_col7.hide()
            self.ui.lineEdit_row7.hide()
            self.ui.lineEdit_pitch7.hide()
            self.ui.lineEdit_gauge7.hide()
            self.ui.lineEdit_end7.hide()
            self.ui.lineEdit_edge7.hide()
            self.ui.lineEdit_tens7.hide()
            self.ui.lineEdit_block7.hide()

        uiObj = self.maincontroller.get_user_inputs()
        resultObj = trussboltedconnection(uiObj)
        self.ui.lineEdit_shr.setText(str(resultObj["ShearCapacity"]))
        self.ui.lineEdit_shr2.setText(str(resultObj["ShearCapacity2"]))
        self.ui.lineEdit_shr3.setText(str(resultObj["ShearCapacity3"]))
        self.ui.lineEdit_shr4.setText(str(resultObj["ShearCapacity4"]))
        self.ui.lineEdit_shr5.setText(str(resultObj["ShearCapacity5"]))
        self.ui.lineEdit_shr6.setText(str(resultObj["ShearCapacity6"]))
        self.ui.lineEdit_shr7.setText(str(resultObj["ShearCapacity7"]))
        self.ui.lineEdit_ber.setText(str(resultObj["BearingCapacity"]))
        self.ui.lineEdit_ber2.setText(str(resultObj["BearingCapacity2"]))
        self.ui.lineEdit_ber3.setText(str(resultObj["BearingCapacity3"]))
        self.ui.lineEdit_ber4.setText(str(resultObj["BearingCapacity4"]))
        self.ui.lineEdit_ber5.setText(str(resultObj["BearingCapacity5"]))
        self.ui.lineEdit_ber6.setText(str(resultObj["BearingCapacity6"]))
        self.ui.lineEdit_ber7.setText(str(resultObj["BearingCapacity7"]))
        self.ui.lineEdit_req.setText(str(resultObj["NoOfBoltsReq"]))
        self.ui.lineEdit_req2.setText(str(resultObj["NoOfBoltsReq2"]))
        self.ui.lineEdit_req3.setText(str(resultObj["NoOfBoltsReq3"]))
        self.ui.lineEdit_req4.setText(str(resultObj["NoOfBoltsReq4"]))
        self.ui.lineEdit_req5.setText(str(resultObj["NoOfBoltsReq5"]))
        self.ui.lineEdit_req6.setText(str(resultObj["NoOfBoltsReq6"]))
        self.ui.lineEdit_req7.setText(str(resultObj["NoOfBoltsReq7"]))
        self.ui.lineEdit_row.setText(str(resultObj["NoOfRow"]))
        self.ui.lineEdit_row2.setText(str(resultObj["NoOfRow2"]))
        self.ui.lineEdit_row3.setText(str(resultObj["NoOfRow3"]))
        self.ui.lineEdit_row4.setText(str(resultObj["NoOfRow4"]))
        self.ui.lineEdit_row5.setText(str(resultObj["NoOfRow5"]))
        self.ui.lineEdit_row6.setText(str(resultObj["NoOfRow6"]))
        self.ui.lineEdit_row7.setText(str(resultObj["NoOfRow7"]))
        self.ui.lineEdit_col.setText(str(resultObj["NoOfColumns"]))
        self.ui.lineEdit_col2.setText(str(resultObj["NoOfColumns2"]))
        self.ui.lineEdit_col3.setText(str(resultObj["NoOfColumns3"]))
        self.ui.lineEdit_col4.setText(str(resultObj["NoOfColumns4"]))
        self.ui.lineEdit_col5.setText(str(resultObj["NoOfColumns5"]))
        self.ui.lineEdit_col6.setText(str(resultObj["NoOfColumns6"]))
        self.ui.lineEdit_col7.setText(str(resultObj["NoOfColumns7"]))
        self.ui.lineEdit_pitch.setText(str(resultObj["Pitch"]))
        self.ui.lineEdit_pitch2.setText(str(resultObj["Pitch2"]))
        self.ui.lineEdit_pitch3.setText(str(resultObj["Pitch3"]))
        self.ui.lineEdit_pitch4.setText(str(resultObj["Pitch4"]))
        self.ui.lineEdit_pitch5.setText(str(resultObj["Pitch5"]))
        self.ui.lineEdit_pitch6.setText(str(resultObj["Pitch6"]))
        self.ui.lineEdit_pitch7.setText(str(resultObj["Pitch7"]))
        self.ui.lineEdit_gauge.setText(str(resultObj["Gauge"]))
        self.ui.lineEdit_gauge2.setText(str(resultObj["Gauge2"]))
        self.ui.lineEdit_gauge3.setText(str(resultObj["Gauge3"]))
        self.ui.lineEdit_gauge4.setText(str(resultObj["Gauge4"]))
        self.ui.lineEdit_gauge5.setText(str(resultObj["Gauge5"]))
        self.ui.lineEdit_gauge6.setText(str(resultObj["Gauge6"]))
        self.ui.lineEdit_gauge7.setText(str(resultObj["Gauge7"]))
        self.ui.lineEdit_end.setText(str(resultObj["End"]))
        self.ui.lineEdit_end2.setText(str(resultObj["End2"]))
        self.ui.lineEdit_end3.setText(str(resultObj["End3"]))
        self.ui.lineEdit_end4.setText(str(resultObj["End4"]))
        self.ui.lineEdit_end5.setText(str(resultObj["End5"]))
        self.ui.lineEdit_end6.setText(str(resultObj["End6"]))
        self.ui.lineEdit_end7.setText(str(resultObj["End7"]))
        self.ui.lineEdit_edge.setText(str(resultObj["Edge"]))
        self.ui.lineEdit_edge2.setText(str(resultObj["Edge2"]))
        self.ui.lineEdit_edge3.setText(str(resultObj["Edge3"]))
        self.ui.lineEdit_edge4.setText(str(resultObj["Edge4"]))
        self.ui.lineEdit_edge5.setText(str(resultObj["Edge5"]))
        self.ui.lineEdit_edge6.setText(str(resultObj["Edge6"]))
        self.ui.lineEdit_edge7.setText(str(resultObj["Edge7"]))
        self.ui.lineEdit_tens.setText(str(resultObj["TensionCapacity"]))
        self.ui.lineEdit_tens2.setText(str(resultObj["TensionCapacity2"]))
        self.ui.lineEdit_tens3.setText(str(resultObj["TensionCapacity3"]))
        self.ui.lineEdit_tens4.setText(str(resultObj["TensionCapacity4"]))
        self.ui.lineEdit_tens5.setText(str(resultObj["TensionCapacity5"]))
        self.ui.lineEdit_tens6.setText(str(resultObj["TensionCapacity6"]))
        self.ui.lineEdit_tens7.setText(str(resultObj["TensionCapacity7"]))
        self.ui.lineEdit_block.setText(str(resultObj["BlockShearCapacity"]))
        self.ui.lineEdit_block2.setText(str(resultObj["BlockShearCapacity2"]))
        self.ui.lineEdit_block3.setText(str(resultObj["BlockShearCapacity3"]))
        self.ui.lineEdit_block4.setText(str(resultObj["BlockShearCapacity4"]))
        self.ui.lineEdit_block5.setText(str(resultObj["BlockShearCapacity5"]))
        self.ui.lineEdit_block6.setText(str(resultObj["BlockShearCapacity6"]))
        self.ui.lineEdit_block7.setText(str(resultObj["BlockShearCapacity7"]))


class Maincontroller(QMainWindow):
    closed = pyqtSignal()
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.uiObj = None
        self.defineMembers = SectionSelection(self)

        self.ui.btn_section.clicked.connect(self.section_selection)
        self.ui.combo_member.setItemText(0, "Select no.of members")
        self.ui.combo_member.setCurrentIndex(0)
        self.ui.combo_member.currentIndexChanged.connect(self.no_of_members)
        self.ui.btn_Reset.clicked.connect(self.reset_button_clicked)
        self.ui.btn_bolt_output.clicked.connect(self.bolt_output)
        self.ui.btnFront.clicked.connect(lambda: self.call_2D_drawing("Front"))
        self.gradeType = {'Please select type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.retrieve_prevstate()

        validator = QIntValidator()
        self.ui.txt_Fu.setValidator(validator)
        self.ui.txt_Fy.setValidator(validator)

        min_fu = 290
        max_fu = 590
        self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txt_Fy.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fy, min_fy, max_fy))

    def check_range(self, widget, min_val, max_val):
        """

        Args:
            widget: Fu , Fy lineedit
            min_val: min value
            max_val: max value

        Returns: Check for the value mentioned for the given range

        """
        text_str = widget.text()
        text_str = int(text_str)
        if (text_str < min_val or text_str > max_val or text_str == ' '):
            QMessageBox.about(self, "Error", "Please enter a value between %s-%s"%(min_val, max_val))
            widget.clear()
            widget.setFocus()

    def combotype_current_index_changed(self, index):
        """

        Args:
            index: Number

        Returns: Types of Grade

        """
        items = self.gradeType[str(index)]
        if items != 0 :
            self.ui.combo_grade.clear()
            stritems = []
            for val in items:
                stritems.append(str(val))

            self.ui.combo_grade.addItems(stritems)
        else:
            pass

    def no_of_members(self):
        """

        Returns: Number of Members selected

        """
        membr_num = self.ui.combo_member.currentText()
        print membr_num
        return membr_num

    def section_selection(self):
        section = SectionSelection(self)
        section.show()

    def bolt_output(self):
        section = BoltOutput(self)
        # section = NewTable(self)
        section.show()

    def reset_button_clicked(self):
        """

        Returns: Resets all fields in input as well as output dock

        """
        self.ui.combo_member.setCurrentIndex(0)
        self.ui.txt_Fu.clear()
        self.ui.txt_Fy.clear()
        self.ui.combo_gussetSize.setCurrentIndex(0)
        self.ui.combo_diameter.setCurrentIndex(0)
        self.ui.combo_type.setCurrentIndex(0)
        self.ui.combo_grade.setCurrentIndex(0)

        self.defineMembers.ui.lineEdit_loads.clear()
        self.defineMembers.ui.comboBx_selection.setCurrentIndex(0)


    def get_user_inputs(self):
        """

        Returns: The dictionary objects with user input fields for designing truss bolted connection
                ui_Obj = User input objects
        """
        ui_obj = {}
        ui_obj["Member"] = {}
        ui_obj["Member"]["No. of members"] = self.ui.combo_member.currentText()
        # ui_obj["Member"]["DefineMembers"] = self.ui.btn_section.text()          #TODO call define members dictionary
        ui_obj["Member"]["fu (MPa)"] = self.ui.txt_Fu.text()
        ui_obj["Member"]["fy (MPa)"] = self.ui.txt_Fy.text()

        ui_obj["Bolt"] = {}
        ui_obj["Bolt"]["Diameter (mm)"] = self.ui.combo_diameter.currentText()
        ui_obj["Bolt"]["Type"] = self.ui.combo_type.currentText()
        ui_obj["Bolt"]["Grade"] = self.ui.combo_grade.currentText()

        ui_obj["Gusset"] = {}
        ui_obj["Gusset"]["Thickness (mm)"] = self.ui.combo_gussetSize.currentText()
        print ui_obj, "ui_obj"
        return ui_obj

    def closeEvent(self, event):
        """

        Args:
            event: Yes or No

        Returns: Ask for the confirmation while closing the window

        """
        uiInput = self.get_user_inputs()
        self.save_inputs_totext(uiInput)
        action = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if action == QMessageBox.Yes:
            # self.close.emit()
            self.close()
            event.accept()
        else:
            event.ignore()

    def save_inputs_totext(self, uiObj):
        """

        Args:
            uiObj: User inputs

        Returns: Save the user input to txt format

        """
        input_file = QFile(os.path.join("saveINPUT.txt"))
        if not input_file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s: \n%s"
                                % (input_file.fileName(), input_file.errorString()))
        pickle.dump(uiObj, input_file)

    def get_prevstate(self):
        """

        Returns: Read for the previous user inputs design

        """
        filename = os.path.join("saveINPUT.txt")
        if os.path.isfile(filename):
            file_object = open(filename, 'r')
            uiObj = pickle.load(file_object)
            return uiObj
        else:
            return None

    def retrieve_prevstate(self):
        """

        Returns: Retrieve the previous design parameters done by user

        """
        uiObj = self.get_prevstate()
        self.set_dict_touser_inputs(uiObj)

    def set_dict_touser_inputs(self, uiObj):

        if uiObj is not None:
            self.ui.combo_member.setCurrentIndex(self.ui.combo_member.findText(str(uiObj["Member"]["No. of members"])))
            self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
            self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
            self.ui.combo_gussetSize.setCurrentIndex(self.ui.combo_gussetSize.findText(str(uiObj["Gusset"]["Thickness (mm)"])))
            self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
            self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
            self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
        else:
            pass

    def definemembers_para(self):

        dmObj = self.defineMembers.save_section()
        print dmObj

        # self.uiObj = self.get_user_inputs()
        # if self.defineMembers.saved is True:
        #     define_membr = None
        # else:
        #     define_membr = self.defineMembers.save_section
        # self.uiObj.update(define_membr)
        # print "saved members", self.uiObj

    def design_btnclicked(self):
        """

        Returns:

        """
        self.uiObj = self.get_user_inputs()
        self.dmObj = self.definemembers_para()
        self.outputs = trussboltedconnection(self.uiObj, self.dmObj)
        print "Designbtn", self.dmObj
        self.display_output(self.outputs)
        # self.resultObj = outputs
        # alist =self.resultObj.values()
        # self.display_output(self.resultObj)
        # isempty = [True if val != '' else False for ele in alist for val in ele.values()]

    def display_output(self, outputObj):
        for k in outputObj.keys():
            for value in outputObj.vaules():
                if outputObj.items() == " ":
                    resultObj = outputObj
                else:
                    resultObj = outputObj
        print resultObj

        plate_length = resultObj["Plate"]["Length"]
        self.ui.txt_plateLength.setText(str(plate_length))

        plate_width = resultObj["Plate"]["Width"]
        self.ui.txt_plateWidth.setText(str(plate_width))

        combine_capacity = resultObj["Plate"]["CombineCapacity"]
        self.ui.txt_combineCapacity.setText(str(combine_capacity))

    def call_2D_drawing(self, view):
        """

        Args:
            view: Front, Side & Top views

        Returns: Saves 2D svg drawings

        """
        conn_members = TrussBoltedConnection()
        if view == "Front":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Truss\Front.svg"
            conn_members.save_to_svg(filename, view)
        else:
            pass

    def dockbtn_clicked(self, widgets):
        """

        Args:
            widgets: Input , Output dock

        Returns: Dock & undock the widgets

        """
        flag = widgets.isHidden()
        if flag:
            widgets.show()
        else:
            widgets.hide()


def set_osdaglogger():
    global logger
    if logger is None:

        logger = logging.getLogger("osdag")
    else:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    # create the logging file handler
    fh = logging.FileHandler("trussbolted.log", mode="a")

    # ,datefmt='%a, %d %b %Y %H:%M:%S'
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    formatter = logging.Formatter('''
    <div  class="LOG %(levelname)s">
        <span class="DATE">%(asctime)s</span>
        <span class="LEVEL">%(levelname)s</span>
        <span class="MSG">%(message)s</span>
    </div>''')
    formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def main():
    set_osdaglogger()
    app = QApplication(sys.argv)
    window = Maincontroller()
    module_setup()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


