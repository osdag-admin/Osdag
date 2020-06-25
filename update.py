from PyQt5.QtWidgets import QMessageBox, QMainWindow
import urllib.request
class Update():
    def __init__(self, old_version):
        self.old_version=old_version

    def notifi(self):
        try:
            url = "https://anshulsingh-py.github.io/test/version.txt"
            file = urllib.request.urlopen(url)
            for line in file:
                decoded_line = line.decode("utf-8")
            new_version = decoded_line.split("=")[1]
            return int(new_version) > self.old_version

        except:
            return "no internet"
