"""
Created on 24-Aug-2017

@author: Reshma
"""

from view_main import Ui_Dialog
from ui_extendedendplate  import  Ui_MainWindow
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
import sys
import os
from drawing_2D import ExtendedEndPlate


# class ViewFile(QDialog):
#     def __init__(self, parent=None):
#         QDialog.__init__(self, parent)
#         self.ui = Ui_Dialog()
#         self.ui.setupUi(self)
#         self.mainController = parent

class Maincontroller(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnFront.clicked.connect(lambda : self.go_to_drawing("Front"))
        self.ui.btnTop.clicked.connect(lambda : self.go_to_drawing("Top"))
        self.ui.btnSide.clicked.connect(lambda : self.go_to_drawing("Side"))

    def go_to_drawing(self, view):
        beam_beam = ExtendedEndPlate()
        if view == "Front":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Extended_bothway\Front.svg"
            beam_beam.save_to_svg(filename, view)
        elif view == "Side":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Extended_bothway\Side.svg"
            beam_beam.save_to_svg(filename, view)
        else:
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Extended_bothway\Top.svg"
            beam_beam.save_to_svg(filename, view)


def main():
    app = QApplication(sys.argv)
    window = Maincontroller()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()