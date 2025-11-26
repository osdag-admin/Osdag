"""
Home window for Osdag GUI.
Displays navigation, SVG cards, and home widgets.
"""
import osdag_gui.resources.resources_rc

from PySide6.QtCore import QRectF, Signal, Slot

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication,
    QLabel, QSizePolicy, QFrame, QScrollArea, QButtonGroup
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QIcon, QPaintEvent, QPainter, QColor, QPixmap
from PySide6.QtSvg import QSvgRenderer

from osdag_gui.data.ui_data import Data
from osdag_gui.ui.components.svg_card import SvgCardContainer
from osdag_gui.ui.components.home.navbar import VerticalMenuBar
from osdag_gui.ui.components.custom_buttons import MenuButton
from osdag_gui.ui.components.home.top_right_buttons import TopButton, DropDownButton
from osdag_gui.ui.components.home.home_widget import HomeWidget

# --- Internet Connectivity Indicator Button ---
class InternetConnectionIndicator(TopButton):
    """
    Updates a TopButton's icon pair (default + hover)
    when connectivity changes.
    """
    def __init__(self, connectivity, button):
        self.connectivity = connectivity
        self.button = button

        # Connect signal
        self.connectivity.online_status_changed.connect(self.update_status)
        self.update_status(self.connectivity.is_online())

    @Slot(bool)
    def update_status(self, online: bool):
        """Change the Indicator icons based on internet status."""
        if online:
            self.button.black_icon_path = ":/vectors/internet_connected_default.svg"
            self.button.white_icon_path = ":/vectors/internet_connected_hover.svg"
            self.button.label_text = " Online"
        else:
            self.button.black_icon_path = ":/vectors/internet_disconnected_default.svg"
            self.button.white_icon_path = ":/vectors/internet_disconnected_hover.svg"
            self.button.label_text = " Offline"

        # Update the icon immediately to reflect state
        if self.button.is_hovering:
            self.button.setIcon(QIcon(self.button.white_icon_path))
        else:
            self.button.setIcon(QIcon(self.button.black_icon_path))

# --- Theme Toggle Button ---
class ThemeToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = parent.theme_manager
        self.setFixedSize(50, 50)
        self.setObjectName("themeToggle")
        self.setCursor(Qt.PointingHandCursor)
        self.update_icon()
        self.clicked.connect(self._toggle_theme)

    def _toggle_theme(self):
        self.theme.toggle_theme()
        self.update_icon()

    def update_icon(self):
        if self.theme.is_light():
            icon_path = ":/vectors/day_button.svg"
        else:
            icon_path = ":/vectors/night_button.svg"
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(25, 25))

class BackgroundSvgWidget(QWidget):
    def __init__(self, svg_light, svg_dark, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.theme = parent.theme_manager
        self.is_light = True
        self.light = QSvgRenderer(svg_light)
        self.dark = QSvgRenderer(svg_dark)
        self.pixmap = None
        self.setObjectName("svg_widget_background")
        self.setContentsMargins(0, 0, 0, 0) # Ensure no margins for drawing

    def updatePixmap(self):
        size = self.size()
        if not size.isValid():
            return
        renderer = self.light if self.theme.is_light() else self.dark
        self.pixmap = QPixmap(size)
        self.pixmap.fill(Qt.transparent)
        painter = QPainter(self.pixmap)
        # Draw SVG background
        renderer.render(painter, QRectF(0, 0, size.width(), size.height()))
        # Draw left border
        pen = painter.pen()
        border_color = QColor("#90AF13")
        pen.setColor(border_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, self.height())
        painter.end()

    def resizeEvent(self, event):
        self.updatePixmap()

    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)
        # XOR of both values to check if they differ
        if (self.is_light and not self.theme.is_light()) or (not self.is_light and self.theme.is_light()):
            self.is_light = not self.is_light
            self.updatePixmap()

# --- End of background_svg_widget.py content ---
class FadeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self._opacity = 1.0
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

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
    openProject = Signal(dict)
    openModule = Signal(str)
    cardOpenClicked = Signal(str)  # Signal to propagate upward
    triggerLoadOsi = Signal()
    downloadDatabase = Signal(str, str)
    def __init__(self):
        super().__init__()
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Get theme manager from app instance
        self.app = QApplication.instance()
        self.theme_manager = self.app.theme_manager
    
        dat = Data()
        self.menu_bar_data = dat.MODULES
        floating_navbar = dat.FLOATING_NAVBAR
        navbar_icons = dat.NAVBAR_ICONS

        self.current_primary_button = None
        self.current_secondary_button = None

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        
        # Horizontal line separating titleBar and tabWidget
        self.bottom_line = QWidget()
        self.bottom_line.setObjectName("BottomLine")
        self.bottom_line.setFixedHeight(1)
        main_v_layout.addWidget(self.bottom_line)

        main_h_layout = QHBoxLayout()
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        # Left Navigation Bar
        self.nav_bar = VerticalMenuBar(self.menu_bar_data, navbar_icons)
        self.nav_bar.nav_bar_trigger.connect(self.nav_trigger)

        main_h_layout.addWidget(self.nav_bar, 2)

        self.content = BackgroundSvgWidget(":/vectors/background_light.svg", ":/vectors/background_dark.svg", parent=self)

        content_v_layout = QVBoxLayout(self.content)
        content_v_layout.setContentsMargins(0, 0, 0, 0)
        content_v_layout.setSpacing(0)

        # --- Top Horizontal Layout with SVG and Widget ---
        self.top_right_container = QWidget()
        self.top_right_container.setObjectName("home_top_right_container")

        self.top_right_h_layout = QHBoxLayout(self.top_right_container)
        self.top_right_h_layout.setContentsMargins(10, 5, 10, 0)
        self.top_right_h_layout.setSpacing(10)
        self.top_right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.top_svg_widget_1 = QSvgWidget()
        self.top_svg_widget_1.setFixedSize(181, 80)
        # No explicit stylesheet for QSvgWidget here. It will rely on its parent's background.
        self.top_right_h_layout.addWidget(self.top_svg_widget_1)

        self.top_widget_2 = QHBoxLayout()
        self.top_widget_2.setContentsMargins(0, 0, 15, 0)
        self.top_widget_2.setSpacing(2)
        self.button_group = QButtonGroup(self)
        self.buttons = [] # Store references to the created buttons

        # Instantiate and add the Buttons
        for i, (black_icon, white_icon, label, submenu_data) in enumerate(floating_navbar):
            if i==0 or i==1:
                button = DropDownButton(black_icon, white_icon, label, submenu_data)
                button.downloadDatabase.connect(self.downloadDatabase)
            else:
                button = TopButton(black_icon, white_icon, label)

            if label.strip() == "Import":
                button.clicked.connect(lambda checked=False: self.triggerLoadOsi.emit())
            
            self.buttons.append(button)
            self.button_group.addButton(button, i) # Add button to the group with an ID
            self.top_widget_2.addWidget(button)

        # # --- Internet Connectivity Indicator ---
        # internet_connectivity = QApplication.instance().internet_connectivity
        # internet_connectivity.start_monitoring()
        # connectivityButton = TopButton(
        #     ":/vectors/internet_disconnected_default.svg",
        #     ":/vectors/internet_disconnected_hover.svg",
        #     ""
        # )
        # self.top_widget_2.addWidget(connectivityButton)
        # self.internet_status = InternetConnectionIndicator(internet_connectivity, connectivityButton)

        # --- Theme Toggle Button ---
        self.theme_toggle = ThemeToggleButton(self)
        self.top_widget_2.addWidget(self.theme_toggle)

        self.top_right_h_layout.addStretch(1)
        self.top_right_h_layout.addLayout(self.top_widget_2)

        content_v_layout.addWidget(self.top_right_container)

        # Single SVG Widget below the top horizontal layout (now a wrapper QWidget) ---
        self.middle_top_svg_layout_wrapper_widget = QWidget() # The wrapper widget
        self.middle_top_svg_layout_wrapper_widget.setObjectName("mid_top_svg_lay_wrapper")
        self.middle_top_svg_layout_wrapper = QHBoxLayout(self.middle_top_svg_layout_wrapper_widget) # Layout inside wrapper

        self.middle_top_svg_widget = QSvgWidget()
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
        self.primary_menu_container.setObjectName("pr_menu_container")
        # Set margins on the FadeWidget itself, not just its internal layout
        self.primary_menu_container.setContentsMargins(10, 30, 10, 0) # These margins will be part of the painted area
        self.primary_menu_layout = QHBoxLayout(self.primary_menu_container)
        self.primary_menu_layout.setContentsMargins(0, 0, 0, 0) # Reset internal layout margins to 0
        self.primary_menu_layout.setSpacing(5)
        self.primary_menu_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.variable_layout.addWidget(self.primary_menu_container)

        # Secondary Menu Container
        self.secondary_menu_container = FadeWidget()
        self.secondary_menu_container.setObjectName("sec_menu_container")
        # Set margins on the FadeWidget itself
        self.secondary_menu_container.setContentsMargins(10, 5, 10, 5) # These margins will be part of the painted area
        self.secondary_menu_layout = QHBoxLayout(self.secondary_menu_container)
        self.secondary_menu_layout.setContentsMargins(0, 0, 0, 0) # Reset internal layout margins to 0
        self.secondary_menu_layout.setSpacing(5)
        self.secondary_menu_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.secondary_menu_container.setMaximumHeight(0)
        self.secondary_menu_container.setOpacity(0.0)
        self.secondary_menu_container.hide()
        self.secondary_menu_hidden = True
        self.variable_layout.addWidget(self.secondary_menu_container)

        # --- QScrollArea for SVG Card Area ---
        self.scroll_area_for_svg_cards = QScrollArea()
        self.scroll_area_for_svg_cards.setObjectName("svgCard_scroll_area")
        self.scroll_area_for_svg_cards.setWidgetResizable(True)
        self.scroll_area_for_svg_cards.setFrameShape(QFrame.NoFrame)

        self.svg_card_area = QWidget()
        self.svg_card_area.setObjectName("svg_card_area")

        self.svg_card_layout = QVBoxLayout(self.svg_card_area)
        self.svg_card_layout.setContentsMargins(10,10,10,10)
        self.svg_card_layout.setSpacing(10)
        self.svg_card_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area_for_svg_cards.setWidget(self.svg_card_area)
        self.variable_layout.addWidget(self.scroll_area_for_svg_cards, 1)

        content_v_layout.addWidget(self.variable_widget)

        # --- Bottom Horizontal Layout with three SVG Widgets ---
        self.bottom_right_container = QWidget()
        self.bottom_right_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        self.bottom_right_h_layout = QHBoxLayout(self.bottom_right_container)
        self.bottom_right_h_layout.setContentsMargins(10, 10, 0, 10)
        self.bottom_right_h_layout.setSpacing(20)
        self.bottom_right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.bottom_svg_widget_1 = QSvgWidget()
        self.bottom_svg_widget_1.setFixedSize(130, 60)         # 1032 x 479 ~ 130 x 60
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_1)

        self.bottom_svg_widget_2 = QSvgWidget()
        self.bottom_svg_widget_2.setFixedSize(122, 60)
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_2)

        self.bottom_svg_widget_4 = QSvgWidget()
        self.bottom_svg_widget_4.setFixedSize(58, 60)
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_4)

        self.bottom_svg_widget_3 = QSvgWidget()
        self.bottom_svg_widget_3.setFixedSize(350, 40)
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_3, alignment=Qt.AlignmentFlag.AlignBottom)

        self.bottom_right_h_layout.addStretch(1)

        content_v_layout.addWidget(self.bottom_right_container)

        main_h_layout.addWidget(self.content, 8)       
        main_v_layout.addLayout(main_h_layout)

        self.show_home()

    def paintEvent(self, event: QPaintEvent):
        if self.theme_manager.is_light():
            self.top_svg_widget_1.load(":/vectors/Osdag_label_light.svg")
            self.middle_top_svg_widget.load(":/vectors/Osdag_tagline_light.svg")
            self.bottom_svg_widget_1.load(":/vectors/MOE_light.svg")
            self.bottom_svg_widget_2.load(":/vectors/MOS_light.svg")
            self.bottom_svg_widget_3.load(":/vectors/ConstructSteel_light.svg")
            self.bottom_svg_widget_4.load(":/vectors/INSDAG_light.svg")
        else:
            self.top_svg_widget_1.load(":/vectors/Osdag_label_dark.svg")
            self.middle_top_svg_widget.load(":/vectors/Osdag_tagline_dark.svg")
            self.bottom_svg_widget_1.load(":/vectors/MOE_dark.svg")
            self.bottom_svg_widget_2.load(":/vectors/MOS_dark.svg")
            self.bottom_svg_widget_3.load(":/vectors/ConstructSteel_dark.svg")
            self.bottom_svg_widget_4.load(":/vectors/INSDAG_dark.svg")
        return super().paintEvent(event)

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

        if name == 'Home':
            self.show_home()

        elif isinstance(menu_bar_data, list):
            # zero level menu bar
            svg_card_widget = SvgCardContainer(menu_bar_data)
            svg_card_widget.cardOpenClicked.connect(self.handle_card_open_clicked)
            self._clear_layout(self.svg_card_layout)

            label = QLabel(name)
            label.setObjectName("module_section_label")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

            self.svg_card_layout.addWidget(label)
            self.svg_card_layout.addStretch()
            self.svg_card_layout.addWidget(svg_card_widget)
            self.svg_card_layout.addStretch()
            self.primary_menu_container.hide()
            svg_card_widget.cardOpenClicked.connect(self.cardOpenClicked)

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
        home_widget.openProject.connect(self.openProject)
        home_widget.openModule.connect(self.openModule)
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

