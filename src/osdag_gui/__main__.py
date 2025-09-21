"""
Entry point for Osdag GUI application.
Handles splash screen and main window launch.
"""
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon
from osdag_gui.ui.windows.launch_screen import OsdagLaunchScreen
from osdag_gui.data.database.database_config import refactor_database, create_user_database
import sys

class LoadingThread(QThread):
    finished = Signal()

    def run(self):
        import time
        self.create_sqlite()
        # Create user database if not exist
        create_user_database()
        # Clean up user database to ensure 10 records and atmost 60 days older with path exist
        refactor_database()
        time.sleep(5)
        self.finished.emit()

    def create_sqlite(self):
        import os
        from importlib.resources import files

        ############################ Pre-Build Database Updation/Creation #################
        sqlpath = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sql')
        sqlitepath = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sqlite')

        if sqlpath.exists():
            if not sqlitepath.exists():
                cmd = 'sqlite3 ' + str(sqlitepath) + ' < ' + str(sqlpath)
                os.system(cmd)
                sqlpath.touch()
                print('Database Created')

            elif sqlitepath.stat().st_size == 0 or sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1:
                try:
                    sqlitenewpath = files('osdag.data.ResourceFiles.Database').joinpath('Intg_osdag_new.sqlite')
                    cmd = 'sqlite3 ' + str(sqlitenewpath) + ' < ' + str(sqlpath)
                    error = os.system(cmd)
                    print(error)
                    os.remove(sqlitepath)
                    sqlitenewpath.rename(sqlitepath)
                    sqlpath.touch()
                    print('Database Updated', sqlpath.stat().st_mtime, sqlitepath.stat().st_mtime)
                except Exception as e:
                    sqlitenewpath.unlink()
                    print('Error: ', e)

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
        from osdag_gui.main_window import MainWindow
        app.main_window = MainWindow()
        app.main_window.show()

    splash = LaunchScreenPopup(on_finish=show_main_window)
    splash.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()