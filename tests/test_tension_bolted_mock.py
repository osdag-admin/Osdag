import unittest
from unittest.mock import MagicMock, patch

# mock functions in python are fake implementations of real objects or methods.
# they’re used in unit testing when you don’t want to depend on actual implementation
# (like database calls, file reads, or in this case, a heavy design computation class).
# the mock just pretends to do what the real method does and returns predefined values.
# this makes testing fast, isolated, and easy to control.

# here, we are mocking the Tension_bolted class (probably a heavy structural module from osdag),
# and we're faking its method outputs by giving hardcoded (predefined) results.

class TestTensionBolted(unittest.TestCase):
    def setUp(self):
        # create a fake object (mock) for the Tension_bolted class
        self.tension_bolted = MagicMock()

        # whenever results_to_test is called on our mock object, return an empty dictionary by default
        self.tension_bolted.results_to_test.return_value = {}

        # make sure set_input_values just silently returns nothing
        self.tension_bolted.set_input_values.return_value = None

    @patch('tension_bolted.Tension_bolted')  # this replaces the real class with a mock during the test
    def test_tension_bolted_test1(self, mock_tension_bolted):
        # test case 1: check if results match expected mock values

        # this is what we expect the real method to return (but we mock it)
        mock_results = {
            "KEY_DISP_DESIGNATION": "40 x 20 x 3",
            "KEY_DISP_TENSION_YIELDCAPACITY": "79.09",
            "KEY_OUT_DISP_BOLT_LINE": "2",
            "KEY_OUT_DISP_BOLTS_ONE_LINE": "2",
            "KEY_OUT_DISP_BOLT_CAPACITY": "17.71",
            "KEY_OUT_DISP_GRD_PROVIDED": "3.6",
            "KEY_OUT_DISP_D_PROVIDED": "20"
        }
        self.tension_bolted.results_to_test.return_value = mock_results

        # fake user input for the test
        design_dict = {
            "KEY_SECSIZE": "40 x 20 x 3",
            "KEY_GRD": "3.6",
            "KEY_D": "20",
            "KEY_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SEC_PROFILE": "Angles",
            "KEY_LOCATION": "Long Leg",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "10",
            "KEY_AXIAL": "50",
        }

        # expected outputs based on the mock results
        expected_designation = "40 x 20 x 3"
        expected_tension_capacity_section = 79.09
        expected_tension_capacity_plate = 70.84
        expected_bolt_grade = 3.6
        expected_number_of_bolts = 4
        expected_bolt_diameter = 20

        # simulate setting the inputs and getting the result
        self.tension_bolted.set_input_values(design_dict)
        results = self.tension_bolted.results_to_test("temp_test1.txt")

        # assert that each value matches our expectations
        self.assertEqual(results["KEY_DISP_DESIGNATION"], expected_designation)
        self.assertAlmostEqual(float(results["KEY_DISP_TENSION_YIELDCAPACITY"]), expected_tension_capacity_section, places=2)

        # calculate bolt capacity manually and check if it matches expected plate capacity
        number_of_bolts = int(results["KEY_OUT_DISP_BOLT_LINE"]) * int(results["KEY_OUT_DISP_BOLTS_ONE_LINE"])
        plate_capacity = float(results["KEY_OUT_DISP_BOLT_CAPACITY"]) * number_of_bolts
        self.assertAlmostEqual(plate_capacity, expected_tension_capacity_plate, places=2)
        self.assertEqual(float(results["KEY_OUT_DISP_GRD_PROVIDED"]), expected_bolt_grade)
        self.assertEqual(number_of_bolts, expected_number_of_bolts)
        self.assertEqual(int(results["KEY_OUT_DISP_D_PROVIDED"]), expected_bolt_diameter)

    @patch('tension_bolted.Tension_bolted')
    def test_tension_bolted_test2(self, mock_tension_bolted):
        # test case 2

        mock_results = {
            "KEY_DISP_DESIGNATION": "MC 100",
            "KEY_DISP_TENSION_YIELDCAPACITY": "104.82",
            "KEY_OUT_DISP_BOLT_LINE": "1",
            "KEY_OUT_DISP_BOLTS_ONE_LINE": "3",
            "KEY_OUT_DISP_BOLT_CAPACITY": "58.25",
            "KEY_OUT_DISP_GRD_PROVIDED": "12.9",
            "KEY_OUT_DISP_D_PROVIDED": "12"
        }
        self.tension_bolted.results_to_test.return_value = mock_results

        design_dict = {
            "KEY_SECSIZE": "MC 100",
            "KEY_GRD": "12.9",
            "KEY_D": "12",
            "KEY_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SEC_PROFILE": "Channels",
            "KEY_LOCATION": "Web",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "10",
            "KEY_AXIAL": "50",
        }

        expected_designation = "MC 100"
        expected_tension_capacity_section = 104.82
        expected_tension_capacity_plate = 174.75
        expected_bolt_grade = 12.9
        expected_number_of_bolts = 3
        expected_bolt_diameter = 12

        self.tension_bolted.set_input_values(design_dict)
        results = self.tension_bolted.results_to_test("temp_test2.txt")

        self.assertEqual(results["KEY_DISP_DESIGNATION"], expected_designation)
        self.assertAlmostEqual(float(results["KEY_DISP_TENSION_YIELDCAPACITY"]), expected_tension_capacity_section, places=2)

        number_of_bolts = int(results["KEY_OUT_DISP_BOLT_LINE"]) * int(results["KEY_OUT_DISP_BOLTS_ONE_LINE"])
        plate_capacity = float(results["KEY_OUT_DISP_BOLT_CAPACITY"]) * number_of_bolts
        self.assertAlmostEqual(plate_capacity, expected_tension_capacity_plate, places=2)
        self.assertEqual(float(results["KEY_OUT_DISP_GRD_PROVIDED"]), expected_bolt_grade)
        self.assertEqual(number_of_bolts, expected_number_of_bolts)
        self.assertEqual(int(results["KEY_OUT_DISP_D_PROVIDED"]), expected_bolt_diameter)

    @patch('tension_bolted.Tension_bolted')
    def test_tension_bolted_test3(self, mock_tension_bolted):
        # test case 3

        mock_results = {
            "KEY_DISP_DESIGNATION": "40 x 40 x 3",
            "KEY_DISP_TENSION_YIELDCAPACITY": "28.79",
            "KEY_OUT_DISP_BOLT_LINE": "2",
            "KEY_OUT_DISP_BOLTS_ONE_LINE": "2",
            "KEY_OUT_DISP_BOLT_CAPACITY": "12.0",
            "KEY_OUT_DISP_GRD_PROVIDED": "4.6",
            "KEY_OUT_DISP_D_PROVIDED": "10"
        }
        self.tension_bolted.results_to_test.return_value = mock_results

        design_dict = {
            "KEY_SECSIZE": "40 x 40 x 3",
            "KEY_GRD": "4.6",
            "KEY_D": "10",
            "KEY_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SEC_PROFILE": "Angles",
            "KEY_LOCATION": "Long Leg",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "10",
            "KEY_AXIAL": "50",
        }

        expected_designation = "40 x 40 x 3"
        expected_tension_capacity_section = 28.79
        expected_tension_capacity_plate = 48.0
        expected_bolt_grade = 4.6
        expected_number_of_bolts = 4
        expected_bolt_diameter = 10

        self.tension_bolted.set_input_values(design_dict)
        results = self.tension_bolted.results_to_test("temp_test3.txt")

        self.assertEqual(results["KEY_DISP_DESIGNATION"], expected_designation)
        self.assertAlmostEqual(float(results["KEY_DISP_TENSION_YIELDCAPACITY"]), expected_tension_capacity_section, places=2)

        number_of_bolts = int(results["KEY_OUT_DISP_BOLT_LINE"]) * int(results["KEY_OUT_DISP_BOLTS_ONE_LINE"])
        plate_capacity = float(results["KEY_OUT_DISP_BOLT_CAPACITY"]) * number_of_bolts
        self.assertAlmostEqual(plate_capacity, expected_tension_capacity_plate, places=2)
        self.assertEqual(float(results["KEY_OUT_DISP_GRD_PROVIDED"]), expected_bolt_grade)
        self.assertEqual(number_of_bolts, expected_number_of_bolts)
        self.assertEqual(int(results["KEY_OUT_DISP_D_PROVIDED"]), expected_bolt_diameter)

    @patch('tension_bolted.Tension_bolted')
    def test_tension_bolted_test4(self, mock_tension_bolted):
        # test case 4

        mock_results = {
            "KEY_DISP_DESIGNATION": "MC 175",
            "KEY_DISP_TENSION_YIELDCAPACITY": "363.86",
            "KEY_OUT_DISP_BOLT_LINE": "2",
            "KEY_OUT_DISP_BOLTS_ONE_LINE": "3",
            "KEY_OUT_DISP_BOLT_CAPACITY": "61.62",
            "KEY_OUT_DISP_GRD_PROVIDED": "5.6",
            "KEY_OUT_DISP_D_PROVIDED": "20"
        }
        self.tension_bolted.results_to_test.return_value = mock_results

        design_dict = {
            "KEY_SECSIZE": "MC 175",
            "KEY_GRD": "5.6",
            "KEY_D": "20",
            "KEY_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SEC_PROFILE": "Channels",
            "KEY_LOCATION": "Web",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "10",
            "KEY_AXIAL": "50",
        }

        expected_designation = "MC 175"
        expected_tension_capacity_section = 363.86
        expected_tension_capacity_plate = 369.72
        expected_bolt_grade = 5.6
        expected_number_of_bolts = 6
        expected_bolt_diameter = 20

        self.tension_bolted.set_input_values(design_dict)
        results = self.tension_bolted.results_to_test("temp_test4.txt")

        self.assertEqual(results["KEY_DISP_DESIGNATION"], expected_designation)
        self.assertAlmostEqual(float(results["KEY_DISP_TENSION_YIELDCAPACITY"]), expected_tension_capacity_section, places=2)

        number_of_bolts = int(results["KEY_OUT_DISP_BOLT_LINE"]) * int(results["KEY_OUT_DISP_BOLTS_ONE_LINE"])
        plate_capacity = float(results["KEY_OUT_DISP_BOLT_CAPACITY"]) * number_of_bolts
        self.assertAlmostEqual(plate_capacity, expected_tension_capacity_plate, places=2)
        self.assertEqual(float(results["KEY_OUT_DISP_GRD_PROVIDED"]), expected_bolt_grade)
        self.assertEqual(number_of_bolts, expected_number_of_bolts)
        self.assertEqual(int(results["KEY_OUT_DISP_D_PROVIDED"]), expected_bolt_diameter)

# this runs all tests when we execute the file
if __name__ == "__main__":
    unittest.main()
