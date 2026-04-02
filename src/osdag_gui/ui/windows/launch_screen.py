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
from PySide6.QtGui import QFontDatabase, QFont, QIcon
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

        self.AestheticVector = QSvgWidget(self.centralwidget)
        self.AestheticVector.setObjectName(u"SplashScreen_AestheticVector")
        self.AestheticVector.setGeometry(QRect(2, 3, 606, 308))

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
        self.OsdagLabel.setGeometry(QRect(115, 23, 170, 75)) # Exact ratio 127 = (217/96)(size)*56  
              
        self.OsdagTagline = QSvgWidget(self.centralwidget)
        self.OsdagTagline.setObjectName(u"SplashScreen_OsdagTagline")
        self.OsdagTagline.setGeometry(QRect(20, 120, 350, 29)) # Exact ratio 322 = (985/95)(size)*31

        self.VersionLabel = QSvgWidget(self.centralwidget)
        self.VersionLabel.setObjectName(u"SplashScreen_VersionLabel")
        self.VersionLabel.setGeometry(QRect(20, 155, 72, 10))

        self.DescriptionLabel = QSvgWidget(self.centralwidget)
        self.DescriptionLabel.setObjectName(u"SplashScreen_DescriptionLabel")
        self.DescriptionLabel.setGeometry(QRect(20, 190, 360, 112))

        self.FOSSEELogo = QSvgWidget(self.centralwidget)
        self.FOSSEELogo.setObjectName(u"SplashScreen_FOSSEELogo")
        self.FOSSEELogo.setGeometry(QRect(20, 340, 111, 41)) # Exact ratio 111 = (1883/695)(size)*41
        
        self.LoadingLabel = QLabel(self.centralwidget)
        self.LoadingLabel.setObjectName(u"SplashScreen_LoadingLabel")
        self.LoadingLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.LoadingLabel.setGeometry(QRect(20, 310, 200, 30))
        self.LoadingLabel.setObjectName("splash_loading_label")

        # aligned at to right with margin(top = right = 10 wrt size of MainWindow)
        self.IITBLogo = QSvgWidget(self.centralwidget)
        self.IITBLogo.setObjectName(u"SplashScreen_IITBLogo")
        self.IITBLogo.setGeometry(QRect(508, 10, 92, 90)) # Exact ratio 92 = (1200/1176)(size)*90

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
            self.LoadingLabel.setText(f"Loading application .  ")
            self.show_dot = 1
        elif self.show_dot == 1:
            self.LoadingLabel.setText(f"Loading application .. ")
            self.show_dot = 2
        elif self.show_dot == 2:
            self.LoadingLabel.setText(f"Loading application ...")
            self.show_dot = 3
        elif self.show_dot == 3:
            self.LoadingLabel.setText(f"Loading application    ")
            self.show_dot = 0

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("Splash Screen", u"Splash Screen", None))

        self.AestheticVector.load(":/vectors/contour_lines.svg")

        self.OsdagLogo.load(":/vectors/Osdag_logo.svg")

        self.OsdagLabel.load(":/vectors/Osdag_label_light.svg")

        self.OsdagTagline.load(":/vectors/Osdag_tagline_light.svg")
        
        self.VersionLabel.load(":/vectors/version.svg")

        self.DescriptionLabel.load(":/vectors/description_label.svg")

        self.LoadingLabel.setText(f"Loading application    ")

        self.IITBLogo.load(":/vectors/IITB_Launch.svg")

        self.FOSSEELogo.load(":/vectors/FOSSEE_light.svg")