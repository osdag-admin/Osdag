'''
Created on 09-Sep-2014

@author: deepa
'''
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtSql import *
import logging, os

# logging.basicConfig(filename = 'finlog.html',filemode = 'w',level = logging.DEBUG)
logger = None


def set_databaseconnection():
    '''
    Setting connection with SQLite
    '''
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ResourceFiles', 'Database', 'CleatSections')
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filepath)
    db.open()
    if not db.open():
        QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                                   QtGui.qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information "
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                   QtGui.QMessageBox.Cancel)
        return False

        # logger.info("fetching records from database")


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
    while (beamQuery.next()):
        comboList.append(beamQuery.value(0).toString())
    # print "printing comboList"
    # print comboList
    return comboList


def get_beamdata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Beam section properties.
    '''
    section = sect

    queryStr = "Select * from Beams where Designation = '%s'" % section

    designQuery = QSqlQuery(queryStr)
    # print(designQuery)

    # print designQuery.size()
    retDict = {}
    record = designQuery.record()

    while (designQuery.next()):
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
    comboList.append("Select section")
    while (columnQuery.next()):
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

    retDict = {}
    record = designQuery.record()

    while (designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i).toString()

    return retDict


def get_anglecombolist():
    '''(None) -> (List)
    This function returns list of Indian Standard Angle Designation.
    '''
    comboList = []
    angleQuery = QSqlQuery("Select Designation from Angles")
    comboList.append("Select Designation")
    while (angleQuery.next()):
        comboList.append(angleQuery.value(0).toString())
    # print "printing comboList"
    # print comboList
    return comboList


def get_angledata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Angle section properties.
    '''
    section = sect

    queryStr = "Select * from angles where Designation = '%s'" % section

    designQuery = QSqlQuery(queryStr)
    # print(designQuery)
    #
    # print designQuery.size()
    retDict = {}
    record = designQuery.record()

    # TODO rework angle section name 
    while (designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i).toString()

    # print(retDict[QString("tw")])

    return retDict

    # module_setup()
