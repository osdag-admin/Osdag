"""
@Author:    Danish Ansari - Osdag Team, IIT Bombay [(P) danishdyp@gmail.com / danishansari@iitb.ac.in]

@Module - This is a helper file for the following modules

            Beam-Beam End Plate Splice Connection
               - Flushed End Plate
               - Extended One Way End Plate
               - Extended Both Way End Plate

            Beam-Column End Plate Splice Connection
               - Flushed End Plate
               - Extended One Way End Plate
               - Extended Both Way End Plate

 Note: This file works with the parent file(s) of end plate splice connection at ../Osdag/design_type/connection
"""

# Importing modules from the project directory

from utils.common.component import *
from utils.common.common_calculation import *

import logging
import math


class EndPlateSpliceHelper:

    def __init__(self, load, bolt, ep_type="", bolt_design_status="False", plate_design_status="False", overall_design_status="False"):
        """ helper file to run simulation for bolt design, plate design etc. """

        self.load = load
        self.bolt = bolt
        self.ep_type = ep_type
        self.bolt_design_status = bolt_design_status
        self.plate_design_status = plate_design_status
        self.overall_design_status = overall_design_status
        self.flange_capacity_status = False
        self.bolt_design_combined_check_status = False

        self.endplate_type = ""
        self.beam_properties = {}
        self.safety_factors = {}
        self.tension = []
        self.lever_arm = []
        self.bolt_column = 0
        self.bolt_row = 0
        self.bolt_numbers = 0
        self.bolt_diameter_provided = 0
        self.bolt_grade_provided = 0.0
        self.beam_D = 0.0
        self.beam_B = 0.0
        self.beam_T = 0.0
        self.beam_r1 = 0.0
        self.beam_fy = 0.0
        self.gamma_m0 = 0.0
        self.load_moment_effective = 0.0
        self.end_distance_provided = 0.0
        self.pitch_distance_provided = 0.0
        self.r_c = 0.0
        self.beta = 2
        self.proof_stress = 0.0
        self.dp_plate_fy = 0.0
        self.dp_plate_fu = 0.0
        self.plate_thickness = 0.0
        self.b_e = 0.0
        self.mp_plate = 0.0
        self.lv = 0.0
        self.le_1 = 0.0
        self.le_2 = 0.0
        self.le = 0.0
        self.t_1 = 0.0
        self.prying_force = 0.0
        self.bolt_tension_demand = 0.0
        self.flange_capacity = 0.0
        self.bolt_tension_capacity = 0.0
        self.bolt_numbers_provided = 0
        self.bolt_shear_demand = 0.0
        self.bolt_shear_capacity = 0.0
        self.bolt_combined_check_UR = 0.0

    def perform_bolt_design(self, endplate_type, beam_properties, safety_factors, bolt_column, bolt_row, bolt_diameter_provided, bolt_grade_provided,
                            load_moment_effective, end_distance_provided, pitch_distance_provided, beta, proof_stress, dp_plate_fy, plate_thickness,
                            dp_plate_fu):
        """ perform bolt design """

        self.endplate_type = endplate_type
        self.beam_properties = beam_properties
        self.safety_factors = safety_factors
        self.bolt_column = bolt_column
        self.bolt_row = bolt_row
        self.bolt_diameter_provided = bolt_diameter_provided
        self.bolt_grade_provided = bolt_grade_provided
        self.load_moment_effective = load_moment_effective
        self.end_distance_provided = end_distance_provided
        self.pitch_distance_provided = pitch_distance_provided
        self.beta = beta
        self.proof_stress = proof_stress
        self.dp_plate_fy = dp_plate_fy
        self.dp_plate_fu = dp_plate_fu
        self.plate_thickness = plate_thickness

        self.beam_D = self.beam_properties["beam_D"]
        self.beam_B = self.beam_properties["beam_B"]
        self.beam_T = self.beam_properties["beam_T"]
        self.beam_r1 = self.beam_properties["beam_r1"]
        self.beam_fy = self.beam_properties["beam_fy"]

        self.gamma_m0 = self.safety_factors["gamma_m0"]

        # start of checks

        # Check 1: Capacity of the flange under compression [A_g*f_y / gamma_m0]
        self.flange_capacity = (self.beam_B * self.beam_T * self.beam_fy) / self.gamma_m0  # kN

        # Check 2: Find lever arm of each bolt under tension
        # Assumption: NA passes through the centre of the bottom/compression flange
        self.self.lever_arm = []

        if self.endplate_type == 'Flushed - Reversible Moment':
            row_list = np.arange(1, self.bolt_row + 1, 1).tolist()

            # Note: In this connection all the odd rows will be near top flange and even rows near the bottom flange
            for a in row_list:
                if (a % 2) != 0:  # odd row
                    if a == 1:
                        r_1 = self.beam_D - (self.beam_T / 2) - self.beam_T - self.end_distance_provided  # mm, lever arm of row 1
                        self.lever_arm.append(r_1)
                    else:
                        r_a = r_1 - (round_up(((a / 2) - 1), 1) * self.pitch_distance_provided)  # mm, lever arm for remaining rows i.e. 3, 5, 7,...
                        self.lever_arm.append(r_a)
                else:  # even row
                    if a == 2:
                        r_2 = (self.beam_T / 2) + self.end_distance_provided  # mm, lever arm of row 2
                        self.lever_arm.append(r_2)
                    else:
                        r_a = r_2 + (((a / 2) - 1) * self.pitch_distance_provided)  # mm, lever arm for remaining rows i.e. 4, 6, 8,...
                        self.lever_arm.append(r_a)

        elif self.endplate_type == 'Extended One Way - Irreversible Moment':
            # Note: defining bolt models for this connection due to its un-symmetric nature of bolt placement, hence the equation cannot be
            # generalised up-to 5 rows (total)
            # From 6th and beyond rows, the equation is generalised since the bolts will be added inside flange only in an iterative manner

            if self.bolt_row == 3:  # 3 bolt rows model (2 rows at tension flange and 1 at compression flange)
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                r_1 = self.beam_D - self.beam_T
                self.lever_arm.append(r_1)
                r_2 = r_1
                self.lever_arm.append(r_2)

                # compression flange
                r_3 = (self.beam_T / 2) + self.end_distance_provided
                self.lever_arm.append(r_3)

            elif self.bolt_row == 4:  # 4 bolt rows model (3 rows at tension flange and 1 at compression flange)
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                r_1 = self.beam_D - self.beam_T
                self.lever_arm.append(r_1)
                r_2 = r_1
                self.lever_arm.append(r_2)

                # compression flange
                r_3 = (self.beam_T / 2) + self.end_distance_provided
                self.lever_arm.append(r_3)

                r_4 = r_2 - self.pitch_distance_provided  # top flange
                self.lever_arm.append(r_4)

            elif self.bolt_row == 5:  # 5 bolt rows model (4 rows at tension flange and 1 at compression flange)
                # Assumption: row r1, r2, r4 and r5 (at tension flange) carry equal force to act like a T-stub

                # top flange
                r_1 = self.beam_D - self.beam_T
                self.lever_arm.append(r_1)
                r_2 = r_1
                self.lever_arm.append(r_2)

                # compression flange
                r_3 = (self.beam_T / 2) + self.end_distance_provided
                self.lever_arm.append(r_3)

                r_4 = r_1  # top flange
                self.lever_arm.append(r_4)
                r_5 = r_1
                self.lever_arm.append(r_5)

            else:  # model for 6 rows and beyond
                # Assumption: row r1, r2, r4 and r5 (at tension flange) carry equal force to act like a T-stub

                # top flange
                r_1 = self.beam_D - self.beam_T
                self.lever_arm.append(r_1)
                r_2 = r_1
                self.lever_arm.append(r_2)

                # compression flange
                r_3 = (self.beam_T / 2) + self.end_distance_provided
                self.lever_arm.append(r_3)

                r_4 = r_1  # top flange
                self.lever_arm.append(r_4)
                r_5 = r_1
                self.lever_arm.append(r_5)

                # remaining new rows
                row_list = np.arange(5, self.bolt_row + 1, 1).tolist()

                pitch_counter = 0  # subtracting (pitch_counter times pitch distance) after the first iteration in the below loop to find lever arm
                for a in row_list:
                    r_a = r_1 - (self.beam_T / 2) - self.end_distance_provided - ((2 + pitch_counter) * self.pitch_distance_provided)
                    pitch_counter += 1

                    self.lever_arm.append(r_a)

        elif self.endplate_type == 'Extended Both Ways - Reversible Moment':
            row_list = np.arange(1, self.bolt_row + 1, 1).tolist()

            r_1 = self.beam_D - self.beam_T
            self.lever_arm.append(r_1)
            r_2 = r_1
            self.lever_arm.append(r_2)
            r_3 = 0
            self.lever_arm.append(r_3)
            r_4 = (self.beam_T / self.end_distance_provided) + self.end_distance_provided
            self.lever_arm.append(r_4)

            if len(row_list) > 4:  # if number of rows are more than 4
                r_5 = r_1 - (self.beam_T / 2) - self.end_distance_provided - self.pitch_distance_provided
                self.lever_arm.append(r_5)
                r_6 = r_4 + self.pitch_distance_provided
                self.lever_arm.append(r_6)

            if len(row_list) >= 8:  # if number of rows are more or equal than 8
                r_7 = 0
                self.lever_arm.append(r_7)
                r_8 = r_4 + self.pitch_distance_provided
                self.lever_arm.append(r_8)

            if len(row_list) >= 10:  # if number of rows are more or equal than 10
                r_9 = r_8 + self.pitch_distance_provided
                self.lever_arm.append(r_9)
                r_10 = r_1 - (self.beam_T / 2) - self.end_distance_provided - (2 * self.pitch_distance_provided)
                self.lever_arm.append(r_10)

            if len(row_list) >= 12:  # if number of rows are more or equal than 12
                update_row_list = row_list[10:]

                for a in update_row_list:
                    p = a - 3  # previous odd and even row for r_a

                    if (a % 2) != 0:  # for odd rows beyond 10, r11, r13, ...
                        r_i = row_list[p] + self.pitch_distance_provided
                        self.lever_arm.append(r_i)
                    else:  # for even rows beyond 10, r12, r14, ...
                        r_i = row_list[p] - self.pitch_distance_provided
                        self.lever_arm.append(r_i)

        # final list with all the lever arm distances calculated
        self.lever_arm = self.lever_arm

        # Check 3: Find force on each bolt under tension
        self.tension = []

        a = 0
        if self.endplate_type == 'Flushed - Reversible Moment':

            # Note: In this connection all the odd rows will be near top flange and even rows near the bottom flange
            for a in row_list:
                if a == 1:  # for 1st row only

                    summation = r_1
                    for p in range(1, len(row_list)):
                        summation += self.lever_arm[p] ** 2 / r_1

                    self.t_1 = self.load_moment_effective / (self.bolt_column * summation)  # kN, tension in row 1
                    self.tension.append(self.t_1)

                if a > 1:
                    t_a = self.t_1 * (self.lever_arm[a - 1] / r_1)  # kN, tension in the remaining rows (both odd and even after 1)
                    self.tension.append(t_a)

        elif self.endplate_type == 'Extended One Way - Irreversible Moment':

            if self.bolt_row == 3:
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_3 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (2 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 2 * self.t_1 * (r_3 / r_1)
                self.tension.append(t_3)

            elif self.bolt_row == 4:
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_3 ** 2 / r_1) + (r_4 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (2 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 2 * self.t_1 * (r_3 / r_1)
                self.tension.append(t_3)

                t_4 = 2 * self.t_1 * (r_4 / r_1)  # top flange
                self.tension.append(t_4)

            elif self.bolt_row == 5:
                # Assumption: row r1, r2, r4 and r5 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_3 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (4 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 4 * self.t_1 * (r_3 / r_1)
                self.tension.append(t_3)

                # top flange
                t_4 = self.t_1
                self.tension.append(t_4)
                t_5 = self.t_1
                self.tension.append(t_5)

            else:
                # Assumption: row r1, r2, r4 and r5 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_3 ** 2 / r_1) + (r_6 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (4 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 4 * self.t_1 * (r_3 / r_1)
                self.tension.append(t_3)

                # top flange
                t_4 = self.t_1
                self.tension.append(t_4)
                t_5 = self.t_1
                self.tension.append(t_5)
                t_6 = 4 * self.t_1 * (r_6 / r_1)
                self.tension.append(t_5)

                # remaining new rows
                if self.bolt_row > 6:
                    row_list = np.arange(7, self.bolt_row + 1, 1).tolist()

                    pitch_counter = 0  # subtracting (pitch_counter times pitch distance) to find lever arm
                    for a in row_list:
                        r_a = r_1 - (self.beam_T / 2) - self.end_distance_provided - ((3 + pitch_counter) * self.pitch_distance_provided)
                        pitch_counter += 1

                        self.lever_arm.append(r_a)

        elif self.endplate_type == 'Extended Both Ways - Reversible Moment':
            if self.bolt_row == 4:
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_4 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (2 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 0
                self.tension.append(t_3)
                t_4 = 2 * self.t_1 * (r_4 / r_1)
                self.tension.append(t_4)

            elif self.bolt_row == 6:
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_4 ** 2 / r_1) + (r_5 ** 2 / r_1) + (r_6 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (2 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 0
                self.tension.append(t_3)
                t_4 = 2 * self.t_1 * (r_4 / r_1)
                self.tension.append(t_4)

                t_5 = 2 * self.t_1 * (r_5 / r_1)
                self.tension.append(t_5)
                t_6 = 2 * self.t_1 * (r_6 / r_1)
                self.tension.append(t_6)

            elif self.bolt_row == 8:
                # Assumption: row r1, r2, r5 and r6 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_4 ** 2 / r_1) + (r_8 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (4 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 0
                self.tension.append(t_3)
                t_4 = 4 * self.t_1 * (r_4 / r_1)
                self.tension.append(t_4)
                t_5 = self.t_1
                self.tension.append(t_5)
                t_6 = self.t_1
                self.tension.append(t_6)
                t_7 = 0
                self.tension.append(t_7)
                t_8 = 4 * self.t_1 * (r_8 / r_1)
                self.tension.append(t_8)

            else:
                # Assumption: row r1, r2, r5 and r6 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_4 ** 2 / r_1) + (r_8 ** 2 / r_1) + (r_9 ** 2 / r_1) + (r_10 ** 2 / r_1)

                self.t_1 = self.load_moment_effective / (4 * self.bolt_column * summation)  # kN, tension in row 1 and 2
                self.tension.append(self.t_1)
                t_2 = self.t_1
                self.tension.append(t_2)

                # compression flange
                t_3 = 0
                self.tension.append(t_3)
                t_4 = 4 * self.t_1 * (r_4 / r_1)
                self.tension.append(t_4)

                # top flange
                t_5 = self.t_1
                self.tension.append(t_5)
                t_6 = self.t_1
                self.tension.append(t_6)

                t_7 = 0
                self.tension.append(t_7)
                t_8 = 4 * self.t_1 * (r_8 / r_1)
                self.tension.append(t_8)
                t_9 = 4 * self.t_1 * (r_9 / r_1)
                self.tension.append(t_9)
                t_10 = 4 * self.t_1 * (r_10 / r_1)
                self.tension.append(t_10)

                # remaining new rows
                if self.bolt_row > 10:
                    row_list = np.arange(11, self.bolt_row + 1, 1).tolist()

                    for a in row_list:
                        t_a = 4 * self.t_1 * (r_a / r_1)
                        self.tension.append(t_a)

        # final list with all the tension values calculated
        self.tension = self.tension

        # Check 4: Total tension
        # r_c = reaction due to tension in all the bolts
        self.r_c = 0
        for val in range(0, len(self.tension)):
            self.r_c = self.r_c + self.tension[val]  # adding all the values of tension

        # total tension considering the bolt columns
        self.r_c = self.r_c * self.bolt_column  # kN

        # Check 5: Reaction at bottom flange
        if self.r_c > self.flange_capacity:
            self.flange_capacity_status = False
            self.bolt_design_status = False
        else:
            self.flange_capacity_status = True
            self.bolt_design_status = True

        # Check 6: Moment capacity of the end plate
        self.b_e = self.beam_B / self.bolt_column
        self.mp_plate = (self.dp_plate_fy / self.gamma_m0) * ((self.b_e * self.plate_thickness ** 2) / 4)

        # Check 7: Prying force check in the critical bolt
        self.lv = self.end_distance_provided - (self.beam_r1 / 2)
        self.le_1 = self.end_distance_provided
        self.le_2 = (1.1 * self.plate_thickness) * math.sqrt((self.beta * self.proof_stress) / self.dp_plate_fy)
        self.le = min(self.le_1, self.le_2)

        # taking moment about the toe of weld or edge of the flange from bolt center-line to find the actual prying force (Q) in the critical bolt
        # Mp_plate = T*l_v - Q.l_e
        self.prying_force = ((self.t_1 * self.lv) - self.mp_plate) / self.le  # kN

        if self.prying_force < 0:
            self.plate_design_status = False
            self.bolt_design_status = False
        else:
            self.plate_design_status = True
            self.bolt_design_status = True

        # Check 8: Tension capacity of bolt
        self.bolt_tension_capacity = Bolt.calculate_bolt_tension_capacity(self.bolt_diameter_provided, self.bolt_grade_provided)  # kN

        # checking the critical bolt for its tension capacity against tension due to moment + prying force
        self.bolt_tension_demand = self.t_1 + self.prying_force

        if self.bolt_tension_demand > self.bolt_tension_capacity:
            self.bolt_design_status = False
        else:
            self.bolt_design_status = True

        # Check 9: combined shear + tension check of bolts
        self.bolt_numbers_provided = self.bolt_column * self.bolt_row

        # Check 9.1: shear demand
        self.bolt_shear_demand = self.load.shear_force / self.bolt_numbers_provided  # kN, shear on each bolt

        # Check 9.2: shear capacity
        self.bolt_shear_capacity = self.bolt.calculate_bolt_capacity(self.bolt_diameter_provided, self.bolt_grade_provided,
                                                                     [(self.plate_thickness, self.dp_plate_fu, self.dp_plate_fy),
                                                                      (self.plate_thickness, self.dp_plate_fu, self.dp_plate_fy)], 1,
                                                                     self.end_distance_provided, self.pitch_distance_provided,
                                                                     seatedangle_e=0)  # kN

        # Check 9.3: combined shear + tension check
        self.bolt_combined_check_UR = self.bolt.calculate_combined_shear_tension_capacity(self.bolt_shear_demand, self.bolt_shear_capacity,
                                                                                          self.bolt_tension_demand, self.bolt_tension_capacity,
                                                                                          self.bolt.bolt_type)

        if self.bolt_combined_check_UR > 1.0:
            self.bolt_design_combined_check_status = False
            self.bolt_design_status = False
        else:
            self.bolt_design_combined_check_status = True
            self.bolt_design_status = True

        # overall status
        if self.bolt_design_status and self.plate_design_status and self.bolt_design_combined_check_status and self.flange_capacity_status is True:
            self.overall_design_status = True
        else:
            self.overall_design_status = False
