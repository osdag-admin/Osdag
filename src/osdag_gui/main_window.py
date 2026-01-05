"""
Main application window for Osdag GUI.
Handles tab management, docking icons, and main window controls.
"""
import osdag_gui.resources.resources_rc

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal

import sys
import os, yaml
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QFileDialog,
    QMainWindow, QTabBar, QTabWidget,
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QTimer
from PySide6.QtGui import QIcon, QGuiApplication, QPixmap

from osdag_gui.ui.windows.home_window import HomeWindow
from osdag_gui.ui.windows.template_page import CustomWindow
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType

from osdag_gui.data.database.database_config import PROJECT_PATH, ID, update_project_path, delete_project_record

from osdag_gui.data.database.database_config import get_module_function
from osdag_core.Common import *
# Backend Class Imports
from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection
from osdag_core.design_type.connection.cleat_angle_connection import CleatAngleConnection
from osdag_core.design_type.connection.seated_angle_connection import SeatedAngleConnection
from osdag_core.design_type.connection.end_plate_connection import EndPlateConnection
from osdag_core.design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from osdag_core.design_type.tension_member.tension_bolted import Tension_bolted
from osdag_core.design_type.tension_member.tension_welded import Tension_welded
from osdag_core.design_type.connection.lap_joint_welded import LapJointWelded
from osdag_core.design_type.connection.lap_joint_bolted import LapJointBolted
from osdag_core.design_type.connection.butt_joint_bolted import ButtJointBolted
from osdag_core.design_type.connection.butt_joint_welded import ButtJointWelded
from osdag_core.design_type.compression_member.compression_welded import Compression_welded
from osdag_core.design_type.compression_member.compression_bolted import Compression_bolted
from osdag_core.design_type.plate_girder.weldedPlateGirder import PlateGirderWelded
from osdag_core.design_type.compression_member.compression_column import ColumnDesign
from osdag_core.design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from osdag_core.design_type.connection.beam_cover_plate import BeamCoverPlate
from osdag_core.design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
from osdag_core.design_type.connection.column_end_plate import ColumnEndPlate
from osdag_core.design_type.connection.column_cover_plate import ColumnCoverPlate
from osdag_core.design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from osdag_core.design_type.connection.base_plate_connection import BasePlateConnection
from osdag_core.design_type.flexural_member.flexure import Flexure
from osdag_core.design_type.flexural_member.flexure_purlin import Flexure_Purlin
from osdag_core.design_type.flexural_member.flexure_cantilever import Flexure_Cantilever

import openpyxl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget_instance = None
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.setCursor(Qt.CursorShape.ArrowCursor)
        # Apply global QToolTip stylesheet here

        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        app = QApplication.instance()
        self.theme = app.theme_manager

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

        # Initialize UI first, as sidebar will overlay it
        self.init_ui() # Call init_ui before sidebar creation to ensure main content exists
        self.handle_add_tab("Home")

        # Using QTimer to delay maximizing until after the window is fully initialized
        # Before maximizing, so that when we click on Restore it comes to normal state.
        QTimer.singleShot(0, self.showMaximized)

        # Ensure correct deletion on close
        self.setAttribute(Qt.WA_DeleteOnClose, True)


    def init_ui(self):
        # Main Vertical Layout for the entire window's *content*
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_v_layout = QVBoxLayout(central_widget)
        main_v_layout.setContentsMargins(1, 0, 1, 1)
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
        
        # Keep a reference for event filtering (double-click to maximize/restore)
        self.icon_label_widget = icon_label_widget

        tabs_h_layout = QHBoxLayout()
        tabs_h_layout.setSpacing(0)
        tabs_h_layout.setContentsMargins(0, 2, 0, 0)

        # QTabBar
        self.tab_bar = QTabBar()
        self.tab_bar.setObjectName("main_tabs")
        self.tab_bar.setExpanding(False)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(False)
        self.tab_bar.tabCloseRequested.connect(self.handle_close_tab)
        tabs_h_layout.addWidget(self.tab_bar)
        top_h_layout.addLayout(tabs_h_layout)
        
        # Install event filters for double-click maximize/restore on title widgets
        self.tab_bar.installEventFilter(self)
        self.icon_label_widget.installEventFilter(self)

        # Stretch to push buttons to the right
        top_h_layout.addStretch(1)

        # Helper function to create a styled button
        def create_button(icon_svg, is_close=False):
            btn = QPushButton()
            btn.setFixedSize(self.btn_size)
            btn.setIcon(QIcon(QPixmap.fromImage(QPixmap(icon_svg).toImage())))
            btn.setIconSize(QSize(14, 14))
            if is_close:
                btn.setObjectName("close_button")
            else:
                btn.setObjectName("window_control_button")
            return btn

        self.minimize_button = create_button(":/vectors/window_minimize_light.svg")
        self.minimize_button.clicked.connect(self.showMinimized)
        top_h_layout.addWidget(self.minimize_button)

        self.maximize_button = create_button(":/vectors/window_maximize_light.svg")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        top_h_layout.addWidget(self.maximize_button)

        self.close_button = create_button(":/vectors/window_close_light.svg", is_close=True)
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
        self.tab_widget_content = []
        self.tab_widget.tabCloseRequested.connect(self.handle_close_tab)
        main_v_layout.addWidget(self.tab_widget)

        # Connect the QTabBar to custom handler
        self.tab_bar.currentChanged.connect(self.handle_tab_change)

        # Ensure initial synchronization
        if self.tab_bar.count() > 0:
            self.tab_widget.setCurrentIndex(self.tab_bar.currentIndex())

    def paintEvent(self, event):
        if self.theme.is_light():
            self.minimize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_minimize_light.svg").toImage())))
            self.close_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_close_light.svg").toImage())))
            if self.isMaximized():
                self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_restore_light.svg").toImage())))
            else:
                self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_maximize_light.svg").toImage())))

        else:
            self.minimize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_minimize_dark.svg").toImage())))
            self.close_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_close_dark.svg").toImage())))
            if self.isMaximized():
                self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_restore_dark.svg").toImage())))
            else:
                self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_maximize_dark.svg").toImage())))

        super().paintEvent(event)

    def set_maximize_icon(self):
        if self.theme.is_light():
            self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_maximize_light.svg").toImage())))
        else:
            self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_maximize_dark.svg").toImage())))

    def set_restore_icon(self):
        if self.theme.is_light():
            self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_restore_light.svg").toImage())))
        else:
            self.maximize_button.setIcon(QIcon(QPixmap.fromImage(QPixmap(":/vectors/window_restore_dark.svg").toImage())))

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
        # Widget of the Module
        self.tab_widget_content.append(body_widget)
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

        # print("@[New Tab Added]Total Widgets. ", len(QApplication.allWidgets()))

    def handle_tab_change(self, index):
        # Switch the QTabWidget to the new tab
        if index < len(self.tab_widget_content) and index >= 0:
            self.tab_widget.setCurrentIndex(index)

            # Update main_widget_instance to the main widget in the current tab
            body_widget = self.tab_widget_content[index]
            if hasattr(body_widget, 'layout') and body_widget.layout().count() > 0:
                widget_item = body_widget.layout().itemAt(0)
                if widget_item is not None:
                    widget = widget_item.widget()
                    if widget is not None:
                        self.main_widget_instance = widget
            # Update main_widget_layout to the layout of the current tab's body_widget
            if hasattr(body_widget, 'layout'):
                self.main_widget_layout = body_widget.layout()

    # This is triggered by Quit button in Menu bar on template_page
    def close_current_tab(self):
        current_index = self.tab_bar.currentIndex()
        self.handle_close_tab(current_index)

    # General closing function
    def handle_close_tab(self, index):

        tab_title = self.tab_bar.tabText(index) if index >= 0 else "Module"
        is_last_tab = self.tab_widget.count() == 1
        to_save = self._check_design_done(index)
        module = self._get_template_instance(index)
        
        if to_save and is_last_tab:
            result = CustomMessageBox(
                title="Confirm Exit",
                text=(
                    f"'{tab_title}' is the last tab.\n"
                     "Closing it will exit Osdag.\n"
                    f"Do you want to save your '{tab_title}' design before closing?"
                ),
                buttons=["Save and Exit", "Exit Without Saving", "Cancel"]
            ).exec()
            
            if result == "Save and Exit":
                # Call Save Function
                module.saveDesign_inputs()
                # Exit Osdag
                self.close()
            elif result == "Exit Without Saving":
                # Exit Osdag
                self.close()
        
        elif to_save:
            result = CustomMessageBox(
                title="Save Design",
                text=f" Do you want to Save Your '{tab_title}' design before closing?",
                buttons=["Yes", "No"],
                dialogType=MessageBoxType.Warning,
            ).exec()

            if result == "Yes":
                # Call Save Function
                module.saveDesign_inputs()
                self._close_tab(index)
            elif result == "No":
                # Close Tab
                self._close_tab(index)

        elif is_last_tab:
            result = CustomMessageBox(
                title="Confirm Exit",
                text=f"'{tab_title}' is the last tab.\nClosing it will exit Osdag.\nDo you really want to close this tab?",
                buttons=["Yes", "No"],
                dialogType=MessageBoxType.Warning,
            ).exec()

            # Handle result
            if result == "Yes":
                self.close()  # Close the main window (exit Osdag)
        else:
            self._close_tab(index)

    # Check if design is created in the module or not
    def _check_design_done(self, index) -> bool:
        module = self._get_template_instance(index)
        if hasattr(module, 'backend'):
            return module.backend.design_status
        else:
            return False

    
    def _get_template_instance(self, index) -> object:
        return self.tab_widget_content[index].layout().itemAt(0).widget()

    def clear_layout(self, layout):
        """Properly clear layout with signal disconnection and widget cleanup."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                try:
                    widget.setUpdatesEnabled(False)
                    widget.blockSignals(True)
                    widget.hide()
                    
                    # Disconnect specific signals if they exist
                    signals = ['openNewTab', 'downloadDatabase', 'triggerLoadOsi',
                            'openProject', 'openModule', 'cardOpenClicked']
                    
                    for sig in signals:
                        if hasattr(widget, sig):
                            try:
                                getattr(widget, sig).disconnect()
                            except:
                                pass
                    
                    widget.setParent(None)
                    widget.deleteLater()
                except (RuntimeError, TypeError):
                    pass
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self.clear_layout(sub_layout)
                    sub_layout.deleteLater()

    def _cleanup_scroll_area(self, scroll_area):
        """Special cleanup for QScrollArea widgets."""
        from PySide6.QtWidgets import QScrollArea
        
        if not isinstance(scroll_area, QScrollArea):
            return
        
        try:
            # Get and clean the viewport widget
            viewport = scroll_area.viewport()
            if viewport:
                viewport_widget = scroll_area.widget()
                if viewport_widget:
                    self.delete_all_children(viewport_widget)
                    viewport_widget.setParent(None)
                    viewport_widget.deleteLater()
                
                # Clear the scroll area
                scroll_area.setWidget(None)
                
        except (RuntimeError, AttributeError) as e:
            print(f"[ERROR] Error cleaning scroll area: {e}")

    def _close_tab(self, index):
        """Close tab with comprehensive cleanup."""
        widget = self.tab_widget.widget(index)
        
        # print(f"\n@Before cleanup - Total Widgets: {len(QApplication.allWidgets())}")
        
        template_instance = self._get_template_instance(index)
        
        if template_instance:
            try:
                # Disable updates immediately
                template_instance.setUpdatesEnabled(False)
                template_instance.blockSignals(True)
                template_instance.hide()
                
                # Find and clean all scroll areas first (they create the container widgets)
                from PySide6.QtWidgets import QScrollArea
                scroll_areas = template_instance.findChildren(QScrollArea)
                for scroll_area in scroll_areas:
                    self._cleanup_scroll_area(scroll_area)
                
                # Recursively delete all children
                self.delete_all_children(template_instance)
                
                # Finally delete the template instance itself
                template_instance.setParent(None)
                template_instance.deleteLater()
                        
            except (RuntimeError, AttributeError) as e:
                print(f"[ERROR] Error in pre-cleanup: {e}")
        
        # Remove from UI structures
        self.tab_widget.removeTab(index)
        self.tab_bar.removeTab(index)
        self.tab_widget_content.pop(index)
        
        if widget:
            widget.setParent(None)
            widget.deleteLater()
        
        self._synchronize_tab_widget()
        
        # Force immediate processing of deferred deletions
        QApplication.processEvents()
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # print(f"@After cleanup - Total Widgets: {len(QApplication.allWidgets())}\n")
    
    def delete_all_children(self, widget):
            """
            Recursively delete all child widgets of the given widget.
            Traverses depth-first, deleting only QWidget children on the way back up.
            """
            from PySide6.QtWidgets import QWidget
            
            # Get all immediate children
            children = widget.children()
            
            # Recursively process each child
            for child in children:
                # Only process QWidget instances
                if isinstance(child, QWidget):
                    # First, recursively delete this child's children
                    self.delete_all_children(child)
                    
                    # Then delete this child itself
                    child.deleteLater()

    def _synchronize_tab_widget(self):
        current_index = self.tab_bar.currentIndex()
        self.tab_widget.setCurrentIndex(current_index)
        # Update global variables and icons
        body_widget = self.tab_widget_content[current_index]
        if hasattr(body_widget, 'layout') and body_widget.layout().count() > 0:
            widget = body_widget.layout().itemAt(0).widget()
            self.main_widget_instance = widget
        # Ensure main_widget_layout points to the currently active tab's layout
        if hasattr(body_widget, 'layout'):
            self.main_widget_layout = body_widget.layout()

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
        
        # restore holding cursor so cursor can update
        self.unsetCursor()
        QApplication.restoreOverrideCursor()
        self.releaseMouse()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Toggle maximize/restore when double-clicking in the draggable title area
        if event.button() == Qt.LeftButton:
            draggable_height = self.tab_bar.height() + (self.layout().contentsMargins().top() * 2)
            if event.position().y() < draggable_height:
                self.toggle_maximize_restore()

    def eventFilter(self, obj, event):
        # Handle double-click on title widgets (e.g., tab bar, logo area)
        if event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.LeftButton:
                self.toggle_maximize_restore()
                return True
        return super().eventFilter(obj, event)

    def handle_card_open_clicked(self, card_title):
        # print(f"[INFO] Card opened: {card_title}")

        #----------Shear-Connections--------------
        if card_title == "Fin Plate":
            self.open_fin_plate_shear_conn()
        elif card_title == "Cleat Angle":
            self.open_cleat_angle_shear_conn()
        elif card_title == "Header Plate":
            self.open_header_plate_shear_conn()
        elif card_title == "Seated Angle":
            self.open_seated_angle_shear_conn()

        #----------Beam-to-Column-Connections--------------
        elif card_title == "End Plate":
            self.open_btc_end_plate_moment_conn() 

        #----------Beam-to-Beam-Connections--------------
        elif card_title == "Cover Plate Welded":
            self.open_btb_cover_plate_weld_moment_conn()
        elif card_title == "Cover Plate Bolted":
            self.open_btb_cover_plate_bolt_moment_conn()
        elif card_title == "Beam Beam End Plate":
            self.open_btb_end_plate_moment_conn()

        #----------Column-to-Column-Connections--------------
        elif card_title == "Column Cover Plate Bolted":
            self.open_ctc_cover_plate_bolt_moment_conn()
        elif card_title == "Column Cover Plate Welded":
            self.open_ctc_cover_plate_weld_moment_conn()
        elif card_title == "Column End Plate":
            self.open_ctc_end_plate_moment_connection()

        #----------Simple-Connections--------------
        elif card_title == "Lap Joint Welded":
            self.open_lap_joint_welded_simple_conn()
        elif card_title == "Lap Joint Bolted":
            self.open_lap_joint_bolted_simple_conn()
        elif card_title == "Butt Joint Bolted":
            self.open_butt_joint_bolted_simple_conn()
        elif card_title == "Butt Joint Welded":
            self.open_butt_joint_welded_simple_conn()

        #----------Tension-Member--------------
        elif card_title == "Bolted to End Gusset":
            self.open_tension_bolted()
        elif card_title == "Welded to End Gusset":
            self.open_tension_welded()

        #----------Compression-Member--------------
        elif card_title == "Column Design":
            self.open_column_design_compress_member()
        elif card_title == "Struts Welded to End Gusset":
            self.open_struts_weld_end_gusset_compress_member()
        elif card_title == "Struts Bolted to End Gusset":
            self.open_struts_bolted_end_gusset_compress_member()

        #----------Flexure-Member--------------
        elif card_title == "Simply Supported Beam":
            self.open_simply_supported_beam_flexure()
        elif card_title == "Cantilever Beam":
            self.open_cantilever_beam_flexure()
        elif card_title == "Plate Girder":
            self.open_plate_girder_flexure()
        elif card_title == "Purlin":
            self.open_purlin_flexure()

        #---------Base Plate Connection------------------
        elif card_title == "Base Plate Connection":
            self.open_base_plate_conn()


    #-------------Functions-to-load-modules-in-Tabwidget-START---------------------------

    def common_open_module(self, backend_class, title):
        self.clear_layout(self.main_widget_layout)
        template_page = CustomWindow(title, backend_class, parent=self)

        # Load the last Design Inputs-start------------------------------------
        last_design_folder = os.path.join('ResourceFiles', 'last_designs')
        last_design_file = str(template_page.backend.module_name()).replace(' ', '') + ".osi"
        last_design_file = os.path.join(last_design_folder, last_design_file)
        last_design_dictionary = {}

        # Create folder if it doesn't exist
        if not os.path.isdir(last_design_folder):
            os.makedirs(last_design_folder)

        # Load previous design if file exists
        if os.path.isfile(last_design_file):
            with open(str(last_design_file), 'r') as last_design:
                last_design_dictionary = yaml.safe_load(last_design)
                template_page.setDictToUserInputs(last_design_dictionary)
        # Load the last Design Inputs-end------------------------------------

        self.main_widget_instance = template_page
        template_page.openNewTab.connect(self.handle_add_tab)
        template_page.downloadDatabase.connect(self.download_Database)
        self.main_widget_layout.addWidget(template_page)
        index = self.tab_bar.currentIndex()
        self.tab_bar.setTabText(index, title)

    # 1-Fin-plate-shear-connection
    def open_fin_plate_shear_conn(self):
        self.common_open_module(FinPlateConnection, "Fin Plate Connection")

    # 2-Cleat-angle-shear-connection
    def open_cleat_angle_shear_conn(self):
        self.common_open_module(CleatAngleConnection, "Cleat Angle Connection")

    # 3-Header-plate-shear-connection
    def open_header_plate_shear_conn(self):
        self.common_open_module(EndPlateConnection, "Header Plate Connection")  
    
    # 4-Seated-angle-shear-connection
    def open_seated_angle_shear_conn(self):
        self.common_open_module(SeatedAngleConnection, "Seated Angle Connection")
    
    # 5-Beam-to-Column-end-plate-moment-connection
    def open_btc_end_plate_moment_conn(self):
        self.common_open_module(BeamColumnEndPlate, "Beam Column End Plate Connection")

    # 6-Beam-to-Beam-cover-plate-welded-moment-connection
    def open_btb_cover_plate_weld_moment_conn(self):
        self.common_open_module(BeamCoverPlateWeld, "Beam Beam Cover Plate Welded")

    # 7-Beam-to-Beam-cover-plate-bolted-moment-connection
    def open_btb_cover_plate_bolt_moment_conn(self):
        self.common_open_module(BeamCoverPlate, "Beam Beam Cover Plate Bolted")
        
    # 8-Beam-to-Beam-end-plate-splice-moment-connection
    def open_btb_end_plate_moment_conn(self):
        self.common_open_module(BeamBeamEndPlateSplice, "Beam Beam End Plate")

    # 9-Column-to-Column-end-plate-moment-connection
    def open_ctc_end_plate_moment_connection(self):
        self.common_open_module(ColumnEndPlate, "Column End plate")    

    # 10-Column-to-Column-cover-plate-bolted-moment-connection
    def open_ctc_cover_plate_bolt_moment_conn(self):
        self.common_open_module(ColumnCoverPlate, "Column Cover Plate Bolted")
        
    # 11-Column-to-Column-cover-plate-welded-moment-connection
    def open_ctc_cover_plate_weld_moment_conn(self):
        self.common_open_module(ColumnCoverPlateWeld, "Column Cover Plate Welded")

    # 12-Lap-joint-welded-simple-Connection
    def open_lap_joint_welded_simple_conn(self):
        self.common_open_module(LapJointWelded, "Lap Joint Welded Connection")

    # 13-Lap-joint-bolted-simple-connection
    def open_lap_joint_bolted_simple_conn(self):
        self.common_open_module(LapJointBolted, "Lap Joint Bolted Connection")
        
    # 14-Butt-joint-bolted-simple-connection
    def open_butt_joint_bolted_simple_conn(self):
        self.common_open_module(ButtJointBolted, "Butt Joint Bolted Connection")

    # 15-Butt-joint-welded-simple-connection
    def open_butt_joint_welded_simple_conn(self):
        self.common_open_module(ButtJointWelded, "Butt Joint Welded Connection") 

    # 16-Bolted-to-End-Gusset-Tension-Member
    def open_tension_bolted(self):
        self.common_open_module(Tension_bolted, "Tension Member: Bolted to End Gusset")
 
    # 17-Welded-to-End-Gusset-Tension-Member
    def open_tension_welded(self):
        self.common_open_module(Tension_welded, "Tension Member: Welded to End Gusset")     
 
    # 18-Column-design-Compression-Member
    def open_column_design_compress_member(self):
        self.common_open_module(ColumnDesign, "Column Design")

    # 19-Struts-welded-to-end-gusset-compression-member
    def open_struts_weld_end_gusset_compress_member(self):
        self.common_open_module(Compression_welded, "Struts: Welded to End Gusset")

    def open_struts_bolted_end_gusset_compress_member(self):
        self.common_open_module(Compression_bolted, "Struts: Bolted to End Gusset")

    # 20-Simply-Supported-Beam-Flexure-member
    def open_simply_supported_beam_flexure(self):
        self.common_open_module(Flexure, "Simply Supported Beam")
        
    # 21-Cantilever-Beam-Flexure-member
    def open_cantilever_beam_flexure(self):
        self.common_open_module(Flexure_Cantilever, "Cantilever Beam")

    # 22-Plate-girder
    def open_plate_girder_flexure(self):
        self.common_open_module(PlateGirderWelded, "Plate Girder")  

    # 23-Flexure-purlin
    def open_purlin_flexure(self):
        self.common_open_module(Flexure_Purlin, "Purlin")

    # 24-Base-Plate-connection
    def open_base_plate_conn(self):
        self.common_open_module(BasePlateConnection, "Base Plate Connection")

    def open_home_page(self, module):
        self.clear_layout(self.main_widget_layout)
        home_window = HomeWindow()
        home_window.triggerLoadOsi.connect(self.common_osi_load)
        home_window.openProject.connect(self.handle_open_project)
        home_window.openModule.connect(self.handle_open_module)
        home_window.downloadDatabase.connect(self.download_Database)
        self.main_widget_instance = home_window
        home_window.set_active_button(module)
        home_window.cardOpenClicked.connect(self.handle_card_open_clicked)
        self.main_widget_layout.addWidget(home_window)

    # To open the recent module
    def handle_open_module(self, key:str):
        func = get_module_function(key)
        if func != 'None':
            func = getattr(self, func)
            func() # Open the Releated Module

    # To handle the click on open project of any recent project
    def handle_open_project(self, record: dict):
        self.common_osi_load(osi_path=record.get(PROJECT_PATH), id=record.get(ID))

    # Common function to load osi file and also to open recent project
    # If osi_path=None -> it triggers Load Osi else trigger open recent project
    def common_osi_load(self, osi_path=None, id=None):
        if osi_path is None:
            osi_path, _ = QFileDialog.getOpenFileName(self, "Open Design", os.path.join(str(' ')),
                                                  "InputFiles(*.osi)")
            
        else:
            if not Path(osi_path).exists():
                result = CustomMessageBox(
                    title="Warning",
                    text="Osi File has been moved, File does not exist!",
                    dialogType=MessageBoxType.Warning,
                    buttons=["Locate Osi", "Remove Record"]
                ).exec()
                if result == "Locate Osi":
                    file_dialog_path, _ = QFileDialog.getOpenFileName(self, "Locate Osi File", os.path.expanduser("~"), "InputFiles(*.osi)")
                    if file_dialog_path and id is not None:
                        osi_path = file_dialog_path
                        new_name = Path(osi_path).stem
                        try:
                            update_project_path(id, osi_path, new_name)
                        except Exception as e:
                            print(f"[ERROR] Failed to update project path: {e}")
                    else:
                        print("[INFO] No file selected for relocation.")
                        return
                elif result == "Remove Record":
                    print("[INFO] Remove Record")
                    if id is not None:
                        try:
                            delete_project_record(id)
                            # Also delete the latex files for this project
                            import shutil
                            report_folder = f"osdag_gui/data/reports/file_{id}"
                            try:
                                shutil.rmtree(report_folder)
                            except FileNotFoundError:
                                pass
                            except Exception as e:
                                print(f"[ERROR] Failed to delete report folder: {e}")
                            CustomMessageBox(
                                title="Record Removed",
                                text="The record has been removed from recent projects.",
                                dialogType=MessageBoxType.Information
                            ).exec()
                            # Update Home page with deleted project
                            self.main_widget_instance.show_home()

                        except Exception as e:
                            CustomMessageBox(
                                title="Error",
                                text=f"Failed to remove record: {e}",
                                dialogType=MessageBoxType.Critical
                            ).exec()
                    else:
                        print("[INFO] No ID provided for record removal.")
                    return

        if not osi_path:
            print("[INFO] No Path selected!")
            return
        try:
            in_file = str(osi_path)
            with open(in_file, 'r') as fileObject:
                uiObj = yaml.safe_load(fileObject)
            module = uiObj[KEY_MODULE]

            print(f"[INFO] Osi File Belongs to: {module}")

            func = get_module_function(module)
            if func == 'None':
                CustomMessageBox(
                    title="Information",
                    text="Please load the appropriate Input",
                    dialogType=MessageBoxType.Information
                ).exec()
                print("[INFO] Module Under Development.")
                return
            func = getattr(self, func)
            func()
            # Set variables in template page because it is opened project
            self.main_widget_instance.setDictToUserInputs(uiObj)
            self.main_widget_instance.project_id = id

        except IOError:
            CustomMessageBox(
                title="Unable to open file",
                text="There was an error opening \"%s\"" % osi_path,
                dialogType=MessageBoxType.Critical
            ).exec()
            return    

    #-------------Functions-to-load-modules-in-Tabwidget-END------------------------------------

    #----------------------------Download-Database/Excel-END-----------------------------------------
    def download_Database(self, table, call_type="database"):

        default_dir = os.path.join(get_documents_folder(), str(table+"_Details.xlsx"))
        fileName, _ = QFileDialog.getSaveFileName(  QFileDialog(), 
                                                    "Download File",
                                                    default_dir,
                                                    "SectionDetails(*.xlsx)"
                                                )
        if not fileName:
            return
        try:
            conn = sqlite3.connect(PATH_TO_DATABASE)
            c = conn.cursor()
            header = get_db_header(table)
            wb = openpyxl.Workbook()
            sheet = wb.create_sheet(table, 0)

            col = 1
            for head in header:
                sheet.cell(row=1, column=col).value = head
                col += 1
            if call_type != "header":
                if table == 'Columns':
                    c.execute("SELECT * FROM Columns")
                elif table == 'Beams':
                    c.execute("SELECT * FROM Beams")
                elif table == 'Angles':
                    c.execute("SELECT * FROM Angles")
                elif table == 'Channels':
                    c.execute("SELECT * FROM Channels")
                data = c.fetchall()
                conn.commit()
                c.close()
                row = 2
                for rows in data:
                    col = 1
                    for cols in range(len(header)):
                        sheet.cell(row=row, column=col).value = rows[col - 1]
                        col += 1
                    row += 1
            wb.save(fileName)
            CustomMessageBox(
                title='Information',
                text='Your File is Downloaded.',
                dialogType=MessageBoxType.Information
            ).exec()

        except IOError:
            CustomMessageBox(
                title='Information',
                text='Unable to save file',
                informativeText="There was an error saving \"%s\"" % fileName,
                dialogType=MessageBoxType.Information
            ).exec()
            return
    def closeEvent(self, event):
        """Explicitly schedule deletion on close."""
        self.delete_all_children(self)
        event.accept()
        self.deleteLater()

    #----------------------------Download-Database/Excel--END----------------------------------------

# if __name__ == "__main__":
#     import sys, os
#     from osdag_gui.ui.utils.theme_manager import ThemeManager
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#     from PySide6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     app.theme_manager = ThemeManager(app)
#     app.setStyle("Fusion")
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec())
    
    
    
