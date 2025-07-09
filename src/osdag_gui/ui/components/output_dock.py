import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QGroupBox,
    QFormLayout, QLineEdit, QScrollArea
)
from PySide6.QtGui import QPalette, QColor, QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QPoint, QEasingCurve

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

def create_row(label_text, widget, label_width=120, field_width=130, spacing=4):
    row_widget = QWidget()
    row_layout = QHBoxLayout(row_widget)
    row_layout.setContentsMargins(0, 0, 0, 0)
    row_layout.setSpacing(spacing)

    label = QLabel(label_text)
    label.setFixedWidth(label_width)
    widget.setFixedWidth(field_width)

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

    for field in fields:
        if field["type"] == "lineedit":
            line = QLineEdit()
            line.setStyleSheet(style_line_edit())
            form.addRow(create_row(field["label"], line, label_width=120, field_width=130, spacing=4))
        elif field["type"] == "button":
            btn = QPushButton(field["label"])
            btn.setStyleSheet(style_small_button())
            btn.setEnabled(not field.get("disabled", False))
            row_label = field.get("row_label", field["label"])
            form.addRow(create_row(row_label, btn, label_width=120, field_width=130, spacing=4))

    layout.addLayout(form)
    return group_box

class OutputDock(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: #FFF;")
        self.dock_width = 360
        self.panel_visible = False # Initially hidden

        # Animation setup
        self.animation = QPropertyAnimation(self, b"pos") # This animation is no longer used for width, but can remain if other pos animations are intended
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self._on_animation_finished)
        self._animation_callback = None

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(0,0,0,0)
        output_layout.setSpacing(0)

        # Set initial hidden width for the dock itself
        self.setMinimumWidth(0)
        self.setMaximumWidth(0)

        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #94b816;")
        self.toggle_strip.setFixedWidth(0) # Initially hidden
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("❯") # Initially points right to show
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setToolTip("Show panel") # Initially tooltip to show
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

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(5,5,5,5)
        right_layout.setSpacing(4)

        # Top button
        top_button_layout = QHBoxLayout()
        output_dock_btn = QPushButton("Output Dock")
        output_dock_btn.setStyleSheet(style_main_buttons())
        top_button_layout.addWidget(output_dock_btn)
        top_button_layout.addStretch()
        right_layout.addLayout(top_button_layout)

        # Scroll area for group boxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #EFEFEC;
                background-color: transparent;
                padding: 3px;
            }
            QScrollBar:vertical {
                background: #C3E05D;
                width: 8px;
                margin: 0px 0px 0px 3px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #90AF13;
                min-height: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6c8408;
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
        group_layout = QVBoxLayout(group_container)
        for title, fields in GROUPS_DATA.items():
            group_box = create_group_box(title, fields)
            group_layout.addWidget(group_box)
        group_layout.addStretch() # Push content to top

        scroll_area.setWidget(group_container)
        right_layout.addWidget(scroll_area)

        # Bottom buttons
        create_btn = QPushButton("Create Design Report")
        create_btn.setStyleSheet(style_main_buttons())
        save_btn = QPushButton("Save Output")
        save_btn.setStyleSheet(style_main_buttons())
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setAlignment(Qt.AlignCenter)
        wrapper_layout.setSpacing(10)
        wrapper_layout.addWidget(create_btn)
        wrapper_layout.addWidget(save_btn)
        right_layout.addWidget(wrapper)
        output_layout.addLayout(right_layout)

    def toggle_output_dock(self):
        is_collapsing = self.panel_visible
        self.parent.output_dock_icon_toggle()
        target_dock_width = 0 if is_collapsing else self.dock_width
        target_strip_width = 0 if is_collapsing else 6

        # Animate the OutputDock (self) width
        for prop in [b"minimumWidth", b"maximumWidth"]:
            dock_anim = QPropertyAnimation(self, prop)
            dock_anim.setDuration(300)
            dock_anim.setStartValue(self.width())
            dock_anim.setEndValue(target_dock_width)
            dock_anim.start()
            setattr(self, f"_dock_anim_{prop.decode()}", dock_anim)

        # Animate the toggle_strip width
        for prop in [b"minimumWidth", b"maximumWidth"]:
            strip_anim = QPropertyAnimation(self.toggle_strip, prop)
            strip_anim.setDuration(300)
            strip_anim.setStartValue(self.toggle_strip.width())
            strip_anim.setEndValue(target_strip_width)
            strip_anim.start()
            setattr(self, f"_strip_anim_{prop.decode()}", strip_anim)

        # Update the button text and tooltip
        self.toggle_btn.setText("❮" if is_collapsing else "❯")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

        # Toggle the panel visibility state
        self.panel_visible = not self.panel_visible

    def _on_animation_finished(self):
        # Callback logic can go here if needed after animation completes
        # For now, we don't have a specific callback for the width animation
        pass

    def is_panel_visible(self):
        return self.panel_visible


