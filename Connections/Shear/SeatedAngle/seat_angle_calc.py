""" 
References:

Design of Steel Structures (DoSS) - N. Subramanian
First published 2008, 14th impression 2014
    Chapter 5: Bolted Connections
    Example 5.14, Page 406

IS 800: 2007
    General construction in steel - Code of practice (Third revision)

ASCII diagram

            +-+-------------+-+   +-------------------------+
            | |             | |   |-------------------------|
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |-------------------------|
            | |             | |   +-------------------------+
            | |             | |+-----------+
            | |             | || +---------+
            | |             | || |
            | |         +---|-||-|---+
            | |         +---|-||-|---+
            | |             | || |
            | |         +---|-||-|---+
            | |         +---|-||-|---+
            | |             | ||_|
            | |             | |
            | |             | |
            +-+-------------+-+

"""

import math
import logging
from model import *
from model import get_angledata, get_beamdata, get_columndata
from Connections.connection_calculations import ConnectionCalculations

logger = logging.getLogger("osdag.SeatAngleCalc")


class SeatAngleCalculation(ConnectionCalculations):
    """Perform design and detailing checks for seated angle connection.

    Attributes:
        gamma_mb (float): partial safety factor for material - resistance of connection - bolts
        gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling
        gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress
        bolt_hole_type (string): 'Standard' or 'Over-sized'
        beam_col_clear_gap (int): clearance + tolerance
        min_edge_multiplier (float): multiplier for min edge distance check - based on edge type
        root_clearance_sa (int): clearance of first bolt from the root of seated angle
        root_clearance_col (int): clearance of first bolt from the root of supporting column
        clear_col_space (int): for CWBF, clear space between the column flanges
        type_of_edge (string)
        is_environ_corrosive (string): "Yes" if members are under corrosive influences (used for max edge distance)
        design_method (string)
        is_friction_grip_bolt (boolean): True if the bolt is to be designed as Friction Grip Bolt with slip not permitted at ultimate load
        n_e (int): Number of effective surfaces offering frictional resistance to Friction Grip Bolt bolts
        mu_f (float): slip-factor/ coefficient of friction of Friction Grip Bolt bolts
        bolt_fu_overwrite (int)
        top_angle (string)
        dict_top_angle_data (dict): top angle section - geometric properties
        top_angle_recommended (string): Calculated top angle size based on thumb rules
        connectivity (string)
        beam_section (string)
        column_section (string)
        beam_fu (float)
        beam_fy (float)
        column_fu (float)
        column_fy (float)
        angle_fy (float)
        angle_fu (float)
        shear_force (float)
        bolt_diameter (int)
        bolt_type (string)
        bolt_grade (float)
        bolt_fu (int)
        bolt_diameter (int)
        bolt_hole_clearance_value (float)
        bolt_hole_diameter (int)
        angle_sec (string): seated angle section
        dict_angle_data (dict): seated angle section - geometric properties        
        beam_w_t (float): beam web thickness
        beam_f_t (float): beam flange thickness
        beam_d  (float): beam depth
        beam_b  (float): beam width
        beam_R1 (float): beam root radius
        column_f_t (float): column flange thickness
        column_w_t (float): column web thickness
        column_d (float): column depth
        column_b (float): column width        
        column_R1 (float): column root radius R1
        column_R2 (float): column root radius R2
        angle_t (float): angle thickness
        angle_A  (float): longer leg of unequal angle
        angle_B  (float): shorter leg of unequal angle
        angle_R1 (float)
        angle_R2 (float)
        angle_l (float)
        top_angle_A (int)
        top_angle_B (int)
        top_angle_R1 (float)
        top_angle_R2 (float)

        safe (Boolean) : status of connection, True if safe
        output_dict (dictionary)

        moment_at_root_angle (float)
        outstanding_leg_length_required (float): Required leg length of seated angle
        moment_capacity_angle (float): Moment capacity of outstanding leg of the seated angle
        is_shear_high (boolean): denotes if the shear fails in high shear [Cl 8.2.1]
        moment_high_shear_beta (float): factor for moment capacity with high shear
        leg_moment_d (float): M_d
        outstanding_leg_shear_capacity (float)
        beam_shear_strength (float)
        beam_web_local_buckling_capacity (float)
        bolt_shear_capacity (float)
        thickness_governing_min (float): min thick of connecting component for calculating bolt bearing capacity
        k_b (float)
        bolt_bearing_capacity (float)
        bolt_value (float)
        bolt_group_capacity (float)
        bolts_required (int)
        bolts_provided (int)
        num_rows (int)
        num_cols (int)
        pitch (float)
        gauge (float)
        gauge_two_bolt (float): gauge length for two bolts on each leg of top angle
        end_dist (int)
        edge_dist (int)        
        min_end_dist (int)
        min_edge_dist (int)
        min_pitch (int)
        min_gauge (int)
        max_spacing (int)
        max_edge_dist (int)
        top_angle_end_dist_column (float): Distance of first bolt from tip of top_angle_leg (A) connected to column   
        top_angle_end_dist_beam (float): Distance of first bolt from tip of top_angle_leg (B) connected to beam
        seat_angle_end_dist_beam (float): Distance of first bolt from tip of seat_angle_leg (B) connected to beam

    """

    def __init__(self):
        """Initialize all attributes."""
        super(SeatAngleCalculation, self).__init__()
        self.gamma_mb = 0.0
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0
        self.bolt_hole_type = 'Standard'
        self.beam_col_clear_gap = 0
        self.min_edge_multiplier = 1
        self.root_clearance_sa = 0
        self.root_clearance_col = 0
        self.clear_col_space = 0
        self.type_of_edge = "b - Machine flame cut"
        self.is_environ_corrosive = "No"
        self.design_method = "Limit State Design"
        self.is_friction_grip_bolt = False
        self.n_e = 1  # interfaces offering friction - for Friction Grip Bolt design
        self.mu_f = 0.4  # slip factor - for Friction Grip Bolt design
        self.bolt_fu_overwrite = 0

        self.top_angle = ""
        self.dict_top_angle_data = {}
        self.top_angle_recommended = " "
        self.connectivity = ""
        self.beam_section = ""
        self.dict_beam_data = {}
        self.column_section = ""
        self.dict_column_data = {}
        self.beam_fu = 0
        self.beam_fy = 0
        self.column_fu = 0
        self.column_fy = 0
        self.angle_fy = 0
        self.angle_fu = 0
        self.shear_force = 0.0
        self.bolt_diameter = 1
        self.bolt_type = 1
        self.bolt_grade = ""
        self.bolt_fu = 0
        self.bolt_diameter = 1
        self.bolt_hole_clearance_value = 1.0
        self.bolt_hole_diameter = 1
        self.angle_sec = ""
        self.dict_angle_data = {}
        self.beam_w_t = 1
        self.beam_f_t = 1
        self.beam_d = 1
        self.beam_b = 1
        self.beam_R1 = 1
        self.column_f_t = 1
        self.column_w_t = 1
        self.column_d = 1
        self.column_b = 1
        self.column_R1 = 1
        self.column_R2 = 1
        self.angle_t = 1
        self.angle_A = 1
        self.angle_B = 1
        self.angle_R1 = 1
        self.angle_R2 = 1
        self.angle_l = 1
        self.top_angle_t = 1
        self.top_angle_A = 1
        self.top_angle_B = 1
        self.top_angle_R1 = 1
        self.top_angle_R2 = 1

        self.safe = True
        self.output_dict = {}

        self.moment_at_root_angle = 0.0
        self.outstanding_leg_length_required = 0.0
        self.moment_capacity_angle = 0.0
        self.is_shear_high = False
        self.moment_high_shear_beta = 0.0
        self.leg_moment_d = 0.0
        self.outstanding_leg_shear_capacity = 0.0
        self.beam_shear_strength = 0.0
        self.beam_web_local_buckling_capacity = 0.0
        self.bolt_shear_capacity = 0.0
        self.thickness_governing_min = 0.0
        self.k_b = 0.0
        self.bolt_bearing_capacity = 0.0
        self.bolt_value = 0.0
        self.bolt_group_capacity = 0.0
        self.bolts_required = 1
        self.bolts_provided = 1
        self.num_rows = 1
        self.num_cols = 1
        self.pitch = 1
        self.gauge = 1
        self.gauge_two_bolt = 1
        self.end_dist = 1
        self.edge_dist = 1
        self.min_end_dist = 1
        self.min_edge_dist = 1
        self.min_pitch = 1
        self.min_gauge = 1
        self.max_spacing = 1
        self.max_edge_dist = 1
        self.top_angle_end_dist_column = 1.0
        self.top_angle_end_dist_beam = 1.0
        self.seat_angle_end_dist_beam = 1.0

    def top_angle_section(self):
        """Identify appropriate top angle size based on beam depth.

        Args:            

        Returns:
            top_angle(string): top angle section

        Note:
            Assumptions:
                Calculating top angle dimensions based on thumb rules:
                    top_angle_side = beam_depth/4
                    top_angle_thickness = top_angle_side/10
                Select the nearest available equal angle as the top angle.
                Equal angles satisfying both these thumb rules are selected for this function from steel tables
        """
        # minimum length of leg of top angle is twice edge distance + angle thickness.
        # as the side length is rounded up in the next step, ignoring angle thickness while calculating
        # minimum length of side
        top_angle_side_minimum = 2 * self.min_edge_multiplier * self.bolt_hole_diameter  # twice edge distance
        top_angle_side = max(float(self.beam_d) / 4, top_angle_side_minimum)
        # round up to nearest 5 mm. '+2' for conservative round up.
        top_angle_side = ConnectionCalculations.round_up_5(top_angle_side + 2)

        try:
            top_angle = {20: "20 20 X 3",  # does not satisfy min edge dist req for 12 mm bolt
                         25: "25 25 X 3",  # does not satisfy min edge dist req for 12 mm bolt
                         30: "30 30 X 3",  # does not satisfy min edge dist req for 12 mm bolt
                         35: "35 35 X 4",  # does not satisfy min edge dist req for 12 mm bolt
                         40: "40 40 X 4",
                         45: "45 45 X 5",
                         50: "50 50 X 5",
                         55: "55 55 X 6",
                         60: "60 60 X 6",
                         65: "65 65 X 6",
                         70: "70 70 X 7",
                         75: "75 75 X 8",
                         80: "80 80 X 8",
                         90: "90 90 X 10",
                         100: "100 100 X 10"
                         }[top_angle_side]
        except KeyError:
            top_angle = " cannot compute"
        return top_angle

    def sa_params(self, input_dict):
        """Initialise variables to use in calculations from input dictionary.

        Args:
            input_dict: dictionary generated based on user inputs in GUI

        Returns:
            none

        Note:
            Assumptions:
            angle f_y and f_u are equal to beam f_y and f_u respectively
            clear gap = 5 + 5 mm

        """
        # Initialise Design Preferences
        self.gamma_mb = 1.25  # partial safety factor for material - resistance of connection - bolts
        self.gamma_m0 = 1.1  # partial safety factor for material - resistance governed by yielding or buckling
        self.gamma_m1 = 1.25  # partial safety factor for material - resistance governed by ultimate stress

        self.bolt_hole_type = input_dict['bolt']['bolt_hole_type']  # "Standard" or "Over-sized"

        self.is_friction_grip_bolt = False
        if input_dict['Bolt']['Type'] == "Friction Grip Bolt":
            self.is_friction_grip_bolt = True  # set to True, if bolt is Friction Grip Bolt with no slip at ultimate load
        self.mu_f = input_dict['bolt']['slip_factor']  # slip factor - for Friction Grip Bolt design
        self.bolt_fu_overwrite = input_dict['bolt']['bolt_fu']  # F_u overwrite for bolt material
        self.beam_col_clear_gap = input_dict['detailing']['gap']  # clearance + tolerance
        # min edge distance multiplier based on edge type (cl. 10.2.4.2)
        self.min_edge_multiplier = input_dict['detailing']['min_edgend_dist']
        self.type_of_edge = input_dict['detailing']['typeof_edge']
        # set to "Yes", if environment is corrosive
        self.is_environ_corrosive = input_dict['detailing']['is_env_corrosive']
        self.design_method = str(input_dict['design']['design_method'])

        self.top_angle = input_dict['Angle']['TopAngleSection']
        self.connectivity = input_dict['Member']['Connectivity']
        self.beam_section = input_dict['Member']['BeamSection']
        self.column_section = input_dict['Member']['ColumnSection']
        self.beam_fu = float(input_dict['Member']['fu (MPa)'])
        self.beam_fy = float(input_dict['Member']['fy (MPa)'])
        self.column_fy = float(self.beam_fy)
        self.column_fu = float(self.beam_fu)
        self.angle_fy = float(str(self.beam_fy))
        self.angle_fu = float(self.beam_fu)
        self.shear_force = float(input_dict['Load']['ShearForce (kN)'])
        self.bolt_diameter = int(input_dict['Bolt']['Diameter (mm)'])
        self.bolt_type = input_dict['Bolt']['Type']
        self.bolt_grade = input_dict['Bolt']['Grade']
        self.bolt_fu = float(input_dict["bolt"]["bolt_fu"])
        self.angle_sec = input_dict['Angle']["AngleSection"]

        # TODO for test_calc and test_report, uncomment the below line
        # model.set_databaseconnection()
        self.dict_beam_data = get_beamdata(self.beam_section)
        self.dict_column_data = get_columndata(self.column_section)
        self.dict_angle_data = get_angledata(self.angle_sec)
        self.beam_w_t = float(self.dict_beam_data["tw"])  # beam web thickness
        self.beam_f_t = float(self.dict_beam_data["T"])  # beam flange thickness
        self.beam_d = float(self.dict_beam_data["D"])  # beam depth
        self.beam_b = float(self.dict_beam_data["B"])  # beam width
        self.beam_R1 = float(self.dict_beam_data["R1"])  # beam root radius
        self.column_f_t = float(self.dict_column_data["T"])  # column flange thickness
        self.column_w_t = float(self.dict_column_data["tw"])  # column web thickness
        self.column_d = float(self.dict_column_data["D"])  # column depth
        self.column_b = float(self.dict_column_data["B"])  # column width
        self.column_R1 = float(self.dict_column_data["R1"])  # column root radius R1
        self.column_R2 = float(self.dict_column_data["R2"])  # column root radius R2
        self.angle_t = float(self.dict_angle_data["t"])  # angle thickness
        seat_legsizes = str(self.dict_angle_data["AXB"])
        self.angle_A = int(seat_legsizes.split('x')[0])  # longer leg of unequal angle
        self.angle_B = int(seat_legsizes.split('x')[1])  # shorter leg of unequal angle
        self.angle_R1 = float(self.dict_angle_data["R1"])
        self.angle_R2 = float(self.dict_angle_data["R2"])
        self.dict_top_angle_data = get_angledata(self.top_angle)
        self.top_angle_t = float(self.dict_top_angle_data["t"])  # angle thickness
        top_angle_legsizes = str(self.dict_top_angle_data["AXB"])
        self.top_angle_A = int(top_angle_legsizes.split('x')[0])  # longer leg of unequal angle
        self.top_angle_B = int(top_angle_legsizes.split('x')[1])  # shorter leg of unequal angle
        self.top_angle_R1 = float(self.dict_top_angle_data["R1"])
        self.top_angle_R2 = float(self.dict_top_angle_data["R2"])

        self.pitch = 0
        self.top_angle_recommended = self.top_angle_section()
        self.safe = True

    def sa_output(self):
        """Create and return dictionary of output parameters."""
        self.output_dict = {
            'SeatAngle': {
                    "Length (mm)": self.angle_l,
                    "Moment Demand (kN-mm)": self.moment_at_root_angle,
                    "Moment Capacity (kN-mm)": self.moment_capacity_angle,
                    "Shear Demand (kN)": self.shear_force,
                    "Shear Capacity (kN)": self.outstanding_leg_shear_capacity,
                    "Beam Shear Strength (kN)": self.beam_shear_strength,
                    "Top Angle": self.top_angle,
                    "status": self.safe
            },
            'Bolt': {
                    "status": self.safe,
                    "Shear Capacity (kN)": self.bolt_shear_capacity,
                    "Bearing Capacity (kN)": self.bolt_bearing_capacity,
                    "Capacity of Bolt (kN)": self.bolt_value,
                    "Bolt group capacity (kN)": self.bolt_group_capacity,
                    "No. of Bolts Provided": self.bolts_provided,
                    "No. of Bolts Required": self.bolts_required,
                    "No. of Row": int(self.num_rows),
                    "No. of Column": int(self.num_cols),
                    "Pitch Distance (mm)": self.pitch,
                    "Gauge Distance (mm)": self.gauge,
                    "Gauge Two Bolt (mm)": self.gauge_two_bolt,
                    "End Distance (mm)": self.end_dist,
                    "Edge Distance (mm)": self.edge_dist,
                    # Use below distances only for generating 2D drawings and CAD
                    "top_angle_end_dist_column": self.top_angle_end_dist_column,
                    "top_angle_end_dist_beam": self.top_angle_end_dist_beam,
                    "seat_angle_end_dist_beam": self.seat_angle_end_dist_beam,

                    # output dictionary items for design report
                    "bolt_fu": self.bolt_fu,
                    "bolt_dia": self.bolt_diameter,
                    "k_b": self.k_b,
                    "beam_w_t": self.beam_w_t,
                    "beam_fu": self.beam_fu,
                    "shearforce": self.shear_force,
                    "hole_dia": self.bolt_hole_diameter
            }
        }

    def bolt_design(self):
        """Calculate bolt capacities, distances and layout.

        Args:

        Returns:

        """
        self.root_clearance_sa = 1.5 * self.bolt_diameter
        self.root_clearance_col = 1.5 * self.bolt_diameter
        self.bolt_hole_clearance_value = self.bolt_hole_clearance(self.bolt_hole_type, self.bolt_diameter)
        self.bolt_hole_diameter = self.bolt_diameter + self.bolt_hole_clearance_value

        self.thickness_governing_min = min(self.column_f_t, self.angle_t)
        self.calculate_distances(self.bolt_diameter, self.bolt_hole_diameter, self.min_edge_multiplier,
                                 self.thickness_governing_min, self.is_environ_corrosive)
        self.max_spacing = min(self.max_spacing, 32 * self.thickness_governing_min)
        self.edge_dist = self.min_edge_dist
        self.end_dist = self.min_end_dist
        self.pitch = self.min_pitch
        self.edge_dist = ConnectionCalculations.round_up_5(self.edge_dist)
        self.end_dist = ConnectionCalculations.round_up_5(self.end_dist)

        self.calculate_kb()

        # Bolt capacity

        if self.is_friction_grip_bolt is False:
            self.bolt_shear_capacity = ConnectionCalculations.bolt_shear(bolt_diameter=self.bolt_diameter,
                                                                         number_of_bolts=1, bolt_fu=self.bolt_fu)
            self.bolt_bearing_capacity = ConnectionCalculations.bolt_bearing(bolt_diameter=self.bolt_diameter,
                                        number_of_bolts=1, thickness_plate=self.thickness_governing_min,
                                        k_b=self.k_b, plate_fu=self.beam_fu)
            self.bolt_value = min(self.bolt_shear_capacity, self.bolt_bearing_capacity)

        elif self.is_friction_grip_bolt:
            self.bolt_shear_capacity = ConnectionCalculations.bolt_shear_friction_grip_bolt(self.bolt_diameter, self.bolt_fu,
                                                                              self.mu_f,
                                                                              self.n_e,
                                                                              self.bolt_hole_type)
            self.bolt_bearing_capacity = 0.000
            self.bolt_value = self.bolt_shear_capacity
        # Check for long joints is not applicable for seated angle connection
        self.bolts_required = int(math.ceil(float(self.shear_force) / self.bolt_value))

    def seat_angle_connection(self, input_dict):
        """ Perform design and detailing checks based for seated angle connection.

        Args:
            input_dict (dictionary)

        Returns:
            output_dict (dictionary)

        Note:
            Algorithm:
            1) Initialise variables to use
            2) Bolt Design (layout and spacing)
            3) Determine length of outstanding leg of seated angle
            4) Determine shear strength of outstanding leg and compare with capacity

        """

        self.sa_params(input_dict)

        self.clear_col_space = self.column_d - 2 * self.column_f_t - 2 * self.column_R1 - 2 * self.root_clearance_col
        if self.connectivity == "Column web-Beam flange" and self.beam_b > self.clear_col_space:
            self.safe = False
            logger.error(": Compatibility failure")
            logger.warning(": Beam width (%s mm) is greater than the clear space available" + \
                           " between column flanges (%s mm)" % self.clear_col_space, self.beam_b)
            logger.info(": Select compatible beam and column sizes")

        old_beam_section = get_oldbeamcombolist()
        old_col_section = get_oldcolumncombolist()


        if self.column_section in old_col_section or self.beam_section in old_beam_section:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
        if self.beam_fu < 410 or self.beam_fy < 230 or self.column_fu < 410 or self.column_fy < 230:
            logger.warning(" : You are using a section of grade that is not available in latest version of IS 2062")

        self.bolt_design()

        if self.top_angle_recommended != self.top_angle:
            logger.warning(": Based on thumb rules, a top angle of size %s may sufficient to provide stability to %s ",
                           self.top_angle_recommended, self.beam_section)

        self.top_angle_end_dist_column = (float(self.top_angle_A) - self.top_angle_t - self.top_angle_R1
                                          - self.top_angle_R2) / 2 + self.top_angle_R2
        self.top_angle_end_dist_beam = (float(self.top_angle_B) - self.top_angle_t - self.top_angle_R1
                                        - self.top_angle_R2) / 2 + self.top_angle_R2
        self.seat_angle_end_dist_beam = (float(self.angle_B) - self.angle_t - self.angle_R1
                                         - self.angle_R2) / 2 + self.angle_R2

        self.top_angle_end_dist_column = ConnectionCalculations.round_up_5(self.top_angle_end_dist_column)
        self.top_angle_end_dist_beam = ConnectionCalculations.round_up_5(self.top_angle_end_dist_beam)
        self.seat_angle_end_dist_beam = ConnectionCalculations.round_up_5(self.seat_angle_end_dist_beam)

        if self.top_angle_end_dist_column < self.min_end_dist:
            self.safe = False
            logger.error(": Detailing failure for the top angle")
            logger.warning(": Minimum end distance for the selected bolt is %2.2f mm [cl. 10.2.2] " % self.min_end_dist)
            logger.info(": Select bolt with lower grade/diameter to reduce minimum end distances")
            logger.info(": or increase leg A of the top angle")

        if self.top_angle_end_dist_beam < self.min_end_dist:
            self.safe = False
            logger.error(": Detailing failure for the top angle")
            logger.warning(": Minimum end distance for the selected bolt is %2.2f mm [cl. 10.2.2] " % self.min_end_dist)
            logger.info(": Select bolts with a lower grade/diameter to reduce the minimum end distances required")
            logger.info(": or Increase leg B of the top angle")

        if self.seat_angle_end_dist_beam < self.min_end_dist:
            self.safe = False
            logger.error(": Detailing failure for the seat angle")
            logger.warning(": Minimum end distance for the selected bolt is %2.2f mm [cl. 10.2.2] " % self.min_end_dist)
            logger.info(": Select bolts with a lower grade/diameter to reduce the minimum end distances required")
            logger.info(": or increase leg B of the seat angle")

        # To avoid bolts intersecting the column web in CFBF connectivity:
        if self.connectivity == "Column flange-Beam flange":
            if self.bolts_required == 3:
                self.bolts_required = 4
            elif self.bolts_required == 5:
                self.bolts_required = 8
                logger.info(": 5 bolts are required but 8 are being provided")
                logger.info(": Select bolts with a higher grade/diameter")
            elif self.bolts_required == 6:
                self.bolts_required = 8
                logger.info(": 6 bolts are required but 8 are being provided")
                logger.info(": It is recommended to increase the bolt grade or bolt diameter")
            elif self.bolts_required == 7:
                self.bolts_required = 8
                logger.info(": 7 bolts are required but 8 are being provided")
                logger.info(": It is recommended to increase the bolt grade or bolt diameter")

        self.bolt_group_capacity = round(self.bolts_required * self.bolt_value, 1)

        if self.connectivity == "Column web-Beam flange":
            limiting_angle_length = self.column_d - 2 * self.column_f_t - 2 * self.column_R1 - self.root_clearance_col

            self.angle_l = float(math.ceil(min(self.beam_b, limiting_angle_length)))
        elif self.connectivity == "Column flange-Beam flange":
            self.angle_l = float(math.ceil(min(self.beam_b, self.column_b)))

        if self.angle_t < 6:
            logger.warning(": Minimum thickness of 6 mm is recommended for the seat angle")
            logger.warning(": Please revise the seat angle section")

        # Determine single or double line of bolts
        length_avail = (self.angle_l - 2 * self.edge_dist)

        # Determine gauge for two bolts (to be used for top angle)
        self.gauge_two_bolt = length_avail

        self.num_rows = 1
        self.num_cols = max(self.bolts_required, 2)
        self.gauge = round(int(math.ceil(length_avail / (self.num_cols - 1))), 3)

        if self.gauge < self.min_gauge:
            self.num_rows = 2
            if self.bolts_required % 2 == 1:
                self.bolts_provided = self.bolts_required + 1
            else:
                self.bolts_provided = self.bolts_required
            self.num_cols = self.bolts_provided / 2
            if self.num_cols == 1:
                self.safe = False
                logger.error(": Detailing failure")
                logger.warning(
                    ": Minimum gauge distance for selected bolt is %2.2f mm [cl. 10.2.2] " % self.min_gauge)
                logger.warning(
                    ": Minimum edge distance for selected bolt is %2.2f mm [cl. 10.2.4.2]" % self.min_edge_dist)
                logger.warning(": Available length of the seat angle is %2.2f mm " % self.angle_l)
                logger.warning(": 2 bolts of the selected diameter cannot fit in the available length of the seat angle")
                logger.info(": Select bolts with a lower grade/diameter to reduce minimum gauge and edge distances required)")
            else:
                self.gauge = int(math.ceil(length_avail / (self.num_cols - 1)))
                if self.gauge < self.min_gauge:
                    self.safe = False
                    logger.error(": Detailing failure")
                    logger.error(": Bolt gauge %2.0f mm is less than the minimum gauge distance [cl. 10.2.2]" % self.gauge)
                    logger.warning(": Bolt gauge should be more than %2.2f mm " % self.min_gauge)
                    logger.warning(": Maximum gauge distance allowed is %2.2f mm " % self.max_spacing)
                    logger.info(": Select bolts with a higher grade/diameter to reduce the number of bolts)")
        if self.gauge > self.max_spacing:
            """
            Assumption: keeping minimum edge distance the same and increasing the number of bolts,
                to meet the max spacing requirement.
            1) set gauge = max spacing
            2) get approx (conservative) number of bolts per line based on this gauge
            3) use the revised number of bolts per line to get revised gauge distance

            The engineer can choose to use a different logic by keeping the number of bolts same,
                and increasing the edge distance.
            # gauge = max_spacing
            # edge_distance = (angle_l - (bolts_per_line-1)*gauge)/2
            """
            self.gauge = int(math.ceil(self.max_spacing))
            self.num_cols = int(math.ceil((length_avail / self.gauge) + 1))
            self.gauge = round(int(math.ceil(length_avail / (self.num_cols - 1))), 3)

        # End-user-developers may uncomment the below lines for an additional compatibility check
        # if self.connectivity == "Column flange-Beam flange":
        #     if self.gauge < self.column_w_t + 2*self.column_R1:
        #         self.safe = False
        #         logger.error(": Detailing failure")
        #         logger.warning(": Bolt passes through the column root")
        #         logger.info(": Increase the bolt gauge by reducing the number of bolts")

        if self.min_pitch > self.max_pitch:
            """
            Assumption: This unlikely case could occur when the minimum pitch (which is governed by the bolt diameter), 
            is greater than the maximum pitch (which is governed by thickness of connected member(s)).
            It is recommended to decrease the bolt diameter or increase the thickness of the connected members.
            """
            self.safe = False
            logger.error(": Calculated minimum pitch is greater than calculated (rounded) maximum pitch")
            logger.warning(": Bolt pitch should be more than  %2.2f mm " % self.min_pitch)
            logger.warning(": Bolt pitch should be less than  %2.2f mm " % self.max_pitch)
            logger.info(": Select bolts with a smaller diameter OR")
            logger.info(": Select a connected member with a greater thickness.)")

        self.bolts_provided = self.num_cols * self.num_rows
        self.bolt_group_capacity = round(self.bolts_provided * self.bolt_value, 1)

        if self.num_rows == 1:
            self.pitch = 0
        elif self.num_rows == 2:
            self.pitch = self.min_pitch
        self.end_dist = self.angle_A - self.angle_t - self.angle_R1 - self.root_clearance_sa - self.pitch
        self.end_dist = ConnectionCalculations.round_down_5(self.end_dist)
        self.pitch = (self.angle_A - self.angle_t - self.angle_R1 - self.root_clearance_sa - self.end_dist) * \
                     (self.num_rows - 1)
        if self.end_dist < self.min_end_dist:
            self.safe = False
            logger.error(": Detailing error")
            logger.error(": Calculated bolt end distance is smaller than the minimum end distance")
            logger.warning(": End distance should be more than  %2.2f mm " % self.min_end_dist)
            logger.info(": Select bolts with a smaller diameter OR")
            logger.info(": Select a seat angle with longer vertical leg.")

        root_3 = math.sqrt(3)

        # Approximate shear capacity of beam, Vd = A_v*F_yw/root_3/gamma_m0 cl. 8.4.1
        self.beam_shear_strength = round(
            self.beam_d * self.beam_w_t * float(self.beam_fy) / root_3 / self.gamma_m0 / 1000,
            1)

        if self.beam_shear_strength < float(self.shear_force):
            self.safe = False
            logger.error(": Shear capacity of the supported beam is not sufficient [cl. 8.4.1]")
            logger.warning(": Shear capacity of the supported beam should be at least %2.2f kN" % float(self.shear_force))
            logger.warning(": Beam design is outside the scope of this module")

        # length of bearing required at the root line of beam (b) = R*gamma_m0/t_w*f_yw
        # Rearranged equation from cl. 8.7.4
        bearing_length = round((float(self.shear_force) * 1000) * self.gamma_m0 / self.beam_w_t / self.angle_fy, 3)
        # logger.info(": Length of the bearing required at the root line of beam = " + str(bearing_length))

        # Required length of outstanding leg = bearing length + beam_col_clear_gap - beam_flange_thickness
        # (-beam_flange_thickness) comes from the 45 degree dispersion, but is conservatively not taken into account
        # while calculating the outstanding_leg_length
        self.outstanding_leg_length_required = bearing_length + self.beam_col_clear_gap

        if self.outstanding_leg_length_required > self.angle_B:
            self.safe = False
            logger.error(": Length of the outstanding leg of the seat angle is less than the required bearing length [cl. 8.7.4]")
            logger.warning(
                ": Outstanding leg length should be more than %2.2f mm" % self.outstanding_leg_length_required)
            logger.info(": Select seated angle with longer outstanding leg")

        """ comparing 0.6*shear strength (0.6*V_d) vs shear force V for calling moment capacity routine
        Shear capacity check cl. 8.4.1
        Shear capacity of the outstanding leg of cleat = A_v * f_yw / root_3 / gamma_m0
         = w*t*fy/gamma_m0/root_3
        """

        self.outstanding_leg_shear_capacity = round(
            self.angle_l * self.angle_t * self.angle_fy * 0.001 / root_3 * self.gamma_m0, 1)  # kN

        if self.outstanding_leg_shear_capacity < self.shear_force:
            self.safe = False
            required_angle_thickness_shear = math.ceil(
                self.shear_force * self.angle_t / self.outstanding_leg_shear_capacity)
            logger.error(": Shear capacity of outstanding leg of seated angle is insufficient [cl. 8.4.1]")
            logger.warning(
                ": Shear capacity of outstanding leg of seated angle is %2.2f kN" % float(
                    self.outstanding_leg_shear_capacity))
            logger.warning(
                ": Shear capacity should be more than factored shear force %2.2f kN" % float(self.shear_force))
            logger.info(": Select a seat angle with thickness greater than %2.1f mm" % required_angle_thickness_shear)

        # based on 45 degree dispersion cl. 8.7.1.3, stiff bearing length (b1) is calculated as
        # (stiff) bearing length on cleat (b1) = b - T_f (beam flange thickness) - r_b (root radius of beam flange)
        b1 = max(bearing_length - self.beam_f_t - self.beam_R1, bearing_length/2)

        # Distance from the end of bearing on cleat to root angle OR A TO B in Fig 5.31 in Subramanian's book
        b2 = max(b1 + self.beam_col_clear_gap - self.angle_t - self.angle_R1, 0)

        """Check moment capacity of outstanding leg

        Assumption:
            1) load is uniform over the stiff bearing length (b1)
            2) Moment (demand) is calculated at root of angle (at location B)
                due to load on the right of location B

        Shear force is compared against 0.6*shear capacity of outstanding leg to
            use appropriate moment capacity equation
        """

        if b1 > 0.1:
            self.moment_at_root_angle = round(float(self.shear_force) * (b2 / b1) * (b2 / 2), 1)

        if self.shear_force * self.shear_force < 1 or b2 == 0 or b1 < 0.1 or self.moment_at_root_angle < 0:
            self.safe = False
            logger.warning(": Calculated moment demand on the angle leg is %s " % self.moment_at_root_angle)
            logger.debug(": The algorithm used to calculate this moment could give erroneous values due to one or " +
                           "more of the following:")
            logger.debug(": a) Very low value of shear force ")
            logger.debug(": b) Large seat angle section and a low value of the gap between beam and column")
            logger.debug(": c) Large beam section and a low value of the shear force")
            logger.debug(": Please verify the results manually ")
            self.moment_at_root_angle = 0.0

        """
        Assumption
            1) beta_b (in the equation in cl. 8.2.1.2) = 1.0 as the outstanding leg is plastic section
            2) using Z_e (Elastic section modulus) for moment capacity
        """
        self.leg_moment_d = (self.angle_fy / self.gamma_m0) * (self.angle_l * self.angle_t ** 2 / 6) / 1000

        if float(self.shear_force) <= 0.6 * self.outstanding_leg_shear_capacity:
            angle_moment_capacity_clause = "cl. 8.2.1.2"
            self.is_shear_high = False
            # to avoid irreversible deformation (in case of cantilever),
            # under service-ability loads, moment_d shall be less than 1.5*Z_e*f_y/gamma_m0
            leg_moment_d_limiting = 1.5 * (self.angle_fy / self.gamma_m0) * (
                self.angle_l * self.angle_t ** 2 / 6) / 1000
            angle_outst_leg_mcapacity = min(self.leg_moment_d, leg_moment_d_limiting)
        else:
            self.is_shear_high = True
            angle_moment_capacity_clause = "cl. 8.2.1.3"
            """ cl. 8.2.1.3
            if shear force > 0.6 * shear strength of outstanding leg:
            The moment capacity of the outstanding leg is calculated as,
            M_d = M_dv (as defined in cl. 9.2)
            cl. 9.2.2 for plastic section

            Assumption :
            M_fd=0 as the shear resiting area and moment resisting area are the same,
                for the cross section of the outstanding leg
            Thus,
            M_dv = min ((1-beta)*M_d, 1.2*Z_e*f_y/gamma_m0)
            where, beta = ((2V/V_d) - 1)^2
            """
            leg_moment_d_limiting = 1.2 * (self.angle_fy / self.gamma_m0) * (
                self.angle_l * self.angle_t ** 2 / 6) / 1000
            beta_moment = ((2 * float(self.shear_force) / self.outstanding_leg_shear_capacity) - 1) ** 2
            angle_outst_leg_mcapacity = min((1 - beta_moment) * self.leg_moment_d, leg_moment_d_limiting)
            self.moment_high_shear_beta = beta_moment

        self.moment_capacity_angle = round(angle_outst_leg_mcapacity, 1)

        if self.moment_capacity_angle < self.moment_at_root_angle:
            self.safe = False
            logger.error(": Moment capacity of the outstanding leg of the seat angle is not sufficient "
                         + angle_moment_capacity_clause)
            logger.warning(": Moment capacity should be at least %2.2f kN-mm" % self.moment_at_root_angle)
            logger.info(": Increase thickness or decrease length of the outstanding leg of the seat angle")

        """ Check for local buckling capacity of web of supported beam (cl. 8.7.3.1)
        Variables are prefixed with bwlb: beam web local buckling

        Assumptions:
                1) Effective length of web of supported beam (8.7.1.5) [KL = L]
                2) steel_E = 200000 MPa
                3) Effective sectional area for computing design compressive strength P_d (7.1.2)
                is taken as indicated in (8.7.3.1)
        """

        # Area of cross section of beam web:
        bwlb_b1 = b1  # width of stiff bearing on flange (8.7.1.3)

        # Dispersion of the load through the web at 45 degree, to the level of half the depth of the cross-section
        bwlb_n1 = self.beam_d / 2 - self.beam_R1 - self.beam_f_t

        # Effective length of web of supported beam (8.7.1.5) assumed KL = L
        bwlb_KL = self.beam_d - 2 * self.beam_f_t - 2 * self.beam_R1

        # For calculating design compressive strength of web of supported beam (7.1.2.1)
        steel_E = 200000  # MPa
        bwlb_lambda = (bwlb_KL * 2 * root_3 / self.beam_w_t / math.pi) * math.sqrt(float(self.beam_fy) / steel_E)
        bwlb_alpha = 0.49  # Imperfection factor for buckling class 'c' (IS 800 - Table 7 and 8.7.3.1)
        bwlb_phi = 0.5 * (1 + bwlb_alpha * (bwlb_lambda - 0.2) + bwlb_lambda ** 2)
        bwlb_chi = max((bwlb_phi + (bwlb_phi ** 2 - bwlb_lambda ** 2) ** 0.5) ** (-1), 1.0)
        bwlb_f_cd = bwlb_chi * float(self.beam_fy) / self.gamma_m0

        # Design compressive strength (7.1.2)
        bwlb_P_d = (bwlb_b1 + bwlb_n1) * bwlb_f_cd
        self.beam_web_local_buckling_capacity = bwlb_P_d

        if self.beam_web_local_buckling_capacity < self.shear_force:
            self.safe = False
            logger.error(": Local buckling capacity of the web of the supported beam is less than the shear force [cl. 8.7.3.1]")
            logger.warning(": Local buckling capacity is %2.2f kN-mm" % self.beam_web_local_buckling_capacity)
            logger.info(": Increase the length of the outstanding leg of the seat angle to increase the stiff bearing length")

        # End of calculation
        # ---------------------------------------------------------------------------
        self.sa_output()

        if self.output_dict['SeatAngle']['status'] is True:
            logger.info(": Overall seated angle connection design is safe")
            logger.debug(": =========End Of design===========")
        else:
            logger.error(": Design is not safe")
            logger.debug(": =========End Of design===========")

        return self.output_dict
