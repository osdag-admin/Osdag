from osdag_gui.main_window import LaunchScreenPopup
from PySide6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    splash = LaunchScreenPopup()
    splash.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()