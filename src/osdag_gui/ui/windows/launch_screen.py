"""
Launch screen UI for Osdag GUI.
Displays splash screen with animation and logos.
"""
import osdag_gui.resources.resources_rc

from PySide6.QtCore import (QCoreApplication, QMetaObject, QEasingCurve,
                            QRect, QTimer, Qt, QPropertyAnimation)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QLabel, QWidget)
from PySide6.QtSvgWidgets import QSvgWidget
import os

class OsdagLaunchScreen(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"SplashScreen_MainWindow")
        MainWindow.resize(610, 400)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowIcon(QIcon(":/images/osdag_logo.png"))

        def close_on_click(event):
            MainWindow.hide()
        
        MainWindow.mouseDoubleClickEvent = close_on_click
        MainWindow.setCursor(Qt.CursorShape.ArrowCursor)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"SplashScreen_CentralWidget")

        # Use instead of QSvgWidget
        self.AnimatedGIF = PNGSequencePlayer(self.centralwidget)
        self.AnimatedGIF.setObjectName(u"SplashScreen_AnimatedGIF")
        self.AnimatedGIF.setGeometry(QRect(330, 110, 320, 180))
        
        from pathlib import Path
        # Use module's location to find resources - works on Linux/Windows/Mac
        # pathlib automatically handles path separators for each OS
        module_dir = Path(__file__).resolve().parent.parent.parent  # Goes up to osdag_gui/
        base_path = module_dir / "resources" / "animation"
        
        if base_path.exists():
            animation_path = str(base_path / "{:04d}.png")
            self.AnimatedGIF.load_sequence(animation_path, 96, 34)
        else:
            print(f"Warning: Animation path not found: {base_path}")

        self.AestheticVector = QSvgWidget(self.centralwidget)
        self.AestheticVector.setObjectName(u"SplashScreen_AestheticVector")
        self.AestheticVector.setGeometry(QRect(0, 0, 610, 380))

        self.OsdagLogo = QSvgWidget(self.centralwidget)
        self.OsdagLogo.setObjectName(u"SplashScreen_OsdagLogo")
        self.OsdagLogo.setGeometry(QRect(20, 20, 81, 81))

        # ======== POP-IN ANIMATION ========
        # Set initial small size at the same position
        start_rect = QRect(45, 45, 10, 10)  # Start with a small size (adjust as needed)
        end_rect = QRect(20, 20, 81, 81)    # End with the desired size (same as your original)

        self.OsdagLogo.setGeometry(start_rect)

        # Create geometry (size and position) animation
        self.logo_pop_anim = QPropertyAnimation(self.OsdagLogo, b"geometry")
        self.logo_pop_anim.setDuration(1000)  # 1 second duration
        self.logo_pop_anim.setStartValue(start_rect)
        self.logo_pop_anim.setEndValue(end_rect)
        self.logo_pop_anim.setEasingCurve(QEasingCurve.OutBack)  # Adds a slight overshoot for a "pop" feel

        # Start animation
        self.logo_pop_anim.start()
        # ======== END OF ANIMATION ========

        self.OsdagLabel = QSvgWidget(self.centralwidget)
        self.OsdagLabel.setObjectName(u"SplashScreen_OsdagLabel")
        self.OsdagLabel.setGeometry(QRect(115, 40, 127, 56)) # Exact ratio 127 = (217/96)(size)*56  
              
        self.OsdagTagline = QSvgWidget(self.centralwidget)
        self.OsdagTagline.setObjectName(u"SplashScreen_OsdagTagline")
        self.OsdagTagline.setGeometry(QRect(20, 120, 350, 29)) # Exact ratio 322 = (985/95)(size)*31

        self.VersionLabel = QSvgWidget(self.centralwidget)
        self.VersionLabel.setObjectName(u"SplashScreen_VersionLabel")
        self.VersionLabel.setGeometry(QRect(15, 150, 92, 24)) # Exact ratio 92 = (73/19)(size)*24

        self.DescriptionLabel = QSvgWidget(self.centralwidget)
        self.DescriptionLabel.setObjectName(u"SplashScreen_DescriptionLabel")
        self.DescriptionLabel.setGeometry(QRect(20, 190, 321, 90)) # Exact ratio 322 = (985/95)(size)*31
        
        self.LoadingLabel = QLabel(self.centralwidget)
        self.LoadingLabel.setObjectName(u"SplashScreen_LoadingLabel")
        self.LoadingLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.LoadingLabel.setGeometry(QRect(20, 290, 160, 25))
        self.LoadingLabel.setObjectName("splash_loading_label")
        self.LoadingLabel.setFont(QFont("Ubuntu Sans", 11))

        # aligned at to right with margin(top = right = 10 wrt size of MainWindow)
        self.IITBLogo = QSvgWidget(self.centralwidget)
        self.IITBLogo.setObjectName(u"SplashScreen_IITBLogo")
        self.IITBLogo.setGeometry(QRect(508, 10, 92, 90)) # Exact ratio 92 = (1200/1176)(size)*90

        # All 3 are aligned in bottom with line y = 340+41 = 357+24
        self.FOSSEELogo = QSvgWidget(self.centralwidget)
        self.FOSSEELogo.setObjectName(u"SplashScreen_FOSSEELogo")
        self.FOSSEELogo.setGeometry(QRect(20, 330, 138, 51)) # Exact ratio 138 = (1883/695)(size)*51

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        # To Trigger Updation
        self.show_dot = 0
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.simulateLoading)
        # Blinking Time
        self.timer.start(1000)

    def simulateLoading(self):
        if self.show_dot == 0:
            self.LoadingLabel.setText(f"Loading Application .  ")
            self.show_dot = 1
        elif self.show_dot == 1:
            self.LoadingLabel.setText(f"Loading Application .. ")
            self.show_dot = 2
        elif self.show_dot == 2:
            self.LoadingLabel.setText(f"Loading Application ...")
            self.show_dot = 3
        elif self.show_dot == 3:
            self.LoadingLabel.setText(f"Loading Application    ")
            self.show_dot = 0

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("Splash Screen", u"Splash Screen", None))

        self.AestheticVector.load(":/vectors/contour_lines.svg")
        
        self.OsdagLogo.load(":/vectors/Osdag_logo.svg")

        self.OsdagLabel.load(":/vectors/Osdag_label_light.svg")

        self.OsdagTagline.load(":/vectors/Osdag_tagline_light.svg")
        
        self.VersionLabel.load(":/vectors/version.svg")

        self.DescriptionLabel.load(":/vectors/description_label.svg")

        self.LoadingLabel.setText(f"Loading Application    ")

        self.IITBLogo.load(":/vectors/IITB_logo_light.svg")

        self.FOSSEELogo.load(":/vectors/FOSSEE_light.svg")

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QApplication

class PNGSequencePlayer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frames = []
        self.current_frame = 0
        self.frame_count = 0
        self.timer = QTimer()
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)  # Use precise timer for smooth animation
        self.setScaledContents(True)
        self.timer.timeout.connect(self.next_frame)
        self.loop = False
        self._target_size = None
        
    def load_sequence(self, base_path, frame_count, fps=24, loop=False):
        """
        Load PNG sequence
        base_path: path pattern like ":/animation/{:04d}.png"
        frame_count: total number of frames
        fps: frames per second
        """
        self.frame_count = frame_count
        self.frames = []
        self.loop = loop
        self._target_size = self.size()
        
        # Pre-load and pre-scale all frames for smoother playback
        for i in range(1, frame_count + 1):
            frame_path = base_path.format(i)
            pixmap = QPixmap(frame_path)
            if not pixmap.isNull():
                # Pre-scale to widget size for faster rendering
                if self._target_size.isValid() and self._target_size.width() > 0:
                    pixmap = pixmap.scaled(
                        self._target_size, 
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                self.frames.append(pixmap)
            
            # Process events periodically to keep UI responsive during loading
            if i % 10 == 0:
                QApplication.processEvents()
        
        # Show first frame immediately
        if self.frames:
            self.setPixmap(self.frames[0])
        
        # Set timer interval based on FPS
        interval = int(1000 / fps)  # Convert to milliseconds
        self.timer.start(interval)
        
    def next_frame(self):
        if self.frames:
            self.current_frame += 1
            
            # Stop when reaching the end if not looping
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0  # Loop back to start
                else:
                    self.timer.stop()  # Stop animation
                    self.current_frame = len(self.frames) - 1  # Stay on last frame
                    return
            
            self.setPixmap(self.frames[self.current_frame])
    
    def stop_animation(self):
        self.timer.stop()
        
    def start_animation(self):
        if self.frames and not self.timer.isActive():
            self.current_frame = 0
            self.timer.start()