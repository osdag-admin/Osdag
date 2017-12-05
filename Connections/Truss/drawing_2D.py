from numpy import math
import svgwrite
import cairosvg
import numpy as np
import os


class TrussBoltedConnection(object):
    def __init__(self):
        self.plate_length = 600
        self.plate_width = 400
        self.plate_thick = 22

        self.angle1_A = 150
        self.angle1_B = 150
        self.angle1_T = 12

        self.angle2_A = 100
        self.angle2_B = 65
        self.angl2_T = 12

        self.angle_length = 1000

        self.bolt_diameter = 20
        self.bolt_hole_diameter = self.bolt_diameter + 2

        self.theta = {"theta1": 50, "theta2": 160, "theta3": 250, "theta4": 340}
        self.TrsDist = {"TrsDist1": 250, "TrsDist2": 250, "TrsDist3": 250, "TrsDist4": 250}

        self.edge_dist = 40
        self.end_dist = 40
        self.gauge = 90

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

        Truss_2D_Front = Truss2DFront(self)

        if view == "Front":
            Truss_2D_Front.call_Truss_2DFront(filename)
        else:
            pass

class Truss2DFront(object):
    def __init__(self, Truss_common_object):
        self.data_object = Truss_common_object
        # --------------------------------------------------------------------------
        #                               FRONT VIEW
        # --------------------------------------------------------------------------

        self.origin = np.array([0,0])

        offsetX = 000
        offsetY = 00
        ####### GUSSET PLATE ######
        Ax = -self.data_object.plate_length + offsetX
        Ay = self.data_object.plate_width + offsetY
        self.A = np.array([Ax, Ay])

        Bx = self.data_object.plate_length + offsetX
        By = self.data_object.plate_width + offsetY
        self.B = np.array([Bx, By])

        Cx = self.data_object.plate_length + offsetX
        Cy = -self.data_object.plate_width + offsetY
        self.C = np.array([Cx, Cy])

        Dx = -self.data_object.plate_length + offsetX
        Dy = -self.data_object.plate_width + offsetY
        self.D = np.array([Dx, Dy])
        ####### GUSSET PLATE ######


    def  call_Truss_2DFront(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-1400 -850 2840 1740'), debug=True)  # 230 = move towards left ,
        # 600= move towards
        # down, 2840= width of view, 2340= height of view
        # dwg.add(dwg.line(self.A, self.B).stroke('blue', width=2.5, linecap='square'))
        # dwg.add(dwg.line(self.B, self.C).stroke('blue', width=2.5, linecap='square'))
        # dwg.add(dwg.line(self.C, self.D).stroke('blue', width=2.5, linecap='square'))
        # dwg.add(dwg.line(self.D, self.A).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.polyline(points=[self.A, self.B, self.C, self.D, self.A], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.CentrePoint, self.EndPoint).stroke('blue', width=5, linecap='square'))

        dwg.save()
