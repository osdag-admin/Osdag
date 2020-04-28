from PyQt5.QtCore import pyqtSlot,pyqtSignal, QObject, Qt,QSize
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox, QFileDialog, QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QTabWidget, QRadioButton, QButtonGroup, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5 import uic
import sys
from gui.ui_tutorial import Ui_Tutorial
from gui.ui_aboutosdag import Ui_AboutOsdag
from gui.ui_ask_question import Ui_AskQuestion
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
from gui.ui_template import Ui_ModuleWindow

import configparser
import os
import os.path
import subprocess
from gui.ui_template import Ui_ModuleWindow
from gui.ui_design_summary import Ui_DesignReport



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

class New_Tab_Widget(QTabWidget):
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

class Submodule_Page(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/Submodule_Page.ui',self)

class Submodule_Widget(QWidget):
    def __init__(self,Iterative,parent):
        super().__init__()
        Name,Image,ObjName=Iterative
        layout=QVBoxLayout()
        self.setLayout(layout)
        label=QLabel(Name)
        layout.addWidget(label)
        self.rdbtn=QRadioButton()
        self.rdbtn.setObjectName(ObjName)
        self.rdbtn.setIcon(QIcon('C:/Users/satya/Desktop/Osdag3/ResourceFiles/images/finplate.png'))
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
        uic.loadUi('gui/LeftPanel_Button.ui',self)
        self.LP_Button.setText(text)  #LP_Button is the QPushButton widget inside the LeftPanelButton Widget
class OsdagMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/ui_OsdagMainPage.ui',self)
        self.comboBox_help.currentIndexChanged.connect(self.selection_change)
        self.Under_Development='UNDER DEVELOPMENT'
        self.Modules={
                'Connection' : {
                                'Shear Connection' : [
                                    ('Fin Plate','Fin Plate Image','Fin_Plate'),
                                    ('Cleat Angle','Cleat Angle Image','Cleat_Angle'),
                                    ('End Plate','End Plate Image','End_Plate'),
                                    ('Seated Angle','Seated Angle Image','Seated_Angle'),
                                    self.show_shear_connection,
                                                    ],
                                'Moment Connection' :{
                                                    'Beam to Beam' :[
                                                                ('Cover Plate Bolted','Cover Plate Bolted Image','B2B_Cover_Plate_Bolted'),
                                                                ('Cover Plate Welded','Cover Plate Welded Image','B2B_Cover_Plate_Welded'),
                                                                ('Cover Plate Connection','Cover Plate Connection Image','B2B_Cover_Plate_Connection'),
                                                                self.show_moment_connection,
                                                                    ],
                                                    'Beam to Column' :[
                                                                ('End Plate Connection','End Plate Connection Image','B2C_End_Plate_Connection'),
                                                                self.show_base_plate,
                                                                      ],
                                                    'Column to Column' :[
                                                                ('Cover Plate Bolted','Cover Plate Bolted Image','C2C_Cover_Plate_Bolted'),
                                                                ('Cover Plate Welded','Cover Plate Welded Image','C2C_Cover_Plate_Welded'),
                                                                ('Cover Plate Connection','Cover Plate Connection Image','C2C_Cover_Plate_Connection'),
                                                                self.show_moment_connection_cc,
                                                                    ],
                                                    'PEB' : 'UNDER DEVELOPMENT',
                                                    },
                                'Base Plate': 'UNDER DEVELOPMENT',
                                'Truss Connection' : 'UNDER DEVELOPMENT',
                                },
                'Tension Member' : [
                            ('Bolted','Bolted Image','Tension_Bolted'),
                            ('Welded','Welded Image','Tension_Welded'),
                            self.show_tension_module,
                                   ],
                'Compression Member' : [
                            ('Bolted','Bolted Image','Compression_Bolted'),
                            ('Welded','Welded Image','Compression_Welded'),
                            self.show_compression_module,
                                       ],
                'Flexural Member' : 'UNDER DEVELOPMENT',
                'Beam-Column' : 'UNDER DEVELOPMENT',
                'Plate Girder' : 'UNDER DEVELOPMENT',
                'Truss' : 'UNDER DEVELOPMENT',
                '2D Frame' : 'UNDER DEVELOPMENT',
                '3D Frame' : 'UNDER DEVELOPMENT',
                'Group Design' : 'UNDER DEVELOPMENT',
                }

####################################### UI Formation ################################

        for ModuleName in self.Modules:                      #Level 1 dictionary handling
            Button= LeftPanelButton(ModuleName)
            self.ButtonConnection(Button,list(self.Modules.keys()),ModuleName)  
            self.verticalLayout.addWidget(Button)       
            if(type(self.Modules[ModuleName])==dict):        #level 2 dictionary handling
                Page= ModulePage()
                self.myStackedWidget.addWidget(Page)
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

                                for Selection in Current_SubModule[Sub_Sub_Module][:-1]:
                                    widget=Submodule_Widget(Selection,New_Sub_Tab)
                                    group.addButton(widget.rdbtn)
                                    New_Sub_Tab.gridLayout.addWidget(widget,row,col)

                                    if(col==1):
                                        row+=1
                                        col=0

                                    else:
                                        col+=1
                                New_Sub_Tab.StartButton.clicked.connect(Current_SubModule[Sub_Sub_Module][-1])

                            elif(Current_SubModule[Sub_Sub_Module]==self.Under_Development):   # Final Under Development Handling
                                Sub_Tab_Widget.addTab(self.UnderDevelopmentModule(),Sub_Sub_Module)

                            else:
                                raise ValueError

                    elif(type(Current_Module[Submodule]) in [list,tuple]):      #Level 3 list/tuple handling
                        New_Tab=Submodule_Page()
                        Tab_Widget.addTab(New_Tab,Submodule)
                        group=QButtonGroup(QWidget(Page))
                        row,col=0,0

                        for Selection in Current_Module[Submodule][:-1]:
                            widget=Submodule_Widget(Selection,New_Tab)
                            group.addButton(widget.rdbtn)
                            New_Tab.gridLayout.addWidget(widget,row,col)

                            if(col==1):
                                row+=1
                                col=0

                            else:
                                col+=1
                        New_Tab.StartButton.clicked.connect(Current_Module[Submodule][-1])

                    elif(Current_Module[Submodule]==self.Under_Development):       #Level 3 Under Development handling
                        Tab_Widget.addTab(self.UnderDevelopmentModule(),Submodule)

                    else:
                        raise ValueError

            elif(type(self.Modules[ModuleName]) in [list,tuple]):            # Level 2 list/tuple handling
                Page= Submodule_Page()
                self.myStackedWidget.addWidget(Page)
                group=QButtonGroup(QWidget(Page))
                row,col=0,0

                for Selection in self.Modules[ModuleName][:-1]:
                    widget=Submodule_Widget(Selection,Page)
                    group.addButton(widget.rdbtn)
                    Page.gridLayout.addWidget(widget,row,col)

                    if(col==1):
                        row+=1
                        col=0

                    else:
                        col+=1
                Page.StartButton.clicked.connect(self.Modules[ModuleName][-1])

            elif(self.Modules[ModuleName]==self.Under_Development):           #Level 2 Under Development handling
                self.myStackedWidget.addWidget(self.UnderDevelopmentModule())

            else:
                raise ValueError

################################ UI Methods ###############################################

    def selection_change(self):
        loc = self.comboBox_help.currentText()
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
        Button.LP_Button.clicked.connect(lambda : self.myStackedWidget.setCurrentIndex(Modules.index(ModuleName)+1))

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
        elif self.findChild(QRadioButton,'B2B_Cover_Plate_Connection').isChecked():
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

        elif self.findChild(QRadioButton,'C2C_Cover_Plate_Connection').isChecked():
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
        
