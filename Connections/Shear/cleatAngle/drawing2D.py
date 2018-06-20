'''
Created on 24-Aug-2015

@author: deepa
'''
import svgwrite
import cmath
import math
import numpy as np
from numpy import math
from model import *
import cairosvg


class cleatCommonData(object):
    def __init__(self, input_obj, ouput_obj, dict_beam_data, dict_column_data, dict_angle_data, folder):
        '''
        Provide all the data related to Finplate connection

        :param input_obj:
        :type input_obj:dictionary(Input parameter dictionary)
        :param ouput_obj:
        :type ouputObj :dictionary (output parameter dictionary)
        :param dict_beam_data :
        :type dict_beam_data:  dictionary (Beam sectional properties)
        :param dict_column_data :
        :type dict_beam_data: dictionary (Column sectional properties dictionary)
        '''
        self.beam_T = float(dict_beam_data["T"])
        self.col_T = float(dict_column_data["T"])
        self.D_beam = int(dict_beam_data["D"])
        self.D_col = int(dict_column_data["D"])
        self.col_B = int(dict_column_data["B"])
        self.beam_B = int(dict_beam_data["B"])
        self.col_tw = float(dict_column_data["tw"])
        self.beam_tw = float(dict_beam_data["tw"])
        self.col_Designation = dict_column_data["Designation"]
        self.beam_Designation = dict_beam_data["Designation"]
        self.beam_R1 = float(dict_beam_data["R1"])
        self.col_R1 = float(dict_column_data["R1"])
        self.cleat_ht = float(ouput_obj['cleat']["height"])
        cleat_legsizes = str(dict_angle_data["AXB"])
        cleat_legsize_A = int(cleat_legsizes.split('x')[0])
        cleat_legsize_B = int(cleat_legsizes.split('x')[1])
        self.cleat_legsize = int(cleat_legsize_A)
        self.cleat_legsize_1 = int(cleat_legsize_B)
        # self.cleat_legsize_1 = 120
        self.cleat_thk = int(dict_angle_data["t"])
        # self.plate_ht= ouput_obj['Plate']['height']
        # self.cleat_thk = input_obj['Plate']["Thickness (mm)"]

        # self.plate_width = ouput_obj['Plate']['width']
        # self.cleat_thk = ouput_obj['Plate']['height']
        # self.cleat_thk = ouput_obj['Weld']['thickness']
        self.bolt_dia = int(input_obj["Bolt"]["Diameter (mm)"])
        self.dia_hole = (ouput_obj['Bolt']['diahole'])
        self.bolt_type = str(input_obj["Bolt"]["Type"])
        self.bolt_grade = float(input_obj['Bolt']['Grade'])
        self.connectivity = input_obj['Member']['Connectivity']
        self.pitch = ouput_obj['Bolt']["pitch"]
        self.gauge = ouput_obj['Bolt']["gauge"]
        self.end_dist = ouput_obj['Bolt']["enddist"]
        self.edge_dist = ouput_obj['Bolt']["edge"]
        self.no_of_rows = ouput_obj['Bolt']["numofrow"]
        self.no_of_col = ouput_obj['Bolt']["numofcol"]
        self.no_of_crows = ouput_obj['cleat']['numofrow']
        self.no_of_ccol = ouput_obj['cleat']['numofcol']
        self.cpitch = ouput_obj['cleat']['pitch']
        self.cgauge = ouput_obj['cleat']['guage']
        self.cedge_dist = ouput_obj['cleat']['edge']
        self.cend_dist = ouput_obj['cleat']['end']
        self.col_L = 800
        self.beam_L = 350
        # self.gap = 20  # Clear distance between Column and Beam as per subramanyam's book ,range 15-20 mm
        self.gap = input_obj["detailing"]["gap"]
        # self.notch_L = (self.col_B / 2 - self.col_tw / 2) + 10
        # self.notch_offset = (self.col_T + self.col_R1)

        self.R1_max = max([self.col_R1, self.beam_R1, 10])
        self.notch_L = ((self.col_B / 2 - self.col_tw / 2) + self.gap)
        self.notch_offset = max([self.col_T, self.beam_T]) + max([self.col_R1, self.beam_R1]) + max([(self.col_T/2), (self.beam_T/2),10])

        self.folder = folder

    def add_s_marker(self, dwg):
        '''
        Draws start arrow to given line  -------->

        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)

        '''

        smarker = dwg.marker(insert=(8, 3), size=(30, 30), orient="auto")

        smarker.add(dwg.path(d=" M0,0 L3,3 L0,6 L8,3 L0,0", fill='black'))
        dwg.defs.add(smarker)

        return smarker

    def add_section_maker(self, dwg):
        '''
        Draws start arrow to given line  -------->

        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)

        '''
        section_marker = dwg.marker(insert=(0, 5), size=(10, 10), orient="auto")

        section_marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill='blue', stroke='black'))    #makes arrow
        dwg.defs.add(section_marker)

        return section_marker

    def add_e_marker(self, dwg):
        '''
        This routine returns end arrow  <---------

        :param dwg :
        :type dwg : svgwrite  ( Container for all svg elements)

        '''
        emarker = dwg.marker(insert=(0, 3), size=(30, 20), orient="auto")
        emarker.add(dwg.path(d=" M0,3 L8,6 L5,3 L8,0 L0,3", fill='black'))
        dwg.defs.add(emarker)
        return emarker

    def draw_arrow(self, line, s_arrow, e_arrow):
        line['marker-start'] = s_arrow.get_funciri()
        line['marker-end'] = e_arrow.get_funciri()

    def draw_start_arrow(self, line, s_arrow):
        line['marker-start'] = s_arrow.get_funciri()

    def draw_end_arrow(self, line, e_arrow):
        line['marker-end'] = e_arrow.get_funciri()

    def draw_faint_line(self, pt_one, pt_two, dwg):
        '''
        Draw faint line to show dimensions.

        :param dwg :
        :type dwg : svgwrite (obj)
        :param: pt_one :
        :type NumPy Array
        :param pt_two :
        :type NumPy Array

        '''
        dwg.add(dwg.line(pt_one, pt_two).stroke('#D8D8D8', width=2.5, linecap='square', opacity=0.7))

    def draw_dimension_outer_arrow(self, dwg, pt1, pt2, text, params):

        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: pt1 :
        :type NumPy Array
        :param pt2 :
        :type NumPy Array
        :param text :
        :type text : String
        :param params["offset"] :
        :type params["offset"] : offset of the dimension line
        :param params["textoffset"]:
        :type params["textoffset"]: float (offset of text from dimension line)
        :param params["lineori"]:
        :type params ["lineori"]: String (right/left)
        :param params["endlinedim"]:
        :type params'["endlindim"] : float (dimension line at the end of the outer arrow)
        '''
        smarker = self.add_s_marker(dwg)
        emarker = self.add_e_marker(dwg)

        line_vector = pt2 - pt1  # [a, b]
        normal_vector = np.array([-line_vector[1], line_vector[0]])  # [-b, a]
        normal_unit_vector = self.normalize(normal_vector)
        if params["lineori"] == "left":
            normal_unit_vector = -normal_unit_vector

        Q1 = pt1 + params["offset"] * normal_unit_vector
        Q2 = pt2 + params["offset"] * normal_unit_vector
        line = dwg.add(dwg.line(Q1, Q2).stroke('black', width=2.5, linecap='square'))
        self.draw_start_arrow(line, emarker)
        self.draw_end_arrow(line, smarker)

        Q12mid = 0.5 * (Q1 + Q2)
        txt_pt = Q12mid + params["textoffset"] * normal_unit_vector
        dwg.add(dwg.text(text, insert=(txt_pt), fill='black', font_family="sans-serif", font_size=28))

        L1 = Q1 + params["endlinedim"] * normal_unit_vector
        L2 = Q1 + params["endlinedim"] * (-normal_unit_vector)
        dwg.add(dwg.line(L1, L2).stroke('black', width=2.5, linecap='square', opacity=1.0))
        L3 = Q2 + params["endlinedim"] * normal_unit_vector
        L4 = Q2 + params["endlinedim"] * (-normal_unit_vector)
        dwg.add(dwg.line(L3, L4).stroke('black', width=2.5, linecap='square', opacity=1.0))

    def normalize(self, vec):
        a = vec[0]
        b = vec[1]
        mag = math.sqrt(a * a + b * b)
        return vec / mag

    def draw_cross_section(self, dwg, ptA, ptB, txt_pt, text):
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param ptA :
        :type ptA : NumPy Array
        :param ptB :
        :type ptB : NumPy Array
        :param txt_pt :
        :type txt_pt : NumPy Array
        :param text :
        :type text : String

        '''
        line = dwg.add(dwg.line((ptA), (ptB)).stroke('black', width=2.5, linecap='square'))
        sec_arrow = self.add_section_maker(dwg)
        self.draw_end_arrow(line, sec_arrow)                  # adds arrow to the line
        dwg.add(dwg.text(text, insert=(txt_pt), fill='black', font_family="sans-serif", font_size=52))

    def draw_dimension_inner_arrow(self, dwg, ptA, ptB, text, params):
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptA :
        :type NumPy Array
        :param ptB :
        :type NumPy Array
        :param text :
        :type text : String
        :param params["textoffset"]:
        :type params["textoffset"]: float (offset of text from dimension line)
        :param params["endlinedim"]:
        :type params'["endlindim"] : float (dimension line at the end of the outer arrow)   
        :param params["arrowlen"]:
        :type params["arrowlen"]: float (Size of the arrow)
        '''

        smarker = self.add_s_marker(dwg)
        emarker = self.add_e_marker(dwg)

        u = ptB - ptA  # [a, b]
        u_unit_vector = self.normalize(u)

        v_unit_vector = np.array([-u_unit_vector[1], u_unit_vector[0]])  # [-b, a]

        A1 = ptA + params["endlinedim"] * v_unit_vector
        A2 = ptA - params["endlinedim"] * (-v_unit_vector)
        dwg.add(dwg.line(A1, A2).stroke('black', width=2.5, linecap='square'))
        B1 = ptB + params["endlinedim"] * v_unit_vector
        B2 = ptB - params["endlinedim"] * (-v_unit_vector)
        dwg.add(dwg.line(B1, B2).stroke('black', width=2.5, linecap='square'))
        A3 = ptA - params["arrowlen"] * u_unit_vector
        B3 = ptB + params["arrowlen"] * u_unit_vector

        line = dwg.add(dwg.line(A3, ptA).stroke('black', width=2.5, linecap='square'))
        self.draw_end_arrow(line, smarker)
        # self.draw_start_arrow(line, emarker)
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width=2.5, linecap='butt'))
        self.draw_end_arrow(line, smarker)
        # self.draw_start_arrow(line, emarker)
        txt_pt = B3 + params["textoffset"] * u_unit_vector
        dwg.add(dwg.text(text, insert=(txt_pt), fill='black', font_family="sans-serif", font_size=28))

    def draw_oriented_arrow(self, dwg, pt, theta, orientation, offset, text_up, text_down):

        '''
        Drawing an arrow on given direction
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptA :
        :type NumPy Array
        :param theta: 
        :type theta : Int
        :param orientation :
        :type orientation : String
        :param offset :
        :type offset : float
        :param text_up :
        :type text_up : String
        :param text_down :
        :type text_up : String
        '''
        # Right Up.
        theta = math.radians(theta)
        char_width = 16
        x_vector = np.array([1, 0])
        y_vector = np.array([0, 1])
        p1 = pt
        lengthA = offset / math.sin(theta)

        arrow_vector = None
        if (orientation == "NE"):
            arrow_vector = np.array([-math.cos(theta), math.sin(theta)])
        elif (orientation == "NW"):
            arrow_vector = np.array([math.cos(theta), math.sin(theta)])
        elif (orientation == "SE"):
            arrow_vector = np.array([-math.cos(theta), -math.sin(theta)])
        elif (orientation == "SW"):
            arrow_vector = np.array([math.cos(theta), -math.sin(theta)])

        p2 = p1 - lengthA * arrow_vector

        text = text_down if len(text_down) > len(text_up) else text_up
        lengthB = len(text) * char_width

        label_vector = None
        if (orientation == "NE"):
            label_vector = -x_vector
        elif (orientation == "NW"):
            label_vector = x_vector
        elif (orientation == "SE"):
            label_vector = -x_vector
        elif (orientation == "SW"):
            label_vector = x_vector

        p3 = p2 + lengthB * (-label_vector)

        txt_offset = 18
        offset_vector = -y_vector

        txt_pt_up = None
        if (orientation == "NE"):
            txt_pt_up = p2 + 0.1 * lengthB * (-label_vector) + txt_offset * offset_vector
            txt_pt_down = p2 - 0.1 * lengthB * (label_vector) - (txt_offset + 15) * offset_vector
        elif (orientation == "NW"):
            txt_pt_up = p3 + 0.1 * lengthB * label_vector + txt_offset * offset_vector
            txt_pt_down = p3 - 0.1 * lengthB * label_vector - (txt_offset + 15) * offset_vector
        elif (orientation == "SE"):
            txt_pt_up = p2 + 0.1 * lengthB * (-label_vector) + txt_offset * offset_vector
            txt_pt_down = p2 - 0.1 * lengthB * (label_vector) - (txt_offset + 15) * offset_vector
        elif (orientation == "SW"):
            txt_pt_up = p3 + 0.1 * lengthB * label_vector + (txt_offset) * offset_vector
            txt_pt_down = p3 - 0.1 * lengthB * label_vector - (txt_offset + 10) * offset_vector

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill='none', stroke='black', stroke_width=2.5))

        emarker = self.add_e_marker(dwg)
        self.draw_start_arrow(line, emarker)

        dwg.add(dwg.text(text_up, insert=(txt_pt_up), fill='black', font_family="sans-serif", font_size=28))
        dwg.add(dwg.text(text_down, insert=(txt_pt_down), fill='black', font_family="sans-serif", font_size=28))

    def save_to_svg(self, filename, view):
        '''
         It returns the svg drawing depending upon connectivity
        CFBW = Column Flange Beam Web
        CWBW = Column Web Beam Web
        BWBW = Beam Web Beam Web
        '''
        fin_2d_front = Cleat2DCreatorFront(self)
        fin_2d_top = Cleat2DCreatorTop(self)
        fin_2d_side = Cleat2DCreatorSide(self)

        if self.connectivity == 'Column flange-Beam web':
            if view == "Front":
                fin_2d_front.call_CFBW_front(filename)
            elif view == "Side":
                fin_2d_side.call_CFBW_side(filename)
            elif view == "Top":
                fin_2d_top.call_CFBW_top(filename)
            else:
                filename = os.path.join(str(self.folder), "images_html", "cleatFront.svg")
                fin_2d_front.call_CFBW_front(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatFront.png"))

                filename = os.path.join(str(self.folder), "images_html", "cleatSide.svg")
                fin_2d_side.call_CFBW_side(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatSide.png"))


                filename = os.path.join(str(self.folder), "images_html", "cleatTop.svg")
                fin_2d_top.call_CFBW_top(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatTop.png"))


        elif self.connectivity == 'Column web-Beam web':
            if view == "Front":
                fin_2d_front.call_CWBW_front(filename)
            elif view == "Side":
                fin_2d_side.call_CWBW_side(filename)
            elif view == "Top":
                fin_2d_top.call_CWBW_top(filename)
            else:
                filename = os.path.join(str(self.folder), "images_html", "cleatFront.svg")
                fin_2d_front.call_CWBW_front(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatFront.png"))

                filename = os.path.join(str(self.folder), "images_html", "cleatSide.svg")
                fin_2d_side.call_CWBW_side(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatSide.png"))

                filename = os.path.join(str(self.folder), "images_html", "cleatTop.svg")
                fin_2d_top.call_CWBW_top(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatTop.png"))


        else:
            if view == "Front":
                fin_2d_front.call_BWBW_front(filename)
            elif view == "Side":
                fin_2d_side.call_BWBW_side(filename)
            elif view == "Top":
                fin_2d_top.call_BWBW_top(filename)
            else:
                filename = os.path.join(str(self.folder), "images_html", "cleatFront.svg")
                fin_2d_front.call_BWBW_front(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatFront.png"))

                filename = os.path.join(str(self.folder), "images_html", "cleatSide.svg")
                fin_2d_side.call_BWBW_side(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatSide.png"))

                filename = os.path.join(str(self.folder), "images_html", "cleatTop.svg")
                fin_2d_top.call_BWBW_top(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "cleatTop.png"))



class Cleat2DCreatorFront(object):
    def __init__(self, fin_common_obj):

        self.dataObj = fin_common_obj

        self.A2 = (self.dataObj.col_B, (self.dataObj.col_L - self.dataObj.D_beam) / 2)
        self.B = (self.dataObj.col_B, 0)
        self.A = (0, 0)
        self.D = (0, self.dataObj.col_L)
        self.C = (self.dataObj.col_B, self.dataObj.col_L)
        self.B2 = (self.dataObj.col_B, (self.dataObj.D_beam + self.dataObj.col_L) / 2)

        ptEx = (self.dataObj.col_B - self.dataObj.col_tw) / 2
        ptEy = 0.0
        self.E = (ptEx, ptEy)

        ptHx = (self.dataObj.col_B - self.dataObj.col_tw) / 2
        ptHy = self.dataObj.col_L
        self.H = (ptHx, ptHy)

        ptFx = (self.dataObj.col_B + self.dataObj.col_tw) / 2
        ptFy = 0
        self.F = (ptFx, ptFy)

        ptGx = (self.dataObj.col_B + self.dataObj.col_tw) / 2
        ptGy = self.dataObj.col_L
        self.G = np.array([ptGx, ptGy])

        # Draw rectangle for finPlate PRSU
        ptPx = (self.dataObj.col_B + self.dataObj.col_tw) / 2
        ptPy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.P = (ptPx, ptPy)
        self.ptP = np.array([ptPx, ptPy])

        self.U = self.ptP + (self.dataObj.cleat_ht * np.array([0, 1]))

        ptRx = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.cleat_legsize
        ptRy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.R = (ptRx, ptRy)

        ptSx = ptRx
        ptSy = ptPy + self.dataObj.cleat_ht
        self.S = (ptSx, ptSy)

        ptC1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap)
        ptC1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.C1 = np.array([ptC1x, ptC1y])

        ptA1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap)
        ptA1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        self.A1 = np.array([ptA1x, ptA1y])

        ptA3x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap) + self.dataObj.beam_L
        ptA3y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        self.A3 = (ptA3x, ptA3y)

        ptB3x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap) + self.dataObj.beam_L
        ptB3y = ((self.dataObj.col_L + self.dataObj.D_beam) / 2)
        self.B3 = (ptB3x, ptB3y)

        ptB1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap)
        ptB1y = ((self.dataObj.col_L + self.dataObj.D_beam) / 2)
        self.B1 = np.array([ptB1x, ptB1y])
        self.ptB1 = np.array([ptB1x, ptB1y])

        ptC2x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap)
        ptC2y = ptC1y + self.dataObj.cleat_ht
        self.C2 = (ptC2x, ptC2y)

        ptA5x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap)
        ptA5y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + self.dataObj.beam_T
        self.A5 = ptA5x, ptA5y

        ptA4x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap) + self.dataObj.beam_L
        ptA4y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + self.dataObj.beam_T
        self.A4 = (ptA4x, ptA4y)

        ptB4x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.gap) + self.dataObj.beam_L
        ptB4y = ((self.dataObj.col_L + self.dataObj.D_beam) / 2) - self.dataObj.beam_T
        self.B4 = (ptB4x, ptB4y)

        ptBx5 = ((self.dataObj.col_B + self.dataObj.col_tw) / 2) + self.dataObj.gap
        ptBy5 = ((self.dataObj.col_L + self.dataObj.D_beam) / 2) - self.dataObj.beam_T
        self.B5 = (ptBx5, ptBy5)

        ptP1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist)
        ptP1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + (self.dataObj.col_tw + self.dataObj.beam_R1 + 3) + self.dataObj.end_dist)
        self.P1 = (ptP1x, ptP1y)

        # ### Column flange points for column flange beam web connectivity #####

        from_plate_pt = self.dataObj.D_col + self.dataObj.gap  # 20 mm clear distance between colume and beam
        ptFAx = 0
        ptFAy = 0
        self.FA = (ptFAx, ptFAy)

        ptFEx = self.dataObj.col_T
        ptFEy = 0.0
        self.FE = (ptFEx, ptFEy)

        ptFFx = self.dataObj.D_col - self.dataObj.col_T
        ptFFy = 0.0
        self.FF = (ptFFx, ptFFy)

        ptFBx = self.dataObj.D_col
        ptFBy = 0.0
        self.FB = (ptFBx, ptFBy)

        ptFCx = self.dataObj.D_col
        ptFCy = self.dataObj.col_L
        self.FC = np.array([ptFBx, ptFCy])

        ptFGx = self.dataObj.D_col - self.dataObj.col_T
        ptFGy = self.dataObj.col_L
        self.FG = (ptFGx, ptFGy)

        ptFHx = self.dataObj.col_T
        ptFHy = self.dataObj.col_L
        self.FH = (ptFHx, ptFHy)

        ptFDx = 0.0
        ptFDy = self.dataObj.col_L
        self.FD = (ptFDx, ptFDy)

        ptFPx = self.dataObj.D_col
        ptFPy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FP = (ptFPx, ptFPy)
        self.ptFP = np.array([ptFPx, ptFPy])

        self.FW = self.FP + self.dataObj.cleat_thk * np.array([1, 0])

        ptFUx = self.dataObj.D_col
        ptFUy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        self.FU = (ptFUx, ptFUy)

        # FC1
        ptFC1x = from_plate_pt
        ptFC1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FC1 = np.array([ptFC1x, ptFC1y])

        # FC2
        ptFC2x = from_plate_pt
        ptFC2y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        self.FC2 = (ptFC2x, ptFC2y)

        # FA1
        ptFA1x = from_plate_pt
        ptFA1y = (self.dataObj.col_L - self.dataObj.D_beam) / 2
        self.FA1 = np.array([ptFA1x, ptFA1y])

        # FA4
        ptFA4x = from_plate_pt
        ptFA4y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.beam_T
        self.FA4 = ptFA4x, ptFA4y

        # FA2
        ptFA2x = ptFC1x + self.dataObj.beam_L
        ptFA2y = ptFA1y
        self.FA2 = np.array([ptFA2x, ptFA2y])

        # FA3
        ptFA3x = from_plate_pt + self.dataObj.beam_L
        ptFA3y = (((self.dataObj.col_L - self.dataObj.D_beam) / 2) + self.dataObj.beam_T)
        self.FA3 = ptFA3x, ptFA3y

        # FB3
        ptFB3x = from_plate_pt + self.dataObj.beam_L
        ptFB3y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB3 = (ptFB3x, ptFB3y)

        # FB2
        ptFB2x = from_plate_pt + self.dataObj.beam_L
        ptFB2y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam
        self.FB2 = ptFB2x, ptFB2y

        # FB1
        ptFB1x = self.dataObj.D_col + self.dataObj.gap
        ptFB1y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam
        self.FB1 = np.array([ptFB1x, ptFB1y])

        # FB4
        ptFB4x = from_plate_pt
        ptFB4y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB4 = ptFB4x, ptFB4y

        # #### Points for Beam-Beam connection ######

        # for primary beam
        self.BA = (0, 0)
        self.BB = self.BA + (self.dataObj.col_B) * np.array([1, 0])
        self.BC = self.BB + (self.dataObj.col_T) * np.array([0, 1])
        self.BD = self.BC - (self.dataObj.col_B - self.dataObj.col_tw) / 2 * np.array([1, 0])
        self.BE = self.BD + (self.dataObj.D_col - 2 * self.dataObj.col_T) * np.array([0, 1])
        self.BF = self.BC + (self.dataObj.D_col - 2 * self.dataObj.col_T) * np.array([0, 1])
        self.BG = self.BF + (self.dataObj.col_T) * np.array([0, 1])
        self.BH = self.BG - (self.dataObj.col_B) * np.array([1, 0])
        self.BI = self.BH - (self.dataObj.col_T) * np.array([0, 1])
        self.BJ = self.BI + (self.dataObj.col_B - self.dataObj.col_tw) / 2 * np.array([1, 0])
        self.BK = self.BJ - (self.dataObj.D_col - 2 * self.dataObj.col_T) * np.array([0, 1])
        self.BL = self.BI - (self.dataObj.D_col - 2 * self.dataObj.col_T) * np.array([0, 1])

        # for secondary beam
        self.D_notch = self.dataObj.col_T + self.dataObj.col_R1
        self.BA1 = self.BB + 10 * np.array([1, 0])
        self.BA2 = self.BA1 + (self.dataObj.beam_L - 10 - self.dataObj.col_B / 2 + self.dataObj.col_tw / 2 + self.dataObj.gap) * np.array([1, 0])
        self.BB2 = self.BA2 + self.dataObj.D_beam * np.array([0, 1])
        self.BB1 = self.BB2 - self.dataObj.beam_L * np.array([1, 0])
        self.BA4 = self.BA1 + self.dataObj.beam_T * np.array([0, 1])
        self.BA3 = self.BA2 + self.dataObj.beam_T * np.array([0, 1])
        self.BB3 = self.BB2 - self.dataObj.beam_T * np.array([0, 1])
        self.BB4 = self.BB1 - self.dataObj.beam_T * np.array([0, 1])
        self.BC1 = self.BB1 - (self.dataObj.D_beam - self.dataObj.notch_offset) * np.array([0, 1])
        self.BC2 = self.BC1 + self.dataObj.cleat_ht * np.array([0, 1])
        self.BA5 = self.BA1 + self.dataObj.notch_offset * np.array([0, 1])

        # for cleat angle

        self.BP = self.BC1 - self.dataObj.gap * np.array([1, 0])
        self.BQ = self.BP + self.dataObj.cleat_thk * np.array([1, 0])
        self.BR = self.BP + self.dataObj.cleat_legsize * np.array([1, 0])
        self.BP1 = self.BP + self.dataObj.cleat_ht * np.array([0, 1])
        self.BQ1 = self.BP1 + self.dataObj.cleat_thk * np.array([1, 0])
        self.BR1 = self.BP1 + self.dataObj.cleat_legsize * np.array([1, 0])

    def call_BWBW_front(self, filename):
        v_height = self.dataObj.D_col + 850
        pt1 = self.BA5 - self.dataObj.col_R1 * np.array([0, 1])
        #         dwg = svgwrite.Drawing(filename, size=('1200mm', '1225mm'), viewBox=('-500 -250 1500 1225'))
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-350 -400 1300 1300'))

        # ################ Cross section A-A ##################
        ptSecA = self.BA + (320 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.BA2 + (320 * np.array([0, -1]))
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        #############################################################################
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))
        dwg.add(dwg.polyline(
            points=[(self.BA), (self.BB), (self.BC), (self.BD), (self.BE), (self.BF), (self.BG), (self.BH), (self.BI), (self.BJ), (self.BK), (self.BL),
                    (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        #         dwg.add(dwg.polyline(points = [(self.BC1),(self.BA5),(self.BA1),(self.BA2),(self.BB2),(self.BB1),(self.BB4),(self.BC2)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
        dwg.add(
            dwg.polyline(points=[(pt1), (self.BA1), (self.BA2), (self.BB2), (self.BB1), (self.BB4), (self.BC2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BC1), (self.BC2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BA4), (self.BA3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BB4), (self.BB3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BQ), size=((self.dataObj.cleat_legsize - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill='none', stroke='blue',
                         stroke_width=2.5))
        #         "M10 10 C 20 20, 40 20, 50 10"
        pt1 = self.BA5 - self.dataObj.col_R1 * np.array([0, 1])
        pt2 = self.BA5 - self.dataObj.col_R1 * np.array([1, 0])

        d = []
        d.append("M")
        d.append(pt1)
        d.append("A")
        d.append(np.array([self.dataObj.col_R1, self.dataObj.col_R1]))
        d.append(",")
        d.append("0")
        d.append(",")
        d.append("0")
        d.append(",")
        d.append("1")
        d.append(",")
        d.append(pt2)
        dwg.add(dwg.path(d=d, stroke="blue", fill="none", stroke_width="2.5"))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        nr_c = self.dataObj.no_of_crows
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list_c = []

        for i in range(1, (nr + 1)):
            col_list = []
            for j in range(1, (nc + 1)):
                pt = self.BP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1, 0]) + self.dataObj.edge_dist * np.array([0, 1]) + \
                     (i - 1) * self.dataObj.pitch * np.array([0, 1]) + (j - 1) * self.dataObj.gauge * np.array([-1, 0])
                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1, 0])
                PtD = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line((ptC), (PtD)).stroke('red', width=2.0, linecap='square'))

                ptE = pt - (bolt_r + 4) * np.array([0, 1])
                PtF = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line((ptE), (PtF)).stroke('red', width=2.0, linecap='square'))
                col_list.append(pt)
            pt_list.append(col_list)

        for i in range(1, (nr_c + 1)):
            pt_c = self.BP + self.dataObj.cedge_dist * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0]) + (i - 1) * self.dataObj.cpitch * np.array(
                [0, 1])
            pt1_c = pt_c - bolt_r * np.array([0, 1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width), fill="black", stroke='black', stroke_width=2.0))
            pt_B1 = pt_c - 10 * np.array([1, 0])
            pt_B2 = pt_c + (self.dataObj.col_T + self.dataObj.cleat_thk + 10) * np.array([1, 0])
            dwg.add(dwg.line((pt_B1), (pt_B2)).stroke('black', width=2.0, linecap='square'))
            pt_list_c.append(pt_c)

        pitch_pts = []
        for row in pt_list:
            if len(row) > 0:
                pitch_pts.append(row[0])

                # Included cleat height and pitch details of column bolt group
                # Drawing faint lines at right top and bottom corners of cleat
        rt2 = self.BR + (self.dataObj.beam_L + 150 - self.dataObj.gauge) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.BR, rt2, dwg)
        #         rb1 = rt1 + self.dataObj.cleat_ht * np.array([0,1])
        rb2 = rt2 + self.dataObj.cleat_ht * np.array([0, 1])
        self.dataObj.draw_faint_line(self.BR1, rb2, dwg)
        # drawing inner arrow to represent cleat height
        params = {"offset": self.dataObj.beam_L, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BR, self.BR1, str(int(self.dataObj.cleat_ht)), params)

        # ########################### BEAM CONNECTIVITY MARKING ###############################
        # Drawing faint lines at bolt groups on Beam
        bt1 = np.array(pt_list[0][0])
        bt2 = bt1 + (self.dataObj.beam_L + 150) * np.array([1, 0])
        self.dataObj.draw_faint_line(bt1, bt2, dwg)
        bb1 = np.array(pt_list[-1][0])
        bb2 = bb1 + (self.dataObj.beam_L + 150) * np.array([1, 0])
        self.dataObj.draw_faint_line(bb1, bb2, dwg)

        # ###### drawing outer arrow on beam bolt group to represent pitch and end distance ##########
        # pitch @ no_of_beam_bolt_row
        params = {"offset": self.dataObj.beam_L + 150, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt1, bb1, str(len(pitch_pts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)
        # end distance
        bt2 = bt1 - self.dataObj.edge_dist * np.array([0, 1])
        params = {"offset": self.dataObj.beam_L + 150, "textoffset": 10, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt1, bt2, str(self.dataObj.edge_dist), params)
        # end Distance
        bb2 = bb1 + self.dataObj.edge_dist * np.array([0, 1])
        params = {"offset": self.dataObj.beam_L + 150, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bb1, bb2, str(self.dataObj.edge_dist), params)

        # Gauge Distance when two lines of bolts present
        # Outer arrow to represent gauge 
        # faint line at top of second column bolt
        if self.dataObj.no_of_col > 1:
            A = self.BP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1, 0])
            B = A - self.dataObj.gauge * np.array([1, 0])
            offset = self.dataObj.notch_offset + 100  # #NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC
            # Faint line on second lines of bolt
            B_up = B - offset * np.array([0, 1])
            self.dataObj.draw_faint_line(B, B_up, dwg)
            params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, A, B, str(int(self.dataObj.gauge)), params)

        # Faint lines and outer arrow for edge distance--RIGHT TO THE ABOVE DRAWN FAINT LINE AND OUTER ARROW
        v_offset = self.dataObj.col_T + self.dataObj.col_R1
        BR_left = self.BR - self.dataObj.end_dist * np.array([1, 0])
        BR_left_up = BR_left - ((v_offset) + 180) * np.array([0, 1])  # #NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC  
        BR_up = self.BR - ((v_offset) + 180) * np.array([0, 1])  # #NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC     
        self.dataObj.draw_faint_line(BR_left, BR_left_up, dwg)
        self.dataObj.draw_faint_line(self.BR, BR_up, dwg)
        offset = ((v_offset) + 180)  # #NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC     
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BR, BR_left, str(int(self.dataObj.end_dist)), params)

        # ##################COLUMN CONNECTIVITY MARKING#####################
        # Draw Faint Line To Represent Distance Between Beam Flange and Cleat Angle.
        length = (self.dataObj.beam_B - self.dataObj.beam_tw) / 2
        # v_offset = self.dataObj.col_T + self.dataObj.col_R1  # #NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC
        v_offset = self.dataObj.notch_offset
        BA_down = self.BA + v_offset * np.array([0, 1])
        BA_left = self.BA - 30 * np.array([1, 0])
        BA_left_down = BA_left + v_offset * np.array([0, 1])
        self.dataObj.draw_faint_line(self.BA, BA_left, dwg)
        self.dataObj.draw_faint_line(self.BC1, BA_left_down, dwg)
        # #Arrow Dimension NEED TO BE CHANGED AFTER CONSIDERING THE CONDITIONS FROM JSC  
        params = {"offset": 30, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BA, BA_down, str(int(v_offset)), params)

        # Draw Faint Line To Represent column pitch and end Distance.
        self.dataObj.draw_faint_line(self.BP, self.BP - (length + 30 + self.dataObj.beam_tw) * np.array([1, 0]), dwg)
        self.dataObj.draw_faint_line(np.array(pt_list_c[0]), np.array(pt_list_c[0]) - (length + 30) * np.array([1, 0]), dwg)
        offset = length + 30
        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        BP_left = self.BP - self.dataObj.col_tw * np.array([1, 0])
        self.dataObj.draw_dimension_outer_arrow(dwg, BP_left, np.array(pt_list_c[0]), str(int(self.dataObj.cedge_dist)), params)
        self.dataObj.draw_faint_line(np.array(pt_list_c[-1]), np.array(pt_list_c[-1]) - (length + 30) * np.array([1, 0]), dwg)
        offset = length + 30
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), np.array(pt_list_c[-1]),
                                                str(len(pt_list_c) - 1) + "@" + str(int(self.dataObj.cpitch)) + ' c/c', params)
        self.dataObj.draw_faint_line(self.BP1, self.BP1 - (length + 30 + self.dataObj.beam_tw) * np.array([1, 0]), dwg)
        offset = length + 30
        BP1_left = self.BP1 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, BP1_left, np.array(pt_list_c[-1]), str(int(self.dataObj.cedge_dist)), params)

        # ##################### BEAM designation and number bolt information ##############
        # SUPORTED BEAM Designation
        beam_pt = self.BB2
        theta = 45
        offset = 20
        text_up = ""
        text_down = "Beam " + self.dataObj.beam_Designation  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION

        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # SUPORTING BEAM Designation
        beam_pt1 = self.BA
        theta = 90
        offset = 100
        text_up = "Beam " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt1, theta, "NW", offset, text_up, text_down)

        #  Secondary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col

        bolt_pt_x = np.array(pt_list[0][0])
        theta = 55
        offset = (self.dataObj.D_beam * 3) / 8 + 75  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"
        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(
        #     self.dataObj.bolt_grade) + ')'  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down)

        # Primary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol
        bolt_pt = np.array(pt_list_c[-1])
        theta = 70
        offset = (self.dataObj.D_col - self.dataObj.D_beam)  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(
        #     self.dataObj.bolt_grade) + ')'  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt, theta, "SE", offset, text_up, text_down)

        # cleat angle information
        cleat_pt = self.BR1
        theta = 60
        offset = (self.dataObj.D_beam/2 + 10)
        text_up = ""
        text_down = "ISA." + str(int(self.dataObj.cleat_legsize)) + "X" + str(int(self.dataObj.cleat_legsize_1)) + "X" + str(int(self.dataObj.cleat_thk))
        self.dataObj.draw_oriented_arrow(dwg, cleat_pt, theta, "SE", offset, text_up, text_down)

        # 2D view name
        ptx = self.BH + 100 * np.array([0, 1])
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        ptx = self.BH + 140 * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CFBW_front(self, filename):
        v_width = self.dataObj.D_col + 1300
        dwg = svgwrite.Drawing(filename, size=('1200mm', '1225mm'), viewBox=('-500 -350 ' + str(v_width) + ' 1450'))
        dwg.add(dwg.polyline(points=[(self.FA), (self.FB), (self.FC), (self.FD), (self.FA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.FE), (self.FH)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FF), (self.FG)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.FC1), (self.FA1), (self.FA2), (self.FB2), (self.FB1), (self.FC2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.FC1), (self.FC2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.FA4), (self.FA3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FB4), (self.FB3)).stroke('blue', width=2.5, linecap='square'))


        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FW), size=(self.dataObj.cleat_legsize - self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue',
                         stroke_width=2.5))
        # dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.cleat_legsize, self.dataObj.cleat_ht),fill = 'none', stroke='blue', stroke_width=2.5))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        nr_c = self.dataObj.no_of_crows
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list_c = []

        for i in range(1, (nr + 1)):
            col_list = []
            for j in range(1, (nc + 1)):
                pt = self.ptFP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1, 0]) + self.dataObj.edge_dist * np.array([0, 1]) + \
                     (i - 1) * self.dataObj.pitch * np.array([0, 1]) + (j - 1) * self.dataObj.gauge * np.array([-1, 0])
                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1, 0])
                PtD = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line((ptC), (PtD)).stroke('red', width=2.0, linecap='square'))

                ptE = pt - (bolt_r + 4) * np.array([0, 1])
                PtF = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line((ptE), (PtF)).stroke('red', width=2.0, linecap='square'))
                col_list.append(pt)
            pt_list.append(col_list)

        for i in range(1, (nr_c + 1)):
            pt_c = self.ptFP + self.dataObj.cedge_dist * np.array([0, 1]) - self.dataObj.col_T * np.array([1, 0]) + (i - 1) * self.dataObj.cpitch * np.array(
                [0, 1])
            pt1_c = pt_c - bolt_r * np.array([0, 1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.col_T + self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width), fill="black", stroke='black', stroke_width=2.0))
            pt_B1 = pt_c - 10 * np.array([1, 0])
            pt_B2 = pt_c + (self.dataObj.col_T + self.dataObj.cleat_thk + 10) * np.array([1, 0])
            dwg.add(dwg.line((pt_B1), (pt_B2)).stroke('black', width=2.0, linecap='square'))
            pt_list_c.append(pt_c)

        pitch_pts = []
        for row in pt_list:
            if len(row) > 0:
                pitch_pts.append(row[0])

                # Cross section A-A
        ptSecA = self.FA + (270 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        # Included cleat height and pitch details of column bolt group
        # Drawing faint lines at right top and bottom corners of cleat--AT BEAM
        rt1 = self.FP + self.dataObj.cleat_legsize * np.array([1, 0])
        rt2 = rt1 + (self.dataObj.beam_L + 225 - self.dataObj.gauge) * np.array([1, 0])
        self.dataObj.draw_faint_line(rt1, rt2, dwg)
        rb1 = rt1 + self.dataObj.cleat_ht * np.array([0, 1])
        rb2 = rt2 + self.dataObj.cleat_ht * np.array([0, 1])
        self.dataObj.draw_faint_line(rb1, rb2, dwg)
        # drawing inner arrow for the above drawn faint lines
        params = {"offset": self.dataObj.beam_L, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, rt1, rb1, str(int(self.dataObj.cleat_ht)), params)
        # Drawing faint lines at bolt groups on Beam
        bt1 = np.array(pt_list[0][0])
        bt2 = bt1 + (self.dataObj.beam_L + 225) * np.array([1, 0])
        self.dataObj.draw_faint_line(bt1, bt2, dwg)
        bb1 = np.array(pt_list[-1][0])
        bb2 = bb1 + (self.dataObj.beam_L + 225) * np.array([1, 0])
        self.dataObj.draw_faint_line(bb1, bb2, dwg)

        # drawing inner arrow beam bolt group
        params = {"offset": self.dataObj.beam_L + 225, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt1, bb1, str(len(pitch_pts) - 1) + "@" + str(int(self.dataObj.pitch)) + "c/c", params)

        bt2 = bt1 - self.dataObj.edge_dist * np.array([0, 1])
        params = {"offset": self.dataObj.beam_L + 225, "textoffset": 10, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt1, bt2, str(self.dataObj.edge_dist), params)

        bb2 = bb1 + self.dataObj.edge_dist * np.array([0, 1])
        params = {"offset": self.dataObj.beam_L + 225, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bb1, bb2, str(self.dataObj.edge_dist), params)

        # end distance and edge distance are........DONE 
        params = {"offset": self.dataObj.D_col + 50, "textoffset": 145, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), np.array(pt_list_c[-1]),
                                                str(len(pt_list_c) - 1) + u' \u0040' + str(int(self.dataObj.cpitch)) + " c/c", params)

        # Distance between Beam Flange and Plate
        params = {"offset": self.dataObj.D_col + self.dataObj.gap + self.dataObj.col_T + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.FA1, self.FC1, str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)), params)

        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        pt_one = self.FA1
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        pt_two = (ptBx, ptBy)
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        # End Distance from the starting point of plate Information

        edgPt = self.FP - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + 50, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), edgPt, str(int(self.dataObj.cedge_dist)), params)

        # Edge Distance from plate end point.
        edgPt1 = self.FU - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[-1]), edgPt1, str(int(self.dataObj.cedge_dist)), params)

        #         End Distance information.DO SOME ADJUSTMENTS HERE IN Y-CORDINATE
        pt1A = self.FP + self.dataObj.cleat_legsize * np.array([1, 0])
        pt1B = pt1A - self.dataObj.end_dist * np.array([1, 0])
        offset = self.dataObj.edge_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3
        params = {"offset": self.dataObj.D_beam / 2 + self.dataObj.edge_dist - 50, "textoffset": 10, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt1A, pt1B, str(int(self.dataObj.end_dist)), params)

        # ##Faint Lines ######
        A = self.FP + (self.dataObj.cleat_legsize) * np.array([1, 0])
        A_up = A - (self.dataObj.D_beam / 2 + self.dataObj.edge_dist - 50) * np.array([0, 1])
        self.dataObj.draw_faint_line(A, A_up, dwg)
        A_left = A - self.dataObj.end_dist * np.array([1, 0])
        A_left_up = A_left - (self.dataObj.D_beam / 2 + self.dataObj.edge_dist - 50) * np.array([0, 1])
        self.dataObj.draw_faint_line(A_left, A_left_up, dwg)

        # Gauge Distance when two lines of bolts present
        if self.dataObj.no_of_col > 1:
            A = self.FP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1, 0])
            B = A - self.dataObj.gauge * np.array([1, 0])
            offset = (self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + self.dataObj.edge_dist) + 50
            params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, A, B, str(int(self.dataObj.gauge)), params)
            FA = self.FP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1, 0])
            FB = FA + ((self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 130) * np.array([0, -1])
            FA_left = self.FP + (self.dataObj.cleat_legsize - self.dataObj.end_dist - self.dataObj.gauge) * np.array([1, 0])
            FB_left = FA_left + ((self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 130) * np.array([0, -1])
            #             self.dataObj.draw_faint_line(FA, FB, dwg)
            self.dataObj.draw_faint_line(FA_left, FB_left, dwg)

        # Gap Distance
        gap_pt = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3))
        ptG1 = self.ptFP + (gap_pt + 30) * np.array([0, 1])
        ptG2 = self.FC1 + (gap_pt + 30) * np.array([0, 1])
        offset = self.dataObj.col_L  # 60% of the column length
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.dataObj.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.dataObj.gap), params)

        # Draw Faint line for Gap Distance
        ptC1 = self.FC
        ptC2 = ptC1 + 40 * np.array([0, 1])
        self.dataObj.draw_faint_line(ptC1, ptC2, dwg)

        ptD1 = self.FB1
        ptD2 = ptD1 + 240 * np.array([0, 1])
        self.dataObj.draw_faint_line(ptD1, ptD2, dwg)

        # The first line on the cleat for column
        ptA = self.FP
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptB = (ptBx, ptBy)
        self.dataObj.draw_faint_line(ptA, ptB, dwg)

        pt1 = np.array(pt_list_c[0])
        ptBx = -30
        ptBy1 = ptBy + self.dataObj.cedge_dist
        pt2 = (ptBx, ptBy1)
        self.dataObj.draw_faint_line(pt1, pt2, dwg)

        pt_one = np.array(pt_list_c[-1])
        ptBx = -30
        ptBy1 = ptBy1 + (len(pt_list_c) - 1) * self.dataObj.cpitch
        pt_two = (ptBx, ptBy1)
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        pt_one = self.FU
        ptBx = -30
        ptBy1 = ptBy1 + self.dataObj.cedge_dist
        pt_two = (ptBx, ptBy1)
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        # Beam Information
        beam_pt = self.FA1 + self.dataObj.D_beam * np.array([0, 1])
        theta = 45
        offset = (self.dataObj.D_beam / 2 )
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # Column Designation
        ptx = self.dataObj.D_col / 3
        pty = 0
        pt = np.array([ptx, pty])
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.beam_L) /5.5
        text_up = "Column " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, pt, theta, "NW", offset, text_up, text_down)

        # Bolt Information for beam part
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col

        bolt_pt_x = np.array(pt_list[0][0])
        theta = 45
        offset = (self.dataObj.D_beam * 3) / 8
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M " + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(
        #     self.dataObj.bolt_grade) + ')'  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down)

        # Bolt Information for column part
        no_of_bolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2
        bolt_pt_x = np.array(pt_list_c[-1])
        theta = 60
        offset = (self.dataObj.D_col + 10)
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M " + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(
        #     self.dataObj.bolt_grade) + ')'  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "SW", offset, text_up, text_down)

        # cleat angle information
        plate_pt_x = self.dataObj.D_col + self.dataObj.cleat_legsize / 2
        plate_pt_y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        plate_pt = np.array([plate_pt_x, plate_pt_y])
        theta = 45
        offset = (self.dataObj.D_beam - self.dataObj.beam_T - self.dataObj.cleat_ht) + 50
        text_up = "ISA." + str(int(self.dataObj.cleat_legsize)) + "X" + str(int(self.dataObj.cleat_legsize_1)) + "X" + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plate_pt, theta, "SE", offset, text_up, text_down)

        # 2D view name
        ptx = self.FG + (self.dataObj.col_B/2) * np.array([0, 1])  # 1150
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        # # All dimensions in "mm"
        ptx = self.FG + (self.dataObj.col_B/2 + 40) * np.array([0, 1])   # + 2000 * np.array([0, 1])  # 1150

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CWBW_front(self, filename):
        v_width = self.dataObj.col_B / 2 + self.dataObj.gap + self.dataObj.beam_L + 1000
        dwg = svgwrite.Drawing(filename, size=('1250mm', '1240mm'), viewBox=('-510 -400 1600 1700'))

        ptSecA = self.A + (280 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.beam_B / 2 + 30 + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.A2), (self.B), (self.A), (self.D), (self.C), (self.B2)], stroke='blue', fill='none', stroke_width=2.5))

        dwg.add(dwg.line((self.E), (self.H)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.F), (self.G)).stroke('blue', width=2.5, linecap='square'))

        # Diagonal Hatching to represent WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(4, 4), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=0.7))

        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill="none", stroke='blue', stroke_width=2.0))
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.cleat_legsize, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))

        # C1,A1,A3,B3,B1,C2
        dwg.add(dwg.polyline(points=[(self.C1), (self.A1), (self.A3), (self.B3), (self.B1), (self.C2)], stroke='blue', fill='none', stroke_width=2.5))
        # C1,C2
        dwg.add(dwg.line((self.C1), (self.C2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        # A2,B2
        dwg.add(dwg.line((self.A2), (self.B2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.line((self.A5), (self.A4)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.B5), (self.B4)).stroke('blue', width=2.5, linecap='square'))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        nr_c = self.dataObj.no_of_crows
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list_c = []

        for i in range(1, (nr + 1)):
            col_list = []
            for j in range(1, (nc + 1)):
                pt = self.ptP + (self.dataObj.cleat_legsize - self.dataObj.end_dist) * np.array([1, 0]) + self.dataObj.edge_dist * np.array([0, 1]) + \
                     (i - 1) * self.dataObj.pitch * np.array([0, 1]) + (j - 1) * self.dataObj.gauge * np.array([-1, 0])
                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1, 0])
                PtD = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line((ptC), (PtD)).stroke('red', width=2.0, linecap='square'))
                ptE = pt - (bolt_r + 4) * np.array([0, 1])
                ptF = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line((ptE), (ptF)).stroke('blue', width=1.5, linecap='square').dasharray(dasharray=([20, 5, 1, 5])))
                col_list.append(pt)
            pt_list.append(col_list)

        for i in range(1, (nr_c + 1)):
            pt_c = self.ptP + self.dataObj.cedge_dist * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0]) + (i - 1) * self.dataObj.cpitch * np.array(
                [0, 1])
            pt1_c = pt_c - bolt_r * np.array([0, 1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width), fill="black", stroke='black', stroke_width=2.0))

            pt_list_c.append(pt_c)

        pitch_pts = []
        for row in pt_list:
            if len(row) > 0:
                pitch_pts.append(row[0])

            #     cleat Angle  Information
        plate_pt_x = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.cleat_legsize / 2
        plate_pt_y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.cleat_ht
        plate_pt = np.array([plate_pt_x, plate_pt_y])
        theta = 45
        offset = (self.dataObj.D_beam + 100) / 2
        text_up = "ISA. " + str(int(self.dataObj.cleat_legsize)) + "X" + str(int(self.dataObj.cleat_legsize_1)) + "X" + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plate_pt, theta, "SE", offset, text_up, text_down)

        # Column Designation
        ptx = self.dataObj.col_B / 3
        pty = 0
        pt = np.array([ptx, pty])
        theta = 90
        offset = 100
        text_up = "Column " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, pt, theta, "NW", offset, text_up, text_down)

        # Beam Information marking arrow
        beam_pt = self.B1
        theta = 60
        offset = 250
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # beam Bolt Information arrow
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        bolt_pt_x = np.array(pt_list[0][0])
        theta = 45
        offset = (self.dataObj.col_L - self.dataObj.D_beam) /2
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down)

        # column bolt marking Arrow
        no_of_cbolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2
        theta = 65
        offset = (self.dataObj.col_B * 3) / 4
        text_up = str(no_of_cbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.draw_oriented_arrow(dwg, np.array(pt_list_c[0]), theta, "NW", offset, text_up, text_down)

        # Included cleat height and pitch details of column bolt group
        # Drawing faint lines at right top and bottom corners of cleat--AT BEAM
        rt1 = self.P + self.dataObj.cleat_legsize * np.array([1, 0])
        rt2 = rt1 + (self.dataObj.beam_L + 275 - self.dataObj.gauge) * np.array([1, 0])
        self.dataObj.draw_faint_line(rt1, rt2, dwg)
        rb1 = rt1 + self.dataObj.cleat_ht * np.array([0, 1])
        rb2 = rt2 + self.dataObj.cleat_ht * np.array([0, 1])
        self.dataObj.draw_faint_line(rb1, rb2, dwg)

        # drawing inner arrow for the above drawn faint lines
        params = {"offset": self.dataObj.beam_L, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, rt1, rb1, str(int(self.dataObj.cleat_ht)), params)

        # Drawing faint lines at bolt groups on column
        bt1 = np.array(pt_list[0][0])
        bt2 = bt1 + (self.dataObj.beam_L + 275) * np.array([1, 0])
        self.dataObj.draw_faint_line(bt1, bt2, dwg)
        bb1 = np.array(pt_list[-1][0])
        bb2 = bb1 + (self.dataObj.beam_L + 275) * np.array([1, 0])
        self.dataObj.draw_faint_line(bb1, bb2, dwg)

        # drawing outer arrow beam bolt group
        params = {"offset": self.dataObj.beam_L + 275, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt1, bb1, str(len(pt_list) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)

        bt2 = bt1 - self.dataObj.edge_dist * np.array([0, 1])
        params = {"offset": self.dataObj.beam_L + 275, "textoffset": 10, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt1, bt2, str(self.dataObj.edge_dist), params)

        bb2 = bb1 + self.dataObj.edge_dist * np.array([0, 1])
        params = {"offset": self.dataObj.beam_L + 275, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bb1, bb2, str(self.dataObj.edge_dist), params)

        # ###Column bolt group and related dimension marking
        # The first line on the cleat for column
        ptA = self.P
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptB = (ptBx, ptBy)
        self.dataObj.draw_faint_line(ptA, ptB, dwg)

        # Faint lines for column bolt group and edge distances  
        pt1 = np.array(pt_list_c[0])
        ptBx = -30
        ptBy1 = ptBy + self.dataObj.cedge_dist
        pt2 = (ptBx, ptBy1)
        self.dataObj.draw_faint_line(pt1, pt2, dwg)

        pt_one = np.array(pt_list_c[-1])
        ptBx = -30
        ptBy1 = ptBy1 + (len(pt_list_c) - 1) * self.dataObj.cpitch
        pt_two = (ptBx, ptBy1)
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        pt_one = self.U
        ptBx = -30
        ptBy1 = ptBy1 + self.dataObj.cedge_dist
        pt_two = (ptBx, ptBy1)
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)
        # Outer arrow for the pitch,edge distance marking
        # Related to the above drawn faint line
        # drawing inner arrow beam bolt group
        params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw) / 2 + 30, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), pt_list_c[-1],
                                                str(len(pt_list_c) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)

        bt2 = self.P - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw) / 2 + 30, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, bt2, np.array(pt_list_c[0]), str(int(self.dataObj.cedge_dist)), params)

        params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw) / 2 + 30, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt_list_c[-1], self.P + self.dataObj.cleat_ht * np.array([0, 1]) - self.dataObj.col_tw,
                                                str(int(self.dataObj.cedge_dist)), params)

        # faint lines and outer arrow for the edge distance--AT BEAM
        rt = self.P + self.dataObj.cleat_legsize * np.array([1, 0])
        rt1 = rt - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + 60) * np.array([0, 1])
        rt_left = rt - self.dataObj.end_dist * np.array([1, 0])
        rt_left_top = rt_left - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + 60) * np.array([0, 1])
        self.dataObj.draw_faint_line(rt, rt1, dwg)
        self.dataObj.draw_faint_line(rt_left, rt_left_top, dwg)
        params = {"offset": (self.dataObj.col_L - self.dataObj.D_beam) / 2 + 60, "textoffset": 10, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, rt, rt_left, str(int(self.dataObj.end_dist)), params)

        # faint lines and outer arrow for beam gauge representation for double lines of bolts
        if self.dataObj.no_of_col > 1:
            rt_left_left = rt_left - self.dataObj.gauge * np.array([1, 0])  # make center line of bolts
            rt_left_left_top = rt_left_left - (self.dataObj.beam_T + self.dataObj.beam_R1 + 130) * np.array([0, 1])
            self.dataObj.draw_faint_line(rt_left_left, rt_left_left_top, dwg)
            params = {"offset": (self.dataObj.col_B - self.dataObj.col_tw) / 2 + 15, "textoffset": 10, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, rt_left, rt_left_left, str(int(self.dataObj.gauge)), params)

        # 2D view name
        ptx = self.D + (self.dataObj.beam_B) * np.array([0, 1])  # 1090
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        # # All dimensions in "mm"
        ptx2 = self.D + (self.dataObj.beam_B + 40) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx2), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()


class Cleat2DCreatorTop(object):
    def __init__(self, fin_common_obj):

        self.dataObj = fin_common_obj
        self.A = np.array([0, 0])
        self.B = np.array([0, 0]) + (self.dataObj.col_B) * np.array([1, 0])
        self.C = self.B + (self.dataObj.col_T) * np.array([0, 1])
        self.D = self.A + (self.dataObj.col_B + self.dataObj.col_tw) / 2 * np.array([1, 0]) + (self.dataObj.col_T) * np.array([0, 1])
        self.E = self.A + (self.dataObj.col_B + self.dataObj.col_tw) / 2 * np.array([1, 0]) + (self.dataObj.D_col - self.dataObj.col_T) * np.array([0, 1])
        self.F = self.B + (self.dataObj.D_col - self.dataObj.col_T) * np.array([0, 1])
        self.G = self.B + (self.dataObj.D_col) * np.array([0, 1])
        self.H = self.A + (self.dataObj.D_col) * np.array([0, 1])
        self.I = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([0, 1])
        self.J = self.E - (self.dataObj.col_tw) * np.array([1, 0])
        self.K = self.D - (self.dataObj.col_tw) * np.array([1, 0])
        self.L = self.A + (self.dataObj.col_T) * np.array([0, 1])
        self.A7 = self.A + (self.dataObj.col_B / 2 + self.dataObj.col_tw / 2 + self.dataObj.gap) * np.array([1, 0]) + (
                                                                                                                      self.dataObj.D_col / 2 - self.dataObj.beam_tw / 2) * np.array(
            [0, 1])

        self.A1 = self.A7 + (self.dataObj.beam_B / 2 - self.dataObj.beam_tw / 2) * np.array([0, -1])
        self.A4 = self.A1 + self.dataObj.beam_B * np.array([0, 1])
        self.A5 = self.A7 - 20 * np.array([1, 0])
        self.A8 = self.A7 + (self.dataObj.beam_L) * np.array([1, 0])
        self.P1 = self.A1 + (self.dataObj.beam_B + self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.A6 = self.P1 + (self.dataObj.beam_L) * np.array([1, 0])
        self.P = self.P1 - self.dataObj.gap * np.array([1, 0])
        self.P2 = self.P + (self.dataObj.cleat_legsize) * np.array([1, 0])
        self.P3 = self.P2 + (self.dataObj.cleat_thk) * np.array([0, 1])
        self.P6 = self.P3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1, 0])
        self.P5 = self.P6 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0, 1])
        self.P4 = self.P5 - (self.dataObj.cleat_thk) * np.array([1, 0])
        self.P7 = self.P1 + (self.dataObj.cleat_thk) * np.array([0, 1])
        self.Q = self.P1 - self.dataObj.gap * np.array([1, 0]) - (self.dataObj.beam_tw) * np.array([0, 1])
        self.Q1 = self.Q + (self.dataObj.gap) * np.array([1, 0])
        self.Q2 = self.Q + (self.dataObj.cleat_legsize) * np.array([1, 0])
        self.Q3 = self.Q2 - (self.dataObj.cleat_thk) * np.array([0, 1])
        self.Q7 = self.Q1 - (self.dataObj.cleat_thk) * np.array([0, 1])
        self.Q6 = self.Q3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1, 0])
        self.Q5 = self.Q6 - (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0, 1])
        self.Q4 = self.Q5 - (self.dataObj.cleat_thk) * np.array([1, 0])

        # Weld Triangle

        self.ptP = self.P + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.O = self.P + self.dataObj.cleat_thk * np.array([1, 0])
        self.ptO = self.O + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.R = self.P + self.dataObj.cleat_thk * np.array([0, -1])
        self.ptR = self.R + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])

        self.X = self.P + (self.dataObj.cleat_thk) * np.array([0, 1])
        self.ptX = self.X + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.Y = self.X + (self.dataObj.cleat_thk) * np.array([0, 1])
        self.ptY = self.Y + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.Z = self.X + (self.dataObj.cleat_thk) * np.array([1, 0])
        self.ptZ = self.Z + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])

        # ### CFBW connectivity points
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.dataObj.col_T * np.array([1, 0])
        self.FC = self.FB + (self.dataObj.col_B - self.dataObj.col_tw) / 2 * np.array([0, 1])
        self.FD = self.FC + (self.dataObj.D_col - 2 * (self.dataObj.col_T)) * np.array([1, 0])
        self.FE = self.FA + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.FF = self.FA + self.dataObj.D_col * np.array([1, 0])
        self.FG = self.FF + self.dataObj.col_B * np.array([0, 1])
        self.FH = self.FG + self.dataObj.col_T * np.array([-1, 0])
        self.FI = self.FD + self.dataObj.col_tw * np.array([0, 1])
        self.FJ = self.FC + self.dataObj.col_tw * np.array([0, 1])
        self.FK = self.FB + self.dataObj.col_B * np.array([0, 1])
        self.FL = self.FK + self.dataObj.col_T * np.array([-1, 0])
        self.FA7 = self.FA + (self.dataObj.D_col + self.dataObj.gap) * np.array([1, 0]) + (self.dataObj.col_B / 2 - self.dataObj.beam_tw / 2) * np.array([0, 1])
        self.FA1 = self.FA7 + (self.dataObj.beam_B / 2 - self.dataObj.beam_tw / 2) * np.array([0, -1])
        self.FA4 = self.FA1 + self.dataObj.beam_B * np.array([0, 1])
        self.FA5 = self.FA7 - 20 * np.array([1, 0])
        self.FA8 = self.FA7 + (self.dataObj.beam_L) * np.array([1, 0])
        self.FP1 = self.FA1 + (self.dataObj.beam_B + self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.FA6 = self.FP1 + (self.dataObj.beam_L) * np.array([1, 0])
        self.FP = self.FP1 - self.dataObj.gap * np.array([1, 0])
        self.FP2 = self.FP + (self.dataObj.cleat_legsize) * np.array([1, 0])
        self.FP3 = self.FP2 + (self.dataObj.cleat_thk) * np.array([0, 1])
        self.FP6 = self.FP3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1, 0])
        self.FP5 = self.FP6 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0, 1])
        self.FP4 = self.FP5 - (self.dataObj.cleat_thk) * np.array([1, 0])
        self.FP7 = self.FP1 + (self.dataObj.cleat_thk) * np.array([0, 1])
        self.FQN = self.FP1 - self.dataObj.gap * np.array([1, 0]) - (self.dataObj.beam_tw) * np.array([0, 1])
        self.FQ1 = self.FQN + (self.dataObj.gap) * np.array([1, 0])
        self.FQ2 = self.FQN + (self.dataObj.cleat_legsize) * np.array([1, 0])
        self.FQ3 = self.FQ2 - (self.dataObj.cleat_thk) * np.array([0, 1])
        self.FQ7 = self.FQ1 - (self.dataObj.cleat_thk) * np.array([0, 1])
        self.FQ6 = self.FQ3 - (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1, 0])
        self.FQ5 = self.FQ6 - (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0, 1])
        self.FQ4 = self.FQ5 - (self.dataObj.cleat_thk) * np.array([1, 0])

        # Points for Beam - Beam connection
        self.beam_beam_length = self.dataObj.beam_B + 200
        # for primary beam
        self.notch_length = (self.dataObj.col_B - self.dataObj.col_tw) / 2 - 10

        self.BA = (0, 0)
        self.BB = self.BA + (self.dataObj.col_B) * np.array([1, 0])
        self.BC = self.BB + self.beam_beam_length * np.array([0, 1])
        self.BD = self.BA + self.beam_beam_length * np.array([0, 1])
        self.BE = self.BA + (self.dataObj.col_B - self.dataObj.col_tw) / 2 * np.array([1, 0])
        self.BF = self.BE + self.beam_beam_length * np.array([0, 1])
        self.BG = self.BE + self.dataObj.col_tw * np.array([1, 0])
        self.BH = self.BG + self.beam_beam_length * np.array([0, 1])

        # for secondary beam

        self.BA3 = self.BB + 10 * np.array([1, 0]) + (self.beam_beam_length - self.dataObj.beam_B) / 2 * np.array([0, 1])
        self.BA2 = self.BA3 - 10 * np.array([1, 0])
        self.BA1 = self.BA3 - self.notch_length * np.array([1, 0])
        self.BA4 = self.BA3 + (self.dataObj.beam_L - self.notch_length) * np.array([1, 0])
        self.BA5 = self.BA4 + self.dataObj.beam_B * np.array([0, 1])
        self.BA6 = self.BA3 + self.dataObj.beam_B * np.array([0, 1])
        self.BA7 = self.BA2 + self.dataObj.beam_B * np.array([0, 1])
        self.BA8 = self.BA1 + self.dataObj.beam_B * np.array([0, 1])
        self.BA9 = self.BA1 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA10 = self.BA2 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA11 = self.BA3 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA12 = self.BA4 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA13 = self.BA4 + (self.dataObj.beam_B + self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA14 = self.BA3 + (self.dataObj.beam_B + self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA15 = self.BA2 + (self.dataObj.beam_B + self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.BA16 = self.BA1 + (self.dataObj.beam_B + self.dataObj.beam_tw) / 2 * np.array([0, 1])

        #          for cleat angle
        self.BP1 = self.BG + (self.beam_beam_length / 2 - self.dataObj.beam_tw / 2 - self.dataObj.cleat_legsize_1) * np.array([0, 1])  # BEAM_TW
        self.BP2 = self.BP1 + self.dataObj.cleat_thk * np.array([1, 0])
        self.BP3 = self.BP2 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0, 1])
        self.BP4 = self.BB + (self.beam_beam_length / 2 - self.dataObj.beam_tw / 2 - self.dataObj.cleat_thk) * np.array([0, 1])  # BEAM_TW
        self.BP5 = self.BP4 + 10 * np.array([1, 0])
        self.BP6 = self.BP3 + (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1, 0])
        self.BP7 = self.BP6 + self.dataObj.cleat_thk * np.array([0, 1])
        self.BP9 = self.BP4 + self.dataObj.cleat_thk * np.array([0, 1])
        self.BP10 = self.BP1 + self.dataObj.cleat_legsize_1 * np.array([0, 1])

        self.BQ1 = self.BH + (self.beam_beam_length / 2 - self.dataObj.beam_tw / 2 - self.dataObj.cleat_legsize_1) * np.array([0, -1])  # BEAM_TW
        self.BQ2 = self.BQ1 + self.dataObj.cleat_thk * np.array([1, 0])
        self.BQ3 = self.BQ2 + (self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk) * np.array([0, -1])
        self.BQ4 = self.BC + (self.beam_beam_length / 2 - self.dataObj.beam_tw / 2 - self.dataObj.cleat_thk) * np.array([0, -1])  # BEAM_TW
        self.BQ5 = self.BQ4 + 10 * np.array([1, 0])
        self.BQ6 = self.BQ3 + (self.dataObj.cleat_legsize - self.dataObj.cleat_thk) * np.array([1, 0])
        self.BQ7 = self.BQ6 + self.dataObj.cleat_thk * np.array([0, -1])
        self.BQ9 = self.BQ4 + self.dataObj.cleat_thk * np.array([0, -1])
        self.BQ10 = self.BQ1 + self.dataObj.cleat_legsize_1 * np.array([0, -1])

    def call_BWBW_top(self, filename):

        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox='-200 -350 1200 1200')

        # ########### B-B section #################
        ptSecA = self.BB + ((300 + self.dataObj.gap + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txt_pt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.BC + ((300 + self.dataObj.gap + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        # ########### C-C section #################
        ptSecA = self.FL + (50) * np.array([-1, 0]) + ((self.dataObj.D_beam * 3) / 8 + 220) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (20 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.dataObj.gap + self.dataObj.beam_L + 50) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (20 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BC), (self.BD), (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BE), (self.BF)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BG), (self.BH)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.BA2), (self.BA1), (self.BA8), (self.BA7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.BA2), (self.BA3), (self.BA4), (self.BA5), (self.BA6), (self.BA7)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BA3), (self.BA6)).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.line((self.BA9), (self.BA10)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BA16), (self.BA15)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.line((self.BA10), (self.BA11)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BA15), (self.BA14)).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.line((self.BA11), (self.BA12)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BA14), (self.BA13)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        # cleat Angle 
        dwg.add(dwg.polyline(points=[(self.BP1), (self.BP2), (self.BP3), (self.BP6), (self.BP7), (self.BP10), (self.BP1)], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline(points=[(self.BQ1), (self.BQ2), (self.BQ3), (self.BQ6), (self.BQ7), (self.BQ10), (self.BQ1)], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([5, 5])))

        nc = self.dataObj.no_of_col
        nc_c = self.dataObj.no_of_ccol
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list_c = []
        pt_list_c1 = []
        if nc >= 1:
            for col in range(nc):
                pt = self.BP6 - self.dataObj.end_dist * np.array([1, 0]) - (col) * self.dataObj.gauge * np.array([1, 0])
                pt1 = pt - bolt_r * np.array([1, 0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + 2 * (self.dataObj.cleat_thk)
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0, -1])
                B2 = pt + (rect_ht + 10) * np.array([0, 1])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                pt_list.append(pt)

        if nc_c >= 1:
            for col in range(nc_c):
                pt_c = self.BP1 + self.dataObj.cend_dist * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0]) + (col) * self.dataObj.cgauge * np.array(
                    [0, 1])
                pt1_c = pt_c - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt_c + 10 * np.array([-1, 0])
                B2 = pt_c + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                pt_list_c.append(pt_c)

                pt_c1 = self.BQ1 + self.dataObj.cend_dist * np.array([0, -1]) - self.dataObj.col_tw * np.array([1, 0]) - (col) * self.dataObj.cgauge * np.array(
                    [0, 1])
                pt1_c1 = pt_c1 - bolt_r * np.array([0, 1])
                rect_width1 = self.dataObj.bolt_dia
                rect_length1 = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c1), size=(rect_length1, rect_width1), fill='black', stroke='black', stroke_width=2.5))
                B1_1 = pt_c1 + 10 * np.array([-1, 0])
                B2_1 = pt_c1 + (rect_ht + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_1), (B2_1)).stroke('black', width=2.5, linecap='square'))
                pt_list_c1.append(pt_c1)

        # Faint lines and outer arrow for column cleat connectivity
        # Faint lines at the edge of the plate
        # above the beam part
        pt2 = self.BP1 - (self.dataObj.col_B + 200 + self.dataObj.col_T) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(self.BP1, pt2, dwg)
        ptx = np.array(pt_list_c[0]) - (self.dataObj.col_B + 200) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list_c[0]), ptx, dwg)
        pt2_left = self.BP1 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B + 200) / 2, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt2_left, np.array(pt_list_c[0]), str(int(self.dataObj.cend_dist)), params)
        # below the beam part
        pt2 = self.BQ1 - (self.dataObj.col_B + 200 + self.dataObj.col_T) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(self.BQ1, pt2, dwg)
        ptx = np.array(pt_list_c1[0]) - (self.dataObj.col_B + 200) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list_c1[0]), ptx, dwg)
        pt2_left = self.BQ1 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B + 200) / 2, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt2_left, np.array(pt_list_c1[0]), str(int(self.dataObj.cend_dist)), params)
        if nc_c > 1:
            pt1 = np.array(pt_list_c[1])
            pt2 = pt1 - (self.dataObj.col_B + 200) / 2 * np.array([1, 0])
            self.dataObj.draw_faint_line(pt1, pt2, dwg)
            params = {"offset": (self.dataObj.col_B + 200) / 2, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt1, np.array(pt_list_c[0]), str(int(self.dataObj.cgauge)), params)

            pt1 = np.array(pt_list_c1[1])
            pt2 = pt1 - (self.dataObj.col_B + 200) / 2 * np.array([1, 0])
            self.dataObj.draw_faint_line(pt1, pt2, dwg)
            params = {"offset": (self.dataObj.col_B + 200) / 2, "textoffset": 50, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt1, np.array(pt_list_c1[0]), str(int(self.dataObj.cgauge)), params)

        # marking and drawing arrow for beam connectivity
        dim_offset = self.beam_beam_length / 2 + 25
        pt1 = np.array(pt_list[0])
        pt2 = self.BP6
        pt3 = pt1 - dim_offset * np.array([0, 1])
        pt4 = pt2 - dim_offset * np.array([0, 1])
        self.dataObj.draw_faint_line(pt1, pt3, dwg)
        self.dataObj.draw_faint_line(pt2, pt4, dwg)
        params = {"offset": dim_offset, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt1, pt2, str(int(self.dataObj.end_dist)), params)
        if nc > 1:
            pt1 = np.array(pt_list[1])
            pt2 = pt1 - dim_offset * np.array([0, 1])
            self.dataObj.draw_faint_line(pt1, pt2, dwg)
            params = {"offset": dim_offset + 25, "textoffset": 10, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt1, np.array(pt_list[0]), str(int(self.dataObj.gauge)), params)
        # ########################All Dimensional marking has been done ######################

        # Beam Information
        beam_pt = (self.BA4 + self.BA5) / 2
        theta = 1
        offset = 0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # Column Information
        col_pt = (self.BA + self.BB) / 2
        theta = 90
        offset = 150
        text_up = "Beam " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "NE", offset, text_up, text_down)

        # cleat information
        plt_pt = self.BP6
        theta = 40
        offset = self.dataObj.beam_B / 2 + 50
        text_up = "ISA. " + str(int(self.dataObj.cleat_legsize)) + 'x' + str(int(self.dataObj.cleat_legsize_1)) + 'x' + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plt_pt, theta, "NE", offset, text_up, text_down)

        # Bolt Information for beam connectivity
        #         bolt_pt = self.FP5 + self.dataObj.edge_dist * np.array([1,0]) + (nc -1) * self.dataObj.gauge * np.array([1,0])
        bolt_pt = np.array(pt_list[0])
        theta = 45
        offset = (self.dataObj.beam_B) + 100
        text_up = str(self.dataObj.no_of_rows * self.dataObj.no_of_col) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # Bolt information for column connectivity
        no_of_bolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2
        weld_pt = np.array(pt_list_c1[-1])
        theta = 30
        offset = (self.beam_beam_length - 2 * self.dataObj.cleat_legsize) / 2 + 25
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "SE", offset, text_up, text_down)

        # Gap Informatoin
        ptG1 = self.BC + 100 * np.array([0, 1])
        ptG2 = ptG1 + 20 * np.array([1, 0])
        offset = 1
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim": 10, "arrowlen": 50}
        self.dataObj.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.dataObj.gap), params)
        # Draw Faint Lines to representation of Gap distance 
        ptA = self.BC
        ptB = ptG1
        self.dataObj.draw_faint_line(ptA, ptB, dwg)
        ptC = self.BA6
        ptD = ptC + (self.dataObj.D_col - self.dataObj.beam_B) / 2 * np.array([0, 1])
        self.dataObj.draw_faint_line(ptC, ptD, dwg)

        # 2D view name
        ptx = self.BD + 100 * np.array([1, 0]) + 300 * np.array([0, 1])  # 640
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        ptx = self.BD + 100 * np.array([1, 0]) + 340 * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CFBW_top(self, filename):
        '''
        '''
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-400 -250 1500 1020'))

        # ########### B-B section #################
        ptSecA = self.FF + ((290 + self.dataObj.gap + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txt_pt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.FG + ((290 + self.dataObj.gap + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        # ########### C-C section #################
        ptSecA = self.FL + (50) * np.array([-1, 0]) + ((self.dataObj.D_beam * 3) / 8 + 100) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.gap + self.dataObj.beam_L + 100) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(
            points=[(self.FA), (self.FB), (self.FC), (self.FD), (self.FE), (self.FF), (self.FG), (self.FH), (self.FI), (self.FJ), (self.FK), (self.FL),
                    (self.FA)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FA1), size=(self.dataObj.beam_L, self.dataObj.beam_B), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.FA7), (self.FA8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.FP1), (self.FA6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.line((self.FP), (self.FP1)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FQN), (self.FQ1)).stroke('blue', width=2.5, linecap='square'))

        dwg.add( dwg.polyline(points=[(self.FP1), (self.FP2), (self.FP3), (self.FP7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline(points=[(self.FQ1), (self.FQ2), (self.FQ3), (self.FQ7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.FP7), (self.FP6), (self.FP5), (self.FP4)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[(self.FQ7), (self.FQ6), (self.FQ5), (self.FQ4)], stroke='blue', fill='none', stroke_width=2.5))


        nc = self.dataObj.no_of_col
        nc_c = self.dataObj.no_of_ccol
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list_c = []
        pt_list_c1 = []
        if nc >= 1:
            for col in range(nc):
                pt = self.FQ3 - self.dataObj.end_dist * np.array([1, 0]) - (col) * self.dataObj.gauge * np.array([1, 0])
                pt1 = pt - bolt_r * np.array([1, 0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + 2 * (self.dataObj.cleat_thk)
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0, -1])
                B2 = pt + (rect_ht + 10) * np.array([0, 1])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                pt_list.append(pt)
                if len(pt_list) > 1:
                    dim_offset = self.dataObj.beam_B / 2 + self.dataObj.col_T + self.dataObj.col_R1 + 100
                    pt1 = np.array(pt_list[1])
                    pt2 = pt1 - (self.dataObj.beam_B / 2 + self.dataObj.col_T + self.dataObj.col_R1 + 100) * np.array([0, 1])
                    params = {"offset": dim_offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_faint_line(pt1, pt2, dwg)
        if nc_c >= 1:
            for col in range(nc_c):
                pt_c = self.FQ4 + self.dataObj.cend_dist * np.array([0, 1]) - self.dataObj.col_T * np.array([1, 0]) + (col) * self.dataObj.cgauge * np.array(
                    [0, 1])
                pt1_c = pt_c - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_T + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt_c + 10 * np.array([-1, 0])
                B2 = pt_c + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                pt_list_c.append(pt_c)

                pt_c1 = self.FP4 + self.dataObj.cend_dist * np.array([0, -1]) - self.dataObj.col_T * np.array([1, 0]) - (col) * self.dataObj.cgauge * np.array(
                    [0, 1])
                pt1_c1 = pt_c1 - bolt_r * np.array([0, 1])
                rect_width1 = self.dataObj.bolt_dia
                rect_length1 = self.dataObj.col_T + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c1), size=(rect_length1, rect_width1), fill='black', stroke='black', stroke_width=2.5))
                B1_1 = pt_c1 + 10 * np.array([-1, 0])
                B2_1 = pt_c1 + (rect_ht + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_1), (B2_1)).stroke('black', width=2.5, linecap='square'))
                pt_list_c1.append(pt_c1)

        if nc_c > 1:
            ptb = np.array(pt_list_c[1])
            ptb1 = ptb - (self.dataObj.D_col + 30) * np.array([1, 0])
            params = {"offset": self.dataObj.D_col + 30, "textoffset": 100, "lineori": "right", "endlinedim": 10}
            #             self.dataObj.draw_dimension_outer_arrow(dwg,np.array(pt_list_c[0]),np.array(pt_list_c[1]),  str(int(self.dataObj.gauge)) , params)
            self.dataObj.draw_faint_line(ptb, ptb1, dwg)
            self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), np.array(pt_list_c[1]), str(int(self.dataObj.cgauge)), params)

            ptb = np.array(pt_list_c1[1])
            ptb1 = ptb - (self.dataObj.D_col + 30) * np.array([1, 0])
            params = {"offset": self.dataObj.D_col + 30, "textoffset": 100, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c1[0]), np.array(pt_list_c1[1]), str(int(self.dataObj.cgauge)), params)
            self.dataObj.draw_faint_line(ptb, ptb1, dwg)

        # Faint lines and outer arrow for column cleat connectivity
        # Faint lines at the edge of the plate
        # above the beam part
        pt2 = self.FQ4 - (self.dataObj.D_col + 30 + self.dataObj.col_T) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.FQ4, pt2, dwg)
        ptx = np.array(pt_list_c[0]) - (self.dataObj.D_col + 30) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list_c[0]), ptx, dwg)
        pt2_left = self.FQ4 - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + 30, "textoffset": 100, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt2_left, np.array(pt_list_c[0]), str(int(self.dataObj.cend_dist)), params)
        # below the beam part
        pt2 = self.FP4 - (self.dataObj.D_col + 30 + self.dataObj.col_T) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.FP4, pt2, dwg)
        ptx = np.array(pt_list_c1[0]) - (self.dataObj.D_col + 30) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list_c1[0]), ptx, dwg)
        pt2_left = self.FP4 - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + 30, "textoffset": 100, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt2_left, np.array(pt_list_c1[0]), str(int(self.dataObj.cend_dist)), params)
        # marking and drawing arrow for beam connectivity
        dim_offset = self.dataObj.beam_B / 2 + self.dataObj.col_T + self.dataObj.col_R1 + 150
        pt1 = np.array(pt_list[0])
        pt2 = self.FQ3
        pt3 = pt1 - dim_offset * np.array([0, 1])
        pt4 = pt2 - dim_offset * np.array([0, 1])
        self.dataObj.draw_faint_line(pt1, pt3, dwg)
        self.dataObj.draw_faint_line(pt2, pt4, dwg)
        params = {"offset": dim_offset, "textoffset": 10, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, pt1, pt2, str(int(self.dataObj.end_dist)), params)
        # ########################All Dimensional marking has been done ######################

        # Beam Information
        beam_pt = self.FA6
        theta = 1
        offset = 0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # Column Information
        col_pt = self.FL
        theta = 45
        offset = (self.dataObj.D_beam * 3) / 8
        text_up = "Column " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, text_up, text_down)

        # cleat information
        plt_pt = self.FP3
        theta = 45
        offset = self.dataObj.beam_B / 2 + 50
        text_up = "ISA. " + str(int(self.dataObj.cleat_legsize)) + 'x' + str(int(self.dataObj.cleat_legsize_1)) + 'x' + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, text_up, text_down)

        # Bolt Information for beam connectivity
        bolt_pt = np.array(pt_list[0])
        theta = 70
        offset = (self.dataObj.beam_B) + 80
        text_up = str(self.dataObj.no_of_rows * self.dataObj.no_of_col) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # Bolt information for column connectivity
        no_of_bolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol
        weld_pt = np.array(pt_list_c[0])
        theta = 70
        offset = (self.dataObj.D_col - self.dataObj.beam_B) / 2 + 80
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NW", offset, text_up, text_down)

        # Gap Informatoin
        ptG1 = self.FG + 50 * np.array([0, 1])
        ptG2 = ptG1 + 20 * np.array([1, 0])
        offset = 10
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim": 20, "arrowlen": 50}
        self.dataObj.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)

        # Draw Faint Lines to representation of Gap distance 
        ptA = self.FG
        ptB = ptG1
        self.dataObj.draw_faint_line(ptA, ptB, dwg)
        ptC = self.FA4
        ptD = ptC + (self.dataObj.D_col - self.dataObj.beam_B)/1.5  * np.array([0, 1])
        self.dataObj.draw_faint_line(ptC, ptD, dwg)

        # 2D view name
        ptx = self.FG + (self.dataObj.beam_B * 2) * np.array([0, 1])  # 740
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        ptx = self.FG + (self.dataObj.beam_B * 2 + 40) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CWBW_top(self, filename):
        '''
        '''
        v_width = self.dataObj.beam_L + self.dataObj.col_B / 2 + 850
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-300 -300 ' + str(v_width)) + ' 1200')

        # Cross section B-B and C-C            
        ptSecA = self.B + (20 * np.array([0, -1])) + (self.dataObj.beam_L + 350) * np.array([1, 0])
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txt_pt = ptSecB + (70 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.G + (20 * np.array([0, 1])) + (self.dataObj.beam_L + 350) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (70 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ptSecA = self.I + (250 * np.array([0, 1])) + (10 * np.array([-1, 0]))
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (50 * np.array([0, -1])) + (15 * np.array([-1, 0]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (520 * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (50 * np.array([0, -1])) + (15 * np.array([-1, 0]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(
            points=[(self.A), (self.B), (self.C), (self.D), (self.E), (self.F), (self.G), (self.H), (self.I), (self.J), (self.K), (self.L), (self.A)],
            stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A1), size=(self.dataObj.beam_L, self.dataObj.beam_B), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.A7), (self.A8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.P1), (self.A6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.P), (self.P1)).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.P1), (self.P2), (self.P3), (self.P7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline(points=[(self.Q1), (self.Q2), (self.Q3), (self.Q7)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.P7), (self.P6), (self.P5), (self.P4)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[(self.Q7), (self.Q6), (self.Q5), (self.Q4)], stroke='blue', fill='none', stroke_width=2.5))

        dwg.add(dwg.line((self.Q), (self.Q1)).stroke('blue', width=2.5, linecap='square'))

        nc = self.dataObj.no_of_col
        nc_c = self.dataObj.no_of_ccol
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list_c = []
        pt_list_c1 = []
        if nc >= 1:
            for col in range(nc):
                pt = self.Q3 - self.dataObj.end_dist * np.array([1, 0]) - (col) * self.dataObj.gauge * np.array([1, 0])
                pt1 = pt - bolt_r * np.array([1, 0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + 2 * (self.dataObj.cleat_thk)
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0, -1])
                B2 = pt + (rect_ht + 10) * np.array([0, 1])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                pt_list.append(pt)
            if nc > 1:
                dim_offset = self.dataObj.beam_B / 2 + self.dataObj.beam_tw / 2 + self.dataObj.cleat_thk + 150
                pt_down = np.array(pt_list[1]) + dim_offset * np.array([0, 1])
                self.dataObj.draw_faint_line(np.array(pt_list[1]), pt_down, dwg)
                params = {"offset": dim_offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
                self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[1]), str(int(self.dataObj.gauge)), params)
        if nc_c >= 1:
            for col in range(nc_c):
                pt_c = self.Q4 + self.dataObj.cend_dist * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0]) + (col) * self.dataObj.cgauge * np.array(
                    [0, 1])
                pt1_c = pt_c - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt_c + 10 * np.array([-1, 0])
                B2 = pt_c + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_c1 = self.P4 + self.dataObj.cend_dist * np.array([0, -1]) - self.dataObj.col_tw * np.array([1, 0]) - (col) * self.dataObj.cgauge * np.array(
                    [0, 1])
                pt1_c1 = pt_c1 - bolt_r * np.array([0, 1])
                rect_width1 = self.dataObj.bolt_dia
                rect_length1 = self.dataObj.col_tw + self.dataObj.cleat_thk
                dwg.add(dwg.rect(insert=(pt1_c1), size=(rect_length1, rect_width1), fill='black', stroke='black', stroke_width=2.5))
                B1_1 = pt_c1 + 10 * np.array([-1, 0])
                B2_1 = pt_c1 + (rect_ht + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_1), (B2_1)).stroke('black', width=2.5, linecap='square'))

                pt_list_c.append(pt_c)
                pt_list_c1.append(pt_c1)
            if nc_c > 1:
                dim_offset = self.dataObj.beam_B / 2 + self.dataObj.col_tw + 100
                pt_left = np.array(pt_list_c[1]) - dim_offset * np.array([1, 0])
                pt_left_1 = np.array(pt_list_c1[1]) - dim_offset * np.array([1, 0])
                self.dataObj.draw_faint_line(np.array(pt_list_c[1]), pt_left, dwg)
                self.dataObj.draw_faint_line(np.array(pt_list_c1[1]), pt_left_1, dwg)
                params = {"offset": dim_offset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), np.array(pt_list_c[1]), str(int(self.dataObj.cgauge)), params)
                self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c1[1]), np.array(pt_list_c1[0]), str(int(self.dataObj.cgauge)), params)

        # ##Faint lines and edge distance marking on beam connectivity
        dim_offset = self.dataObj.beam_B / 2 + self.dataObj.beam_tw / 2 + self.dataObj.cleat_thk + 200
        pt_down = np.array(pt_list[0]) + dim_offset * np.array([0, 1])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), pt_down, dwg)
        pt_down = self.Q3 + dim_offset * np.array([0, 1])
        self.dataObj.draw_faint_line(self.Q3, pt_down, dwg)
        params = {"offset": dim_offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), self.Q3, str(int(self.dataObj.end_dist)), params)

        # #####Faint lines for column connectivity  edge(end) distance outer arrow
        dim_offset = self.dataObj.beam_B / 2 + self.dataObj.col_tw + 100
        pt_left = np.array(pt_list_c[0]) - dim_offset * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list_c[0]), pt_left, dwg)
        pt_left = np.array(pt_list_c1[0]) - dim_offset * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list_c1[0]), pt_left, dwg)
        pt_left = self.Q4 - dim_offset * np.array([1, 0])
        self.dataObj.draw_faint_line(self.Q4, pt_left, dwg)
        pt_left = self.P4 - dim_offset * np.array([1, 0])
        self.dataObj.draw_faint_line(self.P4, pt_left, dwg)
        params = {"offset": dim_offset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        params_1 = {"offset": dim_offset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), self.Q4 - self.dataObj.col_tw * np.array([1, 0]), str(int(self.dataObj.cend_dist)),
                                                params_1)
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c1[0]), self.P4 - self.dataObj.col_tw * np.array([1, 0]),
                                                str(int(self.dataObj.cend_dist)), params)
        c_gauge = 2 * self.dataObj.cleat_legsize_1 + self.dataObj.beam_tw - 2 * self.dataObj.cend_dist

        params = {"offset": dim_offset, "textoffset": 75, "lineori": "right", "endlinedim": 10}
        if self.dataObj.no_of_ccol > 1:
            self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[1]), np.array(pt_list_c1[1]), str(int(c_gauge)), params)
        else:
            self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list_c[0]), np.array(pt_list_c1[0]), str(int(c_gauge)), params)

        # Beam Information
        beam_pt = self.A6
        theta = 1
        offset = 0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # column  Information
        col_pt = (self.A + self.B) / 4
        theta = 90
        offset = 100
        text_up = "Column " + self.dataObj.col_Designation
        text_down = " "
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "NW", offset, text_up, text_down)

        # Cleat Information
        plt_pt = self.P3
        theta = 45
        offset = self.dataObj.beam_B / 2 + 50
        text_up = "ISA." + str(int(self.dataObj.cleat_legsize)) + 'x' + str(int(self.dataObj.cleat_legsize_1)) + 'x' + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, text_up, text_down)

        # beam Bolt Information
        no_of_bbolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        bolt_pt = np.array(pt_list[0])
        theta = 45
        offset = (self.dataObj.beam_B)
        text_up = str(no_of_bbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # column bolt information
        no_of_cbolts = self.dataObj.no_of_crows * self.dataObj.no_of_ccol * 2
        weld_pt = np.array(pt_list_c[0])
        theta = 45
        offset = self.dataObj.beam_B + 50
        text_up = str(no_of_cbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down)

        # Gap Informatoin
        ptG1 = self.D + 100 * np.array([0, -1])
        ptG2 = ptG1 + self.dataObj.gap * np.array([1, 0])
        offset = 100
        params = {"offset": offset, "textoffset": 10, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.dataObj.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.dataObj.gap), params)

        # Draw Faint Lines to representation of Gap distance #
        ptA = self.D
        ptB = ptA + (150) * np.array([0, -1])
        self.dataObj.draw_faint_line(ptA, ptB, dwg)
        ptC = self.A1
        ptD = ptC + (150) * np.array([0, -1]) - (self.dataObj.D_col - 2 * self.dataObj.col_T - self.dataObj.beam_B) / 2 * np.array([0, 1])
        self.dataObj.draw_faint_line(ptC, ptD, dwg)

        # 2D view name
        ptx = self.G + (self.dataObj.beam_B * 2) * np.array([0, 1])  # 1090
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black', font_family="sans-serif", font_size=32))
        ptx = self.G + (self.dataObj.beam_B * 2+ 40) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()


class Cleat2DCreatorSide(object):
    def __init__(self, fin_common_obj):

        self.dataObj = fin_common_obj

        # CWBW connectivity points
        self.A = np.array([0, 0])
        self.B = self.A + self.dataObj.col_T * np.array([1, 0])
        self.C = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.D = self.A + self.dataObj.D_col * np.array([1, 0])
        self.H = self.C + self.dataObj.col_L * np.array([0, 1])
        self.G = self.B + self.dataObj.col_L * np.array([0, 1])
        self.A1 = ((self.dataObj.D_col - self.dataObj.beam_B) / 2) * np.array([1, 0]) + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array([0, 1])
        self.A2 = self.A1 + self.dataObj.beam_B * np.array([1, 0])
        self.A3 = self.A2 + self.dataObj.beam_T * np.array([0, 1])
        self.A12 = self.A1 + self.dataObj.beam_T * np.array([0, 1])
        self.A11 = self.A12 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([1, 0])
        self.A4 = self.A11 + self.dataObj.beam_tw * np.array([1, 0])
        self.A5 = self.A4 + (self.dataObj.D_beam - (2 * self.dataObj.beam_T)) * np.array([0, 1])
        self.A6 = self.A2 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0, 1])
        self.A7 = self.A2 + self.dataObj.D_beam * np.array([0, 1])
        self.A8 = self.A1 + self.dataObj.D_beam * np.array([0, 1])
        self.A9 = self.A1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0, 1])
        self.A10 = self.A11 + (self.dataObj.D_beam - (2 * self.dataObj.beam_T)) * np.array([0, 1])
        self.P = self.A11 + (self.dataObj.beam_R1 + 3) * np.array([0, 1])
        self.Q = self.P + self.dataObj.cleat_thk * np.array([-1, 0])
        self.X = self.P + self.dataObj.cleat_legsize_1 * np.array([-1, 0])
        self.R = self.P + self.dataObj.cleat_ht * np.array([0, 1])

        self.P1 = self.P + self.dataObj.beam_tw * np.array([1, 0])
        self.Q1 = self.P1 + self.dataObj.cleat_thk * np.array([1, 0])
        self.X1 = self.P1 + self.dataObj.cleat_legsize_1 * np.array([1, 0])
        self.R1 = self.P1 + self.dataObj.cleat_ht * np.array([0, 1])

        #### CFBW connectivity
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.dataObj.col_B * np.array([1, 0])
        self.ptMid = self.FA + ((self.dataObj.col_B / 2) + (self.dataObj.col_tw / 2)) * np.array([1, 0])
        self.ptMid1 = self.ptMid + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array([0, 1])
        self.FC = self.FB + self.dataObj.col_L * np.array([0, 1])
        self.FD = self.FA + self.dataObj.col_L * np.array([0, 1])
        self.FA1 = self.FA + (self.dataObj.col_B - self.dataObj.beam_B) / 2 * np.array([1, 0]) + (self.dataObj.col_L - self.dataObj.D_beam) / 2 * np.array(
            [0, 1])
        self.FA2 = self.FA1 + self.dataObj.beam_B * np.array([1, 0])
        self.FA3 = self.FA2 + self.dataObj.beam_T * np.array([0, 1])
        self.FA12 = self.FA1 + self.dataObj.beam_T * np.array([0, 1])
        self.FA11 = self.FA12 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([1, 0])
        self.FA4 = self.FA11 + self.dataObj.beam_tw * np.array([1, 0])
        self.FA5 = self.FA4 + (self.dataObj.D_beam - (2 * self.dataObj.beam_T)) * np.array([0, 1])
        self.FA6 = self.FA2 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0, 1])
        self.FA7 = self.FA2 + self.dataObj.D_beam * np.array([0, 1])
        self.FA8 = self.FA1 + self.dataObj.D_beam * np.array([0, 1])
        self.FA9 = self.FA1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0, 1])
        self.FA10 = self.FA11 + (self.dataObj.D_beam - (2 * self.dataObj.beam_T)) * np.array([0, 1])

        self.FP = self.FA11 + (self.dataObj.beam_R1 + 3) * np.array([0, 1])
        self.FQ = self.FP + self.dataObj.cleat_thk * np.array([-1, 0])
        self.FX = self.FP + self.dataObj.cleat_legsize_1 * np.array([-1, 0])
        self.FP2 = self.FP + self.dataObj.cleat_ht * np.array([0, 1])
        self.FQ2 = self.FQ + self.dataObj.cleat_ht * np.array([0, 1])
        self.FX2 = self.FX + self.dataObj.cleat_ht * np.array([0, 1])

        self.FP1 = self.FP + self.dataObj.beam_tw * np.array([1, 0])
        self.FQ1 = self.FP1 + self.dataObj.cleat_thk * np.array([1, 0])
        self.FX1 = self.FP1 + self.dataObj.cleat_legsize_1 * np.array([1, 0])
        self.FP3 = self.FP1 + self.dataObj.cleat_ht * np.array([0, 1])
        self.FQ3 = self.FQ1 + self.dataObj.cleat_ht * np.array([0, 1])
        self.FX3 = self.FX1 + self.dataObj.cleat_ht * np.array([0, 1])

        ##### Points for Beam-Beam connection #####

        self.beam_beam_length = self.dataObj.beam_B + 200  # #beam_B

        # for primary beam

        self.BA = (0, 0)
        self.BB = self.BA + self.beam_beam_length * np.array([1, 0])  # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS
        self.BC = self.BB + self.dataObj.col_T * np.array([0, 1])
        self.BD = self.BC - (self.beam_beam_length - self.dataObj.beam_tw) / 2 * np.array([1, 0])  # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS
        self.BE = self.BD - self.dataObj.beam_tw * np.array([1, 0])  # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS :BEAM_TW
        self.BF = self.BA + self.dataObj.col_T * np.array([0, 1])
        self.BG = self.BA + (self.dataObj.D_col - self.dataObj.col_T) * np.array([0, 1])
        self.BH = self.BG + self.beam_beam_length * np.array([1, 0])
        self.BI = self.BH + self.dataObj.col_T * np.array([0, 1])
        self.BJ = self.BG + self.dataObj.col_T * np.array([0, 1])

        # for secondary beam ### changes after importing beam

        self.BA1 = self.BA + (self.beam_beam_length - self.dataObj.beam_B) / 2 * np.array([1, 0])  # NEED TO BE CHANGED AFTER IMPORTING BEAM DETAILS :BEAM_B
        self.BB1 = self.BA1 + self.dataObj.beam_B * np.array([1, 0])  # BEAM_B
        self.BC1 = self.BB1 + self.dataObj.beam_T * np.array([0, 1])
        self.BD1 = self.BC1 - (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([1, 0])
        self.BE1 = self.BD1 + (self.dataObj.D_beam - 2 * self.dataObj.beam_T) * np.array([0, 1])
        self.BF1 = self.BC1 + (self.dataObj.D_beam - 2 * self.dataObj.beam_T) * np.array([0, 1])
        self.BG1 = self.BF1 + self.dataObj.beam_T * np.array([0, 1])
        self.BL1 = self.BA1 + self.dataObj.beam_T * np.array([0, 1])
        self.BH1 = self.BL1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0, 1])
        self.BI1 = self.BL1 + (self.dataObj.D_beam - 2 * self.dataObj.beam_T) * np.array([0, 1])
        self.BJ1 = self.BE1 - self.dataObj.beam_tw * np.array([1, 0])
        self.BK1 = self.BD1 - self.dataObj.beam_tw * np.array([1, 0])

        # for cleat angle

        self.BP = self.BD + (self.dataObj.notch_offset - self.dataObj.col_T) * np.array([0, 1])
        self.BQ = self.BP + self.dataObj.cleat_thk * np.array([1, 0])
        self.BR = self.BP + self.dataObj.cleat_legsize_1 * np.array([1, 0])
        self.BP1 = self.BP + self.dataObj.cleat_ht * np.array([0, 1])
        self.BQ1 = self.BQ + self.dataObj.cleat_ht * np.array([0, 1])
        self.BR1 = self.BR + self.dataObj.cleat_ht * np.array([0, 1])
        self.BX = self.BP - self.dataObj.beam_tw * np.array([1, 0])  # beam_tw
        self.BY = self.BX - self.dataObj.cleat_thk * np.array([1, 0])
        self.BZ = self.BX - self.dataObj.cleat_legsize_1 * np.array([1, 0])
        self.BX1 = self.BX + self.dataObj.cleat_ht * np.array([0, 1])
        self.BY1 = self.BY + self.dataObj.cleat_ht * np.array([0, 1])
        self.BZ1 = self.BZ + self.dataObj.cleat_ht * np.array([0, 1])

    def call_BWBW_side(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-540 -400 1500 1400'))
        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BI), (self.BJ), (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BG), (self.BH)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BF), (self.BE)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BD), (self.BC)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BE), (self.BD)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline(
            points=[(self.BB1), (self.BC1), (self.BD1), (self.BE1), (self.BF1), (self.BG1), (self.BH1), (self.BI1), (self.BJ1), (self.BK1), (self.BL1),
                    (self.BA1)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.BP, size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.BQ, size=((self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill='none', stroke='blue',
                         stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.BY, size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=self.BZ, size=((self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill='none', stroke='blue',
                         stroke_width=2.5))

        ####################Arrangng Bolts on both beams #######################
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia / 2
        c_nr = self.dataObj.no_of_crows
        c_nc = self.dataObj.no_of_ccol

        pitch_pts = []
        pitch_pts_c = []
        pitch_pts_c1 = []
        for row in range(nr):
            pt = self.BY + self.dataObj.edge_dist * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1])
            pt1 = pt - bolt_r * np.array([0, 1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.beam_tw + 2 * self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill="black", stroke='none', stroke_width=2.5))
            blt1 = pt - 5 * np.array([1, 0])
            blt2 = pt + (5 + rect_length) * np.array([1, 0])
            dwg.add(dwg.line((blt1), (blt2)).stroke('black', width=1.5, linecap='square'))
            pitch_pts.append(pt)

        for row1 in range(c_nr):
            col_list = []  # CHANGE NAME
            colList_c = []  # CHANGE NAME
            for col in range(c_nc):  # CHANGE cpitch,cend_dist,cedge_dist to bpitch etc in future after supported beam array imported
                pt_c = self.BZ + self.dataObj.cedge_dist * np.array([0, 1]) + (self.dataObj.cend_dist) * np.array([1, 0]) + (
                                                                                                                            row1) * self.dataObj.cpitch * np.array(
                    [0, 1]) + (col) * self.dataObj.cgauge * np.array([1, 0])
                dwg.add(dwg.circle(center=(pt_c), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                cbolt1 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([1, 0])
                cbolt2 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([-1, 0])
                cbolt3 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, 1])
                cbolt4 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, -1])
                dwg.add(dwg.line((cbolt1), (cbolt2)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))
                dwg.add(dwg.line((cbolt3), (cbolt4)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))

                pt_c1 = self.BR + self.dataObj.cedge_dist * np.array([0, 1]) + (self.dataObj.cend_dist) * np.array([-1, 0]) + (
                                                                                                                              row1) * self.dataObj.cpitch * np.array(
                    [0, 1]) + (col) * self.dataObj.cgauge * np.array([-1, 0])
                dwg.add(dwg.circle(center=(pt_c1), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                cbolt1_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([1, 0])
                cbolt2_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([-1, 0])
                cbolt3_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, 1])
                cbolt4_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, -1])
                dwg.add(dwg.line((cbolt1_1), (cbolt2_1)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))
                dwg.add(dwg.line((cbolt3_1), (cbolt4_1)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))

                col_list.append(pt_c)
                colList_c.append(pt_c1)
            pitch_pts_c.append(col_list)
            pitch_pts_c1.append(colList_c)

            # #################### Faint Lines and outer arrow for suporting beam connectivity ############
        length = (self.beam_beam_length - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw) / 2  # beam_tw
        pt_right = self.BR + (length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.BR, pt_right, dwg)
        pt = self.BR1
        pt_right = self.BR1 + (length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt, pt_right, dwg)

        pt_right = np.array(pitch_pts_c1[0][0]) + (self.dataObj.cend_dist + length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[0][0]), pt_right, dwg)
        pt_right = np.array(pitch_pts_c1[-1][0]) + (self.dataObj.cend_dist + length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][0]), pt_right, dwg)

        params = {"offset": length + 20, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BR, self.BR1, str(int(self.dataObj.cleat_ht)), params)

        offset = self.dataObj.cend_dist + length + 200
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[0][0]), np.array(pitch_pts_c1[-1][0]),
                                                str(len(pitch_pts_c1) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)

        pt_up = np.array(pitch_pts_c1[0][0]) - self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[0][0]), pt_up, str(int(self.dataObj.cedge_dist)), params)

        pt_down = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[-1][0]), pt_down, str(int(self.dataObj.cedge_dist)), params)
        # ###notch height###############
        self.dataObj.draw_faint_line(self.BB, self.BB + 200 * np.array([1, 0]), dwg)
        pt_down = self.BB + self.dataObj.notch_offset * np.array([0, 1])
        params = {"offset": 200, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BB, pt_down, str(int(self.dataObj.notch_offset)), params)

        # ###########Vertical column marking ###############
        v_length = (self.dataObj.D_col - self.dataObj.cleat_ht - self.dataObj.notch_offset) + 50
        ptY = self.BZ1
        ptY1 = self.BR1
        ptY_down = ptY + v_length * np.array([0, 1])
        ptY1_down = ptY1 + v_length * np.array([0, 1])
        self.dataObj.draw_faint_line(ptY, ptY_down, dwg)
        self.dataObj.draw_faint_line(ptY1, ptY1_down, dwg)

        pt_bolt = np.array(pitch_pts_c[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0, 1])
        pt_bolt_1 = np.array(pitch_pts_c1[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0, 1])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][0]), pt_bolt_1, dwg)
        self.dataObj.draw_faint_line(np.array(pitch_pts_c[-1][0]), pt_bolt, dwg)

        pt_down = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": v_length, "textoffset": 50, "lineori": "right", "endlinedim": 20}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptY, pt_down, str(int(self.dataObj.cend_dist)), params)

        pt_down = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": v_length, "textoffset": 50, "lineori": "left", "endlinedim": 20}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptY1, pt_down, str(int(self.dataObj.cend_dist)), params)

        if c_nc > 1:
            pt_bolt_down = np.array(pitch_pts_c[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0, 1])
            pt_bolt_1_down = np.array(pitch_pts_c1[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0, 1])
            self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][-1]), pt_bolt_1_down, dwg)
            self.dataObj.draw_faint_line(np.array(pitch_pts_c[-1][-1]), pt_bolt_down, dwg)

            pt_down = np.array(pitch_pts_c1[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            params = {"offset": v_length + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(self.dataObj.cgauge)), params)

            pt_down = np.array(pitch_pts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            params = {"offset": v_length + 50, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(self.dataObj.cgauge)), params)

            pt_down = np.array(pitch_pts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cgauge + self.dataObj.cend_dist) - self.dataObj.beam_tw  # Beam_tw
            params = {"offset": v_length + 100, "textoffset": 50, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(c_gauge)), params)

        else:
            pt_down = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cend_dist) - self.dataObj.beam_tw  # Beam_tw
            params = {"offset": v_length + 100, "textoffset": 50, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(c_gauge)), params)

            # ###################### Faint Lines and outer arrow for beam connectivity ############

        length = self.beam_beam_length / 2 - self.dataObj.beam_tw / 2 - self.dataObj.cleat_thk  # Beam_tw
        ptQ1 = self.BY
        pt_left = ptQ1 - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(ptQ1, pt_left, dwg)
        pt = ptQ1 + self.dataObj.cleat_ht * np.array([0, 1])
        pt_left = pt - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt, pt_left, dwg)

        pt_left = np.array(pitch_pts[0]) - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts[0]), pt_left, dwg)
        pt_left = np.array(pitch_pts[-1]) - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts[-1]), pt_left, dwg)

        offset = length + 100
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[0]), np.array(pitch_pts[-1]),
                                                str(len(pitch_pts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)

        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[0]), ptQ1, str(int(self.dataObj.edge_dist)), params)

        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[-1]), pt, str(int(self.dataObj.edge_dist)), params)
        # ##################################################################################################################
        # SUPORTED BEAM Designation
        beam_pt = self.BG1
        theta = 45
        offset = (self.dataObj.beam_B * 1.4)   # beam_B
        text_up = "Beam " + self.dataObj.beam_Designation  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # SUPORTING BEAM Designation
        theta = 75
        offset = 200
        text_up = ""
        text_down =  "Beam " + self.dataObj.col_Designation
        self.dataObj.draw_oriented_arrow(dwg, self.BG, theta, "SW", offset, text_up, text_down)

        #  primary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol

        bolt_pt_x = np.array(pitch_pts_c1[0][0])
        theta = 60
        offset = (self.dataObj.D_beam * 3) / 8 + 75  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(
        #     self.dataObj.bolt_grade) + ')'  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down)

        # secondary BEAM Bolt GROUP  Information
        no_of_bolts = self.dataObj.no_of_rows * self.dataObj.no_of_col  # Double Angle cleat

        bolt_pt = np.array(pitch_pts[0])
        theta = 75
        offset = (self.beam_beam_length / 2 + 50)  # #
        text_up = str(no_of_bolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(
        #     self.dataObj.bolt_grade) + ')'  # #NEED TO CHANGED AFTER IMPORTING SUPPORTED BEAM INFORMATION
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # cleat angle information
        cleat_pt = self.BZ1
        theta = 55
        offset = (self.dataObj.beam_B * 1.2)   # beam_tw
        text_up = "ISA." + str(int(self.dataObj.cleat_legsize)) + "X" + str(int(self.dataObj.cleat_legsize_1)) + "X" + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, cleat_pt, theta, "SW", offset, text_up, text_down)

        # 2D view name
        ptx = self.BG + (self.dataObj.beam_B * 3) * np.array([0, 1])  # 980
        dwg.add(dwg.text('Side View (Sec B-B)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        # # All dimensions in "mm"
        ptx = self.BG + (self.dataObj.beam_B * 3+ 40) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CWBW_side(self, filename):
        '''
        '''
        v_width = self.dataObj.D_col + 500 + 600
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-500 -300 1500 1600'))
        dwg.add(dwg.rect(insert=(self.A), size=(self.dataObj.D_col, self.dataObj.col_L), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.C), (self.H)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.B), (self.G)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(
            points=[(self.A1), (self.A2), (self.A3), (self.A4), (self.A5), (self.A6), (self.A7), (self.A8), (self.A9), (self.A10), (self.A11), (self.A12),
                    (self.A1)], stroke='blue', fill='none', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.X), size=((self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill="none", stroke='blue',
                         stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.Q), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.Q1), size=((self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill="none", stroke='blue',
                         stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.P1), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia / 2
        c_nr = self.dataObj.no_of_crows
        c_nc = self.dataObj.no_of_ccol

        pitch_pts = []
        pitch_pts_c = []
        pitch_pts_c1 = []
        for row in range(nr):
            pt = self.Q + self.dataObj.edge_dist * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1])
            pt1 = pt - bolt_r * np.array([0, 1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.beam_tw + 2 * self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill="black", stroke='none', stroke_width=2.5))
            blt1 = pt - 5 * np.array([1, 0])
            blt2 = pt + (5 + rect_length) * np.array([1, 0])
            dwg.add(dwg.line((blt1), (blt2)).stroke('black', width=1.5, linecap='square'))
            pitch_pts.append(pt)

        for row1 in range(c_nr):
            col_list = []
            colList_c = []
            for col in range(c_nc):
                pt_c = self.X + self.dataObj.cedge_dist * np.array([0, 1]) + (self.dataObj.cend_dist) * np.array([1, 0]) + (
                                                                                                                           row1) * self.dataObj.cpitch * np.array(
                    [0, 1]) + (col) * self.dataObj.cgauge * np.array([1, 0])
                dwg.add(dwg.circle(center=(pt_c), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                cbolt1 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([1, 0])
                cbolt2 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([-1, 0])
                cbolt3 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, 1])
                cbolt4 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, -1])
                dwg.add(dwg.line((cbolt1), (cbolt2)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))
                dwg.add(dwg.line((cbolt3), (cbolt4)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))

                pt_c1 = self.X1 + self.dataObj.cedge_dist * np.array([0, 1]) + (self.dataObj.cend_dist) * np.array([-1, 0]) + (
                                                                                                                              row1) * self.dataObj.cpitch * np.array(
                    [0, 1]) + (col) * self.dataObj.cgauge * np.array([-1, 0])
                dwg.add(dwg.circle(center=(pt_c1), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                cbolt1_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([1, 0])
                cbolt2_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([-1, 0])
                cbolt3_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, 1])
                cbolt4_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, -1])
                dwg.add(dwg.line((cbolt1_1), (cbolt2_1)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))
                dwg.add(dwg.line((cbolt3_1), (cbolt4_1)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))

                col_list.append(pt_c)
                colList_c.append(pt_c1)
            pitch_pts_c.append(col_list)
            pitch_pts_c1.append(colList_c)

        # #################### Faint Lines and outer arrow for suporting beam connectivity ############
        length = (self.dataObj.D_col - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw) / 2
        pt_right = self.X1 + (length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.X1, pt_right, dwg)
        pt = self.X1 + self.dataObj.cleat_ht * np.array([0, 1])
        pt_right = self.X1 + self.dataObj.cleat_ht * np.array([0, 1]) + (length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt, pt_right, dwg)

        pt_right = np.array(pitch_pts_c1[0][0]) + (self.dataObj.cend_dist + length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[0][0]), pt_right, dwg)
        pt_right = np.array(pitch_pts_c1[-1][0]) + (self.dataObj.cend_dist + length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][0]), pt_right, dwg)

        params = {"offset": length + 20, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.X1, self.X1 + self.dataObj.cleat_ht * np.array([0, 1]), str(int(self.dataObj.cleat_ht)), params)

        offset = self.dataObj.cend_dist + length + 200
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[0][0]), np.array(pitch_pts_c1[-1][0]),
                                                str(len(pitch_pts_c1) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)

        pt_up = np.array(pitch_pts_c1[0][0]) - self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[0][0]), pt_up, str(int(self.dataObj.cedge_dist)), params)

        pt_down = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[-1][0]), pt_down, str(int(self.dataObj.cedge_dist)), params)

        # ###########Vertical column marking ###############
        v_length = self.dataObj.col_L / 2
        ptY = self.X + self.dataObj.cleat_ht * np.array([0, 1])
        ptY1 = self.X1 + self.dataObj.cleat_ht * np.array([0, 1])
        ptY_down = ptY + v_length * np.array([0, 1])
        ptY1_down = ptY1 + v_length * np.array([0, 1])
        self.dataObj.draw_faint_line(ptY, ptY_down, dwg)
        self.dataObj.draw_faint_line(ptY1, ptY1_down, dwg)

        pt_bolt = np.array(pitch_pts_c[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0, 1])
        pt_bolt_1 = np.array(pitch_pts_c1[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0, 1])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][0]), pt_bolt_1, dwg)
        self.dataObj.draw_faint_line(np.array(pitch_pts_c[-1][0]), pt_bolt, dwg)

        pt_down = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "right", "endlinedim": 20}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptY, pt_down, str(int(self.dataObj.cend_dist)), params)

        pt_down = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "left", "endlinedim": 20}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptY1, pt_down, str(int(self.dataObj.cend_dist)), params)

        if c_nc > 1:
            pt_bolt_down = np.array(pitch_pts_c[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0, 1])
            pt_bolt_1_down = np.array(pitch_pts_c1[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0, 1])
            self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][-1]), pt_bolt_1_down, dwg)
            self.dataObj.draw_faint_line(np.array(pitch_pts_c[-1][-1]), pt_bolt_down, dwg)

            pt_down = np.array(pitch_pts_c1[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(self.dataObj.cgauge)), params)

            pt_down = np.array(pitch_pts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(self.dataObj.cgauge)), params)

            pt_down = np.array(pitch_pts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cgauge + self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 100, "textoffset": 35, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(c_gauge)), params)

        else:
            pt_down = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(c_gauge)), params)

        # ###################### Faint Lines and outer arrow for beam connectivity ############

        length = self.dataObj.D_col / 2 - self.dataObj.beam_tw / 2
        ptQ1 = self.P - self.dataObj.cleat_thk * np.array([1, 0])
        pt_left = ptQ1 - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(ptQ1, pt_left, dwg)

        pt = ptQ1 + self.dataObj.cleat_ht * np.array([0, 1])
        pt_left = pt - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt, pt_left, dwg)

        pt_left = np.array(pitch_pts[0]) - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts[0]), pt_left, dwg)
        pt_left = np.array(pitch_pts[-1]) - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts[-1]), pt_left, dwg)

        offset = length + 100
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[0]), np.array(pitch_pts[-1]),
                                                str(len(pitch_pts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)

        params = {"offset": offset, "textoffset": 60, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[0]), ptQ1, str(int(self.dataObj.edge_dist)), params)

        params = {"offset": offset, "textoffset": 60, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[-1]), pt, str(int(self.dataObj.edge_dist)), params)

        # ################ Beam Information ##############################################
        beam_pt = self.A2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam)/2 + 30
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        #       column  Information
        col_pt = self.A
        theta = 90
        offset = self.dataObj.beam_B/2
        text_up = "Column " + self.dataObj.col_Designation
        text_down = " "
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "NW", offset, text_up, text_down)

        #       cleat Angle Information
        beam_pt = self.R + self.dataObj.cleat_thk / 2 * np.array([-1, 0])
        theta = 45
        offset = self.dataObj.cleat_thk + self.dataObj.beam_B / 2 + 80
        text_up = "ISA. " + str(int(self.dataObj.cleat_legsize)) + 'x' + str(int(self.dataObj.cleat_legsize_1)) + 'x' + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        #       beam bolt information
        no_of_bbolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        boltPt = np.array(pitch_pts[0])
        theta = 60
        offset = (self.dataObj.D_col) / 2 + 10
        text_up = str(no_of_bbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, boltPt, theta, "NW", offset, text_up, text_down)

        #       column bolt information
        no_of_cbolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol

        boltPt = np.array(pitch_pts_c1[0][0])
        theta = 60
        offset =  (self.dataObj.D_col) / 2 + 10
        text_up = str(no_of_cbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, boltPt, theta, "NE", offset, text_up, text_down)

        # 2D view name
        ptx = self.G + (self.dataObj.beam_B + 100) * np.array([0, 1])
        dwg.add(dwg.text('Side view (Sec B-B)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        # # All dimensions in "mm"
        ptx2 = self.G + (self.dataObj.beam_B + 140) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx2), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CFBW_side(self, filename):
        '''
        '''
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox='-460 -300 1500 1600')
        dwg.add(dwg.rect(insert=(self.FA), size=(self.dataObj.col_B, self.dataObj.col_L), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(
            points=[(self.FA1), (self.FA2), (self.FA3), (self.FA4), (self.FA5), (self.FA6), (self.FA7), (self.FA8), (self.FA9), (self.FA10), (self.FA11),
                    (self.FA12), (self.FA1)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FX), size=((self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill="none", stroke='blue',
                         stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FQ), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FQ1), size=((self.dataObj.cleat_legsize_1 - self.dataObj.cleat_thk), self.dataObj.cleat_ht), fill="none", stroke='blue',
                         stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP1), size=(self.dataObj.cleat_thk, self.dataObj.cleat_ht), fill='none', stroke='blue', stroke_width=2.5))

        nr = self.dataObj.no_of_rows
        bolt_r = self.dataObj.bolt_dia / 2
        c_nr = self.dataObj.no_of_crows
        c_nc = self.dataObj.no_of_ccol

        pitch_pts = []
        pitch_pts_c = []
        pitch_pts_c1 = []
        for row in range(nr):
            pt = self.FQ + self.dataObj.edge_dist * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1])
            pt1 = pt - bolt_r * np.array([0, 1])
            rect_width = self.dataObj.bolt_dia
            rect_length = self.dataObj.beam_tw + 2 * self.dataObj.cleat_thk
            dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill="black", stroke='none', stroke_width=2.5))
            blt1 = pt - 5 * np.array([1, 0])
            blt2 = pt + (5 + rect_length) * np.array([1, 0])
            dwg.add(dwg.line((blt1), (blt2)).stroke('black', width=1.5, linecap='square'))
            pitch_pts.append(pt)

        for row1 in range(c_nr):
            col_list = []
            col_list1 = []
            for col in range(c_nc):
                pt_c = self.FX + self.dataObj.cedge_dist * np.array([0, 1]) + (self.dataObj.cend_dist) * np.array([1, 0]) + (
                                                                                                                            row1) * self.dataObj.cpitch * np.array(
                    [0, 1]) + (col) * self.dataObj.cgauge * np.array([1, 0])
                dwg.add(dwg.circle(center=(pt_c), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                cbolt1 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([1, 0])
                cbolt2 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([-1, 0])
                cbolt3 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, 1])
                cbolt4 = pt_c + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, -1])
                dwg.add(dwg.line((cbolt1), (cbolt2)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))
                dwg.add(dwg.line((cbolt3), (cbolt4)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))

                pt_c1 = self.FX1 + self.dataObj.cedge_dist * np.array([0, 1]) + (self.dataObj.cend_dist) * np.array([-1, 0]) + (
                                                                                                                               row1) * self.dataObj.cpitch * np.array(
                    [0, 1]) + (col) * self.dataObj.cgauge * np.array([-1, 0])
                dwg.add(dwg.circle(center=(pt_c1), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                cbolt1_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([1, 0])
                cbolt2_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([-1, 0])
                cbolt3_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, 1])
                cbolt4_1 = pt_c1 + (self.dataObj.bolt_dia / 2 + 4) * np.array([0, -1])
                dwg.add(dwg.line((cbolt1_1), (cbolt2_1)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))
                dwg.add(dwg.line((cbolt3_1), (cbolt4_1)).stroke('red', width=1.5, linecap='square').dasharray(dasharray=([10, 5, 1, 5])))

                col_list.append(pt_c)
                col_list1.append(pt_c1)
            pitch_pts_c.append(col_list)
            pitch_pts_c1.append(col_list1)

        # #################### Faint Lines and outer arrow for Primary beam connectivity ############
        length = (self.dataObj.col_B - self.dataObj.cleat_legsize_1 * 2 - self.dataObj.beam_tw) / 2 + 50
        pt_right = self.FX1 + (length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.FX1, pt_right, dwg)
        pt = self.FX1 + self.dataObj.cleat_ht * np.array([0, 1])
        pt_right = self.FX1 + self.dataObj.cleat_ht * np.array([0, 1]) + (length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt, pt_right, dwg)

        pt_right = np.array(pitch_pts_c1[0][0]) + (self.dataObj.cend_dist + length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[0][0]), pt_right, dwg)
        pt_right = np.array(pitch_pts_c1[-1][0]) + (self.dataObj.cend_dist + length + 200) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][0]), pt_right, dwg)

        params = {"offset": length + 20, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.X1, self.X1 + self.dataObj.cleat_ht * np.array([0, 1]), str(int(self.dataObj.cleat_ht)), params)

        offset = self.dataObj.cend_dist + length + 200
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[0][0]), np.array(pitch_pts_c1[-1][0]),
                                                str(len(pitch_pts_c1) - 1) + "@" + str(int(self.dataObj.cpitch)) + " c/c", params)

        pt_up = np.array(pitch_pts_c1[0][0]) - self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[0][0]), pt_up, str(int(self.dataObj.cedge_dist)), params)

        pt_down = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts_c1[-1][0]), pt_down, str(int(self.dataObj.cedge_dist)), params)

        # ###########Vertical column marking ###############
        v_length = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam / 2 - (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptY = self.FX + self.dataObj.cleat_ht * np.array([0, 1])
        ptY1 = self.FX1 + self.dataObj.cleat_ht * np.array([0, 1])
        ptY_down = ptY + v_length * np.array([0, 1])
        ptY1_down = ptY1 + v_length * np.array([0, 1])
        self.dataObj.draw_faint_line(ptY, ptY_down, dwg)
        self.dataObj.draw_faint_line(ptY1, ptY1_down, dwg)

        pt_bolt = np.array(pitch_pts_c[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0, 1])
        pt_bolt_1 = np.array(pitch_pts_c1[-1][0]) + (v_length + 50 + self.dataObj.cedge_dist) * np.array([0, 1])
        self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][0]), pt_bolt_1, dwg)
        self.dataObj.draw_faint_line(np.array(pitch_pts_c[-1][0]), pt_bolt, dwg)

        pt_down = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "right", "endlinedim": 20}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptY, pt_down, str(int(self.dataObj.cend_dist)), params)

        pt_down = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
        params = {"offset": v_length, "textoffset": 35, "lineori": "left", "endlinedim": 20}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptY1, pt_down, str(int(self.dataObj.cend_dist)), params)

        if c_nc > 1:
            pt_bolt_down = np.array(pitch_pts_c[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0, 1])
            pt_bolt_1_down = np.array(pitch_pts_c1[-1][-1]) + (v_length + 100 + self.dataObj.cedge_dist) * np.array([0, 1])
            self.dataObj.draw_faint_line(np.array(pitch_pts_c1[-1][-1]), pt_bolt_1_down, dwg)
            self.dataObj.draw_faint_line(np.array(pitch_pts_c[-1][-1]), pt_bolt_down, dwg)

            pt_down = np.array(pitch_pts_c1[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(self.dataObj.cgauge)), params)

            pt_down = np.array(pitch_pts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            params = {"offset": v_length + 50, "textoffset": 35, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(self.dataObj.cgauge)), params)
            pt_down = np.array(pitch_pts_c[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][-1]) + self.dataObj.cedge_dist * np.array([0, 1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cgauge + self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length + 100, "textoffset": 35, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(c_gauge)), params)

        else:
            pt_down = np.array(pitch_pts_c[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            pt_down_left = np.array(pitch_pts_c1[-1][0]) + self.dataObj.cedge_dist * np.array([0, 1])
            c_gauge = 2 * self.dataObj.cleat_legsize_1 - 2 * (self.dataObj.cend_dist) - self.dataObj.beam_tw
            params = {"offset": v_length , "textoffset": 35, "lineori": "right", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, pt_down, pt_down_left, str(int(c_gauge)), params)


            ####################### Faint Lines and outer arrow for beam connectivity ############

        length = self.dataObj.col_B / 2 - self.dataObj.beam_tw / 2 - self.dataObj.cleat_thk
        ptQ1 = self.FP - self.dataObj.cleat_thk * np.array([1, 0])
        pt_left = ptQ1 - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(ptQ1, pt_left, dwg)
        pt = ptQ1 + self.dataObj.cleat_ht * np.array([0, 1])
        pt_left = pt - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt, pt_left, dwg)

        pt_left = np.array(pitch_pts[0]) - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts[0]), pt_left, dwg)
        pt_left = np.array(pitch_pts[-1]) - (length + 100) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pitch_pts[-1]), pt_left, dwg)

        offset = length + 150
        params = {"offset": offset, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[0]), np.array(pitch_pts[-1]),
                                                str(len(pitch_pts) - 1) + "@" + str(int(self.dataObj.pitch)) + " c/c", params)

        params = {"offset": offset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[0]), ptQ1, str(int(self.dataObj.edge_dist)), params)

        params = {"offset": offset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pitch_pts[-1]), pt, str(int(self.dataObj.edge_dist)), params)

        ###################################################################################################################
        ##### Beam Information
        beam_pt = (self.FA2 + self.FA1) / 2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + 50
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # column  Information
        col_pt = self.FA
        theta = 90
        offset = 50
        text_up = "Column " + self.dataObj.col_Designation
        text_down = " "
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "NW", offset, text_up, text_down)

        # cleat Angle Information
        beam_pt = (self.FX3)
        theta = 40
        offset = self.dataObj.cleat_ht / 2
        text_up = "ISA. " + str(int(self.dataObj.cleat_legsize)) + 'x' + str(int(self.dataObj.cleat_legsize_1)) + 'x' + str(int(self.dataObj.cleat_thk))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # beam bolt information
        no_of_bbolts = self.dataObj.no_of_rows * self.dataObj.no_of_col
        boltPt = np.array(pitch_pts[0])
        theta = 60
        offset = (self.dataObj.col_B) / 2 + 130
        text_up = str(no_of_bbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.draw_oriented_arrow(dwg, boltPt, theta, "NE", offset, text_up, text_down)

        # column bolt information
        no_of_cbolts = self.dataObj.no_of_crows * 2 * self.dataObj.no_of_ccol
        boltPt = np.array(pitch_pts_c1[0][0])
        theta = 55
        offset =  (self.dataObj.col_B) / 2.2 + 30
        text_up = str(no_of_cbolts) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        # text_down = "for M" + str(self.dataObj.bolt_dia) + 'bolts' + '(grade ' + str(self.dataObj.bolt_grade) + ')'
        self.dataObj.draw_oriented_arrow(dwg, boltPt, theta, "NE", offset, text_up, text_down)

        # 2D view name
        ptx = self.G + (self.dataObj.beam_B + 50) * np.array([0, 1])  # 1190
        dwg.add(dwg.text('Side view (Sec B-B)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        # # All dimensions in "mm"
        ptx2 = self.G + (self.dataObj.beam_B + 90) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=(ptx2), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()
