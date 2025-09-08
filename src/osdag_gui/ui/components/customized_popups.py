from PySide6.QtWidgets import (QPushButton, QLabel, QMessageBox, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QTextEdit, QFrame, QDialogButtonBox,QFileDialog,
                               QListWidget, QListWidgetItem, QAbstractItemView, QApplication, QSizePolicy, QFormLayout, QLayout, QProgressBar)
from PySide6.QtCore import (QRect, QMetaObject, QCoreApplication, QSize, QThread, Signal)
from PySide6.QtGui import Qt, QGuiApplication, QCursor
import time,os

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

class DummyThread(QThread):
    finished = Signal()

    def __init__(self, sec, parent):
        self.sec = sec
        super().__init__(parent=parent)

    def run(self):
        time.sleep(self.sec)
        self.finished.emit()

# Dialog to capture company details before save design report
class Ui_Dialog1(object):

    def __init__(self, design_exist, loggermsg):
        self.design_exist = design_exist
        self.loggermsg = loggermsg

    def setupUi(self, Dialog, main, module_window):
        self.Dialog = Dialog
        self.module_window = module_window
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(int(600), int(550))
        self.Dialog.setInputMethodHints(Qt.ImhNone)
        self.gridLayout = QGridLayout(self.Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_companyName = QLabel(self.Dialog)
        self.lbl_companyName.setObjectName("lbl_companyName")
        self.gridLayout.addWidget(self.lbl_companyName, 0, 0, 1, 1)
        self.lineEdit_companyName = QLineEdit(self.Dialog)
        self.lineEdit_companyName.setCursor(QCursor(Qt.ArrowCursor))
        self.lineEdit_companyName.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_companyName.setObjectName("lineEdit_companyName")
        self.gridLayout.addWidget(self.lineEdit_companyName, 0, 1, 1, 1)
        self.lbl_comapnyLogo = QLabel(self.Dialog)
        self.lbl_comapnyLogo.setObjectName("lbl_comapnyLogo")
        self.gridLayout.addWidget(self.lbl_comapnyLogo, 1, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_browse = QPushButton(self.Dialog)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_browse.sizePolicy().hasHeightForWidth())
        self.btn_browse.setSizePolicy(sizePolicy)
        self.btn_browse.setFocusPolicy(Qt.TabFocus)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.lbl_browse = QLabel(self.Dialog)
        self.lbl_browse.setMouseTracking(True)
        self.lbl_browse.setAcceptDrops(True)
        self.lbl_browse.setText("")
        self.lbl_browse.setObjectName("lbl_browse")
        self.horizontalLayout.addWidget(self.lbl_browse)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.lbl_groupName = QLabel(self.Dialog)
        self.lbl_groupName.setObjectName("lbl_groupName")
        self.gridLayout.addWidget(self.lbl_groupName, 2, 0, 1, 1)
        self.lineEdit_groupName = QLineEdit(self.Dialog)
        self.lineEdit_groupName.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_groupName.setCursorPosition(0)
        self.lineEdit_groupName.setObjectName("lineEdit_groupName")
        self.gridLayout.addWidget(self.lineEdit_groupName, 2, 1, 1, 1)
        self.lbl_designer = QLabel(self.Dialog)
        self.lbl_designer.setObjectName("lbl_designer")
        self.gridLayout.addWidget(self.lbl_designer, 3, 0, 1, 1)
        self.lineEdit_designer = QLineEdit(self.Dialog)
        self.lineEdit_designer.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_designer.setObjectName("lineEdit_designer")
        self.gridLayout.addWidget(self.lineEdit_designer, 3, 1, 1, 1)
        self.formLayout = QFormLayout()
        self.formLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.formLayout.setObjectName("formLayout")
        self.btn_useProfile = QPushButton(self.Dialog)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_useProfile.sizePolicy().hasHeightForWidth())
        self.btn_useProfile.setSizePolicy(sizePolicy)
        self.btn_useProfile.setFocusPolicy(Qt.TabFocus)
        self.btn_useProfile.setObjectName("btn_useProfile")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.btn_useProfile)
        self.btn_saveProfile = QPushButton(self.Dialog)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_saveProfile.sizePolicy().hasHeightForWidth())
        self.btn_saveProfile.setSizePolicy(sizePolicy)
        self.btn_saveProfile.setFocusPolicy(Qt.TabFocus)
        self.btn_saveProfile.setObjectName("btn_saveProfile")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.btn_saveProfile)
        self.gridLayout.addLayout(self.formLayout, 4, 1, 1, 1)
        self.lbl_projectTitle = QLabel(self.Dialog)
        self.lbl_projectTitle.setObjectName("lbl_projectTitle")
        self.gridLayout.addWidget(self.lbl_projectTitle, 5, 0, 1, 1)
        self.lineEdit_projectTitle = QLineEdit(self.Dialog)
        self.lineEdit_projectTitle.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_projectTitle.setObjectName("lineEdit_projectTitle")
        self.gridLayout.addWidget(self.lineEdit_projectTitle, 5, 1, 1, 1)
        self.lbl_subtitle = QLabel(self.Dialog)
        self.lbl_subtitle.setObjectName("lbl_subtitle")
        self.gridLayout.addWidget(self.lbl_subtitle, 6, 0, 1, 1)
        self.lineEdit_subtitle = QLineEdit(self.Dialog)
        self.lineEdit_subtitle.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_subtitle.setText("")
        self.lineEdit_subtitle.setObjectName("lineEdit_subtitle")
        self.gridLayout.addWidget(self.lineEdit_subtitle, 6, 1, 1, 1)
        self.lbl_jobNumber = QLabel(self.Dialog)
        self.lbl_jobNumber.setObjectName("lbl_jobNumber")
        self.gridLayout.addWidget(self.lbl_jobNumber, 7, 0, 1, 1)
        self.lineEdit_jobNumber = QLineEdit(self.Dialog)
        self.lineEdit_jobNumber.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_jobNumber.setObjectName("lineEdit_jobNumber")
        self.gridLayout.addWidget(self.lineEdit_jobNumber, 7, 1, 1, 1)
        self.lbl_client = QLabel(self.Dialog)
        self.lbl_client.setObjectName("lbl_client")
        self.gridLayout.addWidget(self.lbl_client, 8, 0, 1, 1)
        self.lineEdit_client = QLineEdit(self.Dialog)
        self.lineEdit_client.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit_client.setObjectName("lineEdit_client")
        self.gridLayout.addWidget(self.lineEdit_client, 8, 1, 1, 1)
        self.lbl_addComment = QLabel(self.Dialog)
        self.lbl_addComment.setObjectName("lbl_addComment")
        self.gridLayout.addWidget(self.lbl_addComment, 9, 0, 1, 1)
        self.txt_additionalComments = QTextEdit(self.Dialog)
        self.txt_additionalComments.setFocusPolicy(Qt.StrongFocus)
        self.txt_additionalComments.setStyleSheet("  QTextCursor textCursor;\n"
                                                  "  textCursor.setPosistion(0, QTextCursor::MoveAnchor); \n"
                                                  "  textedit->setTextCursor( textCursor );")
        self.txt_additionalComments.setInputMethodHints(Qt.ImhNone)
        self.txt_additionalComments.setFrameShape(QFrame.WinPanel)
        self.txt_additionalComments.setFrameShadow(QFrame.Sunken)
        self.txt_additionalComments.setTabChangesFocus(False)
        self.txt_additionalComments.setReadOnly(False)
        self.txt_additionalComments.setObjectName("txt_additionalComments")
        self.gridLayout.addWidget(self.txt_additionalComments, 9, 1, 1, 1)
        self.buttonBox = QDialogButtonBox(self.Dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 10, 1, 1, 1)

        self.retranslateUi()

        # self.buttonBox.accepted.connect(self.Dialog.accept)
        self.buttonBox.accepted.connect(lambda: self.save_inputSummary(main))
        self.buttonBox.rejected.connect(self.Dialog.reject)
        self.btn_browse.clicked.connect(self.lbl_browse.clear)
        QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.setTabOrder(self.lineEdit_companyName, self.btn_browse)
        self.Dialog.setTabOrder(self.btn_browse, self.lineEdit_groupName)
        self.Dialog.setTabOrder(self.lineEdit_groupName, self.lineEdit_designer)
        self.Dialog.setTabOrder(self.lineEdit_designer, self.btn_useProfile)
        self.Dialog.setTabOrder(self.btn_useProfile, self.btn_saveProfile)
        self.Dialog.setTabOrder(self.btn_saveProfile, self.lineEdit_projectTitle)
        self.Dialog.setTabOrder(self.lineEdit_projectTitle, self.lineEdit_subtitle)
        self.Dialog.setTabOrder(self.lineEdit_subtitle, self.lineEdit_jobNumber)
        self.Dialog.setTabOrder(self.lineEdit_jobNumber, self.lineEdit_client)
        self.Dialog.setTabOrder(self.lineEdit_client, self.txt_additionalComments)
        self.Dialog.setTabOrder(self.txt_additionalComments, self.buttonBox)

    def save_inputSummary(self, main):
        input_summary = self.getPopUpInputs()  # getting all inputs entered by user in PopUp dialog box.
        file_type = "PDF (*.pdf)"
        # filename, _ = QFileDialog.getSaveFileName(QFileDialog(), "Save File As", os.path.join(str(' '), "untitled.pdf"),
        #                                           file_type)
        filename, _ = QFileDialog.getSaveFileName(self.Dialog, "Save File As", '', file_type, None, QFileDialog.DontUseNativeDialog)
        # filename, _ = QFileDialog.getSaveFileName(self.Dialog, "Save File As", '', file_type)
        '''
        Uncomment the third QFileDialog function if you want to use NativeDialog which will be both system and OS dependent hence
        it would be impossible to assign any modal to QFileDialog once it's opened, therefore it'll look like system is hanged.
        But if you want to control the behaviour of QFileDialog according to your need then use the second function(QFileDialog provided by Qt which is faster than NativeDialog).

        Same is the case when we'll select 'Load Input' option. We can't control the behaviour of QFileDialog because it's native and hence
        OS and system dependent.
        '''

        if filename == '':
            return
        # else:
        #     self.create_pdf_file(filename,main, input_summary)
        #     self.pdf_file_message(filename)

        loading_widget = QDialog(self.module_window)
        window_width = self.module_window.width() // 2
        window_height = self.module_window.height() // 10
        loading_widget.setFixedSize(window_width, int(1.5 * window_height))
        loading_widget.setWindowFlag(Qt.FramelessWindowHint)

        self.progress_bar = QProgressBar(loading_widget)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setGeometry(QRect(0, 0, window_width, window_height // 2))
        loading_label = QLabel(loading_widget)
        loading_label.setGeometry(QRect(0, window_height // 2, window_width, window_height))
        loading_label.setFixedSize(window_width, window_height)
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setText("<p style='font-weight:500'>Please Wait...</p>")
        self.thread_1 = DummyThread(0.00001, self.module_window)
        self.thread_1.start()
        self.thread_2 = DummyThread(0.00001, self.module_window)
        self.thread_1.finished.connect(lambda: loading_widget.exec())
        self.thread_1.finished.connect(lambda: self.progress_bar.setValue(20))
        self.thread_1.finished.connect(lambda: self.thread_2.start())
        self.thread_2.finished.connect(lambda: self.create_pdf_file(filename, main, input_summary))
        self.thread_2.finished.connect(lambda: loading_widget.close())
        self.thread_2.finished.connect(lambda: self.progress_bar.setValue(90))
        self.thread_2.finished.connect(lambda: self.pdf_file_message(filename))

    def create_pdf_file(self, filename, main, input_summary):
        fname_no_ext = filename.split(".")[0]
        input_summary['filename'] = fname_no_ext
        input_summary['does_design_exist'] = self.design_exist
        input_summary['logger_messages'] = self.loggermsg
        # self.progress_bar.setValue(30)
        main.save_design(input_summary)
        # self.progress_bar.setValue(80)

    def pdf_file_message(self, filename):
        """Handle PDF generation completion and display appropriate message"""
        try:
            # **FIX**: Determine the correct UI object reference
            ui_ref = None
            if hasattr(self, 'ui') and self.ui:
                ui_ref = self.ui
            elif hasattr(self, 'lblmessage'):
                ui_ref = self  # self is the UI object directly
            else:
                print("Could not find UI reference")
                return

            # **FIX**: Handle encoding issues when reading log file
            logfile_path = filename + '.log'
            logs = ""
            
            if os.path.exists(logfile_path):
                # Try multiple encoding strategies to handle LaTeX log files
                encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encodings_to_try:
                    try:
                        with open(logfile_path, 'r', encoding=encoding) as logfile:
                            logs = logfile.read()
                        print(f"Successfully read log file with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error reading with {encoding}: {e}")
                        continue
                else:
                    # If all encodings fail, try with error handling
                    try:
                        with open(logfile_path, 'r', encoding='utf-8', errors='ignore') as logfile:
                            logs = logfile.read()
                        print("Read log file with UTF-8 and ignored decode errors")
                    except Exception as e:
                        print(f"Final fallback failed: {e}")
                        logs = "Could not read log file due to encoding issues"
            else:
                logs = "Log file not found"
                print(f"Log file not found: {logfile_path}")

            # Check for LaTeX errors in the log content
            has_latex_error = False
            has_fatal_error = False
            
            if logs:
                # Check for various types of LaTeX errors
                error_indicators = [
                    "LaTeX Error:",
                    "! LaTeX Error:",
                    "Fatal error occurred",
                    "Emergency stop",
                    "! ==> Fatal error occurred",
                    "Runaway argument",
                    "! Undefined control sequence",
                    "! Missing $ inserted",
                    "! File ended while scanning"
                ]
                
                for error in error_indicators:
                    if error in logs:
                        has_latex_error = True
                        if "Fatal" in error or "Emergency stop" in error:
                            has_fatal_error = True
                        break

            # Check if PDF was actually generated regardless of log errors
            pdf_file_path = filename + '.pdf'
            pdf_exists = os.path.exists(pdf_file_path)
            
            # Determine the appropriate message
            if pdf_exists:
                if has_fatal_error:
                    message = "<font color='orange'>PDF generated with warnings. Please check the output.</font>"
                elif has_latex_error:
                    message = "<font color='orange'>PDF generated successfully with some LaTeX warnings.</font>"
                else:
                    message = "<font color='green'>PDF generated successfully.</font>"
            else:
                # PDF not generated
                if has_latex_error or has_fatal_error:
                    message = "<font color='red'>ERROR: LaTeX file processing failed. PDF not generated.</font>"
                else:
                    message = "<font color='red'>ERROR: PDF generation failed for unknown reason.</font>"

            # **FIX**: Set message using the correct UI reference
            if hasattr(ui_ref, 'lblmessage'):
                ui_ref.lblmessage.setText(message)
            elif hasattr(ui_ref, 'label') and hasattr(ui_ref.label, 'setText'):
                ui_ref.label.setText(message)
            else:
                print(f"Message would be: {message}")

            # **FIX**: Enable/disable buttons using correct UI reference
            if pdf_exists:
                # Enable view buttons if they exist
                for btn_name in ['btn_viewPDF', 'pushButton_3', 'pushButton_view']:
                    if hasattr(ui_ref, btn_name):
                        getattr(ui_ref, btn_name).setEnabled(True)
            else:
                # Disable view buttons
                for btn_name in ['btn_viewPDF', 'pushButton_3', 'pushButton_view']:
                    if hasattr(ui_ref, btn_name):
                        getattr(ui_ref, btn_name).setEnabled(False)

            # Update progress bar if it exists
            for progress_name in ['progressBar', 'progress']:
                if hasattr(ui_ref, progress_name):
                    getattr(ui_ref, progress_name).setValue(100)
                    break

            # Enable close buttons
            for btn_name in ['btn_close', 'buttonBox']:
                if hasattr(ui_ref, btn_name):
                    getattr(ui_ref, btn_name).setEnabled(True)

            print(f"PDF exists: {pdf_exists}")
            print(f"Has LaTeX error: {has_latex_error}")
            print(f"Has fatal error: {has_fatal_error}")

        except Exception as e:
            print(f"Error in pdf_file_message: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback message
            pdf_file_path = filename + '.pdf'
            if os.path.exists(pdf_file_path):
                message = "<font color='green'>PDF generated successfully.</font>"
            else:
                message = "<font color='red'>ERROR: Could not determine PDF generation status.</font>"
            
            # Try to set message with fallback approach
            try:
                if hasattr(self, 'lblmessage'):
                    self.lblmessage.setText(message)
                elif hasattr(self, 'ui') and hasattr(self.ui, 'lblmessage'):
                    self.ui.lblmessage.setText(message)
                else:
                    print(f"Fallback message: {message}")
            except:
                print(f"Could not set UI message: {message}")

    def call_designreport(self, main, fileName, report_summary, folder):
        self.alist = main.report_input
        self.column_details = main.report_supporting
        self.beam_details = main.report_supported
        self.result = main.report_result
        self.Design_Check = main.report_check
        # save_html(main.report_result, main.report_input, main.report_check, main.report_supporting,main.report_supported, report_summary,fileName, folder)
        # CreateLatex.\
        #     save_latex(CreateLatex(),main.report_result, main.report_input, main.report_check, main.report_supporting,
        #           main.report_supported, report_summary, fileName, folder)

    def getPopUpInputs(self):
        input_summary = {}
        input_summary["ProfileSummary"] = {}
        input_summary["ProfileSummary"]["CompanyName"] = str(self.lineEdit_companyName.text())
        input_summary["ProfileSummary"]["CompanyLogo"] = str(self.lbl_browse.text())
        input_summary["ProfileSummary"]["Group/TeamName"] = str(self.lineEdit_groupName.text())
        input_summary["ProfileSummary"]["Designer"] = str(self.lineEdit_designer.text())

        input_summary["ProjectTitle"] = str(self.lineEdit_projectTitle.text())
        input_summary["Subtitle"] = str(self.lineEdit_subtitle.text())
        input_summary["JobNumber"] = str(self.lineEdit_jobNumber.text())
        input_summary["AdditionalComments"] = str(self.txt_additionalComments.toPlainText())
        input_summary["Client"] = str(self.lineEdit_client.text())

        return input_summary

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Design Report Summary"))
        self.lbl_companyName.setText(_translate("Dialog", "Company Name :"))
        self.lbl_comapnyLogo.setText(_translate("Dialog", "Company Logo :"))
        self.btn_browse.setText(_translate("Dialog", "Browse..."))
        self.lbl_groupName.setText(_translate("Dialog", "Group/Team Name :"))
        self.lbl_designer.setText(_translate("Dialog", "Designer :"))
        self.btn_useProfile.setText(_translate("Dialog", "Use Profile"))
        self.btn_saveProfile.setText(_translate("Dialog", "Save Profile"))
        self.lbl_projectTitle.setText(_translate("Dialog", "Project Title :"))
        self.lbl_subtitle.setText(_translate("Dialog", "Subtitle :"))
        self.lineEdit_subtitle.setPlaceholderText(_translate("Dialog", "(Optional)"))
        self.lbl_jobNumber.setText(_translate("Dialog", "Job Number :"))
        self.lbl_client.setText(_translate("Dialog", "Client :"))
        self.lbl_addComment.setText(_translate("Dialog", "Additional Comments :"))
        self.txt_additionalComments.setHtml(_translate("Dialog",
                                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                       "p, li { white-space: pre-wrap; }\n"
                                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
                                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:11pt;\"><br /></p></body></html>"))


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