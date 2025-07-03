import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QFont, QCursor, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QSize, QEvent, Signal
from PySide6.QtSvgWidgets import QSvgWidget

import osdag_gui.resources.resources_rc

class CustomButton1(QPushButton):
    def __init__(self, text, icon_path_default, icon_path_clicked, group=None, parent=None):
        super().__init__(text, parent)
        self.group = group
        self.is_clicked = False
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)

        self.default_icon = QIcon(icon_path_default)
        self.clicked_icon = QIcon(icon_path_clicked)
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(20, 20)) # Initial size, will be updated
        self.set_default_style()

    def mousePressEvent(self, event):
        if self.group:
            for btn in self.group:
                btn.set_default_style()
                btn.setIcon(btn.default_icon)
                btn.is_clicked = False
        self.set_active_style()
        self.setIcon(self.clicked_icon)
        self.is_clicked = True
        print(self.text().strip(), "clicked")
        super().mousePressEvent(event)

    def set_font_size(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    def set_default_style(self):
        # Base style for default state
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                padding: 4px 4px 8px 8px;
                font-family: "Calibri";
                border-top: 1px solid #ffffff;
                border-bottom: 1px solid #ffffff;
                text-align: left;
            }
            QPushButton:hover {
                background-color: transparent;
                color: #90AF13;
                border-top: 1px solid #90AF13;
                border-bottom: 1px solid #90AF13;
            }
        """)

    def set_active_style(self):
        # Base style for active state
        self.setStyleSheet("""
            QPushButton {
                background-color: #90AF13;
                color: #ffffff;
                padding: 4px 4px 8px 8px;
                font-family: "Calibri";
                border-top: 1px solid #90AF13;
                border-bottom: 1px solid #90AF13;
                text-align: left;
            }
        """)

class VerticalMenuBar(QWidget):
    nav_bar_trigger = Signal(object, object)
    def __init__(self, data: dict):
        super().__init__()

        # Set size policy to expanding so it grows/shrinks with its parent layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(2, 5, 2, 0)
        self.main_layout.setSpacing(0)
        

        # Header section
        self.header = QFrame()
        self.header.setStyleSheet("background-color: #ffffff;")
        self.header_layout = QVBoxLayout(self.header)
        self.header_layout.setSpacing(5)
        self.header_layout.setAlignment(Qt.AlignCenter) # Center logo in header

        self.osdag_logo = QSvgWidget(":/vectors/Osdag_logo.svg", parent=self)
        # Remove fixed size here, will be set dynamically in resizeEvent
        self.header_layout.addWidget(self.osdag_logo, alignment=Qt.AlignCenter)
        
        self.main_layout.addWidget(self.header)

        # Add a spacer to push content down if header is small
        self.main_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons section
        self.button_group = []
        # Get paths relative to the script's directory
        icon_default = ":/images/default_icon.png"
        icon_clicked = ":/images/clicked_icon.png"

        names = list(data.keys())
        for name in names:
            btn = CustomButton1("  " + name, icon_default, icon_clicked, group=self.button_group)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Make buttons expand vertically
            btn.clicked.connect(lambda _,label=name, data=data.get(name): self._on_nav_button_clicked(data, label))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.button_group.append(btn)
            self.main_layout.addWidget(btn)

        # Set initial active button
        if self.button_group:
            self.button_group[0].set_active_style()
            self.button_group[0].setIcon(self.button_group[0].clicked_icon)
            self.button_group[0].is_clicked = True
        
        # Add a spacer to push content up if buttons are small
        self.main_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Bottom section
        self.bottom_frame = QFrame()
        self.bottom_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setSpacing(5)

        self.iitb_logo = QSvgWidget(":/vectors/IITB_logo.svg", parent=self)
        # Remove fixed size here, will be set dynamically in resizeEvent
        self.bottom_layout.addWidget(self.iitb_logo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.version_label = QLabel("v2025.01.a.2")
        self.version_label.setFont(QFont("Calibri", 12)) # Initial font, will be updated
        self.version_label.setStyleSheet("""
            QLabel {
                color: gray;
            }
        """)
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottom_layout.addWidget(self.version_label)

        self.main_layout.addWidget(self.bottom_frame)

        # Initial update of sizes and fonts
        self.update_responsive_elements()

    def _on_nav_button_clicked(self, data, name):
        """
        Internal slot to handle button clicks and emit the custom signal.
        """
        self.nav_bar_trigger.emit(data, name)

    def update_responsive_elements(self):
        """Updates font sizes and SVG sizes based on current widget dimensions."""
        widget_height = self.height()
        widget_width = self.width()

        if widget_height <= 0 or widget_width <= 0:
            return # Avoid division by zero or invalid sizes

        # --- Responsive Font Sizes ---
        # Calculate a base font size relative to the widget's height or width
        # You can adjust the divisor (e.g., 40, 50) to make fonts larger/smaller
        # Adding a minimum font size to prevent them from becoming too tiny
        base_font_size = max(8, int(widget_height / 45)) 
        button_font_size = max(10, int(widget_height / 55)) # Buttons can be slightly smaller
        version_font_size = max(6, int(widget_height / 100)) # Version label can be smaller

        for btn in self.button_group:
            btn.set_font_size(button_font_size)
            # Adjust icon size based on button font size or a direct proportion
            icon_size = max(16, int(button_font_size * 1.5))
            btn.setIconSize(QSize(icon_size, icon_size))
            
            # Reapply style to ensure font update takes effect if style sheets override it
            if btn.is_clicked:
                btn.set_active_style()
            else:
                btn.set_default_style()


        font_version = QFont("Calibri", version_font_size)
        self.version_label.setFont(font_version)
        self.version_label.setStyleSheet(f"""
            QLabel {{
                color: gray;
                font-size: {version_font_size}pt; /* Apply font size directly via stylesheet for consistency */
            }}
        """)

        # --- Responsive SVG Sizes ---
        # Calculate SVG size based on a percentage of the sidebar's width or height
        # Using min(width, height) to maintain a square aspect ratio for logos
        # Adjust the divisor (e.g., 3, 4) to make logos larger/smaller
        logo_size = max(40, int(min(widget_width, widget_height) / 3))

        self.osdag_logo.setFixedSize(logo_size, logo_size)
        self.iitb_logo.setFixedSize(logo_size, logo_size)

        # Set header's fixed height based on the logo size + some padding
        # This ensures the header height also scales with the logo
        self.header.setFixedHeight(logo_size + 10) # 10 pixels for padding top/bottom


    def resizeEvent(self, event: QEvent):
        """Called when the widget is resized."""
        super().resizeEvent(event)
        self.update_responsive_elements() # Recalculate and apply sizes

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("white"))
        painter.drawRect(self.rect())
        super().paintEvent(event)
