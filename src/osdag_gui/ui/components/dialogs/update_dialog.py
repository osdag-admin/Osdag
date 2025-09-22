from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QTextBrowser, QSizePolicy, QProgressBar
)
from PySide6.QtCore import QProcess, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QIcon
from packaging.version import Version, InvalidVersion
from pathlib import Path
import sys, shutil, json

from osdag_gui.__config__ import INSTALLATION_TYPE, VERSION
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar

class UpdateDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.old_version = Version(VERSION)
        self.process = QProcess(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("UpdateDialog")
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.setFixedSize(580, 450)

        # Layout and style
        self.setStyleSheet("""
            QDialog#UpdateDialog { background-color: #ffffff; border: 1px solid #90AF13; }
            QWidget#ContentWidget { background-color: #ffffff; }
            QTextBrowser { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 4px;
                           font-family: 'Arial'; font-size: 8pt; padding: 8px; }
            QProgressBar { border: 1px solid #ccc; border-radius: 5px; text-align: center; height: 20px; }
            QProgressBar::chunk { background-color: #90AF13; }
            QPushButton { background-color: #90AF13; color: white; border: none; border-radius: 5px;
                          padding: 5px 20px; font-size: 12px; font-weight: bold; }
            QPushButton:hover { background-color: #7A9611; }
            QPushButton:pressed { background-color: #6B850F; }
        """)

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        # Title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("Check for Updates")
        mainLayout.addWidget(self.titleBar)

        # Content
        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        contentLayout.setSpacing(10)

        self.logoLabel = QSvgWidget(":/vectors/Osdag.svg", self)
        self.logoLabel.setFixedHeight(106)
        self.logoLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        contentLayout.addWidget(self.logoLabel, 0, Qt.AlignCenter)

        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textBrowser.setStyleSheet(
            "font-size: 12pt;"
            )
        contentLayout.addWidget(self.textBrowser)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 0) 
        contentLayout.addWidget(self.progressBar)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        self.okButton = QPushButton("OK", self)
        self.okButton.setFixedHeight(30)
        self.okButton.setStyleSheet("""
            QPushButton { background-color: #90AF13; color: white; border: none; border-radius: 5px;
                           padding: 5px 20px; font-size: 12px; font-weight: bold; }
            QPushButton:hover { background-color: #7A9611; }
            QPushButton:pressed { background-color: #6B850F; }
        """)
        self.okButton.clicked.connect(self.accept)
        buttonLayout.addWidget(self.okButton)

        # Update buttons (hidden initially)
        self.updateNowButton = QPushButton("Update Now", self)
        self.updateLaterButton = QPushButton("Update Later", self)
        self.updateNowButton.setFixedHeight(30)
        self.updateLaterButton.setFixedHeight(30)
        self.updateNowButton.clicked.connect(self.update_to_latest)
        self.updateLaterButton.clicked.connect(self.close)
        self.updateNowButton.hide()
        self.updateLaterButton.hide()
        buttonLayout.addWidget(self.updateNowButton)
        buttonLayout.addWidget(self.updateLaterButton)

        contentLayout.addLayout(buttonLayout)
        mainLayout.addWidget(contentWidget)

        # Start checking for updates immediately
        self.textBrowser.setHtml("<p style='color:blue;'>Checking for updates...</p>")
        self._set_exec_paths()
        self.check_for_updates()

    def _set_exec_paths(self):
        env_path = Path(sys.prefix)
        base_conda_path = env_path.parents[1]
        if sys.platform.startswith("win"):
            self.conda_path = base_conda_path / "Scripts" / "conda.exe"
            self.pixi_path = env_path / "Scripts" / "pixi.exe"
        else:
            self.conda_path = base_conda_path / "bin/conda"
            self.pixi_path = env_path / "bin/pixi"

        self.conda_path = str(self.conda_path if self.conda_path.exists() else shutil.which("conda"))
        self.pixi_path = str(self.pixi_path if self.pixi_path.exists() else shutil.which("pixi"))

    def check_for_updates(self):
        """Run QProcess to fetch version asynchronously."""
        if INSTALLATION_TYPE == "conda":
            cmd = [self.conda_path, "search", "-c", "conda-forge", "osdag::osdag", "--info", "--json"]
        elif INSTALLATION_TYPE == "pixi":
            cmd = [self.pixi_path, "search", "osdag", "--channel", "osdag"]
        else:
            self.update_text("<p style='color:red;'>Unknown installation type.</p>")
            return

        self.process.readyReadStandardOutput.connect(self.on_output)
        self.process.readyReadStandardError.connect(self.on_error)
        self.process.finished.connect(self.on_finished)
        self.process.start(cmd[0], cmd[1:])

    def update_to_latest(self):
        try:
            if INSTALLATION_TYPE == "conda":
                if not Path(self.conda_path).exists():
                    self.update_text(f"<p style='color:red;'>conda not found at {self.conda_path}</p>")
                    return
                cmd = [self.conda_path, "update", "-y", "osdag", "--channel", "osdag"]
            elif INSTALLATION_TYPE == "pixi":
                if not Path(self.pixi_path).exists():
                    self.update_text(f"<p style='color:red;'>pixi not found at {self.pixi_path}</p>")
                    return
                cmd = [self.pixi_path, "update", "-y", "osdag", "--channel", "osdag"]
            else:
                self.update_text("<p style='color:red;'>Unknown installation type.</p>")
                return
            
            # Show progress bar again
            self.progressBar.show()
            self.progressBar.setRange(0, 0) 
            self.updateNowButton.hide()
            self.updateLaterButton.hide()

            # Configure process
            self.process = QProcess(self)
            self.process.setProgram(cmd[0])
            self.process.setArguments(cmd[1:])
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.finished.connect(self.handle_update_finished)

            # Start update
            self.update_text("<p style='color:blue;'>Updating Osdag to the latest version...</p>")
            self.process.start()
            
        except Exception as e:
            self.update_text(f"<p style='color:red;'>Update failed: {e}</p>")

    def on_output(self):
        self.output_data = self.process.readAllStandardOutput().data().decode()

    def on_error(self):
        self.error_data = self.process.readAllStandardError().data().decode()

    def on_finished(self):
        self.progressBar.hide()
        latest_version = None

        try:
            if INSTALLATION_TYPE == "conda":
                data = json.loads(self.output_data)
                versions = data.get("osdag", [])
                if versions:
                    latest_version = sorted(versions, key=lambda x: x["version"])[-1]["version"]
            elif INSTALLATION_TYPE == "pixi":
                for line in self.output_data.splitlines():
                    if line.strip().startswith("Version"):
                        latest_version = line.split()[-1].strip()

            if latest_version:
                lv = Version(latest_version)
                if lv > self.old_version:
                    self.update_text(
                        f"<p style='color:green;'>A new version of Osdag is available: "
                        f"<b>{lv}</b> (You have {self.old_version}).<br>"
                        f"Visit <a href='https://osdag.fossee.in/resources/downloads'>downloads</a>.</p>"
                    )
                    self.okButton.hide()
                    self.updateNowButton.show()
                    self.updateLaterButton.show()
                else:
                    self.update_text(
                        f"<p style='color:blue;'>You are using the latest version of Osdag "
                        f"(<b>{self.old_version}</b>).</p>"
                    )
            else:
                self.update_text("<p style='color:orange;'>Could not fetch version information.</p>")

        except Exception as e:
            self.update_text(f"<p style='color:red;'>Error checking for updates: {e}</p>")

    def update_text(self, html: str):
        self.textBrowser.setHtml(f"<p style='font-family:Arial; font-size:9pt;'>{html}</p>")


    def handle_stdout(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.update_text(f"<pre style='font-size:9pt;'>{output}</pre>")

    def handle_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        self.update_text(f"<pre style='color:red; font-size:9pt;'>{error}</pre>")

    def handle_update_finished(self):
        self.progressBar.hide()
        self.okButton.show()
        exit_code = self.process.exitCode()
        if exit_code == 0:
            self.update_text("<p style='color:green;'>Update completed successfully!</p>")
        else:
            self.update_text(f"<p style='color:red;'>Update failed with exit code {exit_code}.</p>")