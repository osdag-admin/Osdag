"""
Input dock widget for Osdag GUI.
Handles user input forms and group boxes for connection design.
"""
import sys, time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QComboBox, QScrollArea, QLabel, QFormLayout, QLineEdit, QGroupBox, QSizePolicy
)
from PySide6.QtWidgets import QMessageBox, QDialog, QGridLayout, QProgressBar
from PySide6.QtCore import Qt, QRegularExpression, QCoreApplication, QRect, QThread, Signal
from PySide6.QtGui import QPixmap, QIcon, QBrush, QColor, QDoubleValidator, QRegularExpressionValidator, QIntValidator

from osdag_gui.ui.components.additional_inputs_button import AdditionalInputsButton
from osdag_gui.ui.components.custom_buttons import CustomButton
import osdag_gui.resources.resources_rc
from osdag_gui.ui.components.customized_popups import Ui_Popup

from osdag_core.Common import *

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()  # Prevent changing selection on scroll

def right_aligned_widget(widget):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    layout.setAlignment(widget, Qt.AlignVCenter)  # Optional: vertical center
    return container

def left_aligned_widget(widget):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    layout.addStretch()
    layout.setAlignment(widget, Qt.AlignVCenter)  # Optional: vertical center
    return container

def apply_field_style(widget):
    arrow_down_path = ":/images/down_arrow.png"
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    # Removed setFixedWidth to allow expansion
    if isinstance(widget, QComboBox):
        style = f"""
        QComboBox {{
            padding: 2px;
            border: 1px solid black;
            border-radius: 5px;
            background-color: white;
            color: black;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            border-left: 0px;
        }}
        QComboBox::down-arrow {{
            image: url("{arrow_down_path}");
            width: 15px;
            height: 15px;
            margin-right: 5px;
        }}
        QComboBox QAbstractItemView {{
            background-color: white;
            border: 1px solid black;
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            color: black;
            background-color: white;
            border: none;
            border: 1px solid white;
            border-radius: 0;
            padding: 2px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            border: 1px solid #90AF13;
            background-color: #90AF13;
            color: black;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: #90AF13;
            color: black;
            border: 1px solid #90AF13;
        }}
        QComboBox QAbstractItemView::item:selected:hover {{
            background-color: #90AF13;
            color: black;
            border: 1px solid #94b816;
        }}
        """
        widget.setStyleSheet(style)
    elif isinstance(widget, QLineEdit):
        widget.setStyleSheet("""
        QLineEdit {
            padding: 1px 7px;
            border: 1px solid #070707;
            border-radius: 6px;
            background-color: white;
            color: #000000;
            font-weight: normal;
        }
        """)

def style_main_buttons():
    return """
        QPushButton {
            background-color: #94b816;
            color: white;
            font-weight: bold;
            border-radius: 4px;
            padding: 6px 18px;
        }
        QPushButton:hover {
            background-color: #7a9a12;
        }
        QPushButton:pressed {
            background-color: #5f7a0e;
        }
    """


class InputDock(QWidget):
    # inputDockVisibilityChanged = Signal(bool)

    def __init__(self, backend:object, parent):
        super().__init__()
        self.parent = parent
        # Already an Object created in template_page.py
        self.backend = backend
        self.input_widget = None

        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.left_container = QWidget()
        self.original_width = int(self.width())

        # Bring the data instance from `design_type` folder
        input_field_list = self.backend.input_values()
        # To equalize the label length
        # So that they are of equal size
        input_field_list = self.equalize_label_length(input_field_list)

        self.build_left_panel(input_field_list)
        self.main_layout.addWidget(self.left_container)

        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #94b816;")
        self.toggle_strip.setFixedWidth(6)
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("❮")
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setToolTip("Hide panel")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c8408;
                color: white;
                font-size: 12px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #5e7407;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_input_dock)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        self.main_layout.addWidget(self.toggle_strip)
    
    # To equalize the size of label strings
    def equalize_label_length(self, list):
        # Calculate maximum size
        max_len = 0
        for t in list:
            if t[2] not in [TYPE_TITLE, TYPE_IMAGE]:
                if len(t[1]) > max_len:
                    max_len = len(t[1])
        
        # Create a new list with equal string length
        return_list = [] 
        for t in list:
            if t[2] not in [TYPE_TITLE, TYPE_IMAGE]:
                new_tupple = (t[0], t[1].ljust(max_len)) + t[2:]
            else:
                new_tupple = t
            return_list.append(new_tupple)

        return return_list

    def get_validator(self, validator):
        if validator == 'Int Validator':
            return QRegularExpressionValidator(QRegularExpression("^(0|[1-9]\d*)(\.\d+)?$"))
        elif validator == 'Double Validator':
            return QDoubleValidator()
        else:
            return None
        
    def build_left_panel(self, field_list):
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # --- Main Content Panel (to be scrolled horizontally and vertically) ---
        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("background-color: white;")
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(5, 5, 5, 5)
        panel_layout.setSpacing(0)

        # --- Top Bar (fixed inside scroll area) ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)
        input_dock_btn = QPushButton("Basic Inputs")
        input_dock_btn.setStyleSheet(style_main_buttons())
        input_dock_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(input_dock_btn)
        additional_inputs_btn = AdditionalInputsButton()
        additional_inputs_btn.clicked.connect(lambda: self.parent.common_function_for_save_and_design(self.backend, data, "Design_Pref"))
        additional_inputs_btn.clicked.connect(lambda: self.parent.combined_design_prefer(data,self.backend))
        additional_inputs_btn.clicked.connect(lambda: self.parent.design_preferences())
        additional_inputs_btn.setToolTip("Additional Inputs")
        additional_inputs_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(additional_inputs_btn)
        panel_layout.addLayout(top_bar)

        # Vertical scroll area for group boxes (vertical only)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #EFEFEC;
                background-color: transparent;
                padding: 3px;
            }
            QScrollBar:vertical {
                background: #E0E0E0;
                width: 8px;
                margin: 0px 0px 0px 3px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #A0A0A0;
                min-height: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #707070;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        group_container = QWidget()
        self.input_widget = group_container
        group_container_layout = QVBoxLayout(group_container)

        # --- Main Content (group boxes) ---

        # Track any group is active or not
        track_group = False
        index = 0
        for field in field_list:
            index += 1
            label = field[1]
            type = field[2]
            print(f"Option:{field}")
            if type == TYPE_MODULE:
                # No use of module title will see.
                continue
            elif type == TYPE_TITLE:
                if track_group:
                    current_group.setLayout(cur_box_form)
                    group_container_layout.addWidget(current_group)
                    track_group = False
                
                # Initialized the group box for current title
                current_group = QGroupBox(label)
                current_group.setObjectName(label + "_group")
                track_group = True
                current_group.setStyleSheet("""
                    QGroupBox {
                        border: 1px solid #90AF13;
                        border-radius: 4px;
                        margin-top: 0.8em;
                        font-weight: bold;
                    }
                    QGroupBox::title {
                        subcontrol-origin: content;
                        subcontrol-position: top left;
                        left: 10px;
                        padding: 0 4px;
                        margin-top: -15px;
                        background-color: white;
                    }
                """)
                cur_box_form = QFormLayout()
                cur_box_form.setHorizontalSpacing(5)
                cur_box_form.setVerticalSpacing(10)
                cur_box_form.setContentsMargins(10, 10, 10, 10)
                cur_box_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
                cur_box_form.setAlignment(Qt.AlignmentFlag.AlignRight)

            elif type == TYPE_COMBOBOX or type ==TYPE_COMBOBOX_CUSTOMIZED:
                # Use monospace font for the label
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")

                right = NoScrollComboBox()
                right.setObjectName(field[0])
                apply_field_style(right)
                option_list = field[3]
                right.addItems(option_list)

                cur_box_form.addRow(left, right_aligned_widget(right))
            
            elif type == TYPE_IMAGE:
                left = ""
                right = QLabel()
                right.setFixedWidth(90)
                right.setFixedHeight(90)
                right.setObjectName(field[0])
                right.setScaledContents(True)
                pixmap = QPixmap(field[3])
                right.setPixmap(pixmap)
                right.setAlignment(Qt.AlignmentFlag.AlignLeft)
                cur_box_form.addRow(left, left_aligned_widget(right))
            
            elif type == TYPE_TEXTBOX:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")
                
                right = QLineEdit()
                apply_field_style(right)
                right.setObjectName(field[0])
                right.setEnabled(True if field[4] else False)
                if field[5] != 'No Validator':
                    right.setValidator(self.get_validator(field[5]))
                cur_box_form.addRow(left, right_aligned_widget(right))
            
            if index == len(field_list):
                # Last Data tupple
                # Must add group_box with form
                current_group.setLayout(cur_box_form)
                group_container_layout.addWidget(current_group)

        group_container_layout.addStretch()
        scroll_area.setWidget(group_container)

        ###############################
        # Customized option in Combobox
        ###############################
        """
        This routine takes both customized_input list and input_value_changed list.
        Customized input list is the list displayed in popup, when "Customized" option is clicked.
        input_value_Changed is the list of keys whose values depend on values of other keys in input dock.
        The function which returns customized_input values takes no arguments.
        But if a key is common in both customized input and input value changed, it takes argument as specified in
         input value changed.
        Here, on_change_key_popup gives list of keys which are common in both and needs an input argument.
        Since, we don't know how may customized popups can be used in a module we have provided,
         "triggered.connect" for up to 10 customized popups
        """
        print("\n\n\n",self.backend,"$$$$",self.backend.customized_input,self.backend.input_value_changed)
        new_list = self.backend.customized_input()
        updated_list = self.backend.input_value_changed()

        print(f'\n ui_template.py input_value_changed {updated_list} \n new_list {new_list}')
        data = {}

        d = {}
        if new_list != []:
            for t in new_list:
                Combobox_key = t[0]
                disabled_values = []
                if len(t) == 4:
                    disabled_values = t[2]
                d[Combobox_key] = self.input_widget.findChild(QWidget, t[0])
                if updated_list != None:
                    onchange_key_popup = [item for item in updated_list if item[1] == t[0] and item[2] == TYPE_COMBOBOX_CUSTOMIZED]
                    arg_list = []
                    if onchange_key_popup != []:
                        for change_key in onchange_key_popup[0][0]:
                            print(change_key)
                            arg_list.append(self.input_widget.findChild(QWidget, change_key).currentText())
                        data[t[0] + "_customized"] = [all_values_available for all_values_available in
                                                      t[1](arg_list) if all_values_available not in disabled_values]
                    else:
                        data[t[0] + "_customized"] = [all_values_available for all_values_available in t[1]()
                                                      if all_values_available not in disabled_values]
                else:
                    data[t[0] + "_customized"] = [all_values_available for all_values_available in t[1]()
                                                  if all_values_available not in disabled_values]
            try:
                print(f"<class 'AttributeError'>: {d} \n {new_list}")

                #changed this code bcz an error was occuring in the code -t.s.
                # Connect signals only for widgets that exist
                for i in range(11):  # We were trying to connect 11 items before
                    if i < len(new_list):
                        widget = d.get(new_list[i][0])
                        if widget is not None and hasattr(widget, 'activated'):
                            widget.activated.connect(lambda checked, w=widget: self.popup(w, new_list, updated_list, data))
            except Exception as e:
                print(f"Error connecting signals: {str(e)}")
                # changed ended here -t.s.
                pass

        # Change in Ui based on Connectivity selection
        ##############################################

        print("\n\n\n*****")
        self.print_widget_tree(group_container)
        if updated_list is not None:
            for t in updated_list:
                for key_name in t[0]:
                    key_changed = self.input_widget.findChild(QWidget, key_name)
                    print(f"~~finding {key_name} get {key_changed} object {key_changed.objectName()}")
                    self.on_change_connect(key_changed, updated_list, data, self.backend)                    
                    print(f"key_name{key_name} \n key_changed{key_changed}  \n self.on_change_connect ")

        panel_layout.addWidget(scroll_area)

        # --- Bottom Design Button (fixed inside scroll area) ---
        btn_button_layout = QHBoxLayout()
        btn_button_layout.setContentsMargins(0, 20, 0, 0)
        btn_button_layout.addStretch(2)

        save_input_btn = CustomButton("       Save Input        ", ":/vectors/save.svg")
        save_input_btn.clicked.connect(lambda: self.parent.common_function_for_save_and_design(self.backend, data, "Save"))
        btn_button_layout.addWidget(save_input_btn)
        btn_button_layout.addStretch(1)

        design_btn = CustomButton("        Design           ", ":/vectors/design.svg")
        design_btn.clicked.connect(lambda: self.parent.start_thread(data))
        btn_button_layout.addWidget(design_btn)
        btn_button_layout.addStretch(2)

        panel_layout.addLayout(btn_button_layout)

        # --- Horizontal scroll area for all right content ---
        h_scroll_area = QScrollArea()
        h_scroll_area.setWidgetResizable(True)
        h_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        h_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        h_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:horizontal {
                background: #E0E0E0;
                height: 8px;
                margin: 3px 0px 0px 0px;
                border-radius: 2px;
            }
            QScrollBar::handle:horizontal {
                background: #A0A0A0;
                min-width: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #707070;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        h_scroll_area.setWidget(self.left_panel)

        left_layout.addWidget(h_scroll_area)

    def print_widget_tree(self, widget: QWidget, indent: int=0):
        prefix = "  " * (indent*4)
        print(f"{prefix}{widget.objectName()}({widget.__class__.__name__})")
        for child in widget.children():
            if isinstance(child, QWidget):
                self.print_widget_tree(child, indent+1)

    def popup(self,key, for_custom_list,updated_list,data):

        """
        Function for retaining the values in the popup once it is closed.
        """

        for c_tup in for_custom_list:
            if c_tup[0] != key.objectName():
                continue
            selected = key.currentText()
            f = c_tup[1]
            disabled_values = []
            note = ""
            if updated_list != None:
                onchange_key_popup = [item for item in updated_list if item[1] == c_tup[0] and item[2] == TYPE_COMBOBOX_CUSTOMIZED]
            else:
                onchange_key_popup = []
            if onchange_key_popup != []:
                arg_list = []
                for change_key in onchange_key_popup[0][0]:
                    arg_list.append(
                        self.input_widget.findChild(QWidget, change_key).currentText())
                options = f(arg_list)
                existing_options = data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    if len(c_tup) == 4:
                        disabled_values = c_tup[2]
                        note = c_tup[3]
                    data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options,
                                                                                disabled_values, note)
                    if data[c_tup[0] + "_customized"] == []:
                        # data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f(arg_list)
                        #                                   if all_values_available not in disabled_values]
                        data[c_tup[0] + "_customized"] = options
                        key.setCurrentIndex(0)
                else:
                    # data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f(arg_list)
                    #                                   if all_values_available not in disabled_values]
                    data[c_tup[0] + "_customized"] = options

                    # input = f(arg_list)
                    # data[c_tup[0] + "_customized"] = input
            else:
                options = f()
                existing_options = data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    if len(c_tup) == 4:
                        disabled_values = c_tup[2]
                        note = c_tup[3]
                    data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options,
                                                                                disabled_values, note)
                    if data[c_tup[0] + "_customized"] == []:
                        # data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f()
                        #                               if all_values_available not in disabled_values]
                        data[c_tup[0] + "_customized"] = options
                        key.setCurrentIndex(0)
                else:
                    # data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f()
                    #                                   if all_values_available not in disabled_values]
                    data[c_tup[0] + "_customized"] = options

    def open_customized_popup(self, op, KEYEXISTING_CUSTOMIZED, disabled_values=None, note=""):
        """
        Function to connect the customized_popup with the ui_template file
        on clicking the customized option
        """
        if disabled_values is None:
            disabled_values = []
        self.window = QDialog()
        self.ui = Ui_Popup()
        self.ui.setupUi(self.window, disabled_values, note)
        self.ui.addAvailableItems(op, KEYEXISTING_CUSTOMIZED)
        self.window.exec()
        return self.ui.get_right_elements()

    def on_change_connect(self, key_changed, updated_list, data, backend):
        key_changed.currentIndexChanged.connect(lambda: self.change(key_changed, updated_list, data, backend))

    # To update the label and combobox if Connectivity
    def change(self, k1, new, data, main):
        print(f"$${new}")
        for tup in new:
            (object_name, k2_key, typ, f) = tup
            print(f"\n object_name:{object_name}")
            print(f"\n k1:{k1}")
            print(f"\n f: {f}")
            print(f"\n k1.objectName():{k1.objectName()}")
            print(f"\n k2_key:{k2_key}")
            print(f"\n typ:{typ}")
            print(f"\n type:{typ}")
            if k1.objectName() not in object_name:
                continue
            if typ in [TYPE_LABEL, TYPE_OUT_LABEL]:
                k2_key = k2_key + "_label"
            if typ == TYPE_NOTE:
                k2_key = k2_key + "_note"

            if typ in [TYPE_OUT_DOCK, TYPE_OUT_LABEL]:
                k2 = self.input_widget.findChild(QWidget, k2_key)
            elif typ == TYPE_WARNING:
                k2 = str(k2_key)
            else:
                k2 = self.input_widget.findChild(QWidget, k2_key)


            arg_list = []
            for ob_name in object_name:
                key = self.input_widget.findChild(QWidget, ob_name)
                arg_list.append(key.currentText())

            val = f(arg_list)
            print(f"\n k2:{k2}")
            print(f"\n val:{val}")
            if typ == TYPE_COMBOBOX:
                print("\n\nCombo")
                k2.clear()
                for values in val:
                    k2.addItem(values)
                    k2.setCurrentIndex(0)
                if VALUES_WELD_TYPE[1] in val:
                    k2.setCurrentText(VALUES_WELD_TYPE[1])
                if k2_key in RED_LIST:
                    red_list_set = set(red_list_function())
                    current_list_set = set(val)
                    current_red_list = list(current_list_set.intersection(red_list_set))
                    for value in current_red_list:
                        indx = val.index(str(value))
                        k2.setItemData(indx, QBrush(QColor("red")), Qt.ForegroundRole)
            elif typ == TYPE_COMBOBOX_CUSTOMIZED:
                print("\n\nCust_Combo")
                k2.setCurrentIndex(0)
                data[k2_key + "_customized"] = val
            elif typ == TYPE_CUSTOM_MATERIAL:
                print("\n\nCust_Combo_material")
                if val:
                    self.new_material_dialog()
            elif typ == TYPE_CUSTOM_SECTION:
                if val:
                    self.import_custom_section()

            elif typ == TYPE_LABEL:
                print("\n\nLabel")
                k2.setText(val)
            elif typ == TYPE_NOTE:
                print("\n\nNote")
                k2.setText(val)
            elif typ == TYPE_IMAGE:
                print("\n\nImg")
                pixmap1 = QPixmap(val)
                k2.setPixmap(pixmap1)
            elif typ == TYPE_TEXTBOX:
                print("\n\ntext")
                if val:
                    k2.setEnabled(True)
                else:
                    k2.setDisabled(True)
                    k2.setText("")
            elif typ == TYPE_COMBOBOX_FREEZE:
                print("\n\nfreeze_Combo")
                if val:
                    k2.setEnabled(False)
                else:
                    k2.setEnabled(True)
            elif typ == TYPE_WARNING:
                print("\n\nwarning")
                if val:
                    QMessageBox.warning(self, "Application", k2)
            elif typ in [TYPE_OUT_DOCK, TYPE_OUT_LABEL]:
                print("\n\nlast")
                if val:
                    k2.setVisible(False)
                else:
                    k2.setVisible(True)


    def toggle_input_dock(self):
        parent = self.parent
        if hasattr(parent, 'toggle_animate'):
            is_collapsing = self.width() > 0
            parent.toggle_animate(show=not is_collapsing, dock='input')
        
        self.toggle_btn.setText("❯" if is_collapsing else "❮")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

    def new_material_dialog(self):
        dialog = QDialog(self)
        self.material_popup_message = ''
        self.invalid_field = ''
        dialog.setWindowTitle('Custom Material')
        layout = QGridLayout(dialog)
        # Center the content by adding side stretch columns and margins
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setHorizontalSpacing(6)
        layout.setVerticalSpacing(12)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(3, 1)
        widget = QWidget(dialog)
        widget.setLayout(layout)
        dialog.setStyleSheet("""
            QDialog, QWidget {
                background-color: #ffffff;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                padding: 2px 4px;
                selection-background-color: #3875d6;
                selection-border-color: #90af13;
            }
            QPushButton {
                background-color: #90af13;
                color: #000000;
                padding: 4px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5e7407;
            }
            QPushButton:pressed {
                background-color: #7d9710;
            }
            """)
        _translate = QCoreApplication.translate
        textbox_list = ['Grade', 'Fy_20', 'Fy_20_40', 'Fy_40', 'Fu']
        event_function = ['', self.material_popup_fy_20_event, self.material_popup_fy_20_40_event,
                          self.material_popup_fy_40_event, self.material_popup_fu_event]
        self.original_focus_event_functions = {}

        i = 0
        for textbox_name in textbox_list:
            label = QLabel(widget)
            label.setObjectName(textbox_name+"_label")
            label.setText(_translate("MainWindow", "<html><body><p>" + textbox_name + "</p></body></html>"))
            label.setFixedSize(100, 30)
            layout.addWidget(label, i, 1, 1, 1)

            textbox = QLineEdit(widget)
            textbox.setObjectName(textbox_name)
            textbox.setFixedSize(200, 24)
            if textbox_name == 'Grade':
                textbox.setReadOnly(True)
                textbox.setText("Cus____")
            else:
                textbox.setValidator(QIntValidator())
                # textbox.mousePressEvent = event_function[textbox_list.index(textbox_name)]
                self.original_focus_event_functions.update({textbox_name: textbox.focusOutEvent})
                textbox.focusOutEvent = event_function[textbox_list.index(textbox_name)]

            self.connect_change_popup_material(textbox, widget)
            layout.addWidget(textbox, i, 2, 1, 1)

            i += 1

        add_button = QPushButton(widget)
        add_button.setObjectName("material_add")
        add_button.setText("Add")
        add_button.clicked.connect(lambda: self.update_material_db_validation(widget))
        layout.addWidget(add_button, i, 1, 1, 2)

        dialog.setFixedSize(350, 250)
        closed = dialog.exec()
        if closed is not None:
            input_dock_material = self.input_widget.findChild(QWidget, KEY_MATERIAL)
            input_dock_material.clear()
            for item in connectdb("Material"):
                input_dock_material.addItem(item)
            input_dock_material.setCurrentIndex(1)

    def material_popup_fy_20_event(self, e):
        self.original_focus_event_functions['Fy_20'](e)
        if self.invalid_field == 'Fy_20':
            self.show_material_popup_message()

    def material_popup_fy_20_40_event(self, e):
        self.original_focus_event_functions['Fy_20_40'](e)
        if self.invalid_field == 'Fy_20_40':
            self.show_material_popup_message()

    def material_popup_fy_40_event(self, e):
        self.original_focus_event_functions['Fy_40'](e)
        if self.invalid_field == 'Fy_40':
            self.show_material_popup_message()

    def material_popup_fu_event(self, e):
        self.original_focus_event_functions['Fu'](e)
        if self.invalid_field == 'Fu':
            self.show_material_popup_message()

    def connect_change_popup_material(self, textbox, widget):
        if textbox.objectName() != 'Grade':
            textbox.textChanged.connect(lambda: self.change_popup_material(widget))

    def change_popup_material(self, widget):

        grade = widget.findChild(QLineEdit, 'Grade')
        fy_20 = widget.findChild(QLineEdit, 'Fy_20').text()
        fy_20_40 = widget.findChild(QLineEdit, 'Fy_20_40').text()
        fy_40 = widget.findChild(QLineEdit, 'Fy_40').text()
        fu = widget.findChild(QLineEdit, 'Fu').text()

        material = str("Cus_"+fy_20+"_"+fy_20_40+"_"+fy_40+"_"+fu)
        material_validator = MaterialValidator(material)
        if not material_validator.is_valid_custom():
            if str(material_validator.invalid_value):
                self.material_popup_message = "Please select "+str(material_validator.invalid_value)+" in valid range!"
                self.invalid_field = str(material_validator.invalid_value)
            else:
                self.material_popup_message = ''
                self.invalid_field = ''
        else:
            self.material_popup_message = ''
            self.invalid_field = ''
        grade.setText(material)

    def update_material_db_validation(self, widget):

        material = widget.findChild(QLineEdit, 'Grade').text()

        material_validator = MaterialValidator(material)
        if material_validator.is_already_in_db():
            QMessageBox.about(QMessageBox(), "Information", "Material already exists in Database!")
            return
        elif not material_validator.is_format_custom():
            QMessageBox.about(QMessageBox(), "Information", "Please fill all missing parameters!")
            return
        elif not material_validator.is_valid_custom():
            QMessageBox.about(QMessageBox(), "Information", "Please select "+str(material_validator.invalid_value)+" in valid range!")
            return

        self.update_material_db(grade=material, material=material_validator)
        QMessageBox.information(QMessageBox(), 'Information', 'Data is added successfully to the database.')

    def update_material_db(self, grade, material):

        fy_20 = int(material.fy_20)
        fy_20_40 = int(material.fy_20_40)
        fy_40 = int(material.fy_40)
        fu = int(material.fu)
        elongation = 0

        if fy_20 > 350:
            elongation = 20
        elif 250 < fy_20 <= 350:
            elongation = 22
        elif fy_20 <= 250:
            elongation = 23

        conn = sqlite3.connect(PATH_TO_DATABASE)
        c = conn.cursor()
        c.execute('''INSERT INTO Material (Grade,[Yield Stress (< 20)],[Yield Stress (20 -40)],
        [Yield Stress (> 40)],[Ultimate Tensile Stress],[Elongation ]) VALUES (?,?,?,?,?,?)''',
                  (grade, fy_20, fy_20_40, fy_40, fu, elongation))
        conn.commit()
        c.close()
        conn.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Checking hasattr is only meant to prevent errors,
        # while standalone testing of this widget
        if self.parent and hasattr(self.parent, 'parent') and self.parent.parent:
            if self.width() == 0:
                if hasattr(self.parent.parent, 'update_docking_icons'):
                    self.parent.parent.update_docking_icons(input_is_active=False)
                if hasattr(self.parent, 'update_input_label_state'):
                    self.parent.update_input_label_state(True)
            elif self.width() > 0:
                if hasattr(self.parent.parent, 'update_docking_icons'):
                    self.parent.parent.update_docking_icons(input_is_active=True)
                if hasattr(self.parent, 'update_input_label_state'):
                    self.parent.update_input_label_state(False)

#----------------Standalone-Test-Code--------------------------------
from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("border: none")

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.main_h_layout.addWidget(InputDock(backend=FinPlateConnection ,parent=self),15)

        self.main_h_layout.addStretch(40)

        self.setWindowState(Qt.WindowMaximized)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec()) 