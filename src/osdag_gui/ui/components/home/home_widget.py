"""
Home widget for Osdag GUI.
Displays recent projects, modules, and search bar.
"""
import sys, shutil
import os, subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QLineEdit, QPushButton, QFileDialog,
    QMenu, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, QPoint, Signal, QPropertyAnimation, QEasingCurve, QThread
from PySide6.QtGui import QIcon, QKeySequence, QColor, QFont, QShortcut, QCursor, QPainter, QPixmap, QFontMetrics
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer # Import QSvgRenderer for custom painting

import osdag_gui.resources.resources_rc
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
from osdag_gui.data.database.database_config import *

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
    openProject = Signal(dict)
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
                font-size: 13px;
            }
            #submoduleName, #dateLabel{
                color: #718096;
                font-size: 11px;
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
        info_layout.addWidget(number_label)


        # Project details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(1)

        # Truncate long project names
        project_name = self.project_data[PROJECT_NAME]
        short_project_name = project_name
        if len(project_name) > 30:
            short_project_name = short_project_name[:30] + "..."
        
        project_name_label = QLabel(short_project_name)
        project_name_label.setObjectName("projectName")
        if len(project_name) > 30:
            project_name_label.setToolTip(project_name)
        project_name_label.setStyleSheet("""
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
        project_name_label.setWordWrap(True)
        project_name_label.setContentsMargins(2, 2, 2, 2)
        project_name_label.setMinimumHeight(18) 
        details_layout.addWidget(project_name_label)
        
        sub_detail_layout = QHBoxLayout()
        sub_detail_layout.setSpacing(0)
        sub_detail_layout.setContentsMargins(2, 0, 20, 0)

        # Truncate long project names
        submodule = self.project_data[RELATED_SUBMODULE]
        if len(submodule) > 24:
            submodule = submodule[:24] + "..."
        
        submodule_label = QLabel(submodule)
        submodule_label.setObjectName("submoduleName")
        submodule_label.setContentsMargins(1, 1, 1, 1)
        submodule_label.setMinimumHeight(18)
        sub_detail_layout.addWidget(submodule_label)
        
        # Date label
        date_label = QLabel(self.project_data[LAST_EDITED])
        date_label.setObjectName("dateLabel")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        sub_detail_layout.addWidget(date_label)

        details_layout.addLayout(sub_detail_layout)        
        info_layout.addLayout(details_layout)
        
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
        self.generate_btn.clicked.connect(lambda checked=False, record=self.project_data: self.recents_generate_report(record))

        self.download_btn = QPushButton("Download OSI")
        self.download_btn.clicked.connect(lambda checked=False, record=self.project_data: self.handle_download_osi(record))

        self.open_btn = QPushButton("Open Project")
        self.open_btn.clicked.connect(lambda checked=False, record=self.project_data: self.openProject.emit(record))
        
        # GUARANTEED full visibility styling
        for btn in [self.generate_btn, self.download_btn, self.open_btn]:
            btn.setFixedHeight(25)  # Slightly smaller
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
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

    def handle_download_osi(self, record: dict):
        # Ask user for save location
        src_path = record.get(PROJECT_PATH)
        if not src_path or not os.path.exists(src_path):
            CustomMessageBox(
                title="Error",
                text="Project file not found.",
                dialogType=MessageBoxType.Critical
            ).exec()
            return

        # Suggest a default filename
        default_name = os.path.basename(src_path) if src_path else "project.osi"
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save OSI File",
            default_name,
            "Osdag Project Files (*.osi);;All Files (*)"
        )
        if save_path:
            try:
                shutil.copy2(src_path, save_path)
                CustomMessageBox(
                    title="Success",
                    text=f"Project saved to:\n{save_path}",
                    dialogType=MessageBoxType.Success
                ).exec()
                
                # Open the directory containing the saved file
                folder = os.path.dirname(save_path)
                if folder and os.path.exists(folder):
                    try:
                        if sys.platform == 'win32':
                            os.startfile(folder)
                        elif sys.platform == 'darwin':
                            import subprocess
                            subprocess.run(['open', folder])
                        else:
                            import subprocess
                            subprocess.run(['xdg-open', folder])
                    except Exception as e:
                        print(f"Failed to open folder: {e}")

            except Exception as e:
                CustomMessageBox(
                    title="Error",
                    text=f"Failed to save file:\n{e}",
                    dialogType=MessageBoxType.Critical
                ).exec()

    #-------------Functions-to-generate-report-of-recent-project-START---------------------------

    class ReportWorker(QThread):
        success = Signal(str)   # emits PDF path
        error = Signal(str)     # emits error message

        def __init__(self, record, target_pdf, parent=None):
            super().__init__(parent)
            self.record = record
            self.target_pdf = target_pdf

        def run(self):
            try:
                # 1. Check if tex exist
                tex_path = os.path.join("osdag_gui", "data", "reports", f"file_{self.record[ID]}", "report.tex")
                if not os.path.isfile(tex_path):
                    self.error.emit(f"LaTeX file not found for this project:\n{tex_path}")
                    return

                # 2. Copy images
                base_dir = os.path.join("ResourceFiles", "images")
                os.makedirs(base_dir, exist_ok=True)

                report_dir = os.path.join("osdag_gui", "data", "reports", f"file_{self.record[ID]}")
                required_images = ["3d.png", "front.png", "top.png", "side.png"]

                for img in required_images:
                    src = os.path.join(report_dir, img)
                    dst = os.path.join(base_dir, img)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)

                # 3. Run pdflatex
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", os.path.basename(tex_path)],
                    cwd=os.path.dirname(tex_path),
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                # 4. Copy PDF
                generated_pdf = os.path.join(os.path.dirname(tex_path), "report.pdf")
                if os.path.isfile(generated_pdf):
                    shutil.copy2(generated_pdf, self.target_pdf)
                    self.success.emit(self.target_pdf)
                else:
                    self.error.emit("PDF generation failed. report.pdf not found.")

            except subprocess.TimeoutExpired:
                self.error.emit("pdflatex timed out.")
            except Exception as e:
                self.error.emit(str(e))
    
    def recents_generate_report(self, record: dict):
        # QFileDialog must stay in the main thread
        target_pdf, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report As",
            record[PROJECT_NAME],
            "PDF (*.pdf)"
        )
        if not target_pdf:
            return

        if not target_pdf.lower().endswith(".pdf"):
            target_pdf += ".pdf"

        # Run heavy stuff in worker thread
        self.worker = self.ReportWorker(record, target_pdf, parent=self)
        self.worker.success.connect(lambda path: CustomMessageBox(
            title="Success",
            text=f"PDF report saved successfully to:\n{path}",
            dialogType=MessageBoxType.Success
        ).exec())
        self.worker.error.connect(lambda msg: CustomMessageBox(
            title="Error",
            text=msg,
            dialogType=MessageBoxType.Critical
        ).exec())
        self.worker.start()

    #-------------Functions-to-generate-report-of-recent-project-END---------------------------

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
    openModule = Signal(str) # Module Key
    def __init__(self, module_data, is_dark_mode):
        super().__init__()
        self.module_data = module_data
        self.is_dark_mode = is_dark_mode
        self.setCursor(Qt.CursorShape.PointingHandCursor)
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
                font-size: 13px;
            }
            #subModuleLabel, #dateLabel {
                color: #718096;
                font-size: 11px;
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
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
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
        layout.addWidget(icon_label)

        # Module details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(2)
        
        module_name_label = EllipsisLabel(self.module_data[RELATED_SUBMODULE])
        module_name_label.setObjectName("moduleName")
        details_layout.addWidget(module_name_label)
        
        sub_detail_layout = QHBoxLayout()
        sub_detail_layout.setSpacing(0)
        sub_detail_layout.setContentsMargins(0, 0, 0, 0)

        sub_module_label = EllipsisLabel(self.module_data[RELATED_MODULE])
        sub_module_label.setObjectName("subModuleLabel")
        sub_detail_layout.addWidget(sub_module_label)
        
        # Date label
        date_label = QLabel(self.module_data[LAST_OPENED])
        date_label.setObjectName("dateLabel")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        sub_detail_layout.addWidget(date_label)

        details_layout.addLayout(sub_detail_layout)
        layout.addLayout(details_layout)
    
    # Mouse Press Event
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.openModule.emit(self.module_data.get(MODULE_KEY))
        return super().mousePressEvent(event)

class SectionWidget(QFrame):
    openProject = Signal(dict)
    openModule = Signal(str)
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
                item_widget.openProject.connect(self.openProject)
            else:
                is_dark = self.main_window.is_dark_mode if self.main_window else False
                item_widget = ModuleItem(item, is_dark)
                item_widget.openModule.connect(self.openModule)
            vbox.addWidget(item_widget)
        
        if len(self.items) == 0:
            vbox.addStretch()
            container.setStyleSheet("""
                QWidget#scrollContainer {
                    background: #f8f9fa;
                    border: 1px solid #e2e8f0;
                    margin: 2px 4px 6px 4px;
                    border-radius: 10px;
                }
            """)
            path = ''
            if self.is_project:
                path = ":/vectors/no_projects_light.svg"
            else:
                path = ":/vectors/no_modules_light.svg"
            empty_label = QSvgWidget(path)
            hlayout = QHBoxLayout()
            hlayout.addStretch()
            hlayout.addWidget(empty_label)
            hlayout.addStretch()
            vbox.addLayout(hlayout)
        
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
    openProject = Signal(dict)
    openModule = Signal(str)
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
        content_area_layout.addStretch()

        search_layout = QHBoxLayout()
        search_layout.addStretch()
        self.search_bar = SearchBarWidget()
        self.search_bar.setFixedWidth(500)
        search_layout.addWidget(self.search_bar)
        search_layout.addStretch()

        content_area_layout.addLayout(search_layout)
        content_area_layout.addStretch()

        sections_layout = QHBoxLayout()
        sections_layout.setSpacing(30)
        
        # Fetch recents data from database
        projects = fetch_all_recent_projects()
        modules = fetch_all_recent_modules()

        self.recent_projects = SectionWidget("Recent Projects", projects, is_project=True, main_window=self)
        self.recent_projects.openProject.connect(self.openProject)
        self.recent_modules = SectionWidget("Recently Used Modules", modules, is_project=False, main_window=self)
        self.recent_modules.openModule.connect(self.openModule)
        sections_layout.addStretch(1)
        sections_layout.addWidget(self.recent_projects, alignment=Qt.AlignCenter)
        sections_layout.addWidget(self.recent_modules, alignment=Qt.AlignCenter)
        sections_layout.addStretch(1)
        content_area_layout.addLayout(sections_layout)
        content_area_layout.addStretch()