'''
    INSTRUCTIONS TO USE OSDAG MAIN PAGE TEMPLATE(OsdagMainWindow):
----------------------------------------------------------------------------------------------------
    Note: This code is designed to handle a 3 level structure, e.g. ,

..................................................................................................................
.                            Modules (Main Dictionary)                                                           .
.        _______________________|______________________________________________________..........                .    ((LEVEL 1))
.        |               |          |            |                    |               |                          .
.    Module_1        Module_2    Module_3     Module_4             Module_5     Module_6         (Keys of Main Dictionary)
........|..............|............|...........|....................|...............|............................
        |              |            |           |                    |               |
        |              |            |           |                    |               |
        |              |            | [List/Tuple of Module Variants]|               |
        |              |            |                                |               |
        |              |    [List/Tuple of Module Variants]          |               |
        |      (UNDER DEVELOPMENT)                             (UNDER DEVELOPMENT)   |
........|............................................................................|............................
.   ____|________________________________.....               ________________________|______......     (Sub Dictionaries)
.   |                   |               |                    |              |              |                     .     ((LEVEL 2))
.   Submodule_1    Submodule_2    Submodule_3           Submodule_1    Submodule_2    Submodule_3     (Keys of Sub Dictionaries)
.       |               |               |                |                  |              |                     .
........|...............|...............|................|..................|..............|......................
        |               |               |                |                  |              |
        |               |               |                |                  |              |
        |               |               |                |                  |              |
        |               |      (UNDER DEVELOPMENT)       |                  |              |
        |               |                  [List/Tuple of Module Variants]  |              |
        |  [List/Tuple of Module Variants]                                  |  [List/Tuple of Module Variants]
        |                                                                   |
........|...................................................................|.....................................
.   ____|________________________________.....               _______________|_______________......     (Sub-Sub Dictionaries)
.   |                   |               |                    |              |              |                     .     ((LEVEL 3))
. Sub-Submodule_1  Sub-Submodule_2  Sub-Submodule_3  Sub-Submodule_1  Sub-Submodule_2  Sub-Submodule_3 (Keys of Sub-Sub Dictionaries)
.       |               |               |                    |                  |              |                 .
........|...............|...............|....................|..................|..............|..................
        |               |               |                    |                  |              |
        |    (UNDER DEVELOPMENT)        |     [List/Tuple of Module Variants]  |    [List/Tuple of Module Variants]
        |                   [List/Tuple of Module Variants]     [List/Tuple of Module Variants]
[List/Tuple of Module Variants]


The Rules/Steps to use the template are(OsdagMainWindow):
-----------------------------------------------------------------------------
1) The data for the template structuring will go into a variable called self.Modules .

2) self.Modules must be a dictionary with keys as the name of modules in string format (LEVEL 1: Left Panel Buttons).

3) The values to these keys can be a dictionary(Modules), a List/Tuple(Module Variants) or self.Under_Development :
        (i) If the value is a dictionary then it should contain keys as modules in string format and for values
            read RULE 4 . (LEVEL 2: Tab for each module)
       (ii) If the value is a List/Tuple then it should contain sub-lists/sub-tuples informing about the module variants :
                    (a) The module variants as sub-list/sub-tuple will have 3 values, Module_Name, Image_Path and Object_Name .
                    (b) The List/Tuple can have several sub-lists/sub-tuples but the last element should be a method,
                        which connects to the start button on the module variants' page and help launch a certain module.
      (iii) If the value is self.Under_Development then that module/module variant is marked as UNDER DEVELOPMENT.

4) In case of RULE 3(i) if value of any sub-module key is a dictionary then that dictionary will follow the RULE 3
   all over again and the values of the keys can be a dictionary(Sub-Modules), a List/Tuple(Sub-Module Variants) or
   self.Under_Development:
        (i) If the value is a dictionary then it should contain keys as sub-modules in string format and for values
            read RULE 5 . (LEVEL 3 Sub Tab for each tab)
       (ii) If the value is a List/Tuple then it should contain sub-lists/sub-tuples informing about the module variants :
                    (a) The module variants as sub-list/sub-tuple will have 3 values, Module_Name, Image_Path and Object_Name .
                    (b) The List/Tuple can have several sub-lists/sub-tuples but the last element should be a method,
                        which connects to the start button on the module variants' page and help launch a certain module.
      (iii) If the value is self.Under_Development then that module/module variant is marked as UNDER DEVELOPMENT.

5) In case of RULE 4(i) if the value of any sub-module key is a dictionary then that dictionary will have keys as sub-sub-module
   and the values can either be a List/Tuple(Sub-Sub-Module Variants) or self.Under_Development but not another dictionary:
        (i) If the value is a List/Tuple then it should contain sub-lists/sub-tuples informing about the module variants :
                    (a) The module variants as sub-list/sub-tuple will have 3 values, Module_Name, Image_Path and Object_Name .
                    (b) The List/Tuple can have several sub-lists/sub-tuples but the last element should be a method,
                        which connects to the start button on the module variants' page and help launch a certain module.
       (ii) If the value is self.Under_Development then that module/module variant is marked as UNDER DEVELOPMENT.

6) Object_Name, the third value in the sub-lists/sub-tuples, is used to tie to the Radiobuttons on each page thus making it easier to locate them. This is further used
   in the methods to search the Radiobutton using it for the respective modules to be launched .

7) Any further Levels will result in an error .
'''







from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject, Qt,QSize
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QTabWidget, QRadioButton, QButtonGroup, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import math
import sys
from gui.ui_tutorial import Ui_Tutorial
from gui.ui_aboutosdag import Ui_AboutOsdag
from gui.ui_ask_question import Ui_AskQuestion
from gui.ui_design_summary import Ui_DesignReport
from gui.LeftPanel_Button import Ui_LPButton
from gui.Submodule_Page import Ui_Submodule_Page
from gui.ui_OsdagMainPage import Ui_MainWindow
# from design_type.connection.fin_plate_connection import design_report_show
# from design_type.connection.fin_plate_connection import DesignReportDialog
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.cleat_angle_connection import CleatAngleConnection
from design_type.connection.seated_angle_connection import SeatedAngleConnection
from design_type.connection.end_plate_connection import EndPlateConnection
from design_type.connection.base_plate_connection import BasePlateConnection

from design_type.connection.beam_cover_plate import BeamCoverPlate
from design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld

from design_type.tension_member.tension_bolted import Tension_bolted
from design_type.tension_member.tension_welded import Tension_welded
from design_type.connection.beam_end_plate import BeamEndPlate
from design_type.connection.column_cover_plate import ColumnCoverPlate
from design_type.connection.column_end_plate import ColumnEndPlate
from design_type.compression_member.compression import Compression
#from design_type.tension_member.tension import Tension
# from cad.cad_common import call_3DBeam

import configparser
import os
import os.path
import subprocess
from gui.ui_template import Ui_ModuleWindow



class MyTutorials(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Tutorial()
        self.ui.setupUi(self)
        self.osdagmainwindow = parent


class MyAboutOsdag(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AboutOsdag()
        self.ui.setupUi(self)
        self.osdagmainwindow = parent

class MyAskQuestion(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_AskQuestion()
        self.ui.setupUi(self)
        self.osdagmainwindow = parent

class New_Tab_Widget(QTabWidget):           # Empty Custom Tab Widget
    def __init__(self):
        super().__init__()
        self.setTabShape(QTabWidget.Triangular)
        self.setStyleSheet(
            '''
            QTabBar::tab {
                margin-right: 10;
                border-top-left-radius: 2px ;
                border-top-right-radius: 2px ;
                border-bottom-left-radius: 0px ;
                border-bottom-right-radius: 0px ;
                height: 40px;
                width: 200px;
                background-color: #925a5b;
                color:#ffffff;
                font-family: "Arial", Helvetica, sans-serif;
                font-size: 18px;
                font-weight: bold;
                        }

            QTabBar::tab::selected{
	            background-color: #d97f7f;
                color:#000000 ;
                        }

            QTabBar::tab::hover{
                background-color: #d97f7f;
                color:#000000 ;
                        }

            '''
                        )

class Submodule_Page(QWidget):             # Module Varaints' page with a GridLayout and a Start Button
    def __init__(self):
        super().__init__()
        self.ui=Ui_Submodule_Page()
        self.ui.setupUi(self)

class Submodule_Widget(QWidget):            # Module Variant widget with a Name, RadioButton and an Image
    def __init__(self,Iterative,parent):
        super().__init__()
        Module_Name,Image_Path,Object_Name=Iterative
        layout=QVBoxLayout()
        self.setLayout(layout)
        label=QLabel(Module_Name)
        layout.addWidget(label)
        self.rdbtn=QRadioButton()
        self.rdbtn.setObjectName(Object_Name)
        self.rdbtn.setIcon(QIcon(Image_Path))
        self.rdbtn.setIconSize(QSize(300,300))
        layout.addWidget(self.rdbtn)
        self.setStyleSheet(
                    '''
                        QLabel{
                            font-family: "Arial", Helvetica, sans-serif;
                            font-size: 20px;
                            font-weight: bold;
                              }
                    '''
                )
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

class ModulePage(QWidget):              # Empty Page with a layout
    def __init__(self):
        super().__init__()
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,5,0,0)

class LeftPanelButton(QWidget):          # Custom Button widget for the Left Panel
    def __init__(self,text):
        super().__init__()
        self.ui=Ui_LPButton()
        self.ui.setupUi(self)
        self.ui.LP_Button.setText(text)  #LP_Button is the QPushButton widget inside the LeftPanelButton Widget
class OsdagMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox_help.currentIndexChanged.connect(self.selection_change)
        self.Under_Development='UNDER DEVELOPMENT'
        self.Modules={
                'Connection' : {
                                'Shear Connection' : [
                                    ('Fin Plate','ResourceFiles/images/finplate.png','Fin_Plate'),
                                    ('Cleat Angle','ResourceFiles/images/cleatAngle.png','Cleat_Angle'),
                                    ('End Plate','ResourceFiles/images/endplate.png','End_Plate'),
                                    ('Seated Angle','ResourceFiles/images/seatedAngle1.png','Seated_Angle'),
                                    self.show_shear_connection,
                                                    ],
                                'Moment Connection' :{
                                                    'Beam to Beam' :[
                                                                ('Cover Plate Bolted','ResourceFiles/images/coverplate.png','B2B_Cover_Plate_Bolted'),
                                                                ('Cover Plate Welded','ResourceFiles/images/coverplate.png','B2B_Cover_Plate_Welded'),
                                                                ('End Plate Connection','ResourceFiles/images/endplate.png','B2B_End_Plate_Connection'),
                                                                self.show_moment_connection,
                                                                    ],
                                                    'Beam to Column': self.Under_Development,
                                                    'Column to Column' :[
                                                                ('Cover Plate Bolted','ResourceFiles/images/coverplate.png','C2C_Cover_Plate_Bolted'),
                                                                ('Cover Plate Welded','ResourceFiles/images/coverplate.png','C2C_Cover_Plate_Welded'),
                                                                ('End Plate Connection','ResourceFiles/images/endplate.png','C2C_End_Plate_Connection'),
                                                                self.show_moment_connection_cc,
                                                                    ],
                                                    'PEB' : self.Under_Development,
                                                    },
                                'Base Plate':[
                                        ('Base Plate', 'ResourceFiles/images/BasePlate.jpeg', 'Base_Plate'),
                                        self.show_base_plate,
                                            ],
                                'Truss Connection' : self.Under_Development,
                                },
                'Tension Member' : [
                            ('Bolted','ResourceFiles/images/beam_column_endplate.png','Tension_Bolted'),
                            ('Welded','ResourceFiles/images/finplate.png','Tension_Welded'),
                            self.show_tension_module,
                                   ],
                'Compression Member' : [
                            ('Bolted','ResourceFiles/images/beam_column_endplate.png','Compression_Bolted'),
                            ('Welded','ResourceFiles/images/finplate.png','Compression_Welded'),
                            self.show_compression_module,
                                       ],
                'Flexural Member' : self.Under_Development,
                'Beam-Column' : self.Under_Development,
                'Plate Girder' : self.Under_Development,
                'Truss' : self.Under_Development,
                '2D Frame' : self.Under_Development,
                '3D Frame' : self.Under_Development,
                'Group Design' : self.Under_Development,
                }

####################################### UI Formation ################################

        for ModuleName in self.Modules:                      #Level 1 dictionary handling
            Button= LeftPanelButton(ModuleName)
            self.ButtonConnection(Button,list(self.Modules.keys()),ModuleName)
            self.ui.verticalLayout.addWidget(Button)
            if(type(self.Modules[ModuleName])==dict):        #level 2 dictionary handling
                Page= ModulePage()
                self.ui.myStackedWidget.addWidget(Page)
                Current_Module=self.Modules[ModuleName]
                Tab_Widget=New_Tab_Widget()
                Page.layout.addWidget(Tab_Widget)
                for Submodule in Current_Module:
                    if(type(Current_Module[Submodule])==dict):          #Level 3 dictionary handling
                        New_Tab=ModulePage()
                        Tab_Widget.addTab(New_Tab,Submodule)
                        Sub_Page= ModulePage()
                        New_Tab.layout.addWidget(Sub_Page)
                        Current_SubModule=Current_Module[Submodule]
                        Sub_Tab_Widget=New_Tab_Widget()
                        Sub_Page.layout.addWidget(Sub_Tab_Widget)

                        for Sub_Sub_Module in Current_SubModule:
                            if(type(Current_SubModule[Sub_Sub_Module]) in [list,tuple]):        # Final List/tuple Handling
                                New_Sub_Tab=Submodule_Page()
                                Sub_Tab_Widget.addTab(New_Sub_Tab,Sub_Sub_Module)
                                group=QButtonGroup(QWidget(Page))
                                row,col=0,0
                                n=math.floor((len(Current_SubModule[Sub_Sub_Module])-2)/2)

                                for Selection in Current_SubModule[Sub_Sub_Module][:-1]:
                                    widget=Submodule_Widget(Selection,New_Sub_Tab)
                                    group.addButton(widget.rdbtn)
                                    New_Sub_Tab.ui.gridLayout.addWidget(widget,row,col)

                                    if(col==n and len(Current_SubModule[Sub_Sub_Module])!=3):
                                        row+=1
                                        col=0

                                    else:
                                        col+=1
                                New_Sub_Tab.ui.StartButton.clicked.connect(Current_SubModule[Sub_Sub_Module][-1])

                            elif(Current_SubModule[Sub_Sub_Module]==self.Under_Development):   # Final Under Development Handling
                                Sub_Tab_Widget.addTab(self.UnderDevelopmentModule(),Sub_Sub_Module)

                            else:
                                raise ValueError

                    elif(type(Current_Module[Submodule]) in [list,tuple]):      #Level 3 list/tuple handling
                        New_Tab=Submodule_Page()
                        Tab_Widget.addTab(New_Tab,Submodule)
                        group=QButtonGroup(QWidget(Page))
                        row,col=0,0
                        n=math.floor((len(Current_Module[Submodule])-2)/2)

                        for Selection in Current_Module[Submodule][:-1]:
                            widget=Submodule_Widget(Selection,New_Tab)
                            group.addButton(widget.rdbtn)
                            New_Tab.ui.gridLayout.addWidget(widget,row,col)

                            if(col==n and len(Current_Module[Submodule])!=3):
                                row+=1
                                col=0

                            else:
                                col+=1
                        New_Tab.ui.StartButton.clicked.connect(Current_Module[Submodule][-1])

                    elif(Current_Module[Submodule]==self.Under_Development):       #Level 3 Under Development handling
                        Tab_Widget.addTab(self.UnderDevelopmentModule(),Submodule)

                    else:
                        raise ValueError

            elif(type(self.Modules[ModuleName]) in [list,tuple]):            # Level 2 list/tuple handling
                Page= Submodule_Page()
                self.ui.myStackedWidget.addWidget(Page)
                group=QButtonGroup(QWidget(Page))
                row,col=0,0
                n=math.floor((len(self.Modules[ModuleName])-2)/2)

                for Selection in self.Modules[ModuleName][:-1]:
                    widget=Submodule_Widget(Selection,Page)
                    group.addButton(widget.rdbtn)
                    Page.ui.gridLayout.addWidget(widget,row,col)

                    if(col==n and len(self.Modules[ModuleName])!=3):
                        row+=1
                        col=0

                    else:
                        col+=1
                Page.ui.StartButton.clicked.connect(self.Modules[ModuleName][-1])

            elif(self.Modules[ModuleName]==self.Under_Development):           #Level 2 Under Development handling
                self.ui.myStackedWidget.addWidget(self.UnderDevelopmentModule())

            else:
                raise ValueError
        self.showMaximized()

################################ UI Methods ###############################################

    def selection_change(self):
        loc = self.ui.comboBox_help.currentText()
        if loc == "Design Examples":
            self.design_examples()
        elif loc == "Video Tutorials":
            self.open_tutorials()
        elif loc == "About Osdag":
            self.about_osdag()
        elif loc == "Ask Us a Question":
            self.ask_question()
        # elif loc == "FAQ":
        #     pass

    def select_workspace_folder(self):
        # This function prompts the user to select the workspace folder and returns the name of the workspace folder
        config = configparser.ConfigParser()
        config.read_file(open(r'Osdag.config'))
        desktop_path = config.get("desktop_path", "path1")
        folder = QFileDialog.getExistingDirectory(self, "Select Workspace Folder (Don't use spaces in the folder name)", desktop_path)
        return folder

    @staticmethod
    def UnderDevelopmentModule():
        Page= ModulePage()
        label=QLabel('This Module is Currently Under Devopment')
        Page.layout.addWidget(label)
        label.setAlignment(Qt.AlignCenter)
        Page.setStyleSheet(
            '''
                QLabel{
                    font-family: "Times New Roman", Times, serif;
                    font-size: 30px;
                }
            '''
        )
        return Page

    def ButtonConnection(self,Button,Modules,ModuleName):
        Button.ui.LP_Button.clicked.connect(lambda : self.ui.myStackedWidget.setCurrentIndex(Modules.index(ModuleName)+1))

#################################### Module Launchers ##########################################

    @pyqtSlot()
    def show_shear_connection(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.findChild(QRadioButton,'Fin_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, FinPlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.findChild(QRadioButton,'Cleat_Angle').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, CleatAngleConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.findChild(QRadioButton,'Seated_Angle').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, SeatedAngleConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.findChild(QRadioButton,'End_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, EndPlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        else:
            QMessageBox.about(self, "INFO", "Please select appropriate connection")
    #
    # def show_compression_module(self):
    #     folder = self.select_workspace_folder()
    #     folder = str(folder)
    #     if not os.path.exists(folder):
    #         if folder == '':
    #             pass
    #         else:
    #             os.mkdir(folder, 0o755)
    #
    #     root_path = folder
    #     images_html_folder = ['images_html']
    #     flag = True
    #     for create_folder in images_html_folder:
    #         if root_path == '':
    #             flag = False
    #             return flag
    #         else:
    #             try:
    #                 os.mkdir(os.path.join(root_path, create_folder))
    #             except OSError:
    #                 shutil.rmtree(os.path.join(folder, create_folder))
    #                 os.mkdir(os.path.join(root_path, create_folder))
    #     self.hide()
    #     self.ui3 = Ui_ModuleWindow()
    #     self.ui3.setupUi(self.ui3, Compression, folder)
    #     self.ui3.show()
    #     self.ui3.closed.connect(self.show)


    def show_moment_connection(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.findChild(QRadioButton,'B2B_Cover_Plate_Bolted').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, BeamCoverPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'B2B_Cover_Plate_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, BeamCoverPlateWeld, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)
        elif self.findChild(QRadioButton,'B2B_End_Plate_Connection').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2,BeamEndPlate,' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
            # self.window = MainController(Ui_ModuleWindow, FinPlateConnection, folder)
            # self.window.show()
            # self.window.closed.connect(self.show)


    def show_base_plate(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))
        if self.findChild(QRadioButton, 'Base_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, BasePlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_moment_connection_cc(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.findChild(QRadioButton,'C2C_Cover_Plate_Bolted').isChecked() :
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, ColumnCoverPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'C2C_Cover_Plate_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, ColumnCoverPlateWeld, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.findChild(QRadioButton,'C2C_End_Plate_Connection').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, ColumnEndPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_compression_module(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))
        if self.findChild(QRadioButton,'Compression_Bolted').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, Compression, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.findChild(QRadioButton,'Compression_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, Compression, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_tension_module(self):
        # folder = self.select_workspace_folder()
        # folder = str(folder)
        # if not os.path.exists(folder):
        #     if folder == '':
        #         pass
        #     else:
        #         os.mkdir(folder, 0o755)
        #
        # root_path = folder
        # images_html_folder = ['images_html']
        # flag = True
        # for create_folder in images_html_folder:
        #     if root_path == '':
        #         flag = False
        #         return flag
        #     else:
        #         try:
        #             os.mkdir(os.path.join(root_path, create_folder))
        #         except OSError:
        #             shutil.rmtree(os.path.join(folder, create_folder))
        #             os.mkdir(os.path.join(root_path, create_folder))

        if self.findChild(QRadioButton,'Tension_Bolted').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2,Tension_bolted, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.findChild(QRadioButton,'Tension_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow()
            self.ui2.setupUi(self.ui2, Tension_welded, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

################################# Help Actions ############################################

    def about_osdag(self):
        dialog = MyAboutOsdag(self)
        dialog.show()

    def open_osdag(self):
         self.about_osdag()

    def tutorials(self):
        dialog = MyTutorials(self)
        dialog.show()

    def open_tutorials(self):
        self.tutorials()

    def ask_question(self):
        dialog = MyAskQuestion(self)
        dialog.show()

    def open_question(self):
        self.ask_question()

    def design_examples(self):
        root_path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'design_example', '_build', 'html')
        for html_file in os.listdir(root_path):
           if html_file.startswith('index'):
               if sys.platform == ("win32" or "win64"):
                   os.startfile("%s/%s" % (root_path, html_file))
               else:
                   opener ="open" if sys.platform == "darwin" else "xdg-open"
                   subprocess.call([opener, "%s/%s" % (root_path, html_file)])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    # app.exec_()
    # sys.exit(app.exec_())
    try:
        sys.exit(app.exec_())
    except BaseException as e:
        print("ERROR", e)
