'''
Created on 22-May-2019

@author: darshan
'''
from numpy import math
from Connections.connection_calculations import ConnectionCalculations
import svgwrite
import cairosvg
import numpy as np
import os


class FlushEndPlate(object):

    def __init__(self, input_dict, output_dict, column_data, beam_data, folder):
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

        self.column_length_L1 = 1000
        self.beam_length_L2 = 500

        self.column_depth_D1 = int(column_data["D"])
        self.beam_depth_D2 = int(beam_data["D"])

        self.beam_designation = beam_data['Designation']
        self.column_designation = column_data['Designation']

        self.column_width_B1 = int(column_data["B"])
        self.beam_width_B2 = int(beam_data["B"])

        self.plate_thickness_p1 = int(output_dict['Plate']['Thickness'])
        self.plate_thickness_p2 = int(output_dict['ContPlateComp']['Thickness'])
        self.weld_plate_thickness_p2 = int(output_dict['ContPlateComp']['Weld'])


        self.plate_width_B2 = int(output_dict['ContPlateComp']['Width'])
        self.plate_length_L2 = int(output_dict['ContPlateComp']['Length'])


        self.plate_width_B1 = int(output_dict['Plate']['Width'])

        self.plate_length_L1 = int(output_dict['Plate']['Height'])

        self.flange_thickness_T1 = (column_data["T"])
        self.flange_thickness_T2 = (beam_data["T"])

        self.web_thickness_tw1 = int(column_data["tw"])
        self.web_thickness_tw2 = int(beam_data["tw"])

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
        self.weld = input_dict["Weld"]["Method"]
        self.stiffener_weld = 0

        self.no_of_columns = 2
        self.no_of_bolts = output_dict['Bolt']['NumberOfBolts']
        if self.no_of_bolts == 4:
            self.pitch12 = float(output_dict['Bolt']['Pitch12'])
            # self.bolts_outside_top_flange_row = 0
            self.bolts_inside_top_flange_row = 1
            self.bolts_inside_bottom_flange_row = 1
            # self.bolts_outside_bottom_flange_row = 0
        elif self.no_of_bolts == 8:
            self.pitch12 = float(output_dict['Bolt']['Pitch12'])
            self.pitch23 = float(output_dict['Bolt']['Pitch23'])
            self.pitch34 = float(output_dict['Bolt']['Pitch34'])
            # self.bolts_outside_top_flange_row = 0
            self.bolts_inside_top_flange_row = 2
            self.bolts_inside_bottom_flange_row = 2
            # self.bolts_outside_bottom_flange_row = 0
        elif self.no_of_bolts == 12:
            self.pitch12 = float(output_dict['Bolt']['Pitch12'])
            self.pitch23 = float(output_dict['Bolt']['Pitch23'])
            self.pitch34 = float(output_dict['Bolt']['Pitch34'])
            self.pitch45 = float(output_dict['Bolt']['Pitch45'])
            self.pitch56 = float(output_dict['Bolt']['Pitch56'])
            # self.bolts_outside_top_flange_row = 0
            self.bolts_inside_top_flange_row = 3
            self.bolts_inside_bottom_flange_row = 3
            # self.bolts_outside_bottom_flange_row = 0


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
        flush_2d_front = FlushEnd2DFront(self)
        flush_2d_top = FlushEnd2DTop(self)
        flush_2d_side = FlushEnd2DSide(self)
        if view == "Front":
            flush_2d_front.call_flush_front(filename)
        elif view == "Top":
            flush_2d_top.call_flush_top(filename)
        elif view == "Side":
            flush_2d_side.call_flush_side(filename)
        else:
            filename = os.path.join(str(self.folder), 'images_html', 'extendFront.svg')
            flush_2d_front.call_flush_front(filename)
            cairosvg.svg2png(file_obj=filename,
                             write_to=os.path.join(str(self.folder), "images_html", "extendFront.png"))

            filename = os.path.join(str(self.folder), 'images_html', 'extendTop.svg')
            flush_2d_top.call_flush_top(filename)
            cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "extendTop.png"))

            filename = os.path.join(str(self.folder), 'images_html', 'extendSide.svg')
            flush_2d_side.call_flush_side(filename)
            cairosvg.svg2png(file_obj=filename,
                             write_to=os.path.join(str(self.folder), "images_html", "extendSide.png"))


class FlushEnd2DFront(object):
    """
	Contains functions for generating the front view of the Extended bothway endplate connection.
	"""

    def __init__(self, extnd_common_object):

        self.data_object = extnd_common_object

        # --------------------------------------------------------------------------
        #                               FRONT VIEW
        # --------------------------------------------------------------------------
        # ================ Column 1 ================

        # darshan

        """	
		defining co-ordinates of Beam B1 in front view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptA1x = 0
        ptA1y = 0
        self.A1 = np.array([ptA1x, ptA1y])

        ptA2x = ptA1x + self.data_object.column_depth_D1
        ptA2y = ptA1y
        self.A2 = np.array([ptA2x, ptA2y])

        ptA3x = ptA2x
        ptA3y = ptA2y + self.data_object.column_length_L1
        self.A3 = np.array([ptA3x, ptA3y])

        ptA4x = ptA1x
        ptA4y = ptA1y + self.data_object.column_length_L1
        self.A4 = np.array([ptA4x, ptA4y])

        ptA5x = ptA1x + self.data_object.flange_thickness_T1
        ptA5y = ptA1y
        self.A5 = np.array([ptA5x, ptA5y])

        ptA6x = ptA2x - self.data_object.flange_thickness_T1
        ptA6y = ptA2y
        self.A6 = np.array([ptA6x, ptA6y])

        ptA7x = ptA3x - self.data_object.flange_thickness_T1
        ptA7y = ptA3y
        self.A7 = np.array([ptA7x, ptA7y])

        ptA8x = ptA4x + self.data_object.flange_thickness_T1
        ptA8y = ptA4y
        self.A8 = np.array([ptA8x, ptA8y])

        # ================ Connecting Plate ==================

        # darshan

        """	
		defining co-ordinates of Connecting plate in front view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptP1x = ptA1x + self.data_object.column_depth_D1
        ptP1y = ptA1y + self.data_object.column_length_L1 / 2 - self.data_object.plate_length_L1 /2
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = ptP1x + self.data_object.plate_thickness_p1
        ptP2y = ptP1y
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = ptP2x
        ptP3y = ptP2y + self.data_object.plate_length_L1
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP1x
        ptP4y = ptP3y
        self.P4 = np.array([ptP4x, ptP4y])

        # ================ Beam ==================

        # darshan

        """	
		defining co-ordinates of Beam B2 in front view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptAA1x = ptP2x
        ptAA1y = ptP2y + self.data_object.plate_length_L1/2 - self.data_object.beam_depth_D2/2
        self.AA1 = np.array([ptAA1x, ptAA1y])

        ptAA2x = ptAA1x + self.data_object.beam_length_L2
        ptAA2y = ptAA1y
        self.AA2 = np.array([ptAA2x, ptAA2y])

        ptAA3x = ptAA2x
        ptAA3y = ptAA2y + self.data_object.beam_depth_D2
        self.AA3 = np.array([ptAA3x, ptAA3y])

        ptAA4x = ptAA3x - self.data_object.beam_length_L2
        ptAA4y = ptAA3y
        self.AA4 = np.array([ptAA4x, ptAA4y])

        ptAA5x = ptAA1x
        ptAA5y = ptAA1y + self.data_object.flange_thickness_T2
        self.AA5 = np.array([ptAA5x, ptAA5y])

        ptAA6x = ptAA2x
        ptAA6y = ptAA2y + self.data_object.flange_thickness_T2
        self.AA6 = np.array([ptAA6x, ptAA6y])

        ptAA7x = ptAA3x
        ptAA7y = ptAA3y - self.data_object.flange_thickness_T2
        self.AA7 = np.array([ptAA7x, ptAA7y])

        ptAA8x = ptAA4x
        ptAA8y = ptAA4y - self.data_object.flange_thickness_T2
        self.AA8 = np.array([ptAA8x, ptAA8y])

        # ================ Stiffeners ==================

        # darshan

        """	
        defining co-ordinates of Beam B2 in front view
        right of origin is considered as +ve X axis
        downward to the origin is considered as +ve Y axis
        """

        ptS1x = ptAA1x - self.data_object.plate_thickness_p1 - self.data_object.column_depth_D1 + self.data_object.flange_thickness_T1
        ptS1y = ptAA1y
        self.S1 = np.array([ptS1x, ptS1y])

        ptS2x = ptAA1x - self.data_object.plate_thickness_p1 - self.data_object.flange_thickness_T1
        ptS2y = ptAA1y
        self.S2 = np.array([ptS2x, ptS2y])

        ptS3x = ptAA5x - self.data_object.plate_thickness_p1 - self.data_object.flange_thickness_T1
        ptS3y = ptAA5y
        self.S3 = np.array([ptS3x, ptS3y])

        ptS4x = ptAA5x - self.data_object.plate_thickness_p1 - self.data_object.column_depth_D1 + self.data_object.flange_thickness_T1
        ptS4y = ptAA5y
        self.S4 = np.array([ptS4x, ptS4y])

        ptS5x = ptAA8x - self.data_object.plate_thickness_p1 - self.data_object.column_depth_D1 + self.data_object.flange_thickness_T1
        ptS5y = ptAA8y
        self.S5 = np.array([ptS5x, ptS5y])

        ptS6x = ptAA8x - self.data_object.plate_thickness_p1 - self.data_object.flange_thickness_T1
        ptS6y = ptAA8y
        self.S6 = np.array([ptS6x, ptS6y])

        ptS7x = ptAA4x - self.data_object.plate_thickness_p1 - self.data_object.flange_thickness_T1
        ptS7y = ptAA4y
        self.S7 = np.array([ptS7x, ptS7y])

        ptS8x = ptAA4x - self.data_object.plate_thickness_p1 - self.data_object.column_depth_D1 + self.data_object.flange_thickness_T1
        ptS8y = ptAA4y
        self.S8 = np.array([ptS8x, ptS8y])

        # ================ Weld  ==================
        # darshan

        """	
        defining co-ordinates of weld in front view
        right of origin is considered as +ve X axis
        downward to the origin is considered as +ve Y axis
        """
        if self.data_object.weld == "Fillet Weld":

            # ------------------------------------------  Weld triangle  UP ---------------------------------------------
            self.B3 = self.AA1
            self.B2 = self.B3 + self.data_object.flange_weld_thickness * np.array([1, 0])
            self.B1 = self.B3 + self.data_object.flange_weld_thickness * np.array([0, -1])

            self.B6 = self.AA5
            self.B5 = self.B6 + self.data_object.flange_weld_thickness * np.array([1, 0])
            self.B4 = self.B6 + self.data_object.flange_weld_thickness * np.array([0, 1])

            # ------------------------------------------  Weld triangle  DOWN -------------------------------------------
            self.B7 = self.AA8
            self.B8 = self.B7 + self.data_object.flange_weld_thickness * np.array([0, -1])
            self.B9 = self.B7 + self.data_object.flange_weld_thickness * np.array([1, 0])

            self.B11 = self.AA4
            self.B12 = self.B11 + self.data_object.flange_weld_thickness * np.array([1, 0])
            self.B13 = self.B11 + self.data_object.flange_weld_thickness * np.array([0, 1])

        else:
            # ------------------------------------------  Weld triangle  UP ---------------------------------------------
            self.B3 = self.AA1
            self.B2 = self.B3 + self.data_object.flange_thickness_T2 * np.array([1, 0])
            self.B1 = self.B3 + self.data_object.flange_thickness_T2 * np.array([0, 1])
            # ------------------------------------------  Weld triangle  DOWN -------------------------------------------
            self.B11 = self.AA4
            self.B12 = self.B11 + self.data_object.flange_thickness_T2 * np.array([1, 0])
            self.B13 = self.B11 + self.data_object.flange_thickness_T2 * np.array([0, -1])

        self.Lv = self.data_object.Lv

    def call_flush_front(self, filename):
        """

		Args:
			filename: path of the images to be saved

		Returns:
			Saves the image in the folder

		"""
        vb_width = (int(2 * self.data_object.column_length_L1 + 2 * self.data_object.plate_thickness_p1 + 300))
        vb_ht = (int(3 * self.data_object.plate_length_L1))
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=(
            '-600 -400 2000 1800'))
        """
		drawing line as per co-ordinate defined to create the required view
		"""

        dwg.add(dwg.polyline(points=[self.A1, self.A2, self.A3, self.A4, self.A1], stroke='black', fill='none',
                             stroke_width=2.5))
        dwg.add(dwg.line(self.A5, self.A8).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.A6, self.A7).stroke('black', width=2.5, linecap='square'))

        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='black', fill='none',
                             stroke_width='2.5'))
        dwg.add(dwg.polyline(points=[self.AA1, self.AA2, self.AA3, self.AA4, self.AA1], stroke='black', fill='none',
                             stroke_width=2.5))
        dwg.add(dwg.line(self.AA5, self.AA6).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA8, self.AA7).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.S1, self.S2).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.S3, self.S4).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.S5, self.S6).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.S7, self.S8).stroke('black', width=2.5, linecap='square'))

        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse",
                                           patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.S1 - self.data_object.weld_plate_thickness_p2 * np.array([0, 1])),size=((self.data_object.column_depth_D1 - 2 * self.data_object.flange_thickness_T1),
                (self.data_object.weld_plate_thickness_p2)), fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
        dwg.add(dwg.rect(insert=self.S4,size=((self.data_object.column_depth_D1 - 2 * self.data_object.flange_thickness_T1),
                (self.data_object.weld_plate_thickness_p2)), fill="url(#diagonalHatch)", stroke='white',stroke_width=1.0))
        dwg.add(dwg.rect(insert=(self.S5 - self.data_object.weld_plate_thickness_p2 * np.array([0, 1])),size=((self.data_object.column_depth_D1 - 2 * self.data_object.flange_thickness_T1),
             (self.data_object.weld_plate_thickness_p2)), fill="url(#diagonalHatch)", stroke='white',stroke_width=1.0))
        dwg.add(dwg.rect(insert=self.S8,size=((self.data_object.column_depth_D1 - 2 * self.data_object.flange_thickness_T1),
                (self.data_object.weld_plate_thickness_p2)), fill="url(#diagonalHatch)", stroke='white',stroke_width=1.0))

        if self.data_object.weld == "Fillet Weld":
            pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse",
                                               patternTransform="rotate(45 2 2)"))
            pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
            dwg.add(dwg.rect(insert=self.AA5, size=(self.data_object.web_weld_thickness, (
                        self.data_object.beam_depth_D2 - self.data_object.flange_thickness_T2 - self.data_object.flange_weld_thickness - 10)),
                             fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))

            dwg.add(dwg.polyline(points=[self.B3, self.B2, self.B1, self.B3], stroke='black', fill='black',
                                 stroke_width=2.5))
            dwg.add(dwg.polyline(points=[self.B6, self.B5, self.B4, self.B6], stroke='black', fill='black',
                                 stroke_width=2.5))
            dwg.add(dwg.polyline(points=[self.B7, self.B8, self.B9, self.B7], stroke='black', fill='black',
                                 stroke_width=2.5))
            dwg.add(dwg.polyline(points=[self.B11, self.B12, self.B13, self.B11], stroke='black', fill='black',
                                 stroke_width=2.5))
        else:
            dwg.add(dwg.polyline(points=[self.B3, self.B2, self.B1, self.B3], stroke='black', fill='black',
                                 stroke_width=2.5))
            dwg.add(dwg.polyline(points=[self.B11, self.B12, self.B13, self.B11], stroke='black', fill='black',
                                 stroke_width=2.5))

        bitfr = self.data_object.bolts_inside_top_flange_row
        bolt_r = int(self.data_object.bolt_diameter) / 2

        # ------------------------------------------  Bolts Inside Top Flange -------------------------------------------
        pt_inside_top_column_list = []
        for i in range(bitfr):
            if self.data_object.no_of_bolts == 4:
                ptx = self.AA1 - (self.data_object.flange_thickness_T2 + self.Lv) \
                      * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1) * np.array(
                    [1, 0])
            elif self.data_object.no_of_bolts == 8:
                ptx = self.AA1 - (self.data_object.flange_thickness_T2 + self.Lv) \
                      * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1) * np.array(
                    [1, 0]) + i * self.data_object.pitch12 * np.array([0, 1])
            elif self.data_object.no_of_bolts == 12:
                ptx = self.AA1 - (self.data_object.flange_thickness_T2 + self.Lv) \
                      * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1) * np.array(
                    [1, 0]) + i * self.data_object.pitch23 * np.array([0, 1])

            ptx1 = ptx - bolt_r * np.array([0, 1])
            rect_width = float (self.data_object.bolt_diameter)
            rect_length = float (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1)
            dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
            # dwg.add(dwg.rect(insert=ptx1, size=(rect_length,12), fill='black', stroke='black', stroke_width=2.5))

            pt_Cx = ptx + np.array([1, 0])
            pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
            dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
            pt_inside_top_column_list.append(ptx)

            pt_Cx1 = ptx + np.array([-1, 0])
            pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
            dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
            pt_inside_top_column_list.append(ptx)

            bibfr = self.data_object.bolts_inside_bottom_flange_row

        # ------------------------------------------  Bolts Inside Bottom Flange -------------------------------------------
        pt_inside_bottom_column_list = []
        for i in range(bibfr):
            if self.data_object.no_of_bolts == 4:
                ptx = self.AA4 + (self.data_object.flange_thickness_T2 + self.Lv) \
                      * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1) * np.array(
                    [1, 0])
            elif self.data_object.no_of_bolts == 8:
                ptx = self.AA4 + (self.data_object.flange_thickness_T2 + self.Lv) \
                      * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1) * np.array(
                    [1, 0]) + i * self.data_object.pitch12 * np.array([0, -1])

            elif self.data_object.no_of_bolts == 12:
                ptx = self.AA4 + (self.data_object.flange_thickness_T2 + self.Lv) \
                      * np.array([0, -1]) - (self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1) * np.array(
                    [1, 0]) + i * self.data_object.pitch23 * np.array([0, -1])

            ptx1 = ptx - bolt_r * np.array([0, 1])
            rect_width = float(self.data_object.bolt_diameter)
            rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1)
            dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
            # dwg.add(dwg.rect(insert=ptx1, size=(12, 12), fill='black', stroke='black', stroke_width=2.5))

            pt_Cx = ptx + np.array([1, 0])
            pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
            dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
            pt_inside_bottom_column_list.append(ptx)

            pt_Cx1 = ptx + np.array([-1, 0])
            pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
            dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
            pt_inside_bottom_column_list.append(ptx)

        # ------------------------------------------  Labeling Inside top bolt of flange -------------------------------------------
        no_of_bolts_flange = self.data_object.bolts_inside_top_flange_row * self.data_object.no_of_columns
        point = np.array(pt_inside_top_column_list[0])
        theta = 60
        offset = 25
        textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
        textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(
            self.data_object.bolt_type) + " bolts (grade " + str(
            self.data_object.grade) + ")"
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        # ------------------------------------------  Labeling Inside bottom bolt of flange -------------------------------------------
        no_of_bolts_flange = self.data_object.bolts_inside_bottom_flange_row * self.data_object.no_of_columns
        point = np.array(pt_inside_bottom_column_list[1])
        theta = 60
        offset = 25
        textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
        textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(
            self.data_object.bolt_type) + " bolts (grade " + str(
            self.data_object.grade) + ")"
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown, element)

        # ------------------------------------------  Labeling Weld of flange -------------------------------------------
        # point = self.AA1
        # theta = 60
        # offset = 100
        # textup = "          z  " + str(self.data_object.flange_weld_thickness)
        # textdown = " "
        # element = "weld"
        # self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

        if self.data_object.weld == "Fillet Weld":
            point = self.AA1
            theta = 60
            offset = 50
            textup = "          z " + str(self.data_object.flange_weld_thickness)
            textdown = "          z " + str(self.data_object.flange_weld_thickness)
            element = "weld"
            self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
        else:
            point = self.AA1
            theta = 60
            offset = 50
            textup = "               "
            textdown = "               "
            element = "weld"
            self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

        # ------------------------------------------  Labeling Weld of Web -------------------------------------------
        # point = self.AA1  + self.data_object.beam_depth_D2/2 * np.array([0, 1])
        # theta = 60
        # offset = 100
        # textup = "         z  " + str(self.data_object.web_weld_thickness)
        # textdown = " "
        # element = "weld"
        # self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

        if self.data_object.weld == "Fillet Weld":
            point = self.AA1 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
            theta = 60
            offset = 100
            textup = "         z  " + str(self.data_object.web_weld_thickness)
            textdown = "         z  " + str(self.data_object.web_weld_thickness)
            element = "weld"
            self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
        else:
            point = self.AA1 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
            theta = 60
            offset = 100
            textup = "               "
            textdown = "               "
            element = "weld"
            self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

        # ------------------------------------------  Primary Beam 1& 2 -------------------------------------------
        point = self.A1
        theta = 60
        offset = 50
        textup = "Beam " + str(self.data_object.column_designation)
        textdown = " "
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        point = self.AA2 - 100 * np.array([1, 0])
        theta = 60
        offset = 50
        textup = "Beam " + str(self.data_object.beam_designation)
        textdown = " "
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

        # ------------------------------------------  End Plate 1 & 2-------------------------------------------
        point = self.P1
        theta = 60
        offset = 100
        textup = "End Plate " + str(self.data_object.plate_length_L1) + "x" + str(
            self.data_object.plate_width_B1) + "x" + str(
            self.data_object.plate_thickness_p1)
        textdown = " "
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        # ------------------------------------------  Sectional arrow -------------------------------------------
        pt_a1 = self.A1 + (300) * np.array([0, -1])
        pt_b1 = pt_a1 + (50 * np.array([0, 1]))
        txt_1 = pt_b1 + (20 * np.array([-1, 0])) + (75 * np.array([0, 1]))
        text = "A"
        self.data_object.draw_cross_section(dwg, pt_a1, pt_b1, txt_1, text)

        pt_a2 = pt_a1 + (self.data_object.column_depth_D1 + self.data_object.beam_length_L2 + self.data_object.plate_thickness_p1) * np.array(
            [1, 0])
        pt_b2 = pt_a2 + (50 * np.array([0, 1]))
        txt_2 = pt_b2 + (20 * np.array([-1, 0])) + (75 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, pt_a2, pt_b2, txt_2, text)

        dwg.add(dwg.line(pt_a1, pt_a2).stroke('black', width=1.5, linecap='square'))

        # ------------------------------------------  View details-------------------------------------------
        ptx = self.A3 - 100 * np.array([1, 0]) + 100 * np.array([0, 1])
        dwg.add(dwg.text('Front view (Sec C-C) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = ptx + 40 * np.array([0, 1])
        dwg.add(
            dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

        dwg.save()

class FlushEnd2DTop(object):
    """
	Contains functions for generating the top view of the Extended bothway endplate connection.

	"""

    def __init__(self, extnd_common_object):
        self.data_object = extnd_common_object
        # -------------------------------------------------------------------------------------------------
        #                                           TOP VIEW
        # -------------------------------------------------------------------------------------------------
        # ====================== Column 1  =====================

        """	
		defining co-ordinates of Beam B1 in top view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptA1x = 0
        ptA1y = 0
        self.A1 = np.array([ptA1x, ptA1y])

        ptA2x = ptA1x + self.data_object.flange_thickness_T1
        ptA2y = 0
        self.A2 = np.array([ptA2x, ptA2y])

        ptA3x = ptA2x
        ptA3y = ptA2y + self.data_object.column_width_B1
        self.A3 = np.array([ptA3x, ptA3y])

        ptA4x = ptA1x
        ptA4y = ptA1y + self.data_object.column_width_B1
        self.A4 = np.array([ptA4x, ptA4y])

        ptA5x = ptA2x
        ptA5y = ptA2y + self.data_object.column_width_B1 / 2 - self.data_object.flange_thickness_T1 / 2
        self.A5 = np.array([ptA5x, ptA5y])

        ptA6x = ptA5x + self.data_object.column_depth_D1 - (2 * self.data_object.flange_thickness_T1)
        ptA6y = ptA5y
        self.A6 = np.array([ptA6x, ptA6y])

        ptA7x = ptA6x
        ptA7y = ptA6y + self.data_object.web_thickness_tw1
        self.A7 = np.array([ptA7x, ptA7y])

        ptA8x = ptA5x
        ptA8y = ptA5y + self.data_object.web_thickness_tw1
        self.A8 = np.array([ptA8x, ptA8y])

        ptA9x = ptA1x + self.data_object.column_depth_D1 - self.data_object.flange_thickness_T1
        ptA9y = ptA1y
        self.A9 = np.array([ptA9x, ptA9y])

        ptA10x = ptA9x + self.data_object.flange_thickness_T1
        ptA10y = ptA9y
        self.A10 = np.array([ptA10x, ptA10y])

        ptA11x = ptA10x
        ptA11y = ptA10y + self.data_object.column_width_B1
        self.A11 = np.array([ptA11x, ptA11y])

        ptA12x = ptA9x
        ptA12y = ptA9y + self.data_object.column_width_B1
        self.A12 = np.array([ptA12x, ptA12y])


        # ====================== End Plate   =====================

        """	
		defining co-ordinates of plate in top view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptP1x = ptA10x
        ptP1y = ptA10y + self.data_object.column_width_B1 / 2 - self.data_object.plate_width_B1 / 2
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = ptP1x + self.data_object.plate_thickness_p1
        ptP2y = ptP1y
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = ptP2x
        ptP3y = ptP2y + self.data_object.plate_width_B1
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP3x - self.data_object.plate_thickness_p1
        ptP4y = ptP3y
        self.P4 = np.array([ptP4x, ptP4y])

        # ====================== Beam ==========================
        """	
		defining co-ordinates of Beam 2 in top view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptAA1x = ptP2x
        ptAA1y = ptP2y + self.data_object.plate_width_B1 / 2 - self.data_object.beam_width_B2 / 2
        self.AA1 = np.array([ptAA1x, ptAA1y])

        ptAA2x = ptAA1x + self.data_object.beam_length_L2
        ptAA2y = ptAA1y
        self.AA2 = np.array([ptAA2x, ptAA2y])

        ptAA3x = ptAA2x
        ptAA3y = ptAA2y + self.data_object.beam_width_B2
        self.AA3 = np.array([ptAA3x, ptAA3y])

        ptAA4x = ptAA1x
        ptAA4y = ptAA1y + self.data_object.beam_width_B2
        self.AA4 = np.array([ptAA4x, ptAA4y])

        ptAA5x = ptAA1x
        ptAA5y = ptAA1y + (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2) / 2
        self.AA5 = np.array([ptAA5x, ptAA5y])

        ptAA6x = ptAA2x
        ptAA6y = ptAA2y + (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2) / 2
        self.AA6 = np.array([ptAA6x, ptAA6y])

        ptAA7x = ptAA6x
        ptAA7y = ptAA6y + self.data_object.web_thickness_tw2
        self.AA7 = np.array([ptAA7x, ptAA7y])

        ptAA8x = ptAA5x
        ptAA8y = ptAA5y + self.data_object.web_thickness_tw2
        self.AA8 = np.array([ptAA8x, ptAA8y])


    def call_flush_top(self, filename):
        """

		Args:
			filename: path of the images to be saved

		Returns:
			Saves the image in the folder

		"""
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-500 -500 2000 1500'))
        dwg.add(dwg.polyline(points=[self.A1, self.A2, self.A3, self.A4, self.A1], stroke='black', fill='none',
                             stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.A9, self.A10, self.A11, self.A12, self.A9], stroke='black', fill='none',
                             stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.A5, self.A6, self.A7, self.A8, self.A5], stroke='black', fill='none',
                             stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='black', fill='none',
                             stroke_width='2.5'))

        dwg.add(dwg.line(self.AA5, self.AA6).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA7, self.AA8).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.A2, self.A9).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.A3, self.A12).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.AA1, self.AA2, self.AA3, self.AA4, self.AA1], stroke='black', fill='none',
                             stroke_width=2.5))

        if self.data_object.weld == "Fillet Weld":
            pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse",
                                               patternTransform="rotate(45 2 2)"))
            pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
            dwg.add(
                dwg.rect(insert=self.AA1, size=(self.data_object.flange_weld_thickness, self.data_object.beam_width_B2),
                         fill="url(#diagonalHatch)",
                         stroke='white', stroke_width=1.0))
        else:
            pass

        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse",
                                           patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.A2, size=(self.data_object.weld_plate_thickness_p2, (
                self.data_object.column_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2)),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A5 - self.data_object.weld_plate_thickness_p2 * np.array([0, 1])), size=(
            (self.data_object.column_depth_D1 - 2 * self.data_object.flange_thickness_T1),
            self.data_object.weld_plate_thickness_p2),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A9 - self.data_object.weld_plate_thickness_p2 * np.array([1, 0])), size=(
            self.data_object.weld_plate_thickness_p2,
            (self.data_object.column_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2)),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.A8, size=(self.data_object.weld_plate_thickness_p2, (
                self.data_object.column_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2)),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.A8, size=((self.data_object.column_depth_D1 - 2 * self.data_object.flange_thickness_T1),
                 self.data_object.weld_plate_thickness_p2), fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
        pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A7 - self.data_object.weld_plate_thickness_p2 * np.array([1, 0])), size=(
            self.data_object.weld_plate_thickness_p2,
            (self.data_object.column_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2)),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))

        nofc = self.data_object.no_of_columns
        bolt_r = int(self.data_object.bolt_diameter) / 2

        # ------------------------------------------  Bolts Outside Top Flange -------------------------------------------
        pt_outside_top_column_list = []
        if nofc >= 1:
            for i in range(nofc):
                ptx = self.P2 + self.data_object.edge_dist * np.array([0, 1]) - \
                      (self.data_object.flange_thickness_T1 + self.data_object.plate_thickness_p1) * np.array([1, 0]) + \
                      i * self.data_object.cross_centre_gauge_dist * np.array([0, 1])
                ptx1 = ptx - bolt_r * np.array([0, 1])
                rect_width = float(self.data_object.bolt_diameter)
                rect_length = float(self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1)
                dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black',
                                 stroke_width=2.5))
                # dwg.add(dwg.rect(insert=ptx1, size=(12, 12), fill='black', stroke='black', stroke_width=2.5))

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
        pty1 = ptx1 + (self.data_object.beam_length_L2 + 60) * np.array([1, 0])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_outside_top_column_list[1]) + self.data_object.cross_centre_gauge_dist * np.array([0, 1])
        pty2 = ptx2 + (self.data_object.beam_length_L2 + 60) * np.array([1, 0])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + (self.data_object.cross_centre_gauge_dist) * np.array([0, -1])
        params = {"offset": (self.data_object.beam_length_L2 + 60), "textoffset": 10, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.cross_centre_gauge_dist),
                                                    params)

        # ------------------------------------------  Primary Beam 1& 2 -------------------------------------------
        point = self.A2
        theta = 60
        offset = 50
        textdown = " "
        textup = "Beam " + str(self.data_object.column_designation)
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
        point = self.P1  + self.data_object.plate_thickness_p1 / 2 * np.array([1, 0])
        theta = 60
        offset = 150
        textdown = " "
        textup = "End Plate " + str(self.data_object.plate_length_L1) + "x" + str(
            self.data_object.plate_width_B1) + "x" + str(
            self.data_object.plate_thickness_p1)
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        # ------------------------------------------ Continuity Plate-------------------------------------------
        point = self.A8 + self.data_object.column_depth_D1 / 4* np.array([1, 0])
        theta = 60
        offset = 50
        textup = "Continuity Plate" + str(self.data_object.plate_length_L2) + "x" + str(
            self.data_object.plate_width_B2) + "x" + str(
            self.data_object.plate_thickness_p2)
        textdown = " "
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        # ------------------------------------------  Weld label --------------------------------------------------
        # point = self.AA1 + 2
        # theta = 60
        # offset = 50
        # textup = "   z      " + str(self.data_object.flange_weld_thickness)
        # textdown = " "
        # element = "weld"
        # self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)
        self.data_object.stiffener_weld = 1
        point = self.A3 - self.data_object.column_width_B1 / 4 * np.array([0, 1])
        theta = 1
        offset = 1
        textup = "          z " + str(self.data_object.weld_plate_thickness_p2)
        textdown = "          z " + str(self.data_object.weld_plate_thickness_p2)
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)
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

        # ------------------------------------------  Sectional arrow -------------------------------------------
        pt_a1 = self.A4 - (200) * np.array([0, -1]) - (100 * np.array([1, 0]))
        pt_b1 = pt_a1 + (50 * np.array([0, -1]))
        txt_1 = pt_b1 + (50 * np.array([0, -1])) + (20 * np.array([-1, 0]))
        text = "C"
        self.data_object.draw_cross_section(dwg, pt_a1, pt_b1, txt_1, text)

        pt_a2 = pt_a1 + (
                self.data_object.column_depth_D1 + self.data_object.beam_length_L2 + self.data_object.plate_thickness_p1) * np.array(
            [1, 0]) + 200 * np.array([1, 0])
        pt_b2 = pt_a2 + (50 * np.array([0, -1]))
        txt_2 = pt_b2 + (50 * np.array([0, -1])) + (20 * np.array([-1, 0]))
        self.data_object.draw_cross_section(dwg, pt_a2, pt_b2, txt_2, text)

        dwg.add(dwg.line(pt_a1, pt_a2).stroke('black', width=1.5, linecap='square'))

        pt_a3 = self.A2 + (self.data_object.beam_length_L2 + 750) * np.array([1, 0])
        pt_b3 = pt_a3 + (50 * np.array([-1, 0]))
        txt_3 = pt_b3 + (75 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        text = "B"
        self.data_object.draw_cross_section(dwg, pt_a3, pt_b3, txt_3, text)

        pt_a4 = pt_a3 + (self.data_object.column_width_B1 * np.array([0, 1]))
        pt_b4 = pt_a4 + (50 * np.array([-1, 0]))
        txt_4 = pt_b4 + (75 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, pt_a4, pt_b4, txt_4, text)

        dwg.add(dwg.line(pt_a3, pt_a4).stroke('black', width=1.5, linecap='square'))

        # ------------------------------------------  View details -------------------------------------------
        ptx = self.P4 - 50 * np.array([1, 0]) + 300 * np.array([0, 1])
        dwg.add(dwg.text('Top view (Sec A-A) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = ptx + 40 * np.array([0, 1])
        dwg.add(
            dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

        dwg.save()


class FlushEnd2DSide(object):
    """
	Contains functions for generating the side view of the Extended bothway endplate connection.

	"""

    def __init__(self, extnd_common_object):
        self.data_object = extnd_common_object

        # =========================  End Plate 1  =========================
        """	
		defining co-ordinates of plate in side view
		right of origin is considered as +ve X axis
		downward to the origin is considered as +ve Y axis
		"""

        ptP1x = 0
        ptP1y = 0
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = ptP1x + self.data_object.plate_width_B1
        ptP2y = 0
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = ptP2x
        ptP3y = ptP2y + self.data_object.plate_length_L1
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP1x
        ptP4y = ptP1x + self.data_object.plate_length_L1
        self.P4 = np.array([ptP4x, ptP4y])

        # ========================= Beam  =========================

        ptA1x = ptP1x + (self.data_object.plate_width_B1 - self.data_object.beam_width_B2) / 2
        ptA1y = ptP1y + (self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2
        self.A1 = np.array([ptA1x, ptA1y])

        ptA2x = ptA1x + self.data_object.beam_width_B2
        ptA2y = ptA1y
        self.A2 = np.array([ptA2x, ptA2y])

        ptA3x = ptA2x
        ptA3y = ptA2y + self.data_object.flange_thickness_T2
        self.A3 = np.array([ptA3x, ptA3y])

        ptA12x = ptA1x
        ptA12y = ptA1y + self.data_object.flange_thickness_T2
        self.A12 = np.array([ptA12x, ptA12y])

        ptA4x = ptA12x + (self.data_object.beam_width_B2 / 2 + self.data_object.web_thickness_tw2 / 2)
        ptA4y = ptA3y
        self.A4 = np.array([ptA4x, ptA4y])

        ptA8x = ptA1x
        ptA8y = (self.data_object.plate_length_L1 + self.data_object.beam_depth_D2) / 2
        self.A8 = np.array([ptA8x, ptA8y])

        ptA9x = ptA1x
        ptA9y = ptA8y - self.data_object.flange_thickness_T2
        self.A9 = np.array([ptA9x, ptA9y])

        ptA7x = ptA8x + self.data_object.beam_width_B2
        ptA7y = ptA8y
        self.A7 = np.array([ptA7x, ptA7y])

        ptA6x = ptA7x
        ptA6y = ptA7y - self.data_object.flange_thickness_T2
        self.A6 = np.array([ptA6x, ptA6y])

        ptA5x = ptA4x
        ptA5y = ptA6y
        self.A5 = np.array([ptA5x, ptA5y])

        ptA11x = ptA12x + (self.data_object.beam_width_B2 / 2 - self.data_object.web_thickness_tw2 / 2)
        ptA11y = ptA12y
        self.A11 = np.array([ptA11x, ptA11y])

        ptA10x = ptA11x
        ptA10y = ptA9y
        self.A10 = np.array([ptA10x, ptA10y])

        self.P = self.A11 - self.data_object.web_weld_thickness * np.array([1, 0])

        # ========================= Column  =========================

        ptAA1x = ptP1x + self.data_object.plate_width_B1 / 2 - self.data_object.column_width_B1 / 2
        ptAA1y = ptP1y + self.data_object.plate_length_L1 / 2 - self.data_object.column_length_L1 / 2
        self.AA1 = np.array([ptAA1x, ptAA1y])

        ptAA2x = ptAA1x + self.data_object.column_width_B1
        ptAA2y = ptAA1y
        self.AA2 = np.array([ptAA2x, ptAA2y])

        ptAA3x = ptAA2x
        ptAA3y = ptAA2y + self.data_object.column_length_L1 / 2 - self.data_object.plate_length_L1 / 2
        self.AA3 = np.array([ptAA3x, ptAA3y])

        ptAA4x = ptAA1x
        ptAA4y = ptAA1y + self.data_object.column_length_L1 / 2 - self.data_object.plate_length_L1 / 2
        self.AA4 = np.array([ptAA4x, ptAA4y])

        ptAA5x = ptAA4x
        ptAA5y = ptAA4y + self.data_object.plate_length_L1
        self.AA5 = np.array([ptAA5x, ptAA5y])

        ptAA6x = ptAA3x
        ptAA6y = ptAA3y + self.data_object.plate_length_L1
        self.AA6 = np.array([ptAA6x, ptAA6y])

        ptAA7x = ptAA6x
        ptAA7y = ptAA6y - self.data_object.plate_length_L1 / 2 + self.data_object.column_length_L1 / 2
        self.AA7 = np.array([ptAA7x, ptAA7y])

        ptAA8x = ptAA7x - self.data_object.column_width_B1
        ptAA8y = ptAA7y
        self.AA8 = np.array([ptAA8x, ptAA8y])

        ptAA9x = ptAA1x + self.data_object.column_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2
        ptAA9y = ptAA1y
        self.AA9 = np.array([ptAA9x, ptAA9y])

        ptAA10x = ptAA9x + self.data_object.web_thickness_tw1
        ptAA10y = ptAA1y
        self.AA10 = np.array([ptAA10x, ptAA10y])

        ptAA11x = ptAA4x + self.data_object.column_width_B1 / 2 + self.data_object.web_thickness_tw1 / 2
        ptAA11y = ptAA4y
        self.AA11 = np.array([ptAA11x, ptAA11y])

        ptAA12x = ptAA11x - self.data_object.web_thickness_tw1
        ptAA12y = ptAA11y
        self.AA12 = np.array([ptAA12x, ptAA12y])

        ptAA13x = ptAA5x + self.data_object.column_width_B1 / 2 - self.data_object.web_thickness_tw1 / 2
        ptAA13y = ptAA5y
        self.AA13 = np.array([ptAA13x, ptAA13y])

        ptAA14x = ptAA13x + self.data_object.web_thickness_tw1
        ptAA14y = ptAA5y
        self.AA14 = np.array([ptAA14x, ptAA14y])

        ptAA15x = ptAA7x - self.data_object.column_width_B1 / 2 + self.data_object.web_thickness_tw1 / 2
        ptAA15y = ptAA7y
        self.AA15 = np.array([ptAA15x, ptAA15y])

        ptAA16x = ptAA15x - self.data_object.web_thickness_tw1
        ptAA16y = ptAA7y
        self.AA16 = np.array([ptAA16x, ptAA16y])

        # =========================  Continuity Plate  =========================
        """	
        defining co-ordinates of plate in side view
        right of origin is considered as +ve X axis
        downward to the origin is considered as +ve Y axis
        """

        ptS1x = ptA1x - self.data_object.column_width_B1 / 2 + self.data_object.beam_width_B2 / 2
        ptS1y = ptA1y
        self.S1 = np.array([ptS1x, ptS1y])

        ptS2x = ptA12x - self.data_object.column_width_B1 / 2 + self.data_object.beam_width_B2 / 2
        ptS2y = ptA12y
        self.S2 = np.array([ptS2x, ptS2y])

        ptS3x = ptA9x - self.data_object.column_width_B1 / 2 + self.data_object.beam_width_B2 / 2
        ptS3y = ptA9y
        self.S3 = np.array([ptS3x, ptS3y])

        ptS4x = ptA8x - self.data_object.column_width_B1 / 2 + self.data_object.beam_width_B2 / 2
        ptS4y = ptA8y
        self.S4 = np.array([ptS4x, ptS4y])

        ptS5x = ptA7x + self.data_object.column_width_B1 / 2 - self.data_object.beam_width_B2 / 2
        ptS5y = ptA7y
        self.S5 = np.array([ptS5x, ptS5y])

        ptS6x = ptA6x + self.data_object.column_width_B1 / 2 - self.data_object.beam_width_B2 / 2
        ptS6y = ptA6y
        self.S6 = np.array([ptS6x, ptS6y])

        ptS7x = ptA3x + self.data_object.column_width_B1 / 2 - self.data_object.beam_width_B2 / 2
        ptS7y = ptA3y
        self.S7 = np.array([ptS7x, ptS7y])

        ptS8x = ptA2x + self.data_object.column_width_B1 / 2 - self.data_object.beam_width_B2 / 2
        ptS8y = ptA2y
        self.S8 = np.array([ptS8x, ptS8y])

    def call_flush_side(self, filename):
        """

		Args:
			filename: path of the images to be saved

		Returns:
			Saves the image in the folder

		"""
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-600 -500 1500 1500'))
        dwg.add(dwg.polyline(
            points=[self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7, self.A8, self.A9, self.A10, self.A11,
                    self.A12, self.A1],
            stroke='black', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='black', fill='none',
                             stroke_width='2.5'))
        dwg.add(dwg.line(self.AA1, self.AA2).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA1, self.AA4).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA2, self.AA3).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA5, self.AA8).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA8, self.AA7).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA6, self.AA7).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA9, self.AA12).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA10, self.AA11).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA13, self.AA16).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA14, self.AA15).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA4, self.AA5).stroke('black', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA3, self.AA6).stroke('black', width=2.5, linecap='square'))

        dwg.add(dwg.line(self.S1, self.A1).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S2, self.A12).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S3, self.A9).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S4, self.A8).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S5, self.A7).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S6, self.A6).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S7, self.A3).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.S8, self.A2).stroke('black', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))

        if self.data_object.weld == "Fillet Weld":
            pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(2, 6), patternUnits="userSpaceOnUse",
                                               patternTransform="rotate(45 1 1)"))
            pattern.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))

            dwg.add(dwg.rect(insert=self.A11 - self.data_object.web_weld_thickness * np.array([1, 0]),
                             size=(self.data_object.web_weld_thickness,
                                   (self.data_object.beam_depth_D2 - (2 * self.data_object.flange_thickness_T2))),
                             fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))
            dwg.add(dwg.rect(insert=self.A4,
                             size=(self.data_object.web_weld_thickness,
                                   (self.data_object.beam_depth_D2 - (2 * self.data_object.flange_thickness_T2))),
                             fill="url(#diagonalHatch)", stroke='white', stroke_width=1.0))

            pattern1 = dwg.defs.add(dwg.pattern(id="diagonalHatch1", size=(6, 6), patternUnits="userSpaceOnUse",
                                                patternTransform="rotate(45 2 2)", ))
            pattern1.add(dwg.path(d="M 0,1 l 6,0", stroke='#000000', stroke_width=2.5))
            dwg.add(dwg.rect(insert=(self.A1 - self.data_object.flange_weld_thickness * np.array([0, 1])),
                             size=(self.data_object.beam_width_B2, self.data_object.flange_weld_thickness),
                             fill="url(#diagonalHatch1)", stroke='white',
                             stroke_width=1.0))
            dwg.add(dwg.rect(insert=self.A4,
                             size=((self.data_object.beam_width_B2 / 2 - self.data_object.web_thickness_tw1 / 2),
                                   self.data_object.flange_weld_thickness),
                             fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
            dwg.add(dwg.rect(insert=(self.A9 - self.data_object.flange_weld_thickness * np.array([0, 1])),
                             size=((self.data_object.beam_width_B2 / 2 - self.data_object.web_thickness_tw2 / 2),
                                   self.data_object.flange_weld_thickness),
                             fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
            dwg.add(dwg.rect(insert=(self.A5 - self.data_object.flange_weld_thickness * np.array([0, 1])),
                             size=((self.data_object.beam_width_B2 / 2 - self.data_object.web_thickness_tw2 / 2),
                                   self.data_object.flange_weld_thickness),
                             fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
            dwg.add(dwg.rect(insert=self.A12,
                             size=((self.data_object.beam_width_B2 / 2 - self.data_object.web_thickness_tw2 / 2),
                                   self.data_object.flange_weld_thickness),
                             fill="url(#diagonalHatch1)", stroke='white', stroke_width=1.0))
            dwg.add(dwg.rect(insert=self.A8,
                             size=(self.data_object.beam_width_B2, self.data_object.flange_weld_thickness),
                             fill="url(#diagonalHatch1)", stroke='white',
                             stroke_width=1.0))

        else:
            pass

        nofc = self.data_object.no_of_columns
        bitfr = self.data_object.bolts_inside_top_flange_row
        bolt_r = int(self.data_object.bolt_diameter) / 2

        # ------------------------------------------  Bolts Inside Top Flange -------------------------------------------
        pt_inside_top_column_list = []
        for i in range(1, (bitfr + 1)):
            col_inside_list_top = []
            for j in range(1, (nofc + 1)):
                if self.data_object.no_of_bolts == 4:
                    pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T2 + self.data_object.Lv) * np.array(
                        [0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
                elif self.data_object.no_of_bolts == 8:
                    pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T1 + self.data_object.Lv) * np.array(
                        [0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch12 * np.array([0, 1]) + (
                                 j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
                elif self.data_object.no_of_bolts == 12:
                    pt = self.P1 + ((self.data_object.plate_length_L1 - self.data_object.beam_depth_D2) / 2 + self.data_object.flange_thickness_T1 + self.data_object.Lv) * np.array(
                        [0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch23 * np.array([0, 1]) + (
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
        bibfr = self.data_object.bolts_inside_bottom_flange_row

        # ------------------------------------------  Bolts Inside Bottom Flange -------------------------------------------
        pt_inside_bottom_column_list = []
        for i in range(1, (bibfr + 1)):
            col_inside_list_bottom = []
            for j in range(1, (nofc + 1)):
                if self.data_object.no_of_bolts == 4:
                    pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D2) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv) * np.array(
                        [0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
                elif self.data_object.no_of_bolts == 8:
                    pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D2) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv) * np.array(
                        [0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch34 * np.array([0, -1]) + (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
                elif self.data_object.no_of_bolts == 12:
                    pt = self.P1 + ((self.data_object.plate_length_L1 + self.data_object.beam_depth_D2) / 2 - self.data_object.flange_thickness_T1 - self.data_object.Lv) * np.array(
                        [0, 1]) + self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch45 * np.array([0, -1]) + (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])

                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='black', fill='none', stroke_width=1.5))
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

        ptx2 = np.array(pt_inside_top_column_list[0][0])
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

        ptxx2 = np.array(pt_inside_top_column_list[0][1])
        ptyy2 = ptxx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

        point2 = ptxx2 + (self.data_object.edge_dist) * np.array([1, 0])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptxx2, point2, str(self.data_object.edge_dist), params)

        ptxx3 = np.array(pt_inside_top_column_list[0][1])
        ptyy3 = ptxx3 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
        self.data_object.draw_faint_line(ptxx3, ptyy3, dwg)

        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, point1, point2, str(self.data_object.cross_centre_gauge_dist),
                                                    params)

        # ------------------------------------------  Faint line for inside top flange bolts-------------------------------------------
        if self.data_object.no_of_bolts == 4:
            ptx1 = np.array(pt_inside_top_column_list[0][1])
            pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx1, pty1, dwg)

            ptx2 = np.array(pt_inside_bottom_column_list[0][1])
            pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx2, pty2, dwg)

            point1 = np.array(pt_inside_top_column_list[0][1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch12), params)

            point2 = ptx1 + self.data_object.Lv * np.array([0, -1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10,
                      "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx1, point2, str(self.data_object.Lv), params)

        elif self.data_object.no_of_bolts == 8:
            ptx2 = np.array(pt_inside_top_column_list[1][1])
            pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx2, pty2, dwg)

            ptx3 = np.array(pt_inside_top_column_list[0][1])
            pty3 = ptx3 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx3, pty3, dwg)

            point3 = ptx3 + self.data_object.Lv * np.array([0, -1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx3, point3, str(self.data_object.Lv), params)

            point2 =np.array(pt_inside_top_column_list[1][1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx3, point2, str(self.data_object.pitch12), params)

            point1 = np.array(pt_inside_bottom_column_list[1][1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch23), params)

        elif self.data_object.no_of_bolts == 12:
            ptx2 = np.array(pt_inside_top_column_list[1][1])
            pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx2, pty2, dwg)

            ptx3 = np.array(pt_inside_top_column_list[0][1])
            pty3 = ptx3 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx3, pty3, dwg)

            point1 = ptx3 + self.data_object.pitch12 * np.array([0, 1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, point1, ptx3, str(self.data_object.pitch12), params)

            point3 = ptx3 + self.data_object.Lv * np.array([0, -1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                      "endlinedim": 10,
                      "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, point3, ptx3, str(self.data_object.Lv), params)

            ptx4 = np.array(pt_inside_top_column_list[2][1])
            pty4 = ptx4 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx4, pty4, dwg)

            point2 = ptx4 + self.data_object.pitch23 * np.array([0, -1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10,
                      "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx4, point2, str(self.data_object.pitch23), params)

            point2 = np.array(pt_inside_bottom_column_list[2][1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                      "endlinedim": 10,
                      "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx4, point2, str(self.data_object.pitch34), params)

        # ------------------------------------------  Faint line for inside bottom flange bolts-------------------------------------------
        if self.data_object.no_of_bolts == 4:
            ptx2 = np.array(pt_inside_bottom_column_list[0][1])
            pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx2, pty2, dwg)

            point2 = np.array(pt_inside_bottom_column_list[0][1]) + self.data_object.Lv * np.array([0, 1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, point2, ptx2, str(self.data_object.Lv), params)

        elif self.data_object.no_of_bolts == 8:
            ptx1 = np.array(pt_inside_bottom_column_list[1][1])
            pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx1, pty1, dwg)

            ptx2 = np.array(pt_inside_bottom_column_list[0][1])
            pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx2, pty2, dwg)

            point1 = ptx2 + self.data_object.pitch34 * np.array([0, -1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch34), params)

            point2 =  np.array(pt_inside_bottom_column_list[0][1]) + self.data_object.Lv * np.array([0, 1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg,point2, ptx2, str(self.data_object.Lv), params)

        elif self.data_object.no_of_bolts == 12:
            ptx5 = np.array(pt_inside_bottom_column_list[2][1])
            pty5 = ptx5 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx5, pty5, dwg)

            point2 = ptx5 + self.data_object.pitch45 * np.array([0, 1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx5, point2, str(self.data_object.pitch45), params)

            ptx6 = np.array(pt_inside_bottom_column_list[1][1])
            pty6 = ptx6 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx6, pty6, dwg)

            ptx7 = np.array(pt_inside_bottom_column_list[0][1])
            pty7 = ptx7 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx7, pty7, dwg)

            point1 = ptx7 + self.data_object.pitch56 * np.array([0, -1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, ptx7, point1, str(self.data_object.pitch56), params)

            ptx7 = np.array(pt_inside_bottom_column_list[0][1])
            pty7 = ptx7 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
            self.data_object.draw_faint_line(ptx7, pty7, dwg)

            point3 =  np.array(pt_inside_bottom_column_list[0][1]) + self.data_object.Lv * np.array([0, 1])
            params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right",
                      "endlinedim": 10, "arrowlen": 20}
            self.data_object.draw_dimension_outer_arrow(dwg, point3, ptx7, str(self.data_object.Lv), params)

        # ------------------------------------------  End Plate 1 -------------------------------------------
        point = self.P2
        theta = 60
        offset = 100
        textup = "End plate " + str(self.data_object.plate_length_L1) + "x" + str(
            self.data_object.plate_width_B1) + "x" + str(
            self.data_object.plate_thickness_p1)
        textdown = " "
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown, element)

        # ------------------------------------------  Primary Beam 1 -------------------------------------------
        point = self.A1
        theta = 1
        offset = 1
        textup = " "
        textdown = "Beam " + str(self.data_object.beam_designation)
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        point = self.AA1
        theta = 1
        offset = 1
        textup = " "
        textdown = "Beam " + str(self.data_object.column_designation)
        element = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

        # ---------------------------------------------  Web Welding ----------------------------------------------
        if self.data_object.weld == "Fillet Weld":
            point = self.A11 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
            theta = 60
            offset = 50
            textup = "                    z " + str(self.data_object.web_weld_thickness)
            textdown = "                    z " + str(self.data_object.web_weld_thickness)
            element = "weld"
            self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)
        else:
            point = self.A11 + self.data_object.beam_depth_D2 / 2 * np.array([0, 1])
            theta = 60
            offset = 50
            textup = "               "
            textdown = "               "
            element = "weld"
            self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown, element)

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
        ptx = self.AA8 * np.array([0, 1]) + 100 * np.array([0, 1])
        dwg.add(dwg.text('Side view (Sec B-B) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = ptx + 40 * np.array([0, 1])
        dwg.add(
            dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

        dwg.save()

