# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OsdagMainPage.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1410, 1110)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/images/Osdag.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(_fromUtf8("QWidget::showMaximised()"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.myListWidget = QtGui.QListWidget(self.centralwidget)
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
        self.myListWidget.setStyleSheet(_fromUtf8("QListWidget\n"
"{\n"
"background-color: #abc250 ;\n"
"}"))
        self.myListWidget.setFrameShape(QtGui.QFrame.Panel)
        self.myListWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.myListWidget.setLineWidth(4)
        self.myListWidget.setMidLineWidth(2)
        self.myListWidget.setObjectName(_fromUtf8("myListWidget"))
        item = QtGui.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.myListWidget.addItem(item)
        self.gridLayout.addWidget(self.myListWidget, 0, 0, 1, 2)
        self.myStackedWidget = QtGui.QStackedWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setItalic(False)
        self.myStackedWidget.setFont(font)
        self.myStackedWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.myStackedWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.myStackedWidget.setObjectName(_fromUtf8("myStackedWidget"))
        self.Osdagpage = QtGui.QWidget()
        self.Osdagpage.setObjectName(_fromUtf8("Osdagpage"))
        self.gridLayout_2 = QtGui.QGridLayout(self.Osdagpage)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lbl_OsdagHeader = QtGui.QLabel(self.Osdagpage)
        self.lbl_OsdagHeader.setMinimumSize(QtCore.QSize(800, 200))
        self.lbl_OsdagHeader.setMaximumSize(QtCore.QSize(800, 200))
        self.lbl_OsdagHeader.setText(_fromUtf8(""))
        self.lbl_OsdagHeader.setPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/images/Osdag_header.png")))
        self.lbl_OsdagHeader.setScaledContents(True)
        self.lbl_OsdagHeader.setObjectName(_fromUtf8("lbl_OsdagHeader"))
        self.gridLayout_2.addWidget(self.lbl_OsdagHeader, 0, 0, 2, 2)
        spacerItem = QtGui.QSpacerItem(20, 738, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 2, 2, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 646, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.lbl_fosseelogo = QtGui.QLabel(self.Osdagpage)
        self.lbl_fosseelogo.setMinimumSize(QtCore.QSize(250, 92))
        self.lbl_fosseelogo.setMaximumSize(QtCore.QSize(250, 92))
        self.lbl_fosseelogo.setText(_fromUtf8(""))
        self.lbl_fosseelogo.setPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/images/Fossee_logo.png")))
        self.lbl_fosseelogo.setScaledContents(True)
        self.lbl_fosseelogo.setObjectName(_fromUtf8("lbl_fosseelogo"))
        self.gridLayout_2.addWidget(self.lbl_fosseelogo, 3, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(532, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 3, 1, 1, 1)
        self.lbl_iitblogo = QtGui.QLabel(self.Osdagpage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_iitblogo.sizePolicy().hasHeightForWidth())
        self.lbl_iitblogo.setSizePolicy(sizePolicy)
        self.lbl_iitblogo.setMinimumSize(QtCore.QSize(100, 100))
        self.lbl_iitblogo.setText(_fromUtf8(""))
        self.lbl_iitblogo.setPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/images/logoiitb.png")))
        self.lbl_iitblogo.setScaledContents(False)
        self.lbl_iitblogo.setObjectName(_fromUtf8("lbl_iitblogo"))
        self.gridLayout_2.addWidget(self.lbl_iitblogo, 3, 2, 1, 1)
        self.myStackedWidget.addWidget(self.Osdagpage)
        self.Connectionpage = QtGui.QWidget()
        self.Connectionpage.setObjectName(_fromUtf8("Connectionpage"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.Connectionpage)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mytabWidget = QtGui.QTabWidget(self.Connectionpage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mytabWidget.sizePolicy().hasHeightForWidth())
        self.mytabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.mytabWidget.setFont(font)
        self.mytabWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mytabWidget.setStyleSheet(_fromUtf8("QTabBar::tab {\n"
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
" "))
        self.mytabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.mytabWidget.setObjectName(_fromUtf8("mytabWidget"))
        self.tab1_shearconnection = QtGui.QWidget()
        font = QtGui.QFont()
        font.setItalic(True)
        self.tab1_shearconnection.setFont(font)
        self.tab1_shearconnection.setObjectName(_fromUtf8("tab1_shearconnection"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab1_shearconnection)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(20, 102, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 102, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 0, 6, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(87, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 1, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.rdbtn_finplate = QtGui.QRadioButton(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.rdbtn_finplate.setFont(font)
        self.rdbtn_finplate.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_finplate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_finplate.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("ResourceFiles/images/finplate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_finplate.setIcon(icon1)
        self.rdbtn_finplate.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_finplate.setCheckable(True)
        self.rdbtn_finplate.setObjectName(_fromUtf8("rdbtn_finplate"))
        self.verticalLayout.addWidget(self.rdbtn_finplate)
        self.gridLayout_3.addLayout(self.verticalLayout, 1, 1, 1, 3)
        spacerItem6 = QtGui.QSpacerItem(175, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 1, 4, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.rdbtn_cleat = QtGui.QRadioButton(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.rdbtn_cleat.setFont(font)
        self.rdbtn_cleat.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_cleat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_cleat.setStyleSheet(_fromUtf8("QRadioButton {\n"
"text-shadow : black 0.1em 0.1em 0.2em  ;\n"
"}"))
        self.rdbtn_cleat.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("ResourceFiles/images/cleatAngle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_cleat.setIcon(icon2)
        self.rdbtn_cleat.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_cleat.setObjectName(_fromUtf8("rdbtn_cleat"))
        self.verticalLayout_2.addWidget(self.rdbtn_cleat)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 5, 1, 3)
        spacerItem7 = QtGui.QSpacerItem(87, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem7, 1, 8, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(87, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 2, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_4 = QtGui.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.rdbtn_endplate = QtGui.QRadioButton(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.rdbtn_endplate.setFont(font)
        self.rdbtn_endplate.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_endplate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rdbtn_endplate.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("ResourceFiles/images/endplate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_endplate.setIcon(icon3)
        self.rdbtn_endplate.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_endplate.setObjectName(_fromUtf8("rdbtn_endplate"))
        self.verticalLayout_3.addWidget(self.rdbtn_endplate)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 2, 1, 1, 3)
        spacerItem9 = QtGui.QSpacerItem(175, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem9, 2, 4, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_5 = QtGui.QLabel(self.tab1_shearconnection)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_4.addWidget(self.label_5)
        self.rdbtn_seat = QtGui.QRadioButton(self.tab1_shearconnection)
        self.rdbtn_seat.setFocusPolicy(QtCore.Qt.TabFocus)
        self.rdbtn_seat.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/images/seatedAngle1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbtn_seat.setIcon(icon4)
        self.rdbtn_seat.setIconSize(QtCore.QSize(300, 300))
        self.rdbtn_seat.setObjectName(_fromUtf8("rdbtn_seat"))
        self.verticalLayout_4.addWidget(self.rdbtn_seat)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 2, 5, 1, 3)
        spacerItem10 = QtGui.QSpacerItem(87, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem10, 2, 8, 1, 1)
        spacerItem11 = QtGui.QSpacerItem(20, 102, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem11, 3, 1, 1, 1)
        spacerItem12 = QtGui.QSpacerItem(20, 102, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem12, 3, 7, 1, 1)
        spacerItem13 = QtGui.QSpacerItem(262, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 4, 3, 1, 1)
        self.btn_start = QtGui.QPushButton(self.tab1_shearconnection)
        self.btn_start.setMinimumSize(QtCore.QSize(190, 30))
        self.btn_start.setMaximumSize(QtCore.QSize(190, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start.setFont(font)
        self.btn_start.setFocusPolicy(QtCore.Qt.TabFocus)
        self.btn_start.setStyleSheet(_fromUtf8("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}"))
        self.btn_start.setCheckable(False)
        self.btn_start.setAutoExclusive(False)
        self.btn_start.setAutoDefault(True)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        self.gridLayout_3.addWidget(self.btn_start, 4, 4, 1, 1)
        spacerItem14 = QtGui.QSpacerItem(262, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem14, 4, 5, 1, 1)
        self.mytabWidget.addTab(self.tab1_shearconnection, _fromUtf8(""))
        self.tab2_momentconnection = QtGui.QWidget()
        self.tab2_momentconnection.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tab2_momentconnection.setObjectName(_fromUtf8("tab2_momentconnection"))
        self.mytabWidget.addTab(self.tab2_momentconnection, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.mytabWidget)
        self.myStackedWidget.addWidget(self.Connectionpage)
        self.tensionpage = QtGui.QWidget()
        self.tensionpage.setObjectName(_fromUtf8("tensionpage"))
        self.label = QtGui.QLabel(self.tensionpage)
        self.label.setGeometry(QtCore.QRect(350, 260, 271, 111))
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.myStackedWidget.addWidget(self.tensionpage)
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.myStackedWidget.addWidget(self.page)
        self.gridLayout.addWidget(self.myStackedWidget, 0, 2, 1, 1)
        self.comboBox_help = QtGui.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.comboBox_help.setFont(font)
        self.comboBox_help.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBox_help.setStyleSheet(_fromUtf8("QComboBox::hover\n"
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
""))
        self.comboBox_help.setFrame(True)
        self.comboBox_help.setObjectName(_fromUtf8("comboBox_help"))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.comboBox_help.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_help, 1, 1, 1, 1)
        self.btn_openfile = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_openfile.setFont(font)
        self.btn_openfile.setStyleSheet(_fromUtf8("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}"))
        self.btn_openfile.setAutoDefault(True)
        self.btn_openfile.setObjectName(_fromUtf8("btn_openfile"))
        self.gridLayout.addWidget(self.btn_openfile, 1, 0, 1, 1)
        self.btn_connection = QtGui.QPushButton(self.centralwidget)
        self.btn_connection.setGeometry(QtCore.QRect(60, 120, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_connection.setFont(font)
        self.btn_connection.setMouseTracking(False)
        self.btn_connection.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_connection.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.btn_connection.setStyleSheet(_fromUtf8("QPushButton::hover\n"
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
""))
        self.btn_connection.setAutoDefault(True)
        self.btn_connection.setDefault(False)
        self.btn_connection.setObjectName(_fromUtf8("btn_connection"))
        self.btn_tension = QtGui.QPushButton(self.centralwidget)
        self.btn_tension.setGeometry(QtCore.QRect(60, 180, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_tension.setFont(font)
        self.btn_tension.setStyleSheet(_fromUtf8("QPushButton::hover\n"
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
""))
        self.btn_tension.setAutoDefault(True)
        self.btn_tension.setObjectName(_fromUtf8("btn_tension"))
        self.btn_compression = QtGui.QPushButton(self.centralwidget)
        self.btn_compression.setGeometry(QtCore.QRect(60, 240, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_compression.setFont(font)
        self.btn_compression.setStyleSheet(_fromUtf8("QPushButton::hover\n"
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
""))
        self.btn_compression.setAutoDefault(True)
        self.btn_compression.setObjectName(_fromUtf8("btn_compression"))
        self.btn_flexural = QtGui.QPushButton(self.centralwidget)
        self.btn_flexural.setGeometry(QtCore.QRect(60, 300, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_flexural.setFont(font)
        self.btn_flexural.setStyleSheet(_fromUtf8("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}"))
        self.btn_flexural.setAutoDefault(True)
        self.btn_flexural.setObjectName(_fromUtf8("btn_flexural"))
        self.btn_beamCol = QtGui.QPushButton(self.centralwidget)
        self.btn_beamCol.setGeometry(QtCore.QRect(60, 360, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_beamCol.setFont(font)
        self.btn_beamCol.setStyleSheet(_fromUtf8("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}"))
        self.btn_beamCol.setAutoDefault(True)
        self.btn_beamCol.setObjectName(_fromUtf8("btn_beamCol"))
        self.btn_plate = QtGui.QPushButton(self.centralwidget)
        self.btn_plate.setGeometry(QtCore.QRect(60, 420, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_plate.setFont(font)
        self.btn_plate.setStyleSheet(_fromUtf8("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}"))
        self.btn_plate.setAutoDefault(True)
        self.btn_plate.setObjectName(_fromUtf8("btn_plate"))
        self.btn_gantry = QtGui.QPushButton(self.centralwidget)
        self.btn_gantry.setGeometry(QtCore.QRect(60, 480, 200, 35))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_gantry.setFont(font)
        self.btn_gantry.setStyleSheet(_fromUtf8("QPushButton::hover\n"
"{\n"
"   background-color: #d97f7f;\n"
"   color:#000000 ;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color: #925a5b;\n"
"color:#ffffff;\n"
"}"))
        self.btn_gantry.setAutoDefault(True)
        self.btn_gantry.setObjectName(_fromUtf8("btn_gantry"))
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
        self.btn_openfile.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1410, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.myStackedWidget.setCurrentIndex(1)
        self.mytabWidget.setCurrentIndex(0)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Osdag", None))
        __sortingEnabled = self.myListWidget.isSortingEnabled()
        self.myListWidget.setSortingEnabled(False)
        item = self.myListWidget.item(0)
        item.setText(_translate("MainWindow", " Design :", None))
        self.myListWidget.setSortingEnabled(__sortingEnabled)
        self.mytabWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p><a href=\"#\">Shear Connection</a></p></body></html>", None))
        self.label_2.setToolTip(_translate("MainWindow", "Shift+F", None))
        self.label_2.setText(_translate("MainWindow", "Finplate", None))
        self.rdbtn_finplate.setShortcut(_translate("MainWindow", "Shift+F", None))
        self.label_3.setToolTip(_translate("MainWindow", "Shift+C", None))
        self.label_3.setText(_translate("MainWindow", "Cleat Angle", None))
        self.rdbtn_cleat.setShortcut(_translate("MainWindow", "Shift+C", None))
        self.label_4.setToolTip(_translate("MainWindow", "Shift+E", None))
        self.label_4.setText(_translate("MainWindow", "Endplate", None))
        self.rdbtn_endplate.setShortcut(_translate("MainWindow", "Shift+E", None))
        self.label_5.setToolTip(_translate("MainWindow", "Shift+S", None))
        self.label_5.setText(_translate("MainWindow", "Seated Angle", None))
        self.rdbtn_seat.setShortcut(_translate("MainWindow", "Shift+S", None))
        self.btn_start.setToolTip(_translate("MainWindow", "Ctrl+S", None))
        self.btn_start.setText(_translate("MainWindow", "Start", None))
        self.btn_start.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab1_shearconnection), _translate("MainWindow", "Shear Connection", None))
        self.mytabWidget.setTabText(self.mytabWidget.indexOf(self.tab2_momentconnection), _translate("MainWindow", "Moment Connection", None))
        self.label.setText(_translate("MainWindow", "Coming Soon ...", None))
        self.comboBox_help.setItemText(0, _translate("MainWindow", "Help", None))
        self.comboBox_help.setItemText(1, _translate("MainWindow", "Sample Reports", None))
        self.comboBox_help.setItemText(2, _translate("MainWindow", "Sample Problems", None))
        self.comboBox_help.setItemText(3, _translate("MainWindow", "Video Tutorials", None))
        self.comboBox_help.setItemText(4, _translate("MainWindow", "FAQ", None))
        self.comboBox_help.setItemText(5, _translate("MainWindow", "Ask Us a Question", None))
        self.comboBox_help.setItemText(6, _translate("MainWindow", "About Osdag", None))
        self.btn_openfile.setText(_translate("MainWindow", "Open file", None))
        self.btn_connection.setToolTip(_translate("MainWindow", "Ctrl+Shift+C", None))
        self.btn_connection.setText(_translate("MainWindow", "Connection", None))
        self.btn_connection.setShortcut(_translate("MainWindow", "Ctrl+Shift+C", None))
        self.btn_tension.setToolTip(_translate("MainWindow", "Ctrl+Shift+T", None))
        self.btn_tension.setText(_translate("MainWindow", "Tension Member", None))
        self.btn_tension.setShortcut(_translate("MainWindow", "Ctrl+Shift+T", None))
        self.btn_compression.setToolTip(_translate("MainWindow", "Ctrl+Shift+M", None))
        self.btn_compression.setText(_translate("MainWindow", "Compression Member", None))
        self.btn_compression.setShortcut(_translate("MainWindow", "Ctrl+Shift+M", None))
        self.btn_flexural.setToolTip(_translate("MainWindow", "Ctrl+Shift+F", None))
        self.btn_flexural.setText(_translate("MainWindow", "Flexural Member", None))
        self.btn_flexural.setShortcut(_translate("MainWindow", "Ctrl+Shift+F", None))
        self.btn_beamCol.setToolTip(_translate("MainWindow", "Ctrl+Shift+B", None))
        self.btn_beamCol.setText(_translate("MainWindow", "Beam-Column", None))
        self.btn_beamCol.setShortcut(_translate("MainWindow", "Ctrl+Shift+B", None))
        self.btn_plate.setToolTip(_translate("MainWindow", "Ctrl+Shift+P", None))
        self.btn_plate.setText(_translate("MainWindow", "Plate Girder", None))
        self.btn_plate.setShortcut(_translate("MainWindow", "Ctrl+Shift+P", None))
        self.btn_gantry.setToolTip(_translate("MainWindow", "Ctrl+Shift+G", None))
        self.btn_gantry.setText(_translate("MainWindow", "Gantry Girder", None))
        self.btn_gantry.setShortcut(_translate("MainWindow", "Ctrl+Shift+G", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

import osdagMainPageIcons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

