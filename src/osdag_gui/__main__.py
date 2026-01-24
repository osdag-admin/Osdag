"""
Entry point for Osdag GUI application.
Handles splash screen and main window launch.

Startup sequence:
1. OS/environment setup (GPU detection, Qt configuration)
2. Safety initialization (multiprocessing spawn, OCC guards)  
3. GUI launch
"""

# =============================================================================
# CRITICAL: Import and run safety protocols BEFORE any PySide6/Qt imports
# =============================================================================
from osdag_gui.OS_safety_protocols import setup_environment, ensure_safe_startup

setup_environment()
ensure_safe_startup()

# =============================================================================
# Now safe to import Qt and other modules
# =============================================================================
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal, QFile, QTextStream
from PySide6.QtGui import QFontDatabase, QFont, QIcon

# Disable native file dialogs globally to prevent OpenGL context conflicts
# This is critical for Linux systems with Intel/Mesa graphics drivers
QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
from osdag_core.utils.internet_connectivity import InternetConnectivity
from osdag_gui.ui.windows.launch_screen import OsdagLaunchScreen
from osdag_gui.data.database.database_config import refactor_database, create_user_database
from osdag_gui.ui.utils.theme_manager import ThemeManager
from osdag_core.cli import run_module
import osdag_gui.resources.resources_rc
import sys, click, os
from pathlib import Path


# Uncomment below to enable print tracing for debugging
# =========================================================
# import builtins
# import inspect

# _original_print = builtins.print

# def traced_print(*args, **kwargs):
#     frame = inspect.stack()[1]
#     filename = frame.filename
#     line = frame.lineno
#     _original_print(f"[{filename}:{line}]", *args, **kwargs)

# builtins.print = traced_print
# =========================================================a


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
        import sqlite3
        import subprocess
        from importlib.resources import files
        import shutil
        
        try:
            # Get paths
            sqlpath = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sql')
            sqlitepath = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sqlite')

            if not sqlpath.exists():
                print(f"[ERROR] SQL file not found: {sqlpath}")
                return

            # Determine if we need to create or update
            needs_creation = not sqlitepath.exists()
            needs_update = (sqlitepath.exists() and 
                        (sqlitepath.stat().st_size == 0 or 
                            sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1))

            if not needs_creation and not needs_update:
                # print("[INFO] Database is up to date")
                return

            # Create backup if updating existing database
            backup_path = None
            if needs_update:
                backup_path = sqlitepath.with_suffix('.sqlite.backup')
                shutil.copy2(sqlitepath, backup_path)

            # Create/update database
            target_path = sqlitepath
            if needs_update:
                # Create in temp location first
                target_path = sqlitepath.parent / 'Intg_osdag_temp.sqlite'

            # Try Python sqlite3 first
            try:
                with open(sqlpath, 'r', encoding='utf-8') as sql_file:
                    sql_content = sql_file.read()
                
                conn = sqlite3.connect(target_path)
                conn.executescript(sql_content)
                conn.close()
                
                print(f"[INFO] Database {'created' if needs_creation else 'updated'} using Python sqlite3")
                
            except Exception as e:
                print(f"[ERROR] Python sqlite3 failed: {e}, trying command line")
                
                # Fallback to command line
                result = subprocess.run([
                    'sqlite3', str(target_path), 
                    f'.read {sqlpath}'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    raise Exception(f"[ERROR] Command line sqlite3 failed: {result.stderr}")
                
                print(f"[INFO] Database {'created' if needs_creation else 'updated'} using command line")

            # If updating, replace the original
            if needs_update:
                sqlitepath.unlink()
                target_path.rename(sqlitepath)
                if backup_path and backup_path.exists():
                    backup_path.unlink()

            # Touch the SQL file to update timestamp
            sqlpath.touch()

        except Exception as e:
            print(f"[ERROR] Database setup failed: {e}")
            
            # Cleanup on failure
            if needs_update:
                # Restore backup if available
                if backup_path and backup_path.exists():
                    if not sqlitepath.exists():
                        shutil.copy2(backup_path, sqlitepath)
                    backup_path.unlink()
                
                # Remove temp file
                temp_path = sqlitepath.parent / 'Intg_osdag_temp.sqlite'
                if temp_path.exists():
                    temp_path.unlink()

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

def show_crash_dialog(reason, excecption, logfile):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Osdag Error")

    if reason == "PYTHON EXCEPTION":
        text = "Osdag encountered an internal error"
    elif "FREEZE" in reason:
        text = "Not responding. Osdag has detected a freeze."
    else:
        text = "Osdag crashed due to a system error."

    msg.setText(text)
    msg.setInformativeText(f"A crash report was saved to:\n{logfile}")
    msg.exec()
    QApplication.quit()


def GUI():
    from osdag_gui.error_handler import CrashLogger, TerminalLogger

    # set app directory
    user_docs = os.path.join(Path.home(), "Documents")
    app_dir = os.path.join(user_docs, "Osdag")
    os.makedirs(app_dir, exist_ok=True)
    os.chdir(app_dir)

    # Start crash logger
    log_dir = os.path.join(app_dir, "data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    TerminalLogger = TerminalLogger(log_dir=log_dir)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # Load bundled Ubuntu Sans font - works on all OS without needing font installed
    fid = QFontDatabase.addApplicationFont(":/fonts/UbuntuSans-Regular.ttf")
    if fid != -1:
        font_family = QFontDatabase.applicationFontFamilies(fid)[0]
        app.setFont(QFont(font_family, 10))  # Set as default app font
    else:
        print("[WARNING] Failed to load Ubuntu Sans font from resources")

    app.theme_manager = ThemeManager(app)
    app.theme_manager.load_theme(app.theme_manager.current_theme)

    if app.theme_manager.is_light():
        file = QFile(":/themes/lightstyle.qss")
    else:
        file = QFile(":/themes/darkstyle.qss")

    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        stylesheet = stream.readAll()
        file.close()
        app.setStyleSheet(stylesheet)
    
    def show_main_window():
        from osdag_gui.main_window import MainWindow
        app.internet_connectivity = InternetConnectivity() # --- Internet Connectivity object ---
        # Parallely load the MainWindow
        app.main_window = MainWindow()
        app.main_window.show()
        app.setWindowIcon(QIcon(":/images/osdag_logo.png"))

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
  osdag-cli run -i TensionBolted.osi\n
  osdag-cli run -i TensionBolted.osi -t save_csv -o result.csv\n
  osdag-cli run -i TensionBolted.osi -t generate_report -o result.pdf\n
  osdag-cli run -i TensionBolted.osi -t print_result\n
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
@click.option("-t", "--op_type", "op_type",
              type=click.Choice(["save_csv", "generate_report", "print_result"]),
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
