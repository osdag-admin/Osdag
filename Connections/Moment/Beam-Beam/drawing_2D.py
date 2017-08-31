'''
Created on 24-Aug-2017

@author: reshma
'''
from numpy import math
import svgwrite
import cairosvg
import numpy as np
import os


class ExtendedEndPlate(object):
    def __init__(self):
        # self.filename = filename
        self.length_L1 = 500
        self.length_L2 = 500
        self.depth_D1 = 300
        self.depth_D2 = 300
        self.width_B1 = 150
        self.width_B2 = 150
        self.plate_thickness_p1 = 30
        self.plate_thickness_p2 = 30
        self.plate_width_B1 = 150
        self.plate_width_B2 = 150
        self.plate_length_L1 = 500
        self.plate_length_L2 = 500
        self.flange_thickness_T1 = 20
        self.flange_thickness_T2 = 20
        self.web_thickness_tw1 = 40
        self.web_thickness_tw2 = 40
        self.flange_weld_thickness = 12
        self.web_weld_thickness = 16

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
            text_point_up = p2 + 0.2 * length_B * (-label_vector) + text_offset * offset_vector
            text_point_down = p2 - 0.2 * length_B * label_vector - (text_offset + 15) * offset_vector
        elif orientation == "NW":
            text_point_up = p3 + 0.2 * length_B * (label_vector) + text_offset * offset_vector
            text_point_down = p3 - 0.2 * length_B * label_vector - (text_offset + 15) * offset_vector
        elif orientation == "SE":
            text_point_up = p2 + 0.2 * length_B * (-label_vector) + text_offset * offset_vector
            text_point_down = p2 - 0.2 * length_B * label_vector - (text_offset + 15) * offset_vector
        elif orientation == "SW":
            text_point_up = p3 + 0.2 * length_B * (label_vector) + text_offset * offset_vector
            text_point_down = p3 - 0.2 * length_B * label_vector - (text_offset + 15) * offset_vector

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill="None", stroke='black', stroke_width=2.5))

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
        extnd_bothway_end_2d_front = ExtendedEnd2DFront(self)
        extnd_bothway_end_2d_top = ExtendedEnd2DTop(self)
        extnd_bothway_end_2d_side = ExtendedEnd2DSide(self)
        if view == "Front":
            extnd_bothway_end_2d_front.call_ExtndBoth_front(filename)
            # cairosvg.svg2png(file_obj=filename, write_to="D:\PyCharmWorkspace\Osdag\Connections\Moment\Beam-Beam")
        elif view == "Side":
            extnd_bothway_end_2d_side.call_ExtndBoth_side(filename)
        elif view == "Top":
            extnd_bothway_end_2d_top.call_ExtndBoth_top(filename)
        # else:
        #     filename = "D:\PyCharmWorkspace\Osdag\Connections\Moment\Beam-Beam\Front.svg"
        #     extnd_bothway_end_2d_front.call_ExtndBoth_front(filename)


class ExtendedEnd2DFront(object):
    """
    Contains functions for generating the front view of the Extended bothway endplate
     connection.
    """
    def __init__(self, extnd_common_object):
        self.data_object = extnd_common_object

        # --------------------------------------------------------------------------
        #                               FRONT VIEW
        # --------------------------------------------------------------------------
        # ================ Primary Beam 1 ================

        ptA1x = 0
        ptA1y =0
        self.A1 = np.array([ptA1x, ptA1y])

        ptA2x = self.data_object.length_L1
        ptA2y = 0
        self.A2 = np.array([ptA2x, ptA2y])

        ptA6x = self.data_object.length_L1
        ptA6y = self.data_object.flange_thickness_T1
        self.A6 = np.array([ptA6x, ptA6y])

        ptA7x = self.data_object.length_L1
        ptA7y = (self.data_object.depth_D1 - self.data_object.flange_thickness_T1)
        self.A7 = np.array([ptA7x, ptA7y])

        ptA3x = self.data_object.length_L1
        ptA3y = self.data_object.depth_D1
        self.A3 = np.array([ptA3x, ptA3y])

        ptA4x = 0
        ptA4y = self.data_object.depth_D1
        self.A4 = np.array([ptA4x, ptA4y])

        ptA8x = 0
        ptA8y = (self.data_object.depth_D1 - self.data_object.flange_thickness_T1)
        self.A8 = np.array([ptA8x, ptA8y])

        ptA5x = 0
        ptA5y = self.data_object.flange_thickness_T1
        self.A5 = np.array([ptA5x, ptA5y])

        # =========================  End Plate 1  =========================

        ptP1x = self.data_object.length_L1
        ptP1y = -(self.data_object.plate_length_L1 - self.data_object.depth_D1)/2
        self.P1 = np.array([ptP1x, ptP1y])

        ptP2x = (self.data_object.length_L1 + self.data_object.plate_thickness_p1)
        ptP2y = ptP1y
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x =  ptP2x
        ptP3y = (self.data_object.plate_length_L1 + self.data_object.depth_D1)/2
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP1x
        ptP4y = ptP3y
        self.P4 = np.array([ptP4x, ptP4y])

        self.B3 = self.A2 
        self.B1 = self.B3 + 2.5 * np.array([0, 1]) + 2.5 * np.array([0, 1])
        self.B2 = self.B3 + 2.5 * np.array([-1, 0])+ 2.5 * np.array([-1, 0])  #+ self.data_object.flange_weld_thickness * np.array([-1, 0])

        # =========================  End Plate 2  =========================

        ptPP1x = (self.data_object.length_L1 + self.data_object.plate_thickness_p1)
        ptPP1y = -(self.data_object.plate_length_L2 - self.data_object.depth_D2)/2
        self.PP1 = np.array([ptPP1x, ptPP1y])

        ptPP2x = ptPP1x + self.data_object.plate_thickness_p2
        ptPP2y = ptPP1y
        self.PP2 = np.array([ptPP2x, ptPP2y])

        ptPP3x = ptPP2x
        ptPP3y =  (self.data_object.plate_length_L2 + self.data_object.depth_D2)/2
        self.PP3 = np.array([ptPP3x, ptPP3y])

        ptPP4x = ptPP1x
        ptPP4y = ptPP3y
        self.PP4 = np.array([ptPP4x, ptPP4y])

        # =========================  Primary Beam 2  =========================

        ptAA1x = self.data_object.length_L1 + self.data_object.plate_thickness_p1 + self.data_object.plate_thickness_p2
        ptAA1y = 0
        self.AA1 = np.array([ptAA1x, ptAA1y])

        ptAA2x = ptAA1x + self.data_object.plate_length_L2
        ptAA2y = 0
        self.AA2 = np.array([ptAA2x, ptAA2y])

        ptAA6x = ptAA2x
        ptAA6y = self.data_object.flange_thickness_T2
        self.AA6 = np.array([ptAA6x, ptAA6y])

        ptAA7x = ptAA2x
        ptAA7y = (self.data_object.depth_D2 - self.data_object.flange_thickness_T2)
        self.AA7 = np.array([ptAA7x, ptAA7y])

        ptAA3x = ptAA2x
        ptAA3y = self.data_object.depth_D2
        self.AA3 = np.array([ptAA3x, ptAA3y])

        ptAA4x = ptAA1x
        ptAA4y = self.data_object.depth_D2
        self.AA4 = np.array([ptAA4x, ptAA4y])

        ptAA8x = ptAA1x
        ptAA8y = (self.data_object.depth_D2 - self.data_object.flange_thickness_T2)
        self.AA8 = np.array([ptAA8x, ptAA8y])

        ptAA5x = ptAA1x
        ptAA5y = self.data_object.flange_thickness_T2
        self.AA5 = np.array([ptAA5x, ptAA5y])

    def call_ExtndBoth_front(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-200 -600 1500 1700'))
        dwg.add(dwg.polyline(points=[self.A1, self.A2, self.A3, self.A4, self.A1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.A5, self.A6).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.A8, self.A7).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.polyline(points=[self.P1, self.P2, self.P3, self.P4, self.P1], stroke='blue', fill='none', stroke_width='2.5'))
        dwg.add(dwg.polyline(points=[self.PP1, self.PP2, self.PP3, self.PP4, self.PP1], stroke='blue', fill='none', stroke_width=2.5))

        dwg.add(dwg.polyline(points=[self.B1, self.B3, self.B2, self.B1], stroke='black', fill='black', stroke_width=2.5))

        dwg.add(dwg.polyline(points=[self.AA1, self.AA2, self.AA3, self.AA4, self.AA1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.AA5, self.AA6).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.AA8, self.AA7).stroke('blue', width=2.5, linecap='square'))

        dwg.save()





class ExtendedEnd2DTop(object):
    """

    """
    def __init__(self, extnd_common_object):
        self.data_object = extnd_common_object
        # -------------------------------------------------------------------------------------------------
        #                                           TOP VIEW
        # -------------------------------------------------------------------------------------------------
        # ====================== Primary Beam 1  =====================

        self.A1 = np.array([0, 0])

        ptA5x = (self.data_object.width_B1 - self.data_object.web_thickness_tw1)/2
        ptA5y = 0
        self.A5 = np.array([ptA5x, ptA5y])

        ptA6x = (self.data_object.width_B1 + self.data_object.web_thickness_tw1)/2
        ptA6y = 0
        self.A6 = np.array([ptA6x, ptA6y])

        ptA2x = self.data_object.width_B1
        ptA2y = 0
        self.A2 = np.array([ptA2x, ptA2y])

        ptA3x = ptA2x
        ptA3y = self.data_object.length_L1
        self.A3 = np.array([ptA3x, ptA3y])

        ptA7x = ptA6x
        ptA7y = self.data_object.length_L1
        self.A7 = np.array([ptA7x, ptA7y])

        ptA8x =ptA5x
        ptA8y = self.data_object.length_L1
        self.A8 = np.array([ptA8x, ptA8y])

        ptA4x = 0
        ptA4y = self.data_object.length_L1
        self.A4 = np.array([ptA4x, ptA4y])

        # ====================== End Plate 1  =====================
        ptP2x = 0
        ptP2y = self.data_object.length_L1
        self.P2 = np.array([ptP2x, ptP2y])

        ptP3x = self.data_object.plate_width_B1
        ptP3y = self.data_object.length_L1
        self.P3 = np.array([ptP3x, ptP3y])

        ptP4x = ptP3x
        ptP4y = (self.data_object.length_L1 + self.data_object.plate_thickness_p1)
        self.P4 = np.array([ptP4x, ptP4y])

        ptP1x = 0
        ptP1y = (self.data_object.length_L1 + self.data_object.plate_thickness_p1)
        self.P1 = np.array([ptP1x, ptP1y])

        # ====================== End Plate 2  =====================
        ptPP2x = 0
        ptPP2y = ptP1y
        self.PP2 = np.array([ptPP2x, ptPP2y])

        ptPP3x = self.data_object.plate_width_B2
        ptPP3y = ptP4y
        self.PP3 = np.array([ptPP3x, ptPP3y])

        ptPP4x = ptPP3x
        ptPP4y = self.data_object.plate_thickness_p2
        self.PP4 = np.array([ptPP4x, ptPP4y])

        ptPP1x = 0
        ptPP1y = self.data_object.plate_thickness_p2
        self.PP1 = np.array([ptPP1x, ptPP1y])

        # ====================== Primary Beam 2  =====================
        ptAA1x = 0
        ptAA1y = ptPP1y
        self.AA1 = np.array([ptAA1x, ptAA1y])

        ptAA5x = (self.data_object.length_L2 - self.data_object.web_thickness_tw2)/2
        ptAA5y = ptPP1y
        self.AA5 = np.array([ptAA5x, ptAA5y])

        ptAA6x = (self.data_object.length_L2 + self.data_object.web_thickness_tw2)/2
        ptAA6y = ptPP1y
        self.AA6 = np.array([ptAA6x, ptAA6y])

        ptAA2x = self.data_object.width_B2
        ptAA2y = ptPP4y
        self.AA2 = np.array([ptAA2x, ptAA2y])













    def call_ExtndBoth_top(self):
        # TODO
        pass

class ExtendedEnd2DSide(object):
    """

    """
    def __init__(self, extnd_common_object):
        self.data_object = extnd_common_object

    def call_ExtndBoth_side(self):
        # TODO
        pass








































