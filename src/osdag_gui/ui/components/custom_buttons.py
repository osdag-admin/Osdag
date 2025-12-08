"""
Custom button widgets for Osdag GUI.
Includes menu and action buttons with custom styles.
"""
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout,
    QLabel, QMainWindow, QSizePolicy, QFrame
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QRect, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QPainter

class MenuButton(QPushButton):
    """Base class for menu buttons to manage selected/unselected styles."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._is_selected = False
        self.setCheckable(False)  # We manage selection via stylesheet directly
        self._update_style()  # Apply initial default style
        self.setObjectName("menu_button")

    def _update_style(self):
        """Applies the appropriate stylesheet based on the selected state."""
        if self._is_selected:
            self.setProperty("selected", "true")
        else:
            self.setProperty("selected", "false")
        
        # Force style refresh
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def is_selected(self):
        """Returns True if the button is currently selected, False otherwise."""
        return self._is_selected

    def set_selected(self, selected):
        """Sets the selected state of the button and updates its style."""
        if self._is_selected != selected:  # Only update if state changes
            self._is_selected = selected
            self._update_style()


class DockCustomButton(QPushButton):
    def __init__(self, text: str, icon_path: str, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("dock_custom_button")

        # Layout for icons and text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)

        # Left icon
        left_icon = QSvgWidget()
        left_icon.load(icon_path)
        left_icon.setFixedSize(18, 18)
        left_icon.setObjectName("button_icon")
        layout.addWidget(left_icon)

        # Center text
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setObjectName("button_label")
        layout.addWidget(text_label)

        layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(layout)
        
        # Calculate minimum width to prevent overlap
        text_width = text_label.sizeHint().width()
        icon_width = 18
        margins = layout.contentsMargins().left() + layout.contentsMargins().right()
        padding = 20
        min_width = text_width + icon_width + margins + padding
        self.setMinimumWidth(min_width)