'''
Created on 2-Sept-2016
@author: jayant patil
'''

''' 
References:

Design of Steel Structures (DoSS) - N. Subramanian
First published 2008, 14th impression 2014
    Chapter 5: Bolted Connections
    Example 5.14, Page 406

IS 800: 2007
    General construction in steel - Code of practice (Third revision)
'''

'''
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

'''

import math
import logging
import model
from PyQt4.Qt import QString

logger = logging.getLogger("osdag.SeatAngleCalc")

# TODO docstrings for functions
# TODO block shear check
# TODO test cases
# TODO add input validation to select only angles which can accomodate 2 lines of bolts
# TODO check if a clause exists on minimum angle thickness
# TODO calculate other geometry params for SA
# TODO check code block for min ply thk
# TODO include bolt design function
# TODO SCI minimum 3 bolts (chapter 6 in SCI - for fin plate)
# TODO check reduction factors for bolt group capacity
# TODO area of bolts for smaller bolt diameters
    # 5, 6, 8, 10 - bolt_hole_clearance() and bolt_shear() need to be updated
# TODO add logger messages

class SeatAngleConnection(object):
    """Perform design and detailing checks for seated angle connection.

    """

    def __init__(self):
        pass

    def sa_params(self, input_dict):
        """Intialise variables to use in calculations from input dictionary.

        Assumptions:
            angle f_y and f_u are equal to beam f_y and f_u respectively
            clear gap = 5 + 5 mm
        """
        # Initialise Design Preferences
        self.gamma_mb = 1.25  # partial safety factor for material - resistance of connection - bolts
        self.gamma_m0 = 1.1  # partial safety factor for material - resistance governed by yielding or buckling
        self.gamma_m1 = 1.25 # partial safety factor for material - resistance governed by ultimate stress
        self.bolt_hole_type = 1  # standard bolt hole
        # self.bolt_hole_type = 0  # oversize bolt hole
        self.custom_hole_clearance = None  # user defined hole clearance, if any
        self.clear_gap = 5 + 5  # clearance + tolerance
        # min edge distance multiplier based on edge type (Cl 10.2.4.2)
        self.min_edge_multiplier = 1.5  # rolled, machine-flame cut, sawn and planed edges
        # self.min_edge_multiplier = 1.7  # sheared or hand flame cut edges

        # Intialise seated angle connection parameters
        self.top_angle = "ISA 100X65X8"
        self.connectivity = input_dict['Member']['Connectivity']
        self.beam_section = input_dict['Member']['BeamSection']
        self.column_section = input_dict['Member']['ColumnSection']
        self.beam_fu = input_dict['Member']['fu (MPa)']
        self.beam_fy = input_dict['Member']['fy (MPa)']
        self.angle_fy = self.beam_fy
        self.angle_fu = self.beam_fu
        self.shear_force = input_dict['Load']['ShearForce (kN)']
        self.bolt_diameter = input_dict['Bolt']['Diameter (mm)']
        self.bolt_type = input_dict['Bolt']['Type']
        self.bolt_grade = input_dict['Bolt']['Grade']
        self.angle_sec = input_dict['Angle']["AngleSection"]

        if connectivity == "Beam-Beam":
            self.dict_beam_data = model.get_beamdata(self.beam_section)
            self.dict_column_data = model.get_beamdata(self.column_section)
        else:
            self.dict_beam_data = model.get_beamdata(self.beam_section)
            self.dict_column_data = model.get_columndata(self.column_section)
        self.dict_angle_data = model.get_angledata(angle_sec)

        self.beam_w_t = float(self.dict_beam_data[QString("tw")])  # beam web thickness
        self.beam_f_t = float(self.dict_beam_data[QString("T")])  # beam flange thickness
        self.beam_d = float(self.dict_beam_data[QString("D")])  # beam depth
        self.beam_w_f = float(self.dict_beam_data[QString("B")])  # beam width
        self.beam_R1 = float(self.dict_beam_data[QString("R1")])  # beam root radius
        self.column_f_t = float(dict_column_data[QString("T")])  # column flange thickness
        self.angle_t = float(dict_angle_data[QString("t")])  # angle thickness
        self.angle_A = float(dict_angle_data[QString("A")])  # longer leg of unequal angle
        self.angle_B = float(dict_angle_data[QString("B")])  # shorter leg of unequal angle
        self.angle_R1 = float(dict_angle_data[QString("R1")])

        self.safe = True

    def sa_output(self):
        """Create and return dictionary of output parameters."""
        self.output_dict = {}
        self.output_dict['SeatAngle'] = {
            "Length (mm)": self.angle_l,
            "Moment Demand (kNm)": self.moment_at_root_angle,
            "Moment Capacity (kNm)": self.moment_capacity_angle,
            "Shear Demand (kN/mm)": self.shear_force,
            "Shear Capacity (kN/mm)": self.outstanding_leg_shear_strength,
            "Beam Shear Strength (kN/mm)": self.beam_shear_capacity
            "Top Angle": self.top_angle
        }

        self.output_dict['Bolt'] = {
            "status": self.safe,
            "Shear Capacity (kN)": self.bolt_shear_capacity,
            "Bearing Capacity (kN)": self.bolt_bearing_capacity,
            "Capacity of Bolt (kN)": self.bolt_value,
            "Bolt group capacity (kN)": self.bolt_group_capacity,
            "No. of Bolts": self.bolts_required,
            # TODO remove hardcoded values
            "No. of Row": self.num_rows,
            "No. of Column": self.num_cols,
            "Pitch Distance (mm)": self.pitch,
            "Gauge Distance (mm)": self.gauge,
            "End Distance (mm)": self.min_end_dist,
            "Edge Distance (mm)": self.min_edge_dist,

            # output dictionary items for design report
            "bolt_fu": self.bolt_fu,
            "bolt_dia": self.bolt_diameter,
            "k_b": self.k_b,
            "beam_w_t": self.beam_w_t,
            "beam_fu": self.beam_fu,
            "shearforce": self.shear_force,
            "hole_dia": self.bolt_hole_diameter
        }

    def bolt_shear(self, bolt_diameter, number_of_bolts, bolt_fu):
        """Calculate and return bolt shear capacity (float) based on IS 800, Cl 10.3.3.

        Bolt factored shear capacity = bolt_fu * number_of_bolts * Area_bolt_net_tensile / (square_root(3) * gamma_mb)

        Assumptions:
            1)for all bolts, shear plane passes through threaded area
            2)for all bolts, tensile stress area equals the threaded area
            3)reduction factors for long joints, large grip lengths, packing plates are not applicable
            4) values for tensile stress area (mm^2) are taken from Table 5.9 in DoSS - N. Subramanian
        """
        bolt_area = {
            '12': 84.3,
            '16': 157,
            '20': 245,
            '22': 303,
            '24': 353,
            '27': 459,
            '30': 561,
            '36': 817
        }[str(bolt_diameter)]
        bolt_nominal_shear_capacity = bolt_fu * number_of_bolts * bolt_area / math.sqrt(3) / 1000
        return round(bolt_nominal_shear_capacity / self.gamma_mb, 3)

    def bolt_bearing(self, bolt_diameter, number_of_bolts, thickness_plate, k_b, bolt_fu):
        """Calculate and return factored bearing capacity of single (float) based on IS 800, Cl 10.3.4.

        Bolt factored bearing capacity = 2.5 * k_b * bolt_diameter * sum_thickness_of_connecting_plates * f_u / gamma_mb
        """
        bolt_nominal_bearing_capacity = 2.5 * k_b * bolt_diameter * number_of_bolts * thickness_plate * bolt_fu / (1000)
        return round(bolt_nominal_bearing_capacity / self.gamma_mb, 3)

    def bolt_hole_clearance(self, bolt_diameter):
        """Calculate and return bolt hole clearance as int.

        INPUTS:
            bolt_diameter: int

        RETURN:
            hole_clearance: int

        Reference:
            IS 800, Table 19 (Cl 10.2.1) : Clearances for Fastener Holes
        """
        if self.bolt_hole_type == 1:  # standard hole
            hole_clearance = {
                12: 1,
                14: 1,
                16: 2,
                18: 2,
                20: 2,
                22: 2,
                24: 2,
                30: 3,
                36: 3
            }[bolt_diameter]
        elif self.bolt_hole_type == 0:  # over size hole
            hole_clearance = {
                12: 3,
                14: 3,
                16: 4,
                18: 4,
                20: 4,
                22: 4,
                24: 6,
                30: 8,
                36: 8
            }[bolt_diameter]
        if self.custom_hole_clearance is not None:
            hole_clearance = self.custom_hole_clearance  # units: mm
        return hole_clearance  # units: mm

    def bolt_design(self):
        """Calculate bolt capacities and layout."""
        self.angle_root_clearance = 5
        self.bolt_hole_diameter = self.bolt_diameter + bolt_hole_clearance(self.bolt_diameter)

        self.bolt_fu = int(self.bolt_grade) * 100

        # Minimum pitch and gauge IS 800 Cl 10.2.2
        self.min_pitch = int(2.5 * self.bolt_diameter)
        self.min_gauge = int(2.5 * self.bolt_diameter)

        # Min edge and end distances IS 800 Cl 10.2.4.2
        self.min_end_dist = int(self.min_edge_multiplier * self.bolt_hole_diameter)
        self.min_edge_dist = int(self.min_edge_multiplier * self.bolt_hole_diameter)

        # TODO: rethink rounding off of MINIMUM distances
        # round off the actual distances and check against minimum
        if self.min_pitch % 10 != 0 or self.min_gauge % 10 != 0:
            self.min_pitch = (self.min_pitch / 10) * 10 + 10
            self.min_gauge = (self.min_gauge / 10) * 10 + 10
        if self.min_edge_dist % 10 != 0:
            self.min_edge_dist = (self.min_edge_dist / 10) * 10 + 10
            self.min_end_dist = (self.min_end_dist / 10) * 10 + 10

        self.edge_dist = self.min_edge_dist
        self.end_dist = self.min_end_dist
        if not self.pitch:
            self.pitch = self.min_pitch
        # Calculation of k_b
        self.k_b = min(self.end_dist / float(3 * self.bolt_hole_diameter),
                       self.pitch / float(3 * self.bolt_hole_diameter) - 0.25,
                       self.bolt_fu / float(self.angle_fu),
                       1)
        self.k_b = round(self.k_b, 3)

        # Bolt capacity
        self.thickness_governing = min(beam_w_t.real, angle_t.real)
        self.bolt_shear_capacity = bolt_shear(self.bolt_diameter, number_of_bolts=1, self.bolt_fu).real
        self.bolt_bearing_capacity = bolt_bearing(self.bolt_diameter, number_of_bolts=1, self.thickness_governing,
                                                  self.beam_fu, self.k_b).real
        self.bolt_value = min(self.bolt_shear_capacity, self.bolt_bearing_capacity)
        self.bolts_required = math.ceil(self.shear_force / self.bolt_value)

        # TODO SCI minimum 3 bolts (chapter 6 in SCI - for fin plate)
        # assumption: provide minimum 3 bolts based on SCI guidelines
        # check if odd number of bolts can be allowed
        if self.bolts_required <= 2:
            self.bolts_required = 3
            # print "Number of bolts required = " + str(bolts_required)

        self.bolt_group_capacity = self.bolts_required * self.bolt_value
        # print "bolt group capacity = " + str(self.bolt_group_capacity)

        # Max spacing IS 800 Cl 10.2.3.1
        self.max_spacing = int(min(32 * self.thickness_governing, 300))
        # print "Max spacing = " + str(self.max_spacing)

        # Max spacing IS 800 Cl 10.2.4.3
        self.max_edge_dist = int((12 * self.thickness_governing * math.sqrt(250 / self.angle_fy)).real)
        # print "Max edge distance = " + str(self.max_edge_dist)

        # Cl 10.2.4.3 in case of corrosive influences, the maximum edge distance shall not exceed
        # 40mm plus 4t, where t is the thickness of the thinner connected plate.
        # self.max_edge_dist = min(self.max_edge_dist, 40 + 4*self.thickness_governing)

    def block_shear_check(self):
        # TODO discuss the block shear case(s) with team. Non-trivial assumptions involved.
        # TODO add block shear check to seat_angle_connection()
        """Calculate and return block shear capacity of seated angle.

         Assumption:
            1) horizontal leg does not contribute to block shear capacity (very conservative)
        """
        root_3 = math.sqrt(3)
        thickness = self.angle_t
        # pitch = self.pitch
        end_dist = self.end_dist
        edge_dist = self.edge_dist
        bolt_hole_diameter = self.bolt_hole_diameter
        f_y = self.angle_fy
        f_u = self.angle_fu
        gamma_m0 = self.gamma_m0
        gamma_m1 = self.gamma_m1
        number_rows = self.num_rows
        # number_cols = self.num_cols
        vertical_leg_length = self.angle_A

        area_vg = thickness * (vertical_leg_length - end_dist)
        area_vn = thickness * (vertical_leg_length - end_dist - (number_rows - 1 + 0.5) * bolt_hole_diameter)
        area_tg = thickness * edge_dist
        area_tn = thickness * (edge_dist - 0.5 * bolt_hole_diameter)

        block_shear_db1 = area_vg * f_y / (root_3 * gamma_m0) + 0.9 * area_tn * f_u / gamma_m1
        block_shear_db2 = 0.9 * area_vn * f_u(root_3 * gamma_m1) + area_tg * f_y / gamma_m0
        block_shear_db = min(block_shear_db1, block_shear_db2)
        block_shear_db = round(block_shear_db / 1000, 3)

        return block_shear_db

    def seat_angle_connection(self, input_dict):
        """ Perform design and detailing checks based on input dict and return a dict containing results of calculations.

        INPUTS:
            input_dict: dictionary

        RETURNS:
            output_dict: dictionary

        Algorithm:
            1) Initialise variables to use
            2) Bolt Design (layout and spacing)
            3) Determine length of outstanding leg of seated angle
            4) Determine shear strength of outstanding leg and compare with capacity
        """
        self.sa_params(input_dict)
        self.bolt_design()

        # ------------------------------------------------------------------------
        self.angle_l = self.beam_w_f

        # Determine single or double line of bolts
        length_avail = (self.angle_l - 2 * self.edge_dist)

        # Determine number of bolt lines:
        self.num_rows = 1
        self.num_cols = self.bolts_required
        self.gauge = round(length_avail / (self.num_cols - 1), 3)
        if self.gauge < self.min_gauge:
            self.num_rows = 2
            self.num_cols = int((self.bolts_required + 1) / 2)
            self.gauge = round(length_avail / (self.num_cols - 1), 3)
            if self.gauge < self.min_gauge:
                logger.error(
                    ": Calculated gauge length with 2 rows for selected bolt size is less than minimum gauge lenth")
                logger.warning(": Gauge length should be more than  %2.2f mm " % (self.min_gauge))
                logger.warning(": Maximum gauge length allowed is %2.2f mm " % (self.max_spacing))
                logger.info(
                    ": Increase the bolt diameter (size) or bolt grade (to decrease the number of required bolts)")
        if self.gauge > self.max_spacing:
            """
            Assumption: keeping minimum edge distance the same and increasing the number of bolts,
                to meet the max spacing requirement.
            1) set gauge = max spacing
            2) get approx (conservative) number of bolts per line based on this gauge
            3) use the revised number of bolts per line to get revised gauge length

            The engineer can choose to use a different logic by keeping the number of bolts same,
                and increasing the edge distance.
            # gauge = max_spacing
            # edge_distance = (angle_l - (bolts_per_line-1)*gauge)/2
            """
            self.gauge = self.max_spacing
            self.num_cols = math.ceil((length_avail / gauge) + 1)
            self.gauge = round(length_avail / (self.num_cols - 1), 3)

        self.pitch = (self.num_rows-1)*(self.angle_A - self.end_dist - self.angle_t - self.angle_R1 - self.angle_root_clearance)

        # length of bearing required at the root line of beam (b) = R*gamma_m0/t_w*f_yw
        # Rearranged equation from Cl 8.7.4
        bearing_length = round((self.shear_force * 1000) * self.gamma_m0 / self.beam_w_t / self.angle_fy, 3)
        print "Length of bearing required at the root line of beam = " + str(bearing_length)

        # Required length of outstanding leg = bearing length + clear_gap,
        outstanding_leg_length_required = bearing_length + self.clear_gap
        print "Outstanding leg length = " + str(outstanding_leg_length_required)

        if outstanding_leg_length_required > self.angle_B:
            self.safe = False
            logger.error(": Connection is not safe")
            logger.warning(
                ": Outstanding leg length of seated angle should be more than " + str(outstanding_leg_length_required))
            print "Error: Seated angle's outstanding leg length needs to be increased"

        """ comparing 0.6*shear strength (0.6*V_d) vs shear force V for calling moment capacity routine
        Shear capacity check Cl 8.4.1
        Shear capacity of the outstanding leg of cleat = A_v * f_yw / root_3 / gamma_m0
         = w*t*fy/gamma_m0/root_3
        """
        root_3 = math.sqrt(3)
        self.outstanding_leg_shear_strength = round(
            self.angle_l * self.angle_t * self.angle_fy * 0.001 / root_3 * self.gamma_m0, 3)  # kN
        print "Shear strength of outstanding leg of Seated Angle = " + str(self.outstanding_leg_shear_strength)

        if self.outstanding_leg_shear_strength < self.shear_force:
            self.safe = False
            logger.error(": Shear capacity is insufficient")
            logger.warning(": Shear capacity should be at least " + str(self.shear_force))
            print "Error: Shear capacity is insufficient"

        # based on 45 degree dispersion Cl 8.7.1.3, stiff bearing length (b1) is calculated as
        # (stiff) bearing length on cleat (b1) = b - T_f (beam flange thickness) - r_b (root radius of beam flange)
        b1 = bearing_length - self.beam_f_t - self.beam_R1
        print "Length of bearing on cleat" + str(b1)

        # Distance from the end of bearing on cleat to root angle OR A TO B = b2
        b2 = b1 + self.clear_gap - self.angle_t - self.angle_R1
        print "Distance A to B = " + str(b2)

        """Check moment capacity of outstanding leg

        Assumption:
            1) load is uniform over the stiff bearing length (b1)
            2) Moment (demand) is calculated at root of angle (at location B)
                due to load on the right of location B

        Shear force is compared against 0.6*shear capacity of outstanding leg to
            use appropriate moment capacity equation
        """

        self.moment_at_root_angle = round(self.shear_force * (b2 / b1) * (b2 / 2), 3)
        # print "Moment at root angle = " + str(self.moment_at_root_angle)

        self.moment_capacity_angle = round( 1.2 * (self.angle_fy / self.gamma_m0) * self.angle_l * (self.angle_t ** 2) * 0.001 / 6, 3)
        # print "Moment capacity =" + str(self.moment_capacity_angle)

        """
        Assumption
            1) beta_b (in the equation in Cl 8.2.1.2) = 1.0 as the outstanding leg is plastic section
            2) using Z_p (plastic section modulus) for moment capacity
        """
        leg_moment_d = (self.angle_fy / self.gamma_m0) * (self.angle_l * (self.angle_t ** 2) / 4)

        if self.shear_force <= 0.6 * self.outstanding_leg_shear_strength:
            # to avoid irreversible deformation (in case of cantilever),
            # under serviceablitiy loads, moment_d shall be less than 1.5*Z_e*f_y/gamma_m0
            leg_moment_d_limiting = 1.5 * (self.angle_fy / self.gamma_m0) * (self.angle_l * (self.angle_t ** 2) / 6)
            angle_outst_leg_mcapacity = min(leg_moment_d, leg_moment_d_limiting)
        else:
            """ Cl 8.2.1.3
            if shear force > 0.6 * shear strength of outstanding leg:
            The moment capacity of the outstanding leg is calculated as,
            M_d = M_dv (as defined in Cl 9.2)
            Cl 9.2.2 for plastic section

            Assumption :
            M_fd=0 as the shear resiting area and moment resisting area are the same,
                for the cross section of the outstanding leg
            Thus,
            M_dv = min ((1-beta)*M_d, 1.2*Z_e*f_y/gamma_m0)
            where, beta = ((2V/V_d) - 1)^2
            """
            leg_moment_d_limiting = 1.2 * (self.angle_fy / self.gamma_m0) * (self.angle_l * (self.angle_t ** 2) / 6)
            beta_moment = ((2 * self.shear_force / self.outstanding_leg_shear_strength) - 1) ** 2
            angle_outst_leg_mcapacity = min((1 - beta_moment) * leg_moment_d, leg_moment_d_limiting)

        self.moment_capacity_angle = round(angle_outst_leg_mcapacity, 3)
        print "Moment capacity = " + str(self.moment_capacity_angle)

        if self.moment_capacity_angle < self.moment_at_root_angle:
            self.safe = False
            logger.error(": Connection is not safe")
            logger.warning(": Moment capacity should be at least " + str(moment_at_root_angle))
            print "Error: Connection not safe"

        # shear capacity of beam, Vd = A_v*F_yw/root_3/gamma_m0
        self.beam_shear_capacity = round(self.beam_d * self.beam_w_t * self.beam_fy / root_3 / self.gamma_m0 / 1000, 3)
        print "Beam shear capacity = " + str(self.beam_shear_capacity)

        if self.beam_shear_capacity < self.shear_force:
            self.safe = False
            logger.error(": Beam shear capacity is insufficient")
            logger.warning(": Beam shear capacity should be at least " + str(self.shear_force + "kN"))
            logger.warning(": Beam design is outside the scope of this module")

        # End of calculation
        #---------------------------------------------------------------------------
        self.sa_output()

        if output_dict['Bolt']['status'] == True:
            logger.info(": Overall seated angle connection design is safe \n")
            logger.debug(": =========End Of design===========")
        else:
            logger.error(": Design is not safe \n ")
            logger.debug(": =========End Of design===========")

        return self.output_dict

## Test Case(s) below:
# if __name__ == '__main__':
#     output = SeatAngleConn()
#     print output