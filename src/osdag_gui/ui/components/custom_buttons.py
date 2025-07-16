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
        self.setCheckable(False) # We manage selection via stylesheet directly
        self._update_style() # Apply initial default style

    def _update_style(self):
        """Applies the appropriate stylesheet based on the selected state."""
        # Default style for unselected buttons
        default_style = """
            QPushButton {
                font-size: 14px;
                width: 140px;
                color: black;
                background-color: white;
                border: 2px solid white;
                border-radius: 5px;
                padding: 8px 4px;
                margin: 1px 2px;
            }
            QPushButton:hover {
                border: 2px solid #90AF13;
            }
            QPushButton:pressed {
                background-color: #90AF13;
                border: 2px solid #90AF13;
                color: white;
            }
        """
        # Style for selected buttons
        selected_style = """
            QPushButton {
                font-size: 14px;
                width: 140px;
                color: white;
                background-color: #90AF13;
                border: 2px solid #90AF13;
                border-radius: 5px;
                padding: 8px 4px;
                margin: 1px 2px;
            }
        """
        if self._is_selected:
            self.setStyleSheet(selected_style)
        else:
            self.setStyleSheet(default_style)

    def is_selected(self):
        """Returns True if the button is currently selected, False otherwise."""
        return self._is_selected

    def set_selected(self, selected):
        """Sets the selected state of the button and updates its style."""
        if self._is_selected != selected: # Only update if state changes
            self._is_selected = selected
            self._update_style()

class CustomButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #90AF13;
                border-radius: 5px;
                padding: 10px;
                text-align: center;
            }
            QPushButton:pressed {
                background-color: #7d9710;
            }
            QLabel {
                background: transparent;
                color: white;
            }
            QSvgWidget{
                background: transparent;
            }
        """)

        # Layout for icons and text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)

        # Left icon (extract from design_button.svg or use a similar SVG)
        left_icon = QSvgWidget()
        left_icon.load(':/vectors/design.svg')
        left_icon.setFixedSize(18, 18)
        layout.addWidget(left_icon)

        # Center text
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Right icon (use a down arrow SVG or PNG)
        right_icon = QSvgWidget()
        right_icon.load(':/vectors/arrow_down.svg')
        right_icon.setFixedSize(18, 18)
        layout.addWidget(right_icon)

        layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(layout)
        
        # Calculate minimum width to prevent overlap
        text_width = text_label.sizeHint().width()
        icon_width = 18 + 18  # Left and right icon widths
        margins = layout.contentsMargins().left() + layout.contentsMargins().right()  # 10 + 10
        padding = 20  # 10px padding on each side from stylesheet
        min_width = text_width + icon_width + margins + padding
        self.setMinimumWidth(min_width)
