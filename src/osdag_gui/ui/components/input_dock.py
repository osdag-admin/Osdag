import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QComboBox, QScrollArea, QLabel, QFormLayout, QLineEdit, QGroupBox, QSizePolicy
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QSize
from PySide6.QtGui import QPixmap, QIcon, QPainter, QColor

from osdag_gui.ui.components.additional_inputs_button import AdditionalInputsButton
import osdag_gui.resources.resources_rc

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()  # Prevent changing selection on scroll

def right_aligned_widget(widget):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addStretch()
    layout.addWidget(widget)
    return container

def apply_dropdown_style(widget, arrow_down_path):
    widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    widget.setFixedWidth(150)
    if isinstance(widget, QComboBox):
        style = f"""
        QComboBox {{
            padding: 1px 5px;
            border: 1px solid black;
            border-radius: 5px;
            background-color: white;
            color: black;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border-left: 0px;
        }}
        QComboBox::down-arrow {{
            image: url("{arrow_down_path}");
            width: 18px;
            height: 18px;
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
            padding: 2px 3px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            border: 1px solid #90AF13;
            background-color: white;
            color: black;
        }}
        QComboBox QAbstractItemView::item:selected {{
            background-color: white;
            color: black;
            border: 1px solid #90AF13;
        }}
        QComboBox QAbstractItemView::item:selected:hover {{
            background-color: white;
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

def create_connecting_members_group(apply_style_func, arrow_path):
    connectivity_configs = {
        "Column Flange-Beam Web": {
            "image": ":/images/colF2.png",
            "fields": [
                {"label": "Column Section *", "items": ["HB150", "HB200", "HB250", "HB300"]},
                {"label": "Primary Beam *", "items": ["JB150", "JB175", "JB200", "JB225"]},
                {"label": "Material *", "items": ["E 165 (Fe 290)", "E250", "E300", "E350"]}
            ]
        },
        "Column Web-Beam Web": {
            "image": ":/images/colW1.png",
            "fields": [
                {"label": "Column Section *", "items": ["HB150", "HB200", "HB250", "HB300"]},
                {"label": "Primary Beam *", "items": ["JB150", "JB175", "JB200", "JB225"]},
                {"label": "Material *", "items": ["E 165 (Fe 290)", "E250", "E300", "E350"]}
            ]
        },
        "Beam-Beam": {
            "image": ":/images/fin_beam_beam.png",
            "fields": [
                {"label": "Primary Beam *", "items": ["JB150", "JB175", "JB200", "JB225"]},
                {"label": "Secondary Beam *", "items": ["JB150", "JB175", "JB200", "JB225"]},
                {"label": "Material *", "items": ["E 165 (Fe 290)", "E250", "E300", "E350"]}
            ]
        }
    }

    group = QGroupBox("Connecting Members")
    group.setStyleSheet("""
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
    layout = QVBoxLayout(group)
    layout.setSpacing(5)
    layout.setContentsMargins(4, 4, 4, 4)

    conn_form = QFormLayout()
    conn_form.setHorizontalSpacing(20)
    conn_form.setVerticalSpacing(10)
    conn_form.setContentsMargins(10, 5, 10, 5)
    conn_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
    conn_form.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align fields to the right

    connectivity_cb = NoScrollComboBox()
    connectivity_cb.addItems(list(connectivity_configs.keys()))
    apply_style_func(connectivity_cb, arrow_path)
    conn_form.addRow("Connectivity *", right_aligned_widget(connectivity_cb))
    layout.addLayout(conn_form)

    details_widget = QWidget()
    details_layout = QVBoxLayout(details_widget)
    details_layout.setContentsMargins(0, 0, 0, 0)
    details_layout.setSpacing(0)

    all_comboboxes = [connectivity_cb]
    connectivity_widgets = {}

    for conn_type, config in connectivity_configs.items():
        widget = QWidget()
        widget_layout = QVBoxLayout(widget)
        widget_layout.setContentsMargins(5, 5, 5, 5)
        widget_layout.setSpacing(5)

        img_label = QLabel()
        img_path = config["image"]
        img_label.setPixmap(QPixmap(img_path).scaledToWidth(90, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        form = QFormLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(10)
        form.setContentsMargins(10, 5, 10, 5)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setAlignment(Qt.AlignmentFlag.AlignRight)  # Align fields to the right

        form.addRow("", img_label)

        for field in config["fields"]:
            cb = NoScrollComboBox()
            cb.addItems(field["items"])
            apply_style_func(cb, arrow_path)
            form.addRow(field["label"], right_aligned_widget(cb))
            all_comboboxes.append(cb)

        widget_layout.addLayout(form)
        details_layout.addWidget(widget)
        connectivity_widgets[conn_type] = widget

    def switch_view(text):
        for conn_type, widget in connectivity_widgets.items():
            widget.setVisible(conn_type == text)

    connectivity_cb.currentTextChanged.connect(switch_view)
    switch_view(connectivity_cb.currentText())

    layout.addWidget(details_widget)
    return group

def create_group_box(title, fields, apply_style_func, arrow_path, horizontal_spacing=20):
    group = QGroupBox(title)
    group.setStyleSheet("""
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
        QLabel {
            margin-top: 4px;
        }
    """)
    
    form_layout = QFormLayout()
    form_layout.setHorizontalSpacing(horizontal_spacing)
    form_layout.setVerticalSpacing(10)
    form_layout.setContentsMargins(10, 5, 10, 5)
    form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
    
    all_widgets = []
    for field in fields:
        label = field["label"]
        if "items" in field:
            widget = NoScrollComboBox()
            widget.addItems(field["items"])
        else:
            widget = QLineEdit()
            if "placeholder" in field:
                widget.setPlaceholderText(field["placeholder"])
        
        apply_style_func(widget, arrow_path)
        form_layout.addRow(label, right_aligned_widget(widget))
        all_widgets.append(widget)
    
    group.setLayout(form_layout)
    return group, all_widgets

class InputDock(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.left_container = QWidget()
        self.original_width = int(self.width())
        # self.left_container.setMinimumWidth(self.original_width)
        # self.left_container.setMaximumWidth(self.original_width)
        self.build_left_panel()
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

        self.right_spacer = QWidget()
        self.main_layout.addWidget(self.right_spacer)

    def build_left_panel(self):
        left_layout = QVBoxLayout(self.left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.left_panel = QWidget()
        self.left_panel.setStyleSheet("background-color: white;")
        # self.left_panel.setMinimumWidth(360)
        # self.left_panel.setMaximumWidth(400)

        panel_layout = QVBoxLayout(self.left_panel)
        panel_layout.setContentsMargins(10, 10, 10, 10)

        # --- Top Bar (fixed) ---
        top_bar = QHBoxLayout()
        input_dock_btn = QPushButton("Input Dock")
        input_dock_btn.setStyleSheet("background-color: #90AF13; color: white; border-radius: 5px;")
        input_dock_btn.setFixedSize(108, 28)
        top_bar.addWidget(input_dock_btn)
        additional_inputs_btn = AdditionalInputsButton()
        additional_inputs_btn.setToolTip("Additional Inputs")
        top_bar.addWidget(additional_inputs_btn)
        top_bar.addStretch()
        panel_layout.addLayout(top_bar)

        # --- Scroll Area for Main Content ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Modern scrollbar style
        scroll_area.setStyleSheet('''
            QScrollArea {
                border: 1px solid #EFEFEC;
                background-color: white;
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
        ''')
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(5)

        arrow_path = ":/images/down_arrow.png"
        connecting_members_group = create_connecting_members_group(apply_dropdown_style, arrow_path)
        scroll_layout.addWidget(connecting_members_group)

        group_configs = {
            "Factored Loads": {
                "horizontal_spacing": 38,
                "fields": [
                    {"label": "Shear Force (kN)", "placeholder": "ex. 10 kN"},
                    {"label": "Axial Force (kN)", "placeholder": "ex. 10 kN"}
                ]
            },
            "Bolt": {
                "horizontal_spacing": 16,
                "fields": [
                    {"label": "Diameter (mm) *", "items": ["All", "Customized"]},
                    {"label": "Type *", "items": ["Bearing Bolt", "Friction Grip Bolt"]},
                    {"label": "Property Class *(mm)", "items": ["All", "Customized"]}
                ]
            },
            "Plate": {
                "horizontal_spacing": 38,
                "fields": [
                    {"label": "Thickness (mm) *", "items": ["All", "Customized"]}
                ]
            }
        }

        all_comboboxes = []
        for title, config in group_configs.items():
            group, widgets = create_group_box(
                title=title,
                fields=config["fields"],
                apply_style_func=apply_dropdown_style,
                arrow_path=arrow_path,
                horizontal_spacing=config["horizontal_spacing"]
            )
            scroll_layout.addWidget(group)
            all_comboboxes.extend(widgets)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        panel_layout.addWidget(scroll_area, 1)  # Expands to fill space between top and bottom

        # --- Bottom Design Button (fixed) ---
        svg_widget = QSvgWidget(":/vectors/design_button.svg")
        svg_widget.setFixedSize(150, 30)
        svg_widget.setToolTip("Design")
        svg_widget.setStyleSheet("""
            background-color: white;
            border: 2px solid #94b816;
            border-radius: 4px;
        """)
        svg_clickable_btn = QPushButton(svg_widget)
        svg_clickable_btn.setStyleSheet("background-color: transparent; border: none;")
        svg_clickable_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        svg_clickable_btn.setFixedSize(svg_widget.size())
        svg_clickable_btn.clicked.connect(lambda: print("design clicked"))

        svg_outer_layout = QVBoxLayout()
        svg_outer_layout.setContentsMargins(0, 20, 0, 0)
        svg_button_layout = QHBoxLayout()
        svg_button_layout.addStretch()
        svg_button_layout.addWidget(svg_widget)
        svg_button_layout.addStretch()
        svg_outer_layout.addLayout(svg_button_layout)
        panel_layout.addLayout(svg_outer_layout)

        panel_layout.addStretch()
        left_layout.addWidget(self.left_panel)

    def toggle_input_dock(self):
        is_collapsing = self.left_container.width() > 0
        self.parent.input_dock_icon_toggle()
        # Define a fixed expanded width that's suitable for your content
        EXPANDED_WIDTH = 340  # or whatever width works best for your comboboxes

        # Then use it in your animation
        target_width = 0 if is_collapsing else EXPANDED_WIDTH

        for prop in [b"minimumWidth", b"maximumWidth"]:
            container_anim = QPropertyAnimation(self.left_container, prop)
            container_anim.setDuration(300)
            container_anim.setStartValue(self.left_container.width())
            container_anim.setEndValue(target_width)
            container_anim.start()
            setattr(self, f"_container_anim_{prop.decode()}", container_anim)

            strip_anim = QPropertyAnimation(self.toggle_strip, prop)
            strip_anim.setDuration(300)
            strip_anim.setStartValue(self.toggle_strip.width())
            strip_anim.setEndValue(0 if is_collapsing else 6)
            strip_anim.start()
            setattr(self, f"_strip_anim_{prop.decode()}", strip_anim)

        self.toggle_btn.setText("❯" if is_collapsing else "❮")
        self.toggle_btn.setToolTip("Show panel" if is_collapsing else "Hide panel")

#----------------Standalone-Test-Code--------------------------------

# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setStyleSheet("border: none")

#         self.central_widget = QWidget()
#         self.central_widget.setObjectName("central_widget")
#         self.setCentralWidget(self.central_widget)

#         self.main_h_layout = QHBoxLayout(self.central_widget)
#         self.main_h_layout.addWidget(InputDock(),15)

#         self.main_h_layout.addStretch(40)

#         self.setWindowState(Qt.WindowMaximized)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec()) 

