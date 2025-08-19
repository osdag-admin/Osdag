"""
Main application window for Osdag GUI.
Handles tab management, docking icons, and main window controls.
"""
import osdag_gui.resources.resources_rc

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread, Signal

import sys
import os
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGridLayout,
    QLabel, QMainWindow, QSizePolicy, QFrame, QScrollArea, QButtonGroup, QTabBar, QTabWidget,
    QMessageBox
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QRect, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QGuiApplication, QPixmap
from PySide6.QtSvg import QSvgRenderer

from osdag_gui.ui.windows.home_window import HomeWindow
from osdag_gui.ui.windows.template_page import CustomWindow

from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget_instance = None

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
            QMainWindow {
                background-color: #fff;
                margin: 0px;
                padding: 0px;
            }  
        """)

        # Initialize UI first, as sidebar will overlay it
        self.init_ui() # Call init_ui before sidebar creation to ensure main content exists
        self.handle_add_tab("Home")

        # self.maximize_button.click()

    def init_ui(self):
        # Main Vertical Layout for the entire window's *content*
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_v_layout = QVBoxLayout(central_widget)
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
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
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
        self.input_dock_control.clicked.connect(self.toggle_input_dock)
        self.input_dock_active = True
        control_button_layout.addWidget(self.input_dock_control)

        self.log_dock_control = ClickableSvgWidget()
        self.log_dock_control.load(":/vectors/logs_dock_inactive.svg")
        self.log_dock_control.setFixedSize(18, 18)
        self.log_dock_control.clicked.connect(self.logs_dock_icon_toggle)
        self.log_dock_active = False
        control_button_layout.addWidget(self.log_dock_control)

        self.output_dock_control = ClickableSvgWidget()
        self.output_dock_control.load(":/vectors/output_dock_inactive.svg")
        self.output_dock_control.setFixedSize(18, 18)
        self.output_dock_control.clicked.connect(self.toggle_output_dock)
        self.output_dock_active = False
        control_button_layout.addWidget(self.output_dock_control)

        self.input_dock_control.hide()
        self.log_dock_control.hide()
        self.output_dock_control.hide()

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

        # QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.tabBar().hide()
        self.tab_widget.setTabsClosable(True) # Allow closing tabs
        self.tab_widget.setMovable(False) # Allow reordering tabs
        self.tab_widget.setStyleSheet("""
            QTabWidget {
                border: 0px;
            }
        """)
        self.tab_widget_content = []
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        main_v_layout.addWidget(self.tab_widget)

        # Connect the QTabBar to custom handler
        self.tab_bar.currentChanged.connect(self.handle_tab_change)

        # Ensure initial synchronization
        if self.tab_bar.count() > 0:
            self.tab_widget.setCurrentIndex(self.tab_bar.currentIndex())

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

    def add_new_tab(self, module):
        """Helper to add a new tab to QTabWidget."""
        body_widget = QWidget()
        
        # Create and set layout for body_widget first
        self.main_widget_layout = QHBoxLayout(body_widget)
        self.main_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget_layout.setSpacing(0)

        # it initially sets the home on the Tab
        self.open_home_page(module)
        # False(dock icons show status), True(input dock show), False(logs dock show), False(output dock show)
        self.tab_widget_content.append([body_widget, False, True, False, False])
        self.tab_widget.addTab(body_widget, f"Tab {self.current_tab_index + 1}")
        # Update main_widget_layout to the layout of the new tab's body_widget
        if hasattr(body_widget, 'layout'):
            self.main_widget_layout = body_widget.layout()

    def handle_add_tab(self, module):
        """Handles the 'Add New Tab' button click."""
        self.current_tab_index += 1
        self.tab_bar.addTab("Home") # Add to tab bar
        # Set the newly added tab as current
        self.add_new_tab(module) # Add to tab widget
        
        new_index = self.tab_bar.count() - 1
        self.tab_bar.setCurrentIndex(new_index)
        self.tab_widget.setCurrentIndex(new_index)
        # Update docking icons for the newly added tab
        current_tab_data = self.tab_widget_content[new_index]
        self.update_docking_icons(current_tab_data[1], current_tab_data[2], current_tab_data[3], current_tab_data[4])
        
        # self.sidebar.raise_() # Ensure sidebar stays on top after new tab addition

    def handle_tab_change(self, index):
        # 1. Switch the QTabWidget to the new tab
        self.tab_widget.setCurrentIndex(index)

        if len(self.tab_widget_content)>0:
            if self.tab_bar.tabText(index) == "Home":
                self.tab_widget_content[index][1] = False
            else:
                self.tab_widget_content[index][1] = True
            current_tab_data = self.tab_widget_content[index]
            self.update_docking_icons(current_tab_data[1], current_tab_data[2], current_tab_data[3], current_tab_data[4])
            
            # Update main_widget_instance to the main widget in the current tab
            body_widget = self.tab_widget_content[index][0]
            if hasattr(body_widget, 'layout') and body_widget.layout().count() > 0:
                widget_item = body_widget.layout().itemAt(0)
                if widget_item is not None:
                    widget = widget_item.widget()
                    if widget is not None:
                        self.main_widget_instance = widget
            # Update main_widget_layout to the layout of the current tab's body_widget
            if hasattr(body_widget, 'layout'):
                self.main_widget_layout = body_widget.layout()

        # 2. Update dock icons based on the new tab's state
        if index < len(self.tab_widget_content):
            current_tab_data = self.tab_widget_content[index]
            self.update_docking_icons(current_tab_data[1], current_tab_data[2], current_tab_data[3], current_tab_data[4])
    
    def update_docking_icons(self, docking_icons_active=None, input_is_active=None, log_is_active=None, output_is_active=None):
        index = self.tab_bar.currentIndex()
        current_tab_data = self.tab_widget_content[index]
        if(docking_icons_active is None):
            docking_icons_active = current_tab_data[1]

        # Update input dock icon
        if docking_icons_active:
            self.input_dock_control.show()
            self.output_dock_control.show()
            self.log_dock_control.show()
            if(input_is_active is not None):
                self.input_dock_active = input_is_active
                if self.input_dock_active:
                    self.input_dock_control.load(":/vectors/input_dock_active.svg")
                else:
                    self.input_dock_control.load(":/vectors/input_dock_inactive.svg")
                            
            # Update output dock icon
            if(output_is_active is not None):
                self.output_dock_active = output_is_active
                if self.output_dock_active:
                    self.output_dock_control.load(":/vectors/output_dock_active.svg")
                else:
                    self.output_dock_control.load(":/vectors/output_dock_inactive.svg")

            # Update log dock icon
            if(log_is_active is not None):
                self.log_dock_active = log_is_active
                if self.log_dock_active:
                    self.log_dock_control.load(":/vectors/logs_dock_active.svg")
                else:
                    self.log_dock_control.load(":/vectors/logs_dock_inactive.svg")
        else:
            self.input_dock_control.hide()
            self.output_dock_control.hide()
            self.log_dock_control.hide()

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

        if self.tab_widget.count() > 0:
            current_index = self.tab_widget.currentIndex()
            body_widget = self.tab_widget_content[current_index][0]
            if hasattr(body_widget, 'layout') and body_widget.layout().count() > 0:
                widget_item = body_widget.layout().itemAt(0)
                if widget_item is not None:
                    widget = widget_item.widget()
                    if widget is not None:
                        self.main_widget_instance = widget
            # Show docking Icons
            self.tab_widget_content[current_index][1] = True
            current_tab_data = self.tab_widget_content[index]
            self.update_docking_icons(current_tab_data[1], current_tab_data[2], current_tab_data[3], current_tab_data[4])

    def show_message(self, title, message):
        """Helper function to display a message box."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    # Allow dragging the window when frameless
    def mousePressEvent(self, event):
        # The draggable area is the combined height of the top_h_layout (tab bar + buttons) and the menu_bar
        if self.isMaximized():
            return
        draggable_height = self.tab_bar.height() + (self.layout().contentsMargins().top() * 2) # Account for potential margins/spacing
        # A more robust way might be to check if the cursor is within the bounding box of top_h_layout or menu_bar
        if event.button() == Qt.LeftButton and event.position().y() < draggable_height:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            return
        if hasattr(self, 'old_pos'):
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if self.isMaximized():
            return
        if event.button() == Qt.LeftButton:
            if hasattr(self, 'old_pos'):
                del self.old_pos

    def handle_card_open_clicked(self, card_title):
        if card_title == "Fin Plate":
            self.open_fin_plate_page()

    def open_fin_plate_page(self):
        title = "Fin Plate Connection"
        self.clear_layout(self.main_widget_layout)
        fin_plate = CustomWindow(title, FinPlateConnection, parent=self)

        # dock icon update trigger signal
        fin_plate.outputDockIconToggle.connect(self.output_dock_icon_toggle)
        fin_plate.inputDockIconToggle.connect(self.input_dock_icon_toggle)

        self.main_widget_instance = fin_plate
        fin_plate.openNewTab.connect(self.handle_add_tab)
        self.main_widget_layout.addWidget(fin_plate)
        index = self.tab_bar.currentIndex()
        self.tab_bar.setTabText(index, title)
        # Show docking Icons
        self.tab_widget_content[index][1] = True
        current_tab_data = self.tab_widget_content[index]
        self.update_docking_icons(current_tab_data[1], current_tab_data[2], current_tab_data[3], current_tab_data[4])

    def open_home_page(self, module):
        self.clear_layout(self.main_widget_layout)
        home_window = HomeWindow()
        self.main_widget_instance = home_window
        home_window.set_active_button(module)
        home_window.cardOpenClicked.connect(self.handle_card_open_clicked)
        self.main_widget_layout.addWidget(home_window)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.clear_layout(item.layout())  

    def input_dock_icon_toggle(self):
        self.input_dock_active = not self.input_dock_active
        self.tab_widget_content[self.tab_bar.currentIndex()][2] = self.input_dock_active
        if self.input_dock_active:
            self.input_dock_control.load(":/vectors/input_dock_active.svg")
        else:
            self.input_dock_control.load(":/vectors/input_dock_inactive.svg")

    def toggle_input_dock(self):
        if self.main_widget_instance:
            self.main_widget_instance.input_dock_toggle()
        
    def output_dock_icon_toggle(self):
        self.output_dock_active = not self.output_dock_active
        self.tab_widget_content[self.tab_bar.currentIndex()][4] = self.output_dock_active
        if self.output_dock_active:
            self.output_dock_control.load(":/vectors/output_dock_active.svg")
        else:
            self.output_dock_control.load(":/vectors/output_dock_inactive.svg")
    
    def toggle_output_dock(self):
        if self.main_widget_instance:
            self.main_widget_instance.output_dock_toggle()

    def logs_dock_icon_toggle(self):
        self.log_dock_active = not self.log_dock_active
        self.tab_widget_content[self.tab_bar.currentIndex()][3] = self.log_dock_active
        if self.log_dock_active:
            self.log_dock_control.load(":/vectors/logs_dock_active.svg")
        else:
            self.log_dock_control.load(":/vectors/logs_dock_inactive.svg")    

        if self.main_widget_instance:
            self.main_widget_instance.logs_dock_toggle(self.log_dock_active)

if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

