'''
Only difference between Unitest.py and Multitest.py file is Multitest uses for loop to run each file
whereas unitest has a unique function for each file.

Now if we have fixed number of test files it's better to use Unitest if we want to find out which file
is failing the test case. It'll show  name of the function which is failing the test case and from there
we can traceback the filename(coz we know which function is running which input file).

But using Multitest we can't traceback which file is failing coz it's running in for loop. It'll just show
the number of test cases failed and passed.

Multitest.py is dynamic so we doesn't have to worry about number of input files.
'''

import yaml
from design_type.connection.fin_plate_connection import FinPlateConnection
import unittest
import os

fname_no_ext = 'C:/Users/nitin/Desktop/PDF_output/'  # Output pdf location. Change it according to your need.

# Predefined pop-up summary.
popup_summary = {'ProfileSummary': {'CompanyName': 'LoremIpsum', 'CompanyLogo': '', 'Group/TeamName': 'LoremIpsum', 'Designer': 'LoremIpsum'},
                'ProjectTitle': 'Fossee', 'Subtitle': '', 'JobNumber': '123', 'AdditionalComments': 'No comments', 'Client': 'LoremIpsum'}


path = 'C:/Users/nitin/Desktop/FOSSEE/Osdag3/ResourceFiles/design_example/'  ## path of input files

files = os.listdir(path)  # get all files in input files directory




###################    BEGIN  -  FOR FINPLATE FILES   ##################



list_of_dict_finplate = []   # List of tuples. In each tuple first item is file name and second item is file data


''' We are also storing file name here so the tuple would look like (filename, file_data)
    We will need this file name for testing purpose and giving each output pdf it's corresponding
    input file name.

    We can also traceback the file name which is failing the test. Suppose the function which failed
    the test case is test_9, it means file is located at 9th index in the list(list_of_dict_finplate)
    and therefore we can access the file name with list_of_dict_finplate[9][0].
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





class TestClass_for_FinPlate(unittest.TestCase):  # Similarly make other classes for other modules

    finplate = Modules()

    # Make the number of functions equal to number of input files.

    def test_0(self):

        file_name = list_of_dict_finplate[0][0]   #index 0
        file_data = list_of_dict_finplate[0][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_1(self):

        file_name = list_of_dict_finplate[1][0]   #index 1
        file_data = list_of_dict_finplate[1][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_2(self):

        file_name = list_of_dict_finplate[2][0]   #index 2
        file_data = list_of_dict_finplate[2][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_3(self):

        file_name = list_of_dict_finplate[3][0]   #index 3
        file_data = list_of_dict_finplate[3][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_4(self):

        file_name = list_of_dict_finplate[4][0]   #index 4
        file_data = list_of_dict_finplate[4][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_5(self):

        file_name = list_of_dict_finplate[5][0]   #index 5
        file_data = list_of_dict_finplate[5][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_6(self):

        file_name = list_of_dict_finplate[6][0]   #index 6
        file_data = list_of_dict_finplate[6][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_7(self):

        file_name = list_of_dict_finplate[7][0]   #index 7
        file_data = list_of_dict_finplate[7][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_8(self):

        file_name = list_of_dict_finplate[8][0]   #index 8
        file_data = list_of_dict_finplate[8][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_9(self):

        file_name = list_of_dict_finplate[9][0]   #index 9
        file_data = list_of_dict_finplate[9][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_10(self):

        file_name = list_of_dict_finplate[10][0]   #index 10
        file_data = list_of_dict_finplate[10][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_11(self):

        file_name = list_of_dict_finplate[11][0]   #index 11
        file_data = list_of_dict_finplate[11][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_12(self):

        file_name = list_of_dict_finplate[12][0]   #index 12
        file_data = list_of_dict_finplate[12][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_13(self):

        file_name = list_of_dict_finplate[13][0]   #index 13
        file_data = list_of_dict_finplate[13][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created

    def test_14(self):

        file_name = list_of_dict_finplate[14][0]   #index 14
        file_data = list_of_dict_finplate[14][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created


    def test_15(self):

        file_name = list_of_dict_finplate[15][0]   #index 15
        file_data = list_of_dict_finplate[15][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created


    def test_16(self):

        file_name = list_of_dict_finplate[16][0]   #index 16
        file_data = list_of_dict_finplate[16][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created


    def test_17(self):

        file_name = list_of_dict_finplate[17][0]   #index 17
        file_data = list_of_dict_finplate[17][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created


    def test_18(self):

        file_name = list_of_dict_finplate[18][0]   #index 18
        file_data = list_of_dict_finplate[18][1]
        ans = self.finplate.Finplate_test(self.finplate,FinPlateConnection,file_name, file_data)

        self.assertTrue(ans is True)    #check if pdf created




if __name__ == '__main__':

    read_finplate_files()  # precomputing all finplate data

    unittest.main()  # run test
