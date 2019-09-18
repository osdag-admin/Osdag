'''
Created on 24-Aug-2017

@author: reshma
'''
from numpy import math
from Connections.connection_calculations import ConnectionCalculations
import svgwrite
import cairosvg
import numpy as np
import os


class ExtendedEndPlate(object):
	def __init__(self, input_dict, output_dict, beam_data, folder):
		"""

		Args:
			input_dict: input parameters from GUI
			output_dict:  output parameters based on calculation
			beam_data:  geometric properties of beam
			folder: path to save the generated images

		Returns:
			None

		"""
		print "calculation", input_dict
		self.folder = folder
		self.beam_length_L1 = 700
		self.beam_length_L2 = 700

		self.beam_depth_D1 = int(beam_data["D"])
		self.beam_depth_D2 = self.beam_depth_D1

		self.beam_designation = beam_data['Designation']

		self.beam_width_B1 = int(beam_data["B"])
		self.beam_width_B2 = self.beam_width_B1

		self.plate_thickness_p1 = int(output_dict['Plate']['Thickness'])
		self.plate_thickness_p2 = self.plate_thickness_p1

		self.plate_width_B1 = int(output_dict['Plate']['Width'])
		self.plate_width_B2 = self.plate_width_B1

		self.plate_length_L1 = int(output_dict['Plate']['Height'])
		self.plate_length_L2 = self.plate_length_L1

		self.flange_thickness_T1 = (beam_data["T"])
		self.flange_thickness_T2 = self.flange_thickness_T1

		self.web_thickness_tw1 = int(beam_data["tw"])
		self.web_thickness_tw2 = self.web_thickness_tw1

		self.flange_weld_thickness = int(input_dict['Weld']['Flange (mm)'])  # 12
		self.web_weld_thickness = int(input_dict["Weld"]['Web (mm)'])  # 8

		self.bolt_diameter = int(input_dict['Bolt']['Diameter (mm)'])  # 24
		self.bolt_type = input_dict["Bolt"]["Type"]
		self.bolt_hole_type = input_dict['bolt']['bolt_hole_type']
		self.cal_bolt_holedia = ConnectionCalculations.bolt_hole_clearance(self.bolt_hole_type, self.bolt_diameter)
		self.bolt_hole_diameter = self.cal_bolt_holedia + self.bolt_diameter
		self.edge_dist = int(output_dict['Bolt']['Edge'])
		self.end_dist = int(output_dict['Bolt']['End'])
		self.cross_centre_gauge_dist = int(output_dict['Bolt']['CrossCentreGauge'])  # 90
		# self.pitch = 60

		self.grade = float(input_dict["Bolt"]["Grade"])  # 8.8
		self.Lv = float(output_dict['Bolt']['Lv'])

		self.weld = input_dict["Weld"]["Type"]

		self.stiffener_height = int(output_dict['Stiffener']['Height'])
		self.stiffener_length = int(output_dict['Stiffener']['Length'])
		self.stiffener_thickness = int(output_dict['Stiffener']['Thickness'])
		self.stiffener_notchsize = int(output_dict['Stiffener']['NotchSize'])
		self.stiffener_weldsize = int(output_dict['Stiffener']['WeldSize'])
		self.stiffener_weld = 0

		self.no_of_columns = 2
		self.no_of_bolts = output_dict['Bolt']['NumberOfBolts']
		if self.no_of_bolts == 8:
			self.pitch = float(output_dict['Bolt']['Pitch'])
			self.bolts_outside_top_flange_row = 1
			self.bolts_inside_top_flange_row = 1
			self.bolts_inside_bottom_flange_row = 1
			self.bolts_outside_bottom_flange_row = 1
		elif self.no_of_bolts == 12:
			self.pitch23 = float(output_dict['Bolt']['Pitch23'])
			self.pitch34 = float(output_dict['Bolt']['Pitch34'])
			self.pitch45 = float(output_dict['Bolt']['Pitch45'])
			self.bolts_outside_top_flange_row = 1
			self.bolts_inside_top_flange_row = 2
			self.bolts_inside_bottom_flange_row = 2
			self.bolts_outside_bottom_flange_row = 1
		elif self.no_of_bolts == 16:
			self.pitch23 = float(output_dict['Bolt']['Pitch23'])
			self.pitch34 = float(output_dict['Bolt']['Pitch34'])
			self.pitch45 = float(output_dict['Bolt']['Pitch45'])
			self.pitch56 = float(output_dict['Bolt']['Pitch56'])
			self.pitch67 = float(output_dict['Bolt']['Pitch67'])
			self.bolts_outside_top_flange_row = 1
			self.bolts_inside_top_flange_row = 3
			self.bolts_inside_bottom_flange_row = 3
			self.bolts_outside_bottom_flange_row = 1
		elif self.no_of_bolts == 20:
			self.pitch12 = float(output_dict['Bolt']['Pitch12'])
			self.pitch34 = float(output_dict['Bolt']['Pitch34'])
			self.pitch45 = float(output_dict['Bolt']['Pitch45'])
			self.pitch56 = float(output_dict['Bolt']['Pitch56'])
			self.pitch67 = float(output_dict['Bolt']['Pitch67'])
			self.pitch78 = float(output_dict['Bolt']['Pitch78'])
			self.pitch910 = float(output_dict['Bolt']['Pitch910'])
			self.bolts_outside_top_flange_row = 2
			self.bolts_inside_top_flange_row = 3
			self.bolts_inside_bottom_flange_row = 3
			self.bolts_outside_bottom_flange_row = 2

	def add_s_marker(self, dwg):
		"""

		Args:
			dwg: svgwrite (obj)

		Returns:
			Container for all svg elements

		"""
		smarker = dwg.marker(insert=(8, 3), size=(30, 30), orient="auto")
		smarker.add(dwg.path(d=" M0,0 L3,3 L0,6 L8,3 L0,0", fill="black"))
		dwg.defs.add(smarker)
		return smarker

	def add_section_marker(self, dwg):
		"""

		Args:
			dwg: svgwrite (obj)

		Returns:
			Container for all svg elements

		"""
		section_marker = dwg.marker(insert=(0, 5), size=(10, 10), orient="auto")
		section_marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill="blue", stroke="black"))
		dwg.defs.add(section_marker)
		return section_marker

	def add_e_marker(self, dwg):
		"""

		Args:
			dwg: svgwrite (obj)

		Returns:
			Container for all svg elements

		"""
		emarker = dwg.marker(insert=(0, 3), size=(30, 20), orient="auto")
		emarker.add(dwg.path(d=" M0,3 L8,6 L5,3 L8,0 L0,3", fill="black"))
		dwg.defs.add(emarker)
		return emarker

	def draw_start_arrow(self, line, s_arrow):
		"""

		Args:
			line: start line marker
			s_arrow: start arrow

		Returns:
			None

		"""
		line["marker-start"] = s_arrow.get_funciri()

	def draw_end_arrow(self, line, e_arrow):
		"""

		Args:
			line: end line marker
			e_arrow: end arrow

		Returns:
			None

		"""
		line["marker-end"] = e_arrow.get_funciri()

	def draw_faint_line(self, pt_one, pt_two, dwg):
		"""

		Args:
			pt_one: first point
			pt_two: second point
			dwg: svgwrite (obj)

		Returns:
			None

		"""
		dwg.add(dwg.line(pt_one, pt_two).stroke("#D8D8D8", width=2.5, linecap="square", opacity=0.70))

	def draw_dimension_outer_arrow(self, dwg, pt1, pt2, text, params):
		# TODO

		"""

		Args:
			dwg: svgwrite (obj)
			pt1: first point
			pt2: second point
			text: text message
			params:

		Returns:
			None

		"""
		smarker = self.add_s_marker(dwg)
		emarker = self.add_e_marker(dwg)
		line_vector = pt2 - pt1  # [a, b]
		normal_vector = np.array([-line_vector[1], line_vector[0]])  # [-b, a]
		normal_unit_vector = self.normalize(normal_vector)

		if params["lineori"] == "left":
			normal_unit_vector = -normal_unit_vector

		Q1 = pt1 + params["offset"] * normal_unit_vector
		Q2 = pt2 + params["offset"] * normal_unit_vector
		line = dwg.add(dwg.line(Q1, Q2).stroke("black", width=2.5, linecap="square"))
		self.draw_start_arrow(line, emarker)
		self.draw_end_arrow(line, smarker)

		Q12_mid = 0.5 * (Q1 + Q2)
		text_pt = Q12_mid + params["textoffset"] * normal_unit_vector
		dwg.add(dwg.text(text, insert=text_pt, fill="black", font_family="sans-serif", font_size=28))

		L1 = Q1 + params["endlinedim"] * normal_unit_vector
		L2 = Q1 + params["endlinedim"] * (-normal_unit_vector)
		dwg.add(dwg.line(L1, L2).stroke("black", width=2.5, linecap="square", opacity=1.0))

		L3 = Q2 + params["endlinedim"] * normal_unit_vector
		L4 = Q2 + params["endlinedim"] * (-normal_unit_vector)
		dwg.add(dwg.line(L3, L4).stroke("black", width=2.5, linecap="square", opacity=1.0))

	def normalize(self, vector):
		"""

		Args:
			vector: list containing X, Y ordinates of vector

		Returns:
			vector containing normalized X and Y ordinates

		"""
		a = vector[0]
		b = vector[1]
		magnitude = math.sqrt(a * a + b * b)
		return vector / magnitude

	def draw_cross_section(self, dwg, pt_a, pt_b, text_pt, text):
		"""

		Args:
			dwg: svgwrite (obj)
			pt_a: point A
			pt_b: point B
			text_pt: text point
			text: text message

		Returns:
			None

		"""
		line = dwg.add(dwg.line(pt_a, pt_b).stroke("black", width=2.5, linecap="square"))
		sec_arrow = self.add_section_marker(dwg)
		self.draw_end_arrow(line, sec_arrow)
		dwg.add(dwg.text(text, insert=text_pt, fill="black", font_family="sans-serif", font_size=52))

	def draw_dimension_inner_arrow(self, dwg, pt_a, pt_b, text, params):
		# TODO
		"""

		Args:
			dwg: svgwrite (obj)
			pt_a: point A
			pt_b: point B
			text: text message
			params:
				params["offset"] (float): offset of the dimension line
				params["textoffset"] (float): offset of text from dimension line
				params["lineori"] (float): orientation of line [right/left]
				params["endlinedim"] (float): dimension line at the end of the outer arrow
				params["arrowlen"] (float): size of the arrow

		Returns:
			None

		"""
		smarker = self.add_s_marker(dwg)
		emarker = self.add_e_marker(dwg)
		u = pt_b - pt_a  # [a, b]
		u_unit = self.normalize(u)
		v_unit = np.array([-u_unit[1], u_unit[0]])  # [-b, a]

		A1 = pt_a + params["endlinedim"] * v_unit
		A2 = pt_a + params["endlinedim"] * (-v_unit)
		dwg.add(dwg.line(A1, A2).stroke("black", width=2.5, linecap="square"))

		B1 = pt_b + params["endlinedim"] * v_unit
		B2 = pt_a + params["endlinedim"] * (-v_unit)
		dwg.add(dwg.line(B1, B2).stroke("black", width=2.5, linecap="square"))

		A3 = pt_a - params["arrowlen"] * u_unit
		B3 = pt_b + params["arrowlen"] * u_unit
		line = dwg.add(dwg.line(A3, pt_a).stroke("black", width=2.5, linecap="square"))
		self.draw_end_arrow(line, smarker)

		line = dwg.add(dwg.line(B3, pt_b).stroke("black", width=2.5, linecap="butt"))
		self.draw_end_arrow(line, smarker)

		if params["lineori"] == "right":
			text_pt = B3 + params["textoffset"] * u_unit
		else:
			text_pt = A3 - (params["textoffset"] + 100) * u_unit

		dwg.add(dwg.text(text, insert=text_pt, fill="black", font_family='sans-serif', font_size=28))

	def draw_oriented_arrow(self, dwg, point, theta, orientation, offset, textup, textdown, element):
		"""

		Args:
			dwg: svgwrite (obj)
			point: point
			theta: theta
			orientation: direction (east, west, south, north)
			offset: position of the text
			textup: text written above line
			textdown: text written below line

		Returns:
			None

		"""
		# Right Up.
		theta = math.radians(theta)
		char_width = 16
		x_vector = np.array([1, 0])
		y_vector = np.array([0, 1])

		p1 = point
		length_A = offset / (math.sin(theta))

		arrow_vector = None
		if orientation == "NE":
			arrow_vector = np.array([-math.cos(theta), math.sin(theta)])
		elif orientation == "NW":
			arrow_vector = np.array([math.cos(theta), math.sin(theta)])
		elif orientation == "SE":
			arrow_vector = np.array([-math.cos(theta), -math.sin(theta)])
		elif orientation == "SW":
			arrow_vector = np.array([math.cos(theta), -math.sin(theta)])
		p2 = p1 - length_A * arrow_vector

		text = textdown if len(textdown) > len(textup) else textup
		length_B = len(text) * char_width

		label_vector = None
		if orientation == "NE":
			label_vector = -x_vector
		elif orientation == "NW":
			label_vector = x_vector
		elif orientation == "SE":
			label_vector = -x_vector
		elif orientation == "SW":
			label_vector = x_vector
		p3 = p2 + length_B * (-label_vector)

		text_offset = 18
		offset_vector = -y_vector

		text_point_up = None
		text_point_down = None
		if orientation == "NE":
			text_point_up = p2 + 0.2 * length_B * (-label_vector) + text_offset * offset_vector
			text_point_down = p2 - 0.2 * length_B * label_vector - (text_offset + 15) * offset_vector
		elif orientation == "NW":
			text_point_up = p3 + 0.05 * length_B * (label_vector) + text_offset * offset_vector
			text_point_down = p3 - 0.05 * length_B * label_vector - (text_offset + 15) * offset_vector
		elif orientation == "SE":
			text_point_up = p2 + 0.2 * length_B * (-label_vector) + text_offset * offset_vector
			text_point_down = p2 - 0.2 * length_B * label_vector - (text_offset + 15) * offset_vector
		elif orientation == "SW":
			text_point_up = p3 + 0.05 * length_B * (label_vector) + text_offset * offset_vector
			text_point_down = p3 - 0.05 * length_B * label_vector - (text_offset + 15) * offset_vector

		line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill="none", stroke='black', stroke_width=2.5))

		emarker = self.add_e_marker(dwg)
		self.draw_start_arrow(line, emarker)

		dwg.add(dwg.text(textup, insert=text_point_up, fill='black', font_family='sans-serif', font_size=28))
		dwg.add(dwg.text(textdown, insert=text_point_down, fill='black', font_family='sans-serif', font_size=28))

		if element == "weld":
			if self.weld == "Fillet Weld":
				if orientation == "NE":
					self.draw_weld_marker1(dwg, 30, 7.5, line)
				else:
					self.draw_weld_marker2(dwg, 30, 7.5, line)
			else:
				if orientation == "NE":
					self.draw_weld_marker3(dwg, 15, -8.5, line)
				else:
					self.draw_weld_marker4(dwg, 15, 8.5, line)

			if self.stiffener_weld == 1:
				if orientation == "NE":
					self.draw_weld_marker1(dwg, 30, 7.5, line)
				else:
					self.draw_weld_marker2(dwg, 30, 7.5, line)
			else:
				pass

			print "successful"

	def draw_weld_marker1(self, dwg, oriX, oriY, line):
		weldMarker = dwg.marker(insert=(oriX, oriY), size=(15, 15), orient="auto")
		# weldMarker.add(dwg.path(d="M 0 0 L 8 7.5 L 0 15 z", fill='none', stroke='black'))
		weldMarker.add(dwg.path(d="M 15 7.5 L 8 0 L 8 15 z", fill='none', stroke='black'))
		dwg.defs.add(weldMarker)
		self.draw_end_arrow(line, weldMarker)

	def draw_weld_marker2(self, dwg, oriX, oriY, line):
		weldMarker = dwg.marker(insert=(oriX, oriY), size=(15, 15), orient="auto")
		# weldMarker.add(dwg.path(d="M 0 0 L 8 7.5 L 0 15 z", fill='none', stroke='black'))
		weldMarker.add(dwg.path(d="M 0 7.5 L 8 0 L 8 15 z", fill='none', stroke='black'))
		dwg.defs.add(weldMarker)
		self.draw_end_arrow(line, weldMarker)

	def draw_weld_marker3(self, dwg, oriX, oriY, line):
		weldMarker = dwg.marker(insert=(oriX, oriY), size=(15, 15), orient="auto")
		# weldMarker.add(dwg.path(d="M 0 0 L 8 7.5 L 0 15 z", fill='none', stroke='black'))
		weldMarker.add(dwg.path(d="M 0 0 L 0 -7.5 L 7.5 0 ", fill='none', stroke='black'))
		dwg.defs.add(weldMarker)
		self.draw_end_arrow(line, weldMarker)

	def draw_weld_marker4(self, dwg, oriX, oriY, line):
		weldMarker = dwg.marker(insert=(oriX, oriY), size=(15, 15), orient="auto")
		# weldMarker.add(dwg.path(d="M 0 0 L 8 7.5 L 0 15 z", fill='none', stroke='black'))
		weldMarker.add(dwg.path(d="M 0 0 L 0 7.5 L -7.5 0 ", fill='none', stroke='black'))
		dwg.defs.add(weldMarker)
		self.draw_end_arrow(line, weldMarker)

	def save_to_svg(self, filename, view):
		"""

		Args:
			filename: path of the folder
			view: front, top, side views of drawings to be generated

		Returns:
			None

		Note:


		"""
		extnd_bothway_end_2d_front = ExtendedEnd2DFront(self)
		extnd_bothway_end_2d_top = ExtendedEnd2DTop(self)
		extnd_bothway_end_2d_side = ExtendedEnd2DSide(self)

		if view == "Front":
			extnd_bothway_end_2d_front.call_ExtndBoth_front(filename)
		elif view == "Top":
			extnd_bothway_end_2d_top.call_ExtndBoth_top(filename)
		elif view == "Side":
			extnd_bothway_end_2d_side.call_ExtndBoth_side(filename)
		else:
			filename = os.path.join(str(self.folder), 'images_html', 'extendFront.svg')
			extnd_bothway_end_2d_front.call_ExtndBoth_front(filename)
			cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "extendFront.png"))

			filename = os.path.join(str(self.folder), 'images_html', 'extendTop.svg')
			extnd_bothway_end_2d_top.call_ExtndBoth_top(filename)
			cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "extendTop.png"))

			filename = os.path.join(str(self.folder), 'images_html', 'extendSide.svg')
			extnd_bothway_end_2d_side.call_ExtndBoth_side(filename)
			cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "extendSide.png"))


class ExtendedEnd2DFront(object):
	"""
	Contains functions for generating the front view of the Extended bothway endplate connection.
	"""

	def __init__(self, extnd_common_object):

		self.data_object = extnd_common_object

		# --------------------------------------------------------------------------
		#                               FRONT VIEW
		# --------------------------------------------------------------------------
		# ================ Primary Beam 1 ================

		ptA1x = 0
		ptA1y = 0
		self.A1 = np.array([ptA1x, ptA1y])

		ptA2x = ptA1x + self.data_object.beam_length_L1
		ptA2y = 0
		self.A2 = np.array([ptA2x, ptA2y])

		ptA6x = ptA2x
		ptA6y = ptA2y + self.data_object.flange_thickness_T1
		self.A6 = np.array([ptA6x, ptA6y])

		ptA7x = ptA2x
		ptA7y = ptA2y + (self.data_object.beam_depth_D1 - self.data_object.flange_thickness_T1)
		self.A7 = np.array([ptA7x, ptA7y])

		ptA3x = ptA2x
		ptA3y = ptA2y + self.data_object.beam_depth_D1
		self.A3 = np.array([ptA3x, ptA3y])

		ptA4x = ptA1x
		ptA4y = ptA1y + self.data_object.beam_depth_D1
		self.A4 = np.array([ptA4x, ptA4y])

		ptA8x = ptA1x
		ptA8y = ptA4y - self.data_object.flange_thickness_T1  # (self.data_object.beam_depth_D1 - self.data_object.flange_thickness_T1)
		self.A8 = np.array([ptA8x, ptA8y])

		ptA5x = ptA1x
		ptA5y = self.data_object.flange_thickness_T1
		self.A5 = np.array([ptA5x, ptA5y])

		self.Q = self.A6 + self.data_object.web_weld_thickness * np.array([-1, 0])

		# =========================  End Plate 1  =========================

		ptP1x = self.data_object.beam_length_L1
		ptP1y = -(self.data_object.plate_length_L1 - self.data_object.beam_depth_D1) / 2
		self.P1 = np.array([ptP1x, ptP1y])

		ptP2x = ptP1x + self.data_object.plate_thickness_p1
		ptP2y = ptP1y
		self.P2 = np.array([ptP2x, ptP2y])

		ptP3x = ptP2x
		ptP3y = (self.data_object.plate_length_L1 + self.data_object.beam_depth_D1) / 2
		self.P3 = np.array([ptP3x, ptP3y])

		ptP4x = ptP1x
		ptP4y = ptP3y
		self.P4 = np.array([ptP4x, ptP4y])

		if self.data_object.weld == "Fillet Weld":
			# ------------------------------------------  Weld triangle  UP-------------------------------------------
			self.B3 = self.A2
			self.B2 = self.B3 + self.data_object.flange_weld_thickness * np.array([-1, 0])
			self.B1 = self.B3 + self.data_object.flange_weld_thickness * np.array([0, -1])

			self.B6 = self.A3
			self.B5 = self.B6 + self.data_object.flange_weld_thickness * np.array([-1, 0])
			self.B4 = self.B6 + self.data_object.flange_weld_thickness * np.array([0, 1])

			# ------------------------------------------  Weld triangle  DOWN -------------------------------------------
			self.B7 = self.A6
			self.B8 = self.B7 + self.data_object.flange_weld_thickness * np.array([0, 1])
			self.B9 = self.B7 + self.data_object.flange_weld_thickness * np.array([-1, 0])

			self.B11 = self.A7
			self.B12 = self.B11 + self.data_object.flange_weld_thickness * np.array([-1, 0])
			self.B13 = self.B11 + self.data_object.flange_weld_thickness * np.array([0, -1])
		else:
			# ------------------------------------------  Weld triangle  UP-------------------------------------------
			self.B3 = self.A2
			self.B2 = self.B3 + self.data_object.flange_thickness_T1 * np.array([-1, 0])
			self.B1 = self.B3 + self.data_object.flange_thickness_T1 * np.array([0, 1])

			self.B6 = self.A3
			self.B5 = self.B6 + self.data_object.flange_thickness_T1 * np.array([-1, 0])
			self.B4 = self.B6 + self.data_object.flange_thickness_T1 * np.array([0, -1])

		# =========================  End Plate 2  =========================

		ptPP1x = ptP2x
		ptPP1y = -(self.data_object.plate_length_L2 - self.data_object.beam_depth_D2) / 2
		self.PP1 = np.array([ptPP1x, ptPP1y])

		ptPP2x = ptPP1x + self.data_object.plate_thickness_p2
		ptPP2y = ptPP1y
		self.PP2 = np.array([ptPP2x, ptPP2y])

		ptPP3x = ptPP2x
		ptPP3y = (self.data_object.plate_length_L2 + self.data_object.beam_depth_D2) / 2
		self.PP3 = np.array([ptPP3x, ptPP3y])

		ptPP4x = ptPP1x
		ptPP4y = ptPP3y
		self.PP4 = np.array([ptPP4x, ptPP4y])

		# =========================  Primary Beam 2  =========================

		ptAA1x = ptPP2x  # self.data_object.beam_length_L1 + self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2
		ptAA1y = 0
		self.AA1 = np.array([ptAA1x, ptAA1y])

		ptAA2x = ptAA1x + self.data_object.beam_length_L2
		ptAA2y = 0
		self.AA2 = np.array([ptAA2x, ptAA2y])

		ptAA6x = ptAA2x
		ptAA6y = self.data_object.flange_thickness_T2
		self.AA6 = np.array([ptAA6x, ptAA6y])

		ptAA7x = ptAA2x
		ptAA7y = (self.data_object.beam_depth_D2 - self.data_object.flange_thickness_T2)
		self.AA7 = np.array([ptAA7x, ptAA7y])

		ptAA3x = ptAA2x
		ptAA3y = self.data_object.beam_depth_D2
		self.AA3 = np.array([ptAA3x, ptAA3y])

		ptAA4x = ptAA1x
		ptAA4y = self.data_object.beam_depth_D2
		self.AA4 = np.array([ptAA4x, ptAA4y])

		ptAA8x = ptAA1x
		ptAA8y = (self.data_object.beam_depth_D2 - self.data_object.flange_thickness_T2)
		self.AA8 = np.array([ptAA8x, ptAA8y])

		ptAA5x = ptAA1x
		ptAA5y = self.data_object.flange_thickness_T2
		self.AA5 = np.array([ptAA5x, ptAA5y])

		if self.data_object.weld == "Fillet Weld":
			# ------------------------------------------  Weld triangle UP -------------------------------------------
			self.BB3 = self.AA1
			self.BB2 = self.BB3 + self.data_object.flange_weld_thickness * np.array([1, 0])
			self.BB1 = self.BB3 + self.data_object.flange_weld_thickness * np.array([0, -1])

			self.BB7 = self.AA5
			self.BB8 = self.BB7 + self.data_object.flange_weld_thickness * np.array([0, 1])
			self.BB9 = self.BB7 + self.data_object.flange_weld_thickness * np.array([1, 0])

			# ------------------------------------------  Weld triangle  DOWN -------------------------------------------
			self.BB6 = self.AA4
			self.BB5 = self.BB6 + self.data_object.flange_weld_thickness * np.array([1, 0])
			self.BB4 = self.BB6 + self.data_object.flange_weld_thickness * np.array([0, 1])

			self.BB11 = self.AA8
			self.BB12 = self.BB11 + self.data_object.flange_weld_thickness * np.array([1, 0])
			self.BB13 = self.BB11 + self.data_object.flange_weld_thickness * np.array([0, -1])


		else:
			self.BB3 = self.AA1
			self.BB2 = self.BB3 + self.data_object.flange_thickness_T2 * np.array([1, 0])
			self.BB1 = self.BB3 + self.data_object.flange_thickness_T2 * np.array([0, 1])

			self.BB6 = self.AA4
			self.BB5 = self.BB6 + self.data_object.flange_thickness_T2 * np.array([1, 0])
			self.BB4 = self.BB6 + self.data_object.flange_thickness_T2 * np.array([0, -1])

		# self.Lv = self.PP2 + ((self.data_object.plate_length_L2 - self.data_object.beam_depth_D2) / 2 - self.data_object.end_dist - self.data_object.flange_weld_thickness)
		# ========================= Stiffener Top Right =========================

		ptS1x = ptPP2x
		ptS1y = ptAA1y - self.data_object.stiffener_height
		self.S1 = np.array([ptS1x, ptS1y])

		ptS2x = ptS1x + 25
		ptS2y = ptS1y
		self.S2 = np.array([ptS2x, ptS2y])

		ptS6x = ptS1x
		ptS6y = ptAA1y - self.data_object.stiffener_notchsize
		self.S6 = np.array([ptS6x, ptS6y])

		ptS5x = ptS1x + self.data_object.stiffener_notchsize
		ptS5y = ptAA1y
		self.S5 = np.array([ptS5x, ptS5y])

		ptS4x = ptAA1x + self.data_object.stiffener_length
		ptS4y = ptAA1y
		self.S4 = np.array([ptS4x, ptS4y])

		ptS3x = ptS4x
		ptS3y = ptS4y - 25
		self.S3 = np.array([ptS3x, ptS3y])

		# ========================= Stiffener Top Left =========================

		ptSS1x = ptA2x
		ptSS1y = ptA2y - self.data_object.stiffener_height
		self.SS1 = np.array([ptSS1x, ptSS1y])

		ptSS2x = ptSS1x - 25
		ptSS2y = ptSS1y
		self.SS2 = np.array([ptSS2x, ptSS2y])

		ptSS6x = ptSS1x
		ptSS6y = ptA2y - self.data_object.stiffener_notchsize
		self.SS6 = np.array([ptSS6x, ptSS6y])

		ptSS5x = ptSS1x - self.data_object.stiffener_notchsize
		ptSS5y = ptA2y
		self.SS5 = np.array([ptSS5x, ptSS5y])

		ptSS4x = ptA2x - self.data_object.stiffener_length
		ptSS4y = ptA2y
		self.SS4 = np.array([ptSS4x, ptSS4y])

		ptSS3x = ptSS4x
		ptSS3y = ptSS4y - 25
		self.SS3 = np.array([ptSS3x, ptSS3y])

		# ========================= Stiffener Bottom Right =========================

		ptBS1x = ptPP3x
		ptBS1y = ptAA4y + self.data_object.stiffener_height
		self.BS1 = np.array([ptBS1x, ptBS1y])

		ptBS2x = ptBS1x + 25
		ptBS2y = ptBS1y
		self.BS2 = np.array([ptBS2x, ptBS2y])

		ptBS6x = ptBS1x
		ptBS6y = ptAA4y + self.data_object.stiffener_notchsize
		self.BS6 = np.array([ptBS6x, ptBS6y])

		ptBS5x = ptBS1x + self.data_object.stiffener_notchsize
		ptBS5y = ptAA4y
		self.BS5 = np.array([ptBS5x, ptBS5y])

		ptBS4x = ptAA4x + self.data_object.stiffener_length
		ptBS4y = ptAA4y
		self.BS4 = np.array([ptBS4x, ptBS4y])

		ptBS3x = ptBS4x
		ptBS3y = ptBS4y + 25
		self.BS3 = np.array([ptBS3x, ptBS3y])

		# ========================= Stiffener Bottom Left =========================

		ptBSS1x = ptA3x
		ptBSS1y = ptA3y + self.data_object.stiffener_height
		self.BSS1 = np.array([ptBSS1x, ptBSS1y])

		ptBSS2x = ptBSS1x - 25
		ptBSS2y = ptBSS1y
		self.BSS2 = np.array([ptBSS2x, ptBSS2y])

		ptBSS6x = ptBSS1x
		ptBSS6y = ptA3y + self.data_object.stiffener_notchsize
		self.BSS6 = np.array([ptBSS6x, ptBSS6y])

		ptBSS5x = ptBSS1x - self.data_object.stiffener_notchsize
		ptBSS5y = ptA3y
		self.BSS5 = np.array([ptBSS5x, ptBSS5y])

		ptBSS4x = ptA3x - self.data_object.stiffener_length
		ptBSS4y = ptA3y
		self.BSS4 = np.array([ptBSS4x, ptBSS4y])

		ptBSS3x = ptBSS4x
		ptBSS3y = ptBSS4y + 25
		self.BSS3 = np.array([ptBSS3x, ptBSS3y])

	def call_ExtndBoth_front(self, filename):
		"""

		Args:
			filename: path of the images to be saved

		Returns:
			Saves the image in the folder

		"""
		vb_width = (int(2 * self.data_object.beam_length_L1 + 2 * self.data_object.plate_thickness_p1 + 300))
		vb_ht = (int(3 * self.data_object.plate_length_L1))
		dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=(
			'-350 -600 2000 1740'))  # 200 = move towards left , 600= move towards down, 2300= width of view, 1740= height of view
		dwg.add(dwg.polyline(points=[self.A1, self.A2, self.A3, self.A4, self.A1], stroke='blue', fill='none', stroke_width=2.5))
		dwg.add(dwg.line(self.A5, self.A6).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.A8, self.A7).stroke('blue', width=2.5, linecap='square'))

		dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width='2.5'))
		dwg.add(dwg.polyline(points=[self.PP1, self.PP2, self.PP3, self.PP4, self.PP1], stroke='blue', fill='none', stroke_width=2.5))

		dwg.add(dwg.polyline(points=[self.AA1, self.AA2, self.AA3, self.AA4, self.AA1], stroke='blue', fill='none', stroke_width=2.5))
		dwg.add(dwg.line(self.AA5, self.AA6).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.AA8, self.AA7).stroke('blue', width=2.5, linecap='square'))

		dwg.add(dwg.line(self.S1, self.S2).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.S2, self.S3).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.S3, self.S4).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.S5, self.S6).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.SS1, self.SS2).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.SS2, self.SS3).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.SS3, self.SS4).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.SS5, self.SS6).stroke('blue', width=2.5, linecap='square'))

		dwg.add(dwg.line(self.BS1, self.BS2).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BS2, self.BS3).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BS3, self.BS4).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BS5, self.BS6).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BSS1, self.BSS2).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BSS2, self.BSS3).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BSS3, self.BSS4).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.BSS5, self.BSS6).stroke('blue', width=2.5, linecap='square'))

		if self.data_object.weld == "Fillet Weld":
			pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse",
											   patternTransform="rotate(45 2 2)"))
			pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
			dwg.add(dwg.rect(insert=self.Q, size=(self.data_object.web_weld_thickness, (
					self.data_object.beam_depth_D1 - self.data_object.flange_thickness_T1 - self.data_object.flange_weld_thickness - 10)),
							 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
			dwg.add(dwg.rect(insert=self.AA5, size=(self.data_object.web_weld_thickness, (
					self.data_object.beam_depth_D2 - self.data_object.flange_thickness_T2 - self.data_object.flange_weld_thickness - 10)),
							 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		else:
			pass

		if self.data_object.weld == "Fillet Weld":
			dwg.add(dwg.polyline(points=[self.B3, self.B2, self.B1, self.B3], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.B6, self.B5, self.B4, self.B6], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.B7, self.B8, self.B9, self.B7], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.B11, self.B12, self.B13, self.B11], stroke='black', fill='black',
								 stroke_width=2.5))

			dwg.add(dwg.polyline(points=[self.BB3, self.BB2, self.BB1, self.BB3], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.BB6, self.BB5, self.BB4, self.BB6], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.BB8, self.BB7, self.BB9, self.BB8], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.BB12, self.BB11, self.BB13, self.BB12], stroke='black', fill='black',
								 stroke_width=2.5))
		else:
			dwg.add(dwg.polyline(points=[self.B3, self.B2, self.B1, self.B3], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.B6, self.B5, self.B4, self.B6], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.BB3, self.BB2, self.BB1, self.BB3], stroke='black', fill='black',
								 stroke_width=2.5))
			dwg.add(dwg.polyline(points=[self.BB6, self.BB5, self.BB4, self.BB6], stroke='black', fill='black',
								 stroke_width=2.5))
		botfr = self.data_object.bolts_outside_top_flange_row
		bitfr = self.data_object.bolts_inside_top_flange_row
		bolt_r = int(self.data_object.bolt_diameter) / 2

		# ------------------------------------------  Bolts Outside Top Flange -------------------------------------------

		pt_outside_top_column_list = []
		for i in range(1, botfr + 1):
			if self.data_object.no_of_bolts == 20:
				ptx = self.PP2 + (self.data_object.end_dist) * np.array([0, 1]) - (
							self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) \
					  * np.array([1, 0]) + (i - 1) * self.data_object.pitch12 * np.array([0, 1])
				ptx1 = ptx - bolt_r * np.array([0, 1])
				rect_width = float(self.data_object.bolt_diameter)
				rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
				dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black',
								 stroke_width=2.5))
			else:
				ptx = self.PP2 + (self.data_object.end_dist) * np.array([0, 1]) - \
					  (self.data_object.plate_thickness_p1 +self.data_object.plate_thickness_p2) * np.array([1, 0])
				ptx1 = ptx - bolt_r * np.array([0, 1])
				rect_width = float(self.data_object.bolt_diameter)
				rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
				dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black',
								 stroke_width=2.5))

			pt_Cx = ptx + np.array([1, 0])
			pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
			dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
			pt_outside_top_column_list.append(ptx)

			pt_Cx1 = ptx + np.array([-1, 0])
			pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
			dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
			pt_outside_top_column_list.append(ptx)

		# ------------------------------------------  Bolts Inside Top Flange -------------------------------------------
		pt_inside_top_column_list = []
		for i in range(bitfr):
			if self.data_object.no_of_bolts == 8:
				ptx = self.AA1 + (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness ) * np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch * np.array([0, 1])
			elif self.data_object.no_of_bolts == 12:
				ptx = self.AA1 + (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch23 * np.array([0, 1])
			elif self.data_object.no_of_bolts == 16:
				ptx = self.AA1 + (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) +  i * self.data_object.pitch23 * np.array([0, 1])
			else:
				ptx = self.AA1 + (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness)* np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch34 * np.array([0, 1])

			ptx1 = ptx - bolt_r * np.array([0, 1])
			rect_width = float(self.data_object.bolt_diameter)
			rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
			dwg.add(
				dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

			pt_Cx = ptx + np.array([1, 0])
			pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
			dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
			pt_inside_top_column_list.append(ptx)

			pt_Cx1 = ptx + np.array([-1, 0])
			pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
			dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
			pt_inside_top_column_list.append(ptx)

			bobfr = self.data_object.bolts_outside_bottom_flange_row
			bibfr = self.data_object.bolts_inside_bottom_flange_row

		# ------------------------------------------  Bolts Outside Bottom Flange -------------------------------------------
		pt_outside_bottom_column_list = []
		for i in range(bobfr):
			if self.data_object.no_of_bolts == 20:
				ptx = self.PP3 + (self.data_object.end_dist) * np.array([0, -1]) - (
						self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array([1, 0]) - (i - 1) * self.data_object.pitch910 * np.array([0, -1])
				ptx1 = ptx - bolt_r * np.array([0, 1])
				rect_width = float(self.data_object.bolt_diameter)
				rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
				dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black',
								 stroke_width=2.5))
			else:
				ptx = self.PP3 + (self.data_object.end_dist) * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0])  # + column * self.data_object.gauge * np.array([0, 1])

			ptx1 = ptx - bolt_r * np.array([0, 1])
			rect_width = float(self.data_object.bolt_diameter)
			rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
			dwg.add(
				dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

			pt_Cx = ptx + np.array([1, 0])
			pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
			dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
			pt_outside_bottom_column_list.append(ptx)
			pt_Cx1 = ptx + np.array([-1, 0])
			pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
			dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
			pt_outside_bottom_column_list.append(ptx)

		# ------------------------------------------  Bolts Inside Bottom Flange -------------------------------------------
		pt_inside_bottom_column_list = []
		for i in range(bibfr):
			if self.data_object.no_of_bolts == 8:
				ptx = self.AA4 - (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness) \
					  * np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch * np.array([0, -1])
			elif self.data_object.no_of_bolts == 12:
				ptx = self.AA4 - (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness) \
					  * np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch23 * np.array([0, -1])
			elif self.data_object.no_of_bolts == 16:
				ptx = self.AA4 - (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness) \
					  * np.array([0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch23 * np.array([0, -1])
			else:
				ptx = self.AA4 - (self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array(
					[0, 1]) - (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2) * np.array(
					[1, 0]) + i * self.data_object.pitch34 * np.array([0, -1])

			ptx1 = ptx - bolt_r * np.array([0, 1])
			rect_width = float(self.data_object.bolt_diameter)
			rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
			dwg.add(
				dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

			pt_Cx = ptx + np.array([1, 0])
			pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
			dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
			pt_inside_bottom_column_list.append(ptx)

			pt_Cx1 = ptx + np.array([-1, 0])
			pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
			dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
			pt_inside_bottom_column_list.append(ptx)

		# ------------------------------------------  Labeling Outside top bolt of flange -------------------------------------------
		no_of_bolts_flange = self.data_object.bolts_outside_top_flange_row * self.data_object.no_of_columns
		point = np.array(pt_outside_top_column_list[0])
		theta = 60
		offset = 50
		textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
		textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(
			self.data_object.grade) + ")"
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		# ------------------------------------------  Labeling Outside bottom bolt of flange -------------------------------------------
		no_of_bolts_flange = self.data_object.bolts_outside_bottom_flange_row * self.data_object.no_of_columns
		point = np.array(pt_outside_bottom_column_list[0])
		theta = 60
		offset = 50
		textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
		textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(
			self.data_object.grade) + ")"
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown, element)

		# ------------------------------------------  Labeling Inside top bolt of flange -------------------------------------------
		no_of_bolts_flange = self.data_object.bolts_inside_top_flange_row * self.data_object.no_of_columns
		point = np.array(pt_inside_top_column_list[0])
		theta = 60
		offset = 50
		textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
		textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(
			self.data_object.grade) + ")"
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		# ------------------------------------------  Labeling Inside bottom bolt of flange -------------------------------------------
		no_of_bolts_flange = self.data_object.bolts_inside_bottom_flange_row * self.data_object.no_of_columns
		point = np.array(pt_inside_bottom_column_list[1])
		theta = 60
		offset = 50
		textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
		textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(
			self.data_object.grade) + ")"
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown, element)

		# ------------------------------------------  Labeling Weld of flange -------------------------------------------
		if self.data_object.weld == "Fillet Weld":
			point = self.B2
			theta = 60
			offset = 150
			textup = "          z " + str(self.data_object.flange_weld_thickness)
			textdown = "          z " + str(self.data_object.flange_weld_thickness)
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
		else:
			point = self.B2
			theta = 60
			offset = 100
			textup = "               "
			textdown = "               "
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------  Labeling Weld of Web -------------------------------------------
		if self.data_object.weld == "Fillet Weld":
			point = self.AA5 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
			theta = 60
			offset = 100
			textup = "         z  " + str(self.data_object.web_weld_thickness)
			textdown = "         z  " + str(self.data_object.web_weld_thickness)
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
		else:
			point = self.AA5 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
			theta = 60
			offset = 100
			textup = "               "
			textdown = "               "
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------  Primary Beam 1& 2 -------------------------------------------
		point = self.A1 + 50 * np.array([1, 0])
		theta = 60
		offset = 25
		textup = "Beam " + str(self.data_object.beam_designation)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		point = self.AA2 - 300 * np.array([1, 0])
		theta = 60
		offset = 25
		textup = "Beam " + str(self.data_object.beam_designation)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------  End Plate 1 & 2-------------------------------------------
		point = self.P1
		theta = 60
		offset = 100
		textup = "End Plate " + str(self.data_object.plate_length_L1) + "x" + str(self.data_object.plate_width_B1) + "x" + str(
			self.data_object.plate_thickness_p1)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		point = self.PP2
		theta = 60
		offset = 100
		textup = "End Plate " + str(self.data_object.plate_length_L2) + "x" + str(self.data_object.plate_width_B2) + "x" + str(
			self.data_object.plate_thickness_p2)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------ Stiffener -------------------------------------------------
		point = self.BS3
		theta = 60
		offset = 50
		textup = "Stiffener " + str(self.data_object.stiffener_height) + "x" + str(
			self.data_object.stiffener_length) + "x" + str(
			self.data_object.stiffener_thickness)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "SE", offset, textup, textdown, element)

		# ------------------------------------------  Sectional arrow -------------------------------------------
		pt_a1 = self.A1 + 500 * np.array([0, -1])
		pt_b1 = pt_a1 + (50 * np.array([0, 1]))
		txt_1 = pt_b1 + (10 * np.array([-1, 0])) + (60 * np.array([0, 1]))
		text = "A"
		self.data_object.draw_cross_section(dwg, pt_a1, pt_b1, txt_1, text)

		pt_a2 = pt_a1 + (2 * self.data_object.beam_length_L1 + 2 * self.data_object.plate_thickness_p1) * np.array([1, 0])
		pt_b2 = pt_a2 + (50 * np.array([0, 1]))
		txt_2 = pt_b2 + (10 * np.array([-1, 0])) + (60 * np.array([0, 1]))
		self.data_object.draw_cross_section(dwg, pt_a2, pt_b2, txt_2, text)

		dwg.add(dwg.line(pt_a1, pt_a2).stroke('black', width=1.5, linecap='square'))

		# ------------------------------------------  View details-------------------------------------------
		ptx = self.P4 - 100 * np.array([1, 0]) + 200 * np.array([0, 1])
		dwg.add(dwg.text('Front view (Sec C-C) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
		ptx1 = ptx + 40 * np.array([0, 1])
		dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

		dwg.save()


class ExtendedEnd2DTop(object):
	"""
	Contains functions for generating the top view of the Extended bothway endplate connection.

	"""

	def __init__(self, extnd_common_object):
		self.data_object = extnd_common_object
		# -------------------------------------------------------------------------------------------------
		#                                           TOP VIEW
		# -------------------------------------------------------------------------------------------------
		# ====================== Primary Beam 1  =====================

		ptA1x = 0
		ptA1y = 0
		self.A1 = np.array([ptA1x, ptA1y])

		ptA2x = ptA1x + self.data_object.beam_length_L1
		ptA2y = 0
		self.A2 = np.array([ptA2x, ptA2y])

		ptA7x = ptA2x
		ptA7y = ptA2y + (self.data_object.beam_width_B1 - self.data_object.web_thickness_tw1) / 2
		self.A7 = np.array([ptA7x, ptA7y])

		ptAS7x = ptA7x - self.data_object.stiffener_length
		ptAS7y = ptA7y
		self.AS7 = np.array([ptAS7x, ptAS7y])

		ptA8x = ptA2x
		ptA8y = ptA7y + self.data_object.web_thickness_tw1
		self.A8 = np.array([ptA8x, ptA8y])

		ptAS8x = ptA8x - self.data_object.stiffener_length
		ptAS8y = ptA8y
		self.AS8 = np.array([ptAS8x, ptAS8y])

		ptA3x = ptA2x
		ptA3y = ptA2y + self.data_object.beam_width_B1
		self.A3 = np.array([ptA3x, ptA3y])

		ptA4x = 0
		ptA4y = ptA1y + self.data_object.beam_width_B1
		self.A4 = np.array([ptA4x, ptA4y])

		ptA5x = 0
		ptA5y = ptA1y + (self.data_object.beam_width_B1 + self.data_object.web_thickness_tw1) / 2
		self.A5 = np.array([ptA5x, ptA5y])

		ptA6x = 0
		ptA6y = ptA5y - self.data_object.web_thickness_tw1
		self.A6 = np.array([ptA6x, ptA6y])

		# ------------------------------------------  Weld triangle  UP-------------------------------------------
		self.B1 = self.A7
		self.B2 = self.B1 + self.data_object.web_weld_thickness * np.array([-1, 0])
		self.B3 = self.B1 + self.data_object.web_weld_thickness * np.array([0, -1])

		# ------------------------------------------  Weld triangle  DOWN -------------------------------------------
		self.B4 = self.A8
		self.B5 = self.B4 + self.data_object.web_weld_thickness * np.array([-1, 0])
		self.B6 = self.B4 + self.data_object.web_weld_thickness * np.array([0, 1])

		# ====================== End Plate 1  =====================
		ptP1x = self.data_object.beam_length_L1
		ptP1y = -(self.data_object.plate_width_B1 - self.data_object.beam_width_B1) / 2
		self.P1 = np.array([ptP1x, ptP1y])

		ptP2x = ptP1x + self.data_object.plate_thickness_p1
		ptP2y = ptP1y
		self.P2 = np.array([ptP2x, ptP2y])

		ptP3x = ptP2x
		ptP3y = (self.data_object.plate_width_B1 + self.data_object.beam_width_B1) / 2
		self.P3 = np.array([ptP3x, ptP3y])

		ptP4x = ptP1x
		ptP4y = ptP3y
		self.P4 = np.array([ptP4x, ptP4y])

		# ====================== End Plate 2  =====================
		ptPP1x = ptP2x
		ptPP1y = -(self.data_object.plate_width_B2 - self.data_object.beam_width_B2) / 2
		self.PP1 = np.array([ptPP1x, ptPP1y])

		ptPP2x = ptPP1x + self.data_object.plate_thickness_p2
		ptPP2y = ptPP1y
		self.PP2 = np.array([ptPP2x, ptPP2y])

		ptPP3x = ptPP2x
		ptPP3y = (self.data_object.plate_width_B2 + self.data_object.beam_width_B2) / 2
		self.PP3 = np.array([ptPP3x, ptPP3y])

		ptPP4x = ptPP1x
		ptPP4y = ptPP3y
		self.PP4 = np.array([ptPP4x, ptPP4y])

		# ====================== Primary Beam 2  =====================
		ptAA1x = ptPP2x
		ptAA1y = 0
		self.AA1 = np.array([ptAA1x, ptAA1y])

		ptAA2x = ptAA1x + self.data_object.beam_length_L2
		ptAA2y = 0
		self.AA2 = np.array([ptAA2x, ptAA2y])

		ptAA7x = ptAA2x
		ptAA7y = ptAA2y + (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2) / 2
		self.AA7 = np.array([ptAA7x, ptAA7y])

		ptAA8x = ptAA2x
		ptAA8y = ptAA7y + self.data_object.web_thickness_tw2
		self.AA8 = np.array([ptAA8x, ptAA8y])

		ptAA3x = ptAA2x
		ptAA3y = ptAA2y + self.data_object.beam_width_B2
		self.AA3 = np.array([ptAA3x, ptAA3y])

		ptAA4x = ptAA1x
		ptAA4y = ptAA1y + self.data_object.beam_width_B2
		self.AA4 = np.array([ptAA4x, ptAA4y])

		ptAA5x = ptAA1x
		ptAA5y = ptAA4y - (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2) / 2
		self.AA5 = np.array([ptAA5x, ptAA5y])

		ptAAS5x = ptAA5x + self.data_object.stiffener_length
		ptAAS5y = ptAA5y
		self.AAS5 = np.array([ptAAS5x, ptAAS5y])

		ptAA6x = ptAA1x
		ptAA6y = ptAA5y - self.data_object.web_thickness_tw2
		self.AA6 = np.array([ptAA6x, ptAA6y])

		ptAAS6x = ptAA6x + self.data_object.stiffener_length
		ptAAS6y = ptAA6y
		self.AAS6 = np.array([ptAAS6x, ptAAS6y])

		self.P = self.A2 + self.data_object.flange_weld_thickness * np.array([-1, 0])

		# ------------------------------------------  Weld triangle  UP-------------------------------------------
		self.BB1 = self.AA6
		self.BB2 = self.BB1 + self.data_object.web_weld_thickness * np.array([1, 0])
		self.BB3 = self.BB1 + self.data_object.web_weld_thickness * np.array([0, -1])

		# ------------------------------------------  Weld triangle  DOWN-------------------------------------------
		self.BB4 = self.AA5
		self.BB5 = self.BB4 + self.data_object.web_weld_thickness * np.array([1, 0])
		self.BB6 = self.BB4 + self.data_object.web_weld_thickness * np.array([0, 1])

	def call_ExtndBoth_top(self, filename):
		"""

		Args:
			filename: path of the images to be saved

		Returns:
			Saves the image in the folder

		"""
		dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-80 -700 1800 1800'))
		dwg.add(dwg.line(self.A5, self.AS8).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
		dwg.add(dwg.line(self.AS8, self.A8).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.A6, self.AS7).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
		dwg.add(dwg.line(self.AS7, self.A7).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.AS7, self.AS8).stroke('blue', width=2.5, linecap='square'))

		dwg.add(dwg.polyline(points=[self.A1, self.A2, self.A3, self.A4, self.A1], stroke='blue', fill='none', stroke_width=2.5))

		dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width='2.5'))
		dwg.add(dwg.polyline(points=[self.PP1, self.PP2, self.PP3, self.PP4, self.PP1], stroke='blue', fill='none', stroke_width=2.5))

		dwg.add(dwg.polyline(points=[self.AA1, self.AA2, self.AA3, self.AA4, self.AA1], stroke='blue', fill='none', stroke_width=2.5))

		dwg.add(dwg.line(self.AA5, self.AAS5).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.AAS5, self.AA8).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
		dwg.add(dwg.line(self.AA6, self.AAS6).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.AAS6, self.AA7).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
		dwg.add(dwg.line(self.AAS6, self.AAS5).stroke('blue', width=2.5, linecap='square'))

		dwg.add(dwg.polyline(points=[self.B1, self.B2, self.B3, self.B1], stroke='red', fill='red', stroke_width=2.5))
		dwg.add(dwg.polyline(points=[self.B4, self.B5, self.B6, self.B4], stroke='red', fill='red', stroke_width=2.5))
		dwg.add(dwg.polyline(points=[self.BB1, self.BB2, self.BB3, self.BB1], stroke='red', fill='red', stroke_width=2.5))
		dwg.add(dwg.polyline(points=[self.BB4, self.BB5, self.BB6, self.BB4], stroke='red', fill='red', stroke_width=2.5))

		pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
		pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))

		dwg.add(dwg.rect(insert=self.AS8, size=(self.data_object.stiffener_length, self.data_object.stiffener_weldsize),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		dwg.add(dwg.rect(insert=self.AS7 - self.data_object.stiffener_weldsize * np.array([0, 1]),
						 size=(self.data_object.stiffener_length, self.data_object.stiffener_weldsize),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		dwg.add(dwg.rect(insert=self.AA5, size=(self.data_object.stiffener_length, self.data_object.stiffener_weldsize),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		dwg.add(dwg.rect(insert=self.AA6 - self.data_object.stiffener_weldsize * np.array([0, 1]),
						 size=(self.data_object.stiffener_length, self.data_object.stiffener_weldsize),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))

		if self.data_object.weld == "Fillet Weld":
			pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse",
											   patternTransform="rotate(45 2 2)"))
			pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
			dwg.add(
				dwg.rect(insert=self.P, size=(self.data_object.flange_weld_thickness, self.data_object.beam_width_B1),
						 fill="url(#diagonalHatch)",
						 stroke='white', stroke_width=1.0))
			dwg.add(
				dwg.rect(insert=self.AA1, size=(self.data_object.flange_weld_thickness, self.data_object.beam_width_B2),
						 fill="url(#diagonalHatch)",
						 stroke='white', stroke_width=1.0))
		else:
			pass

		nofc = self.data_object.no_of_columns
		bolt_r = int(self.data_object.bolt_diameter) / 2

		# ------------------------------------------  Bolts Outside Top Flange -------------------------------------------
		pt_outside_top_column_list = []
		if nofc >= 1:
			for i in range(nofc):
				ptx = self.PP2 - self.data_object.edge_dist * np.array([0, -1]) - \
					  (self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p1) * np.array([1, 0]) + \
					  i * self.data_object.cross_centre_gauge_dist * np.array([0, 1])
				ptx1 = ptx - bolt_r * np.array([0, 1])
				rect_width = float(self.data_object.bolt_diameter)
				rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2)
				dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

				pt_Cx = ptx + 10 * np.array([1, 0])
				pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
				dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
				pt_outside_top_column_list.append(ptx)

				pt_Cx1 = ptx + 1 * np.array([-1, 0])
				pt_Dx1 = ptx + (rect_length - 14) * np.array([-1, 0])
				dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
				pt_outside_top_column_list.append(ptx)

		# ------------------------------------------  Faint line for bolts-------------------------------------------
		ptx1 = np.array(pt_outside_top_column_list[0])
		pty1 = ptx1 + (self.data_object.beam_length_L1 + 75) * np.array([1, 0])
		self.data_object.draw_faint_line(ptx1, pty1, dwg)

		ptx2 = np.array(pt_outside_top_column_list[1]) + self.data_object.cross_centre_gauge_dist * np.array([0, 1])
		pty2 = ptx2 + (self.data_object.beam_length_L1 + 75) * np.array([1, 0])
		self.data_object.draw_faint_line(ptx2, pty2, dwg)

		point1 = ptx2 + (self.data_object.cross_centre_gauge_dist) * np.array([0, -1])
		params = {"offset": (self.data_object.beam_length_L1 + 75), "textoffset": 10, "lineori": "right",
				  "endlinedim": 10, "arrowlen": 20}
		self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.cross_centre_gauge_dist), params)

		# ------------------------------------------  Primary Beam 1& 2 -------------------------------------------
		point = self.A2 - self.data_object.beam_length_L1 / 2 * np.array([1, 0])
		theta = 60
		offset = 50
		textdown = " "
		textup = "Beam " + str(self.data_object.beam_designation)
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		point = self.AA2 - self.data_object.beam_length_L2 / 2 * np.array([1, 0])
		theta = 60
		offset = 50
		textup = "Beam " + str(self.data_object.beam_designation)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------  End Plate 1 & 2 -------------------------------------------
		point = self.P1 + self.data_object.plate_thickness_p1 / 2 * np.array([1, 0])
		theta = 60
		offset = 150
		textdown = " "
		textup = "End Plate " + str(self.data_object.plate_length_L1) + "x" + str(self.data_object.plate_width_B1) + "x" + str(
			self.data_object.plate_thickness_p1)
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		point = self.PP1 + self.data_object.plate_thickness_p1 / 2 * np.array([1, 0])
		theta = 60
		offset = 150
		textup = "End Plate " + str(self.data_object.plate_length_L2) + "x" + str(self.data_object.plate_width_B2) + "x" + str(
			self.data_object.plate_thickness_p2)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------  Weld label --------------------------------------------------
		self.data_object.stiffener_weld = 1
		point = self.AAS6
		theta = 60
		offset = 50
		textup = "          z " + str(self.data_object.stiffener_weldsize)
		textdown = "          z " + str(self.data_object.stiffener_weldsize)
		element = "weld"
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
		self.data_object.stiffener_weld = 0

		if self.data_object.weld == "Fillet Weld":
			point = self.AA1
			theta = 60
			offset = 100
			textup = "          z " + str(self.data_object.flange_weld_thickness)
			textdown = "          z " + str(self.data_object.flange_weld_thickness)
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
		else:
			point = self.AA1
			theta = 60
			offset = 100
			textup = "               "
			textdown = "               "
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		# ------------------------------------------ Stiffener -------------------------------------------------
		point = self.AAS5
		theta = 60
		offset = 50
		textup = "Stiffener " + str(self.data_object.stiffener_height) + "x" + str(
			self.data_object.stiffener_length) + "x" + str(
			self.data_object.stiffener_thickness)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "SE", offset, textup, textdown, element)

	# ------------------------------------------  Sectional arrow -------------------------------------------
		pt_a1 = self.A4 - (200) * np.array([0, -1])
		pt_b1 = pt_a1 + (50 * np.array([0, -1]))
		txt_1 = pt_b1 + (10 * np.array([-1, 0])) + (40 * np.array([0, -1]))
		text = "C"
		self.data_object.draw_cross_section(dwg, pt_a1, pt_b1, txt_1, text)

		pt_a2 = pt_a1 + (2 * self.data_object.beam_length_L1 + 2 * self.data_object.plate_thickness_p1) * np.array([1, 0])
		pt_b2 = pt_a2 + (50 * np.array([0, -1]))
		txt_2 = pt_b2 + (10 * np.array([-1, 0])) + (40 * np.array([0, -1]))
		self.data_object.draw_cross_section(dwg, pt_a2, pt_b2, txt_2, text)

		dwg.add(dwg.line(pt_a1, pt_a2).stroke('black', width=1.5, linecap='square'))

		pt_a3 = self.AA2 + (200) * np.array([1, 0])
		pt_b3 = pt_a3 + (50 * np.array([-1, 0]))
		txt_3 = pt_b3 + (10 * np.array([0, 1])) + (60 * np.array([-1, 0]))
		text = "B"
		self.data_object.draw_cross_section(dwg, pt_a3, pt_b3, txt_3, text)

		pt_a4 = pt_a3 + (self.data_object.beam_width_B1 * np.array([0, 1]))
		pt_b4 = pt_a4 + (50 * np.array([-1, 0]))
		txt_4 = pt_b4 + (10 * np.array([0, 1])) + (60 * np.array([-1, 0]))
		self.data_object.draw_cross_section(dwg, pt_a4, pt_b4, txt_4, text)

		dwg.add(dwg.line(pt_a3, pt_a4).stroke('black', width=1.5,linecap='square'))

		# ------------------------------------------  View details -------------------------------------------
		ptx = self.P4 - 50 * np.array([1, 0]) + 300 * np.array([0, 1])
		dwg.add(dwg.text('Top view (Sec A-A) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
		ptx1 = ptx + 40 * np.array([0, 1])
		dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

		dwg.save()


class ExtendedEnd2DSide(object):
	"""
	Contains functions for generating the side view of the Extended bothway endplate connection.

	"""

	def __init__(self, extnd_common_object):
		self.data_object = extnd_common_object

		# =========================  End Plate 1  =========================
		ptP1x = 0
		ptP1y = 0  # (self.data_object.plate_length_L1 + self.data_object.beam_depth_D1)/2
		self.P1 = np.array([ptP1x, ptP1y])

		ptP2x = self.data_object.plate_width_B1
		ptP2y = 0
		self.P2 = np.array([ptP2x, ptP2y])

		ptP3x = self.data_object.plate_width_B1
		ptP3y = self.data_object.plate_length_L1
		self.P3 = np.array([ptP3x, ptP3y])

		ptP4x = 0
		ptP4y = self.data_object.plate_length_L1
		self.P4 = np.array([ptP4x, ptP4y])

		ptP5x = ptP1x + self.data_object.plate_width_B1 / 2 - self.data_object.stiffener_thickness / 2
		ptP5y = ptP1y
		self.P5 = np.array([ptP5x, ptP5y])

		ptP6x = ptP1x + self.data_object.plate_width_B1 / 2 + self.data_object.stiffener_thickness / 2
		ptP6y = ptP1y
		self.P6 = np.array([ptP6x, ptP6y])

		ptP7x = ptP4x + self.data_object.plate_width_B1 / 2 - self.data_object.stiffener_thickness / 2
		ptP7y = ptP4y
		self.P7 = np.array([ptP7x, ptP7y])

		ptP8x = ptP4x + self.data_object.plate_width_B1 / 2 + self.data_object.stiffener_thickness / 2
		ptP8y = ptP4y
		self.P8 = np.array([ptP8x, ptP8y])

		# =========================  Primary Beam 1  =========================
		ptA1x = (self.data_object.plate_width_B1 - self.data_object.beam_width_B1) / 2
		ptA1y = (self.data_object.plate_length_L1 - self.data_object.beam_depth_D1) / 2
		self.A1 = np.array([ptA1x, ptA1y])

		ptA2x = ptA1x + self.data_object.beam_width_B1
		ptA2y = ptA1y
		self.A2 = np.array([ptA2x, ptA2y])

		ptA3x = ptA2x
		ptA3y = ptA2y + self.data_object.flange_thickness_T1
		self.A3 = np.array([ptA3x, ptA3y])

		ptA12x = ptA1x
		ptA12y = ptA1y + self.data_object.flange_thickness_T1
		self.A12 = np.array([ptA12x, ptA12y])

		ptA4x = ptA12x + (self.data_object.beam_width_B1 / 2 + self.data_object.web_thickness_tw1 / 2)
		ptA4y = ptA3y
		self.A4 = np.array([ptA4x, ptA4y])

		ptAS4x = ptA1x + self.data_object.beam_width_B2 / 2 - self.data_object.stiffener_thickness / 2
		ptAS4y = ptA1y
		self.AS4 = np.array([ptAS4x, ptAS4y])

		ptA8x = ptA1x
		ptA8y = (self.data_object.plate_length_L1 + self.data_object.beam_depth_D1) / 2
		self.A8 = np.array([ptA8x, ptA8y])

		ptA9x = ptA1x
		ptA9y = ptA8y - self.data_object.flange_thickness_T1
		self.A9 = np.array([ptA9x, ptA9y])

		ptA7x = ptA8x + self.data_object.beam_width_B1
		ptA7y = ptA8y
		self.A7 = np.array([ptA7x, ptA7y])

		ptA6x = ptA7x
		ptA6y = ptA7y - self.data_object.flange_thickness_T1
		self.A6 = np.array([ptA6x, ptA6y])

		ptA5x = ptA4x
		ptA5y = ptA6y
		self.A5 = np.array([ptA5x, ptA5y])

		ptAS5x = ptA8x + self.data_object.beam_width_B2 / 2 - self.data_object.stiffener_thickness / 2
		ptAS5y = ptA8y
		self.AS5 = np.array([ptAS5x, ptAS5y])

		ptA11x = ptA12x + (self.data_object.beam_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2)
		ptA11y = ptA12y
		self.A11 = np.array([ptA11x, ptA11y])

		ptAS11x = ptA1x + self.data_object.beam_width_B2 / 2 + self.data_object.stiffener_thickness / 2
		ptAS11y = ptA1y
		self.AS11 = np.array([ptAS11x, ptAS11y])

		ptA10x = ptA11x
		ptA10y = ptA9y
		self.A10 = np.array([ptA10x, ptA10y])

		self.P = self.A11 - self.data_object.web_weld_thickness * np.array([1, 0])

		ptAS10x = ptA8x + self.data_object.beam_width_B2 / 2 + self.data_object.stiffener_thickness / 2
		ptAS10y = ptA8y
		self.AS10 = np.array([ptAS10x, ptAS10y])

	def call_ExtndBoth_side(self, filename):
		"""

		Args:
			filename: path of the images to be saved

		Returns:
			Saves the image in the folder

		"""
		dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-450 -500 1200 1400'))
		dwg.add(dwg.polyline(
			points=[self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7, self.A8, self.A9, self.A10, self.A11, self.A12, self.A1],
			stroke='blue', fill='#E0E0E0', stroke_width=2.5))
		dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width='2.5'))

		dwg.add(dwg.line(self.P6, self.AS11).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.P5, self.AS4).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.P8, self.AS10).stroke('blue', width=2.5, linecap='square'))
		dwg.add(dwg.line(self.P7, self.AS5).stroke('blue', width=2.5, linecap='square'))

		pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(2, 6), patternUnits="userSpaceOnUse",
										   patternTransform="rotate(45 1 1)"))
		pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
		dwg.add(dwg.rect(insert=(self.P5 + self.data_object.stiffener_weldsize * np.array([-1, 0])),
						 size=(self.data_object.stiffener_weldsize, (
								 self.data_object.plate_length_L1/2 - self.data_object.beam_depth_D2/2)),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		dwg.add(dwg.rect(insert=self.P6, size=(self.data_object.stiffener_weldsize, (
					self.data_object.plate_length_L1/2 - self.data_object.beam_depth_D2/2)),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		dwg.add(dwg.rect(insert=self.AS10,
						 size=(self.data_object.stiffener_weldsize, (
								 self.data_object.plate_length_L1/2 - self.data_object.beam_depth_D2/2)),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
		dwg.add(dwg.rect(insert=(self.AS5 + self.data_object.stiffener_weldsize * np.array([-1, 0])), size=(self.data_object.stiffener_weldsize, (
				self.data_object.plate_length_L1/2 - self.data_object.beam_depth_D2/2)),
						 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))

		if self.data_object.weld == "Fillet Weld":
			pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(2, 6), patternUnits="userSpaceOnUse",
											   patternTransform="rotate(45 1 1)"))
			pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))

			dwg.add(dwg.rect(insert=self.P, size=(self.data_object.web_weld_thickness, (
					self.data_object.beam_depth_D1 - (2 * self.data_object.flange_thickness_T1))),
							 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
			dwg.add(dwg.rect(insert=self.A4, size=(self.data_object.web_weld_thickness, (
					self.data_object.beam_depth_D2 - (2 * self.data_object.flange_thickness_T2))),
							 fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
			pattern1 = dwg.defs.add(dwg.pattern(id="diagonalHatch1", size=(6, 6), patternUnits="userSpaceOnUse",
												patternTransform="rotate(45 2 2)", ))
			pattern1.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
			dwg.add(dwg.rect(insert=(self.A1 - self.data_object.flange_weld_thickness * np.array([0, 1])),
							 size=(self.data_object.beam_width_B1, self.data_object.flange_weld_thickness),
							 fill="url(#diagonalHatch1)", stroke='white',
							 stroke_width=1.0))
			dwg.add(dwg.rect(insert=self.A4,
							 size=((self.data_object.beam_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2),
								   self.data_object.flange_weld_thickness),
							 fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
			dwg.add(dwg.rect(insert=(self.A9 - self.data_object.flange_weld_thickness * np.array([0, 1])),
							 size=((self.data_object.beam_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2),
								   self.data_object.flange_weld_thickness),
							 fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
			dwg.add(dwg.rect(insert=(self.A5 - self.data_object.flange_weld_thickness * np.array([0, 1])),
							 size=((self.data_object.beam_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2),
								   self.data_object.flange_weld_thickness),
							 fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
			dwg.add(dwg.rect(insert=self.A12,
							 size=((self.data_object.beam_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2),
								   self.data_object.flange_weld_thickness),
							 fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
			dwg.add(dwg.rect(insert=self.A8,
							 size=(self.data_object.beam_width_B1, self.data_object.flange_weld_thickness),
							 fill="url(#diagonalHatch1)", stroke='white',
							 stroke_width=1.0))

		else:
			pass
		# dwg.add(dwg.rect(insert=(self.A1-self.data_object.flange_weld_thickness * np.array([1, 0])), size=(self.data_object.beam_width_B1, self.data_object.flange_weld_thickness), fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))

		# TODO hatching lines flange welding for sides of flange
		# dwg.add(dwg.rect(insert=(self.A1-self.data_object.flange_weld_thickness * np.array([1, 0])), size=(self.data_object.flange_weld_thickness, self.data_object.flange_thickness_T1), fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
		# dwg.add(dwg.rect(insert=self.A2, size=(self.data_object.flange_weld_thickness, self.data_object.flange_thickness_T1), fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))

		nofc = self.data_object.no_of_columns
		botfr = self.data_object.bolts_outside_top_flange_row
		bitfr = self.data_object.bolts_inside_top_flange_row
		bolt_r = int(self.data_object.bolt_diameter) / 2

		# ------------------------------------------  Bolts Outside Top Flange -------------------------------------------
		pt_outside_top_column_list = []

		for i in range(1, (botfr + 1)):
			col_outside_list_top = []
			for j in range(1, (nofc + 1)):
				if self.data_object.no_of_bolts == 8:
					pt = self.P1 + self.data_object.end_dist * np.array([0, 1]) + self.data_object.edge_dist * np.array(
						[1, 0]) + (i - 1) * self.data_object.pitch * np.array([0, 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 12:
					pt = self.P1 + self.data_object.end_dist * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (
								 i - 1) * self.data_object.pitch23 * np.array([0, 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 16:
					pt = self.P1 + self.data_object.end_dist * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (
								 i - 1) * self.data_object.pitch23 * np.array([0, 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 20:
					pt = self.P1 + self.data_object.end_dist * np.array(
						[0, 1]) + \
						 self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch12 * np.array(
						[0, 1]) + (j - 1) * \
						 self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='black', fill='none', stroke_width=1.5))
				pt_C = pt - (bolt_r + 4) * np.array([1, 0])
				pt_D = pt + (bolt_r + 4) * np.array([1, 0])
				dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

				pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
				pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
				dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

				col_outside_list_top.append(pt)
			pt_outside_top_column_list.append(col_outside_list_top)

		# ------------------------------------------  Bolts Inside Top Flange -------------------------------------------
		pt_inside_top_column_list = []
		for i in range(1, (bitfr + 1)):
			col_inside_list_top = []
			for j in range(1, (nofc + 1)):
				if self.data_object.no_of_bolts == 8:
					pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T2 + self.data_object.Lv + self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (
									 i - 1) * self.data_object.pitch * np.array(
						[0, 1]) + (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 12:
					pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T1 + self.data_object.Lv + self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch23 * np.array([0, 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 16:
					pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T1 + self.data_object.Lv + self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + ( i - 1) * self.data_object.pitch23 * np.array([0, 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 20:
					pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T1 + self.data_object.Lv + self.data_object.flange_thickness_T2 ) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch34 * np.array([0, 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='black', fill='none', stroke_width=1.5))
				pt_C = pt - (bolt_r + 4) * np.array([1, 0])
				pt_D = pt + (bolt_r + 4) * np.array([1, 0])
				dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

				pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
				pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
				dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

				col_inside_list_top.append(pt)
			pt_inside_top_column_list.append(col_inside_list_top)
		# ================================================================================================

		nofc = self.data_object.no_of_columns
		bobfr = self.data_object.bolts_outside_bottom_flange_row
		bibfr = self.data_object.bolts_inside_bottom_flange_row
		# ------------------------------------------  Bolts Outside Bottom Flange -------------------------------------------

		pt_outside_bottom_column_list = []
		for i in range(1, (bobfr + 1)):
			col_outside_list_bottom = []
			for j in range(1, (nofc + 1)):
				if self.data_object.no_of_bolts == 8:
					pt = self.P4 + self.data_object.end_dist * np.array(
						[0, -1]) + self.data_object.edge_dist * np.array([1, 0]) + (
								 i - 1) * self.data_object.pitch * np.array([0, - 1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 12:
					pt = self.P4 + self.data_object.end_dist * np.array(
						[0, -1]) + self.data_object.edge_dist * np.array([1, 0]) + (
								 i - 1) * self.data_object.pitch23 * np.array([0, -1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 16:
					pt = self.P4 + self.data_object.end_dist * np.array(
						[0, -1]) + self.data_object.edge_dist * np.array([1, 0]) + (
								 i - 1) * self.data_object.pitch23 * np.array([0, -1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 20:
					pt = self.P4 + self.data_object.end_dist * \
						 np.array([0, -1]) + self.data_object.edge_dist * np.array([1, 0]) + (
								 i - 1) * self.data_object.pitch12 * np.array([0, -1]) + \
						 (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='black', fill='none', stroke_width=1.5))
				pt_C = pt - (bolt_r + 4) * np.array([1, 0])
				pt_D = pt + (bolt_r + 4) * np.array([1, 0])
				dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

				pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
				pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
				dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

				col_outside_list_bottom.append(pt)
			pt_outside_bottom_column_list.append(col_outside_list_bottom)

		# ------------------------------------------  Bolts Inside Bottom Flange -------------------------------------------
		pt_inside_bottom_column_list = []
		for i in range(1, (bibfr + 1)):

			col_inside_list_bottom = []
			for j in range(1, (nofc + 1)):
				if self.data_object.no_of_bolts == 8:
					pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D1) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv - self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch * np.array([0, -1]) + (
									 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 12:
					pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D1) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv - self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch45 * np.array([0, -1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 16:
					pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D1) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv - self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch56* np.array([0, -1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
				elif self.data_object.no_of_bolts == 20:
					pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D1) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv - self.data_object.flange_thickness_T2) * np.array(
						[0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch56 * np.array([0, -1]) + (
								 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])

				dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
				pt_C = pt - (bolt_r + 4) * np.array([1, 0])
				pt_D = pt + (bolt_r + 4) * np.array([1, 0])
				dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

				pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
				pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
				dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

				col_inside_list_bottom.append(pt)
			pt_inside_bottom_column_list.append(col_inside_list_bottom)

			# ------------------------------------------  Faint line for top bolts-------------------------------------------
		ptx1 = self.P1
		pty1 = ptx1 + self.data_object.beam_width_B2 * np.array([0, -1])
		self.data_object.draw_faint_line(ptx1, pty1, dwg)

		ptx2 = np.array(pt_outside_top_column_list[0][0])
		pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
		self.data_object.draw_faint_line(ptx2, pty2, dwg)

		point1 = ptx2 + (self.data_object.edge_dist) * np.array([-1, 0])
		params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
				  "endlinedim": 10, "arrowlen": 20}
		self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.edge_dist), params)
		# -------------------------------------------------------------------------------------------
		ptxx1 = self.P2
		ptyy1 = ptxx1 + self.data_object.beam_width_B2 * np.array([0, -1])
		self.data_object.draw_faint_line(ptxx1, ptyy1, dwg)

		ptxx2 = np.array(pt_outside_top_column_list[0][1])
		ptyy2 = ptxx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
		self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

		point2 = ptxx2 + (self.data_object.edge_dist) * np.array([1, 0])
		params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
				  "endlinedim": 10, "arrowlen": 20}
		self.data_object.draw_dimension_outer_arrow(dwg, ptxx2, point2, str(self.data_object.edge_dist), params)

		if self.data_object.no_of_bolts == 20:
			ptx3 = np.array(pt_outside_top_column_list[1][1])
			point2 = ptx3 + (self.data_object.Lv + self.data_object.flange_weld_thickness)* np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx3, point2, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)
		else:
			point2 = ptxx2 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptxx2, point2, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

		params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
				  "endlinedim": 10, "arrowlen": 20}
		self.data_object.draw_dimension_outer_arrow(dwg, ptx2, ptxx2, str(self.data_object.cross_centre_gauge_dist),
													params)

		ptx3 = np.array(pt_outside_top_column_list[0][1])

		point2 = ptx3 + self.data_object.end_dist * np.array([0, -1])
		params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
				  "endlinedim": 10, "arrowlen": 20}
		self.data_object.draw_dimension_outer_arrow(dwg, point2, ptx3, str(self.data_object.end_dist), params)

		# ------------------------------------------  Faint line for inside top flange bolts-------------------------------------------
		if self.data_object.no_of_bolts == 8:
			ptx1 = np.array(pt_inside_top_column_list[0][1])
			pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx1, pty1, dwg)

			ptx2 = np.array(pt_inside_bottom_column_list[0][1])
			pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx2, pty2, dwg)

			point1 = np.array(pt_inside_top_column_list[0][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch), params)

			point2 = ptx1 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10,
					  "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx1, point2, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

			point3 = ptx2 + (self.data_object.Lv  + self.data_object.flange_weld_thickness) * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point3, ptx2, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

		elif self.data_object.no_of_bolts == 12:
			ptx2 = np.array(pt_inside_top_column_list[1][1])
			pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx2, pty2, dwg)

			ptx3 = np.array(pt_inside_top_column_list[0][1])
			pty3 = ptx3 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx3, pty3, dwg)

			point3 = ptx3 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx3, point3, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

			point2 = np.array(pt_inside_bottom_column_list[1][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point2, str(self.data_object.pitch34), params)

			point1 = ptx2 + self.data_object.pitch23 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch23), params)

		elif self.data_object.no_of_bolts == 16:
			ptx2 = np.array(pt_inside_top_column_list[1][1])
			pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx2, pty2, dwg)

			ptx3 = np.array(pt_inside_top_column_list[0][1])
			pty3 = ptx3 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx3, pty3, dwg)

			point1 = np.array(pt_inside_top_column_list[1][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point1, ptx3, str(self.data_object.pitch23), params)

			point3 = ptx3 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10,
					  "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point3, ptx3, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

			ptx4 = np.array(pt_inside_top_column_list[2][1])
			pty4 = ptx4 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx4, pty4, dwg)

			point2 = ptx4 + self.data_object.pitch34 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10,
					  "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx4, point2, str(self.data_object.pitch34), params)

			point2 = np.array(pt_inside_bottom_column_list[2][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10,
					  "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx4, point2, str(self.data_object.pitch45), params)

		elif self.data_object.no_of_bolts == 20:
			ptx1 = np.array(pt_outside_top_column_list[0][1])
			pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx1, pty1, dwg)

			ptx2 = np.array(pt_outside_top_column_list[1][1])
			pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx2, pty2, dwg)
			point1 = ptx2 + self.data_object.pitch12 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch12), params)

			ptx3 = np.array(pt_inside_top_column_list[1][1])
			pty3 = ptx3 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx3, pty3, dwg)

			ptx4 = np.array(pt_inside_top_column_list[0][1])
			pty4 = ptx4 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx4, pty4, dwg)
			point2 = ptx4 + self.data_object.pitch34 * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx4, point2, str(self.data_object.pitch34), params)

			point6 = ptx4 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10,
					  "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx4, point6, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

			ptx5 = np.array(pt_inside_top_column_list[2][1])
			pty5 = ptx5 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx5, pty5, dwg)
			point3 = ptx5 + self.data_object.pitch45 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx5, point3, str(self.data_object.pitch45), params)

			point4 = np.array(pt_inside_bottom_column_list[2][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx5, point4, str(self.data_object.pitch56), params)

		# ------------------------------------------  Faint line for inside bottom flange bolts-------------------------------------------
		if self.data_object.no_of_bolts == 8:
			pass

		elif self.data_object.no_of_bolts == 12:
			ptx1 = np.array(pt_inside_bottom_column_list[1][1])
			pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx1, pty1, dwg)

			ptx2 = np.array(pt_inside_bottom_column_list[0][1])
			pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx2, pty2, dwg)

			point1 = np.array(pt_inside_bottom_column_list[1][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch45), params)

			point2 = ptx2 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point2, ptx2, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

		elif self.data_object.no_of_bolts == 16:
			ptx5 = np.array(pt_inside_bottom_column_list[2][1])
			pty5 = ptx5 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx5, pty5, dwg)

			point2 = ptx5 + self.data_object.pitch56 * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx5, point2, str(self.data_object.pitch56), params)

			ptx6 = np.array(pt_inside_bottom_column_list[1][1])
			pty6 = ptx6 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx6, pty6, dwg)

			ptx7 = np.array(pt_inside_bottom_column_list[0][1])
			pty7 = ptx7 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx7, pty7, dwg)

			point1 = ptx7 + self.data_object.pitch67 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx7, point1, str(self.data_object.pitch67), params)

			point3 = ptx7 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point3, ptx7, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

		elif self.data_object.no_of_bolts == 20:
			ptx6 = np.array(pt_inside_bottom_column_list[2][1])
			pty6 = ptx6 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx6, pty6, dwg)

			ptx7 = np.array(pt_inside_bottom_column_list[1][1])
			pty7 = ptx7 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx7, pty7, dwg)
			point3 = np.array(pt_inside_bottom_column_list[2][1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10,
					  "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx7, point3, str(self.data_object.pitch67), params)

			ptx8 = np.array(pt_inside_bottom_column_list[0][1])
			pty8 = ptx8 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx8, pty8, dwg)
			point1 = ptx8 + self.data_object.pitch78 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx8, point1, str(self.data_object.pitch78), params)

			ptx9 = np.array(pt_outside_bottom_column_list[1][1])
			pty9 = ptx9 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx9, pty9, dwg)

			ptx10 = np.array(pt_outside_bottom_column_list[0][1])
			pty10 = ptx10 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
			self.data_object.draw_faint_line(ptx10, pty10, dwg)
			point2 = ptx10 + self.data_object.pitch910 * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, ptx10, point2, str(self.data_object.pitch910), params)

			point3 = ptx8 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, 1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point3, ptx8, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

		# ------------------------------------------  Faint line for bottom bolts showing end distance-------------------------------------------
		ptx1 = self.P3
		pty1 = ptx1 + self.data_object.beam_width_B2 * np.array([1, 0])
		self.data_object.draw_faint_line(ptx1, pty1, dwg)

		ptx2 = np.array(pt_outside_bottom_column_list[0][1])
		pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
		self.data_object.draw_faint_line(ptx2, pty2, dwg)

		point1 = ptx2 + self.data_object.end_dist * np.array([0, 1])
		params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
				  "endlinedim": 10, "arrowlen": 20}
		self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.end_dist), params)

		if self.data_object.no_of_bolts == 20:
			ptx3 = np.array(pt_outside_bottom_column_list[1][1])
			point2 = ptx3 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point2, ptx3, str(self.data_object.Lv +self.data_object.flange_weld_thickness), params)
		else:
			point2 = ptx2 + (self.data_object.Lv + self.data_object.flange_weld_thickness) * np.array([0, -1])
			params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
					  "endlinedim": 10, "arrowlen": 20}
			self.data_object.draw_dimension_outer_arrow(dwg, point2, ptx2, str(self.data_object.Lv + self.data_object.flange_weld_thickness), params)

		# ------------------------------------------  End Plate 1 -------------------------------------------
		point = self.P1 + 10 * np.array([1, 0])
		theta = 60
		offset = 50
		textup = "End plate " + str(self.data_object.plate_length_L1) + "x"+ str(self.data_object.plate_width_B1)+ "x" + str(
			self.data_object.plate_thickness_p1)
		textdown = " "
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		# ------------------------------------------  Primary Beam 1 -------------------------------------------
		point = self.A1 +5* np.array([0, 1])
		theta = 1
		offset = 1
		textdown = " "
		textup = "Beam " + str(self.data_object.beam_designation)
		element = " "
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		# ---------------------------------------------  Web Welding ----------------------------------------------
		if self.data_object.weld == "Fillet Weld":
			point = self.A4 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
			theta = 60
			offset = 50
			textup = "                    z " + str(self.data_object.web_weld_thickness)
			textdown = "                    z " + str(self.data_object.web_weld_thickness)
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)
		else:
			point = self.A4 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
			theta = 60
			offset = 50
			textup = "               "
			textdown = "               "
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)
		# ---------------------------------------------  Stiffener Welding ----------------------------------------------
		self.data_object.stiffener_weld = 1
		point = self.P6
		theta = 60
		offset = 50
		textup = "           z " + str(self.data_object.stiffener_weldsize)
		textdown = "           z " + str(self.data_object.stiffener_weldsize)
		element = "weld"
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

		point = self.P7
		theta = 60
		offset = 50
		textup = "           z " + str(self.data_object.stiffener_weldsize)
		textdown = "           z " + str(self.data_object.stiffener_weldsize)
		element = "weld"
		self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)
		self.data_object.stiffener_weld = 0

		# ---------------------------------------------  Flange Welding -------------------------------------------
		if self.data_object.weld == "Fillet Weld":
			point = self.A1 + 20 * np.array([1, 0])
			theta = 60
			offset = 50
			textup = " z " + str(self.data_object.flange_weld_thickness) + "               "
			textdown = " z " + str(self.data_object.flange_weld_thickness) + "              "
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)
		else:
			point = self.A1 + 20 * np.array([1, 0])
			theta = 60
			offset = 50
			textup = "               "
			textdown = "               "
			element = "weld"
			self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

		# ------------------------------------------  View details-------------------------------------------
		ptx = self.P4 * np.array([0, 1]) + 125 * np.array([0, 1])
		dwg.add(dwg.text('Side view (Sec B-B) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
		ptx1 = ptx + 40 * np.array([0, 1])
		dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

		dwg.save()
