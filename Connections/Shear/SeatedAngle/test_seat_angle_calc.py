import sys
import unittest, model, math
from seat_angle_calc import SeatAngleCalculation
from PyQt4 import QtGui


class TestSeatAngleCalculation(unittest.TestCase, SeatAngleCalculation):
    def setUp(self):
        app = QtGui.QApplication(sys.argv)
        model.module_setup()
        sample_input = create_sample_ui_input()
        self.sa_params(sample_input)

    def test_sa_params(self):
        self.assertEqual(self.top_angle, "ISA 100X65X8")
        self.assertEqual(self.connectivity, "Column flange-Beam web")
        self.assertEqual(self.beam_section, "ISMB 300")
        self.assertEqual(self.column_section, "ISSC 200")
        self.assertEqual(self.beam_fu, 410)
        self.assertEqual(self.beam_fy, 250)
        self.assertEqual(self.angle_fu, 410)
        self.assertEqual(self.angle_fy, 250)
        self.assertEqual(self.shear_force, 100)
        self.assertEqual(self.bolt_diameter, 20)
        self.assertEqual(self.bolt_type, "Black Bolt")
        self.assertEqual(self.bolt_grade, "4.6")
        self.assertEqual(self.angle_sec, "ISA 150X75X12")
        self.assertEqual(self.beam_w_t, 7.7)
        self.assertEqual(self.beam_f_t, 13.1)
        self.assertEqual(self.beam_d, 300)
        self.assertEqual(self.beam_w_f, 140)
        self.assertEqual(self.beam_R1, 14)
        self.assertEqual(self.column_f_t, 15)
        self.assertEqual(self.angle_t, 12)
        self.assertEqual(self.angle_A, 150)
        self.assertEqual(self.angle_B, 75)
        self.assertEqual(self.angle_R1, 10)

    def test_top_angle_section(self):
        """Test top angle size selection based on beam depth.

        Note:
            Assumptions:
                Calculating top angle dimensions based on thumb rules:
                    top_angle_side = beam_depth/4
                    top_angle_thickness = top_angle_side/10
                Select the nearest available equal angle as the top angle.
        """
        temporary_beam_d = self.beam_d
        self.beam_d = 313
        self.assertEqual(SeatAngleCalculation.top_angle_section(self), "ISA 80X80X8")
        self.beam_d = 300
        self.assertEqual(SeatAngleCalculation.top_angle_section(self), "ISA 75X75X8")
        self.beam_d = 270
        self.assertEqual(SeatAngleCalculation.top_angle_section(self), "ISA 70X70X7")
        self.beam_d = 222
        self.assertEqual(SeatAngleCalculation.top_angle_section(self), "ISA 55X55X6")
        self.beam_d = 140
        self.assertEqual(SeatAngleCalculation.top_angle_section(self), "ISA 35X35X4")
        self.beam_d = 100
        self.assertEqual(SeatAngleCalculation.top_angle_section(self), "ISA 25X25X3")

    def test_sa_output(self):
        pass

    def test_bolt_shear_capacity_single_bolt(self):
        """
        Note:
            Values marked in inline comments # are calculated with V_nsb=185 MPa

        """
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 12, 1, 400), 1), 15.6)
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 16, 1, 400), 1), 29.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 20, 1, 400), 1), 45.3)
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 22, 1, 400), 1), 56.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 24, 1, 400), 1), 65.2)  # 65.3
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 27, 1, 400), 1), 84.8)  # 84.9
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 30, 1, 400), 1), 103.6)  # 103.8
        self.assertEqual(round(SeatAngleCalculation.bolt_shear(self, 36, 1, 400), 1), 150.9)  # 151.1

    def test_bolt_bearing_capacity_single_bolt(self):
        """
        Note:
            Values tested
            Diameters: 12, 16, 20, 22, 24, 27, 30, 36
            k_b: 0.25, 0.5
            thickness_plate: 10, 20
            bolt_fu: 400, 800

        """
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 12, 1, 10, 0.5, 400), 1), 48.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 16, 1, 10, 0.5, 400), 1), 64.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 20, 1, 20, 0.5, 400), 1), 160.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 22, 1, 20, 0.5, 400), 1), 176.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 24, 1, 10, 0.25, 400), 1), 48.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 27, 1, 10, 0.25, 400), 1), 54.0)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 30, 1, 10, 0.25, 800), 1), 120)
        self.assertEqual(round(SeatAngleCalculation.bolt_bearing(self, 36, 1, 10, 0.25, 800), 1), 144)

    def test_bolt_hole_clearance(self):
        # standard hole
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 12, None), 1)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 14, None), 1)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 16, None), 2)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 18, None), 2)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 20, None), 2)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 22, None), 2)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 24, None), 2)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 30, None), 3)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 1, 36, None), 3)

        # oversize hole
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 12, None), 3)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 14, None), 3)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 16, None), 4)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 18, None), 4)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 20, None), 4)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 22, None), 4)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 24, None), 6)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 30, None), 8)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 36, None), 8)

        # #custom hole clearance
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 12, 2), 2)
        self.assertEqual(SeatAngleCalculation.bolt_hole_clearance(self, 0, 24, 8), 8)

    def test_bolt_design(self):
        self.bolt_design(12)
        self.assertEqual(self.min_pitch, 30)
        self.assertEqual(self.min_gauge, 30)
        self.min_edge_multiplier = 1.5
        self.assertEqual(self.min_end_dist, 20)
        self.assertEqual(self.min_edge_dist, 20)
        self.assertEqual(self.k_b, 0.513)
        self.assertEqual(round(self.bolt_shear_capacity, 1), 15.6)
        self.assertEqual(round(self.bolt_bearing_capacity, 1), 60.6)
        self.assertEqual(round(self.bolts_required, 1), math.ceil(100 / 15.6))
        self.assertEqual(round(self.bolt_group_capacity, 1), round(self.bolt_shear_capacity * 7, 1))
        self.assertEqual(round(self.max_spacing, 0), 300)
        self.assertEqual(round(self.max_edge_dist, 0), 144)

        self.bolt_design(16)
        self.assertEqual(self.min_pitch, 40)
        self.assertEqual(self.min_gauge, 40)
        self.assertEqual(self.min_end_dist, 30)
        self.assertEqual(self.min_edge_dist, 30)
        self.assertEqual(self.k_b, 0.491)
        self.assertEqual(round(self.bolt_shear_capacity, 1), 29.0)
        self.assertEqual(round(self.bolt_bearing_capacity, 1), 77.3)
        self.assertEqual(round(self.bolts_required, 1), math.ceil(100 / 29.0))
        self.assertEqual(round(self.bolt_group_capacity, 1), round(self.bolt_shear_capacity * 4, 1))

        self.bolt_design(24)
        self.assertEqual(self.min_pitch, 60)
        self.assertEqual(self.min_gauge, 60)
        self.assertEqual(self.min_end_dist, 40)
        self.assertEqual(self.min_edge_dist, 40)
        self.assertEqual(self.k_b, 0.513)
        self.assertEqual(round(self.bolt_shear_capacity, 1), 65.2)
        self.assertEqual(round(self.bolt_bearing_capacity, 1), 121.2)
        self.assertEqual(round(self.bolts_required, 1), math.ceil(100 / 65.2))
        self.assertEqual(round(self.bolt_group_capacity, 1), round(self.bolt_shear_capacity * 2, 1))

        self.bolt_design(20)
        self.assertEqual(self.min_pitch, 50)
        self.assertEqual(self.min_gauge, 50)
        self.assertEqual(self.min_end_dist, 35)
        self.assertEqual(self.min_edge_dist, 35)
        self.assertEqual(self.k_b, 0.508)
        self.assertEqual(round(self.bolt_shear_capacity, 1), 45.3)
        self.assertEqual(round(self.bolt_bearing_capacity, 1), 100.0)
        self.assertEqual(round(self.bolts_required, 1), math.ceil(100 / 45.3))
        self.assertEqual(round(self.bolt_group_capacity, 1), round(self.bolt_shear_capacity * 3, 1))

    def test_block_shear_check(self):
        pass

    def test_seat_angle_connection(self):
        # self.seat_angle_connection(create_sample_ui_input())
        pass


def create_sample_ui_input():
    input_dict = {'Member': {}, 'Load': {}, 'Bolt': {}, 'Angle': {}}
    input_dict['Member']['Connectivity'] = "Column flange-Beam web"
    input_dict['Member']['BeamSection'] = "ISMB 300"
    input_dict['Member']['ColumnSection'] = "ISSC 200"
    input_dict['Member']['fu (MPa)'] = 410
    input_dict['Member']['fy (MPa)'] = 250
    input_dict['Load']['ShearForce (kN)'] = 100
    input_dict['Bolt']['Diameter (mm)'] = 20
    input_dict['Bolt']['Type'] = "Black Bolt"
    input_dict['Bolt']['Grade'] = "4.6"
    input_dict['Angle']["AngleSection"] = "ISA 150X75X12"
    return input_dict


def create_sample_ui_output():
    output_dict = {'SeatAngle': {}, 'Bolt': {}}
    output_dict['SeatAngle'] = {
        "Length (mm)": 140,
        "Moment Demand (kNm)": 542,
        "Moment Capacity (kNm)": 916,
        "Shear Demand (kN/mm)": 100,
        "Shear Capacity (kN/mm)": 220,
        "Beam Shear Strength (kN/mm)": 303,
        "Top Angle": "ISA 60X60X6"
    }
    output_dict['Bolt'] = {
        "status": True,
        "Shear Capacity (kN)": 45.3,
        "Bearing Capacity (kN)": 96,
        "Capacity of Bolt (kN)": 45.3,
        "Bolt group capacity (kN)": 181.2,
        "No. of Bolts": 4,
        "No. of Row": 2,
        "No. of Column": 2,
        "Pitch Distance (mm)": 50,
        "Gauge Distance (mm)": 40,
        "End Distance (mm)": 50,
        "Edge Distance (mm)": 50,

        "bolt_fu": 400,
        "bolt_dia": 20,
        "k_b": 0.5,
        "beam_w_t": 7.7,
        "beam_fu": 410,
        "shearforce": 100,
        "hole_dia": 22
    }
    return output_dict


if __name__ == '__main__':
    unittest.main()
    # launchSeatAngleController(None)
    # set_osdaglogger()
    # rawLogger = logging.getLogger("raw")
    # rawLogger.setLevel(logging.INFO)
    # # while launching from Osdag Main:
    # # fh = logging.FileHandler("./Connections/Shear/SeatAngle/seatangle.log", mode="w")
    # # while launching from Seated Angle folder
    # fh = logging.FileHandler("./seatangle.log", mode="w")
    # formatter = logging.Formatter('''%(message)s''')
    # fh.setFormatter(formatter)
    # rawLogger.addHandler(fh)
    # # while launching from Osdag Main:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href="./Connections/Shear/SeatedAngle/log.css"/>''')
    # while launching from Seated Angle folder:
    # rawLogger.info('''<link rel="stylesheet" type="text/css" href=".//log.css"/>''')

    app = QtGui.QApplication(sys.argv)
    # window = MainController()
    # window.show()
    ex = TestSeatAngleCalculation()
    sys.exit(app.exec_())
