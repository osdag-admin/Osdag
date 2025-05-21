######################### UpDateNotifi ################
import urllib.request
import requests
import re
from PyQt5.QtWidgets import QMessageBox, QMainWindow
import sys

class Update():
    def __init__(self):
        self.old_version = self.get_current_version()
        # msg = self.notifi()

    def notifi(self):
        try:
            url = "https://raw.githubusercontent.com/osdag-admin/Osdag/master/src/osdag/_version.py"
            file = urllib.request.urlopen(url)
            version = 'not found'
            # Read the whole file content, as _version.py is small
            file_content = file.read().decode("utf-8")
            VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
            mo = re.search(VSRE, file_content, re.M)
            if mo:
                version = mo.group(1)
            
            # Compare versions properly
            # Convert version strings to tuples of integers and strings
            def parse_version(v):
                parts = []
                for part in v.split('.'):
                    try:
                        parts.append(int(part))
                    except ValueError:
                        parts.append(part)
                return parts
                
            current_version = parse_version(self.old_version)
            latest_version = parse_version(version)
            
            # Compare version parts
            if latest_version > current_version:
                msg = 'Current version: ' + self.old_version + '<br>' + 'Latest version ' + str(version) + '<br>' + \
                      'Update will be available <a href="https://osdag.fossee.in/resources/downloads"> here </a>'
            else:
                msg = 'Already up to date'
            return msg
        except Exception as e:
            return "No internet connection"

    def get_current_version(self):
        version_file = "_version.py"
        # Get the directory where this script is located
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        VERSIONFILE = os.path.join(script_dir, version_file)

        try:
            verstrline = open(VERSIONFILE, "rt").read()
        except EnvironmentError:
            return "Unknown"  # Return a default value when version file isn't found
        else:
            VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
            mo = re.search(VSRE, verstrline, re.M)
            if mo:
                verstr = mo.group(1)
                return verstr
            else:
                print("unable to find version in %s" % (VERSIONFILE,))
                raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))
