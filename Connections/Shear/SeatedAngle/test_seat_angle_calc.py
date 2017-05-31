import sys
import unittest
import model
import math
from PyQt5.QtWidgets import QApplication
from seat_angle_calc import SeatAngleCalculation


class TestSeatAngleCalculation(unittest.TestCase, SeatAngleCalculation):

    def setUp(self):
        QApplication(sys.argv)
        model.module_setup()
        sample_input = create_sample_ui_input_sa("SA_0")
        self.sa_calc_instance = SeatAngleCalculation()
        self.sa_calc_instance.sa_params(sample_input)

    def test_sa_params(self):
        self.assertEqual(self.sa_calc_instance.top_angle, "75 75 X 8")
        self.assertEqual(self.sa_calc_instance.connectivity, "Column flange-Beam web")
        self.assertEqual(self.sa_calc_instance.beam_section, "MB 300")
        self.assertEqual(self.sa_calc_instance.column_section, "SC 200")
        self.assertEqual(self.sa_calc_instance.beam_fu, 410)
        self.assertEqual(self.sa_calc_instance.beam_fy, 250)
        self.assertEqual(self.sa_calc_instance.angle_fu, 410)
        self.assertEqual(self.sa_calc_instance.angle_fy, 250)
        self.assertEqual(self.sa_calc_instance.shear_force, 100)
        self.assertEqual(self.sa_calc_instance.bolt_diameter, 20)
        self.assertEqual(self.sa_calc_instance.bolt_type, "Black Bolt")
        self.assertEqual(self.sa_calc_instance.bolt_grade, "4.6")
        self.assertEqual(self.sa_calc_instance.angle_sec, "150 75 X 12")
        self.assertEqual(self.sa_calc_instance.beam_w_t, 7.7)
        self.assertEqual(self.sa_calc_instance.beam_f_t, 13.1)
        self.assertEqual(self.sa_calc_instance.beam_d, 300)
        self.assertEqual(self.sa_calc_instance.beam_b, 140)
        self.assertEqual(self.sa_calc_instance.beam_R1, 14)
        self.assertEqual(self.sa_calc_instance.column_f_t, 15)
        self.assertEqual(self.sa_calc_instance.angle_t, 12)
        self.assertEqual(self.sa_calc_instance.angle_A, 150)
        self.assertEqual(self.sa_calc_instance.angle_B, 75)
        self.assertEqual(self.sa_calc_instance.angle_R1, 10)

    def test_top_angle_section(self):
        """Test top angle size selection based on beam depth.

        Note:
            Assumptions:
                Calculating top angle dimensions based on thumb rules:
                    top_angle_side = beam_depth/4
                    top_angle_thickness = top_angle_side/10
                Select the nearest available equal angle as the top angle.
        """
        self.sa_calc_instance.beam_d = 313
        self.sa_calc_instance.bolt_diameter = 12
        self.sa_calc_instance.bolt_design()
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "80 80 X 8")
        self.sa_calc_instance.beam_d = 300
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "75 75 X 8")
        self.sa_calc_instance.beam_d = 270
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "70 70 X 7")
        self.sa_calc_instance.beam_d = 222
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "55 55 X 6")
        self.sa_calc_instance.beam_d = 140
        # "35 35 X 4" based on thumb rule. '45 45 X 5' is based on edge distance requirement for 12 mm bolt
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "45 45 X 5")
        self.sa_calc_instance.beam_d = 100
        # "25 25 X 3" based on thumb rule. '45 45 X 5' is based on edge distance requirement for 12 mm bolt
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "45 45 X 5")
        self.sa_calc_instance.beam_d = 222
        self.sa_calc_instance.bolt_diameter = 20
        self.sa_calc_instance.bolt_design()
        # "55 55 X 6" based on thumb rule. '70 70 X 7' is based on edge distance requirement for 20 mm bolt
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "75 75 X 8")
        self.sa_calc_instance.beam_d = 100
        # "25 25 X 3" based on thumb rule. '70 70 X 7' is based on edge distance requirement for 20 mm bolt
        self.assertEqual(self.sa_calc_instance.top_angle_section(), "75 75 X 8")

    def test_bolt_shear_capacity_single_bolt(self):
        """
        Note:
            Values marked in inline comments # are calculated with V_nsb=185 MPa

        """
        self.assertEqual(round(self.sa_calc_instance.bolt_shear(12, 1, 400), 1), 15.6)
        self.assertEqual(round(self.sa_calc_instance.bolt_shear(16, 1, 400), 1), 29.0)
        self.assertEqual(round(self.sa_calc_instance.bolt_shear(20, 1, 400), 1), 45.3)
        self.assertEqual(round(self.sa_calc_instance.bolt_shear(24, 1, 400), 1), 65.2)  # 65.3
        self.assertEqual(round(self.sa_calc_instance.bolt_shear(30, 1, 400), 1), 103.6)  # 103.8
        self.assertEqual(round(self.sa_calc_instance.bolt_shear(36, 1, 400), 1), 150.9)  # 151.1

    def test_bolt_bearing_capacity_single_bolt(self):
        """
        Note:
            Values tested
            Diameters: 12, 16, 20, 22, 24, 27, 30, 36
            k_b: 0.25, 0.5
            thickness_plate: 10, 20
            bolt_fu: 400, 800

        """
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing(12, 1, 10, 0.5, 400), 1), 48.0)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing(16, 1, 10, 0.5, 400), 1), 64.0)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing(20, 1, 20, 0.5, 400), 1), 160.0)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing(24, 1, 10, 0.25, 400), 1), 48.0)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing(30, 1, 10, 0.25, 800), 1), 120)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing(36, 1, 10, 0.25, 800), 1), 144)

    def test_bolt_hole_clearance(self):
        # standard hole
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Standard", 12, None), 1)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Standard", 16, None), 2)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Standard", 20, None), 2)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Standard", 24, None), 2)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Standard", 30, None), 3)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Standard", 36, None), 3)

        # oversize hole
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Over-sized", 12, None), 3)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Over-sized", 16, None), 4)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Over-sized", 20, None), 4)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Over-sized", 24, None), 6)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Over-sized", 30, None), 8)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value("Over-sized", 36, None), 8)

        # #custom hole clearance
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value(0, 12, 2), 2)
        self.assertEqual(self.sa_calc_instance.bolt_hole_clearance_value(0, 24, 8), 8)

    def test_bolt_design(self):
        self.sa_calc_instance.bolt_diameter = 12
        self.sa_calc_instance.bolt_design()
        self.assertEqual(self.sa_calc_instance.min_pitch, 30)
        self.assertEqual(self.sa_calc_instance.min_gauge, 30)
        self.sa_calc_instance.min_edge_multiplier = 1.5
        self.assertEqual(self.sa_calc_instance.min_end_dist, 25)
        self.assertEqual(self.sa_calc_instance.min_edge_dist, 25)
        self.assertEqual(self.sa_calc_instance.k_b, 0.375) # 0.464
        self.assertEqual(round(self.sa_calc_instance.bolt_shear_capacity, 1), 15.6)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing_capacity, 1), 54.8)
        self.assertEqual(round(self.sa_calc_instance.bolts_required, 1), math.ceil(100 / 15.6))
        self.assertEqual(round(self.sa_calc_instance.bolt_group_capacity, 1), round(self.sa_calc_instance.bolt_shear_capacity * 7, 1))
        self.assertEqual(round(self.sa_calc_instance.max_spacing, 0), 300)
        self.assertEqual(round(self.sa_calc_instance.max_edge_dist, 0), 144)

        self.sa_calc_instance.bolt_diameter = 16
        self.sa_calc_instance.bolt_design()
        self.assertEqual(self.sa_calc_instance.min_pitch, 40)
        self.assertEqual(self.sa_calc_instance.min_gauge, 40)
        self.assertEqual(self.sa_calc_instance.min_end_dist, 30)
        self.assertEqual(self.sa_calc_instance.min_edge_dist, 30)
        self.assertEqual(self.sa_calc_instance.k_b, 0.417)
        self.assertEqual(round(self.sa_calc_instance.bolt_shear_capacity, 1), 29.0)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing_capacity, 1), 65.7)
        self.assertEqual(round(self.sa_calc_instance.bolts_required, 1), math.ceil(100 / 29.0))
        self.assertEqual(round(self.sa_calc_instance.bolt_group_capacity, 1), round(self.sa_calc_instance.bolt_shear_capacity * 4, 1))

        self.sa_calc_instance.bolt_diameter = 24
        self.sa_calc_instance.bolt_design()
        self.assertEqual(self.sa_calc_instance.min_pitch, 60)
        self.assertEqual(self.sa_calc_instance.min_gauge, 60)
        self.assertEqual(self.sa_calc_instance.min_end_dist, 45)
        self.assertEqual(self.sa_calc_instance.min_edge_dist, 45)
        self.assertEqual(self.sa_calc_instance.k_b, 0.464)
        self.assertEqual(round(self.sa_calc_instance.bolt_shear_capacity, 1), 65.2)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing_capacity, 1), 109.6)
        self.assertEqual(round(self.sa_calc_instance.bolts_required, 1), math.ceil(100 / 65.2))
        self.assertEqual(round(self.sa_calc_instance.bolt_group_capacity, 1), round(self.sa_calc_instance.bolt_shear_capacity * 2, 1))

        self.sa_calc_instance.bolt_diameter = 20
        self.sa_calc_instance.bolt_design()
        self.assertEqual(self.sa_calc_instance.min_pitch, 50)
        self.assertEqual(self.sa_calc_instance.min_gauge, 50)
        self.assertEqual(self.sa_calc_instance.min_end_dist, 40)
        self.assertEqual(self.sa_calc_instance.min_edge_dist, 40)
        self.assertEqual(self.sa_calc_instance.k_b, 0.444)
        self.assertEqual(round(self.sa_calc_instance.bolt_shear_capacity, 1), 45.3)
        self.assertEqual(round(self.sa_calc_instance.bolt_bearing_capacity, 1), 87.4)
        self.assertEqual(round(self.sa_calc_instance.bolts_required, 1), math.ceil(100 / 45.3))
        self.assertEqual(round(self.sa_calc_instance.bolt_group_capacity, 1), round(self.sa_calc_instance.bolt_shear_capacity * 3, 1))


def create_sample_ui_input_sa(sa_connection_id):
    input_dict = {'Member': {}, 'Load': {}, 'Bolt': {}, 'Angle': {}, 'bolt': {}, 'detailing':{}, 'design':{}}
    input_dict['Member']['fu (MPa)'] = 410
    input_dict['Member']['fy (MPa)'] = 250
    if sa_connection_id == "SA_0":
        input_dict['Member']['Connectivity'] = "Column web-Beam flange"
        input_dict['Member']['BeamSection'] = "MB 550"
        input_dict['Member']['ColumnSection'] = "SC 200"
        input_dict['Load']['ShearForce (kN)'] = 100
        input_dict['Bolt']['Diameter (mm)'] = 20
        input_dict['Bolt']['Type'] = "Bearing Bolt"
        input_dict['Bolt']['Grade'] = "4.6"
        input_dict['Angle']["AngleSection"] = "150 150 X 15"
        input_dict['Angle']["TopAngleSection"] = "150 75 X 12"
        input_dict['bolt']['bolt_hole_type'] = 'Standard'
        input_dict['bolt']['bolt_hole_clrnce'] = 2.0
        input_dict['bolt']['slip_factor'] = 0.48
        input_dict['bolt']['bolt_fu'] = 400
        input_dict['design']['design_method'] = 'Limit State Design'
        input_dict['detailing']['typeof_edge'] = 'b - Machine flame cut'
        input_dict['detailing']['gap'] = 10
        input_dict['detailing']['min_edgend_dist'] = 1.5
        input_dict['detailing']['is_env_corrosive'] = 'Yes'
    elif sa_connection_id == "SA_2":
        input_dict['Member']['Connectivity'] = "Column flange-Beam flange"
        input_dict['Member']['BeamSection'] = "MB 300"
        input_dict['Member']['ColumnSection'] = "UC 203 x 203 x 86"
        input_dict['Load']['ShearForce (kN)'] = 100
        input_dict['Bolt']['Diameter (mm)'] = 20
        input_dict['Bolt']['Type'] = "Bearing Bolt"
        input_dict['Bolt']['Grade'] = "5.8"
        input_dict['Angle']["AngleSection"] = "150 150 X 15"
        input_dict['Angle']["TopAngleSection"] = "150 150 X 10"
        input_dict['bolt']['bolt_hole_type'] = 'Standard'
        input_dict['bolt']['bolt_hole_clrnce'] = 2.0
        input_dict['bolt']['slip_factor'] = 0.55
        input_dict['bolt']['bolt_fu'] = 500
        input_dict['design']['design_method'] = 'Limit State Design'
        input_dict['detailing']['typeof_edge'] = 'a - Sheared or hand flame cut'
        input_dict['detailing']['gap'] = 20
        input_dict['detailing']['min_edgend_dist'] = 1.7
        input_dict['detailing']['is_env_corrosive'] = 'No'
    elif sa_connection_id == "SA_3":
        input_dict['Member']['Connectivity'] = "Column flange-Beam flange"
        input_dict['Member']['BeamSection'] = "MB 300"
        input_dict['Member']['ColumnSection'] = "UC 203 x 203 x 86"
        input_dict['Load']['ShearForce (kN)'] = 100
        input_dict['Bolt']['Diameter (mm)'] = 16
        input_dict['Bolt']['Type'] = "Bearing Bolt"
        input_dict['Bolt']['Grade'] = "5.8"
        input_dict['Angle']["AngleSection"] = "150 150 X 15"
        input_dict['Angle']["TopAngleSection"] = "150 150 X 10"
        input_dict['bolt']['bolt_hole_type'] = 'Standard'
        input_dict['bolt']['bolt_hole_clrnce'] = 2.0
        input_dict['bolt']['slip_factor'] = 0.55
        input_dict['bolt']['bolt_fu'] = 500
        input_dict['design']['design_method'] = 'Limit State Design'
        input_dict['detailing']['typeof_edge'] = 'a - Sheared or hand flame cut'
        input_dict['detailing']['gap'] = 20
        input_dict['detailing']['min_edgend_dist'] = 1.7
        input_dict['detailing']['is_env_corrosive'] = 'No'
    elif sa_connection_id == "SA_4":
        input_dict['Member']['Connectivity'] = "Column flange-Beam flange"
        input_dict['Member']['BeamSection'] = "MB 200"
        input_dict['Member']['ColumnSection'] = "UC 203 x 203 x 86"
        input_dict['Load']['ShearForce (kN)'] = 80
        input_dict['Bolt']['Diameter (mm)'] = 12
        input_dict['Bolt']['Type'] = "Bearing Bolt"
        input_dict['Bolt']['Grade'] = "6.8"
        input_dict['Angle']["AngleSection"] = "150 150 X 15"
        input_dict['Angle']["TopAngleSection"] = "150 75 X 12"
        input_dict['bolt']['bolt_hole_type'] = 'Over-sized'
        input_dict['bolt']['bolt_hole_clrnce'] = 3.0
        input_dict['bolt']['slip_factor'] = 0.55
        input_dict['bolt']['bolt_fu'] = 600
        input_dict['design']['design_method'] = 'Limit State Design'
        input_dict['detailing']['typeof_edge'] = 'a - Sheared or hand flame cut'
        input_dict['detailing']['gap'] = 10
        input_dict['detailing']['min_edgend_dist'] = 1.7
        input_dict['detailing']['is_env_corrosive'] = 'No'
    elif sa_connection_id == "SA_6":
        input_dict['Member']['Connectivity'] = "Column flange-Beam flange"
        input_dict['Member']['BeamSection'] = "MB 300"
        input_dict['Member']['ColumnSection'] = "UC 203 x 203 x 86"
        input_dict['Load']['ShearForce (kN)'] = 100
        input_dict['Bolt']['Diameter (mm)'] = 12
        input_dict['Bolt']['Type'] = "Bearing Bolt"
        input_dict['Bolt']['Grade'] = "5.8"
        input_dict['Angle']["AngleSection"] = "150 150 X 15"
        input_dict['Angle']["TopAngleSection"] = "150 75 X 12"
        input_dict['bolt']['bolt_hole_type'] = 'Standard'
        input_dict['bolt']['bolt_hole_clrnce'] = 1.0
        input_dict['bolt']['slip_factor'] = 0.55
        input_dict['bolt']['bolt_fu'] = 500
        input_dict['design']['design_method'] = 'Limit State Design'
        input_dict['detailing']['typeof_edge'] = 'a - Sheared or hand flame cut'
        input_dict['detailing']['gap'] = 20
        input_dict['detailing']['min_edgend_dist'] = 1.7
        input_dict['detailing']['is_env_corrosive'] = 'No'

    return input_dict


def create_sample_ui_output_sa():
    output_dict = {'SeatAngle': {}, 'Bolt': {}}
    output_dict['SeatAngle'] = {
        "Length (mm)": 140,
        "Moment Demand (kNm)": 542,
        "Moment Capacity (kNm)": 916,
        "Shear Demand (kN/mm)": 100,
        "Shear Capacity (kN/mm)": 220,
        "Beam Shear Strength (kN/mm)": 303,
        "Top Angle": "60 60X6"
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
    app = QApplication(sys.argv)
    ex = TestSeatAngleCalculation()
    sys.exit(app.exec_())
