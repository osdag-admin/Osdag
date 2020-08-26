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

from design_type.connection.beam_beam_end_plate_splice import BeamBeamEndPlateSplice
from design_type.connection.shear_connection import ShearConnection
from utils.common.is800_2007 import IS800_2007
from utils.common.other_standards import IS_5624_1993
from utils.common.component import *
from utils.common.material import *
from utils.common.common_calculation import *
from Common import *
from utils.common.load import Load
from utils.common.other_standards import *
from design_report.reportGenerator import save_html
from Report_functions import *
from design_report.reportGenerator_latex import CreateLatex

import logging
import math


class EndPlateSpliceHelper(BeamBeamEndPlateSplice):

    def __init__(self):
        super(EndPlateSpliceHelper, self).__init__()
        """ helper file to run simulation for bolt design, plate design etc. """
        self.total_number_bolts = 0

    def perform_bolt_design(self, bolt_numbers_tension_flange, bolt_numbers_web):
        """ perform bolt design """
        # re-initialize parameters for each iteration
        self.bolt_numbers_tension_flange = bolt_numbers_tension_flange
        self.bolt_numbers_web = bolt_numbers_web

        # start of checks

        # Check 1: tension capacity of bolt
        self.bolt_tension_capacity = self.bolt.calculate_bolt_tension_capacity(self.bolt_diameter_provided, self.bolt_grade_provided)

        # Check 1.2: tension in each bolt due to bending moment
        self.bolt_tension = self.load_tension_flange / self.bolt_numbers_tension_flange  # kN

        # Check 1.3: calculate prying force in each bolt
        self.lv = self.end_distance_provided - (self.beam_r1 / 2)
        self.b_e = self.ep_width_provided - (2 * self.edge_distance_provided)

        self.bolt_prying_force = self.cl_10_4_7_bolt_prying_force(self.bolt_tension, self.lv, self.proof_load, self.b_e,
                                                                  self.plate_thickness, self.plate.fy, self.end_distance_provided,
                                                                  self.bolt.bolt_tensioning, eta=1.5)  # kN

        # Check 1.4: total tension demand of bolt (tension + prying)
        self.bolt_tension_demand = self.bolt_tension + self.bolt_prying_force  # kN

        # Check 1.5: tension check in bolt
        self.bolt_tension_check_UR = round(self.bolt_tension_demand / self.bolt.bolt_tension_capacity, 3)

        if self.bolt_tension_check_UR > 1.0:
            self.bolt_design_status = False
        else:
            self.bolt_design_status = True

        # Check 2: shear check of bolt

        # Check 2.1: shear demand
        self.bolt_shear = self.load.shear_force / (self.bolt_numbers_tension_flange + self.bolt_numbers_web)  # kN, shear on each bolt

        # Check 2.2: shear capacity
        self.bolt_shear_capacity = self.bolt.calculate_bolt_capacity(self.bolt_diameter_provided, self.bolt_grade_provided,
                                                                     [(self.plate_thickness, self.plate.fu, self.plate.fy),
                                                                      (self.plate_thickness, self.plate.fu, self.plate.fy)], 1,
                                                                     self.end_distance_provided, self.pitch_distance_provided,
                                                                     seatedangle_e=0)  # kN

        # Check 2.3: group capacity
        self.bolt_group_shear_capacity = self.bolt_shear_capacity * (self.bolt_numbers_tension_flange + self.bolt_numbers_web)  # kN

        # check
        self.bolt_shear_check_UR = round(self.load.shear_force / self.bolt_group_shear_capacity, 3)

        if self.bolt_shear_check_UR > 1.0:
            self.bolt_design_combined_check_status = False
            self.bolt_design_status = False
        else:
            self.bolt_design_combined_check_status = True
            self.bolt_design_status = True

        # Check 2.4: combined shear + tension check
        self.bolt_combined_check = self.bolt.calculate_combined_shear_tension_capacity(self.bolt_shear, self.bolt_shear_capacity,
                                                                                 self.bolt_tension, self.bolt_tension_capacity,
                                                                                 self.bolt.bolt_type)

        if self.bolt_combined_check > 1.0:
            self.bolt_design_combined_check_status = False
            self.bolt_design_status = False
        else:
            self.bolt_design_combined_check_status = True
            self.bolt_design_status = True

        # total number of bolts
        if self.bolt_design_status == True:

            # create a list which satisfies all the checks
            self.selected_list = [self.bolt_column, self.rows_near_tension_flange, self.rows_near_web]


            # self.bolt_numbers_tension_flange = self.bolt_column * self.rows_near_tension_flange
            # self.bolt_numbers_web = self.bolt_column * self.rows_near_web

            if self.connectivity == 'Flushed - Reversible Moment':
                self.rows_outside_D_provided = 0
                self.rows_inside_D_provided = 2
            self.total_number_bolts = 1

