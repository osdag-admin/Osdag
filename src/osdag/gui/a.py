import sys
import time
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QDialog, QLabel
from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor
import math

class CircularProgressWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.setFixedSize(100, 100)  # Larger size for better quality
        
        # Timer for animation - higher frame rate for smoother motion
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)  # ~60 FPS for ultra smooth animation
    
    def rotate(self):
        self.angle = (self.angle - 6) % 360  # Smaller increment for smoother rotation
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
        self.setFixedSize(220, 170)  # Slightly larger for the bigger spinner
        
        # Set up layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)  # Better spacing
        
        # Add circular progress widget
        self.circular_progress = CircularProgressWidget()
        layout.addWidget(self.circular_progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add loading text
        self.loading_label = QLabel("Please Wait...")
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
        
        # Enhanced dialog styling
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(255, 255, 255, 0.98);
                border-radius: 12px;
                border: 1px solid rgba(200, 200, 200, 0.8);
            }
        """)
    
    def closeEvent(self, event):
        self.circular_progress.stop_animation()
        super().closeEvent(event)

# Dummy thread to simulate background task
class DummyThread(QThread):
    finished = Signal()

    def __init__(self, delay=2, parent=None):
        super().__init__(parent)
        self.delay = delay

    def run(self):
        # simulate work
        time.sleep(self.delay)
        self.finished.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Loading Spinner Test - PySide6")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # Button for regular spinner
        btn = QPushButton("Start Loading", self)
        btn.clicked.connect(self.start_regular_loading)
        layout.addWidget(btn)

    def start_regular_loading(self):
        self.loading_widget = ModernLoadingDialog(self)

        # Center the dialog on parent
        parent_geometry = self.geometry()
        x = parent_geometry.x() + (parent_geometry.width() - self.loading_widget.width()) // 2
        y = parent_geometry.y() + (parent_geometry.height() - self.loading_widget.height()) // 2
        self.loading_widget.move(x, y)

        # Background thread simulation
        self.thread_1 = DummyThread(3, self)  # 3 sec "work"
        self.thread_1.finished.connect(lambda: print("Task finished"))
        self.thread_1.finished.connect(self.loading_widget.close)
        self.thread_1.finished.connect(self.loading_widget.circular_progress.stop_animation)

        # Show dialog and start thread
        self.loading_widget.show()
        self.thread_1.start()

    # Your original function replacement
    def start_loadingWindow(self, main=None, data=None):
        """
        Replace your original function with this one
        """
        self.loading_widget = ModernLoadingDialog(self)
        
        # Center the dialog on parent window
        parent_geometry = self.geometry()
        x = parent_geometry.x() + (parent_geometry.width() - self.loading_widget.width()) // 2
        y = parent_geometry.y() + (parent_geometry.height() - self.loading_widget.height()) // 2
        self.loading_widget.move(x, y)
        
        # Your existing thread logic (assuming DummyThread is your actual thread class)
        self.thread_1 = DummyThread(0.00001, self)
        self.thread_1.start()
        self.thread_2 = DummyThread(0.00001, self)
        
        self.thread_1.finished.connect(lambda: self.loading_widget.show())
        self.thread_1.finished.connect(lambda: self.thread_2.start())
        self.thread_2.finished.connect(lambda: self.parent.common_function_for_save_and_design(main, data, "Design"))
        self.thread_2.finished.connect(lambda: self.loading_widget.close())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())