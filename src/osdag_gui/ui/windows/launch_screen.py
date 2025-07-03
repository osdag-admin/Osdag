import osdag_gui.resources.resources_rc

from PySide6.QtCore import (QCoreApplication, QMetaObject, QEasingCurve,
                            QRect, QTimer, Qt, QPropertyAnimation, QFile)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QLabel, QWidget)
from PySide6.QtSvgWidgets import QSvgWidget

class OsdagLaunchScreen(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"SplashScreen_MainWindow")
        MainWindow.resize(610, 400)
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowIcon(QIcon(":/vectors/Osdag_logo.svg"))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"SplashScreen_CentralWidget")
        self.centralwidget.setStyleSheet("""
            #SplashScreen_CentralWidget {
                border: 1px solid #90af13;
                border-radius: 5px;
                background-image: url(':/backgrounds/splash_bg.jpg');
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        self.AnimatedGIF = QSvgWidget(self.centralwidget)
        self.AnimatedGIF.setObjectName(u"SplashScreen_AnimatedGIF")
        self.AnimatedGIF.setGeometry(QRect(400, 150, 191, 181))
        

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
        self.LoadingLabel.setAlignment(Qt.AlignCenter)
        self.LoadingLabel.setGeometry(QRect(20, 290, 130, 25))
        self.LoadingLabel.setStyleSheet("""
                QLabel {
                        background-color: rgba(255,255,255,0.3)
                }
        """)
        self.LoadingLabel.setFont(QFont("Menlo", 9))

        # aligned at to right with margin(top = right = 10 wrt size of MainWindow)
        self.IITBLogo = QSvgWidget(self.centralwidget)
        self.IITBLogo.setObjectName(u"SplashScreen_IITBLogo")
        self.IITBLogo.setGeometry(QRect(539, 10, 61, 60)) # Exact ratio 61 = (1200/1176)(size)*60

        # All 3 are aligned in bottom with line y = 340+41 = 357+24
        self.FOSSEELogo = QSvgWidget(self.centralwidget)
        self.FOSSEELogo.setObjectName(u"SplashScreen_FOSSEELogo")
        self.FOSSEELogo.setGeometry(QRect(20, 340, 111, 41)) # Exact ratio 111 = (1883/695)(size)*41
        # Gap of 19px in x
        self.MOSLogo = QSvgWidget(self.centralwidget)
        self.MOSLogo.setObjectName(u"SplashScreen_MOSLogo")
        self.MOSLogo.setGeometry(QRect(150, 340, 84, 41)) # Exact ratio 111 = (1883/695)(size)*41
        # Gap of 19px in x
        self.ConstructsteelLogo = QSvgWidget(self.centralwidget)
        self.ConstructsteelLogo.setObjectName(u"SplashScreen_ConstructsteelLogo")
        self.ConstructsteelLogo.setGeometry(QRect(253, 357, 211, 24)) # Exact ratio 211 = (904/103)(size)*24

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

        self.AnimatedGIF.load(":/vectors/AnimateComponent_back.svg")

        self.AestheticVector.load(":/vectors/contour_lines.svg")
        
        self.OsdagLogo.load(":/vectors/Osdag_logo.svg")

        self.OsdagLabel.load(":/vectors/Osdag_label.svg")

        self.OsdagTagline.load(":/vectors/Osdag_tagline.svg")
        
        self.VersionLabel.load(":/vectors/version.svg")

        self.DescriptionLabel.load(":/vectors/description_label.svg")

        self.LoadingLabel.setText(f"Loading Application    ")

        self.IITBLogo.load(":/vectors/IITB_logo.svg")

        self.FOSSEELogo.load(":/vectors/FOSSEE_logo.svg")
   
        self.MOSLogo.load(":/vectors/MOS_logo.svg")
   
        self.ConstructsteelLogo.load(":/vectors/ConstructSteel_logo.svg")
