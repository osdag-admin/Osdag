from design_type.connection.fin_plate_connection import FinPlateConnection
from PyQt5.QtCore import QFile, pyqtSignal, QTextStream, Qt, QIODevice
from PyQt5.QtWidgets import QMainWindow, QDialog, QFontDialog, QApplication, QFileDialog, QColorDialog
import sys
import os.path
from gui.ui_template import Ui_ModuleWindow

class MainController(QMainWindow):
    closed = pyqtSignal()
    def __init__(self, Ui_ModuleWindow, main, folder):
        super(MainController,self).__init__()
        QMainWindow.__init__(self)
        self.ui = Ui_ModuleWindow()
        self.ui.setupUi(self, main)
        self.folder = folder

if __name__ == '__main__':
    app = QApplication(sys.argv)
    folder_path = r'C:\Users\Deepthi\Desktop\OsdagWorkspace'
    # folder_path = r'C:\Users\Win10\Desktop'
    # folder_path = r'C:\Users\pc\Desktop'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path, 0o755)
    image_folder_path = os.path.join(folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0o755)
    print(Ui_ModuleWindow,FinPlateConnection,folder_path)
    window = MainController(Ui_ModuleWindow,FinPlateConnection,folder_path)
    print(window)
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("ERROR")
