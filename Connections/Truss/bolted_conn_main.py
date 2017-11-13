"""
Created on 27-Sept-2017

@author: Reshma Konjari
"""
from ui_boltedconnection import Ui_MainWindow
from ui_selection import Ui_Selection
from ui_singleangle import Ui_Singleangle
from ui_doubleangle import Ui_Doubleangle
from ui_channel import Ui_Channel
from ui_output import Ui_BoltOutput
from newoutput import Ui_Table
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIntValidator, QPalette, QDoubleValidator
from PyQt5.Qt import Qt
from model import *
import sys
import os

class NewTable(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Table()
        self.ui.setupUi(self)
        self.maincontroller = parent

        item = "23.341343"
        self.ui.tableWidget.setItem(2, 2, QTableWidgetItem(item))
        self.ui.tableWidget.setRowHidden(6, True)


class SingleAngleSelection(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle()
        self.ui.setupUi(self)
        self.maincontroller = parent
        self.sectionselection = parent
        self.saved =None

        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.save_singledata_para)
        self.ui.btn_save.clicked.connect(self.lbl_section)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):

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
        self.close()

    def lbl_section(self):
        ui_sing_obj = self.save_singledata_para()
        type = ui_sing_obj["SingleAngle"]["angle_type"]["type"]
        section = ui_sing_obj["SingleAngle"]["angle_type"]["section"]
        leg = ui_sing_obj["SingleAngle"]["leg"]
        print ui_sing_obj, type, section, leg

        section_type = self.sectionselection.ui.comboBx_selection.currentText()
        if section_type == "Select type":
            pass
        elif section_type == "Single Angle":
            if type == "Equal angle":
                section_label = self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section)
            else:
                section_label = self.sectionselection.ui.lbl_sectionSelection.setText(type + ' ' + section + ' ' + leg)

        section_type2 = self.sectionselection.ui.comboBx_selection_2.currentText()
        if section_type2 == "Select type":
            pass
        else:
            if type == "Equal angle":
                section_label2 = self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section)
            else:
                section_label2 = self.sectionselection.ui.lbl_sectionSelection_2.setText(type + ' ' + section + ' ' + leg)

        section_type3 = self.sectionselection.ui.comboBx_selection_3.currentText()
        if section_type3 == "Select type":
            pass
        else:
            if type == "Equal angle":
                section_label3 = self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section)
            else:
                section_label3 = self.sectionselection.ui.lbl_sectionSelection_3.setText(type + ' ' + section + ' ' + leg)


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

        self.ui.comboBox_doub_angle.setCurrentIndex(0)
        self.ui.comboBox_doub_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_doub_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.save_doubledata_para)
        self.ui.btn_close.clicked.connect(self.close_doubledata_para)

    def save_doubledata_para(self):

        self.save_doubledata = {}
        self.save_doubledata["DoubleAngle"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"] = {}
        self.save_doubledata["DoubleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_doub_angle.currentText())
        self.save_doubledata["DoubleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_doub_selct_section.currentText())
        self.save_doubledata["DoubleAngle"]["leg"] = str(self.ui.comboBox_doub_leg.currentText())
        print self.save_doubledata, "Double data"
        QMessageBox.about(self, 'Information', "Double angle data saved")

        return self.save_doubledata

    def close_doubledata_para(self):
        self.close()

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
        self.maincontroller = parent

        # if self.ui.comboBox_channel.itemText('Channel') == "Channel":
        #     pass
        # self.ui.comboBox_channel.itemText(self.get_channeldata)

        # self.ui.comboBox_channel.setCurrentIndex(0)
        # self.ui.comboBox_channel.currentIndexChanged.connect(self.get_channeldata)
        # self.ui.btn_save.clicked.connect(self.save_channel_para)
        # self.ui.btn_close.clicked.connect(self.close_channel_para)

    def save_channel_para(self):
        self.save_channeldata = {}
        self.save_channeldata["Channel"]["type"] = str(self.ui.comboBox_channel.currentIndex())
        self.save_channeldata["Channel"]["section"] = str(self.ui.comboBox_channl_selct_section.currentText())
        print self.save_channeldata, "Channel data"
        QMessageBox.about(self, "Information", "Channel data saved")

        return self.save_channeldata

    def close_channel_para(self):
        self.close()

    def get_channeldata(self):

        channeldata = get_channelcombolist()
        self.ui.comboBox_channl_selct_section.addItems(channeldata)

    def fetchChannelPara(self):
        channel_sec = self.ui.comboBox_channl_selct_section.currentText()
        dictchanneldata = get_channeldata(channel_sec)
        return dictchanneldata


class SectionSelection(QDialog):
    def __init__(self, parent=None):
        super(SectionSelection, self).__init__(parent)
        QDialog.__init__(self, parent)
        self.ui = Ui_Selection()
        self.ui.setupUi(self)
        self.maincontroller = parent

        self.singledataparams = SingleAngleSelection(self)
        self.doubledataparams = DoubleAngleSelection(self)
        self.channeldataparams = ChannelSelection(self)
        self.ui.btn_save.clicked.connect(self.save_definemembrs_para)
        self.ui.btn_close.clicked.connect(self.close_definemembrs_para)


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

            # self.ui.buttonBox.clicked.connect(self.save_user_inputs)

        # QMessageBox.about(self, 'Information', 'Define members saved')


    def save_user_inputs(self):
        pass
        # self.save_section = {}
        # self.save_section["members"] = {}
        # self.save_section["members"]["no. of members"] = str(self.ui.lineEdit_no_of_member.text())
        # self.save_section["angle"] = {}
        # print self.save_section, "inputs"

    def single_angle_selection1(self):
        """

        Returns: Select type of Angle

        """
        loc = self.ui.comboBx_selection.currentText()
        if loc == "Single Angle":
            self.single_angle()
        elif loc == "Double Angle":
            self.double_angle()
        elif loc == "Select type":
            pass
        else:
            self.channel()

    def single_angle_selection2(self):
        """

        Returns: Select type of Angle

        """
        loc1 = self.ui.comboBx_selection_2.currentText()
        if loc1 =="Single Angle":
            self.single_angle()
        elif loc1 == "Double Angle":
            self.double_angle()
        elif loc1 == "Select type":
            pass
        else:
            self.channel()

    def single_angle_selection3(self):
        """

        Returns: Select type of Angle

        """
        loc2 = self.ui.comboBx_selection_3.currentText()
        if loc2 == "Single Angle":
            self.single_angle()
        elif loc2 == "Double Angle":
            self.double_angle()
        elif loc2 == "Select type":
            pass
        else:
            self.channel()

    def single_angle_selection4(self):
        """

        Returns: Select type of Angle

        """
        loc3 = self.ui.comboBx_selection_4.currentText()
        if loc3 == "Single Angle":
            self.single_angle()
        elif loc3 == "Double Angle":
            self.double_angle()
        elif loc3 == "Select type":
            pass
        else:
            self.channel()

    def single_angle_selection5(self):
        """

        Returns: Select type of Angle

        """
        loc4 = self.ui.comboBx_selection_5.currentText()
        if loc4 == "Single Angle":
            self.single_angle()
        elif loc4 == "Double Angle":
            self.double_angle()
        elif loc4 == "Select type":
            pass
        else:
            self.channel()

    def single_angle_selection6(self):
        """

        Returns: Select type of Angle

        """
        loc5 = self.ui.comboBx_selection_6.currentText()
        if loc5 == "Single Angle":
            self.single_angle()
        elif loc5 == "Double Angle":
            self.double_angle()
        elif loc5 == "Select type":
            pass
        else:
            self.channel()

    def single_angle_selection7(self):
        """

        Returns: Select type of Angle

        """
        loc6 = self.ui.comboBx_selection_7.currentText()
        if loc6 == "Single Angle":
            self.single_angle()
        elif loc6 == "Double Angle":
            self.double_angle()
        elif loc6 == "Select type":
            pass
        else:
            self.channel()

    def single_angle(self):
        section = SingleAngleSelection(self)
        section.show()

    def double_angle(self):
        section = DoubleAngleSelection(self)
        section.show()

    def channel(self):
        section = ChannelSelection(self)
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

        # ui_obj = self.maincontroller.get_user_inputs()
        # no_of_member = ui_obj["Member"]["No. of members"]
        ui_obj = self.maincontroller.no_of_members()
        no_of_member = ui_obj
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


class Maincontroller(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_section.clicked.connect(self.section_selection)
        self.ui.combo_member.setItemText(0, "Select no.of members")
        self.ui.combo_member.setCurrentIndex(0)
        self.ui.combo_member.currentIndexChanged.connect(self.no_of_members)
        self.ui.btn_Reset.clicked.connect(self.reset_button_clicked)
        self.ui.btn_bolt_output.clicked.connect(self.bolt_output)

    def no_of_members(self):
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

    def get_user_inputs(self):
        """

        Returns: The dictionary objects with user input fields for designing truss bolted connection

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


def main():
    app = QApplication(sys.argv)
    window = Maincontroller()
    module_setup()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()


