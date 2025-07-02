
from osdag_gui.ui.windows.launchScreen_UI import OsdagLaunchScreen

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread, Signal

class LoadingThread(QThread):
    finished = Signal()

    def run(self):
        # Simulate loading (replace with your real setup)
        import time
        time.sleep(15)
        self.finished.emit()

class LaunchScreenPopup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = OsdagLaunchScreen()
        self.ui.setupUi(self)
        self.show()

        self.loader = LoadingThread()
        self.loader.finished.connect(self.close_and_launch)
        self.loader.start()

    def close_and_launch(self):
        self.close()