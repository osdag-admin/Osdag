from PySide6.QtWidgets import (QPushButton, QLabel, QMessageBox, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget,
                               QListWidget, QListWidgetItem, QAbstractItemView, QApplication, QSizePolicy)
from PySide6.QtCore import (QRect, QMetaObject, QCoreApplication, QSize, Qt)
from PySide6.QtGui import QGuiApplication
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar

def get_screen_dimensions():
    """
    Get the primary screen dimensions.
    Returns (width, height) tuple.
    """
    try:
        screen = QGuiApplication.primaryScreen()
        if screen:
            screen_size = screen.availableGeometry()
            return screen_size.width(), screen_size.height()
        else:
            desktop = QApplication.desktop()
            if desktop:
                screen_geometry = desktop.screenGeometry()
                return screen_geometry.width(), screen_geometry.height()
    except Exception:
        pass
    
    # Default fallback
    return 1920, 1080

class My_ListWidget(QListWidget):
    """Custom ListWidget with improved item handling."""
    
    def addItems(self, Iterable, p_str=None):
        QListWidget.addItems(self, Iterable)

    def addItem(self, *__args):
        QListWidget.addItem(self, My_ListWidgetItem(__args[0]))


class My_ListWidgetItem(QListWidgetItem):
    """Custom ListWidgetItem with numeric sorting capability."""
    
    def __lt__(self, other):
        try:
            import re
            self_text = str(re.sub("[^0-9]", "", self.text()))
            other_text = str(re.sub("[^0-9]", "", other.text()))
            return float(self_text) < float(other_text)
        except Exception:
            return QListWidgetItem.__lt__(self, other)


class CustomValueSelectPopup(object):
    """Customized popup UI with dynamic sizing based on screen percentage."""
    
    def __init__(self):
        self.screen_width, self.screen_height = get_screen_dimensions()
        
        # Define UI dimensions as percentages of screen size
        self.window_width_pct = 0.28  # 28% of screen width
        self.window_height_pct = 0.44  # 44% of screen height
        
        # Calculate base dimensions
        self.window_width = int(self.screen_width * self.window_width_pct)
        self.window_height = int(self.screen_height * self.window_height_pct)
        
        # Define component dimensions as percentages of window size
        self.list_width_pct = 0.33  # 33% of window width
        self.list_height_pct = 0.64  # 64% of window height
        self.button_width_pct = 0.13  # 13% of window width
        self.button_height_pct = 0.09  # 9% of window height
        
        # Calculate component dimensions
        self.list_width = int(self.window_width * self.list_width_pct)
        self.list_height = int(self.window_height * self.list_height_pct)
        self.button_width = int(self.window_width * self.button_width_pct)
        self.button_height = int(self.window_height * self.button_height_pct)
        
        # Margins and spacing (as percentages)
        self.margin_pct = 0.037  # 3.7% of window size
        self.spacing_pct = 0.074  # 7.4% of window size
        
        self.margin = int(min(self.window_width, self.window_height) * self.margin_pct)
        self.spacing = int(min(self.window_width, self.window_height) * self.spacing_pct)

    def setupUi(self, MainWindow, disabled_values, note):
        """Setup the UI with dynamic sizing and custom title bar."""
        MainWindow.setObjectName("CustomValueSelectPopup")
        MainWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        MainWindow.setAttribute(Qt.WA_StyledBackground, True)
        MainWindow.setModal(True)
        
        self.disabled_values = disabled_values
        self.note = note
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(0)
        
        title_bar = CustomTitleBar(parent=MainWindow)
        title_bar.setTitle('Select Values')
        main_layout.addWidget(title_bar)
        
        # Content widget
        content_widget = QWidget()
        content_widget.setObjectName("content_widget")
        self.setupContent(content_widget, MainWindow)
        main_layout.addWidget(content_widget)
        
        # Apply dialog styles
        MainWindow.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #c0c0c0;
            }
            QWidget#content_widget {
                background-color: #ffffff;
            }
        """)
        
        MainWindow.setLayout(main_layout)
        MainWindow.resize(self.window_width, self.window_height + 30)  # Add height for title bar
        
        # Center the dialog
        self.centerDialog(MainWindow)
        
        QMetaObject.connectSlotsByName(MainWindow)

    def setupContent(self, content_widget, MainWindow):
        """Setup the main content area."""
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        
        # Labels container
        labels_layout = QHBoxLayout()
        
        # Available label
        self.label = QLabel("Available:")
        self.label.setObjectName("label")
        self.label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 13px;
                color: #333333;
                padding: 2px;
            }
        """)
        labels_layout.addWidget(self.label)
        labels_layout.addStretch()
        
        # Selected label
        self.label_2 = QLabel("Selected:")
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 13px;
                color: #333333;
                padding: 2px;
            }
        """)
        labels_layout.addWidget(self.label_2)
        
        content_layout.addLayout(labels_layout)
        
        # Lists and buttons container
        lists_layout = QHBoxLayout()
        lists_layout.setSpacing(self.spacing // 2)
        
        # Available list
        self.listWidget = My_ListWidget()
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setFocusPolicy(Qt.NoFocus)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.itemDoubleClicked.connect(self.move_to_selected)
        self.listWidget.setStyleSheet(self.get_list_style())
        self.listWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lists_layout.addWidget(self.listWidget)
        
        # Buttons container
        buttons_widget = QWidget()
        buttons_widget.setFixedWidth(self.button_width)
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        # Move all button (>>)
        self.pushButton = QPushButton(">>")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFixedHeight(self.button_height)
        self.pushButton.setStyleSheet(self.get_button_style())
        buttons_layout.addWidget(self.pushButton)
        
        # Move one button (>)
        self.pushButton_2 = QPushButton(">")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setFixedHeight(self.button_height)
        self.pushButton_2.setStyleSheet(self.get_button_style())
        buttons_layout.addWidget(self.pushButton_2)
        
        # Move one back button (<)
        self.pushButton_3 = QPushButton("<")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFixedHeight(self.button_height)
        self.pushButton_3.setStyleSheet(self.get_button_style())
        buttons_layout.addWidget(self.pushButton_3)
        
        # Move all back button (<<)
        self.pushButton_4 = QPushButton("<<")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setFixedHeight(self.button_height)
        self.pushButton_4.setStyleSheet(self.get_button_style())
        buttons_layout.addWidget(self.pushButton_4)
        
        buttons_layout.addStretch()
        lists_layout.addWidget(buttons_widget)
        
        # Selected list
        self.listWidget_2 = My_ListWidget()
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setSortingEnabled(True)
        self.listWidget_2.setFocusPolicy(Qt.NoFocus)
        self.listWidget_2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_2.itemDoubleClicked.connect(self.move_to_available)
        self.listWidget_2.setStyleSheet(self.get_list_style())
        self.listWidget_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lists_layout.addWidget(self.listWidget_2)
        
        content_layout.addLayout(lists_layout)
        
        # Note label if needed
        if self.note:
            self.note_label = QLabel("<b>Note:</b> " + self.note)
            self.note_label.setObjectName("note_label")
            self.note_label.setStyleSheet("""
                QLabel {
                    background-color: #f9f9f9;
                    border: 1px solid #e0e0e0;
                    border-radius: 5px;
                    padding: 10px;
                    color: #555555;
                    font-size: 12px;
                }
            """)
            self.note_label.setWordWrap(True)
            self.note_label.setMaximumHeight(80)
            content_layout.addWidget(self.note_label)
        
        # Submit button container
        submit_layout = QHBoxLayout()
        submit_layout.setContentsMargins(0, 10, 0, 0)
        submit_layout.addStretch()
        
        self.pushButton_5 = QPushButton("Submit")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setDefault(True)
        self.pushButton_5.setFixedSize(120, 35)
        self.pushButton_5.setStyleSheet("""
            QPushButton {
                background-color: #90AF13;
                color: white;
                font-weight: bold;
                font-size: 13px;
                border-radius: 5px;
                border: none;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #7a9a12;
            }
            QPushButton:pressed {
                background-color: #5f7a0e;
            }
        """)
        submit_layout.addWidget(self.pushButton_5)
        submit_layout.addStretch()
        
        content_layout.addLayout(submit_layout)
        
        # Setup connections
        self.connections(MainWindow)
        self.update_buttons_status()

    def get_list_style(self):
        """Return the style for list widgets."""
        return """
            QListWidget {
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                border-left: 2px solid transparent;
                background-color: transparent;
                padding: 3px;
                margin: 1px;
            }
            QListWidget::item:hover {
                background-color: #f0f7d0;
                border-left-color: #90af13;
            }
            QListWidget::item:selected {
                background-color: #e8f4c8;
                color: black;
                border-left: 2px solid #90AF13;
            }
            QListWidget::item:selected:hover {
                background-color: #d8e4b8;
                border-left-color: #7a9a12;
            }
            QListWidget::item:disabled {
                color: #999999;
                background-color: #f5f5f5;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #90AF13;
            }
        """

    def get_button_style(self):
        """Return the style for control buttons."""
        return """
            QPushButton {
                background-color: #90AF13;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7a9a12;
            }
            QPushButton:pressed {
                background-color: #5f7a0e;
            }
            QPushButton:disabled {
                background-color: #d0d0d0;
                color: #888888;
            }
        """

    def centerDialog(self, dialog):
        """Center the dialog on the screen or parent window."""
        if dialog.parent():
            parent_geometry = dialog.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - dialog.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - dialog.height()) // 2
        else:
            screen_geometry = QGuiApplication.primaryScreen().geometry()
            x = (screen_geometry.width() - dialog.width()) // 2
            y = (screen_geometry.height() - dialog.height()) // 2
        dialog.move(x, y)

    def connections(self, MainWindow):
        """Setup signal connections."""
        self.listWidget.itemSelectionChanged.connect(self.update_buttons_status)
        self.listWidget_2.itemSelectionChanged.connect(self.update_buttons_status)
        self.pushButton_2.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.pushButton_3.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.pushButton_4.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.pushButton.clicked.connect(self.on_mButtonToSelected_clicked)
        self.pushButton_5.clicked.connect(self.get_right_elements)
        self.pushButton_5.clicked.connect(lambda: self.is_empty(MainWindow))

    def is_empty(self, MainWindow):
        """Check whether values are selected or not."""
        if len(self.get_right_elements()) == 0:
            error_message = QMessageBox(MainWindow)
            error_message.setWindowTitle('Information')
            error_message.setIcon(QMessageBox.Critical)
            error_message.setText('Please select some values.')
            error_message.exec()
        else:
            MainWindow.close()

    def update_buttons_status(self):
        """Update button enabled/disabled states based on selection."""
        self.pushButton_2.setDisabled(not bool(self.listWidget.selectedItems()))
        self.pushButton_3.setDisabled(not bool(self.listWidget_2.selectedItems()))

    def on_mBtnMoveToAvailable_clicked(self):
        """Move selected items from available to selected list."""
        items = self.listWidget.selectedItems()
        for item in items:
            self.listWidget_2.addItem(item.text())
        for item in items:
            self.listWidget.takeItem(self.listWidget.row(item))

    def on_mBtnMoveToSelected_clicked(self):
        """Move selected items from selected to available list."""
        items = self.listWidget_2.selectedItems()
        for item in items:
            self.listWidget.addItem(item.text())
        for item in items:
            self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def on_mButtonToAvailable_clicked(self):
        """Move all items from selected to available list."""
        while self.listWidget_2.count() > 0:
            self.listWidget.addItem(self.listWidget_2.takeItem(0).text())

    def on_mButtonToSelected_clicked(self):
        """Move all items from available to selected list."""
        while self.listWidget.count() > 0:
            item = self.listWidget.takeItem(0)
            if item.flags() != Qt.NoItemFlags:  # Only move enabled items
                self.listWidget_2.addItem(item.text())
            else:
                self.listWidget.addItem(item.text())  # Put disabled items back

    def addAvailableItems(self, items, KEY_EXISTINGVAL_CUSTOMIZED):
        """Add items to the available list with proper handling of disabled values."""
        self.listWidget.clear()
        self.listWidget_2.clear()
        
        # Add existing customized values to selected list
        for item in KEY_EXISTINGVAL_CUSTOMIZED:
            if item not in self.disabled_values:
                self.listWidget_2.addItem(item)
        
        # Add remaining items to available list
        remaining_items = list(set(items) - set(KEY_EXISTINGVAL_CUSTOMIZED))
        for item in remaining_items:
            list_item = self.listWidget.addItem(item)
            # Disable items that are in disabled_values
            if item in self.disabled_values:
                items = self.listWidget.findItems(item, Qt.MatchExactly)
                for disabled_item in items:
                    disabled_item.setFlags(Qt.NoItemFlags)

    def get_right_elements(self):
        """Get the selected elements from the right list."""
        return [self.listWidget_2.item(i).text() for i in range(self.listWidget_2.count())]

    def move_to_selected(self, item):
        """Move item to selected list on double click."""
        if item.flags() != Qt.NoItemFlags:  # Only move if not disabled
            self.listWidget_2.addItem(item.text())
            self.listWidget.takeItem(self.listWidget.row(item))

    def move_to_available(self, item):
        """Move item to available list on double click."""
        self.listWidget.addItem(item.text())
        self.listWidget_2.takeItem(self.listWidget_2.row(item))