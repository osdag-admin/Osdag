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
                                                 "the Qt SQL driver documentation for information "
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
    combo_list = []
    beam_query = QSqlQuery("Select Designation from Beams")
    combo_list.append("Select section")
    while(beam_query.next()):
        combo_list.append(beam_query.value(0))
    return combo_list


def get_beamdata(sect):
    '''(None) --> (Dictionary)
    This Function returns the Indian Standard Beam section properties.
    '''
    section = sect

    query_str = "Select * from Beams where Designation = '%s'" % section

    design_query = QSqlQuery(query_str)
    ret_dict = {}
    record = design_query.record()

    while(design_query.next()):
        for i in range(0, record.count()):
            col_name = record.fieldName(i)
            ret_dict[col_name] = design_query.value(i)

    # print(ret_dict[QString("tw")])

    return ret_dict

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
    combo_list = []
    column_query = QSqlQuery("SELECT Designation FROM Columns")
    combo_list.append("Select section")
    while(column_query.next()):
        combo_list.append(column_query.value(0))
    return combo_list


def get_columndata(sect):

    '''(None) --> (Dictionary)
    This Function returns the Indian Standard column section properties.
    '''
    section = sect
    # section = Ui_MainWindow.comboColSec.currentText()
    query_str = "Select * from Columns where Designation = '%s'" % section

    design_query = QSqlQuery(query_str)

    ret_dict = {}
    record = design_query.record()

    while(design_query.next()):
        for i in range(0, record.count()):
            col_name = record.fieldName(i)
            ret_dict[col_name] = design_query.value(i)

    return ret_dict

# module_setup()
