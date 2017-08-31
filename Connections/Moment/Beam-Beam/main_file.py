"""

"""

from view_main import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QApplication
import sys
import os
from drawing_2D import ExtendedEndPlate

# class ViewFile(QDialog):
#     def __init__(self, parent=None):
#         QDialog.__init__(self, parent)
#         self.ui = Ui_Dialog()
#         self.ui.setupUi(self)
#         self.mainController = parent

class Maincontroller(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Drawing views")
        self.ui.pushButton.clicked.connect(lambda : self.go_to_drawing("Front"))
        self.ui.pushButton_2.clicked.connect(lambda : self.go_to_drawing("Top"))
        self.ui.pushButton_3.clicked.connect(lambda : self.go_to_drawing("Side"))

    def go_to_drawing(self, view):
        beam_beam = ExtendedEndPlate()
        if view == "Front":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Beam-Beam\Front.svg"
            beam_beam.save_to_svg(filename, view)
        elif view == "Side":
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Beam-Beam\Side.svg"
            beam_beam.save_to_svg(filename, view)
        else:
            filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Beam-Beam\Top.svg"
            beam_beam.save_to_svg(filename, view)


def main():
    app = QApplication(sys.argv)
    window = Maincontroller()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()