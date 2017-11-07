"""
Created on 7-November-2017

@author: Reshma Konjari
"""
from ui_coverplatebolted import Ui_MainWindow
from ui_flangespliceplate import Ui_Flangespliceplate
from ui_webspliceplate import Ui_Webspliceplate
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication
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

        self.ui.btn_flangePlate.clicked.connect(self.flangesplice_plate)
        self.ui.btn_webPlate.clicked.connect(self.websplice_plate)

    def flangesplice_plate(self):
        section = Flangespliceplate(self)
        section.show()

    def websplice_plate(self):
        section = Webspliceplate(self)
        section.show()

def main():
    app = QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
