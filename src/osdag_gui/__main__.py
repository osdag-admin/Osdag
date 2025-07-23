"""
Entry point for Osdag GUI application.
Handles splash screen and main window launch.
"""
from osdag_gui.main_window import MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, Signal
from osdag_gui.ui.windows.launch_screen import OsdagLaunchScreen
import sys

class LoadingThread(QThread):
    finished = Signal()

    def run(self):
        import time
        time.sleep(5)
        self.finished.emit()

class LaunchScreenPopup(QMainWindow):
    def __init__(self, on_finish):
        super().__init__()
        self.ui = OsdagLaunchScreen()
        self.ui.setupUi(self)
        self.show()

        self.loader = LoadingThread()
        self.loader.finished.connect(self.close_and_launch)
        self.on_finish = on_finish
        self.loader.start()

    def close_and_launch(self):
        self.close()
        if self.on_finish:
            self.on_finish()

def main():
    app = QApplication(sys.argv)

    def show_main_window():
        app.main_window = MainWindow()
        app.main_window.show()

    splash = LaunchScreenPopup(on_finish=show_main_window)
    splash.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()