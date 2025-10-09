"""
Search overlay components for Osdag GUI
Displays search results in a dropdown below the search bar
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame, QPushButton, QApplication
)
from PySide6.QtCore import Qt, Signal, QPoint, QPropertyAnimation, QEasingCurve, QTimer, QEvent
from PySide6.QtGui import QCursor, QPainterPath, QRegion
from osdag_gui.data.database.database_config import *

class SearchResultItem(QFrame):
    """Individual search result item with expandable action buttons"""
    openModule = Signal(str)
    openProject = Signal(dict)
    generateReport = Signal(dict)
    downloadOsi = Signal(dict)
    
    def __init__(self, item_data, item_type=KEY_SEARCH_PROJ, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.item_type = item_type
        self.original_height = 50
        self.expanded_height = 85
        self.is_expanded = False
        
        if item_type==KEY_SEARCH_MODULE:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.setStyleSheet("""
            SearchResultItem {
                background: white;
                border: 1px solid white;
                border-radius: 15px;
                padding: 4px 12px;
            }
            SearchResultItem:hover {
                border: 1px solid #9BC53D;
                background: #D5E49B;
            }
            QLabel#primaryText {
                color: #1a202c;
                font-size: 13px;
                font-weight: 600;
                background: transparent;
            }
            QLabel#secondaryText {
                color: #718096;
                font-size: 12px;
                background: transparent;
            }
            QLabel#dateText {
                color: #a0aec0;
                background: transparent;
                font-size: 11px;
            }
            QLabel#iconLabel {
                color: #2d3748;
                font-size: 16px;
                background: transparent;
                font-weight: bold;
            }
        """)
        
        self.setupUI()
    
    def setupUI(self):
        self.setFixedHeight(self.original_height)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(0)
        
        # Main info layout
        info_layout = QHBoxLayout()
        info_layout.setSpacing(12)
        
        # Icon/Letter
        icon_label = QLabel("L")
        icon_label.setObjectName("iconLabel")
        icon_label.setFixedSize(20, 20)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(icon_label)
        
        # Content layout
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)
        
        # Primary text (Project/Module name)
        if self.item_type == KEY_SEARCH_PROJ:
            primary_text = self.item_data.get(PROJECT_NAME)
        else:
            primary_text = self.item_data.get(RELATED_SUBMODULE)
        
        primary_label = QLabel(primary_text)
        primary_label.setObjectName("primaryText")
        content_layout.addWidget(primary_label)
        
        # Secondary text (Full path or module name)
        if self.item_type == KEY_SEARCH_PROJ:
            secondary_text = self.item_data.get(RELATED_SUBMODULE)
        else:
            secondary_text = self.item_data.get(RELATED_MODULE)
        
        if secondary_text:
            secondary_label = QLabel(secondary_text)
            secondary_label.setObjectName("secondaryText")
            content_layout.addWidget(secondary_label)
        
        info_layout.addLayout(content_layout, 1)
        
        # Date
        date_text = self.item_data.get(LAST_EDITED, "")
        if date_text:
            date_label = QLabel(date_text)
            date_label.setObjectName("dateText")
            date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            info_layout.addWidget(date_label)
        
        main_layout.addLayout(info_layout)
        
        # Action buttons frame (only for projects)
        if self.item_type == KEY_SEARCH_PROJ:
            self.actions_frame = QFrame()
            self.actions_frame.setObjectName("actionsFrame")
            self.actions_frame.setStyleSheet("background: transparent;")
            actions_layout = QHBoxLayout(self.actions_frame)
            actions_layout.setContentsMargins(28, 2, 10, 2)
            actions_layout.setSpacing(5)
            
            # Create action buttons
            self.generate_btn = QPushButton("Generate Report")
            self.generate_btn.clicked.connect(lambda checked=False, record=self.item_data: self.generateReport.emit(record))

            self.download_btn = QPushButton("Download OSI")
            self.download_btn.clicked.connect(lambda checked=False, record=self.item_data: self.downloadOsi.emit(record))
            
            self.open_btn = QPushButton("Open Project")
            self.open_btn.clicked.connect(lambda checked=False, record=self.item_data: self.openProject.emit(record))
            
            # Style buttons
            for btn in [self.generate_btn, self.download_btn, self.open_btn]:
                btn.setFixedHeight(25)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ffffff;
                        border-radius: 12px;
                        color: #2d3748;
                        border: 1px solid #cccccc;
                        padding: 4px 5px;
                        font-size: 10px;
                        font-weight: 600;
                    }
                    QPushButton:hover {
                        background-color: #f0f4e3;
                        border-color: #9BC53D;
                    }
                    QPushButton:pressed {
                        background-color: #d6e6be;
                    }
                """)

            actions_layout.addWidget(self.generate_btn)
            actions_layout.addWidget(self.download_btn)
            actions_layout.addWidget(self.open_btn)
            
            self.actions_frame.setVisible(False)
            main_layout.addWidget(self.actions_frame)
            
            # Smooth animation for minimum height
            self.expand_animation = QPropertyAnimation(self, b"minimumHeight")
            self.expand_animation.setDuration(250)
            self.expand_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.expand_animation.valueChanged.connect(self.update_fixed_height)
    
    def update_fixed_height(self, value):
        """Update fixed height during animation"""
        self.setFixedHeight(int(value))
    
    def enterEvent(self, event):
        if self.item_type == KEY_SEARCH_PROJ and not self.is_expanded:
            self.is_expanded = True
            
            # Show buttons immediately
            self.actions_frame.setVisible(True)
            self.actions_frame.raise_()
            
            # Animate expansion
            self.expand_animation.stop()
            self.expand_animation.setStartValue(self.original_height)
            self.expand_animation.setEndValue(self.expanded_height)
            self.expand_animation.start()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if self.item_type == KEY_SEARCH_PROJ and self.is_expanded:
            self.is_expanded = False
            
            # Hide buttons
            self.actions_frame.setVisible(False)
            
            # Animate collapse
            self.expand_animation.stop()
            self.expand_animation.setStartValue(self.expanded_height)
            self.expand_animation.setEndValue(self.original_height)
            self.expand_animation.start()
        
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.item_type == KEY_SEARCH_MODULE:
            self.openModule.emit(self.item_data.get(MODULE_KEY))
        return super().mousePressEvent(event)


class SearchOverlay(QFrame):
    """Overlay widget that displays search results"""
    openModule = Signal(str)
    openProject = Signal(dict)
    generateReport = Signal(dict)
    downloadOsi = Signal(dict)
    closeRequested = Signal()  # New signal to request closing
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Use ToolTip instead of Popup - it doesn't steal focus
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self.border_radius = 12
        self.max_height = 400  # Maximum height for the overlay
        self.setObjectName("overlayFrame")
        self.search_widget = None  # Reference to the search bar widget
        
        self.setStyleSheet("""
            #overlayFrame {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 15px;
            }
            #projectsHeader {
                color: #2d3748;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 12px;
                background-color: #f7fafc;
                border-bottom: 1px solid #e2e8f0;
            }
            #modulesHeader {
                color: #2d3748;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 12px;
                background-color: #f7fafc;
                border-top: 1px solid #e2e8f0;
                border-bottom: 1px solid #e2e8f0;
            }
            
            #noResults {
                color: #718096;
                font-size: 13px;
                padding: 24px;
            }
            QScrollArea {
                border: none;
                background: transparent;
                border-radius: 12px;
                margin: 3px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f7fafc;
                width: 3px;
                margin-top: 8px;
                margin-bottom: 8px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e0;
                border-radius: 2px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0aec0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        self.setupUI()
        
        # Install event filter on application to detect clicks outside
        QApplication.instance().installEventFilter(self)
    
    def set_search_widget(self, widget):
        """Set the search bar widget reference"""
        self.search_widget = widget
    
    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area for results
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(3)
        
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
    
    def eventFilter(self, obj, event):
        """Filter events to detect clicks outside the overlay and window focus changes"""
        if self.isVisible():
            # Handle mouse clicks outside overlay
            if event.type() == QEvent.Type.MouseButtonPress:
                # Get the global position of the click
                click_pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
                
                # Check if click is outside both overlay and search widget
                if not self.geometry().contains(self.mapFromGlobal(click_pos)):
                    # Also check if click is outside search widget
                    if self.search_widget:
                        search_rect = self.search_widget.rect()
                        search_local_pos = self.search_widget.mapFromGlobal(click_pos)
                        if not search_rect.contains(search_local_pos):
                            self.hide()
                            self.closeRequested.emit()
                    else:
                        self.hide()
                        self.closeRequested.emit()
            
            # Handle window deactivation (Alt+Tab, focus loss)
            elif event.type() == QEvent.Type.WindowDeactivate:
                self.hide()
                self.closeRequested.emit()
            
            # Handle application state changes (minimize, focus loss)
            elif event.type() == QEvent.Type.ApplicationStateChange:
                self.hide()
                self.closeRequested.emit()
        
        return super().eventFilter(obj, event)
    
    def showEvent(self, event):
        """Apply clipping mask when widget is shown"""
        super().showEvent(event)
        self.apply_rounded_mask()
    
    def resizeEvent(self, event):
        """Reapply mask when widget is resized"""
        super().resizeEvent(event)
        self.apply_rounded_mask()
    
    def apply_rounded_mask(self):
        """Apply a rounded rectangle mask to clip content at borders"""
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 
                           self.border_radius, self.border_radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
    
    def adjust_size_to_content(self):
        """Adjust the overlay size to fit content, up to maximum"""
        # Get the content widget's size hint
        content_height = self.content_widget.sizeHint().height()
        
        # Add some padding for margins
        total_height = min(content_height + 6, self.max_height)
        
        # Set the height (width will be set by position_below_widget)
        if total_height > 0:
            self.setFixedHeight(total_height)
        else:
            self.setFixedHeight(80)  # Minimum height for "No results"
    
    def show_results(self, search_data):
        """Display search results"""
        # Clear existing content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        projects = search_data.get(KEY_SEARCH_PROJ)
        modules = search_data.get(KEY_SEARCH_MODULE)
        
        # Show no results message if empty
        if not projects and not modules:
            no_results = QLabel("No results found")
            no_results.setObjectName("noResults")
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout.addWidget(no_results)
            # Adjust size after adding content
            QTimer.singleShot(0, self.adjust_size_to_content)
            return
        
        # Add Projects section
        if projects:
            projects_header = QLabel("Projects")
            projects_header.setObjectName("projectsHeader")
            self.content_layout.addWidget(projects_header)
            
            for proj in projects:
                result_item = SearchResultItem(proj, KEY_SEARCH_PROJ)
                result_item.openProject.connect(self._handle_open_project)
                result_item.generateReport.connect(self._handle_generate_report)
                result_item.downloadOsi.connect(self._handle_download_osi)
                self.content_layout.addWidget(result_item)
        
        # Add Modules section
        if modules:
            modules_header = QLabel("Modules")
            modules_header.setObjectName("modulesHeader")
            self.content_layout.addWidget(modules_header)
            
            for mod in modules:
                result_item = SearchResultItem(mod, KEY_SEARCH_MODULE)
                result_item.openModule.connect(self._handle_open_module)
                self.content_layout.addWidget(result_item)
        
        self.content_layout.addStretch()
        
        # Adjust size after adding all content
        QTimer.singleShot(0, self.adjust_size_to_content)
    
    def _handle_open_project(self, record):
        """Handle open project and close overlay"""
        self.openProject.emit(record)
        self.hide()
    
    def _handle_generate_report(self, record):
        """Handle generate report and close overlay"""
        self.generateReport.emit(record)
        self.hide()
    
    def _handle_download_osi(self, record):
        """Handle download OSI and close overlay"""
        self.downloadOsi.emit(record)
        self.hide()
    
    def _handle_open_module(self, module_key):
        """Handle open module and close overlay"""
        self.openModule.emit(module_key)
        self.hide()
    
    def position_below_widget(self, target_widget):
        """Position the overlay below the target widget"""
        global_pos = target_widget.mapToGlobal(QPoint(0, target_widget.height() + 4))
        self.move(global_pos)
        self.setFixedWidth(target_widget.width())
    
    def closeEvent(self, event):
        """Clean up event filter when closing"""
        QApplication.instance().removeEventFilter(self)
        super().closeEvent(event)