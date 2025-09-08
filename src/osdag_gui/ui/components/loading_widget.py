import sys, time
from PySide6.QtWidgets import QApplication, QVBoxLayout, QDialog, QLabel, QProgressBar
from PySide6.QtCore import Qt, QThread, Signal, QTimer

class LinearProgressDialog(QDialog):
    """Modern modal progress dialog with thick progress bar and no title bar."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(400, 100)
        
        # Center the dialog on screen
        self.center_on_screen()
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Loading label
        self.label = QLabel("Loading...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        
        # Modern styling
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: 500;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #f1f3f4;
                height: 8px;
            }
            QProgressBar::chunk {
                background: #90AF13;
                border-radius: 4px;
            }
        """)
    
    def center_on_screen(self):
        """Center the dialog on the screen."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def set_progress(self, value: int):
        """Update progress value (0-100) and close dialog when complete."""
        value = max(0, min(100, int(value)))
        self.progress.setValue(value)
        QApplication.processEvents()
        if value >= 100:
            self.close()

class DelayThread(QThread):
    finished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        time.sleep(0.05)
        self.finished.emit()