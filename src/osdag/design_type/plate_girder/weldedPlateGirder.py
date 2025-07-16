"""

@Author:    Rutvik Joshi - Osdag Team, IIT Bombay [(P) rutvikjoshi63@gmail.com / 30005086@iitb.ac.in]
12.03.2025
Revised Design for GUI: Parth Karia - Osdag Team, IIT Bombay [30006096@iitb.ac.in]

@Module - Beam Design- Simply Supported member
           - Laterally Supported Beam [Moment + Shear]
           - Laterally Unsupported Beam [Moment + Shear]


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               4) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

other          8)
references     9)

"""
import logging
import math
import numpy as np
from pyswarms.single.global_best import GlobalBestPSO
from ...Common import *
# from ..connection.moment_connection import MomentConnection
from ...utils.common.material import *
from ...utils.common.load import Load
from ...utils.common.component import ISection, Material
from ...utils.common.component import *
from ..member import Member
from ...Report_functions import *
from ...design_report.reportGenerator_latex import CreateLatex
from ...utils.common.common_calculation import *
from ..tension_member import *
from ...utils.common.Section_Properties_Calculator import BBAngle_Properties
from ...utils.common import is800_2007
from ...utils.common.component import *
from osdag.cad.items.plate import Plate
from ...utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties


#GUI TO SELECT CUSTOM IN DESIGN PREFERENCES
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QFormLayout,
    QApplication, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import re
import sys

scale = 1  # For resizing components

class RangeInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Range Input")
        self.setFixedSize(350, 200)
        self.set_styles()

        self.values = []

        self.lower_input = QLineEdit()
        self.upper_input = QLineEdit()
        self.step_input = QLineEdit()

        for widget in [self.lower_input, self.upper_input, self.step_input]:
            widget.setFont(QFont("Segoe UI", 11))  # Slightly larger font
            widget.setFixedHeight(32)              # Increased height

        # Form layout
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)

        lower_label = QLabel("Lower Bound:")
        upper_label = QLabel("Upper Bound:")
        step_label = QLabel("Step:")

        for label in [lower_label, upper_label, step_label]:
            label.setFont(QFont("Segoe UI", 10))

        form_layout.addRow(lower_label, self.lower_input)
        form_layout.addRow(upper_label, self.upper_input)
        form_layout.addRow(step_label, self.step_input)

        self.submit_button = QPushButton("Add")
        self.submit_button.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.submit_button.clicked.connect(self.validate_and_submit)

        form_layout.addRow(self.submit_button)
        self.setLayout(form_layout)

    def set_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 10pt;
            }
            QLineEdit {
                font-size: 11pt;
                padding: 4px 6px;
                border: 1px solid #aaa;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #814c4c;
                color: white;
                font-size: 10pt;
                font-weight: bold;
                height: 28px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #a05c5c;
            }
        """)

    def validate_and_submit(self):
        lower_text = self.lower_input.text().strip()
        upper_text = self.upper_input.text().strip()
        step_text = self.step_input.text().strip()

        if not lower_text or not upper_text or not step_text:
            self.show_error("All fields must be filled.")
            return

        try:
            lower = float(lower_text)
            upper = float(upper_text)
            step = float(step_text)

            if step <= 0:
                self.show_error("Step must be greater than 0.")
                return

            self.values = [lower, upper, step]
            self.accept()

        except ValueError:
            self.show_error("Please enter valid numeric values.")

    def show_error(self, message):
        QMessageBox.warning(self, "Input Error", message)

    def get_values(self):
        return self.values
    

class My_ListWidget(QListWidget):
    def addItems(self, Iterable, p_str=None):
        super().addItems(Iterable)
        self.sortItems()

    def addItem(self, *__args):
        super().addItem(My_ListWidgetItem(__args[0]))
        self.sortItems()

class My_ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        try:
            self_text = str(re.sub("[^0-9.]", "", self.text()))
            other_text = str(re.sub("[^0-9.]", "", other.text()))
            return float(self_text) < float(other_text)
        except Exception:
            return super().__lt__(other)

class PopupDialog(QDialog):
    def __init__(self, disabled_values=[], note="", parent=None):
        super().__init__(parent)
        self.disabled_values = disabled_values
        self.note = note
        self.setWindowTitle("Customized")
        self.resize(int(scale*540), int(scale*470))
        self.init_ui()
        self.set_styles()

    def init_ui(self):
        self.label = QtWidgets.QLabel("Available:", self)
        self.label.setGeometry(QtCore.QRect(20, 20, 150, 30))

        self.label_2 = QtWidgets.QLabel("Selected:", self)
        self.label_2.setGeometry(QtCore.QRect(int(scale * 320), 20, 150, 30))

        self.listWidget = My_ListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(20, 50, int(scale*180), int(scale*300)))
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.itemDoubleClicked.connect(self.move_to_selected)

        self.listWidget_2 = My_ListWidget(self)
        self.listWidget_2.setGeometry(QtCore.QRect(int(scale*320), 50, int(scale*180), int(scale*300)))
        self.listWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_2.itemDoubleClicked.connect(self.move_to_available)

        self.pushButton = QtWidgets.QPushButton(">>", self)
        self.pushButton.setGeometry(QtCore.QRect(int(scale*225), int(scale*140), int(scale*70), int(scale*30)))

        self.pushButton_2 = QtWidgets.QPushButton(">", self)
        self.pushButton_2.setGeometry(QtCore.QRect(int(scale*225), int(scale*180), int(scale*70), int(scale*30)))

        self.pushButton_3 = QtWidgets.QPushButton("<", self)
        self.pushButton_3.setGeometry(QtCore.QRect(int(scale*225), int(scale*220), int(scale*70), int(scale*30)))

        self.pushButton_4 = QtWidgets.QPushButton("<<", self)
        self.pushButton_4.setGeometry(QtCore.QRect(int(scale*225), int(scale*260), int(scale*70), int(scale*30)))

        self.pushButton_5 = QtWidgets.QPushButton("Submit", self)
        self.pushButton_5.setGeometry(QtCore.QRect(int(scale*190), int(scale*400), int(scale*140), int(scale*35)))
        self.pushButton_5.setDefault(True)

        self.pushButton.clicked.connect(self.move_all_to_selected)
        self.pushButton_2.clicked.connect(self.move_selected_to_selected)
        self.pushButton_3.clicked.connect(self.move_selected_to_available)
        self.pushButton_4.clicked.connect(self.move_all_to_available)
        self.pushButton_5.clicked.connect(self.accept)

        self.listWidget.itemSelectionChanged.connect(self.update_buttons_status)
        self.listWidget_2.itemSelectionChanged.connect(self.update_buttons_status)

        self.update_buttons_status()

    def update_buttons_status(self):
        self.pushButton_2.setDisabled(not bool(self.listWidget.selectedItems()))
        self.pushButton_3.setDisabled(not bool(self.listWidget_2.selectedItems()))

    def move_selected_to_selected(self):
        for item in self.listWidget.selectedItems():
            self.listWidget_2.addItem(item.text())
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

    def move_selected_to_available(self):
        for item in self.listWidget_2.selectedItems():
            self.listWidget.addItem(item.text())
        for item in self.listWidget_2.selectedItems():
            self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def move_all_to_selected(self):
        while self.listWidget.count() > 0:
            self.listWidget_2.addItem(self.listWidget.takeItem(0).text())

    def move_all_to_available(self):
        while self.listWidget_2.count() > 0:
            self.listWidget.addItem(self.listWidget_2.takeItem(0).text())

    def move_to_selected(self, item):
        self.listWidget_2.addItem(item.text())
        self.listWidget.takeItem(self.listWidget.row(item))

    def move_to_available(self, item):
        self.listWidget.addItem(item.text())
        self.listWidget_2.takeItem(self.listWidget_2.row(item))

    def get_selected_items(self):
        return [self.listWidget_2.item(i).text() for i in range(self.listWidget_2.count())]

    def set_styles(self):
        brown = "#925a5b"
        grey = "#8e8e8e"
        white = "#ffffff"

        button_style = f"""
        QPushButton {{
            background-color: {brown};
            color: {white};
            border-radius: 6px;
            font-size: 22px;
            padding: 6px 18px;
            border: none;
        }}
        QPushButton:disabled {{
            background-color: {grey};
            color: {white};
        }}
        """
        for btn in [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.pushButton_5]:
            btn.setStyleSheet(button_style)

        list_item_style = """
        QListWidget::item {
            font-size: 24px;
            color: black;
            margin: 2px 0px;
        }
        """
        scrollbar_style = f"""
        QScrollBar:vertical {{
            border: none;
            background: #f5f5f5;
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:vertical {{
            background: {grey};
            min-height: 20px;
            border-radius: 6px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            background: none;
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QScrollBar:horizontal {{
            height: 0px;
        }}
        """
        self.listWidget.setStyleSheet(list_item_style + scrollbar_style)
        self.listWidget_2.setStyleSheet(list_item_style + scrollbar_style)








class PlateGirderWelded(Member):
    int_thicklist = []
    long_thicklist = []

    def __init__(self):
        super(PlateGirderWelded, self).__init__()
        self.design_status = False
        
        

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):

        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """
        tabs = []

        t1 = (KEY_DISP_GIRDERSEC, TYPE_TAB_1, self.tab_girder_sec)
        tabs.append(t1)

        t5 = ("Optimisation", TYPE_TAB_2, self.optimization_tab_welded_plate_girder_design)
        tabs.append(t5)

        t1 = ("Stiffeners", TYPE_TAB_2, self.Stiffener_design)
        tabs.append(t1)

        t1 = ("Additional Girder Data", TYPE_TAB_2, self.girder_geometry)
        tabs.append(t1)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        t6 = ("Deflection"  , TYPE_TAB_2, self.deflection_values)
        tabs.append(t6)

        return tabs
    
    def tab_value_changed(self):
        change_tab = []

        t1 = (KEY_DISP_GIRDERSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section_plate_girder)
        change_tab.append(t1)

        t4 = (KEY_DISP_GIRDERSEC, ['Label_6', 'Label_7', 'Label_8', 'Label_9', 'Label_10', 'Label_11'],
              ['Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20', 'Label_21', 'Label_22','Label_23'], TYPE_TEXTBOX, self.Unsymm_I_Section_properties)
        change_tab.append(t4)

        t9 = ("Deflection", [KEY_STR_TYPE], [KEY_MEMBER_OPTIONS], TYPE_COMBOBOX, self.member_options_change)
        change_tab.append(t9)
        t9 = ("Deflection", [KEY_MEMBER_OPTIONS], [KEY_SUPPORTING_OPTIONS], TYPE_COMBOBOX, self.supp_options_change)
        change_tab.append(t9)
        t9 = ("Deflection", [KEY_STR_TYPE,KEY_DESIGN_LOAD,KEY_MEMBER_OPTIONS,KEY_SUPPORTING_OPTIONS], [KEY_MAX_DEFL], TYPE_TEXTBOX, self.max_defl_change)
        change_tab.append(t9)
        t10 = ("Stiffeners", [KEY_IntermediateStiffener_thickness], [KEY_IntermediateStiffener_thickness_val], TYPE_COMBOBOX, self.Int_stiffener_thickness_customized)
        change_tab.append(t10)
        t11 = ("Stiffeners", [KEY_LongitudnalStiffener_thickness], [KEY_LongitudnalStiffener_thickness_val], TYPE_COMBOBOX, self.Long_stiffener_thickness_customized)
        change_tab.append(t11)

        
        # t10 = ('Stiffeners',[KEY_WEB_PHILOSOPHY],[KEY_IntermediateStiffener_spacing],TYPE_TEXTBOX,self.Intm_stiffener_spacing_change)
        # change_tab.append(t10)



        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
                Not required for this module but empty list should be passed"""
        return []

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t1 = (KEY_DISP_GIRDERSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])#Need to check
        design_input.append(t1)
        
        t1 = (KEY_DISP_GIRDERSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        design_input.append(t1)

        t2 = ("Optimisation", TYPE_TEXTBOX, [KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE])  # , KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Optimisation", TYPE_COMBOBOX, [KEY_ALLOW_CLASS, KEY_LOAD])  # , KEY_STEEL_COST
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_COMBOBOX, [KEY_IntermediateStiffener,KEY_LongitudnalStiffener,KEY_IntermediateStiffener_thickness,KEY_LongitudnalStiffener_thickness])
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_TEXTBOX, [KEY_IntermediateStiffener_spacing])
        design_input.append(t2)

        t2 = ("Stiffeners", TYPE_COMBOBOX, [KEY_ShearBucklingOption,KEY_IntermediateStiffener_thickness_val,KEY_LongitudnalStiffener_thickness_val])
        design_input.append(t2)

        t2 = ("Additional Girder Data", TYPE_COMBOBOX, [KEY_IS_IT_SYMMETRIC])
        design_input.append(t2)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Deflection",TYPE_COMBOBOX, [KEY_STR_TYPE,KEY_DESIGN_LOAD,KEY_MEMBER_OPTIONS,KEY_SUPPORTING_OPTIONS]) 
        design_input.append(t7)
        t7 = ("Deflection",TYPE_TEXTBOX, [KEY_MAX_DEFL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):

        design_input = []

        t2 = (KEY_MATERIAL, [KEY_DP_DESIGN_METHOD], 'Input Dock')
        design_input.append(t2)

        t2 = (None, [KEY_ALLOW_CLASS, KEY_EFFECTIVE_AREA_PARA, KEY_LENGTH_OVERWRITE, KEY_LOAD, KEY_DP_DESIGN_METHOD,KEY_STR_TYPE,KEY_DESIGN_LOAD,KEY_MEMBER_OPTIONS,KEY_MAX_DEFL,
                     KEY_SUPPORTING_OPTIONS,KEY_ShearBucklingOption, KEY_IntermediateStiffener_spacing, KEY_IntermediateStiffener,KEY_LongitudnalStiffener,KEY_IntermediateStiffener_thickness_val,KEY_LongitudnalStiffener_thickness_val,
                     KEY_IntermediateStiffener_thickness,KEY_LongitudnalStiffener_thickness, KEY_IS_IT_SYMMETRIC], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):

        add_buttons = []

        return add_buttons

    def get_values_for_design_pref(self, key, design_dictionary):
        # if design_dictionary[KEY_MATERIAL] != 'Select Material':
        #     material = Material(design_dictionary[KEY_MATERIAL], 41)
        #     material_grade = design_dictionary[KEY_MATERIAL]
        #     fu = material.fu
        #     fy = material.fy
        # else:
        #     fu = ''
        #     fy = ''

            

        val = {
            KEY_ALLOW_CLASS: 'Yes',
            KEY_EFFECTIVE_AREA_PARA: '1.0',
            KEY_LENGTH_OVERWRITE: 'NA',
            KEY_LOAD: 'Normal',
            KEY_DP_DESIGN_METHOD: "Limit State Design",
            KEY_ShearBucklingOption: KEY_DISP_SB_Option[0],
            KEY_IS_IT_SYMMETRIC: 'Symmetrical',
            KEY_IntermediateStiffener_spacing:'NA',
            KEY_IntermediateStiffener: 'No',
            KEY_IntermediateStiffener_thickness:'All',
            KEY_LongitudnalStiffener: 'Yes and 1 stiffener',
            KEY_LongitudnalStiffener_thickness:'All',
            KEY_STR_TYPE:'Highway Bridge',
            KEY_DESIGN_LOAD:'Live Load',
            KEY_MEMBER_OPTIONS :'Simple Span',
            KEY_SUPPORTING_OPTIONS: 'NA',
            KEY_MAX_DEFL : 'Span/600',
            KEY_IntermediateStiffener_thickness_val : VALUES_STIFFENER_THICKNESS,
            KEY_LongitudnalStiffener_thickness_val : VALUES_STIFFENER_THICKNESS
        }[key]

        return val
    def member_options_change(self):
        if self[0] == KEY_DISP_STR_TYP3:
            return {KEY_MEMBER_OPTIONS : VALUES_MEMBER_OPTIONS[1]}
        elif self[0] == KEY_DISP_STR_TYP4:
            return {KEY_MEMBER_OPTIONS :VALUES_MEMBER_OPTIONS[2]}
        else:
            return {KEY_MEMBER_OPTIONS : VALUES_MEMBER_OPTIONS[0]}
        

    def supp_options_change(self):
        if self[0] in ['Purlin and Girts', 'Simple span', 'Cantilever span']:
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_PSC}
        elif self[0]  == 'Rafter Supporting':
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_RS}
        elif self[0]  == 'Gantry':
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_GNT}
        elif self[0] in  ['Floor and roof', 'Cantilever']:
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_FRC}
        else:
            return {KEY_SUPPORTING_OPTIONS : VALUES_SUPPORTING_OPTIONS_DEF}

    def max_defl_change(self):
        if self[0] in ['Highway Bridge','Railway Bridge']:
            if self[2] == 'Simple Span':
                if self[1] == 'Live load':
                    return {KEY_MAX_DEFL :VALUES_MAX_DEFL[0]}
                elif self[1] == 'Dead load':
                    return  {KEY_MAX_DEFL : VALUES_MAX_DEFL[1]}
                else:
                    return {KEY_MAX_DEFL : 'NA'}
                    
            else:
                if self[1] == 'Live load':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[2]}
                elif self[1] == 'Dead load':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[1]}
                else:
                    return {KEY_MAX_DEFL : 'NA'}
                
        elif self[0] == 'Other Building':
            if self[1] == 'Live load':
                if self[2] == 'Floor and roof':
                    if self[3] == 'Elements not susceptible to cracking':
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[3]}
                    else:
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[4]}
                else:
                    if self[3] == 'Elements not susceptible to cracking':
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[5]}
                    else:
                        return {KEY_MAX_DEFL : VALUES_MAX_DEFL[6]}
            else:
                return {KEY_MAX_DEFL : 'NA'}
        else:
            if self[2] == 'Purlin and Girts' and self[1] == 'Live load':
                if self[3] == 'Elastic cladding':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[5]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[6]}
            elif self[2] == 'Simple span' and self[1] == 'Live load':
                if self[3] == 'Elastic cladding':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[7]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[3]}
            elif self[2] == 'Cantilever span' and self[1] == 'Live load':
                if self[3] == 'Elastic cladding':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[8]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[5]}
            elif self[2] == 'Rafter Supporting' and self[1] == 'Live load':
                if self[3] == 'Profiled Metal sheeting':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[6]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[7]}
            elif self[2] == 'Gantry' and self[1] == 'Live load':
                if self[1] == 'Crane Load(Manual operation)':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[9]}
                elif self[1] == 'Crane load(Electric operation up to 50t)':
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[10]}
                else:
                    return {KEY_MAX_DEFL : VALUES_MAX_DEFL[11]}
            else:
                return {KEY_MAX_DEFL : 'NA'}
            
    def Int_stiffener_thickness_customized(self):
        selected_items = []
        if self[0] == 'All':
            return {KEY_IntermediateStiffener_thickness_val : VALUES_STIFFENER_THICKNESS}
        else:
            popup = PopupDialog()
            popup.listWidget.addItems(VALUES_STIFFENER_THICKNESS)  # Set available items
            if popup.exec_() == QDialog.Accepted:
                selected_items = popup.get_selected_items()
            # print("Selected:", selected_items)
            PlateGirderWelded.int_thicklist = selected_items
            return {KEY_IntermediateStiffener_thickness_val : selected_items}                                 
            
    def Long_stiffener_thickness_customized(self):
        selected_items2 = []
        if self[0] == 'All':
            return {KEY_LongitudnalStiffener_thickness_val : VALUES_STIFFENER_THICKNESS}
        else:
            popup = PopupDialog()
            popup.listWidget.addItems(VALUES_STIFFENER_THICKNESS)  # Set available items
            if popup.exec_() == QDialog.Accepted:
                selected_items2 = popup.get_selected_items()
            # print("Selected:", selected_items2)
            PlateGirderWelded.long_thicklist = selected_items2
            return {KEY_LongitudnalStiffener_thickness_val : selected_items2}

    ####################################
    # Design Preference Functions End
    ####################################
    # Setting up logger and Input and Output Docks
    ####################################
    def module_name(self):
        print('in module')
        return KEY_DISP_PLATE_GIRDER_WELDED


    def set_osdaglogger(key):
        """
        Set logger for Column Design Module.
        """
        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def customized_input(self):

        c_lst = []
        # t1 = (KEY_SECSIZE, self.fn_profile_section)
        # c_lst.append(t1)
        t1 = (KEY_TOP_FLANGE_THICKNESS_PG, self.plate_thick_customized)
        c_lst.append(t1)

        t2 = (KEY_BOTTOM_FLANGE_THICKNESS_PG, self.plate_thick_customized)
        c_lst.append(t2)

        t3= (KEY_WEB_THICKNESS_PG, self.plate_thick_customized)
        c_lst.append(t3)

        # t4 = (KEY_LongitudnalStiffener_thickness,self.long_stf_thk_customized)
        # c_lst.append(t4)
        return c_lst



    def input_values(self):

        self.module = KEY_DISP_PLATE_GIRDER_WELDED
        options_list = []

        t1 = (None, KEY_DISP_PG_SectionDetail, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t1 = (KEY_MODULE, KEY_DISP_PLATE_GIRDER_WELDED, TYPE_MODULE, None, True, "No Validator")
        options_list.append(t1)

        t4 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t4)

        t2 = (KEY_OVERALL_DEPTH_PG_TYPE, KEY_DISP_OVERALL_DEPTH_PG_TYPE, TYPE_COMBOBOX, VALUES_DEPTH_PG, True, 'No Validator')
        options_list.append(t2)
        t33 = (KEY_OVERALL_DEPTH_PG, KEY_DISP_OVERALL_DEPTH_PG, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t33)

        t4 = (KEY_WEB_THICKNESS_PG, KEY_DISP_WEB_THICKNESS_PG, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True,
              'Int Validator')
        options_list.append(t4)

        # t2 = (KEY_TOP_Bflange_PG_Type, KEY_DISP_TOP_Bflange_PG_Type, TYPE_COMBOBOX, VALUES_DEPTH_PG, True, 'No Validator')
        # options_list.append(t2)

        t2 = (KEY_TOP_Bflange_PG, KEY_DISP_TOP_Bflange_PG, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t2)

        t4 = (KEY_TOP_FLANGE_THICKNESS_PG, KEY_DISP_TOP_FLANGE_THICKNESS_PG, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True, 'Int Validator')
        options_list.append(t4)

        # t2 = (KEY_BOTTOM_Bflange_PG_Type, KEY_DISP_BOTTOM_Bflange_PG_Type, TYPE_COMBOBOX, VALUES_DEPTH_PG, True, 'No Validator')
        # options_list.append(t2)
        t22 = (KEY_BOTTOM_Bflange_PG, KEY_DISP_BOTTOM_Bflange_PG, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t22)

        t4 = (KEY_BOTTOM_FLANGE_THICKNESS_PG, KEY_DISP_BOTTOM_FLANGE_THICKNESS_PG, TYPE_COMBOBOX_CUSTOMIZED, VALUES_PLATETHK, True,
              'No Validator')
        options_list.append(t4)

        t2 = (KEY_LENGTH, KEY_DISP_LENGTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t2)

        t1 = (None, KEY_DISP_SECTION_DATA_PG, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (
            KEY_DESIGN_TYPE_FLEXURE,
            KEY_BEAM_SUPP_TYPE,
            TYPE_COMBOBOX,
            VALUES_SUPP_TYPE_temp,
            True,
            "No Validator",
        )
        options_list.append(t2)

        #t4 = (KEY_STR_TYPE, KEY_DISP_STR_TYPE, TYPE_COMBOBOX, KEY_DISP_STR_TYPE_list, True, 'No Validator')
        #options_list.append(t4)
        t5 = (KEY_SUPPORT_WIDTH, KEY_DISP_SUPPORT_WIDTH, TYPE_TEXTBOX, None, True, 'Int Validator')
        options_list.append(t5)

        t4 = (KEY_WEB_PHILOSOPHY, KEY_DISP_WEB_PHILOSOPHY, TYPE_COMBOBOX, WEB_PHILOSOPHY_list, True, 'No Validator')
        options_list.append(t4)

        t10 = (KEY_TORSIONAL_RES, DISP_TORSIONAL_RES, TYPE_COMBOBOX, Torsion_Restraint_list, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_WARPING_RES, DISP_WARPING_RES, TYPE_COMBOBOX, Warping_Restraint_list, True, 'No Validator')
        options_list.append(t11)

        t7 = (None, KEY_LOADING, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        t8 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t8)

        t8= (KEY_BENDING_MOMENT_SHAPE, KEY_DISP_BENDING_MOMENT_SHAPE, TYPE_COMBOBOX, Bending_moment_shape_list, True,
             'No Validator' )
        options_list.append(t8)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE_BIGGER, VALUES_IMAGE_PLATEGIRDER[0], True,'No Validator')
        options_list.append(t15)
        return options_list

    def fn_torsion_warping(self):
        print( 'Inside fn_torsion_warping', self)
        if self[0] == Torsion_Restraint1:
            return Warping_Restraint_list
        elif self[0] == Torsion_Restraint2:
            return [Warping_Restraint5]
        else:
            return [Warping_Restraint5]

    def axis_bending_change(self):
        design = self[0]
        print( 'Inside fn_supp_image', self)
        if self[0] == KEY_DISP_DESIGN_TYPE_FLEXURE:
            return ['NA']
        else:
            return VALUES_BENDING_TYPE
        
    def fn_conn_image(self):

        "Function to populate section images based on the type of section "
        img = self[0]
        if img == Bending_moment_shape_list[0]:
            return VALUES_IMAGE_PLATEGIRDER[0]
        elif img ==Bending_moment_shape_list[1]:
            return VALUES_IMAGE_PLATEGIRDER[1]
        elif img ==Bending_moment_shape_list[2]:
            return VALUES_IMAGE_PLATEGIRDER[2]
        elif img ==Bending_moment_shape_list[3]:
            return VALUES_IMAGE_PLATEGIRDER[3]
        else:
            return VALUES_IMAGE_PLATEGIRDER[4]
        
    def customized_dimensions(self):
        conn = self[0]
        if conn == "Customized":
            return KEY_DISP_OVERALL_DEPTH_PG
        else:
            return ''
    
    def customized_dimensions_1(self):
        conn = self[0]
        if conn == "Customized":
            return KEY_DISP_TOP_Bflange_PG
        else:
            return ''
        
    def customized_dimensions_2(self):
        conn = self[0]
        if conn == "Customized":
            return KEY_DISP_BOTTOM_Bflange_PG
        else:
            return ''

    def customized_dims(self):
        conn = self[0]
        if conn == "Customized":
            return True
        else:
            return False
    def customized_options(self):
        conn = self[0]
        if conn == "Customized":
            return VALUES_PLATETHK
        else:
            return VALUES_OPT
        

    def input_value_changed(self):

        lst = []
        t1 = ([KEY_BENDING_MOMENT_SHAPE], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t1)

        t3 = ([KEY_TORSIONAL_RES], KEY_WARPING_RES, TYPE_COMBOBOX, self.fn_torsion_warping)
        lst.append(t3)

        t44 = ([KEY_OVERALL_DEPTH_PG_TYPE],KEY_OVERALL_DEPTH_PG, TYPE_LABEL, self.customized_dimensions)
        lst.append(t44)
        t45 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_OVERALL_DEPTH_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t45)
        # t46 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_WEB_THICKNESS_PG, TYPE_COMBOBOX, self.customized_options)
        # lst.append(t46)

        t2 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_Bflange_PG, TYPE_LABEL, self.customized_dimensions_1)
        lst.append(t2)
        t3 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_Bflange_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t3)
        # t47 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, self.customized_options)
        # lst.append(t47)

        t23 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_Bflange_PG, TYPE_LABEL, self.customized_dimensions_2)
        lst.append(t23)
        t24 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_Bflange_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t24)
        # t47 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, self.customized_options)
        # lst.append(t47)

        t3 = ([KEY_MATERIAL], KEY_MATERIAL, TYPE_CUSTOM_MATERIAL, self.new_material)
        lst.append(t3)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_T_constatnt, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_T_constatnt, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_W_constatnt, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_W_constatnt, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_IMPERFECTION_FACTOR_LTB, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_IMPERFECTION_FACTOR_LTB, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_SR_FACTOR_LTB, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_SR_FACTOR_LTB, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_NON_DIM_ESR_LTB, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_NON_DIM_ESR_LTB, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_DESIGN_STRENGTH_COMPRESSION, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_DESIGN_STRENGTH_COMPRESSION, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_Elastic_CM, TYPE_OUT_LABEL, self.output_modifier)
        lst.append(t18)

        t18 = ([KEY_DESIGN_TYPE_FLEXURE],
               KEY_Elastic_CM, TYPE_OUT_DOCK, self.output_modifier)
        lst.append(t18)

        t19 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_thickness,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t19)

        t20 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_thickness,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t20)

        t21 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_thickness,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t21)

        t22 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_thickness,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t22)

        t23 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_spacing,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t23)

        t24 = ([KEY_WEB_PHILOSOPHY],KEY_IntermediateStiffener_spacing,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t24)

        t25 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_numbers,TYPE_OUT_LABEL,self.output_modifier2)
        lst.append(t25)

        t26 = ([KEY_WEB_PHILOSOPHY],KEY_LongitudnalStiffener_numbers,TYPE_OUT_DOCK,self.output_modifier2)
        lst.append(t26)

        return lst

    def warning_majorbending(self):
        print(self)
        if self[0] == VALUES_SUPP_TYPE_temp[2]:
            return True
        # elif self[0] == VALUES_SUPP_TYPE_temp[0] or self[0] == VALUES_SUPP_TYPE_temp[1] :
        #     return True
        else:
            return False

    def output_modifier(self):
        print(self)
        if self[0] == VALUES_SUPP_TYPE_temp[2]:
            return False
        # elif self[0] == VALUES_SUPP_TYPE_temp[0] or self[0] == VALUES_SUPP_TYPE_temp[1] :
        #     return True
        else:
            return True
        
    def output_modifier2(self):
        print(self)
        if self[0] == 'Thin Web with ITS':
            return False
        # elif self[0] == VALUES_SUPP_TYPE_temp[0] or self[0] == VALUES_SUPP_TYPE_temp[1] :
        #     return True
        else:
            return True

    def Design_pref_modifier(self):
        print("Design_pref_modifier",self)


    def output_values(self, flag):

        out_list = []

        t0 = (None, DISP_TITLE_STRUT_SECTION, TYPE_TITLE, None, True)
        out_list.append(t0)

        t1 = (KEY_TITLE_OPTIMUM_DESIGNATION, KEY_DISP_TITLE_OPTIMUM_DESIGNATION, TYPE_TEXTBOX,
              self.result_designation if flag else '', True)
        out_list.append(t1)

        t2 = (
        KEY_OPTIMUM_UR_COMPRESSION, KEY_DISP_OPTIMUM_UR_COMPRESSION, TYPE_TEXTBOX, round(self.result_UR,3) if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_OPTIMUM_SC, KEY_DISP_OPTIMUM_SC, TYPE_TEXTBOX, self.section_classification_val if flag else '', True)
        out_list.append(t3)

        t4 = (KEY_betab_constatnt,KEY_DISP_betab_constatnt, TYPE_TEXTBOX,
              self.betab if flag else '', True)
        out_list.append(t4)

        t5 = (
        KEY_EFF_SEC_AREA, KEY_DISP_EFF_SEC_AREA, TYPE_TEXTBOX, self.effectivearea if flag else '',
        True)
        out_list.append(t5)

        # t6 = (None,"Design Results" , TYPE_TITLE, None, True)
        # out_list.append(t6)

        

        

        # t9 = (None, KEY_DISP_DESIGN_STIFFER , TYPE_TITLE, None, True)
        # out_list.append(t9)

        t10 = (KEY_IntermediateStiffener_thickness, KEY_DISP_IntermediateStiffener_thickness, TYPE_TEXTBOX,
              self.intstiffener_thk if flag else '', True)
        out_list.append(t10)

        t10 = (KEY_IntermediateStiffener_spacing, KEY_DISP_IntermediateStiffener_spacing, TYPE_TEXTBOX,
              self.intstiffener_spacing if flag else '', True)
        out_list.append(t10)

        t1 = (KEY_LongitudnalStiffener_thickness, KEY_DISP_LongitudnalStiffener_thickness, TYPE_TEXTBOX,
              self.longstiffener_thk if flag else '', True)
        out_list.append(t1)

        t1 = (KEY_LongitudnalStiffener_numbers, KEY_DISP_LongitudnalStiffener_numbers, TYPE_TEXTBOX, '', True)
        out_list.append(t1)

        t2 = (KEY_EndpanelStiffener_thickness, KEY_DISP_EndpanelStiffener_thickness, TYPE_TEXTBOX,
              '', True)
        out_list.append(t2)

        t1 = (KEY_MOMENT_STRENGTH, KEY_DISP_MOMENT, TYPE_TEXTBOX,
              self.design_moment if flag else '', True)
        out_list.append(t1)

        # t1 = (None, KEY_DISP_WELD_DESIGN, TYPE_TITLE, None, True)
        # out_list.append(t1)

        t1 = (KEY_WeldWebtoflange, KEY_DISP_WeldWebtoflange, TYPE_TEXTBOX,
              '', True)
        out_list.append(t1)

        t1 = (KEY_WeldStiffenertoweb, KEY_DISP_WeldStiffenertoweb, TYPE_TEXTBOX,
              '', True)
        out_list.append(t1)

        # t1 = (None, KEY_DISP_LTB, TYPE_TITLE, None, False)
        # out_list.append(t1)

        t2 = (KEY_T_constatnt, KEY_DISP_T_constatnt, TYPE_TEXTBOX,
              self.torsion_cnst if flag else '', False)
        out_list.append(t2)

        t2 = (KEY_W_constatnt, KEY_DISP_W_constatnt, TYPE_TEXTBOX, self.warping_cnst if flag else '', False)
        out_list.append(t2)

        t2 = (
            KEY_IMPERFECTION_FACTOR_LTB, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, '',
            False)
        out_list.append(t2)

        t2 = (KEY_SR_FACTOR_LTB, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, '', False)
        out_list.append(t2)

        t2 = (KEY_NON_DIM_ESR_LTB, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, '', False)
        out_list.append(t2)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
              '', False)
        out_list.append(t1)

        t2 = (KEY_Elastic_CM, KEY_DISP_Elastic_CM, TYPE_TEXTBOX, self.critical_moment if flag else '', False)
        out_list.append(t2)

        # TODO @Rutvik: can add tab button for asthetics

        # t2 = (KEY_T_constatnt, KEY_DISP_T_constatnt, TYPE_TEXTBOX,
        #       self.result_tc if flag else '', False)
        # out_list.append(t2)

        # t2 = (KEY_W_constatnt, KEY_DISP_W_constatnt, TYPE_TEXTBOX, self.result_wc if flag else '', False)
        # out_list.append(t2)

        # t2 = (
        #     KEY_IMPERFECTION_FACTOR_LTB, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, self.result_IF_lt if flag else '',
        #     False)
        # out_list.append(t2)

        # t2 = (KEY_SR_FACTOR_LTB, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, self.result_srf_lt if flag else '', False)
        # out_list.append(t2)

        # t2 = (KEY_NON_DIM_ESR_LTB, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, self.result_nd_esr_lt if flag else '', False)
        # out_list.append(t2)

        # t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
        #       self.result_fcd__lt if flag else
        #       '', False)
        # out_list.append(t1)

        # t2 = (KEY_Elastic_CM, KEY_DISP_Elastic_CM, TYPE_TEXTBOX, self.result_mcr if flag else '', False)
        # out_list.append(t2)

        # t1 = (None, KEY_PERFORMANCE_EVALUATION, TYPE_TITLE, None, True)
        # out_list.append(t1)
        #
        # t2 = (KEY_ESR, KEY_DISP_UTILIZATION_RATION_PG , TYPE_TEXTBOX, self.result_eff_sr if flag else '', True)
        # out_list.append(t2)
        #
        # t2 = (KEY_EULER_BUCKLING_STRESS, KEY_DISP_PERMISSIBLE_PG, TYPE_TEXTBOX,
        #       self.result_ebs if flag else '', True)
        # out_list.append(t2)
        #
        # t2 = (KEY_BUCKLING_CURVE, KEY_DISP_DEFLECTION_PG, TYPE_TEXTBOX, self.result_bc if flag else '', True)
        # out_list.append(t2)

        return out_list
    def spacing(self, status):

        spacing = []

        t2 = (KEY_T_constatnt, KEY_DISP_T_constatnt, TYPE_TEXTBOX,
              self.result_tc if status else '', False)
        spacing.append(t2)

        t2 = (KEY_W_constatnt, KEY_DISP_W_constatnt, TYPE_TEXTBOX, self.result_wc if status else '', False)
        spacing.append(t2)

        t2 = (
            KEY_IMPERFECTION_FACTOR_LTB, KEY_DISP_IMPERFECTION_FACTOR, TYPE_TEXTBOX, self.result_IF_lt if status else '',
            False)
        spacing.append(t2)

        t2 = (KEY_SR_FACTOR_LTB, KEY_DISP_SR_FACTOR, TYPE_TEXTBOX, self.result_srf_lt if status else '', False)
        spacing.append(t2)

        t2 = (KEY_NON_DIM_ESR_LTB, KEY_DISP_NON_DIM_ESR, TYPE_TEXTBOX, self.result_nd_esr_lt if status else '', False)
        spacing.append(t2)

        t1 = (KEY_DESIGN_STRENGTH_COMPRESSION, KEY_DISP_COMP_STRESS, TYPE_TEXTBOX,
              self.result_fcd__lt if status else
              '', False)
        spacing.append(t1)

        t2 = (KEY_Elastic_CM, KEY_DISP_Elastic_CM, TYPE_TEXTBOX, self.result_mcr if status else '', False)
        spacing.append(t2)

        return spacing

    def func_for_validation(self, design_dictionary):
        print(f"func_for_validation here")
        all_errors = []
        self.design_status = False
        flag = False
        self.output_values(self, flag)
        flag1 = False
        flag2 = False
        flag3 = False
        option_list = self.input_values(self)
        missing_fields_list = []
        print(f'func_for_validation option_list {option_list}'
            f"\n  design_dictionary {design_dictionary}"
              )
        for option in option_list:
            if option[2] == TYPE_TEXTBOX or option[0] == KEY_LENGTH or option[0] == KEY_SHEAR or option[0] == KEY_MOMENT:
                try:
                    if design_dictionary[option[0]] == '':
                        if design_dictionary['Total.Design_Type'] == 'Optimized':
                            if design_dictionary[KEY_OVERALL_DEPTH_PG] == '' or design_dictionary[KEY_TOP_Bflange_PG] == '' or design_dictionary[KEY_BOTTOM_Bflange_PG] == '':
                                pass
                            else:
                                missing_fields_list.append(option[1])
                                continue
                                
                        else:
                            missing_fields_list.append(option[1])
                            continue
                    if option[0] == KEY_LENGTH:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)

                        else:
                            flag1 = True
                    elif option[0] == KEY_SHEAR:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag2 = True
                    elif option[0] == KEY_MOMENT:
                        if float(design_dictionary[option[0]]) <= 0.0:
                            print("Input value(s) cannot be equal or less than zero.")
                            error = "Input value(s) cannot be equal or less than zero."
                            all_errors.append(error)
                        else:
                            flag3 = True
                except:
                        error = "Input value(s) are not valid"
                        all_errors.append(error)

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
        else:
            flag = True

        if flag and flag1 and flag2 and flag3:
            print(f"\n design_dictionary{design_dictionary}")
            self.set_input_values(self, design_dictionary)
            print("WORKING VALIDATION")
            # if self.design_status ==False and len(self.failed_design_dict)>0:
            #     logger.error(
            #         "Design Failed, Check Design Report"
            #     )
            #     return # ['Design Failed, Check Design Report'] @TODO
            # elif self.design_status:
            #     pass
            # else:
            #     logger.error(
            #         "Design Failed. Selender Sections Selected"
            #     )
            #     return # ['Design Failed. Selender Sections Selected']
        else:
            return all_errors

    def get_3d_components(self):

        components = []
        t3 = ('Model', self.call_3DModel)
        components.append(t3)

        # t3 = ('Column', self.call_3DColumn)
        # components.append(t3)

        return components

    # warn if a beam of older version of IS 808 is selected
    def warn_text(self):
        """ give logger warning when a beam from the older version of IS 808 is selected """
        global logger
        red_list = red_list_function()

        if (self.sec_profile == VALUES_SEC_PROFILE[0]) or (self.sec_profile == VALUES_SEC_PROFILE[1]):  # Beams or Columns
            for section in self.sec_list:
                if section in red_list:
                    logger.warning(" : You are using a section ({}) (in red color) that is not available in latest version of IS 808".format(section))

    # Setting inputs from the input dock GUI
    def set_input_values(self, design_dictionary):
        self.module = design_dictionary[KEY_MODULE]
        self.design_type = design_dictionary[KEY_OVERALL_DEPTH_PG_TYPE]
        self.section_class = None
        if self.design_type == 'Optimized':
            self.total_depth = 1
            self.web_thickness_list = design_dictionary[KEY_WEB_THICKNESS_PG]
            self.top_flange_width = 1
            self.top_flange_thickness_list = design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG]
            self.bottom_flange_width = 1
            self.bottom_flange_thickness_list = design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG]
            #optimize the initialization for list outputs
            self.web_thickness = float(design_dictionary[KEY_WEB_THICKNESS_PG][0])
            self.top_flange_thickness = float(design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG][0])
            self.bottom_flange_thickness = float(design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG][0])
        
        else:

            self.total_depth = float(design_dictionary[KEY_OVERALL_DEPTH_PG])
            self.web_thickness = float(design_dictionary[KEY_WEB_THICKNESS_PG][0])
            self.top_flange_width = float(design_dictionary[KEY_TOP_Bflange_PG])
            self.top_flange_thickness = float(design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG][0])
            self.bottom_flange_width = float(design_dictionary[KEY_BOTTOM_Bflange_PG])
            self.bottom_flange_thickness = float(design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG][0])

            #3 list loops for V inp<V_d and M inp < Md criteria for not considering thickness (3)
            # self.total_depth = float(design_dictionary[KEY_OVERALL_DEPTH_PG])
            # self.web_thickness_list = float(design_dictionary[KEY_WEB_THICKNESS_PG])
            # self.top_flange_width = float(design_dictionary[KEY_TOP_Bflange_PG])
            # self.top_flange_thickness_list = float(design_dictionary[KEY_TOP_FLANGE_THICKNESS_PG])
            # self.bottom_flange_width = float(design_dictionary[KEY_BOTTOM_Bflange_PG])
            # self.bottom_flange_thickness_list = float(design_dictionary[KEY_BOTTOM_FLANGE_THICKNESS_PG])
        
        
        ########## - modify when the thickness becomes a list
        thickness_for_mat = max(self.web_thickness,self.top_flange_thickness, self.bottom_flange_thickness)
        self.eff_depth = self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness)
        self.IntStiffnerwidth = min(self.top_flange_width,self.bottom_flange_width) - self.web_thickness/2 - 10
        self.material = Material(design_dictionary[KEY_MATERIAL],thickness_for_mat)
        self.eff_width_longitudnal = min(self.top_flange_width,self.bottom_flange_width) - self.web_thickness/2 - 10
        
        #--------------------------------------------------------------------------------
        # if design_dictionary[KEY_IntermediateStiffener_thickness] == 'All':
        if design_dictionary[KEY_IntermediateStiffener_thickness] == 'Customized':
            design_dictionary[KEY_IntermediateStiffener_thickness_val] = PlateGirderWelded.int_thicklist
        else:
            design_dictionary[KEY_IntermediateStiffener_thickness_val] = VALUES_STIFFENER_THICKNESS
        
        self.int_thickness_list = design_dictionary[KEY_IntermediateStiffener_thickness_val]

        if design_dictionary[KEY_LongitudnalStiffener_thickness] == 'Customized':
            design_dictionary[KEY_LongitudnalStiffener_thickness_val] = PlateGirderWelded.long_thicklist
        else:
            design_dictionary[KEY_LongitudnalStiffener_thickness_val] = VALUES_STIFFENER_THICKNESS

        self.long_thickness_list = design_dictionary[KEY_LongitudnalStiffener_thickness_val]   #float conv required

        self.support_condition = 'Simply Supported'
        self.loading_case = design_dictionary[KEY_BENDING_MOMENT_SHAPE]
        self.shear_type = None
        self.support_type = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]
        self.loading_condition = design_dictionary[KEY_LOAD]
        self.torsional_res = design_dictionary[KEY_TORSIONAL_RES]
        self.warping = design_dictionary[KEY_WARPING_RES]
        self.length = float(design_dictionary[KEY_LENGTH])
        self.effective_length = None
        self.allow_class = design_dictionary[KEY_ALLOW_CLASS]
        self.loading_case = design_dictionary[KEY_BENDING_MOMENT_SHAPE]
        self.beta_b_lt = None
        self.web_philosophy = design_dictionary[KEY_WEB_PHILOSOPHY]
        self.epsilon = math.sqrt(250 / self.material.fy)
        self.b1 = float(design_dictionary[KEY_SUPPORT_WIDTH])
        self.c = design_dictionary[KEY_IntermediateStiffener_spacing]
        self.Is = None
        self.IntStiffThickness = float(self.int_thickness_list[0])
        self.LongStiffThickness = float(self.long_thickness_list[0])
        self.V_cr = None
        self.V_d = None
        self.V_tf = None
        self.long_Stiffner = design_dictionary[KEY_LongitudnalStiffener]
        self.load = Load(shear_force=design_dictionary[KEY_SHEAR],axial_force="",moment=design_dictionary[KEY_MOMENT],unit_kNm=True,)
        self.alpha_lt = 0.49
        self.phi_lt = None
        self.gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]["yielding"]
        self.X_lt = None
        self.fbd_lt = None
        self.Md = None
        if self.support_type == 'Major Laterally Supported':
            self.lefactor = 0.7
        else:
            self.lefactor = 1
        self.M_cr = None
        self.F_q = None
        self.Critical_buckling_load = None
        self.shear_ratio = 0
        self.moment_ratio = 0
        self.deflection_ratio = 0
        self.It = None
        self.Iw = None
        self.torsion_cnst = None
        self.warping_cnst = None
        self.critical_moment = None
        self.fcd = None
        # #OUTPUT VAR INITIALIZATION
        # self.result_designation = None
        # self.result_UR = None
        # self.result_section_class  = None
        # self.result_betab = None
        # self.result_effective_area = None
        # self.result_shear = None
        # self.result_bending = None
        # self.result_tc = None
        # self.result_wc = None
        # self.result_IF_lt = None
        # self.result_srf_lt = None
        # self.result_nd_esr_lt = None
        # self.result_nd_esr_lt = None
        # self.result_mcr = None

        # design type
        # self.design_type_temp = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]  # or KEY_DISP_DESIGN_TYPE2_FLEXURE
        # self.latex_design_type = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]  # or KEY_DISP_DESIGN_TYPE2_FLEXURE
        # if self.design_type_temp == VALUES_SUPP_TYPE_temp[0]:
        #     self.design_type = VALUES_SUPP_TYPE[0]  # or KEY_DISP_DESIGN_TYPE2_FLEXURE
        #     self.bending_type = KEY_DISP_BENDING1
        #     # TODO self.support_cndition_shear_buckling
        #     self.support_cndition_shear_buckling = 'NA'#design_dictionary[KEY_ShearBucklingOption]
        # elif self.design_type_temp == VALUES_SUPP_TYPE_temp[1]:
        #     self.design_type = VALUES_SUPP_TYPE[0]
        #     self.bending_type = KEY_DISP_BENDING2 #if design_dictionary[KEY_BENDING] != 'Disabled' else 'NA'
        #     self.support_cndition_shear_buckling = 'NA'

        # elif self.design_type_temp == VALUES_SUPP_TYPE_temp[2]:
        #     self.design_type = VALUES_SUPP_TYPE[1]
        #     self.bending_type = KEY_DISP_BENDING1
        #     self.support_cndition_shear_buckling = 'NA'

        # section user data
        # self.length = float(design_dictionary[KEY_LENGTH])

        # end condition
        # self.support = design_dictionary[KEY_DESIGN_TYPE_FLEXURE]

        # factored loads
        
        





        # design preferences
        # self.allowable_utilization_ratio = float(design_dictionary[KEY_ALLOW_UR])
        # self.latex_efp = design_dictionary[KEY_LENGTH_OVERWRITE]
        # self.effective_area_factor = float(design_dictionary[KEY_EFFECTIVE_AREA_PARA])
        # self.allowable_utilization_ratio = 1.0
        # self.optimization_parameter = "Utilization Ratio"
        # if 'Semi-Compact' is available
        # self.steel_cost_per_kg = 50
        # # Step 2 - computing the design compressive stress for web_buckling & web_crippling
        # self.bearing_length = design_dictionary[KEY_BEARING_LENGTH]
        # #TAKE from Design Dictionary
        # self.allowed_sections = []
        # if self.allow_class == "Yes":
        #     self.allowed_sections == KEY_SemiCompact

        # print(f"self.allowed_sections {self.allowed_sections}")
        # print("==================")
        # # print(f"self.load_type {self.load_type}")

        # print(f"self.module{self.module}")
        # print(f"self.sec_list {self.sec_list}")
        # print(f"self.material {self.material}")
        # print(f"self.length {self.length}")
        # print(f"self.load {self.load}")
        # print("==================")

        # # safety factors
        
        # self.gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]["ultimate_stress"]
        # self.material_property = Material(material_grade=self.material, thickness=0)
        # self.fyf = self.material_property.fy
        # self.fyw = self.material_property.fy

        # print(f"self.material_property {self.material_property}]")
        # print( "self.material_property",self.material_property.fy)
        # initialize the design status
        # self.design_status_list = []
        self.design_status = False

        self.shear_force_optimal = False
        self.moment_optimal = False
        self.min_mass = False  
        # self.sec_prop_initial_dict = {}
        # self.failed_design_dict = {}
        if self.design_type == 'Optimized':
            is_thick_web = False
            is_symmetric = False
            if self.web_philosophy == 'Thick Web without ITS':
                is_thick_web = True
            else:
                is_thick_web = False

            if design_dictionary[KEY_IS_IT_SYMMETRIC] == 'Symmetric Girder':
                is_symmetric = True
            else:
                is_symmetric = False
            self.optimized_method(self,design_dictionary,is_thick_web,is_symmetric)
            
            # pass
        else:
            self.design_check(self,design_dictionary)
        # if self.flag:
        #     self.results(self, design_dictionary)
         

        # else:
        #     pass
        #     # logger.warning(
        #     #         "Plastic section modulus of selected sections is less than required."
        #     #     )
        #     return

    # Simulation starts here
    def section_classification(self,design_dictionary):
        self.design_status = False

        print("THICKNESS VALUES INT STIFFNER", self.int_thickness_list)
        print("THICKNESS VALUE LONG STIFFENER",self.long_thickness_list)
        flange_class_top = IS800_2007.Table2_i(((self.top_flange_width / 2)),self.top_flange_thickness,self.material.fy,'Welded')[0]
        flange_class_bottom = IS800_2007.Table2_i(((self.bottom_flange_width / 2)),self.bottom_flange_thickness,self.material.fy,'Welded')[0]
        web_class = IS800_2007.Table2_iii((self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness),self.web_thickness,self.material.fy)
        web_ratio = (self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness)) / self.web_thickness
        flange_ratio_top = self.top_flange_width / (2 *self.top_flange_thickness)
        flange_ratio_bottom = self.bottom_flange_width / (2 *self.bottom_flange_thickness)
        print("Section classification- top flange, bottom flange, Web",flange_class_top, flange_class_bottom,web_class,web_ratio,flange_ratio_top,flange_ratio_bottom)
        if flange_class_bottom == "Slender" or web_class == "Slender" or flange_class_top == 'Slender':
                self.section_class = "Slender"
        else:
            if flange_class_top == KEY_Plastic:
                if web_class == KEY_Plastic:
                    if flange_class_bottom == KEY_Plastic:
                        self.section_class = KEY_Plastic
                    elif flange_class_bottom == KEY_Compact:
                        self.section_class = KEY_Compact
                    else:  # SemiCompact
                        self.section_class = KEY_SemiCompact
                elif web_class == KEY_Compact:
                    if flange_class_bottom in [KEY_Plastic, KEY_Compact]:
                        self.section_class = KEY_Compact
                    else:  # SemiCompact
                        self.section_class = KEY_SemiCompact
                else:  # web SemiCompact
                    self.section_class = KEY_SemiCompact

            elif flange_class_top == KEY_Compact:
                if web_class == KEY_Plastic:
                    if flange_class_bottom in [KEY_Plastic, KEY_Compact]:
                        self.section_class = KEY_Compact
                    else:  # SemiCompact
                        self.section_class = KEY_SemiCompact
                elif web_class == KEY_Compact:
                    if flange_class_bottom in [KEY_Plastic, KEY_Compact]:
                        self.section_class = KEY_Compact
                    else:  # SemiCompact
                        self.section_class = KEY_SemiCompact
                else:  # web SemiCompact
                    self.section_class = KEY_SemiCompact

            else:  # flange_class_top == SemiCompact
                self.section_class = KEY_SemiCompact
        print("overall section class", self.section_class)
        self.Zp_req = self.load.moment * self.gamma_m0 / self.material.fy
        self.effective_length_beam(self, design_dictionary, self.length)

        print( 'self.allow_class', self.allow_class)

        if self.section_class == 'Slender':
            return False
        else:
            return True


    def beta_value(self,design_dictionary,section_class):
        self.plast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_PlasticModulusZ(self,self.total_depth,self.top_flange_width,self.bottom_flange_width,
                                                    self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.epsilon)
        self.elast_sec_mod_z =Unsymmetrical_I_Section_Properties.calc_ElasticModulusZz(self,self.total_depth,self.top_flange_width,self.bottom_flange_width,
                                                    self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness)
        print("self.plast_sec_mod_z",self.plast_sec_mod_z)
        print("self.elast_sec_mod_z",self.elast_sec_mod_z)
        self.Zp_req = self.load.moment * self.gamma_m0 / self.material.fy
        if self.plast_sec_mod_z >= self.Zp_req:
            print( 'self.section_property.plast_sec_mod_z More than Requires',self.plast_sec_mod_z,self.Zp_req)
        if section_class == KEY_Plastic or section_class == KEY_Compact:
            self.beta_b_lt = 1.0
        else:
            self.beta_b_lt = (self.elast_sec_mod_z/ self.plast_sec_mod_z)
        print("Beta value",self.beta_b_lt)

    
    #-----add a check function to call everything.

    #checks thick web thickness
    def min_web_thickness_thick_web(self, d, tw, eps, stiffner_type,c):
        if IS800_2007.cl_8_6_1_1_and_8_6_1_2_web_thickness_check(d, tw, eps, stiffner_type, c):
            return True
        else:
            return False


    #check 2 moment capacity for major laterally supported & thick web and thin web 
    def moment_capacity_laterally_supported(self, V,Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot, section_class) :
        A_vg = (D - tf_top - tf_bot) * tw
        self.V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
        if V > 0.6 * self.V_d: #high shear(Mdv calculation for high shear. Naming kept Md for compatibility)
            self.Md = self.calc_Mdv(self, V, self.V_d, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot)
        else: #low shear
            self.Md = IS800_2007.cl_8_2_1_2_design_bending_strength(section_class, Zp, Ze, Fy, gamma_m0, self.support_condition)
        self.moment_ratio = self.load.moment/ self.Md
        if self.Md >= self.load.moment:
            return True
        else:
            return False
    
    #check 3 shear capacity for major laterally supported & thick web
    def shear_capacity_laterally_supported_thick_web(self, Fy, gamma_m0, D, tw, tf_top, tf_bot):
        A_vg = (D - tf_top - tf_bot) * tw
        self.V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
        self.shear_ratio =  max(self.load.shear_force / self.V_d,self.shear_ratio)
        if self.V_d >= self.load.shear_force:
            return True
        else:
            return False
    

    #check 4 Web buckling for major laterally supported and unsupported & thick web
    def web_buckling_laterally_supported_thick_web(self, Fy, gamma_m0, D, tw, tf_top, tf_bot,E, b1):
        self.eff_depth = D - (tf_bot + tf_top)
        n1 = self.eff_depth / 2
        Ac = (b1 + n1) * tw
        slenderness_input = 2.5 * self.eff_depth / tw
        self.fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(Fy, gamma_m0, slenderness_input, E)
        Critical_buckling_load = round(Ac * self.fcd, 2)
        self.shear_ratio =  max(self.load.shear_force / Critical_buckling_load , self.shear_ratio)
        if Critical_buckling_load>= self.load.shear_force:
            return True
        else:
            return False
    
    #check 5 Web crippling for major laterally supported and unsupported & thick web
    def web_crippling_laterally_supported_thick_web(self, Fy, gamma_m0, tw, tf_top, b1):
        n2 = 2.5 * tf_top
        Critical_crippling_load = round((b1 + n2) * tw * Fy / (gamma_m0), 2)
        self.shear_ratio =  max(self.load.shear_force / Critical_crippling_load , self.shear_ratio)
        if Critical_crippling_load >= self.load.shear_force:
            return True
        else:
            return False


    #check 6 moment capacity for major laterally unsupported & thick web

    def get_K_from_warping_restraint(self,warping_condition):
        """
        Return effective length factor K based on exact warping restraint description (IS 800:2007, Clause E.1).
        """
        if warping_condition == "Both flanges fully restrained":
            return 0.5
        elif warping_condition == "Compression flange fully restrained":
            return 0.7
        elif warping_condition == "Compression flange partially restrained":
            return 0.85
        elif warping_condition == "Warping not restrained in both flanges":
            return 1.0
        else:
            raise ValueError("Invalid warping restraint. Use one of the four standard conditions.")
    def bending_check_lat_unsupported(self, beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy, M_cr, section_class):
        self.lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy,
                                                                    M_cr)

        self.phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(self.alpha_lt, self.lambda_lt)
        self.X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(self.phi_lt, self.lambda_lt)
        self.fbd_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(self.X_lt, fy, self.gamma_m0)
        self.Md = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(plast_sec_mod_z, elast_sec_mod_z, self.fbd_lt,
                                                                        section_class)

        return round(self.Md, 2)
    
    def calc_Mdv_lat_unsupported(self, V, Vd, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot,
                             Md):  # only for major laterally supp
        """
        Calculate Mdv for high shear conditions.

        Parameters:
        V         : Factored applied shear force
        Vd        : Design shear strength governed by web yielding/buckling
        Zp        : Plastic section modulus of the section (Z-axis)
        Ze        : Elastic section modulus of the section (Z-axis)
        Fy        : Yield strength of material
        gamma_m0  : Partial safety factor for material
        D         : Total depth of section
        tw        : Thickness of the web
        tf_top    : Thickness of the top flange
        tf_bot    : Thickness of the bottom flange

        Returns:
        Mdv : Design bending strength under high shear condition
        """

        # Calculating beta
        beta = (2 * V / Vd - 1) ** 2

        # Calculating Aw and Zfd
        d = D - (tf_top + tf_bot)
        Aw = d * tw
        Zfd = Zp - (Aw * D / 4)
        print("Aw", Aw, "Zfd", Zfd)
        # Calculating Mfd
        Mfd = Zfd * Fy / gamma_m0

        # Calculating Mdv
        Mdv = Md - beta * (Md - Mfd)

        # Limiting value as per the provided formula
        Mdv_limit = (1.2 * Ze * Fy) / gamma_m0
        print("Mfd", Mfd, "Mdv", Mdv, "Mdv_limit", Mdv_limit)
        return round(min(Mdv, Mdv_limit), 2)
    
    def calc_Mdv(self, V, Vd, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot):  # only for major laterally supp
        """
        Calculate Mdv for high shear conditions.

        Parameters:
        V         : Factored applied shear force
        Vd        : Design shear strength governed by web yielding/buckling
        Zp        : Plastic section modulus of the section (Z-axis)
        Ze        : Elastic section modulus of the section (Z-axis)
        Fy        : Yield strength of material
        gamma_m0  : Partial safety factor for material
        D         : Total depth of section
        tw        : Thickness of the web
        tf_top    : Thickness of the top flange
        tf_bot    : Thickness of the bottom flange

        Returns:
        Mdv : Design bending strength under high shear condition
        """

        # Calculating beta
        beta = (2 * V / Vd - 1) ** 2

        # Calculating Aw and Zfd
        d = D - (tf_top + tf_bot)
        Aw = d * tw
        Zfd = Zp - (Aw * D / 4)
        print("Aw", Aw, "Zfd", Zfd)

        # Calculating Mfd
        Mfd = Zfd * Fy / gamma_m0

        # Calculating Md (Plastic Design Moment)
        Md = Zp * Fy / gamma_m0

        # Calculating Mdv
        Mdv = Md - beta * (Md - Mfd)

        # Limiting value as per the provided formula
        Mdv_limit = (1.2 * Ze * Fy) / gamma_m0
        print("Mfd", Mfd / 1000000, "Mdv", Mdv / 1000000, "Mdv_limit", Mdv_limit / 1000000)

        return round(min(Mdv, Mdv_limit), 2)

    def calc_yj(self,Bf_top, tf_top, Bf_bot, tf_bot, D):
        """
        Calculate yj per IS 800:2007 Clause E.3.2.2. Returns 0 for symmetric sections.
        """
        if Bf_top == Bf_bot and tf_top == tf_bot:
            return 0.0  # symmetric section
        h = D - (tf_top + tf_bot)
        Ift = (Bf_top * tf_top**3) / 12
        Ifc = (Bf_bot * tf_bot**3) / 12
        beta_f = Ifc / (Ifc + Ift)
        alpha = 0.8 if beta_f > 0.5 else 1.0
        return alpha * (2 * beta_f - 1) * h / 2
    
    def moment_capacity_laterally_unsupported(self,E, LLT, D,
                            tf_top, tf_bot, Bf_top, Bf_bot,tw,
                            LoadingCase,gamma_m0, Fy,shear_force):
        if Bf_top == Bf_bot and tf_top == tf_bot:
            return 0.0  # symmetric section
        h = D - (tf_top + tf_bot)
        Ift = (Bf_top * tf_top ** 3) / 12
        Ifc = (Bf_bot * tf_bot ** 3) / 12
        beta_f = Ifc / (Ifc + Ift)
        alpha = 0.8 if beta_f > 0.5 else 1.0
        alpha * (2 * beta_f - 1) * h / 2


        G = 0.769 * 10**5
        Kw = self.get_K_from_warping_restraint(self,self.warping)
        Iy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
        It = Unsymmetrical_I_Section_Properties.calc_TorsionConstantIt(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
        Iw = Unsymmetrical_I_Section_Properties.calc_WarpingConstantIw(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
        
        #Mcr calc
        yg = D / 2
        yj = self.calc_yj(self, Bf_top, tf_top, Bf_bot, tf_bot, D)
        K_value = 0
        # Constants from Table 42 (IS 800:2007)
        if LoadingCase == KEY_DISP_UDL_PIN_PIN_PG:
            K_value == 1.0
            c1, c2, c3 = 1.132, 0.459, 0.525
        elif LoadingCase == KEY_DISP_UDL_FIX_FIX_PG:
            K_value == 0.5
            c1, c2, c3 = 0.712, 0.652, 1.070
        elif LoadingCase == KEY_DISP_PL_PIN_PIN_PG:
            K_value == 1.0
            c1, c2, c3 = 1.365, 0.553, 1.780
        elif LoadingCase == KEY_DISP_PL_FIX_FIX_PG:
            K_value == 0.5
            c1, c2, c3 = 0.938, 0.715, 4.800
        else:
            raise ValueError("Invalid Loading Case.")

        # Symmetric section (Eq 2.20)
        if Bf_top == Bf_bot and tf_top == tf_bot:
            term1 = (math.pi ** 2 * E * Iy) / (LLT ** 2)
            term2 = (Iw / Iy)
            term3 = (G * It * LLT ** 2) / (math.pi ** 2 * E * Iy)
            self.M_cr = term1 * math.sqrt(term2 + term3)
        else:
            # Unsymmetric case (Annex E full formula)
            term1 = (math.pi ** 2 * E * Iy) / (LLT ** 2)
            bracket = ((K_value / Kw) ** 2 * (Iw / Iy) +
                    (G * It * LLT ** 2) / (math.pi ** 2 * E * Iy) +
                    (c2 * yg - c3 * yj) ** 2)
            self.M_cr = c1 * term1 * math.sqrt(bracket) - term1 * (c2 * yg - c3 * yj)
        
        print("Input moment",self.load.moment)
        print("MCR VAL",self.M_cr)
        A_vg = (D - tf_top - tf_bot) * tw
        self.V_d = ((A_vg * Fy) / (math.sqrt(3) * gamma_m0))
        if shear_force > 0.6 * self.V_d:  # high shear(Mdv calculation for high shear. Naming kept Md for compatibility)
            self.Md = self.calc_Mdv_lat_unsupported(self, self.load.shear_force, self.V_d, self.plast_sec_mod_z,
                                                    self.elast_sec_mod_z, self.material.fy, self.gamma_m0,
                                                    self.total_depth, self.web_thickness, self.top_flange_thickness,
                                                    self.bottom_flange_thickness, self.Md)
        else:  # low shear
            self.Md = self.bending_check_lat_unsupported(self, self.beta_b_lt, self.plast_sec_mod_z, self.elast_sec_mod_z,
                                                        self.material.fy, self.M_cr, self.section_class)


        self.moment_ratio = self.load.moment/ self.Md
        print("Ratio for moment", self.moment_ratio)
        #     # print("supp mdv",self.Mdv)
        if self.Md >= self.load.moment:
            return True
        else:
            return False

    #effective length calculation
    def effective_length_beam(self, design_dictionary, length):
        if design_dictionary[KEY_LENGTH_OVERWRITE] == 'NA':
            self.effective_length = IS800_2007.cl_8_3_1_EffLen_Simply_Supported(Torsional=self.torsional_res,Warping=self.warping,
                                                                                length=length,depth=(self.total_depth/1000),load=self.loading_condition)
            print(f"Working 1 {self.effective_length}")
        else:
            try:
                if float(design_dictionary[KEY_LENGTH_OVERWRITE]) <= 0:
                    design_dictionary[KEY_LENGTH_OVERWRITE] = 'NA'
                else:
                    length = length * float(design_dictionary[KEY_LENGTH_OVERWRITE])

                self.effective_length = length
                print(f"Working 2 {self.effective_length}")
            except:
                print(f"Inside effective_length_beam",type(design_dictionary[KEY_LENGTH_OVERWRITE]))
                logger.warning("Invalid Effective Length Parameter.")
                logger.info('Effective Length Parameter is set to default: 1.0')
                design_dictionary[KEY_LENGTH_OVERWRITE] = '1.0'
                self.effective_length_beam(self, design_dictionary, length)
                print(f"Working 3 {self.effective_length}")
        print(f"Inside effective_length_beam",self.effective_length, design_dictionary[KEY_LENGTH_OVERWRITE])

    
    def end_panel_stiffener_calc(self,
        Bf_top, Bf_bot, tw, tq, fy, gamma_m0, effective_depth,
        tf_top, total_depth, effective_length, tf_bot, E, eps
):
        """
        Calculate end panel stiffener properties.

        Parameters:
        Bf_top (float): Width of flange at top (mm)
        Bf_bot (float): Width of flange at bottom (mm)
        tw (float): Thickness of web (mm)
        tq (float): Thickness of stiffener (mm)
        fy (float): Yield strength of material (MPa)
        gamma_m0 (float): Partial safety factor


        effective_depth (float): Effective depth (mm)
        tf_top (float): Top flange thickness (mm)
        total_depth (float): Total depth of section (mm)
        effective_length (float): Effective length for slenderness (mm)
        D (float): Depth of section (mm)
        E (float):  modulus of elasticity of steel (MPa)

        Returns:
        dict: Dictionary of results including buckling resistance, bearing capacity, and torsion check.
        """

        # Geometrical properties
        net_outstand = min(Bf_top, Bf_bot) - tq
        width_stiffener = min(max(net_outstand, 14 * tq * eps), 20 * tq * eps)

        # Core area and moment of inertia for buckling resistance
        A_core = (14 * tq * epsilon * 2) + (20 * tw * tw)
        Ixx = ((tq * (14 * tq * epsilon * 2) ** 3) / 12) + ((20 * tw * tw ** 3) / 12)
        r = math.sqrt(Ixx / A_core)
        # Slenderness ratio
        slenderness_input = 0.7 * effective_depth / r
        self.fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
            fy,
            gamma_m0,
            slenderness_input,
            E )
        buckling_resistance = self.fcd * A_core

        # Bearing capacity
        chamfered_width = 15  # mm
        Aq = 2 * (width_stiffener - chamfered_width) * tq
        bearing_capacity = (Aq * fy) / (0.8 * gamma_m0)

        # Torsional restraint
        ry = Unsymmetrical_I_Section_Properties.calc_RadiusOfGyrationY(self, total_depth, Bf_top, Bf_bot, tw, tf_top, tf_bot)
        slender_torsion = effective_length / ry

        if slender_torsion <= 50:
            alpha_s = 0.006
        elif slender_torsion <= 100:
            alpha_s = 0.3 / slender_torsion
        else:
            alpha_s = 30 / (slender_torsion ** 2)

        torsion_check = 0.34 * alpha_s * (total_depth ** 3) * tf_top
        Is = (tq * (2 * width_stiffener) ** 3) / 12
        torsion_ok = Is >= torsion_check

        return {
            "Buckling Resistance (N)": buckling_resistance,
            "Bearing Capacity (N)": bearing_capacity,
            "Slenderness Ratio": slenderness_input,
            "Design Compressive Strength fcd (MPa)": self.fcd,
            "Moment of Inertia Is (mm^4)": Is,
            "Torsion Check (mm^4)": torsion_check,
            "Torsion OK": torsion_ok
        }

    def deflection_from_moment_kNm_mm(self,M_kNm, L, E, I, case):
        """
        Compute max mid-span deflection from bending moment,
        converting M (kN·m) → N·m and L (mm) → m internally.

        Parameters
        ----------
        M_kNm : float
            Max bending moment in kN·m.
        L_mm : float
            Span length in mm.
        E : float
            Young’s modulus in Pa (N/m²).
        I : float
            Second moment of area in m^4.
        case : str
            One of 'simple_udl', 'fixed_udl', 'simple_point', 'fixed_point'.

        Returns
        -------
        delta : float
            Mid-span deflection in meters.
        """
        # unit conversions
        M = M_kNm  # kN·m → N·m

        pref = M * L ** 2 / (E * I)
        if case == KEY_DISP_UDL_PIN_PIN_PG:
            return (5 / 48) * pref
        elif case == KEY_DISP_UDL_FIX_FIX_PG:
            return (1 / 32) * pref
        elif case == KEY_DISP_PL_PIN_PIN_PG:
            return (1 / 12) * pref
        elif case == KEY_DISP_PL_FIX_FIX_PG:
            return (1 / 24) * pref
        else:
            raise ValueError(
                "Unknown case. Use 'simple_udl', 'fixed_udl', 'simple_point', or 'fixed_point'."
            )
        
    def evaluate_deflection_kNm_mm(self,
        M_kNm, L, E, case, criteria_list=VALUES_MAX_DEFL
):
        """
        1) Calculate deflection from moment (with unit conversions).
        2) Compare against span-based limits.
        Returns (delta_m, results_dict, best_criterion).
        """
        # 1) compute deflection in meters
        I = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(self,self.total_depth,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness)
        delta = self.deflection_from_moment_kNm_mm(self,M_kNm, L, E, I, case)

        # 2) compare against each 'Span/N' limit
        results = {}
        passed = []
        for crit in criteria_list:
            try:
                _, denom = crit.split('/')
                n = float(denom)
            except ValueError:
                continue
            allowable = L / n
            ok = (delta <= allowable)
            self.deflection_ratio = max(delta / allowable, self.deflection_ratio)

            if ok:
                return True
            else:
                return False
        #     results[crit] = {
        #         'allowable_m': allowable,
        #         'actual_m': delta,
        #         'passes': ok
        #     }
        #     if ok:
        #         passed.append((n, crit))

        # # pick most stringent (smallest denom) that still passes
        # best = min(passed)[1] if passed else None

        # return delta, results

    def shear_stress_unsym_I(self, V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w):

        # Part areas [mm^2]
        A_t = b_ft * t_ft
        A_b = b_fb * t_fb
        A_w = t_w * h_w

        # Section total depth & area
        D = t_fb + h_w + t_ft
        A = A_t + A_b + A_w

        # Centroid y‐coords from bottom of bottom flange [mm]
        y_b = t_fb / 2
        y_w = t_fb + h_w / 2
        y_t = t_fb + h_w + t_ft / 2

        # Neutral axis from bottom [mm]
        y_na = (A_b * y_b + A_w * y_w + A_t * y_t) / A

        # Second moment I_z [mm^4]
        I_b = b_fb * t_fb ** 3 / 12 + A_b * (y_b - y_na) ** 2
        I_w = t_w * h_w ** 3 / 12 + A_w * (y_w - y_na) ** 2
        I_t = b_ft * t_ft ** 3 / 12 + A_t * (y_t - y_na) ** 2
        I_z = I_b + I_w + I_t

        # First moments Q [mm^3]
        Q_bot = A_b * abs(y_na - y_b)
        Q_top = A_t * abs(y_t - y_na)

        # Shear flows q = V*Q / I  [kN·mm^3 / mm^4 = kN/mm]
        q_bot = V_ed * Q_bot / I_z
        q_top = V_ed * Q_top / I_z

        return {
            'y_na_mm': y_na, 'I_z_mm4': I_z,
            'Q_top_mm3': Q_top, 'Q_bot_mm3': Q_bot,
            'q_top_kN_per_mm': q_top,
            'q_bot_kN_per_mm': q_bot,
        }
        
    def weld_leg_from_q_with_cl10(self,
                              q_kN_per_mm,  # shear flow [kN/mm]
                              ultimate_stresses,  # list of MPa
                              fabrication='shop'
                              ):
        """
        Compute fillet‐weld leg a [mm] from shear flow,
        using f_wd from cl.10.5.7.1.1.
        """
        # 1) get f_wd in MPa → convert to N/mm²
        f_wd = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses, fabrication
        )  # MPa

        # 2) convert q to N/mm
        q_N_per_mm = q_kN_per_mm * 1e3

        # 3) throat thickness t = q / f_wd  [mm]
        t_throat = q_N_per_mm / f_wd

        # 4) leg size a = t·√2
        return t_throat * math.sqrt(2)


    def design_welds_with_strength_web_to_flange(self,
                                             # section loads & geometry
                                             V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w,
                                             # material / weld properties
                                             ultimate_stresses, fabrication,
                                             # stiffener inputs
                                             t_st, b_st, V_unstf, L_weld
                                             ):
        # compute shear flows
        sf = self.shear_stress_unsym_I(self, V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w)

        # weld legs using cl.10 strength
        a_top = self.weld_leg_from_q_with_cl10(self,
                                            sf['q_top'], ultimate_stresses, fabrication
                                            )
        a_bot = self.weld_leg_from_q_with_cl10(self,
                                            sf['q_bot'], ultimate_stresses, fabrication
                                            )

        # end‐stiffener check (unchanged)

        return {
            **sf,
            'a_top_mm': a_top,
            'a_bot_mm': a_bot
        }

    def weld_for_end_stiffener(self, t_st, b_st, V_ed, V_unstf, D, t_ft, t_fb, tw):
        """
        t_st : thickness of stiffener
        b_st : width of stiffener
        V_ed : design shear force
        V_unstf : unstiffened shear force
        D : depth of section
        t_ft : thickness of top flange
        t_fb : thickness of bottom flange
        tw : thickness of web
        Automatically computes L_weld = D - t_ft - t_fb,
        then returns:
        q1_min    = t_st^2/(5·b_st)
        q2_ext    = (V_ed–V_unstf)/L_weld
        q_total   = q1 + q2
        q_each_weld = q_total/2
        All in kN/mm.
        """
        # 0) available weld length
        L_weld = D - t_ft - t_fb

        # 1) min weld per side
        q1 = tw ** 2 / (5 * b_st)

        # 2) stiffener shear per unit length
        delta_V = max(V_ed - V_unstf, 0)
        q2 = delta_V / L_weld

        # 3) total on one side
        q_tot = q1 + q2

        # 4) split into two welds (each face)
        q_each = q_tot / 2

        return {
            'L_weld_mm': L_weld,
            'q1_min': q1,
            'q2_ext': q2,
            'q_total': q_tot,
            'q_each_weld': q_each
        }
    

    #-------------Thin Web (Simple post critical method)------------------------#
    def shear_buckling_check_simple_postcritical(self, eff_depth,D,tf_top,tf_bot,tw, V, c=0):
        A_vg = (D - tf_top - tf_bot) * tw
        if self.web_philosophy == 'Thick Web without ITS':
            K_v = 5.35
        else:
            if c / eff_depth < 1:
                K_v = 4 + 5.35 / (c / eff_depth) ** 2
            else:
                K_v = 5.35 + 4 / (c / eff_depth) ** 2
        E = self.material.modulus_of_elasticity
        mu = 0.3
        tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, eff_depth, self.web_thickness)
        lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(self.material.fy, tau_crc)
        tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, self.material.fy)
        self.V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
        print("V_cr value", self.V_cr)
        self.shear_ratio =  max(self.load.shear_force / self.V_cr , self.shear_ratio)
        if self.V_cr > V:
            return True
        else:
            return False


    def shear_buckling_check_intermediate_stiffener(
    self,
    d,
    tw,
    c,
    e,
    IntStiffThickness,
    IntStiffenerWidth,
    V_cr,
    V_ed,
    gamma_m0,
    fy,
    E
):
        """
        Performs global and shear buckling checks for an intermediate stiffener.

        Parameters:
        d                    : float : depth of web panel (mm)
        tw                   : float : thickness of web (mm)
        c                    : float : stiffener spacing (mm)
        e                    : float : outstand ratio factor
        IntStiffThickness    : float : thickness of intermediate stiffener (mm)
        IntStiffenerWidth    : float : width of intermediate stiffener leg (mm)
        V_cr                 : float : critical shear buckling force (kN)
        V_ed                 : float : design shear force on panel (kN)
        gamma_m0             : float : partial safety factor for material
        fy                   : float : yield strength of steel (MPa)
        E                    : float : modulus of elasticity of steel (MPa)

        Returns:
        bool : True if stiffener passes both global and shear buckling checks, False otherwise.
        """
        # 1. Global buckling check of stiffener
        cd_ratio = c / d
        if cd_ratio >= math.sqrt(2):
            I_min_global = 0.75 * d * tw**3
        else:
            I_min_global = (1.5 * d * tw**3) / (c**2)

        # Moment of inertia of stiffener cross-section
        I_s = (((2 * IntStiffenerWidth + tw)**3) * IntStiffThickness) / 12
        I_s -= (IntStiffThickness * tw**3) / 12

        # Maximum allowable outstand
        max_outstand = 14 * IntStiffThickness * e

        # Fail global check if inertia or outstand insufficient
        if I_s < I_min_global or max_outstand < IntStiffenerWidth:
            return False

        # 2. Shear buckling (axial) check of stiffener
        # Effective shear force on stiffener
        F_q = (V_ed - V_cr) / gamma_m0

        # Provided cross-sectional area
        A_s = 2 * IntStiffenerWidth * IntStiffThickness

        # Combined area for axial buckling (stiffener + bearing area)
        A_x = A_s + (20 * tw * 2)

        # Moment of inertia for axial buckling
        I_x = (((2 * IntStiffenerWidth + tw)**3) * IntStiffThickness) / 12
        I_x += (20 * tw * 2 * tw**3) / 12
        I_x -= (IntStiffThickness * tw**3) / 12

        # Radius of gyration
        r_x = math.sqrt(I_x / A_x)

        # Slenderness ratio
        Le = self.lefactor * d
        slenderness_input = Le / r_x

        # Design compressive stress from IS 800
        fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
            fy, gamma_m0, slenderness_input, E
        )

        # Critical buckling resistance (kN)
        Pd = round(A_x * fcd / 1000, 2)
        self.shear_ratio =  max(self.load.shear_force / Pd , self.shear_ratio)
        self.Critical_buckling_resistance = Pd

        # Debug prints
        print("Design shear force on stiffener F_q:", round(F_q, 2), "kN")
        print("Critical buckling resistance Pd:", Pd, "kN")

        # Check axial capacity
        return F_q < Pd

    def tension_field_end_stiffener(self, d, tw, fyw, V_tf, V_cr, shear_force, moment):
            # Formula 1: H_q = 1.25·V_p·√[1 – (V_cr–V_p)/(V_tf–V_cr)]
        V_dp = (d * tw * fyw * math.sqrt(3)) / 1000
        denom = V_tf - V_cr
        rad = 1.0 - (V_cr - V_dp) / denom
        if rad < 0:
            raise ValueError(f"Negative radicand under sqrt: {rad:.3f}")
        H_q = 1.25 * V_dp * math.sqrt(rad)
        R_tf = H_q / 2
        A_v= d * tw
        V_n= (fyw * A_v) /( 1000 * math.sqrt(3) * self.gamma_m0)
        # Moment demand M_tf (kN·m)
        M_tf = (H_q * d)  / 10
        y = c / 2
        I = tw * c ** 3 / 12
        M_q = (I * fyw) / (self.gamma_m0 * y)
        self.moment_ratio =  max(M_tf / M_q , self.moment_ratio)
        self.shear_ratio =  max(self.load.shear_force / R_tf , self.shear_ratio)
        if V_n >= R_tf:
            if M_q >= M_tf:
                return True
        return False
    
    def shear_buckling_check_tension_field(self, eff_depth,D,tf_top,tf_bot,tw, c=0, Nf=0):
        A_vg = (D - tf_top - tf_bot) * tw
        if self.web_philosophy == 'Thick Web without ITS':
            K_v = 5.35
        else:
            if c / eff_depth < 1:
                K_v = 4 + 5.35 / (c / eff_depth) ** 2
            else:
                K_v = 5.35 + 4 / (c / eff_depth) ** 2
        E = self.material.modulus_of_elasticity
        mu = 0.3
        tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E, mu, eff_depth, self.web_thickness)
        lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(self.material.fy, tau_crc)
        tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, self.material.fy)
        self.V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
        phi, M_fr, s, w_tf, sai, fv, self.V_tf = IS800_2007.cl_8_4_2_2_TensionField(c, eff_depth, self.web_thickness,
                                                                            self.material.fy, self.top_flange_width,
                                                                            self.top_flange_thickness,
                                                                            self.material.fy, Nf, self.gamma_m0,
                                                                            A_vg, tau_b, self.load.shear_force)
        print("vtf val",self.V_tf)
        self.shear_ratio =  max(self.load.shear_force / self.V_tf , self.shear_ratio)
        if self.V_tf >= self.load.shear_force:
            return True
        else:
            return False
    

    #PSO HELPER FUNCTIONS

    
    # 1. Generate the “empirical” first particle
    def generate_first_particle(self,L, M, fy,is_thick_web, is_symmetric,k=67):
        D_empirical = L * 1000 / 25       # span in mm
        d_opt = ((M * k) / fy) ** (1/3)    # mm
        D_final = max(D_empirical, d_opt)

        bf_top = 0.3 * D_final
        bf_bot = 0.3 * D_final
        bf = 0.3 * D_final


        tf_top = bf / 24
        tf_bot = bf / 24
        tf = bf / 24


        d = D_final - 2 * tf
        tw = d / 200
        c = 200     # min panel length (if used)
        t_stiff = 6 # min stiffener thickness (if used)
        # Order must match your variable list below
        varlst = []
        if is_symmetric:
            if is_thick_web:
                varlst += [tf,tw,bf,D_final]
            else:
                varlst += [tf,tw,bf,D_final,c,t_stiff]
        else:
            if is_thick_web:
                varlst  += [tf_top,tf_bot,tw,bf_top,bf_bot,D_final]
            else:
                varlst += [tf_top,tf_bot,tw,bf_top,bf_bot,D_final,c,t_stiff]
        print(varlst)
        return varlst

    # 2. Build the list of variables
    def build_variable_structure(self,is_thick_web=True, is_symmetric=True):
        variables = []
        if is_symmetric:
            # tf, tw, bf, D
            variables += ['tf', 'tw', 'bf', 'D']
        else:
            variables += ['tf_top', 'tf_bot', 'tw', 'bf_top', 'bf_bot', 'D']

        if not is_thick_web:
            variables += ['c', 't_stiff']

        return variables

    # 3. Create bounds array
    def get_bounds(self,variable_list):
        bounds_map = {
            'tf': (6, 100),
            'tf_top': (6, 100),
            'tf_bot': (6, 100),
            'tw': (6, 40),
            'bf': (100, 1000),
            'bf_top': (100, 1000),
            'bf_bot': (100, 1000),
            'D': (200, 2000),
            'c': (75, 3000),
            't_stiff': (6, 40)
        }
        lower = [bounds_map[v][0] for v in variable_list]
        upper = [bounds_map[v][1] for v in variable_list]
        return (np.array(lower), np.array(upper))

    
    # 4. Assign a particle vector to your section object
    def assign_particle_to_section(self,particle, variable_list, section):
        for name, value in zip(variable_list, particle):
            setattr(section, name, value)
        
        # handle symmetric naming if needed
        print("Particle",particle)
        print("Variable list",variable_list)
        if 'tf' in variable_list:
            section.tf_top = section.tf_bot = section.tf
            section.bf_top     = section.bf_bot     = section.bf
        
        self.top_flange_thickness = section.tf_top
        self.bottom_flange_thickness = section.tf_bot
        self.web_thickness = section.tw
        self.top_flange_width = section.bf_top
        self.bottom_flange_width = section.bf_bot
        self.total_depth = section.D
        self.c = section.c
        self.IntStiffThickness = section.t_stiff
    
    # 5. Objective function
    def objective_function(self,x, variable_list,design_dictionary,is_symmetric,is_thick_web):
        """
        x: array of shape (n_particles, n_dimensions)
        returns: 1D array of costs
        """
        costs = []
        for particle in x:
            sec = Section()
            self.assign_particle_to_section(self,particle, variable_list, sec)
            cost = self.run_design_checks(self,sec,design_dictionary,is_symmetric,is_thick_web)
            costs.append(cost)
        return np.array(costs)
    
    def run_design_checks(self,section,design_dictionary,is_symmetric,is_thick_web):
        """
        Perform your area calculation + penalties here,
        return a scalar cost.
        """
        
        if is_symmetric:
            if is_thick_web:
                weight = (2 * section.bf * section.tf) + (section.tw * (section.D - 2*section.tf)) * self.length * 7850
            else:
                weight = (2 * section.bf * section.tf) + (section.tw * (section.D - 2*section.tf)) * self.length * 7850   + ((self.length / section.c) - 1) * section.t_stiff * self.IntStiffnerwidth * self.eff_depth *7850  
        else:
            if is_thick_web:

                weight = ((section.bf_top * section.tf_top) + (section.bf_bot * section.tf_bot) + (section.tw * (section.D - section.tf_top - section.tf_bot)) ) * self.length * 7850
            else:
                weight = ((section.bf_top * section.tf_top) + (section.bf_bot * section.tf_bot) + (section.tw * (section.D - section.tf_top - section.tf_bot)) ) * self.length * 7850 + ((self.length / section.c) - 1) * section.t_stiff * self.IntStiffnerwidth * self.eff_depth *7850

        
        
        # placeholder penalty
        penalty = 0
       
        penalty = abs(100 - (self.design_check_optimized_version(self,design_dictionary) * 100)) * 1e6
        
        return weight + penalty


    
    def design_check(self,design_dictionary):
        self.design_flag = False
        self.design_flag2 = False
        self.shearflag1 = False
        self.shearflag2 = False
        self.shearflag3 = False
        self.shearchecks = False
        self.momentchecks = False
        self.defl_check = False
        self.design_flag = self.section_classification(self, design_dictionary)
        if self.design_flag == False:
            logger.error("slender section not allowed")
            
        else:
            self.beta_value(self, design_dictionary,self.section_class)

            if self.web_philosophy == 'Thick Web without ITS':
                self.design_flag2 = self.min_web_thickness_thick_web(self,self.eff_depth,self.web_thickness,self.epsilon,"no_stiffener",0)
                
                if self.design_flag2 == True:
                    
                    #shear check
                    if self.shear_capacity_laterally_supported_thick_web(self,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness):
                        self.shearflag1 = True
                        logger.info("Shear Check passed")
                        
                    else:
                        self.shearflag1 = False
                        logger.error("Shear Check failed")

                    
                    #web buckling check
                    if self.web_buckling_laterally_supported_thick_web(self,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.material.modulus_of_elasticity,self.b1):
                        self.shearflag2 = True
                        logger.info("Web Buckling Check passed")
                    else:
                        self.shearflag2 = False
                        logger.error("Web Buckling Check failed")
                    
                    #web crippling check
                    if self.web_crippling_laterally_supported_thick_web(self,self.material.fy,self.gamma_m0,self.web_thickness,self.top_flange_thickness,self.b1):
                        self.shearflag3 = False
                        logger.info("Web Crippling Check passed")
                    else:
                        self.shearflag3 = False
                        logger.error("Web Crippling Check failed")
                    
                    if self.shearflag1 == True and self.shearflag2 == True and self.shearflag3 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False
                    
                    #support type supp or unsupp
                    if self.support_type == 'Major Laterally Supported':

                        #moment check supp
                        if self.moment_capacity_laterally_supported(self,self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class):
                            self.momentchecks = True
                            logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            logger.error("Moment Check failed")
                    
                    else:  #unsupp

                        #moment check unspp
                        if self.moment_capacity_laterally_unsupported(self,self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force):
                            self.momentchecks = True
                            logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            logger.error("Moment Check failed")
                else:
                    logger.error("Increase the web thickness")

            else: #thin web condition
                stiffener_type = None
                if self.long_Stiffner == 'Yes and 1 stiffener':
                    stiffener_type == "transverse_and_one_longitudinal_compression"
                elif self.long_Stiffner == 'Yes and 2 stiffeners':
                    stiffener_type == "transverse_and_two_longitudinal_neutral"
                else:
                    stiffener_type == "transverse_only"
                
                if self.c == 'NA':
                    logger.error("c value not provided")
                    self.c = 0
                else:
                    self.c = float(self.c)
                print("c value",self.c)
                self.design_flag2 = self.min_web_thickness_thick_web(self,self.eff_depth,self.web_thickness,self.epsilon,stiffener_type,self.c)
                if self.design_flag2 == True:

                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        #shear check
                        if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.web_thickness,self.load.shear_force,self.c):
                            self.shearflag1 = True
                            logger.info("Shear Check passed")
                        else:
                            self.shearflag1 = False
                            logger.error("Shear Check failed")
                    
                        if self.shear_buckling_check_intermediate_stiffener(self,self.eff_depth,self.web_thickness,self.c,self.epsilon,self.IntStiffThickness,self.IntStiffnerwidth,self.V_cr,self.load.shear_force,self.gamma_m0,self.material.fy,self.material.modulus_of_elasticity):
                            self.shearflag2 = True
                            logger.info("Shear Buckling Check passed")
                        else:
                            self.shearflag2 = False
                            logger.error("Shear Buckling Check failed")
                    
                    else: #tension field

                        if self.shear_buckling_check_tension_field(self,self.eff_depth,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.web_thickness,self.c):
                            self.shearflag1 = True
                            logger.info("Shear Buckling Check passed")
                        else:
                            self.shearflag1 = False
                            logger.error("Shear Buckling Check failed")

                        if self.tension_field_end_stiffener(self,self.eff_depth,self.web_thickness,self.material.fy,self.V_tf,self.V_cr,self.load.shear_force,self.load.moment):
                            self.shearflag2 = True
                            logger.info("Tension Field Check passed")
                        else:
                            self.shearflag2 = False
                            logger.error("Tension Field Check failed")
                      
                    if self.shearflag1 == True and self.shearflag2 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False

                    
                    if self.support_type == 'Major Laterally Supported':
                        #moment check supp
                        if self.moment_capacity_laterally_supported(self,self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class):
                            self.moment_checks = True
                            logger.info("Moment Check passed")
                        else:
                            self.moment_checks = False
                            logger.error("Moment Check failed")
                    
                    else:  #unsupp

                        #moment check unspp
                        if self.moment_capacity_laterally_unsupported(self,self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force):
                            self.moment_checks = True
                            logger.info("Moment Check passed")
                        else:
                            self.moment_checks = False
                            logger.error("Moment Check failed")



                

                else:
                    logger.error("Increase the web thickness")

       


        #deflection checks
        if self.evaluate_deflection_kNm_mm(self,self.load.moment, self.effective_length, self.material.modulus_of_elasticity, self.loading_case):
            self.defl_check = True
            logger.info("Deflection Check passed")
        else:
            self.defl_check = False
            logger.error("Deflection Check failed")

        #in pso check for self.moment_checks and self.shearchecks

        #for customized
        if self.design_flag == True and self.design_flag2 == True and self.defl_check == True:
            pass
        self.final_format(self,design_dictionary)

    def design_check_optimized_version(self,design_dictionary):
        self.design_flag = False
        self.design_flag2 = False
        self.shearflag1 = False
        self.shearflag2 = False
        self.shearflag3 = False
        self.shearchecks = False
        self.momentchecks = False
        self.defl_check = False
        self.design_flag = self.section_classification(self, design_dictionary)
        if self.design_flag == False:
            pass
            # logger.error("slender section not allowed")
            
        else:
            self.beta_value(self, design_dictionary,self.section_class)

            if self.web_philosophy == 'Thick Web without ITS':
                self.design_flag2 = self.min_web_thickness_thick_web(self,self.eff_depth,self.web_thickness,self.epsilon,"no_stiffener",0)
                
                if self.design_flag2 == True:
                    
                    #shear check
                    if self.shear_capacity_laterally_supported_thick_web(self,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness):
                        self.shearflag1 = True
                        # logger.info("Shear Check passed")
                        
                    else:
                        self.shearflag1 = False
                        # logger.error("Shear Check failed")

                    
                    #web buckling check
                    if self.web_buckling_laterally_supported_thick_web(self,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.material.modulus_of_elasticity,self.b1):
                        self.shearflag2 = True
                        # logger.info("Web Buckling Check passed")
                    else:
                        self.shearflag2 = False
                        # logger.error("Web Buckling Check failed")
                    
                    #web crippling check
                    if self.web_crippling_laterally_supported_thick_web(self,self.material.fy,self.gamma_m0,self.web_thickness,self.top_flange_thickness,self.b1):
                        self.shearflag3 = False
                        # logger.info("Web Crippling Check passed")
                    else:
                        self.shearflag3 = False
                        # logger.error("Web Crippling Check failed")
                    
                    if self.shearflag1 == True and self.shearflag2 == True and self.shearflag3 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False
                    
                    #support type supp or unsupp
                    if self.support_type == 'Major Laterally Supported':

                        #moment check supp
                        if self.moment_capacity_laterally_supported(self,self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class):
                            self.momentchecks = True
                            # logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            # logger.error("Moment Check failed")
                    
                    else:  #unsupp

                        #moment check unspp
                        if self.moment_capacity_laterally_unsupported(self,self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force):
                            self.momentchecks = True
                            # logger.info("Moment Check passed")
                        else:
                            self.momentchecks = False
                            # logger.error("Moment Check failed")
                else:
                    # logger.error("Increase the web thickness")
                    pass

            else: #thin web condition
                stiffener_type = None
                if self.long_Stiffner == 'Yes and 1 stiffener':
                    stiffener_type == "transverse_and_one_longitudinal_compression"
                elif self.long_Stiffner == 'Yes and 2 stiffeners':
                    stiffener_type == "transverse_and_two_longitudinal_neutral"
                else:
                    stiffener_type == "transverse_only"
                
                if self.c == 'NA':
                    # logger.error("c value not provided")
                    self.c = 0
                else:
                    self.c = float(self.c)
                self.design_flag2 = self.min_web_thickness_thick_web(self,self.eff_depth,self.web_thickness,self.epsilon,stiffener_type,self.c)
                if self.design_flag2 == True:

                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        #shear check
                        if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.web_thickness,self.load.shear_force,self.c):
                            self.shearflag1 = True
                            # logger.info("Shear Check passed")
                        else:
                            self.shearflag1 = False
                            # logger.error("Shear Check failed")
                    
                        if self.shear_buckling_check_intermediate_stiffener(self,self.eff_depth,self.web_thickness,self.c,self.epsilon,self.IntStiffThickness,self.IntStiffnerwidth,self.V_cr,self.load.shear_force,self.gamma_m0,self.material.fy,self.material.modulus_of_elasticity):
                            self.shearflag2 = True
                            # logger.info("Shear Buckling Check passed")
                        else:
                            self.shearflag2 = False
                            # logger.error("Shear Buckling Check failed")
                    
                    else: #tension field

                        if self.shear_buckling_check_tension_field(self,self.eff_depth,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.web_thickness,self.c):
                            self.shearflag1 = True
                            # logger.info("Shear Buckling Check passed")
                        else:
                            self.shearflag1 = False
                            # logger.error("Shear Buckling Check failed")

                        if self.tension_field_end_stiffener(self,self.eff_depth,self.web_thickness,self.material.fy,self.V_tf,self.V_cr,self.load.shear_force,self.load.moment):
                            self.shearflag2 = True
                            # logger.info("Tension Field Check passed")
                        else:
                            self.shearflag2 = False
                            # logger.error("Tension Field Check failed")
                      
                    if self.shearflag1 == True and self.shearflag2 == True:
                        self.shearchecks = True
                    else:
                        self.shearchecks = False

                    
                    if self.support_type == 'Major Laterally Supported':
                        #moment check supp
                        if self.moment_capacity_laterally_supported(self,self.load.shear_force,self.plast_sec_mod_z,self.elast_sec_mod_z,self.material.fy,self.gamma_m0,self.total_depth,self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness,self.section_class):
                            self.moment_checks = True
                            # logger.info("Moment Check passed")
                        else:
                            self.moment_checks = False
                            # logger.error("Moment Check failed")
                    
                    else:  #unsupp

                        #moment check unspp
                        if self.moment_capacity_laterally_unsupported(self,self.material.modulus_of_elasticity,self.effective_length,self.total_depth,self.top_flange_thickness,self.bottom_flange_thickness,self.top_flange_width,self.bottom_flange_width,self.web_thickness,self.loading_case,self.gamma_m0,self.material.fy,self.load.shear_force):
                            self.moment_checks = True
                            # logger.info("Moment Check passed")
                        else:
                            self.moment_checks = False
                            # logger.error("Moment Check failed")



                

                else:
                    # logger.error("Increase the web thickness")
                    pass

       


        #deflection checks
        if self.evaluate_deflection_kNm_mm(self,self.load.moment, self.effective_length, self.material.modulus_of_elasticity, self.loading_case):
            self.defl_check = True
            # logger.info("Deflection Check passed")
        else:
            self.defl_check = False
            # logger.error("Deflection Check failed")

        #in pso check for self.moment_checks and self.shearchecks

        #for customized
        print(f"RATIOS  moment {self.moment_ratio} shear {self.shear_ratio} deflection {self.deflection_ratio}")
        return max(self.moment_ratio,self.shear_ratio,self.deflection_ratio)
                    

        
    def optimized_method(self,design_dictionary,is_thick_web, is_symmetric):
        # is_thick_web = False
        # is_symmetric = False
        # if self.web_philosophy == 'Thick Web without ITS':
        #     is_thick_web = True
        # else:
        #     is_thick_web = False
        # if design_dictionary[KEY_IS_IT_SYMMETRIC] == 'Symmetric Girder':
        #     is_symmetric = True
        # else:
        #     is_symmetric = False
        variable_list = self.build_variable_structure(self,is_thick_web, is_symmetric)
        lb, ub = self.get_bounds(self,variable_list)
        optimizer = GlobalBestPSO(
        n_particles=50,
        dimensions=len(variable_list),
        options={'c1': 1.5, 'c2': 1.5, 'w': 0.4},
        bounds=(lb, ub)
    )
        fp = self.generate_first_particle(self,float(self.length) * 1000, float(self.load.moment), float(self.material.fy),is_thick_web,is_symmetric)
        optimizer.swarm.position[0] = np.clip(fp, lb, ub)

        best_cost, best_pos = optimizer.optimize(
        objective_func=lambda swarm: self.objective_function(self,swarm, variable_list,design_dictionary,is_symmetric,is_thick_web),
        iters=100
    )
        logger.info("PSO calculation successfully completed")
        print("Best cost:", best_cost)
        best_design_var = dict(zip(variable_list, best_pos))
        print("Best design variables:", best_design_var)
        def ceil_to_nearest(x, multiple):
            return float(math.ceil(x / multiple) * multiple)
        if is_symmetric:
            self.bottom_flange_thickness = self.top_flange_thickness = float(best_design_var['tf'])
            for i in self.bottom_flange_thickness_list:
                if float(i) > self.bottom_flange_thickness:
                    self.bottom_flange_thickness = float(i)
                    self.top_flange_thickness = float(i)
                    break
            self.web_thickness = float(best_design_var['tw'])
            for i in self.web_thickness_list:
                if float(i) > self.web_thickness:
                    self.web_thickness = float(i)
                    break

            self.top_flange_width = self.bottom_flange_width = round(float(best_design_var['bf']),0)
            self.top_flange_width = self.bottom_flange_width = ceil_to_nearest(self.top_flange_width,25)
            self.total_depth = round(float(best_design_var['D']),0)
            self.total_depth =  ceil_to_nearest(self.total_depth,25)


            # self.IntStiffThickness = float(best_design_var[''])
            # for i in self.int_thickness_list:
            #     if float(i) > se
        else:
            self.bottom_flange_thickness = float(best_design_var['tf_bot'])
            for i in self.bottom_flange_thickness_list:
                if float(i) > self.bottom_flange_thickness:
                    self.bottom_flange_thickness = float(i)
                    break
            self.top_flange_thickness = float(best_design_var['tf_top'])
            for i in self.top_flange_thickness_list:
                if float(i) > self.top_flange_thickness:
                    self.top_flange_thickness = float(i)
                    break
            self.web_thickness = float(best_design_var['tw'])
            for i in self.web_thickness_list:
                if float(i) > self.web_thickness:
                    self.web_thickness = float(i)
                    break

            self.bottom_flange_width = round(float(best_design_var['bf_bot']),0)
            self.bottom_flange_width = ceil_to_nearest(self.bottom_flange_width,25)
            self.top_flange_width = round(float(best_design_var['bf_top']),0)
            self.top_flange_width = ceil_to_nearest(self.top_flange_width,25)
            self.total_depth = round(float(best_design_var['D']),0)
            self.total_depth =  ceil_to_nearest(self.total_depth,25)
            

        if not is_thick_web:
            self.IntStiffThickness = float(best_design_var['t_stiff'])
            for i in self.int_thickness_list:
                if float(i) > self.IntStiffThickness:
                    self.IntStiffThickness = float(i)
                    break
            
            self.c = round(float(best_design_var['c']),0)
            self.c = ceil_to_nearest(self.c,25)

        
        logger.info(f"Optimized values : Flange width top and bottom {self.top_flange_width} {self.bottom_flange_width} flange thickness top and bottom {self.top_flange_thickness} { self.bottom_flange_thickness} web_thickness  {self.web_thickness} total depth { self.total_depth} C value {self.c} thickness stiffener { self.IntStiffThickness}")

        self.design_check(self,design_dictionary)



        # logger.info(f"Web Thickness: {self.web_thickness}, Flange Thickness Top: {self.top_flange_thickness}, Flange Width Top: {self.top_flange_width}, Total Depth: {self.total_depth}")



        




        
    
    def final_format(self,design_dictionary):
        
        self.result_designation = (str(int(self.total_depth)) + " x " +str(int(self.web_thickness)) + " x " +str(int(self.bottom_flange_width)) + " x " +str(int(self.bottom_flange_thickness)) + " x " +str(int(self.top_flange_width)) + " x "  +str(int(self.top_flange_thickness)))
        if self.moment_ratio == None:
            self.moment_ratio = 0
        if self.shear_ratio == None:
            self.shear_ratio = 0
        print(self.moment_ratio, self.shear_ratio)
        self.result_UR = max(self.moment_ratio,self.shear_ratio) * 100
        self.section_classification_val = self.section_class
        if self.beta_b_lt == None:
            self.beta_b_lt = 0
        self.betab = round(self.beta_b_lt,2)
        self.effectivearea = Unsymmetrical_I_Section_Properties.calc_area(self,self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
        if self.Md == None:
            self.Md = 0

        if self.M_cr == None:
            self.M_cr = 0
        if self.V_cr == None:
            self.V_cr = 0
        if self.shear_type == 'Low':
            self.design_moment = round(self.Md/1000000,1)
        else:
            self.design_moment = round(self.Md/1000000,1)
        if self.support_type == 'Major Laterally Unsupported':
            self.critical_moment = round(self.M_cr/1000000,1)
            self.torsion_cnst = round(self.It/10000,0)
            self.warping_cnst = round(self.Iw/1000000,0)    
        self.intstiffener_thk = self.IntStiffThickness
        self.longstiffener_thk = self.LongStiffThickness
        self.intstiffener_spacing = self.c
        self.design_status = True

class Section:
    def __init__(self):
        self.tf = self.tw = self.bf = self.D = self.tf_top = self.tf_bot = self.bf_top = self.bf_bot = self.c = self.t_stiff = None
    # ... add other properties as needed
    
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
