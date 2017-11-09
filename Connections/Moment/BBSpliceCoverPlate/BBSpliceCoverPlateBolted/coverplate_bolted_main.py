"""
Created on 7-November-2017

@author: Reshma Konjari
"""
from ui_coverplatebolted import Ui_MainWindow
from ui_flangespliceplate import Ui_Flangespliceplate
from ui_webspliceplate import Ui_Webspliceplate
from cover_plate_bolted_calc import coverplateboltedconnection
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
from model import *
import sys

class Flangespliceplate(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Flangespliceplate()
        self.ui.setupUi(self)
        self.maincontroller = parent

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


        self.ui.combo_connLoc.setCurrentIndex(0)
        self.ui.combo_connLoc.currentIndexChanged.connect(self.get_beamdata)
        # self.get_beamdata()
        self.gradeType = {'Please select type': '', 'HSFG': [8.8, 10.9],
                          'Bearing Bolt': [3.6, 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8, 10.9, 12.9]}
        self.ui.combo_type.addItems(self.gradeType.keys())
        self.ui.combo_type.currentIndexChanged[str].connect(self.combotype_current_index_changed)
        self.ui.combo_type.setCurrentIndex(0)

        self.ui.btn_Design.clicked.connect(self.design_btnclicked)

        self.ui.btn_flangePlate.clicked.connect(self.flangesplice_plate)
        self.ui.btn_webPlate.clicked.connect(self.websplice_plate)

    def get_beamdata(self):
        loc = self.ui.combo_connLoc.currentText()
        beamdata = get_beamcombolist()
        if loc == 'Beam-Beam':
            self.ui.combo_beamSec.addItems(beamdata)

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

    def design_btnclicked(self):
        self.uiObj = self.get_user_inputs()
        outputs = coverplateboltedconnection(self.uiObj)
        # self.resultObj = outputs.cov
        self.display_output(outputs)

    def display_output(self, outputObj):
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                if (outputObj[k][key] == ""):
                    resultObj = outputObj
                else:
                    resultObj = outputObj
        flange_shear_capacity = resultObj["Fla"]

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
