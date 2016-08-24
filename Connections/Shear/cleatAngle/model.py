'''
Created on 09-Sep-2014

@author: deepa
'''
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtSql import *
import logging
import os


# logging.basicConfig(filename = 'finlog.html',filemode = 'w',level = logging.DEBUG)
logger = None

def set_databaseconnection():
    '''
    Setting connection with SQLite
    '''
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ResourceFiles', 'Database', 'CleatSections')
#     filepath = "D:\EclipseWorkspace\OsdagWorkshop\Database\CleatSections"

#     db = QSqlDatabase.database("QSQLITE")
#     if db.IsValid():
#         return True
    
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filepath)
    # db.open()
    if not db.open():
        
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
               QtGui.qApp.tr("Unable to establish a database connection.\n"
                             "This example needs SQLite support. Please read "
                             "the Qt SQL driver documentation for information "
                             "how to build it.\n\n"
                             "Click Cancel to exit."),
               QtGui.QMessageBox.Cancel)
        return False   

    

# def set_databaseconnection():
#     '''
#     Setting connection with MySQL database
#     '''
#     db = QSqlDatabase.addDatabase("QMYSQL")
#     db.setHostName("localhost")
#     db.setPort(3306)
#     db.setDatabaseName("OSDAG")
#     db.setUserName("root")
#     db.setPassword("root")
#     db.open()
#     logger.info("feching records from database")
    
def module_setup():
    global logger 
    logger = logging.getLogger("osdag.model")
    set_databaseconnection()

def get_beamcombolist():
    '''(None) -> (List)
    This function returns list of Indian Standard Beam Designation.
    '''      
    comboList = []
    beamQuery = QSqlQuery("Select Designation from Beams")
    comboList.append("Select Designation")
    while(beamQuery.next()):
        comboList.append(beamQuery.value(0).toString())
    print "printing comboList"
    print comboList
    return comboList


def get_beamdata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Beam section properties.
    '''
    section = sect
   
    queryStr = "Select * from Beams where Designation = '%s'" % section
    
    designQuery = QSqlQuery(queryStr)
    print(designQuery)

    print designQuery.size()
    retDict = {}
    record = designQuery.record()
    
    while(designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i).toString()

    # print(retDict[QString("tw")])
    
    return retDict
    
def get_columncombolist():
    '''(None) -> (List)
    This function returns the list of Indian Standard Column Designation.
    '''      
    comboList = []
    columnQuery = QSqlQuery("SELECT Designation FROM Columns")
    comboList.append("Select Column")
    while(columnQuery.next()):
        comboList.append(columnQuery.value(0).toString())
    return comboList

def get_columndata(sect):

    '''(None) --> (Dictionary)
    This Function returns the Indian Standard column section properties.
    '''
    section = sect
    # section = Ui_MainWindow.comboColSec.currentText()
    queryStr = "Select * from Columns where Designation = '%s'" % section
    
    designQuery = QSqlQuery(queryStr)
    print(designQuery)
    
    print designQuery.size()
    retDict = {}
    record = designQuery.record()
    
    while(designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i).toString()
    
    return retDict

def get_anglecombolist():
    '''(None) -> (List)
    This function returns the list of Indian Standard Angles Designation.
    '''      
    comboList = []
    angleQuery = QSqlQuery("SELECT Designation FROM Angles ORDER BY A,B")
    comboList.append("Select Cleat")
    while(angleQuery.next()):
        comboList.append(angleQuery.value(0).toString())
    return comboList

def get_angledata(sect):
 
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Angle section properties.
    '''
    section = sect
#     section = Ui_MainWindow.comboColSec.currentText()
    queryStr = "Select * from Angles where Designation = '%s'" % section
     
    designQuery = QSqlQuery(queryStr)
    print(designQuery)
     
    print designQuery.size()
    retDict = {}
    record = designQuery.record()
     
    while(designQuery.next()):
        for i in range(0, record.count()):
            angleName = record.fieldName(i)
            retDict[angleName] = designQuery.value(i).toString()
    
    return retDict

# module_setup()
