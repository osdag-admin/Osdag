'''
Only difference between Unitest.py and Multitest.py file is Multitest uses for loop to run each file
whereas unitest has a unique function for each file.

Now if we have fixed number of test files it's better to use Unitest if we want to find out which file
is failing the test case. It'll show  name of the function which is failing the test case and from there
we can traceback the filename(coz we know which function is running which input file).

But using Multitest we can't traceback which file is failing coz it's running in for loop. It'll just show
the number of test cases failed and passed.

This file is dynamic it means we doesn't have to worry about number of input files.
'''

import yaml
from design_type.connection.fin_plate_connection import FinPlateConnection
import unittest
import os
import sys


fname_no_ext = 'C:/Users/nitin/Desktop/PDF_output/'  # Output pdf location. Change it according to your need.

# Predefined pop-up summary.
popup_summary = {'ProfileSummary': {'CompanyName': 'LoremIpsum', 'CompanyLogo': '', 'Group/TeamName': 'LoremIpsum', 'Designer': 'LoremIpsum'},
                'ProjectTitle': 'Fossee', 'Subtitle': '', 'JobNumber': '123', 'AdditionalComments': 'No comments', 'Client': 'LoremIpsum'}


path = 'C:/Users/nitin/Desktop/FOSSEE/Osdag3/ResourceFiles/design_example/'  ## path of input files

files = os.listdir(path)  # get all files in input files directory




###################    BEGIN  -  FOR FINPLATE FILES   ##################



list_of_dict_finplate = []   # List of tuples. In each tuple first item is file name and second item is file data


''' We are also storing file name here and tuple would look like (filename, file_data)
    We will need this file name for testing purpose and giving each output pdf it's corresponding
    input file name.

    We can't traceback the file name here.
'''


def read_finplate_files():
        for file in files:
            if 'fin_' in file:                      # if file name contains fin_ (not specific change it according to need).
                raw_file_name = file.split('.')[0]  # File name without extension
                file_name = file                    # File name with extension
                in_file = path + file_name
                with open(in_file, 'r') as fileObject:
                    uiObj = yaml.load(fileObject)
                list_of_dict_finplate.append((raw_file_name, uiObj))



###################    END - FOR FINPLATE FILES   ##################



class Modules:

    def Finplate_test(self,mainWindow,main,file_name, file_data): # FinPlate test function . Similarly make functions for other Modules.

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

            duplicate = fname_no_ext         # Making duplicate so that original path doesn't change.
            duplicate = duplicate + file_name  # giving each output file it's corresponding input file name.
            popup_summary['filename'] = duplicate    # adding this key in popup_summary dict.
            main.save_design(main,popup_summary)  # calling the function.
            pdf_created = True   # if pdf created

        return pdf_created



class TestModules(unittest.TestCase):
    def __init__(self, input, output):
        super(TestModules, self).__init__()
        self.input = input
        self.output = output
        self.finplate = Modules()

    def runTest(self):

        file_name = self.input[0]
        file_data = self.input[1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is self.output)



def suite():
    suite = unittest.TestSuite()
    suite.addTests(TestModules(list_of_dict_finplate[i], True) for i in range(len(list_of_dict_finplate)))
    return suite


if __name__ == '__main__':

    read_finplate_files()  # precomputing all finplate data

    result = unittest.TextTestRunner(verbosity=2).run(suite())


    ''' Uncomment it if you want to see the exit Status of the test.'''
    #test_exit_code = int(not result.wasSuccessful())
    #print('Exit Status Code is : ',test_exit_code)
