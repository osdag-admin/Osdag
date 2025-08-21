######################### UpDateNotifi ################

import urllib.request
import re
from pathlib import Path
from packaging.version import Version, InvalidVersion
from PyQt5.QtCore import QObject, QProcess, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTextEdit, QLabel
import subprocess
import sys, os


version_file = Path(__file__).parent / "_version.py"
version_var = {}
exec(version_file.read_text(), version_var)
curr_version = version_var["__version__"]
install_type = version_var["__installation_type__"]
class Update(QObject):
    output_signal = pyqtSignal(str)   
    finished_signal = pyqtSignal(bool, str) 


    URL = "https://osdag.fossee.in/resources/downloads"
    PATTERN = re.compile(r'Install\s+Osdag\s*\(\s*v([\w._-]+)\s*\)', re.IGNORECASE)

    def __init__(self):
        super().__init__()
        self.old_version = curr_version
        self.process = QProcess(self)

    def fetch_latest_version(self) -> str:
        """Fetch the latest version string from Osdag downloads page."""
        try:
            with urllib.request.urlopen(self.URL) as response:
                for line in response:
                    decoded_line = line.decode("utf-8")
                    match = self.PATTERN.search(decoded_line)
                    if match:
                        return match.group(1)
            return None
        except urllib.error.URLError as e:
            raise ConnectionError(f"Network error: {e.reason}")
        except urllib.error.HTTPError as e:
            raise ConnectionError(f"HTTP error {e.code}: {e.reason}")

    def notifi(self) -> str:
        """Compare current version with latest version and return update message."""
        try:
            latest_version = self.fetch_latest_version()
            if latest_version is None:
                return False, "Could not determine latest version."

            latest_version = latest_version.lstrip("v").replace("_", ".")
            if Version(latest_version) > Version(self.old_version):
                return True, (
                    f"Current version: {self.old_version}\n"
                    f"Latest version: {latest_version}\n"
                )
            else:
                return False, "Already up to date"
            
        except InvalidVersion:
            return False, "Could not parse version string."
        
    def update_to_latest(self):
        """Run conda update in background using QProcess."""
        try:
            latest_version = self.fetch_latest_version()
            if latest_version:
                latest_version = latest_version.lstrip("v").replace("_", ".")
        except Exception as e:
            return
        try:
            # cmd = ["conda", "install", "-y", f"osdag=={latest_version}"]
            
            env_path = sys.prefix  
            env_path = Path(env_path)
            base_conda_path = env_path.parents[1]
            if sys.platform.startswith("win"):
                conda_path = base_conda_path / "Scripts" / "conda.exe"
                pixi_path = env_path / "Scripts" / "pixi.exe"
                print(conda_path, pixi_path)
            else:
                conda_path = base_conda_path / "bin/conda"
                pixi_path = env_path / "bin/pixi"
            if install_type == "conda":
                if not conda_path.exists():
                    self.finished_signal.emit(False, f"conda not found at {conda_path}")
                    return 
                cmd = [str(conda_path), "update", "-y", "osdag"]
                # cmd = ["cmd", "/c", f"echo Updating to version {latest_version} with conda && timeout /t 5"]
            elif install_type == "pixi":
                if not pixi_path.exists():
                    self.finished_signal.emit(False, f"pixi.exe not found in {pixi_path}")
                    return 
                cmd = [str(pixi_path), "update", "-y", "osdag"]

            # Create QProcess
            self.process.setProgram(cmd[0]) 
            self.process.setArguments(cmd[1:])

            # Connect signals for output
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.finished.connect(self.handle_finished)

            # Start the process
            self.process.start()

            # result = subprocess.run(cmd, capture_output=False, text=True)
            # if result.returncode == 0:
            #     self.finished_signal.emit(True, "Update successful! Please restart Osdag.")
            # else:
            #     self.finished_signal.emit(False, f"Update failed.\nError: {result.stderr}\n"
            #                    "Please retry or run:\nconda install --force-reinstall osdag::osdag")
                
        
        except Exception as e:
            self.finished_signal.emit(False, f"Update failed: {e}")
            return

    
    def handle_stdout(self):
        """Read stdout and print it, also emit signal for GUI."""
        if self.process:
            output = self.process.readAllStandardOutput().data().decode("utf-8")
            self.output_signal.emit(output)
            print(output, end="")  
            # self.progress_text.append(output)  
            # self.progress_text.verticalScrollBar().setValue(
            #     self.progress_text.verticalScrollBar().maximum()
            # )

    def handle_stderr(self):
        """Read stderr and print it."""
        if self.process:
            error = self.process.readAllStandardError().data().decode("utf-8")
            self.output_signal.emit(error)
            print(error, end="")
            # self.output_signal.emit(error)
            # self.progress_text.append(error)  
            # self.progress_text.verticalScrollBar().setValue(
            #     self.progress_text.verticalScrollBar().maximum()
            # )

    def handle_finished(self, exit_code, exit_status):
        """Handle when the process finishes."""
        if exit_code == 0:
            self.finished_signal.emit(True, "Update successful! Please restart Osdag.")
        else:
            self.finished_signal.emit(False, f"Update failed with code {exit_code}")
        self.process = None

    