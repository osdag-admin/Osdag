'''
Created on 09-Sep-2014

@author: deepa
'''
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox, qApp
import logging
import os
logger = None


def set_databaseconnection():
    '''
    Setting connection with SQLite
    '''
    # TODO explicitly close database connection on exit
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ResourceFiles', 'Database', 'Intg_osdag.sqlite')
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filepath)
    if not db.open():
        QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                   qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information "
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                   QMessageBox.Cancel)
        return False


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
    while (beamQuery.next()):
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

    while (designQuery.next()):
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
    columnQuery = QSqlQuery("SELECT Designation FROM Columns")
    comboList.append("Select section")
    while (columnQuery.next()):
        comboList.append(columnQuery.value(0))
    return comboList


def get_columndata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard column section properties.
    '''
    section = sect
    queryStr = "Select * from Columns where Designation = '%s'" % section
    designQuery = QSqlQuery(queryStr)
    retDict = {}
    record = designQuery.record()
    while (designQuery.next()):
        for i in range(0, record.count()):
            colName = record.fieldName(i)
            retDict[colName] = designQuery.value(i)
    return retDict


def get_anglecombolist():
    '''(None) -> (List)
    This function returns list of Indian Standard Angle Designation.
    '''
    comboList = []
    angleQuery = QSqlQuery("Select Designation from Angles")
    comboList.append("Select section")
    while (angleQuery.next()):
        comboList.append(angleQuery.value(0))
    return comboList


def get_angledata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Angle section properties.
    '''
    section = sect
    queryStr = "Select * from angles where Designation = '%s'" % section
    designQuery = QSqlQuery(queryStr)
    retDict = {}
    record = designQuery.record()

    while (designQuery.next()):
        for i in range(0, record.count()):
            angle_name = record.fieldName(i)
            retDict[angle_name] = designQuery.value(i)
    return retDict
