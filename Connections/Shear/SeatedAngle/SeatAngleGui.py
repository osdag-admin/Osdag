'''
Created on 14-Aug-2015

@author: Jeffy
'''
'''
Created on 07-May-2015
comment

@author: Jeffy
'''
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QString, pyqtSignal
import logging
from Connections.Shear.SeatAngle.ui_SeatAngle import Ui_MainWindow
from model import *
from SeatAngleConsoleCalc import SeatAngleConn
import yaml
import pickle

import os.path

# Developed by Jeffy

class MainController(QtGui.QMainWindow):
    
    closed = pyqtSignal()
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.comboBeamSec.addItems(get_beamcombolist())
        self.ui.comboAngleSec.addItems(get_anglecombolist())      
        self.ui.comboColSec.addItems(get_columncombolist())
        
        self.ui.inputDock.setFixedSize(310,710)
        
        self.gradeType ={'Please Select Type':'',
                         'HSFG': [8.8,10.8],
                         'Black Bolt':[3.6,4.6,4.8,5.6,5.8,6.8,9.8,12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)
        
        
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        #self.retrieve_prevstate()
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        
#         self.ui.btn_front.clicked.connect(self.call_Frontview)
#         self.ui.btn_top.clicked.connect(self.call_Topview)
#         self.ui.btn_side.clicked.connect(self.call_Sideview)
#         
#         self.ui.btn3D.clicked.connect(lambda:self.call_3DModel(True))
#         self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
#         self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
#         self.ui.chkBxSeatAngle.clicked.connect(self.call_3DFinplate)
        
        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)
        
        dbl_validator = QtGui.QDoubleValidator()
#         self.ui.txtPlateLen.setValidator(dbl_validator)
#         self.ui.txtPlateLen.setMaxLength(7)
#         self.ui.txtPlateWidth.setValidator(dbl_validator)
#         self.ui.txtPlateWidth.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)
        
        minfuVal = 290
        maxfuVal = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu,self.ui.lbl_fu, minfuVal, maxfuVal))
        
        minfyVal = 165
        maxfyVal = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy,self.ui.lbl_fy, minfyVal, maxfyVal))
       
        ##### MenuBar #####
        self.ui.actionQuit_fin_plate_design.setShortcut('Ctrl+Q')
        self.ui.actionQuit_fin_plate_design.setStatusTip('Exit application')
        self.ui.actionQuit_fin_plate_design.triggered.connect(QtGui.qApp.quit)
        
        self.ui.actionCreate_design_report.triggered.connect(self.save_design)
        self.ui.actionSave_log_messages.triggered.connect(self.save_log)
        self.ui.actionEnlarge_font_size.triggered.connect(self.showFontDialogue)
#         self.ui.actionZoom_in.triggered.connect(self.callZoomin)
#         self.ui.actionZoom_out.triggered.connect(self.callZoomout)
#         self.ui.actionSave_3D_model_as.triggered.connect(self.save3DcadImages)
#         self.ui.actionSave_current_2D_image_as.triggered.connect(self.save2DcadImages)
#         self.ui.actionView_2D_on_ZX.triggered.connect(self.call_Frontview)
#         self.ui.actionView_2D_on_XY.triggered.connect(self.call_Topview)
#         self.ui.actionView_2D_on_YZ.triggered.connect(self.call_Sideview)
#         self.ui.actionPan.triggered.connect(self.call_Pannig)
        
        # self.ui.comboBeamSec.addItems(get_beamcombolist())
        # self.ui.comboColSec.addItems(get_columncombolist())
      
        
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.save_design)#Saves the create design report
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        
        
        # Saving and Restoring the finPlate window state.
        #self.retrieve_prevstate()
        
#         self.ui.btnZmIn.clicked.connect(self.callZoomin)
#         self.ui.btnZmOut.clicked.connect(self.callZoomout)
#         self.ui.btnRotatCw.clicked.connect(self.callRotation)
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        
        # Initialising the qtviewer
#         self.display,_ = self.init_display(backend_str="pyqt4")
        
#         self.ui.btnSvgSave.clicked.connect(self.save3DcadImages)
        #self.ui.btnSvgSave.clicked.connect(lambda:self.saveTopng(self.display))
        
        self.connectivity = None
        self.fuse_model = None
        self.disableViewButtons()
        
    def showFontDialogue(self):
        
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.ui.inputDock.setFont(font)
            self.ui.outputDock.setFont(font)
            self.ui.textEdit.setFont(font)
    
    def disableViewButtons(self):
        '''
        Disables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(False)
        self.ui.btn_top.setEnabled(False)
        self.ui.btn_side.setEnabled(False)
        
        self.ui.btn3D.setEnabled(False)
        self.ui.chkBxBeam.setEnabled(False)
        self.ui.chkBxCol.setEnabled(False)
        self.ui.chkBxSeatAngle.setEnabled(False)
    
    def enableViewButtons(self):
        '''
        Enables the all buttons in toolbar
        '''
        self.ui.btn_front.setEnabled(True)
        self.ui.btn_top.setEnabled(True)
        self.ui.btn_side.setEnabled(True)
        
        self.ui.btn3D.setEnabled(True)
        self.ui.chkBxBeam.setEnabled(True)
        self.ui.chkBxCol.setEnabled(True)
        self.ui.chkBxSeatAngle.setEnabled(True)
        
 
    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if(uiObj != None):
            self.ui.comboBeamSec.setCurrentIndex(self.ui.comboBeamSec.findText(uiObj['Member']['Beam section']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['Column section']))
            self.ui.comboAngleSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['Angle Section']))

             
            self.ui.txtFu.setText(str(uiObj['Member']['fu (MPa)']))
            self.ui.txtFy.setText(str(uiObj['Member']['fy (MPa)']))
            
            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['Connectivity'])))
             
            self.ui.txtShear.setText(str(uiObj['Load']['Shear force (kN)']))
             
            self.ui.comboDiameter.setCurrentIndex(self.ui.comboDiameter.findText(str(uiObj['Bolt']['Diameter (mm)'])))
            comboTypeIndex = self.ui.comboType.findText(str(uiObj['Bolt']['Type']))
            self.ui.comboType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['Type']))
             
            prevValue = str(uiObj['Bolt']['Grade'])
         
            comboGradeIndex = self.ui.comboGrade.findText(prevValue)
           
            self.ui.comboGrade.setCurrentIndex(comboGradeIndex)
         
        
    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web":
            
            pixmap = QtGui.QPixmap(":/newPrefix/images/beam2.jpg")
            pixmap.scaledToHeight(50)
            pixmap.scaledToWidth(60)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            #self.ui.lbl_connectivity.show()
        elif(loc == "Column web-Beam web"):
            picmap = QtGui.QPixmap(":/newPrefix/images/beam.jpg")
            picmap.scaledToHeight(50)
            picmap.scaledToWidth(60)
            self.ui.lbl_connectivity.setPixmap(picmap)
        else:
            self.ui.lbl_connectivity.hide()
            
        
    def getuser_inputs(self):
        '''(nothing) -> Dictionary
        
        Returns the dictionary object with the user input fields for designing fin plate connection
        
        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["Diameter (mm)"] = self.ui.comboDiameter.currentText().toInt()[0]
        uiObj["Bolt"]["Grade"] = float(self.ui.comboGrade.currentText())                                                                                                                                                                                                                                                              
        uiObj["Bolt"]["Type"] = str(self.ui.comboType.currentText())
        
        uiObj['Member'] = {}
        uiObj['Member']['BeamSection'] = str(self.ui.comboBeamSec.currentText())
        uiObj['Member']['ColumSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['Connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu (MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiObj['Member']['fy (MPa)'] = self.ui.txtFy.text().toInt()[0]
             
        uiObj['Load'] = {}
        uiObj['Load']['ShearForce (kN)'] = self.ui.txtShear.text().toInt()[0]
        
        uiObj['Angle'] = {}
        uiObj['Angle']['AngleSection'] = str(self.ui.comboAngleSec.currentText())
        
        return uiObj    
    
    def save_inputs(self,uiObj):
         
        '''(Dictionary)--> None
         
        '''
        inputFile = QtCore.QFile('saveINPUT.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        #yaml.dump(uiObj, inputFile,allow_unicode=True, default_flow_style = False)
        pickle.dump(uiObj, inputFile)
        
    
    def get_prevstate(self):
        '''
        '''
        fileName = 'saveINPUT.txt'
         
        if os.path.isfile(fileName):
            fileObject = open(fileName,'r')
            uiObj = pickle.load(fileObject)
            return uiObj
        else:
            return None
    
            
    def outputdict(self):
        
        ''' Returns the output of design in dictionary object.
        '''
        outObj = {}
        outObj['SeatAngle'] ={}
        outObj['SeatAngle']["Length (mm)"] = float(self.ui.txtSeatLength.text())
        outObj['SeatAngle']["Moment Demand (kNm)"] = float(self.ui.txtExtMomnt.text())
        outObj['SeatAngle']["Moment Capacity (kNm)"] = float(self.ui.txtMomntCapacity.text())
        outObj['SeatAngle']["Shear Demand (kN/mm)"] = float(self.ui.txtShearDemand.text())
        outObj['SeatAngle']["Shear Capacity (kN/mm)"] = float(self.ui.txtShearCapacity_2.text())
        outObj['SeatAngle']["Beam Shear Strength (kN/mm)"] = float(self.ui.txtBeamShearStrength.text())
         
        outObj['Bolt'] = {}
        outObj['Bolt']["Shear Capacity (kN)"] = float(self.ui.txtShearCapacity.text())
        outObj['Bolt']["Bearing Capacity (kN)"] = float(self.ui.txtBearingCapacity.text())
        outObj['Bolt']["Capacity Of Bolt (kN)"] = float(self.ui.txtBoltCapacity.text())
        outObj['Bolt']["Bolt group capacity (kN)"] = float(self.ui.txtBoltGroupCapacity.text())
        outObj['Bolt']["No Of Bolts"] = float(self.ui.txtNoBolts.text())
        outObj['Bolt']["No.Of Row"] = int(self.ui.txt_row.text())
        outObj['Bolt']["No.Of Column"] = int(self.ui.txt_col.text())
        outObj['Bolt']["Pitch Distance (mm)"] = float(self.ui.txtPitch.text())
        outObj['Bolt']["Guage Distance (mm)"] = float(self.ui.txtGuage.text())
        outObj['Bolt']["End Distance (mm)"]= float(self.ui.txtEndDist.text())
        outObj['Bolt']["Edge Distance (mm)"]= float(self.ui.txtEdgeDist.text())
        
        return outObj
    
    
    def save_design(self):
        self.outdict = self.outputdict()
        self.inputdict = self.getuser_inputs()
        self.save_yaml(self.outdict,self.inputdict)
    
        #self.save(self.outdict,self.inputdict)
        
    def save_log(self):
        
        fileName,pat =QtGui.QFileDialog.getSaveFileNameAndFilter(self,"Save File As","/home/jeffy/SaveMessages","Text files (*.txt)")
        return self.save_file(fileName+".txt")
          
    def save_file(self, fileName):
        '''(file open for writing)-> boolean
        '''
        fname = QtCore.QFile(fileName)
        
        if not fname.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (fileName, fname.errorString()))
            return False

        outf = QtCore.QTextStream(fname)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        #self.setCurrentFile(fileName);
        
        #QtGui.QMessageBox.about(self,'Information',"File saved")
       
    
    
    def save_yaml(self,outObj,uiObj):
        '''(dictiionary,dictionary) -> NoneType
        Saving input and output to file in following format.
        Bolt:
          diameter: 6
          grade: 8.800000190734863
          type: HSFG
        Load:
          shearForce: 100
          
        '''
        newDict = {"INPUT": uiObj, "OUTPUT": outObj} 
        fileName = QtGui.QFileDialog.getSaveFileName(self,"Save File As","/home/jeffy/SaveDesign","Text File (*.txt)")
        f = open(fileName,'w')
        yaml.dump(newDict,f,allow_unicode=True, default_flow_style=False)
        
        #return self.save_file(fileName+".txt")
        #QtGui.QMessageBox.about(self,'Information',"File saved")

        
    def resetbtn_clicked(self):
        '''(NoneType) -> NoneType
        
        Resets all fields in input as well as output window
    
        '''
        # user Inputs

        self.ui.comboDiameter.setCurrentIndex(0)
        self.ui.comboGrade.setCurrentIndex(0)                                                                                                                                                                                                                                                              
        self.ui.comboType.setCurrentIndex(0)
        
        self.ui.comboBeamSec.setCurrentIndex(0)
        self.ui.comboColSec.setCurrentIndex(0)
        self.ui.comboConnLoc.setCurrentIndex(0)
        self.ui.txtFu.clear()
        self.ui.txtFy.clear()
             
        self.ui.txtShear.clear()
        
        self.ui.comboAngleSec.setCurrentIndex(0)
        
        
        #----Output
           
        self.ui.txtSeatLength.clear()
        self.ui.txtExtMomnt.clear()
        self.ui.txtMomntCapacity.clear()
        self.ui.txtShearDemand.clear()
        self.ui.txtShearCapacity.clear()
        self.ui.txtBeamShearStrength.clear()
         
        self.ui.txtShrCapacity_2.clear()
        self.ui.txtBearingCapacity.clear()
        self.ui.txtBoltCapacity.clear()
        self.ui.txtBoltGroupCapacity.clear()
        self.ui.txtNoBolts.clear()
        self.ui.txt_row.clear()
        self.ui.txt_col.clear()
        self.ui.txtPitch.clear()
        self.ui.txtGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()
        
        #------ Erase Display
        self.display.EraseAll()
        
    def dockbtn_clicked(self,widget):
        
        '''(QWidget) -> NoneType
        
        This method dock and undock widget(QdockWidget)
        '''
        
        flag = widget.isHidden()
        if(flag):
            
            widget.show()
        else:
            widget.hide()
            
    def  combotype_currentindexchanged(self,index):
        
        '''(Number) -> NoneType
        '''
        items = self.gradeType[str(index)]

        self.ui.comboGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))
            
        self.ui.comboGrade.addItems(strItems)
        
        
    def check_range(self, widget,lblwidget, minVal, maxVal):
        
        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr) 
        if( val < minVal or val > maxVal):
            QtGui.QMessageBox.about(self,'Error','Please Enter a value between %s-%s' %(minVal, maxVal))
            widget.clear()
            widget.setFocus()
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QtGui.QPalette()
            lblwidget.setPalette(palette)
            
    def display_output(self, outputObj):
        '''(dictionary) --> NoneType
        Setting design result values to the respective textboxes in the output window
        '''
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                if (outputObj[k][key] == ""):
                    resultObj = outputObj
                else:
                    resultObj = outputObj
                    
        # resultObj['Bolt']
        bolt_shear_capacity = resultObj['Bolt']['Shear Capacity (kN)']
        self.ui.txtShearCapacity.setText(str(bolt_shear_capacity))
        
        bearing_capacity = resultObj['Bolt']['Bearing Capacity (kN)']
        self.ui.txtBearingCapacity.setText(str(bearing_capacity))
        
        bolt_capacity = resultObj['Bolt']['Capacity Of Bolt (kN)']
        self.ui.txtBoltCapacity.setText(str(bolt_capacity))
        
        no_ofbolts = resultObj['Bolt']['No Of Bolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        #newly added field
        boltGrp_capacity = resultObj['Bolt']['Bolt group capacity (kN)']
        self.ui.txtBoltGroupCapacity.setText(str(boltGrp_capacity))
        
        no_ofrows = resultObj['Bolt']['No.Of Row']
        self.ui.txt_row.setText(str(no_ofrows))
         
        no_ofcol = resultObj['Bolt']['No.Of Column']
        self.ui.txt_col.setText(str(no_ofcol))
        
        pitch_dist = resultObj['Bolt']['Pitch Distance (mm)']
        self.ui.txtPitch.setText(str(pitch_dist))
        
        gauge_dist = resultObj['Bolt']['Guage Distance (mm)']
        self.ui.txtGuage.setText(str(gauge_dist))
        
        end_dist = resultObj['Bolt']['End Distance (mm)']
        self.ui.txtEndDist.setText(str(end_dist))
#
        edge_dist = resultObj['Bolt']['Edge Distance (mm)']
        self.ui.txtEdgeDist.setText(str(edge_dist))
        
        angle_length = resultObj['SeatAngle']['Length (mm)']
        self.ui.txtSeatLength.setText(str(angle_length))
        
        moment_demand = resultObj['SeatAngle']['Moment Demand (kNm)']
        self.ui.txtExtMomnt.setText(str(moment_demand))
        
        moment_capacity = resultObj['SeatAngle']['Moment Capacity (kNm)']
        self.ui.txtMomntCapacity.setText(str(moment_capacity))
        
        shear_demand = resultObj['SeatAngle']['Shear Demand (kN/mm)']
        self.ui.txtShearDemand.setText(str(shear_demand))
        
        angle_shear_capacity = resultObj['SeatAngle']['Shear Capacity (kN/mm)']
        self.ui.txtShearCapacity_2.setText(str(angle_shear_capacity))
        
        beam_shear_strength = resultObj['SeatAngle']['Beam Shear Strength (kN/mm)']
        self.ui.txtBeamShearStrength.setText(str(beam_shear_strength))
        
        
    def displaylog_totextedit(self):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''
        
        afile = QtCore.QFile('./seatangle.log')
        
        if not afile.open(QtCore.QIODevice.ReadOnly):#ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())
        
        stream = QtCore.QTextStream(afile)
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        vscrollBar = self.ui.textEdit.verticalScrollBar();
        vscrollBar.setValue(vscrollBar.maximum());
        afile.close()
        
        
   
    def fetchBeamPara(self):
        beam_sec = self.ui.comboBeamSec.currentText()
        dictbeamdata  = get_beamdata(beam_sec)
        return dictbeamdata
    
    def fetchColumnPara(self):
        column_sec = self.ui.comboColSec.currentText()
        dictcoldata = get_columndata(column_sec)
        return dictcoldata
    
    def fetchAnglePara(self):
        angle_sec = self.ui.comboAngleSec.currentText()
        dictangledata = get_angledata(angle_sec)
        return dictangledata
    
        
    def design_btnclicked(self):
        '''
        '''
        self.ui.outputDock.setFixedSize(310,710)
        self.enableViewButtons()
        
        #self.set_designlogger()
        # Getting User Inputs.
        uiObj = self.getuser_inputs()
        
        # Seat Angle Connection Design Calculations. 
        resultObj = SeatAngleConn(uiObj)
        
        # Displaying Design Calculations To Output Window
        self.display_output(resultObj)
        
        # Displaying Messages related to Seat Angle Design.
        self.displaylog_totextedit()

   
    def closeEvent(self, event):
        '''
        Closing Seat Angle window.
        '''
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.closed.emit()
            event.accept()
        else:
            event.ignore() 

                        
def set_osdaglogger():
    
    logger = logging.getLogger("osdag")
    logger.setLevel(logging.DEBUG)
 
    # create the logging file handler
    fh = logging.FileHandler("./seatangle.log", mode="a")
    
    #,datefmt='%a, %d %b %Y %H:%M:%S'
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    formatter = logging.Formatter('''
    <div  class="LOG %(levelname)s">
        <span class="DATE">%(asctime)s</span>
        <span class="LEVEL">%(levelname)s</span>
        <span class="MSG">%(message)s</span>
    </div>''')
    formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    
def launchSeatAngleController(osdagMainWindow):
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("./seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="./log.css"/>''')
     
    #app = QtGui.QApplication(sys.argv)
    window = MainController()
    osdagMainWindow.hide()
     
    window.show()
    window.closed.connect(osdagMainWindow.show)
     
    #sys.exit(app.exec_())
    
    

if __name__ == '__main__':
    #launchSeatAngleController(None)
       
    # linking css to log file to display colour logs.
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("seatangle.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')
       
    app = QtGui.QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())





