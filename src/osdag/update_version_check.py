######################### UpDateNotifi ################

import urllib.request
import re
from pathlib import Path

version_file = Path(__file__).parent / "_version.py"
ns = {}
exec(version_file.read_text(), ns)
curr_version = ns["__version__"]

class Update():
    URL = "https://osdag.fossee.in/resources/downloads"
    PATTERN = re.compile(r'Install Osdag \((v[0-9a-zA-Z_]+)\)')

    def __init__(self):
        super().__init__()
        self.old_version = curr_version

    def fetch_latest_version(self) -> str:
        """Fetch the latest version string from Osdag downloads page."""
        try:
            with urllib.request.urlopen(self.URL) as response:
                for line in response:
                    decoded_line = line.decode("utf-8")
                    match = self.PATTERN.search(decoded_line)
                    if match:
                        return match.group(1)
            return "not found"
        except Exception as e:
            raise ConnectionError(f"Error fetching latest version: {e}")

    def notifi(self) -> str:
        """Compare current version with latest version and return update message."""
        try:
            latest_version = self.fetch_latest_version().lstrip("v").replace("_", ".")
            if latest_version == "not found":
                return "Could not determine latest version."

            if latest_version != self.old_version:
                return (
                    f"Current version: {self.old_version}<br>"
                    f"Latest version: {latest_version}<br>"
                )

            return "Already up to date"

        except Exception as e:
            return str(e)


