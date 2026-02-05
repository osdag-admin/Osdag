from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QComboBox, QScrollArea, QLabel, QLineEdit, QSizePolicy, QTabWidget
)
from PySide6.QtWidgets import QDialog, QGridLayout, QTextBrowser, QFrame, QFileDialog
from PySide6.QtCore import Qt, QRegularExpression, Signal, QObject
from PySide6.QtGui import QPixmap, QBrush, QColor, QDoubleValidator, QRegularExpressionValidator, QIcon, QFontMetrics, QTextCursor, QGuiApplication, QTextCharFormat, QCursor

from osdag_core.Common import *
from osdag_core.utils.common.Section_Properties_Calculator import *
from osdag_core.utils.common.component import *
from osdag_core.utils.common.other_standards import *
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType

import os
import sqlite3
import openpyxl

class MyTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName("TableWidget")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def addTab(self, widget, text):
        self.tabs.addTab(widget, text)
        widget.setAutoFillBackground(True)

class Window(QDialog):
    downloadDatabase = Signal(str, str)
    importSection = Signal(str)
    def __init__(self, main, input_dictionary, parent=None):
        super().__init__(parent)
        self.input_dictionary = input_dictionary
        self.do_not_clear_list = []
        self.save_changes_list = []
        self.values_changed = False
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        for t in main.input_dictionary_design_pref():
            self.save_changes_list.extend(t[2])
        
        self.initUI(main, input_dictionary)

    def center(self):
        frameGm = self.frameGeometry()
        # get screen under cursor
        screen = QGuiApplication.screenAt(QCursor.pos())
        if screen is None:
            screen = QGuiApplication.primaryScreen()
        centerPoint = screen.geometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def closeEvent(self, event):
        if self.values_changed:
            result = CustomMessageBox(
                title="Save",
                text=f"Do you want to save the changes?",
                buttons=["Yes", "No", "Cancel"],
                dialogType=MessageBoxType.Information,
            ).exec()
            
            if result == "Yes":
                self.accept()
                event.accept()
            elif result == "No":
                self.reject()
                event.accept()
            else:
                event.ignore()

        else:
            QDialog.closeEvent(self, event)

    def connect_widget_for_change(self, widget):
        if isinstance(widget, QComboBox):
            widget.currentIndexChanged.connect(self.something_changed)
        elif isinstance(widget, QLineEdit):
            widget.textChanged.connect(self.something_changed)

    def something_changed(self):
        self.values_changed = True

    def initUI(self, main, input_dictionary):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("AdditionalInputs")
    
        scale = 1
        button_size_x = int(scale*190)
        button_size_y = int(scale*30)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(1, 1, 1, 5)
        self.main_layout.setSpacing(0)
        # Custom title bar
        self.titleBar = CustomTitleBar()
        self.titleBar.setTitle('Additional Inputs')
        self.main_layout.addWidget(self.titleBar)

        self.tabWidget = MyTableWidget()
        self.main_layout.addWidget(self.tabWidget)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(5)
        self.btn_defaults = QPushButton("Defaults")
        self.btn_save = QPushButton("Save")
        self.btn_defaults.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.btn_save.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.btn_defaults.setFixedSize(button_size_x, button_size_y)
        self.btn_save.setFixedSize(button_size_x, button_size_y)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.btn_defaults)
        self.button_layout.addWidget(self.btn_save)
        self.button_layout.addStretch()

        tab_index = -1
        # print(f"@tab_list()= {main.tab_list()} ")
        for tab_details in main.tab_list():
            last_title = ""
            tab_name = tab_details[0]
            tab_elements = tab_details[2]
            tab_type = tab_details[1]

            scrollArea = QScrollArea()
            scrollArea.setWidgetResizable(True)
            scrollAreaWidgetContents = QWidget()
            scrollArea.setWidget(scrollAreaWidgetContents)

            if tab_type == TYPE_TAB_1:

                tab = QWidget()
                self.tabWidget.addTab(tab, tab_name)
                tab_index +=1
                self.tabWidget.tabs.setTabText(tab_index, tab_name)
                tab.setObjectName(tab_name)

                lay = QVBoxLayout(tab)
                lay.addWidget(scrollArea)


                vertical = QVBoxLayout(scrollAreaWidgetContents)
                horizontalLayout = QHBoxLayout()
                vertical.addLayout(horizontalLayout)

                horizontal = QHBoxLayout()
                lay.addLayout(horizontal)

                buttons = [(str("pushButton_Add_" + tab_name), 'Add'), (str("pushButton_Clear_" + tab_name), 'Clear'),
                            (str("pushButton_Import_" + tab_name), "Import xlsx file"), (str("pushButton_Download_" + tab_name), "Download xlsx file")]

                elements = tab_elements(input_dictionary)
                # print(f"@elements: {elements}")
                for i in range(len(buttons)):
                    object_name = buttons[i][0]
                    btn_text = buttons[i][1]
                    button = QPushButton(tab)
                    button.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                    horizontal.addWidget(button)
                    button.setObjectName(object_name)
                    button.setText(btn_text)
                    button.setFixedSize(button_size_x, button_size_y)
                    if input_dictionary != {}:
                        if main.module_name() == KEY_DISP_BASE_PLATE and input_dictionary[KEY_CONN] == VALUES_CONN_BP[2]:
                            button.setEnabled(False)

                r = 1
                grid = QGridLayout()
                horizontalLayout.addLayout(grid)
                grid.setAlignment(Qt.AlignTop|Qt.AlignLeft)
                grid.setHorizontalSpacing(10)
                grid.setVerticalSpacing(10)
                # print(f"ui_de_pref elements {elements}\n")
                for element in elements:
                    type = element[2]
                    lable = element[1]
                    if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                        label = QLabel(tab)
                        label.setObjectName(element[0] + "_label")
                        label.setText("<html><head/><body><p>" + lable + "</p></body></html>")
                        grid.addWidget(label,r,1)
                        label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))

                    if type ==TYPE_TEXTBOX:
                        line = QLineEdit(tab)
                        grid.addWidget(line,r,2)
                        line.setObjectName(element[0])
                        line.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        line.setFixedSize(120, 20)
                        if lable == 'Designation' or lable == KEY_DISP_SEC_PROFILE:
                            line.textChanged.connect(self.manage_designation_size(line))

                        if input_dictionary:
                            line.setText(str(element[4]))

                        if lable in [KEY_DISP_FU, KEY_DISP_FY, KEY_DISP_POISSON_RATIO, KEY_DISP_THERMAL_EXP,
                                     KEY_DISP_MOD_OF_ELAST, KEY_DISP_MOD_OF_RIGID, 'Source']:
                            line.setReadOnly(True)
                            self.do_not_clear_list.append(line)
                        if main.module_name() in [KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED] and lable in \
                                [KEY_DISP_LOCATION, KEY_DISP_SEC_PROFILE]:
                            line.setReadOnly(True)
                            self.do_not_clear_list.append(line)
                        if last_title == KEY_DISP_DIMENSIONS:
                            if element[1] in [KEY_DISP_ROOT_R, KEY_DISP_TOE_R]:
                                regex_validator = QRegularExpression("[0-9]*[.][0-9]*|[.][0-9]*|0")
                            else:
                                regex_validator = QRegularExpression("[1-9][0-9]*[.][0-9]*|[.][0-9]*")
                            line.setValidator(QRegularExpressionValidator(regex_validator, line))
                        if last_title == KEY_DISP_SEC_PROP:
                            regex_validator = QRegularExpression("[1-9][0-9]*[.][0-9]*|[.][0-9]*|N/A|-")
                            line.setValidator(QRegularExpressionValidator(regex_validator, line))

                        if element[0] in self.save_changes_list:
                            self.connect_widget_for_change(line)

                        r += 1

                    if type == TYPE_COMBOBOX:
                        combo = QComboBox(tab)
                        grid.addWidget(combo,r,2)
                        combo.setMaxVisibleItems(5)
                        combo.setObjectName(element[0])
                        combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                        combo.addItems(element[3])
                        if input_dictionary:
                            combo.setCurrentText(str(element[4]))
                        font = combo.font()
                        metrices = QFontMetrics(font)
                        item_width = 0
                        item_width = max([metrices.boundingRect(item).width() for item in element[3]],default = 0)
                        combo.view().setMinimumWidth(item_width + 30)

                        combo.setStyleSheet("QComboBox { combobox-popup: 0; }")

                        if lable == KEY_DISP_MATERIAL:
                            self.do_not_clear_list.append(combo)

                        combo.setFixedSize(120,20)
                        if element[0] in self.save_changes_list:
                            self.connect_widget_for_change(combo)
                        r += 1

                    if type == TYPE_TITLE:
                        title = QLabel(tab)
                        title.setText(lable)
                        grid.addWidget(title,r,1,1,2)
                        title.setObjectName("_title")
                        title.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        last_title = lable
                        r += 1

                    if type == TYPE_IMAGE:
                        img = QLabel(tab)
                        img.setObjectName(element[0])
                        grid.addWidget(img,r,1,10,2)
                        pmap = QPixmap(element[4])
                        img.setPixmap(pmap.scaled(300,300,Qt.KeepAspectRatio, Qt.FastTransformation)) # you can also use IgnoreAspectRatio
                        r += 10

                    if type == TYPE_BREAK:
                        r = 1
                        grid = QGridLayout()
                        horizontalLayout.addLayout(grid)
                        grid.setAlignment(Qt.AlignTop|Qt.AlignLeft)
                        grid.setHorizontalSpacing(10)
                        grid.setVerticalSpacing(10)
                        continue

            elif tab_type == TYPE_TAB_2:


                tab = QWidget()
                self.tabWidget.addTab(tab, tab_name)
                tab_index +=1
                self.tabWidget.tabs.setTabText(tab_index, tab_name)
                tab.setObjectName(tab_name)

                lay = QVBoxLayout(tab)
                lay.addWidget(scrollArea)


                vertical = QVBoxLayout(scrollAreaWidgetContents)
                horizontalLayout = QHBoxLayout()
                vertical.addLayout(horizontalLayout)


                r = 1
                grid = QGridLayout()
                horizontalLayout.addLayout(grid)
                grid.setHorizontalSpacing(10)
                grid.setVerticalSpacing(10)
                grid.setAlignment(Qt.AlignTop|Qt.AlignLeft)

                label_1 = QLabel(tab)
                label_1.setObjectName("_title")
                label_1.setText("Inputs")
                grid.addWidget(label_1,r,1)


                r += 3

                Notes = []
                elements = tab_elements(input_dictionary)
                for element in elements:
                    type = element[2]
                    lable = element[1]
                    if type in [TYPE_COMBOBOX, TYPE_TEXTBOX]:
                        label = QLabel(tab)
                        label.setText("<html><head/><body><p>" + lable + "</p></body></html>")
                        label.setObjectName(element[0] + "_label")
                        grid.addWidget(label,r,1)
                        label.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))

                    if type == TYPE_TEXTBOX:
                        line = QLineEdit(tab)
                        grid.addWidget(line,r,2)
                        line.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        line.setObjectName(element[0])
                        line.setFixedSize(120, 22)
                        if element[3]:
                            line.setText(element[3])
                        dbl_validator = QDoubleValidator()
                        if element[0] in [KEY_DP_WELD_MATERIAL_G_O]:
                            line.setValidator(dbl_validator)
                            line.setMaxLength(7)
                        if element[0] in [KEY_DP_DETAILING_GAP] and main.module_name() in [KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED]:
                            line.setReadOnly(True)
                            self.do_not_clear_list.append(line)
                        if element[0] in [KEY_BASE_PLATE_FU, KEY_BASE_PLATE_FY, KEY_DP_ANCHOR_BOLT_DESIGNATION_OCF,
                                          KEY_DP_ANCHOR_BOLT_DESIGNATION_ICF, KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_OCF,
                                          KEY_DP_ANCHOR_BOLT_MATERIAL_G_O_ICF, KEY_DP_ANCHOR_BOLT_TYPE_OCF,
                                          KEY_DP_ANCHOR_BOLT_TYPE_ICF]:
                            line.setReadOnly(True)
                        if input_dictionary:
                            line.setText(str(element[4]))

                        if element[0] in self.save_changes_list:
                            self.connect_widget_for_change(line)
                        r += 1

                    if type == TYPE_COMBOBOX:
                        combo = QComboBox(tab)
                        grid.addWidget(combo,r,2)
                        combo.setMaxVisibleItems(5)
                        combo.setObjectName(element[0])
                        combo.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                        combo.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        combo.setStyleSheet("QComboBox { combobox-popup: 0; }")
                        combo.addItems(element[3])
                        font = combo.font()
                        metrices = QFontMetrics(font)
                        item_width = max([metrices.boundingRect(item).width() for item in element[3]],default = 0)
                        combo.view().setMinimumWidth(item_width + 30)
                        combo.setFixedSize(120, 22)
                        if element[0] == KEY_DP_DESIGN_METHOD:
                            combo.model().item(1).setEnabled(False)
                            combo.model().item(2).setEnabled(False)
                        if input_dictionary:
                            combo.setCurrentText(str(element[4]))
                        if element[0] in self.save_changes_list:
                            self.connect_widget_for_change(combo)
                        r += 1

                    if type == 'Title':
                        title = QLabel(tab)
                        title.setProperty("heading", True)
                        title.style().unpolish(title)
                        title.style().polish(title)
                        title.setText(element[1])
                        grid.addWidget(title,r,1)
                        title.setObjectName("_title")
                        title.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        r += 1

                    if type == 'Image':
                        img = QLabel(tab)
                        grid.addWidget(img,r,1,10,2)
                        pmap = QPixmap('C:/Users/nitin/Desktop/FOSSEE/Osdag3/ResourceFiles/images/Channel.png')
                        img.setPixmap(pmap.scaled(220,800,Qt.KeepAspectRatio, Qt.FastTransformation))
                        r += 10

                    if type == 'TextBrowser':
                        r = 1
                        grid = QGridLayout()
                        horizontalLayout.addLayout(grid)
                        grid.setHorizontalSpacing(10)
                        grid.setVerticalSpacing(10)
                        grid.setAlignment(Qt.AlignRight|Qt.AlignTop)
                        grid.setContentsMargins(50,0,0,0)
                        lbl = QLabel(tab)
                        lbl.setText('Description')
                        grid.addWidget(lbl,r,1)
                        lbl.setObjectName("label_3")
                        lbl.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum))
                        r += 1

                        txt_browser = QTextBrowser(tab)
                        txt_browser.setHtml(element[3])
                        txt_browser.horizontalScrollBar().setVisible(False)
                        txt_browser.setObjectName(element[0])
                        grid.addWidget(txt_browser,r,1) # if using setMinimumSize


                    if type == 'Note':
                        Notes.append(lable)

                    if type == 'Break':
                        r = 1
                        grid = QGridLayout()
                        horizontalLayout.addLayout(grid)
                        grid.setHorizontalSpacing(10)
                        grid.setVerticalSpacing(10)
                        grid.setAlignment(Qt.AlignTop|Qt.AlignLeft)
                        continue

                if Notes:

                    hl1 = QFrame(tab)
                    hl1.setFrameShape(QFrame.HLine)
                    vertical.addWidget(hl1)
                    for lable in Notes:
                        lbl = QLabel(tab)
                        lbl.setWordWrap(True)
                        lbl.setText("<html><head/><body><p>" + lable + "</p></body></html>")
                        lbl.setObjectName("_title")
                        vertical.addWidget(lbl)


            scrollArea.setWidget(scrollAreaWidgetContents)

        self.main_layout.addLayout(self.button_layout)
        total_tabs = self.tabWidget.tabs.count()
        # print(f"Total tabs created: {total_tabs}")
        if total_tabs > 0:
            # Set to the last tab or a specific index if it exists
            target_index = min(2, total_tabs - 1)
            self.tabWidget.tabs.setCurrentIndex(target_index)
        module = main.module_name()

        if module in [KEY_DISP_FINPLATE, KEY_DISP_ENDPLATE, KEY_DISP_CLEATANGLE, KEY_DISP_SEATED_ANGLE, KEY_DISP_BCENDPLATE]:

            pushButton_Clear_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_COLSEC)
            pushButton_Clear_Column.clicked.connect(lambda: self.clear_tab(KEY_DISP_COLSEC))
            pushButton_Add_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_COLSEC)
            pushButton_Add_Column.clicked.connect(self.add_tab_column)
            pushButton_Import_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_COLSEC)
            pushButton_Import_Column.clicked.connect(lambda _, table="Columns": self.importSection.emit(table))
            pushButton_Download_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_COLSEC)
            pushButton_Download_Column.clicked.connect(lambda _, table="Columns", call_type="header": self.downloadDatabase.emit(table, call_type))
            pushButton_Clear_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_BEAMSEC)
            pushButton_Clear_Beam.clicked.connect(lambda: self.clear_tab(KEY_DISP_BEAMSEC))
            pushButton_Add_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_BEAMSEC)
            pushButton_Add_Beam.clicked.connect(self.add_tab_beam)
            pushButton_Import_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_BEAMSEC)
            pushButton_Import_Beam.clicked.connect(lambda _, table="Beams": self.importSection.emit(table))
            pushButton_Download_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_BEAMSEC)
            pushButton_Download_Beam.clicked.connect(lambda _, table="Beams", call_type="header": self.downloadDatabase.emit(table, call_type))

            if module == KEY_DISP_CLEATANGLE:
                pushButton_Clear_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + DISP_TITLE_CLEAT)
                pushButton_Clear_Angle.clicked.connect(lambda: self.clear_tab(DISP_TITLE_CLEAT))
                pushButton_Add_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + DISP_TITLE_CLEAT)
                pushButton_Add_Angle.clicked.connect(self.add_tab_angle)
                pushButton_Import_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + DISP_TITLE_CLEAT)
                pushButton_Import_Angle.clicked.connect(lambda _, table="Angles": self.importSection.emit(table))
                pushButton_Download_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + DISP_TITLE_CLEAT)
                pushButton_Download_Angle.clicked.connect(lambda _, table="Angles", call_type="header": self.downloadDatabase.emit(table, call_type))
            if module == KEY_DISP_SEATED_ANGLE:
                pushButton_Clear_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_SEATED_ANGLE)
                pushButton_Clear_Angle.clicked.connect(lambda: self.clear_tab(KEY_DISP_SEATED_ANGLE))
                pushButton_Add_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_SEATED_ANGLE)
                pushButton_Add_Angle.clicked.connect(self.add_tab_angle)
                pushButton_Import_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_SEATED_ANGLE)
                pushButton_Import_Angle.clicked.connect(lambda _, table="Angles": self.importSection.emit(table))
                pushButton_Download_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_SEATED_ANGLE)
                pushButton_Download_Angle.clicked.connect(lambda _, table="Angles", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module == KEY_DISP_COLUMNCOVERPLATE or module == KEY_DISP_COLUMNCOVERPLATEWELD or module == KEY_DISP_COLUMNENDPLATE:
            pushButton_Clear_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_COLSEC)
            pushButton_Clear_Column.clicked.connect(lambda: self.clear_tab(KEY_DISP_COLSEC))
            pushButton_Add_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_COLSEC)
            pushButton_Add_Column.clicked.connect(self.add_tab_column)
            pushButton_Import_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_COLSEC)
            pushButton_Import_Column.clicked.connect(lambda _, table="Columns": self.importSection.emit(table))
            pushButton_Download_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_COLSEC)
            pushButton_Download_Column.clicked.connect(lambda _, table="Columns", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module == KEY_DISP_BEAMCOVERPLATE or module == KEY_DISP_BEAMCOVERPLATEWELD:
            pushButton_Clear_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_BEAMSEC)
            pushButton_Clear_Beam.clicked.connect(lambda: self.clear_tab(KEY_DISP_BEAMSEC))
            pushButton_Add_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_BEAMSEC)
            pushButton_Add_Beam.clicked.connect(self.add_tab_beam)
            pushButton_Import_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_BEAMSEC)
            pushButton_Import_Beam.clicked.connect(lambda _, table="Beams": self.importSection.emit(table))
            pushButton_Download_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_BEAMSEC)
            pushButton_Download_Beam.clicked.connect(lambda _, table="Beams", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module == KEY_DISP_BB_EP_SPLICE:
            pushButton_Clear_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_BEAMSEC)
            pushButton_Clear_Beam.clicked.connect(lambda: self.clear_tab(KEY_DISP_BEAMSEC))
            pushButton_Add_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_BEAMSEC)
            pushButton_Add_Beam.clicked.connect(self.add_tab_beam)
            pushButton_Import_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_BEAMSEC)
            pushButton_Import_Beam.clicked.connect(lambda _, table="Beams": self.importSection.emit(table))
            pushButton_Download_Beam = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_BEAMSEC)
            pushButton_Download_Beam.clicked.connect(lambda _, table="Beams", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module == KEY_DISP_COMPRESSION:
            pushButton_Clear_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_COLSEC)
            pushButton_Clear_Column.clicked.connect(lambda: self.clear_tab(KEY_DISP_COLSEC))
            pushButton_Add_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_COLSEC)
            pushButton_Add_Column.clicked.connect(self.add_tab_column)
            pushButton_Import_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_COLSEC)
            pushButton_Import_Column.clicked.connect(lambda _, table="Columns": self.importSection.emit(table))
            pushButton_Download_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_COLSEC)
            pushButton_Download_Column.clicked.connect(lambda _, table="Columns", call_type="header": self.downloadDatabase.emit(table, call_type))
            pushButton_Clear_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + DISP_TITLE_CHANNEL)
            pushButton_Clear_Channel.clicked.connect(lambda: self.clear_tab(DISP_TITLE_CHANNEL))
            pushButton_Add_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + DISP_TITLE_CHANNEL)
            pushButton_Add_Channel.clicked.connect(self.add_tab_channel)
            pushButton_Import_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + DISP_TITLE_CHANNEL)
            pushButton_Import_Channel.clicked.connect(lambda _, table="Channels": self.importSection.emit(table))
            pushButton_Download_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + DISP_TITLE_CHANNEL)
            pushButton_Download_Channel.clicked.connect(lambda _, table="Channels", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module == KEY_DISP_COMPRESSION_STRUT:
            pushButton_Clear_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + DISP_TITLE_ANGLE)
            pushButton_Clear_Angle.clicked.connect(lambda: self.clear_tab(DISP_TITLE_ANGLE))
            pushButton_Add_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + DISP_TITLE_ANGLE)
            pushButton_Add_Angle.clicked.connect(self.add_tab_angle)
            pushButton_Import_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + DISP_TITLE_ANGLE)
            pushButton_Import_Angle.clicked.connect(lambda _, table="Angles": self.importSection.emit(table))
            pushButton_Download_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + DISP_TITLE_ANGLE)
            pushButton_Download_Angle.clicked.connect(lambda _, table="Angles", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module == KEY_DISP_BASE_PLATE:
            pushButton_Clear_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_COLSEC)
            pushButton_Clear_Column.clicked.connect(lambda: self.clear_tab(KEY_DISP_COLSEC))
            pushButton_Add_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_COLSEC)
            pushButton_Add_Column.clicked.connect(self.add_tab_column)
            pushButton_Import_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_COLSEC)
            pushButton_Import_Column.clicked.connect(lambda _, table="Columns": self.importSection.emit(table))
            pushButton_Download_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_COLSEC)
            pushButton_Download_Column.clicked.connect(lambda _, table="Columns", call_type="header": self.downloadDatabase.emit(table, call_type))

        if module in [KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED]:
            pushButton_Clear_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + DISP_TITLE_ANGLE)
            pushButton_Clear_Angle.clicked.connect(lambda: self.clear_tab(DISP_TITLE_ANGLE))
            pushButton_Add_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + DISP_TITLE_ANGLE)
            pushButton_Add_Angle.clicked.connect(self.add_tab_angle)
            pushButton_Import_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + DISP_TITLE_ANGLE)
            pushButton_Import_Angle.clicked.connect(lambda _, table="Angles": self.importSection.emit(table))
            pushButton_Download_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + DISP_TITLE_ANGLE)
            pushButton_Download_Angle.clicked.connect(lambda _, table="Angles", call_type="header": self.downloadDatabase.emit(table, call_type))
            pushButton_Clear_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + DISP_TITLE_CHANNEL)
            pushButton_Clear_Channel.clicked.connect(lambda: self.clear_tab(DISP_TITLE_CHANNEL))
            pushButton_Add_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + DISP_TITLE_CHANNEL)
            pushButton_Add_Channel.clicked.connect(self.add_tab_channel)
            pushButton_Import_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + DISP_TITLE_CHANNEL)
            pushButton_Import_Channel.clicked.connect(lambda _, table="Channels": self.importSection.emit(table))
            pushButton_Download_Channel = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + DISP_TITLE_CHANNEL)
            pushButton_Download_Channel.clicked.connect(lambda _, table="Channels", call_type="header": self.downloadDatabase.emit(table, call_type))
        
        if module in [KEY_DISP_STRUT_BOLTED_END_GUSSET, KEY_DISP_STRUT_WELDED_END_GUSSET]:
            pushButton_Clear_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + DISP_TITLE_ANGLE)
            pushButton_Clear_Angle.clicked.connect(lambda: self.clear_tab(DISP_TITLE_ANGLE))
            pushButton_Add_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + DISP_TITLE_ANGLE)
            pushButton_Add_Angle.clicked.connect(self.add_tab_angle)
            pushButton_Import_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + DISP_TITLE_ANGLE)
            pushButton_Import_Angle.clicked.connect(lambda _, table="Angles": self.importSection.emit(table))
            pushButton_Download_Angle = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + DISP_TITLE_ANGLE)
            pushButton_Download_Angle.clicked.connect(lambda _, table="Angles", call_type="header": self.downloadDatabase.emit(table, call_type))
        
        if module in [KEY_DISP_FLEXURE, KEY_DISP_FLEXURE2]:
            pushButton_Clear_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Clear_" + KEY_DISP_COLSEC)
            pushButton_Clear_Column.clicked.connect(lambda: self.clear_tab(KEY_DISP_COLSEC))
            pushButton_Add_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Add_" + KEY_DISP_COLSEC)
            pushButton_Add_Column.clicked.connect(self.add_tab_column)
            pushButton_Import_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Import_" + KEY_DISP_COLSEC)
            pushButton_Import_Column.clicked.connect(lambda _, table="Columns": self.importSection.emit(table))
            pushButton_Download_Column = self.tabWidget.tabs.findChild(QWidget, "pushButton_Download_" + KEY_DISP_COLSEC)
            pushButton_Download_Column.clicked.connect(lambda _, table="Columns", call_type="header": self.downloadDatabase.emit(table, call_type))

    def set_lock(self):
        """
        This method locks input fields.
        """
        locked = self.state_locked

        # Set input fields to read-only based on state_locked
        for widget in self.findChildren(QWidget):
            if isinstance(widget, (QComboBox, QLineEdit)):
                widget.setDisabled(locked)

        # Set buttons to disabled based on state_locked
        self.btn_defaults.setDisabled(locked)
        # self.btn_save.setDisabled(locked)
        button_objectname_pattern = QRegularExpression(r"^pushButton_(Add|Clear|Import)_")
        for button in self.findChildren(QPushButton, button_objectname_pattern):
            button.setDisabled(locked)

        # Tooltip on dialog
        if locked:
            self.setToolTip("🔒Unlock to Edit")
        else:
            self.setToolTip("")

    def manage_designation_size(self,line_edit):
        def change_size():
            font = line_edit.font()
            text = line_edit.text()
            metrices = QFontMetrics(font)
            width = metrices.boundingRect(text).width()
            width += 25
            if width > 91:
                line_edit.setFixedWidth(width)
            else:
                line_edit.setFixedWidth(120)
        return change_size

    def clear_tab(self, tab_name):
        '''
        @author: Umair
        '''
        tab = self.tabWidget.tabs.findChild(QWidget, tab_name)

        if tab:
            for c in tab.findChildren(QWidget):
                if c in self.do_not_clear_list:
                    continue
            
                # Block signals to prevent triggering textChanged/currentIndexChanged
                c.blockSignals(True)

                if isinstance(c, QComboBox):
                    c.setCurrentIndex(0)
                elif isinstance(c, QLineEdit):
                    c.clear()
                
                # Re-enable signals
                c.blockSignals(False)

    def add_baseplate_tab_column(self):
        '''
        @author: Umair
        '''
        tab_Column = self.tabWidget.tabs.findChild(QWidget, KEY_DISP_COLSEC)
        rhs = connectdb("RHS", call_type="popup")
        shs = connectdb("SHS", call_type="popup")
        chs = connectdb("CHS", call_type="popup")
        hs = rhs + shs
        input_section = self.input_dictionary[KEY_SECSIZE]

        if input_section in hs:
            table = "RHS" if input_section in rhs else "SHS"
            values = {KEY_SECSIZE: '', 'Label_21': ''}
            for i in [1, 2, 3, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
                key = "Label_HS_"+str(i)
                values.update({key: ''})
        elif input_section in chs:
            table = "CHS"
            values = {KEY_SECSIZE: '', 'Label_21': ''}
            for i in [1, 2, 3, 11, 12, 13, 14, 15, 16]:
                key = "Label_CHS_" + str(i)
                values.update({key: ''})
        else:
            table = "Columns"
            values = {KEY_SECSIZE: '', 'Label_8': '', 'Label_21': ''}
            for i in [1, 2, 3, 11, 12, 13, 14, 15, 16]:
                key = "Label_" + str(i)
                values.update({key: ''})

        keys_to_add = values.keys()

        for ch in tab_Column.findChildren(QWidget):
            if isinstance(ch, QLineEdit) and ch.text() == "":
                CustomMessageBox(
                    title="Warning",
                    text="Please fill all the missing parameters!",
                    dialogType=MessageBoxType.Warning,
                ).exec()
                return
            elif isinstance(ch, QLineEdit) and ch.text() != "":
                if ch.objectName() in keys_to_add:
                    values[ch.objectName()] = ch.text()
            elif isinstance(ch, QComboBox):
                if ch.objectName() in keys_to_add:
                    values[ch.objectName()] = ch.currentText()

        for k in keys_to_add:
            if k in [KEY_SECSIZE, "Label_21", "Label_8"]:
                continue
            else:
                values[key] = float(values[key])

        if ch:
            conn = sqlite3.connect(PATH_TO_DATABASE)
            c = conn.cursor()
            query = "SELECT count(*) FROM "+table+" WHERE Designation = ?"
            c.execute(query, (values[KEY_SECSIZE],))
            data = c.fetchone()[0]
            if data == 0:
                if table == "RHS":
                    c.execute('''INSERT INTO RHS (Designation,D,B,T,W,A,Izz,Iyy,Rzz,Ryy,
                        Zzz,Zyy,Zpz,Zpy,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (values[KEY_SECSIZE], values["Label_HS_1"], values["Label_HS_2"],
                               values["Label_HS_3"], values["Label_HS_11"], values["Label_HS_12"],
                               values["Label_HS_13"], values["Label_HS_14"], values["Label_HS_15"],
                               values["Label_HS_16"], values["Label_HS_17"], values["Label_HS_18"],
                               values["Label_HS_19"], values["Label_HS_20"], values["Label_HS_21"],
                               ))
                    conn.commit()
                elif table == "SHS":
                    c.execute('''INSERT INTO SHS (Designation,D,B,T,W,A,Izz,Iyy,Rzz,Ryy,
                        Zzz,Zyy,Zpz,Zpy,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (values[KEY_SECSIZE], values["Label_HS_1"], values["Label_HS_2"],
                               values["Label_HS_3"], values["Label_HS_11"], values["Label_HS_12"],
                               values["Label_HS_13"], values["Label_HS_14"], values["Label_HS_15"],
                               values["Label_HS_16"], values["Label_HS_17"], values["Label_HS_18"],
                               values["Label_HS_19"], values["Label_HS_20"], values["Label_HS_21"],
                               ))
                    conn.commit()
                elif table == "CHS":
                    c.execute('''INSERT INTO CHS (Designation,NB,OD,T,W,A,V,Ves,Vis,I,
                        Z,R,Rsq,Source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (values[KEY_SECSIZE], values["Label_CHS_1"], values["Label_CHS_2"],
                               values["Label_CHS_3"], values["Label_HS_11"], values["Label_HS_12"],
                               values["Label_HS_13"], values["Label_HS_14"], values["Label_HS_15"],
                               values["Label_HS_16"], values["Label_HS_17"], values["Label_HS_18"],
                               values["Label_HS_19"], values["Label_HS_20"], values["Label_HS_21"],
                               ))
                    conn.commit()
                else:
                    c.execute('''INSERT INTO Columns (Designation,Mass,Area,D,B,tw,T,FlangeSlope,R1,R2,Iz,Iy,rz,ry,
                        Zz,Zy,Zpz,Zpy,It,Iw,Source,Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (Designation_c, Mass_c, Area_c,
                               D_c, B_c, tw_c, T_c,FlangeSlope_c,
                               R1_c, R2_c, Iz_c, Iy_c, rz_c,
                               ry_c, Zz_c, Zy_c,
                               Zpz_c, Zpy_c, It_c,Iw_c,Source_c, Type))
                    conn.commit()
                c.close()
                conn.close()
                CustomMessageBox(
                    title="Information",
                    text="Data is added successfully to the database!",
                    dialogType=MessageBoxType.Warning,
                ).exec()
            else:
                CustomMessageBox(
                    title="Warning",
                    text="Designation already exists in the database!",
                    dialogType=MessageBoxType.Warning,
                ).exec()

    def add_tab_column(self):
        '''
        @author: Umair
        '''
        tab_Column = self.tabWidget.tabs.findChild(QWidget, KEY_DISP_COLSEC)
        name = self.tabWidget.tabs.tabText(self.tabWidget.tabs.indexOf(tab_Column))
        if name in [KEY_DISP_COLSEC, KEY_DISP_SECSIZE]:
            table = "Columns"
        elif name == KEY_DISP_PRIBM:
            table = "Beams"
        else:
            pass
        for ch in tab_Column.findChildren(QWidget):
            if isinstance(ch, QLineEdit) and ch.text() == "":
                CustomMessageBox(
                    title="Warning",
                    text="Designation already exists in the database!",
                    dialogType=MessageBoxType.Warning,
                ).exec()
                return
            elif isinstance(ch, QLineEdit) and ch.text() != "":
                if ch.objectName() == KEY_SECSIZE or ch.objectName() == KEY_SUPTNGSEC:
                    Designation_c = ch.text()
                elif ch.objectName() == KEY_SOURCE:
                    Source_c = ch.text()
                elif ch.objectName() == 'Label_1':
                    D_c = float(ch.text())
                elif ch.objectName() == 'Label_2':
                    B_c = float(ch.text())
                elif ch.objectName() == 'Label_3':
                    T_c = float(ch.text())
                elif ch.objectName() == 'Label_4':
                    tw_c = float(ch.text())
                elif ch.objectName() == 'Label_5':
                    FlangeSlope_c = float(ch.text())
                elif ch.objectName() == 'Label_6':
                    R1_c = float(ch.text())
                elif ch.objectName() == 'Label_7':
                    R2_c = float(ch.text())
                elif ch.objectName() == 'Label_11':
                    Mass_c = float(ch.text())
                elif ch.objectName() == 'Label_12':
                    Area_c = float(ch.text())
                elif ch.objectName() == 'Label_13':
                    Iz_c = float(ch.text())
                elif ch.objectName() == 'Label_14':
                    Iy_c = float(ch.text())
                elif ch.objectName() == 'Label_15':
                    rz_c = float(ch.text())
                elif ch.objectName() == 'Label_16':
                    ry_c = float(ch.text())
                elif ch.objectName() == 'Label_17':
                    Zz_c = float(ch.text())
                elif ch.objectName() == 'Label_18':
                    Zy_c = float(ch.text())
                elif ch.objectName() == 'Label_19':
                    if ch.text() == "":
                        ch.setText("0")
                    Zpz_c = ch.text()
                elif ch.objectName() == 'Label_20':
                    if ch.text() == "":
                        ch.setText("0")
                    Zpy_c = ch.text()
                elif ch.objectName() == 'Label_21':
                    if ch.text() == "":
                        ch.setText("0")
                    It_c = ch.text()
                elif ch.objectName() == 'Label_22':
                    if ch.text() == "":
                        ch.setText("0")
                    Iw_c = ch.text()
                else:
                    pass
            elif isinstance(ch, QComboBox):
                if ch.objectName() == 'Label_8':
                    Type = ch.currentText()

        if ch:
            conn = sqlite3.connect(PATH_TO_DATABASE)
            c = conn.cursor()
            if table == "Beams":
                c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_c,))
                data = c.fetchone()[0]
            else:
                c.execute("SELECT count(*) FROM Columns WHERE Designation = ?", (Designation_c,))
                data = c.fetchone()[0]
            if data == 0:
                if table == "Beams":
                    c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,FlangeSlope,R1,R2,Iz,Iy,rz,ry,
                        Zz,Zy,Zpz,Zpy,It,Iw,Source,Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (Designation_c, Mass_c, Area_c,
                               D_c, B_c, tw_c, T_c,FlangeSlope_c,
                               R1_c, R2_c, Iz_c, Iy_c, rz_c,
                               ry_c, Zz_c, Zy_c,
                               Zpz_c, Zpy_c, It_c,Iw_c,Source_c, Type))
                    conn.commit()
                else:
                    c.execute('''INSERT INTO Columns (Designation,Mass,Area,D,B,tw,T,FlangeSlope,R1,R2,Iz,Iy,rz,ry,
                        Zz,Zy,Zpz,Zpy,It,Iw,Source,Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (Designation_c, Mass_c, Area_c,
                               D_c, B_c, tw_c, T_c,FlangeSlope_c,
                               R1_c, R2_c, Iz_c, Iy_c, rz_c,
                               ry_c, Zz_c, Zy_c,
                               Zpz_c, Zpy_c, It_c,Iw_c,Source_c, Type))
                    conn.commit()
                c.close()
                conn.close()
                CustomMessageBox(
                    title="Information",
                    text="Data is added successfully to the database!",
                    dialogType=MessageBoxType.Information,
                ).exec()

            else:
                CustomMessageBox(
                    title="Warning",
                    text="Designation already exists in the database!",
                    dialogType=MessageBoxType.Warning,
                ).exec()

    def add_tab_beam(self):
        '''
        @author: Umair
        '''
        tab_Beam = self.tabWidget.tabs.findChild(QWidget, KEY_DISP_BEAMSEC)
        name = self.tabWidget.tabs.tabText(self.tabWidget.tabs.indexOf(tab_Beam))
        for ch in tab_Beam.findChildren(QWidget):
            if isinstance(ch, QLineEdit) and ch.text() == "":
                CustomMessageBox(
                    title="Warning",
                    text="Please fill all the missing parameters!",
                    dialogType=MessageBoxType.Warning,
                ).exec()
                add_bm = tab_Beam.findChild(QWidget, 'pushButton_Add_'+KEY_DISP_BEAMSEC)
                add_bm.setDisabled(True)
                return

            elif isinstance(ch, QLineEdit) and ch.text() != "":

                if ch.objectName() == KEY_SECSIZE or ch.objectName() == KEY_SUPTDSEC:
                    Designation_b = ch.text()
                elif ch.objectName() == KEY_SOURCE:
                    Source_b = ch.text()
                elif ch.objectName() == 'Label_1':
                    D_b = float(ch.text())
                elif ch.objectName() == 'Label_2':
                    B_b = float(ch.text())
                elif ch.objectName() == 'Label_3':
                    T_b = float(ch.text())
                elif ch.objectName() == 'Label_4':
                    tw_b = float(ch.text())
                elif ch.objectName() == 'Label_5':
                    FlangeSlope_b = float(ch.text())
                elif ch.objectName() == 'Label_6':
                    R1_b = float(ch.text())
                elif ch.objectName() == 'Label_7':
                    R2_b = float(ch.text())
                elif ch.objectName() == 'Label_11':
                    Mass_b = float(ch.text())
                elif ch.objectName() == 'Label_12':
                    Area_b = float(ch.text())
                elif ch.objectName() == 'Label_13':
                    Iz_b = float(ch.text())
                elif ch.objectName() == 'Label_14':
                    Iy_b = float(ch.text())
                elif ch.objectName() == 'Label_15':
                    rz_b = float(ch.text())
                elif ch.objectName() == 'Label_16':
                    ry_b = float(ch.text())
                elif ch.objectName() == 'Label_17':
                    Zz_b = float(ch.text())
                elif ch.objectName() == 'Label_18':
                    Zy_b = float(ch.text())
                elif ch.objectName() == 'Label_19':
                    if ch.text() == "":
                        ch.setText("0")
                    Zpz_b = ch.text()
                elif ch.objectName() == 'Label_20':
                    if ch.text() == "":
                        ch.setText("0")
                    Zpy_b = ch.text()
                elif ch.objectName() == 'Label_21':
                    if ch.text() == "":
                        ch.setText("0")
                    I_t = ch.text()
                elif ch.objectName() == 'Label_22':
                    if ch.text() == "":
                        ch.setText("0")
                    I_w = ch.text()
                else:
                    pass
            elif isinstance(ch, QComboBox):
                if ch.objectName() == 'Label_8':
                    Type = ch.currentText()

        # if ch.objectName() ==  "pushButton_Download_" + name:
        if ch:
            conn = sqlite3.connect(PATH_TO_DATABASE)

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Beams WHERE Designation = ?", (Designation_b,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Beams (Designation,Mass,Area,D,B,tw,T,FlangeSlope,R1,R2,Iz,Iy,rz,ry,Zz,Zy,Zpz,Zpy,
                    It,Iw,Source,Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (Designation_b, Mass_b, Area_b,
                           D_b, B_b, tw_b, T_b, FlangeSlope_b,
                           R1_b, R2_b, Iz_b, Iy_b, rz_b,
                           ry_b, Zz_b, Zy_b,
                           Zpz_b, Zpy_b,I_t,I_w, Source_b, Type))
                conn.commit()
                c.close()
                conn.close()
                CustomMessageBox(
                    title="Information",
                    text="Data is added successfully to the database.",
                    dialogType=MessageBoxType.Information
                ).exec()
            else:
                CustomMessageBox(
                    title="Warning",
                    text="Designation already exists in the database!",
                    dialogType=MessageBoxType.Warning
                ).exec()

    def add_tab_angle(self):
        '''
        @author: Umair
        '''

        tab_Angle = self.tabWidget.tabs.findChild(QWidget, DISP_TITLE_ANGLE)
        tab_name = DISP_TITLE_ANGLE
        if tab_Angle == None:
            tab_Angle = self.tabWidget.tabs.findChild(QWidget, DISP_TITLE_CLEAT)
            tab_name  = DISP_TITLE_CLEAT
        if tab_Angle == None:
            tab_Angle = self.tabWidget.tabs.findChild(QWidget, KEY_DISP_SEATED_ANGLE)
            tab_name  = KEY_DISP_SEATED_ANGLE
        if tab_Angle == None:
            tab_Angle = self.tabWidget.tabs.findChild(QWidget, KEY_DISP_TOPANGLE)
            tab_name = KEY_DISP_TOPANGLE
        # tab_cleat_angle = self.tabWidget.tabs.findChild(QWidget, DISP_TITLE_CLEAT)
        # name = self.tabWidget.tabs.tabText(self.tabWidget.tabs.indexOf(tab_Angle))
        if self.add_compound_section(tab_Angle):
            return
        for ch in tab_Angle.findChildren(QWidget):
            if isinstance(ch, QLineEdit) and ch.text() == "":
                CustomMessageBox(
                    title="Warning",
                    text="Please fill all the missing parameters!",
                    dialogType=MessageBoxType.Warning
                ).exec()
                add_bm = tab_Angle.findChild(QWidget, 'pushButton_Add_'+tab_name)
                add_bm.setDisabled(True)
                return

            elif isinstance(ch, QLineEdit) and ch.text() != "":

                if ch.objectName() == KEY_SECSIZE_SELECTED or ch.objectName() == KEY_ANGLE_SELECTED:
                    Designation_a = ch.text()
                elif ch.objectName() == KEY_SOURCE:
                    Source = ch.text()
                elif ch.objectName() == 'Label_1':
                    a = ch.text()
                elif ch.objectName() == 'Label_2':
                    b = ch.text()
                elif ch.objectName() == 'Label_3':
                    t = float(ch.text())
                elif ch.objectName() == 'Label_4':
                    R1 = float(ch.text())
                elif ch.objectName() == 'Label_5':
                    R2 = float(ch.text())
                elif ch.objectName() == 'Label_7':
                    Cz = float(ch.text())
                elif ch.objectName() == 'Label_8':
                    Cy = float(ch.text())
                elif ch.objectName() == 'Label_9':
                    Mass = float(ch.text())
                elif ch.objectName() == 'Label_10':
                    Area = float(ch.text())
                elif ch.objectName() == 'Label_11':
                    I_z = float(ch.text())
                elif ch.objectName() == 'Label_12':
                    I_y = float(ch.text())
                elif ch.objectName() == 'Label_13':
                    I_u_max = float(ch.text())
                elif ch.objectName() == 'Label_14':
                    I_v_min = float(ch.text())
                elif ch.objectName() == 'Label_15':
                    rz = float(ch.text())
                elif ch.objectName() == 'Label_16':
                    ry = float(ch.text())
                elif ch.objectName() == 'Label_17':
                    if ch.text() == "":
                        ch.setText("0")
                    ru_max = float(ch.text())
                elif ch.objectName() == 'Label_18':
                    if ch.text() == "":
                        ch.setText("0")
                    rv_min = ch.text()
                elif ch.objectName() == 'Label_19':
                    if ch.text() == "":
                        ch.setText("0")
                    zz = ch.text()
                elif ch.objectName() == 'Label_20':
                    if ch.text() == "":
                        ch.setText("0")
                    zy = ch.text()
                elif ch.objectName() == 'Label_21':
                    if ch.text() == "":
                        ch.setText("0")
                    zpz = ch.text()
                elif ch.objectName() == 'Label_22':
                    if ch.text() == "":
                        ch.setText("0")
                    zpy = ch.text()
                elif ch.objectName() == 'Label_23':
                    if ch.text() == "":
                        ch.setText("0")
                    It = ch.text()

                else:
                    pass
            elif isinstance(ch, QComboBox):
                if ch.objectName() == 'Label_6':
                    Type = ch.currentText()

        # if ch.objectName() ==  "pushButton_Download_" + name:
        if ch:
            conn = sqlite3.connect(PATH_TO_DATABASE)

            c = conn.cursor()

            c.execute("SELECT count(*) FROM Angles WHERE Designation = ?", (Designation_a,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Angles (Designation,Mass,Area,a,b,t,R1,R2,Cz,Cy,Iz,Iy,Iumax,Ivmin,rz,ry,
                rumax,rvmin,Zz,Zy,Zpz,Zpy,It,Source,Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (Designation_a, Mass, Area,
                           a,b, t, R1, R2, Cz,Cy,I_z,I_y,I_u_max,
                           I_v_min, rz, ry, ru_max, rv_min,zz,zy,zpz,zpy,It,Source,Type))
                conn.commit()
                c.close()
                conn.close()
                
                CustomMessageBox(
                    title="Information",
                    text="Data is added successfully to the database.",
                    dialogType=MessageBoxType.Information
                ).exec()
            else:
                CustomMessageBox(
                    title="Warning",
                    text="Designation already exists in the database!",
                    dialogType=MessageBoxType.Warning
                ).exec()

    def add_tab_channel(self):
        '''
        @author: Umair
        '''
        tab_Channel = self.tabWidget.tabs.findChild(QWidget, DISP_TITLE_CHANNEL)

        if self.add_compound_section(tab_Channel):
            return

        name = self.tabWidget.tabs.tabText(self.tabWidget.tabs.indexOf(tab_Channel))
        for ch in tab_Channel.findChildren(QWidget):
            if isinstance(ch, QLineEdit) and ch.text() == "":
                CustomMessageBox(
                    title="Warning",
                    text="Please fill all the missing parameters!",
                    dialogType=MessageBoxType.Warning,
                ).exec()
                add_bm = tab_Channel.findChild(QWidget, 'pushButton_Add_'+DISP_TITLE_ANGLE)
                add_bm.setDisabled(True)
                return

            elif isinstance(ch, QLineEdit) and ch.text() != "":

                if ch.objectName() == KEY_SECSIZE_SELECTED:
                    Designation_c = ch.text()
                elif ch.objectName() == KEY_SOURCE:
                    Source = ch.text()
                elif ch.objectName() == 'Label_1':
                    B = float(ch.text())
                elif ch.objectName() == 'Label_2':
                    T = float(ch.text())
                elif ch.objectName() == 'Label_3':
                    D = float(ch.text())
                elif ch.objectName() == 'Label_13':
                    t_w = float(ch.text())
                elif ch.objectName() == 'Label_14':
                    Flange_Slope = float(ch.text())
                elif ch.objectName() == 'Label_4':
                    R1 = float(ch.text())
                elif ch.objectName() == 'Label_5':
                    R2 = float(ch.text())
                elif ch.objectName() == 'Label_9':
                    Mass = float(ch.text())
                elif ch.objectName() == 'Label_10':
                    Area = float(ch.text())
                elif ch.objectName() == 'Label_17':
                    if ch.text() == "":
                        ch.setText("0")
                    cy = float(ch.text())
                elif ch.objectName() == 'Label_11':
                    I_z = float(ch.text())
                elif ch.objectName() == 'Label_12':
                    I_y = float(ch.text())
                elif ch.objectName() == 'Label_15':
                    rz = float(ch.text())
                elif ch.objectName() == 'Label_16':
                    ry = float(ch.text())

                elif ch.objectName() == 'Label_19':
                    if ch.text() == "":
                        ch.setText("0")
                    zz = ch.text()
                elif ch.objectName() == 'Label_20':
                    if ch.text() == "":
                        ch.setText("0")
                    zy = ch.text()
                elif ch.objectName() == 'Label_21':
                    if ch.text() == "":
                        ch.setText("0")
                    zpz = ch.text()
                elif ch.objectName() == 'Label_22':
                    if ch.text() == "":
                        ch.setText("0")
                    zpy = ch.text()
                elif ch.objectName() == 'Label_26':
                    if ch.text() == "":
                        ch.setText("0")
                    It = ch.text()
                elif ch.objectName() == 'Label_27':
                    if ch.text() == "":
                        ch.setText("0")
                    Iw = ch.text()

                else:
                    pass
            elif isinstance(ch, QComboBox):
                if ch.objectName() == 'Label_6':
                    Type = ch.currentText()

        # if ch.objectName() ==  "pushButton_Download_" + name:
        if ch:
            conn = sqlite3.connect(PATH_TO_DATABASE)

            c = conn.cursor()
            c.execute("SELECT count(*) FROM Channels WHERE Designation = ?", (Designation_c,))
            data = c.fetchone()[0]
            if data == 0:
                c.execute('''INSERT INTO Channels (Designation,Mass, Area,D,B,tw,T,FlangeSlope, R1, R2,Cy,Iz,Iy,
                 rz, ry,Zz,Zy,Zpz,Zpy,It,Iw,Source,Type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (Designation_c, Mass, Area,D,B,t_w,T,
                           Flange_Slope, R1, R2,cy,I_z,I_y, rz, ry,zz,zy,zpz,zpy,It, Iw,Source,Type))
                conn.commit()
                c.close()
                conn.close()
                CustomMessageBox(
                    title="Information",
                    text="Data is added successfully to the database.",
                    dialogType=MessageBoxType.Information,
                ).exec()
            else:
                CustomMessageBox(
                    title="Warning",
                    text="Designation already exists in the database!",
                    dialogType=MessageBoxType.Warning,
                ).exec()

    def add_compound_section(self, tab):
        if tab.findChild(QWidget, KEY_SEC_PROFILE):
            if tab.findChild(QWidget, KEY_SEC_PROFILE).text() in ['Back to Back Angles', 'Star Angles', 'Back to Back Channels']:
                CustomMessageBox(
                    title="Information",
                    text="To create new compound section please add as single section.",
                    dialogType=MessageBoxType.Information,
                ).exec()
                return True
            else:
                return False
        else:
            return False

class AdditionalInputs(QObject):
    def __init__(self, main, module_window, input_dictionary, parent=None):
        self.ui = Window(main, input_dictionary, parent=parent)
        # print(f"@@input_dictionary: {input_dictionary}\n\n")
        self.main = main
        self.main_controller = parent
        self.module_window = module_window
        self.saved = None
        self.flag = False
        self.sectionalprop = I_sectional_Properties()
        self.ui.btn_save.clicked.connect(self.close_designPref)
        self.ui.btn_defaults.clicked.connect(lambda: self.default_fn(main, input_dictionary))
        self.module = main.module_name()
        self.window_close_flag = True
        self.changes = None

    def show(self):
        screen = QGuiApplication.primaryScreen()
        resolution = screen.geometry()
        width = resolution.width()
        height = resolution.height()
        self.ui.resize(int(width * 0.7), int(height * 0.6))
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.center()
        self.changes = self.ui.exec_()
        if self.changes != QDialog.Accepted:
            self.flag = False
        self.module_window.prev_inputs = self.module_window.input_dock_inputs

    def default_fn(self, main, input_dictionary):
        '''
        @author: Umair
        '''
        tab_Bolt = self.ui.tabWidget.tabs.findChild(QWidget, "Bolt")
        tab_Weld = self.ui.tabWidget.tabs.findChild(QWidget, "Weld")
        tab_Detailing = self.ui.tabWidget.tabs.findChild(QWidget, "Detailing")
        tab_Design = self.ui.tabWidget.tabs.findChild(QWidget, "Design")
        # For Base Plate Connection
        tab_anchor_bolt = self.ui.tabWidget.tabs.findChild(QWidget, "Anchor Bolt")
        # For Column Design, Simply Supported, Cantiliver, Plate Girder
        tab_optimization = self.ui.tabWidget.tabs.findChild(QWidget, "Optimization")
        # For Plate Girder
        tab_stiffeners = self.ui.tabWidget.tabs.findChild(QWidget, "Stiffeners")
        tab_additional_pg = self.ui.tabWidget.tabs.findChild(QWidget, "Additional Girder Data")
        tab_deflection = self.ui.tabWidget.tabs.findChild(QWidget, "Deflection")

        bolt_values_dictionary = {}
        weld_values_dictionary = {}
        design_values_dictionary = {}
        detailing_values_dictionary = {}
        # For Base Plate Connection
        base_anchor_bolt_dictionary = {}
        # For Column Design, Simply Supported, Cantiliver, Plate Girder
        optimization_dictionary = {}
        # For Plate Girder
        stiffeners_dictionary = {}
        additional_pg_dictionary = {}
        deflection_dictionary = {}

        if tab_Bolt is not None:
            f = self.find_function_reference(main.tab_list(), "Bolt")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    bolt_values_dictionary.update(
                        {i[0]: str(main.get_values_for_design_pref(i[0], input_dictionary))})

            for children in tab_Bolt.findChildren(QWidget):
                if children.objectName() in bolt_values_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(bolt_values_dictionary[children.objectName()])
                        # if bolt_values_dictionary[children.objectName()==0:
                        #     children.textEdit.setDisabled(True)

                    elif type(children) == QComboBox:
                        children.setCurrentText(bolt_values_dictionary[children.objectName()])
                    else:
                        pass

        if tab_Weld is not None:
            f = self.find_function_reference(main.tab_list(), "Weld")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    weld_values_dictionary.update(
                        {i[0]: str(main.get_values_for_design_pref(i[0], input_dictionary))})

            for children in tab_Weld.findChildren(QWidget):
                if children.objectName() in weld_values_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(weld_values_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(weld_values_dictionary[children.objectName()])
                    else:
                        pass

        if tab_Detailing is not None:
            f = self.find_function_reference(main.tab_list(), "Detailing")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    detailing_values_dictionary.update(
                        {i[0]: str(main.get_values_for_design_pref(i[0], input_dictionary))})

            for children in tab_Detailing.findChildren(QWidget):
                if children.objectName() in detailing_values_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(detailing_values_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(detailing_values_dictionary[children.objectName()])
                    else:
                        pass

        if tab_Design is not None:
            f = self.find_function_reference(main.tab_list(), "Design")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    design_values_dictionary.update(
                        {i[0]: str(main.get_values_for_design_pref(i[0], input_dictionary))})

            for children in tab_Design.findChildren(QWidget):
                if children.objectName() in design_values_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(design_values_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(design_values_dictionary[children.objectName()])
                    else:
                        pass
        
        # For Base Plate Connection
        if tab_anchor_bolt is not None:
            f = self.find_function_reference(main.tab_list(), "Anchor Bolt")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    try:
                        val = str(main.get_values_for_design_pref(i[0], input_dictionary))
                    except KeyError:
                        val = str(i[4]) if i[4] is not None else ''
                    base_anchor_bolt_dictionary.update({i[0]: val})

            for children in tab_anchor_bolt.findChildren(QWidget):
                if children.objectName() in base_anchor_bolt_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(base_anchor_bolt_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(base_anchor_bolt_dictionary[children.objectName()])
                    else:
                        pass
        
        # For Column Design, Simply Supported, Cantiliver, Plate Girder
        if tab_optimization is not None:
            f = self.find_function_reference(main.tab_list(), "Optimization")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    try:
                        val = str(main.get_values_for_design_pref(i[0], input_dictionary))
                    except KeyError:
                        val = str(i[4]) if i[4] is not None else ''
                    optimization_dictionary.update({i[0]: val})

            for children in tab_optimization.findChildren(QWidget):
                if children.objectName() in optimization_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(optimization_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(optimization_dictionary[children.objectName()])
                    else:
                        pass
        
        # For Plate Girder
        if tab_stiffeners is not None:
            f = self.find_function_reference(main.tab_list(), "Stiffeners")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    try:
                        val = str(main.get_values_for_design_pref(i[0], input_dictionary))
                    except KeyError:
                        val = str(i[4]) if i[4] is not None else ''
                    stiffeners_dictionary.update({i[0]: val})

            for children in tab_stiffeners.findChildren(QWidget):
                if children.objectName() in stiffeners_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(stiffeners_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(stiffeners_dictionary[children.objectName()])
                    else:
                        pass
        
        # For Plate Girder
        if tab_additional_pg is not None:
            f = self.find_function_reference(main.tab_list(), "Additional Girder Data")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    try:
                        val = str(main.get_values_for_design_pref(i[0], input_dictionary))
                    except KeyError:
                        val = str(i[4]) if i[4] is not None else ''
                    additional_pg_dictionary.update({i[0]: val})

            for children in tab_additional_pg.findChildren(QWidget):
                if children.objectName() in additional_pg_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(additional_pg_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(additional_pg_dictionary[children.objectName()])
                    else:
                        pass
        
        # For Plate Girder
        if tab_deflection is not None:
            f = self.find_function_reference(main.tab_list(), "Deflection")
            for i in f(input_dictionary):
                if i[2] in [TYPE_TEXTBOX, TYPE_COMBOBOX]:
                    try:
                        val = str(main.get_values_for_design_pref(i[0], input_dictionary))
                    except KeyError:
                        val = str(i[4]) if i[4] is not None else ''
                    deflection_dictionary.update({i[0]: val})

            for children in tab_deflection.findChildren(QWidget):
                if children.objectName() in deflection_dictionary.keys():
                    if type(children) == QLineEdit:
                        children.setText(deflection_dictionary[children.objectName()])
                    elif type(children) == QComboBox:
                        children.setCurrentText(deflection_dictionary[children.objectName()])
                    else:
                        pass

    # find function reference
    def find_function_reference(self, list, tab_name):
        for i in list:
            if i[0] == tab_name:
                return i[2]

    def highlight_slipfactor_description(self):
        """Highlight the description of currosponding slipfactor on selection of inputs
        Note : This routine is not in use in current version
        :return:
        """
        slip_factor = str(self.ui.combo_slipfactor.currentText())
        self.textCursor = QTextCursor(self.ui.textBrowser.document())
        cursor = self.textCursor
        # Setup the desired format for matches
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("red")))
        # Setup the regex engine
        pattern = str(slip_factor)
        regex = QRegularExpression(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.ui.textBrowser.toPlainText(), pos)
        while (index != -1):
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfLine, 1)
            # cursor.movePosition(QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.ui.textBrowser.toPlainText(), pos)


    def fu_fy_validation_connect(self, fu_fy_list, f, m):
        f.textChanged.connect(lambda: self.fu_fy_validation(fu_fy_list, f, m))

    def fu_fy_validation(self, fu_fy_list, textbox, material_key):
        self.window_close_flag = False
        # self.rejected.disconnect()
        # self.rejected.connect(self.closeEvent_accept)
        #print(fu_fy_list[0].text(), fu_fy_list[1].text())
        if "" not in [fu_fy_list[0].text(), fu_fy_list[1].text()]:
            fu = float(fu_fy_list[0].text())
            fy = float(fu_fy_list[1].text())
            material = material_key.currentText()

        else:
            textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: black;")
            return

        if fu and fy:
            if 'Ultimate_Strength' in textbox.objectName():

                if fu < 290 or fu > 639:
                    textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: red;")
                    self.window_close_flag = False
                    self.rejected.connect(self.closeEvent)
                    return
                else:

                    fu_limits = self.get_limits_for_fu(str(material))

                    if fu_limits['lower'] <= fu <= fu_limits['upper']:
                        textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: black;")
                        self.window_close_flag = True
                        self.rejected.connect(self.closeEvent)
                        return
                    else:
                        textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: red;")
                        self.window_close_flag = False
                        self.rejected.connect(self.closeEvent)
                        return

            if 'Yield_Strength' in textbox.objectName():
                if fy < 165 or fy > 499:
                    textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: red;")
                    self.window_close_flag = False
                    self.rejected.connect(self.closeEvent)
                    return

                else:

                    fy_limits = self.get_limits_for_fy(str(material))
                    if fy_limits['lower'] <= fy <= fy_limits['upper']:
                        textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: black;")
                        self.window_close_flag = True
                        self.rejected.connect(self.closeEvent)
                        return
                    else:
                        textbox.setStyleSheet("border: 1 px; border-style: solid; border-color: red;")
                        self.window_close_flag = False
                        self.rejected.connect(self.closeEvent)
                        return

    def get_limits_for_fu(self, material_grade):

        lower_fu = {'E 165 (Fe 290)': 290,
                    'E 250 (Fe 410 W)A': 410,
                    'E 250 (Fe 410 W)B': 410,
                    'E 250 (Fe 410 W)C': 410,
                    'E 300 (Fe 440)': 440,
                    'E 350 (Fe 490)': 490,
                    'E 410 (Fe 540)': 540,
                    'E 450 (Fe 570)D': 570,
                    'E 450 (Fe 590) E': 590}[material_grade]

        upper_fu = {'E 165 (Fe 290)': 409,
                    'E 250 (Fe 410 W)A': 439,
                    'E 250 (Fe 410 W)B': 439,
                    'E 250 (Fe 410 W)C': 439,
                    'E 300 (Fe 440)': 489,
                    'E 350 (Fe 490)': 539,
                    'E 410 (Fe 540)': 569,
                    'E 450 (Fe 570)D': 589,
                    'E 450 (Fe 590) E': 639}[material_grade]

        return {'lower': lower_fu, 'upper': upper_fu}

    def get_limits_for_fy(self, material_grade):

        lower_fy = {'E 165 (Fe 290)': 165,
                    'E 250 (Fe 410 W)A': 230,
                    'E 250 (Fe 410 W)B': 230,
                    'E 250 (Fe 410 W)C': 230,
                    'E 300 (Fe 440)': 280,
                    'E 350 (Fe 490)': 320,
                    'E 410 (Fe 540)': 380,
                    'E 450 (Fe 570)D': 420,
                    'E 450 (Fe 590) E': 420}[material_grade]

        upper_fy = {'E 165 (Fe 290)': 249,
                    'E 250 (Fe 410 W)A': 299,
                    'E 250 (Fe 410 W)B': 299,
                    'E 250 (Fe 410 W)C': 299,
                    'E 300 (Fe 440)': 349,
                    'E 350 (Fe 490)': 409,
                    'E 410 (Fe 540)': 449,
                    'E 450 (Fe 570)D': 499,
                    'E 450 (Fe 590) E': 499}[material_grade]

        return {'lower': lower_fy, 'upper': upper_fy}

    def closeEvent(self, event):
        if self.window_close_flag:
            event.accept()
            # self.module_window.prev_inputs = self.module_window.input_dock_inputs
        else:
            CustomMessageBox(
                title="Error",
                text=f"Select correct values for fu and fy!",
                dialogType=MessageBoxType.Warning,
            ).exec()
            event.ignore()

    def close_designPref(self):
        self.ui.accept()