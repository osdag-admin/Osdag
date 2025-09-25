import time
from PySide6.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QIcon

class CircularProgressWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.setFixedSize(100, 100)
        
        # Higher frame rate for smoother motion
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        # ~60 FPS for ultra smooth animation
        self.timer.start(16)
    
    def rotate(self):
        # Smaller increment for smoother rotation
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
        pen.setColor(QColor(230, 230, 230))  # Lighter, more subtle background
        painter.setPen(pen)
        painter.drawEllipse(x, y, w, h)
        
        # Draw progress arc with precise positioning
        pen.setColor(QColor(0x90, 0xAF, 0x13))  # #90AF13
        painter.setPen(pen)
        
        # Use integer angles
        start_angle = int(self.angle * 16)  # Qt uses 16ths of a degree
        span_angle = 80 * 16  # Arc span
        
        painter.drawArc(x, y, w, h, start_angle, span_angle)
    
    def stop_animation(self):
        self.timer.stop()

class ModernLoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(220, 170)
        self.setWindowIcon(QIcon(":/images/osdag_logo.png"))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Set up layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Add circular progress widget
        self.circular_progress = CircularProgressWidget()
        layout.addWidget(self.circular_progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add loading text
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 500;
                color: #444;
                margin-top: 5px;
            }
        """)
        layout.addWidget(self.loading_label)
        
        self.setLayout(layout)
        
        # Remove window background styling; custom paint will handle rounded corners and border
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
        painter.setBrush(QColor(255, 255, 255, 250))
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


class DelayThread(QThread):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        time.sleep(1)
        self.finished.emit()


if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        import sys
        app = QApplication(sys.argv)
        owns_app = True
    else:
        owns_app = False
    dialog = ModernLoadingDialog()
    QTimer.singleShot(5000, dialog.accept)
    dialog.exec()
    if owns_app:
        app.quit()
