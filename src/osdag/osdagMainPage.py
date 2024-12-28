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

import os
from pathlib import Path
import re
import io
import traceback
import time
from importlib.resources import files
import urllib.request
from PyQt5.QtWidgets import QMessageBox,QApplication, QDialog, QMainWindow
from .update_version_check import Update
#from Thread import timer
from .get_DPI_scale import scale

############################ Pre-Build Database Updation/Creation #################
# TODO: Is there a better way to create and use the sqlite file rather than directly in the installation?
sqlpath = files('osdag.data.ResourceFiles.Database').joinpath('Intg_osdag.sql')
sqlitepath = files('osdag.data.ResourceFiles.Database').joinpath('Intg_osdag.sqlite')

if sqlpath.exists():
    if not sqlitepath.exists():
        cmd = 'sqlite3 ' + str(sqlitepath) + ' < ' + str(sqlpath)
        os.system(cmd)
        sqlpath.touch()
        print('Database Created')

    elif sqlitepath.stat().st_size == 0 or sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1:
        try:
            sqlitenewpath = files('osdag.data.ResourceFiles.Database').joinpath('Intg_osdag_new.sqlite')
            cmd = 'sqlite3 ' + str(sqlitenewpath) + ' < ' + str(sqlpath)
            error = os.system(cmd)
            print(error)
            # if error != 0:
            #      raise Exception('SQL to SQLite conversion error 1')
            # if sqlitenewpath.stat().st_size == 0:
            #      raise Exception('SQL to SQLite conversion error 2')
            os.remove(sqlitepath)
            sqlitenewpath.rename(sqlitepath)
            sqlpath.touch()
            print('Database Updated', sqlpath.stat().st_mtime, sqlitepath.stat().st_mtime)
        except Exception as e:
            sqlitenewpath.unlink()
            print('Error: ', e)
#########################################################################################

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject, Qt,QSize, QFile, QTextStream, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QTabWidget, QRadioButton, QButtonGroup, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore, QtGui
import math
import sys
from .gui.ui_tutorial import Ui_Tutorial
from .gui.ui_aboutosdag import Ui_AboutOsdag
from .gui.ui_ask_question import Ui_AskQuestion
from .gui.ui_design_summary import Ui_DesignReport
from .gui.LeftPanel_Button import Ui_LPButton
from .gui.Submodule_Page import Ui_Submodule_Page
from .gui.ui_OsdagMainPage import Ui_MainWindow
from .gui.ExceptionDialog import CriticalExceptionDialog
# from .design_type.connection.fin_plate_connection import design_report_show
# from .design_type.connection.fin_plate_connection import DesignReportDialog
from .design_type.connection.fin_plate_connection import FinPlateConnection
from .design_type.connection.cleat_angle_connection import CleatAngleConnection
from .design_type.connection.seated_angle_connection import SeatedAngleConnection
from .design_type.connection.end_plate_connection import EndPlateConnection
from .design_type.connection.base_plate_connection import BasePlateConnection
from .design_type.connection.truss_connection_bolted import TrussConnectionBolted

from .design_type.connection.beam_cover_plate import BeamCoverPlate
from .design_type.connection.beam_cover_plate_weld import BeamCoverPlateWeld
from .design_type.connection.column_cover_plate_weld import ColumnCoverPlateWeld
from .design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from .design_type.tension_member.tension_bolted import Tension_bolted
from .design_type.tension_member.tension_welded import Tension_welded

from .design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice

from .design_type.connection.column_cover_plate import ColumnCoverPlate
from .design_type.connection.column_end_plate import ColumnEndPlate
from .design_type.compression_member import Column
from .design_type.compression_member.compression import Compression
from .design_type.compression_member.Column import ColumnDesign
#from .design_type.beam_column.Beam_Colum_Compression import ColumnDesign

from .design_type.flexural_member.flexure import Flexure
from .design_type.flexural_member.flexure_cantilever import Flexure_Cantilever
from design_type.flexural_member.flexure_purlin import Flexure_Purlin
from .design_type.flexural_member.flexure_othersupp import Flexure_Misc
# from .design_type.plate_girder.weldedPlateGirder import PlateGirderWelded
# from .cad.cad_common import call_3DBeam
from .APP_CRASH.Appcrash import api as appcrash
import configparser
import os.path
import subprocess
if sys.platform == 'darwin':
    print('its mac')
    from .gui.ui_template_for_mac import Ui_ModuleWindow
else:
    from .gui.ui_template import Ui_ModuleWindow
# from .gui.ui_template import Ui_ModuleWindow

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
        #self.setTabShape(QTabWidget.Triangular)


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
        label.setObjectName('module_name_label')
        self.rdbtn=QRadioButton()
        self.rdbtn.setObjectName(Object_Name)
        self.rdbtn.setIcon(QIcon(Image_Path))

        self.rdbtn.setIconSize(QSize(int(scale*300), int(scale*300)))

        layout.addWidget(self.rdbtn)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

class ModulePage(QWidget):              # Empty Page with a layout
    def __init__(self,margin=0):
        super().__init__()
        self.layout=QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

class LeftPanelButton(QWidget):          # Custom Button widget for the Left Panel
    def __init__(self,text):
        super().__init__()
        self.ui=Ui_LPButton()
        self.ui.setupUi(self,scale)
        self.ui.LP_Button.setText(text)  #LP_Button is the QPushButton widget inside the LeftPanelButton Widget


class OsdagMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        width = resolution.width()
        height = resolution.height()

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.switch.toggled.connect(self.change_theme)
        self.ui.comboBox_help.currentIndexChanged.connect(self.selection_change)
        self.ui.myStackedWidget.currentChanged.connect(self.current_changed)
        self.Under_Development='UNDER DEVELOPMENT'
        self.Modules={
                'Connection' : {
                                'Shear Connection' : [
                                    ('Fin Plate',str(files("osdag.data.ResourceFiles.images").joinpath("finplate.png")),'Fin_Plate'),
                                    ('Cleat Angle',str(files("osdag.data.ResourceFiles.images").joinpath("cleatAngle.png")),'Cleat_Angle'),
                                    ('End Plate',str(files("osdag.data.ResourceFiles.images").joinpath("endplate.png")),'End_Plate'),
                                    ('Seated Angle',str(files("osdag.data.ResourceFiles.images").joinpath("seatedAngle1.png")),'Seated_Angle'),
                                    self.show_shear_connection,
                                                    ],
                                'Moment Connection' :{
                                                    'Beam-to-Beam Splice' :[
                                                                ('Cover Plate Bolted',str(files("osdag.data.ResourceFiles.images").joinpath("bbcoverplatebolted.png")),'B2B_Cover_Plate_Bolted'),
                                                                ('Cover Plate Welded',str(files("osdag.data.ResourceFiles.images").joinpath("bbcoverplatewelded.png")),'B2B_Cover_Plate_Welded'),
                                                                ('End Plate', str(files("osdag.data.ResourceFiles.images").joinpath("bb_splice.png")), 'B2B_End_Plate_Splice'),
                                                                self.show_moment_connection,
                                                                    ],
                                                    'Beam-to-Column': [
                                                                ('End Plate', str(files("osdag.data.ResourceFiles.images").joinpath("BC-EBW_GUI.png")),'BC_End_Plate'),
                                                                self.show_moment_connection_bc
                                                                    ],
                                                    'Column-to-Column Splice' :[
                                                                ('Cover Plate Bolted',str(files("osdag.data.ResourceFiles.images").joinpath("cccoverplatebolted.png")),'C2C_Cover_Plate_Bolted'),
                                                                ('Cover Plate Welded',str(files("osdag.data.ResourceFiles.images").joinpath("cccoverplatewelded.png")),'C2C_Cover_Plate_Welded'),
                                                                ('End Plate',str(files("osdag.data.ResourceFiles.images").joinpath("ccep_flush.png")),'C2C_End_Plate_Connection'),
                                                                self.show_moment_connection_cc,
                                                                    ],
                                                    'PEB' : self.Under_Development,
                                                    },
                                'Base Plate':[
                                        ('Base Plate Connection', str(files("osdag.data.ResourceFiles.images").joinpath("base_plate.png")), 'Base_Plate'),
                                        self.show_base_plate,
                                            ],
                                'Truss Connection' : self.Under_Development,
                                    # [
                                    # ('Truss Connection Bolted', str(files("osdag.data.ResourceFiles.images").joinpath("broken.png")), 'Truss_Bolted'),
                                    # ('Truss Connection Welded', str(files("osdag.data.ResourceFiles.images").joinpath("broken.png")), 'Truss_Welded'),
                                    # self.show_truss_bolted,
                                    #                ],
                                },
                'Tension Member' : [
                            ('Bolted to End Gusset',str(files("osdag.data.ResourceFiles.images").joinpath("bolted_ten.png")),'Tension_Bolted'),
                            ('Welded to End Gusset',str(files("osdag.data.ResourceFiles.images").joinpath("welded_ten.png")),'Tension_Welded'),
                            self.show_tension_module,
                                   ],
                'Compression Member': [('Columns with known support conditions', str(files("osdag.data.ResourceFiles.images").joinpath("CompressionMembers_ColumnsInFrames")), 'Column_Design'),
                                       # ('Beam-Column Design', str(files("osdag.data.ResourceFiles.images").joinpath("BC_CF-BW-Flush.png")), 'Beam_Column_Design'),
                                       ('Struts in Trusses', str(files("osdag.data.ResourceFiles.images").joinpath("strut.jpg")), 'Strut_Design'),
                                       self.show_compression_module,
                                       ],
                'Flexural Member' : [
                    ('Simply Supported Beam', str(files("osdag.data.ResourceFiles.images").joinpath("simply-supported-beam.jpg")), 'Beam_flexure'),
                    ('Cantilever Beam', str(files("osdag.data.ResourceFiles.images").joinpath("cantilever-beam.jpg")), 'Beam_flexure2'),
                    ('Purlin', str(files("osdag.data.ResourceFiles.images").joinpath("purlin.jpg")), 'Beam_flexure4'),
                    # ('Other Beams', str(files("osdag.data.ResourceFiles.images").joinpath("fixed-beam.png")), 'Beam_flexure3'),
                    
                    # ('Laterally Unsupported Beam', str(files("osdag.data.ResourceFiles.images").joinpath("broken.png")), 'Truss_Welded'),
                    self.show_flexure_module,
                ],
                'Beam-Column' : self.Under_Development,
                'Plate Girder' : self.Under_Development,
                # TODO @rutvik
                # 'Beam-Column' :[
                #     ('Beam-Column Design', str(files("osdag.data.ResourceFiles.images").joinpath("broken.png")), 'Beam_Column_Design'),
                #     self.show_beamcolumn_module,
                # ],
                # 'Plate Girder' : [ #TODO: Check number of sub modules required
                #     ('Welded Girder Design', str(files("osdag.data.ResourceFiles.images").joinpath("broken.png")), 'Welded_Girder_Design'),
                #     self.Show_Girder_Design,
                # ],
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
            # print(f"Here1{ModuleName}")
            if(type(self.Modules[ModuleName])==dict):        #level 2 dictionary handling
                Page= ModulePage()
                self.ui.myStackedWidget.addWidget(Page)
                Current_Module=self.Modules[ModuleName]
                Tab_Widget=New_Tab_Widget()
                Page.layout.addWidget(Tab_Widget)
                # print(f"Here2{self.Modules[ModuleName]}")
                for Submodule in Current_Module:
                    # print(f"Here3{Submodule}")
                    if(type(Current_Module[Submodule])==dict):          #Level 3 dictionary handling
                        New_Tab=ModulePage()
                        Tab_Widget.addTab(New_Tab,Submodule)
                        Sub_Page= ModulePage()
                        New_Tab.layout.addWidget(Sub_Page)
                        Current_SubModule=Current_Module[Submodule]
                        Sub_Tab_Widget=New_Tab_Widget()
                        Sub_Page.layout.addWidget(Sub_Tab_Widget)
                        # print(f"Here4{Submodule}")

                        for Sub_Sub_Module in Current_SubModule:
                            # print(f"Here5{Sub_Sub_Module}")
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
                        # print(f"Here6")

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
                # print(f"Here7")

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

        self.resize(int(width*(0.85)), int(height*(0.75)))
        self.center()
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    @pyqtSlot(int)
    def current_changed(self, index):
        l = list(self.Modules.keys())
        items = list(self.ui.verticalLayout.itemAt(i) for i in range(self.ui.verticalLayout.count()))
        # print(items,"hfhh")
        for item in range(len(items)):
            if item == index-1:
                items[item].widget().ui.LP_Button.setStyleSheet('''

                background-color: qradialgradient(cx: 0.5, cy: 0.5, radius: 2, fx: 0.5, fy: 1, stop: 0 rgba(130, 36, 38,190), stop: 0.2 rgb(171, 39, 42), stop: 0.4 rgba(255,30,30,32));

                ''')
            else:
                items[item].widget().ui.LP_Button.setStyleSheet(";")

################################ UI Methods ###############################################

    def closeEvent(self, event):
        try:
            sqlitepath = Path('ResourceFiles/Database/Intg_osdag.sqlite')
            sqlpath = Path('ResourceFiles/Database/Intg_osdag.sql')
            precisionscript = 'ResourceFiles/Database/precision.awk'
            if sqlitepath.exists() and (
                    not sqlpath.exists() or sqlpath.stat().st_size == 0 or sqlpath.stat().st_mtime < sqlitepath.stat().st_mtime - 1):
                sqlnewpath = Path('ResourceFiles/Database/Intg_osdag_new.sql')
                cmd = 'sqlite3 ' + str(sqlitepath) + ' .dump | gawk -f ' + precisionscript + ' > ' + str(sqlnewpath)
                error = os.system(cmd)
                # if error != 0:
                #      raise Exception('SQLite conversion to SQL error 1')
                # if sqlnewpath.stat().st_size == 0:
                #      raise Exception('SQLite conversion to SQL error 2')
                os.remove(sqlpath)
                sqlnewpath.rename(sqlpath)
                sqlitepath.touch()
                print('DUMP updated')
        except Exception as e:
            sqlnewpath.unlink()
            print('Error: ', e)

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
        elif loc == "Check for Update":
            update_class = Update()
            msg = update_class.notifi()
            QMessageBox.information(self, 'Info',msg)
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
        label=QLabel('This Module is Currently Under Development')
        Page.layout.addWidget(label)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName('under_development_label')
        return Page

    def ButtonConnection(self,Button,Modules,ModuleName):
        Button.ui.LP_Button.clicked.connect(lambda : self.ui.myStackedWidget.setCurrentIndex(Modules.index(ModuleName)+1))

#################################### Module Launchers ##########################################

    @pyqtSlot()
    def show_shear_connection(self):
        if self.findChild(QRadioButton,'Fin_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(FinPlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'Cleat_Angle').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(CleatAngleConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'Seated_Angle').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow( SeatedAngleConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'End_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(EndPlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        else:
            QMessageBox.about(self, "INFO", "Please select appropriate connection")

    def show_moment_connection(self):
        if self.findChild(QRadioButton,'B2B_Cover_Plate_Bolted').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(BeamCoverPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'B2B_Cover_Plate_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(BeamCoverPlateWeld, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        # elif self.findChild(QRadioButton,'B2B_End_Plate_Connection').isChecked():
        #     self.hide()
        #     self.ui2 = Ui_ModuleWindow(BeamBeamEndPlateSplice,' ')
        #     self.ui2.show()
        #     self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton, 'B2B_End_Plate_Splice').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(BeamBeamEndPlateSplice, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_moment_connection_bc(self):
        if self.findChild(QRadioButton,'BC_End_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(BeamColumnEndPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_base_plate(self):
        if self.findChild(QRadioButton, 'Base_Plate').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(BasePlateConnection, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_truss_bolted(self):
        if self.findChild(QRadioButton, 'Truss_Bolted').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(TrussConnectionBolted, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        #elif self.findChild(QRadioButton,'Truss_Welded').isChecked():
        #    self.hide()
        #    self.ui2 = Ui_ModuleWindow(BasePlateConnection, ' ')
        #    self.ui2.show()
        #    self.ui2.closed.connect(self.show)
        else:
            QMessageBox.about(self, "INFO", "Please select appropriate connection")

    def show_moment_connection_cc(self):
        if self.findChild(QRadioButton,'C2C_Cover_Plate_Bolted').isChecked() :
            self.hide()
            self.ui2 = Ui_ModuleWindow(ColumnCoverPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton,'C2C_Cover_Plate_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(ColumnCoverPlateWeld, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.findChild(QRadioButton,'C2C_End_Plate_Connection').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(ColumnEndPlate, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    # def show_compression_module(self):
    #     # folder = self.select_workspace_folder()
    #     # folder = str(folder)
    #     # if not os.path.exists(folder):
    #     #     if folder == '':
    #     #         pass
    #     #     else:
    #     #         os.mkdir(folder, 0o755)
    #     #
    #     # root_path = folder
    #     # images_html_folder = ['images_html']
    #     # flag = True
    #     # for create_folder in images_html_folder:
    #     #     if root_path == '':
    #     #         flag = False
    #     #         return flag
    #     #     else:
    #     #         try:
    #     #             os.mkdir(os.path.join(root_path, create_folder))
    #     #         except OSError:
    #     #             shutil.rmtree(os.path.join(folder, create_folder))
    #     #             os.mkdir(os.path.join(root_path, create_folder))
    #     if self.findChild(QRadioButton,'Compression_Bolted').isChecked():
    #         self.hide()
    #         self.ui2 = Ui_ModuleWindow(Compression, ' ')
    #         self.ui2.show()
    #         self.ui2.closed.connect(self.show)
    #
    #     elif self.findChild(QRadioButton,'Compression_Welded').isChecked():
    #         self.hide()
    #         self.ui2 = Ui_ModuleWindow(Compression, ' ')
    #         self.ui2.show()
    #         self.ui2.closed.connect(self.show)

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
            self.ui2 = Ui_ModuleWindow(Tension_bolted, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.findChild(QRadioButton,'Tension_Welded').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(Tension_welded, ' ')
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_compression_module(self):
        """ Create radio buttons for the sub-modules under the compression module"""
        # print(f"Here8")
        if self.findChild(QRadioButton, 'Column_Design').isChecked():
            # print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(ColumnDesign, ' ')
            # print(f"Here11")
            self.ui2.show()
            self.ui2.closed.connect(self.show)

        elif self.findChild(QRadioButton, 'Strut_Design').isChecked():
            print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(Compression, ' ')
            print(f"Here11.2")
            self.ui2.show()
            self.ui2.closed.connect(self.show)

    def show_flexure_module(self):
        """ Create radio buttons for the sub-modules under the compression module"""
        # print(f"Here8")
        if self.findChild(QRadioButton, 'Beam_flexure').isChecked():
            # print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(Flexure, ' ')
            # print(f"Here11")
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton, 'Beam_flexure2').isChecked():
            # print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(Flexure_Cantilever, ' ')
            # print(f"Here11")
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton, 'Beam_flexure3').isChecked():
            # print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(Flexure_Misc, ' ')
            # print(f"Here11")
            self.ui2.show()
            self.ui2.closed.connect(self.show)
        elif self.findChild(QRadioButton, 'Beam_flexure4').isChecked():
            # print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(Flexure_Purlin, ' ')
            # print(f"Here11")
            self.ui2.show()
            self.ui2.closed.connect(self.show)
    def show_beamcolumn_module(self):
        if self.findChild(QRadioButton, 'Beam_flexure').isChecked():
            # print(f"Here9")
            self.hide()
            self.ui2 = Ui_ModuleWindow(Flexure, ' ')
            # print(f"Here11")
            self.ui2.show()
            self.ui2.closed.connect(self.show)
    def Show_Girder_Design(self):
        if self.findChild(QRadioButton, 'Welded_Girder_Design').isChecked():
            self.hide()
            self.ui2 = Ui_ModuleWindow(PlateGirderWelded, ' ')
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
        root_path = os.path.join('ResourceFiles', 'html_page', '_build', 'html')
        for html_file in os.listdir(root_path):
            # if html_file.startswith('index'):
            print(os.path.splitext(html_file)[1])
            if os.path.splitext(html_file)[1] == '.html':
               if sys.platform == ("win32" or "win64"):
                   os.startfile(os.path.join(root_path, html_file))
               else:
                   opener ="open" if sys.platform == "darwin" else "xdg-open"
                   subprocess.call([opener, "%s/%s" % (root_path, html_file)])

    def change_theme(self):
        state = self.ui.switch.isChecked()
        toggle_stylesheet(state)

# class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
#
#     def __init__(self, icon, parent=None):
#         QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
#         self.parent = parent
#         menu = QtWidgets.QMenu(self.parent)
#         self.setContextMenu(menu)
#         menu.addAction("Exit", self.exit)
#
#
#     def exit(self):
#         QCoreApplication.exit()

######################### UpDateNotifi ################

# class Update(QMainWindow):
#     def __init__(self, old_version):
#         super().__init__()
#         self.old_version=old_version
#     def notifi(self):
#         try:
#             url = "https://anshulsingh-py.github.io/test/version.txt"
#             file = urllib.request.urlopen(url)
#             for line in file:
#                 decoded_line = line.decode("utf-8")
#             new_version = decoded_line.split("=")[1]
#             if int(new_version) > self.old_version:
#                 print("update")
#                 msg = QMessageBox.information(self, 'Update available','<a href=https://google.com>Click to downlaod<a/>')
#         except:
#             print("No internet connection")

def toggle_stylesheet(state):
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("No Qt Application found.")
    if state:
        path = 'darkstyle.qss'
    else:
        path = 'light.qss'
    theme_path = str(files("osdag.data.themes").joinpath(path))
    file = QFile(theme_path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

def hook_exception(exc_type, exc_value, tracebackobj):

    instance = QApplication.instance()
    # KeyboardInterrupt is a special case.
    # We don't raise the error dialog when it occurs.
    if issubclass(exc_type, KeyboardInterrupt):
        if instance:
            instance.closeAllWindows()
        return

    separator = '-' * 80
    notice = \
        """An unhandled exception occurred. Please report the problem\n""" \
        """using the error reporting dialog or raise the issue to {}.\n""" \
        """\n\nError information:\n""".format('github.com/osdag-admin/Osdag')
    time_string = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(exc_type), str(exc_value))

    sections = [separator, time_string, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    error_box.text_edit.setText(str(notice) + str(msg))
    error_box.titlebar.save_log.clicked.connect(save_log(str(notice)+str(msg)))
    error_box.titlebar.report_issue.clicked.connect(send_crash_report)

    error_box.setWindowModality(QtCore.Qt.ApplicationModal)
    if not error_box.exec_():
        instance.quit()

def save_log(log):
    def save_():
        file_type = "log (*.log)"
        filename, _ = QFileDialog.getSaveFileName(QFileDialog(), "Save File As", '', file_type)
        if filename:
            with open(filename,'w') as file:
                file.write(log)
            QMessageBox.information(QMessageBox(), "Information", "Log saved successfully.")
    return save_

def get_system_info():
    return 'OS: %s\nPython: %r' % (sys.platform, sys.version_info)

def get_application_log():
    return error_box.text_edit.toPlainText()

def send_crash_report():
    appcrash.get_application_log = get_application_log
    appcrash.get_system_information = get_system_info
    appcrash.show_report_dialog()

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        menu = QtWidgets.QMenu(self.parent)
        self.setContextMenu(menu)
        menu.addAction("Exit", self.exit)


    def exit(self):
        QCoreApplication.exit()

# FIXME: This is created in `do_stuff` and used above. Find better alternatives.
error_box = None

def do_stuff():
    # from .cad.common_logic import CommonDesignLogic
    from multiprocessing import Pool
    import multiprocessing

    # app = QApplication(sys.argv)
    # screen = app.screens()[0]
    # dpi = screen.physicalDotsPerInch()
    # scale = round(dpi/140.0,1)
    #
    # print('scale', dpi, scale,scale*300)
    path = str(files("osdag.data.themes").joinpath('light.qss'))
    file = QFile(path)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app = QApplication(sys.argv)
    app.setStyleSheet(stream.readAll())
    app.setStyle('Fusion')

    # path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'images', 'Osdag.png')
    window = OsdagMainWindow()
    # print("Here0")

    # trayIcon = SystemTrayIcon(QtGui.QIcon(path), window)

    ############################     Exception Dialog and Error Reporting  ###################

    global error_box
    error_box = CriticalExceptionDialog()

    GITHUB_OWNER = 'osdag-admin'    # username of the github account where crash report is to be submitted
    GITHUB_REPO = 'Osdag'       # repo name
    EMAIL = 'your.email@provider.com'  # Email address of developers

    appcrash.install_backend(appcrash.backends.GithubBackend(GITHUB_OWNER, GITHUB_REPO))
    appcrash.install_backend(appcrash.backends.EmailBackend(EMAIL, 'Osdag'))

    #my_settings = QtCore.QSettings('FOSSEE','osdag')
    #appcrash.set_qsettings(my_settings)
    '''
    You can save your GitHub username and password across each sessions so that you don't have to enter it each time you report an issue.
    
    Simply uncomment above two lines. To use QSetings we need to give an organisation name and the application name (compulsory).

    For example, 'FOSSEE' is an organisation name and 'Osdag' is the application name in the above QSettings. Feel free to change them to suit your requirement, but try to keep it constant.
    Do not change it frequently.

    '''

    ############################     Exception Dialog and Error Reporting  ###################

    # trayIcon.show()

    try:
        # window.notification2()
        #update = Update(0)
        #update.notifi()

        sys.excepthook = hook_exception
        QCoreApplication.exit(app.exec()) # to properly close the Qt Application use QCoreApplication instead of sys
    except BaseException as e:
        print("ERROR", e)

if __name__ == '__main__':
    do_stuff()
