import math


class ConnectionCalculations(object):
    """Perform common calculations for connection components in abstract class.

    Attributes:
        k_b (float) - factor for bolt bearing capacity calculation
        bolt_hole_diameter (int)
        bolt_fu (int)
        angle_fu (int)
        angle_fy (int)
        min_pitch (int)
        min_gauge (int)
        min_edge_dist (int)
        min_end_dist (int)
        max_pitch (int)
        max_edge_dist (int)
        end_dist (int)
        pitch (int)

    Note:
        This is the parent class for each connection module's calculation class.

    """

    def __init__(self):
        self.k_b = 1.0
        self.bolt_hole_diameter = 1.0
        self.bolt_fu = 1.0
        self.angle_fu = 1.0
        self.angle_fy = 1.0
        self.max_spacing = 1.0
        self.min_pitch = 1.0
        self.min_gauge = 1.0
        self.min_edge_dist = 1.0
        self.min_end_dist = 1.0
        self.max_pitch = 1.0
        self.max_edge_dist = 1.0
        self.end_dist = 1.0
        self.pitch = 1.0

    @staticmethod
    def bolt_hole_clearance(bolt_hole_type, bolt_diameter):
        """Calculate bolt hole clearance.

        Args:
            bolt_hole_type (string)
            bolt_diameter (int)            

        Returns:
            hole_clearance (int)

        Note:
            Reference:
            IS 800, Table 19 (Cl 10.2.1) : Clearances for Fastener Holes

        """
        hole_clearance = 0
        if bolt_hole_type == "Standard":  # standard hole
            hole_clearance = {
                12: 1,
                16: 2,
                20: 2,
                24: 2,
                30: 3,
                36: 3
            }[bolt_diameter]
        elif bolt_hole_type == "Over-sized":  # over sized hole
            hole_clearance = {
                12: 3,
                16: 4,
                20: 4,
                24: 6,
                30: 8,
                36: 8
            }[bolt_diameter]

        return hole_clearance  # units: mm

    @staticmethod
    def bolt_shear(bolt_diameter, number_of_bolts, bolt_fu):
        """Calculate factored shear capacity of bolt(s) based on IS 800, Cl 10.3.3.

        Args:
            bolt_diameter (int)
            number_of_bolts (int)
            bolt_fu (int)

        Returns:
            Factored shear capacity of bolt(s) as float.

        Note:
            Bolt factored shear capacity = bolt_fu * number_of_bolts * Area_bolt_net_tensile / square_root_3 / gamma_mb
            Assumptions:
            1)for all bolts, shear plane passes through threaded area
            2)for all bolts, tensile stress area equals the threaded area
            3)reduction factors for long joints, large grip lengths, packing plates are not applicable
            4) values for tensile stress area (mm^2) are taken from Table 5.9 in DoSS - N. Subramanian

        """
        gamma_mb = 1.25
        bolt_area = {
            '12': 84.3,
            '16': 157,
            '20': 245,
            # '22': 303,
            '24': 353,
            # '27': 459,
            '30': 561,
            '36': 817
        }[str(bolt_diameter)]
        bolt_nominal_shear_capacity = bolt_fu * number_of_bolts * bolt_area / math.sqrt(3) / 1000
        return round(bolt_nominal_shear_capacity / gamma_mb, 1)

    @staticmethod
    def proof_load_F_0(bolt_diameter, bolt_fu):
        """

        Args:
            bolt_diameter:
            bolt_fu:

        Returns:

        """
        proof_stress = 0.7 *float( bolt_fu)  # proof stress
        # bolt_area_threads - area of bolt at threads
        bolt_area_threads = {
            '12': 84.3,
            '16': 157,
            '20': 245,
            '22': 303,
            '24': 353,
            '27': 459,
            '30': 561,
            '36': 817
        }[str(bolt_diameter)]
        F_0 = bolt_area_threads * proof_stress / 1000  # (Kn)
        return F_0

    @staticmethod
    def calculate_k_h(bolt_hole_type):
        """

        Args:
            bolt_hole_type (string):

        Returns:

        """
        k_h = {"Standard": 1.0, "Over-sized": 0.85}
        return k_h[bolt_hole_type]

    @staticmethod
    def bolt_shear_friction_grip_bolt(bolt_diameter, bolt_fu, mu_f, n_e, bolt_hole_type):
        """ Calculate design shear capacity of a single Friction Grip Bolt bolt(s) based on Cl 10.4.3
        Args:
             bolt_diameter (int)
             bolt_fu (int) - ultimate stress of bolt Fu
             mu_f(float) - coefficient of friction/ slip factor
             n_e (int) - number of effective interfaces offering resistance to slip
             bolt_hole_type (string) - "Standard" or "Over-sized"

        Returns:

            v_db - Factored shear capacity of Friction Grip Bolt bolt as float

        Note:
            Assumptions:
            1) slip is not allowed at ultimate load
            2) there is no tension acting on bolt
            3) area of bolt at threaded portion (mm^2) is taken from DSS- N. Subramanian table 5.9 (pg 348)
            4) the provision of long joints is applicable - Cl 10.4.3.1 and is calculated according to Cl 10.3.3.1
            5) Minimum bolt tension (proof load) at installation assumed as bolt_area_threads*proof_stress
            6) Reduction factor for long joints not calculated in this function

        """
        gamma_mf = 1.25  # factor of safety at ultimate load
        # F_0 - minimum bolt tension (proof load) at bolt installation
        # proof load (Kn)(minimum bolt tension)
        # F_0 = bolt_area_threads * proof_stress / 1000  # (Kn)
        # k_h = {
        #     "Standard": 1.0,
        #     "Over-sized": 0.85
        # }[bolt_hole_type]
        F_0 = ConnectionCalculations.proof_load_F_0(bolt_diameter, bolt_fu)
        k_h = ConnectionCalculations.calculate_k_h(bolt_hole_type)
        v_nsf = mu_f * n_e * k_h * F_0  # nominal shear capacity of bolt
        v_dsf = v_nsf / gamma_mf
        return v_dsf

    def calculate_kb(self):
        """Calculate k_b for bearing capacity of bolt

        Args:            

        Returns:

        """
        self.k_b = min(self.end_dist / float(3 * self.bolt_hole_diameter),
                       self.pitch / float(3 * self.bolt_hole_diameter) - 0.25,
                       self.bolt_fu / float(self.angle_fu),
                       1)
        self.k_b = round(self.k_b, 3)

    @staticmethod
    def bolt_bearing(bolt_diameter, number_of_bolts, thickness_plate, k_b, plate_fu):
        """Calculate factored bearing capacity of bolt(s) based on IS 800, Cl 10.3.4.

        Args:
            bolt_diameter (int)
            number_of_bolts (int)
            thickness_plate (float)
            k_b (float)
            plate_fu (int)

        Returns:
             Factored bearing capacity of bolt(s) as float.

        Note:
            Bolt bearing capacity = 2.5 * k_b * bolt_diameter * sum_thickness_of_connecting_plates * f_u / gamma_mb
            #TODO : implement reduction factor 0.7 for over size holes - Cl 10.3.4

        """
        gamma_mb = 1.25
        bolt_nominal_bearing_capacity = 2.5 * float(str(k_b)) * bolt_diameter * number_of_bolts \
                                        * thickness_plate * plate_fu / 1000
        return round(bolt_nominal_bearing_capacity / gamma_mb, 1)

    @staticmethod
    def round_up_5(distance):
        """Calculate and return the nearest multiple of 5 greater than input variable.
        
        Args:
            distance (float): bolt distance in mm

        Returns:
            round_up_distance (float): bolt distance in mm, multiple of 5 mm.

        """
        int_distance = int(distance)
        round_up_distance = int_distance
        if int_distance % 5 != 0:
            round_up_distance = ((int_distance / 5) + 1) * 5
        return round_up_distance

    @staticmethod
    def round_down_5(distance):
        """Calculate and return the nearest multiple of 5 lower than input variable.

        Args:
            distance (float): bolt distance in mm

        Returns:
            round_down_distance (float): bolt distance in mm, multiple of 5 mm.

        """
        int_distance = int(distance)
        round_down_distance = int_distance
        if int_distance % 5 != 0:
            round_down_distance = (int(int_distance / 5)) * 5
        return round_down_distance

    def calculate_distances(self, bolt_diameter, bolt_hole_diameter, min_edge_multiplier, thickness_governing_min,
                            is_environ_corrosive):
        """Calculate minimum pitch, gauge, end and edge distances.

        Args:
            bolt_diameter (int)
            bolt_hole_diameter (int)
            min_edge_multiplier (float)
            thickness_governing_min (float)
            is_environ_corrosive (string) -- "Yes" or "No"

        Returns:
            None

        Note:
            # Minimum pitch and gauge IS 800 Cl 10.2.2
            # Min edge and end distances IS 800 Cl 10.2.4.2
        """
        # Minimum pitch and gauge IS 800 Cl 10.2.2
        self.min_pitch = int(2.5 * bolt_diameter)
        self.min_gauge = int(2.5 * bolt_diameter)

        # Min edge and end distances IS 800 Cl 10.2.4.2
        self.min_end_dist = int(math.ceil(min_edge_multiplier * bolt_hole_diameter))
        self.min_edge_dist = int(math.ceil(min_edge_multiplier * bolt_hole_diameter))

        # Max spacing IS 800 Cl 10.2.3.1
        self.max_spacing = math.ceil(min(32 * thickness_governing_min, 300))

        # Max pitch IS 800 Cl 10.2.3.2
        self.max_pitch = math.ceil(min(12 * thickness_governing_min, 200))

        # Max pitch of outer line of bolts IS 800 Cl 10.2.3.3
        # assuming that this limit applies to the pitch of interior bolts as well
        self.max_pitch = math.ceil(min(100 + 4 * thickness_governing_min, self.max_pitch))

        # Max spacing IS 800 Cl 10.2.4.3
        self.max_edge_dist = math.ceil((12 * thickness_governing_min * math.sqrt(250 / self.angle_fy)))

        # Cl 10.2.4.3 in case of corrosive influences, the maximum edge distance shall not exceed
        # 40mm plus 4t, where t is the thickness of the thinner connected plate.
        if is_environ_corrosive == "Yes":
            self.max_edge_dist = min(self.max_edge_dist, 40 + 4 * thickness_governing_min)

    @staticmethod
    def round_to_next_five(distance):
        """

        Args:
            distance: (float) takes value of distance in mm

        Returns:
            distance: (float) Value of distance rounded up to the nearest multiple of five

        """
        round_up_distance = distance + (5 - distance) % 5
        return round_up_distance
