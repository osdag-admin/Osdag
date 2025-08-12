"""
Home window for Osdag GUI.
Displays navigation, SVG cards, and home widgets.
"""
import osdag_gui.resources.resources_rc

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread, Signal

import sys
import os
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout,
    QLabel, QMainWindow, QSizePolicy, QFrame, QScrollArea, QButtonGroup
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QRect, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QIcon, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer

from osdag_gui.data.menus.menu_data import Data
from osdag_gui.ui.components.svg_card import SvgCardContainer
from osdag_gui.ui.components.navbar import VerticalMenuBar
from osdag_gui.ui.components.custom_buttons import MenuButton
from osdag_gui.ui.components.top_right_button_bar import TopButton, DropDownButton
from osdag_gui.ui.components.home_widget import HomeWidget
from PySide6.QtWidgets import QSplitter

class BackgroundSvgWidget(QWidget):
    def __init__(self, svg_path, parent=None):
        super().__init__(parent)
        self.svg_path = svg_path
        self.svg_renderer = QSvgRenderer(self.svg_path)
        self.setContentsMargins(0, 0, 0, 0) # Ensure no margins for drawing

    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw left border
        border_color = QColor("#90AF13")
        pen = painter.pen()
        pen.setColor(border_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, self.height())
        # Draw SVG background
        target_rect = self.rect()
        self.svg_renderer.render(painter, target_rect)
        painter.end()
        super().paintEvent(event)

# --- End of background_svg_widget.py content ---
class FadeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 1.0
        self.setAttribute(Qt.WA_TranslucentBackground)

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    opacity = Property(float, getOpacity, setOpacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the current opacity for drawing the background
        painter.setOpacity(self._opacity)

        # Now, set opacity for child widgets if needed, or rely on their own painting
        # For child widgets to also respect this opacity, they need to be painted after this
        # or have their own opacity set. For simple layout containers, this is sufficient.
        painter.end() # End painter for the background drawing

        # Now, call the superclass paintEvent. This is where child widgets will be painted.
        # It's crucial to call this AFTER your custom background drawing.
        super().paintEvent(event)

class HomeWindow(QWidget):
    cardOpenClicked = Signal(str)  # Signal to propagate upward
    def __init__(self):
        super().__init__()
        self.setStyleSheet("")

        dat = Data()
        self.menu_bar_data = dat.MODULES
        floating_navbar = dat.FLOATING_NAVBAR

        self.current_primary_button = None
        self.current_secondary_button = None

        # self.osdag_content = QWidget()
        # self.setCentralWidget(self.osdag_content)

        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        # Left Navigation Bar
        self.nav_bar = VerticalMenuBar(self.menu_bar_data)
        self.nav_bar.nav_bar_trigger.connect(self.nav_trigger)

        main_h_layout.addWidget(self.nav_bar, 2)

        self.content = BackgroundSvgWidget(":/vectors/background.svg")
        self.content.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)

        content_v_layout = QVBoxLayout(self.content)
        content_v_layout.setContentsMargins(0, 0, 0, 0)
        content_v_layout.setSpacing(0)

        # --- Top Horizontal Layout with SVG and Widget ---
        self.top_right_container = QWidget()
        self.top_right_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        self.top_right_h_layout = QHBoxLayout(self.top_right_container)
        self.top_right_h_layout.setContentsMargins(10, 5, 10, 0)
        self.top_right_h_layout.setSpacing(10)
        self.top_right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.top_svg_widget_1 = QSvgWidget()
        self.top_svg_widget_1.load(":/vectors/Osdag_label.svg")
        self.top_svg_widget_1.setFixedSize(181, 80)
        # No explicit stylesheet for QSvgWidget here. It will rely on its parent's background.
        self.top_right_h_layout.addWidget(self.top_svg_widget_1)

        self.top_widget_2 = QHBoxLayout()
        self.top_widget_2.setContentsMargins(0, 0, 15, 0)
        self.top_widget_2.setSpacing(2)
        self.button_group = QButtonGroup(self)
        # self.button_group.setExclusive(True) # Removed as buttons are no longer checkable
        self.buttons = [] # Store references to the created buttons

        # Instantiate and add the custom buttons to the header
        for i, (black_icon, white_icon, label) in enumerate(floating_navbar):
            if label == "Resources":
                button = DropDownButton(black_icon, white_icon, label)
            else:
                button = TopButton(black_icon, white_icon, label)
            
            self.buttons.append(button)
            self.button_group.addButton(button, i) # Add button to the group with an ID
            self.top_widget_2.addWidget(button)

        self.top_right_h_layout.addStretch(1)
        self.top_right_h_layout.addLayout(self.top_widget_2)

        content_v_layout.addWidget(self.top_right_container)

        # Single SVG Widget below the top horizontal layout (now a wrapper QWidget) ---
        self.middle_top_svg_layout_wrapper_widget = QWidget() # The wrapper widget
        self.middle_top_svg_layout_wrapper_widget.setStyleSheet("background: transparent;") # Explicit solid background
        self.middle_top_svg_layout_wrapper = QHBoxLayout(self.middle_top_svg_layout_wrapper_widget) # Layout inside wrapper

        self.middle_top_svg_widget = QSvgWidget()
        self.middle_top_svg_widget.load(":/vectors/Osdag_tagline.svg")
        self.middle_top_svg_widget.setFixedSize(420, 35)
        # No explicit stylesheet for QSvgWidget here. It will rely on its parent's background.

        # To align it to the left, remove the stretch before and add it after:
        self.middle_top_svg_layout_wrapper.addWidget(self.middle_top_svg_widget)
        self.middle_top_svg_layout_wrapper.addStretch(1) # Stretch to push content to left

        self.middle_top_svg_layout_wrapper.setContentsMargins(10, 5, 10, 5)
        content_v_layout.addWidget(self.middle_top_svg_layout_wrapper_widget) # Add the wrapper widget

        self.variable_widget = QWidget()
        self.variable_layout = QVBoxLayout(self.variable_widget)

        # Primary Menu Container
        self.primary_menu_container = FadeWidget()
        # Set margins on the FadeWidget itself, not just its internal layout
        self.primary_menu_container.setContentsMargins(10, 30, 10, 0) # These margins will be part of the painted area
        self.primary_menu_layout = QHBoxLayout(self.primary_menu_container)
        self.primary_menu_layout.setContentsMargins(0, 0, 0, 0) # Reset internal layout margins to 0
        self.primary_menu_layout.setSpacing(5)
        self.primary_menu_container.setStyleSheet("background: transparent;") # Keep transparent to allow custom painting
        self.primary_menu_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.variable_layout.addWidget(self.primary_menu_container)

        # Secondary Menu Container
        self.secondary_menu_container = FadeWidget()
        # Set margins on the FadeWidget itself
        self.secondary_menu_container.setContentsMargins(10, 5, 10, 5) # These margins will be part of the painted area
        self.secondary_menu_layout = QHBoxLayout(self.secondary_menu_container)
        self.secondary_menu_layout.setContentsMargins(0, 0, 0, 0) # Reset internal layout margins to 0
        self.secondary_menu_layout.setSpacing(5)
        self.secondary_menu_container.setStyleSheet("background: transparent;") # Keep transparent
        self.secondary_menu_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.secondary_menu_container.setMaximumHeight(0)
        self.secondary_menu_container.setOpacity(0.0)
        self.secondary_menu_container.hide()
        self.secondary_menu_hidden = True
        self.variable_layout.addWidget(self.secondary_menu_container)

        # --- QScrollArea for SVG Card Area ---
        self.scroll_area_for_svg_cards = QScrollArea()
        self.scroll_area_for_svg_cards.setWidgetResizable(True)
        self.scroll_area_for_svg_cards.setFrameShape(QFrame.NoFrame)
        self.scroll_area_for_svg_cards.setStyleSheet("background: transparent;") # Explicit solid white background

        self.svg_card_area = QWidget()
        self.svg_card_layout = QVBoxLayout(self.svg_card_area)
        self.svg_card_layout.setContentsMargins(10,10,10,10)
        self.svg_card_layout.setSpacing(10)
        self.svg_card_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area_for_svg_cards.setWidget(self.svg_card_area)
        self.variable_layout.addWidget(self.scroll_area_for_svg_cards, 1)

        content_v_layout.addWidget(self.variable_widget)

        # # --- Bottom Horizontal Layout with three SVG Widgets ---
        # self.bottom_right_container = QWidget()
        # self.bottom_right_container.setStyleSheet("""
        #     QWidget {
        #         background: transparent; /* Explicit solid background */
        #     }
        # """)
        # self.bottom_right_h_layout = QHBoxLayout(self.bottom_right_container)
        # self.bottom_right_h_layout.setContentsMargins(10, 10, 5, 10)
        # self.bottom_right_h_layout.setSpacing(10)
        # self.bottom_right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # self.bottom_svg_widget_1 = QSvgWidget()
        # self.bottom_svg_widget_1.load(":/vectors/FOSSEE_logo.svg")
        # self.bottom_svg_widget_1.setFixedSize(163, 60)
        # # No explicit stylesheet for QSvgWidget here.
        # self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_1)

        # self.bottom_svg_widget_2 = QSvgWidget()
        # self.bottom_svg_widget_2.load(":/vectors/MOS_logo.svg")
        # self.bottom_svg_widget_2.setFixedSize(122, 60)
        # # No explicit stylesheet for QSvgWidget here.
        # self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_2)

        # self.bottom_svg_widget_3 = QSvgWidget()
        # self.bottom_svg_widget_3.load(":/vectors/ConstructSteel_logo.svg")
        # self.bottom_svg_widget_3.setFixedSize(263, 30)
        # # No explicit stylesheet for QSvgWidget here.
        # self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_3, alignment=Qt.AlignmentFlag.AlignBottom)
        # self.bottom_right_h_layout.addStretch(1)

        # content_v_layout.addWidget(self.bottom_right_container)

        main_h_layout.addWidget(self.content, 8)

        self.show_home()
        # self.showMaximized()

    def _clear_layout(self, layout):
        """Recursively clears a layout and deletes its widgets."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())

    def _reset_primary_menu_style(self):
        """Resets the style of the currently selected primary menu button."""
        if self.current_primary_button:
            self.current_primary_button.set_selected(False)
            self.current_primary_button = None

    def _reset_secondary_menu_style(self):
        """Resets the style of the currently selected secondary menu button."""
        if self.current_secondary_button:
            self.current_secondary_button.set_selected(False)
            self.current_secondary_button = None

    def _animate_secondary_menu(self, show=True):
        self.secondary_menu_animation_height = QPropertyAnimation(self.secondary_menu_container, b"maximumHeight")
        self.secondary_menu_animation_opacity = QPropertyAnimation(self.secondary_menu_container, b"opacity")

        duration = 300 # milliseconds

        self.secondary_menu_animation_height.setDuration(duration)
        self.secondary_menu_animation_opacity.setDuration(duration)
        self.secondary_menu_animation_height.setEasingCurve(QEasingCurve.InOutQuad)
        self.secondary_menu_animation_opacity.setEasingCurve(QEasingCurve.InOutQuad)

        if show:
            self.secondary_menu_container.show()
            self.secondary_menu_animation_height.setStartValue(0)
            self.secondary_menu_animation_height.setEndValue(self.secondary_menu_container.sizeHint().height())
            self.secondary_menu_animation_opacity.setStartValue(0.0)
            self.secondary_menu_animation_opacity.setEndValue(1.0)
            self.secondary_menu_hidden = False
        else:
            self.secondary_menu_animation_height.setStartValue(self.secondary_menu_container.height())
            self.secondary_menu_animation_height.setEndValue(0)
            self.secondary_menu_animation_opacity.setStartValue(1.0)
            self.secondary_menu_animation_opacity.setEndValue(0.0)
            self.secondary_menu_animation_opacity.finished.connect(self.secondary_menu_container.hide)
            self.secondary_menu_hidden = True

        self.secondary_menu_animation_height.start()
        self.secondary_menu_animation_opacity.start()

    def nav_trigger(self, menu_bar_data, name):
        """Triggered by main left navigation bar buttons."""
        self._clear_layout(self.primary_menu_layout)
        self._clear_layout(self.secondary_menu_layout)

        self._reset_primary_menu_style()
        self._reset_secondary_menu_style()

        if not self.secondary_menu_hidden:
            self.show_home()

        if name == 'Home':
            self._clear_layout(self.svg_card_layout)
            self.primary_menu_container.hide()
            home_widget = HomeWidget()
            self.svg_card_layout.addWidget(home_widget)

        elif isinstance(menu_bar_data, list):
            # zero level menu bar
            svg_card_widget = SvgCardContainer(menu_bar_data)
            self._clear_layout(self.svg_card_layout)

            label = QLabel(name)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            label.setStyleSheet("""
                QLabel{
                    color: #000000;
                    font-size: 16px;
                    font-family: 'Calibri';
                    background-color: rgba(255, 255, 255, 150);
                    padding: 2px 0px;
                    border-top: 1px solid #90AF13;
                    border-bottom: 1px solid #90AF13;
                }
            """)
            # self.svg_card_layout.addStretch()
            self.svg_card_layout.addWidget(label)
            self.svg_card_layout.addStretch()
            self.svg_card_layout.addWidget(svg_card_widget)
            self.svg_card_layout.addStretch()
            self.primary_menu_container.hide()

        elif isinstance(menu_bar_data, dict):
            self._clear_layout(self.svg_card_layout)

            self.primary_menu_container.show()
            default_btn = None 
            toggle = True
            self.primary_menu_layout.addStretch(1)
            for i in menu_bar_data.keys():
                internal_dat = menu_bar_data.get(i)
                btn = MenuButton(i)
                if toggle:
                    toggle = False
                    default_btn = [i, btn]
                if isinstance(internal_dat, list):
                    # single level menu bar
                    btn.clicked.connect(lambda _, b=btn, data=internal_dat: self.menu_trigger(data, b))
                elif isinstance(internal_dat, dict):
                    # double level menu bar
                    btn.clicked.connect(lambda _, b=btn, data=internal_dat: self.submenu_trigger(data, b))
                self.primary_menu_layout.addWidget(btn)
            self.primary_menu_layout.addStretch(1)
            # set first Menu as Default
            self.menu_trigger(menu_bar_data.get(default_btn[0]), default_btn[1])

    def show_home(self):
        self._clear_layout(self.svg_card_layout)
        self.primary_menu_container.hide()
        home_widget = HomeWidget()
        self.svg_card_layout.addWidget(home_widget)

    def menu_trigger(self, data, clicked_button=None):
        """
        Triggered when a primary menu button (that directly shows SVG cards)
        or a secondary menu button is clicked.
        """
        self._clear_layout(self.svg_card_layout)

        if isinstance(clicked_button, MenuButton):
            self._reset_primary_menu_style()
            clicked_button.set_selected(True)
            self.current_primary_button = clicked_button
            self._reset_secondary_menu_style()

        if not self.secondary_menu_hidden:
            self.secondary_menu_container.setMaximumHeight(0)
            self.secondary_menu_container.setOpacity(0.0)
            self.secondary_menu_container.hide()
            self.secondary_menu_hidden = True

        svg_card_widget = SvgCardContainer(data)
        svg_card_widget.cardOpenClicked.connect(self.handle_card_open_clicked)
        self.svg_card_layout.addWidget(svg_card_widget)

    def submenu_trigger(self, data, clicked_button=None):
        """
        Triggered when a primary menu button (that leads to a submenu) is clicked.
        """
        self._clear_layout(self.secondary_menu_layout)
        self._clear_layout(self.svg_card_layout)

        if isinstance(clicked_button, MenuButton):
            self._reset_primary_menu_style()
            clicked_button.set_selected(True)
            self.current_primary_button = clicked_button
            self._reset_secondary_menu_style()

        self.secondary_menu_container.setMaximumHeight(0)
        self.secondary_menu_container.setOpacity(0.0)
        self.secondary_menu_container.hide()
        self.secondary_menu_hidden = True

        default_btn = None 
        toggle = True
        
        self.secondary_menu_layout.addStretch(1)
        for i in data.keys():
            internal_dat = data.get(i)
            btn = MenuButton(i)
            if toggle:
                toggle = False
                default_btn = [i, btn]
            btn.clicked.connect(lambda _, b=btn, data=internal_dat: self.menu_bar(data, b))
            self.secondary_menu_layout.addWidget(btn)
        self.secondary_menu_layout.addStretch(1)

        self._animate_secondary_menu(True)
        # set first Menu as Default
        self.menu_bar(data.get(default_btn[0]), default_btn[1])


    def menu_bar(self, data, clicked_button=None):
        """
        Triggered when a secondary menu button is clicked,
        clearing SVG card area and displaying new cards.
        """
        self._clear_layout(self.svg_card_layout)

        if isinstance(clicked_button, MenuButton):
            self._reset_secondary_menu_style()
            clicked_button.set_selected(True)
            self.current_secondary_button = clicked_button

        svg_card_widget = SvgCardContainer(data)
        svg_card_widget.cardOpenClicked.connect(self.handle_card_open_clicked)
        self.svg_card_layout.addWidget(svg_card_widget)

    def handle_card_open_clicked(self, card_title):
        self.cardOpenClicked.emit(card_title)

    def set_active_button(self, module):
        self.nav_bar.set_active_button_by_name(module)

# if __name__ == "__main__":
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#     app = QApplication(sys.argv)
#     window = HomeWindow()
#     window.show()
#     sys.exit(app.exec())

