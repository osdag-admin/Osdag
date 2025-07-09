import sys, os
import osdag_gui.resources.resources_rc
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QTabBar,
    QMessageBox, QMenuBar, QMenu
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEvent, Signal
from PySide6.QtGui import QIcon, QFont, QPixmap, QGuiApplication, QKeySequence, QAction

from osdag_gui.ui.components.floating_nav_bar import SidebarWidget
from osdag_gui.ui.components.input_dock import InputDock
from osdag_gui.ui.components.output_dock import OutputDock

class CustomWindow(QWidget):
    def __init__(self, title: str):
        super().__init__()

        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        screen_width = screen_size.width()
        screen_height = screen_size.height()

        # Calculate window size
        window_width = int(7 * screen_width / 10)
        window_height = int((7 * screen_height) / 8)

        # Set window size
        self.resize(window_width, window_height)

        # Center the window
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.setGeometry(x, y, window_width, window_height)
        self.setWindowFlags(Qt.FramelessWindowHint) # Make the window frameless for custom buttons
        self.current_tab_index = 0 # To keep track of the next tab index
        self.btn_size = QSize(46, 30)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                margin: 0px;
                padding: 0px;
            }
            /* Style for the QMenuBar */
            QMenuBar {
                background-color: #F4F4F4;
                color: #000000;
                padding: 0px;
            }
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
                border-radius: 0px;
            }
            QMenuBar::item:selected { /* when selected via keyboard or mouse */
                background: #FFFFFF; /* Light grey background on hover/selection */
            }
            QMenuBar::item:pressed {
                background: #E8E8E8; /* Darker grey when pressed */
            }

            /* Style for QMenu (dropdown menus) */
            QMenu {
                background-color: #FFFFFF; /* White background for dropdown */
                border: 1px solid #D0D0D0; /* Light grey border */
                border-radius: 4px;
                padding: 0px; /* Padding inside the menu */
            }
            QMenu::item {
                padding: 5px;
                color: #000000;
                font-size: 11px;
            }
            QMenu::item:selected {
                background-color: #E6F0FF;
                border-radius: 3px;
            }
            QMenu::separator {
                height: 1px;
                background: #F0F0F0; /* Separator line color */
                margin-left: 2px;
                margin-right: 2px;
                margin-top: 0px;
                margin-bottom: 0px;
            }
            QMenu::right-arrow {
                width: 8px;
                height: 8px;
            }
        """)

        # Initialize UI first, as sidebar will overlay it
        self.init_ui(title) # Call init_ui before sidebar creation to ensure main content exists

        # Create sidebar - IMPORTANT: Set parent AFTER init_ui sets up main layout
        self.sidebar = SidebarWidget(parent=self)
        self.sidebar.setParent(self) # Keep sidebar as a direct child of CustomWindow
        self.sidebar.resize_sidebar(self.width(), self.height()) # Initial resize based on window
        # Initial position: mostly hidden, adjusted for new layout
        self.sidebar.move(-self.sidebar.width() + 12, self.menu_bar.height() + self.tab_bar.height())

        # Setup animation for the sidebar's geometry
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.sidebar_animation.setDuration(300)
        self.sidebar.installEventFilter(self) # Install event filter for mouse events
        self.sidebar.raise_() # Ensure sidebar is always on top of other widgets

        self.handle_add_tab(title)

    def resizeEvent(self, event):
        # When the main window resizes, resize the sidebar to match its height
        self.sidebar.resize_sidebar(self.sidebar.width(), self.height())

        # If the sidebar is currently hidden (peeked), adjust its position based on new width
        # This check prevents it from jumping if it's already fully out.
        # Adjusted Y based on top bar elements (top_h_layout and menu_bar)
        top_offset = self.menu_bar.height() + self.tab_bar.height()
        # self.y = top_offset
        if self.sidebar.x() < 0: # If it's mostly hidden
            self.sidebar.move(-self.sidebar.width() + 12, top_offset) # Re-position with updated width

        # Ensure the sidebar stays on top after resize
        self.sidebar.raise_()

        super().resizeEvent(event)

    def eventFilter(self, watched, event):
        if watched == self.sidebar:
            if event.type() == QEvent.Enter:
                self.slide_in()
            elif event.type() == QEvent.Leave:
                self.slide_out()
        return super().eventFilter(watched, event)

    def slide_in(self):
        """Slide the sidebar fully into view from the left edge."""
        self.sidebar_animation.stop()
        end_x = 0
        # Ensure the start value is the current geometry to animate from current position
        self.sidebar_animation.setStartValue(self.sidebar.geometry())
        self.sidebar_animation.setEndValue(QRect(end_x, self.y(), self.sidebar.width(), self.sidebar.height()))
        self.sidebar_animation.start()
        self.sidebar.raise_() # Keep sidebar on top during and after animation

    def slide_out(self):
        """Slide the sidebar out to leave only 12px visible on the left.""" # Adjusted to 12px for consistency
        self.sidebar_animation.stop()
        end_x = -self.sidebar.width() + 12 # Use 12px for consistency with initial move
        self.sidebar_animation.setStartValue(self.sidebar.geometry())
        self.sidebar_animation.setEndValue(QRect(end_x, self.y(), self.sidebar.width(), self.sidebar.height()))
        self.sidebar_animation.start()

    def init_ui(self, title: str):
        # Main Vertical Layout for the entire window's *content*
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)

        # --- Top HBox Layout (Contains logo, tabs, and window control buttons) ---
        top_h_layout = QHBoxLayout()
        top_h_layout.setContentsMargins(0, 0, 0, 0)
        top_h_layout.setSpacing(0)

        icon_label_widget = QWidget()
        icon_label_h_layout = QHBoxLayout(icon_label_widget)
        icon_label_h_layout.setContentsMargins(5, 0, 5, 0)
        icon_label_h_layout.setSpacing(0)

        # SVG Widget (Dummy SVG for demonstration)
        self.svg_widget = QSvgWidget()
        self.svg_widget.load(":/vectors/Osdag_logo.svg")
        self.svg_widget.setFixedSize(18, 18)

        icon_label_h_layout.addWidget(self.svg_widget)
        top_h_layout.addWidget(icon_label_widget)

        # QTabBar
        self.tab_bar = QTabBar()
        self.tab_bar.setExpanding(False)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(False)
        self.tab_bar.tabCloseRequested.connect(self.close_tab_bar_tab)
        # Custom tab style
        self.tab_bar.setStyleSheet('''
            QTabBar::tab {
                background: #ffffff;
                border-left: 1px solid #F4F4F4;
                border-right: 1px solid #F4F4F4;
                border-top: 1px solid #FFFFFF;
                border-bottom: 1px solid #FFFFFF;
                padding: 6px 18px 6px 18px;
                color: #000000;
                font-size: 11px;
                margin-left: 0px;
            }
            QTabBar::tab:selected {
                background: #F4F4F4;
                color: #000000;
                border: 1px solid #90AF13;
                border-bottom: 1px solid #F4F4F4;
                padding: 6px 18px 6px 18px;
            }
            QTabBar::tab:hover {
                border-top: 1px solid #90AF13;
                border-left: 1px solid #90AF13;
                border-right: 1px solid #90AF13;
            }
            QTabBar::close-button {
                image: url(:/vectors/window_close.svg);
                subcontrol-origin: padding;
                subcontrol-position: center right;
            }
            QTabBar::close-button:hover {
                image: url(:/vectors/window_close_hover.svg);
            }
        ''')
        top_h_layout.addWidget(self.tab_bar)

        # Stretch to push buttons to the right
        top_h_layout.addStretch(1)

        # Helper function to create a styled button
        def create_button(icon_svg, is_close=False):
            btn = QPushButton()
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    color: white;
                    border: none;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #F4F4F4;
                }
                QPushButton:pressed {
                    background-color: #FAFAFA;
                }
                QPushButton#close_button:hover {
                    background-color: #E81123;
                }
                QPushButton#close_button:pressed {
                    background-color: #F1707A;
                }
            """)
            btn.setFixedSize(self.btn_size)
            btn.setIcon(QIcon(QPixmap.fromImage(QPixmap(icon_svg).toImage())))
            btn.setIconSize(QSize(14, 14))
            if is_close:
                btn.setObjectName("close_button")
            return btn

        class ClickableSvgWidget(QSvgWidget):
            clicked = Signal()  # Define a custom clicked signal
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setCursor(Qt.CursorShape.PointingHandCursor)

            def mousePressEvent(self, event):
                if event.button() == Qt.MouseButton.LeftButton:
                    self.clicked.emit()  # Emit the clicked signal on left-click
                super().mousePressEvent(event)

        # Control buttons
        control_button_layout = QHBoxLayout()
        control_button_layout.setSpacing(10)
        control_button_layout.setContentsMargins(5,5,5,5)

        self.input_dock_control = ClickableSvgWidget()
        self.input_dock_control.load(":/vectors/input_dock_active.svg")
        self.input_dock_control.setFixedSize(18, 18)
        self.input_dock_control.clicked.connect(self.input_dock_toggle)
        self.input_dock_active = True
        control_button_layout.addWidget(self.input_dock_control)

        self.output_dock_control = ClickableSvgWidget()
        self.output_dock_control.load(":/vectors/output_dock_inactive.svg")
        self.output_dock_control.setFixedSize(18, 18)
        self.output_dock_control.clicked.connect(self.output_dock_toggle)
        self.output_dock_active = False
        control_button_layout.addWidget(self.output_dock_control)

        top_h_layout.addLayout(control_button_layout)

        self.minimize_button = create_button(":/vectors/window_minimize.svg")
        self.minimize_button.clicked.connect(self.showMinimized)
        top_h_layout.addWidget(self.minimize_button)

        self.maximize_button = create_button(":/vectors/window_maximize.svg")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        top_h_layout.addWidget(self.maximize_button)

        self.close_button = create_button(":/vectors/window_close.svg", is_close=True)
        self.close_button.clicked.connect(self.close)
        top_h_layout.addWidget(self.close_button)

        self.start_pos = None
        self.start_geometry = None

        # Add top HBox to main VBox
        main_v_layout.addLayout(top_h_layout)

        # --- Menu Bar ---
        self.menu_bar = QMenuBar(self) # Create a QMenuBar instance
        main_v_layout.addWidget(self.menu_bar) # Add it to the top of the main layout, AFTER top_h_layout
        self.create_menu_bar_items() # Call a new method to populate the menu bar


        # --- Bottom Vertical Layout (for TabWidget) ---
        center_v_layout = QVBoxLayout()
        center_v_layout.setContentsMargins(0, 0, 0, 0) # Padding for the bottom content
        center_v_layout.setSpacing(0)

        # QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.tabBar().hide()
        self.tab_widget.setTabsClosable(True) # Allow closing tabs
        self.tab_widget.setMovable(False) # Allow reordering tabs
        self.tab_widget.setStyleSheet("""
            QTabWidget {
                border: 1px solid #F4F4F4;
            }
        """)
        self.tab_widget_content = []
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        center_v_layout.addWidget(self.tab_widget)

        # Add bottom VBox to main VBox
        main_v_layout.addLayout(center_v_layout)

        # Connect QTabBar to QTabWidget
        # self.tab_bar.currentChanged.connect(self.tab_widget.setCurrentIndex) # Removed, handled by handle_tab_change
        # self.tab_widget.currentChanged.connect(self.tab_bar.setCurrentIndex)

        # Connect the QTabBar to custom handler
        self.tab_bar.currentChanged.connect(self.handle_tab_change)

        # Ensure initial synchronization
        if self.tab_bar.count() > 0:
            self.tab_widget.setCurrentIndex(self.tab_bar.currentIndex())

    def input_dock_toggle(self):
        self.tab_widget_content[self.tab_bar.currentIndex()][1].toggle_input_dock()

    def input_dock_icon_toggle(self):
        self.tab_widget_content[self.tab_bar.currentIndex()][3] = not self.tab_widget_content[self.tab_bar.currentIndex()][3]
        self.input_dock_active = self.tab_widget_content[self.tab_bar.currentIndex()][3]
        if self.input_dock_active:
            self.input_dock_control.load(":/vectors/input_dock_active.svg")
        else:
            self.input_dock_control.load(":/vectors/input_dock_inactive.svg")
        
    def output_dock_toggle(self):
        self.tab_widget_content[self.tab_bar.currentIndex()][2].toggle_output_dock()

    def output_dock_icon_toggle(self):
        self.tab_widget_content[self.tab_bar.currentIndex()][4] = not self.tab_widget_content[self.tab_bar.currentIndex()][4]
        self.output_dock_active = self.tab_widget_content[self.tab_bar.currentIndex()][4]
        if self.output_dock_active:
            self.output_dock_control.load(":/vectors/output_dock_active.svg")
        else:
            self.output_dock_control.load(":/vectors/output_dock_inactive.svg")
        
    def create_menu_bar_items(self):
        """
        Creates the menu bar items (menus and actions) for CustomWindow.
        This content is moved from the previous MainWindow example.
        """
        # --- File Menu ---
        file_menu = self.menu_bar.addMenu("File")

        # Load input action
        load_input_action = QAction("Load Input", self)
        load_input_action.setShortcut(QKeySequence("Ctrl+L"))
        load_input_action.triggered.connect(self.on_load_input)
        file_menu.addAction(load_input_action)

        file_menu.addSeparator()

        # Save input action
        save_input_action = QAction("Save Input", self)
        save_input_action.setShortcut(QKeySequence("Ctrl+S"))
        save_input_action.triggered.connect(self.on_save_input)
        file_menu.addAction(save_input_action)

        # Save log messages action
        save_log_action = QAction("Save Log Messages", self)
        save_log_action.setShortcut(QKeySequence("Alt+M"))
        save_log_action.triggered.connect(self.on_save_log_messages)
        file_menu.addAction(save_log_action)

        # Create design report action
        create_report_action = QAction("Create Design Report", self)
        create_report_action.setShortcut(QKeySequence("Alt+C"))
        create_report_action.triggered.connect(self.on_create_design_report)
        file_menu.addAction(create_report_action)

        file_menu.addSeparator()

        # Save 3D model action
        save_3d_action = QAction("Save 3D Model", self)
        save_3d_action.setShortcut(QKeySequence("Alt+3"))
        save_3d_action.triggered.connect(self.on_save_3d_model)
        file_menu.addAction(save_3d_action)

        # Save CAD image action
        save_cad_action = QAction("Save CAD Image", self)
        save_cad_action.setShortcut(QKeySequence("Alt+I"))
        save_cad_action.triggered.connect(self.on_save_cad_image)
        file_menu.addAction(save_cad_action)

        # Add a separator before Quit
        file_menu.addSeparator()

        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Shift+Q"))
        quit_action.triggered.connect(self.close) # Connect to close the window
        file_menu.addAction(quit_action)

        # --- Edit Menu ---
        edit_menu = self.menu_bar.addMenu("Edit")

        # Design Preferences action
        design_prefs_action = QAction("Design Preferences", self)
        design_prefs_action.setShortcut(QKeySequence("Alt+P"))
        design_prefs_action.triggered.connect(self.on_design_preferences)
        edit_menu.addAction(design_prefs_action)

        # --- Graphics Menu ---
        graphics_menu = self.menu_bar.addMenu("Graphics")

        # Zoom in action
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+I"))
        zoom_in_action.triggered.connect(self.on_zoom_in)
        graphics_menu.addAction(zoom_in_action)

        # Zoom out action
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+O"))
        zoom_out_action.triggered.connect(self.on_zoom_out)
        graphics_menu.addAction(zoom_out_action)

        # Pan action
        pan_action = QAction("Pan", self)
        pan_action.setShortcut(QKeySequence("Ctrl+P"))
        pan_action.triggered.connect(self.on_pan)
        graphics_menu.addAction(pan_action)

        # Rotate 3D model action
        rotate_3d_action = QAction("Rotate 3D Model", self)
        rotate_3d_action.setShortcut(QKeySequence("Ctrl+R"))
        rotate_3d_action.triggered.connect(self.on_rotate_3d_model)
        graphics_menu.addAction(rotate_3d_action)

        graphics_menu.addSeparator()

        # Show front view action
        front_view_action = QAction("Show Front View", self)
        front_view_action.setShortcut(QKeySequence("Alt+Shift+F"))
        front_view_action.triggered.connect(self.on_show_front_view)
        graphics_menu.addAction(front_view_action)

        # Show top view action
        top_view_action = QAction("Show Top View", self)
        top_view_action.setShortcut(QKeySequence("Alt+Shift+T"))
        top_view_action.triggered.connect(self.on_show_top_view)
        graphics_menu.addAction(top_view_action)

        # Show side view action
        side_view_action = QAction("Show Side View", self)
        side_view_action.setShortcut(QKeySequence("Alt+Shift+S"))
        side_view_action.triggered.connect(self.on_show_side_view)
        graphics_menu.addAction(side_view_action)

        # Add a separator
        graphics_menu.addSeparator()

        # Model submenu
        model_view_action = QAction("Model", self)
        graphics_menu.addAction(model_view_action)

        # Beam submenu
        beam_view_action = QAction("Beam", self)
        graphics_menu.addAction(beam_view_action)

        # Column submenu
        column_view_action = QAction("Column", self)
        graphics_menu.addAction(column_view_action)

        # Fin Plate submenu
        fin_plate_view_action = QAction("Fin Plate", self)
        graphics_menu.addAction(fin_plate_view_action)

        graphics_menu.addSeparator()

        # Change background action
        change_bg_action = QAction("Change background", self)
        change_bg_action.triggered.connect(self.on_change_background)
        graphics_menu.addAction(change_bg_action)

        # --- Database Menu ---
        database_menu = self.menu_bar.addMenu("Database")

        # Download submenu (placeholder for further actions)
        download_submenu = database_menu.addMenu("Download")
        download_submenu.addAction(QAction("Column", self))
        download_submenu.addAction(QAction("Beam", self))
        download_submenu.addAction(QAction("Angle", self))
        download_submenu.addAction(QAction("Channel", self))

        # Reset action
        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.on_reset_database)
        database_menu.addAction(reset_action)

        # --- Help Menu ---
        help_menu = self.menu_bar.addMenu("Help")

        # Video Tutorials action
        video_tutorials_action = QAction("Video Tutorials", self)
        video_tutorials_action.triggered.connect(self.on_video_tutorials)
        help_menu.addAction(video_tutorials_action)

        # Design Examples action
        design_examples_action = QAction("Design Examples", self)
        design_examples_action.triggered.connect(self.on_design_examples)
        help_menu.addAction(design_examples_action)

        # Add a separator
        help_menu.addSeparator()

        # Ask Us a Question action
        ask_question_action = QAction("Ask Us a Question", self)
        ask_question_action.triggered.connect(self.on_ask_question)
        help_menu.addAction(ask_question_action)

        # About Osdag action
        about_osdag_action = QAction("About Osdag", self)
        about_osdag_action.triggered.connect(self.on_about_osdag)
        help_menu.addAction(about_osdag_action)

        help_menu.addSeparator()

        # Check For Update action
        check_update_action = QAction("Check For Update", self)
        check_update_action.triggered.connect(self.on_check_for_update)
        help_menu.addAction(check_update_action)

    def set_maximize_icon(self):
        self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_maximize.svg").toImage())))

    def set_restore_icon(self):
        self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_restore.svg").toImage())))

    def toggle_maximize_restore(self):
        """Toggles between maximized and normal window states and updates the icon."""
        if self.isMaximized():
            self.showNormal()
            self.set_maximize_icon()
        else:
            self.showMaximized()
            self.set_restore_icon()
        # After maximize/restore, re-raise the sidebar to ensure it's on top
        if self.sidebar: # Check if sidebar exists
            self.sidebar.raise_()
            # Also re-adjust its position if it's supposed to be peeked
            # Adjust the Y position of the sidebar when maximizing/restoring
            top_offset = self.menu_bar.height() + self.tab_bar.height()
            self.sidebar.move(-self.sidebar.width() + 12, top_offset)


    def add_new_tab(self, content_text):
        """Helper to add a new tab to QTabWidget."""
        # ---------------------------
        body_widget = QWidget()
        tab_layout = QHBoxLayout(body_widget)
        tab_layout.setContentsMargins(0,0,0,0)
        tab_layout.setSpacing(0)

        input_dock = InputDock(parent=self)
        tab_layout.addWidget(input_dock)

        tab_layout.addStretch(1)

        output_dock = OutputDock(parent=self)
        # Initially it will bw hidden
        tab_layout.addWidget(output_dock)
                                                               # input dock active, output dock active
        self.tab_widget_content.append([body_widget, input_dock, output_dock, True, False])    
        # ----------------------------
        self.tab_widget.addTab(body_widget, f"Tab {self.current_tab_index + 1}")

    def handle_add_tab(self, title):
        """Handles the 'Add New Tab' button click."""
        self.current_tab_index += 1
        self.tab_bar.addTab(title) # Add to tab bar
        # Set the newly added tab as current
        self.add_new_tab(f"Content for {title}") # Add to tab widget
        
        new_index = self.tab_bar.count() - 1
        self.tab_bar.setCurrentIndex(new_index)
        self.tab_widget.setCurrentIndex(new_index)
        self.input_dock_active = True
        self.output_dock_active = False
        self.update_docking_icons(self.tab_widget_content[new_index][3], self.tab_widget_content[new_index][4])
        
        self.sidebar.raise_() # Ensure sidebar stays on top after new tab addition

    def handle_tab_change(self, index):
        # 1. Switch the QTabWidget to the new tab
        self.tab_widget.setCurrentIndex(index)
        # self.tab_bar.setCurrentIndex(index)  # Removed, handled by tab_widget.currentChanged sync

        # 2. Update dock icons based on the new tab's state
        if index < len(self.tab_widget_content):
            self.update_docking_icons(self.tab_widget_content[index][3], self.tab_widget_content[index][4])
    
    def update_docking_icons(self, input_active, output_active):
        # Update input dock icon
            if input_active != self.input_dock_active:
                self.input_dock_active = not self.input_dock_active
                if self.input_dock_active:
                    self.input_dock_control.load(":/vectors/input_dock_active.svg")
                else:
                    self.input_dock_control.load(":/vectors/input_dock_inactive.svg")
                            
            if output_active != self.output_dock_active:
                self.output_dock_active = not self.output_dock_active
                if self.output_dock_active:
                    self.output_dock_control.load(":/vectors/output_dock_active.svg")
                else:
                    self.output_dock_control.load(":/vectors/output_dock_inactive.svg")
                
    def close_tab(self, index):
        """Handles closing of tabs."""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
            self.tab_bar.removeTab(index)
            self.tab_widget_content.pop(index)
            # Adjust current index if the closed tab was the last one
            if self.tab_widget.currentIndex() == -1 and self.tab_widget.count() > 0:
                self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
        else:
            # Using QMessageBox for information instead of alert()
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Cannot close the last tab.")
            msg_box.setWindowTitle("Information")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    def close_tab_bar_tab(self, index):
        """Handles closing of tabs from the QTabBar close button."""
        if self.tab_bar.count() > 1:
            self.tab_bar.removeTab(index)
            self.tab_widget.removeTab(index)
            if self.tab_bar.currentIndex() == -1 and self.tab_bar.count() > 0:
                self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
                self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Cannot close the last tab.")
            msg_box.setWindowTitle("Information")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

    # --- Slot methods for menu actions ---
    # These methods are placeholders. In a real application, they would
    # contain the actual logic for each menu item.

    def show_message(self, title, message):
        """Helper function to display a message box."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def on_load_input(self):
        self.show_message("Action", "Load input selected.")

    def on_save_input(self):
        self.show_message("Action", "Save input selected.")

    def on_save_log_messages(self):
        self.show_message("Action", "Save log messages selected.")

    def on_create_design_report(self):
        self.show_message("Action", "Create design report selected.")

    def on_save_3d_model(self):
        self.show_message("Action", "Save 3D model selected.")

    def on_save_cad_image(self):
        self.show_message("Action", "Save CAD image selected.")

    def on_design_preferences(self):
        self.show_message("Action", "Design Preferences selected.")

    def on_zoom_in(self):
        self.show_message("Action", "Zoom in selected.")

    def on_zoom_out(self):
        self.show_message("Action", "Zoom out selected.")

    def on_pan(self):
        self.show_message("Action", "Pan selected.")

    def on_rotate_3d_model(self):
        self.show_message("Action", "Rotate 3D model selected.")

    def on_show_front_view(self):
        self.show_message("Action", "Show front view selected.")

    def on_show_top_view(self):
        self.show_message("Action", "Show top view selected.")

    def on_show_side_view(self):
        self.show_message("Action", "Show side view selected.")

    def on_change_background(self):
        self.show_message("Action", "Change background selected.")

    def on_reset_database(self):
        self.show_message("Action", "Database Reset selected.")

    def on_video_tutorials(self):
        self.show_message("Action", "Video Tutorials selected.")

    def on_design_examples(self):
        self.show_message("Action", "Design Examples selected.")

    def on_ask_question(self):
        self.show_message("Action", "Ask Us a Question selected.")

    def on_about_osdag(self):
        self.show_message("Action", "About Osdag selected.")

    def on_check_for_update(self):
        self.show_message("Action", "Check For Update selected.")

    # Allow dragging the window when frameless
    def mousePressEvent(self, event):
        # The draggable area is the combined height of the top_h_layout (tab bar + buttons) and the menu_bar
        draggable_height = self.tab_bar.height() + self.menu_bar.height() + (self.layout().contentsMargins().top() * 2) # Account for potential margins/spacing
        # A more robust way might be to check if the cursor is within the bounding box of top_h_layout or menu_bar
        if event.button() == Qt.LeftButton and event.position().y() < draggable_height:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'old_pos'):
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self, 'old_pos'):
                del self.old_pos


if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    app = QApplication(sys.argv)
    window = CustomWindow("Fin Plate Connection")
    window.show()
    sys.exit(app.exec())
