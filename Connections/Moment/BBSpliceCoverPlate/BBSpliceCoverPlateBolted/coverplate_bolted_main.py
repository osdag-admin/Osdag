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
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
from PyQt5.Qt import QIntValidator, QDoubleValidator, QFile, Qt, QBrush, QColor
from model import *
import sys
import os.path
import pickle

class Flangespliceplate(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Flangespliceplate()
        self.ui.setupUi(self)
        self.maincontroller = parent

        uiObj = self.maincontroller # TODO pass dictionary
        resultObj_flangeplate = coverplateboltedconnection(uiObj)

        self.ui.txt_plateHeight.setText()

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

        self.resultObj = None
        self.ui.combo_connLoc.setCurrentIndex(0)
        self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
        # self.get_beamdata()
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
        loc = self.ui.combo_connLoc.currentText()
        beamdata = get_beamcombolist()
        old_beamdata = get_oldbeamcombolist()
        # combo_section = ' '
        if loc == 'Beam-Beam':
            self.ui.combo_beamSec.addItems(beamdata)
            # combo_section = self.ui.combo_beamSec

        self.color_oldDatabase_section(old_beamdata, beamdata)

    def color_oldDatabase_section(self, old_section, intg_section):
        for col in old_section:
            if col in intg_section:
                indx = intg_section.index(str(col))
                self.ui.combo_beamSec.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)

        duplicate = [i for i, x in enumerate(intg_section) if intg_section.count(x) > 1]
        for i in duplicate:
            self.ui.combo_beamSec.setItemData(i, QBrush(QColor("red")), Qt.TextColorRole)


    def fetchBeamPara(self):
        beamdata_sec = self.ui.combo_beamSec.currentText()
        dictbeamdata = get_beamdata(beamdata_sec)
        return  dictbeamdata

    def combotype_current_index_changed(self, index):
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
        text_str = widget.text()
        text_str = int(text_str)
        if (text_str < min_val or text_str > max_val or text_str == ' '):
            QMessageBox.about(self, "Error", "Please enter a value between %s-%s"%(min_val, max_val))
            widget.clear()
            widget.setFocus()


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

    def closeEvent(self, event):
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
        input_file = QFile(os.path.join("saveINPUT.txt"))
        if not input_file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s: \n%s"
                                % (input_file.fileName(), input_file.errorString()))
        pickle.dump(uiObj, input_file)

    def get_prevstate(self):
        filename = os.path.join("saveINPUT.txt")
        if os.path.isfile(filename):
            file_object = open(filename, 'r')
            uiObj  = pickle.load(file_object)
            return uiObj
        else:
            return None

    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        self.set_dict_touser_inputs(uiObj)

    def set_dict_touser_inputs(self, uiObj):
        # if uiObj["Member"]["Connectivity"] == "Beam-Beam":
        if uiObj is not None :
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


    def design_btnclicked(self):
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
    window = MainController()
    module_setup()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
