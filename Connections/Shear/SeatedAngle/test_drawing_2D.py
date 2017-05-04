import unittest
import sys
import model
from PyQt4 import QtGui
from seat_angle_calc import SeatAngleCalculation
from test_seat_angle_calc import create_sample_ui_input_sa
from test_seat_angle_calc import create_sample_ui_output_sa
import svgwrite
from PyQt4.QtCore import QString
import cairosvg
from drawing_2D import SeatCommonData, Seat2DCreatorFront, Seat2DCreatorSide, Seat2DCreatorTop

is_test_for_all = False


class TestSeatCommonData(unittest.TestCase, SeatCommonData):
    """Test SeatCommonData Class functions.

    Attributes:
        (inherited)

    Note:
        Currently, can not automatically check and verify the accuracy of the output drawings.
        This needs to be done manually.
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
        sa_sample_ui_input = create_sample_ui_input_sa()
        self.sa_calc_obj.seat_angle_connection(sa_sample_ui_input )

    def test_print_sample_ui_input_output(self):
        """Print sample UI input and sample UI output dictionaries.

           Args:
               None

           Returns:
               None
           """
        # print create_sample_ui_input()
        # print create_sample_ui_output()

    def test_save_drawing_common(self):
        """Check common functions in drawing.

        Args:
            None

        Returns:
            None
        """
        self.save_images_hardcoded("test_image","sideView")
        pass

    def save_images_hardcoded(self, file_name, view):
        """Save svg images at hardcoded location.

        Args:
            report_summary (dict): Structural Engineer details for design report

        Returns:
            None

        Note:
            This function is similar to save_design in seat_angle_main.py except:
            It takes only report_summary as parameter and uses hardcoded values of other parameters.
        """
        output_dict = create_sample_ui_output_sa()
        input_dict = create_sample_ui_input_sa()
        model.module_setup()
        model_beam_data = model.get_beamdata(input_dict["Member"]["BeamSection"])
        model_column_data = model.get_columndata(input_dict["Member"]["ColumnSection"])
        folder_location = "F:\Osdag\Osdag\Osdag_Workspace\one\\"
        base = "3D_ModelFinFB.png"
        base_front = "finFrontFB.svg"
        base_top = "finSideFB.svg"
        base_side = "finTopFB.svg"
        seat_common_instance = SeatCommonData(input_dict, output_dict, model_beam_data, model_column_data, folder_location)
        # base_front, base_top, base_side = seat_common_instance.save_to_svg(str(file_name), "Front")
        # base_front, base_top, base_side = seat_common_instance.save_to_svg(str(file_name), "Side")
        # base_front, base_top, base_side = seat_common_instance.save_to_svg(str(file_name), "Top")
        # base_front, base_top, base_side = seat_common_instance.save_to_svg(str(file_name), "All")

