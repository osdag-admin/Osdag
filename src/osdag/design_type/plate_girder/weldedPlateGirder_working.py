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
import re

scale = 1  # For resizing components

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
            return TYPE_TEXTBOX
        else:
            return ''
        
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
        t46 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_WEB_THICKNESS_PG, TYPE_COMBOBOX, self.customized_options)
        lst.append(t46)

        t2 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_Bflange_PG, TYPE_LABEL, self.customized_dimensions_1)
        lst.append(t2)
        t3 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_Bflange_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t3)
        t47 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_TOP_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, self.customized_options)
        lst.append(t47)

        t23 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_Bflange_PG, TYPE_LABEL, self.customized_dimensions_2)
        lst.append(t23)
        t24 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_Bflange_PG, TYPE_TEXTBOX, self.customized_dims)
        lst.append(t24)
        t47 = ([KEY_OVERALL_DEPTH_PG_TYPE], KEY_BOTTOM_FLANGE_THICKNESS_PG, TYPE_COMBOBOX, self.customized_options)
        lst.append(t47)

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
            self.web_thickness = 1
            self.top_flange_width = 1
            self.top_flange_thickness = 1
            self.bottom_flange_width = 1
            self.bottom_flange_thickness = 1
        
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

        self.long_thickness_list = design_dictionary[KEY_LongitudnalStiffener_thickness_val]
        
        
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

        self.F_q = None
        self.Critical_buckling_load = None
        self.shear_ratio = None
        self.moment_ratio = None
        self.It = None
        self.Iw = None
        self.torsion_cnst = None
        self.warping_cnst = None
        self.critical_moment = None
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
        # self.sec_prop_initial_dict = {}
        # self.failed_design_dict = {}
        self.section_classification(self, design_dictionary)
        # if self.flag:
        #     self.results(self, design_dictionary)
        self.shear_force_optimal = False
        self.moment_optimal = False
        self.min_mass = False   

        # else:
        #     pass
        #     # logger.warning(
        #     #         "Plastic section modulus of selected sections is less than required."
        #     #     )
        #     return

    # Simulation starts here
    def section_classification(self,design_dictionary):
        self.design_status = False
        # for self.web_thickness in self.web_thickness_list:
        #     for self.top_flange_thickness in self.top_flange_thickness_list:
        # print("THICKNESS VALUES INT STIFFNER", self.int_thickness_list)
        #         for
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
        self.plast_sec_mod_z = Unsymmetrical_I_Section_Properties.calc_PlasticModulusZ(self,self.total_depth,self.top_flange_width,self.bottom_flange_width,
                                                    self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness)
        self.elast_sec_mod_z =Unsymmetrical_I_Section_Properties.calc_ElasticModulusZz(self,self.total_depth,self.top_flange_width,self.bottom_flange_width,
                                                    self.web_thickness,self.top_flange_thickness,self.bottom_flange_thickness)
        print("self.plast_sec_mod_z",self.plast_sec_mod_z)
        print("self.elast_sec_mod_z",self.elast_sec_mod_z)
        self.Zp_req = self.load.moment * self.gamma_m0 / self.material.fy
        if self.plast_sec_mod_z >= self.Zp_req:
            print( 'self.section_property.plast_sec_mod_z More than Requires',self.plast_sec_mod_z,self.Zp_req)
        if self.section_class == KEY_Plastic or self.section_class == KEY_Compact:
            self.beta_b_lt = 1.0
        else:
            self.beta_b_lt = (self.elast_sec_mod_z/ self.plast_sec_mod_z)
        print("Beta value",self.beta_b_lt)
        A_vg = (self.total_depth - self.top_flange_thickness - self.bottom_flange_thickness) * self.web_thickness    
        self.V_d = ((A_vg * self.material.fy) / (math.sqrt(3) * self.gamma_m0))
        print("Shear check",self.V_d, self.material.fy)
        print("shear force ",self.load.shear_force)  #V value self.load.shear_force
        if IS800_2007.cl_8_2_1_2_high_shear_check(self.load.shear_force,self.V_d):
            self.shear_type = 'High' #high shear
            if self.support_type == 'Major Laterally Supported':
                if self.web_philosophy == 'Thick Web without ITS':
                    if IS800_2007.cl_8_6_1_1_plate_girder_minimum_web_a(self.total_depth,self.web_thickness,self.epsilon,self.top_flange_thickness,self.bottom_flange_thickness):
                        self.Mdv = self.calc_Mdv(self,self.load.shear_force,self.V_d, self.plast_sec_mod_z,self.elast_sec_mod_z, self.material.fy, self.gamma_m0, self.total_depth, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                        self.moment_ratio = self.load.moment / self.Mdv
                        print("Ratio for moment", self.moment_ratio)
                        self.web_buckling_check(self)
                        print("Bending moment",self.Mdv/1000000)
                        self.eff_depth = self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness)
                        
                        n1 = self.eff_depth / 2
                        Ac = (self.b1 + n1) * self.web_thickness
                        slenderness_input = 2.5 * self.eff_depth / self.web_thickness
                        self.fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
                            self.material.fy,
                            self.gamma_m0,
                            slenderness_input,
                            self.material.modulus_of_elasticity
                        )

                        print("Web Buckling at ")
                        print(f"fcd: {self.fcd}N/mm2")
                        Critical_buckling_load = round(Ac * self.fcd / 1000, 2)
                        print(f"Critical buckling load: {Critical_buckling_load}kN")

                        #Web Crippling
                        print("Web Crippling")
                        n2= 2.5*self.top_flange_thickness
                        Critical_crippling_load= round((self.b1+n2)*self.web_thickness*self.material.fy/(1.1*1000),2)
                        print(f"Critical crippling load: {Critical_crippling_load}kN")
                        


                        if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':       #buckling method
                            c = 0
                            if self.c != 'NA':
                                c = float(self.c)
                            if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,A_vg,self.load.shear_force,c):
                                print("Check passed")
                            else:
                                print("Check Failed")
                        else:   #tension field
                            pass
                                #to add tension field check


                    
                            
                    else:
                        logger.error("Web thickness is not sufficient\n Re-enter new thickness")
                
                else: #thin web condition
                    
                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        else:
                            # assuming stiffner thickness is a val for now - to add list parsing
                            # Simple post critical check
                            if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,A_vg,self.load.shear_force,float(self.c)):
                                print("Simple Post Critical Check passed")
                            else:
                                print("Simple Post Critical Check Failed")
                            # intermediate stiffner shear check
                            if self.shear_buckling_check_intermediate_stiffner(self,self.eff_depth,float(self.IntStiffThickness),float(self.IntStiffnerwidth),self.V_cr,self.web_thickness):
                                print("Shear Intermediate check passed")
                            else:
                                print("Intermediate Stiffner thickness needs to be increased or Intermediate Stiffner spacing needs to be reduced")
                            #end stiffener check
                            if self.simple_post_critical_end_stiffener(self,self.eff_depth, self.web_thickness, self.material.fy, self.load.moment,self.V_cr,self.load.shear_force):
                                print("End stiffner check okay")
                            else:
                                print("CHECK THE NEXT THICKNESS")


                            #longitudnal stiffner check
                            if self.long_Stiffner == 'Yes':
                                print("Checking long stiffener")
                                if self.design_longitudinal_stiffeners(self,self.eff_depth, self.web_thickness, float(self.c), self.epsilon):
                                    logger.error("Longitudnal Stiffner thickess is less than required")
                                else:
                                    print("Longitudnal Stiffner check passed")

                            #Intermediate stiffner check
                            self.Is = float((self.IntStiffThickness) * (((self.IntStiffnerwidth * 2) + self.web_thickness) ** 3)/ 12)-(((self.IntStiffThickness) * ((( self.web_thickness) ** 3)/ 12)))
                            if IS800_2007.cl_8_7_2_4_min_stiffners(float(self.c),self.eff_depth,self.web_thickness,self.Is):
                                print("Stiffener provided is OKAY")
                            else:
                                print("As per minimum stiffener required by IS 800 clause 8.7.2.4 is not satisfied. Reduce spacing or increase the thickness of the stiffener")

                    else: #tension field
                    
                        lever_arm = self.total_depth - (self.top_flange_thickness / 2) - (self.bottom_flange_thickness / 2)  # in mm
                        Nf = self.load.moment * 1_000_000 / lever_arm
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        c = float(self.c)
                        if self.shear_buckling_check_tension_field(self,self.eff_depth,A_vg,c,Nf):
                            print("Check passed")
                        else:
                            print("Check Failed")
                        
                        if self.tension_field_end_stiffner(self,self.eff_depth,self.web_thickness,self.material.fy,self.V_tf,self.V_cr,self.load.shear_force,self.load.moment):
                            print("End stiffner TF check okay")
                        else:
                            print("CHECK THE NEXT THICKNESS")
                             
                        

                    
            else: #unsupported type 
                if self.web_philosophy == 'Thick Web without ITS':
                    self.eff_depth = self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness)
                    n1 = self.eff_depth / 2
                    Ac = (self.b1 + n1) * self.web_thickness
                    slenderness_input = 2.5 * self.eff_depth / self.web_thickness
                    self.fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
                            self.material.fy,
                            self.gamma_m0,
                            slenderness_input,
                            self.material.modulus_of_elasticity
                        )

                    print("Web Buckling at ")
                    print(f"fcd: {self.fcd}N/mm2")
                    Critical_buckling_load = round(Ac * self.fcd / 1000, 2)
                    print(f"Critical buckling load: {Critical_buckling_load}kN")

                    #Web Crippling
                    print("Web Crippling")
                    n2= 2.5*self.top_flange_thickness
                    Critical_crippling_load= round((self.b1+n2)*self.web_thickness*self.material.fy/(1.1*1000),2)
                    print(f"Critical crippling load: {Critical_crippling_load}kN")
                
                else: #thin web condition
                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':

                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        else:
                            # assuming stiffner thickness is a val for now - to add list parsing
                            # Simple post critical check
                            if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,A_vg,self.load.shear_force,float(self.c)):
                                print("Simple Post Critical Check passed")
                            else:
                                print("Simple Post Critical Check Failed")
                            # intermediate stiffner shear check
                            if self.shear_buckling_check_intermediate_stiffner(self,self.eff_depth,float(self.IntStiffThickness),float(self.IntStiffnerwidth),self.V_cr,self.web_thickness):
                                print("Shear Intermediate check passed")
                            else:
                                print("Intermediate Stiffner thickness needs to be increased or Intermediate Stiffner spacing needs to be reduced")
                            #end stiffener check
                            if self.simple_post_critical_end_stiffener(self,self.eff_depth, self.web_thickness, self.material.fy, self.load.moment,self.V_cr,self.load.shear_force):
                                print("End stiffner check okay")
                            else:
                                print("CHECK THE NEXT THICKNESS")


                            #longitudnal stiffner check
                            if self.long_Stiffner == 'Yes':
                                print("Checking long stiffener")
                                if self.design_longitudinal_stiffeners(self,self.eff_depth, self.web_thickness, float(self.c), self.epsilon):
                                    logger.error("Longitudnal Stiffner thickess is less than required")
                                else:
                                    print("Longitudnal Stiffner check passed")

                            #Intermediate stiffner check
                            self.Is = float((self.IntStiffThickness) * (((self.IntStiffnerwidth * 2) + self.web_thickness) ** 3)/ 12)-(((self.IntStiffThickness) * ((( self.web_thickness) ** 3)/ 12)))
                            if IS800_2007.cl_8_7_2_4_min_stiffners(float(self.c),self.eff_depth,self.web_thickness,self.Is):
                                print("Stiffener provided is OKAY")
                            else:
                                print("As per minimum stiffener required by IS 800 clause 8.7.2.4 is not satisfied. Reduce spacing or increase the thickness of the stiffener")
                    else: #tension field
                        lever_arm = self.total_depth - (self.top_flange_thickness / 2) - (self.bottom_flange_thickness / 2)  # in mm
                        Nf = self.load.moment * 1_000_000 / lever_arm
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        c = float(self.c)
                        if self.shear_buckling_check_tension_field(self,self.eff_depth,A_vg,c,Nf):
                            print("Check passed")
                        else:
                            print("Check Failed")
                        
                        if self.tension_field_end_stiffner(self,self.eff_depth,self.web_thickness,self.material.fy,self.V_tf,self.V_cr,self.load.shear_force,self.load.moment):
                            print("End stiffner TF check okay")
                        else:
                            print("CHECK THE NEXT THICKNESS")


                G = 0.769 * 10**5
                Kw = self.get_K_from_warping_restraint(self,self.warping)
                Iy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                self.It = Unsymmetrical_I_Section_Properties.calc_TorsionConstantIt(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                self.Iw = Unsymmetrical_I_Section_Properties.calc_WarpingConstantIw(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                self.M_cr = self.calc_Mcr_LoadingCase(self,self.material.modulus_of_elasticity, G, Iy, self.It, self.Iw, self.effective_length, Kw, self.total_depth,
                            self.top_flange_thickness, self.bottom_flange_thickness, self.top_flange_width, self.bottom_flange_width,
                            self.loading_case, self.warping)
                print("Input moment",self.load.moment)
                print("It VAL",self.It, self.Iw)
                self.Md = self.bending_check_lat_unsupported(self,self.beta_b_lt, self.plast_sec_mod_z, self.elast_sec_mod_z, self.material.fy, self.M_cr,self.section_class)

                self.Mdv = self.calc_Mdv_lat_unsupported(self,self.load.shear_force,self.V_d, self.plast_sec_mod_z,self.elast_sec_mod_z, self.material.fy, self.gamma_m0, self.total_depth, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness,self.Md)
                self.moment_ratio = self.load.moment/ self.Mdv
                print("Ratio for moment", self.moment_ratio)
                print("MDV",self.Mdv)
                # print("supp mdv",self.Mdv)
                if self.Mdv >= self.load.moment:
                    print("Section is passed")
                else:
                    logger.error("Change the section")


        else: #low shear
            self.shear_type = 'Low'
            if self.support_type == 'Major Laterally Supported':  
                if self.web_philosophy == 'Thick Web without ITS':
                    if IS800_2007.cl_8_6_1_1_plate_girder_minimum_web_a(self.total_depth,self.web_thickness,self.epsilon,self.top_flange_thickness,self.bottom_flange_thickness):
                        self.Md =self.beta_b_lt * self.plast_sec_mod_z * self.material.fy / self.gamma_m0
                        print("Moment Capacity Md",self.Md/1000000, self.plast_sec_mod_z)
                        self.web_buckling_check(self)
                        self.eff_depth = self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness)
                        
                        n1 = self.eff_depth / 2
                        Ac = (self.b1 + n1) * self.web_thickness
                        slenderness_input = 2.5 * self.eff_depth / self.web_thickness
                        self.fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
                            self.material.fy,
                            self.gamma_m0,
                            slenderness_input,
                            self.material.modulus_of_elasticity
                        )

                        print("Web Buckling at ")
                        print(f"fcd: {self.fcd}N/mm2")
                        Critical_buckling_load = round(Ac * self.fcd / 1000, 2)
                        print(f"Critical buckling load: {Critical_buckling_load}kN")

                        #Web Crippling
                        print("Web Crippling")
                        n2= 2.5*self.top_flange_thickness
                        Critical_crippling_load= round((self.b1+n2)*self.web_thickness*self.material.fy/(1.1*1000),2)
                        print(f"Critical crippling load: {Critical_crippling_load}kN")
                        
                        if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':                    #bukling method
                            c = 0
                            lever_arm = self.total_depth - (self.top_flange_thickness / 2) - (self.bottom_flange_thickness / 2)  # in mm
                            Nf = self.load.moment * 1000000 / lever_arm
                            if self.c != 'NA':
                                c = float(self.c)
                            if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,A_vg,self.load.shear_force,c):
                                print("Check passed")
                            else:
                                print("Check Failed")
                            self.shear_ratio =  self.load.shear_force / self.V_cr
                            print("Ratio for shear",self.shear_ratio)
                        else:
                            pass
                    else:
                        logger.error("Web thickness is not sufficient\n Re-enter new thickness")
                
                else: #thin web condition
                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        else:
                            # assuming stiffner thickness is a val for now - to add list parsing
                            # Simple post critical check
                            if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,A_vg,self.load.shear_force,float(self.c)):
                                print("Simple Post Critical Check passed")
                            else:
                                print("Simple Post Critical Check Failed")
                            self.shear_ratio =  self.load.shear_force / self.V_cr
                            print("Ratio for shear",self.shear_ratio)
                            # intermediate stiffner shear check
                            if self.shear_buckling_check_intermediate_stiffner(self,self.eff_depth,float(self.IntStiffThickness),float(self.IntStiffnerwidth),self.V_cr,self.web_thickness):
                                print("Shear Intermediate check passed")
                            else:
                                print("Intermediate Stiffner thickness needs to be increased or Intermediate Stiffner spacing needs to be reduced")
                            #end stiffener check
                            if self.simple_post_critical_end_stiffener(self,self.eff_depth, self.web_thickness, self.material.fy, self.load.moment,self.V_cr,self.load.shear_force):
                                print("End stiffner check okay")
                            else:
                                print("CHECK THE NEXT THICKNESS")


                            #longitudnal stiffner check
                            if self.long_Stiffner == 'Yes':
                                print("Checking long stiffener")
                                if self.design_longitudinal_stiffeners(self,self.eff_depth, self.web_thickness, float(self.c), self.epsilon):
                                    logger.error("Longitudnal Stiffner thickess is less than required")
                                else:
                                    print("Longitudnal Stiffner check passed")

                            #Intermediate stiffner check
                            self.Is = float((self.IntStiffThickness) * (((self.IntStiffnerwidth * 2) + self.web_thickness) ** 3)/ 12)-(((self.IntStiffThickness) * ((( self.web_thickness) ** 3)/ 12)))
                            if IS800_2007.cl_8_7_2_4_min_stiffners(float(self.c),self.eff_depth,self.web_thickness,self.Is):
                                print("Stiffener provided is OKAY")
                            else:
                                print("As per minimum stiffener required by IS 800 clause 8.7.2.4 is not satisfied. Reduce spacing or increase the thickness of the stiffener")
                                
                    else: #tension field
                        lever_arm = self.total_depth - (self.top_flange_thickness / 2) - (self.bottom_flange_thickness / 2)  # in mm
                        Nf = self.load.moment * 1_000_000 / lever_arm
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        c = float(self.c)
                        if self.shear_buckling_check_tension_field(self,self.eff_depth,A_vg,c,Nf):
                            print("Check passed")
                        else:
                            print("Check Failed")
                        
                        if self.tension_field_end_stiffner(self,self.eff_depth,self.web_thickness,self.material.fy,self.V_tf,self.V_cr,self.load.shear_force,self.load.moment):
                            print("End stiffner TF check okay")
                        else:
                            print("CHECK THE NEXT THICKNESS")
            
            else: #unsupported
                if self.web_philosophy == 'Thick Web without ITS':
                    self.eff_depth = self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness)
                    
                    n1 = self.eff_depth / 2
                    Ac = (self.b1 + n1) * self.web_thickness
                    slenderness_input = 2.5 * self.eff_depth / self.web_thickness
                    self.fcd = IS800_2007.cl_7_1_2_1_design_compressisive_stress_plategirder(
                            self.material.fy,
                            self.gamma_m0,
                            slenderness_input,
                            self.material.modulus_of_elasticity
                        )

                    print("Web Buckling at ")
                    print(f"fcd: {self.fcd}N/mm2")
                    Critical_buckling_load = round(Ac * self.fcd / 1000, 2)
                    print(f"Critical buckling load: {Critical_buckling_load}kN")

                    #Web Crippling
                    print("Web Crippling")
                    n2= 2.5*self.top_flange_thickness
                    Critical_crippling_load= round((self.b1+n2)*self.web_thickness*self.material.fy/(1.1*1000),2)
                    print(f"Critical crippling load: {Critical_crippling_load}kN")
                else: #thin web
                    if design_dictionary[KEY_ShearBucklingOption] == 'Simple Post Critical':
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        else:
                            # assuming stiffner thickness is a val for now - to add list parsing
                            # Simple post critical check
                            if self.shear_buckling_check_simple_postcritical(self,self.eff_depth,A_vg,self.load.shear_force,float(self.c)):
                                print("Simple Post Critical Check passed")
                            else:
                                print("Simple Post Critical Check Failed")
                            # intermediate stiffner shear check
                            if self.shear_buckling_check_intermediate_stiffner(self,self.eff_depth,float(self.IntStiffThickness),float(self.IntStiffnerwidth),self.V_cr,self.web_thickness):
                                print("Shear Intermediate check passed")
                            else:
                                print("Intermediate Stiffner thickness needs to be increased or Intermediate Stiffner spacing needs to be reduced")
                            #end stiffener check
                            if self.simple_post_critical_end_stiffener(self,self.eff_depth, self.web_thickness, self.material.fy, self.load.moment,self.V_cr,self.load.shear_force):
                                print("End stiffner check okay")
                            else:
                                print("CHECK THE NEXT THICKNESS")


                            #longitudnal stiffner check
                            if self.long_Stiffner == 'Yes':
                                print("Checking long stiffener")
                                if self.design_longitudinal_stiffeners(self,self.eff_depth, self.web_thickness, float(self.c), self.epsilon):
                                    logger.error("Longitudnal Stiffner thickess is less than required")
                                else:
                                    print("Longitudnal Stiffner check passed")

                            #Intermediate stiffner check
                            self.Is = float((self.IntStiffThickness) * (((self.IntStiffnerwidth * 2) + self.web_thickness) ** 3)/ 12)-(((self.IntStiffThickness) * ((( self.web_thickness) ** 3)/ 12)))
                            if IS800_2007.cl_8_7_2_4_min_stiffners(float(self.c),self.eff_depth,self.web_thickness,self.Is):
                                print("Stiffener provided is OKAY")
                            else:
                                print("As per minimum stiffener required by IS 800 clause 8.7.2.4 is not satisfied. Reduce spacing or increase the thickness of the stiffener")
                    else: #tension field
                        lever_arm = self.total_depth - (self.top_flange_thickness / 2) - (self.bottom_flange_thickness / 2)  # in mm
                        Nf = self.load.moment * 1_000_000 / lever_arm
                        if self.c == 'NA':
                            logger.error("Intermediate Stiffner Spacing cannot be 'NA'")
                        c = float(self.c)
                        if self.shear_buckling_check_tension_field(self,self.eff_depth,A_vg,c,Nf):
                            print("Check passed")
                        else:
                            print("Check Failed")
                        
                        if self.tension_field_end_stiffner(self,self.eff_depth,self.web_thickness,self.material.fy,self.V_tf,self.V_cr,self.load.shear_force,self.load.moment):
                            print("End stiffner TF check okay")
                        else:
                            print("CHECK THE NEXT THICKNESS")

                G = 0.769 * 10**5
                Kw = self.get_K_from_warping_restraint(self,self.warping)
                Iy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                self.It = Unsymmetrical_I_Section_Properties.calc_TorsionConstantIt(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                self.Iw = Unsymmetrical_I_Section_Properties.calc_WarpingConstantIw(self, self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
                self.M_cr = self.calc_Mcr_LoadingCase(self,self.material.modulus_of_elasticity, G, Iy, self.It, self.Iw, self.effective_length, Kw, self.total_depth,
                            self.top_flange_thickness, self.bottom_flange_thickness, self.top_flange_width, self.bottom_flange_width,
                            self.loading_case, self.warping)
                print("Input moment",self.load.moment)
                print("It VAL", self.It, self.Iw)
                print("MCR VAL",self.M_cr)
                self.Md = self.bending_check_lat_unsupported(self,self.beta_b_lt, self.plast_sec_mod_z, self.elast_sec_mod_z, self.material.fy, self.M_cr,self.section_class)
                self.moment_ratio = self.load.moment/ self.Md
                print("Ratio for moment", self.moment_ratio)
                print("MD",self.Md)
                if self.Md >= self.load.moment:
                    print("Section is passed")
                else:
                    logger.error("update the section size")
                
         

        self.design_status = False
        self.final_format(self,design_dictionary)

    
    def final_format(self,design_dictionary):
        
        self.result_designation = (str(int(self.total_depth)) + " x " +str(int(self.web_thickness)) + " x " +str(int(self.bottom_flange_width)) + " x " +str(int(self.bottom_flange_thickness)) + " x " +str(int(self.top_flange_width)) + " x "  +str(int(self.top_flange_thickness)))
        if self.moment_ratio == None:
            self.moment_ratio = 0
        if self.shear_ratio == None:
            self.shear_ratio = 0
        print(self.moment_ratio, self.shear_ratio)
        self.result_UR = max(self.moment_ratio,self.shear_ratio) * 100
        self.section_classification_val = self.section_class
        self.betab = round(self.beta_b_lt,2)
        self.effectivearea = Unsymmetrical_I_Section_Properties.calc_area(self,self.total_depth, self.top_flange_width, self.bottom_flange_width, self.web_thickness, self.top_flange_thickness, self.bottom_flange_thickness)
        if self.shear_type == 'Low':
            self.design_moment = round(self.Md/1000000,1)
        else:
            self.design_moment = round(self.Mdv/1000000,1)
        if self.support_type == 'Major Laterally Unsupported':
            self.critical_moment = round(self.M_cr/1000000,1)
            self.torsion_cnst = round(self.It/10000,0)
            self.warping_cnst = round(self.Iw/1000000,0)    
        self.intstiffener_thk = self.IntStiffThickness
        self.longstiffener_thk = self.LongStiffThickness
        self.intstiffener_spacing = self.c
        self.design_status = True




    
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


    
    def web_buckling_check(self):
        self.web_buckling = IS800_2007.cl_8_2_1_web_buckling(
            d=self.total_depth - (self.top_flange_thickness + self.bottom_flange_thickness),
            tw=self.web_thickness,
            e=self.epsilon,)
        print("Web buckling",self.web_buckling)

        # if not self.web_buckling_check:
        #     self.web_not_buckling_steps(self)

    def shear_buckling_check_simple_postcritical(self,eff_depth,A_vg,V,c=0):
        if self.web_philosophy == 'Thick Web without ITS':
            K_v = 5.35
        else:
            if c/eff_depth < 1:
                K_v = 4 + 5.35/(c/eff_depth)**2
            else:
                K_v = 5.35 + 4/(c/eff_depth)**2
        E = self.material.modulus_of_elasticity
        mu = 0.3
        tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E,mu, eff_depth, self.web_thickness)
        lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(self.material.fy, tau_crc)
        tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, self.material.fy)
        self.V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
        print("V_cr value",self.V_cr)
        if self.V_cr > V:
            return True
        else:
            return False
        
    def shear_buckling_check_intermediate_stiffner(self,d,IntStiffThickness,IntStiffnerwidth,V_cr,tw):
        I_x = ((((IntStiffnerwidth * 2) + tw )**  3 * (IntStiffThickness )) / 12)-(IntStiffThickness * tw **  3 / 12)
        A_s = IntStiffnerwidth * IntStiffThickness * 2
        r_x = (I_x / A_s) ** 0.5
        le = self.lefactor * d
        slenderness_input = le / r_x
        dataframe = IS800_2007.cl_7_1_2_1_design_compressisive_stress_fcd_buckling_class_c()
        interp_val = self.interpolate_value(self,slenderness_input, self.material.fy,dataframe)
        fcd = round(interp_val, 2)
        self.Critical_buckling_load = round(A_s * fcd / 1000, 2)
        print("Shear force ",self.load.shear_force)
        self.F_q = (self.load.shear_force - V_cr) /self.gamma_m0
        print("Shear intermeditate stiffner f_q , cbl",self.F_q,self.Critical_buckling_load)
        if self.F_q < self.Critical_buckling_load:
            return True
        else:
            return False
        

    def design_longitudinal_stiffeners(self,d, tw, c, eps_w, second_stiffener=False):
        """
        Determine whether horizontal (longitudinal) stiffeners are required in a plate girder
        and compute the minimum required second moment of area Is.

        Parameters
        ----------
        d : float
            Clear depth of web (distance between flanges), in mm (or consistent units).
        tw : float
            Web thickness, in mm.
        c : float
            Clear distance from compression - flange angles to the neutral axis, in mm.
        eps_w : float
            Web slenderness parameter ε_w = √(E/Fy), unitless.
        second_stiffener : bool, optional
            If True, assume a stiffener at the neutral axis will be provided (enabling Eq. 2.39).

        Returns
        -------
        dict
            {
                'required'     : bool,   # Is any stiffener required?
                'slenderness'  : float,  # Governing slenderness ratio used
                'limit'        : float,  # Allowable slenderness limit
                'locations'    : tuple,  # (x1, x2), distances from comp. flange to stiffeners
                'I1_min'       : float,  # Eq. 2.40: first stiffener Is ≥ 4·c·t_w³
                'I2_min'       : float,  # Eq. 2.41: second stiffener Is ≥ d2²·t_w³, where d2=2·c
                'Imin_global'  : float,  # Eqs. 2.42 - 2.43: overall minimum stiffener Is
                'Is_required'  : float   # Governing Is = max(I1_min, I2_min, Imin_global)
            }

        Notes
        -----
        - Uses Eq. 2.36 - 2.38 for the unstiffened web checks; if `second_stiffener=True`, uses
        Eq. 2.39 (d/tw ≤ 400·ε_w) instead.
        - Locations: x1 = c/5 from compression flange; x2 = 0 (neutral axis).
        """
        # 1) determine slenderness check
        if second_stiffener:
            # Eq. 2.39: when a stiffener is at the neutral axis
            slenderness = d / tw
            limit = 400 * eps_w
        else:
            if 2.4*d >= c >= d:
                # Eq. 2.36
                slenderness = d / tw
                limit = 250 * eps_w
            elif d > c >= 0.74*d:
                # Eq. 2.37
                slenderness = c / tw
                limit = 250 * eps_w
            else:
                # c < 0.74 d → Eq. 2.38
                slenderness = d / tw
                limit = 340 * eps_w

        required = slenderness > limit

        # 2) stiffener locations
        x1 = c / 5.0        # first stiffener at 1/5 of c
        x2 = 0.0            # second stiffener at neutral axis

        # 3) design criteria for Is
        I1_min = 4.0 * c * tw**3           # Eq. 2.40
        d2 = 2.0 * c                       # twice clear distance to NA
        I2_min = d2**2 * tw**3             # Eq. 2.41

        # 4) global minimum (Eqs. 2.42–2.43)
        cd_ratio = c / d
        if cd_ratio >= math.sqrt(2):
            Imin_global = 0.75 * d * tw**3
        else:
            Imin_global = (1.5 * d * tw**3) / (c**2)

        Is_required = max(I1_min, I2_min, Imin_global)
        Is_provided = (self.eff_width_longitudnal * (self.LongStiffThickness ** 3)) / 12

        print("Req",Is_required,"Prov",Is_provided)
        print(f"'required': {required} 'slenderness': {slenderness} 'limit': {limit},'locations': {(x1, x2)} 'I1_min': {I1_min}  'I2_min': {I2_min} 'Imin_global': {Imin_global} 'Is_required': {Is_required}")

        if Is_required > Is_provided:
            return True
        else:
            return False

        # return {
        #     'required': required,
        #     'slenderness': slenderness,
        #     'limit': limit,
        #     'locations': (x1, x2),
        #     'I1_min': I1_min,
        #     'I2_min': I2_min,
        #     'Imin_global': Imin_global,
        #     'Is_required': Is_required
        # }



    def simple_post_critical_end_stiffener(self,d, tw, fyw, V_cr, gamma_m0, c):
        """
            Calculates simple-post critical end-panel stiffener requirements.
                Parameters:
            d            : float : depth of web panel (mm)
            tw           : float : thickness of web (mm)
            fyw          : float : yield stress of web (MPa or N/mm²)
            flange_width : float : outstanding flange width (mm)
            gamma_m0    : float : partial safety factor for material
            c            : float : Stiffener spacing (mm)
                
        V_cr: critical shear buckling force (kN)
        V_dp: panel shear strength (kN)
        H_q: horizontal anchor force (kN)
        R_tf: reaction force at stiffener (kN)
        M_tf: moment demand at stiffener (kN·m)
        stiffener_width: recommended stiffener width (mm)
        max_thickness: maximum allowable stiffener thickness (mm)
        """# Panel shear strength V_dp (kN)
        V_dp = (d * tw * fyw / math.sqrt(3)) / 1000
        # Horizontal anchor force H_q (kN)
        if V_dp <= V_cr:
            # raise ValueError("Stiffeners not required: V_dp <= V_cr")
            logger.error("Stiffeners not required: V_dp <= V_cr")
            H_q = 0
        else:
            H_q = 1.25 * V_dp * math.sqrt(1 - (V_cr / V_dp))
        # Reaction force R_tf (kN)
        R_tf = H_q / 2
        A_v= d * tw
        V_n= (fyw * A_v) /( 1000 * math.sqrt(3) * gamma_m0)
        # Moment demand M_tf (kN·m)
        M_tf = (H_q * d)  / 10
        y = c / 2
        I = tw * c ** 3 / 12
        M_q = (I * fyw) / (gamma_m0 * y)
        if V_n >= R_tf:
            if M_q >= M_tf:
                return True
        return False
    
    def tension_field_end_stiffner(self,d,tw,fyw,V_tf,V_cr,shear_force,moment):
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
        if V_n >= R_tf:
            if M_q >= M_tf:
                return True
        return False



    def shear_buckling_check_tension_field(self,eff_depth,A_vg,c=0,Nf = 0):
        if self.web_philosophy == 'Thick Web without ITS':
            K_v = 5.35
        else:
            if c/eff_depth < 1:
                K_v = 4 + 5.35/(c/eff_depth)**2
            else:
                K_v = 5.35 + 4/(c/eff_depth)**2
        E = self.material.modulus_of_elasticity
        mu = 0.3
        tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(K_v, E,mu, eff_depth, self.web_thickness)
        lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(self.material.fy, tau_crc)
        tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, self.material.fy)
        self.V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, A_vg)
        phi,M_fr,s, w_tf,sai,fv,self.V_tf = IS800_2007.cl_8_4_2_2_TensionField( c, eff_depth, self.web_thickness, self.material.fy, self.top_flange_width,self.top_flange_thickness, self.material.fy,Nf, self.gamma_m0, A_vg,tau_b,self.load.shear_force)
        print("vtf val",self.V_tf)
        if self.V_tf >= self.load.shear_force:
            return True
        else:
            return False
        
    def bending_check_lat_unsupported(self,beta_b_lt, plast_sec_mod_z, elast_sec_mod_z, fy, M_cr,section_class):
        self.lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(beta_b_lt,plast_sec_mod_z,elast_sec_mod_z,fy,M_cr)

        self.phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(self.alpha_lt, self.lambda_lt)
        self.X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(self.phi_lt, self.lambda_lt)
        self.fbd_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(self.X_lt,fy, self.gamma_m0)
        self.Md = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(plast_sec_mod_z,elast_sec_mod_z,self.fbd_lt,section_class)


        return round(self.Md,2)


    def calc_Mdv(self,V, Vd, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot):  #only for major laterally supp
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
        print("Aw",Aw,"Zfd",Zfd)

        # Calculating Mfd
        Mfd = Zfd * Fy / gamma_m0


        # Calculating Md (Plastic Design Moment)
        Md = Zp * Fy / gamma_m0

        # Calculating Mdv
        Mdv = Md - beta * (Md - Mfd)

        # Limiting value as per the provided formula
        Mdv_limit = (1.2 * Ze * Fy) / gamma_m0
        print("Mfd",Mfd/1000000,"Mdv",Mdv/1000000, "Mdv_limit",Mdv_limit/1000000)

        return round(min(Mdv, Mdv_limit), 2)
    
    def calc_Mdv_lat_unsupported(self,V, Vd, Zp, Ze, Fy, gamma_m0, D, tw, tf_top, tf_bot,Md):  #only for major laterally supp
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
        print("Mfd",Mfd,"Mdv",Mdv, "Mdv_limit",Mdv_limit)
        return round(min(Mdv, Mdv_limit), 2)

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

    def calc_Mcr_LoadingCase(self,E, G, Iy, It, Iw, LLT, Kw, D,
                            tf_top, tf_bot, Bf_top, Bf_bot,
                            LoadingCase, warping_condition):
        """
        Calculate Elastic Critical Moment Mcr based on IS 800:2007 (Annex E or Eq 2.20 for symmetric).
        Returns:
            Mcr : Elastic Critical Moment in N·mm
        """
        yg = D / 2
        yj = self.calc_yj(self,Bf_top, tf_top, Bf_bot, tf_bot, D)
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
            term3 = (G * It * LLT**2) / (math.pi**2 * E * Iy)
            Mcr = term1 * math.sqrt(term2 + term3)
            print("It", It, "Iw", Iw, "LLT", LLT, "E", E, "I", Iy, "G", G)
        else:
            # Unsymmetric case (Annex E full formula)
            term1 = (math.pi ** 2 * E * Iy) / (LLT ** 2)
            bracket = ((K_value / Kw) ** 2 * (Iw / Iy) +
                    (G * It * LLT ** 2) / (math.pi ** 2 * E * Iy) +
                    (c2 * yg - c3 * yj) ** 2)
            Mcr = c1 * term1 * math.sqrt(bracket) - term1 * (c2 * yg - c3 * yj)
            print("It", It, "Iw", Iw, "LLT", LLT, "E", E, "I", Iy, "G", G)
        return Mcr  # in N·mm
                        
    def shear_stress_unsym_I(self, V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w):

        # Part areas [mm^2]
        A_t = b_ft * t_ft
        A_b = b_fb * t_fb
        A_w = t_w  * h_w

        # Section total depth & area
        D = t_fb + h_w + t_ft
        A = A_t + A_b + A_w

        # Centroid y‐coords from bottom of bottom flange [mm]
        y_b =  t_fb/2
        y_w =  t_fb + h_w/2
        y_t =  t_fb + h_w + t_ft/2

        # Neutral axis from bottom [mm]
        y_na = (A_b*y_b + A_w*y_w + A_t*y_t) / A

        # Second moment I_z [mm^4]
        I_b = b_fb*t_fb**3/12 + A_b*(y_b - y_na)**2
        I_w = t_w *h_w**3/12 + A_w*(y_w - y_na)**2
        I_t = b_ft*t_ft**3/12 + A_t*(y_t - y_na)**2
        I_z = I_b + I_w + I_t

        # First moments Q [mm^3]
        Q_bot = A_b * abs(y_na - y_b)
        Q_top = A_t * abs(y_t - y_na)

        # Shear flows q = V*Q / I  [kN·mm^3 / mm^4 = kN/mm]
        q_bot = V_ed * Q_bot / I_z
        q_top = V_ed * Q_top / I_z

        return {
            'y_na_mm': y_na,    'I_z_mm4': I_z,
            'Q_top_mm3': Q_top,'Q_bot_mm3': Q_bot,
            'q_top_kN_per_mm': q_top,
            'q_bot_kN_per_mm': q_bot,
        }
    
    def weld_leg_from_q_with_cl10(self,
    q_kN_per_mm,              # shear flow [kN/mm]
    ultimate_stresses,        # list of MPa
    fabrication='shop'
):
        """
        Compute fillet‐weld leg a [mm] from shear flow,
        using f_wd from cl.10.5.7.1.1.
        """
        # 1) get f_wd in MPa → convert to N/mm²
        f_wd = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses, fabrication
        )                   # MPa

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
        sf = self.shear_stress_unsym_I(self,V_ed, b_ft, t_ft, b_fb, t_fb, t_w, h_w)

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
            'a_top_mm':    a_top,
            'a_bot_mm':    a_bot
        }
    
    def weld_for_end_stiffener_autoL(self,
    # stiffener
    t_st, b_st,          # thickness & height [mm]
    # loads
    V_ed, V_unstf,       # design shear & unstiffened capacity [kN]
    # section geometry
    D, t_ft, t_fb        # overall depth & flange thicknesses [mm]
):
        """
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
        q1 = t_st**2 / (5 * b_st)

        # 2) stiffener shear per unit length
        delta_V = max(V_ed - V_unstf, 0)
        q2 = delta_V / L_weld

        # 3) total on one side
        q_tot = q1 + q2

        # 4) split into two welds (each face)
        q_each = q_tot / 2

        return {
            'L_weld_mm':   L_weld,
            'q1_min':      q1,
            'q2_ext':      q2,
            'q_total':     q_tot,
            'q_each_weld': q_each
        }
    
    def deflection_from_moment_kNm_mm(self,M_kNm, L_mm, E, I, case):
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
        M = M_kNm * 1e3  # kN·m → N·m
        L = L_mm / 1e3  # mm → m

        pref = M * L ** 2 / (E * I)
        if case == 'simple_udl':
            return (5 / 48) * pref
        elif case == 'fixed_udl':
            return (1 / 32) * pref
        elif case == 'simple_point':
            return (1 / 12) * pref
        elif case == 'fixed_point':
            return (1 / 24) * pref
        else:
            raise ValueError(
                "Unknown case. Use 'simple_udl', 'fixed_udl', 'simple_point', or 'fixed_point'."
            )


    def evaluate_deflection_kNm_mm(self,
            M_kNm, L_mm, E, I, case, criteria_list=VALUES_MAX_DEFL
    ):
        """
        1) Calculate deflection from moment (with unit conversions).
        2) Compare against span-based limits.
        Returns (delta_m, results_dict, best_criterion).
        """
        # 1) compute deflection in meters
        delta = self.deflection_from_moment_kNm_mm(self,M_kNm, L_mm, E, I, case)
        L = L_mm / 1e3  # span in meters

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
            results[crit] = {
                'allowable_m': allowable,
                'actual_m': delta,
                'passes': ok
            }
            if ok:
                passed.append((n, crit))

        # pick most stringent (smallest denom) that still passes
        best = min(passed)[1] if passed else None

        return delta, results

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def section_classification1(self, design_dictionary,trial_section=""):
        """Classify the sections based on Table 2 of IS 800:2007"""
        print(f"Inside section_classification")
        local_flag = True
        self.input_modified = []
        self.input_section_list = []
        self.input_section_classification = {}
        lambda_check = False
        for trial_section in self.sec_list:
            trial_section = trial_section.strip("'")
            self.section_property = self.section_connect_database(self, trial_section)
            print(f"Type of section{self.section_property.designation}")
            if self.section_property.type == "Rolled":
                web_class = IS800_2007.Table2_iii(
                    self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius),
                    self.section_property.web_thickness,
                    self.material_property.fy,
                )
                flange_class_bottom = IS800_2007.Table2_i(
                    self.section_property.flange_width / 2,
                    self.section_property.flange_thickness,
                    self.material_property.fy,self.section_property.type
                )[0]
                web_ratio = (self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2  /self.section_property.flange_thickness
            else:
                flange_class_bottom = IS800_2007.Table2_i(
                    (
                        (self.section_property.flange_width / 2)
                        # - (self.section_property.web_thickness / 2)
                    ),
                    self.section_property.flange_thickness,
                    self.section_property.fy,
                    self.section_property.type,
                )[0]

                web_class = IS800_2007.Table2_iii(
                    (
                        self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius)
                    ),
                    self.section_property.web_thickness,
                    self.material_property.fy, # classification_type="Axial compression",
                )
                web_ratio = (self.section_property.depth - 2 * (
                            self.section_property.flange_thickness + self.section_property.root_radius)) / self.section_property.web_thickness
                flange_ratio = self.section_property.flange_width / 2 / self.section_property.flange_thickness
            print(f"\n \n \n flange_class_bottom {flange_class_bottom} \n web_class{web_class} \n \n")
            if flange_class_bottom == "Slender" or web_class == "Slender":
                self.section_class = "Slender"
            else:
                if flange_class_bottom == KEY_Plastic and web_class == KEY_Plastic:
                    self.section_class = KEY_Plastic
                elif flange_class_bottom == KEY_Plastic and web_class == KEY_Compact:
                    self.section_class = KEY_Compact
                elif flange_class_bottom == KEY_Plastic and web_class == KEY_SemiCompact:
                    self.section_class = KEY_SemiCompact
                elif flange_class_bottom == KEY_Compact and web_class == KEY_Plastic:
                    self.section_class = KEY_Compact
                elif flange_class_bottom == KEY_Compact and web_class == KEY_Compact:
                    self.section_class = KEY_Compact
                elif flange_class_bottom == KEY_Compact and web_class == KEY_SemiCompact:
                    self.section_class = KEY_SemiCompact
                elif flange_class_bottom == KEY_SemiCompact and web_class == KEY_Plastic:
                    self.section_class = KEY_SemiCompact
                elif flange_class_bottom == KEY_SemiCompact and web_class == KEY_Compact:
                    self.section_class = KEY_SemiCompact
                elif flange_class_bottom == KEY_SemiCompact and web_class == KEY_SemiCompact:
                    self.section_class = KEY_SemiCompact

            self.Zp_req = self.load.moment * self.gamma_m0 / self.material_property.fy
            self.effective_length_beam(self, design_dictionary, self.length)  # mm

            print( 'self.allow_class', self.allow_class)
            if self.section_property.plast_sec_mod_z >= self.Zp_req:
                print( 'self.section_property.plast_sec_mod_z More than Requires')

                if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
                    self.It = self.section_property.It
                    # (
                    #                   2
                    #                   * self.section_property.flange_width
                    #                   * self.section_property.flange_thickness ** 3
                    #           ) / 3 + (
                    #                   (self.section_property.depth - self.section_property.flange_thickness)
                    #                   * self.section_property.web_thickness ** 3
                    #           ) / 3
                    self.hf = self.section_property.depth - self.section_property.flange_thickness
                    self.Iw = self.section_property.Iw
                    # 0.5 ** 2 * self.section_property.mom_inertia_y * self.hf ** 2


                    if self.section_class == KEY_Plastic or self.section_class == KEY_Compact:
                        self.beta_b_lt = 1.0
                    else:
                        self.beta_b_lt = (
                                self.section_property.elast_sec_mod_z
                                / self.section_property.plast_sec_mod_z
                        )
                    _ = IS800_2007.cl_8_2_2_Unsupported_beam_bending_non_slenderness(
                        self.material_property.modulus_of_elasticity,
                        0.3,
                        self.section_property.mom_inertia_y,
                        self.It,
                        self.Iw,
                        self.effective_length * 1e3, self.beta_b_lt, self.section_property.plast_sec_mod_z, self.hf, self.section_property.rad_of_gy_y, self.section_property.flange_thickness
                    )
                    self.M_cr = _[0]
                    self.fcrb = _[1]
                    lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(
                        self.beta_b_lt,
                        self.section_property.plast_sec_mod_z,
                        self.section_property.elast_sec_mod_z,
                        self.material_property.fy,
                        self.M_cr
                    )
                    if lambda_lt < 0.4:
                        lambda_check = True
                        continue
                if self.allow_class != 'No':
                    if (
                        self.section_class == KEY_SemiCompact
                        or self.section_class == KEY_Compact
                        or self.section_class == KEY_Plastic
                    ):

                        self.input_section_list.append(trial_section)
                        if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
                            self.input_section_classification.update({trial_section: [self.section_class, flange_class_bottom, web_class, flange_ratio, web_ratio,self.It,self.hf,self.Iw,self.M_cr,self.beta_b_lt,lambda_lt,self.fcrb]})
                        else:
                            self.input_section_classification.update({trial_section: [self.section_class, flange_class_bottom, web_class, flange_ratio, web_ratio]})

                    elif self.section_class == "Slender":
                        logger.warning(f"The section.{trial_section} is Slender. Ignoring")
                else:
                    if self.section_class == KEY_Compact or self.section_class == KEY_Plastic:
                        self.input_section_list.append(trial_section)
                        if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
                            self.input_section_classification.update({trial_section: [self.section_class, flange_class_bottom, web_class, flange_ratio, web_ratio,self.It,self.hf,self.Iw,self.M_cr,self.beta_b_lt,lambda_lt, self.fcrb]})
                        else:
                            self.input_section_classification.update({trial_section: [self.section_class, flange_class_bottom, web_class, flange_ratio, web_ratio]})
                    elif self.section_class == "Slender":
                        logger.warning(f"The section.{trial_section} is Slender. Ignoring")
                        # self.design_status = False
                        # self.design_status_list.append(self.design_status)
                    elif self.section_class == KEY_SemiCompact:
                        logger.warning(
                            f"The section.{trial_section} is Semi-Compact. Ignoring"
                        )
                        # self.design_status = False
                        # self.design_status_list.append(self.design_status)
        if lambda_check:
            logger.info("After checking Non-dimensional slenderness ratio for given sections, some sections maybe be ignored by Osdag.[Ref IS 8.2.2] ")
        if len(self.input_section_list) == 0:
            local_flag = False
        else:
            local_flag = True
        return local_flag
    
    def design(self, design_dictionary, flag=0):
        '''
        TODO optimimation_tab_check changes to include self.material_property = Material(material_grade=self.material, thickness=0)
            for each section
        '''

        self.optimization_tab_check(self)

        self.design_beam(self, design_dictionary)

    def optimization_tab_check(self):
        '''
        TODO add button to give user option to take Tension holes or not
        '''
        print(f"\n Inside optimization_tab_check")
        self.latex_tension_zone = False
        if (self.effective_area_factor <= 0.10) or (self.effective_area_factor > 1.0):
            logger.error(
                "The defined value of Effective Area Factor in the design preferences tab is out of the suggested range."
            )
            logger.info("Provide an appropriate input and re-design.")
            logger.warning("Assuming a default value of 1.0.")
            self.effective_area_factor = 1.0
            # self.design_status = False
            # self.design_status_list.append(self.design_status)
            self.optimization_tab_check(self)
        elif (self.steel_cost_per_kg < 0.10) or (self.effective_area_factor > 1.0) or (self.effective_area_factor < 0):
            # No suggested range in Description
            logger.warning(
                "The defined value of the effective area factor in the design preferences tab is out of the suggested range."
            )
            # logger.info("Provide an appropriate input and re-design.")
            logger.info("Assuming a default value of 1.0")
            self.steel_cost_per_kg = 50
            self.effective_area_factor = 1
            self.design_status = False
            # self.design_status_list.append(self.design_status)
        else:
            if self.latex_tension_zone:
                if self.effective_area_factor >= (self.material_property.fy * self.gamma_m0 / (self.material_property.fu * 0.9 * self.gamma_m1)):
                    pass
                else:
                    self.latex_tension_zone = True
                    print(f'self.latex_tension_zone: {self.latex_tension_zone}')
                # self.effective_area_factor = (
                #     self.material_property.fy
                #     * self.gamma_m0
                #     / (self.material_property.fu * 0.9 * self.gamma_m1)
                # )
                # logger.info(
                #     f"The effect of holes in the tension flange is considered on the design bending strength. The ratio of net to gross area of the flange in tension is considered {self.effective_area_factor}"
                # )

        logger.info("Provided appropriate design preference, now checking input.")

    def input_modifier(self):
        """Classify the sections based on Table 2 of IS 800:2007"""
        print(f"Inside input_modifier")
        local_flag = True
        self.input_modified = []
        self.input_section_list = []
        # self.input_section_classification = {}

        for section in self.sec_list:
            section = section.strip("'")
            self.section_property = self.section_connect_database(self, section)

            self.Zp_req = self.load.moment * self.gamma_m0 / self.material_property.fy
            print('Inside input_modifier not allow_class',self.allow_class,self.load.moment, self.gamma_m0, self.material_property.fy)
            if self.section_property.plast_sec_mod_z >= self.Zp_req:

                self.input_modified.append(section)
                # logger.info(
                #     f"Required self.Zp_req = {round(self.Zp_req * 10**-3,2)} x 10^3 mm^3 and Zp of section {self.section_property.designation} = {round(self.section_property.plast_sec_mod_z* 10**-3,2)} x 10^3 mm^3.Section satisfy Min self.Zp_req value")
            # else:
                # local_flag = False

                # logger.warning(
                #     f"Required self.Zp_req = {round(self.Zp_req* 10**-3,2)} x 10^3 mm^3 and Zp of section {self.section_property.designation} = {round(self.section_property.plast_sec_mod_z* 10**-3,2)} x 10^3 mm^3.Section dosen't satisfy Min self.Zp_req value")
        # logger.info("")
        print("self.input_modified", self.input_modified)

    def section_connect_database(self, section):
        print(f"section_connect_database{section}")
        print(section)
        # print(self.sec_profile)
        if (
            self.sec_profile == VALUES_SECTYPE[1]
            or self.sec_profile == "I-section"
        ):  # I-section
            self.section_property = ISection(
                designation=section, material_grade=self.material
            )
            self.material_property.connect_to_database_to_get_fy_fu(
                self.material, max(self.section_property.flange_thickness, self.section_property.web_thickness)
            )
            print(f"section_connect_database material_property.fy{self.material_property.fy}")
            self.epsilon = math.sqrt(250 / self.material_property.fy)
        return self.section_property

    def design_beam(self, design_dictionary):
        # 1- Based on optimum UR
        self.optimum_section_ur_results = {}
        self.optimum_section_ur = []

        # 2 - Based on optimum cost
        self.optimum_section_cost_results = {}
        self.optimum_section_cost = []

        # 1 - section classification
        self.flag = self.section_classification(self,design_dictionary)

        print('self.flag:',self.flag)
        if self.effective_area_factor < 1.0:
            logger.warning(
                "Reducing the effective sectional area as per the definition in the Design Preferences tab."
            )
        else:
            logger.info(
                "The effective sectional area is taken as 100% of the cross-sectional area [Reference: Cl. 7.3.2, IS 800:2007]."
            )
        # Effective length
        print(
            f"self.effective_length {self.effective_length} \n self.input_section_classification{self.input_section_classification} ")
        print('self.input_section_list:',self.input_section_list)
        if self.flag:
            for section in self.input_section_list:
                # initialize lists for updating the results dictionary
                self.section_property = self.section_connect_database(self, section)
                if self.section_property.type == 'Rolled':
                    self.effective_depth = (self.section_property.depth - 2 * (
                            self.section_property.flange_thickness + self.section_property.root_radius))
                else:
                    self.effective_depth = (self.section_property.depth - 2 *self.section_property.flange_thickness )
                print('self.section_property.type:',self.section_property.type, self.bending_type)

                if self.sec_profile == 'Beams' or self.sec_profile == 'Columns' or self.sec_profile == VALUES_SECTYPE[1]:
                    if self.section_property.type == "Rolled" and self.bending_type == KEY_DISP_BENDING1:
                        self.shear_area = self.section_property.depth * self.section_property.web_thickness
                    elif self.section_property.type != "Rolled" and self.bending_type == KEY_DISP_BENDING1:
                        self.shear_area = self.effective_depth * self.section_property.web_thickness
                    elif self.bending_type == KEY_DISP_BENDING2:
                        self.shear_area = 2 * self.section_property.flange_width * self.section_property.flange_thickness

                self.effective_length_beam(self, design_dictionary, self.length)  # mm

                # Step 1.1 - computing the effective sectional area
                self.effective_area = self.section_property.area
                self.common_checks_1(self, section, step=2)


                list_result = []
                list_1 = []
                list_result.append(section)
                self.section_class = self.input_section_classification[section][0]
                print(f"Inside design_beam self.design_type:{self.design_type}")

                if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
                     self.It = self.input_section_classification[section][ 5 ]
                     self.hf = self.input_section_classification[section][ 6 ]
                     self.Iw = self.input_section_classification[section][ 7 ]
                     self.M_cr = self.input_section_classification[section][ 8 ]
                     self.beta_b_lt = self.input_section_classification[section][ 9 ]
                     self.lambda_lt = self.input_section_classification[section][ 10 ]
                     self.fcrb = self.input_section_classification[section][ 11 ]
                     print('self.design_type:',self.design_type, self.It,
                            self.hf,
                            self.Iw,
                            self.M_cr,
                            self.beta_b_lt,
                            self.lambda_lt)

                self.beam_web_buckling(self)
                if self.web_buckling_check:
                    self.web_not_buckling_steps(self)

                    # self.shear_strength = IS800_2007.cl_8_4_design_shear_strength(
                    #     self.shear_area,
                    #     self.material_property.fy
                    # ) / 10 ** 3
                    # self.high_shear_check = IS800_2007.cl_8_2_1_2_high_shear_check(
                    #     self.load.shear_force / 1000, self.shear_strength
                    # )
                    # self.bending_strength_section = self.bending_strength() / 10 ** 6

                    # self.web_buckling_steps(self)
                    # self.high_shear_check = False
                    # self.bending_strength_section = self.bending_strength_girder(self) / 10 ** 6

                # print(f"Common result {list_result, self.section_class, self.V_d, self.high_shear_check, self.bending_strength_section}")
                print('self.bending_strength_section',self.bending_strength_section,'self.shear_strength',self.shear_strength, 'self.load.moment',self.load.moment,'self.load.shear_force',self.load.shear_force)
                # 2.8 - UR
                self.ur = max((self.load.moment / self.bending_strength_section * 10 ** -6),(self.load.shear_force / self.shear_strength * 10 ** -3))# ( +  round(self.load.axial_force / self.section_capacity, 3)
                print("UR", self.ur)
                # 2.9 - Cost of the section in INR
                self.cost = (
                        (
                                self.section_property.unit_mass
                                * self.section_property.area
                                * 1e-4
                        )
                        * self.length
                        * self.steel_cost_per_kg
                )
                self.optimum_section_cost.append(self.cost)
                self.web_buckling = False  # When Bearing length is provided

                if self.bearing_length != 'NA': #and self.web_crippling
                    print(f"Check for Web Buckling")
                    try:
                        self.bearing_length = float(design_dictionary[KEY_BEARING_LENGTH])
                        self.web_buckling = True  # WEB BUCKLING
                        self.I_eff_web = self.bearing_length * self.section_property.web_thickness ** 3 / 12
                        self.A_eff_web = self.bearing_length * self.section_property.web_thickness
                        self.r = math.sqrt(self.I_eff_web / self.A_eff_web)
                        self.slenderness = 0.7 * self.effective_depth / self.r
                        self.common_checks_1(self, section, step=3)
                        # step == 4
                        self.common_checks_1(
                            self, section, step=4, list_result=["Concentric"]
                        )
                        # 2.7 - Capacity of the section for web_buckling
                        self.section_capacity = (
                                self.design_compressive_stress * (
                                    self.bearing_length + self.section_property.depth / 2) * self.section_property.web_thickness
                                * 10 ** -3)  # N
                        print(self.design_compressive_stress, self.bearing_length, self.section_property.depth,
                            self.section_property.web_thickness)

                        print(self.bending_strength_section, self.shear_strength, self.section_capacity)

                        self.F_wb = (self.bearing_length + 2.5 * (
                                    self.section_property.root_radius + self.section_property.flange_thickness)) * self.section_property.web_thickness * self.material_property.fy / (
                                                self.gamma_m0 * 10 ** 3)
                        if self.bending_strength_section > self.load.moment * 10 ** -6 and self.shear_strength > self.load.shear_force * 10 ** -3 and self.section_capacity > self.load.shear_force * 10 ** -3 and self.F_wb > self.load.shear_force * 10 ** -3:
                            list_result, list_1 = self.list_changer(self, change='Web Buckling', check=True,
                                                                    list=list_result, list_name=list_1)
                            self.optimum_section_ur.append(self.ur)
                        else:
                            list_result, list_1 = self.list_changer(self, change='Web Buckling', check=True,
                                                                    list=list_result, list_name=list_1)
                            self.optimum_section_ur.append(self.ur)
                        # Step 3 - Storing the optimum results to a list in a descending order
                        self.common_checks_1(self, section, 5, list_result, list_1)
                    except:
                        logger.warning('Bearing length is invalid.')
                        logger.info('Ignoring web Buckling and Crippling check')
                        self.bearing_length = 'NA'
                        self.web_buckling = False
                        # 2.8 - UR
                        print(self.bending_strength_section, self.shear_strength)
                        if self.bending_strength_section > self.load.moment * 10 ** -6 and self.shear_strength > self.load.shear_force * 10 ** -3:
                            list_result, list_1 = self.list_changer(self, change='', check=True,list=list_result, list_name=list_1)
                            self.optimum_section_ur.append(self.ur)


                            # Step 3 - Storing the optimum results to a list in a descending order
                            self.common_checks_1(self, section, 5, list_result, list_1)
                        else:
                            list_result, list_1 = self.list_changer(self, change='', check=True,list=list_result, list_name=list_1)
                            self.optimum_section_ur.append(self.ur)
                            # Step 3 - Storing the optimum results to a list in a descending order
                            self.common_checks_1(self, section, 5, list_result, list_1)

                else:
                    self.web_buckling = False
                    # 2.8 - UR
                    print(self.bending_strength_section, self.shear_strength)
                    if self.bending_strength_section > self.load.moment * 10**-6 and self.shear_strength > self.load.shear_force * 10**-3:

                        self.optimum_section_ur.append(self.ur)
                        list_result, list_1 = self.list_changer(self, change=' ', check=True, list=list_result, list_name=list_1)

                        # Step 3 - Storing the optimum results to a list in a descending order
                        self.common_checks_1(self, section, 5, list_result, list_1)
                    else:
                        self.optimum_section_ur.append(self.ur)
                        list_result, list_1 = self.list_changer(self, change=' ', check=True, list=list_result, list_name=list_1)

                        # Step 3 - Storing the optimum results to a list in a descending order
                        self.common_checks_1(self, section, 5, list_result, list_1)
                print('self.optimum_section_ur', self.optimum_section_ur)

    def beam_web_buckling(self):

        print(f"Working web_buckling_check")
        # 3 - web buckling under shear
        self.web_buckling_check = IS800_2007.cl_8_2_1_web_buckling(
            d=self.effective_depth,
            tw=self.section_property.web_thickness,
            e=self.epsilon,
        )
        print(self.web_buckling_check, self.section_property.designation)

        if not self.web_buckling_check:
            self.web_not_buckling_steps(self)
    def web_buckling_steps(self):
        print(f"Not using web_buckling_steps")
        # logger.info(f"Considering  {self.support_cndition_shear_buckling}")
        # 5 - Web Buckling check(when high shear) -If user wants then only
        # if web_buckling:
        #     b1 = input('Enter bearing')
        #     self.web_buckling_strength = self.section_property.web_thickness * (b1 + 1.25 * self.section_property.depth)
        # self.V_d = pass
        # web_buckling_message = 'Thin web'
        if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0]:
            self.K_v = IS800_2007.cl_8_4_2_2_K_v_Simple_postcritical('only support')
            self.plate_girder_strength(self)
            # logger.info('Section = {}, V_cr = {}'.format(self.section_property.designation, round(self.V_cr,2)))
            self.shear_strength = self.V_cr / self.gamma_m0
            # if self.V_d > self.load.shear_force * 10**-3:
            #
            #     return True
            # else:
            #     return False
            # self.V_d = IS800_2007.cl_8_4_2_2_ShearBuckling_Simple_postcritical((self.section_property.depth - 2 *(self.section_property.flange_thickness + self.section_property.root_radius),
            #                                                                     self.section_property.web_thickness,space,0.3, self.fyw))
        elif self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1]:
            self.V_p = IS800_2007.cl_8_4_design_shear_strength(
                self.shear_area,
                self.material_property.fy
            ) / 10 ** 3 * self.gamma_m0
            self.Mfr = IS800_2007.cl_8_4_2_2_Mfr_TensionField(self.section_property.flange_width,
                                                     self.section_property.flange_thickness, self.fyf,
                                                     self.load.moment / (
                                                             self.section_property.depth - self.section_property.flange_thickness),
                                                     self.gamma_m0)
            print('MFr', self.Mfr)
            if self.Mfr > 0:
                print('Starting loop', int(round(self.effective_length*10**4/self.effective_depth,-1)/10))
                # for c_d in range(3,self.effective_length/self.result_eff_d):
                for c_d in reversed(list(range(3,int(round(self.effective_length * 1000/self.effective_depth,-1))))):
                    print('c_d',c_d,'c/d',self.effective_length * 1000/self.effective_depth)
                    c_d = c_d/10 + 0.1
                    self.c = round(c_d * self.effective_depth, -1)
                    print('c',self.c)
                    self.K_v = IS800_2007.cl_8_4_2_2_K_v_Simple_postcritical('many support', self.c, self.effective_depth)
                    self.plate_girder_strength2(self)

                    self.shear_strength = self.V_tf_girder / self.gamma_m0 * 10**-3
                    logger.info('Intermediate Stiffeners required d ={}, c = {}, Section = {}, V_tf = {}, V_d = {}'.format(self.effective_depth,self.c,
                                                                                                          self.section_property.designation,
                                                                                                          self.V_tf_girder,self.shear_strength))
                    if self.shear_strength > self.load.shear_force * 10**-3:
                        return
                return
            else:
                self.shear_strength = 0.1
    def web_not_buckling_steps(self):
        print(f"Working web_not_buckling_steps")
        self.V_d = IS800_2007.cl_8_4_design_shear_strength(
            self.shear_area,
            self.material_property.fy
        ) / 10 ** 3
        self.shear_strength = self.V_d
        self.high_shear_check = IS800_2007.cl_8_2_1_2_high_shear_check(
            self.load.shear_force / 1000, self.V_d
        )
        print(f"self.V_d {self.V_d},{self.section_property.depth* self.section_property.web_thickness}, {self.material_property.fy}")
        # 4 -  design bending strength
        self.bending_strength_section = self.bending_strength(self) / 10 ** 6



    def bending_strength(self):
        print('Inside bending_strength ','\n self.section_class', self.section_class)
        # 4 - design bending strength
        M_d = IS800_2007.cl_8_2_1_2_design_bending_strength(
            self.section_class,
            self.section_property.plast_sec_mod_z,
            self.section_property.elast_sec_mod_z,
            self.material_property.fy,
            self.gamma_m0,
            self.support,
        )
        if self.section_class == KEY_Plastic or self.section_class == KEY_Compact :
            self.beta_b_lt = 1
        else :
            self.beta_b_lt = self.section_property.elast_sec_mod_z/self.section_property.plast_sec_mod_z
            print('self.beta_b_lt: ',self.beta_b_lt)
        self.M_d = M_d
        if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
            if self.high_shear_check:
                if self.section_class == KEY_Plastic or self.section_class == KEY_Compact:
                    bending_strength_section = self.bending_strength_reduction(self, M_d)
                else:
                    bending_strength_section = (
                        self.section_property.elast_sec_mod_z
                        * self.material_property.fy
                        / self.gamma_m0
                    )
            else:
                bending_strength_section = M_d
            print('Inside bending_strength 1', M_d, self.high_shear_check, bending_strength_section)
        else:
            print('self.design_type:',self.design_type, self.It,
                            self.hf,
                            self.Iw,
                            self.M_cr,
                            self.beta_b_lt,
                            self.lambda_lt, self.fcrb)
            # self.It = (
            #     2
            #     * self.section_property.flange_width
            #     * self.section_property.flange_thickness**3
            # ) / 3 + (
            #     (self.section_property.depth - self.section_property.flange_thickness)
            #     * self.section_property.web_thickness**3
            # ) / 3
            # self.hf = self.section_property.depth - self.section_property.flange_thickness
            # self.Iw = 0.5**2 * self.section_property.mom_inertia_y * self.hf**2
            # self.M_cr = IS800_2007.cl_8_2_2_Unsupported_beam_bending_non_slenderness(
            #     self.material_property.modulus_of_elasticity,
            #     0.3,
            #     self.section_property.mom_inertia_y,
            #     self.It,
            #     self.Iw,
            #     self.effective_length * 1e3
            # )
            #
            # if self.section_class == KEY_Plastic or self.section_class == KEY_Compact:
            #     self.beta_b_lt = 1.0
            # else:
            #     self.beta_b_lt = (
            #         self.section_property.elast_sec_mod_z
            #         / self.section_property.plast_sec_mod_z
            #     )
            if self.section_property.type == "Rolled":
                alpha_lt = 0.21
            else:
                alpha_lt = 0.49
            # lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment(
            #     self.beta_b_lt,
            #     self.section_property.plast_sec_mod_z,
            #     self.section_property.elast_sec_mod_z,
            #     self.material_property.fy,
            #     self.M_cr
            # )
            phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(
                alpha_lt, self.lambda_lt
            )
            X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(
                phi_lt, self.lambda_lt
            )
            fbd = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(
                X_lt, self.material_property.fy, self.gamma_m0
            )
            bending_strength_section = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(
                    self.section_property.plast_sec_mod_z,
                    self.section_property.elast_sec_mod_z,
                    fcd=fbd,
                    section_class=self.section_class
                )
            # self.beta_b_lt = beta_b
            self.alpha_lt = alpha_lt
            # self.lambda_lt = lambda_lt
            self.phi_lt = phi_lt
            self.X_lt = X_lt
            self.fbd_lt = fbd
            self.lateral_tb = self.M_cr * 10**-6
            print('Inside bending_strength 2.1', fbd, self.section_property.plast_sec_mod_z )
            if self.high_shear_check:
                if self.section_class == KEY_Plastic or self.section_class == KEY_Compact:
                    bending_strength_section = self.bending_strength_reduction(self,Md=bending_strength_section
                    )
                else:
                    bending_strength_section = (
                        self.beta_b_lt
                        * self.section_property.plast_sec_mod_z
                        * fbd
                    )
            print('Inside bending_strength 2',self.It,self.hf,self.Iw,self.M_cr ,self.beta_b_lt,alpha_lt,self.lambda_lt,phi_lt,X_lt,fbd,bending_strength_section)
        self.bending_strength_section_reduced = bending_strength_section
        return bending_strength_section
    def bending_strength_girder(self):
        print('Inside bending_strength of girder ')
        web_class = IS800_2007.Table2_i(
            (self.section_property.flange_width - self.section_property.web_thickness)/2,
            self.section_property.flange_thickness,
            self.material_property.fy, self.section_property.type
        )[0]
        flange_class_bottom = IS800_2007.Table2_i(
            self.section_property.depth - 2 * self.section_property.flange_thickness,
            self.section_property.web_thickness,
            self.material_property.fy,self.section_property.type
        )[0]
        if flange_class_bottom == "Slender" or web_class == "Slender":
            self.section_class_girder = "Slender"
        else:
            if flange_class_bottom == KEY_Plastic and web_class == KEY_Plastic:
                self.section_class_girder = KEY_Plastic
            elif flange_class_bottom == KEY_Plastic and web_class == KEY_Compact:
                self.section_class_girder = KEY_Compact
            elif flange_class_bottom == KEY_Plastic and web_class == KEY_SemiCompact:
                self.section_class_girder = KEY_SemiCompact
            elif flange_class_bottom == KEY_Compact and web_class == KEY_Plastic:
                self.section_class_girder = KEY_Compact
            elif flange_class_bottom == KEY_Compact and web_class == KEY_Compact:
                self.section_class_girder = KEY_Compact
            elif flange_class_bottom == KEY_Compact and web_class == KEY_SemiCompact:
                self.section_class_girder = KEY_SemiCompact
            elif flange_class_bottom == KEY_SemiCompact and web_class == KEY_Plastic:
                self.section_class_girder = KEY_SemiCompact
            elif flange_class_bottom == KEY_SemiCompact and web_class == KEY_Compact:
                self.section_class_girder = KEY_SemiCompact
            elif flange_class_bottom == KEY_SemiCompact and web_class == KEY_SemiCompact:
                self.section_class_girder = KEY_SemiCompact
        # 4 - design bending strength
        I_flange = 2 * (self.section_property.flange_width * self.section_property.flange_thickness**3/12 + self.section_property.flange_width * self.section_property.flange_thickness * (self.section_property.depth/2 - self.section_property.flange_thickness/2)**2)
        Zez_flange = I_flange / self.section_property.depth /2
        y_top = (self.section_property.flange_width * self.section_property.flange_thickness * (self.section_property.depth - self.section_property.flange_thickness)/2) / (self.section_property.flange_width * self.section_property.flange_thickness)
        Zpz_flange = 2 * self.section_property.flange_width * self.section_property.flange_thickness * y_top
        M_d = IS800_2007.cl_8_2_1_2_design_bending_strength(
            self.section_class_girder,
            Zpz_flange,
            Zez_flange,
            self.material_property.fy,
            self.gamma_m0,
            self.support,
        )
        if self.section_class_girder == KEY_Plastic or self.section_class_girder == KEY_Compact :
            self.beta_b_lt = 1
        else :
            self.beta_b_lt = Zez_flange/Zpz_flange
        self.M_d = M_d
        if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
            if self.high_shear_check:
                if self.section_class_girder == KEY_Plastic or self.section_class_girder == KEY_Compact:
                    bending_strength_section = self.bending_strength_reduction(self, M_d)
                else:
                    bending_strength_section = (
                        self.section_property.elast_sec_mod_z
                        * self.material_property.fy
                        / self.gamma_m0
                    )
            else:
                bending_strength_section = M_d
            print('Inside bending_strength 1', M_d, self.high_shear_check, bending_strength_section)
        else:
            # self.It = (
            #     2
            #     * self.section_property.flange_width
            #     * self.section_property.flange_thickness**3
            # ) / 3 + (
            #     (self.section_property.depth - self.section_property.flange_thickness)
            #     * self.section_property.web_thickness**3
            # ) / 3
            self.hf = self.section_property.depth - self.section_property.flange_thickness
            # self.Iw = 0.5**2 * self.section_property.mom_inertia_y * self.hf**2
            self.fcrb = IS800_2007.cl_8_2_2_Unsupported_beam_bending_fcrb(
                self.material_property.modulus_of_elasticity,
                self.effective_length/self.section_property.rad_of_gy_y,
                self.hf/self.section_property.flange_thickness
            )

            if self.section_class_girder == KEY_Plastic or self.section_class_girder == KEY_Compact:
                self.beta_b_lt = 1.0
            else:
                self.beta_b_lt = (
                    self.section_property.elast_sec_mod_z
                    / self.section_property.plast_sec_mod_z
                )
            if self.section_property.type == "Rolled":
                alpha_lt = 0.21
            else:
                alpha_lt = 0.49
            lambda_lt = IS800_2007.cl_8_2_2_1_elastic_buckling_moment_fcrb(
                self.material_property.fy, self.fcrb
            )
            phi_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_phi_lt(
                alpha_lt, lambda_lt
            )
            X_lt = IS800_2007.cl_8_2_2_Unsupported_beam_bending_stress_reduction_factor(
                phi_lt, lambda_lt
            )
            fbd = IS800_2007.cl_8_2_2_Unsupported_beam_bending_compressive_stress(
                X_lt, self.material_property.fy, self.gamma_m0
            )
            bending_strength_section = IS800_2007.cl_8_2_2_Unsupported_beam_bending_strength(
                    self.section_property.plast_sec_mod_z,
                    self.section_property.elast_sec_mod_z,
                    fcd=fbd,
                    section_class=self.section_class_girder
                )


            # self.beta_b_lt = beta_b
            self.alpha_lt = alpha_lt
            # self.lambda_lt = lambda_lt
            self.phi_lt = phi_lt
            self.X_lt = X_lt
            self.fbd_lt = fbd
            self.lateral_tb = self.fcrb * 10**-6
            print('Inside bending_strength 2.1', fbd, self.section_property.plast_sec_mod_z )
            if self.high_shear_check:
                if self.section_class_girder == KEY_Plastic or self.section_class_girder == KEY_Compact:
                    bending_strength_section = self.bending_strength_reduction(self,Md=bending_strength_section
                    )
                else:
                    bending_strength_section = (
                        self.beta_b_lt
                        * self.section_property.plast_sec_mod_z
                        * fbd
                    )
            print('Inside bending_strength 2',self.It,self.hf,self.Iw,self.fcrb ,self.beta_b_lt,alpha_lt,lambda_lt,phi_lt,X_lt,fbd,bending_strength_section)
        self.bending_strength_section_reduced = bending_strength_section
        return bending_strength_section
    def bending_strength_reduction(self, Md):
        Zfd = (
            self.section_property.plast_sec_mod_z
            - (self.section_property.depth**2 * self.section_property.web_thickness / 4)
        )
        Mfd = Zfd * self.material_property.fy / self.gamma_m0
        beta = ((2 * self.load.shear_force / (self.shear_strength * 10**3)) - 1) ** 2
        Mdv = (Md - beta * (Md - Mfd))
        print('Inside bending_strength_reduction',Mdv, Md, beta, Mfd, Zfd)
        self.bending_strength_section_reducedby = Mfd
        self.beta_reduced = beta
        if (
            Mdv
            <= 1.2
            * self.section_property.plast_sec_mod_z
            * self.material_property.fy
            / self.gamma_m0
        ):
            return Mdv
        else:
            return (
                1.2
                * self.section_property.plast_sec_mod_z
                * self.material_property.fy
                / self.gamma_m0
            )


    


    def effective_length_beam1(self, design_dictionary, length):
        print(f"Inside effective_length_beam")
        self.Loading = design_dictionary[KEY_LOAD]  # 'Normal'or 'Destabilizing'
        # self.Latex_length = design_dictionary[KEY_LENGTH_OVERWRITE]
        if design_dictionary[KEY_LENGTH_OVERWRITE] == 'NA':
            if self.support == KEY_DISP_SUPPORT1:
                self.torsional_res = design_dictionary[KEY_TORSIONAL_RES]
                self.warping = design_dictionary[KEY_WARPING_RES]
                self.effective_length = IS800_2007.cl_8_3_1_EffLen_Simply_Supported(
                    Torsional=self.Torsional_res,
                    Warping=self.Warping,
                    length=length,
                    depth=(self.section_property.depth/1000),
                    load=self.Loading,
                )
                print(f"Working 1 {self.effective_length}")
            elif self.support == KEY_DISP_SUPPORT2:
                self.Support = design_dictionary[KEY_SUPPORT_TYPE]
                self.Top = design_dictionary[KEY_SUPPORT_TYPE2]
                self.effective_length = IS800_2007.cl_8_3_3_EffLen_Cantilever(
                    Support=self.Support,
                    Top=self.Top,
                    length=length,
                    load=self.Loading,
                )
                print(f"Working 2 {self.effective_length}")
        else:
            if self.support == KEY_DISP_SUPPORT1:
                self.Torsional_res = design_dictionary[KEY_TORSIONAL_RES]
                self.Warping = design_dictionary[KEY_WARPING_RES]

            elif self.support == KEY_DISP_SUPPORT2:
                self.Support = design_dictionary[KEY_SUPPORT_TYPE]
                self.Top = design_dictionary[KEY_SUPPORT_TYPE2]

            try:
                if float(design_dictionary[KEY_LENGTH_OVERWRITE]) <= 0:
                    design_dictionary[KEY_LENGTH_OVERWRITE] = 'NA'
                else:
                    length = length * float(design_dictionary[KEY_LENGTH_OVERWRITE])

                self.effective_length = length
                print(f"Working 3 {self.effective_length}")
            except:
                print(f"Inside effective_length_beam",type(design_dictionary[KEY_LENGTH_OVERWRITE]))
                logger.warning("Invalid Effective Length Parameter.")
                logger.info('Effective Length Parameter is set to default: 1.0')
                design_dictionary[KEY_LENGTH_OVERWRITE] = '1.0'
                self.effective_length_beam(self, design_dictionary, length)
                print(f"Working 4 {self.effective_length}")
        print(f"Inside effective_length_beam",self.effective_length, design_dictionary[KEY_LENGTH_OVERWRITE])


    def lambda_lt_check_member_type(self, Mcr=0, fcrb=0, Zp=0, f_y=0, Ze=0, beta_b=0):
        lambda_lt_1 = math.sqrt(beta_b * Zp * f_y / Mcr)
        lambda_lt_2 = math.sqrt(f_y / fcrb)
        lambda_lt_check = math.sqrt(1.2 * Ze * f_y / Mcr)
        if lambda_lt_1 == lambda_lt_2:
            if lambda_lt_1 <= lambda_lt_check:
                return lambda_lt_1
        logger.warning(" Issues with the non-dimensional slenderness ratio Lambda_lt")

    def common_checks_1(self, section, step=1, list_result=[], list_1=[]):
        if step == 1:
            print(f"Working correct here")
        elif step == 2:
            # reduction of the area based on the connection requirements (input from design preferences)
            if self.effective_area_factor < 1.0:
                self.effective_area = round(
                    self.effective_area * self.effective_area_factor, 2
                )


        elif step == 3:
            # 2.1 - Buckling curve classification and Imperfection factor
            if self.section_property.type == 'Rolled':
                self.buckling_class = 'c'
            self.imperfection_factor = IS800_2007.cl_7_1_2_1_imperfection_factor(
                                                                                    buckling_class=self.buckling_class
                                                                                )
        elif step == 4:
            # self.slenderness = self.effective_length / min(self.section_property.rad_of_gy_z, self.section_property.rad_of_gy_y) * 1000
            print(
                f"\n data sent "
                f" self.material_property.fy {self.material_property.fy}"
                f"self.gamma_m0 {self.gamma_m0}"
                f"self.slenderness {self.slenderness}"
                f" self.imperfection_factor {self.imperfection_factor}"
                f"self.section_property.modulus_of_elasticity {self.section_property.modulus_of_elasticity}"
            )

            list_cl_7_1_2_1_design_compressisive_stress = (
                IS800_2007.cl_7_1_2_1_design_compressisive_stress(
                    self.material_property.fy,
                    self.gamma_m0,
                    self.slenderness,
                    self.imperfection_factor,
                    self.section_property.modulus_of_elasticity,
                    check_type=list_result,
                )
            )
            for x in list_cl_7_1_2_1_design_compressisive_stress:
                print(f"x {x} ")
            self.euler_buckling_stress = list_cl_7_1_2_1_design_compressisive_stress[0]
            self.nondimensional_effective_slenderness_ratio = (
                list_cl_7_1_2_1_design_compressisive_stress[1]
            )
            self.phi = list_cl_7_1_2_1_design_compressisive_stress[2]
            self.stress_reduction_factor = list_cl_7_1_2_1_design_compressisive_stress[
                3
            ]
            self.design_compressive_stress_fr = (
                list_cl_7_1_2_1_design_compressisive_stress[4]
            )
            self.design_compressive_stress = (
                list_cl_7_1_2_1_design_compressisive_stress[5]
            )
            self.design_compressive_stress_max = (
                list_cl_7_1_2_1_design_compressisive_stress[6]
            )
        elif step == 5:
            # 1- Based on optimum UR
            self.optimum_section_ur_results[self.ur] = {}
            list_2 = list_result.copy()
            for j in list_1:
                # k = 0
                for k in list_2:
                    self.optimum_section_ur_results[self.ur][j] = k
                    # k += 1
                    list_2.pop(0)
                    break

            # 2- Based on optimum cost
            self.optimum_section_cost_results[self.cost] = {}

            list_2 = list_result.copy()  # Why?
            for j in list_1:
                for k in list_2:
                    self.optimum_section_cost_results[self.cost][j] = k
                    list_2.pop(0)
                    break
            print(
                f"\n self.optimum_section_cost_results {self.optimum_section_cost_results}"
                f"\n self.optimum_section_ur_results {self.optimum_section_ur_results}"
            )
        elif step == 6:
            self.single_result[self.sec_profile] = {}
            list_2 = list_result.copy()
            for j in list_1:
                # k = 0
                for k in list_2:
                    self.single_result[self.sec_profile][j] = k
                    # k += 1
                    list_2.pop(0)
                    break
            print(f"\n self.single_result {self.single_result}")

    def list_changer(self, change, list,list_name, check = True):
        list_name.extend([
            "Designation"])
        if self.high_shear_check and self.section_class != 'Semi-Compact':
            list.extend(
                [self.bending_strength_section_reducedby, self.beta_reduced, self.M_d])
            list_name.extend([
                "Mfd",
                "Beta_reduced",
                'M_d'
            ])
        #Latex para also
        list.extend(
            [self.latex_tension_zone,self.web_buckling_check,self.effective_depth, self.web_buckling, self.section_class, self.effective_area, self.shear_strength, self.high_shear_check,
             self.bending_strength_section, self.effective_length, self.ur,
             self.cost, self.beta_b_lt])
        list_name.extend([
            'latex.tension_zone',
            'Web.Buckling',
            'Reduced.depth',
            'Buckling.crippling',
            "Section class",
            "Effective area",
            "Shear Strength",
            "High Shear check",
            "Bending Strength",
            "Effective_length",
            "UR",
            "Cost",
            "Beta_b"
        ])
        #Web buckling parameters
        # if self.web_buckling_check and (self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0] or self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1] ) :
        #     list.extend(
        #         [self.K_v, self.tau_crc, self.lambda_w, self.tau_b,
        #          self.V_cr])
        #     list_name.extend([
        #         'Kv',
        #         'tau_crc',
        #         'lambda_w',
        #         'tau_b',
        #         "V_cr"
        #     ])
        if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1] and self.web_buckling_check:
            list.extend(
                [self.Mfr, self.load.moment / (
                                                             self.section_property.depth - self.section_property.flange_thickness)
                    , self.c, self.phi_girder,self.s_girder ,self.wtf_girder,self.sai_girder, self.fv_girder,self.V_p,self.V_tf_girder])
            list_name.extend([
                'Mfr',
                'Nf',
                'c',
                'phi_girder',
                "s_girder",
                'wtf_girder',
                'sai_girder',
                'fv_girder',
                'V_p',
                'V_tf_girder'
            ])
        if change == 'Web Buckling':
            list.extend([self.I_eff_web, self.A_eff_web, self.r, self.buckling_class,
                            self.imperfection_factor,
                            self.slenderness,
                            self.euler_buckling_stress,
                            self.nondimensional_effective_slenderness_ratio,
                            self.phi,
                            self.stress_reduction_factor,
                            self.design_compressive_stress_fr,
                            self.design_compressive_stress_max,
                            self.design_compressive_stress,
                            self.section_capacity,
                            self.F_wb])

            list_name.extend ([
                "WebBuckling.I_eff",
                "WebBuckling.A_eff",
                "WebBuckling.r_eff",
                "Buckling_class",
                "IF",
                "Effective_SR",
                "EBS",
                "ND_ESR",
                "phi",
                "SRF",
                "FCD_formula",
                "FCD_max",
                "FCD",
                "Capacity",
                "Web_crippling"
            ])
        if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
            list.extend([self.It,
                            self.Iw,
                            self.alpha_lt,
                            self.lambda_lt,
                            self.phi_lt,
                            self.X_lt,
                            self.fbd_lt,
                            self.lateral_tb])

            list_name.extend([
                "It",
                "Iw",
                "IF_lt",
                "ND_ESR_lt",
                "phi_lt",
                "SRF_lt",
                "FCD_lt",
                "Mcr"
            ])
        return  list,list_name

    # def plate_girder_design(self, section):
    #     if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0]:
    #         self.tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(self.K_v,
    #                                                                          self.material_property.modulus_of_elasticity,
    #                                                                          0.3,self.effective_depth,
    #                                                                          self.section_property.web_thickness)
    #         self.lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(self.fyw,self.tau_crc)
    #         self.tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(self.lambda_w, self.fyw)
    #         self.V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(self.tau_b, self.effective_depth * self.section_property.web_thickness)
        # d_red = self.section_property.depth - 2*(self.section_property.flange_thickness + self.section_property.root_radius)
        # tau_b = self.load.shear_force / (self.effective_depth * self.section_property.web_thickness)
        # if tau_b <= self.fyw / math.sqrt(3):
        #     lambda_w = 0.8
        # else:
        #     lambda_w = min((tau_b*(math.sqrt(3)/self.fyw) - 1.64) / (-0.8), math.sqrt(tau_b*(math.sqrt(3)/self.fyw)))
        # tau_crc = self.fyw / (math.sqrt(3) * lambda_w ** 2)

    def plate_girder_strength(self):
        self.tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(self.K_v,
                                                                         self.material_property.modulus_of_elasticity,
                                                                         0.3,self.effective_depth,
                                                                         self.section_property.web_thickness)
        self.lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(self.fyw,self.tau_crc)
        self.tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(self.lambda_w, self.fyw)
        self.V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(self.tau_b, self.effective_depth * self.section_property.web_thickness) / 10**3
        print('\n plate_girder_strength', '\n tau_crc',self.tau_crc,'\n self.lambda_w',self.lambda_w,'\n self.tau_b',self.tau_b,'\n self.V_cr',self.V_cr)
    def plate_girder_strength2(self):

            self.plate_girder_strength(self)
            self.phi_girder, self.M_fr_girder ,self.s_girder ,self.wtf_girder,self.sai_girder, self.fv_girder, self.V_tf_girder= IS800_2007.cl_8_4_2_2_TensionField(self.c,
                                                                             self.effective_depth,self.section_property.web_thickness,
                                                                             self.fyw,self.section_property.flange_width,
                                                                             self.section_property.flange_thickness,self.fyf,
                                                                             self.load.moment/(self.section_property.depth - self.section_property.flange_thickness),
                                                                             self.gamma_m0,self.effective_depth * self.section_property.web_thickness,self.tau_b,self.V_p )


    def results(self, design_dictionary):
        _ = [i for i in self.optimum_section_ur if i > 1.0]
        print( '_ ',_)
        if len(_)==1:
            temp = _[0]
        elif len(_)==0:
            temp = None
        else:
            temp = sorted(_)[0]
        self.failed_design_dict = self.optimum_section_ur_results[temp] if temp is not None else None
        print('self.failed_design_dict ',self.failed_design_dict)

        # sorting results from the dataset
        # if len(self.input_section_list) > 1:
        # results based on UR
        if self.optimization_parameter == "Utilization Ratio":
            filter_UR = filter(
                lambda x: x <= min(self.allowable_utilization_ratio, 1.0),
                self.optimum_section_ur
            )
            self.optimum_section_ur = list(filter_UR)

            self.optimum_section_ur.sort()
            print(f"self.optimum_section_ur{self.optimum_section_ur} \n self.optimum_section_ur_results{self.optimum_section_ur_results}")
            # print(f"self.result_UR{self.result_UR}")

            # selecting the section with most optimum UR
            if len(self.optimum_section_ur) == 0:  # no design was successful
                logger.warning(
                    "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
                    "criteria"
                )
                logger.error(
                    "The solver did not find any adequate section from the defined list."
                )

                self.design_status = False
                if len(self.failed_design_dict)>0:
                    logger.info(
                    "The details for the best section provided is being shown"
                )
                    self.result_UR = self.failed_design_dict['UR'] #temp  TODO @Rutvik
                    self.common_result(
                        self,
                        list_result=self.failed_design_dict,
                        result_type=None,
                    )
                    logger.warning(
                    "Re-define the list of sections or check the Design Preferences option and re-design."
                )
                else:
                    logger.warning(
                    "Plastic section modulus of selected sections is less than required."
                )
                    return
                # self.design_status_list.append(self.design_status)

            else:
                self.failed_design_dict = None
                self.result_UR = self.optimum_section_ur[-1]  # optimum section which passes the UR check
                print(f"self.result_UR{self.result_UR}")
                self.design_status = True
                self.common_result(
                    self,
                    list_result=self.optimum_section_ur_results,
                    result_type=self.result_UR,
                )

        else:  # results based on cost
            self.optimum_section_cost.sort()

            # selecting the section with most optimum cost
            self.result_cost = self.optimum_section_cost[0]
            self.design_status = True
        # print results
        # if len(self.optimum_section_ur) == 0:
        #     logger.warning(
        #         "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
        #         "criteria"
        #     )
        #     logger.error(
        #         "The solver did not find any adequate section from the defined list."
        #     )
        #     logger.info(
        #         "Re-define the list of sections or check the Design Preferences option and re-design."
        #     )
        #     self.design_status = False
        #     self.design_status_list.append(self.design_status)
        #     pass
        # else:
        #     if self.optimization_parameter == "Utilization Ratio":
        #         self.common_result(
        #             self,
        #             list_result=self.optimum_section_ur_results,
        #             result_type=self.result_UR,
        #         )
        #     else:
        #         self.result_UR = self.optimum_section_cost_results[
        #             self.result_cost
        #         ]["UR"]
        #
        #         # checking if the selected section based on cost satisfies the UR
        #         if self.result_UR > min(self.allowable_utilization_ratio, 1.0):
        #             trial_cost = []
        #             for cost in self.optimum_section_cost:
        #                 self.result_UR = self.optimum_section_cost_results[
        #                     cost
        #                 ]["UR"]
        #                 if self.result_UR <= min(
        #                     self.allowable_utilization_ratio, 1.0
        #                 ):
        #                     trial_cost.append(cost)
        #
        #             trial_cost.sort()
        #
        #             if len(trial_cost) == 0:  # no design was successful
        #                 logger.warning(
        #                     "The sections selected by the solver from the defined list of sections did not satisfy the Utilization Ratio (UR) "
        #                     "criteria"
        #                 )
        #                 logger.error(
        #                     "The solver did not find any adequate section from the defined list."
        #                 )
        #                 logger.info(
        #                     "Re-define the list of sections or check the Design Preferences option and re-design."
        #                 )
        #                 self.design_status = False
        #                 self.design_status_list.append(self.design_status)
        #                 print(f"design_status_list{self.design_status} \n")
        #             else:
        #                 self.result_cost = trial_cost[
        #                     0
        #                 ]  # optimum section based on cost which passes the UR check
        #                 self.design_status = True
        #
        #         # results
        #         self.common_result(
        #             self,
        #             list_result=self.optimum_section_cost_results,
        #             result_type=self.result_cost,
        #         )
        #
        #         print(f"design_status_list2{self.design_status}")
        self.design_status_list.append(self.design_status)
        for status in self.design_status_list:
            print('status list', status)
            if status is False:
                self.design_status = False
                break
            else:
                self.design_status = True

    def common_result(self, list_result, result_type, flag=1):
        try:
            self.result_designation = list_result[result_type]["Designation"] # TODO debug
            logger.info(
            "The section is {}. The {} section  has  {} flange({}) and  {} web({}).  [Reference: Cl 3.7, IS 800:2007].".format(
                self.input_section_classification[self.result_designation][0] ,
                self.result_designation,
                self.input_section_classification[self.result_designation][1], round(self.input_section_classification[self.result_designation][3],2),
                self.input_section_classification[self.result_designation][2], round(self.input_section_classification[self.result_designation][4],2)
            )
        )
            self.result_latex_tension_zone = list_result[result_type]["latex.tension_zone"]
            self.result_web_buckling_check = list_result[result_type]["Web.Buckling"]
            self.result_eff_d = list_result[result_type]["Reduced.depth"]
            self.result_buckling_crippling = list_result[result_type]["Buckling.crippling"]

            self.result_section_class = list_result[result_type]["Section class"]
            self.result_effective_area = round(list_result[result_type]["Effective area"],2)
            if self.effective_area_factor < 1.0:
                logger.info(
                    "The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".format(
                        round((self.result_effective_area / self.effective_area_factor), 2),
                        self.result_effective_area,
                    )
                )

            self.result_shear = round(list_result[result_type]["Shear Strength"], 2)
            self.result_high_shear = list_result[result_type]["High Shear check"]
            self.result_bending = round(list_result[result_type]["Bending Strength"], 2)
            self.result_eff_len = round(list_result[result_type]["Effective_length"], 2)
            self.result_cost = list_result[result_type]["Cost"]
            self.result_betab = list_result[result_type]["Beta_b"]

            if self.result_web_buckling_check :
                logger.warning(
                    "Thin web so take flange to resist moment and web to resist shear[Reference: Cl 8.2.1.1, IS 800:2007]")
                if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0]:
                    logger.info('Transverse Stiffeners at supports required. Design not done for them')
                    self.result_web_buckling_simple_kv = round(list_result[result_type]['Kv'], 2)
                    self.result_web_buckling_simple_tau_crc = round(list_result[result_type]['tau_crc'], 2)
                    self.result_web_buckling_simple_lambda_w = round(list_result[result_type]['lambda_w'], 2)
                    self.result_web_buckling_simple_tau_b = round(list_result[result_type]['tau_b'], 2)
                    self.result_web_buckling_simple_V_cr = round(list_result[result_type]['V_cr'], 2)
                elif self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1]:
                    logger.info('Transverse Stiffeners at supports  and intermediate transverse stiffener required. Design not done for them')
                    self.result_web_buckling_simple_kv = round(list_result[result_type]['Kv'], 2)
                    self.result_web_buckling_simple_tau_crc = round(list_result[result_type]['tau_crc'], 2)
                    self.result_web_buckling_simple_lambda_w = round(list_result[result_type]['lambda_w'], 2)
                    self.result_web_buckling_simple_tau_b = round(list_result[result_type]['tau_b'], 2)
                    self.result_web_buckling_simple_V_cr = round(list_result[result_type]['V_cr'], 2)
                    self.result_web_buckling_simple_Mfr = round(list_result[result_type]['Mfr']*10**-6, 2)
                    self.result_web_buckling_simple_Nf = round(list_result[result_type]['Nf'], 2)
                    self.result_web_buckling_simple_c = round(list_result[result_type]['c'], 2)
                    self.result_web_buckling_simple_phi_girder = round(list_result[result_type]['phi_girder'], 2)
                    self.result_web_buckling_simple_s_girder = round(list_result[result_type]['s_girder'], 2)
                    self.result_web_buckling_simple_wtf_girder = round(list_result[result_type]['wtf_girder'], 2)
                    self.result_web_buckling_simple_sai_girder = round(list_result[result_type]['sai_girder'], 2)
                    self.result_web_buckling_simple_fv_girder = round(list_result[result_type]['fv_girder'], 2)
                    self.result_web_buckling_simple_V_p_girder = round(list_result[result_type]['V_p'], 2)
                    self.result_web_buckling_simple_fV_tf_girder = round(list_result[result_type]['V_tf_girder'], 2)

            if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE :
                self.result_mcr = round(list_result[result_type]['Mcr'], 2)
                self.result_IF_lt = round(list_result[result_type]["IF_lt"], 2)
                self.result_tc = round(list_result[result_type]["It"], 2)
                self.result_wc = round(list_result[result_type]["Iw"], 2)
                self.result_nd_esr_lt = round(list_result[result_type]["ND_ESR_lt"], 2)
                self.result_phi_lt = round(list_result[result_type]["phi_lt"], 2)
                self.result_srf_lt = round(list_result[result_type]["SRF_lt"], 2)
                self.result_fcd__lt = round(list_result[result_type]["FCD_lt"], 2)
            else:
                self.result_mcr = 'NA'
                self.result_IF_lt = 'NA'
                self.result_tc = 'NA'
                self.result_wc = 'NA'
                self.result_nd_esr_lt = 'NA'
                self.result_phi_lt = 'NA'
                self.result_srf_lt = 'NA'
                self.result_fcd__lt = 'NA'

            if self.web_buckling :

                self.result_bcI_eff = list_result[result_type]['WebBuckling.I_eff']
                self.result_bcA_eff = list_result[result_type]['WebBuckling.A_eff']
                self.result_bcr_eff = list_result[result_type]['WebBuckling.r_eff']
                self.result_bc = list_result[result_type]['Buckling_class']
                self.result_IF = round(list_result[result_type]["IF"], 2)
                self.result_eff_sr = round(list_result[result_type]["Effective_SR"], 2)
                self.result_ebs = round(list_result[result_type]["EBS"], 2)
                self.result_nd_esr = round(list_result[result_type]["ND_ESR"], 2)
                self.result_phi_zz = round(list_result[result_type]["phi"], 2)
                self.result_srf = round(list_result[result_type]["SRF"], 2)
                self.result_fcd_1_zz = round(list_result[result_type]["FCD_formula"], 2)
                self.result_fcd_2 = round(list_result[result_type]["FCD_max"], 2)
                self.result_fcd = round(list_result[result_type]["FCD"], 2)
                self.result_capacity = round(list_result[result_type]["Capacity"], 2)
                self.result_crippling = round(list_result[result_type]["Web_crippling"], 2)
            else:
                self.result_bc = 'NA'
                self.result_IF = 'NA'
                self.result_eff_sr = 'NA'
                self.result_lambda_vv = 'NA'
                self.result_lambda_psi = 'NA'
                self.result_ebs = 'NA'
                self.result_nd_esr = 'NA'
                self.result_phi_zz = 'NA'
                self.result_srf = 'NA'
                self.result_fcd_1_zz = 'NA'
                self.result_fcd_2 = 'NA'
                self.result_fcd = 'NA'
                self.result_capacity = 'NA'
                self.result_crippling = 'NA'
            if self.result_high_shear and self.input_section_classification[self.result_designation][0] != 'Semi-Compact':
                self.result_mfd = list_result[result_type]["Mfd"]
                self.result_beta_reduced = list_result[result_type]["Beta_reduced"]
                self.result_Md= list_result[result_type]["M_d"]
        except:
            self.result_designation = list_result["Designation"]
            logger.info(
            "The section is {}. The {} section  has  {} flange({}) and  {} web({}).  [Reference: Cl 3.7, IS 800:2007].".format(
                self.input_section_classification[self.result_designation][0] ,
                self.result_designation,
                self.input_section_classification[self.result_designation][1], round(self.input_section_classification[self.result_designation][3],2),
                self.input_section_classification[self.result_designation][2], round(self.input_section_classification[self.result_designation][4],2)
            )
        )
            self.result_latex_tension_zone = list_result["latex.tension_zone"]
            self.result_web_buckling_check = list_result["Web.Buckling"]
            self.result_eff_d = list_result["Reduced.depth"]
            self.result_buckling_crippling = list_result["Buckling.crippling"]

            self.result_section_class = list_result["Section class"]
            self.result_effective_area = round(list_result["Effective area"],2)
            if self.effective_area_factor < 1.0:
                logger.info(
                    "The actual effective area is {} mm2 and the reduced effective area is {} mm2 [Reference: Cl. 7.3.2, IS 800:2007]".format(
                        round((self.result_effective_area / self.effective_area_factor), 2),
                        self.result_effective_area,
                    )
                )

            self.result_shear = round(list_result["Shear Strength"], 2)
            self.result_high_shear = list_result["High Shear check"]
            self.result_bending = round(list_result["Bending Strength"], 2)
            self.result_eff_len = round(list_result["Effective_length"], 2)
            self.result_cost = list_result["Cost"]
            self.result_betab = list_result["Beta_b"]

            if self.result_web_buckling_check :
                logger.warning(
                    "Thin web so take flange to resist moment and web to resist shear[Reference: Cl 8.2.1.1, IS 800:2007]")
                if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0]:
                    logger.info('Transverse Stiffeners at supports required. Design not done for them')
                    self.result_web_buckling_simple_kv = round(list_result['Kv'], 2)
                    self.result_web_buckling_simple_tau_crc = round(list_result['tau_crc'], 2)
                    self.result_web_buckling_simple_lambda_w = round(list_result['lambda_w'], 2)
                    self.result_web_buckling_simple_tau_b = round(list_result['tau_b'], 2)
                    self.result_web_buckling_simple_V_cr = round(list_result['V_cr'], 2)
                elif self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1]:
                    logger.info('Transverse Stiffeners at supports  and intermediate transverse stiffener required. Design not done for them')
                    self.result_web_buckling_simple_kv = round(list_result['Kv'], 2)
                    self.result_web_buckling_simple_tau_crc = round(list_result['tau_crc'], 2)
                    self.result_web_buckling_simple_lambda_w = round(list_result['lambda_w'], 2)
                    self.result_web_buckling_simple_tau_b = round(list_result['tau_b'], 2)
                    self.result_web_buckling_simple_V_cr = round(list_result['V_cr'], 2)
                    self.result_web_buckling_simple_Mfr = round(list_result['Mfr']*10**-6, 2)
                    self.result_web_buckling_simple_Nf = round(list_result['Nf'], 2)
                    self.result_web_buckling_simple_c = round(list_result['c'], 2)
                    self.result_web_buckling_simple_phi_girder = round(list_result['phi_girder'], 2)
                    self.result_web_buckling_simple_s_girder = round(list_result['s_girder'], 2)
                    self.result_web_buckling_simple_wtf_girder = round(list_result['wtf_girder'], 2)
                    self.result_web_buckling_simple_sai_girder = round(list_result['sai_girder'], 2)
                    self.result_web_buckling_simple_fv_girder = round(list_result['fv_girder'], 2)
                    self.result_web_buckling_simple_V_p_girder = round(list_result['V_p'], 2)
                    self.result_web_buckling_simple_fV_tf_girder = round(list_result['V_tf_girder'], 2)

            if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE :
                self.result_mcr = round(list_result['Mcr'], 2)
                self.result_IF_lt = round(list_result["IF_lt"], 2)
                self.result_tc = round(list_result["It"], 2)
                self.result_wc = round(list_result["Iw"], 2)
                self.result_nd_esr_lt = round(list_result["ND_ESR_lt"], 2)
                self.result_phi_lt = round(list_result["phi_lt"], 2)
                self.result_srf_lt = round(list_result["SRF_lt"], 2)
                self.result_fcd__lt = round(list_result["FCD_lt"], 2)
            else:
                self.result_mcr = 'NA'
                self.result_IF_lt = 'NA'
                self.result_tc = 'NA'
                self.result_wc = 'NA'
                self.result_nd_esr_lt = 'NA'
                self.result_phi_lt = 'NA'
                self.result_srf_lt = 'NA'
                self.result_fcd__lt = 'NA'

            if self.web_buckling :

                self.result_bcI_eff = list_result['WebBuckling.I_eff']
                self.result_bcA_eff = list_result['WebBuckling.A_eff']
                self.result_bcr_eff = list_result['WebBuckling.r_eff']
                self.result_bc = list_result['Buckling_class']
                self.result_IF = round(list_result["IF"], 2)
                self.result_eff_sr = round(list_result["Effective_SR"], 2)
                self.result_ebs = round(list_result["EBS"], 2)
                self.result_nd_esr = round(list_result["ND_ESR"], 2)
                self.result_phi_zz = round(list_result["phi"], 2)
                self.result_srf = round(list_result["SRF"], 2)
                self.result_fcd_1_zz = round(list_result["FCD_formula"], 2)
                self.result_fcd_2 = round(list_result["FCD_max"], 2)
                self.result_fcd = round(list_result["FCD"], 2)
                self.result_capacity = round(list_result["Capacity"], 2)
                self.result_crippling = round(list_result["Web_crippling"], 2)
            else:
                self.result_bc = 'NA'
                self.result_IF = 'NA'
                self.result_eff_sr = 'NA'
                self.result_lambda_vv = 'NA'
                self.result_lambda_psi = 'NA'
                self.result_ebs = 'NA'
                self.result_nd_esr = 'NA'
                self.result_phi_zz = 'NA'
                self.result_srf = 'NA'
                self.result_fcd_1_zz = 'NA'
                self.result_fcd_2 = 'NA'
                self.result_fcd = 'NA'
                self.result_capacity = 'NA'
                self.result_crippling = 'NA'
            if self.result_high_shear and self.input_section_classification[self.result_designation][0] != 'Semi-Compact':
                self.result_mfd = list_result["Mfd"]
                self.result_beta_reduced = list_result["Beta_reduced"]
                self.result_Md= list_result["M_d"]

    ### start writing save_design from here!
    def save_design(self, popup_summary):
        # print('self.design_status', self.design_status,'len(self.failed_design_dict)', len(self.failed_design_dict))
        if (self.design_status and self.failed_design_dict is None) or (not self.design_status and len(self.failed_design_dict)>0):# TODO @Rutvik
            self.section_property = self.section_connect_database(self, self.result_designation)
            if self.sec_profile=='Columns' or self.sec_profile=='Beams' or self.sec_profile == VALUES_SECTYPE[1]:
                self.report_column = {KEY_DISP_SEC_PROFILE: "ISection",
                                      KEY_DISP_SECSIZE_pg: (self.section_property.designation, self.sec_profile),
                                      KEY_DISP_COLSEC_REPORT: self.section_property.designation,
                                      KEY_DISP_MATERIAL: self.section_property.material,
     #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
                                      KEY_REPORT_MASS: self.section_property.mass,
                                      KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
                                      KEY_REPORT_DEPTH: self.section_property.depth,
                                      KEY_REPORT_WIDTH: self.section_property.flange_width,
                                      KEY_REPORT_WEB_THK: self.section_property.web_thickness,
                                      KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
                                      KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope,
                                      KEY_REPORT_R1: self.section_property.root_radius,
                                      KEY_REPORT_R2: self.section_property.toe_radius,
                                      KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4, 2),
                                      KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4, 2),
                                      KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1, 2),
                                      KEY_REPORT_RY: round(self.section_property.rad_of_gy_y * 1e-1, 2),
                                      KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3, 2),
                                      KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3, 2),
                                      KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3, 2),
                                      KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3, 2)}



            self.report_input = \
                {#KEY_MAIN_MODULE: self.mainmodule,
                 KEY_MODULE: self.module, #"Axial load on column "
                    KEY_DISP_SHEAR+'*': self.load.shear_force * 10 ** -3,
                    KEY_DISP_BEAM_MOMENT_Latex+'*': self.load.moment * 10 ** -6,
                    KEY_DISP_LENGTH_BEAM: self.result_eff_len,
                    KEY_DISP_SEC_PROFILE: self.sec_profile,
                    KEY_DISP_SECSIZE_pg: str(self.sec_list),
                 KEY_MATERIAL: self.material,
                    "Selected Section Details": self.report_column,
                    KEY_BEAM_SUPP_TYPE: self.latex_design_type,
                }

            # if self.latex_design_type == VALUES_SUPP_TYPE_temp[0]:
            #     self.report_input.update({
            #         KEY_DISP_BENDING: self.bending_type})
            # elif self.latex_design_type == VALUES_SUPP_TYPE_temp[1]:
            #     self.report_input.update({
            #         KEY_BEAM_SUPP_TYPE_DESIGN: self.support,
            #         # KEY_DISP_BENDING: self.bending_type,
            #     })
            self.report_input.update({
                KEY_DISP_SUPPORT : self.support,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.material_property.fu,
                KEY_DISP_YIELD_STRENGTH_REPORT: self.material_property.fy,
                "End Conditions - " + str(self.support): "TITLE",
            })
            # if self.Latex_length == 'NA':
            if self.support == KEY_DISP_SUPPORT1:
                self.report_input.update({
                    DISP_TORSIONAL_RES: self.Torsional_res,
                    DISP_WARPING_RES:self.Warping })
            else:
                self.report_input.update({
                    DISP_SUPPORT_RES: self.Support,
                    DISP_TOP_RES: self.Top})
            self.report_input.update({
                "Design Preference" : "TITLE",
                KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor,
                KEY_DISP_CLASS: self.allow_class,
                KEY_DISP_LOAD: self.Loading,
                KEY_DISPP_LENGTH_OVERWRITE: self.latex_efp,
                KEY_DISP_BEARING_LENGTH + ' (mm)': self.bearing_length,

            })
            # if self.latex_design_type == VALUES_SUPP_TYPE_temp[0] and self.result_web_buckling_check:
            #     self.report_input.update({
            #         KEY_ShearBuckling: self.support_cndition_shear_buckling
            #     })
            # self.report_input.update({
            #      # KEY_DISP_SEC_PROFILE: self.sec_profile,
            #      "I Section - anical PropertiesMech": "TITLE",
            #      })
            self.report_input.update()
            self.report_check = []

            t1 = ('Selected', 'Selected Member Data', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Effective Area', '|p{4cm}|p{1.5cm}|p{9.5cm}|p{1cm}|')
            self.report_check.append(t1)
            t1 = ('Effective Area ($mm^2$)', ' ',
                  sectional_area_change(round(self.result_effective_area,2), round(self.section_property.area,2),
                                        self.effective_area_factor),
                  ' ')
            self.report_check.append(t1)

            # t1 = ('SubSection', 'Section parameters', '|p{4cm}|p{1.5cm}|p{9.5cm}|p{1cm}|')
            # self.report_check.append(t1)
            # t1 = ('d_{web}', ' ',
            #       sectional_area_change(round(self.result_effective_area,2), round(self.section_property.area,2),
            #                             self.effective_area_factor),
            #       ' ')
            # self.report_check.append(t1)

            t1 = ('SubSection', 'Section Classification', '|p{3cm}|p{3.5cm}|p{8.5cm}|p{1cm}|')
            self.report_check.append(t1)
            t1 = ('Web Class', 'Neutral Axis at Mid-Depth',
                  cl_3_7_2_section_classification_web(round(self.result_eff_d, 2), round(self.section_property.web_thickness, 2), round(self.input_section_classification[self.result_designation][4],2),
                                         self.epsilon, self.section_property.type,
                                        self.input_section_classification[self.result_designation][2]),
                  ' ')
            self.report_check.append(t1)
            t1 = ('Flange Class', self.section_property.type,
                  cl_3_7_2_section_classification_flange(round(self.section_property.flange_width/2, 2),
                                                      round(self.section_property.flange_thickness, 2), round(
                          self.input_section_classification[self.result_designation][3], 2),
                                                      self.epsilon,
                                                      self.input_section_classification[self.result_designation][1]),
                  ' ')
            self.report_check.append(t1)
            t1 = ('Section Class', ' ',
                  cl_3_7_2_section_classification(
                                                      self.input_section_classification[self.result_designation][0]),
                  ' ')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Web Slenderness Check', '|p{3cm}|p{4cm}|p{6cm}|p{3 cm}|')
            self.report_check.append(t1)
            t1 = (KEY_DISP_Web_Buckling, cl_8_2_1web_buckling_required(round(self.epsilon,2),round(67 * self.epsilon,2)),
                  cl_8_2_1web_buckling_1(self.result_eff_d, self.section_property.web_thickness,
                                       round(self.result_eff_d / self.section_property.web_thickness,2), self.result_web_buckling_check),
                  get_pass_fail(67 * self.epsilon, round(self.result_eff_d / self.section_property.web_thickness,2), relation="Custom"))
            self.report_check.append(t1)
            if self.result_web_buckling_check:
                t1 = ('SubSection', 'Shear Strength Results: ' + self.support_cndition_shear_buckling, '|p{3.5cm}|p{1.5cm}|p{10cm}|p{1cm}|')
                self.report_check.append(t1)
                if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0]:
                    t1 = (KEY_DISP_K_v_latex , ' ',cl_8_4_2_2_KV(self.result_web_buckling_simple_kv,self.support_cndition_shear_buckling),

                          ' ')
                elif self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1]:
                    t1 = (KEY_DISP_Transverse_Stiffener_spacing, ' ',
                          cl_8_4_2_2_Transverse_Stiffener_spacing(self.result_web_buckling_simple_c),
                          ' ')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_K_v_latex, ' ',cl_8_4_2_2_KV(self.result_web_buckling_simple_kv,self.support_cndition_shear_buckling, self.result_web_buckling_simple_c,self.result_eff_d ),
                          ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_Elastic_Critical_shear_stress_web, ' ',
                      cl_8_4_2_2_taucrc(self.result_web_buckling_simple_kv, 2 * 10 ** 5, 0.3,
                                        self.result_eff_d,
                                        self.section_property.web_thickness,
                                        self.result_web_buckling_simple_tau_crc),
                      ' ')
                self.report_check.append(t1)



                t1 = (KEY_DISP_slenderness_ratio_web, ' ',
                      cl_8_4_2_2_slenderness_ratio(self.fyw, self.result_web_buckling_simple_lambda_w,
                                           self.result_web_buckling_simple_tau_crc),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_OUT_DISP_WELD_SHEAR_STRESS, ' ',
                      cl_8_4_2_2_shearstress_web(self.fyw, self.result_web_buckling_simple_lambda_w, self.result_web_buckling_simple_tau_b),
                      ' ')
                self.report_check.append(t1)

                if self.support_cndition_shear_buckling == KEY_DISP_SB_Option[0]:
                    t1 = (KEY_DISP_DESIGN_STRENGTH_SHEAR + '(V_{d})', self.load.shear_force * 10 ** -3,
                          cl_8_4_2_2_shearstrength(self.result_eff_d, self.section_property.web_thickness,self.result_web_buckling_simple_V_cr,
                                                     self.result_web_buckling_simple_tau_b, self.result_shear),
                          ' ')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_ALLOW_SHEAR, ' ',
                          cl_8_2_1_2_shear_check(round(self.result_shear, 2), round(0.6 * self.result_shear, 2),
                                                 self.result_high_shear, self.load.shear_force * 10 ** -3),
                          get_pass_fail(self.load.shear_force * 10 ** -3, round(0.6 * self.result_shear, 2),
                                        relation="Warn", M1=self.result_high_shear))
                    self.report_check.append(t1)

                elif self.support_cndition_shear_buckling == KEY_DISP_SB_Option[1]:
                    t1 = (KEY_DISP_BUCKLING_STRENGTH + '(V_p)', ' ',
                          cl_8_4_1_plastic_shear_resistance_Vp(self.result_eff_d,self.section_property.web_thickness,self.fyw, self.result_web_buckling_simple_V_p_girder
                                                     ),
                          ' ')
                    self.report_check.append(t1)

                    t1 = ('N_f (N)', ' ',
                          cl_8_4_2_2_N_f(self.section_property.depth,
                                                                 self.section_property.flange_thickness,
                                                                 self.section_property.depth - self.section_property.flange_thickness,
                                         round(self.load.moment / (
                                                 self.section_property.depth - self.section_property.flange_thickness),2) , self.load.moment
                                                                 ),
                          ' ')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_reduced_moment + '(M_{fr})', ' ',
                          cl_8_4_2_2_TensionField_reduced_moment(self.result_web_buckling_simple_Mfr, self.section_property.flange_width,self.section_property.flange_thickness,
                                                               self.fyf, round(self.load.moment / (
                                                 self.section_property.depth - self.section_property.flange_thickness),2)
                                                               ),
                          ' ')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_tension_field_incline , ' ',
                          cl_8_4_2_2_TensionField_phi(self.result_web_buckling_simple_phi_girder, self.result_web_buckling_simple_c,self.result_eff_d
                                                                 ),
                          ' ')
                    self.report_check.append(t1)

                    t1 = (KEY_DISP_AnchoragelengthTensionField, ' ',
                          cl_8_4_2_2_TensionField_anchorage_length(self.result_web_buckling_simple_s_girder, self.result_web_buckling_simple_phi_girder,
                          self.result_web_buckling_simple_Mfr, self.fyw, self.section_property.web_thickness
                                                                 ),
                          ' ')
                    self.report_check.append(t1)


                    t1 = (KEY_DISP_WidthTensionField , ' ',
                          cl_8_4_2_2_KEY_DISP_WidthTensionField(self.result_eff_d,self.result_web_buckling_simple_phi_girder,
                                                                 self.result_web_buckling_simple_c,
                                                                 self.result_web_buckling_simple_s_girder,self.result_web_buckling_simple_wtf_girder
                                                                 ),
                          ' ')
                    self.report_check.append(t1)
                    # t1 = (KEY_DISP_reduced_moment + '(M_{fr}', ' ',
                    #       cl_8_4_2_2_TensionField_reduced_moment(self.result_eff_d,
                    #                                              self.result_web_buckling_simple_phi_girder,
                    #                                              self.result_web_buckling_simple_c,
                    #                                              self.result_web_buckling_simple_s_girder,self.result_web_buckling_simple_wtf_girder
                    #                                              ),
                    #       ' ')
                    # self.report_check.append(t1)
                    t1 = (KEY_DISP_Yield_Strength_Tension_field, ' ',
                          cl_8_4_2_2_Yield_Strength_Tension_field(self.fyw,
                                                                 self.result_web_buckling_simple_tau_b,
                                                                 self.result_web_buckling_simple_phi_girder,
                                                                 self.result_web_buckling_simple_fv_girder
                                                                 ),
                          ' ')
                    self.report_check.append(t1)
                    t1 = (KEY_DISP_DESIGN_STRENGTH_SHEAR + '(V_{d})', self.load.shear_force * 10 ** -3,
                          cl_8_4_2_2_shearstrength_tensionfield(self.effective_depth * self.section_property.web_thickness, self.result_web_buckling_simple_tau_b,self.result_web_buckling_simple_V_p_girder,
                                                     self.result_shear,self.section_property.web_thickness, self.result_web_buckling_simple_wtf_girder, self.result_web_buckling_simple_fv_girder,
                                                                self.result_web_buckling_simple_phi_girder, round(self.result_web_buckling_simple_fV_tf_girder * 10**-3,2)),
                          ' ')
                    self.report_check.append(t1)


            else:

                t1 = ('SubSection', 'Shear Strength Results', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)

                t1 = (KEY_DISP_DESIGN_STRENGTH_SHEAR, self.load.shear_force * 10 ** -3,
                      cl_8_4_shear_yielding_capacity_member_(self.section_property.depth,
                                                            self.section_property.web_thickness, self.material_property.fy,
                                                            self.gamma_m0, round(self.result_shear, 2)),
                      get_pass_fail(self.load.shear_force * 10 ** -3, round(self.result_shear, 2), relation="lesser"))
                self.report_check.append(t1)

                t1 = (KEY_DISP_ALLOW_SHEAR, ' ',
                      cl_8_2_1_2_shear_check(round(self.result_shear,2), round(0.6 * self.result_shear,2), self.result_high_shear,self.load.shear_force*10**-3),
                      get_pass_fail(self.load.shear_force*10**-3, round(0.6 * self.result_shear,2), relation="Warn",M1=self.result_high_shear))
                self.report_check.append(t1)

                # t1 = ('SubSection', 'Moment Strength Results', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')

            t1 = ('SubSection', 'Moment Strength Results', '|p{4cm}|p{1.5cm}|p{9cm}|p{1.5cm}|')
            self.report_check.append(t1)
            if self.design_type == KEY_DISP_DESIGN_TYPE_FLEXURE:
                if self.result_high_shear:
                    t1 = (KEY_DISP_Bending_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending_md_init(
                              self.section_property.elast_sec_mod_z,
                              self.section_property.plast_sec_mod_z,
                              self.material_property.fy, self.support,
                              self.gamma_m0, round(self.result_betab, 2),
                              round(self.result_Md * 10 ** -6, 2), self.result_section_class
                          ),
                          ' ')
                    self.report_check.append(t1)
                    t1 = (KEY_DISP_PLASTIC_STRENGTH_MOMENT,' ',
                          cl_9_2_2_combine_shear_bending_mfd(
                                                         self.section_property.plast_sec_mod_z,
                                                         self.section_property.depth,
                                                         self.section_property.web_thickness,
                                                         self.material_property.fy,
                                                         self.gamma_m0,
                                                         round(self.result_mfd * 10 ** -6, 2)),
                          ' ')
                    self.report_check.append(t1)

                    # temp = cl_8_2_1_2_plastic_moment_capacity_member(self.result_betab,
                    #                                           self.section_property.plast_sec_mod_z,
                    #                                           self.material_property.fy, self.gamma_m0,
                    #                                           round(self.result_bending, 2))
                    # print('tempt',temp)

                    t1 = (KEY_DISP_DESIGN_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending(round(self.result_bending,2),self.section_property.elast_sec_mod_z,
                                                         self.material_property.fy,self.result_section_class,self.load.shear_force*10**-3, round(self.result_shear,2),
                                                         self.gamma_m0, round(self.result_beta_reduced,2),round(self.result_Md*10**-6,2),round(self.result_mfd*10**-6,2)),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)

                else:
                    t1 = (KEY_DISP_DESIGN_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_8_2_1_2_moment_capacity_member(round(self.result_betab,3),
                                                                    self.section_property.plast_sec_mod_z,
                                                                    self.material_property.fy, self.gamma_m0,
                                                                    round(self.result_bending, 2), self.section_property.elast_sec_mod_z,self.result_section_class,self.support),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)
            elif self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
                # KEY_DISP_Elastic_CM_latex
                t1 = (KEY_DISP_Elastic_CM_latex, ' ',
                          cl_8_2_2_1_Mcr(
                              self.result_mcr,
                              self.material_property.modulus_of_elasticity,
                              self.section_property.mom_inertia_y,
                              self.result_eff_len, self.material_property.modulus_of_elasticity/(2*1.3),
                              self.section_property.It, self.section_property.Iw
                            #   round(self.result_Md * 10 ** -6, 2), self.result_section_class
                          ),
                          ' ')
                self.report_check.append(t1)

                # t1 = (KEY_DISP_I_eff_latex + '($mm^4$)', ' ',
                #       cl_8_7_3_Ieff_web_check(self.bearing_length, self.section_property.web_thickness,
                #                                            round(self.result_bcI_eff,2)),
                #       ' ')
            #     self.report_check.append(t1)

            #     t1 = (KEY_DISP_A_eff_latex+ '($mm^2$)', ' ',
            #           cl_8_7_3_Aeff_web_check(self.bearing_length, self.section_property.web_thickness,
            #                                                self.result_bcA_eff),
            #           ' ')
            #     self.report_check.append(t1)

            #     t1 = (KEY_DISP_r_eff_latex+ '(mm)', ' ',
            #           cl_8_7_3_reff_web_check(round(self.result_bcr_eff,2), round(self.result_bcI_eff,2),
            #                                                self.result_bcA_eff),
            #           ' ')
            #     self.report_check.append(t1)

                t1 = (KEY_DISP_SLENDER + r'($\lambda_{LT}$)', ' ',
                      cl_8_2_2_slenderness(round(self.result_betab, 2),self.section_property.elast_sec_mod_z,
                              self.section_property.plast_sec_mod_z,self.result_mcr,self.material_property.fy,
                                              self.result_nd_esr_lt),
                      ' ')
                self.report_check.append(t1)

            #     # t1 = (KEY_DISP_SLENDER, ' ',
            #     #       cl_8_7_1_5_slenderness(round(self.result_bcr_eff, 2), round(self.result_eff_d, 2),
            #     #                              self.result_eff_sr),
            #     #       ' ')
            #     # self.report_check.append(t1)

            #     t1 = (KEY_DISP_BUCKLING_CURVE_ZZ, ' ',
            #           cl_8_7_1_5_buckling_curve(),
            #           ' ')
            #     self.report_check.append(t1)

                t1 = (KEY_DISP_IMPERFECTION_FACTOR_ZZ + r'($\alpha_{LT}$)', ' ',
                      cl_8_7_1_5_imperfection_factor(self.result_IF_lt),
                      ' ')
                self.report_check.append(t1)

            #     t1 = (KEY_DISP_EULER_BUCKLING_STRESS_ZZ, ' ',
            #           cl_8_7_1_5_buckling_stress(self.section_property.modulus_of_elasticity,self.result_eff_sr,self.result_ebs),
            #           ' ')
            #     self.report_check.append(t1)

                t1 = (r'$\phi_{LT}$', ' ',
                      cl_8_2_2_phi(self.result_IF_lt,self.result_nd_esr_lt, self.result_phi_lt),
                      ' ')
                self.report_check.append(t1)

                t1 = ('Bending Compressive stress($N/mm^2$)', ' ',
                      cl_8_2_2_Bending_Compressive(self.material_property.fy,self.gamma_m0,self.result_nd_esr_lt,self.result_phi_lt,self.result_fcd__lt),
                      ' ')
                self.report_check.append(t1)

            #     t1 = (KEY_DISP_BUCKLING_STRENGTH, self.load.shear_force * 10 ** -3,
            #           cl_7_1_2_design_compressive_strength(self.result_capacity,round((
            #                     self.bearing_length + self.section_property.depth / 2) * self.section_property.web_thickness,2), self.result_fcd,self.load.shear_force * 10 ** -3),
            #           get_pass_fail(self.load.shear_force * 10 ** -3, round(self.result_capacity, 2), relation="leq"))
            #     self.report_check.append(t1)

                if self.result_high_shear:
                    t1 = (KEY_DISP_LTB_Bending_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending_md_init(
                              self.section_property.elast_sec_mod_z,
                              self.section_property.plast_sec_mod_z,
                              self.material_property.fy, self.support,
                              self.gamma_m0, round(self.result_betab, 2),
                              round(self.result_Md * 10 ** -6, 2), self.result_section_class
                          ),
                          ' ')
                    self.report_check.append(t1)
                    t1 = (KEY_DISP_PLASTIC_STRENGTH_MOMENT,' ',
                          cl_9_2_2_combine_shear_bending_mfd(
                                                         self.section_property.plast_sec_mod_z,
                                                         self.section_property.depth,
                                                         self.section_property.web_thickness,
                                                         self.material_property.fy,
                                                         self.gamma_m0,
                                                         round(self.result_mfd * 10 ** -6, 2)),
                          ' ')
                    self.report_check.append(t1)

                    # temp = cl_8_2_1_2_plastic_moment_capacity_member(self.result_betab,
                    #                                           self.section_property.plast_sec_mod_z,
                    #                                           self.material_property.fy, self.gamma_m0,
                    #                                           round(self.result_bending, 2))
                    # print('tempt',temp)
                    t1 = (KEY_DISP_REDUCE_STRENGTH_MOMENT, self.load.moment*10**-6,
                          cl_9_2_2_combine_shear_bending(round(self.result_bending,2),self.section_property.elast_sec_mod_z,
                                                         self.material_property.fy,self.result_section_class,self.load.shear_force*10**-3, round(self.result_shear,2),
                                                         self.gamma_m0, round(self.result_betab,2),round(self.result_Md*10**-6,2),round(self.result_mfd*10**-6,2)),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)

                else:
                    t1 = ('Moment Strength (kNm)', self.load.moment*10**-6,
                          cl_8_2_2_moment_capacity_member(round(self.result_betab,2),
                                                                    self.section_property.plast_sec_mod_z,
                                                                    self.material_property.fy, self.gamma_m0,
                                                                    round(self.result_bending, 2),self.section_property.elast_sec_mod_z,self.result_section_class,self.support),
                          get_pass_fail(self.load.moment*10**-6, round(self.result_bending, 2), relation="lesser"))
                    self.report_check.append(t1)

            if self.result_buckling_crippling:
                t1 = ('SubSection', 'Web Buckling Checks', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
                self.report_check.append(t1)

                t1 = (KEY_DISP_I_eff_latex + '($mm^4$)', ' ',
                      cl_8_7_3_Ieff_web_check(self.bearing_length, self.section_property.web_thickness,
                                                           round(self.result_bcI_eff,2)),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_A_eff_latex+ '($mm^2$)', ' ',
                      cl_8_7_3_Aeff_web_check(self.bearing_length, self.section_property.web_thickness,
                                                           self.result_bcA_eff),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_r_eff_latex+ '(mm)', ' ',
                      cl_8_7_3_reff_web_check(round(self.result_bcr_eff,2), round(self.result_bcI_eff,2),
                                                           self.result_bcA_eff),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_SLENDER + r'($\lambda$)', ' ',
                      cl_8_7_1_5_slenderness(round(self.result_bcr_eff, 2), round(self.result_eff_d, 2),
                                              self.result_eff_sr),
                      ' ')
                self.report_check.append(t1)

                # t1 = (KEY_DISP_SLENDER, ' ',
                #       cl_8_7_1_5_slenderness(round(self.result_bcr_eff, 2), round(self.result_eff_d, 2),
                #                              self.result_eff_sr),
                #       ' ')
                # self.report_check.append(t1)

                t1 = (KEY_DISP_BUCKLING_CURVE_ZZ, ' ',
                      cl_8_7_1_5_buckling_curve(),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_IMPERFECTION_FACTOR_ZZ + r'($\alpha$)', ' ',
                      cl_8_7_1_5_imperfection_factor(self.result_IF),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_EULER_BUCKLING_STRESS_ZZ, ' ',
                      cl_8_7_1_5_buckling_stress(self.section_property.modulus_of_elasticity,self.result_eff_sr,self.result_ebs),
                      ' ')
                self.report_check.append(t1)

                t1 = (r'$\phi$', ' ',
                      cl_8_7_1_5_phi(0.49,self.result_eff_sr, self.result_phi_zz),
                      ' ')
                self.report_check.append(t1)

                t1 = ('Buckling stress($N/mm^2$)', ' ',
                      cl_8_7_1_5_Buckling(self.material_property.fy,self.gamma_m0,self.result_eff_sr,self.result_phi_zz,self.result_fcd_2,self.result_fcd),
                      ' ')
                self.report_check.append(t1)

                t1 = (KEY_DISP_BUCKLING_STRENGTH, self.load.shear_force * 10 ** -3,
                      cl_7_1_2_design_compressive_strength(self.result_capacity,round((
                                self.bearing_length + self.section_property.depth / 2) * self.section_property.web_thickness,2), self.result_fcd,self.load.shear_force * 10 ** -3),
                      get_pass_fail(self.load.shear_force * 10 ** -3, round(self.result_capacity, 2), relation="leq"))
                self.report_check.append(t1)

                t1 = ('SubSection', 'Web Bearing Checks', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
                self.report_check.append(t1)

                t1 = ('Bearing Strength(kN)', self.load.shear_force * 10 ** -3,
                      cl_8_7_4_Bearing_stiffener_check(self.bearing_length, round(2.5 * (
                                                    self.section_property.root_radius + self.section_property.flange_thickness), 2),
                                                       self.section_property.web_thickness,
                                                       self.material_property.fy, self.gamma_m0,
                                                       round(self.result_crippling, 2),
                                                       self.section_property.root_radius,
                                                       self.section_property.flange_thickness),
                      get_pass_fail(self.load.shear_force * 10 ** -3, round(self.result_crippling, 2), relation="leq"))

                self.report_check.append(t1)

            t1 = ('SubSection', 'Utilization', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            self.report_check.append(t1)
            # TODO
            if self.result_buckling_crippling:
                t1 = (KEY_DISP_Utilization_Ratio, 1.0,
                    Utilization_Ratio_Latex(self.load.shear_force * 10 ** -3,round(self.result_shear, 2),
                                                            self.load.moment*10**-6, round(self.result_bending, 2),
                                                            self.result_UR,type=2,Pd=self.result_capacity, fw=self.result_crippling),
                    get_pass_fail(1.0, self.result_UR, relation="geq"))
            else:
                t1 = (KEY_DISP_Utilization_Ratio, 1.0,
                    Utilization_Ratio_Latex(self.load.shear_force * 10 ** -3,round(self.result_shear, 2),
                                                            self.load.moment*10**-6, round(self.result_bending, 2),
                                                            self.result_UR),
                    get_pass_fail(1.0, self.result_UR, relation="geq"))
            self.report_check.append(t1)
#
    #     elif not self.design_status or len(self.failed_design_dict)>0:
    #         self.section_property = self.section_connect_database(self, self.result_designation)

    #         if self.sec_profile=='Columns' or self.sec_profile=='Beams' or self.sec_profile == VALUES_SECTYPE[1]:
    #             self.report_column = {KEY_DISP_SEC_PROFILE: "ISection",
    #                                   KEY_DISP_SECSIZE: (self.section_property.designation, self.sec_profile),
    #                                   KEY_DISP_COLSEC_REPORT: self.section_property.designation,
    #                                   KEY_DISP_MATERIAL: self.section_property.material,
    #  #                                 KEY_DISP_APPLIED_AXIAL_FORCE: self.section_property.,
    #                                   KEY_REPORT_MASS: self.section_property.mass,
    #                                   KEY_REPORT_AREA: round(self.section_property.area * 1e-2, 2),
    #                                   KEY_REPORT_DEPTH: self.section_property.depth,
    #                                   KEY_REPORT_WIDTH: self.section_property.flange_width,
    #                                   KEY_REPORT_WEB_THK: self.section_property.web_thickness,
    #                                   KEY_REPORT_FLANGE_THK: self.section_property.flange_thickness,
    #                                   KEY_DISP_FLANGE_S_REPORT: self.section_property.flange_slope,
    #                                   KEY_REPORT_R1: self.section_property.root_radius,
    #                                   KEY_REPORT_R2: self.section_property.toe_radius,
    #                                   KEY_REPORT_IZ: round(self.section_property.mom_inertia_z * 1e-4, 2),
    #                                   KEY_REPORT_IY: round(self.section_property.mom_inertia_y * 1e-4, 2),
    #                                   KEY_REPORT_RZ: round(self.section_property.rad_of_gy_z * 1e-1, 2),
    #                                   KEY_REPORT_RY: round(self.section_property.rad_of_gy_y * 1e-1, 2),
    #                                   KEY_REPORT_ZEZ: round(self.section_property.elast_sec_mod_z * 1e-3, 2),
    #                                   KEY_REPORT_ZEY: round(self.section_property.elast_sec_mod_y * 1e-3, 2),
    #                                   KEY_REPORT_ZPZ: round(self.section_property.plast_sec_mod_z * 1e-3, 2),
    #                                   KEY_REPORT_ZPY: round(self.section_property.plast_sec_mod_y * 1e-3, 2)}



    #         self.report_input = \
    #             {#KEY_MAIN_MODULE: self.mainmodule,
    #              KEY_MODULE: self.module, #"Axial load on column "
    #                 KEY_DISP_SHEAR+'*': self.load.shear_force * 10 ** -3,
    #                 KEY_DISP_BEAM_MOMENT_Latex+'*': self.load.moment * 10 ** -6,
    #                 KEY_DISP_LENGTH_BEAM: self.result_eff_len,
    #                 KEY_DISP_SEC_PROFILE: self.sec_profile,
    #                 KEY_DISP_SECSIZE: str(self.sec_list),
    #              KEY_MATERIAL: self.material,
    #                 "Selected Section Details": self.report_column,
    #                 KEY_BEAM_SUPP_TYPE: self.latex_design_type,
    #             }

            # if self.design_type == KEY_DISP_DESIGN_TYPE2_FLEXURE:
            #     t1 = ('SubSection', 'Lateral Torsional Buckling Checks', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            #     self.report_check.append(t1)

            #     t1 = ('SubSection', 'Web Bearing Checks', '|p{4cm}|p{2 cm}|p{7cm}|p{3 cm}|')
            #     self.report_check.append(t1)

            #     t1 = ('Bearing Strength(kN)', self.load.shear_force * 10 ** -3,
            #           cl_8_7_4_Bearing_stiffener_check(self.bearing_length, round(2.5 * (
            #                                         self.section_property.root_radius + self.section_property.flange_thickness), 2),
            #                                            self.section_property.web_thickness,
            #                                            self.material_property.fy, self.gamma_m0,
            #                                            round(self.result_crippling, 2),
            #                                            self.section_property.root_radius,
            #                                            self.section_property.flange_thickness),
            #           get_pass_fail(self.load.shear_force * 10 ** -3, round(self.result_crippling, 2), relation="leq"))

            #     self.report_check.append(t1)
                # t1 = (KEY_DISP_A_eff_latex + '(mm^2)', ' ',
                #       cl_8_7_3_Aeff_web_check(self.bearing_length, self.section_property.web_thickness,
                #                               self.result_bcA_eff),
                #       ' ')
                # self.report_check.append(t1)
            # if self.latex_tension_zone == True :
            #     t1 = (KEY_DISP_TENSION_HOLES, ' ',
            #           sectional_area_change(self.result_effective_area, self.section_property.area,
            #                                 self.effective_area_factor),
            #           ' ')
            #     self.report_check.append(t1)

        # else:
        #     t1 = (KEY_DISP_ALLOW_SHEAR, self.load.shear_force,
        #           allow_shear_capacity(round(self.result_shear, 2), round(0.6 * self.result_shear, 2)),
        #           get_pass_fail(self.load.shear_force))
        # self.report_check.append(t1)



        # self.h = (self.beam_D - (2 * self.beam_tf))
        #
        # 1.1 Input sections display
        # t1 = ('SubSection', 'List of Input Sections',self.sec_list),
        # self.report_check.append(t1)
        #
        # # 2.2 CHECK: Buckling Class - Compatibility Check
        # t1 = ('SubSection', 'Buckling Class - Compatibility Check', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{2cm}|')
        # self.report_check.append(t1)
        #
        # t1 = ("Section Class ", comp_column_class_section_check_required(self.result_section_class, self.h, self.bf),
        #       comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf),
        #       'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)

        # t1 = ("h/bf , tf ", comp_column_class_section_check_required(self.bucklingclass, self.h, self.bf),
        #       comp_column_class_section_check_provided(self.bucklingclass, self.h, self.bf, self.tf, self.var_h_bf),
        #       'Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)
        #
        # # 2.3 CHECK: Cross-section classification
        # t1 = ('SubSection', 'Cross-section classification', '|p{4.5cm}|p{3cm}|p{6.5cm}|p{1.5cm}|')
        # self.report_check.append(t1)
        #
        # t1 = ("b/tf and d/tw ", cross_section_classification_required(self.section),
        #       cross_section_classification_provided(self.tf, self.b1, self.epsilon, self.section, self.b1_tf,
        #                                             self.d1_tw, self.ep1, self.ep2, self.ep3, self.ep4),
        #       'b = bf / 2,d = h – 2 ( T + R1),έ = (250 / Fy )^0.5,Compatible')  # if self.bc_compatibility_status is True else 'Not compatible')
        # self.report_check.append(t1)
        #
        # # 2.4 CHECK : Member Check
        # t1 = ("Slenderness", cl_7_2_2_slenderness_required(self.KL, self.ry, self.lamba),
        #       cl_7_2_2_slenderness_provided(self.KL, self.ry, self.lamba), 'PASS')
        # self.report_check.append(t1)
        #
        # t1 = (
        # "Design Compressive stress (fcd)", cl_7_1_2_1_fcd_check_required(self.gamma_mo, self.f_y, self.f_y_gamma_mo),
        # cl_7_1_2_1_fcd_check_provided(self.facd), 'PASS')
        # self.report_check.append(t1)
        #
        # t1 = ("Design Compressive strength (Pd)", cl_7_1_2_design_comp_strength_required(self.axial),
        #       cl_7_1_2_design_comp_strength_provided(self.Aeff, self.facd, self.A_eff_facd), "PASS")
        # self.report_check.append(t1)
        #
        # t1 = ('', '', '', '')
        # self.report_check.append(t1)
        else:
            self.report_input = \
                {#KEY_MAIN_MODULE: self.mainmodule,
                 KEY_MODULE: self.module, #"Axial load on column "
                    KEY_DISP_SHEAR+'*': self.load.shear_force * 10 ** -3,
                    KEY_DISP_BEAM_MOMENT_Latex+'*': self.load.moment * 10 ** -6,
                    KEY_DISP_LENGTH_BEAM: self.length,
                    KEY_DISP_SEC_PROFILE: self.sec_profile,
                    KEY_DISP_SECSIZE_pg: str(self.sec_list),
                 KEY_MATERIAL: self.material,
                    # "Failed Section Details": self.report_column,
                    KEY_BEAM_SUPP_TYPE: self.latex_design_type,
                }
            self.report_input.update({
                KEY_DISP_SUPPORT : self.support,
                KEY_DISP_ULTIMATE_STRENGTH_REPORT: self.material_property.fu,
                KEY_DISP_YIELD_STRENGTH_REPORT: self.material_property.fy,
                "End Conditions - " + str(self.support): "TITLE",
            })
            # if self.Latex_length == 'NA':
            if self.support == KEY_DISP_SUPPORT1:
                self.report_input.update({
                    DISP_TORSIONAL_RES: self.Torsional_res,
                    DISP_WARPING_RES:self.Warping })
            else:
                self.report_input.update({
                    DISP_SUPPORT_RES: self.Support,
                    DISP_TOP_RES: self.Top})
            self.report_input.update({
                "Design Preference" : "TITLE",
                KEY_DISP_EFFECTIVE_AREA_PARA: self.effective_area_factor,
                KEY_DISP_CLASS: self.allow_class,
                KEY_DISP_LOAD: self.Loading,
                KEY_DISPP_LENGTH_OVERWRITE: self.latex_efp,
                KEY_DISP_BEARING_LENGTH + ' (mm)': self.bearing_length,

            })
            # if self.latex_design_type == VALUES_SUPP_TYPE_temp[0] and self.result_web_buckling_check:
            #     self.report_input.update({
            #         KEY_ShearBuckling: self.support_cndition_shear_buckling
            #     })
            # self.report_input.update({
            #      # KEY_DISP_SEC_PROFILE: self.sec_profile,
            #      "I Section - Mechanical Properties": "TITLE",
            #      })
            self.report_input.update()
            self.report_check = []

            t1 = ('Selected', 'All Members Failed', '|p{5cm}|p{2cm}|p{2cm}|p{2cm}|p{4cm}|')
            self.report_check.append(t1)

            t1 = ('SubSection', 'Plastic Section Modulus', '|p{4cm}|p{1.5cm}|p{2.5cm}|p{8cm}|')
            self.report_check.append(t1)
            t1 = ('Plastic Section Modulus($mm^3$)', round(self.Zp_req,2),
                  ' ',
                  'Select Sections with atleast required Plastic Section Modulus ')
            self.report_check.append(t1)


        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"

        print(sys.path[0])
        rel_path = str(sys.path[0])
        rel_path = os.path.abspath(".") # TEMP
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext,
                              rel_path, Disp_2d_image, Disp_3D_image, module=self.module) #
        
