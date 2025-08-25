from PySide6.QtWidgets import (QPushButton, QLabel, QMessageBox, QDialog,
                               QListWidget, QListWidgetItem, QAbstractItemView, QApplication)
from PySide6.QtCore import (QRect, QMetaObject, QCoreApplication, QSize)
from PySide6.QtGui import Qt, QGuiApplication

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


class Ui_Popup(object):
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
        """Setup the UI with dynamic sizing."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.window_width, self.window_height)
        
        self.disabled_values = disabled_values
        self.note = note

        # Setup labels
        self._setup_labels(MainWindow)
        
        # Setup list widgets
        self._setup_list_widgets(MainWindow)
        
        # Setup buttons
        self._setup_buttons(MainWindow)
        
        # Setup note label if needed
        if self.note:
            self._setup_note_label(MainWindow)
        
        # Setup connections and finalize
        self.connections(MainWindow)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.update_buttons_status()

    def _setup_labels(self, MainWindow):
        """Setup the labels with dynamic positioning."""
        # Common label style
        label_style = '''
            QLabel {
                font-weight: bold;
                font-size: 12px;
                color: #333333;
                padding: 2px;
            }
        '''
        
        # Available label
        self.label = QLabel(MainWindow)
        self.label.setGeometry(QRect(self.margin, self.margin, 150, 30))
        self.label.setObjectName("label")
        self.label.setStyleSheet(label_style)
        
        # Selected label
        self.label_2 = QLabel(MainWindow)
        label2_x = self.margin + self.list_width + self.spacing + self.button_width + self.spacing
        self.label_2.setGeometry(QRect(label2_x, self.margin, 150, 30))
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(label_style)

    def _setup_list_widgets(self, MainWindow):
        """Setup the list widgets with dynamic positioning."""
        # List widget style with custom selection color
        list_style = '''
            QListWidget {
                background-color: white;
            }
            QListWidget::item {
                border-left: 2px solid transparent;
                background-color: transparent;
            }
            QListWidget::item:hover {
                border-left-color: #90af13;
            }
            QListWidget::item:selected {
                background-color: #f9f9f9;
                color: black;
                border-left: 2px solid #90AF13;
            }
            QListWidget::item:selected:hover {
                border-left-color: #000000;
            }
        '''
        
        # Available list widget
        self.listWidget = My_ListWidget(MainWindow)
        list_y = self.margin + 30 + self.margin  # Below label
        self.listWidget.setGeometry(QRect(self.margin, list_y, self.list_width, self.list_height))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSortingEnabled(True)
        self.listWidget.setFocusPolicy(Qt.NoFocus)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget.itemDoubleClicked.connect(self.move_to_selected)
        self.listWidget.setStyleSheet(list_style)
        
        # Selected list widget
        self.listWidget_2 = My_ListWidget(MainWindow)
        list2_x = self.margin + self.list_width + self.spacing + self.button_width + self.spacing
        self.listWidget_2.setGeometry(QRect(list2_x, list_y, self.list_width, self.list_height))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setSortingEnabled(True)
        self.listWidget_2.setFocusPolicy(Qt.NoFocus)
        self.listWidget_2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_2.itemDoubleClicked.connect(self.move_to_available)
        self.listWidget_2.setStyleSheet(list_style)

    def _setup_buttons(self, MainWindow):
        """Setup the control buttons with dynamic positioning."""
        button_x = self.margin + self.list_width + self.spacing
        button_center_y = self.margin + 30 + self.margin + (self.list_height // 2)
        
        # Common button style
        button_style = '''
            QPushButton {
                background-color: #90AF13;
                border-radius: 5px;
                border: 1px solid #90AF13;
                padding: 3px;
                margin: 2px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a9a0f;
            }
            QPushButton:pressed {
                background-color: #5a7a0a;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border: 1px solid #cccccc;
                color: #666666;
            }
        '''
        
        # Move all button (>>)
        self.pushButton = QPushButton(MainWindow)
        self.pushButton.setGeometry(QRect(button_x, button_center_y - 2*self.button_height - self.spacing//2, 
                                        self.button_width, self.button_height))
        self.pushButton.setStyleSheet(button_style)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setAutoDefault(False)
        
        # Move one button (>)
        self.pushButton_2 = QPushButton(MainWindow)
        self.pushButton_2.setGeometry(QRect(button_x, button_center_y - self.button_height, 
                                          self.button_width, self.button_height))
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setAutoDefault(False)
        
        # Move one back button (<)
        self.pushButton_3 = QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QRect(button_x, button_center_y, 
                                          self.button_width, self.button_height))
        self.pushButton_3.setStyleSheet(button_style)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setAutoDefault(False)
        
        # Move all back button (<<)
        self.pushButton_4 = QPushButton(MainWindow)
        self.pushButton_4.setGeometry(QRect(button_x, button_center_y + self.button_height + self.spacing//2, 
                                          self.button_width, self.button_height))
        self.pushButton_4.setStyleSheet(button_style)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setAutoDefault(False)
        
        # Submit button
        self.pushButton_5 = QPushButton(MainWindow)
        submit_width = int(self.window_width * 0.26)  # 26% of window width
        submit_height = int(self.window_height * 0.09)  # 8% of window height
        submit_x = (self.window_width - submit_width) // 2  # Center horizontally
        submit_y = self.window_height - submit_height - self.margin
        self.pushButton_5.setGeometry(QRect(submit_x, submit_y, submit_width, submit_height))
        self.pushButton_5.setStyleSheet(button_style)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setDefault(True)

    def _setup_note_label(self, MainWindow):
        """Setup the note label if a note is provided."""
        self.note_label = QLabel(MainWindow)
        note_width = self.window_width - 2 * self.margin
        note_height = int(self.window_height * 0.15)  # 15% of window height
        note_y = self.window_height - note_height - self.margin - int(self.window_height * 0.09) - self.margin
        self.note_label.setGeometry(QRect(self.margin, note_y, note_width, note_height))
        self.note_label.setObjectName("note_label")
        self.note_label.setText("<b>Note</b>: " + self.note)
        self.note_label.setStyleSheet("""
            QLabel {
                background-color: white; 
                border: 1px solid #cccccc; 
                border-radius: 5px;
                padding: 10px;
                color: #333333;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        self.note_label.setWordWrap(True)
        self.note_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.note_label.resize(QSize(self.note_label.sizeHint()))
        
        # Adjust window height to accommodate note
        MainWindow.resize(self.window_width, self.window_height + note_height + self.margin)

    def retranslateUi(self, Form):
        """Set the text for all UI elements."""
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "Customized"))
        self.label.setText(_translate("MainWindow", "Available:"))
        self.label_2.setText(_translate("MainWindow", "Selected:"))
        self.pushButton.setText(_translate("MainWindow", ">>"))
        self.pushButton_2.setText(_translate("MainWindow", ">"))
        self.pushButton_3.setText(_translate("MainWindow", "<"))
        self.pushButton_4.setText(_translate("MainWindow", "<<"))
        self.pushButton_5.setText(_translate("MainWindow", "Submit"))

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
            self.error_message = QMessageBox()
            self.error_message.setWindowTitle('Information')
            self.error_message.setIcon(QMessageBox.Critical)
            self.error_message.setText('Please Select some values.')
            self.error_message.exec()
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
            self.listWidget.addItem(self.listWidget_2.takeItem(0))

    def on_mButtonToSelected_clicked(self):
        """Move all items from available to selected list."""
        while self.listWidget.count() > 0:
            self.listWidget_2.addItem(self.listWidget.takeItem(0))

    def addAvailableItems(self, items, KEY_EXISTINGVAL_CUSTOMIZED):
        """Add items to the available list with proper handling of disabled values."""
        self.listWidget_2.clear()
        
        if items not in KEY_EXISTINGVAL_CUSTOMIZED:
            # Add existing customized values to selected list
            for item in KEY_EXISTINGVAL_CUSTOMIZED:
                if item in self.disabled_values:
                    continue
                self.listWidget_2.addItem(item)

            # Add remaining items to available list
            remaining_items = list(set(items) - set(KEY_EXISTINGVAL_CUSTOMIZED))
            for item in list(set(remaining_items + self.disabled_values)):
                self.listWidget.addItem(item)
        else:
            # Add all items to selected list
            for item in items:
                self.listWidget_2.addItem(item)

        # Disable items that are in disabled_values
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.text() in self.disabled_values:
                item.setFlags(Qt.NoItemFlags)

    def get_right_elements(self):
        """Get the selected elements from the right list."""
        return [self.listWidget_2.item(i).text() for i in range(self.listWidget_2.count())]

    def move_to_selected(self, item):
        """Move item to selected list on double click."""
        self.listWidget_2.addItem(item.text())
        self.listWidget.takeItem(self.listWidget.row(item))

    def move_to_available(self, item):
        """Move item to available list on double click."""
        self.listWidget.addItem(item.text())
        self.listWidget_2.takeItem(self.listWidget_2.row(item))

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     MainWindow = QDialog()
#     ui = Ui_Popup()
#     ui.setupUi(MainWindow, [], "This is a test note to demonstrate the popup functionality.")
    
#     # Add some sample data to test the functionality
#     sample_items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7", "Item 8"]
#     ui.addAvailableItems(sample_items, [])
    
#     MainWindow.show()
#     sys.exit(app.exec())