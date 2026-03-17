"""
Settings Dialog
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QWidget, QRadioButton, QCheckBox, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont

from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
import osdag_gui.resources.resources_rc


def _section_header(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("SettingsSectionHeader")
    font = lbl.font()
    font.setBold(True)
    lbl.setFont(font)
    return lbl


class SettingsDialog(QDialog):
    def __init__(self, current_position="right", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.old_pos = current_position
        self.setObjectName("settings_dialog")

        app = QApplication.instance()
        self.theme = app.theme_manager

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(1, 1, 1, 1)
        mainLayout.setSpacing(0)

        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle("Settings")
        mainLayout.addWidget(self.titleBar)

        contentWidget = QWidget(self)
        contentWidget.setObjectName("ContentWidget")
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(20, 16, 20, 16)
        contentLayout.setSpacing(4)

        # ── Section: Window ───────────────────────────────────────────────────
        contentLayout.addWidget(_section_header("Control Button Position"))
        contentLayout.addSpacing(4)

        # Left radio — indented
        leftRow = QHBoxLayout()
        leftRow.setContentsMargins(24, 0, 0, 0)
        self.leftRadio = QRadioButton("Left side (macOS style)")
        self.leftRadio.setObjectName("LeftPositionRadio")
        leftRow.addWidget(self.leftRadio)
        leftRow.addStretch()
        contentLayout.addLayout(leftRow)

        # Right radio — indented
        rightRow = QHBoxLayout()
        rightRow.setContentsMargins(24, 0, 0, 0)
        self.rightRadio = QRadioButton("Right side (Windows style)")
        self.rightRadio.setObjectName("RightPositionRadio")
        rightRow.addWidget(self.rightRadio)
        rightRow.addStretch()
        contentLayout.addLayout(rightRow)

        if current_position == "left":
            self.leftRadio.setChecked(True)
        else:
            self.rightRadio.setChecked(True)

        # ── Section: Tabs ─────────────────────────────────────────────────────
        contentLayout.addSpacing(12)
        contentLayout.addWidget(_section_header("Window Closing Behavior"))
        contentLayout.addSpacing(4)

        # Checkbox — indented
        closeRow = QHBoxLayout()
        closeRow.setContentsMargins(24, 0, 0, 0)
        always_close = self.theme.get_always_close_all_tabs()
        self.chkAlwaysClose = QCheckBox("Always close all tabs without asking")
        self.chkAlwaysClose.setObjectName("AlwaysCloseAllTabsCheckbox")
        self.chkAlwaysClose.setChecked(always_close)
        closeRow.addWidget(self.chkAlwaysClose)
        closeRow.addStretch()
        contentLayout.addLayout(closeRow)

        # ── Buttons ───────────────────────────────────────────────────────────
        contentLayout.addSpacing(12)

        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(8)
        buttonLayout.addStretch()

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedHeight(32)
        self.cancelButton.setFixedWidth(80)
        self.cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.cancelButton)

        self.applyButton = QPushButton("Apply")
        self.applyButton.setFixedHeight(32)
        self.applyButton.setFixedWidth(80)
        self.applyButton.clicked.connect(self.accept)
        buttonLayout.addWidget(self.applyButton)

        contentLayout.addLayout(buttonLayout)
        mainLayout.addWidget(contentWidget)

    def accept(self):
        new_position = "left" if self.leftRadio.isChecked() else "right"
        self.theme.set_control_btn_pos(new_position)
        if self.old_pos != new_position:
            CustomMessageBox(
                title="Info",
                text="Changes to control button position will take effect after restarting Osdag.\n",
                dialogType=MessageBoxType.Information,
            ).exec()

        self.theme.set_always_close_all_tabs(self.chkAlwaysClose.isChecked())
        super().accept()