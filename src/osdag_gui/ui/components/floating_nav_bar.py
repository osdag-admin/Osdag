import os
import osdag_gui.resources.resources_rc

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QApplication, QToolTip
)
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt, QSize, QPoint, QTimer

class SidebarIconButton(QPushButton):
    # Class-level attribute for default hover color
    default_hover_color = "#d1f16a"
    selected_color = "#d1f16a"
    BUTTON_MARGIN = 3
    BUTTON_PADDING = 1

    def __init__(self, icon_path, tooltip_text="", selected_icon_path=None, hover_icon_path=None, group=None, parent=None):
        super().__init__(parent)
        self.group = group
        self.icon_path = icon_path
        self.selected_icon_path = selected_icon_path
        self.hover_icon_path = hover_icon_path

        self.is_selected = False
        self.custom_tooltip_text = tooltip_text

        # Load icons
        self.default_icon = self._load_icon(icon_path, "default")
        self.selected_icon = self._load_icon(selected_icon_path, "selected") if selected_icon_path else self.default_icon
        self.hover_icon = self._load_icon(hover_icon_path, "hover") if hover_icon_path else self.selected_icon

        self.setIcon(self.default_icon)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)

        self.set_default_style()

        self.tooltip_show_timer = QTimer(self)
        self.tooltip_show_timer.setSingleShot(True)
        self.tooltip_show_timer.setInterval(100)
        self.tooltip_show_timer.timeout.connect(self._show_custom_tooltip)

    def _load_icon(self, path, icon_type=""):
        return QIcon(path)

    def mousePressEvent(self, event):
        if self.group:
            for btn in self.group:
                if btn != self:
                    btn.is_selected = False
                    btn.set_default_style()
                    btn.setIcon(btn.default_icon)

        self.is_selected = True
        self.set_selected_style()
        self.setIcon(self.selected_icon)

        QToolTip.hideText()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        if not self.is_selected:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.default_hover_color};
                    border: none;
                    border-radius: 5px;
                    margin: {self.BUTTON_MARGIN}px;
                    padding: {self.BUTTON_PADDING}px;
                }}
            """)
            self.setIcon(self.hover_icon)

        self.tooltip_show_timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_selected:
            self.set_default_style()
            self.setIcon(self.default_icon)

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
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: white;
                border: none;
                border-radius: 5px;
                margin: {self.BUTTON_MARGIN}px;
                padding: {self.BUTTON_PADDING}px;
            }}
        """)

    def set_selected_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.selected_color};
                border-radius: 5px;
                border: none;
                margin: {self.BUTTON_MARGIN}px;
                padding: {self.BUTTON_PADDING}px;
            }}
        """)

class SidebarWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.button_group = []
        self.button_container = QWidget(self)
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignHCenter)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(0)  # spacing between buttons
        icon_paths = [
            (":/vectors/default_icon.svg", "Home"),
            (":/vectors/default_icon.svg", "Connection"),
            (":/vectors/default_icon.svg", "Tension Member"),
            (":/vectors/default_icon.svg", "Compression Member"),
            (":/vectors/default_icon.svg", "Flexural Member"),
            (":/vectors/default_icon.svg", "Beam Column"),
            (":/vectors/default_icon.svg", "Plate Girder"),
            (":/vectors/default_icon.svg", "Truss"),
            (":/vectors/default_icon.svg", "2D Frame"),
            (":/vectors/default_icon.svg", "3D Frame"),
            (":/vectors/default_icon.svg", "Group Design")
        ]
        self.icon_size = 48  # px, you can adjust this value as needed
        for i, (icon_path, tooltip) in enumerate(icon_paths):
            btn = SidebarIconButton(icon_path, tooltip_text=tooltip, selected_icon_path=":/vectors/clicked_icon.svg", hover_icon_path=":/vectors/clicked_icon.svg" ,group=self.button_group)
            self.button_layout.addWidget(btn)
            self.button_group.append(btn)
            btn.clicked.connect(lambda _,title=tooltip: self.parent.handle_add_tab(title))
        self.button_container.setLayout(self.button_layout)
        self.layout.addWidget(self.button_container, alignment=Qt.AlignCenter)
        self.update_sidebar_size()

        # Apply global QToolTip stylesheet here
        QApplication.instance().setStyleSheet("""
            QToolTip {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #90AF13;
                padding: 2px 2px;
                font-size: 10px;
                border-radius: 0px;
                qproperty-alignment: AlignVCenter;
            }
        """)


    def update_sidebar_size(self):
        num_buttons = len(self.button_group)
        margin = SidebarIconButton.BUTTON_MARGIN
        padding = SidebarIconButton.BUTTON_PADDING
        spacing = self.button_layout.spacing()
        icon_size = self.icon_size
        button_size = icon_size + 2 * (margin + padding)
        sidebar_width = button_size
        sidebar_height = num_buttons * button_size + (num_buttons - 1) * spacing
        self.setFixedWidth(sidebar_width)
        self.setFixedHeight(sidebar_height)
        for btn in self.button_group:
            btn.setFixedSize(icon_size, icon_size)
            btn.setIconSize(QSize(icon_size * 0.4, icon_size * 0.4))

    def resize_sidebar(self, window_width, window_height):
        # No longer use window size for sidebar sizing
        self.update_sidebar_size()
        self.setStyleSheet("""
            QWidget{
                border: 1px solid #90AF13;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
        """)