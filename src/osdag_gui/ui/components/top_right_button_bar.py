import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QMenu, QLabel, QPushButton, QButtonGroup
)
from PySide6.QtCore import Qt, QSize, QPoint, QPropertyAnimation, QEasingCurve, QTimer, Signal
from PySide6.QtGui import QIcon, QAction

# Define colors used in the UI
OSDAG_GREEN = "#90AF13"
OSDAG_GREEN_DARK = "#8AB23A"
BORDER_COLOR = "#000000"

class TopButton(QPushButton):
    """
    Custom QPushButton that changes style on hover and provides a momentary
    color change on click, instead of a persistent selected state.
    """
    def __init__(self, black_icon_path, white_icon_path, label, parent=None):
        super().__init__(parent)
        self.black_icon_path = black_icon_path
        self.white_icon_path = white_icon_path
        self.label_text = label
        
        # Internal flag to track if the mouse is currently hovering over the button
        self.is_hovering = False
        
        # Timer for reverting the style after a click
        self.click_animation_timer = QTimer(self)
        self.click_animation_timer.setSingleShot(True)
        self.click_animation_timer.timeout.connect(self._reset_style_after_click)
        
        # Set up initial button properties
        self.setMinimumSize(40, 40) # Initial collapsed size
        self.setMaximumHeight(40)
        self.setIconSize(QSize(20, 20))
        
        # Initialize width animation for smooth expansion/collapse
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200) # milliseconds
        self.animation.setEasingCurve(QEasingCurve.OutCubic) # Smooth transition

        self.animation_max_width = QPropertyAnimation(self, b"maximumWidth")
        self.animation_max_width.setDuration(200)
        self.animation_max_width.setEasingCurve(QEasingCurve.OutCubic)

        # Start with the default black icon and no text
        self.setIcon(QIcon(self.black_icon_path))
        self.setText("")
        # Apply the default style sheet initially
        self.setStyleSheet(self.default_style_sheet())
        self.setCursor(Qt.PointingHandCursor) # Indicate clickable element
        
        # Enable hover tracking for enterEvent and leaveEvent
        self.setAttribute(Qt.WA_Hover, True)

    def default_style_sheet(self):
        """
        Returns the CSS for the button's default (unhovered, unclicked) state.
        White background, black text/icon, standard border.
        """
        return f"""
            QPushButton {{
                background: #fff;
                border: 1px solid {BORDER_COLOR};
                color: #000;
                font-size: 1px; /* Text size is effectively 0 when collapsed */
                padding: 10px;
                text-align: center;
            }}
        """

    def hover_style_sheet(self):
        """
        Returns the CSS for the button's hover state.
        Green background, white text/icon, slightly darker green border, larger font.
        """
        return f"""
            QPushButton {{
                background: {OSDAG_GREEN};
                border: 1px solid {OSDAG_GREEN_DARK};
                color: #fff;
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
                text-align: center;
            }}
        """

    def pressed_style_sheet(self):
        """
        Returns the CSS for the button's momentarily pressed state.
        A darker shade of green for the background and border to indicate click.
        """
        return f"""
            QPushButton {{
                background: {OSDAG_GREEN_DARK}; /* Darker green on press */
                border: 1px solid {OSDAG_GREEN_DARK};
                color: #fff;
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
                text-align: center;
            }}
        """

    def _apply_animated_style(self, style_sheet_func, target_width, label_text=None, icon_path=None):
        """
        Applies a given style sheet and animates the button's width.
        Stops any ongoing animations before starting new ones.
        """
        self.animation.stop()
        self.animation_max_width.stop()

        current_width = self.width()

        self.animation.setStartValue(current_width)
        self.animation.setEndValue(target_width)
        self.animation_max_width.setStartValue(current_width)
        self.animation_max_width.setEndValue(target_width)
        
        # Apply the style sheet immediately
        self.setStyleSheet(style_sheet_func())

        # Update icon and text if provided
        if icon_path:
            self.setIcon(QIcon(icon_path))
        if label_text is not None:
            self.setText(label_text)

        # Start the width animations
        self.animation.start()
        self.animation_max_width.start()

    def enterEvent(self, event):
        """
        Handles mouse entering the button area.
        Changes style to hover state if no click animation is active.
        """
        self.is_hovering = True
        # Only apply hover style if the button is not currently in a "clicked" animation
        if not self.click_animation_timer.isActive():
            self._apply_animated_style(self.hover_style_sheet, 120, self.label_text, self.white_icon_path)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        Handles mouse leaving the button area.
        Reverts style to default state if no click animation is active.
        """
        self.is_hovering = False
        # Only apply default style if the button is not currently in a "clicked" animation
        if not self.click_animation_timer.isActive():
            self._apply_animated_style(self.default_style_sheet, 36, "", self.black_icon_path)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """
        Handles mouse button press event.
        Applies a momentary 'pressed' style and starts a timer to revert it.
        """
        if event.button() == Qt.LeftButton:
            # Apply the pressed style immediately
            self._apply_animated_style(self.pressed_style_sheet, 120, self.label_text, self.white_icon_path)
            # Start the timer to reset the style after a short delay
            self.click_animation_timer.start(150) # Revert after 150 milliseconds
        super().mousePressEvent(event)

    def _reset_style_after_click(self):
        """
        Callback function for `click_animation_timer`.
        Resets the button's style based on whether the mouse is still hovering or not.
        """
        if self.is_hovering:
            # If the mouse is still over the button, revert to hover style
            self._apply_animated_style(self.hover_style_sheet, 120, self.label_text, self.white_icon_path)
        else:
            # If the mouse has left, revert to default style
            self._apply_animated_style(self.default_style_sheet, 36, "", self.black_icon_path)

class TopButton1(QPushButton):
    """
    Custom QPushButton that changes style on hover and provides a momentary
    color change on click, instead of a persistent selected state.
    """
    # Define custom signals that this button will emit
    button_activated = Signal(QPushButton) # Emits the button instance when activated
    button_deactivated = Signal(QPushButton) # Emits the button instance when deactivated

    def __init__(self, black_icon_path, white_icon_path, label, parent=None):
        super().__init__(parent)
        self.black_icon_path = black_icon_path
        self.white_icon_path = white_icon_path
        self.label_text = label
        
        self.is_hovering = False
        self.is_active = False 
        
        self.click_animation_timer = QTimer(self)
        self.click_animation_timer.setSingleShot(True)
        self.click_animation_timer.timeout.connect(self._reset_style_after_click)
        
        self.setMinimumSize(40, 40)
        self.setMaximumHeight(40)
        self.setIconSize(QSize(20, 20))
        
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        self.animation_max_width = QPropertyAnimation(self, b"maximumWidth")
        self.animation_max_width.setDuration(200)
        self.animation_max_width.setEasingCurve(QEasingCurve.OutCubic)

        self.setIcon(QIcon(self.black_icon_path))
        self.setText("")
        self.setStyleSheet(self.default_style_sheet())
        self.setCursor(Qt.PointingHandCursor)
        
        self.setAttribute(Qt.WA_Hover, True)

    def default_style_sheet(self):
        return f"""
            QPushButton {{
                background: #fff;
                border: 1px solid {BORDER_COLOR};
                color: #000;
                font-size: 1px;
                padding: 10px;
                text-align: center;
            }}
        """

    def hover_style_sheet(self):
        return f"""
            QPushButton {{
                background: {OSDAG_GREEN};
                border: 1px solid {OSDAG_GREEN_DARK};
                color: #fff;
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
                text-align: center;
            }}
        """

    def pressed_style_sheet(self):
        return f"""
            QPushButton {{
                background: {OSDAG_GREEN_DARK};
                border: 1px solid {OSDAG_GREEN_DARK};
                color: #fff;
                font-size: 14px;
                font-weight: 600;
                padding: 12px;
                text-align: center;
            }}
        """

    def _apply_animated_style(self, style_sheet_func, target_width, label_text=None, icon_path=None):
        self.animation.stop()
        self.animation_max_width.stop()

        current_width = self.width()

        self.animation.setStartValue(current_width)
        self.animation.setEndValue(target_width)
        self.animation_max_width.setStartValue(current_width)
        self.animation_max_width.setEndValue(target_width)
        
        self.setStyleSheet(style_sheet_func())

        if icon_path:
            self.setIcon(QIcon(icon_path))
        if label_text is not None:
            self.setText(label_text)

        self.animation.start()
        self.animation_max_width.start()

    def enterEvent(self, event):
        self.is_hovering = True
        if not self.is_active and not self.click_animation_timer.isActive():
            self._apply_animated_style(self.hover_style_sheet, 120, self.label_text, self.white_icon_path)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovering = False
        if not self.is_active and not self.click_animation_timer.isActive():
            self._apply_animated_style(self.default_style_sheet, 36, "", self.black_icon_path)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._apply_animated_style(self.pressed_style_sheet, 120, self.label_text, self.white_icon_path)
            
            self.click_animation_timer.start(100)

            # Toggle the active state
            self.is_active = not self.is_active
            
            # Emit the signals directly from this button instance
            if self.is_active:
                self.button_activated.emit(self) # Emitting from TopButton1
            else:
                self.button_deactivated.emit(self) # Emitting from TopButton1

        super().mousePressEvent(event)

    def _reset_style_after_click(self):
        if self.is_active:
            self._apply_animated_style(self.hover_style_sheet, 120, self.label_text, self.white_icon_path)
        elif self.is_hovering:
            self._apply_animated_style(self.hover_style_sheet, 120, self.label_text, self.white_icon_path)
        else:
            self._apply_animated_style(self.default_style_sheet, 36, "", self.black_icon_path)

    def set_active(self, active: bool):
        if self.is_active == active:
            return

        self.is_active = active
        if self.is_active:
            self._apply_animated_style(self.hover_style_sheet, 120, self.label_text, self.white_icon_path)
        else:
            self._apply_animated_style(self.default_style_sheet, 36, "", self.black_icon_path)

class DropDownButton(TopButton1):
    """
    A specialized TopButton for "Resources" that opens a dropdown menu on click.
    It inherits the momentary click effect from TopButton.
    """
    def __init__(self, black_icon_path, white_icon_path, label, parent=None):
        super().__init__(black_icon_path, white_icon_path, label, parent)
        self.setup_menu()

    def setup_menu(self):
        """
        Sets up the dropdown menu with Osdag-themed styling and actions.
        """
        self.menu = QMenu(self)
        self.menu.setStyleSheet(f"""
            QMenu {{
                background: #fff;
                border: 1px solid {OSDAG_GREEN};
                font-size: 14px;
                padding: 0px;
            }}
            QMenu::item {{
                padding: 8px 16px;
                color: #333;
                border: none;
                margin: 1px;
            }}
            QMenu::item:selected {{
                background: {OSDAG_GREEN};
                color: #fff;
                border-radius: 2px;
            }}
        """)
        
        menu_items = ["Videos", "Osi File", "Documentation", "Databases"]
        for text in menu_items:
            action = QAction(text, self)
            # Connect each action to a simple print statement for demonstration
            action.triggered.connect(lambda clicked, t=text: print(f"Resources -> {t} clicked"))
            self.menu.addAction(action)

    def mousePressEvent(self, event):
        """
        Overrides mousePressEvent to show the dropdown menu when the button is clicked.
        Also calls the super class's mousePressEvent to get the momentary click animation.
        """
        super().mousePressEvent(event) # Call parent's method for click animation
        # Use singleShot to ensure the menu pops up slightly after the click visual feedback
        # This prevents the menu from interfering with the immediate style change
        QTimer.singleShot(50, lambda: self.menu.popup(self.mapToGlobal(QPoint(0, self.height()))))
