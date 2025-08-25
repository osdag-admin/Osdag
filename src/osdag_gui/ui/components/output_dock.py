"""
Output dock widget for Osdag GUI.
Displays output fields and report generation for connection design.
"""
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGroupBox,
    QFormLayout, QLineEdit, QScrollArea
)
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QPoint, QEasingCurve, Signal

from osdag_gui.ui.components.custom_buttons import CustomButton
from osdag_core.Common import *
import osdag_gui.resources.resources_rc

def style_line_edit():
    return """
        QLineEdit {
            padding: 2px 7px;
            border: 1px solid #070707;
            border-radius: 4px;
            background-color: white;
            color: #000000;
            font-weight: normal;
            min-width: 100px;
            max-width: 120px;
        }
    """

def style_small_button():
    return """
        QPushButton {
            padding: 2px 7px;
            background-color: #888;
            color: white;
            border-radius: 4px;
            min-width: 100px;
            max-width: 120px;
            font-size: 12px;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
    """

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

class OutputDock(QWidget):
    def __init__(self, backend:object, parent):
        super().__init__(parent)
        self.parent = parent
        self.backend = backend()
        self.setStyleSheet("background-color: #FFF;")
        self.dock_width = 360
        self.panel_visible = False # Initially hidden
        self.setMinimumWidth(0)
        self.setMaximumWidth(16777215)

        # Ensure OutputDock expands in splitter
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Animation setup
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self._on_animation_finished)
        self._animation_callback = None

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(0,0,0,0)
        output_layout.setSpacing(0)

        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #94b816;")
        self.toggle_strip.setFixedWidth(6)  # Always visible
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("❯")  # Show state initially
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setToolTip("Show panel")
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
        self.toggle_btn.clicked.connect(self.toggle_output_dock)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        output_layout.addWidget(self.toggle_strip)

        # # Hide the dock initially
        # self.setMinimumWidth(0)
        # self.setMaximumWidth(0)

        # Show the dock initially for testing
        self.setMinimumWidth(self.dock_width)
        self.setMaximumWidth(self.dock_width)

        # --- Right content (everything except toggle strip) ---
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setContentsMargins(5,5,5,5)
        right_layout.setSpacing(4)

        # Top button
        top_button_layout = QHBoxLayout()
        output_dock_btn = QPushButton("Output Dock")
        output_dock_btn.setStyleSheet(style_main_buttons())
        output_dock_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_button_layout.addWidget(output_dock_btn)
        top_button_layout.addStretch()
        right_layout.addLayout(top_button_layout)

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

        # Group container
        group_container = QWidget()
        group_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_container_layout = QVBoxLayout(group_container)

        # Bring the data instance from `design_type` folder
        field_list = self.backend.output_values(False)
        # To equalize the label length
        # So that they are of equal size
        field_list = self.equalize_label_length(field_list)

        # Track any group is active or not
        track_group = False
        index = 0
        for field in field_list:
            index += 1
            label = field[1]
            type = field[2]
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
                current_group.setObjectName(label)
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

            elif type == TYPE_TEXTBOX:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")
                
                right = QLineEdit()
                right.setStyleSheet(style_line_edit())
                right.setObjectName(field[0])
                right.setReadOnly(True)
                cur_box_form.addRow(left, right)
            
            elif type == TYPE_OUT_BUTTON:
                left = QLabel(label)
                left.setObjectName(field[0] + "_label")
                left.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")
                
                right = QPushButton(label.strip())
                right.setObjectName(field[0])
                right.setStyleSheet(style_small_button())
                right.setDisabled(True)
                cur_box_form.addRow(left, right)

            if index == len(field_list):
                # Last Data tupple
                # Must add group_box with form
                current_group.setLayout(cur_box_form)
                group_container_layout.addWidget(current_group)

        group_container_layout.addStretch()
        scroll_area.setWidget(group_container)
        right_layout.addWidget(scroll_area)

        btn_button_layout = QHBoxLayout()
        btn_button_layout.setContentsMargins(0, 20, 0, 0)
        btn_button_layout.addStretch(2)

        design_report_btn = CustomButton("Generate Design Report", ":/vectors/design_report.svg")
        design_report_btn.clicked.connect(lambda: print("Report Generate clicked"))
        btn_button_layout.addWidget(design_report_btn)
        btn_button_layout.addStretch(1)       

        save_output_csv_btn = CustomButton("  Save Outputs (csv)  ", ":/vectors/design_report.svg")
        save_output_csv_btn.clicked.connect(lambda: print("Report Generate clicked"))
        btn_button_layout.addWidget(save_output_csv_btn)
        btn_button_layout.addStretch(2)

        right_layout.addLayout(btn_button_layout)

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
        h_scroll_area.setWidget(right_content)

        output_layout.addWidget(h_scroll_area)

    # To equalize the size of label strings
    def equalize_label_length(self, list):
        # Calculate maximum size
        max_len = 0
        for t in list:
            if t[2] not in [TYPE_TITLE]:
                if len(t[1]) > max_len:
                    max_len = len(t[1])
        
        # Create a new list with equal string length
        return_list = [] 
        for t in list:
            if t[2] not in [TYPE_TITLE]:
                new_tupple = (t[0], t[1].ljust(max_len)) + t[2:]
            else:
                new_tupple = t
            return_list.append(new_tupple)

        return return_list

    def toggle_output_dock(self):
        parent = self.parent
        if hasattr(parent, 'toggle_animate'):
            is_collapsing = self.width() > 0
            parent.toggle_animate(show=not is_collapsing, dock='output')
        
        self.toggle_btn.setText("❮" if is_collapsing else "❯")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

    def _on_animation_finished(self):
        # Callback logic can go here if needed after animation completes
        # For now, we don't have a specific callback for the width animation
        pass

    def is_panel_visible(self):
        return self.panel_visible

    def set_results(self, result_dict):
        layout = self.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for key, value in result_dict.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)
        self.current_result = result_dict      

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Checking hasattr is only meant to prevent errors,
        # while standalone testing of this widget
        if self.parent and hasattr(self.parent, 'parent') and self.parent.parent:
            if self.width() == 0:
                if hasattr(self.parent.parent, 'update_docking_icons'):
                    self.parent.parent.update_docking_icons(output_is_active=False)
                if hasattr(self.parent, 'update_input_label_state'):
                    self.parent.update_output_label_state(True)
            elif self.width() > 0:
                if hasattr(self.parent.parent, 'update_docking_icons'):
                    self.parent.parent.update_docking_icons(output_is_active=True)
                if hasattr(self.parent, 'update_input_label_state'):
                    self.parent.update_output_label_state(False)

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
        self.main_h_layout.addStretch(40)

        self.main_h_layout.addWidget(OutputDock(backend=FinPlateConnection ,parent=self),15)
        self.setWindowState(Qt.WindowMaximized)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec()) 

