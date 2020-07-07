# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_section_parameters.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from Common import PATH_TO_DATABASE

class Ui_SectionParameters(QtWidgets.QDialog):
    def __init__(self,index_type,index_template):
        super().__init__()
        self.setObjectName("Dialog")
        self.setWindowModality(QtCore.Qt.NonModal)
        #self.resize(319, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        #self.setMinimumSize(QtCore.QSize(0, 300))
        self.setMaximumSize(QtCore.QSize(100000, 100000))
        self.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.parameterLabel_1 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_1.setFont(font)
        self.parameterLabel_1.setObjectName("parameterLabel_1")
        self.verticalLayout.addWidget(self.parameterLabel_1)
        self.parameterLabel_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_2.setFont(font)
        self.parameterLabel_2.setObjectName("parameterLabel_2")
        self.verticalLayout.addWidget(self.parameterLabel_2)
        self.parameterLabel_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_3.setFont(font)
        self.parameterLabel_3.setObjectName("parameterLabel_3")
        self.verticalLayout.addWidget(self.parameterLabel_3)
        self.parameterLabel_4 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_4.setFont(font)
        self.parameterLabel_4.setObjectName("parameterLabel_4")
        self.verticalLayout.addWidget(self.parameterLabel_4)
        self.parameterLabel_5 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_5.setFont(font)
        self.parameterLabel_5.setObjectName("parameterLabel_5")
        self.verticalLayout.addWidget(self.parameterLabel_5)
        self.parameterLabel_6 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_6.setFont(font)
        self.parameterLabel_6.setObjectName("parameterLabel_6")
        self.verticalLayout.addWidget(self.parameterLabel_6)
        self.parameterLabel_7 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterLabel_7.setFont(font)
        self.parameterLabel_7.setObjectName("parameterLabel_7")
        self.verticalLayout.addWidget(self.parameterLabel_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.parameterText_1 = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_1.sizePolicy().hasHeightForWidth())
        self.parameterText_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_1.setFont(font)
        self.parameterText_1.setObjectName("parameterText_1")
        self.verticalLayout_2.addWidget(self.parameterText_1)
        self.parameterText_2 = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_2.sizePolicy().hasHeightForWidth())
        self.parameterText_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_2.setFont(font)
        self.parameterText_2.setObjectName("parameterText_2")
        self.verticalLayout_2.addWidget(self.parameterText_2)
        self.parameterText_3 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_3.sizePolicy().hasHeightForWidth())
        self.parameterText_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_3.setFont(font)
        self.parameterText_3.setObjectName("parameterText_3")
        self.verticalLayout_2.addWidget(self.parameterText_3)
        self.parameterText_4 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_4.sizePolicy().hasHeightForWidth())
        self.parameterText_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_4.setFont(font)
        self.parameterText_4.setObjectName("parameterText_4")
        self.verticalLayout_2.addWidget(self.parameterText_4)
        self.parameterText_5 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_5.sizePolicy().hasHeightForWidth())
        self.parameterText_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_5.setFont(font)
        self.parameterText_5.setObjectName("parameterText_5")
        self.verticalLayout_2.addWidget(self.parameterText_5)
        self.parameterText_6 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_6.sizePolicy().hasHeightForWidth())
        self.parameterText_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_6.setFont(font)
        self.parameterText_6.setObjectName("parameterText_6")
        self.verticalLayout_2.addWidget(self.parameterText_6)
        self.parameterText_7 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterText_7.sizePolicy().hasHeightForWidth())
        self.parameterText_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.parameterText_7.setFont(font)
        self.parameterText_7.setObjectName("parameterText_7")
        self.verticalLayout_2.addWidget(self.parameterText_7)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.saveBtn = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.saveBtn.setFont(font)
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout_2.addWidget(self.saveBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.update_parameters(index_type,index_template)
        self.saveBtn.clicked.connect(lambda:self.save_parameters(index_type,index_template))
        self.textBoxVisible={} 
        self.apply_character_validations()  
        self.set_image_tooltip(index_type,index_template) 

    def apply_character_validations(self):
        '''
        Method to add basic character validations to section parameters
        '''
        self.parameterText_3.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.parameterText_3
        ))
        self.parameterText_4.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.parameterText_4
        ))
        self.parameterText_5.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.parameterText_5
        ))
        self.parameterText_6.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.parameterText_6
        ))
        self.parameterText_7.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp("[0-9.]*"), self.parameterText_7
        ))

    def save_parameters(self,index_type,index_template):
        '''
        Save Section Parameters for further use
        '''
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_1").isVisible()):
            self.textBoxVisible['parameterText_1']=[self.findChild(QtWidgets.QLabel,"parameterLabel_1").text().strip()[:-1],self.findChild(QtWidgets.QComboBox,'parameterText_1').currentText()]
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_2").isVisible()):
            self.textBoxVisible['parameterText_2']=[self.findChild(QtWidgets.QLabel,"parameterLabel_2").text().strip()[:-1],self.findChild(QtWidgets.QComboBox,'parameterText_2').currentText()]
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_3").isVisible()):
            self.textBoxVisible['parameterText_3']=[self.findChild(QtWidgets.QLabel,"parameterLabel_3").text().strip()[:-1],self.findChild(QtWidgets.QLineEdit,'parameterText_3').text()]
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_4").isVisible()):
            self.textBoxVisible['parameterText_4']=[self.findChild(QtWidgets.QLabel,"parameterLabel_4").text().strip()[:-1],self.findChild(QtWidgets.QLineEdit,'parameterText_4').text()]
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_5").isVisible()):
            self.textBoxVisible['parameterText_5']=[self.findChild(QtWidgets.QLabel,"parameterLabel_5").text().strip()[:-1],self.findChild(QtWidgets.QLineEdit,'parameterText_5').text()]
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_6").isVisible()):
            self.textBoxVisible['parameterText_6']=[self.findChild(QtWidgets.QLabel,"parameterLabel_6").text().strip()[:-1],self.findChild(QtWidgets.QLineEdit,'parameterText_6').text()]
        if(self.findChild(QtWidgets.QLabel,"parameterLabel_7").isVisible()):
            self.textBoxVisible['parameterText_7']=[self.findChild(QtWidgets.QLabel,"parameterLabel_7").text().strip()[:-1],self.findChild(QtWidgets.QLineEdit,'parameterText_7').text()]
        flag="ErrorType"        
        for parameter in self.textBoxVisible:
            if(self.textBoxVisible[parameter][1]=="" or  'select' in self.textBoxVisible[parameter][1].lower()):
                flag='NoPara'
            try:
                if(self.textBoxVisible[parameter][1].count('.')>1 or '.' == self.textBoxVisible[parameter][1][-1]):
                    flag='DecimalProb'
            except:
                flag='WrittenandDeleted'        
            

        if(flag in ['NoPara','WrittenandDeleted']):
            QtWidgets.QMessageBox.critical(self,'Save Error','All Parameters not entered/selected')
            self.textBoxVisible={}
            return
        elif(flag=='DecimalProb'):
            QtWidgets.QMessageBox.critical(self,'Save Error','Ill-positioned or extra decimals found.')
            self.textBoxVisible={}
            return

        error,string=self.func_for_numerical_validations(index_type,index_template)
        if(error==True):
            QtWidgets.QMessageBox.critical(self, "Error", f"Following condition(s) is/are not satisfied:\n\n{string}") 
            self.textBoxVisible={}     
            return  

        self.close()
    
    def func_for_numerical_validations(self,index_type,index_template):
        '''
        Method to validate template-wise Section Parameters
        '''
        error=False
        string=""
        conn = sqlite3.connect(PATH_TO_DATABASE)
        if(index_type==1):
            cursor = conn.execute("SELECT B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
            B=float(cursor.fetchone()[0])
            s=float(self.parameterText_3.text())
            if(s<=B):
                error=True
                string+='S > '+str(B)+'\n'
        elif(index_type==2):
            cursor = conn.execute("SELECT B FROM Channels where Designation="+repr(self.parameterText_1.currentText()))
            B=float(cursor.fetchone()[0])      
            s=float(self.parameterText_3.text())  
            if(index_template==1):
                if(s<=2*B):
                    error=True
                    string+='S > '+str(2*B)+'\n'
        elif(index_type==4):
            if(index_template==1):
                cursor = conn.execute("SELECT D,T,tw FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                D,T,t=map(float,cursor.fetchall()[0])
                s=float(self.parameterText_3.text())
                P=float(self.parameterText_6.text())
                ta=float(self.parameterText_7.text())
                Db=D-(2*T)
                comp=round(Db/2,1)
                if(P>=comp):
                    error=True
                    string+='P < '+str(comp)+'\n'
                if(ta<t or ta>T):
                    error=True
                    string+=str(t)+' <= t* <= '+str(T)+'\n'

        return error,string
    
    def set_image_tooltip(self,index_type,index_template):
        '''
        Method to set Tooltip Image for each Section Parameter(Template-wise)
        '''
        if(index_type==1):
            self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/1.1(1).png'>")
            self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/1.1(2).png'>")
            self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/1.1(3).png'>")
        elif(index_type==2):
            if(index_template==1):
                self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/2.1(1).png'>")
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/2.1(2).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/2.1(3).png'>")
            elif(index_template==2):
                self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/2.2(1).png'>")
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/2.2(2).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/2.2(3).png'>")
        elif(index_type==3):
            if(index_template==1):
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.1(2).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.1(1).png'>")
            elif(index_template==2):
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.2(1).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.2(2).png'>")
            elif(index_template==3):
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.3(1).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.3(2).png'>")
            elif(index_template==4):
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.4(1).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.4(2).png'>")
            elif(index_template==5):
                self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.5(1).png'>")
                self.parameterText_4.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.5(2).png'>")
                self.parameterText_5.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.5(4).png'>")
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.5(3).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/3.1.5(5).png'>")
        elif(index_type==4):
            if(index_template==1):
                self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.1.1(2).png'>")
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.1.1(1).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.1.1(3).png'>")
            elif(index_template==2):
                self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.1.2(2).png'>")
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.1.2(1).png'>")
            elif(index_template==3):
                self.parameterText_5.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.2.1(1).png'>")
                self.parameterText_6.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.2.1(2).png'>")
                self.parameterText_7.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/4.2.1(3).png'>")

        elif(index_type==5):
            self.parameterText_3.setToolTip("<img src='./ResourceFiles/images/SectionModeller/SectionParameters/5.1.1(1).png'>")

    def update_parameters(self,index_type,index_template):
        '''
        Method for Updation of field in Section Parameters Dialog
        and also contents on some fields based on conditions
        '''
        conn = sqlite3.connect(PATH_TO_DATABASE)
        if(index_type==1):
            def calc_length():
                if(self.parameterText_3.text() in ['',None] or self.parameterText_1.currentIndex()==0):
                        return
                cursor = conn.execute("SELECT tw,B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                t,B=map(float,cursor.fetchall()[0])
                s=float(self.parameterText_3.text())
                self.parameterText_6.setText(str(round((s+(2*((B/2)+(2*(t/2))))),1)))          
            
            def calc_t():
                if(self.parameterText_1.currentIndex()==0):
                        return
                cursor = conn.execute("SELECT tw FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                t=float(cursor.fetchone()[0])
                if(t%3==0):
                    ta=t
                else:
                    ta=((t//3)+1)*3
                self.parameterText_7.setText(str(ta))

            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            self.parameterLabel_4.hide()
            self.parameterText_4.hide()
            self.parameterLabel_5.hide()
            self.parameterText_5.hide()
            self.parameterLabel_1.setText('Type of I-Section:')
            self.parameterLabel_3.setText('Spacing(web-web) between I Sections, S(mm):')
            self.parameterLabel_6.setText('Length of Cover Plate, l(mm):')
            self.parameterText_6.setDisabled(True)
            self.parameterLabel_7.setText('Thickness of Cover Plate, t*(mm):')
            self.parameterText_7.setDisabled(True)
            self.parameterText_3.textChanged.connect(calc_length)
            self.parameterText_1.currentIndexChanged.connect(calc_t)
            self.parameterText_1.currentIndexChanged.connect(calc_length)
            
        elif(index_type==2):

            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            self.parameterLabel_4.hide()
            self.parameterText_4.hide()
            self.parameterLabel_5.hide()
            self.parameterText_5.hide()
            self.parameterLabel_1.setText('Type of Channel Section:')
            self.parameterLabel_3.setText('Spacing(web-web) between the Channel sections, S(mm):')

            def calc_length():
                if(self.parameterText_3.text() in ['',None] or self.parameterText_1.currentIndex()==0):
                        return
                cursor = conn.execute("SELECT tw,B FROM Channels where Designation="+repr(self.parameterText_1.currentText()))
                t,B=map(float,cursor.fetchall()[0])
                s=float(self.parameterText_3.text())
                if(index_template==1):
                    comp=round(s+(2*t),1)                    
                if(index_template==2):
                    comp=round(s+(2*B),1)  
                self.parameterText_6.setText(str(comp))
            
            def calc_t():
                if(self.parameterText_1.currentIndex()==0):
                        return
                cursor = conn.execute("SELECT tw FROM Channels where Designation="+repr(self.parameterText_1.currentText()))
                t=float(cursor.fetchone()[0])
                if(t%3==0):
                    ta=t
                else:
                    ta=((t//3)+1)*3
                self.parameterText_7.setText(str(ta))
            
            

            self.parameterText_6.setDisabled(True)
            self.parameterText_3.textChanged.connect(calc_length)   
            self.parameterText_1.currentIndexChanged.connect(calc_length) 
            self.parameterText_1.currentIndexChanged.connect(calc_t) 
            self.parameterLabel_6.setText('Length of Cover Plate, l(mm):')
            self.parameterLabel_7.setText('Thickness of Cover Plate, t*(mm):')
            self.parameterText_7.setDisabled(True)

        elif(index_type==3):
            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            self.parameterLabel_1.setText('Type of Angle Section:')
            if(index_template<5):
                self.parameterLabel_2.hide()
                self.parameterText_2.hide()
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_3.hide()
                self.parameterText_3.hide()
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_6.setText('Length of the Gusset Plate, l(mm):')            
                self.parameterLabel_7.setText('Thickness of the Gusset Plate, t*(mm):') 

                

                def calc_length():
                    if(self.parameterText_1.currentIndex()==0 or self.parameterText_1.currentIndex()==0):
                        return
                    cursor = conn.execute("SELECT a FROM Angles where Designation="+repr(self.parameterText_1.currentText()))
                    a = float(cursor.fetchone()[0])
                    if(index_template!=4):
                        comp=2*a
                    if(index_template==4):
                        comp=a
                    self.parameterText_6.setText(str(comp))
                
                self.parameterText_1.currentIndexChanged.connect(calc_length)                    
                self.parameterText_6.setDisabled(True)
            else:
                self.parameterLabel_3.setText('Spacing(Shorter Leg), S(mm):')
                self.parameterLabel_4.setText('Spacing(Longer Leg), S*(mm):')
                self.parameterLabel_5.setText('Length of the Gusset Plate(Horizantal), l(mm):')
                self.parameterLabel_6.setText('Length of the Gusset Plate(Verticle), l*(mm):')
                self.parameterLabel_7.setText('Thickness of the Gusset Plate, t*(mm):') 
                def calc_length_h():
                    if(self.parameterText_1.currentIndex()==0 or self.parameterText_3.text() in ['',None] or self.parameterText_7.text() in ['',None]):
                        return
                    cursor = conn.execute("SELECT b FROM Angles where Designation="+repr(self.parameterText_1.currentText()))
                    b = float(cursor.fetchone()[0])
                    s=float(self.parameterText_3.text())
                    ta=float(self.parameterText_7.text())  
                    self.parameterText_5.setText(str(s+(2*ta)+(2*b)))
                def calc_length_v():
                    if(self.parameterText_4.text() in ['',None] or self.parameterText_1.currentIndex()==0):
                        return
                    cursor = conn.execute("SELECT a FROM Angles where Designation="+repr(self.parameterText_1.currentText()))
                    a = float(cursor.fetchone()[0])
                    sa=float(self.parameterText_4.text())
                    self.parameterText_6.setText(str(sa+(2*a)))

                self.parameterText_1.currentIndexChanged.connect(calc_length_h)
                self.parameterText_1.currentIndexChanged.connect(calc_length_v)
                self.parameterText_7.textChanged.connect(calc_length_h)
                self.parameterText_3.textChanged.connect(calc_length_h)
                self.parameterText_4.textChanged.connect(calc_length_v)
                self.parameterText_5.setDisabled(True)
                self.parameterText_6.setDisabled(True)
                
        elif(index_type==4):
            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            if(index_template==1):
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_1.setText('Type of I-Section:')
                self.parameterLabel_3.setText('Spacing, S(mm):')
                self.parameterLabel_6.setText('Lip Size, P(mm):')
                self.parameterLabel_7.setText('Thickness of Lip, t*(mm):')
                def calc_t():
                    if(self.parameterText_1.currentIndex()==0):
                        return
                    cursor = conn.execute("SELECT T,tw FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                    T,t=map(float,cursor.fetchall()[0])
                    if(t==T):
                        self.parameterText_7.setText(str(t))
                        self.parameterText_7.setDisabled(True)
                    else:
                        self.parameterText_7.clear()
                        self.parameterText_7.setDisabled(False)
                def calc_s():
                    if(self.parameterText_1.currentIndex()==0 or self.parameterText_7.text() in ['',None]):
                        return
                    try:
                        float(self.parameterText_7.text())
                    except:
                        return
                    cursor = conn.execute("SELECT B,tw FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                    B,t=map(float,cursor.fetchall()[0])
                    ta=float(self.parameterText_7.text())
                    s=round((B-t-(2*ta))/2,1)
                    self.parameterText_3.setText(str(s))


                self.parameterText_1.currentIndexChanged.connect(calc_t)
                self.parameterText_3.setDisabled(True)
                self.parameterText_1.currentIndexChanged.connect(calc_s)
                self.parameterText_7.textChanged.connect(calc_s)

            elif(index_template==2):
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_1.setText('I-Section Type:')
                self.parameterLabel_3.setText('Spacing , S(mm):')
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_6.setText('Length of Web of T, d(mm):')
                self.parameterLabel_7.hide()
                self.parameterText_7.hide()
                def para():
                    if(self.parameterText_1.currentIndex()==0):
                        return
                    cursor = conn.execute("SELECT D,T,tw,B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                    D,T,t,B=map(float,cursor.fetchall()[0])
                    Db=D-(2*T)
                    comp1=round((Db-t)/2,1)
                    comp2=round((B-(2*T)-t)/2,1)
                    self.parameterText_6.setText(str(comp1))
                    self.parameterText_7.setText(str(comp2))
                self.parameterText_1.currentIndexChanged.connect(para)
                self.parameterText_6.setDisabled(True)
                self.parameterText_7.setDisabled(True)

                
            elif(index_template==3):
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_3.hide()
                self.parameterText_3.hide()
                self.parameterLabel_1.hide()
                self.parameterText_1.hide()
                self.parameterLabel_5.setText('Length of Hollow Section, B(mm):')
                self.parameterLabel_6.setText('Breadth of Hollow Section, L(mm):')
                self.parameterLabel_7.setText('Thickness of Hollow Section, t(mm):')

        elif(index_type==5):
            self.parameterLabel_4.hide()
            self.parameterText_4.hide()
            self.parameterLabel_5.hide()
            self.parameterText_5.hide()
            self.parameterLabel_6.hide()
            self.parameterText_6.hide()
            self.parameterLabel_7.hide()
            self.parameterText_7.hide()
            self.parameterLabel_1.setText('Type of I-Section:')
            self.parameterLabel_2.setText('Type of Channel Section:')
            self.parameterLabel_3.setText('Spacing between I-Section and Flange of Channel, S(mm):')
            def calc_s():
                if(self.parameterText_1.currentIndex()==0):
                    return
                cursor = conn.execute("SELECT tw,B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                t,B=map(float,cursor.fetchall()[0])
                self.parameterText_3.setText(str(round((B-t)/2,1)))
            self.parameterText_3.setDisabled(True)
            self.parameterText_1.currentIndexChanged.connect(calc_s)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Section Parameters"))
        self.parameterLabel_1.setText(_translate("Dialog", "I-Section Type:"))
        self.parameterLabel_2.setText(_translate("Dialog", "Channel Type:"))
        self.parameterLabel_3.setText(_translate("Dialog", "Spacing_H (s):"))
        self.parameterLabel_4.setText(_translate("Dialog", "Spacing_V (s*):"))
        self.parameterLabel_5.setText(_translate("Dialog", "Length (l):"))
        self.parameterLabel_6.setText(_translate("Dialog", "Thickness_H (l*):"))
        self.parameterLabel_7.setText(_translate("Dialog", "Thickness_V (t*):"))        
        self.saveBtn.setText(_translate("Dialog", "Save"))
