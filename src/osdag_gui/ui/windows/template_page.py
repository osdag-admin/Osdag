import sys, os, yaml, time, gc
import osdag_gui.resources.resources_rc
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog,  QCheckBox, QComboBox, QLineEdit,
    QMenuBar, QSplitter, QSizePolicy, QDialog
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEvent, Signal, QTimer
from PySide6.QtGui import QKeySequence, QAction, QColor, QBrush

from osdag_gui.ui.components.floating_nav_bar import SidebarWidget
from osdag_gui.ui.components.docks.input_dock import InputDock
from osdag_gui.ui.components.docks.output_dock import OutputDock
from osdag_gui.ui.components.docks.log_dock import LogDock
from osdag_gui.ui.components.dialogs.loading_popup import LoadingDialogManager
from osdag_gui.ui.components.dialogs.custom_messagebox import CustomMessageBox, MessageBoxType
from osdag_gui.ui.components.dialogs.video_tutorials import TutorialsDialog
from osdag_gui.ui.components.dialogs.ask_questions import AskQuestions
from osdag_gui.ui.components.dialogs.about_osdag import AboutOsdagDialog
from osdag_gui.common_functions import design_examples

from osdag_core.Common import *

from osdag_gui.ui.windows.design_preferences import AdditionalInputs
from osdag_core.cad.common_logic import CommonDesignLogic
from osdag_gui.data.database.database_config import *

from osdag_gui.__config__ import CAD_BACKEND

class CustomWindow(QWidget):
    openNewTab = Signal(str)
    downloadDatabase = Signal(str, str)
    def __init__(self, title: str, backend: object, parent):
        super().__init__()
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.parent = parent
        self.backend = backend()

        app = QApplication.instance()
        self.theme = app.theme_manager

        # Update recent Modules
        insert_recent_module(self.backend.module_name())
        # State to retain state saved or not
        self.save_state = False
        # Saved Project
        self.project_id = None

        self.current_tab_index = 0
        self.input_dock = None
        self.output_dock = None
        self.design_pref_inputs = {}
        self.prev_inputs = {}
        self.input_dock_inputs = {}
        self.design_inputs = {}
        self.folder = ' '
        self.display_mode = 'Normal'
        self._did_apply_initial_sizes = False
        self.ui_loaded = False
        self.backend.design_status = False
        self.backend.design_button_status = False
        self.fuse_model = None
        self._pso_manager = None  # Lazy init for Plate Girder PSO UI management
        self.setObjectName("template_page")

        # This initializes the cad Window in specific backend 
        self.display, _ = self.init_display(backend_str=CAD_BACKEND)
        self.designPrefDialog = AdditionalInputs(self.backend, self, input_dictionary=self.input_dock_inputs)
        self.designPrefDialog.ui.downloadDatabase.connect(self.downloadDatabase)

        self.init_ui(title)
        self.sidebar = SidebarWidget(parent=self)
        self.sidebar.openNewTab.connect(self.openNewTabEmit)
        self.sidebar.resize_sidebar(self.width(), self.height())
        # Center sidebar vertically within the content area (below menu bar)
        self.sidebar_y = self.height()//2 - self.sidebar.height()//4
        self.sidebar.move(-self.sidebar.width() + 12, self.sidebar_y)
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.sidebar_animation.setDuration(150)
        self.sidebar.installEventFilter(self)
        self.sidebar.raise_()
        
    def closeEvent(self, event):
        """Handle window close event to ensure proper resource cleanup."""
        # Cleanup PSO resources if they exist
        if hasattr(self, '_pso_manager') and self._pso_manager:
            try:
                self._pso_manager.cleanup()
            except Exception:
                pass
        super().closeEvent(event)

    #---------------------------------CAD-SETUP-START----------------------------------------------

    def init_display(self, backend_str=None, size=(1024, 768)):

        from OCC.Display.backend import load_backend, get_qt_modules

        used_backend = load_backend(backend_str)
        # print(f"used_backend {used_backend}")

        global display, start_display, app, _, USED_BACKEND
        if 'qt' in used_backend:
            from OCC.Display.qtDisplay import qtViewer3d
            QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

        from OCC.Display.qtDisplay import qtViewer3d
        from osdag_gui.ui.components.custom_3dviewer import CustomViewer3d

        self.cad_widget = CustomViewer3d(self)
        self.cad_widget.setFocusPolicy(Qt.StrongFocus)
        self.cad_widget.setCursor(Qt.CursorShape.ArrowCursor)
        self.cad_widget.setFocus()
        self.cad_widget.setMouseTracking(True)
        
        # Defer InitDriver to after widget is shown to prevent UI blocking
        # This is critical for cross-platform (especially Linux) stability
        self._cad_init_pending = True
        QTimer.singleShot(100, self._deferred_init_driver)

        # These will be set after deferred init
        display = None
        
        def start_display():
            self.cad_widget.raise_()

        return display, start_display
    
    def _deferred_init_driver(self):
        """Initialize OpenGL driver after widget is visible (prevents blocking)."""
        try:
            if hasattr(self, 'cad_widget') and self.cad_widget and self._cad_init_pending:
                self.cad_widget.InitDriver()
                self._cad_init_pending = False
                
                # Complete the CAD setup that depends on InitDriver
                self._complete_cad_init()
                
                # Process events to ensure UI remains responsive
                QApplication.processEvents()
                
        except Exception as e:
            print(f"[WARNING] OpenGL initialization failed: {e}")
            print("[INFO] 3D view may be unavailable. Try setting LIBGL_ALWAYS_SOFTWARE=1")
            self._cad_init_pending = False
    
    def _is_display_ready(self):
        """Check if the CAD display is initialized and ready to use."""
        return (hasattr(self, 'display') and 
                self.display is not None and
                hasattr(self, '_cad_init_pending') and
                not self._cad_init_pending)
    
    def _complete_cad_init(self):
        """Complete CAD initialization after InitDriver succeeds."""
        try:
            self.display = self.cad_widget._display
            self.cad_widget.context = self.display.Context
            self.cad_widget.view = self.display.View
            # to store model objects
            self.cad_widget.model_ais_objects = {}

            # Disable automatic highlighting to prevent flickering borders
            self.cad_widget.context.SetAutomaticHilight(False)
            
            # Display View Cube
            self.cad_widget.display_view_cube()

            key_function = {Qt.Key.Key_Up: lambda: self.Pan_Rotate_model("Up"),
                            Qt.Key.Key_Down: lambda: self.Pan_Rotate_model("Down"),
                            Qt.Key.Key_Right: lambda: self.Pan_Rotate_model("Right"),
                            Qt.Key.Key_Left: lambda: self.Pan_Rotate_model("Left")}
            self.cad_widget._key_map.update(key_function)

            # background gradient
            self.display.display_triedron()
            self.display.View.SetProj(1, 1, 1)
            
            print("[INFO] 3D CAD viewer initialized successfully")
            
            # Trigger repaint to apply background colors now that display is ready
            self.update()
            
        except Exception as e:
            print(f"[ERROR] Failed to complete CAD initialization: {e}")

    
    def paintEvent(self, event):
        # Guard: Skip CAD display operations if not initialized yet (deferred init)
        cad_ready = (hasattr(self, 'cad_widget') and 
                     self.cad_widget is not None and 
                     hasattr(self.cad_widget, '_display') and 
                     self.cad_widget._display is not None and
                     not getattr(self, '_cad_init_pending', True))
        
        if cad_ready:
            if self.theme.is_light():
                self.cad_widget._display.set_bg_gradient_color([255, 255, 255], [126, 126, 126])
            else:
                self.cad_widget._display.set_bg_gradient_color([83, 83, 83], [0, 0, 0])
        
        # Update control buttons (these don't depend on CAD init)
        if self.theme.is_light():
            if self.input_dock_active:
                self.input_dock_control.load(":/vectors/input_dock_active_light.svg")
            else:
                self.input_dock_control.load(":/vectors/input_dock_inactive_light.svg")
            
            if self.output_dock_active:
                self.output_dock_control.load(":/vectors/output_dock_active_light.svg")
            else:
                self.output_dock_control.load(":/vectors/output_dock_inactive_light.svg")
            
            if self.log_dock_active:
                self.log_dock_control.load(":/vectors/logs_dock_active_light.svg")
            else:
                self.log_dock_control.load(":/vectors/logs_dock_inactive_light.svg")
        else:
            if self.input_dock_active:
                self.input_dock_control.load(":/vectors/input_dock_active_dark.svg")
            else:
                self.input_dock_control.load(":/vectors/input_dock_inactive_dark.svg")
            
            if self.output_dock_active:
                self.output_dock_control.load(":/vectors/output_dock_active_dark.svg")
            else:
                self.output_dock_control.load(":/vectors/output_dock_inactive_dark.svg")
            
            if self.log_dock_active:
                self.log_dock_control.load(":/vectors/logs_dock_active_dark.svg")
            else:
                self.log_dock_control.load(":/vectors/logs_dock_inactive_dark.svg")
        return super().paintEvent(event)
    # Create the view control button on cad widget
    def create_cad_view_controls(self):
        """Create zoom controls anchored correctly below the view cube"""

        # ---- Configuration (single source of truth) ----
        self._view_cube_size = 75     # OCC default
        self._view_cube_margin = 10   # distance from top-right
        self._zoom_btn_size = 40
        self._zoom_spacing = 6

        # ---- Zoom In Button ----
        self.zoom_in_btn = QPushButton("+", self.cad_widget)
        self.zoom_in_btn.setFixedSize(self._zoom_btn_size, self._zoom_btn_size)
        self.zoom_in_btn.setCursor(Qt.PointingHandCursor)
        self.zoom_in_btn.setToolTip("Zoom In (Ctrl+I)")
        self.zoom_in_btn.clicked.connect(lambda: self.display.ZoomFactor(1.1))
        self._style_zoom_button(self.zoom_in_btn)

        # ---- Zoom Out Button ----
        self.zoom_out_btn = QPushButton("-", self.cad_widget)
        self.zoom_out_btn.setFixedSize(self._zoom_btn_size, self._zoom_btn_size)
        self.zoom_out_btn.setCursor(Qt.PointingHandCursor)
        self.zoom_out_btn.setToolTip("Zoom Out (Ctrl+O)")
        self.zoom_out_btn.clicked.connect(lambda: self.display.ZoomFactor(1 / 1.1))
        self._style_zoom_button(self.zoom_out_btn)

        self.zoom_in_btn.show()
        self.zoom_out_btn.show()

        # ---- Initial positioning ----
        self.position_zoom_buttons()

        # ---- Track resize safely ----
        self._orig_resize_event = self.cad_widget.resizeEvent
        self.cad_widget.resizeEvent = self._cad_resize_proxy


    def _style_zoom_button(self, btn):
        btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                background-color: white;
                border: 1px solid #bdbdbd;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QPushButton:pressed {
                background-color: #d6d6d6;
            }
        """)



    def position_zoom_buttons(self):
        if not hasattr(self, "zoom_in_btn"):
            return

        w = self.cad_widget.width()

        # ---- View cube anchor (top-right) ----
        cube_right = w - self._view_cube_margin
        cube_left = cube_right - self._view_cube_size

        
        cube_render_padding = 14
        cube_bottom = self._view_cube_margin + self._view_cube_size + cube_render_padding

        # ---- Center buttons under cube ----
        center_x = cube_left + (self._view_cube_size // 2)
        btn_x = center_x - (self._zoom_btn_size // 2)

        btn_y_1 = cube_bottom + self._zoom_spacing
        btn_y_2 = btn_y_1 + self._zoom_btn_size + self._zoom_spacing

        self.zoom_in_btn.move(btn_x, btn_y_1)
        self.zoom_out_btn.move(btn_x, btn_y_2)

    def _cad_resize_proxy(self, event):
        if self._orig_resize_event:
            self._orig_resize_event(event)
        self.position_zoom_buttons()


    def on_cad_widget_resize(self, event):
        """Handle canvas resize to reposition buttons"""
        # Call the original resize event if it exists
        if hasattr(self, 'original_resize_event') and self.original_resize_event:
            self.original_resize_event(event)
        
        # Reposition our buttons
        self.position_zoom_buttons()

    # Set Direction on cad window
    def view_front(self):
        """Set front view (looking along negative Y axis)"""
        try:
            view = self.display.View
            view.SetProj(0, -1, 0)  # Look along negative Y
            view.SetUp(0, 0, 1)     # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting front view: {e}")
    
    def view_back(self):
        """Set back view (looking along positive Y axis)"""
        try:
            view = self.display.View
            view.SetProj(0, 1, 0)   # Look along positive Y
            view.SetUp(0, 0, 1)     # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting back view: {e}")
    
    def view_left(self):
        """Set left view (looking along negative X axis)"""
        try:
            view = self.display.View
            view.SetProj(-1, 0, 0)  # Look along negative X
            view.SetUp(0, 0, 1)     # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting left view: {e}")
    
    def view_right(self):
        """Set right view (looking along positive X axis)"""
        try:
            view = self.display.View
            view.SetProj(1, 0, 0)   # Look along positive X
            view.SetUp(0, 0, 1)     # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting right view: {e}")
    
    def view_top(self):
        """Set top view (looking along negative Z axis)"""
        try:
            view = self.display.View
            view.SetProj(0, 0, -1)  # Look along negative Z
            view.SetUp(0, 1, 0)     # Y is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting top view: {e}")
    
    def view_bottom(self):
        """Set bottom view (looking along positive Z axis)"""
        try:
            view = self.display.View
            view.SetProj(0, 0, 1)   # Look along positive Z
            view.SetUp(0, 1, 0)     # Y is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting bottom view: {e}")
    
    def view_iso_top_left(self):
        """Set isometric view from top-left"""
        try:
            view = self.display.View
            view.SetProj(-1, -1, 1)  # Isometric projection
            view.SetUp(0, 0, 1)      # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting top-left isometric view: {e}")
    
    def view_iso_top_right(self):
        """Set isometric view from top-right"""
        try:
            view = self.display.View
            view.SetProj(1, -1, 1)   # Isometric projection
            view.SetUp(0, 0, 1)      # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting top-right isometric view: {e}")
    
    def view_iso_bottom_left(self):
        """Set isometric view from bottom-left"""
        try:
            view = self.display.View
            view.SetProj(-1, -1, -1) # Isometric projection
            view.SetUp(0, 0, 1)      # Z is up
            self.fit_all()
        except Exception as e:
            print(f"[Error] setting bottom-left isometric view: {e}")
    
    def view_iso_bottom_right(self):
        """Set isometric view from bottom-right"""
        try:
            view = self.display.View
            view.SetProj(1, -1, -1)  # Isometric projection
            view.SetUp(0, 0, 1)      # Z is up
            self.fit_all()
        except Exception as e:
            print(f"Error setting bottom-right isometric view: {e}")

    def initial_view(self):
        """Setting initial view"""
        try:
            view = self.display.View
            view.SetProj(1, 1, 1)  # Isometric projection
            view.SetUp(0, 0, 1)    
            self.fit_all()

        except Exception as e:
            print(f"Error setting initial view: {e}")
    
    def fit_all(self):
        """Fit all objects in the view"""
        if not self._is_display_ready():
            return
        try:
            self.display.View.SetProj(1, -1, 1)
            self.display.FitAll()
        except Exception as e:
            print(f"[WARNING] fit_all failed: {e}")
        
    
    #---------------------------------CAD-SETUP-END----------------------------------------------
    
    def openNewTabEmit(self, title: str):
        self.openNewTab.emit(title)

    def eventFilter(self, watched, event):
        if watched == self.sidebar:
            if event.type() == QEvent.Enter:
                self.slide_in()
            elif event.type() == QEvent.Leave:
                self.slide_out()
        return super().eventFilter(watched, event)

    def slide_in(self):
        self.sidebar_animation.stop()
        end_x = 5
        top_offset = self.sidebar_y
        self.sidebar_animation.setStartValue(self.sidebar.geometry())
        self.sidebar_animation.setEndValue(QRect(end_x, top_offset, self.sidebar.width(), self.sidebar.height()))
        self.sidebar_animation.start()
        self.sidebar.raise_()

    def slide_out(self):
        self.sidebar_animation.stop()
        end_x = -self.sidebar.width() + 12
        top_offset = self.sidebar_y
        self.sidebar_animation.setStartValue(self.sidebar.geometry())
        self.sidebar_animation.setEndValue(QRect(end_x, top_offset, self.sidebar.width(), self.sidebar.height()))
        self.sidebar_animation.start()

    def init_ui(self, title: str):
        # Docking icons Parent class
        class ClickableSvgWidget(QSvgWidget):
            clicked = Signal()  # Define a custom clicked signal
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setCursor(Qt.CursorShape.PointingHandCursor)

            def mousePressEvent(self, event):
                if event.button() == Qt.MouseButton.LeftButton:
                    self.clicked.emit()  # Emit the clicked signal on left-click
                super().mousePressEvent(event)

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)

        menu_h_layout = QHBoxLayout()
        menu_h_layout.setContentsMargins(0, 0, 0, 0)
        menu_h_layout.setSpacing(0)

        self.menu_bar = QMenuBar(self)
        self.menu_bar.setObjectName("template_page_menu_bar")
        self.menu_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.menu_bar.setFixedHeight(28)
        self.menu_bar.setContentsMargins(0, 0, 0, 0)
        menu_h_layout.addWidget(self.menu_bar)

        # Control buttons
        control_btn_widget = QWidget()
        control_btn_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        control_btn_widget.setObjectName("control_btn_widget")
        control_button_layout = QHBoxLayout(control_btn_widget)
        control_button_layout.setSpacing(10)
        control_button_layout.setContentsMargins(5,5,5,5)

        self.input_dock_control = ClickableSvgWidget()
        self.input_dock_control.setFixedSize(18, 18)
        self.input_dock_control.load(":/vectors/input_dock_active_light.svg")
        self.input_dock_control.clicked.connect(self.input_dock_toggle)
        self.input_dock_active = True
        control_button_layout.addWidget(self.input_dock_control)

        self.log_dock_control = ClickableSvgWidget()
        self.log_dock_control.load(":/vectors/logs_dock_inactive_light.svg")
        self.log_dock_control.setFixedSize(18, 18)
        self.log_dock_control.clicked.connect(self.logs_dock_toggle)
        self.log_dock_active = False
        control_button_layout.addWidget(self.log_dock_control)

        self.output_dock_control = ClickableSvgWidget()
        self.output_dock_control.load(":/vectors/output_dock_inactive_light.svg")
        self.output_dock_control.setFixedSize(18, 18)
        self.output_dock_control.clicked.connect(self.output_dock_toggle)
        self.output_dock_active = False
        control_button_layout.addWidget(self.output_dock_control)

        menu_h_layout.addWidget(control_btn_widget)

        main_v_layout.addLayout(menu_h_layout)
        self.create_menu_bar_items()

        self.body_widget = QWidget()
        self.layout = QHBoxLayout(self.body_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal, self.body_widget)
        self.splitter.setHandleWidth(2)
        self.input_dock = InputDock(backend=self.backend, parent=self)
        input_dock_width = self.input_dock.sizeHint().width()
        self._input_dock_default_width = input_dock_width
        self.splitter.addWidget(self.input_dock)


        central_widget = QWidget()
        central_H_layout = QHBoxLayout(central_widget)

        # Add dock indicator labels
        self.input_dock_label = InputDockIndicator(parent=self)
        self.input_dock_label.setVisible(False)
        central_H_layout.setContentsMargins(0, 0, 0, 0)
        central_H_layout.setSpacing(0)
        central_H_layout.addWidget(self.input_dock_label, 1)

        central_V_layout = QVBoxLayout()
        central_V_layout.setContentsMargins(0, 0, 0, 0)
        central_V_layout.setSpacing(0)

        # Add cad component checkboxes
        self.cad_comp_widget = CadComponentCheckbox(self.backend, parent=self)
        self.cad_comp_widget.hide()
        central_V_layout.addWidget(self.cad_comp_widget)

        self.cad_log_splitter = QSplitter(Qt.Vertical)
        self.cad_log_splitter.setHandleWidth(2)
        # Add Cad Model Widget
        self.create_cad_view_controls()
        self.cad_log_splitter.addWidget(self.cad_widget)

        self.logs_dock = LogDock(parent=self)
        self.logs_dock.setVisible(False)
        # log text
        self.textEdit = self.logs_dock.log_display
        self.backend.set_osdaglogger(self.textEdit)
        self.cad_log_splitter.addWidget(self.logs_dock)

        # Prefer stretch factors so ratio persists on resize
        self.cad_log_splitter.setStretchFactor(0, 6)
        self.cad_log_splitter.setStretchFactor(1, 1)
        # Seed an initial 6:1 split; will be refined after first show
        self.cad_log_splitter.setSizes([6, 1])

        central_V_layout.addWidget(self.cad_log_splitter)        
        central_H_layout.addLayout(central_V_layout, 6)

        # Add output dock indicator label
        self.output_dock_label = OutputDockIndicator(parent=self)
        self.output_dock_label.setVisible(True)
        central_H_layout.addWidget(self.output_dock_label, 1)
        self.splitter.addWidget(central_widget)

        # root is the greatest level of parent that is the MainWindow
        self.output_dock = OutputDock(backend=self.backend, parent=self)
        self.splitter.addWidget(self.output_dock)
        self.output_dock.hide()

        self.layout.addWidget(self.splitter)

        total_width = self.width() - self.splitter.contentsMargins().left() - self.splitter.contentsMargins().right()
        target_sizes = [0] * self.splitter.count()
        target_sizes[0] = input_dock_width
        target_sizes[2] = 0
        remaining_width = total_width - input_dock_width
        target_sizes[1] = max(0, remaining_width)
        self.splitter.setSizes(target_sizes)
        self.layout.activate()
        main_v_layout.addWidget(self.body_widget)

    # To set the initial sizes correctly when the widgets are loaded
    def showEvent(self, event):
        super().showEvent(event)
        if not self._did_apply_initial_sizes:
            QTimer.singleShot(0, self._apply_initial_splitter_sizes)

    def _apply_initial_splitter_sizes(self):
        if self._did_apply_initial_sizes:
            return
        self._did_apply_initial_sizes = True
        try:
            input_dock_width = self.input_dock.sizeHint().width()
        except Exception:
            input_dock_width = max(180, self.input_dock.width())
        try:
            output_dock_width = self.output_dock.sizeHint().width() if self.output_dock.isVisible() else 0
        except Exception:
            output_dock_width = self.output_dock.width() if self.output_dock.isVisible() else 0

        total_width = self.splitter.width()
        if total_width <= 0:
            total_width = self.width() - self.splitter.contentsMargins().left() - self.splitter.contentsMargins().right()
        remaining_width = max(0, total_width - input_dock_width - output_dock_width)
        sizes = [input_dock_width, remaining_width, output_dock_width]
        self.splitter.setSizes(sizes)
        try:
            self.splitter.refresh()
        except Exception:
            pass
        self.body_widget.layout().activate()
        self.splitter.update()
        self.update()
        for i in range(self.splitter.count()):
            self.splitter.widget(i).update()

        # Apply a precise 6:1 ratio between CAD and Logs after visible
        if hasattr(self, 'cad_log_splitter'):
            total_height = self.cad_log_splitter.height()
            if total_height <= 0:
                total_height = self.height() - self.cad_log_splitter.contentsMargins().top() - self.cad_log_splitter.contentsMargins().bottom()
            cad_h = max(0, int(total_height * 6 / 7))
            log_h = max(0, total_height - cad_h)
            self.cad_log_splitter.setSizes([cad_h, log_h])
            # Keep stretch factors as well for subsequent resizes
            self.cad_log_splitter.setStretchFactor(0, 6)
            self.cad_log_splitter.setStretchFactor(1, 1)
       
    def create_menu_bar_items(self):
        # File Menus
        file_menu = self.menu_bar.addMenu("File")

        load_input_action = QAction("Load Input", self)
        load_input_action.setShortcut(QKeySequence("Ctrl+L"))
        load_input_action.triggered.connect(self.loadDesign_inputs)
        file_menu.addAction(load_input_action)

        file_menu.addSeparator()

        save_input_action = QAction("Save Input", self)
        save_input_action.setShortcut(QKeySequence("Ctrl+S"))
        save_input_action.triggered.connect(lambda: self.common_function_for_save_and_design(self.backend, self.input_dock.data, "Save"))
        file_menu.addAction(save_input_action)

        save_log_action = QAction("Save Log Messages", self)
        save_log_action.setShortcut(QKeySequence("Alt+M"))
        save_log_action.triggered.connect(lambda: self.saveLogMessages())
        file_menu.addAction(save_log_action)

        create_report_action = QAction("Create Design Report", self)
        create_report_action.setShortcut(QKeySequence("Alt+C"))
        create_report_action.triggered.connect(lambda:self.output_dock.open_summary_popup(self.backend))
        file_menu.addAction(create_report_action)

        file_menu.addSeparator()

        save_3d_action = QAction("Save 3D Model", self)
        save_3d_action.setShortcut(QKeySequence("Alt+3"))
        save_3d_action.triggered.connect(lambda: self.save3DcadImages(self.backend))
        file_menu.addAction(save_3d_action)

        save_cad_action = QAction("Save CAD Image", self)
        save_cad_action.setShortcut(QKeySequence("Alt+I"))
        save_cad_action.triggered.connect(lambda: self.save_cadImages(self.backend))
        file_menu.addAction(save_cad_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Shift+Q"))

        # quit_action.triggered.connect(self.parent.close_current_tab)
        file_menu.addAction(quit_action)

        # Edit Menus
        edit_menu = self.menu_bar.addMenu("Edit")

        design_prefs_action = QAction("Additional Inputs", self)
        design_prefs_action.setShortcut(QKeySequence("Alt+P"))
        design_prefs_action.triggered.connect(lambda: self.common_function_for_save_and_design(self.backend, self.input_dock.data, "Design_Pref"))
        design_prefs_action.triggered.connect(lambda: self.combined_design_prefer(self.input_dock.data,self.backend))
        design_prefs_action.triggered.connect(lambda: self.design_preferences())
        edit_menu.addAction(design_prefs_action)

        graphics_menu = self.menu_bar.addMenu("Graphics")
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+I"))
        zoom_in_action.triggered.connect(lambda: self.display.ZoomFactor(1.1))
        graphics_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+O"))
        zoom_out_action.triggered.connect(lambda: self.display.ZoomFactor(1/1.1))
        graphics_menu.addAction(zoom_out_action)

        pan_action = QAction("Pan", self)
        pan_action.setShortcut(QKeySequence("Ctrl+P"))
        pan_action.triggered.connect(lambda: self.assign_display_mode("Pan"))
        graphics_menu.addAction(pan_action)

        rotate_3d_action = QAction("Rotate 3D Model", self)
        rotate_3d_action.setShortcut(QKeySequence("Ctrl+R"))
        rotate_3d_action.triggered.connect(lambda: self.assign_display_mode('Rotate'))
        graphics_menu.addAction(rotate_3d_action)

        graphics_menu.addSeparator()

        front_view_action = QAction("Show Front View", self)
        front_view_action.setShortcut(QKeySequence("Alt+Shift+F"))
        front_view_action.triggered.connect(self.view_front)
        graphics_menu.addAction(front_view_action)
        
        top_view_action = QAction("Show Top View", self)
        top_view_action.setShortcut(QKeySequence("Alt+Shift+T"))
        top_view_action.triggered.connect(self.view_top)
        graphics_menu.addAction(top_view_action)
        
        side_view_action = QAction("Show Side View", self)
        side_view_action.setShortcut(QKeySequence("Alt+Shift+S"))
        side_view_action.triggered.connect(self.view_left)
        graphics_menu.addAction(side_view_action)

        graphics_menu.addSeparator()
        
        # Toggle Optimization Graphs (for Plate Girder PSO visualization)
        self.toggle_opt_action = QAction("Show Optimization Graph", self)
        self.toggle_opt_action.setShortcut(QKeySequence("Alt+G"))
        self.toggle_opt_action.triggered.connect(self.toggle_optimization_view)
        self.toggle_opt_action.setEnabled(False)  # Enabled after PSO runs
        graphics_menu.addAction(self.toggle_opt_action)

        graphics_menu.addSeparator()


        # Database Menu
        database_menu = self.menu_bar.addMenu("Database")

        input_csv_action = QAction("Save Inputs (.csv)", self)
        input_csv_action.triggered.connect(lambda: self.output_dock.save_output_to_csv(self.backend))
        database_menu.addAction(input_csv_action)

        output_csv_action = QAction("Save Outputs (.csv)", self)
        output_csv_action.triggered.connect(lambda: self.output_dock.save_output_to_csv(self.backend))
        database_menu.addAction(output_csv_action)

        input_osi_action = QAction("Save Inputs (.osi)", self)
        input_osi_action.triggered.connect(lambda: self.common_function_for_save_and_design(self.backend, self.input_dock.data, "Save"))
        database_menu.addAction(input_osi_action)

        download_database_menu = database_menu.addMenu("Download Database")

        download_column_action = QAction("Column", self)
        download_column_action.triggered.connect(lambda table="Columns", call_type="header": self.downloadDatabase.emit(table, call_type))
        download_database_menu.addAction(download_column_action)

        download_bolt_action = QAction("Beam", self)
        download_bolt_action.triggered.connect(lambda table="Beams", call_type="header": self.downloadDatabase.emit(table, call_type))
        download_database_menu.addAction(download_bolt_action)

        download_weld_action = QAction("Channel", self)
        download_weld_action.triggered.connect(lambda table="Channels", call_type="header": self.downloadDatabase.emit(table, call_type))
        download_database_menu.addAction(download_weld_action)

        download_angle_action = QAction("Angle", self)
        download_angle_action.triggered.connect(lambda table="Angles", call_type="header": self.downloadDatabase.emit(table, call_type))
        download_database_menu.addAction(download_angle_action)
        
        database_menu.addSeparator()

        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.reset_database)
        reset_action.setShortcut(QKeySequence("Alt+R"))
        database_menu.addAction(reset_action)

        # Help Menu
        help_menu = self.menu_bar.addMenu("Help")

        video_tutorials_action = QAction("Video Tutorials", self)
        video_tutorials_action.triggered.connect(lambda: TutorialsDialog().exec())
        help_menu.addAction(video_tutorials_action)

        design_examples_action = QAction("Design Examples", self)
        design_examples_action.triggered.connect(design_examples)
        help_menu.addAction(design_examples_action)

        help_menu.addSeparator()

        ask_question_action = QAction("Ask Us a Question", self)
        ask_question_action.triggered.connect(lambda: AskQuestions().exec())
        help_menu.addAction(ask_question_action)

        about_osdag_action = QAction("About Osdag", self)
        about_osdag_action.triggered.connect(lambda: AboutOsdagDialog().exec())
        help_menu.addAction(about_osdag_action)

        help_menu.addSeparator()

        check_update_action = QAction("Check For Update", self)
        check_update_action.triggered.connect(self.on_check_for_update)
        help_menu.addAction(check_update_action)

    #----------------Function-Trigger-for-MenuBar-START----------------------------------------
    
    # Function for getting inputs from a file
    def loadDesign_inputs(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Design", os.path.join(str(self.folder)),
                                                  "InputFiles(*.osi)")
        if not filePath:
            return
        try:
            in_file = str(filePath)
            with open(in_file, 'r') as fileObject:
                uiObj = yaml.safe_load(fileObject)
            module = uiObj[KEY_MODULE]
            print(f"[Info] Loaded module: {module}")

            selected_module = self.backend.module_name()
            if selected_module == module:
                self.ui_loaded = False
                self.setDictToUserInputs(uiObj)
                self.ui_loaded = True

            else:
                CustomMessageBox(
                    title="Information",
                    text="Please load the appropriate Input",
                    dialogType=MessageBoxType.Information
                ).exec()
                return
        except IOError:
            CustomMessageBox(
                title="Unable to open file",
                text="There was an error opening \"%s\"" % filePath,
                dialogType=MessageBoxType.Information
            ).exec()
            return

    # Helper Function to load .osi -> self.loadDesign_inputs
    def setDictToUserInputs(self, uiObj):
        op_list = self.backend.input_values()
        new = self.backend.customized_input()
        data = self.input_dock.data
        input_widget = self.input_dock.input_widget

        self.load_input_error_message = "Invalid Inputs Found! \n"

        for uiObj_key in uiObj.keys():
            if str(uiObj_key) in [KEY_SUPTNGSEC_MATERIAL, KEY_SUPTDSEC_MATERIAL, KEY_SEC_MATERIAL, KEY_CONNECTOR_MATERIAL,
                             KEY_BASE_PLATE_MATERIAL]:
                material = uiObj[uiObj_key]
                material_validator = MaterialValidator(material)
                if material_validator.is_already_in_db():
                    pass
                elif material_validator.is_format_custom():
                    if material_validator.is_valid_custom():
                        self.update_material_db(grade=material, material=material_validator)
                        input_dock_material = input_widget.findChild(QWidget, KEY_MATERIAL)
                        input_dock_material.clear()
                        for item in connectdb("Material"):
                            input_dock_material.addItem(item)
                    else:
                        self.load_input_error_message += \
                            str(uiObj_key) + ": (" + str(material) + ") - Default Value Considered! \n"
                        continue
                else:
                    self.load_input_error_message += \
                        str(uiObj_key) + ": (" + str(material) + ") - Default Value Considered! \n"
                    continue

            if uiObj_key not in [i[0] for i in op_list]:
                self.design_pref_inputs.update({uiObj_key: uiObj[uiObj_key]})

        for op in op_list:
            key_str = op[0]
            key = input_widget.findChild(QWidget, key_str)
            if op[2] == TYPE_COMBOBOX:
                if key_str in uiObj.keys():
                    index = key.findText(uiObj[key_str], Qt.MatchFixedString)
                    if index >= 0:
                        key.setCurrentIndex(index)
                    else:
                        if key_str in [KEY_SUPTDSEC, KEY_SUPTNGSEC]:
                            self.load_input_error_message += \
                                str(key_str) + ": (" + str(uiObj[key_str]) + ") - Select from available Sections! \n"
                        else:
                            self.load_input_error_message += \
                                str(key_str) + ": (" + str(uiObj[key_str]) + ") - Default Value Considered! \n"
            elif op[2] == TYPE_TEXTBOX:
                if key_str in uiObj.keys():
                    if key_str == KEY_SHEAR or key_str==KEY_AXIAL or key_str == KEY_MOMENT:
                        if uiObj[key_str] == "":
                            pass
                        elif float(uiObj[key_str]) >= 0:
                            pass
                        else:
                            self.load_input_error_message += \
                                str(key_str) + ": (" + str(uiObj[key_str]) + ") - Load should be positive integer! \n"
                            uiObj[key_str] = ""

                    # Convert list values to string before setting text
                    value = uiObj[key_str]
                    if isinstance(value, list):
                        value = value[0] if value else ""
                    key.setText(value if value != 'Disabled' else "")
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if key_str in uiObj.keys():
                    for n in new:
                        if n[0] == key_str and n[0] == KEY_SECSIZE:
                            if set(uiObj[key_str]) != set(n[1]([input_widget.findChild(QWidget,
                                                          KEY_SEC_PROFILE).currentText()])):
                                key.setCurrentIndex(1)
                            else:
                                key.setCurrentIndex(0)
                            data[key_str + "_customized"] = uiObj[key_str]

                        elif n[0] == key_str and n[0] != KEY_SECSIZE:
                            if set(uiObj[key_str]) != set(n[1]()):
                                key.setCurrentIndex(1)
                            else:
                                # print(f"[Info] Key: {key}, Type: {type(key)}")
                                key.setCurrentIndex(1)
                            data[key_str + "_customized"] = uiObj[key_str]
            else:
                pass

        if self.load_input_error_message != "Invalid Inputs Found! \n":
            CustomMessageBox(
                title="Information",
                text=self.load_input_error_message,
                dialogType=MessageBoxType.About
            ).exec()

    # To Save 3D Model
    def save3DcadImages(self, main):
        from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
        from OCC.Core.Interface import Interface_Static_SetCVal
        from OCC.Core.IFSelect import IFSelect_RetDone
        from OCC.Core.StlAPI import StlAPI_Writer
        from OCC.Core import BRepTools
        from OCC.Core import IGESControl

        if not main.design_button_status:
            CustomMessageBox(
                title="Warning",
                text="No design created!",
                dialogType=MessageBoxType.Warning
            ).exec()
            return

        if main.design_status:
            if self.fuse_model is None:
                self.fuse_model = self.commLogicObj.create2Dcad()
            shape = self.fuse_model

            files_types = "IGS (*.igs);;STEP (*.stp);;STL (*.stl);;BREP(*.brep)"

            filePath, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.igs"),
                                                      files_types)
            fName = str(filePath)

            if fName and self.fuse_model:
                file_extension = fName.split(".")[-1]

                if file_extension == 'igs':
                    IGESControl.IGESControl_Controller().Init()
                    iges_writer = IGESControl.IGESControl_Writer()
                    iges_writer.AddShape(shape)
                    iges_writer.Write(fName)

                elif file_extension == 'brep':

                    BRepTools.breptools.Write(shape, fName)

                elif file_extension == 'stp':
                    # initialize the STEP exporter
                    step_writer = STEPControl_Writer()
                    Interface_Static_SetCVal("write.step.schema", "AP203")

                    # transfer shapes and write file
                    step_writer.Transfer(shape, STEPControl_AsIs)
                    status = step_writer.Write(fName)

                    assert (status == IFSelect_RetDone)

                else:
                    stl_writer = StlAPI_Writer()
                    stl_writer.SetASCIIMode(True)
                    stl_writer.Write(shape, fName)

                self.fuse_model = None

                CustomMessageBox(
                    title="Information",
                    text="File Saved",
                    dialogType=MessageBoxType.About
                ).exec()
            else:
                CustomMessageBox(
                    title="Error",
                    text="File not saved",
                    dialogType=MessageBoxType.Critical
                ).exec()
        else:
            CustomMessageBox(
                title="Warning",
                text="Design Unsafe: 3D Model cannot be saved",
                dialogType=MessageBoxType.Warning
            ).exec()

    # Save CAD Model in image formats(PNG,JPEG,BMP,TIFF)
    def save_cadImages(self, main):
        if main.design_status:
            files_types = "PNG (*.png);;JPEG (*.jpeg);;TIFF (*.tiff);;BMP(*.bmp)"
            filePath, _ = QFileDialog.getSaveFileName(self, 'Export', os.path.join(str(self.folder), "untitled.png"),
                                                      files_types)
            fName = str(filePath)
            file_extension = fName.split(".")[-1]

            if file_extension == 'png' or file_extension == 'jpeg' or file_extension == 'bmp' or file_extension == 'tiff':
                self.display.ExportToImage(fName)
                CustomMessageBox(
                    title="Information",
                    text="File saved",
                    dialogType=MessageBoxType.About
                ).exec()
        else:
            CustomMessageBox(
                    title="Information",
                    text="Design Unsafe: CAD image cannot be saved",
                    dialogType=MessageBoxType.About
                ).exec()    

    # To change mode to Pan/Rotate using keyboard keys
    def assign_display_mode(self, mode):
        self.cad_widget.setFocus()
        if mode == 'Pan':
            self.display_mode = 'Pan'
        elif mode == 'Rotate':
            self.display_mode = 'Rotate'
        else:
            self.display_mode = 'Normal'

    def Pan_Rotate_model(self, direction):

        if self.display_mode == 'Pan':
            if direction == 'Up':
                self.display.Pan(0, 10)
            elif direction == 'Down':
                self.display.Pan(0, -10)
            elif direction == 'Left':
                self.display.Pan(-10, 0)
            elif direction == 'Right':
                self.display.Pan(10, 0)
        elif self.display_mode == 'Rotate':
            if direction == 'Up':
                self.display_y += 10
                self.display.Rotation(self.display_x, self.display_y)
            elif direction == 'Down':
                self.display_y -= 10
                self.display.Rotation(self.display_x, self.display_y)
            elif direction == 'Left':
                self.display_x -= 10
                self.display.Rotation(self.display_x, self.display_y)
            elif direction == 'Right':
                self.display_x += 10
                self.display.Rotation(self.display_x, self.display_y)
    
    def reset_database(self):
        conn = sqlite3.connect(PATH_TO_DATABASE)
        tables = ["Columns", "Beams", "Angles", "Channels"]
        text = ""
        for table in tables:
            query = "DELETE FROM "+str(table)+" WHERE Source = ?"
            cursor = conn.execute(query, ('Custom',))
            text += str(table)+": "+str(cursor.rowcount)+" rows deleted. \n"
            conn.commit()
            cursor.close()
        conn.close()
        CustomMessageBox(
            title="Successful",
            text=text,
            dialogType=MessageBoxType.Success
        ).exec()


    #----------------Function-Trigger-for-MenuBar-END------------------------------------------

    def resizeEvent(self, event):

        """Override resizeEvent with safety check."""
        # Check if being deleted
        if not self.isVisible() or self.signalsBlocked():
            return
        
        # Check if splitter exists and has children
        try:
            # Normal Resize Event
            self.sidebar.resize_sidebar(self.width(), self.height())
            # Update sidebar position to keep it centered vertically
            self.sidebar_y = (self.height() - self.menu_bar.height() - self.sidebar.height()) // 2 + self.menu_bar.height()
            top_offset = self.sidebar_y
            if self.sidebar.x() < 0:
                self.sidebar.move(-self.sidebar.width() + 12, top_offset)
            else:
                self.sidebar.move(self.sidebar.x(), top_offset)
                
            if not hasattr(self, 'splitter') or self.splitter is None:
                return
            if self.splitter.count() < 3:
                return

            if self.input_dock.isVisible():
                input_dock_width = self.input_dock.sizeHint().width()
            else:
                input_dock_width = 0
            
            if self.output_dock.isVisible():
                output_dock_width = self.output_dock.sizeHint().width()
            else:
                output_dock_width = 0
            total_width = self.width() - self.splitter.contentsMargins().left() - self.splitter.contentsMargins().right()
            self.splitter.setMinimumWidth(0)
            self.splitter.setCollapsible(0, True)
            self.splitter.setCollapsible(1, True)
            self.splitter.setCollapsible(2, True)
            for i in range(self.splitter.count()):
                self.splitter.widget(i).setMinimumWidth(0)
                self.splitter.widget(i).setMaximumWidth(16777215)
            target_sizes = [0] * self.splitter.count()
            target_sizes[0] = input_dock_width
            target_sizes[2] = output_dock_width
            remaining_width = total_width - input_dock_width - output_dock_width
            target_sizes[1] = max(0, remaining_width)
            self.splitter.setSizes(target_sizes)
            self.splitter.refresh()
            self.body_widget.layout().activate()
            self.splitter.update()
            self.sidebar.raise_()
            super().resizeEvent(event)
            
        except (IndexError, RuntimeError, AttributeError):
            # Being deleted, ignore
            return

    #---------------------------------Docking-Icons-Functionality-START----------------------------------------------

    def input_dock_toggle(self):
        self.input_dock.toggle_input_dock()
        
    def output_dock_toggle(self):
        self.output_dock.toggle_output_dock()

    def logs_dock_toggle(self):
        self.log_dock_active = not self.log_dock_active
        self.logs_dock.setVisible(self.log_dock_active)
        if self.log_dock_active:
            if self.theme.is_light():
                self.log_dock_control.load(":/vectors/logs_dock_active_light.svg")
            else:
                self.log_dock_control.load(":/vectors/logs_dock_active_dark.svg")
        else:
            if self.theme.is_light():
                self.log_dock_control.load(":/vectors/logs_dock_active_light.svg")
            else:
                self.log_dock_control.load(":/vectors/logs_dock_active_dark.svg") 

    def update_docking_icons(self, input_is_active=None, log_is_active=None, output_is_active=None):
            
        if(input_is_active is not None):
            self.input_dock_active = input_is_active
            # Update and save control state
            self.input_dock_active = input_is_active
            if self.input_dock_active:
                if self.theme.is_light():
                    self.input_dock_control.load(":/vectors/input_dock_active_light.svg")
                else:
                    self.input_dock_control.load(":/vectors/input_dock_active_dark.svg")
            else:
                if self.theme.is_light():
                    self.input_dock_control.load(":/vectors/input_dock_inactive_light.svg")
                else:
                    self.input_dock_control.load(":/vectors/input_dock_inactive_dark.svg")
                        
        # Update output dock icon
        if(output_is_active is not None):
            # Update and save control state
            self.output_dock_active = output_is_active
            if self.output_dock_active:
                if self.theme.is_light():
                    self.output_dock_control.load(":/vectors/output_dock_active_light.svg")
                else:
                    self.output_dock_control.load(":/vectors/output_dock_active_dark.svg")
            else:
                if self.theme.is_light():
                    self.output_dock_control.load(":/vectors/output_dock_inactive_light.svg")
                else:
                    self.output_dock_control.load(":/vectors/output_dock_inactive_dark.svg")

        # Update log dock icon
        if(log_is_active is not None):
            self.log_dock_active = log_is_active
            # Update and save control state
            self.logs_dock_active = log_is_active
            if self.log_dock_active:
                if self.theme.is_light():
                    self.log_dock_control.load(":/vectors/logs_dock_active_light.svg")
                else:
                    self.log_dock_control.load(":/vectors/logs_dock_active_dark.svg")
            else:
                if self.theme.is_light():
                    self.log_dock_control.load(":/vectors/logs_dock_inactive_light.svg")
                else:
                    self.log_dock_control.load(":/vectors/logs_dock_inactive_dark.svg")
     
    def toggle_animate(self, show: bool, dock: str = 'output', on_finished=None):
        sizes = self.splitter.sizes()
        n = self.splitter.count()
        if dock == 'input':
            dock_index = 0

        elif dock == 'output':
            dock_index = n - 1
        elif dock == 'log':
            self.logs_dock.setVisible(show)
            if on_finished:
                on_finished()
            return
        else:
            print(f"[Error] Invalid dock: {dock}")
            return
        
        dock_widget = self.splitter.widget(dock_index)
        if show:
            dock_widget.show()
        
        self.splitter.setMinimumWidth(0)
        self.splitter.setCollapsible(dock_index, True)
        for i in range(n):
            self.splitter.widget(i).setMinimumWidth(0)
            self.splitter.widget(i).setMaximumWidth(16777215)
        
        target_sizes = sizes[:]
        total_width = self.width() - self.splitter.contentsMargins().left() - self.splitter.contentsMargins().right()
        input_dock = self.splitter.widget(0)
        output_dock = self.splitter.widget(n - 1)
        
        if dock == 'input':
            if show:
                target_sizes[0] = input_dock.sizeHint().width()
                self.input_dock_label.setVisible(False)
            else:
                target_sizes[0] = 0
            target_sizes[2] = sizes[2]
            remaining_width = total_width - target_sizes[0] - target_sizes[2]
            target_sizes[1] = max(0, remaining_width)
        else:
            if show:
                target_sizes[2] = output_dock.sizeHint().width()
                self.output_dock_label.setVisible(False)
            else:
                target_sizes[2] = 0
                self.output_dock_label.setVisible(True)
            target_sizes[0] = sizes[0]
            remaining_width = total_width - target_sizes[0] - target_sizes[2]
            target_sizes[1] = max(0, remaining_width)

        if sizes == target_sizes:
            if not show:
                dock_widget.hide()
            if on_finished:
                on_finished()
            return
        
        def after_anim():
            self.finalize_dock_toggle(show, dock_widget, target_sizes)
            if on_finished:
                on_finished()

        # User requested "one step animation" with "no delay"
        self.animate_splitter_sizes(
            self.splitter,
            sizes,
            target_sizes,
            duration=0,
            on_finished=after_anim
        )
        if dock == 'input' and not show:
            self.input_dock_label.setVisible(True)

    def animate_splitter_sizes(self, splitter, start_sizes, end_sizes, duration, on_finished=None):
        if duration <= 0:
            # Instant update
            splitter.setSizes(end_sizes)
            splitter.refresh()
            if splitter.parentWidget() and splitter.parentWidget().layout():
                splitter.parentWidget().layout().activate()
            splitter.update()
            if splitter.parentWidget():
                splitter.parentWidget().update()
            self.update()
            for i in range(splitter.count()):
                widget = splitter.widget(i)
                if widget:
                    widget.update()
            
            if on_finished:
                on_finished()
            return

        # Target 60 FPS -> ~16ms interval
        interval = 16
        steps = max(1, duration // interval)
        
        current_step = 0

        def ease_out_quad(t):
            return t * (2 - t)

        def update_step():
            nonlocal current_step
            if current_step <= steps:
                progress = current_step / steps
                # Apply easing
                eased_progress = ease_out_quad(progress)
                
                sizes = [
                    int(start + (end - start) * eased_progress) 
                    for start, end in zip(start_sizes, end_sizes)
                ]
                
                splitter.setSizes(sizes)
                splitter.refresh()
                if splitter.parentWidget() and splitter.parentWidget().layout():
                    splitter.parentWidget().layout().activate()
                splitter.update()
                if splitter.parentWidget():
                    splitter.parentWidget().update()
                self.update()
                for i in range(splitter.count()):
                    widget = splitter.widget(i)
                    if widget:
                        widget.update()
                
                current_step += 1
            else:
                timer.stop()
                if on_finished:
                    on_finished()

        timer = QTimer(self)
        timer.timeout.connect(update_step)
        timer.start(interval)
        self._splitter_anim = timer

    def finalize_dock_toggle(self, show, dock_widget, target_sizes):
        self.splitter.setSizes(target_sizes)
        if not show:
            dock_widget.hide()
        self.splitter.refresh()
        self.splitter.parentWidget().layout().activate()
        self.splitter.update()
        self.splitter.parentWidget().update()
        self.update()
        for i in range(self.splitter.count()):
            self.splitter.widget(i).update()

    #---------------------------------Docking-Icons-Functionality-END----------------------------------------------

    def on_check_for_update(self):
        print("[Action]: Check For Update selected.")

    # This opens loading widget and execute Design
    def start_thread(self, data):
        # Use safety module for multiprocessing (already initialized at startup)
        from osdag_gui.OS_safety_protocols import ensure_safe_startup
        ensure_safe_startup()
        
        # Ensure CAD widget is visible
        self.cad_widget.show()
        
        # Check if this is Plate Girder with Optimized design type
        module_name = self.backend.module_name()
        is_plate_girder = module_name.upper() == "PLATE GIRDER"
        
        # Read design type from the actual input widget (combobox)
        design_type = 'Unknown'
        if is_plate_girder and hasattr(self, 'input_dock') and self.input_dock:
            design_type_widget = self.input_dock.input_widget.findChild(QComboBox, 'Total.Design_Type')
            if design_type_widget:
                design_type = design_type_widget.currentText()
        
        is_optimized = design_type == 'Optimized'
        
        print(f"[DEBUG] module_name: '{module_name}', design_type: '{design_type}'")
        print(f"[DEBUG] is_plate_girder: {is_plate_girder}, is_optimized: {is_optimized}")
        
        if is_plate_girder and is_optimized:
            print("[DEBUG] → Using PSO Visualization (via PSOUIManager)")
            # Lazy init PSOUIManager for Plate Girder module
            if self._pso_manager is None:
                from osdag_core.design_type.plate_girder.gui.pso_ui_manager import PSOUIManager
                self._pso_manager = PSOUIManager(self)
            else:
                # Cleanup previous resources before new design
                self._pso_manager.cleanup()
            
            # Use PSO visualization instead of loading popup
            if not self._pso_manager.start_visualization(data):
                # Fallback to standard design if visualization fails
                self._run_standard_design(data)
        else:
            print("[DEBUG] → Using standard loading popup")
            # Cleanup any previous PSO visualization
            if self._pso_manager:
                self._pso_manager.cleanup()
            # Standard loading popup for all other modules
            self._run_standard_design(data)
    
    # NOTE: PSO visualization methods moved to osdag_core/design_type/plate_girder/gui/pso_ui_manager.py
    # Methods removed: _start_pso_visualization, _restore_cad_from_pso, _show_pso_from_cad,
    # _restore_initial_layout_for_plate_girder, _cleanup_pso_resources, _on_pso_complete
    # Now delegated to self._pso_manager (PSOUIManager instance)
    
    def _run_standard_design(self, data):
        """Run standard design flow with loading popup (for non-Plate Girder modules)."""
        self.loading = LoadingDialogManager(self.theme.is_light())
        self.loading.show()
        self.setEnabled(False)
        time.sleep(1)
        self.common_function_for_save_and_design(self.backend, data, "Design")
    
    def toggle_optimization_view(self):
        """Toggle between PSO visualization and CAD view. 
        Delegates to PSOUIManager for Plate Girder module.
        """
        if self._pso_manager:
            self._pso_manager.toggle_view()
        elif hasattr(self, 'cad_widget') and self.cad_widget:
            # No PSO manager, just ensure CAD is shown
            self.cad_widget.show()
    
    def finished_loading(self):
        # print("Custom Logger: ")
        # print(self.backend.logger.logs)
        time.sleep(1)
        self.loading.hide()
        self.setEnabled(True)

    # Design Functions
    def common_function_for_save_and_design(self, main, data, trigger_type):
        option_list = main.input_values()
        for data_key_tuple in main.customized_input():
            data_key = data_key_tuple[0] + "_customized"
            if data_key in data.keys() and len(data_key_tuple) == 4:
                data[data_key] = [data_values for data_values in data[data_key]
                                  if data_values not in data_key_tuple[2]]

        # print(f"ui_template.py common_function_for_save_and_design \n")
        # print(f"option_list {option_list} \n")
        # print(f"data {data} ")

        self.design_fn(option_list, data, main)

        if trigger_type == "Save":
            self.saveDesign_inputs()
        elif trigger_type == "Design_Pref":
            # print(f"trigger_type == Design_Pref")
            if self.prev_inputs != self.input_dock_inputs or self.designPrefDialog.changes != QDialog.Accepted:
                # print(f"QDialog.Accepted")
                self.designPrefDialog = AdditionalInputs(main, self, input_dictionary=self.input_dock_inputs)

                if 'Select Section' in self.input_dock_inputs.values():
                    # print(f"self.designPrefDialog.flag = False")
                    self.designPrefDialog.flag = False
                else:
                    self.designPrefDialog.flag = True
                # print(f"QDialog done")
                # if self.prev_inputs != {}:
                #     self.design_pref_inputs = {}

        else:
            main.design_button_status = True
            for input_field in self.input_dock.input_widget.findChildren(QWidget):
                if type(input_field) == QLineEdit:
                    input_field.textChanged.connect(self.clear_output_fields)
                elif type(input_field) == QComboBox:
                    input_field.currentIndexChanged.connect(self.clear_output_fields)

            # print(f"\n design_dictionary {self.design_inputs}")
            error = main.func_for_validation(self.design_inputs)
            status = main.design_status
            # print(f"[INFO] Design status: {status}")
            # print(f"[INFO] trigger_type: {trigger_type}")

            if status == False:
                # Open Logs and close Loading
                try:
                    self.toggle_animate(True, 'log', on_finished=self.finished_loading)
                    self.logs_dock_active = True
                except Exception:
                    if hasattr(self, 'logs_dock'):
                        self.logs_dock.setVisible(True)
                
                # Update logs dock control icon
                self.update_docking_icons(log_is_active=True)

            if error is not None:
                self.show_error_msg(error)
                # Close loading popup
                self.finished_loading()
                return

            out_list = main.output_values(status)
            # print('[INFO] out_list changed: ',out_list)

            for option in out_list:
                if option[2] == TYPE_TEXTBOX:
                    txt = self.output_dock.output_widget.findChild(QWidget, option[0])
                    txt.setText(str(option[3]))
                    if status:
                        txt.setVisible(bool(option[3] is not None))
                        txt_label = self.output_dock.output_widget.findChild(QWidget, option[0]+"_label")
                        txt_label.setVisible(bool(option[3] is not None))

                elif option[2] == TYPE_OUT_BUTTON:
                    btn = self.output_dock.output_widget.findChild(QWidget, option[0])
                    if btn is not None:
                        btn.setEnabled(True)
                    btn_push = self.output_dock.output_widget.findChild(QPushButton, option[0])
                    if btn_push is not None:
                        btn_push.setEnabled(True)


            # Ensure Output dock is visible and sized when we have results
            if status:
                # --- Set Camera to Right Top Isometric View ---
                try:
                    # Back Right Top Isometric: Looking from (+X, +Y, +Z) towards origin
                    print("DEBUG: Setting Camera to Back Right Top Isometric (1, -1, 1)...")
                    self.cad_widget.view.SetUp(1, -1, 1)
                    self.cad_widget.view.SetProj(1, -1, 1)
                    self.cad_widget.view.FitAll()
                    self.cad_widget.view.Redraw()
                except Exception as e:
                    print(f"Error setting camera view: {e}")

                def show_logs():
                    try:
                        self.toggle_animate(True, 'log', on_finished=self.finished_loading)
                        self.logs_dock_active = True
                    except Exception:
                        if hasattr(self, 'logs_dock'):
                            self.logs_dock.setVisible(True)
                    
                    # Update logs dock control icon
                    self.update_docking_icons(log_is_active=True)

                def hide_input():
                    self.initial_view()
                    try:
                        self.toggle_animate(False, 'input', on_finished=show_logs)
                        self.input_dock_active = False
                        # Lock Basic Inputs
                        self.input_dock.toggle_lock(set_locked_state=True)
                    except Exception:
                        input_widget = self.splitter.widget(0)
                        if input_widget:
                            input_widget.hide()
                        show_logs()

                try:
                    self.toggle_animate(True, 'output', on_finished=hide_input)
                    self.output_dock_active = True
                except Exception:
                    self.output_dock.show()
                    sizes = self.splitter.sizes()
                    if len(sizes) >= 3 and sizes[2] == 0:
                        total_width = self.width() - self.splitter.contentsMargins().left() - self.splitter.contentsMargins().right()
                        left_width = self.splitter.widget(0).sizeHint().width()
                        right_width = self.output_dock.sizeHint().width()
                        center_width = max(0, total_width - left_width - right_width)
                        self.splitter.setSizes([left_width, center_width, right_width])
                    hide_input()

            # print('[INFO] Output title changed: ',self.output_dock.output_title_change(main))
            self.output_dock.output_title_change(main)
            last_design_folder = os.path.join('ResourceFiles', 'last_designs')
            # print('[INFO] last design: ',last_design_folder)
            if not os.path.isdir(last_design_folder):
                # print('[INFO] not os.path.isdir')
                os.makedirs(last_design_folder)
            last_design_file = str(main.module_name()).replace(' ', '') + ".osi"
            last_design_file = os.path.join(last_design_folder, last_design_file)
            out_titles_status = []
            out_titles = []
            title_repeat = 1
            for option in out_list:
                if option[2] == TYPE_TITLE:
                    title_name = option[1]
                    if title_name in out_titles:
                        title_name += str(title_repeat)
                        title_repeat += 1
                    if self.output_dock.output_title_fields[title_name][0].isVisible():
                        out_titles_status.append(1)
                    else:
                        out_titles_status.append(0)
                    out_titles.append(title_name)
            self.design_inputs.update({"out_titles_status": out_titles_status})
            with open(str(last_design_file), 'w') as last_design:
                yaml.dump(self.design_inputs, last_design)
            self.design_inputs.pop("out_titles_status")

            # if status is True and main.module in [KEY_DISP_FINPLATE, KEY_DISP_BEAMCOVERPLATE,
            #                                       KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_CLEATANGLE,
            #                                       KEY_DISP_ENDPLATE, KEY_DISP_BASE_PLATE, KEY_DISP_SEATED_ANGLE,
            #                                       KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED,KEY_DISP_COLUMNCOVERPLATE,
            #                                       KEY_DISP_COLUMNCOVERPLATEWELD, KEY_DISP_COLUMNENDPLATE]:

            # ##############trial##############
            # status = True
            # ##############trial##############
            if status is True and main.module in [KEY_DISP_FINPLATE, KEY_DISP_BEAMCOVERPLATE, KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_CLEATANGLE,
                                                  KEY_DISP_ENDPLATE, KEY_DISP_BASE_PLATE, KEY_DISP_SEATED_ANGLE, KEY_DISP_TENSION_BOLTED,
                                                  KEY_DISP_TENSION_WELDED, KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_COLUMNCOVERPLATEWELD,
                                                  KEY_DISP_COLUMNENDPLATE, KEY_DISP_BCENDPLATE, KEY_DISP_BB_EP_SPLICE,
                                                  KEY_DISP_COMPRESSION_COLUMN,KEY_DISP_FLEXURE,KEY_DISP_FLEXURE2,KEY_DISP_FLEXURE3,KEY_DISP_FLEXURE4,
                                                  KEY_DISP_COMPRESSION_STRUT, KEY_DISP_STRUT_WELDED_END_GUSSET,KEY_DISP_LAPJOINTBOLTED,KEY_DISP_BUTTJOINTBOLTED, 
                                                  KEY_DISP_LAPJOINTWELDED, KEY_DISP_BUTTJOINTWELDED]:
                # print(self.display, self.folder, main.module, main.mainmodule)
                # print("[INFO] common start")
                # print(f"[INFO] main object type: {type(main)}")
                # print(f"[INFO] main attributes: {dir(main)}")
                # print("[INFO] main.mainmodule",main.mainmodule)

                self.commLogicObj = CommonDesignLogic(self.display, self.cad_widget, self.folder, main.module, main.mainmodule)
                self.commLogicObj.module_object = main
                # print(f"This is MAIN.MODULE {main.module}")
                # print("[INFO] main.mainmodule", main.mainmodule)
                # print("[INFO] common start")
                status = main.design_status
                ##############trial##############
                # status = True
                ##############trial##############

                print("Hover Dictionary: ", main.hover_dict)

                # CRITICAL: Garbage collect before heavy CAD operations to prevent heap corruption
                # This is essential when creating 64+ OpenCASCADE shapes (bolts/nuts/welds)
                gc.collect()
                
                # Process Qt events before OpenGL rendering to prevent segfault on Linux
                from PySide6.QtWidgets import QApplication
                QApplication.processEvents()
                
                # Ensure display is ready before 3D rendering
                if self._is_display_ready():
                    try:
                        self.commLogicObj.call_3DModel(status, main)
                        # Garbage collect after CAD operations to clean up OCC shapes
                        gc.collect()
                    except Exception as e:
                        print(f"[ERROR] 3D model rendering failed: {e}")
                else:
                    print("[WARNING] Display not ready for 3D rendering")
                    
                # Store the design instance for later use in report generation
                if hasattr(self.commLogicObj, 'design_obj'):
                    # Store reference to the design instance
                    self.design_instance = self.commLogicObj.design_obj
                else:
                    # Create and store design instance manually
                    self.design_instance = self.backend
                    # Set design inputs on the instance
                    for key, value in self.design_inputs.items():
                        if hasattr(self.design_instance, key):
                            setattr(self.design_instance, key, value)
                    # Set design status
                    self.design_instance.design_status = status

                print("[INFO] 3D end")
                self.display_x = 90
                self.display_y = 90

                # Show cad component checkboxes
                self.cad_comp_widget.show()
                for chkbox in main.get_3d_components():
                    checkbox_widget = self.cad_comp_widget.findChild(QCheckBox, chkbox[0])
                    if checkbox_widget:
                        # CRITICAL: Block signals to prevent triggering display_3DModel calls
                        # which causes heap corruption from rapid OpenCASCADE operations
                        checkbox_widget.blockSignals(True)
                        checkbox_widget.setChecked(False)
                        checkbox_widget.blockSignals(False)

                fName = str('./ResourceFiles/images/3d.png')
                file_extension = fName.split(".")[-1]
            else:
                # Hide cad component checkboxes
                self.cad_comp_widget.hide()
                for chkbox in main.get_3d_components():
                    checkbox_widget = self.cad_comp_widget.findChild(QCheckBox, chkbox[0])
                    if checkbox_widget:
                        # CRITICAL: Block signals to prevent triggering display_3DModel calls
                        checkbox_widget.blockSignals(True)
                        checkbox_widget.setChecked(False)
                        checkbox_widget.blockSignals(False)
            
    def design_fn(self, op_list, data_list, main):
        design_dictionary = {}
        self.input_dock_inputs = {}
        # print(f"\n op_list {op_list}")
        # print(f"\n data_list{data_list}")
        for op in op_list:
            widget = self.input_dock.input_widget.findChild(QWidget, op[0])
            if op[2] == TYPE_COMBOBOX:
                des_val = widget.currentText()
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_MODULE:
                des_val = op[1]
                module = op[1]
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_COMBOBOX_CUSTOMIZED:
                try:
                    des_val = data_list[op[0] + "_customized"]
                    d1 = {op[0]: des_val}
                except:
                    des_val = data_list["Member.Designation" + "_customized"]
                    d1 = {op[0]: des_val}
            elif op[2] == TYPE_TEXTBOX:
                des_val = widget.text()
                d1 = {op[0]: des_val}
            elif op[2] == TYPE_NOTE:
                widget = self.input_dock.input_widget.findChild(QWidget, op[0] + "_note")
                des_val = widget.text()
                d1 = {op[0]: des_val}
            else:
                d1 = {}
            design_dictionary.update(d1)

            self.input_dock_inputs.update(d1)
            # print(f"\n self.input_dock_inputs{self.input_dock_inputs}")


        for design_pref_key in self.design_pref_inputs.keys():
            if design_pref_key not in self.input_dock_inputs.keys():
                self.input_dock_inputs.update({design_pref_key: self.design_pref_inputs[design_pref_key]})

        if self.designPrefDialog.flag:
            # print('flag true')

            des_pref_input_list = main.input_dictionary_design_pref()
            edit_tabs_list = main.edit_tabs()
            edit_tabs_remove = list(filter(lambda x: x[2] == TYPE_REMOVE_TAB, edit_tabs_list))
            remove_tab_name = [x[0] for x in edit_tabs_remove]
            # remove_tabs = list(filter(lambda x: x[0] in remove_tab_name, des_pref_input_list))
            #
            # remove_func_name = edit_tabs_remove[3]
            result = None
            for edit in main.edit_tabs():
                (tab_name, input_dock_key_name, change_typ, f) = edit
                remove_tabs = list(filter(lambda x: x[0] in remove_tab_name, des_pref_input_list))

                input_dock_key = self.input_dock.input_widget.findChild(QWidget, input_dock_key_name)
                result = list(filter(lambda get_tab:
                                     self.designPrefDialog.ui.findChild(QWidget, get_tab[0]).objectName() !=
                                     f(input_dock_key.currentText()), remove_tabs))

            if result is not None:
                des_pref_input_list_updated = [i for i in des_pref_input_list if i not in result]
            else:
                des_pref_input_list_updated = des_pref_input_list

            # print(f"[INFO] design_fn des_pref_input_list_updated = {des_pref_input_list_updated}\n")
            for des_pref in des_pref_input_list_updated:
                tab_name = des_pref[0]
                input_type = des_pref[1]
                input_list = des_pref[2]
                tab = self.designPrefDialog.ui.findChild(QWidget, tab_name)
                # print(f"design_fn tab_name = {tab_name}\n")
                # print(f"design_fn input_type = {input_type}\n")
                # print(f"design_fn input_list = {input_list}\n")
                # print(f"design_fn tab = {tab}\n")
                for key_name in input_list:
                    key = tab.findChild(QWidget, key_name)
                    if key is None:
                        continue
                    if isinstance(key, QLineEdit):
                        val = key.text()
                        design_dictionary.update({key_name: val})
                    elif isinstance(key, QComboBox):
                        val = key.currentText()
                        design_dictionary.update({key_name: val})
        else:
            # print('flag false')
            for without_des_pref in main.input_dictionary_without_design_pref():
                input_dock_key = without_des_pref[0]
                input_list = without_des_pref[1]
                input_source = without_des_pref[2]
                # print(f"\n ========================Check===========================")
                # print(f"\n[INFO] self.design_pref_inputs.keys() {self.design_pref_inputs.keys()}")
                for key_name in input_list:
                    if input_source == 'Input Dock':
                        design_dictionary.update({key_name: design_dictionary[input_dock_key]})
                    else:
                        val = main.get_values_for_design_pref(key_name, design_dictionary)
                        design_dictionary.update({key_name: val})

            for dp_key in self.design_pref_inputs.keys():
                design_dictionary[dp_key] = self.design_pref_inputs[dp_key]
        # print(f"\n ========================Check done ===========================")

        self.design_inputs = design_dictionary
        self.design_inputs = design_dictionary
        # print(f"\n[INFO] self.input_dock_inputs {self.input_dock_inputs}")
        # print(f"\n[INFO] design_fn design_dictionary{self.design_inputs}")
        # print(f"\n[INFO] main.input_dictionary_without_design_pref(main){main.input_dictionary_without_design_pref()}")

    def combined_design_prefer(self, data, main):
        on_change_tab_list = main.tab_value_changed()
        # print(f"[INFO] ui_template combined_design_prefer on_change_tab_list= {on_change_tab_list} \n")
        for new_values in on_change_tab_list:
            (tab_name, key_list, key_to_change, key_type, f) = new_values
            tab = self.designPrefDialog.ui.tabWidget.tabs.findChild(QWidget, tab_name)
            # print(f"[INFO] key_list = {key_list} \n"
            #       f"[INFO] tab {tab}")

            for key_name in key_list:
                key = tab.findChild(QWidget, key_name)
                # print(f"[INFO] key= {key} \n")

                if isinstance(key, QComboBox):
                    self.connect_combobox_for_tab(key, tab, on_change_tab_list, main)
                elif isinstance(key, QLineEdit):
                    self.connect_textbox_for_tab(key, tab, on_change_tab_list, main)

        for edit in main.edit_tabs():
            (tab_name, input_dock_key_name, change_typ, f) = edit
            tab = self.designPrefDialog.ui.tabWidget.tabs.findChild(QWidget, tab_name)
            input_dock_key = self.input_dock.input_widget.findChild(QWidget, input_dock_key_name)
            if change_typ == TYPE_CHANGE_TAB_NAME:
                self.designPrefDialog.ui.tabWidget.tabs.setTabText(
                    self.designPrefDialog.ui.tabWidget.tabs.indexOf(tab), f(input_dock_key.currentText()))
            elif change_typ == TYPE_REMOVE_TAB:

                if tab.objectName() != f(input_dock_key.currentText()):
                    self.designPrefDialog.ui.tabWidget.tabs.removeTab(
                        self.designPrefDialog.ui.tabWidget.tabs.indexOf(tab))
                # if tab:
                #     self.designPrefDialog.ui.tabWidget.insertTab(0, tab, tab_name)

        for refresh in main.refresh_input_dock():
            (tab_name, key_name, key_type, tab_key, master_key, value, database_arg) = refresh
            tab = self.designPrefDialog.ui.tabWidget.tabs.findChild(QWidget, tab_name)
            if tab:
                add_button = tab.findChild(QWidget, "pushButton_Add_"+tab_name)
                key = self.input_dock.input_widget.findChild(QWidget, key_name)
                selected = key.currentText()
                if master_key:
                    val = self.input_dock.input_widget.findChild(QWidget, master_key).currentText()
                    if val not in value:
                        continue
                self.refresh_section_connect(add_button, selected, key_name, key_type, tab_key, database_arg,data)

    def connect_textbox_for_tab(self, key, tab, new, main):
        key.textChanged.connect(lambda: self.tab_change(key, tab, new, main))

    def connect_combobox_for_tab(self, key, tab, new, main):
        key.currentIndexChanged.connect(lambda: self.tab_change(key, tab, new, main))

    def refresh_section_connect(self, add_button, prev, key_name, key_type, tab_key, arg,data):
        add_button.clicked.connect(lambda: self.refresh_section(prev, key_name, key_type, tab_key, arg,data))

    def refresh_section(self, prev, key_name, key_type, tab_key, arg,data):
        if key_type == TYPE_COMBOBOX_CUSTOMIZED:
            current_list = connectdb(arg,"popup")
        else:
            current_list = connectdb(arg)
        text = self.designPrefDialog.ui.findChild(QWidget, tab_key).text()
        key = self.input_dock.input_widget.findChild(QWidget, key_name)

        if key_type == TYPE_COMBOBOX:
            if text == "":
                return
            key.clear()
            for item in current_list:
                key.addItem(item)
            current_list_set = set(current_list)
            red_list_set = set(red_list_function())
            current_red_list = list(current_list_set.intersection(red_list_set))
            for value in current_red_list:
                indx = current_list.index(str(value))
                key.setItemData(indx, QBrush(QColor("red")), Qt.TextColorRole)
            text_index = key.findText(text, Qt.MatchFixedString)
            if text_index >= 0:
                key.setCurrentIndex(text_index)
            else:
                key.setCurrentIndex(current_list.index(prev))
        elif key_type == TYPE_COMBOBOX_CUSTOMIZED:
            master_list = ['All','Customized']
            data[key_name + "_customized"] = current_list
            key.setCurrentIndex(master_list.index(prev))

    def design_preferences(self):
        #Function to show Design Preferences Dialog
        self.designPrefDialog.ui.state_locked = self.input_dock.state_locked
        self.designPrefDialog.ui.set_lock()
        self.designPrefDialog.show()

    def saveDesign_inputs(self):
        design_state = self.backend.design_status
        filePath = None
        fileName = None
        if not self.save_state:
            default_dir = os.path.join(get_documents_folder(), "Inputs.osi")
            filePath, _ = QFileDialog.getSaveFileName(self,
                                                    "Save Design",
                                                    default_dir,
                                                    "Input Files(*.osi)",
                                                    None)
            fileName = Path(filePath).stem
        else:
            record = get_project_by_id(self.project_id)
            filePath = record.get(PROJECT_PATH)
            fileName = record.get(PROJECT_NAME)
            
        try:
            with open(filePath, 'w') as input_file:
                yaml.dump(self.design_inputs, input_file)
            
            # Design must be done before saving project
            if design_state or self.save_state:
                # Insert saved data in database and update states
                self.save_state = True
                record = {
                    PROJECT_NAME: fileName,
                    PROJECT_PATH: filePath,
                    MODULE_KEY: self.backend.module_name(),
                }
                self.project_id = self.output_dock.save_to_database(record)

            CustomMessageBox(
                title="Success",
                text="Saved OSI Successfully!",
                dialogType=MessageBoxType.Success
            ).exec()

        except Exception as e:
            CustomMessageBox(
                title="Application",
                text="OSI file not saved.",
                dialogType=MessageBoxType.Warning
            ).exec()
            return
    
    def saveLogMessages(self):
        """Save log messages from textEdit to a text file"""
        default_dir = os.path.join(get_documents_folder(), "log_messages.txt")
        filePath, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Log Messages",
                                                  default_dir,
                                                  "Text Files(*.txt);;All Files(*.*)",
                                                  None
                                                )
        if not filePath:
            return
        
        try:
            log_content = self.textEdit.toPlainText()
            with open(filePath, 'w', encoding='utf-8') as log_file:
                log_file.write(log_content)
            
            CustomMessageBox(
                title="Information",
                text="Log messages saved successfully",
                dialogType=MessageBoxType.Information
            ).exec()
        except Exception as e:
            CustomMessageBox(
                title="Error",
                text="Cannot write file %s:\n%s" % (filePath, str(e)),
                dialogType=MessageBoxType.Critical
            ).exec()
            return
    
    #--------------------Unlocking-Inputs-After-Design-Start-----------------------
    # Clear output fields
    def clear_output_fields(self):
        # Flush PSO Visualization when inputs are unlocked/cleared
        self._pso_manager.cleanup() if self._pso_manager else None
        if hasattr(self, 'toggle_opt_action'):
            self.toggle_opt_action.setEnabled(False)
        self.cad_widget.show()
        if hasattr(self, 'logs_dock') and self.logs_dock:
            self.logs_dock.show()
            
        # Reset the design status
        self.backend.design_status = False
        self.backend.design_button_status = False
        for output_field in self.output_dock.output_widget.findChildren(QLineEdit):
            output_field.clear()
        for output_field in self.output_dock.output_widget.findChildren(QPushButton):
            if output_field.objectName() == "dock_custom_button":
                continue
            output_field.setEnabled(False)
        
        # Clear logs
        self.logs_dock.clear_logs()
        self.cad_comp_widget.hide()
    
    # Clear Cad widget
    def flush_cad_widget(self):
        """
        Safely clear the CAD widget using OCCMemoryManager.
        Uses deferred execution and centralized memory management to prevent
        heap corruption from OCC operations conflicting with Qt rendering.
        """
        if not hasattr(self, 'cad_widget') or not self.cad_widget:
            return
            
        # Check if CAD widget is fully initialized (deferred init may not be complete)
        if getattr(self, '_cad_init_pending', True):
            print("[INFO] CAD widget not yet initialized, skipping flush")
            return
        
        # Check if cleanup is already in progress
        try:
            from osdag_gui.OS_safety_protocols import get_occ_memory_manager
            manager = get_occ_memory_manager()
            widget_id = id(self.cad_widget)
            if manager.is_cleanup_in_progress(widget_id):
                print("[INFO] Cleanup already in progress, skipping")
                return
        except Exception:
            pass
        
        # CRITICAL: Defer the actual OCC cleanup to avoid heap corruption
        # This ensures all pending Qt events are processed first
        from PySide6.QtCore import QTimer
        QTimer.singleShot(50, self._do_flush_cad_widget)
    
    def _do_flush_cad_widget(self):
        """
        Internal method that performs the actual CAD widget cleanup.
        Uses the same safe cleanup order as display_3DModel in common_logic.py:
        1. cleanup_for_new_model() FIRST - clears internal Python state
        2. EraseAll() SECOND - clears OCC context  
        3. gc.collect() at safe points
        
        This order is critical to prevent heap corruption.
        """
        if not hasattr(self, 'cad_widget') or not self.cad_widget:
            return
        
        import gc
        
        # Step 1: Initial GC before any OCC operations
        gc.collect()
        
        # Step 2: Clear internal Python state FIRST (before OCC context operations)
        # This clears model_ais_objects, hover labels, view_cube reference, etc.
        # CRITICAL: Must happen BEFORE EraseAll to prevent double-free
        if hasattr(self.cad_widget, 'cleanup_for_new_model'):
            try:
                self.cad_widget.cleanup_for_new_model()
            except Exception as e:
                print(f"[WARNING] Error in cleanup_for_new_model: {e}")
        
        # Step 3: GC after clearing internal state
        gc.collect()
        
        # Step 4: Now safe to clear OCC context
        if hasattr(self.cad_widget, '_display') and self.cad_widget._display:
            try:
                self.cad_widget._display.EraseAll()
            except Exception as e:
                print(f"[WARNING] Error erasing display: {e}")
        
        # Step 5: Final GC to clean up released OCC objects
        gc.collect()
        
        # Step 6: Repaint to show empty view
        if hasattr(self.cad_widget, '_display') and self.cad_widget._display:
            try:
                self.cad_widget._display.Repaint()
            except Exception as e:
                print(f"[WARNING] Error repainting display: {e}")


    # Error Message Box
    def show_error_msg(self, error):
        # Prevent duplicate message boxes by checking if one is already open
        if hasattr(self, '_error_dialog_open') and self._error_dialog_open:
            return
        
        self._error_dialog_open = True
        
        # Create a more informative error message
        if isinstance(error, (list, tuple)) and len(error) > 0:
            if len(error) == 1:
                error_text = f"Validation Error:\n\n{error[0]}"
            else:
                error_text = "Validation Errors:\n\n"
                for i, err in enumerate(error[:5], 1):  # Show first 5 errors
                    error_text += f"{i}. {err}\n"
                if len(error) > 5:
                    error_text += f"\n... and {len(error) - 5} more errors"
        else:
            error_text = f"[Error]: {str(error)}"
        
        msg_box = CustomMessageBox(
            title="Validation Error",
            text=error_text,
            dialogType=MessageBoxType.Critical
        )

        msg_box.finished.connect(lambda: setattr(self, '_error_dialog_open', False))
        msg_box.exec()
        
class InputDockIndicator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.parent = parent
        self.setObjectName("input_dock_indicator")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Fixed width, expanding height

        input_layout = QHBoxLayout(self)
        input_layout.setContentsMargins(6,0,0,0)
        input_layout.setSpacing(0)

        self.input_label = QSvgWidget()
        input_layout.addWidget(self.input_label)
        self.input_label.setFixedWidth(32)

        self.toggle_strip = QWidget()
        self.toggle_strip.setObjectName("toggle_strip")
        self.toggle_strip.setFixedWidth(6)  # Always visible
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignRight)  # Align to right for input dock

        self.toggle_btn = QPushButton("❯")  # Right-pointing chevron for input dock
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.parent.input_dock_toggle)
        self.toggle_btn.setToolTip("Show input panel")
        self.toggle_btn.setObjectName("toggle_strip_button")
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        input_layout.addWidget(self.toggle_strip)
    
    def paintEvent(self, event):
        if self.parent.theme.is_light():
            self.input_label.load(":/vectors/inputs_label_light.svg")
        else:
            self.input_label.load(":/vectors/inputs_label_dark.svg")
        return super().paintEvent(event)

class OutputDockIndicator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.parent = parent
        self.setObjectName("output_dock_indicator")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Fixed width, expanding height

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(0,0,0,0)
        output_layout.setSpacing(0)

        self.toggle_strip = QWidget()
        self.toggle_strip.setFixedWidth(6)  # Always visible
        self.toggle_strip.setObjectName("toggle_strip")
        toggle_layout = QVBoxLayout(self.toggle_strip)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(0)
        toggle_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.toggle_btn = QPushButton("❮")  # Show state initially
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.clicked.connect(self.parent.output_dock_toggle)
        self.toggle_btn.setToolTip("Show panel")
        self.toggle_btn.setObjectName("toggle_strip_button")
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        output_layout.addWidget(self.toggle_strip)

        self.output_label = QSvgWidget()
        output_layout.addWidget(self.output_label)
        self.output_label.setFixedWidth(28)

    def paintEvent(self, event):
        if self.parent.theme.is_light():
            self.output_label.load(":/vectors/outputs_label_light.svg")
        else:
            self.output_label.load(":/vectors/outputs_label_dark.svg")
        return super().paintEvent(event)

class CadComponentCheckbox(QWidget):
    def __init__(self, backend:object, parent):
        super().__init__(parent)
        self.parent = parent
        # Fetch checkbox data
        data = backend.get_3d_components()
        self.setObjectName("cad_custom_selector")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.checkbox_layout = QHBoxLayout(self)
        self.checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self.checkbox_layout.setSpacing(0)
        self.checkbox_layout.addStretch()

        self.checkboxes = []
        for option in data:
            label = option[0]
            check_box = QCheckBox(label)
            check_box.setObjectName(label)
            function_name = option[1]
            self.component_connect(check_box, function_name)
            self.checkbox_layout.addWidget(check_box)
            self.checkboxes.append(check_box)
            
            # Default check for "Model"
            if label == "Model":
                check_box.setChecked(True)
        self.checkbox_layout.addStretch()

    def component_connect(self, check_box, f):
        background = "gradient_light"
        if not self.parent.theme.is_light():
            background = "gradient_dark"
            
        def on_click(state):
            if state:
                # Uncheck others
                for cb in self.checkboxes:
                    if cb != check_box:
                        cb.blockSignals(True)
                        cb.setChecked(False)
                        cb.blockSignals(False)
                QApplication.processEvents()
                # Call display function
                f(self.parent, background)
            else:
                # If trying to uncheck the active one, treat it as re-click or ignore?
                # Usually radio behavior prevents unchecking.
                # Re-check it to enforce selection? Or allow empty view?
                # User says: "when a check box is checked, other checkboxes should be unchecked"
                # Let's enforce single selection.
                check_box.blockSignals(True)
                check_box.setChecked(True)
                check_box.blockSignals(False)

        check_box.clicked.connect(on_click)

# Standalone testing
# python -m osdag_gui.ui.windows.template_page
from osdag_core.design_type.connection.fin_plate_connection import FinPlateConnection
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    app = QApplication(sys.argv)
    window = CustomWindow("Fin Plate Connection", FinPlateConnection, None)
    window.showMaximized()
    window.show()
    sys.exit(app.exec())
