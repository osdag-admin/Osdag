import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QLineEdit, QPushButton, QButtonGroup,
    QMenu, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, QPoint, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QKeySequence, QColor, QFont, QShortcut, QCursor, QPainter, QAction, QFontMetrics
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer # Import QSvgRenderer for custom painting

import osdag_gui.resources.resources_rc
from osdag_gui.resources.databases.data import Data

# --- Theme Toggle Button ---
class ThemeToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark_mode = True
        self.setFixedSize(50, 50)
        self.setObjectName("themeToggle")
        self.setStyleSheet("""
            #themeToggle {
                background: transparent;
                border: none;
                border-radius: 20px;
            }
            #themeToggle:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.toggle_theme)
        self.update_icon()

    def update_icon(self):
        icon_path = ":/vectors/night_button.svg" if not self.is_dark_mode else ":/vectors/day_button_dark.svg"
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(25, 25))

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_icon()
        if self.parent() and hasattr(self.parent(), 'toggle_theme'):
            self.parent().toggle_theme(self.is_dark_mode)

# --- SVG Widget with Theme Support ---
class ThemedSvgWidget(QSvgWidget):
    def __init__(self, light_svg, dark_svg, scale_factor=1.0, parent=None):
        super().__init__(parent)
        self.light_svg_path = light_svg
        self.dark_svg_path = dark_svg
        self.scale_factor = scale_factor
        self.is_dark_mode = False
        self.load_svg()

    def load_svg(self):
        svg_path = self.dark_svg_path if self.is_dark_mode else self.light_svg_path
        if os.path.exists(svg_path):
            self.load(svg_path)
            if self.renderer():
                native_size = self.renderer().defaultSize()
                scaled_size = QSize(
                    int(native_size.width() * self.scale_factor),
                    int(native_size.height() * self.scale_factor)
                )
                self.setFixedSize(scaled_size)

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.load_svg()

# --- Enhanced Search Bar Widget ---
class SearchBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_focused = False
        self.setupUI()
        self.setStyleSheet("""
            #searchContainer {
                    border: 2px solid #e1e5e9;
                    border-radius: 24px;
                    background: white;
                    min-height: 48px;
                    padding: 0px 8px;
            }
            #searchContainer[focused="true"] {
                border-color: #C8D8A2;
            }
            #searchInput {
                border: none;
                background: transparent;
                font-size: 16px;
                color: #333;
            }
            #searchInput:focus {
                outline: none;
                border: none;
            }
            #shortcutKey, #lKey {
                background: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                color: #666;
                font-size: 11px;
                font-weight: 600;
                padding: 2px 4px;
            }
            #plusLabel {
                color: #888;
                font-size: 12px;
                font-weight: 500;
            }
        """)

    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.search_container = QWidget()
        # self.search_container.setStyleSheet("""
        #         QWidget { background: red; }
        # """)
        self.search_container.setObjectName("searchContainer")
        container_layout = QHBoxLayout(self.search_container)
        container_layout.setContentsMargins(15, 0, 15, 0)
        container_layout.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search modules or projects...")
        self.search_input.setFixedHeight(48)
        self.search_input.setObjectName("searchInput")
        container_layout.addWidget(self.search_input)

        shortcut_layout = QHBoxLayout()
        shortcut_layout.setContentsMargins(0, 0, 0, 0)
        shortcut_layout.setSpacing(0)

        self.shortcut_hint = QLabel("Ctrl")
        self.shortcut_hint.setObjectName("shortcutKey")
        self.shortcut_hint.setFixedSize(32, 20)
        self.shortcut_hint.setAlignment(Qt.AlignmentFlag.AlignRight)
        shortcut_layout.addWidget(self.shortcut_hint)

        self.plus_label = QLabel("+")
        self.plus_label.setObjectName("plusLabel")
        self.plus_label.setFixedSize(20, 20)
        self.plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shortcut_layout.addWidget(self.plus_label)

        self.l_key = QLabel("L")
        self.l_key.setObjectName("lKey")
        self.l_key.setFixedSize(20, 20)
        self.l_key.setAlignment(Qt.AlignmentFlag.AlignLeft)
        shortcut_layout.addWidget(self.l_key)

        container_layout.addLayout(shortcut_layout)

        self.search_icon = QSvgWidget(":/vectors/search_icon.svg")
        self.search_icon.setObjectName("searchIcon")
        self.search_icon.setFixedSize(20, 20)
        container_layout.addWidget(self.search_icon)
        

        layout.addWidget(self.search_container)
        
        self.search_input.focusInEvent = self._focus_in_event
        self.search_input.focusOutEvent = self._focus_out_event

    def _focus_in_event(self, event):
        self.is_focused = True
        self.search_container.setProperty("focused", True)
        self.search_container.style().unpolish(self.search_container)
        self.search_container.style().polish(self.search_container)
        QLineEdit.focusInEvent(self.search_input, event)

    def _focus_out_event(self, event):
        self.is_focused = False
        self.search_container.setProperty("focused", False)
        self.search_container.style().unpolish(self.search_container)
        self.search_container.style().polish(self.search_container)
        QLineEdit.focusOutEvent(self.search_input, event)

    @property
    def textChanged(self):
        return self.search_input.textChanged

    def setFocus(self):
        self.search_input.setFocus()

    def selectAll(self):
        self.search_input.selectAll()

# --- Project Item Widget ---
class ProjectItem(QFrame):
    def __init__(self, project_data, index):
        super().__init__()
        self.project_data = project_data
        self.index = index
        self.original_height = 55  # Reduced from 60
        self.expanded_height = 95  # Reduced from 100
        self.is_expanded = False
        self.setStyleSheet("""
            #projectItem{
                background: #f8f9fa;
                border: 1px solid #e2e8f0;
                margin: 2px 4px 6px 4px;
                border-radius: 10px;
            }
            #projectItem:hover{
                background: #D5E49B;
                border-color: #9BC53D;
            }
            #projectItem[selected="true"] {
                background: #D5E49B;
                border-color: #9BC53D;
            }
            #projectName{
                color: #1a202c;
            }
            #projectFullName{
                color: #718096;
            }
        """)
        self.setupUI()
    def mousePressEvent(self, event):
        self.set_selected(True)
        # Optionally notify parent to deselect others

    def set_selected(self, selected):
        if selected:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 2)
            shadow.setColor(QColor(155, 197, 61, 90))
            self.setGraphicsEffect(shadow)
        else:
            self.setGraphicsEffect(None)

    def update_style(self):
        if self.selected:
            self.setProperty("selected", True)
        else:
            self.setProperty("selected", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def setupUI(self):
        self.setObjectName("projectItem")
        self.setFixedHeight(self.original_height)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        
        # Project info layout
        info_layout = QHBoxLayout()
        info_layout.setSpacing(0)
        
        # Number label
        number_label = QLabel("L")
        number_label.setFixedSize(20, 20)
        number_label.setAlignment(Qt.AlignCenter)
        number_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #1a202c;
                font-size: 16px;
            }
        """)

        # Project details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(1)
        
        project_name_label = QLabel(self.project_data["sub_module"])
        project_name_label.setObjectName("projectName")
        project_name_label.setWordWrap(True)
        project_name_label.setContentsMargins(2, 2, 2, 2)  # NEW
        project_name_label.setMinimumHeight(10) 
        
        # Truncate long project names
        project_full_text = self.project_data["project_name"]
        if len(project_full_text) > 35:  # Reduced from 40
            project_full_text = project_full_text[:32] + "..."
        
        project_full_label = QLabel(project_full_text)
        project_full_label.setObjectName("projectFullName")
        project_full_label.setWordWrap(True)
        project_full_label.setContentsMargins(2, 2, 2, 2)
        project_full_label.setMinimumHeight(18)
        
        details_layout.addWidget(project_name_label)
        details_layout.addWidget(project_full_label)
        
        # Date label
        date_label = QLabel(self.project_data["last_date"])
        date_label.setObjectName("dateLabel")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        info_layout.addWidget(number_label)
        info_layout.addLayout(details_layout)
        info_layout.addStretch()
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        
        # FIXED Action buttons - GUARANTEED full visibility
        self.actions_frame = QFrame()
        self.actions_frame.setObjectName("actionsFrame")
        self.actions_frame.setStyleSheet("background: transparent;")
        actions_layout = QHBoxLayout(self.actions_frame)
        actions_layout.setContentsMargins(20, 5, 10, 5)  # Better margins
        actions_layout.setSpacing(5)  # Reduced spacing
        
        # Buttons with FULL visibility
        self.generate_btn = QPushButton("Generate Report")
        self.download_btn = QPushButton("Download OSI")
        self.open_btn = QPushButton("Open project")
        
        # GUARANTEED full visibility styling
        for btn in [self.generate_btn, self.download_btn, self.open_btn]:
            btn.setFixedHeight(25)  # Slightly smaller
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff ;
                    border-radius: 12px;
                    color: #2d3748 ;
                    border: 1px solid #cccccc ;
                    padding: 4px 5px ;
                    font-size: 10px ;
                    font-weight: 600 ;
                }
                QPushButton:hover {
                    background-color: #f0f4e3 ;
                    border-color: #9BC53D ;
                }
                QPushButton:pressed {
                    background-color: #d6e6be ;
                }
            """)
        
        actions_layout.addWidget(self.generate_btn)
        actions_layout.addWidget(self.download_btn)
        actions_layout.addWidget(self.open_btn)
        actions_layout.addStretch()
        
        self.actions_frame.setVisible(False)
        layout.addWidget(self.actions_frame)
        
        # Smooth animation
        self.expand_animation = QPropertyAnimation(self, b"maximumHeight")
        self.expand_animation.setDuration(250)
        self.expand_animation.setEasingCurve(QEasingCurve.OutCubic)

    def enterEvent(self, event):
        if not self.is_expanded:
            self.is_expanded = True
            self.setProperty("hovered", True)
            self.style().unpolish(self)
            self.style().polish(self)
            
            # Show buttons IMMEDIATELY
            self.actions_frame.setVisible(True)
            self.actions_frame.raise_()
            
            # Animate expansion
            self.expand_animation.stop()
            self.expand_animation.setStartValue(self.original_height)
            self.expand_animation.setEndValue(self.expanded_height)
            self.expand_animation.start()
            
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.is_expanded:
            self.is_expanded = False
            self.setProperty("hovered", False)
            self.style().unpolish(self)
            self.style().polish(self)
            
            # Hide buttons
            self.actions_frame.setVisible(False)
            
            # Animate collapse
            self.expand_animation.stop()
            self.expand_animation.setStartValue(self.expanded_height)
            self.expand_animation.setEndValue(self.original_height)
            self.expand_animation.start()
            
        super().leaveEvent(event)

class ModuleItem(QFrame):
    def __init__(self, module_data, is_dark_mode):
        super().__init__()
        self.module_data = module_data
        self.is_dark_mode = is_dark_mode
        self.setStyleSheet("""
            #moduleItem {
                background: #f8f9fa;
                border: 1px solid #e2e8f0;
                margin: 2px 4px 6px 4px;
                border-radius: 10px;
            }
            #moduleItem:hover {
                background: #D5E49B;
                border-color: #9BC53D;
            }
            #moduleName {
                color: #1a202c;
            }
            #subModuleLabel {
                color: #718096;
            }
            #dateLabel {
                color: #a0aec0;
                font-weight: 500;
            }
        """)
        self.setupUI()
        self.selected = False
    def mousePressEvent(self, event):
        self.set_selected(True)
        # Optionally notify parent to deselect others

    def set_selected(self, selected):
        self.selected = selected
        self.update_style()
    def update_style(self):
        if self.selected:
            self.setProperty("selected", True)
        else:
            self.setProperty("selected", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def setupUI(self):
        self.setObjectName("moduleItem")
        self.setFixedHeight(55)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # Icon with proper SVG handling
        icon_label = QLabel()
        icon_label.setFixedSize(20, 20)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setObjectName("moduleIcon")
        
        # Use the correct icon path based on theme
        if self.is_dark_mode:
            icon_path = ":/vectors/recently_used_module_icon_dark.svg"
        else:
            icon_path = ":/vectors/recently_used_module_icon.svg"
        # Create icon using the svg to icon function
        icon = QIcon(icon_path).pixmap(QSize(16, 16))
        icon_label.setPixmap(icon)
        
        # Module details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(2)
        
        module_name_label = EllipsisLabel(self.module_data["module_name"])
        module_name_label.setObjectName("moduleName")
        module_name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        details_layout.addWidget(module_name_label)
        
        if self.module_data.get("sub_module"):
            sub_module_label = EllipsisLabel(self.module_data["sub_module"])
            sub_module_label.setObjectName("subModuleLabel")
            sub_module_label.setFont(QFont("Segoe UI", 8, QFont.Weight.Normal))
            details_layout.addWidget(sub_module_label)
        
        # Date label
        date_label = QLabel(self.module_data["date_created"])
        date_label.setObjectName("dateLabel")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        date_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Normal))
        
        layout.addWidget(icon_label)
        layout.addLayout(details_layout)
        layout.addStretch()
        layout.addWidget(date_label)

class SectionWidget(QFrame):
    def __init__(self, title, items, is_project=True, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.items = items
        self.is_project = is_project
        self.title = title
        self.setObjectName("sectionFrame")
        self.setStyleSheet("""
            #sectionFrame {
                background: #ffffff;
                border: 2px solid #e1e5e9;
                border-radius: 18px;
            }
            #sectionHeading {
                font-family: "Calibri", sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: #000000;
                background: transparent;
                padding: 8px;
            }
            #scrollContainer {
                background: #ffffff;
            }
            
            QScrollArea {
                border: none;
                padding: 10px;
            }

            /* Scrollbar itself */
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }

            /* Handle */
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }

            /* Handle on hover */
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }

            /* Handle when pressed */
            QScrollBar::handle:vertical:pressed {
                background: #808080; /* Even darker grey when pressed */
            }

            /* Remove add/sub line buttons (arrows) */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }

            /* Styling the page area (the track around the handle) */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none; /* Make the page area transparent, letting the QScrollBar background show through */
            }
        """)
        self.setFixedSize(350, 320)
        self.setupUI()

    def set_heading_text(self, new_title):
        heading = self.findChild(QLabel, "sectionHeading")
        if heading:
            heading.setText(new_title)
    
    def setupUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Heading to match the image style
        heading = QLabel(self.title)
        heading.setAlignment(Qt.AlignCenter)
        heading.setObjectName("sectionHeading")
        heading.setFixedHeight(48)
        layout.addWidget(heading)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setObjectName("scrollArea")
        scroll.setFixedHeight(275)
        
        container = QWidget()
        container.setObjectName("scrollContainer")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(8, 5, 8, 5)
        vbox.setSpacing(2)
        
        # Add items
        for i, item in enumerate(self.items, 1):
            if self.is_project:
                item_widget = ProjectItem(item, i)
            else:
                is_dark = self.main_window.is_dark_mode if self.main_window else False
                item_widget = ModuleItem(item, is_dark)
            vbox.addWidget(item_widget)
        
        vbox.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll)

    def update_theme(self, is_dark_mode):
        if not self.is_project:
            # Recreate module items with new theme
            scroll_area = self.findChild(QScrollArea)
            if scroll_area:
                container = scroll_area.widget()
                if container:
                    layout = container.layout()
                    # Clear existing items
                    while layout.count() > 1:
                        child = layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()
                    
                    # Recreate items with new theme
                    for i, item in enumerate(self.items, 1):
                        item_widget = ModuleItem(item, is_dark_mode)
                        layout.insertWidget(i-1, item_widget)

class EllipsisLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self._text = text
        self.setText(text)

    def setText(self, text):
        self._text = text
        self.updateText()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateText()

    def updateText(self):
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self._text, Qt.ElideRight, self.width())
        super().setText(elided)

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_item = None
        self.is_dark_mode = False
        self.setupUI()
        self.setupShortcuts()

    def setupShortcuts(self):
        search_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        search_shortcut.activated.connect(self.focus_search_bar)

    def focus_search_bar(self):
        self.search_bar.setFocus()
        self.search_bar.selectAll()

    def setupUI(self):
        content_area_layout = QVBoxLayout(self)
        content_area_layout.setContentsMargins(0, 0, 0, 0)
        content_area_layout.setSpacing(0)

        search_layout = QHBoxLayout()
        search_layout.addStretch()
        self.search_bar = SearchBarWidget()
        self.search_bar.setFixedWidth(500)
        search_layout.addWidget(self.search_bar)

        self.theme_toggle = ThemeToggleButton(self)
        # self.theme_toggle.clicked.connect(self.toggle_theme)
        search_layout.addWidget(self.theme_toggle)
        search_layout.addStretch()
        content_area_layout.addLayout(search_layout)

        content_area_layout.addStretch()

        sections_layout = QHBoxLayout()
        sections_layout.setSpacing(30)
        # --- Add more dummy data for scroll testing ---
        data = Data()
        projects = data.recent_projects()
        modules = data.recent_modules()

        self.recent_projects = SectionWidget("Recent Projects", projects, is_project=True, main_window=self)
        self.recent_modules = SectionWidget("Recently Used Modules", modules, is_project=False, main_window=self)
        sections_layout.addStretch(1)
        sections_layout.addWidget(self.recent_projects, alignment=Qt.AlignCenter)
        sections_layout.addWidget(self.recent_modules, alignment=Qt.AlignCenter)
        sections_layout.addStretch(1)
        content_area_layout.addLayout(sections_layout)