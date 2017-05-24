# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OsdagMainPage.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1410, 1110)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/Osdag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QWidget::showMaximised()")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.myListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.myListWidget.setMinimumSize(QtCore.QSize(300, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 84, 69))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 84, 69))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(171, 194, 80))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        self.myListWidget.setPalette(palette)
        self.myListWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.myListWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.myListWidget.setStyleSheet("QListWidget\n"
"{\n"
"background-color: #abc250 ;\n"
"}")
        self.myListWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.myListWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.myListWidget.setLineWidth(4)
        self.myListWidget.setMidLineWidth(2)
        self.myListWidget.setObjectName("myListWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.myListWidget.addItem(item)
        self.gridLayout.addWidget(self.myListWidget, 0, 0, 1, 2)
        self.myStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(False)
        self.myStackedWidget.setFont(font)
        self.myStackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.myStackedWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.myStackedWidget.setObjectName("myStackedWidget")
        self.Osdagpage = QtWidgets.QWidget()
        self.Osdagpage.setObjectName("Osdagpage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Osdagpage)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_OsdagHeader = QtWidgets.QLabel(self.Osdagpage)
        self.lbl_OsdagHeader.setMinimumSize(QtCore.QSize(800, 200))
        self.lbl_OsdagHeader.setMaximumSize(QtCore.QSize(800, 200))
        self.lbl_OsdagHeader.setText("")
        self.lbl_OsdagHeader.setPixmap(QtGui.QPixmap(":/newPrefix/images/Osdag_header.png"))
        self.lbl_OsdagHeader.setScaledContents(True)
        self.lbl_OsdagHeader.setObjectName("lbl_OsdagHeader")
        self.gridLayout_2.addWidget(self.lbl_OsdagHeader, 0, 0, 2, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 738, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 2, 2, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 646, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.lbl_fosseelogo = QtWidgets.QLabel(self.Osdagpage)
        self.lbl_fosseelogo.setMinimumSize(QtCore.QSize(250, 92))
        self.lbl_fosseelogo.setMaximumSize(QtCore.QSize(250, 92))
        self.lbl_fosseelogo.setText("")
        self.lbl_fosseelogo.setPixmap(QtGui.QPixmap(":/newPrefix/images/Fossee_logo.png"))
        self.lbl_fosseelogo.setScaledContents(True)
        self.lbl_fosseelogo.setObjectName("lbl_fosseelogo")
        self.gridLayout_2.addWidget(self.lbl_fosseelogo, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(532, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 3, 1, 1, 1)
        self.lbl_iitblogo = QtWidgets.QLabel(self.Osdagpage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_iitblogo.sizePolicy().hasHeightForWidth())
        self.lbl_iitblogo.setSizePolicy(sizePolicy)
        self.lbl_iitblogo.setMinimumSize(QtCore.QSize(100, 100))
        self.lbl_iitblogo.setText("")
        self.lbl_iitblogo.setPixmap(QtGui.QPixmap(":/newPrefix/images/logoiitb.png"))
        self.lbl_iitblogo.setScaledContents(False)
        self.lbl_iitblogo.setObjectName("lbl_iitblogo")
        self.gridLayout_2.addWidget(self.lbl_iitblogo, 3, 2, 1, 1)
        self.myStackedWidget.addWidget(self.Osdagpage)
        self.Connectionpage = QtWidgets.QWidget()
        self.Connectionpage.setObjectName("Connectionpage")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Connectionpage)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mytabWidget = QtWidgets.QTabWidget(self.Connectionpage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mytabWidget.sizePolicy().hasHeightForWidth())
        self.mytabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.mytabWidget.setFont(font)
        self.mytabWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mytabWidget.setStyleSheet("QTabBar::tab {\n"
"    margin-right: 10;\n"
" }\n"
"QTabBar::tab::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QTabBar::tab{\n"
"height: 40px;\n"
"width: 200px;\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}\n"
"QTabBar::tab{\n"
"border-top-left-radius: 2px ;\n"
"border-top-right-radius: 2px ;\n"
"border-bottom-left-radius: 0px ;\n"
"border-bottom-right-radius: 0px ;\n"
"}\n"
" ")
        self.mytabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.mytabWidget.setDocumentMode(False)
        self.mytabWidget.setTabsClosable(False)
        self.mytabWidget.setMovable(False)
        self.mytabWidget.setObjectName("mytabWidget")
        self.tab1_shearconnection = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setItalic(True)
        self.tab1_shearconnection.setFont(font)
        self.tab1_shearconnection.setObjectName("tab1_shearconnection")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab1_shearconnection)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(20, 102, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 102, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 0, 6, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(87, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.rdbtn_finplate = QtWidgets.QRadioButton(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.rdbtn_finplate.setFont(font)
        self.rdbtn_finplate.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_finplate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_finplate.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ResourceFiles/images/finplate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_finplate.setIcon(icon1)
        self.rdbtn_finplate.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_finplate.setCheckable(True)
        self.rdbtn_finplate.setObjectName("rdbtn_finplate")
        self.verticalLayout.addWidget(self.rdbtn_finplate)
        self.gridLayout_3.addLayout(self.verticalLayout, 1, 1, 1, 3)
        spacerItem6 = QtWidgets.QSpacerItem(175, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 1, 4, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.rdbtn_cleat = QtWidgets.QRadioButton(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.rdbtn_cleat.setFont(font)
        self.rdbtn_cleat.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_cleat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_cleat.setStyleSheet("QRadioButton {\n"
"text-shadow : black 0.1em 0.1em 0.2em  ;\n"
"}")
        self.rdbtn_cleat.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ResourceFiles/images/cleatAngle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_cleat.setIcon(icon2)
        self.rdbtn_cleat.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_cleat.setObjectName("rdbtn_cleat")
        self.verticalLayout_2.addWidget(self.rdbtn_cleat)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 5, 1, 3)
        spacerItem7 = QtWidgets.QSpacerItem(87, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem7, 1, 8, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(87, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 2, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.rdbtn_endplate = QtWidgets.QRadioButton(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.rdbtn_endplate.setFont(font)
        self.rdbtn_endplate.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_endplate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_endplate.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ResourceFiles/images/endplate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_endplate.setIcon(icon3)
        self.rdbtn_endplate.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_endplate.setObjectName("rdbtn_endplate")
        self.verticalLayout_3.addWidget(self.rdbtn_endplate)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 2, 1, 1, 3)
        spacerItem9 = QtWidgets.QSpacerItem(175, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem9, 2, 4, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.rdbtn_seat = QtWidgets.QRadioButton(self.tab1_shearconnection)
        self.rdbtn_seat.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_seat.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/images/seatedAngle1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_seat.setIcon(icon4)
        self.rdbtn_seat.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_seat.setObjectName("rdbtn_seat")
        self.verticalLayout_4.addWidget(self.rdbtn_seat)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 2, 5, 1, 3)
        spacerItem10 = QtWidgets.QSpacerItem(87, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem10, 2, 8, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 102, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem11, 3, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 102, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem12, 3, 7, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(262, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 4, 3, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.tab1_shearconnection)
        self.btn_start.setMinimumSize(QtCore.QSize(190, 30))
        self.btn_start.setMaximumSize(QtCore.QSize(190, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start.setFont(font)
        self.btn_start.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_start.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}")
        self.btn_start.setCheckable(False)
        self.btn_start.setAutoExclusive(False)
        self.btn_start.setAutoDefault(True)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout_3.addWidget(self.btn_start, 4, 4, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(262, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem14, 4, 5, 1, 1)
        self.mytabWidget.addTab(self.tab1_shearconnection, "")
        self.tab2_momentconnection = QtWidgets.QWidget()
        self.tab2_momentconnection.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tab2_momentconnection.setObjectName("tab2_momentconnection")
        self.mytabWidget.addTab(self.tab2_momentconnection, "")
        self.horizontalLayout.addWidget(self.mytabWidget)
        self.myStackedWidget.addWidget(self.Connectionpage)
        self.tensionpage = QtWidgets.QWidget()
        self.tensionpage.setObjectName("tensionpage")
        self.label = QtWidgets.QLabel(self.tensionpage)
        self.label.setGeometry(QtCore.QRect(350, 260, 271, 111))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.myStackedWidget.addWidget(self.tensionpage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.myStackedWidget.addWidget(self.page)
        self.gridLayout.addWidget(self.myStackedWidget, 0, 2, 1, 1)
        self.comboBox_help = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.comboBox_help.setFont(font)
        self.comboBox_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBox_help.setAutoFillBackground(False)
        self.comboBox_help.setStyleSheet("QComboBox::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}\n"
"\n"
"")
        self.comboBox_help.setFrame(True)
        self.comboBox_help.setObjectName("comboBox_help")
        self.comboBox_help.addItem("")
        self.comboBox_help.addItem("")
        self.comboBox_help.addItem("")
        self.comboBox_help.addItem("")
        self.comboBox_help.addItem("")
        self.comboBox_help.addItem("")
        self.gridLayout.addWidget(self.comboBox_help, 1, 0, 1, 2)
        self.btn_connection = QtWidgets.QPushButton(self.centralwidget)
        self.btn_connection.setGeometry(QtCore.QRect(60, 120, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_connection.setFont(font)
        self.btn_connection.setMouseTracking(False)
        self.btn_connection.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_connection.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.btn_connection.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}\n"
"")
        self.btn_connection.setAutoDefault(True)
        self.btn_connection.setDefault(False)
        self.btn_connection.setObjectName("btn_connection")
        self.btn_tension = QtWidgets.QPushButton(self.centralwidget)
        self.btn_tension.setGeometry(QtCore.QRect(60, 180, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_tension.setFont(font)
        self.btn_tension.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}\n"
"")
        self.btn_tension.setAutoDefault(True)
        self.btn_tension.setObjectName("btn_tension")
        self.btn_compression = QtWidgets.QPushButton(self.centralwidget)
        self.btn_compression.setGeometry(QtCore.QRect(60, 240, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_compression.setFont(font)
        self.btn_compression.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}\n"
"")
        self.btn_compression.setAutoDefault(True)
        self.btn_compression.setObjectName("btn_compression")
        self.btn_flexural = QtWidgets.QPushButton(self.centralwidget)
        self.btn_flexural.setGeometry(QtCore.QRect(60, 300, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_flexural.setFont(font)
        self.btn_flexural.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}")
        self.btn_flexural.setAutoDefault(True)
        self.btn_flexural.setObjectName("btn_flexural")
        self.btn_beamCol = QtWidgets.QPushButton(self.centralwidget)
        self.btn_beamCol.setGeometry(QtCore.QRect(60, 360, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_beamCol.setFont(font)
        self.btn_beamCol.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}")
        self.btn_beamCol.setAutoDefault(True)
        self.btn_beamCol.setObjectName("btn_beamCol")
        self.btn_plate = QtWidgets.QPushButton(self.centralwidget)
        self.btn_plate.setGeometry(QtCore.QRect(60, 420, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_plate.setFont(font)
        self.btn_plate.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}")
        self.btn_plate.setAutoDefault(True)
        self.btn_plate.setObjectName("btn_plate")
        self.btn_gantry = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gantry.setGeometry(QtCore.QRect(60, 480, 200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_gantry.setFont(font)
        self.btn_gantry.setStyleSheet("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}")
        self.btn_gantry.setAutoDefault(True)
        self.btn_gantry.setObjectName("btn_gantry")
        self.myListWidget.raise_()
        self.myStackedWidget.raise_()
        self.btn_connection.raise_()
        self.btn_tension.raise_()
        self.btn_compression.raise_()
        self.btn_flexural.raise_()
        self.btn_beamCol.raise_()
        self.btn_plate.raise_()
        self.btn_gantry.raise_()
        self.comboBox_help.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1410, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.myStackedWidget.setCurrentIndex(1)
        self.mytabWidget.setCurrentIndex(0)
        self.comboBox_help.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.btn_connection, self.btn_tension)
        MainWindow.setTabOrder(self.btn_tension, self.btn_compression)
        MainWindow.setTabOrder(self.btn_compression, self.btn_flexural)
        MainWindow.setTabOrder(self.btn_flexural, self.btn_beamCol)
        MainWindow.setTabOrder(self.btn_beamCol, self.btn_plate)
        MainWindow.setTabOrder(self.btn_plate, self.btn_gantry)
        MainWindow.setTabOrder(self.btn_gantry, self.rdbtn_seat)
        MainWindow.setTabOrder(self.rdbtn_seat, self.rdbtn_finplate)
        MainWindow.setTabOrder(self.rdbtn_finplate, self.rdbtn_cleat)
        MainWindow.setTabOrder(self.rdbtn_cleat, self.rdbtn_endplate)
        MainWindow.setTabOrder(self.rdbtn_endplate, self.btn_start)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Osdag"))
        __sortingEnabled = self.myListWidget.isSortingEnabled()
        self.myListWidget.setSortingEnabled(False)
        item = self.myListWidget.item(0)
        item.setText(_translate("MainWindow", " Design :"))
        self.myListWidget.setSortingEnabled(__sortingEnabled)
        self.label_2.setToolTip(_translate("MainWindow", "Shift+F"))
        self.label_2.setText(_translate("MainWindow", "Finplate"))
        self.rdbtn_finplate.setShortcut(_translate("MainWindow", "Shift+F"))
        self.label_3.setToolTip(_translate("MainWindow", "Shift+C"))
        self.label_3.setText(_translate("MainWindow", "Cleat Angle"))
        self.rdbtn_cleat.setShortcut(_translate("MainWindow", "Shift+C"))
        self.label_4.setToolTip(_translate("MainWindow", "Shift+E"))
        self.label_4.setText(_translate("MainWindow", "Endplate"))
        self.rdbtn_endplate.setShortcut(_translate("MainWindow", "Shift+E"))
        self.label_5.setToolTip(_translate("MainWindow", "Shift+S"))
        self.label_5.setText(_translate("MainWindow", "Seated Angle"))
        self.rdbtn_seat.setShortcut(_translate("MainWindow", "Shift+S"))
        self.btn_start.setToolTip(_translate("MainWindow", "Ctrl+S"))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.btn_start.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab1_shearconnection), _translate("MainWindow", "Shear Connection"))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab2_momentconnection), _translate("MainWindow", "Moment Connection"))
        self.label.setText(_translate("MainWindow", "Coming Soon ..."))
        self.comboBox_help.setItemText(0, _translate("MainWindow", "Help"))
        self.comboBox_help.setItemText(1, _translate("MainWindow", "Video Tutorials"))
        self.comboBox_help.setItemText(2, _translate("MainWindow", "Sample Design Report"))
        self.comboBox_help.setItemText(3, _translate("MainWindow", "Sample Problems"))
        self.comboBox_help.setItemText(4, _translate("MainWindow", "Ask Us a Question"))
        self.comboBox_help.setItemText(5, _translate("MainWindow", "About Osdag"))
        self.btn_connection.setToolTip(_translate("MainWindow", "Ctrl+Shift+C"))
        self.btn_connection.setText(_translate("MainWindow", "Connection"))
        self.btn_connection.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.btn_tension.setToolTip(_translate("MainWindow", "Ctrl+Shift+T"))
        self.btn_tension.setText(_translate("MainWindow", "Tension Member"))
        self.btn_tension.setShortcut(_translate("MainWindow", "Ctrl+Shift+T"))
        self.btn_compression.setToolTip(_translate("MainWindow", "Ctrl+Shift+M"))
        self.btn_compression.setText(_translate("MainWindow", "Compression Member"))
        self.btn_compression.setShortcut(_translate("MainWindow", "Ctrl+Shift+M"))
        self.btn_flexural.setToolTip(_translate("MainWindow", "Ctrl+Shift+F"))
        self.btn_flexural.setText(_translate("MainWindow", "Flexural Member"))
        self.btn_flexural.setShortcut(_translate("MainWindow", "Ctrl+Shift+F"))
        self.btn_beamCol.setToolTip(_translate("MainWindow", "Ctrl+Shift+B"))
        self.btn_beamCol.setText(_translate("MainWindow", "Beam-Column"))
        self.btn_beamCol.setShortcut(_translate("MainWindow", "Ctrl+Shift+B"))
        self.btn_plate.setToolTip(_translate("MainWindow", "Ctrl+Shift+P"))
        self.btn_plate.setText(_translate("MainWindow", "Plate Girder"))
        self.btn_plate.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
        self.btn_gantry.setToolTip(_translate("MainWindow", "Ctrl+Shift+G"))
        self.btn_gantry.setText(_translate("MainWindow", "Gantry Girder"))
        self.btn_gantry.setShortcut(_translate("MainWindow", "Ctrl+Shift+G"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

import osdagMainPageIcons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

