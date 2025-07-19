import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGroupBox,
    QFormLayout, QLineEdit, QScrollArea
)
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QPoint, QEasingCurve

from osdag_gui.ui.components.custom_buttons import CustomButton

def style_line_edit():
    return """
        QLineEdit {
            padding: 1px 7px;
            border: 1px solid #070707;
            border-radius: 4px;
            background-color: white;
            color: #000000;
            font-weight: normal;
            min-width: 120px;
            max-width: 140px;
        }
    """

def style_small_button():
    return """
        QPushButton {
            padding: 2px 7px;
            background-color: #888;
            color: white;
            border-radius: 4px;
            min-width: 120px;
            max-width: 140px;
            font-size: 12px;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
    """

def style_button():
    return """padding: 4px 10px; background-color: #888; color: white; border-radius: 4px;"""

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

def style_group_box():
    return """
        QGroupBox {
            border: 1px solid #90af13;
            border-radius: 4px;
            margin-top: 0.8em;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: content;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
            margin-top: -10px;
            background-color: white;
        }
    """

def pad_labels(fields):
    max_len = max(len(field.get("row_label", field["label"])) for field in fields)
    for field in fields:
        label = field.get("row_label", field["label"])
        field["label_padded"] = label.ljust(max_len)
    return fields

def create_row(label_text, widget, spacing=4):
    row_widget = QWidget()
    row_layout = QHBoxLayout(row_widget)
    row_layout.setContentsMargins(0, 0, 0, 0)
    row_layout.setSpacing(spacing)

    label = QLabel(label_text)
    label.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace;")
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    row_layout.addWidget(label)
    row_layout.addWidget(widget)
    return row_widget

# Data-driven group and field definition
GROUPS_DATA = {
    "Bolt": [
        {"type": "lineedit", "label": "Diameter (mm)"},
        {"type": "lineedit", "label": "Property Class"},
        {"type": "lineedit", "label": "Shear Capacity (kN)"},
        {"type": "lineedit", "label": "Bearing Capacity (kN)"},
        {"type": "lineedit", "label": "Capacity (kN)"},
        {"type": "lineedit", "label": "Bolt Force (kN)"},
        {"type": "lineedit", "label": "Bolt Columns"},
        {"type": "lineedit", "label": "Bolt Rows"},
        {"type": "button", "label": "Spacing Details", "disabled": True, "row_label": "Spacing"},
    ],
    "Plate": [
        {"type": "lineedit", "label": "Thickness (mm)"},
        {"type": "lineedit", "label": "Height (mm)"},
        {"type": "lineedit", "label": "Length (mm)"},
        {"type": "button", "label": "Capacity Details", "disabled": True, "row_label": "Capacity"},
    ],
    "Section Details": [
        {"type": "button", "label": "Capacity Details", "disabled": True, "row_label": "Capacity"},
    ],
    "Weld": [
        {"type": "lineedit", "label": "Size (mm)"},
        {"type": "lineedit", "label": "Strength (N/mm2)"},
        {"type": "lineedit", "label": "Stress (N/mm)"},
    ],
}

def create_group_box(title, fields):
    group_box = QGroupBox(title)
    group_box.setStyleSheet(style_group_box())
    group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    layout = QVBoxLayout(group_box)
    layout.setContentsMargins(4, 4, 4, 4)
    layout.setSpacing(2)

    form = QFormLayout()
    form.setHorizontalSpacing(4)
    form.setVerticalSpacing(4)
    form.setLabelAlignment(Qt.AlignLeft)
    form.setFormAlignment(Qt.AlignTop)

    layout.addSpacing(4)

    # Pad labels for this group
    fields = pad_labels(fields)

    for field in fields:
        if field["type"] == "lineedit":
            line = QLineEdit()
            line.setStyleSheet(style_line_edit())
            form.addRow(create_row(field["label_padded"], line, spacing=4))
        elif field["type"] == "button":
            btn = QPushButton(field["label"])
            btn.setStyleSheet(style_small_button())
            btn.setEnabled(not field.get("disabled", False))
            form.addRow(create_row(field["label_padded"], btn, spacing=4))

    layout.addLayout(form)
    return group_box

class OutputDock(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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

        # Hide the dock initially
        self.setMinimumWidth(0)
        self.setMaximumWidth(0)

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
        group_layout = QVBoxLayout(group_container)
        for title, fields in GROUPS_DATA.items():
            group_box = create_group_box(title, fields)
            group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            group_layout.addWidget(group_box)
        group_layout.addStretch()

        scroll_area.setWidget(group_container)
        right_layout.addWidget(scroll_area)

        btn_button_layout = QHBoxLayout()
        btn_button_layout.setContentsMargins(0, 20, 0, 0)
        btn_button_layout.addStretch(1)

        clickable_btn = CustomButton("Generate Report")
        clickable_btn.clicked.connect(lambda: print("Report Generate clicked"))

        btn_button_layout.addWidget(clickable_btn, 2)
        btn_button_layout.addStretch(1)
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

    def toggle_output_dock(self):
        parent = self.parent
        if hasattr(parent, 'toggle_animate'):
            is_collapsing = self.width() > 0
            parent.toggle_animate(show=not is_collapsing, dock='output')
        
        self.toggle_btn.setText("❯" if is_collapsing else "❮")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

    def _on_animation_finished(self):
        # Callback logic can go here if needed after animation completes
        # For now, we don't have a specific callback for the width animation
        pass

    def is_panel_visible(self):
        return self.panel_visible
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.width() == 0 and hasattr(self.parent, 'update_docking_icons'):
            self.parent.update_docking_icons(self.parent.input_dock_active, self.parent.log_dock_active, False)
        elif self.width() > 0 and hasattr(self.parent, 'update_docking_icons'):
            self.parent.update_docking_icons(self.parent.input_dock_active, self.parent.log_dock_active, True)

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


