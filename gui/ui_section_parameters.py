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
        #self.setFixedSize(self.sizeHint())    
        self.apply_character_validations()   

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
        flag=False
        for parameter in self.textBoxVisible: 
            if(self.textBoxVisible[parameter][1]=='' or 'Select' in self.textBoxVisible[parameter][1] or 'select' in self.textBoxVisible[parameter][1]):
                flag=True
        if(flag):
            QtWidgets.QMessageBox.critical(self,'Save Error','All Parameters not entered/selected')
            self.textBoxVisible={}
            return
############################ Validations ##############################
        error=False
        string=""
        conn = sqlite3.connect(PATH_TO_DATABASE)
        if(index_type==1):
            cursor = conn.execute("SELECT tw,B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
            t,B=map(float,cursor.fetchall()[0])
            s=float(self.parameterText_3.text())
            l=float(self.parameterText_6.text())
            comp=(s+(2*((B/2)+(2*(t/2)))))         
            if(s>=l/2):
                error=True
                string+='S < '+str(l/2)+'\n'
            if(l!=comp):
                error=True
                string+='l = '+str(comp)+'\n\n ** Try changing l to the value suggested'
        elif(index_type==2):
            cursor = conn.execute("SELECT tw,B FROM Channels where Designation="+repr(self.parameterText_1.currentText()))
            t,B=map(float,cursor.fetchall()[0])
            s=float(self.parameterText_3.text())
            l=float(self.parameterText_6.text())
            if(index_template==1):
                if(s>l-(2*t)):
                    error=True
                    string+='S <= '+str(l-(2*t))+'\n'
                if(l!=s+(2*t)):
                    error=True
                    string+='l = '+str(s+(2*t))+'\n\n ** Try changing l to the value suggested'
            elif(index_template==2):
                if(s>l-(2*B)):
                    error=True
                    string+='S <= '+str(l-(2*B))+'\n'
                if(l!=s+(2*B)):
                    error=True
                    string+='l = '+str(s+(2*B))+'\n\n ** Try changing l to the value suggested'
        elif(index_type==3):
            if(index_template<5):
                cursor = conn.execute("SELECT a FROM Angles where Designation="+repr(self.parameterText_1.currentText()))
                a = float(cursor.fetchone()[0])
                l=float(self.parameterText_6.text())
                ta=float(self.parameterText_7.text())
                if(index_template!=4 and l!=2*a):
                    error=True
                    string+='l = '+str(2*a)+'\n\n ** Try changing l to the value suggested'
                if(index_template==4 and l!=a):
                    error=True
                    string+='l = '+str(a)+'\n\n ** Try changing l to the value suggested'
            elif(index_template==5):
                cursor = conn.execute("SELECT a,t,b FROM Angles where Designation="+repr(self.parameterText_1.currentText()))
                a,t,b = map(float,cursor.fetchall()[0])
                s=float(self.parameterText_3.text())
                sa=float(self.parameterText_4.text())
                l=float(self.parameterText_5.text())
                ta=float(self.parameterText_7.text())
                la=float(self.parameterText_6.text())
                comp=s+(2*ta)+(2*b)
                Da=a-t
                if(sa!=2*Da):
                    error=True
                    string+='S* = '+str(2*Da)+'\n'
                if(s!=l-(2*b)-(2*ta)):
                    error=True
                    string+='S = '+str(l-(2*b)-(2*ta))+'\n'
                if(l!=comp):
                    error=True
                    string+='l = '+str(comp)+'\n'
                if(la!=sa+(2*t)):
                    error=True
                    string+='l* = '+str(sa+(2*t))+'\n'
                if(l<=la):
                    error=True
                    string+='l > l*'+'\n'
        elif(index_type==4):
            if(index_template==1):
                cursor = conn.execute("SELECT D,T,tw FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                D,T,t=map(float,cursor.fetchall()[0])
                P=float(self.parameterText_6.text())
                Q=float(self.parameterText_7.text())
                Db=D-(2*T)
                if(P>=Db/2):
                    error=True
                    string+='P < '+str(Db/2)+'\n'
                if(Q<t):
                    error=True
                    string+=str(T)+' => Q >= '+str(t)+'\n'
                if(Q>T):
                    error=True
                    string+=str(t)+' <= Q <= '+str(T)+'\n'
            elif(index_template==2):
                cursor = conn.execute("SELECT D,T,tw,B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                D,T,t,B=map(float,cursor.fetchall()[0])
                s=float(self.parameterText_3.text())
                d=float(self.parameterText_6.text())
                Db=D-(2*T)
                comp=round((B-(2*T)-t)/2,1)
                if(s!=(Db-t)/2):
                    error=True
                    string+='S = '+str((Db-t)/2)+'\n'
                if(d!=comp):
                    error=True
                    string+='d = '+str(comp)+'\n'
            elif(index_template==3):
                cursor = conn.execute("SELECT B FROM Columns where Designation="+repr(self.parameterText_1.currentText()))
                B=float(cursor.fetchone()[0])
                s=float(self.parameterText_3.text())
                sb=float(self.parameterText_4.text())
                if(s>=B):
                    error=True
                    string+='S < '+str(B)+'\n'
                if(sb>=B):
                    error=True
                    string+='S* < '+str(B)+'\n'
        elif(index_type==5):
            cursor = conn.execute("SELECT D FROM Channels where Designation="+repr(self.parameterText_2.currentText()))
            d=float(cursor.fetchone()[0])
            s=float(self.parameterText_3.text())
            if(s>=d/2):
                error=True
                string+='S < '+str(d/2)+'\n'
        if(error==True):
            QtWidgets.QMessageBox.critical(self, "Error", f"Following condition(s) is/are not satisfied:\n\n{string}") 
            self.textBoxVisible={}     
            return  

        self.close()
    
    def update_parameters(self,index_type,index_template):
        '''
        Method for Updation of field in Section Parameters Dialog
        '''
        if(index_type==1):
            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            self.parameterLabel_4.hide()
            self.parameterText_4.hide()
            self.parameterLabel_5.hide()
            self.parameterText_5.hide()
            self.parameterLabel_1.setText('I-Section Type:')
            self.parameterLabel_3.setText('Spacing between the I-Sections, S(mm):')
            self.parameterLabel_6.setText('Cover Plate Length, l(mm):')
            self.parameterLabel_7.setText('Cover Plate Thickness, t*(mm):')
        elif(index_type==2):
            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            self.parameterLabel_4.hide()
            self.parameterText_4.hide()
            self.parameterLabel_5.hide()
            self.parameterText_5.hide()
            self.parameterLabel_1.setText('Channel Section Type:')
            self.parameterLabel_3.setText('Spacing between the Channel Sections, S(mm):')
            self.parameterLabel_6.setText('Cover Plate Length, l(mm):')
            self.parameterLabel_7.setText('Cover Plate Thickness, t*(mm):')
        elif(index_type==3):
            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            self.parameterLabel_1.setText('Angle Section Type:')
            if(index_template<5):
                self.parameterLabel_2.hide()
                self.parameterText_2.hide()
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_3.hide()
                self.parameterText_3.hide()
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_6.setText('Gusset Plate Length, l(mm):')
                self.parameterLabel_7.setText('Gusset Plate Thickness, t*(mm):') 
            elif(index_template==5):
                self.parameterLabel_3.setText('Spacing between Sections_Horizontal, S(mm):')
                self.parameterLabel_4.setText('Spacing between Sections_Vertical, S*(mm):')
                self.parameterLabel_5.setText('Plate Length(Horizontal), l(mm):')
                self.parameterLabel_6.setText('Plate Length(Vertical), l*(mm):')
                self.parameterLabel_7.setText('Plate Thickness, t*(mm):') 
        elif(index_type==4):
            self.parameterLabel_2.hide()
            self.parameterText_2.hide()
            if(index_template==1):
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_1.setText('I-Section Type:')
                self.parameterLabel_3.hide()
                self.parameterText_3.hide()
                self.parameterLabel_6.setText('Length of Lips, P(mm):')
                self.parameterLabel_7.setText('Breadth of Lips, Q(mm):')
            elif(index_template==2):
                self.parameterLabel_4.hide()
                self.parameterText_4.hide()
                self.parameterLabel_1.setText('I-Section Type:')
                self.parameterLabel_3.setText('Spacing between flange of T to Web of I, S(mm):')
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_6.setText('Length of Web of T, d(mm):')
                self.parameterLabel_7.hide()
                self.parameterText_7.hide()
            elif(index_template==3):
                self.parameterLabel_6.hide()
                self.parameterText_6.hide()
                self.parameterLabel_7.hide()
                self.parameterText_7.hide()
                self.parameterLabel_5.hide()
                self.parameterText_5.hide()
                self.parameterLabel_1.setText('Hollow Section Type:')
                self.parameterLabel_3.setText('Spacing between the Tubes_Horizontal, S(mm):')
                self.parameterLabel_4.setText('Spacing between the Tubes_Vertical, S*(mm):')
        elif(index_type==5):
            self.parameterLabel_4.hide()
            self.parameterText_4.hide()
            self.parameterLabel_5.hide()
            self.parameterText_5.hide()
            self.parameterLabel_6.hide()
            self.parameterText_6.hide()
            self.parameterLabel_7.hide()
            self.parameterText_7.hide()
            self.parameterLabel_1.setText('I-Section Type:')
            self.parameterLabel_2.setText('Channel Section Type:')
            self.parameterLabel_3.setText('Spacing Between Channel and I-Section, S(mm):')

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
