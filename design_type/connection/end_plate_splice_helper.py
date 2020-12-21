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


class EndPlateSpliceHelper(object):

    def __init__(self, module, supporting_section, supported_section, load, bolt, connectivity="", ep_type="", plate_design_status="False",
                 helper_file_design_status="False"):
        """ helper file to run simulation for bolt design, plate design etc. """

        self.module = module
        self.supporting_section = supporting_section
        self.supported_section = supported_section
        self.load = load
        self.bolt = bolt
        self.connectivity = connectivity
        self.ep_type = ep_type
        self.plate_design_status = plate_design_status
        self.helper_file_design_status = helper_file_design_status
        self.bolt_tension_design_status = False
        self.flange_capacity_status = False
        self.bolt_design_combined_check_status = False

        self.endplate_type = ""
        self.beam_properties = {}
        self.safety_factors = {}
        self.tension = []
        self.tension_web_bolts = []
        self.lever_arm = []
        self.lever_arm_web_bolts = []
        self.bolt_column = 0
        self.bolt_row = 0
        self.bolt_row_web = 0
        self.bolt_numbers = 0
        self.bolt_diameter_provided = 0
        self.bolt_grade_provided = 0.0
        self.beam_D = 0.0
        self.beam_bf = 0.0
        self.beam_tf = 0.0
        self.column_tf = 0.0
        self.column_tw = 0.0
        self.beam_r1 = 0.0
        self.beam_fy = 0.0
        self.gamma_m0 = 0.0
        self.load_moment_effective = 0.0
        self.load_shear = 0.0
        self.end_distance_provided = 0.0
        self.pitch_distance_provided = 0.0
        self.pitch_distance_web = 0.0
        self.r_c = 0.0
        self.beta = 2
        self.proof_stress = 0.0
        self.dp_plate_fy = 0.0
        self.dp_plate_fu = 0.0
        self.plate_thickness = 0.0
        self.plate_thickness_req = 0.0
        self.b_e = 0.0
        self.mp_plate = 0.0
        self.plate_moment_capacity = 0.0
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
        self.bolt_bearing_capacity = 0.0
        self.bolt_capacity = 0.0
        self.grip_length = 0.0
        self.beta_lg = 1.0
        self.bolt_grip_length_status = True
        self.bolt_combined_check_UR = 0.0

    def perform_bolt_design(self, endplate_type, supported_section, gamma_m0, bolt_column, bolt_row, bolt_row_web, bolt_diameter_provided,
                            bolt_grade_provided, load_moment_effective, end_distance_provided, pitch_distance_provided, pitch_distance_web, beta,
                            proof_stress, dp_plate_fy, plate_thickness, dp_plate_fu, load_shear):
        """ perform bolt design """

        self.endplate_type = endplate_type
        self.supported_section = supported_section
        self.gamma_m0 = gamma_m0
        self.bolt_column = bolt_column
        self.bolt_row = bolt_row
        self.bolt_row_web = bolt_row_web
        self.bolt_diameter_provided = bolt_diameter_provided
        self.bolt_grade_provided = bolt_grade_provided
        self.load_moment_effective = load_moment_effective
        self.load_shear = load_shear
        self.end_distance_provided = end_distance_provided
        self.pitch_distance_provided = pitch_distance_provided
        self.pitch_distance_web = pitch_distance_web
        self.beta = beta
        self.proof_stress = proof_stress
        self.dp_plate_fy = dp_plate_fy
        self.dp_plate_fu = dp_plate_fu
        self.plate_thickness = plate_thickness

        # beam properties
        self.beam_D = self.supported_section.depth
        self.beam_bf = self.supported_section.flange_width
        self.beam_tf = self.supported_section.flange_thickness
        self.beam_r1 = self.supported_section.root_radius
        self.beam_fy = float(self.supported_section.fy)

        # column properties
        self.column_tf = self.supporting_section.flange_thickness
        self.column_tw = self.supporting_section.web_thickness

        # start of checks

        # Check 1: Capacity of the flange under compression [A_g*f_y / gamma_m0]
        self.flange_capacity = round(((self.beam_bf * self.beam_tf * self.beam_fy) / self.gamma_m0) * 1e-3, 2)  # kN

        # Check 2: Find lever arm of each bolt under tension
        # Assumption: NA passes through the centre of the bottom/compression flange
        self.lever_arm = []

        if self.endplate_type == 'Flushed - Reversible Moment':
            row_list = np.arange(1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()

            # Note: In this connection all the odd rows will be near top flange and even rows near the bottom flange
            a = 0
            for a in row_list:
                if a <= self.bolt_row:

                    if (a % 2) != 0:  # odd row
                        if a == 1:
                            r_1 = self.beam_D - (self.beam_tf / 2) - self.beam_tf - self.end_distance_provided  # mm, lever arm of row 1
                            self.lever_arm.append(r_1)
                        else:
                            r_a = r_1 - (round_up(((a / 2) - 1), 1) * self.pitch_distance_provided)  # mm, lever arm for remaining rows i.e. 3, 5, 7,...
                            self.lever_arm.append(r_a)
                    else:  # even row
                        if a == 2:
                            r_2 = (self.beam_tf / 2) + self.end_distance_provided  # mm, lever arm of row 2
                            self.lever_arm.append(r_2)
                        else:
                            r_a = r_2 + (((a / 2) - 1) * self.pitch_distance_provided)  # mm, lever arm for remaining rows i.e. 4, 6, 8,...
                            self.lever_arm.append(r_a)
                else:  # for bolts at web, taking the last row inside flange on the bottom side as reference
                    # updating the row list to begin the iteration from the rows provided at web with different pitch distance
                    row_list = row_list[a - 1:]

                    row_web_counter = 1
                    for a in row_list:
                        r_a = self.lever_arm[- row_web_counter] + (row_web_counter * self.pitch_distance_web)
                        self.lever_arm.append(r_a)
                        row_web_counter += 1

        elif self.endplate_type == 'Extended One Way - Irreversible Moment':
            # Note: defining bolt models for this connection due to its un-symmetric nature of bolt placement, hence the equation cannot be
            # generalised up-to 5 rows (total)
            # From 6th and beyond rows, the equation is generalised since the bolts will be added inside flange only in an iterative manner

            row_list = np.arange(1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()

            for a in row_list:
                if a <= self.bolt_row:

                    if self.bolt_row == 3:  # 3 bolt rows model (2 rows at tension flange and 1 at compression flange)
                        # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                        if len(self.lever_arm) <= 0:
                            # top flange
                            r_1 = self.beam_D - self.beam_tf
                            self.lever_arm.append(r_1)
                            r_2 = r_1
                            self.lever_arm.append(r_2)

                            # compression flange
                            r_3 = (self.beam_tf / 2) + self.end_distance_provided
                            self.lever_arm.append(r_3)

                    elif self.bolt_row == 4:  # 4 bolt rows model (3 rows at tension flange and 1 at compression flange)
                        # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                        if len(self.lever_arm) <= 0:
                            # top flange
                            r_1 = self.beam_D - self.beam_tf
                            self.lever_arm.append(r_1)
                            r_2 = r_1
                            self.lever_arm.append(r_2)

                            # compression flange
                            r_3 = (self.beam_tf / 2) + self.end_distance_provided
                            self.lever_arm.append(r_3)

                            r_4 = r_2 - self.pitch_distance_provided  # top flange
                            self.lever_arm.append(r_4)

                    elif self.bolt_row == 5:  # 5 bolt rows model (4 rows at tension flange and 1 at compression flange)
                        # Assumption: row r1, r2, r4 and r5 (at tension flange) carry equal force to act like a T-stub

                        if len(self.lever_arm) <= 0:
                            # top flange
                            r_1 = self.beam_D - self.beam_tf
                            self.lever_arm.append(r_1)
                            r_2 = r_1
                            self.lever_arm.append(r_2)

                            # compression flange
                            r_3 = (self.beam_tf / 2) + self.end_distance_provided
                            self.lever_arm.append(r_3)

                            r_4 = r_1  # top flange
                            self.lever_arm.append(r_4)
                            r_5 = r_1
                            self.lever_arm.append(r_5)

                    else:  # model for 6 rows and beyond
                        # Assumption: row r1, r2, r4 and r5 (at tension flange) carry equal force to act like a T-stub

                        if len(self.lever_arm) <= 0:
                            # top flange
                            r_1 = self.beam_D - self.beam_tf
                            self.lever_arm.append(r_1)
                            r_2 = r_1
                            self.lever_arm.append(r_2)

                            # compression flange
                            r_3 = (self.beam_tf / 2) + self.end_distance_provided
                            self.lever_arm.append(r_3)

                            r_4 = r_1  # top flange
                            self.lever_arm.append(r_4)
                            r_5 = r_1
                            self.lever_arm.append(r_5)

                            # remaining new rows, 6th and beyond
                            row_list = np.arange(6, self.bolt_row + 1, 1).tolist()

                            # subtracting (pitch_counter times pitch distance) after the first iteration in the below loop to find lever arm
                            pitch_counter = 0
                            for a in row_list:
                                r_a = r_1 - (self.beam_tf / 2) - self.end_distance_provided - ((2 + pitch_counter) * self.pitch_distance_provided)
                                pitch_counter += 1

                                self.lever_arm.append(r_a)

                else:  # bolts near the web
                    row_list = np.arange(1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()
                    # updating the row list to begin the iteration from the rows provided at web with different pitch distance
                    row_list = row_list[a - 1:]

                    pitch_counter = 1
                    for a in row_list:
                        r_a = r_3 + (pitch_counter * self.pitch_distance_web)
                        self.lever_arm.append(r_a)
                        pitch_counter += 1

                    if a == row_list[-1]:
                        break

        elif self.endplate_type == 'Extended Both Ways - Reversible Moment':
            row_list = np.arange(1, self.bolt_row + 1, 1).tolist()

            r_1 = self.beam_D - self.beam_tf
            self.lever_arm.append(r_1)
            r_2 = r_1
            self.lever_arm.append(r_2)
            r_3 = 0
            self.lever_arm.append(r_3)
            r_4 = (self.beam_tf / 2) + self.end_distance_provided
            self.lever_arm.append(r_4)

            if self.bolt_row == 6:  # if number of rows are 6
                r_5 = r_1 - (self.beam_tf / 2) - self.end_distance_provided - self.pitch_distance_provided
                self.lever_arm.append(r_5)
                r_6 = r_4 + self.pitch_distance_provided
                self.lever_arm.append(r_6)

            if self.bolt_row >= 8:  # if number of rows are 8
                r_5 = r_1
                self.lever_arm.append(r_5)
                r_6 = r_1
                self.lever_arm.append(r_6)
                r_7 = 0
                self.lever_arm.append(r_7)
                r_8 = r_4 + self.pitch_distance_provided
                self.lever_arm.append(r_8)

            if self.bolt_row >= 10:  # if number of rows are 10
                r_9 = r_8 + self.pitch_distance_provided
                self.lever_arm.append(r_9)
                r_10 = r_1 - (self.beam_tf / 2) - self.end_distance_provided - (2 * self.pitch_distance_provided)
                self.lever_arm.append(r_10)

            if self.bolt_row >= 12:  # if number of rows are more or equal than 12
                update_row_list = row_list[10:]

                for a in update_row_list:
                    p = a - 3  # previous odd and even row for r_a

                    if (a % 2) != 0:  # for odd rows beyond 10, r11, r13, ...
                        r_a = self.lever_arm[p] + self.pitch_distance_provided
                        self.lever_arm.append(r_a)
                    else:  # for even rows beyond 10, r12, r14, ...
                        r_a = self.lever_arm[p] - self.pitch_distance_provided
                        self.lever_arm.append(r_a)

        if self.endplate_type == 'Extended Both Ways - Reversible Moment':
            if self.bolt_row_web > 0:

                row_list = np.arange(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()

                if self.bolt_row <= 8:
                    pitch_counter = 1
                    for a in row_list:
                        r_a = self.lever_arm[-pitch_counter] + (pitch_counter * self.pitch_distance_web)
                        self.lever_arm.append(r_a)
                        pitch_counter += 1
                else:
                    pitch_counter = 2
                    for a in row_list:
                        r_a = self.lever_arm[-pitch_counter] + ((pitch_counter - 1) * self.pitch_distance_web)
                        self.lever_arm.append(r_a)
                        pitch_counter += 1

        # final list with all the lever arm distances calculated
        self.lever_arm = self.lever_arm
        self.lever_arm = [round(value_lever_arm, 2) for value_lever_arm in self.lever_arm]

        # Check 3: Find force on each bolt under tension
        self.tension = []
        self.load_moment_effective = self.load_moment_effective * 1e3  # kN-mm

        a = 0
        if self.endplate_type == 'Flushed - Reversible Moment':
            row_list = np.arange(1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()

            # Note: In this connection all the odd rows will be near top flange and even rows near the bottom flange
            for a in row_list:
                if a == 1:  # for 1st row only

                    summation = r_1
                    for p in range(1, len(row_list), 1):
                        print(p)
                        summation += self.lever_arm[p] ** 2 / r_1

                    self.t_1 = self.load_moment_effective / (self.bolt_column * summation)  # kN, tension in row 1
                    self.tension.append(self.t_1)

                else:  # all the rows following after the first row
                    t_a = self.t_1 * (self.lever_arm[a - 1] / r_1)  # kN, tension in the remaining rows (both odd and even after 1)
                    self.tension.append(t_a)

        if self.endplate_type == 'Extended One Way - Irreversible Moment':

            if self.bolt_row == 3:
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_3 ** 2 / r_1)
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

                # tension values
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
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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
                # summation = r_1 + (r_3 ** 2 / r_1) + (r_6 ** 2 / r_1)
                summation = r_1 + (r_3 ** 2 / r_1) + (self.lever_arm[5] ** 2 / r_1)
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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
                # t_6 = 4 * self.t_1 * (r_6 / r_1)
                t_6 = 4 * self.t_1 * (self.lever_arm[5] / r_1)
                self.tension.append(t_6)

                # remaining new rows
                if self.bolt_row > 6:
                    row_list = np.arange(7, self.bolt_row + 1, 1).tolist()

                    for a in row_list:
                        t_a = 4 * self.t_1 * (r_a / r_1)
                        self.tension.append(t_a)

        # calculate tension in additional rows near web
        if self.endplate_type == 'Extended One Way - Irreversible Moment':
            if self.bolt_row_web > 0:

                if self.bolt_row <= 4:
                    factor = 2
                else:
                    factor = 4

                row_list = np.arange(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()
                a = 0
                for a in row_list:
                    t_a = factor * self.t_1 * (r_a / r_1)
                    self.tension.append(t_a)

        if self.endplate_type == 'Extended Both Ways - Reversible Moment':
            p = 0
            if self.bolt_row == 4:
                # Assumption: row r1 and r2 (at tension flange) carry equal force to act like a T-stub

                # top flange
                summation = r_1 + (r_4 ** 2 / r_1)
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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
                if self.bolt_row_web > 0:
                    for p in range(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1):
                        summation += self.lever_arm[p - 1] ** 2 / r_1

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

        # calculate tension in additional rows near web
        if self.endplate_type == 'Extended Both Ways - Reversible Moment':
            if self.bolt_row_web > 0:

                if self.bolt_row <= 6:
                    factor = 2
                else:
                    factor = 4

                row_list = np.arange(self.bolt_row + 1, self.bolt_row + self.bolt_row_web + 1, 1).tolist()
                for a in row_list:
                    t_a = factor * self.t_1 * (r_a / r_1)
                    self.tension.append(t_a)

        # final list with all the tension values calculated
        self.tension = self.tension
        self.tension = [round(value_tension, 2) for value_tension in self.tension]

        # adding the lists of bolt row and tension
        print("ROWS BEFORE ADDING {}".format(self.bolt_row))
        print("ROWS AFTER ADDING {}".format(self.bolt_row + self.bolt_row_web))
        print("ROWS AT WEB {}".format(self.bolt_row_web))

        # Check 4: Total tension
        # r_c = reaction due to tension in all the bolts
        self.r_c = 0
        for val in range(0, len(self.tension)):
            self.r_c += self.tension[val]  # adding all the values of tension

        # total tension considering the bolt columns
        self.r_c = round(self.r_c * self.bolt_column, 2)  # kN

        # Check 5: Reaction at bottom flange
        if self.r_c > self.flange_capacity:
            self.flange_capacity_status = False
        else:
            self.flange_capacity_status = True

        # Check 6: Prying force check in the critical bolt
        self.b_e = self.beam_bf / self.bolt_column  # mm
        self.lv = self.end_distance_provided - (self.beam_r1 / 2)  # mm
        self.le_1 = self.end_distance_provided  # mm
        self.le_2 = (1.1 * self.plate_thickness) * math.sqrt((self.beta * self.proof_stress) / self.dp_plate_fy)  # mm
        self.le = min(self.le_1, self.le_2)  # mm

        self.prying_force = IS800_2007.cl_10_4_7_bolt_prying_force(self.t_1 * 1e3, self.lv, self.proof_stress, self.b_e, self.plate_thickness,
                                                                   self.dp_plate_fy, self.end_distance_provided, self.bolt.bolt_tensioning, eta=1.5)
        self.prying_force = round(self.prying_force * 1e-3, 2)  # kN

        # Check 7: Moment capacity of the end plate and plate thickness check

        # taking moment about the toe of weld or edge of the flange from bolt center-line
        # Mp_plate = T*l_v - Q.l_e
        self.mp_plate = round(((self.t_1 * self.lv) - (self.prying_force * self.le)) * 1e3, 2)  # N-mm

        # negative Mp means prying force is higher than the tension in bolt and the yielding location would be outside the bolts and not near the
        # root of the beam
        if self.mp_plate < 0:
            self.mp_plate = - 1 * self.mp_plate

        # equation Mp_plate with the plate moment capacity to find thickness of plate required
        self.plate_thickness_req = round(math.sqrt((4 * self.gamma_m0 * self.mp_plate) / (self.dp_plate_fy * self.b_e)), 2)  # mm

        if self.plate_thickness < self.plate_thickness_req:
            self.plate_design_status = False
        else:
            self.plate_design_status = True

        # moment capacity of plate
        self.plate_moment_capacity = ((self.b_e * self.plate_thickness ** 2) / 4) * (self.dp_plate_fy / self.gamma_m0)
        self.plate_moment_capacity = round(self.plate_moment_capacity * 1e-6, 2)  # kN-m

        # Check 8: Tension capacity of bolt
        self.bolt.calculate_bolt_tension_capacity(self.bolt_diameter_provided, self.bolt_grade_provided)
        self.bolt_tension_capacity = round(self.bolt.bolt_tension_capacity * 1e-3, 2)  # kN

        # checking the critical bolt for its tension capacity against tension due to moment + prying force
        self.bolt_tension_demand = self.t_1 + self.prying_force

        if self.bolt_tension_demand > self.bolt_tension_capacity:
            self.bolt_tension_design_status = False
        else:
            self.bolt_tension_design_status = True

        # Check 9: combined shear + tension check of bolts
        self.bolt_numbers_provided = self.bolt_column * (self.bolt_row + self.bolt_row_web)

        # Check 9.1: shear demand
        self.bolt_shear_demand = round(self.load_shear / self.bolt_numbers_provided, 2)  # kN, shear on each bolt

        # Check 9.2: bolt capacity - shear design
        self.bolt.calculate_bolt_capacity(self.bolt_diameter_provided, self.bolt_grade_provided,
                                          [(self.plate_thickness, self.dp_plate_fu, self.dp_plate_fy), (self.plate_thickness, self.dp_plate_fu,
                                                                                                        self.dp_plate_fy)], 1,
                                          self.end_distance_provided, self.pitch_distance_provided, seatedangle_e=0)  # kN

        self.bolt_shear_capacity = round(self.bolt.bolt_shear_capacity * 1e-3, 2)  # kN

        if self.bolt.bolt_type == "Bearing Bolt":
            self.bolt_bearing_capacity = round(self.bolt.bolt_bearing_capacity * 1e-3, 2)  # kN
        else:
            self.bolt_bearing_capacity = self.bolt.bolt_bearing_capacity  # N/A
        self.bolt_capacity = round(self.bolt.bolt_capacity * 1e-3, 2)  # kN

        # Check 9.3: Large grip length check
        if self.bolt.bolt_type == "Bearing Bolt":

            if self.module == KEY_DISP_BCENDPLATE:  # BC-EP
                if self.connectivity == VALUES_CONN_1[0]:  # CF-BW
                    self.grip_length = self.plate_thickness + self.column_tf  # mm
                else:  # CW-BW
                    self.grip_length = self.plate_thickness + self.column_tw
            else:  # BB-EP
                self.grip_length = 2 * self.plate_thickness

            if self.grip_length > 8 * self.bolt_diameter_provided:
                self.bolt_grip_length_status = False
                self.beta_lg = 1.0
            else:
                self.bolt_grip_length_status = True

                # beta lg
                if self.grip_length > (5 * self.bolt_diameter_provided):
                    self.beta_lg = round(8 / (3 + (self.grip_length / self.bolt_diameter_provided)), 2)  # reduction factor
                else:
                    self.beta_lg = 1.0

        # reduced capacity of bolt (post reduction factor)
        self.bolt_capacity = round(self.bolt.bolt_capacity * self.beta_lg * 1e-3, 2)  # kN

        # Check 9.4: combined shear + tension check
        self.bolt.calculate_combined_shear_tension_capacity(self.bolt_shear_demand, self.bolt_capacity, self.bolt_tension_demand,
                                                            self.bolt_tension_capacity, self.bolt.bolt_type)

        self.bolt_combined_check_UR = round(self.bolt.bolt_combined_capacity, 3)

        if self.bolt_combined_check_UR > 1.0:
            self.bolt_design_combined_check_status = False
        else:
            self.bolt_design_combined_check_status = True

        # overall status of the helper file
        status = [self.flange_capacity_status, self.plate_design_status, self.bolt_tension_design_status, self.bolt_design_combined_check_status,
                  self.bolt_grip_length_status]
        for check in status:
            if check is False:
                self.helper_file_design_status = False
                break
            else:
                self.helper_file_design_status = True

