'''
Created on 09-Sep-2014

@author: deepa
'''
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox, qApp
import logging
import os

# logging.basicConfig(filename = 'finlog.html',filemode = 'w',level = logging.DEBUG)

logger = None


def set_databaseconnection():
    '''
    Setting connection with SQLite
    '''
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ResourceFiles', 'Database', 'Intg_osdag.sqlite')
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filepath)
    # db.open()
    if not db.open():

        QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                   qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information"
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                   QMessageBox.Cancel)
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
    comboList.append("Select section")
    while(beamQuery.next()):
        comboList.append(beamQuery.value(0))
    return comboList


def get_beamdata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Beam section properties.
    '''
    section = sect

    queryStr = "Select * from Beams where Designation = '%s'" % section

    designQuery = QSqlQuery(queryStr)

    retDict = {}
    record = designQuery.record()

    while(designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i)

    return retDict

def get_oldbeamcombolist():
    '''(None) -> (List)
    This function returns the list of Indian Standard Column Designation.
    '''
    old_columnList = []
    columnQuery = QSqlQuery("SELECT Designation FROM Beams where Source = 'IS808_Old' order by id ASC")
    a = columnQuery.size()

    while(columnQuery.next()):
        old_columnList.append(columnQuery.value(0))

    return old_columnList


def get_oldcolumncombolist():
    '''(None) -> (List)
    This function returns the list of Indian Standard Column Designation.
    '''
    old_columnList = []
    columnQuery = QSqlQuery("SELECT Designation FROM Columns where Source = 'IS808_Old' order by id ASC")
    a = columnQuery.size()

    #comboList.append("Select section")
    while(columnQuery.next()):
        old_columnList.append(columnQuery.value(0))

    return old_columnList


def get_columncombolist():
    '''(None) -> (List)
    This function returns the list of Indian Standard Column Designation.
    '''
    comboList = []
    columnQuery = QSqlQuery("SELECT Designation FROM Columns order by id ASC")
    a = columnQuery.size()

    comboList.append("Select section")
    while(columnQuery.next()):
        comboList.append(columnQuery.value(0))
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

    while(designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i)

    return retDict

# module_setup()
