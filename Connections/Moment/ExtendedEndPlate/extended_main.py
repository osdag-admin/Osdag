"""
Created on 24-Aug-2017

@author: Reshma
"""

from ui_extendedendplate import Ui_MainWindow
from ui_design_preferences import Ui_DesignPreference
from bbExtendedEndPlateSpliceCalc import bbExtendedEndPlateSplice
from drawing_2D import ExtendedEndPlate
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.Qt import QColor, QBrush, Qt, QIntValidator, QDoubleValidator, QFile
from model import *
import sys
import os
import pickle

class DesignPreference(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_DesignPreference()
        self.ui.setupUi(self)
        self.maincontroller = parent

        self.saved = None
        self.ui.combo_design_method.model().item(1).setEnabled(False)
        self.ui.combo_design_method.model().item(2).setEnabled(False)
        # self.set_default_para()
        dbl_validator = QDoubleValidator()
        self.ui.txt_boltFu.setValidator(dbl_validator)
        self.ui.txt_boltFu.setMaxLength(7)
        self.ui.txt_weldFu.setValidator(dbl_validator)
        self.ui.txt_weldFu.setMaxLength(7)
        self.ui.txt_detailingGap.setValidator(dbl_validator)
        self.ui.txt_detailingGap.setMaxLength(5)
        # self.ui.btn_defaults.clicked.connect(self.set_default_para)
        self.ui.btn_save.clicked.connect(self.save_designPref_para)
        self.ui.btn_close.clicked.connect(self.close_designPref)
        # self.ui.combo_boltHoleType.currentIndexChanged[str].connect(self.get_clearance)

    def save_designPref_para(self):
        uiObj = self.maincontroller.get_user_inputs()
        self.saved_designPref = {}
        self.saved_designPref["bolt"] = {}
        self.saved_designPref["bolt"]["bolt_type"] = str(self.ui.combo_boltType.currentText())
        self.saved_designPref["bolt"]["bolt_hole_type"] = str(self.ui.combo_boltHoleType.currentText())
        # self.saved_designPref["bolt"]["bolt_hole_clrnce"] = self.get_clearance()
        self.saved_designPref["bolt"]["bolt_fu"] = int(str(self.ui.txt_boltFu.text()))
        self.saved_designPref["bolt"]["slip_factor"] = float(str(self.ui.combo_slipfactor.currentText()))

        self.saved_designPref["weld"] = {}
        weldType = str(self.ui.combo_weldType.currentText())
        self.saved_designPref["weld"]["typeof_weld"] = weldType
        if weldType == "Shop weld":
            self.saved_designPref["weld"]["safety_factor"] = float(1.25)
        else:
            self.saved_designPref["weld"]["safety_factor"] = float(1.5)
        self.saved_designPref["weld"]["fu_overwrite"] = self.ui.txt_weldFu.text()

        self.saved_designPref["detailing"] = {}
        typeOfEdge = str(self.ui.combo_detailingEdgeType.currentText())
        self.saved_designPref["detailing"]["typeof_edge"] = typeOfEdge
        if typeOfEdge == "a - Sheared or hand flame cut":
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.7)
        else:
            self.saved_designPref["detailing"]["min_edgend_dist"] = float(1.5)
        if self.ui.txt_detailingGap.text() == '':

            self.saved_designPref["detailing"]["gap"] = float(10)
        else:
            self.saved_designPref["detailing"]["gap"] = float(self.ui.txt_detailingGap.text())

        self.saved_designPref["detailing"]["is_env_corrosive"] = str(self.ui.combo_detailing_memebers.currentText())
        self.saved_designPref["design"] = {}
        self.saved_designPref["design"]["design_method"] = str(self.ui.combo_design_method.currentText())
        self.saved = True

        QMessageBox.about(self, 'Information', "Preferences saved")

        return self.saved_designPref

    def close_designPref(self):
        self.close()


class Maincontroller(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.get_beamdata()
        self.resultobj = None
        # self.ui.combo_connLoc.setCurrentIndex(0)
        # self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
        # self.ui.combo_beamSec.setCurrentIndex(0)
        self.gradeType = {'Please select type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)
        self.retrieve_prevstate()

        self.ui.btnFront.clicked.connect(lambda : self.call_2D_drawing("Front"))
        self.ui.btnTop.clicked.connect(lambda : self.call_2D_drawing("Top"))
        self.ui.btnSide.clicked.connect(lambda : self.call_2D_drawing("Side"))

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        self.ui.btn_Reset.clicked.connect(self.reset_btnclicked)
        self.ui.actionDesign_Preferences.triggered.connect(self.design_prefer)

        validator = QIntValidator()
        self.ui.txt_Fu.setValidator(validator)
        self.ui.txt_Fy.setValidator(validator)

        doubl_validator = QDoubleValidator()
        self.ui.txt_Moment.setValidator(doubl_validator)
        self.ui.txt_Shear.setValidator(doubl_validator)
        self.ui.txt_Axial.setValidator(doubl_validator)
        self.ui.txt_plateHeight.setValidator(doubl_validator)
        self.ui.txt_plateWidth.setValidator(doubl_validator)

        min_fu = 290
        max_fu = 590
        self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txt_Fy.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fy, min_fy, max_fy))

    def get_user_inputs(self):
        uiObj = {}
        uiObj["Member"] = {}
        uiObj["Member"]["Connectivity"] = str(self.ui.combo_connLoc.currentText())
        uiObj["Member"]["BeamSection"] = str(self.ui.combo_beamSec.currentText())
        uiObj["Member"]["fu (MPa)"] = self.ui.txt_Fu.text()
        uiObj["Member"]["fy (MPa)"] = self.ui.txt_Fy.text()

        uiObj["Load"] = {}
        uiObj["Load"]["ShearForce (kN)"] = self.ui.txt_Shear.text()
        uiObj["Load"]["Moment (kNm)"] = self.ui.txt_Moment.text()
        uiObj["Load"]["AxialForce (kN)"] = self.ui.txt_Axial.text()

        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.combo_diameter.currentText()
        uiObj["Bolt"]["Grade"] = self.ui.combo_grade.currentText()
        uiObj["Bolt"]["Type"] = self.ui.combo_type.currentText()

        uiObj["Plate"] = {}
        uiObj["Plate"]["Thickness (mm)"] = str(self.ui.combo_plateThick.currentText())
        uiObj["Plate"]["Height (mm)"] = str(self.ui.txt_plateHeight.text())
        uiObj["Plate"]["Width (mm)"] = str(self.ui.txt_plateWidth.text())

        uiObj["Weld"] = {}
        uiObj["Weld"]["Flange (mm)"] = self.ui.combo_flangeSize.currentText()
        uiObj["Weld"]["Web (mm)"] = self.ui.combo_webSize.currentText()
        return uiObj

    def design_prefer(self):
        section = DesignPreference(self)
        section.show()

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

        Returns: Retrieve the previous user inputs

        """
        uiObj = self.get_prevstate()
        self.set_dict_touser_inputs(uiObj)

    def set_dict_touser_inputs(self, uiObj):
        """

        Args:
            uiObj: User inputs

        Returns: Set the dictionary to user inputs

        """
        if uiObj is not None :
            self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(str(uiObj["Member"]["Connectivity"])))
            if uiObj["Member"]["Connectivity"] == "Flush" or "Extended one way" or "Extended both ways":
                self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(uiObj["Member"]["Connectivity"]))
                self.ui.combo_beamSec.setCurrentIndex(self.ui.combo_beamSec.findText(uiObj["Member"]["BeamSection"]))
                self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
                self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
                self.ui.txt_Shear.setText(str(uiObj["Load"]["ShearForce (kN)"]))
                self.ui.txt_Axial.setText(str(uiObj["Load"]["AxialForce (kN)"]))
                self.ui.txt_Moment.setText(str(uiObj["Load"]["Moment (kNm)"]))
                self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
                self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
                self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
                self.ui.combo_plateThick.setCurrentIndex(self.ui.combo_plateThick.findText(uiObj["Plate"]["Thickness (mm)"]))
                self.ui.txt_plateHeight.setText(str(uiObj["Plate"]["Height (mm)"]))
                self.ui.txt_plateWidth.setText(str(uiObj["Plate"]["Width (mm)"]))
                self.ui.combo_flangeSize.setCurrentIndex(self.ui.combo_flangeSize.findText(uiObj["Weld"]["Flange (mm)"]))
                self.ui.combo_webSize.setCurrentIndex(self.ui.combo_webSize.findText(uiObj["Weld"]["Web (mm)"]))

        else:
            pass

    def design_btnclicked(self):
        self.uiObj = self.get_user_inputs()
        print self.uiObj
        outputs = bbExtendedEndPlateSplice(self.uiObj)

    def reset_btnclicked(self):
        self.ui.combo_beamSec.setCurrentIndex(0)
        self.ui.combo_connLoc.setCurrentIndex(0)
        self.ui.txt_Fu.clear()
        self.ui.txt_Fy.clear()
        self.ui.txt_Axial.clear()
        self.ui.txt_Shear.clear()
        self.ui.txt_Moment.clear()
        self.ui.combo_diameter.setCurrentIndex(0)
        self.ui.combo_type.setCurrentIndex(0)
        self.ui.combo_grade.setCurrentIndex(0)
        self.ui.combo_plateThick.setCurrentIndex(0)
        self.ui.txt_plateHeight.clear()
        self.ui.txt_plateWidth.clear()
        self.ui.combo_flangeSize.setCurrentIndex(0)
        self.ui.combo_webSize.setCurrentIndex(0)

    def get_beamdata(self):
        loc = self.ui.combo_connLoc.currentText()
        beamdata = get_beamcombolist()
        old_beamdata = get_oldbeamcombolist()
        combo_section = ''
        self.ui.combo_beamSec.addItems(beamdata)
        combo_section = self.ui.combo_beamSec
        self.color_oldDatabase_section(old_beamdata, beamdata, combo_section)

    def color_oldDatabase_section(self, old_section, intg_section, combo_section):
        """

        Args:
            old_section: Old database
            intg_section: Integrated database
            combo_section: Contents of database

        Returns: Differentiate the database by color code

        """
        for col in old_section:
            if col in intg_section:
                indx = intg_section.index(str(col))
                combo_section.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

        duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]
        for i in duplicate:
            combo_section.setItemData(i, QBrush(QColor("red")), Qt.TextColorRole)

    def fetchBeamPara(self):
        beamdata_sec = self.ui.combo_beamSec.currentText()
        dictbeamdata = get_beamdata(beamdata_sec)
        return  dictbeamdata

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
        if (text_str < min_val or text_str > max_val or text_str == ''):
            QMessageBox.about(self, "Error", "Please enter a value between %s-%s" % (min_val, max_val))
            widget.clear()
            widget.setFocus()

    def call_2D_drawing(self, view):
        beam_beam = ExtendedEndPlate()
        if view == "Front":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\ExtendedEndPlate\Front.svg"
            beam_beam.save_to_svg(filename, view)
        elif view == "Side":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\ExtendedEndPlate\Side.svg"
            beam_beam.save_to_svg(filename, view)
        else:
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\ExtendedEndPlate\Top.svg"
            beam_beam.save_to_svg(filename, view)


def main():
    app = QApplication(sys.argv)
    module_setup()
    window = Maincontroller()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()