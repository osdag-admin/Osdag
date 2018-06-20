"""
Created on 16th October, 2017.

@author: Danish Ansari


Module: Beam to beam extended end plate splice connection (Moment connection)

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel structures by Dr. N Subramanian (chapter 5 and 6)
            3) Fundamentals of Structural steel design by M.L Gambhir
            4) AISC Design guide 16 and 4


ASCII diagram
                                      End plate
                                     +---+
                                 +----------+ Bolt
                                     | | |
+------------------------------------+ | +-------------------------------+
+------------------------------------| | |-------------------------------+
|                                   || | ||                              |
|                                +----------+                            |
|                                   || | ||   Bolt                       |
|                                +----------+                            |
|                                   || | ||                              |
|           Beam Section            || | ||            Beam Section      |
|                                   || | ||                              |
|                                +-----------+                           |
|                                   || | ||     Bolt                     |
|                                +-----------+                           |
|                                   || | ||                              |
+------------------------------------| | |-------------------------------+
+------------------------------------+ | +-------------------------------+
                                     | | |
                                 +----------+  Bolt
                                     +---+

                                      End plate
Note: The above ASCII diagram does not show details of weld


"""
import math
import logging
from model import get_beamdata, get_beamcombolist, get_oldbeamcombolist
from Connections.connection_calculations import ConnectionCalculations

logger = logging.getLogger('osdag.bbExtendedEndPlateSpliceCalc')

class ExtendedEndPlateCalculation(ConnectionCalculations):
	"""

	"""
	def __init__(self):
		super(ExtendedEndPlateCalculation, self).__init__()
		# Design preferences
		self.gamma_mw = 0.0
		self.bolt_hole_type = 'Standard'
		# self.min_edge_multiplier = 1
		# self.root_clearance_sa = 0
		# self.root_clearance_col = 0
		# self.clear_col_space = 0
		self.edge_factor = "b - Machine flame cut"
		self.is_environ_corrosive = "No"
		self.design_method = "Limit State Design"
		self.is_is_friction_grip_bolt = False
		self.n_e = 1  # interfaces offering friction - for HSFG design
		self.mu_f = 0.3  # slip factor - for HSFG design
		self.bolt_fu_overwrite = 0

		# Input dock
		self.connectivity = ""
		self.beam_section = ""
		self.dict_beam_data = {}
		self.dict_column_data = {}
		self.beam_fu = 0
		self.beam_fy = 0
		self.end_plate_fu = 0
		self.end_plate_fy = 0
		self.moment_force = 0.0
		self.shear_force = 0.0
		self.axial_force = 0.0
		self.bolt_diameter = 1
		self.bolt_type = 1
		self.bolt_grade = ""
		self.end_plate_thickness = 1
		self.end_plate_width = 1
		self.end_plate_height = 1
		self.weld_thickness_flange = 1
		self.weld_thickness_web = 1

		self.bolt_fu = 0
		self.bolt_diameter = 1
		self.bolt_hole_clearance_value = 1.0
		self.bolt_hole_diameter = 1
		self.beam_w_t = 1
		self.beam_f_t = 1
		self.beam_d = 1
		self.beam_b = 1
		self.beam_R1 = 1
		self.beam_R2 = 1
		self.alpha = 1
		self.status = True
		self.output_dict = {}

		# Output dock
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

	def extended_endplate_params(self, input_dict):
		self.connectivity = input_dict['Member']['Connectivity']
		self.beam_section = input_dict['Member']['BeamSection']
		self.beam_fu = input_dict['Member']['fu (MPa)']
		self.beam_fy = input_dict['Member']['fy (MPa)']
		# TODO implement after excomm review for different grades of plate
		self.end_plate_fu = input_dict['Member']['fu (MPa)']
		self.end_plate_fy = input_dict['Member']['fy (MPa)']

		self.moment_force = input_dict['Load']['Moment (kNm)']
		self.axial_force = input_dict['Load']['AxialForce (kN)']
		self.shear_force = input_dict['Load']['ShearForce (kN)']

		self.bolt_diameter = input_dict['Bolt']['Diameter (mm)']
		self.bolt_grade = input_dict['Bolt']['Grade']
		self.bolt_type = input_dict["Bolt"]["Type"]
		self.mu_f = input_dict["bolt"]["slip_factor"]
		self.end_plate_thickness = input_dict['Plate']['Thickness (mm)']
		self.end_plate_height = input_dict['Plate']['Height (mm)']
		self.end_plate_width = input_dict['Plate']['Width (mm)']

		self.weld_thickness_flange = input_dict['Weld']['Flange (mm)']
		self.weld_thickness_web = input_dict['Weld']['Web (mm)']

	def extended_endplate_output(self):
		"""

		Returns: Output parameters

		"""
		self.output_dict = {
			'Bolt': {
				'Status': self.status,
				'CriticalTension': "TODO",
				'TensionCapacity': "TODO",
				'ShearCapacity': self.bolt_shear_capacity,
				'BearingCapacity': self.bolt_bearing_capacity,
				'BoltCapacity': "TODO",
				'CombinedCapacity': "TODO",
				'NumberOfBolts': "TODO",
				'NumberOfRows': "TODO",
				'BoltsPerColumn': "TODO",
				'kb': self.k_b,
				'SumPlateThick': "TODO",
				'BoltFy': "TODO",

				'PitchMini': "TODO",
				'PitchMax': "TODO",
				'EndMax': "TODO",
				'EndMini': "TODO",
				'DiaHole': "TODO",
				'Gauge': "TODO",
				'CrossCentreGauge': "TODO",
				'End': "TODO",
				'Edge': "TODO",
				'Lv': "TODO",
			},

			'Plate': {
				'Height': "TODO",
				'Width': "TODO",
				'Thickness': "TODO",
				'MomentDemand': "TODO",
				'MomentCapacity': "TODO",
				'ThickRequired': "TODO",
				'Mp': "TODO",
			},

			'Weld': {
				'CriticalStressflange': "TODO",
				'CriticalStressWeb': "TODO",
				'WeldStrength': "TODO",
				'ForceFlange': "TODO",
				'LeffectiveFlange': "TODO",
				'LeffectiveWeb': "TODO",
				'FaWeb': "TODO",
				'Qweb': "TODO",
				'Resultant': "TODO",
				'UnitCapacity': "TODO",
			},

			'Stiffener': {
				'Height': "TODO",
				'Length': "TODO",
				'Thickness': "TODO",
			}
		}


