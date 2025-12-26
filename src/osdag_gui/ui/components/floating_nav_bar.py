"""
Floating navigation bar for Osdag GUI.
Provides quick access to modules and emits tab open signals.
"""
import osdag_gui.resources.resources_rc
from osdag_gui.data.ui_data import Data

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QToolTip, QApplication, QSizePolicy
)
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt, QSize, QPoint, QTimer, QEvent, Signal

class SidebarIconButton(QPushButton):
    # Class-level attribute for default hover color

    def __init__(self, icon_path, tooltip_text="", selected_icon_path=None, hover_icon_path=None, dark_icon_path=None, group=None, parent=None):
        super().__init__(parent)
        self.theme = QApplication.instance().theme_manager
        self.group = group
        self.icon_path = icon_path
        self.selected_icon_path = selected_icon_path
        self.hover_icon_path = hover_icon_path
        self.setObjectName("floating_btn")

        self.is_selected = False

        # Disable buttons
        if tooltip_text in ["Beam Column",
                            "Truss",
                            "2D Frame",
                            "3D Frame"]:
            self.setDisabled(True)
            self.custom_tooltip_text = "Under Development"
            self.setCursor(Qt.CursorShape.ForbiddenCursor)
        else:
            self.custom_tooltip_text = tooltip_text

        # Load icons
        self.default_icon = self._load_icon(icon_path)
        self.selected_icon = self._load_icon(selected_icon_path)
        self.hover_icon = self._load_icon(hover_icon_path)
        self.dark_icon = self._load_icon(dark_icon_path)

        if self.theme.is_light():
            self.setIcon(self.default_icon)
        else:
            self.setIcon(self.dark_icon)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)

        self.set_default_style()

        self.tooltip_show_timer = QTimer(self)
        self.tooltip_show_timer.setSingleShot(True)
        self.tooltip_show_timer.setInterval(100)
        self.tooltip_show_timer.timeout.connect(self._show_custom_tooltip)

    def _load_icon(self, path, icon_type=""):
        return QIcon(path)

    def paintEvent(self, event):
        if not self.is_selected:
            if self.theme.is_light():
                self.setIcon(self.default_icon)
            else:
                self.setIcon(self.dark_icon)
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        if self.group:
            for btn in self.group:
                if btn != self:
                    btn.is_selected = False
                    btn.set_default_style()
                    if self.theme.is_light():
                        btn.setIcon(btn.default_icon)
                    else:
                        btn.setIcon(btn.dark_icon)

        self.is_selected = True
        self.set_selected_style()
        self.setIcon(self.selected_icon)

        QToolTip.hideText()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if not self.is_selected:
            self.set_selected_style()
            self.setIcon(self.hover_icon)

        self.tooltip_show_timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_selected:
            self.set_default_style()
            if self.theme.is_light():
                self.setIcon(self.default_icon)
            else:
                self.setIcon(self.dark_icon)

        self.tooltip_show_timer.stop()
        QToolTip.hideText()
        super().leaveEvent(event)

    def _show_custom_tooltip(self):
        if not self.custom_tooltip_text:
            return

        global_pos = QCursor.pos()
        offset_x = 18
        offset_y = -8
        tooltip_pos = global_pos + QPoint(offset_x, offset_y)
        QToolTip.showText(tooltip_pos, self.custom_tooltip_text, self)

    def set_default_style(self):
        self.setProperty("state", "default")
        self.style().unpolish(self)
        self.style().polish(self)

    def set_selected_style(self):
        self.setProperty("state", "active")
        self.style().unpolish(self)
        self.style().polish(self)

class SidebarWidget(QWidget):
    openNewTab = Signal(str)
    
    def __init__(self, parent):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.button_group = []
        self.button_container = QWidget(self)
        self.button_container.setObjectName("floating_btn_container")
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignHCenter)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(0)  # spacing between buttons (matches navbar spacing)

        dat = Data()
        navbar_icons = dat.NAVBAR_ICONS

        for tooltip, icons in navbar_icons.items():
            btn = SidebarIconButton(icons[0], tooltip_text=tooltip, selected_icon_path=icons[0], hover_icon_path=icons[0], dark_icon_path=icons[1] ,group=self.button_group)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.button_layout.addWidget(btn)
            self.button_group.append(btn)
            btn.clicked.connect(lambda _,title=tooltip: self.openNewTab.emit(title))
        self.button_container.setLayout(self.button_layout)
        self.layout.addWidget(self.button_container, alignment=Qt.AlignCenter)
        
        # Initial update of sizes
        self.update_responsive_elements()

    def update_responsive_elements(self):
        """Updates button sizes and icon sizes based on parent widget dimensions - matches navbar.py exactly."""
        if not self.parent:
            return
            
        # Use parent's height for calculations (same as navbar.py uses widget_height)
        parent_height = self.parent.height()
        parent_width = self.parent.width()

        if parent_height <= 0 or parent_width <= 0:
            return  # Avoid division by zero or invalid sizes

        num_buttons = len(self.button_group)
        if num_buttons == 0:
            return

        # Calculate button font size (same formula as navbar.py)
        button_font_size = max(10, int(parent_height / 55))
        
        # Calculate icon size (same formula as navbar.py)
        icon_size = max(20, int(button_font_size * 2))
        
        # Calculate button size to match navbar button dimensions
        # Navbar buttons expand vertically, so we estimate their height
        # Using similar proportions: button height is roughly 3.5x the font size
        button_size = max(icon_size + 20, int(button_font_size * 3.5))
        
        # Calculate total sidebar dimensions
        spacing = self.button_layout.spacing()
        sidebar_width = button_size
        sidebar_height = num_buttons * button_size + (num_buttons - 1) * spacing
        
        # Set fixed dimensions
        self.setFixedWidth(sidebar_width)
        self.setFixedHeight(sidebar_height)
        
        # Apply sizes to all buttons
        for btn in self.button_group:
            btn.setFixedSize(button_size, button_size)
            btn.setIconSize(QSize(icon_size, icon_size))

    def resizeEvent(self, event: QEvent):
        """Called when the widget is resized."""
        super().resizeEvent(event)
        self.update_responsive_elements()  # Recalculate and apply sizes

    def resize_sidebar(self, window_width, window_height):
        """Called when parent window is resized - updates sizes"""
        self.update_responsive_elements()
        
    def showEvent(self, event):
        """Called when the widget is shown."""
        super().showEvent(event)
        self.update_responsive_elements()