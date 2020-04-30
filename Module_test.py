import os
import errno
import yaml
import sys
import unittest

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
from design_type.connection.beam_end_plate import BeamEndPlate
from design_type.connection.column_cover_plate import ColumnCoverPlate
from design_type.connection.column_end_plate import ColumnEndPlate
from design_type.compression_member.compression import Compression






all_modules = {'Base Plate':BasePlateConnection, 'Beam Coverplate  Weld Connection':BeamCoverPlateWeld,'Beam Coverplate Connection':BeamCoverPlate,
    'Cleat Angle':CleatAngleConnection, 'Column Coverplate Weld Connection':ColumnCoverPlateWeld, 'Column Coverplate Connection':ColumnCoverPlate,
    'Column Endplate Connection':ColumnEndPlate, 'End Plate':EndPlateConnection, 'Fin Plate':FinPlateConnection,'Seated Angle': SeatedAngleConnection,
    'Tension Members Bolted Design':Tension_bolted, 'Tension Members Welded Design':Tension_welded, 'Compression Member':Compression,
    }


'''
Add more modules from all_modules dict to available_modules for testing or simply use all_modules dict if you want to run test for all modules.

available_module dictionary is used in -

                                    1. method 'runTest(self)' inside TestModules class.
                                    2. function 'suite()'.

Make sure to make the necessary changes in above functions/methods if you are changing the name of available_module.
'''

available_module = {'Column Coverplate Weld Connection': ColumnCoverPlateWeld}






Output_folder_name = 'Output_PDF'

#predefined pop-up summary.
popup_summary = {'ProfileSummary': {'CompanyName': 'LoremIpsum', 'CompanyLogo': '', 'Group/TeamName': 'LoremIpsum', 'Designer': 'LoremIpsum'},
                'ProjectTitle': 'Fossee', 'Subtitle': '', 'JobNumber': '123', 'AdditionalComments': 'No comments', 'Client': 'LoremIpsum'}


input_file_path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'design_example')   # input folder path

output_folder_path = os.path.join(os.path.dirname(__file__), Output_folder_name)               # output folder path






def make_sure_path_exists(path):      # Works on all OS.
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

make_sure_path_exists(output_folder_path)   #make sure output folder exists if not then create.






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
        error = main.func_for_validation(main,self,file_data)  # validating files and setting inputs (although we know files are valid).

        if error is None:  # if ran successfully and all input values are set without any error. Now create pdf

            '''


            In save_design function second argument is popup summary which user gives as an input.
            For testing purpose we are giving some default values for creating every pdf.
            We are actually not comparing pdf. This is just for testing purpose whether function
            is running fine and creating pdf or not.

            I have made some changes in save_design function. Instead of asking for output file
            location from save_design function it'll ask from 'save_inputSummary' function inside
            ui_summary_popup.py file immediately after getting popup inputs and send it to
            save_design function using the same dictionary in which popup inputs are present
            with key name as 'filename'.


            '''

            duplicate = output_folder_path         # Making duplicate so that original path doesn't change.
            duplicate = duplicate + '/' + file_name  # giving each output file it's corresponding input file name.
            popup_summary['filename'] = duplicate    # adding this key in popup_summary dict.
            main.save_design(main,popup_summary)  # calling the function.
            pdf_created = True   # if pdf created

        return pdf_created






class TestModules(unittest.TestCase):
    def __init__(self, input, output):
        super(TestModules, self).__init__()
        self.input = input
        self.output = output
        self.module = Modules()

    def runTest(self):

        file_name = self.input[0]
        file_data = self.input[1]
        file_class = available_module[file_data['Module']]               # check the class.
        ans = self.module.run_test(self.module,file_class,file_name, file_data)
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


    log_file = "test_log_file.txt"   # log file in which test results will be written.


    with open(log_file, 'w') as TEST_LOG_FILE:
        result = unittest.TextTestRunner(stream = TEST_LOG_FILE,verbosity=2).run(suite())     # Writing results to log file.



    with open(log_file, 'r') as content_file:
        content = content_file.read()

    '''
        Reading the log file to see the output on console rather than opening the log file to see the output.
        In actual test environment we won't need it.
    '''
    enablePrint()       # enable printing to print the test log.
    print(content)


    test_exit_code = int(not result.wasSuccessful())
    sys.exit(test_exit_code)                              # This step is important for travis CI if we want to show test case fail as build fail.
