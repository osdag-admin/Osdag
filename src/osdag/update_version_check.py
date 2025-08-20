######################### UpDateNotifi ################

import urllib.request
import re
from pathlib import Path
from packaging.version import Version, InvalidVersion
from PyQt5.QtCore import QObject, QProcess, pyqtSignal
import subprocess


version_file = Path(__file__).parent / "_version.py"
version_var = {}
exec(version_file.read_text(), version_var)
curr_version = version_var["__version__"]
install_type = version_var["__installation_type__"]
class Update(QObject):

    URL = "https://osdag.fossee.in/resources/downloads"
    PATTERN = re.compile(r'Install\s+Osdag\s*\(\s*v([\w._-]+)\s*\)', re.IGNORECASE)

    def __init__(self):
        super().__init__()
        self.old_version = curr_version
        self.process = None

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
            if install_type == "conda":
                cmd = ["conda", "update", "-y", f"osdag"]
                # cmd = ["cmd", "/c", f"echo Updating to version {latest_version} with conda && timeout /t 5"]
            elif install_type == "pixi":
                cmd = ["pixi", "update", "-y", f"osdag"]

            result = subprocess.run(cmd, capture_output=False, text=True)
            if result.returncode == 0:
                return (True, "Update successful! Please restart Osdag.")
            else:
                return (False, f"Update failed.\nError: {result.stderr}\n"
                               "Please retry or run:\nconda install --force-reinstall osdag::osdag")
                
        
        except Exception as e:
            return (False, f"Update failed: {e}")

        