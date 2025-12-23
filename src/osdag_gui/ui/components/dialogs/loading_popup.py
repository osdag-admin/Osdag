import sys
import multiprocessing as mp
from PySide6.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QIcon


class CircularProgressWidget(QLabel):
    def __init__(self, is_light_theme, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.is_light_theme = is_light_theme
        self.setFixedSize(100, 100)
        
        # Higher frame rate for smoother motion
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        # ~60 FPS for ultra smooth animation
        self.timer.start(16)
    
    def rotate(self):
        # Smaller increment for ultra-smooth rotation (3 degrees instead of 6)
        self.angle = (self.angle - 6) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Enable high-quality rendering
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        
        # Calculate center and radius using integers from the start
        rect = self.rect()
        center_x = rect.width() // 2
        center_y = rect.height() // 2
        radius = min(center_x, center_y) - 12
        
        # Ensure all coordinates are integers
        x = center_x - radius
        y = center_y - radius
        w = 2 * radius
        h = 2 * radius
        
        # Set up pen with precise width
        pen = QPen()
        pen.setWidthF(3.0)  # Use floating point width
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        
        # Draw background circle with subtle color
        pen.setColor(QColor(230, 230, 230))  # Lighter background
        painter.setPen(pen)
        painter.drawEllipse(x, y, w, h)
        
        # Draw progress arc with precise positioning
        # Simplified theme detection - you can pass theme via pipe if needed
        if self.is_light_theme:
            pen.setColor(QColor(0x90, 0xAF, 0x13))  #90AF13
        else:
            pen.setColor(QColor(0x6B, 0x7D, 0x20))  #6B7D20
        painter.setPen(pen)
        
        # Use integer angles
        start_angle = int(self.angle * 16)  # Qt uses 16ths of a degree
        span_angle = 80 * 16  # Arc span
        
        painter.drawArc(x, y, w, h, start_angle, span_angle)
    
    def stop_animation(self):
        self.timer.stop()


class ModernLoadingDialog(QDialog):
    def __init__(self, parent=None, is_light_theme=True):
        super().__init__(parent)
        self.is_light_theme = is_light_theme
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setModal(False)  # Changed to False since it's in separate process
        self.setFixedSize(220, 170)
        try:
            self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        except:
            pass  # Ignore if icon not available
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # Keep window on top
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
        # Set up layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Add circular progress widget
        self.circular_progress = CircularProgressWidget(is_light_theme)
        layout.addWidget(self.circular_progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add loading text
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setObjectName("loading_label")
        if self.is_light_theme:
            self.loading_label.setStyleSheet("""
                QLabel#loading_label{
                    font-size: 15px;
                    font-weight: 500;
                    color: #444444;
                    margin-top: 5px;
                }
            """)
        else:
            self.loading_label.setStyleSheet("""
                QLabel#loading_label{
                    font-size: 15px;
                    font-weight: 500;
                    color: #D0D0D0;
                    margin-top: 5px;
                }
            """)

        layout.addWidget(self.loading_label)
        self.setLayout(layout)
        
        # Center on screen
        self.center_on_screen()
    
    def center_on_screen(self):
        """Center the dialog in the middle of the screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        
        self.move(x, y)
    
    def closeEvent(self, event):
        self.circular_progress.stop_animation()
        super().closeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        
        rect = self.rect().adjusted(0, 0, -1, -1)
        radius = 12
        
        # Fill rounded rectangle
        painter.setPen(Qt.PenStyle.NoPen)
        if self.is_light_theme:
            painter.setBrush(QColor(255, 255, 255, 250))
        else:
            painter.setBrush(QColor(56, 56, 56, 250))
        painter.drawRoundedRect(rect, radius, radius)
        
        # Draw subtle border
        pen = QPen(QColor(200, 200, 200, 204))
        pen.setWidth(1)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)
        
        super().paintEvent(event)


def run_loading_dialog_process(stop_event, is_light_theme=True):
    """
    Function to run in separate process
    Args:
        stop_event: multiprocessing.Event to signal when to close
        is_light_theme: bool indicating theme preference
    """
    app = QApplication(sys.argv)
    dialog = ModernLoadingDialog(is_light_theme=is_light_theme)
    
    # Check stop event periodically
    timer = QTimer()
    timer.timeout.connect(lambda: dialog.close() if stop_event.is_set() else None)
    timer.start(100)  # Check every 100ms
    
    dialog.show()
    app.exec()


class LoadingDialogManager:
    """
    Manager class to control the loading dialog.
    Uses in-process dialog on Linux to avoid window duplication issues.
    Uses separate process on Windows/macOS for better performance.
    """
    def __init__(self, is_light_theme=True):
        self.process = None
        self.stop_event = None
        self.is_light_theme = is_light_theme
        self._dialog = None  # For in-process mode
        
        # Detect OS - Linux has issues with multiprocess GUI windows
        import platform
        self._use_process = platform.system() != "Linux"
    
    def show(self):
        """Show the loading dialog"""
        if self._use_process:
            # Windows/macOS - use separate process
            if self.process is not None and self.process.is_alive():
                return  # Already running
            
            self.stop_event = mp.Event()
            self.process = mp.Process(
                target=run_loading_dialog_process,
                args=(self.stop_event, self.is_light_theme)
            )
            self.process.start()
        else:
            # Linux - use in-process dialog to avoid duplicate window issues
            if self._dialog is None:
                self._dialog = ModernLoadingDialog(is_light_theme=self.is_light_theme)
            self._dialog.show()
            QApplication.processEvents()  # Ensure dialog is drawn
    
    def hide(self):
        """Hide the loading dialog"""
        if self._use_process:
            if self.process is not None and self.process.is_alive():
                self.stop_event.set()
                self.process.join(timeout=2)  # Wait up to 2 seconds
                if self.process.is_alive():
                    self.process.terminate()  # Force terminate if still running
                self.process = None
                self.stop_event = None
        else:
            # Linux - close in-process dialog
            if self._dialog is not None:
                self._dialog.hide()
                self._dialog.circular_progress.stop_animation()
                self._dialog = None
    
    def __del__(self):
        """Cleanup when manager is destroyed"""
        self.hide()