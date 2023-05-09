import os
import errno
import yaml
import sys
import unittest
from pathlib import Path
import ast
import logging
is_travis = 'TRAVIS' in os.environ
############################ Pre-Build Database Updation/Creation #################
sqlpath = Path('ResourceFiles/Database/Intg_osdag.sql')
sqlitepath = Path('ResourceFiles/Database/Intg_osdag.sqlite')

if sqlpath.exists():
    if not sqlitepath.exists():
        cmd = 'sqlite3 ' + str(sqlitepath) + ' < ' + str(sqlpath)
        os.system(cmd)
        sqlpath.touch()
        print('Database Created')

    elif sqlitepath.stat().st_size == 0 or sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1:
        try:
            sqlitenewpath = Path('ResourceFiles/Database/Intg_osdag_new.sqlite')
            cmd = 'sqlite3 ' + str(sqlitenewpath) + ' < ' + str(sqlpath)
            error = os.system(cmd)
            print(error)
            # if error != 0:
            #      raise Exception('SQL to SQLite conversion error 1')
            # if sqlitenewpath.stat().st_size == 0:
            #      raise Exception('SQL to SQLite conversion error 2')
            os.remove(sqlitepath)
            sqlitenewpath.rename(sqlitepath)
            sqlpath.touch()
            print('Database Updated', sqlpath.stat().st_mtime, sqlitepath.stat().st_mtime)
        except Exception as e:
            sqlitenewpath.unlink()
            print('Error: ', e)

#########################################################################################
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
from design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
from design_type.connection.beam_column_end_plate import BeamColumnEndPlate
from design_type.connection.column_cover_plate import ColumnCoverPlate
from design_type.connection.column_end_plate import ColumnEndPlate
from design_type.compression_member.compression import Compression
from Common import *


if not is_travis:
    from cad.common_logic import CommonDesignLogic
    from texlive .Design_wrapper import init_display
    display, start_display, add_menu, add_function_to_menu = init_display(backend_str="qt-pyqt5")




all_modules = {'Base Plate':BasePlateConnection, 'Beam Coverplate  Weld Connection':BeamCoverPlateWeld,'Beam Coverplate Connection':BeamCoverPlate,
    'Cleat Angle':CleatAngleConnection, 'Column Coverplate Weld Connection':ColumnCoverPlateWeld, 'Column Coverplate Connection':ColumnCoverPlate,
    'Column Endplate Connection':ColumnEndPlate, 'End Plate':EndPlateConnection, 'Fin Plate':FinPlateConnection,'Seated Angle': SeatedAngleConnection,
    'Tension Members Bolted Design':Tension_bolted, 'Tension Members Welded Design':Tension_welded, 'Compression Member':Compression,
    }


'''
NOTE -> test cases are running on the modules available in available_module dict.

Add more modules from all_modules dict to available_modules for testing or simply use all_modules dict if you want to run test for all modules.

available_module dictionary is used in -

                                    1. method 'runTest(self)' inside TestModules class.
                                    2. function 'suite()'.

Make sure to make the necessary changes in above functions/methods if you are changing the name of available_module.
'''

available_module = {KEY_DISP_FINPLATE:FinPlateConnection,  KEY_DISP_ENDPLATE:EndPlateConnection,
                    KEY_DISP_SEATED_ANGLE:SeatedAngleConnection, KEY_DISP_CLEATANGLE:CleatAngleConnection,
                    KEY_DISP_BEAMCOVERPLATEWELD:BeamCoverPlateWeld,KEY_DISP_BEAMCOVERPLATE:BeamCoverPlate,
                    KEY_DISP_COLUMNCOVERPLATEWELD:ColumnCoverPlateWeld,KEY_DISP_COLUMNCOVERPLATE:ColumnCoverPlate,
                    KEY_DISP_TENSION_WELDED:Tension_welded,KEY_DISP_TENSION_BOLTED:Tension_bolted,
                    KEY_DISP_COLUMNENDPLATE:ColumnEndPlate,KEY_DISP_BASE_PLATE:BasePlateConnection,
                    KEY_DISP_BB_EP_SPLICE:BeamBeamEndPlateSplice, KEY_DISP_BCENDPLATE: BeamColumnEndPlate}

#predefined pop-up summary.
popup_summary = {'ProfileSummary': {'CompanyName': 'LoremIpsum', 'CompanyLogo': '', 'Group/TeamName':
    'LoremIpsum', 'Designer': 'LoremIpsum'},'ProjectTitle': 'Fossee', 'Subtitle': '', 'JobNumber': '123',
                 'AdditionalComments': 'No comments', 'Client': 'LoremIpsum'}




def make_sure_path_exists(path):      # Works on all OS.
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise



input_file_path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'design_example')   # input folder path

output_file_path = os.path.join(os.path.dirname(__file__), 'OUTPUT_FILES', 'Output_PDF')       # output folder path



make_sure_path_exists(output_file_path)   #make sure output folder exists if not then create.






osi_files = [file for file in os.listdir(input_file_path) if file.endswith(".osi")]    # get all osi files in input_file_path directory.

files_data = []   # list of tuples in which the first item will be file name and second item will be data of that file in dictionary format.

def precompute_data():

    for file in osi_files:

        in_file = input_file_path + '/' + file

        with open(in_file, 'r') as fileObject:

            uiObj = yaml.load(fileObject, yaml.Loader)

        files_data.append((file, uiObj))



class Modules:

    def run_test(self,mainWindow,main,file_name, file_data): # FinPlate test function . Similarly make functions for other Modules.

        pdf_created = False
        main.set_osdaglogger(None)
        error = main.func_for_validation(main,file_data)  # validating files and setting inputs (although we know files are valid).

        if error is None:  # if ran successfully and all input values are set without any error. Now create pdf

            '''


            In save_design function second argument is popup summary which user gives as an input.
            For testing purpose we are giving some default values for creating every pdf.
            We are actually not comparing pdf. This is just for testing purpose whether function
            is running fine and creating pdf or not.

            Some changes are made in save_design function. Instead of asking for output file
            location from save_design function it'll ask from 'save_inputSummary' function inside
            ui_summary_popup.py file immediately after getting popup inputs and send it to
            save_design function using the same dictionary in which popup inputs are present
            with key name as 'filename'.


            '''
            file_name = file_name.split(".")[0]

            path =  os.path.join(output_file_path, file_name)

            popup_summary['filename'] = path    # adding this key in popup_summary dict.

            popup_summary['does_design_exist'] = False

            try:

                commLogicObj = CommonDesignLogic(display, ' ', main.module, main.mainmodule)

                status = main.design_status

                commLogicObj.call_3DModel(status, main)

                fName = os.path.join(os.path.dirname(__file__),'ResourceFiles','images','3d.png')
                fName_front = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'images', 'front.png')
                fName_side = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'images', 'side.png')
                fName_top = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'images', 'top.png')
                file_extension = fName.split(".")[-1]

                if file_extension == 'png':

                    display.ExportToImage(fName)
                    display.View_Front()
                    display.FitAll()
                    display.ExportToImage(fName_front)
                    display.View_Top()
                    display.FitAll()
                    display.ExportToImage(fName_side)
                    display.View_Right()
                    display.FitAll()
                    display.ExportToImage(fName_top)

                display.EraseAll()

                popup_summary['does_design_exist'] = True

            except:

                pass

            with open(os.path.join(os.path.dirname(__file__),'logging_text.log'),'r') as LOG: # we are already creating this log file inside each module.
                to_write = LOG.read()

            popup_summary['logger_messages'] = to_write

            main.save_design(main,popup_summary)  # calling the function.

            pdf_created = True   # if pdf created

            is_dict_same = True
            '''
            path = os.path.join(os.path.dirname(__file__), 'OUTPUT_FILES', 'Command_line_output', file_name + ".txt")

            if os.path.isfile(path):

                with open(path,"r") as file_content:

                    content = file_content.read()

                content = ast.literal_eval(content)   # convert dictionary string to dictionary

                output_dict = main.results_to_test(main)

                if output_dict != content:

                    is_dict_same = False    # if dictionary is not equal.
            '''

        open(os.path.join(os.path.dirname(__file__),'logging_text.log'), 'w').close() # better to clear the file than removing the handlers. More efficient.
         # Remove the log handlers also if you don't want to see all the accumulated messages repeating each time.

        return (pdf_created & is_dict_same)



class TestModules(unittest.TestCase):
    def __init__(self, input, output):
        super(TestModules, self).__init__()
        self.input = input
        self.output = output
        self.module = Modules()

    def runTest(self):

        file_name = self.input[0]
        file_data = self.input[1]
        file_class = available_module[file_data['Module']]              # check the class.
        ans = self.module.run_test(self.module, file_class,file_name, file_data)
        self.assertTrue(ans is self.output)




def suite():

    suite = unittest.TestSuite()

    ''' Make changes in this line to add files in TestSuite for testing according to your need or available modules. '''

    suite.addTests(TestModules(item, True) for item in files_data if item[1]['Module'] in available_module)

    return suite




#Block print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__


if __name__ == '__main__':

    blockPrint()         # disable printing to avoid printing from unnecessary print statments in each modules. Although log statements can still print.
    precompute_data()    # precompute all data.

    open(os.path.join(os.path.dirname(__file__),'logging_text.log'), 'w').close()   # Clearing the log file for test module.

    log_file = "test_log_file.log"   # log file in which test results will be written.


    with open(log_file, 'w') as TEST_LOG_FILE:
        result = unittest.TextTestRunner(stream = TEST_LOG_FILE,verbosity=2).run(suite())     # Writing results to log file.


    with open(os.path.join(os.path.dirname(__file__),log_file), 'r') as content_file:
        content = content_file.read()

    '''
        Reading the log file to see the output on console rather than opening the log file to see the output.
        In actual test environment we won't need it.
    '''
    enablePrint()       # enable printing to print the test log.
    print(content)


    test_exit_code = int(not result.wasSuccessful())
    sys.exit(test_exit_code)                              # This step is important for travis CI if we want to show test case fail as build fail.
