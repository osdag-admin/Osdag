"""
Entry point for Osdag GUI application.
Handles splash screen and main window launch.
"""
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, Signal, QFile, QTextStream
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from osdag_gui.ui.windows.launch_screen import OsdagLaunchScreen
from osdag_gui.data.database.database_config import refactor_database, create_user_database
from osdag_core.cli import run_module
import osdag_gui.resources.resources_rc
import sys, click


class LoadingThread(QThread):
    finished = Signal()

    def run(self):
        import time
        self.create_sqlite()
        # Create user database if not exist
        create_user_database()
        # Clean up user database to ensure 10 records and atmost 60 days older with path exist
        refactor_database()
        time.sleep(10)
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

def GUI():
    app = QApplication(sys.argv)
    fid = QFontDatabase.addApplicationFont(":/fonts/UbuntuSans-Regular.ttf")
    font = QFontDatabase.applicationFontFamilies(fid)[0]
    # app.setFont(QFont(font))

    file = QFile(":/themes/lightstyle.qss")
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        file.close()
        app.setStyleSheet(stylesheet)
    
    def show_main_window():
        from osdag_gui.main_window import MainWindow
        app.main_window = MainWindow()
        app.main_window.show()

    splash = LaunchScreenPopup(on_finish=show_main_window)
    splash.show()
    sys.exit(app.exec())


# --- Main CLI group ---
help_msg = """\n\b
==================================================
Osdag Steel Design and Graphics Application

Usage:\n
  osdag                       # Launch GUI (default)\n
  osdag cli run               # Use CLI tools (see below)

By default, running 'osdag' launches the GUI.
You can also run in CLI mode using 'osdag cli run'.

Examples:\n
  osdag\n
  osdag cli run -i TensionBolted.osi\n
  osdag cli run -i TensionBolted.osi -op save_csv -o result.csv\n
  osdag cli run -i TensionBolted.osi -op save_pdf -o result.pdf\n
  osdag cli run -i TensionBolted.osi -op print_result\n
==================================================\n
"""

@click.group(invoke_without_command=True,
            help="\nOsdag Application. Run osdag to launch GUI, or use 'osdag cli run' for command-line tools.\n",
            epilog=help_msg,
            context_settings=dict(help_option_names=['-h', '--help']),
            )

@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        GUI()


# --- CLI group ---
@main.group(help="\nRun in CLI mode (use subcommands like 'run').\n",
            epilog=help_msg,
            context_settings=dict(help_option_names=['-h', '--help']),
            )
def cli():
    pass


# --- Subcommand: run ---
@cli.command(help="\nOsdag Application. Run osdag to launch GUI, or use 'osdag cli run' for command-line tools.\n",
            epilog=help_msg,
            context_settings=dict(help_option_names=['-h', '--help']),
            )
@click.option("-i", "--input", "input_path",
              type=click.Path(exists=True, dir_okay=False),
              required=True,
              help="Path to input file (.osi)")
@click.option("-op", "--op_type",
              type=click.Choice(["save_csv", "save_pdf", "print_result"]),
              default="print_result",
              show_default=True,
              help="Type of operation")
@click.option("-o", "--output", "output_path",
              type=click.Path(dir_okay=False, writable=True),
              help="Path for output file")
def run(input_path, op_type, output_path):
    result = run_module(input_path=input_path,
                        op_type=op_type,
                        output_path=output_path)

    if not result["success"]:
        click.echo("Errors encountered:")
        for err in result["errors"]:
            click.echo(f"   - {err}")
    else:
        click.echo("Operation completed successfully")
        if result.get("output"):
            click.echo(f"Output saved at: {result['output']}")


if __name__ == "__main__":
    main()
