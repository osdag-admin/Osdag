# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OsdagMainPage.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1472, 909)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/images/Osdag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QWidget::showMaximised()")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_help = QtWidgets.QComboBox(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(146, 90, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.comboBox_help.setPalette(palette)
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
        self.gridLayout.addWidget(self.comboBox_help, 1, 0, 1, 1)
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
        self.gridLayout.addWidget(self.myListWidget, 0, 0, 1, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.gridLayout)
        self.myStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.myStackedWidget.setFont(font)
        self.myStackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.myStackedWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.myStackedWidget.setObjectName("myStackedWidget")
        self.Osdagpage = QtWidgets.QWidget()
        self.Osdagpage.setObjectName("Osdagpage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Osdagpage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 646, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.lbl_OsdagHeader = QtWidgets.QLabel(self.Osdagpage)
        self.lbl_OsdagHeader.setMinimumSize(QtCore.QSize(800, 200))
        self.lbl_OsdagHeader.setMaximumSize(QtCore.QSize(800, 200))
        self.lbl_OsdagHeader.setText("")
        self.lbl_OsdagHeader.setPixmap(QtGui.QPixmap(":/newPrefix/images/Osdag_header.png"))
        self.lbl_OsdagHeader.setScaledContents(True)
        self.lbl_OsdagHeader.setObjectName("lbl_OsdagHeader")
        self.gridLayout_2.addWidget(self.lbl_OsdagHeader, 0, 0, 2, 2)
        spacerItem1 = QtWidgets.QSpacerItem(532, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 3, 1, 1, 1)
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
        spacerItem2 = QtWidgets.QSpacerItem(20, 738, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 1, 2, 2, 1)
        self.lbl_fosseelogo = QtWidgets.QLabel(self.Osdagpage)
        self.lbl_fosseelogo.setMinimumSize(QtCore.QSize(250, 92))
        self.lbl_fosseelogo.setMaximumSize(QtCore.QSize(250, 92))
        self.lbl_fosseelogo.setText("")
        self.lbl_fosseelogo.setPixmap(QtGui.QPixmap(":/newPrefix/images/Fossee_logo.png"))
        self.lbl_fosseelogo.setScaledContents(True)
        self.lbl_fosseelogo.setObjectName("lbl_fosseelogo")
        self.gridLayout_2.addWidget(self.lbl_fosseelogo, 3, 0, 1, 1)
        self.myStackedWidget.addWidget(self.Osdagpage)
        self.Connectionpage = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Connectionpage.sizePolicy().hasHeightForWidth())
        self.Connectionpage.setSizePolicy(sizePolicy)
        self.Connectionpage.setObjectName("Connectionpage")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Connectionpage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mytabWidget = QtWidgets.QTabWidget(self.Connectionpage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
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
"\n"
"QTabBar::tab::selected{\n"
"    background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QTabBar::tab::hover{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QTabBar::tab{\n"
"height: 40px;\n"
"width: 200px;\n"
"background-color: #5b1c1d;\n"
"color:#ffffff;\n"
"}\n"
"\n"
"QTabBar::tab{\n"
"border-top-left-radius: 2px ;\n"
"border-top-right-radius: 2px ;\n"
"border-bottom-left-radius: 0px ;\n"
"border-bottom-right-radius: 0px ;\n"
"}\n"
" ")
        self.mytabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.mytabWidget.setDocumentMode(True)
        self.mytabWidget.setTabsClosable(False)
        self.mytabWidget.setMovable(False)
        self.mytabWidget.setObjectName("mytabWidget")
        self.tab1_shearconnection = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setItalic(True)
        self.tab1_shearconnection.setFont(font)
        self.tab1_shearconnection.setObjectName("tab1_shearconnection")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab1_shearconnection)
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
        self.rdbtn_cleat.setStyleSheet("QRadioButton ")
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
        self.mytabWidget_2 = QtWidgets.QTabWidget(self.tab2_momentconnection)
        self.mytabWidget_2.setGeometry(QtCore.QRect(0, 10, 1131, 781))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mytabWidget_2.sizePolicy().hasHeightForWidth())
        self.mytabWidget_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Liberation Sans")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.mytabWidget_2.setFont(font)
        self.mytabWidget_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mytabWidget_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mytabWidget_2.setStyleSheet("QTabBar::tab {\n"
"    margin-right: 10;\n"
" }\n"
"\n"
"QTabBar::tab::selected{\n"
"    background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QTabBar::tab::hover{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QTabBar::tab{\n"
"height: 35px;\n"
"width: 150px;\n"
"background-color: #9e6869;\n"
"color:#ffffff;\n"
"}\n"
"\n"
"QTabBar::tab{\n"
"border-top-left-radius: 2px ;\n"
"border-top-right-radius: 2px ;\n"
"border-bottom-left-radius: 0px ;\n"
"border-bottom-right-radius: 0px ;\n"
"}\n"
" ")
        self.mytabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.mytabWidget_2.setDocumentMode(True)
        self.mytabWidget_2.setTabsClosable(False)
        self.mytabWidget_2.setMovable(False)
        self.mytabWidget_2.setObjectName("mytabWidget_2")
        self.tab_beamtobeam = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setItalic(True)
        self.tab_beamtobeam.setFont(font)
        self.tab_beamtobeam.setObjectName("tab_beamtobeam")
        self.btn_start_2 = QtWidgets.QPushButton(self.tab_beamtobeam)
        self.btn_start_2.setGeometry(QtCore.QRect(460, 670, 190, 30))
        self.btn_start_2.setMinimumSize(QtCore.QSize(190, 30))
        self.btn_start_2.setMaximumSize(QtCore.QSize(190, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start_2.setFont(font)
        self.btn_start_2.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_start_2.setStyleSheet("QPushButton::hover\n"
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
        self.btn_start_2.setCheckable(False)
        self.btn_start_2.setAutoExclusive(False)
        self.btn_start_2.setAutoDefault(True)
        self.btn_start_2.setObjectName("btn_start_2")
        self.rdbtn_endplate_ext = QtWidgets.QRadioButton(self.tab_beamtobeam)
        self.rdbtn_endplate_ext.setGeometry(QtCore.QRect(617, 84, 321, 311))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.rdbtn_endplate_ext.setFont(font)
        self.rdbtn_endplate_ext.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_endplate_ext.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/images/extended.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_endplate_ext.setIcon(icon5)
        self.rdbtn_endplate_ext.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_endplate_ext.setObjectName("rdbtn_endplate_ext")
        self.label_7 = QtWidgets.QLabel(self.tab_beamtobeam)
        self.label_7.setGeometry(QtCore.QRect(625, 40, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label = QtWidgets.QLabel(self.tab_beamtobeam)
        self.label.setGeometry(QtCore.QRect(10, 30, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.rdbtn_coverplate = QtWidgets.QRadioButton(self.tab_beamtobeam)
        self.rdbtn_coverplate.setGeometry(QtCore.QRect(0, 104, 328, 271))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.rdbtn_coverplate.setFont(font)
        self.rdbtn_coverplate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_coverplate.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/newPrefix/images/coverplate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_coverplate.setIcon(icon6)
        self.rdbtn_coverplate.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_coverplate.setObjectName("rdbtn_coverplate")
        self.mytabWidget_2.addTab(self.tab_beamtobeam, "")
        self.tab_beamtocolumn = QtWidgets.QWidget()
        self.tab_beamtocolumn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tab_beamtocolumn.setObjectName("tab_beamtocolumn")
        self.btn_start_3 = QtWidgets.QPushButton(self.tab_beamtocolumn)
        self.btn_start_3.setGeometry(QtCore.QRect(460, 670, 190, 30))
        self.btn_start_3.setMinimumSize(QtCore.QSize(190, 30))
        self.btn_start_3.setMaximumSize(QtCore.QSize(190, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start_3.setFont(font)
        self.btn_start_3.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_start_3.setStyleSheet("QPushButton::hover\n"
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
        self.btn_start_3.setCheckable(False)
        self.btn_start_3.setAutoExclusive(False)
        self.btn_start_3.setAutoDefault(True)
        self.btn_start_3.setObjectName("btn_start_3")
        self.label_8 = QtWidgets.QLabel(self.tab_beamtocolumn)
        self.label_8.setGeometry(QtCore.QRect(10, 20, 181, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.rdbtn_endplate_bc = QtWidgets.QRadioButton(self.tab_beamtocolumn)
        self.rdbtn_endplate_bc.setGeometry(QtCore.QRect(0, 94, 328, 281))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.rdbtn_endplate_bc.setFont(font)
        self.rdbtn_endplate_bc.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_endplate_bc.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("ResourceFiles/images/beam_column_endplate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_endplate_bc.setIcon(icon7)
        self.rdbtn_endplate_bc.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_endplate_bc.setObjectName("rdbtn_endplate_bc")
        self.mytabWidget_2.addTab(self.tab_beamtocolumn, "")
        self.tab_columntocolumn = QtWidgets.QWidget()
        self.tab_columntocolumn.setObjectName("tab_columntocolumn")
        self.label_13 = QtWidgets.QLabel(self.tab_columntocolumn)
        self.label_13.setGeometry(QtCore.QRect(388, 9, 356, 723))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.mytabWidget_2.addTab(self.tab_columntocolumn, "")
        self.tab_PEB = QtWidgets.QWidget()
        self.tab_PEB.setObjectName("tab_PEB")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_PEB)
        self.gridLayout_7.setObjectName("gridLayout_7")
        spacerItem15 = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem15, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tab_PEB)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 0, 1, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem16, 0, 2, 1, 1)
        self.mytabWidget_2.addTab(self.tab_PEB, "")
        self.mytabWidget.addTab(self.tab2_momentconnection, "")
        self.tab3_trussconnection = QtWidgets.QWidget()
        self.tab3_trussconnection.setObjectName("tab3_trussconnection")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab3_trussconnection)
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem17 = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem17, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab3_trussconnection)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 0, 1, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(218, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem18, 0, 2, 1, 1)
        self.mytabWidget.addTab(self.tab3_trussconnection, "")
        self.horizontalLayout.addWidget(self.mytabWidget)
        self.myStackedWidget.addWidget(self.Connectionpage)
        self.beamtobeampage = QtWidgets.QWidget()
        self.beamtobeampage.setObjectName("beamtobeampage")
        self.myStackedWidget.addWidget(self.beamtobeampage)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.myStackedWidget.addWidget(self.page)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.myStackedWidget)
        self.btn_connection = QtWidgets.QPushButton(self.centralwidget)
        self.btn_connection.setGeometry(QtCore.QRect(60, 97, 200, 32))
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
        self.btn_tension.setGeometry(QtCore.QRect(60, 144, 200, 32))
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
        self.btn_compression.setGeometry(QtCore.QRect(60, 191, 200, 32))
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
        self.btn_flexural.setGeometry(QtCore.QRect(60, 238, 200, 32))
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
        self.btn_beamCol.setGeometry(QtCore.QRect(60, 285, 200, 32))
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
        self.btn_plate.setGeometry(QtCore.QRect(60, 332, 200, 32))
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
        self.btn_truss = QtWidgets.QPushButton(self.centralwidget)
        self.btn_truss.setGeometry(QtCore.QRect(60, 379, 200, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_truss.setFont(font)
        self.btn_truss.setStyleSheet("QPushButton::hover\n"
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
        self.btn_truss.setAutoDefault(True)
        self.btn_truss.setObjectName("btn_truss")
        self.btn_2dframe = QtWidgets.QPushButton(self.centralwidget)
        self.btn_2dframe.setGeometry(QtCore.QRect(60, 426, 200, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_2dframe.setFont(font)
        self.btn_2dframe.setStyleSheet("QPushButton::hover\n"
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
        self.btn_2dframe.setAutoDefault(True)
        self.btn_2dframe.setObjectName("btn_2dframe")
        self.btn_3dframe = QtWidgets.QPushButton(self.centralwidget)
        self.btn_3dframe.setGeometry(QtCore.QRect(60, 473, 200, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_3dframe.setFont(font)
        self.btn_3dframe.setStyleSheet("QPushButton::hover\n"
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
        self.btn_3dframe.setAutoDefault(True)
        self.btn_3dframe.setObjectName("btn_3dframe")
        self.btn_groupdesign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_groupdesign.setGeometry(QtCore.QRect(60, 520, 200, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_groupdesign.setFont(font)
        self.btn_groupdesign.setStyleSheet("QPushButton::hover\n"
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
        self.btn_groupdesign.setAutoDefault(True)
        self.btn_groupdesign.setObjectName("btn_groupdesign")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 2, 2))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.layoutWidget.raise_()
        self.btn_beamCol.raise_()
        self.btn_compression.raise_()
        self.btn_truss.raise_()
        self.btn_2dframe.raise_()
        self.btn_3dframe.raise_()
        self.btn_groupdesign.raise_()
        self.btn_plate.raise_()
        self.btn_tension.raise_()
        self.btn_connection.raise_()
        self.btn_flexural.raise_()
        self.myStackedWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1472, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.comboBox_help.setCurrentIndex(0)
        self.myStackedWidget.setCurrentIndex(1)
        self.mytabWidget.setCurrentIndex(0)
        self.mytabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.btn_connection, self.btn_tension)
        MainWindow.setTabOrder(self.btn_tension, self.btn_compression)
        MainWindow.setTabOrder(self.btn_compression, self.btn_flexural)
        MainWindow.setTabOrder(self.btn_flexural, self.btn_beamCol)
        MainWindow.setTabOrder(self.btn_beamCol, self.btn_plate)
        MainWindow.setTabOrder(self.btn_plate, self.btn_truss)
        MainWindow.setTabOrder(self.btn_truss, self.btn_2dframe)
        MainWindow.setTabOrder(self.btn_2dframe, self.btn_3dframe)
        MainWindow.setTabOrder(self.btn_3dframe, self.btn_groupdesign)
        MainWindow.setTabOrder(self.btn_groupdesign, self.comboBox_help)
        MainWindow.setTabOrder(self.comboBox_help, self.rdbtn_finplate)
        MainWindow.setTabOrder(self.rdbtn_finplate, self.rdbtn_cleat)
        MainWindow.setTabOrder(self.rdbtn_cleat, self.rdbtn_endplate)
        MainWindow.setTabOrder(self.rdbtn_endplate, self.rdbtn_seat)
        MainWindow.setTabOrder(self.rdbtn_seat, self.btn_start)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Osdag"))
        self.comboBox_help.setItemText(0, _translate("MainWindow", "Help"))
        self.comboBox_help.setItemText(1, _translate("MainWindow", "Video Tutorials"))
        self.comboBox_help.setItemText(2, _translate("MainWindow", "Design Examples"))
        self.comboBox_help.setItemText(3, _translate("MainWindow", "Ask Us a Question"))
        self.comboBox_help.setItemText(4, _translate("MainWindow", "About Osdag"))
        self.label_2.setToolTip(_translate("MainWindow", "Shift+F"))
        self.label_2.setText(_translate("MainWindow", "Fin Plate"))
        self.rdbtn_finplate.setShortcut(_translate("MainWindow", "Shift+F"))
        self.label_3.setToolTip(_translate("MainWindow", "Shift+C"))
        self.label_3.setText(_translate("MainWindow", "Cleat Angle"))
        self.rdbtn_cleat.setShortcut(_translate("MainWindow", "Shift+C"))
        self.label_4.setToolTip(_translate("MainWindow", "Shift+E"))
        self.label_4.setText(_translate("MainWindow", "End Plate"))
        self.rdbtn_endplate.setShortcut(_translate("MainWindow", "Shift+E"))
        self.label_5.setToolTip(_translate("MainWindow", "Shift+S"))
        self.label_5.setText(_translate("MainWindow", "Seated Angle"))
        self.rdbtn_seat.setShortcut(_translate("MainWindow", "Shift+S"))
        self.btn_start.setToolTip(_translate("MainWindow", "Enter"))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.btn_start.setShortcut(_translate("MainWindow", "Return"))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab1_shearconnection), _translate("MainWindow", "Shear Connection"))
        self.btn_start_2.setToolTip(_translate("MainWindow", "Enter"))
        self.btn_start_2.setText(_translate("MainWindow", "Start"))
        self.btn_start_2.setShortcut(_translate("MainWindow", "Return"))
        self.label_7.setText(_translate("MainWindow", "End Plate Connection"))
        self.label.setText(_translate("MainWindow", "Cover Plate Connection"))
        self.mytabWidget_2.setTabText(self.mytabWidget_2.indexOf(self.tab_beamtobeam), _translate("MainWindow", "Beam To Beam"))
        self.btn_start_3.setToolTip(_translate("MainWindow", "Enter"))
        self.btn_start_3.setText(_translate("MainWindow", "Start"))
        self.btn_start_3.setShortcut(_translate("MainWindow", "Return"))
        self.label_8.setText(_translate("MainWindow", "End Plate Connection"))
        self.mytabWidget_2.setTabText(self.mytabWidget_2.indexOf(self.tab_beamtocolumn), _translate("MainWindow", "Beam To Column"))
        self.label_13.setText(_translate("MainWindow", "This module is not available in the current version."))
        self.mytabWidget_2.setTabText(self.mytabWidget_2.indexOf(self.tab_columntocolumn), _translate("MainWindow", "Column To Column"))
        self.label_12.setText(_translate("MainWindow", "This module is not available in the current version."))
        self.mytabWidget_2.setTabText(self.mytabWidget_2.indexOf(self.tab_PEB), _translate("MainWindow", "PEB"))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab2_momentconnection), _translate("MainWindow", "Moment Connection"))
        self.label_6.setText(_translate("MainWindow", "This module is not available in the current version."))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab3_trussconnection), _translate("MainWindow", "Truss Connection"))
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
        self.btn_truss.setToolTip(_translate("MainWindow", "Ctrl+Shift+R"))
        self.btn_truss.setText(_translate("MainWindow", "Truss"))
        self.btn_truss.setShortcut(_translate("MainWindow", "Ctrl+Shift+R"))
        self.btn_2dframe.setToolTip(_translate("MainWindow", "Ctrl+2"))
        self.btn_2dframe.setText(_translate("MainWindow", "2D Frame"))
        self.btn_2dframe.setShortcut(_translate("MainWindow", "Ctrl+2"))
        self.btn_3dframe.setToolTip(_translate("MainWindow", "Ctrl+3"))
        self.btn_3dframe.setText(_translate("MainWindow", "3D Frame"))
        self.btn_3dframe.setShortcut(_translate("MainWindow", "Ctrl+3"))
        self.btn_groupdesign.setToolTip(_translate("MainWindow", "Ctrl+Shift+D"))
        self.btn_groupdesign.setText(_translate("MainWindow", "Group Design"))
        self.btn_groupdesign.setShortcut(_translate("MainWindow", "Ctrl+Shift+D"))
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

