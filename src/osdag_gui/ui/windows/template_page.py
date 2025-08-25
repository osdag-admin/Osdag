import sys, os
import osdag_gui.resources.resources_rc
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QTabBar,
    QMessageBox, QMenuBar, QMenu, QSplitter, QSizePolicy
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEvent, Signal, QEasingCurve, QTimer
from PySide6.QtGui import QIcon, QFont, QPixmap, QGuiApplication, QKeySequence, QAction

from osdag_gui.ui.components.floating_nav_bar import SidebarWidget
from osdag_gui.ui.components.input_dock import InputDock
from osdag_gui.ui.components.output_dock import OutputDock
from osdag_gui.ui.components.log_dock import LogDock

import time
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QDialog, QProgressBar, QCheckBox, QComboBox, QLineEdit

class CustomWindow(QWidget):
    openNewTab = Signal(str)
    outputDockIconToggle = Signal()
    inputDockIconToggle = Signal()
    def __init__(self, title: str, backend: object, parent):
        super().__init__()
        self.parent = parent
        self.backend = backend
        self.current_tab_index = 0
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                margin: 0px;
                padding: 0px;
            }
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
            QMenuBar::item:selected {
                background: #FFFFFF;
            }
            QMenuBar::item:pressed {
                background: #E8E8E8;
            }
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 4px;
                padding: 0px;
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
                background: #F0F0F0;
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

        self.init_ui(title)
        self.sidebar = SidebarWidget(parent=self)
        self.sidebar.openNewTab.connect(self.openNewTabEmit)
        self.sidebar.setParent(self)
        self.sidebar.resize_sidebar(self.width(), self.height())
        self.sidebar.move(-self.sidebar.width() + 12, self.menu_bar.height())
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.sidebar_animation.setDuration(300)
        self.sidebar.installEventFilter(self)
        self.sidebar.raise_()

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
        end_x = 0
        top_offset = self.menu_bar.height()
        self.sidebar_animation.setStartValue(self.sidebar.geometry())
        self.sidebar_animation.setEndValue(QRect(end_x, top_offset, self.sidebar.width(), self.sidebar.height()))
        self.sidebar_animation.start()
        self.sidebar.raise_()

    def slide_out(self):
        self.sidebar_animation.stop()
        end_x = -self.sidebar.width() + 12
        top_offset = self.menu_bar.height()
        self.sidebar_animation.setStartValue(self.sidebar.geometry())
        self.sidebar_animation.setEndValue(QRect(end_x, top_offset, self.sidebar.width(), self.sidebar.height()))
        self.sidebar_animation.start()

    def init_ui(self, title: str):
        main_v_layout = QVBoxLayout(self)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)

        self.menu_bar = QMenuBar(self)
        self.menu_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.menu_bar.setFixedHeight(28)
        self.menu_bar.setContentsMargins(0, 0, 0, 0)
        main_v_layout.addWidget(self.menu_bar)
        self.create_menu_bar_items()

        self.body_widget = QWidget()
        self.layout = QHBoxLayout(self.body_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal, self.body_widget)
        self.input_dock = InputDock(backend=self.backend, parent=self)
        self.input_dock_active = True
        input_dock_width = self.input_dock.sizeHint().width()
        self._input_dock_default_width = input_dock_width
        self.splitter.addWidget(self.input_dock)
        self.input_dock.setStyleSheet(self.input_dock.styleSheet())

        central_widget = QWidget()
        central_H_layout = QHBoxLayout(central_widget)

        # Add dock indicator labels
        self.input_dock_label = InputDockIndicator(parent=self)
        self.input_dock_label.setVisible(False)
        central_H_layout.setContentsMargins(6, 0, 0, 0)
        central_H_layout.setSpacing(0)
        central_H_layout.addWidget(self.input_dock_label, 1)

        central_V_layout = QVBoxLayout()
        central_V_layout.setContentsMargins(0, 0, 0, 0)
        central_V_layout.setSpacing(0)
        central_V_layout.addStretch(7)
        self.logs_dock = LogDock()
        self.logs_dock_active = True
        self.logs_dock.setVisible(False)
        central_V_layout.addWidget(self.logs_dock, 2)
        central_H_layout.addLayout(central_V_layout, 6)

        # Add output dock indicator label
        self.output_dock_label = OutputDockIndicator(parent=self)
        self.output_dock_label.setVisible(True)
        central_H_layout.addWidget(self.output_dock_label, 1)
        self.splitter.addWidget(central_widget)

        self.output_dock = OutputDock(backend=self.backend, parent=self)
        self.output_dock_active = True
        self.splitter.addWidget(self.output_dock)
        self.output_dock.setStyleSheet(self.output_dock.styleSheet())
        self.output_dock.hide()

        self.layout.addWidget(self.splitter)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 1)

        total_width = self.width() - self.splitter.contentsMargins().left() - self.splitter.contentsMargins().right()
        target_sizes = [0] * self.splitter.count()
        target_sizes[0] = input_dock_width
        target_sizes[2] = 0
        remaining_width = total_width - input_dock_width
        target_sizes[1] = max(0, remaining_width)
        self.splitter.setSizes(target_sizes)
        self.layout.activate()
        main_v_layout.addWidget(self.body_widget)

    def input_dock_toggle(self):
        self.input_dock.toggle_input_dock()
        self.input_dock_active = not self.input_dock_active
        
    def output_dock_toggle(self):
        self.output_dock.toggle_output_dock()
        self.output_dock_active = not self.output_dock_active
        # Show/hide output dock label based on dock state
        # self.output_dock_label.setVisible(self.output_dock_active)

    def logs_dock_toggle(self, log_dock_active):
        self.logs_dock.setVisible(log_dock_active)
        self.logs_dock_active = not self.logs_dock_active

    def update_input_label_state(self, state):
        # Show/hide input dock label based on dock state
        self.input_dock_label.setVisible(state)
    
    def update_output_label_state(self, state):
        # Show/hide input dock label based on dock state
        self.output_dock_label.setVisible(state)
        
    def create_menu_bar_items(self):
        file_menu = self.menu_bar.addMenu("File")
        load_input_action = QAction("Load Input", self)
        load_input_action.setShortcut(QKeySequence("Ctrl+L"))
        load_input_action.triggered.connect(self.on_load_input)
        file_menu.addAction(load_input_action)
        file_menu.addSeparator()
        save_input_action = QAction("Save Input", self)
        save_input_action.setShortcut(QKeySequence("Ctrl+S"))
        save_input_action.triggered.connect(self.on_save_input)
        file_menu.addAction(save_input_action)
        save_log_action = QAction("Save Log Messages", self)
        save_log_action.setShortcut(QKeySequence("Alt+M"))
        save_log_action.triggered.connect(self.on_save_log_messages)
        file_menu.addAction(save_log_action)
        create_report_action = QAction("Create Design Report", self)
        create_report_action.setShortcut(QKeySequence("Alt+C"))
        create_report_action.triggered.connect(self.on_create_design_report)
        file_menu.addAction(create_report_action)
        file_menu.addSeparator()
        save_3d_action = QAction("Save 3D Model", self)
        save_3d_action.setShortcut(QKeySequence("Alt+3"))
        save_3d_action.triggered.connect(self.on_save_3d_model)
        file_menu.addAction(save_3d_action)
        save_cad_action = QAction("Save CAD Image", self)
        save_cad_action.setShortcut(QKeySequence("Alt+I"))
        save_cad_action.triggered.connect(self.on_save_cad_image)
        file_menu.addAction(save_cad_action)
        file_menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Shift+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        edit_menu = self.menu_bar.addMenu("Edit")
        design_prefs_action = QAction("Design Preferences", self)
        design_prefs_action.setShortcut(QKeySequence("Alt+P"))
        design_prefs_action.triggered.connect(self.on_design_preferences)
        edit_menu.addAction(design_prefs_action)

        graphics_menu = self.menu_bar.addMenu("Graphics")
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+I"))
        zoom_in_action.triggered.connect(self.on_zoom_in)
        graphics_menu.addAction(zoom_in_action)
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+O"))
        zoom_out_action.triggered.connect(self.on_zoom_out)
        graphics_menu.addAction(zoom_out_action)
        pan_action = QAction("Pan", self)
        pan_action.setShortcut(QKeySequence("Ctrl+P"))
        pan_action.triggered.connect(self.on_pan)
        graphics_menu.addAction(pan_action)
        rotate_3d_action = QAction("Rotate 3D Model", self)
        rotate_3d_action.setShortcut(QKeySequence("Ctrl+R"))
        rotate_3d_action.triggered.connect(self.on_rotate_3d_model)
        graphics_menu.addAction(rotate_3d_action)
        graphics_menu.addSeparator()
        front_view_action = QAction("Show Front View", self)
        front_view_action.setShortcut(QKeySequence("Alt+Shift+F"))
        front_view_action.triggered.connect(self.on_show_front_view)
        graphics_menu.addAction(front_view_action)
        top_view_action = QAction("Show Top View", self)
        top_view_action.setShortcut(QKeySequence("Alt+Shift+T"))
        top_view_action.triggered.connect(self.on_show_top_view)
        graphics_menu.addAction(top_view_action)
        side_view_action = QAction("Show Side View", self)
        side_view_action.setShortcut(QKeySequence("Alt+Shift+S"))
        side_view_action.triggered.connect(self.on_show_side_view)
        graphics_menu.addAction(side_view_action)
        graphics_menu.addSeparator()
        model_view_action = QAction("Model", self)
        graphics_menu.addAction(model_view_action)
        beam_view_action = QAction("Beam", self)
        graphics_menu.addAction(beam_view_action)
        column_view_action = QAction("Column", self)
        graphics_menu.addAction(column_view_action)
        fin_plate_view_action = QAction("Fin Plate", self)
        graphics_menu.addAction(fin_plate_view_action)
        graphics_menu.addSeparator()
        change_bg_action = QAction("Change background", self)
        change_bg_action.triggered.connect(self.on_change_background)
        graphics_menu.addAction(change_bg_action)

        database_menu = self.menu_bar.addMenu("Database")
        download_submenu = database_menu.addMenu("Download")
        download_submenu.addAction(QAction("Column", self))
        download_submenu.addAction(QAction("Beam", self))
        download_submenu.addAction(QAction("Angle", self))
        download_submenu.addAction(QAction("Channel", self))
        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.on_reset_database)
        database_menu.addAction(reset_action)

        help_menu = self.menu_bar.addMenu("Help")
        video_tutorials_action = QAction("Video Tutorials", self)
        video_tutorials_action.triggered.connect(self.on_video_tutorials)
        help_menu.addAction(video_tutorials_action)
        design_examples_action = QAction("Design Examples", self)
        design_examples_action.triggered.connect(self.on_design_examples)
        help_menu.addAction(design_examples_action)
        help_menu.addSeparator()
        ask_question_action = QAction("Ask Us a Question", self)
        ask_question_action.triggered.connect(self.on_ask_question)
        help_menu.addAction(ask_question_action)
        about_osdag_action = QAction("About Osdag", self)
        about_osdag_action.triggered.connect(self.on_about_osdag)
        help_menu.addAction(about_osdag_action)
        help_menu.addSeparator()
        check_update_action = QAction("Check For Update", self)
        check_update_action.triggered.connect(self.on_check_for_update)
        help_menu.addAction(check_update_action)

    def resizeEvent(self, event):
        self.sidebar.resize_sidebar(self.sidebar.width(), self.height())
        top_offset = self.menu_bar.height()
        if self.sidebar.x() < 0:
            self.sidebar.move(-self.sidebar.width() + 12, top_offset)

        input_dock_width = self.input_dock.sizeHint().width()
        output_dock_width = self.output_dock.sizeHint().width()
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

    def toggle_animate(self, show: bool, dock: str = 'output'):
        sizes = self.splitter.sizes()
        n = self.splitter.count()
        if dock == 'input':
            dock_index = 0

        elif dock == 'output':
            dock_index = n - 1
        elif dock == 'log':
            self.logs_dock.setVisible(show)
            return
        else:
            print(f"Invalid dock: {dock}")
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
            # self.inputDockIconToggle.emit()
            if show:
                target_sizes[0] = input_dock.sizeHint().width()
                self.input_dock_label.setVisible(False)
            else:
                target_sizes[0] = 0
                self.input_dock_label.setVisible(True)
            target_sizes[2] = sizes[2]
            remaining_width = total_width - target_sizes[0] - target_sizes[2]
            target_sizes[1] = max(0, remaining_width)
        else:
            # self.outputDockIconToggle.emit()
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
            return
        
        self.animate_splitter_sizes(
            self.splitter,
            sizes,
            target_sizes,
            duration=100,
            on_finished=lambda: self.finalize_dock_toggle(show, dock_widget, target_sizes)
        )

    def animate_splitter_sizes(self, splitter, start_sizes, end_sizes, duration, on_finished=None):
        steps = 10
        interval = duration // steps
        step_sizes = [
            [start + (end - start) * i / steps for start, end in zip(start_sizes, end_sizes)]
            for i in range(steps + 1)
        ]

        current_step = 0

        def update_step():
            nonlocal current_step
            if current_step <= steps:
                sizes = [int(v) for v in step_sizes[current_step]]
                splitter.setSizes(sizes)
                splitter.refresh()
                splitter.parentWidget().layout().activate()
                splitter.update()
                splitter.parentWidget().update()
                self.update()
                for i in range(splitter.count()):
                    splitter.widget(i).update()
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

    def show_message(self, title, message):
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

class DummyThread(QThread):
        finished = Signal()
        def __init__(self, sec, parent):
            self.sec = sec
            super().__init__(parent=parent)
        def run(self):
            time.sleep(self.sec)
            self.finished.emit()

class InputDockIndicator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: white;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Fixed width, expanding height

        input_layout = QHBoxLayout(self)
        input_layout.setContentsMargins(0,0,0,0)
        input_layout.setSpacing(0)

        input_label = QSvgWidget(":/vectors/inputs_label.svg")
        input_layout.addWidget(input_label)

        self.toggle_strip = QWidget()
        self.toggle_strip.setStyleSheet("background-color: #94b816;")
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
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        input_layout.addWidget(self.toggle_strip)

class OutputDockIndicator(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: white;")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)  # Fixed width, expanding height

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

        self.toggle_btn = QPushButton("❮")  # Show state initially
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setFixedSize(6, 60)
        self.toggle_btn.clicked.connect(self.parent.output_dock_toggle)
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
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.toggle_btn)
        toggle_layout.addStretch()
        output_layout.addWidget(self.toggle_strip)

        output_label = QSvgWidget(":/vectors/outputs_label.svg")
        output_layout.addWidget(output_label)

# if __name__ == "__main__":
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#     app = QApplication(sys.argv)
#     window = CustomWindow("Fin Plate Connection", "FinPlateConnection")
#     window.showMaximized()
#     window.show()
#     sys.exit(app.exec())