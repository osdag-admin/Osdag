from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
screen = app.screens()[0]
dpi = screen.physicalDotsPerInch()
scale = round(dpi / 140.0, 1)