"""
Minimalist main application window with titlebar and native Windows snap functionality.
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTabBar, QApplication
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtCore import QOperatingSystemVersion
import ctypes
from ctypes import wintypes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimalist Window")
        self.setCursor(Qt.CursorShape.ArrowCursor)

        # Window setup
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableGeometry()
        window_width = int(7 * screen_size.width() / 10)
        window_height = int(7 * screen_size.height() / 8)
        x = int((screen_size.width() - window_width) / 2)
        y = int((screen_size.height() - window_height) / 2)
        self.setGeometry(x, y, window_width, window_height)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.btn_size = QSize(46, 30)
        self.init_ui()
        
        # Enable native Windows Aero Snap after window is shown
        QApplication.instance().processEvents()

    def showEvent(self, event):
        """Enable native Windows snap when window is shown."""
        super().showEvent(event)
        if QOperatingSystemVersion.currentType() == QOperatingSystemVersion.Windows:
            self.enable_windows_snap()

    def enable_windows_snap(self):
        """Enable native Windows Aero Snap functionality for frameless window."""
        try:
            hwnd = int(self.winId())
            
            # Define Windows constants
            GWL_STYLE = -16
            WS_CAPTION = 0x00C00000
            WS_THICKFRAME = 0x00040000
            WS_MINIMIZEBOX = 0x00020000
            WS_MAXIMIZEBOX = 0x00010000
            WS_SYSMENU = 0x00080000
            
            # Get current style
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
            
            # Add native window styles for snap to work (but keep frameless appearance)
            new_style = style | WS_THICKFRAME | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
            
            # Set new style
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)
            
            # Extend frame into client area to hide default titlebar but keep snap functionality
            DWM_BB_ENABLE = 0x00000001
            DWM_BB_BLURREGION = 0x00000002
            
            class DWM_BLURBEHIND(ctypes.Structure):
                _fields_ = [
                    ("dwFlags", wintypes.DWORD),
                    ("fEnable", wintypes.BOOL),
                    ("hRgnBlur", wintypes.HRGN),
                    ("fTransitionOnMaximized", wintypes.BOOL)
                ]
            
            # Enable blur behind
            bb = DWM_BLURBEHIND()
            bb.dwFlags = DWM_BB_ENABLE
            bb.fEnable = True
            bb.hRgnBlur = None
            bb.fTransitionOnMaximized = False
            
            try:
                ctypes.windll.dwmapi.DwmEnableBlurBehindWindow(hwnd, ctypes.byref(bb))
            except:
                pass
            
            # Extend frame into client area
            class MARGINS(ctypes.Structure):
                _fields_ = [
                    ("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int)
                ]
            
            # Extend frame by 1 pixel on all sides to enable snap while keeping custom appearance
            margins = MARGINS(-1, -1, -1, -1)
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
            
            # Force window to redraw
            SWP_FRAMECHANGED = 0x0020
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOZORDER = 0x0004
            ctypes.windll.user32.SetWindowPos(
                hwnd, None, 0, 0, 0, 0,
                SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER
            )
            
        except Exception as e:
            print(f"Failed to enable Windows snap: {e}")

    def nativeEvent(self, eventType, message):
        """Handle Windows messages to enable custom titlebar dragging with snap."""
        if eventType == b"windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(int(message))
            
            # WM_NCHITTEST - let Windows know where the caption (draggable area) is
            if msg.message == 0x0084:  # WM_NCHITTEST
                # Get cursor position relative to window
                x = ctypes.wintypes.WORD(msg.lParam & 0xFFFF).value
                y = ctypes.wintypes.WORD((msg.lParam >> 16) & 0xFFFF).value
                
                # Convert screen coordinates to window coordinates
                point = ctypes.wintypes.POINT(x, y)
                ctypes.windll.user32.ScreenToClient(int(self.winId()), ctypes.byref(point))
                
                # Define draggable area (tab bar area)
                draggable_height = self.tab_bar.height() + 10
                
                # Check if cursor is in titlebar area
                if point.y < draggable_height and point.y >= 0:
                    # Check if not over buttons
                    button_area_width = self.minimize_btn.width() + self.maximize_btn.width() + self.close_btn.width()
                    if point.x < self.width() - button_area_width and point.x >= 0:
                        # HTCAPTION tells Windows this is the draggable caption area
                        return True, 2  # 2 = HTCAPTION
            
            # WM_NCCALCSIZE - tell Windows not to draw default frame but allow proper maximize
            elif msg.message == 0x0083:  # WM_NCCALCSIZE
                if msg.wParam:
                    # When wParam is TRUE, we need to handle maximized state properly
                    # Let Windows handle it but adjust for our custom frame
                    return False  # Let default processing happen
                return True, 0
            
            # WM_GETMINMAXINFO - set proper size limits for maximized window
            elif msg.message == 0x0024:  # WM_GETMINMAXINFO
                class MINMAXINFO(ctypes.Structure):
                    _fields_ = [
                        ("ptReserved", ctypes.wintypes.POINT),
                        ("ptMaxSize", ctypes.wintypes.POINT),
                        ("ptMaxPosition", ctypes.wintypes.POINT),
                        ("ptMinTrackSize", ctypes.wintypes.POINT),
                        ("ptMaxTrackSize", ctypes.wintypes.POINT),
                    ]
                
                info = ctypes.cast(msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                
                # Get screen work area (excludes taskbar)
                screen = QGuiApplication.primaryScreen()
                screen_rect = screen.availableGeometry()
                
                # Set maximum size to screen work area
                info.ptMaxSize.x = screen_rect.width()
                info.ptMaxSize.y = screen_rect.height()
                info.ptMaxPosition.x = screen_rect.x()
                info.ptMaxPosition.y = screen_rect.y()
                
                return True, 0
        
        return super().nativeEvent(eventType, message)

    def init_ui(self):
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 0, 1, 1)
        main_layout.setSpacing(0)

        # Top titlebar layout
        titlebar_layout = QHBoxLayout()
        titlebar_layout.setContentsMargins(5, 0, 5, 0)
        titlebar_layout.setSpacing(0)

        # Single tab
        self.tab_bar = QTabBar()
        self.tab_bar.addTab("Home")
        self.tab_bar.setTabsClosable(False)
        self.tab_bar.setMovable(False)
        titlebar_layout.addWidget(self.tab_bar)
        
        # Install event filter for double-click maximize/restore
        self.tab_bar.installEventFilter(self)
        
        titlebar_layout.addStretch(1)

        # Window control buttons
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setFixedSize(self.btn_size)
        self.minimize_btn.clicked.connect(self.showMinimized)
        titlebar_layout.addWidget(self.minimize_btn)

        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setFixedSize(self.btn_size)
        self.maximize_btn.clicked.connect(self.toggle_maximize_restore)
        titlebar_layout.addWidget(self.maximize_btn)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(self.btn_size)
        self.close_btn.clicked.connect(self.close)
        titlebar_layout.addWidget(self.close_btn)

        main_layout.addLayout(titlebar_layout)

        # Empty main content area
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #ffffff;")
        main_layout.addWidget(self.content_widget)

        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                border: 1px solid #90af13;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                border: 1px solid #c0c0c0;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

    def toggle_maximize_restore(self):
        """Toggles between maximized and normal window states and updates the icon."""
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setText("□")
        else:
            self.showMaximized()
            self.maximize_btn.setText("❐")
    
    def changeEvent(self, event):
        """Handle window state changes to adjust geometry."""
        if event.type() == QEvent.WindowStateChange:
            if self.isMaximized():
                # Remove margins when maximized to fit screen perfectly
                self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
            else:
                # Restore margins when not maximized
                self.centralWidget().layout().setContentsMargins(1, 0, 1, 1)
        super().changeEvent(event)

    def eventFilter(self, obj, event):
        """Handle double-click on tab bar to maximize/restore."""
        if event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.LeftButton:
                self.toggle_maximize_restore()
                return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())