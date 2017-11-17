"""
Created on 29-Sept-2017

@author: Reshma
"""
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox, qApp
import logging
import os

logger = None


def set_databaseconnection():
    """

    Returns:  Setting connection with SQLite


    """
    filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'ResourceFiles', 'Database', 'Intg_osdag.sqlite')
    print filepath, "database"
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filepath)
    if not db.open():

        QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                   qApp.tr("Unable to establish a database connection.\n"
                                                 "This example needs SQLite support. Please read "
                                                 "the Qt SQL driver documentation for information"
                                                 "how to build it.\n\n"
                                                 "Click Cancel to exit."),
                                   QMessageBox.Cancel)
        return False


def module_setup():
    global logger
    logger = logging.getLogger("osdag.model")
    set_databaseconnection()


def get_channelcombolist():
    """

    Returns: This function returns the list of Indian Standard Channel Designation

    """
    comboList = []
    channelQuery = QSqlQuery("Select Designation from Channels")
    comboList.append("Select section")
    while(channelQuery.next()):
        comboList.append(channelQuery.value(0))
    return comboList


def get_channeldata(sect):
    """

    Args:
        sect: section properties

    Returns: This function returns the Indian Standard Channel section properties

    """
    section = sect
    queryStr = "SELECT * FROM Channels where Designation = '%s'" % section
    designQuery = QSqlQuery(queryStr)
    retDict = {}
    record = designQuery.record()

    while(designQuery.next()):
        for i in range(0, record.count()):
            colName =  record.fieldName(i)
            retDict[colName] = designQuery.value(i)

    return retDict

def get_equalanglecombolist():
    """

    Returns: This function returns the list of Indian Standard Equal Angle Designation

    """
    comboList = []
    equalangleQuery = QSqlQuery("Select Designation from EqualAngle")
    comboList.append("Select section")

    while equalangleQuery.next():
        comboList.append(equalangleQuery.value(0))
    return comboList


def get_equalangledata(sect):
    """

    Args:
        sect: section properties

    Returns: This function returns the Indian Standard Equal Angle section properties

    """
    section = sect
    queryStr = "SELECT * FROM EqualAngle where Designation = '%s'" % section
    designQuery = QSqlQuery(queryStr)
    retDict = {}
    record = designQuery.record()

    while(designQuery.next()):
        for i in range(0, record.count()):
            colName =  record.fieldName(i)
            retDict[colName] = designQuery.value(i)

    return retDict



def get_unequalanglecombolist():
    """

    Returns: This function returns the list of Indian Standard Unequal Angle Designation

    """
    comboList = []
    unequalangleQuery = QSqlQuery("SELECT Designation FROM UnequalAngle")
    comboList.append("Select section")
    while(unequalangleQuery.next()):
        comboList.append(unequalangleQuery.value(0))
    return comboList


def get_unequalangledata(sect):
    """

    Args:
        sect: section properties

    Returns: This function returns the Indian Standard Unequal Angle section properties

    """
    section = sect
    queryStr = "SELECT * FROM UnequalAngle where Designation = '%s'" % section
    designQuery = QSqlQuery(queryStr)
    retDict = {}
    record = designQuery.record()

    while(designQuery.next()):
        for i in range(0, record.count()):
            colName =  record.fieldName(i)
            retDict[colName] = designQuery.value(i)

    return retDict



