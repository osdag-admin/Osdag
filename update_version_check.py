######################### UpDateNotifi ################
import urllib.request
import requests
import re
from PyQt5.QtWidgets import QMessageBox,QMainWindow
import sys

class Update():
    def __init__(self):
        super().__init__()
        self.old_version=self.get_current_version()
        # msg = self.notifi()

    def notifi(self):
        try:
            url = "https://raw.githubusercontent.com/osdag-admin/Osdag/master/README.md"
            file = urllib.request.urlopen(url)
            version = 'not found'
            for line in file:
                decoded_line = line.decode("utf-8")
                match = re.search(r'Download the latest release version (\S+)', decoded_line)
                if match:
                    version = match.group(1)
                    version = version.split("<")[0]
                    break
            # decoded_line = line.decode("utf-8")
            # new_version = decoded_line.split("=")[1]
            if version != self.old_version:
                msg = 'Current version: '+ self.old_version+'<br>'+'Latest version '+ str(version)+'<br>'+\
                      'Update will be available <a href=\"https://osdag.fossee.in/resources/downloads\"> here <a/>'
            else:
                msg = 'Already up to date'
            return msg
        except:
            return "No internet connection"

    def get_current_version(self):
        version_file = "_version.py"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        VERSIONFILE = rel_path +'/'+ version_file

        try:
            verstrline = open(VERSIONFILE, "rt").read()
        except EnvironmentError:
            pass  # Okay, there is no version file.
        else:
            VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
            mo = re.search(VSRE, verstrline, re.M)
            if mo:
                verstr = mo.group(1)
                return verstr
            else:
                print("unable to find version in %s" % (VERSIONFILE,))
                raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))
