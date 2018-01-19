'''
Created on 24-Aug-2017

@author: reshma
'''
from numpy import math
import svgwrite
import cairosvg
import numpy as np
import os


class CoverEndPlate(object):
    def __init__(self, input):
        # self.filename = filename
        self.beam_length_L1 = 1000
        self.beam_length_L2 = 1000

        self.beam_depth_D1 = 450
        self.beam_depth_D2 = 450

        self.beam_width_B1 = 150
        self.beam_width_B2 = 150

        self.plate_thickness_p1 = 16
        self.plate_thickness_p2 = 16
        self.plate_thickness_p3 = 10

        self.plate_width_B1 = 150
        self.plate_width_B2 = 150
        self.plate_width_B3 = 180

        self.plate_length_L1 = 520
        self.plate_length_L2 = 520
        self.plate_length_L3 = 280

        self.flange_thickness_T1 = 17.4
        self.flange_thickness_T2 = 17.4

        self.web_thickness_tw1 = float(input["WebPlate"]["Thickness (mm)"])  #9.4
        self.web_thickness_tw2 = 9.4

        self.gap_btwn_2beam = float(input["detailing"]["gap"])     #5

        self.bolt_diameter = int(input["Bolt"]["Diameter (mm)"])
        self.bolt_hole_diameter =22

        self.edge_dist1 = 40
        self.edge_dist2 = 40
        self.end_dist = 40

        self.cross_centre_gauge_dist = 100
        self.gauge = 90

        self.pitch1 = 60
        self.pitch2 = 100

        self.bolt_type = input["Bolt"]["Type"]
        self.grade = float(input["Bolt"]["Grade"])

        self.bolts_top_flange1_col = 4
        self.bolts_top_flange1_row = 1  # TODO value should come from dict
        self.bolts_top_of_flange1_row = 2    # TODO value should come from dict

        self.bolts_top_flange2_col = 4
        self.bolts_top_flange2_row = 1  # TODO value should come from dict
        self.bolts_top_of_flange2_row = 2    # TODO value should come from dict

        self.bolts_inside_web_col = 2
        self.bolts_inside_web_row = 3    # TODO value should come from dict

        self.bolts_bottom_flange1_col = 4
        self.bolts_bottom_flange1_row = 1   # TODO value should come from dict

        self.bolts_bottom_flange2_col = 4
        self.bolts_bottom_flange2_row = 1   # TODO value should come from dict

    def add_s_marker(self, dwg):
        """

        Args:
            dwg: svgwrite (obj)

        Returns: Container for all svg elements

        """
        smarker = dwg.marker(insert=(8, 3), size=(30, 30), orient="auto")
        smarker.add(dwg.path(d=" M0,0 L3,3 L0,6 L8,3 L0,0", fill="black"))
        dwg.defs.add(smarker)
        return smarker

    def add_section_marker(self, dwg):
        """

        Args:
            dwg: svgwrite (obj)

        Returns: Container for all svg elements

        """
        section_marker = dwg.marker(insert=(0,5), size=(10, 10), orient="auto")
        section_marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill="blue", stroke="black"))
        dwg.defs.add(section_marker)
        return section_marker

    def add_e_marker(self, dwg):
        """

        Args:
            dwg: svgwrite (obj)

        Returns: Container for all svg elements

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

        """
        line["marker-start"] = s_arrow.get_funciri()

    def draw_end_arrow(self, line, e_arrow):
        """

        Args:
            line: end line marker
            e_arrow: end arrow

        Returns:

        """
        line["marker-end"] = e_arrow.get_funciri()

    def draw_faint_line(self, pt_one, pt_two, dwg):
        """

        Args:
            pt_one: first point
            pt_two: second point
            dwg: svgwrite (obj)

        Returns:

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

        """
        smarker = self.add_s_marker(dwg)
        emarker = self.add_e_marker(dwg)
        line_vector = pt2 - pt1               #[a, b]
        normal_vector = np.array([-line_vector[1], line_vector[0]])     #[-b, a]
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
            vector: vector

        Returns:

        """
        a = vector[0]
        b = vector[1]
        magnitude = math.sqrt(a*a + b*b)
        return vector/magnitude

    def draw_cross_section(self, dwg, pt_a, pt_b, text_pt, text):
        """

        Args:
            dwg: svgwrite (obj)
            pt_a: point A
            pt_b: point B
            text_pt: text point
            text: text message

        Returns:

        """
        line = dwg.add(dwg.line(pt_a, pt_b). stroke("black", width=2.5, linecap="square"))
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
        Returns:

        """
        smarker = self.add_s_marker(dwg)
        emarker = self.add_e_marker(dwg)
        u = pt_b - pt_a          #[a, b]
        u_unit = self.normalize(u)
        v_unit = np.array([-u_unit[1], u_unit[0]])       #[-b, a]

        A1 = pt_a + params["endlinedim"] * v_unit
        A2 = pt_a + params["endlinedim"] * (-v_unit)
        dwg.add(dwg.line(A1, A2).stroke("black", width=2.5, linecap="square"))

        B1 = pt_b + params["endlinedim"] * v_unit
        B2 = pt_a + params["endlinedim"] * (-v_unit)
        dwg.add(dwg.line(B1, B2). stroke("black",width=2.5, linecap="square"))

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

    def draw_oriented_arrow(self, dwg, point, theta, orientation, offset, textup, textdown):
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

        """
        #Right Up.
        theta = math.radians(theta)
        char_width = 16
        x_vector = np.array([1, 0])
        y_vector = np.array([0, 1])

        p1 = point
        length_A = offset/(math.sin(theta))

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
            text_point_up = p2 + 0.1 * length_B * (-label_vector) + text_offset * offset_vector
            text_point_down = p2 - 0.1 * length_B * label_vector - (text_offset + 15) * offset_vector
        elif orientation == "NW":
            text_point_up = p3 + 0.1 * length_B * (label_vector) + text_offset * offset_vector
            text_point_down = p3 - 0.1 * length_B * label_vector - (text_offset + 15) * offset_vector
        elif orientation == "SE":
            text_point_up = p2 + 0.1 * length_B * (-label_vector) + text_offset * offset_vector
            text_point_down = p2 - 0.1 * length_B * label_vector - (text_offset + 15) * offset_vector
        elif orientation == "SW":
            text_point_up = p3 + 0.1 * length_B * (label_vector) + text_offset * offset_vector
            text_point_down = p3 - 0.1 * length_B * label_vector - (text_offset + 15) * offset_vector

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill="none", stroke='black', stroke_width=2.5))

        emarker = self.add_e_marker(dwg)
        self.draw_start_arrow(line, emarker)

        dwg.add(dwg.text(textup, insert=text_point_up, fill='black', font_family='sans-serif', font_size=28))
        dwg.add(dwg.text(textdown, insert=text_point_down, fill='black', font_family='sans-serif', font_size=28))

        print "successful"

    def save_to_svg(self, filename, view):
        """

        Args:
            filename: path of the folder
            view: front, top, side views of drawings to be generated

        Returns:
            None

        Note:


        """
        cover_end_2d_front = CoverEnd2DFront(self)
        cover_end_2d_top = CoverEnd2DTop(self)
        cover_end_2d_side = CoverEnd2DSide(self)
        if view == "Front":
            cover_end_2d_front.call_CoverEnd_front(filename)
            # cairosvg.svg2png(file_obj=filename, write_to="F:\drawing\TFront.svg")
        elif view == "Top":
            cover_end_2d_top.call_CoverEnd_top(filename)
        elif view == "Side":
            cover_end_2d_side.call_CoverEnd_side(filename)
        else:
            # filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Cover_plate\TFront.svg"
            filename = "F:\drawing\TFront.svg"
            cover_end_2d_front.call_CoverEnd_front(filename)

class CoverEnd2DFront(object):
    """

    """
    def __init__(self, coverplate_common_object):

        self.data_object = coverplate_common_object
# --------------------------------------------------------------------------
        #                               FRONT VIEW
        # --------------------------------------------------------------------------
        # =========================  Cover Plate Middle  =========================
        ptW1x = ((self.data_object.beam_length_L1 + self.data_object.beam_length_L2 + self.data_object.gap_btwn_2beam) - self.data_object.plate_width_B3)/2
        ptW1y = (self.data_object.beam_depth_D1 - self.data_object.plate_length_L3)/2
        self.W1 = np.array([ptW1x, ptW1y])

        ptW2x = ptW1x + self.data_object.plate_width_B3
        ptW2y = ptW1y
        self.W2 = np.array([ptW2x, ptW2y])

        ptW3x = ptW2x
        ptW3y = ptW2y + self.data_object.plate_length_L3
        self.W3 = np.array([ptW3x, ptW3y])

        ptW4x = ptW1x
        ptW4y = ptW3y
        self.W4 = np.array([ptW4x, ptW4y])

        # ================ Primary Beam 1 ================

        ptA1x = 0
        ptA1y =0
        self.A1 = np.array([ptA1x, ptA1y])

        ptA2x = ptA1x + self.data_object.beam_length_L1
        ptA2y = 0
        self.A2 = np.array([ptA2x, ptA2y])

        ptA6x = ptA2x
        ptA6y = ptA2y + self.data_object.flange_thickness_T1
        self.A6 = np.array([ptA6x, ptA6y])

        ptA9x = ptA6x
        ptA9y = ptA2y + (self.data_object.beam_depth_D1 - self.data_object.plate_length_L3)/2
        self.A9 = np.array([ptA9x, ptA9y])

        ptA10x = ptA9x
        ptA10y = ptA9y + self.data_object.plate_length_L3
        self.A10 = np.array([ptA10x, ptA10y])

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
        ptA8y = ptA4y - self.data_object.flange_thickness_T1
        self.A8 = np.array([ptA8x, ptA8y])

        ptA5x = ptA1x
        ptA5y = self.data_object.flange_thickness_T1
        self.A5 = np.array([ptA5x, ptA5y])

        # =========================  Primary Beam 2  =========================
        ptAA1x = ptA2x + self.data_object.gap_btwn_2beam
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

        ptAA9x = ptAA5x
        ptAA9y = ptAA1y + (self.data_object.beam_depth_D2 - self.data_object.plate_length_L3) / 2
        self.AA9 = np.array([ptAA9x, ptAA9y])

        ptAA10x = ptAA9x
        ptAA10y = ptAA9y + self.data_object.plate_length_L3
        self.AA10 = np.array([ptAA10x, ptAA10y])

        # =========================  Cover Plate UP  =========================
        ptP1x = ptA1x + ((self.data_object.beam_length_L1 + self.data_object.beam_length_L2 + self.data_object.gap_btwn_2beam) - self.data_object.plate_length_L1)/2
        ptP1y = 0
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = ptP1x
        ptP2y = -(ptP1y + self.data_object.plate_thickness_p1)
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = ptP2x + self.data_object.plate_length_L1
        ptP3y = ptP2y
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP3x
        ptP4y = ptP1y
        self.P4 = np.array([ptP4x, ptP4y])

    # =========================  Cover Plate Down  =========================
        ptPP1x = ((self.data_object.beam_length_L1 + self.data_object.beam_length_L2 + self.data_object.gap_btwn_2beam) - self.data_object.plate_length_L1)/2
        ptPP1y = ( self.data_object.beam_depth_D1)
        self.PP1 = np.array([ptPP1x, ptPP1y])

        ptPP2x = ptPP1x
        ptPP2y = (ptPP1y + self.data_object.plate_thickness_p1)
        self.PP2 = np.array([ptPP2x, ptPP2y])

        ptPP3x = ptPP2x + self.data_object.plate_length_L1
        ptPP3y = ptPP2y
        self.PP3 = np.array([ptPP3x, ptPP3y])

        ptPP4x = ptPP3x
        ptPP4y = ptPP1y
        self.PP4 = np.array([ptPP4x, ptPP4y])

    def call_CoverEnd_front(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-330 -600 2840 1740'))      #230 = move towards left , 600= move towards down, 2840= width of view, 2340= height of view
        dwg.add(dwg.polyline(points=[ self.A10, self.A3, self.A4, self.A1, self.A2, self.A9], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.A5, self.A6).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.A8, self.A7).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.polyline(points=[self.AA9, self.AA1, self.AA2, self.AA3, self.AA4, self.AA10], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.AA5, self.AA6).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA8, self.AA7).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.line(self.A9, self.A10).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA9, self.AA10).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))

        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.PP1, self.PP2, self.PP3, self.PP4, self.PP1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.W1, self.W2, self.W3, self.W4, self.W1], stroke='blue', fill='none', stroke_width=2.5))

        # ------------------------------------------  Bolts Top Flange 1 -------------------------------------------
        btfc1 = self.data_object.bolts_top_flange1_col
        bolt_r = self.data_object.bolt_diameter/2

        pt_top_flange1_list = []
        if btfc1 >= 1:
            for i in range(btfc1):
                ptx = self.P1 + (self.data_object.edge_dist1 * np.array([1, 0])) - (self.data_object.flange_thickness_T1) * np.array([0, 1]) +\
                      i * self.data_object.pitch1 * np.array([1, 0])
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_diameter
                rect_length = self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 20) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_flange1_list.append(ptx)

                pt_Cx1 = ptx + 10 * np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 10) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_flange1_list.append(ptx)

            # ------------------------------------------  Bolts Top Flange 2 -------------------------------------------
            btfc2 = self.data_object.bolts_top_flange2_col
            bolt_r = self.data_object.bolt_diameter / 2

            pt_top_flange2_list = []
            if btfc2 >= 1:
                for i in range(btfc2):
                    ptx = self.P4 + (self.data_object.edge_dist1 * np.array([-1, 0])) - (self.data_object.flange_thickness_T1) * np.array([0, 1]) - \
                          i * self.data_object.pitch1 * np.array([1, 0])
                    ptx1 = ptx - bolt_r * np.array([1, 0])
                    rect_width = self.data_object.bolt_diameter
                    rect_length = self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1
                    dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black',
                                     stroke_width=2.5))

                    pt_Cx = ptx + np.array([0, -1])
                    pt_Dx = ptx + (rect_length - 20) * np.array([0, -1])
                    dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                    pt_top_flange2_list.append(ptx)

                    pt_Cx1 = ptx + 10 * np.array([0, 1])
                    pt_Dx1 = ptx + (rect_length + 10) * np.array([0, 1])
                    dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                    pt_top_flange2_list.append(ptx)

        # ------------------------------------------  Bolts Bottom Flange 1 -------------------------------------------
        bbfc1 = self.data_object.bolts_bottom_flange1_col
        pt_bottom_flange1_list = []
        if bbfc1 >= 1:
            for i in range(bbfc1):
                ptx = self.PP1 + ( self.data_object.edge_dist1 * np.array([1, 0])) - (self.data_object.flange_thickness_T1) * np.array([0, 1]) +\
                      i * self.data_object.pitch1 * np.array([1, 0]) #+ 20
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_diameter
                rect_length = self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 20) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_bottom_flange1_list.append(ptx)

                pt_Cx1 = ptx + 10 * np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 10) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_bottom_flange1_list.append(ptx)

            # ------------------------------------------  Bolts Bottom Flange 2 -------------------------------------------
            bbfc2 = self.data_object.bolts_bottom_flange2_col
            pt_bottom_flange2_list = []
            if bbfc2 >= 1:
                for i in range(bbfc2):
                    ptx = self.PP4 + (self.data_object.edge_dist1 * np.array([-1, 0])) - (self.data_object.flange_thickness_T1) * np.array([0, 1]) - \
                          i * self.data_object.pitch1 * np.array([1, 0])  # + 20
                    ptx1 = ptx - bolt_r * np.array([1, 0])
                    rect_width = self.data_object.bolt_diameter
                    rect_length = self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1
                    dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black',
                                     stroke_width=2.5))

                    pt_Cx = ptx + np.array([0, -1])
                    pt_Dx = ptx + (rect_length - 20) * np.array([0, -1])
                    dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                    pt_bottom_flange2_list.append(ptx)

                    pt_Cx1 = ptx + 10 * np.array([0, 1])
                    pt_Dx1 = ptx + (rect_length + 10) * np.array([0, 1])
                    dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                    pt_bottom_flange2_list.append(ptx)

        # ------------------------------------------  Bolts Inside Web-------------------------------------------
        biwc = self.data_object.bolts_inside_web_col
        biwr = self.data_object.bolts_inside_web_row

        pt_inside_column_list = []
        for i in range(1, (biwr + 1)):
            col_inside_list = []
            for j in range(1, (biwc + 1)):
                pt = self.W1 +(self.data_object.plate_length_L3 - self.data_object.end_dist) * np.array([0, 1]) + self.data_object.edge_dist2 * np.array([1, 0]) + \
                     (i - 1) * self.data_object.pitch2 * np.array([0, -1]) + (j - 1) * self.data_object.cross_centre_gauge_dist * np.array([1, 0])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_inside_list.append(pt)
            pt_inside_column_list.append(col_inside_list)

        # ------------------------------------------  Faint line for top bolts left -------------------------------------------
        ptx1 = self.P2
        pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_top_flange1_list[0])
        pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + (self.data_object.edge_dist1) * np.array([-1, 0])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.edge_dist1), params)
        # -------------------------------------------------------------------------------------------

        ptxx2 = np.array(pt_top_flange1_list[1]) + self.data_object.pitch1 * np.array([1, 0])
        ptyy2 = ptxx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

        point2 = ptxx2 + (self.data_object.pitch1 ) * np.array([-1, 0])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptxx2, point2, str(self.data_object.pitch1), params)

        # ------------------------------------------  Faint line for top bolts right  -------------------------------------------
        ptx1 = self.P3
        pty1 = ptx1 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_top_flange2_list[0])
        pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + (self.data_object.edge_dist1) * np.array([1, 0])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.edge_dist1), params)
        # ----------------------------------------------------------------------------------------------------------------------------------------

        ptxx2 = np.array(pt_top_flange2_list[1]) + self.data_object.pitch1 * np.array([-1, 0])
        ptyy2 = ptxx2 + (self.data_object.beam_width_B2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

        point2 = ptxx2 + (self.data_object.pitch1) * np.array([1, 0])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptxx2, point2, str(self.data_object.pitch1), params)

        # ------------------------------------------  Faint line for bolts inside web   -------------------------------------------
        ptx1 = np.array(pt_inside_column_list[2][0])
        pty1 = ptx1 + (self.data_object.beam_depth_D1 + self.data_object.plate_length_L3 )/2 * np.array([0, -1])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_inside_column_list[2][1])
        pty2 = ptx2 + ( (self.data_object.beam_depth_D1 + self.data_object.plate_length_L3 )/2) * np.array([0, -1])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + (self.data_object.cross_centre_gauge_dist) * np.array([-1, 0])
        params = {"offset": ( (self.data_object.beam_depth_D1 + self.data_object.plate_length_L3 )/2), "textoffset": 10, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.cross_centre_gauge_dist), params)

        # ----------------------------------------------------------------------------------------------------------------------------------------
        ptxx1 = np.array(pt_inside_column_list[2][1])
        ptyy1 = ptxx1 + (self.data_object.beam_length_L2) * np.array([1, 0])
        self.data_object.draw_faint_line(ptxx1, ptyy1, dwg)

        ptxx2 = ptxx1 + self.data_object.pitch2 * np.array([0, 1])
        ptyy2 = ptxx2 + (self.data_object.beam_length_L2) * np.array([1, 0])
        self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

        point3 = ptxx2 + (self.data_object.pitch2) * np.array([0, -1])
        params = {"offset": (self.data_object.beam_length_L2), "textoffset": 10, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptxx2, point3, str(self.data_object.pitch2), params)
        # ----------------------------------------------------------------------------------------------------------------------------------------

        pta1 = self.W2
        ptb1 = pta1 + (self.data_object.beam_length_L2) * np.array([1, 0])
        self.data_object.draw_faint_line(pta1, ptb1,dwg)

        point4 = pta1 + (self.data_object.end_dist) * np.array([0, 1])
        params = {"offset": (self.data_object.beam_length_L2), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pta1, point4, str(self.data_object.end_dist), params)

        # ------------------------------------------  Beam 1& 2 -------------------------------------------
        point = self.A1 + (self.data_object.beam_length_L1 /4) * np.array([1, 0])
        theta = 60
        offset = 50
        textup = "Beam " + str(self.data_object.beam_length_L1) + " x " + str(self.data_object.beam_width_B1) + " x " + str(self.data_object.flange_thickness_T1)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown)

        point = self.AA2 + (self.data_object.beam_length_L2 / 4) * np.array([-1, 0])
        theta = 60
        offset = 50
        textup = "Beam " + str(self.data_object.beam_length_L2) + " x " + str(self.data_object.beam_width_B2) + " x " + str(self.data_object.flange_thickness_T2)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)

        # ------------------------------------------  Plate 1, 2 & 3-------------------------------------------
        point = self.P2
        theta = 60
        offset = 100
        textup = "Flange splice " + str(self.data_object.plate_length_L1) + " x " + str(self.data_object.plate_width_B1) + " x " + str(self.data_object.plate_thickness_p1)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown)

        point = self.PP2
        theta = 60
        offset = 100
        textdown = "Flange splice " + str(self.data_object.plate_length_L2) + " x " + str(self.data_object.plate_width_B2) + " x " + str(self.data_object.plate_thickness_p2)
        textup = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown)

        point = self.W2
        theta = 60
        offset = 200
        textup = "Web splice " + str(self.data_object.plate_length_L3) + " x " + str(self.data_object.plate_width_B3) + " x " + str(self.data_object.plate_thickness_p3)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)


        # ------------------------------------------  View details-------------------------------------------
        ptx = self.PP2 + 100 * np.array([1, 0]) + 200 * np.array([0, 1])
        dwg.add(dwg.text('Front view (Sec C-C) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = ptx + 40 * np.array([0, 1])
        dwg.add(dwg.text('(All distances are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))


        dwg.save()


class CoverEnd2DTop(object):
    """

    """
    def __init__(self, coverplate_common_object):

        self.data_object = coverplate_common_object
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

        ptA8x = ptA2x
        ptA8y = ptA7y + self.data_object.web_thickness_tw1
        self.A8 = np.array([ptA8x, ptA8y])

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

        # ====================== Primary Beam 2  =====================
        ptAA1x = ptA2x + self.data_object.gap_btwn_2beam
        ptAA1y = 0
        self.AA1 = np.array([ptAA1x, ptAA1y])

        ptAA2x = ptAA1x + self.data_object.beam_length_L2
        ptAA2y = 0
        self.AA2 = np.array([ptAA2x, ptAA2y])

        ptAA7x = ptAA2x
        ptAA7y = ptAA2y + (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2)/2
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
        ptAA5y =  ptAA4y - (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2)/2
        self.AA5 = np.array([ptAA5x, ptAA5y])

        ptAA6x = ptAA1x
        ptAA6y = ptAA5y - self.data_object.web_thickness_tw2
        self.AA6 = np.array([ptAA6x, ptAA6y])

        # =========================  Cover Plate UP  =========================
        ptP1x = ptA1x + ((self.data_object.beam_length_L1 + self.data_object.beam_length_L2 + self.data_object.gap_btwn_2beam) - self.data_object.plate_length_L1)/2
        ptP1y = 0
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = ptP1x + self.data_object.plate_length_L1
        ptP2y = 0
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = ptP2x
        ptP3y = ptP2y + self.data_object.plate_width_B1
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP1x
        ptP4y = ptP3y
        self.P4 = np.array([ptP4x, ptP4y])


    def call_CoverEnd_top(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-400 -700 3000 1500' ))
        dwg.add(dwg.line(self.A5, self.A8).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.A6, self.A7).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.A2, self.A3).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.polyline(points=[self.A3, self.A4, self.A1, self.A2, ], stroke='blue', fill='none', stroke_width=2.5))

        dwg.add(dwg.line(self.AA5, self.AA8).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA6, self.AA7).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.line(self.AA1, self.AA4).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[5, 5]))
        dwg.add(dwg.polyline(points=[self.AA1, self.AA2, self.AA3, self.AA4], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width=2.5))

        # ------------------------------------------  Bolts Top Flange 1 -------------------------------------------
        btfc1 = self.data_object.bolts_top_flange1_col
        btofr1 = self.data_object.bolts_top_of_flange1_row
        bolt_r = self.data_object.bolt_diameter/2

        pt_outside_topflange1_list = []
        for i in range(1, (btfc1 +1)):
            col_outside_toflange1_list = []
            for j in range(1, (btofr1 + 1)):
                pt = self.P1 + ( self.data_object.edge_dist1) * np.array([1, 0]) + (self.data_object.plate_width_B1 - self.data_object.gauge)/2 * np.array([0, 1]) + \
                     (i - 1) * self.data_object.pitch1 * np.array([1, 0]) + (j - 1) * self.data_object.gauge * np.array([0, 1])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_outside_toflange1_list.append(pt)
            pt_outside_topflange1_list.append(col_outside_toflange1_list)

        # ------------------------------------------  Bolts Top Flange 2 -------------------------------------------
        btfc2 = self.data_object.bolts_top_flange2_col
        btofr2 = self.data_object.bolts_top_of_flange2_row
        bolt_r = self.data_object.bolt_diameter/2

        pt_outside_topflange2_list = []
        for i in range(1, (btfc2 +1)):
            col_outside_toflange2_list = []
            for j in range(1, (btofr2 + 1)):
                pt = self.P2 + ( self.data_object.edge_dist1) * np.array([-1, 0]) + (self.data_object.plate_width_B2 - self.data_object.gauge)/2 * np.array([0, 1]) - \
                     (i - 1) * self.data_object.pitch1 * np.array([1, 0]) + (j - 1) * self.data_object.gauge * np.array([0, 1])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_outside_toflange2_list.append(pt)
            pt_outside_topflange2_list.append(col_outside_toflange2_list)

        # ------------------------------------------  Faint line for top bolts left   -------------------------------------------
        ptx1 = np.array(pt_outside_topflange1_list[0][0])
        pty1 = ptx1 + (self.data_object.beam_length_L1 - 50) * np.array([-1, 0])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_outside_topflange1_list[0][1])
        pty2 = ptx2 +(self.data_object.beam_length_L1- 50) * np.array([-1, 0])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + (self.data_object.gauge) * np.array([0, -1])
        params = {"offset": (self.data_object.beam_length_L1- 50), "textoffset": 40, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.gauge), params)

        # ------------------------------------------  End, pitch -------------------------------------------
        ptxx1 = np.array(pt_outside_topflange1_list[0][0])
        ptyy1 = ptxx1 + (self.data_object.plate_length_L1/2) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx1, ptyy1, dwg)

        ptxx2 = np.array(pt_outside_topflange1_list[1][0])
        ptyy2 = ptxx2 + (self.data_object.plate_length_L1/2) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

        point2 = ptxx1 + (self.data_object.pitch1) * np.array([1, 0])
        params = {"offset": (self.data_object.plate_length_L1/2), "textoffset": 40, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptxx1, point2, str(self.data_object.pitch1), params)

        # ---------------------------------------------------------------------------------------------------------------------------
        pta1 = self.P1
        ptb1 = pta1 + (self.data_object.plate_length_L1 / 2) * np.array([0, -1])
        self.data_object.draw_faint_line(pta1, ptb1, dwg)

        point21 = pta1 + (self.data_object.edge_dist1) * np.array([1, 0])
        params = {"offset": (self.data_object.plate_length_L1 / 2), "textoffset": 40, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pta1, point21, str(self.data_object.edge_dist1), params)

        # ------------------------------------------  Faint line for top bolts right   -------------------------------------------
        ptx1 = np.array(pt_outside_topflange2_list[0][0])
        pty1 = ptx1 + (self.data_object.beam_length_L1- 50) * np.array([1, 0])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_outside_topflange2_list[0][1])
        pty2 = ptx2 +(self.data_object.beam_length_L1- 50) * np.array([1, 0])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point3 = ptx2 + (self.data_object.gauge) * np.array([0, -1])
        params = {"offset": (self.data_object.beam_length_L1- 50), "textoffset": 10, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point3, str(self.data_object.gauge), params)

        # ------------------------------------------  End, pitch -------------------------------------------
        ptxx1 = np.array(pt_outside_topflange2_list[0][0])
        ptyy1 = ptxx1 + (self.data_object.plate_length_L1/2) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx1, ptyy1, dwg)

        ptxx2 = np.array(pt_outside_topflange2_list[1][0])
        ptyy2 = ptxx2 + (self.data_object.plate_length_L1/2) * np.array([0, -1])
        self.data_object.draw_faint_line(ptxx2, ptyy2, dwg)

        point4 = ptxx1 + (self.data_object.pitch1) * np.array([-1, 0])
        params = {"offset": (self.data_object.plate_length_L1/2), "textoffset": 40, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptxx1, point4, str(self.data_object.pitch1), params)

        # ---------------------------------------------------------------------------------------------------------------------------
        pta2 = self.P2
        ptb2 = pta2 + (self.data_object.plate_length_L1 / 2) * np.array([0, -1])
        self.data_object.draw_faint_line(pta2, ptb2, dwg)

        point31 = pta2 + (self.data_object.edge_dist1) * np.array([-1, 0])
        params = {"offset": (self.data_object.plate_length_L1 / 2), "textoffset": 40, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pta2, point31, str(self.data_object.edge_dist1), params)

        # ------------------------------------------  Primary Beam 1& 2 -------------------------------------------
        point = self.A1 + (self.data_object.beam_length_L1 / 4 )* np.array([1, 0])
        theta = 60
        offset = 50
        textup = "Beam " + str(self.data_object.beam_length_L1) + " x " + str(self.data_object.beam_width_B1) + " x " + str(self.data_object.flange_thickness_T1)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown)

        point = self.AA2 + (self.data_object.beam_length_L2 / 4) * np.array([-1, 0])
        theta = 60
        offset = 50
        textup = "Beam " + str(self.data_object.beam_length_L2) + " x " + str(self.data_object.beam_width_B2) + " x " + str(self.data_object.flange_thickness_T2)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)

        # ------------------------------------------  End Plate 1 & 2 -------------------------------------------
        point = self.P1 + (40 * np.array([0, 1]))
        theta = 60
        offset = 160
        textup = "Flange cover plate " + str(self.data_object.plate_length_L1) + " x " + str(self.data_object.plate_width_B1) + " x " + str(self.data_object.plate_thickness_p1)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown)

        # ------------------------------------------  Bolts details -------------------------------------------
        no_of_bolts_flange = self.data_object.bolts_top_flange1_col * self.data_object.bolts_top_of_flange1_row
        point =  np.array(pt_outside_topflange1_list[1][1])
        theta = 60
        offset = 120
        textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
        textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(self.data_object.bolt_type) + " (grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown)

        no_of_bolts_flange = self.data_object.bolts_top_flange2_col * self.data_object.bolts_top_of_flange2_row
        point =  np.array(pt_outside_topflange2_list[1][1])
        theta = 60
        offset = 120
        textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
        textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(self.data_object.bolt_type) + " (grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SE", offset, textup, textdown)

        # ------------------------------------------  View details -------------------------------------------
        ptx = self.P4 + 100 * np.array([1, 0]) + 300 * np.array([0, 1])
        dwg.add(dwg.text('Top view (Sec A-A) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = ptx + 40 * np.array([0, 1])
        dwg.add(dwg.text('(All distances are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))

        dwg.save()


class CoverEnd2DSide(object):
    """

    """
    def __init__(self, coverplate_common_object):

        self.data_object = coverplate_common_object
        # ----------------------------------------------------------------------------------------------------
        #                                                   SIDE VIEW
        # ----------------------------------------------------------------------------------------------------
        # =========================  Primary Beam 2  =========================
        ptA1x = 0
        ptA1y = 0
        self.A1 = np.array([ptA1x, ptA1y])

        ptA2x = self.data_object.beam_width_B2
        ptA2y = ptA1y
        self.A2 = np.array([ptA2x, ptA2y])

        ptA3x = ptA2x
        ptA3y = ptA2y + self.data_object.flange_thickness_T2
        self.A3 = np.array([ptA3x, ptA3y])

        ptA12x = ptA1x
        ptA12y = ptA1y + self.data_object.flange_thickness_T2
        self.A12 = np.array([ptA12x, ptA12y])

        ptA4x = ptA12x + (self.data_object.beam_width_B2 + self.data_object.web_thickness_tw2)/2
        ptA4y = ptA3y
        self.A4 = np.array([ptA4x, ptA4y])

        ptA8x = ptA1x
        ptA8y = ptA1y + self.data_object.beam_depth_D1
        self.A8 = np.array([ptA8x, ptA8y])

        ptA9x = ptA8x
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

        ptA11x = ptA12x + (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2)/2
        ptA11y = ptA12y
        self.A11 = np.array([ptA11x, ptA11y])

        ptA10x = ptA11x
        ptA10y = ptA9y
        self.A10 = np.array([ptA10x, ptA10y])

        # =========================  Cover Plate Top  =========================
        ptP1x = ptA1x
        ptP1y = ptA1y
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = ptP1x
        ptP2y = -(ptA1y + self.data_object.plate_thickness_p1)
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = ptP2x + self.data_object.plate_width_B1
        ptP3y = ptP2y
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP3x
        ptP4y = ptP1y
        self.P4 = np.array([ptP4x, ptP4y])

        # =========================  Cover Plate Bottom  =========================
        ptPP1x = ptA8x
        ptPP1y = ptA8y
        self.PP1 = np.array([ptPP1x, ptPP1y])

        ptPP2x = ptPP1x
        ptPP2y = ptPP1y + self.data_object.plate_thickness_p2
        self.PP2 = np.array([ptPP2x, ptPP2y])

        ptPP3x = ptPP2x + self.data_object.plate_width_B2
        ptPP3y = ptPP2y
        self.PP3 = np.array([ptPP3x, ptPP3y])

        ptPP4x = ptPP3x
        ptPP4y = ptPP1y
        self.PP4 = np.array([ptPP4x, ptPP4y])

        # =========================  Cover Plate Middle left  =========================
        ptW1x = ptA1x + (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2)/2
        ptW1y = (self.data_object.beam_depth_D2 - self.data_object.plate_length_L3)/2
        self.W1 = np.array([ptW1x, ptW1y])

        ptW2x = (ptW1x - self.data_object.plate_thickness_p3)
        ptW2y = ptW1y
        self.W2 = np.array([ptW2x, ptW2y])

        ptW3x = ptW2x
        ptW3y = ptW2y + self.data_object.plate_length_L3
        self.W3 = np.array([ptW3x, ptW3y])

        ptW4x = ptW3x + self.data_object.plate_thickness_p3
        ptW4y = ptW3y
        self.W4 = np.array([ptW4x, ptW4y])

        #  =========================  Cover Plate Middle right  =========================
        ptWW1x = ptA1x + (self.data_object.beam_width_B2 + self.data_object.web_thickness_tw2)/2
        ptWW1y = (self.data_object.beam_depth_D2 - self.data_object.plate_length_L3) / 2
        self.WW1 = np.array([ptWW1x, ptWW1y])

        ptWW2x = (ptWW1x + self.data_object.plate_thickness_p3)
        ptWW2y = ptWW1y
        self.WW2 = np.array([ptWW2x, ptWW2y])

        ptWW3x = ptWW2x
        ptWW3y = ptWW2y + self.data_object.plate_length_L3
        self.WW3 = np.array([ptWW3x, ptWW3y])

        ptWW4x = (ptWW3x - self.data_object.plate_thickness_p3)
        ptWW4y = ptWW3y
        self.WW4 = np.array([ptWW4x, ptWW4y])

        ptQx = (self.data_object.beam_width_B2 - self.data_object.web_thickness_tw2)/2
        ptQy = 0
        self.Q = np.array([ptQx, ptQy])

    def call_CoverEnd_side(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-700 -400 1500 1400'))
        dwg.add(dwg.polyline(points=[self.A1, self.A2, self.A3, self.A4, self.A5, self.A6, self.A7, self.A8, self.A9, self.A10, self.A11,
                    self.A12, self.A1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.PP1, self.PP2, self.PP3, self.PP4, self.PP1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.W1, self.W2, self.W3, self.W4], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.WW1, self.WW2, self.WW3, self.WW4], stroke='blue', fill='none', stroke_width=2.5))

        btofc1 = self.data_object.bolts_top_of_flange1_row
        bolt_r = self.data_object.bolt_diameter / 2
        # ------------------------------------------  Bolts Top Flange -------------------------------------------
        pt_top_flange_list = []
        if btofc1 >= 1:
            for i in range(btofc1):
                ptx = self.P1 + ((self.data_object.beam_width_B2 -self.data_object.gauge)/2 * np.array([1, 0])) -\
                      (self.data_object.flange_thickness_T1) * np.array([0, 1]) +\
                      i * self.data_object.gauge * np.array([1, 0])
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_diameter
                rect_length = self.data_object.plate_thickness_p1 + self.data_object.flange_thickness_T1
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 20) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_flange_list.append(ptx)

                pt_Cx1 = ptx + 10 * np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 10) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_flange_list.append(ptx)

        # ------------------------------------------  Bolts Inside Web  -------------------------------------------
            biwr = self.data_object.bolts_inside_web_row
            pt_inside_column_list = []
            for i in range(1, (biwr + 1)):
                ptx = self.W4 + ((self.data_object.beam_depth_D2 - self.data_object.plate_length_L3)/2 -  self.data_object.end_dist) * np.array([0, 1]) -\
                      (self.data_object.plate_thickness_p3) * np.array([1, 0]) + (i * self.data_object.pitch2) * np.array([0, -1])

                ptx1 = ptx - bolt_r * np.array([0, 1])
                rect_width = self.data_object.bolt_diameter
                rect_length = (2 * self.data_object.plate_thickness_p3) + self.data_object.web_thickness_tw2
                dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx + np.array([1, 0])
                pt_Dx = ptx + (rect_length + 20) * np.array([1, 0])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_inside_column_list.append(ptx)

                pt_Cx1 = ptx + np.array([-1, 0])
                pt_Dx1 = ptx + (rect_length - 20) * np.array([-1, 0])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_inside_column_list.append(ptx)

        # ------------------------------------------  Bolts Bottom Flange -------------------------------------------
        pt_bottom_flange_list = []
        if btofc1 >= 1:
            for i in range(btofc1):
                ptx = self.PP1 + ((self.data_object.beam_width_B2 -self.data_object.gauge)/2 * np.array([1, 0])) - (self.data_object.flange_thickness_T1) * np.array([0, 1]) +\
                      i * self.data_object.gauge * np.array([1, 0]) #+ 20
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_diameter
                rect_length = self.data_object.plate_thickness_p2 + self.data_object.flange_thickness_T2
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 20) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_bottom_flange_list.append(ptx)

                pt_Cx1 = ptx + 10 * np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 10) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_bottom_flange_list.append(ptx)

        # ------------------------------------------  Faint line for top bolts left   -------------------------------------------
        ptx1 = np.array(pt_top_flange_list[0])
        pty1 = ptx1 + self.data_object.beam_width_B2 * np.array([0, -1])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_top_flange_list[0]) + self.data_object.gauge * np.array([1, 0])
        pty2 = ptx2 + (self.data_object.beam_width_B2 ) * np.array([0, -1])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + self.data_object.gauge * np.array([-1, 0])
        params = {"offset": (self.data_object.beam_width_B2), "textoffset": 10, "lineori": "right",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.gauge), params)

        # ------------------------------------------  Faint line for web  -------------------------------------------
        ptx1 = self.WW3
        pty1 = ptx1 + self.data_object.beam_width_B2 * np.array([1, 0])
        self.data_object.draw_faint_line(ptx1, pty1, dwg)

        ptx2 = np.array(pt_inside_column_list[0])
        pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + self.data_object.edge_dist2 * np.array([0, 1])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.edge_dist2), params)
        # -------------------------------------------------------------------------------------------

        ptx2 = np.array(pt_inside_column_list[0]) + self.data_object.pitch2 * np.array([0, -1])
        pty2 = ptx2 + (self.data_object.beam_width_B2 + 50) * np.array([1, 0])
        self.data_object.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 + self.data_object.pitch2 * np.array([0, 1])
        params = {"offset": (self.data_object.beam_width_B2 + 50), "textoffset": 10, "lineori": "left",
                  "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.data_object.pitch2), params)

        # ------------------------------------------  Labeling  top bolt of flange -------------------------------------------
        no_of_bolts_flange = self.data_object.bolts_top_flange1_col * self.data_object.bolts_top_of_flange1_row
        point = np.array(pt_top_flange_list[0])
        theta = 60
        offset = 50
        textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
        textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(
            self.data_object.bolt_type) + " (grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown)

        # ------------------------------------------  Labeling  Inside bolt of web -------------------------------------------
        no_of_bolts_flange = self.data_object.bolts_inside_web_col * self.data_object.bolts_inside_web_row
        point = np.array(pt_inside_column_list[0])
        theta = 60
        offset = 50
        textup = str(no_of_bolts_flange) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"
        textdown = "for M" + str(self.data_object.bolt_diameter) + " " + str(
            self.data_object.bolt_type) + " (grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown)

        # ------------------------------------------  Web Splice -------------------------------------------
        point = self.WW2
        theta = 50
        offset = 40
        textup = "Web Splice " + str(self.data_object.plate_length_L3) + " x "+ str(self.data_object.plate_width_B3) + " x " + str(self.data_object.plate_thickness_p3)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)

        # ------------------------------------------  Flange Splice -------------------------------------------
        point = self.P3
        theta = 70
        offset = 40
        textup = "Flange Splice " + str(self.data_object.plate_length_L1) + " x " + str(
            self.data_object.plate_width_B1) + " x " + str(self.data_object.plate_thickness_p1)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)

        # ------------------------------------------  View details-------------------------------------------
        ptx = self.PP2 * np.array([0, 1]) + 200 * np.array([0, 1]) + 60 * np.array([-1, 0])
        dwg.add(dwg.text('Side view (Sec B-B) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = ptx + 40 * np.array([0, 1])
        dwg.add(dwg.text('(All distances are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

