'''
Created on Oct 25, 2016

@author: Jayant Patil
'''
import sys
import model
from PyQt5 import QtWidgets
from design_report_generator import ReportGenerator
from seat_angle_calc import SeatAngleCalculation
import test_seat_angle_calc
import unittest
import logging
import seat_angle_main


# logger = logging.getLogger("osdag.SeatAngleCalc")

class TestReportGenerator(unittest.TestCase, ReportGenerator):
    """Test ReportGenerator Class functions.

    Attributes:
        (inherited)

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
        model.set_databaseconnection()

    def test_save_html_report(self):
        """Save html report with dummy images in the views section.

        Args:
            None

        Returns:
            None
        """
        sa_connection_id_list = {
            1: "SA_0",
            2: "SA_2",
            3: "SA_3",
            4: "SA_4",
            5: "SA_6"
        }
        for connection_id in sa_connection_id_list.values():
            self.save_test_design_report(connection_id)

    def save_test_design_report(self, sa_connection_id):
        """Save html design report at hardcoded location.

        Args:
            report_summary (dict): Structural Engineer details for design report

        Returns:
            None

        Note:
            This function is similar to save_design in seat_angle_main.py except:
            It takes only report_summary as parameter and uses hardcoded values of other parameters.
        """

        sa_sample_ui_input = test_seat_angle_calc.create_sample_ui_input_sa(sa_connection_id=sa_connection_id)
        sa_calc_obj = SeatAngleCalculation()
        sa_calc_obj.seat_angle_connection(sa_sample_ui_input)
        report_summary = self.create_sample_report_summary(sa_connection_id)
        folder_location = "F:\Osdag_workspace\seated_angle\one\\"  # Add dummy images of views here.
        file_name = folder_location + "design_report_" + sa_connection_id + ".html"
        report_generator_instance = ReportGenerator(sa_calc_obj)
        report_generator_instance.save_html(report_summary, file_name,
                                            folder_location)

    def create_sample_report_summary(self, sa_connection_id):
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
        report_summary["Subtitle"] = "Seated angle connection"
        report_summary["JobNumber"] = sa_connection_id
        report_summary["Client"] = "Osdag Reviewer"
        report_summary["AdditionalComments"] = "Add more comments here."
        report_summary["Method"] = "Limit State Design (No Earthquake Load)"
        return report_summary
