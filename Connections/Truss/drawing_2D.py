from numpy import math
import svgwrite
from svgwrite.text import Text
import cairosvg
import numpy as np
from math import radians, sin, cos
import os


class TrussBoltedConnection(object):
    def __init__(self):
        self.plate_length = 1000
        self.plate_width = 600
        self.plate_thick = 22

        self.angle1_A = 100
        self.angle1_B = 100
        self.angle1_T = 15
        self.Cz1 = 35.3
        self.Cy1 = 35.3

        self.angle2_A = 100
        self.angle2_B = 65
        self.angle2_T = 8
        self.Cz2 = 32.9
        self.Cy2 = 16.1

        self.angle3_A = 150
        self.angle3_B = 150
        self.angle3_T = 12
        self.Cz3 = 41.2
        self.Cy3 = 41.2

        self.angle4_A = 150
        self.angle4_B = 90
        self.angle4_T = 12
        self.Cz4 = 52.1
        self.Cy4 = 22.7

        self.angle_length = 1000

        self.theta = {"theta1": 70, "theta2": 135, "theta3": 225, "theta4": 315}
        self.TrsDist = {"TrsDist1": 200, "TrsDist2": 200, "TrsDist3": 200, "TrsDist4": 200}

        self.boltDia_1 = 14     #Bolting preferences for ANGLE MEMBER 1
        self.row_1 = 1
        self.col_1 = 4
        self.pitch_1 = 60
        self.gaugeDist_1 = 55
        self.edgeDist_1 = 40
        self.endDist_1 = self.edgeDist_1

        self.boltDia_2 = 14  # Bolting preferences for ANGLE MEMBER 2
        self.row_2 = 1
        self.col_2 = 4
        self.pitch_2 = 60
        self.gaugeDist_2 = 55
        self.edgeDist_2 = 40
        self.endDist_2 = self.edgeDist_2

        self.boltDia_3 = 14  # Bolting preferences for ANGLE MEMBER 3
        self.row_3 = 2
        self.col_3 = 4
        self.pitch_3 = 60
        self.gaugeDist_3 = 55
        self.edgeDist_3 = 40
        self.endDist_3 = self.edgeDist_3

        self.boltDia_4 = 14  # Bolting preferences for ANGLE MEMBER 4
        self.row_4 = 2
        self.col_4 = 4
        self.pitch_4 = 60
        self.gaugeDist_4 = 55
        self.edgeDist_4 = 40
        self.endDist_4 = self.edgeDist_4


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
        char_width = 26
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

        dwg.add(dwg.text(textup, insert=text_point_up, fill='black', font_family='sans-serif', font_size=42))
        dwg.add(dwg.text(textdown, insert=text_point_down, fill='black', font_family='sans-serif', font_size=42))

        # print "successful"

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

        ####### GUSSET PLATE ######

        Ax = -self.data_object.plate_length
        Ay = self.data_object.plate_width
        self.A = np.array([Ax, Ay])

        Bx = self.data_object.plate_length
        By = self.data_object.plate_width
        self.B = np.array([Bx, By])

        Cx = self.data_object.plate_length
        Cy = -self.data_object.plate_width
        self.C = np.array([Cx, Cy])

        Dx = -self.data_object.plate_length
        Dy = -self.data_object.plate_width
        self.D = np.array([Dx, Dy])

        ####### ANGLE MEMBERS (TOTAL 4 ANGLE MEMBERS) ######
        #============ ANGLE MEMBER 1 ================
        rot_mat_1 = ([np.cos(radians(self.data_object.theta["theta1"])), -np.sin(radians(self.data_object.theta["theta1"]))],
                           [np.sin(radians(self.data_object.theta["theta1"])), np.cos(radians(self.data_object.theta["theta1"]))])
        self.pt_origin = [0,0]
        self.pt_1 = [(self.data_object.angle_length+self.data_object.TrsDist["TrsDist1"])*cos(radians(self.data_object.theta["theta1"])),
                     -(self.data_object.angle_length+self.data_object.TrsDist["TrsDist1"])*sin(radians(self.data_object.theta["theta1"]))]

        ptAx_1 = 0
        ptAy_1 = -(self.data_object.angle1_A - self.data_object.Cz1)
        A_1 = [ptAx_1, ptAy_1]
        self.A_1 = np.dot(A_1, rot_mat_1)
        self.A_1[0] = self.A_1[0] + self.data_object.TrsDist["TrsDist1"]*cos(radians(self.data_object.theta["theta1"]))
        self.A_1[1] = self.A_1[1] - self.data_object.TrsDist["TrsDist1"]*sin(radians(self.data_object.theta["theta1"]))
        self.A_1 = [self.A_1[0], self.A_1[1]]

        ptBx_1 = 0
        ptBy_1 = self.data_object.Cz1 - self.data_object.angle1_T
        B_1 = [ptBx_1, ptBy_1]
        self.B_1 = np.dot(B_1, rot_mat_1)
        self.B_1[0] = self.B_1[0] + self.data_object.TrsDist["TrsDist1"]*cos(radians(self.data_object.theta["theta1"]))
        self.B_1[1] = self.B_1[1] - self.data_object.TrsDist["TrsDist1"]*sin(radians(self.data_object.theta["theta1"]))
        self.B_1 = [self.B_1[0], self.B_1[1]]

        ptCx_1 = 0
        ptCy_1 = self.data_object.Cz1
        C_1 = [ptCx_1, ptCy_1]
        self.C_1 = np.dot(C_1, rot_mat_1)
        self.C_1[0] = self.C_1[0] + self.data_object.TrsDist["TrsDist1"]*cos(radians(self.data_object.theta["theta1"]))
        self.C_1[1] = self.C_1[1] - self.data_object.TrsDist["TrsDist1"]*sin(radians(self.data_object.theta["theta1"]))
        self.C_1 = [self.C_1[0], self.C_1[1]]

        ptDx_1 = self.data_object.angle_length
        ptDy_1 = self.data_object.Cz1
        D_1 = [ptDx_1, ptDy_1]
        self.D_1 = np.dot(D_1, rot_mat_1)
        self.D_1[0] = self.D_1[0] + self.data_object.TrsDist["TrsDist1"]*cos(radians(self.data_object.theta["theta1"]))
        self.D_1[1] = self.D_1[1] - self.data_object.TrsDist["TrsDist1"]*sin(radians(self.data_object.theta["theta1"]))
        self.D_1 = [self.D_1[0], self.D_1[1]]

        ptEx_1 = self.data_object.angle_length
        ptEy_1 = self.data_object.Cz1 - self.data_object.angle1_T
        E_1 = [ptEx_1, ptEy_1]
        self.E_1 = np.dot(E_1, rot_mat_1)
        self.E_1[0] = self.E_1[0] + self.data_object.TrsDist["TrsDist1"]*cos(radians(self.data_object.theta["theta1"]))
        self.E_1[1] = self.E_1[1] - self.data_object.TrsDist["TrsDist1"]*sin(radians(self.data_object.theta["theta1"]))
        self.E_1 = [self.E_1[0], self.E_1[1]]

        ptFx_1 = self.data_object.angle_length
        ptFy_1 = -(self.data_object.angle1_A - self.data_object.Cz1)
        F_1 = [ptFx_1, ptFy_1]
        self.F_1 = np.dot(F_1, rot_mat_1)
        self.F_1[0] = self.F_1[0] + self.data_object.TrsDist["TrsDist1"]*cos(radians(self.data_object.theta["theta1"]))
        self.F_1[1] = self.F_1[1] - self.data_object.TrsDist["TrsDist1"]*sin(radians(self.data_object.theta["theta1"]))
        self.F_1 = [self.F_1[0], self.F_1[1]]

        # ============ ANGLE MEMBER 2 ================
        rot_mat_2 = ([np.cos(radians(self.data_object.theta["theta2"])), -np.sin(radians(self.data_object.theta["theta2"]))],
                     [np.sin(radians(self.data_object.theta["theta2"])), np.cos(radians(self.data_object.theta["theta2"]))])

        self.pt_2 = [(self.data_object.angle_length+self.data_object.TrsDist["TrsDist2"]) * cos(radians(self.data_object.theta["theta2"])),
                     -(self.data_object.angle_length+self.data_object.TrsDist["TrsDist2"]) * sin(radians(self.data_object.theta["theta2"]))]

        ptAx_2 = 0
        ptAy_2 = -(self.data_object.angle2_A - self.data_object.Cz2)
        A_2 = [ptAx_2, ptAy_2]
        self.A_2 = np.dot(A_2, rot_mat_2)
        self.A_2[0] = self.A_2[0] + self.data_object.TrsDist["TrsDist2"] * cos(radians(self.data_object.theta["theta2"]))
        self.A_2[1] = self.A_2[1] - self.data_object.TrsDist["TrsDist2"] * sin(radians(self.data_object.theta["theta2"]))
        self.A_2 = [self.A_2[0], self.A_2[1]]

        ptBx_2 = 0
        ptBy_2 = self.data_object.Cz2 - self.data_object.angle2_T
        B_2 = [ptBx_2, ptBy_2]
        self.B_2 = np.dot(B_2, rot_mat_2)
        self.B_2[0] = self.B_2[0] + self.data_object.TrsDist["TrsDist2"] * cos(radians(self.data_object.theta["theta2"]))
        self.B_2[1] = self.B_2[1] - self.data_object.TrsDist["TrsDist2"] * sin(radians(self.data_object.theta["theta2"]))
        self.B_2 = [self.B_2[0], self.B_2[1]]

        ptCx_2 = 0
        ptCy_2 = self.data_object.Cz2
        C_2 = [ptCx_2, ptCy_2]
        self.C_2 = np.dot(C_2, rot_mat_2)
        self.C_2[0] = self.C_2[0] + self.data_object.TrsDist["TrsDist2"] * cos(radians(self.data_object.theta["theta2"]))
        self.C_2[1] = self.C_2[1] - self.data_object.TrsDist["TrsDist2"] * sin(radians(self.data_object.theta["theta2"]))
        self.C_2 = [self.C_2[0], self.C_2[1]]

        ptDx_2 = self.data_object.angle_length
        ptDy_2 = self.data_object.Cz2
        D_2 = [ptDx_2, ptDy_2]
        self.D_2 = np.dot(D_2, rot_mat_2)
        self.D_2[0] = self.D_2[0] + self.data_object.TrsDist["TrsDist2"] * cos(radians(self.data_object.theta["theta2"]))
        self.D_2[1] = self.D_2[1] - self.data_object.TrsDist["TrsDist2"] * sin(radians(self.data_object.theta["theta2"]))
        self.D_2 = [self.D_2[0], self.D_2[1]]

        ptEx_2 = self.data_object.angle_length
        ptEy_2 = self.data_object.Cz2 - self.data_object.angle2_T
        E_2 = [ptEx_2, ptEy_2]
        self.E_2 = np.dot(E_2, rot_mat_2)
        self.E_2[0] = self.E_2[0] + self.data_object.TrsDist["TrsDist2"] * cos(radians(self.data_object.theta["theta2"]))
        self.E_2[1] = self.E_2[1] - self.data_object.TrsDist["TrsDist2"] * sin(radians(self.data_object.theta["theta2"]))
        self.E_2 = [self.E_2[0], self.E_2[1]]

        ptFx_2 = self.data_object.angle_length
        ptFy_2 = -(self.data_object.angle2_A - self.data_object.Cz2)
        F_2 = [ptFx_2, ptFy_2]
        self.F_2 = np.dot(F_2, rot_mat_2)
        self.F_2[0] = self.F_2[0] + self.data_object.TrsDist["TrsDist2"] * cos(radians(self.data_object.theta["theta2"]))
        self.F_2[1] = self.F_2[1] - self.data_object.TrsDist["TrsDist2"] * sin(radians(self.data_object.theta["theta2"]))
        self.F_2 = [self.F_2[0], self.F_2[1]]

        # ============ ANGLE MEMBER 3 ================
        rot_mat_3 = ([np.cos(radians(self.data_object.theta["theta3"])), -np.sin(radians(self.data_object.theta["theta3"]))],
                     [np.sin(radians(self.data_object.theta["theta3"])), np.cos(radians(self.data_object.theta["theta3"]))])
        self.pt_3 = [(self.data_object.angle_length+self.data_object.TrsDist["TrsDist3"]) * cos(radians(self.data_object.theta["theta3"])),
                     -(self.data_object.angle_length+self.data_object.TrsDist["TrsDist3"]) * sin(radians(self.data_object.theta["theta3"]))]

        ptAx_3 = 0
        ptAy_3 = -(self.data_object.angle3_A - self.data_object.Cz3)
        A_3 = [ptAx_3, ptAy_3]
        self.A_3 = np.dot(A_3, rot_mat_3)
        self.A_3[0] = self.A_3[0] + self.data_object.TrsDist["TrsDist3"] * cos(radians(self.data_object.theta["theta3"]))
        self.A_3[1] = self.A_3[1] - self.data_object.TrsDist["TrsDist3"] * sin(radians(self.data_object.theta["theta3"]))
        self.A_3 = [self.A_3[0], self.A_3[1]]

        ptBx_3 = 0
        ptBy_3 = self.data_object.Cz3 - self.data_object.angle3_T
        B_3 = [ptBx_3, ptBy_3]
        self.B_3 = np.dot(B_3, rot_mat_3)
        self.B_3[0] = self.B_3[0] + self.data_object.TrsDist["TrsDist3"] * cos(radians(self.data_object.theta["theta3"]))
        self.B_3[1] = self.B_3[1] - self.data_object.TrsDist["TrsDist3"] * sin(radians(self.data_object.theta["theta3"]))
        self.B_3 = [self.B_3[0], self.B_3[1]]

        ptCx_3 = 0
        ptCy_3 = self.data_object.Cz3
        C_3 = [ptCx_3, ptCy_3]
        self.C_3 = np.dot(C_3, rot_mat_3)
        self.C_3[0] = self.C_3[0] + self.data_object.TrsDist["TrsDist3"] * cos(radians(self.data_object.theta["theta3"]))
        self.C_3[1] = self.C_3[1] - self.data_object.TrsDist["TrsDist3"] * sin(radians(self.data_object.theta["theta3"]))
        self.C_3 = [self.C_3[0], self.C_3[1]]

        ptDx_3 = self.data_object.angle_length
        ptDy_3 = self.data_object.Cz3
        D_3 = [ptDx_3, ptDy_3]
        self.D_3 = np.dot(D_3, rot_mat_3)
        self.D_3[0] = self.D_3[0] + self.data_object.TrsDist["TrsDist3"] * cos(radians(self.data_object.theta["theta3"]))
        self.D_3[1] = self.D_3[1] - self.data_object.TrsDist["TrsDist3"] * sin(radians(self.data_object.theta["theta3"]))
        self.D_3 = [self.D_3[0], self.D_3[1]]

        ptEx_3 = self.data_object.angle_length
        ptEy_3 = self.data_object.Cz3 - self.data_object.angle3_T
        E_3 = [ptEx_3, ptEy_3]
        self.E_3 = np.dot(E_3, rot_mat_3)
        self.E_3[0] = self.E_3[0] + self.data_object.TrsDist["TrsDist3"] * cos(radians(self.data_object.theta["theta3"]))
        self.E_3[1] = self.E_3[1] - self.data_object.TrsDist["TrsDist3"] * sin(radians(self.data_object.theta["theta3"]))
        self.E_3 = [self.E_3[0], self.E_3[1]]

        ptFx_3 = self.data_object.angle_length
        ptFy_3 = -(self.data_object.angle3_A - self.data_object.Cz3)
        F_3 = [ptFx_3, ptFy_3]
        self.F_3 = np.dot(F_3, rot_mat_3)
        self.F_3[0] = self.F_3[0] + self.data_object.TrsDist["TrsDist3"] * cos(radians(self.data_object.theta["theta3"]))
        self.F_3[1] = self.F_3[1] - self.data_object.TrsDist["TrsDist3"] * sin(radians(self.data_object.theta["theta3"]))
        self.F_3 = [self.F_3[0], self.F_3[1]]

        # ============ ANGLE MEMBER 4 ================
        rot_mat_4 = ([np.cos(radians(self.data_object.theta["theta4"])), -np.sin(radians(self.data_object.theta["theta4"]))],
                     [np.sin(radians(self.data_object.theta["theta4"])), np.cos(radians(self.data_object.theta["theta4"]))])
        self.pt_4 = [(self.data_object.angle_length+self.data_object.TrsDist["TrsDist4"]) * cos(radians(self.data_object.theta["theta4"])),
                     -(self.data_object.angle_length+self.data_object.TrsDist["TrsDist4"]) * sin(radians(self.data_object.theta["theta4"]))]

        ptAx_4 = 0
        ptAy_4 = -(self.data_object.angle4_A - self.data_object.Cz4)
        A_4 = [ptAx_4, ptAy_4]
        self.A_4 = np.dot(A_4, rot_mat_4)
        self.A_4[0] = self.A_4[0] + self.data_object.TrsDist["TrsDist4"] * cos(radians(self.data_object.theta["theta4"]))
        self.A_4[1] = self.A_4[1] - self.data_object.TrsDist["TrsDist4"] * sin(radians(self.data_object.theta["theta4"]))
        self.A_4 = [self.A_4[0], self.A_4[1]]

        ptBx_4 = 0
        ptBy_4 = self.data_object.Cz4 - self.data_object.angle4_T
        B_4 = [ptBx_4, ptBy_4]
        self.B_4 = np.dot(B_4, rot_mat_4)
        self.B_4[0] = self.B_4[0] + self.data_object.TrsDist["TrsDist4"] * cos(radians(self.data_object.theta["theta4"]))
        self.B_4[1] = self.B_4[1] - self.data_object.TrsDist["TrsDist4"] * sin(radians(self.data_object.theta["theta4"]))
        self.B_4 = [self.B_4[0], self.B_4[1]]

        ptCx_4 = 0
        ptCy_4 = self.data_object.Cz4
        C_4 = [ptCx_4, ptCy_4]
        self.C_4 = np.dot(C_4, rot_mat_4)
        self.C_4[0] = self.C_4[0] + self.data_object.TrsDist["TrsDist4"] * cos(radians(self.data_object.theta["theta4"]))
        self.C_4[1] = self.C_4[1] - self.data_object.TrsDist["TrsDist4"] * sin(radians(self.data_object.theta["theta4"]))
        self.C_4 = [self.C_4[0], self.C_4[1]]

        ptDx_4 = self.data_object.angle_length
        ptDy_4 = self.data_object.Cz4
        D_4 = [ptDx_4, ptDy_4]
        self.D_4 = np.dot(D_4, rot_mat_4)
        self.D_4[0] = self.D_4[0] + self.data_object.TrsDist["TrsDist4"] * cos(radians(self.data_object.theta["theta4"]))
        self.D_4[1] = self.D_4[1] - self.data_object.TrsDist["TrsDist4"] * sin(radians(self.data_object.theta["theta4"]))
        self.D_4 = [self.D_4[0], self.D_4[1]]

        ptEx_4 = self.data_object.angle_length
        ptEy_4 = self.data_object.Cz4 - self.data_object.angle4_T
        E_4 = [ptEx_4, ptEy_4]
        self.E_4 = np.dot(E_4, rot_mat_4)
        self.E_4[0] = self.E_4[0] + self.data_object.TrsDist["TrsDist4"] * cos(radians(self.data_object.theta["theta4"]))
        self.E_4[1] = self.E_4[1] - self.data_object.TrsDist["TrsDist4"] * sin(radians(self.data_object.theta["theta4"]))
        self.E_4 = [self.E_4[0], self.E_4[1]]

        ptFx_4 = self.data_object.angle_length
        ptFy_4 = -(self.data_object.angle4_A - self.data_object.Cz4)
        F_4 = [ptFx_4, ptFy_4]
        self.F_4 = np.dot(F_4, rot_mat_4)
        self.F_4[0] = self.F_4[0] + self.data_object.TrsDist["TrsDist4"] * cos(radians(self.data_object.theta["theta4"]))
        self.F_4[1] = self.F_4[1] - self.data_object.TrsDist["TrsDist4"] * sin(radians(self.data_object.theta["theta4"]))
        self.F_4 = [self.F_4[0], self.F_4[1]]

    def  call_Truss_2DFront(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-1330 -1100 3040 2140'), debug=True)  # 230 = move towards left ,

        dwg.add(dwg.polyline(points=[self.A, self.B, self.C, self.D, self.A], stroke='blue', fill='none', stroke_width=2.5))    #Gusset Plate
        # boarder
        dwg.add(dwg.line(self.pt_origin, self.pt_1).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[15, 10, 5, 10]))     # CG line of Angle member 1
        dwg.add(dwg.polyline(points=[self.A_1,self.C_1,self.D_1,self.F_1,self.A_1],stroke='blue', fill = 'none',stroke_width=2.5))
        dwg.add(dwg.line(self.B_1, self.E_1).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.A_2, self.C_2, self.D_2, self.F_2, self.A_2], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.pt_origin, self.pt_2).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[15, 10, 5, 10]))  # CG line of Angle
        # member 2
        dwg.add(dwg.line(self.B_2, self.E_2).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.A_3, self.C_3, self.D_3, self.F_3, self.A_3], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.pt_origin, self.pt_3).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[15, 10, 5, 10]))  # CG line of Angle member 3
        dwg.add(dwg.line(self.B_3, self.E_3).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.A_4, self.C_4, self.D_4, self.F_4, self.A_4], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.pt_origin, self.pt_4).stroke('red', width=2.5, linecap='square').dasharray(dasharray=[15, 10, 5, 10]))  # CG line of Angle member 1
        dwg.add(dwg.line(self.B_4, self.E_4).stroke('blue', width=2.5, linecap='square'))

        # ============ Bolts placement over Angle member 1 ================
        list_of_pts_1 = []
        row1 = self.data_object.row_1
        col1 = self.data_object.col_1
        bolt_rad_1 = self.data_object.boltDia_1 / 2

        for i in range(col1):
            for j in range(row1):
                ptX_bolt_1 = (self.data_object.TrsDist["TrsDist1"] + self.data_object.endDist_1 + i * self.data_object.pitch_1)
                ptY_bolt_1 = -(self.data_object.TrsDist["TrsDist1"] + self.data_object.endDist_1 + i * self.data_object.pitch_1)

                ptX_bolt_1 = ptX_bolt_1 * cos(radians(self.data_object.theta["theta1"]))
                ptY_bolt_1 = ptY_bolt_1 * sin(radians(self.data_object.theta["theta1"]))

                pt_bolt_1 = np.array([ptX_bolt_1, ptY_bolt_1])
                dwg.add(dwg.circle(center=pt_bolt_1, r=bolt_rad_1, stroke='blue', fill='none', stroke_width=1.5))

                ptX_C_1 = pt_bolt_1[0] - (bolt_rad_1 + 4) * cos(radians(self.data_object.theta["theta1"]))
                ptY_C_1 = pt_bolt_1[1] + (bolt_rad_1 + 4) * sin(radians(self.data_object.theta["theta1"]))
                pt_C_1 = [ptX_C_1, ptY_C_1]
                ptX_D_1 = pt_bolt_1[0] + (bolt_rad_1 + 4) * cos(radians(self.data_object.theta["theta1"]))
                ptY_D_1 = pt_bolt_1[1] - (bolt_rad_1 + 4) * sin(radians(self.data_object.theta["theta1"]))
                pt_D_1 = [ptX_D_1, ptY_D_1]
                dwg.add(dwg.line(pt_C_1, pt_D_1).stroke('red', width=1.0, linecap='square'))

                ptX_C1_1 = pt_bolt_1[0] - (bolt_rad_1 + 4) * sin(radians(self.data_object.theta["theta1"]))
                ptY_C1_1 = pt_bolt_1[1] - (bolt_rad_1 + 4) * cos(radians(self.data_object.theta["theta1"]))
                pt_C1_1 = [ptX_C1_1, ptY_C1_1]
                ptX_D1_1 = pt_bolt_1[0] + (bolt_rad_1 + 4) * sin(radians(self.data_object.theta["theta1"]))
                ptY_D1_1 = pt_bolt_1[1] + (bolt_rad_1 + 4) * cos(radians(self.data_object.theta["theta1"]))
                pt_D1_1 = [ptX_D1_1, ptY_D1_1]
                dwg.add(dwg.line(pt_C1_1, pt_D1_1).stroke('red', width=1.0, linecap='square'))

                list_of_pts_1.append(pt_bolt_1)

        # ============ Bolts placement over Angle member 2 ================
        list_of_pts_2 = []
        row2 = self.data_object.row_2
        col2 = self.data_object.col_2
        bolt_rad_2 = self.data_object.boltDia_2 / 2

        for i in range(col2):
            for j in range(row2):
                ptX_bolt_2 = (self.data_object.TrsDist["TrsDist2"] + self.data_object.endDist_2 + i * self.data_object.pitch_2)
                ptY_bolt_2 = -(self.data_object.TrsDist["TrsDist2"] + self.data_object.endDist_2 + i * self.data_object.pitch_2)

                ptX_bolt_2 = ptX_bolt_2 * cos(radians(self.data_object.theta["theta2"]))
                ptY_bolt_2 = ptY_bolt_2 * sin(radians(self.data_object.theta["theta2"]))

                pt_bolt_2 = np.array([ptX_bolt_2, ptY_bolt_2])
                dwg.add(dwg.circle(center=pt_bolt_2, r=bolt_rad_2, stroke='blue', fill='none', stroke_width=1.5))

                ptX_C_2 = pt_bolt_2[0] - (bolt_rad_2 + 4) * cos(radians(self.data_object.theta["theta2"]))
                ptY_C_2 = pt_bolt_2[1] + (bolt_rad_2 + 4) * sin(radians(self.data_object.theta["theta2"]))
                pt_C_2 = [ptX_C_2, ptY_C_2]
                ptX_D_2 = pt_bolt_2[0] + (bolt_rad_2 + 4) * cos(radians(self.data_object.theta["theta2"]))
                ptY_D_2 = pt_bolt_2[1] - (bolt_rad_2 + 4) * sin(radians(self.data_object.theta["theta2"]))
                pt_D_2 = [ptX_D_2, ptY_D_2]
                dwg.add(dwg.line(pt_C_2, pt_D_2).stroke('red', width=1.0, linecap='square'))

                ptX_C1_2 = pt_bolt_2[0] - (bolt_rad_2 + 4) * sin(radians(self.data_object.theta["theta2"]))
                ptY_C1_2 = pt_bolt_2[1] - (bolt_rad_2 + 4) * cos(radians(self.data_object.theta["theta2"]))
                pt_C1_2 = [ptX_C1_2, ptY_C1_2]
                ptX_D1_2 = pt_bolt_2[0] + (bolt_rad_2 + 4) * sin(radians(self.data_object.theta["theta2"]))
                ptY_D1_2 = pt_bolt_2[1] + (bolt_rad_2 + 4) * cos(radians(self.data_object.theta["theta2"]))
                pt_D1_2 = [ptX_D1_2, ptY_D1_2]
                dwg.add(dwg.line(pt_C1_2, pt_D1_2).stroke('red', width=1.0, linecap='square'))
                list_of_pts_2.append(pt_bolt_2)

        # ============ Bolts placement over Angle member 3 ================
        row3 = self.data_object.row_3
        col3 = self.data_object.col_3
        bolt_rad_3 = self.data_object.boltDia_3 / 2

        pt_inside_column_list_3 = []
        for i in range(col3):
            col_inside_list_3 = []
            for j in range(row3):
                pt_boltX_3 = self.A_3[0] + (self.data_object.endDist_3 + i * self.data_object.pitch_3) * cos(radians(self.data_object.theta["theta3"]))
                pt_boltY_3 = self.A_3[1] - (self.data_object.endDist_3 + i * self.data_object.pitch_3) * sin(radians(self.data_object.theta["theta3"]))
                pt_bolt_3 = [pt_boltX_3, pt_boltY_3]

                pt_bolt_3[0] = pt_bolt_3[0] + self.data_object.edgeDist_3 * sin(radians(self.data_object.theta["theta3"]))
                pt_bolt_3[1] = pt_bolt_3[1] + self.data_object.edgeDist_3 * cos(radians(self.data_object.theta["theta3"]))

                pt_bolt_3[0] = pt_bolt_3[0] + j * self.data_object.gaugeDist_3 * sin(radians(self.data_object.theta["theta3"]))
                pt_bolt_3[1] = pt_bolt_3[1] + j * self.data_object.gaugeDist_3 * cos(radians(self.data_object.theta["theta3"]))

                dwg.add(dwg.circle(center=pt_bolt_3, r=bolt_rad_3, stroke='blue', fill='none', stroke_width=1.5))

                col_inside_list_3.append(pt_bolt_3)

                ptX_C_3 = pt_bolt_3[0] - (bolt_rad_3 + 4) * cos(radians(self.data_object.theta["theta3"]))
                ptY_C_3 = pt_bolt_3[1] + (bolt_rad_3 + 4) * sin(radians(self.data_object.theta["theta3"]))
                pt_C_3 = [ptX_C_3, ptY_C_3]
                ptX_D_3 = pt_bolt_3[0] + (bolt_rad_3 + 4) * cos(radians(self.data_object.theta["theta3"]))
                ptY_D_3 = pt_bolt_3[1] - (bolt_rad_3 + 4) * sin(radians(self.data_object.theta["theta3"]))
                pt_D_3 = [ptX_D_3, ptY_D_3]
                dwg.add(dwg.line(pt_C_3, pt_D_3).stroke('red', width=1.0, linecap='square'))

                ptX_C1_3 = pt_bolt_3[0] - (bolt_rad_3 + 4) * sin(radians(self.data_object.theta["theta3"]))
                ptY_C1_3 = pt_bolt_3[1] - (bolt_rad_3 + 4) * cos(radians(self.data_object.theta["theta3"]))
                pt_C1_3 = [ptX_C1_3, ptY_C1_3]
                ptX_D1_3 = pt_bolt_3[0] + (bolt_rad_3 + 4) * sin(radians(self.data_object.theta["theta3"]))
                ptY_D1_3 = pt_bolt_3[1] + (bolt_rad_3 + 4) * cos(radians(self.data_object.theta["theta3"]))
                pt_D1_3= [ptX_D1_3, ptY_D1_3]
                dwg.add(dwg.line(pt_C1_3, pt_D1_3).stroke('red', width=1.0, linecap='square'))
            pt_inside_column_list_3.append(col_inside_list_3)

        # ============ Bolts placement over Angle member 4 ================
        row4 = self.data_object.row_4
        col4 = self.data_object.col_4
        bolt_rad_4 = self.data_object.boltDia_4 / 2

        pt_inside_column_list_4 = []
        for i in range(col4):
            col_inside_list_4 = []
            for j in range(row4):
                pt_boltX_4 = self.A_4[0] + (self.data_object.endDist_4 + i * self.data_object.pitch_4) * cos(radians(self.data_object.theta["theta4"]))
                pt_boltY_4 = self.A_4[1] - (self.data_object.endDist_4 + i * self.data_object.pitch_4) * sin(radians(self.data_object.theta["theta4"]))
                pt_bolt_4 = [pt_boltX_4, pt_boltY_4]

                pt_bolt_4[0] = pt_bolt_4[0] + self.data_object.edgeDist_4 * sin(radians(self.data_object.theta["theta4"]))
                pt_bolt_4[1] = pt_bolt_4[1] + self.data_object.edgeDist_4 * cos(radians(self.data_object.theta["theta4"]))

                pt_bolt_4[0] = pt_bolt_4[0] + j * self.data_object.gaugeDist_4 * sin(radians(self.data_object.theta["theta4"]))
                pt_bolt_4[1] = pt_bolt_4[1] + j * self.data_object.gaugeDist_4 * cos(radians(self.data_object.theta["theta4"]))

                dwg.add(dwg.circle(center=pt_bolt_4, r=bolt_rad_4, stroke='blue', fill='none', stroke_width=1.5))
                col_inside_list_4.append(pt_bolt_4)

                ptX_C_4 = pt_bolt_4[0] - (bolt_rad_4 + 4) * cos(radians(self.data_object.theta["theta4"]))
                ptY_C_4 = pt_bolt_4[1] + (bolt_rad_4 + 4) * sin(radians(self.data_object.theta["theta4"]))
                pt_C_4 = [ptX_C_4, ptY_C_4]
                ptX_D_4 = pt_bolt_4[0] + (bolt_rad_4 + 4) * cos(radians(self.data_object.theta["theta4"]))
                ptY_D_4 = pt_bolt_4[1] - (bolt_rad_4 + 4) * sin(radians(self.data_object.theta["theta4"]))
                pt_D_4 = [ptX_D_4, ptY_D_4]
                dwg.add(dwg.line(pt_C_4, pt_D_4).stroke('red', width=1.0, linecap='square'))

                ptX_C1_4 = pt_bolt_4[0] - (bolt_rad_4 + 4) * sin(radians(self.data_object.theta["theta4"]))
                ptY_C1_4 = pt_bolt_4[1] - (bolt_rad_4 + 4) * cos(radians(self.data_object.theta["theta4"]))
                pt_C1_4 = [ptX_C1_4, ptY_C1_4]
                ptX_D1_4 = pt_bolt_4[0] + (bolt_rad_4 + 4) * sin(radians(self.data_object.theta["theta4"]))
                ptY_D1_4 = pt_bolt_4[1] + (bolt_rad_4 + 4) * cos(radians(self.data_object.theta["theta4"]))
                pt_D1_4 = [ptX_D1_4, ptY_D1_4]
                dwg.add(dwg.line(pt_C1_4, pt_D1_4).stroke('red', width=1.0, linecap='square'))
            pt_inside_column_list_4.append(col_inside_list_4)

        # ============ Label for Gusset Plate  ================
        point = self.C - (self.data_object.plate_length/10) * np.array([1, 0])
        theta = 60
        offset = 100
        textup = "Gusset plate " + str(self.data_object.plate_length) + " x " + str(self.data_object.plate_width) + " x " + str(self.data_object.plate_thick)
        textdown = " "
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)

        # ============ Labels for Angle members 1 ================
        point = self.D_1 - ((self.data_object.angle1_A/3) * sin(radians(self.data_object.theta["theta1"]))) * np.array([1,0]) - ((self.data_object.angle1_A/3) * cos(radians(self.data_object.theta["theta1"]))) * np.array([0, 1])
        textup = str(self.data_object.angle1_A) + " x " + str(self.data_object.angle1_B) + " x " + str(self.data_object.angle1_T)
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NE", offset, textup, textdown)

        ptx_lab_1 = list_of_pts_1[0]
        pty_lab_1 = ptx_lab_1 + (1.2*self.data_object.angle1_A)*sin(radians(self.data_object.theta["theta1"]))*np.array([1,0]) + (1.2*self.data_object.angle1_A)*cos(radians(self.data_object.theta["theta1"]))*np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab_1, pty_lab_1, dwg)

        ptx_lab1_1 = list_of_pts_1[-1]
        pty_lab1_1 = ptx_lab1_1 + (1.2 * self.data_object.angle1_A) * sin(radians(self.data_object.theta["theta1"])) * np.array([1,0]) + (1.2*self.data_object.angle1_A) * cos(radians(self.data_object.theta["theta1"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab1_1, pty_lab1_1, dwg)

        # point1 = ptx2 + (self.data_object.edge_dist1) * np.array([-1, 0])
        params = {"offset": (self.data_object.angle1_A), "textoffset": 20, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        text_1 = str(len(list_of_pts_1) - 1) + "@" + str(self.data_object.pitch_1) + "mm c/c"
        self.data_object.draw_dimension_outer_arrow(dwg, ptx_lab_1, ptx_lab1_1, text_1, params)

        ptx_end_1 = self.C_1
        pty_end_1 = self.C_1 + (self.data_object.Cz1) *sin(radians(self.data_object.theta["theta1"]))* np.array([1, 0])
        pty_end_1 = pty_end_1 + (self.data_object.Cz1) *cos(radians(self.data_object.theta["theta1"]))* np.array([0, 1])
        self.data_object.draw_faint_line(ptx_end_1, pty_end_1, dwg)

        ptx_end1_1 = self.C_1 + (self.data_object.endDist_1) *cos(radians(self.data_object.theta["theta1"])) * np.array([1, 0])
        pty_end1_1 = ptx_end1_1 - (self.data_object.endDist_1) *sin(radians(self.data_object.theta["theta1"])) * np.array([0, 1])
        ptx_end1_1 = pty_end1_1+ (self.data_object.Cz1) * sin(radians(self.data_object.theta["theta1"])) * np.array([1, 0])
        pty_end1_1 = ptx_end1_1 + (self.data_object.Cz1) * cos(radians(self.data_object.theta["theta1"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_end1_1, pty_end1_1, dwg)

        params = {"offset": (10), "textoffset": 30, "lineori": "right", "endlinedim": 5, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pty_end_1, pty_end1_1, str(self.data_object.edgeDist_1), params)

        textup = "M" + str(self.data_object.boltDia_1)
        self.data_object.draw_oriented_arrow(dwg, list_of_pts_1[-1], theta, "NW", offset, textup, textdown)

        # ============ Labels for Angle members 2 ================
        point = self.D_2 - ((self.data_object.angle2_A / 3) * sin(radians(self.data_object.theta["theta2"]))) * np.array([1,0]) - ((self.data_object.angle2_A / 3) * cos(radians(self.data_object.theta["theta2"]))) * np.array([0, 1])
        textup = str(self.data_object.angle2_A) + " x " + str(self.data_object.angle2_B) + " x " + str(self.data_object.angle2_T)
        self.data_object.draw_oriented_arrow(dwg, point, theta, "NW", offset, textup, textdown)

        ptx_lab_2 = list_of_pts_2[0]
        pty_lab_2 = ptx_lab_2 - (1.2 * self.data_object.angle2_A) * sin(radians(self.data_object.theta["theta2"])) * np.array([1, 0]) - (1.2*self.data_object.angle2_A) * cos(radians(self.data_object.theta["theta2"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab_2, pty_lab_2, dwg)

        ptx_lab1_2 = list_of_pts_2[-1]
        pty_lab1_2 = ptx_lab1_2 - (1.2 * self.data_object.angle2_A) * sin(radians(self.data_object.theta["theta2"])) * np.array([1,0]) - (1.2 *self.data_object.angle1_A) * cos(radians(self.data_object.theta["theta2"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab1_2, pty_lab1_2, dwg)

        # point1 = ptx2 + (self.data_object.edge_dist1) * np.array([-1, 0])
        params = {"offset": (self.data_object.angle2_A), "textoffset": 100, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        text_2 = str(len(list_of_pts_2) - 1) + "@" + str(self.data_object.pitch_2) + "mm c/c"
        self.data_object.draw_dimension_outer_arrow(dwg, ptx_lab_2, ptx_lab1_2, text_2, params)

        ptx_end_2 = list_of_pts_2[0]
        ptx_end_2 = ptx_end_2 + self.data_object.endDist_2 * sin(radians(self.data_object.theta["theta2"])) * np.array([1, 0])
        pty_end_2 = ptx_end_2 - self.data_object.endDist_2 * cos(radians(self.data_object.theta["theta2"])) * np.array([0, 1])

        ptx_end1_2 = pty_end_2 - (1.2 * self.data_object.angle2_A) * sin(radians(self.data_object.theta["theta2"])) * np.array([1, 0])
        pty_end1_2 = ptx_end1_2 - (1.2 * self.data_object.angle2_A) * cos(radians(self.data_object.theta["theta2"])) * np.array([0, 1])
        self.data_object.draw_faint_line(pty_end_2, pty_end1_2, dwg)

        params = {"offset": (20), "textoffset": 30, "lineori": "right", "endlinedim": 5, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pty_lab_2, pty_end1_2, str(self.data_object.edgeDist_2), params)

        textup = "M" + str(self.data_object.boltDia_2)
        theta = 75
        offset = 200
        self.data_object.draw_oriented_arrow(dwg, list_of_pts_2[-1], theta, "NE", offset, textup, textdown)

        # ============ Labels for Angle members 3 ================

        point = self.D_3 - ((self.data_object.angle3_A / 3) * sin(radians(self.data_object.theta["theta3"]))) * np.array([1,0]) - ((self.data_object.angle3_A / 3) * cos(radians(self.data_object.theta["theta3"]))) * np.array([0, 1])
        textup = str(self.data_object.angle3_A) + " x " + str(self.data_object.angle3_B) + " x " + str(self.data_object.angle3_T)
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SW", offset, textup, textdown)

        ptx_lab_3 = pt_inside_column_list_3[0][0]
        pty_lab_3 = ptx_lab_3 - (1.2 * self.data_object.angle3_A) * sin(radians(self.data_object.theta["theta3"])) * np.array([1, 0]) - (1.2 * self.data_object.angle3_A) * cos(radians(self.data_object.theta["theta3"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab_3, pty_lab_3, dwg)

        ptx_lab1_3 = pt_inside_column_list_3[-1][0]
        pty_lab1_3 = ptx_lab1_3 - (1.2 * self.data_object.angle3_A) * sin(radians(self.data_object.theta["theta3"])) * np.array([1, 0]) - (1.2 * self.data_object.angle3_A) * cos(radians(self.data_object.theta["theta3"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab1_3, pty_lab1_3, dwg)

        ptx_end_3 = pt_inside_column_list_3[0][0]
        ptx_end_3 = ptx_end_3 + self.data_object.endDist_3 * cos(radians(self.data_object.theta["theta3"])) * np.array([1, 0])
        pty_end_3 = ptx_end_3 - self.data_object.endDist_3 * sin(radians(self.data_object.theta["theta3"])) * np.array([0, 1])

        ptx_end1_3 = pty_end_3 - (1.2 * self.data_object.angle3_A) * sin(radians(self.data_object.theta["theta3"])) * np.array([1, 0])
        pty_end1_3 = ptx_end1_3 - (1.2 * self.data_object.angle3_A) * cos(radians(self.data_object.theta["theta3"])) * np.array([0, 1])
        self.data_object.draw_faint_line(pty_end_3, pty_end1_3, dwg)

        textup = "M" + str(self.data_object.boltDia_3)
        theta = 75
        offset = 200
        self.data_object.draw_oriented_arrow(dwg, pt_inside_column_list_3[-1][-1], theta, "NW", offset, textup, textdown)

        # ============ Labels for Angle members 4 ================

        point = self.D_4 - ((self.data_object.angle4_A / 3) * sin(radians(self.data_object.theta["theta4"]))) * np.array([1,0]) - ((self.data_object.angle4_A / 3) * cos(radians(self.data_object.theta["theta4"]))) * np.array([0, 1])
        textup = str(self.data_object.angle4_A) + " x " + str(self.data_object.angle4_B) + " x " + str(self.data_object.angle4_T)
        self.data_object.draw_oriented_arrow(dwg, point, theta, "SE", offset, textup, textdown)     #Angle member designation

        ptx_lab_4 = pt_inside_column_list_4[0][0]
        pty_lab_4 = ptx_lab_4 - (1.2 * self.data_object.angle4_A) * sin(radians(self.data_object.theta["theta4"])) * np.array([1, 0]) - (1.2 *self.data_object.angle4_A) * cos(radians(self.data_object.theta["theta4"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab_4, pty_lab_4, dwg)     #Pitch dimension line first bolt

        ptx_lab1_4 = pt_inside_column_list_4[-1][0]
        pty_lab1_4 = ptx_lab1_4 - (1.2 * self.data_object.angle4_A) * sin(radians(self.data_object.theta["theta4"])) * np.array([1,0]) - (1.2 * self.data_object.angle4_A) * cos(radians(self.data_object.theta["theta4"])) * np.array([0, 1])
        self.data_object.draw_faint_line(ptx_lab1_4, pty_lab1_4, dwg)   #Pitch dimension line last bolt

        ptx_end_4 = pt_inside_column_list_4[0][0]                       #For end distance
        ptx_end_4 = ptx_end_4 + self.data_object.endDist_4 * cos(radians(self.data_object.theta["theta4"])) * np.array([1, 0])
        pty_end_4 = ptx_end_4 - self.data_object.endDist_4 * sin(radians(self.data_object.theta["theta4"])) * np.array([0, 1])

        ptx_end1_4 = pty_end_4 - (1.2 * self.data_object.angle4_A) * sin(radians(self.data_object.theta["theta4"])) * np.array([1, 0])
        pty_end1_4 = ptx_end1_4 - (1.2 * self.data_object.angle4_A) * cos(radians(self.data_object.theta["theta4"])) * np.array([0, 1])
        self.data_object.draw_faint_line(pty_end_4, pty_end1_4, dwg)

        textup = "M" + str(self.data_object.boltDia_4)
        theta = 75
        offset = 200
        self.data_object.draw_oriented_arrow(dwg, pt_inside_column_list_4[-1][-1], theta, "SW", offset, textup, textdown)

        dwg.save()
