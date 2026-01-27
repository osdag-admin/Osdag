"""
Input dock widget for Osdag GUI.
Handles user input forms and group boxes for connection design.
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QToolTip,
    QComboBox, QScrollArea, QLabel, QFormLayout, QLineEdit, QGroupBox, QSizePolicy
)
from PySide6.QtWidgets import QMessageBox, QDialog, QGridLayout, QListView
from PySide6.QtCore import Qt, QRegularExpression, QCoreApplication, QEvent, QTimer, QPoint
from PySide6.QtGui import (QPixmap, QBrush, QColor, QDoubleValidator,
        QRegularExpressionValidator, QIntValidator, QIcon)
from osdag_gui.OS_safety_protocols import get_cleanup_coordinator

from osdag_gui.ui.components.additional_inputs_button import AdditionalInputsButton
from osdag_gui.ui.components.custom_buttons import DockCustomButton
import osdag_gui.resources.resources_rc
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
from osdag_gui.ui.components.dialogs.customized_popup import CustomValueSelectPopup
from osdag_gui.ui.components.dialogs.custom_titlebar import CustomTitleBar
from osdag_gui.ui.components.dialogs.bounds_selector import BoundsSelectorDialog

from osdag_core.Common import *

class NoScrollComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        view = QListView(self)
        view.window().setWindowFlags(Qt.Popup)
        self.setView(view)

    def wheelEvent(self, event):
        event.ignore()

    def showPopup(self):
        super().showPopup()

        popup = self.view().window()

        # Global position below combo
        combo_pos = self.mapToGlobal(QPoint(0, self.height()))

        # Screen geometry where combo exists
        screen = QApplication.screenAt(combo_pos)
        if not screen:
            screen = QApplication.primaryScreen()

        available = screen.availableGeometry()

        # Max height till bottom of screen
        max_height = available.bottom() - combo_pos.y()

        # Apply constraints
        popup.move(combo_pos)
        popup.setMaximumHeight(max_height)

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

class InputDock(QWidget):
    def __init__(self, backend:object, parent):
        super().__init__()

        self.theme_manager = QApplication.instance().theme_manager
        # NOTE: Do NOT use WA_DeleteOnClose - it causes heap corruption (use-after-free)
        # when processEvents() is called during OpenGL rendering. Parent manages lifecycle.
        self.parent = parent
        # Already an Object created in template_page.py
        self.backend = backend
        self.input_widget = None

        self.setObjectName("input_dock")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.left_container = QWidget()
        self.original_width = int(self.width())

        # To connect input dock options with additional inputs
        input_dp_conn_list = self.backend.input_dictionary_without_design_pref()
        input_dp_conn_list = [i[0] for i in input_dp_conn_list if i[2] == "Input Dock"]
        print(f'input_dp_conn_list {input_dp_conn_list}')

        # Bring the data instance from `design_type` folder
        input_field_list = self.backend.input_values()
        # To equalize the label length
        # So that they are of equal size
        label_width, input_width = self.calc_max_width(input_field_list)

        self.build_left_panel(input_field_list, label_width, input_width, input_dp_conn_list)
        self.main_layout.addWidget(self.left_container)

        self.toggle_strip = QWidget()
        self.toggle_strip.setFixedWidth(6)
        self.toggle_strip.setObjectName("toggle_strip")
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("❮")
        self.toggle_btn.setObjectName("toggle_strip_button")
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setToolTip("Hide panel")
        self.toggle_btn.clicked.connect(self.toggle_input_dock)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        self.main_layout.addWidget(self.toggle_strip)
    
    # To equalize the size of label strings
    def calc_max_width(self, in_list):
        # Calculate maximum size
        max_label_len = 0
        max_input_len = 0
        for t in in_list:
            if t[2] in [TYPE_COMBOBOX, TYPE_COMBOBOX_FREEZE, TYPE_COMBOBOX_CUSTOMIZED, TYPE_TEXTBOX]:
                if isinstance(t[3], list):
                    # Check each Option
                    for option in t[3]:
                        if len(option) > max_input_len:
                            max_input_len = len(option)
                    
                # check size of simultaneous label
                if len(t[1]) > max_label_len:
                    max_label_len = len(t[1])
        
        # Width Calculation
        print(f"max_label: {max_label_len}\nmax_input: {max_input_len}")
        max_label_size = (max_label_len * 6) + 10
        max_input_size = (max_input_len * 6) + 20
        return max_label_size, max_input_size

    def get_validator(self, validator):
        if validator == 'Int Validator':
            return QRegularExpressionValidator(QRegularExpression(r"^(0|[1-9]\d*)(\.\d+)?$"))
        elif validator == 'Double Validator':
            return QDoubleValidator()
        else:
            return None
        
    def build_left_panel(self, field_list, label_width, input_width, input_dp_conn_list):
        print("\n","="*100,"\n\n")
        print("[INFO] Building Input Dock UI...")
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # --- Main Content Panel (to be scrolled horizontally and vertically) ---
        self.left_panel = QWidget()
        self.left_panel.setObjectName("inputs-leftpanel")
        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(5, 5, 5, 5)
        panel_layout.setSpacing(4)

        # --- Top Bar (fixed inside scroll area) ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        input_dock_btn = QPushButton("Basic Inputs")
        input_dock_btn.setObjectName("inputs_button")
        input_dock_btn.setCursor(Qt.CursorShape.ArrowCursor)
        input_dock_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(input_dock_btn)
        # additonal input button
        additional_inputs_btn = AdditionalInputsButton()
        additional_inputs_btn.clicked.connect(lambda: self.parent.common_function_for_save_and_design(self.backend, self.data, "Design_Pref"))
        additional_inputs_btn.clicked.connect(lambda: self.parent.combined_design_prefer(self.data, self.backend))
        additional_inputs_btn.clicked.connect(lambda: self.parent.design_preferences())
        additional_inputs_btn.setToolTip("Additional Inputs")
        additional_inputs_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_bar.addWidget(additional_inputs_btn)
        # lock-unlock button
        self.state_locked = False    # Open by default
        self.lock_btn = QPushButton()
        self.lock_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lock_btn.setObjectName("lock_btn")
        self.lock_btn.setCheckable(True)
        self.lock_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lock_btn.clicked.connect(self.toggle_lock)
        top_bar.addWidget(self.lock_btn)
        panel_layout.addLayout(top_bar)

        #-Lock-ToolTip--------------------------------------
        self.lock_btn_tooltp = QLabel("🔒Unlock to Edit")
        self.lock_btn_tooltp.setObjectName("lock_btn_tooltip")
        self.lock_btn_tooltp.setWindowFlags(Qt.ToolTip)
        self.lock_btn_tooltp.hide()
        #--------------------------------------------------

        # Vertical scroll area for group boxes (vertical only)
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("inputs_vscrollarea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.installEventFilter(self)

        group_container = QWidget()
        self.input_widget = group_container
        self.input_widget.setObjectName("inputs_container")
        group_container_layout = QVBoxLayout(group_container)

        # --- Main Content (group boxes) ---

        # Track any group is active or not
        track_group = False
        index = 0
        for field in field_list:
            index += 1
            label = field[1]
            type = field[2]
            # print(f"[INFO] Option:{field}")
            if type == TYPE_MODULE:
                # No use of module title will see.
                pass
            elif type == TYPE_TITLE:
                if track_group:
                    current_group.setLayout(cur_box_form)
                    group_container_layout.addWidget(current_group)
                    track_group = False

                # Check if the next field is also a title
                next_is_title = (
                    index < len(field_list) and
                    field_list[index][2] == TYPE_TITLE
                )

                if next_is_title:
                    # First of two consecutive titles → label only
                    title = QLabel(label)
                    title.setObjectName("no_group_title")
                    group_container_layout.addWidget(title)
                    continue
                
                # Initialized the group box for current title
                current_group = QGroupBox(label)
                # print(f"[INFO] Group_box: {label}")
                current_group.setObjectName(label + "_group")
                track_group = True
                cur_box_form = QFormLayout()
                cur_box_form.setHorizontalSpacing(5)
                cur_box_form.setVerticalSpacing(10)
                cur_box_form.setContentsMargins(10, 10, 10, 10)
                cur_box_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
                cur_box_form.setAlignment(Qt.AlignmentFlag.AlignRight)

            elif type == TYPE_COMBOBOX or type == TYPE_COMBOBOX_CUSTOMIZED:
                # Use monospace font for the label
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setMinimumWidth(label_width)

                right = NoScrollComboBox()
                right.setMinimumWidth(input_width)
                right.setObjectName(field[0])
                right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                option_list = field[3]
                right.addItems(option_list)

                # additonal input connector
                if field[0] in input_dp_conn_list:
                    self.parent.input_dp_connection(right)

                # To disable option at index [1, 2] in Connectivity Combo of Beam to Beam End Plate
                if len(field) == 7:
                    for disabled in field[6]:
                        right.model().item(disabled).setEnabled(False)

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
            
            # For Some Compression Member Images
            elif type == TYPE_IMAGE_COMPRESSION:
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
                left.setMinimumWidth(label_width)

                right = QLineEdit()
                right.setMinimumWidth(input_width)
                right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                right.setObjectName(field[0])
                right.setEnabled(True if field[4] else False)
                if field[5] != 'No Validator':
                    right.setValidator(self.get_validator(field[5]))
                cur_box_form.addRow(left, right_aligned_widget(right))
                
                # additonal input connector
                if field[0] in input_dp_conn_list:
                    self.parent.input_dp_connection(right)

            # For Base Plate
            elif type == TYPE_NOTE:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setMinimumWidth(label_width)

                right = QLineEdit()
                right.setText(field[3])
                right.setMinimumWidth(input_width)
                right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                right.setObjectName(field[0] + "_note")
                right.setAlignment(Qt.AlignmentFlag.AlignLeft)
                right.setDisabled(True)
                cur_box_form.addRow(left, right_aligned_widget(right))
            
            if index == len(field_list):
                # Last Data tupple
                # Must add group_box with form
                current_group.setLayout(cur_box_form)
                group_container_layout.addWidget(current_group)

        group_container_layout.addStretch()
        self.scroll_area.setWidget(group_container)

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
        # print("\n\n\n [INFO] ",self.backend,"\n\n",self.backend.customized_input,self.backend.input_value_changed)
        new_list = self.backend.customized_input()
        updated_list = self.backend.input_value_changed()

        # print(f'\n [INFO] ui_template.py input_value_changed {updated_list} \n new_list {new_list}')
        self.data = {}

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
                            # print(f"[INFO] Change key: {change_key}")
                            arg_list.append(self.input_widget.findChild(QWidget, change_key).currentText())
                        self.data[t[0] + "_customized"] = [all_values_available for all_values_available in
                                                      t[1](arg_list) if all_values_available not in disabled_values]
                    else:
                        self.data[t[0] + "_customized"] = [all_values_available for all_values_available in t[1]()
                                                      if all_values_available not in disabled_values]
                else:
                    self.data[t[0] + "_customized"] = [all_values_available for all_values_available in t[1]()
                                                  if all_values_available not in disabled_values]
            try:
                print(f"New_List: {d} \n {new_list}")

                #changed this code bcz an error was occuring in the code -t.s.
                # Connect signals only for widgets that exist
                for i in range(11):  # We were trying to connect 11 items before
                    if i < len(new_list):
                        widget = d.get(new_list[i][0])
                        if widget is not None and hasattr(widget, 'activated'):
                            widget.activated.connect(lambda checked, w=widget: self.popup(w, new_list, updated_list, self.data))
            except Exception as e:
                print(f"[ERROR] Error connecting signals: {str(e)}")
                # changed ended here -t.s.
                pass

        # Change in Ui based on Connectivity selection
        ##############################################

        print("\n\n\n","="*100)
        self.print_widget_tree(group_container)
        if updated_list is not None:
            for t in updated_list:
                for key_name in t[0]:
                    key_changed = self.input_widget.findChild(QWidget, key_name)
                    self.on_change_connect(key_changed, updated_list, self.data, self.backend)                    
                    # print(f"[INFO] key_name{key_name} \n key_changed{key_changed}  \n self.on_change_connect ")

        panel_layout.addWidget(self.scroll_area)

        # --- Bottom Design Button (fixed inside scroll area) ---
        btn_button_layout = QHBoxLayout()
        btn_button_layout.setContentsMargins(0, 20, 0, 0)
        btn_button_layout.addStretch(2)

        save_input_btn = DockCustomButton("       Save Input        ", ":/vectors/save.svg")
        save_input_btn.clicked.connect(lambda: self.parent.common_function_for_save_and_design(self.backend, self.data, "Save_OSI"))
        btn_button_layout.addWidget(save_input_btn)
        btn_button_layout.addStretch(1)

        design_btn = DockCustomButton("        Design           ", ":/vectors/design.svg")
        design_btn.clicked.connect(lambda: self.parent.start_thread(self.data))
        btn_button_layout.addWidget(design_btn)
        btn_button_layout.addStretch(2)

        panel_layout.addLayout(btn_button_layout)

        # --- Horizontal scroll area for all right content ---
        h_scroll_area = QScrollArea()
        h_scroll_area.setWidgetResizable(True)
        h_scroll_area.setObjectName("inputs_hscrollarea")
        h_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        h_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        h_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_scroll_area.setWidget(self.left_panel)

        left_layout.addWidget(self.left_panel)

    #-Lock-Tooltip-Events-Starts-------------------------------------------------------------------------
    def eventFilter(self, obj, event):
        # Check if it's the scroll area and it's a mouse press
        if obj.objectName() == "inputs_vscrollarea" and event.type() == QEvent.MouseButtonPress:
            if self.state_locked:
                self.show_lock_tooltip()
            return True  # Block the event
        return super().eventFilter(obj, event)
    
    def clear_force_hover(self):
        self.lock_btn.setProperty("forceHover", False)
        self.lock_btn.style().polish(self.lock_btn)
        self.lock_btn.update()

    def show_lock_tooltip(self):
        # Stop any existing timer first
        if hasattr(self, 'tooltip_timer') and self.tooltip_timer.isActive():
            self.tooltip_timer.stop()
        
        # Position tooltip to the right of the lock button
        lock_global_pos = self.lock_btn.mapToGlobal(self.lock_btn.rect().topRight())
        tooltip_pos = lock_global_pos + QPoint(5, 0)
        self.lock_btn.setProperty("forceHover", True)
        self.lock_btn.style().polish(self.lock_btn)
        self.lock_btn.update()
                
        # Adjust size and position
        self.lock_btn_tooltp.adjustSize()
        self.lock_btn_tooltp.move(tooltip_pos)
        self.lock_btn_tooltp.show()
        self.lock_btn_tooltp.raise_()
        
        # Hide after 3 seconds
        if not hasattr(self, 'tooltip_timer'):
            self.tooltip_timer = QTimer()
            self.tooltip_timer.setSingleShot(True)
            self.tooltip_timer.timeout.connect(self.lock_btn_tooltp.hide)
            self.tooltip_timer.timeout.connect(self.clear_force_hover)
        
        self.tooltip_timer.start(3000)
    
    def toggle_lock(self, set_locked_state=False):
        if set_locked_state:
            self.state_locked = True
            self.lock_btn.setChecked(True)
            self.input_widget.setDisabled(True)
            self.update_lock_icon()
        else:
            if self.state_locked:
                # Use CleanupCoordinator for redesign cleanup
                coordinator = get_cleanup_coordinator()
                coordinator.cleanup_for_redesign(self.parent)
            self.state_locked = not self.state_locked
            self.lock_btn.setChecked(self.state_locked)
            self.input_widget.setDisabled(self.state_locked)
            self.update_lock_icon()

    def update_lock_icon(self):
        if self.state_locked:
            icon_name = "lock_close"
        else:
            icon_name = "lock_open"
        
        if self.theme_manager.is_light():
            self.lock_btn.setIcon(QIcon(f":/vectors/{icon_name}_light.svg"))
        else:
            self.lock_btn.setIcon(QIcon(f":/vectors/{icon_name}_dark.svg"))

    def paintEvent(self, event):
        self.update_lock_icon()
        return super().paintEvent(event)
    
    #-Lock-Tooltip-Events-Ends-------------------------------------------------------------------------

    # Used to print the widget tree for debugging
    def print_widget_tree(self, widget: QWidget, indent: int=0):
        prefix = "  " * (indent*4)
        # print(f"[INFO] {prefix}{widget.objectName()}({widget.__class__.__name__})")
        for child in widget.children():
            if isinstance(child, QWidget):
                self.print_widget_tree(child, indent+1)

    def popup(self, key, for_custom_list, updated_list, data):

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
                existing_options = self.data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    if len(c_tup) == 4:
                        disabled_values = c_tup[2]
                        note = c_tup[3]
                    self.data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options,
                                                                                disabled_values, note)
                    if self.data[c_tup[0] + "_customized"] == []:
                        # self.data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f(arg_list)
                        #                                   if all_values_available not in disabled_values]
                        self.data[c_tup[0] + "_customized"] = options
                        key.setCurrentIndex(0)
                else:
                    # self.data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f(arg_list)
                    #                                   if all_values_available not in disabled_values]
                    self.data[c_tup[0] + "_customized"] = options

                    # input = f(arg_list)
                    # self.data[c_tup[0] + "_customized"] = input
            else:
                options = f()
                existing_options = self.data[c_tup[0] + "_customized"]
                if selected == "Customized":
                    if len(c_tup) == 4:
                        disabled_values = c_tup[2]
                        note = c_tup[3]
                    self.data[c_tup[0] + "_customized"] = self.open_customized_popup(options, existing_options,
                                                                                disabled_values, note)
                    if self.data[c_tup[0] + "_customized"] == []:
                        # self.data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f()
                        #                               if all_values_available not in disabled_values]
                        self.data[c_tup[0] + "_customized"] = options
                        key.setCurrentIndex(0)
                else:
                    # self.data[c_tup[0] + "_customized"] = [all_values_available for all_values_available in f()
                    #                                   if all_values_available not in disabled_values]
                    self.data[c_tup[0] + "_customized"] = options

    def open_customized_popup(self, op, KEYEXISTING_CUSTOMIZED, disabled_values=None, note=""):
        """
        Function to connect the customized_popup with the ui_template file
        on clicking the customized option
        """
        if disabled_values is None:
            disabled_values = []
        self.window = QDialog(self)
        self.ui = CustomValueSelectPopup()
        self.ui.setupUi(self.window, disabled_values, note)
        self.ui.addAvailableItems(op, KEYEXISTING_CUSTOMIZED)
        self.window.exec()
        return self.ui.get_right_elements()

    def on_change_connect(self, key_changed, updated_list, data, backend):
        key_changed.currentIndexChanged.connect(lambda: self.change(key_changed, updated_list, self.data, backend))

    # To update the label and combobox if Connectivity
    def change(self, k1, new, data, main):
        for tup in new:
            (object_name, k2_key, typ, f) = tup
            # print(f"\n[INFO] object_name:{object_name}")
            # print(f"\n[INFO] k1:{k1}")
            # print(f"\n[INFO] f: {f}")
            # print(f"\n[INFO] k1.objectName():{k1.objectName()}")
            # print(f"\n[INFO] k2_key:{k2_key}")
            # print(f"\n[INFO] typ:{typ}")
            # print(f"\n[INFO] type:{typ}")
            if k1.objectName() not in object_name:
                continue
            if typ in [TYPE_LABEL, TYPE_OUT_LABEL]:
                k2_key = k2_key + "_label"
            if typ == TYPE_NOTE:
                k2_key = k2_key + "_note"
            if typ in [TYPE_OUT_DOCK, TYPE_OUT_LABEL]:
                k2 = self.parent.output_dock.output_widget.findChild(QWidget, k2_key)
            elif typ == TYPE_WARNING:
                k2 = str(k2_key)
            else:
                k2 = self.input_widget.findChild(QWidget, k2_key)

            arg_list = []
            for ob_name in object_name:
                key = self.input_widget.findChild(QWidget, ob_name)
                arg_list.append(key.currentText())

            val = f(arg_list)
            # print(f"\n[INFO] k2:{k2}")
            # print(f"\n[INFO] val:{val}")
            if typ == TYPE_COMBOBOX:
                # print("\n\n[INFO] Combo")
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
                # print("\n\n[INFO] Cust_Combo")
                k2.setCurrentIndex(0)
                self.data[k2_key + "_customized"] = val
            elif typ == TYPE_CUSTOM_MATERIAL:
                # print("\n\n[INFO] Cust_Combo_material")
                if val:
                    self.new_material_dialog()
            elif typ == TYPE_CUSTOM_SECTION:
                if val:
                    self.import_custom_section()

            elif typ == TYPE_LABEL:
                # print("\n\n[INFO] Label")
                k2.setText(val)
            elif typ == TYPE_NOTE:
                # print("\n\n[INFO] Note")
                k2.setText(val)
            elif typ == TYPE_IMAGE:
                # print("\n\n[INFO] Img")
                if val is None:
                    # To handle NoneType error
                    continue
                pixmap1 = QPixmap(val)
                k2.setPixmap(pixmap1)

            elif typ == TYPE_TEXTBOX:
                # print("\n\n[INFO] text")
                # Trigger to launch Bounds Button for Plate-Girder Module
                if main.module_name() == KEY_PLATE_GIRDER_MAIN_MODULE:
                    w = self.get_current_widget_in_layout(k2_key)
                    if not val and isinstance(w, QLineEdit):  # Show optimization button
                        self.change_text_to_bound_btn(w, tup)
                    elif val and isinstance(w, QPushButton):  # Show textbox for customized input
                        self.change_bound_btn_to_text(w, tup)
                else:
                    if val:
                        k2.setEnabled(True)
                    else: 
                        k2.setText("")
                        k2.setDisabled(True)

            elif typ == TYPE_COMBOBOX_FREEZE:
                # print("\n\n[INFO] freeze_Combo")
                if val:
                    k2.setEnabled(False)
                else:
                    k2.setEnabled(True)
            elif typ == TYPE_WARNING:
                # print("\n\n[INFO] warning")
                if val:
                    CustomMessageBox(
                        title="Application",
                        text=k2,
                        dialogType=MessageBoxType.Warning
                    ).exec()
            elif typ in [TYPE_OUT_DOCK, TYPE_OUT_LABEL]:
                # print(f"\n[INFO] {tup}")
                if val:
                    k2.setVisible(False)
                else:
                    k2.setVisible(True)

    # For Plate-Girder Module-Functions-starts----------------------------------------------------
    def change_text_to_bound_btn(self, old_widget, tupple):
        layout = old_widget.parentWidget().layout()
        if layout is None:
            print(f"[ERROR]: Widget layout not Found for {tupple[1]}")
            return None

        index = layout.indexOf(old_widget)
        if index == -1:
            print(f"[ERROR]: Widget not found for {tupple[1]}")
            return None

        # Create or retrieve button
        if self.backend.bound_widgets.get(tupple[1], ""):
            btn = self.backend.bound_widgets.get(tupple[1])[1]
            # print(f"[INFO] Reusing existing button for {tupple[1]}")
        else:
            # Bounds Button
            btn = QPushButton("Set Bounds")
            btn.clicked.connect(lambda checked=False, name=tupple[1]: self.choose_bounds(name))
            self.backend.bound_widgets[tupple[1]] = [old_widget, btn]
            # print(f"[INFO] Created new button for {tupple[1]}")
        
        btn.setObjectName(tupple[1])
        layout.replaceWidget(old_widget, btn)
        old_widget.hide()  # Hide the old widget
        btn.show()  # Show the button
    
    def change_bound_btn_to_text(self, old_widget, tupple):
        layout = old_widget.parentWidget().layout()
        if layout is None:
            print(f"[ERROR]: Widget layout not Found for {tupple[1]}")
            return None

        index = layout.indexOf(old_widget)
        if index == -1:
            print(f"[ERROR]: Widget not found for {tupple[1]}")
            return None

        # Retrieve or create textbox
        if self.backend.bound_widgets.get(tupple[1], ""):
            text_box = self.backend.bound_widgets.get(tupple[1])[0]
            # print(f"[INFO] Reusing existing LineEdit for {tupple[1]}")
        else:
            # print(f"[INFO] Creating new LineEdit for {tupple[1]}")
            inputs = self.backend.input_values()
            data_tup = None
            for tup in inputs:
                if tup[0] == tupple[1]:
                    data_tup = tup
                    break
            
            text_box = QLineEdit()
            text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            if data_tup and data_tup[5] != 'No Validator':
                text_box.setValidator(self.get_validator(data_tup[5]))
            self.backend.bound_widgets[tupple[1]] = [text_box, old_widget]
        
        text_box.setObjectName(tupple[1])    
        layout.replaceWidget(old_widget, text_box)
        old_widget.hide()  # Hide the button
        text_box.show()  # Show the textbox

    def get_current_widget_in_layout(self, widget_name):
        """Find the actual widget currently in the layout by objectName"""
        # Check if we have it stored in bound_widgets
        if widget_name in self.backend.bound_widgets:
            stored = self.backend.bound_widgets[widget_name]
            # Return whichever widget is currently visible/in layout
            text_box = stored[0]
            button = stored[1]
            
            # Check which one is actually in a layout
            if text_box.parentWidget() and text_box.parentWidget().layout():
                layout = text_box.parentWidget().layout()
                if layout.indexOf(text_box) != -1:
                    return text_box
            
            if button.parentWidget() and button.parentWidget().layout():
                layout = button.parentWidget().layout()
                if layout.indexOf(button) != -1:
                    return button

        return self.input_widget.findChild(QWidget, widget_name)

    def choose_bounds(self, name: str):
        bounds = None
        # Get default values
        if name == KEY_OVERALL_DEPTH_PG:
            bounds = self.backend.bounds_map.get('D')
        elif name == KEY_TOP_Bflange_PG:
            bounds = self.backend.bounds_map.get('bf_top')
        elif name == KEY_BOTTOM_Bflange_PG:
            bounds = self.backend.bounds_map.get('bf_bot')
        
        dialog = BoundsSelectorDialog(name.replace(".", " ") , default=[bounds[0], bounds[1], bounds[2]], parent=self)
        result = dialog.exec()
        
        if result:
            # print(f"[INFO] New bounds for {name}: Upper = {result[0]}, Lower = {result[1]}, Step = {result[2]}")
            # Update Bounds
            if name == KEY_OVERALL_DEPTH_PG:
                self.backend.bounds_map['D'] = (result[0], result[1], result[2])
            elif name == KEY_TOP_Bflange_PG:
                self.backend.bounds_map['bf_top'] = (result[0], result[1], result[2])
            elif name == KEY_BOTTOM_Bflange_PG:
                self.backend.bounds_map['bf_bot'] = (result[0], result[1], result[2]) 
        else:
            # print("[INFO] Dialog was cancelled")
            pass

    # For Plate-Girder Module-ends---------------------------------------------------  

    def toggle_input_dock(self):
        parent = self.parent
        if hasattr(parent, 'toggle_animate'):
            is_collapsing = self.width() > 0
            parent.toggle_animate(show=not is_collapsing, dock='input')
        
        self.toggle_btn.setText("❯" if is_collapsing else "❮")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

    def new_material_dialog(self):
        dialog = QDialog(self)
        dialog.setObjectName("custom_material_popup")
        dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        dialog.setAttribute(Qt.WA_StyledBackground, True)
        dialog.setModal(True)  # Make it modal to ensure it appears on top
        
        self.material_popup_message = ''
        self.invalid_field = ''
        
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(1, 1, 1, 1)
        central_layout.setSpacing(0)
        
        # Create custom title bar
        title_bar = CustomTitleBar(parent=dialog)
        title_bar.setTitle('Custom Material')
        
        # Connect close button if CustomTitleBar has one
        if hasattr(title_bar, 'close_button'):
            title_bar.close_button.clicked.connect(dialog.close)
        
        central_layout.addWidget(title_bar)
        
        # Create main content widget
        content_widget = QWidget()
        content_layout = QGridLayout()
        
        # Center the content by adding side stretch columns and margins
        content_layout.setContentsMargins(20, 10, 20, 10)
        content_layout.setHorizontalSpacing(6)
        content_layout.setVerticalSpacing(12)
        content_layout.setColumnStretch(0, 1)
        content_layout.setColumnStretch(3, 1)
        content_widget.setLayout(content_layout)
        
        _translate = QCoreApplication.translate
        textbox_list = ['Grade', 'Fy_20', 'Fy_20_40', 'Fy_40', 'Fu']
        event_function = ['', self.material_popup_fy_20_event, self.material_popup_fy_20_40_event,
                        self.material_popup_fy_40_event, self.material_popup_fu_event]
        self.original_focus_event_functions = {}
        
        # Create form fields
        for i, textbox_name in enumerate(textbox_list):
            label = QLabel(content_widget)
            label.setObjectName(textbox_name + "_label")
            
            # Format label text
            display_name = textbox_name.replace('_', ' ')
            if textbox_name == 'Fy_20':
                display_name = 'Fy (< 20mm)'
            elif textbox_name == 'Fy_20_40':
                display_name = 'Fy (20-40mm)'
            elif textbox_name == 'Fy_40':
                display_name = 'Fy (> 40mm)'
            elif textbox_name == 'Fu':
                display_name = 'Fu'
                
            label.setText(_translate("MainWindow", display_name + ":"))
            label.setFixedSize(100, 30)
            content_layout.addWidget(label, i, 1, 1, 1)
            
            textbox = QLineEdit(content_widget)
            textbox.setObjectName(textbox_name)
            textbox.setFixedSize(200, 24)
            
            if textbox_name == 'Grade':
                textbox.setReadOnly(True)
                textbox.setText("Cus____")
            else:
                textbox.setValidator(QIntValidator())
                # Store original focus event
                self.original_focus_event_functions[textbox_name] = textbox.focusOutEvent
                textbox.focusOutEvent = event_function[textbox_list.index(textbox_name)]
            
            self.connect_change_popup_material(textbox, content_widget)
            content_layout.addWidget(textbox, i, 2, 1, 1)
        
        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_button = QPushButton("Add")
        add_button.setObjectName("material_add")
        add_button.setFixedSize(80, 30)
        add_button.clicked.connect(lambda: self.update_material_db_validation(content_widget))
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedSize(80, 30)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        
        content_layout.addLayout(button_layout, len(textbox_list), 1, 1, 2, Qt.AlignCenter)
        
        central_layout.addWidget(content_widget)
        dialog.setLayout(central_layout)
        
        # Set dialog size and position
        dialog.setFixedSize(350, 280)
        
        # Show dialog and wait for result
        result = dialog.exec()
        
        # Update material combobox if dialog was accepted (Add button clicked successfully)
        if result == QDialog.Accepted:
            try:
                input_dock_material = self.input_widget.findChild(QWidget, KEY_MATERIAL)
                if input_dock_material:
                    current_text = input_dock_material.currentText()
                    input_dock_material.clear()
                    for item in connectdb("Material"):
                        input_dock_material.addItem(item)
                    # Try to restore previous selection or set to new custom material
                    index = input_dock_material.findText(current_text)
                    if index >= 0:
                        input_dock_material.setCurrentIndex(index)
                    else:
                        input_dock_material.setCurrentIndex(input_dock_material.count() - 1)
            except Exception as e:
                print(f"[ERROR]: Error updating material combobox: {e}")

    def show_material_popup_message(self):
        """Show validation message for material popup"""
        if self.material_popup_message:
            QMessageBox.warning(self, "Validation Error", self.material_popup_message)

    def update_material_db_validation(self, widget):
        """Validate and update material database"""
        material = widget.findChild(QLineEdit, 'Grade').text()
        
        material_validator = MaterialValidator(material)
        if material_validator.is_already_in_db():
            QMessageBox.warning(widget.window(), "Warning", "Material already exists in Database!")
            return
        elif not material_validator.is_format_custom():
            QMessageBox.warning(widget.window(), "Warning", "Please fill all missing parameters!")
            return
        elif not material_validator.is_valid_custom():
            QMessageBox.warning(widget.window(), "Warning", 
                            f"Please select {material_validator.invalid_value} in valid range!")
            return
        
        try:
            self.update_material_db(grade=material, material=material_validator)
            QMessageBox.information(widget.window(), 'Success', 
                                'Material added successfully to the database.')
            # Close dialog with accepted status
            widget.window().accept()
        except Exception as e:
            QMessageBox.critical(widget.window(), 'Error', 
                            f'Failed to add material to database: {str(e)}')
        
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
        if self.parent:
            if self.width() == 0:
                if hasattr(self.parent, 'update_docking_icons'):
                    self.parent.update_docking_icons(input_is_active=False)
            elif self.width() > 0:
                if hasattr(self.parent, 'update_docking_icons'):
                    self.parent.update_docking_icons(input_is_active=True)
    
#----------------Standalone-Test-Code--------------------------------
from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection
from osdag_gui.OS_safety_protocols import setup_environment
from osdag_gui.OS_safety_protocols import get_cleanup_coordinator

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