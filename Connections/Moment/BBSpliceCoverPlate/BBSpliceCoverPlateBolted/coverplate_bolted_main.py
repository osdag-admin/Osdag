"""
Created on 7-November-2017

@author: Reshma Konjari
"""
from ui_coverplatebolted import Ui_MainWindow
from ui_flangespliceplate import Ui_Flangespliceplate
from ui_webspliceplate import Ui_Webspliceplate
from svg_window import SvgWindow
from cover_plate_bolted_calc import coverplateboltedconnection
from drawing_2D import CoverEndPlate
from ui_design_preferences import Ui_DesignPreference
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
from PyQt5.Qt import QIntValidator, QDoubleValidator, QFile, Qt, QBrush, QColor
from model import *
import sys
import os.path
import pickle

class DesignPreferences(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_DesignPreference()
        self.ui.setupUi(self)
        self.maincontroller = parent

        self.saved = None
        self.ui.tabWidget.removeTab(1)
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


class Flangespliceplate(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Flangespliceplate()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller # TODO pass dictionary
        # resultObj_flangeplate = coverplateboltedconnection(uiObj)

        # self.ui.txt_plateHeight.setText()


class Webspliceplate(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Webspliceplate()
        self.ui.setupUi(self)
        self.maincontroller = parent


class MainController(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.get_beamdata()
        self.resultObj = None
        # self.ui.combo_connLoc.setCurrentIndex(0)
        # self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
        # self.ui.combo_beamSec.setCurrentIndex(0)
        self.gradeType = {'Please select type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)
        self.retrieve_prevstate()

        self.ui.btnFront.clicked.connect(lambda: self.call_2D_drawing("Front"))
        self.ui.btnTop.clicked.connect(lambda: self.call_2D_drawing("Top"))
        self.ui.btnSide.clicked.connect(lambda: self.call_2D_drawing("Side"))

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        self.ui.actionDesign_Preferences.triggered.connect(self.design_prefer)
        self.ui.btn_flangePlate.clicked.connect(self.flangesplice_plate)
        self.ui.btn_webPlate.clicked.connect(self.websplice_plate)

        validator = QIntValidator()
        self.ui.txt_Fu.setValidator(validator)
        self.ui.txt_Fy.setValidator(validator)

        doubl_validator = QDoubleValidator()
        self.ui.txt_Moment.setValidator(doubl_validator)
        self.ui.txt_Shear.setValidator(doubl_validator)
        self.ui.txt_Axial.setValidator(doubl_validator)
        self.ui.txt_flangeplateHeight.setValidator(doubl_validator)
        self.ui.txt_flangeplateWidth.setValidator(doubl_validator)
        self.ui.txt_webplateHeight.setValidator(doubl_validator)
        self.ui.txt_webplateWidth.setValidator(doubl_validator)

        min_fu = 290
        max_fu = 590
        self.ui.txt_Fu.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fu, min_fu, max_fu))

        min_fy = 165
        max_fy = 450
        self.ui.txt_Fy.editingFinished.connect(lambda: self.check_range(self.ui.txt_Fy, min_fy, max_fy))

    def get_beamdata(self):
        """

        Returns: Selects beam data from both Old & Integrated database

        """
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
        if (text_str < min_val or text_str > max_val or text_str == ' '):
            QMessageBox.about(self, "Error", "Please enter a value between %s-%s"%(min_val, max_val))
            widget.clear()
            widget.setFocus()

    def get_user_inputs(self):
        """

        Returns: User Input dictionary

        """
        uiObj = {}
        uiObj["Member"] = {}
        uiObj["Member"]["Connectivity"] = str(self.ui.combo_connLoc.currentText())
        uiObj["Member"]["BeamSection"] = str(self.ui.combo_beamSec.currentText())
        uiObj["Member"]["fu (MPa)"] = self.ui.txt_Fu.text()
        uiObj["Member"]["fy (MPa)"] = self.ui.txt_Fy.text()

        uiObj["Load"] = {}
        uiObj["Load"]["ShearForce (kN)"] = self.ui.txt_Shear.text()
        uiObj["Load"]["Moment (kNm)"] = self.ui.txt_Moment.text()
        uiObj["Load"]["AxialForce"] = self.ui.txt_Axial.text()

        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.combo_diameter.currentText()
        uiObj["Bolt"]["Grade"] = self.ui.combo_grade.currentText()
        uiObj["Bolt"]["Type"] = self.ui.combo_type.currentText()

        uiObj["FlangePlate"] = {}
        uiObj["FlangePlate"]["Thickness (mm)"] = self.ui.combo_flangeplateThick.currentText()
        uiObj["FlangePlate"]["Height (mm)"] = self.ui.txt_flangeplateHeight.text()
        uiObj["FlangePlate"]["Width (mm)"] = self.ui.txt_flangeplateWidth.text()

        uiObj["WebPlate"] = {}
        uiObj["WebPlate"]["Thickness (mm)"] = self.ui.combo_webplateThick.currentText()
        uiObj["WebPlate"]["Height (mm)"] = self.ui.txt_webplateHeight.text()
        uiObj["WebPlate"]["Width (mm)"] = self.ui.txt_webplateWidth.text()
        return uiObj

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
        self.ui.combo_flangeplateThick.setCurrentIndex(0)
        self.ui.txt_flangeplateHeight.clear()
        self.ui.txt_flangeplateWidth.clear()
        self.ui.combo_webplateThick.setCurrentIndex(0)
        self.ui.txt_webplateWidth.clear()
        self.ui.txt_webplateHeight.clear()

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
        if uiObj is not None:
            self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(str(uiObj["Member"]["Connectivity"])))
            if uiObj["Member"]["Connectivity"] == "Beam-Beam" or "Select Connectivity":
                self.ui.combo_connLoc.setCurrentIndex(self.ui.combo_connLoc.findText(uiObj["Member"]["Connectivity"]))
                self.ui.combo_beamSec.setCurrentIndex(self.ui.combo_beamSec.findText(uiObj["Member"]["BeamSection"]))
                self.ui.txt_Fu.setText(str(uiObj["Member"]["fu (MPa)"]))
                self.ui.txt_Fy.setText(str(uiObj["Member"]["fy (MPa)"]))
                self.ui.txt_Shear.setText(str(uiObj["Load"]["ShearForce (kN)"]))
                self.ui.txt_Axial.setText(str(uiObj["Load"]["AxialForce"]))
                self.ui.txt_Moment.setText(str(uiObj["Load"]["Moment (kNm)"]))
                self.ui.combo_diameter.setCurrentIndex(self.ui.combo_diameter.findText(uiObj["Bolt"]["Diameter (mm)"]))
                self.ui.combo_type.setCurrentIndex(self.ui.combo_type.findText(uiObj["Bolt"]["Type"]))
                self.ui.combo_grade.setCurrentIndex(self.ui.combo_grade.findText(uiObj["Bolt"]["Grade"]))
                self.ui.combo_flangeplateThick.setCurrentIndex(self.ui.combo_flangeplateThick.findText(uiObj["FlangePlate"]["Thickness (mm)"]))
                self.ui.combo_webplateThick.setCurrentIndex(self.ui.combo_webplateThick.findText(uiObj["WebPlate"]["Thickness (mm)"]))
                self.ui.txt_flangeplateHeight.setText(str(uiObj["FlangePlate"]["Height (mm)"]))
                self.ui.txt_flangeplateWidth.setText(str(uiObj["FlangePlate"]["Width (mm)"]))
                self.ui.txt_webplateHeight.setText(str(uiObj["WebPlate"]["Height (mm)"]))
                self.ui.txt_webplateWidth.setText(str(uiObj["WebPlate"]["Width (mm)"]))

        else:
            pass

    def design_prefer(self):
        section = DesignPreferences(self)
        section.show()

    def design_btnclicked(self):
        """

        Returns:

        """
        self.uiObj = self.get_user_inputs()
        outputs = coverplateboltedconnection(self.uiObj)
        # self.resultObj = outputs
        # alist =self.resultObj.values()
        # self.display_output(self.resultObj)
        # isempty = [True if val != '' else False for ele in alist for val in ele.values()]

    def display_output(self, outputObj):
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                if (outputObj[k][key] == ""):
                    resultObj = outputObj
                else:
                    resultObj = outputObj

        flange_shear_capacity = resultObj["FlangeBolt"]["ShearCapacity"]
        self.ui.txt_shearCapacity.setText(str(flange_shear_capacity))

        flange_bearing_capacity =resultObj["FlangeBolt"]["BearingCapacity"]
        self.ui.txt_bearCapacity.setText(str(flange_bearing_capacity))

        flange_capacity_bolt = resultObj["FlangeBolt"]["CapacityBolt"]
        self.ui.txt_capacityOfbolt.setText(str(flange_capacity_bolt))

        flange_bolt_req = resultObj["FlangeBolt"]["BoltsRequired"]
        self.ui.txt_noBolts.setText(str(flange_bolt_req))

        flange_pitch = resultObj["FlangeBolt"]["Pitch"]
        self.ui.txt_pitch.setText(str(flange_pitch))

        flange_gauge = resultObj["FlangeBolt"]["Gauge"]
        self.ui.txt_gauge.setText(str(flange_gauge))

        flange_enddist = resultObj["FlangeBolt"]["End"]
        self.ui.txt_endDist.setText(str(flange_enddist))

        flange_edgedist = resultObj["FlangeBolt"]["Edge"]
        self.ui.txt_edgeDist.setText(str(flange_edgedist))

        web_shear_capacity = resultObj["WebBolt"]["ShearCapacity"]
        self.ui.txt_shearCapacity_2.setText(str(web_shear_capacity))

        web_bearing_capacity =resultObj["WebBolt"]["BearingCapacity"]
        self.ui.txt_bearCapacity_2.setText(str(web_bearing_capacity))

        web_capacity_bolt = resultObj["WebBolt"]["CapacityBolt"]
        self.ui.txt_capacityOfbolt_2.setText(str(web_capacity_bolt))

        web_bolt_req = resultObj["WebBolt"]["BoltsRequired"]
        self.ui.txt_noBolts_2.setText(str(web_bolt_req))

        web_pitch = resultObj["WebBolt"]["Pitch"]
        self.ui.txt_pitch_2.setText(str(web_pitch))

        web_gauge = resultObj["WebBolt"]["Gauge"]
        self.ui.txt_gauge_2.setText(str(web_gauge))

        web_enddist = resultObj["WebBolt"]["End"]
        self.ui.txt_endDist_2.setText(str(web_enddist))

        web_edgedist = resultObj["WebBolt"]["Edge"]
        self.ui.txt_edgeDist_2.setText(str(web_edgedist))


    def call_2D_drawing(self, view):
        """

        Args:
            view: Front, Side & Top views

        Returns: Saves 2D svg drawings

        """
        beam_beam = CoverEndPlate()
        if view == "Front":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\BBSpliceCoverPlate\BBSpliceCoverPlateBolted\Front.svg"
            beam_beam.save_to_svg(filename, view)
        elif view == "Side":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\BBSpliceCoverPlate\BBSpliceCoverPlateBolted\Side.svg"
            beam_beam.save_to_svg(filename, view)
        else:
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\BBSpliceCoverPlate\BBSpliceCoverPlateBolted\Top.svg"
            beam_beam.save_to_svg(filename, view)

    def flangesplice_plate(self):
        section = Flangespliceplate(self)
        section.show()

    def websplice_plate(self):
        section = Webspliceplate(self)
        section.show()

def main():
    app = QApplication(sys.argv)
    module_setup()
    window = MainController()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
