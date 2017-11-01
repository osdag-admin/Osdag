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
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.QtGui import QIntValidator, QPalette, QDoubleValidator
from PyQt5.Qt import Qt
from model import *
import sys
import os

class SingleAngleSelection(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Singleangle()
        self.ui.setupUi(self)
        self.maincontroller = parent

        self.ui.comboBox_sign_angle.setCurrentIndex(0)
        self.ui.comboBox_sign_angle.currentIndexChanged.connect(self.get_angledata)
        self.ui.comboBox_sign_leg.setEnabled(False)
        self.ui.btn_save.clicked.connect(self.save_singledata_para)
        self.ui.btn_close.clicked.connect(self.close_singledata_para)

    def save_singledata_para(self):

        self.save_singledata = {}
        self.save_singledata["SingleAngle"] = {}
        self.save_singledata["SingleAngle"]["angle_type"] = {}
        self.save_singledata["SingleAngle"]["angle_type"]["type"] = str(self.ui.comboBox_sign_angle.currentText())
        self.save_singledata["SingleAngle"]["angle_type"]["section"] = str(self.ui.comboBox_sign_selct_section.currentText())
        self.save_singledata["SingleAngle"]["leg"] = str(self.ui.comboBox_sign_leg.currentText())
        print self.save_singledata, "Single data"
        QMessageBox.about(self, 'Information', "Single angle data saved")

        return self.save_singledata

    def close_singledata_para(self):
        self.close()

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

        # self.ui.comboBox_channel.setCurrentIndex(0)
        # self.ui.comboBox_channel.currentIndexChanged.connect(self.get_channeldata)
        self.ui.btn_save.clicked.connect(self.save_channel_para)
        self.ui.btn_close.clicked.connect(self.close_channel_para)

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
        QDialog.__init__(self, parent)
        self.ui = Ui_Selection()
        self.ui.setupUi(self)
        self.maincontroller = parent

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

    # def define_members(self):
    #     """
    #
    #     Returns: Shows the define members list depending on members selected
    #
    #     """
        ui_obj = self.maincontroller.get_user_inputs()
        no_of_member = ui_obj["Member"]["No. of members"]
        print no_of_member, "no_of_member"

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

        elif no_of_member == '7':
            no_member_display = str(no_of_member)
            # self.ui.lineEdit_no_of_member.setText(no_member_display)
            pass

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


class BoltOutput(QDialog):
    def __init__(self):
        QDialog.__init__(self, parent=None)



class Maincontroller(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_section.clicked.connect(self.section_selection)
        self.ui.combo_member.setItemText(0, "Select no.of members")
        self.ui.combo_member.setCurrentIndex(0)
        self.ui.btn_Reset.clicked.connect(self.reset_button_clicked)

    def section_selection(self):
        section = SectionSelection(self)
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
        ui_obj["Member"]["Members"] = self.ui.btn_section.text()          #TODO call define members dictionary
        ui_obj["Member"]["fu (MPa)"] = self.ui.txt_Fu.text()
        ui_obj["Member"]["fy (MPa)"] = self.ui.txt_Fy.text()
        # ui_obj["Member"]["Section"] =

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


