'''
Created on Oct 25, 2016

@author: Jayant Patil
'''
import sys
import model
from PyQt5 import QtWidgets
from reportGenerator import save_html
import finPlateCalc, test_fin_plate_calc
import unittest
from model import get_columndata, get_beamdata

class TestReportGenerator(unittest.TestCase):
    """Test save_html function from reportGenerator.

    Note:
        Currently, does not automatically check the output report.
        Need to do it manually.
    """

    def setUp(self):
        """Create database connection.

        Args:
            None

        Returns:
            None
        """
        app = QtWidgets.QApplication(sys.argv)
        model.module_setup()

    def test_print_sample_ui_input_output(self):
        """Print sample UI input and sample UI output dictionaries.

           Args:
               None

           Returns:
               None
           """
        # print create_sample_ui_input()
        # print create_sample_ui_output()

    def test_save_html_report(self):
        """Save html report with dummy images in the views section.

        Args:
            None

        Returns:
            None
        """
        fp_connection_id_list = {
            1: "FP_0",
            2: "FP_2",
            3: "FP_3",
            4: "FP_4"
        }
        for connection_id in fp_connection_id_list.values():
            self.save_test_design_report(connection_id)


    def save_test_design_report(self, fp_connection_id):
        """Save html design report at hardcoded location.

        Args:
            report_summary (dict): Structural Engineer details for design report

        Returns:
            None

        Note:
            This function is similar to save_design in seat_angle_main.py except:
            It takes only report_summary as parameter and uses hardcoded values of other parameters.
        """
        fp_sample_ui_input = test_fin_plate_calc.create_sample_ui_input_fp(fp_connection_id)
        fp_sample_ui_output = finPlateCalc.finConn(fp_sample_ui_input)
        beam_section = fp_sample_ui_input['Member']['BeamSection']
        col_section = fp_sample_ui_input['Member']['ColumSection']
        dict_beam_data = model.get_beamdata(beam_section)
        dict_col_data = model.get_columndata(col_section)
        report_summary = self.create_sample_report_summary(fp_connection_id)
        folder_location = "F:\Osdag\Osdag\Osdag_Workspace\one\\"
        file_name = folder_location+"design_report_" + fp_connection_id + ".html"
        save_html(fp_sample_ui_output, fp_sample_ui_input, dict_beam_data, dict_col_data, report_summary, file_name, folder_location)

    def create_sample_report_summary(self, fp_connection_id):
        """Create and return hardcoded sample report_summary (dict).
    
        Args:
            None
    
        Returns:
            report_summary (dict): Structural Engineer details for design report
        """
        report_summary = {}
        report_summary["ProfileSummary"] = {}
        report_summary["ProfileSummary"]["CompanyName"] = "FOSSEE"
        report_summary["ProfileSummary"]["CompanyLogo"] = "IIT Bombay"
        report_summary["ProfileSummary"]["Group/TeamName"] = "Osdag"
        report_summary["ProfileSummary"]["Designer"] = "Jayant Patil"

        report_summary["ProjectTitle"] = "Connection modules development"
        report_summary["Subtitle"] = "Fin plate connection"
        report_summary["JobNumber"] = fp_connection_id
        report_summary["AdditionalComments"] = "Add more comments here."
        report_summary["Method"] = "Limit State Design (No Earthquake Load)"
        return report_summary
