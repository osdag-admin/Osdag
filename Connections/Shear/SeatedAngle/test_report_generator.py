'''
Created on Oct 25, 2016

@author: Jayant Patil
'''
import time
import math
import sys
import model
from PyQt4 import QtGui
from report_generator import ReportGenerator
from seat_angle_calc import SeatAngleCalculation
from test_seat_angle_calc import create_sample_ui_input
from test_seat_angle_calc import create_sample_ui_output
from seat_angle_calc import SeatAngleCalculation
import unittest
import os

class TestReportGenerator(unittest.TestCase, ReportGenerator):
    """Test ReportGenerator Class functions.

    Attributes:
        (inherited)

    Note:
        Currently, does not automatically check the output report.
        Need to do it manually.
        An object can access the calculation parameters as attributes of
        the instance (sa_calc_obj) of SeatAngleCalculation; which itself
        is an attribute of this class.
    """

    def setUp(self):
        """Create database connection and instantiate sa_calculation object.

        Args:
            None

        Returns:
            None
        """
        app = QtGui.QApplication(sys.argv)
        model.module_setup()
        self.sa_calc_obj = SeatAngleCalculation()
        sa_sample_ui_input = create_sample_ui_input()
        self.sa_calc_obj.seat_angle_connection(sa_sample_ui_input )
        self.report_summary = create_sample_report_summary()

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
        self.save_design_hardcoded(self.report_summary)

    def save_design_hardcoded(self, report_summary):
        """Save html design report at hardcoded location.

        Args:
            report_summary (dict): Structural Engineer details for design report

        Returns:
            None

        Note:
            This function is similar to save_design in seat_angle_main.py except:
            It takes only report_summary as parameter and uses hardcoded values of other parameters.
        """
        output_dict = create_sample_ui_output()
        input_dict = create_sample_ui_input()
        file_name = "design_report.html"
        folder_location = "F:\Osdag\Osdag\Osdag_Workspace\one\\"
        base = "3D_ModelFinFB.png"
        base_front = "finFrontFB.svg"
        base_top = "finSideFB.svg"
        base_side = "finTopFB.svg"

        report_generator_instance = ReportGenerator(self.sa_calc_obj)
        report_generator_instance.save_html(output_dict, input_dict, report_summary, folder_location+file_name,
                                            folder_location, base,
                                            base_front, base_top, base_side)


def create_sample_report_summary():
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

    report_summary["ProjectTitle"] = "Connections Module Development"
    report_summary["Subtitle"] = "Seated Angle Development"
    report_summary["JobNumber"] = "SA001"
    report_summary["AdditionalComments"] = "Add more comments here."
    report_summary["Method"] = "Limit State Design (No Earthquake Load)"
    return report_summary
