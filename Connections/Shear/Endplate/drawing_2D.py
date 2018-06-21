'''
Created on 24-Aug-2015

@author: deepa
'''
# from PyQt4.QtCore import QString
import svgwrite
import numpy as np
from numpy import math
from cmath import sqrt
import cairosvg
import os



class EndCommonData(object):
    def __init__(self, input_obj, ouput_obj, dict_beam_data, dict_column_data, folder):
        '''
        Provide all the data related to EndPlate connection

        :param input_obj:
        :type input_obj:dictionary(Input parameter dictionary)
        :param outputObj:
        :type ouput_obj :dictionary (output parameter dictionary)
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
        self.plate_ht = ouput_obj['Plate']['height']
        self.plate_thick = int(input_obj['Plate']["Thickness (mm)"])
        self.bolt_grade = float(input_obj['Bolt']['Grade'])
        self.bolt_type = str(input_obj['Bolt']['Type'])
        self.plate_width = ouput_obj['Plate']['width']
        self.weld_len = ouput_obj['Weld']['weldlength']
        self.weld_thick = int(input_obj['Weld']['Size (mm)'])
        self.bolt_dia = int(input_obj["Bolt"]["Diameter (mm)"])
        self.dia_hole = int(ouput_obj['Bolt']['dia_hole'])
        self.connectivity = input_obj['Member']['Connectivity']
        self.pitch = ouput_obj['Bolt']["pitch"]
        self.gauge = ouput_obj['Bolt']["gauge"]
        self.end_dist = ouput_obj['Bolt']["enddist"]
        self.edge_dist = ouput_obj['Bolt']["edge"]
        self.no_of_rows = ouput_obj['Bolt']["numofrow"]
        self.no_of_col = ouput_obj['Bolt']["numofcol"]
        self.sectional_gauge = ouput_obj['Plate']['Sectional Gauge']
        self.col_L = 800
        self.beam_L = 350
        self.R1_max = max([self.col_R1, self.beam_R1, 10])
        #self.notch_L = (self.beam_B / 2 - self.beam_tw / 2) + 10
        self.notch_width = (self.col_B / 2.0 - (self.col_tw / 2.0 + self.plate_thick)) + self.plate_thick
        self.notch_offset = (self.col_T + self.col_R1)
        self.notch_ht = max([self.col_T, self.beam_T]) + max([self.col_R1, self.beam_R1]) + max([(self.col_T / 2), (self.beam_T / 2), 10])

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

        # smarker = dwg.marker(insert=(-8,0), size =(30,20), orient="auto")
        # smarker.add(dwg.polyline([(-2.5,0), (0,3), (-8,0), (0,-3)], fill='black'))
        # smarker.add(dwg.polyline([(0,0), (3,3), (0,6), (8,3),(0,0)], fill='black'))

        return smarker

    def add_section_maker(self, dwg):
        '''
        Draws start arrow to given line  -------->

        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)

        '''
        section_marker = dwg.marker(insert=(0, 5), size=(10, 10), orient="auto")
        section_marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill='blue', stroke='black'))
        dwg.defs.add(section_marker)

        return section_marker

    def add_e_marker(self, dwg):
        '''
        This routine returns end arrow  <---------

        :param dwg :
        :type dwg : svgwrite  ( Container for all svg elements)

        '''
        # emarker = dwg.marker(insert=(8,0), size =(30,20), orient="auto")
        emarker = dwg.marker(insert=(0, 3), size=(30, 20), orient="auto")
        # emarker.add(dwg.polyline([(2.5,0), (0,3), (8,0), (0,-3)], fill='black'))
        # emarker.add(dwg.polyline([(0,3), (8,6), (5,3), (8,0),(0,3)], fill='black'))
        # emarker.add(dwg.path(d="M2,2 L2,13 L8,7 L2,2"", fill='red'))
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

    def draw_weld_arrow(self, ptweld, dwg):
        ptweld2 = ptweld + (sqrt(3) * 5 / 2) * np.array([1, 0]) + 5 / 2 * np.array([0, 1])
        ptweld3 = ptweld + (sqrt(3) * 5 / 2) * np.array([1, 0]) - 5 / 2 * np.array([0, 1])
        dwg.add(dwg.polyline(points=[ptweld, ptweld2, ptweld3], stroke='black', fill='none', stroke_width=2.5))

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
        if (params["lineori"] == "left"):
            normal_unit_vector = -normal_unit_vector

        # Q1 = pt1 + params["offset"] * normal_unit_vector
        # Q2 = pt2 + params["offset"] * normal_unit_vector
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
        self.draw_end_arrow(line, sec_arrow)
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

        # smarker = self.add_s_marker(dwg)
        # emarker = self.add_e_marker(dwg)
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

    def draw_oriented_arrow(self, dwg, pt, theta, orientation, offset, text_up, text_down, element):

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
            txt_pt_up = p2 + 0.05 * lengthB * (-label_vector) + txt_offset * offset_vector
            txt_pt_down = p2 - 0.1 * lengthB * (label_vector) - (txt_offset + 15) * offset_vector
        elif (orientation == "SW"):
            txt_pt_up = p3 + 0.1 * lengthB * label_vector + (txt_offset) * offset_vector
            txt_pt_down = p3 - 0.1 * lengthB * label_vector - (txt_offset + 15) * offset_vector

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill='none', stroke='black', stroke_width=2.5))

        # smarker = self.add_s_marker(dwg)
        emarker = self.add_e_marker(dwg)
        # self.draw_start_arrow(line, smarker)
        self.draw_start_arrow(line, emarker)

        dwg.add(dwg.text(text_up, insert=(txt_pt_up), fill='black', font_family="sans-serif", font_size=28))
        dwg.add(dwg.text(text_down, insert=(txt_pt_down), fill='black', font_family="sans-serif", font_size=28))

        if element == "weld":
            if orientation == "NW":
                self.draw_weld_marker(dwg, 15, 7.5, line)
            else:
                self.draw_weld_marker(dwg, 45, 7.5, line)

    def draw_weld_marker(self, dwg, oriX, oriY, line):

        weld_marker = dwg.marker(insert=(oriX, oriY), size=(15, 15), orient="auto")
        weld_marker.add(dwg.path(d="M 0 0 L 8 7.5 L 0 15 z", fill='none', stroke='black'))
        dwg.defs.add(weld_marker)
        self.draw_end_arrow(line, weld_marker)


    def save_to_svg(self, filename, view):
        '''
         It returns the svg drawing depending upon connectivity
        CFBW = Column Flange Beam Web
        CWBW = Column Web Beam Web
        BWBW = Beam Web Beam Web

        '''
        end_2d_front = End2DCreatorFront(self)
        end_2d_top = End2DCreatorTop(self)
        end_2d_side = End2DCreatorSide(self)

        if self.connectivity == 'Column flange-Beam web':
            if view == "Front":
                filename = end_2d_front.call_CFBW_front(filename)
            elif view == "Side":
                filename = end_2d_side.call_CFBW_side(filename)
            elif view == "Top":
                filename = end_2d_top.call_CFBW_top(filename)
            else:
                filename = os.path.join(str(self.folder), "images_html", "endFront.svg")
                end_2d_front.call_CFBW_front(filename)
                cairosvg.svg2png(file_obj=filename, write_to= os.path.join(str(self.folder), "images_html", "endFront.png"))

                filename = os.path.join(str(self.folder), "images_html", "endSide.svg")
                end_2d_side.call_CFBW_side(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endSide.png"))

                filename = os.path.join(str(self.folder), "images_html", "endTop.svg")
                end_2d_top.call_CFBW_top(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endTop.png"))

        elif self.connectivity == 'Column web-Beam web':
            if view == "Front":
                end_2d_front.call_CWBW_front(filename)
            elif view == "Side":
                end_2d_side.call_CWBW_side(filename)
            elif view == "Top":
                end_2d_top.call_CWBW_top(filename)
            else:
                filename = os.path.join(str(self.folder), "images_html", "endFront.svg")
                end_2d_front.call_CWBW_front(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endFront.png"))

                filename = os.path.join(str(self.folder), "images_html", "endSide.svg")
                end_2d_side.call_CWBW_side(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endSide.png"))

                filename = os.path.join(str(self.folder), "images_html", "endTop.svg")
                end_2d_top.call_CWBW_top(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endTop.png"))

        else:
            if view == "Front":
                end_2d_front.call_BWBW_front(filename)
            elif view == "Side":
                end_2d_side.call_BWBW_side(filename)
            elif view == "Top":
                end_2d_top.call_BWBW_top(filename)
            else:
                filename = os.path.join(str(self.folder), "images_html", "endFront.svg")
                end_2d_front.call_BWBW_front(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endFront.png"))

                filename = os.path.join(str(self.folder), "images_html", "endSide.svg")
                end_2d_side.call_BWBW_side(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endSide.png"))

                filename = os.path.join(str(self.folder), "images_html", "endTop.svg")
                end_2d_top.call_BWBW_top(filename)
                cairosvg.svg2png(file_obj=filename, write_to=os.path.join(str(self.folder), "images_html", "endTop.png"))


class End2DCreatorFront(object):
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

        self.U = self.ptP + (self.dataObj.plate_ht) * np.array([0, 1])

        ptRx = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + int(self.dataObj.plate_thick)
        ptRy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.R = (ptRx, ptRy)

        ptSx = ptRx
        ptSy = ptPy + self.dataObj.plate_ht
        self.S = (ptSx, ptSy)

        self.W = self.ptP + self.dataObj.plate_thick * np.array([1, 0])

        ptC1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick)
        ptC1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.C1 = np.array([ptC1x, ptC1y])

        ptA1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick)
        ptA1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        self.A1 = np.array([ptA1x, ptA1y])

        ptA3x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick) + self.dataObj.beam_L
        ptA3y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        self.A3 = (ptA3x, ptA3y)

        ptB3x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick) + self.dataObj.beam_L
        ptB3y = ((self.dataObj.col_L + self.dataObj.D_beam) / 2)
        self.B3 = (ptB3x, ptB3y)

        ptB1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick)
        ptB1y = ((self.dataObj.col_L + self.dataObj.D_beam) / 2)
        self.B1 = np.array([ptB1x, ptB1y])
        self.ptB1 = np.array([ptB1x, ptB1y])

        ptC2x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick)
        ptC2y = ptC1y + self.dataObj.plate_ht
        self.C2 = (ptC2x, ptC2y)

        ptA5x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick)
        ptA5y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + self.dataObj.beam_T
        self.A5 = ptA5x, ptA5y

        ptA4x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick) + self.dataObj.beam_L
        ptA4y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + self.dataObj.beam_T
        self.A4 = (ptA4x, ptA4y)

        ptB4x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick) + self.dataObj.beam_L
        ptB4y = ((self.dataObj.col_L + self.dataObj.D_beam) / 2) - self.dataObj.beam_T
        self.B4 = (ptB4x, ptB4y)

        ptBx5 = ((self.dataObj.col_B + self.dataObj.col_tw) / 2) + self.dataObj.plate_thick
        ptBy5 = ((self.dataObj.col_L + self.dataObj.D_beam) / 2) - self.dataObj.beam_T
        self.B5 = (ptBx5, ptBy5)

        ptP1x = ((self.dataObj.col_B + self.dataObj.col_tw) / 2)
        ptP1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + (self.dataObj.col_tw + self.dataObj.beam_R1 + 3) + self.dataObj.end_dist)
        self.P1 = (ptP1x, ptP1y)

        #### Column flange points for column flange beam web connectivity #####

        from_plate_pt = self.dataObj.D_col + self.dataObj.plate_thick  # 20 mm clear distance between colume and beam
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
        self.FG = np.array([ptFGx, ptFGy])

        ptFHx = self.dataObj.col_T
        ptFHy = self.dataObj.col_L
        self.FH = np.array([ptFHx, ptFHy])

        ptFDx = 0.0
        ptFDy = self.dataObj.col_L
        self.FD = (ptFDx, ptFDy)

        ptFPx = self.dataObj.D_col
        ptFPy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FP = (ptFPx, ptFPy)
        self.ptFP = np.array([ptFPx, ptFPy])

        ptFUx = self.dataObj.D_col
        ptFUy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
        self.FU = (ptFUx, ptFUy)

        self.FW = self.FP + self.dataObj.plate_thick * np.array([1, 0])

        # FC1
        ptFC1x = from_plate_pt
        ptFC1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FC1 = np.array([ptFC1x, ptFC1y])

        # FC2
        ptFC2x = from_plate_pt
        ptFC2y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
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
        ptFB1x = self.dataObj.D_col + self.dataObj.plate_thick
        ptFB1y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam
        self.FB1 = np.array([ptFB1x, ptFB1y])

        # FB4
        ptFB4x = from_plate_pt
        ptFB4y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB4 = ptFB4x, ptFB4y

        # ######################################## POINTS FOR BEAM BEAM CONNECTION ####################################################

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

        self.BP = self.BD + self.dataObj.col_T * np.array([0, -1]) + self.dataObj.notch_ht * np.array([0, 1])
        #self.BA1 = self.BB + 10 * np.array([1, 0])
        self.BA1 = self.BB + self.dataObj.plate_thick * np.array([1, 0])
        #self.BA2 = self.BA1 + (self.dataObj.beam_L - 10 - self.dataObj.col_B / 2 + self.dataObj.col_tw / 2 + self.dataObj.plate_thick) * np.array([1, 0])
        #self.BA2 = self.BA1 + (self.dataObj.beam_L-(self.dataObj.col_B/2 -(self.dataObj.col_tw/2 + self.dataObj.plate_thick))+ self.dataObj.plate_thick) * np.array([1, 0])
        self.BA2 = self.BA1 + (self.dataObj.beam_L- self.dataObj.notch_width) * np.array([1, 0])
        self.BA3 = self.BA2 + self.dataObj.beam_T * np.array([0, 1])
        self.BB2 = self.BA2 + self.dataObj.D_beam * np.array([0, 1])
        self.BB3 = self.BB2 + self.dataObj.beam_T * np.array([0, -1])
        self.BB1 = self.BB2 + self.dataObj.beam_L * np.array([-1, 0])
        self.BB4 = self.BB1 + self.dataObj.beam_T * np.array([0, -1])
        self.BA4 = self.BA1 + self.dataObj.beam_T * np.array([0, 1])
        self.BA6 = self.BP + self.dataObj.plate_thick * np.array([1,0])
        self.BB5 = self.BA6 + self.dataObj.plate_ht * np.array([0,1])
        self.BA5 = self.BA1 + self.dataObj.notch_ht * np.array([0, 1])
        #self.BC1 = self.BB1 - (self.dataObj.D_beam - self.dataObj.notch_offset) * np.array([0, 1])
        self.BC1 = self.BA5 + self.dataObj.R1_max * np.array([0, -1])
        self.BC2 = self.BA5 + self.dataObj.R1_max * np.array([-1, 0])
        self.BX = self.BA6 + self.dataObj.weld_thick * np.array([1,0])
        self.BY = self.BX + self.dataObj.plate_ht * np.array([0,1])
        # self.BC1 = self.BB1 - (self.dataObj.D_beam - self.dataObj.notch_offset) * np.array([0, 1])
        # self.BC2 = self.BC1 + self.dataObj.plate_ht * np.array([0, 1])
        #self.BA5 = self.BA1 + self.dataObj.notch_offset * np.array([0, 1])

        # for end plate

        #self.BP = self.BC1 - self.dataObj.plate_thick * np.array([1, 0])

    def call_BWBW_front(self, filename):
        v_height = self.dataObj.D_col + 850
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-310 -400 1500 1500'))

        # Cross section A-A
        ptSecA = self.BA + (320 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BC), (self.BD), (self.BE), (self.BF), (self.BG), (self.BH), (self.BI), (self.BJ), (self.BK),
                                     (self.BL), (self.BA)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        pt1 = self.BA5 - self.dataObj.col_R1 * np.array([0, 1])
        pt2 = self.BA5 - self.dataObj.col_R1 * np.array([1, 0])
        # dwg.add(dwg.polyline(points=[pt1, self.BA1, self.BA2, self.BB2, self.BB1, self.BB4, self.BC2, self.BC1, pt2], stroke='blue',
        #                      fill='none', stroke_width=2.5))
        # Secondary beam
        dwg.add(dwg.polyline(points = [(self.BC1),(self.BA4),(self.BA1),(self.BA2),(self.BB2),(self.BB1),(self.BB4),(self.BB5)],stroke = 'blue',
                        fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.line((self.BB5), (self.BA6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line(self.BA4, self.BA3).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.BB4, self.BB3).stroke('blue', width=2.5, linecap='square'))
        d = []
        d.append("M")
        d.append(self.BC1)
        d.append("A")
        d.append(np.array([self.dataObj.R1_max, self.dataObj.R1_max]))
        d.append(",")
        d.append("0")
        d.append(",")
        d.append("0")
        d.append(",")
        d.append("1")
        d.append(",")
        d.append(self.BC2)
        dwg.add(dwg.path(d=d, stroke="blue", fill="none", stroke_width="2.5"))

        # Weld hatching to represent WELD.
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(4, 4), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))
        dwg.add(dwg.rect(insert=(self.BA6), size=(self.dataObj.weld_thick, self.dataObj.plate_ht),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=2.0))
        dwg.add(dwg.rect(insert=self.BP, size=(self.dataObj.plate_thick, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line(self.BA6, self.BC2).stroke('blue', width=2.5, linecap='square'))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []

        for i in range(1, (nr + 1)):
            pt = self.BP - self.dataObj.col_tw * np.array([1, 0]) + self.dataObj.end_dist * np.array([0, 1]) + \
                 (i - 1) * self.dataObj.pitch * np.array([0, 1])

            pt1 = pt - bolt_r * np.array([0, 1])
            rect_length = (self.dataObj.col_tw + self.dataObj.plate_thick)
            rect_width = self.dataObj.bolt_dia

            dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
            B1 = pt + 10 * np.array([-1, 0])
            B2 = pt + (rect_length + 10) * np.array([1, 0])
            dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

            pt_list.append(pt)

        pitch_pts = []
        for row in pt_list:
            if len(row) > 0:
                pitch_pts.append(row[0])
        params = {"offset": self.dataObj.col_B / 2 - self.dataObj.col_tw / 2 + 50, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[-1]),
                                                str(len(pitch_pts) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) + "c/c", params)

        # Distance between Beam Flange and Plate
        BA_down = self.BA + (self.dataObj.notch_offset) * np.array([0, 1])
        params = {"offset": 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BA, BA_down, str(int(self.dataObj.notch_offset)), params)
        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        pt_one = self.BA
        pt_two = self.BA - 50 * np.array([1, 0])
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        pt_one = self.BP
        pt_two = self.BP - (self.dataObj.col_B + self.dataObj.col_tw + 100) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        # End Distance from the starting point of plate Information
        edgPt = self.BP - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": self.dataObj.col_B / 2 - self.dataObj.col_tw / 2 + 50, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), edgPt, str(int(self.dataObj.end_dist)), params)

        # End Distance from plate end point.
        edgPt1 = self.BP + self.dataObj.plate_ht * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": self.dataObj.col_B / 2 - self.dataObj.col_tw / 2 + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[-1]), edgPt1, str(int(self.dataObj.end_dist)), params)
        self.dataObj.draw_faint_line(edgPt1, edgPt1 - (self.dataObj.col_B + self.dataObj.col_tw + 100) / 2 * np.array([1, 0]), dwg)
        # ##### Draws faint line to show dimensions #########
        # Faint lines for gauge and edge distances

        pt_two = np.array(pt_list[0]) - (self.dataObj.col_B - self.dataObj.col_tw + 100) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), pt_two, dwg)

        pt_three = np.array(pt_list[-1]) - (self.dataObj.col_B - self.dataObj.col_tw + 100) / 2 * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[-1]), pt_three, dwg)

        # Beam Information
        beam_pt = self.BA2 + self.dataObj.D_beam / 2 * np.array([0, 1])
        theta = 1
        offset = 0.0
        text_up = "Secondary beam " + self.dataObj.beam_Designation
        text_down = ""

        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # Column Designation

        pt = (self.BH + self.BG) / 2
        theta = 90
        offset = 150
        text_up = "Primary beam " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, pt, theta, "SE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.BC1 + (self.dataObj.weld_thick / 2) * np.array([1, 0])
        theta = 35
        offset = self.dataObj.col_B/2
        text_up = " z " + str(int(self.dataObj.weld_thick))
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down, element="weld")

        # Bolt Information
        bolt_pt_x = np.array(pt_list[-1])
        theta = 65
        offset = (self.dataObj.D_beam/1.4)
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "SE", offset, text_up, text_down, element="")

        # Plate Information

        plate_pt = self.BC1 - (self.dataObj.plate_thick / 2) * np.array([1, 0])
        theta = 90
        offset = (self.dataObj.beam_L/2)
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + "X" + str(int(self.dataObj.plate_width)) + "X" + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plate_pt, theta, "NE", offset, text_up, text_down, element="")

        # 2D view name
        ptx = self.BH + 150 * np.array([1, 0]) + 210 * np.array([0, 1])
        dwg.add(dwg.text("Front view (Sec C-C)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = self.BH + 150 * np.array([1, 0]) + 250 * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "########### Beam web Beam web saved ###########"

    def call_CFBW_front(self, filename):
        v_width = self.dataObj.D_col + 1000
        # dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-340 -280 ' + str(v_width) + ' 1225'))
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-350 -350 1500 1500'))

        # Cross section A-A
        ptSecA = self.FA + ( self.dataObj.D_col / 1.5 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.FA), (self.FB), (self.FC), (self.FD), (self.FA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.FE), (self.FH)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FF), (self.FG)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.FC1), (self.FA1), (self.FA2), (self.FB2), (self.FB1), (self.FC2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.FC1), (self.FC2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.FA4), (self.FA3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FB4), (self.FB3)).stroke('blue', width=2.5, linecap='square'))

        # Weld hatching to represent WELD.
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(4, 4), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))

        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.plate_thick, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FW), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.0))

        dwg.add(dwg.line((self.FC1), (self.FC2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []

        for i in range(1, (nr + 1)):
            pt = self.FP - self.dataObj.col_T * np.array([1, 0]) + self.dataObj.end_dist * np.array([0, 1]) + \
                 (i - 1) * self.dataObj.pitch * np.array([0, 1])

            pt1 = pt - bolt_r * np.array([0, 1])
            rect_length = (self.dataObj.col_T + self.dataObj.plate_thick)
            rect_width = self.dataObj.bolt_dia

            dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
            B1 = pt + 10 * np.array([-1, 0])
            B2 = pt + (rect_length + 10) * np.array([1, 0])
            dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

            pt_list.append(pt)

        pitch_pts = []
        for row in pt_list:
            if len(row) > 0:
                pitch_pts.append(row[0])
        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 50, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[-1]), str(len(pitch_pts) - 1) + u' \u0040' +
                                                str(int(self.dataObj.pitch)) + "c/c", params)

        # Distance between Beam Flange and Plate

        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 90, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.FA1, self.FC1, str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)), params)
        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        pt_one = self.FA1
        ptBx = 70 * np.array([-1, 0])
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        pt_two = self.FA1 - (60 + self.dataObj.D_col + self.dataObj.plate_thick) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt_one, pt_two, dwg)

        # End Distance from the starting point of plate Information
        edgPt = self.FP - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 50 , "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), edgPt, str(int(self.dataObj.end_dist)), params)

        # End Distance from plate end point.
        edgPt1 = self.FU - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 50 , "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[-1]), edgPt1, str(int(self.dataObj.end_dist)), params)

        # Edge Distance information
        pt1A = self.ptFP + self.dataObj.edge_dist * np.array([1, 0]) + \
               (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0]) + self.dataObj.end_dist * np.array([0, 1])
        pt1B = self.ptFP + self.dataObj.edge_dist * np.array([1, 0]) + \
               (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0]) + self.dataObj.edge_dist * np.array(
            [1, 0]) + self.dataObj.end_dist * np.array([0, 1])
        offset = self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3
        params = {"offset": self.dataObj.D_col + self.dataObj.edge_dist, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        # self.dataObj.draw_dimension_outer_arrow(dwg, pt1A, pt1B, str(int(self.dataObj.edge_dist)) + " mm" , params)

        # Faint line for Edge distance dimension
        ptB1 = self.ptFP + self.dataObj.edge_dist * np.array([1, 0]) + \
               (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0]) + self.dataObj.edge_dist * np.array([1, 0])
        ptB2 = ptB1 + ((self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 115) * np.array([0, -1])
        # self.dataObj.draw_faint_line(ptB1,ptB2,dwg)

        # Gap Distance
        gap_pt = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3))
        ptG1 = self.ptFP + (gap_pt + 30) * np.array([0, 1])
        ptG2 = self.FC1 + (gap_pt + 30) * np.array([0, 1])
        offset = self.dataObj.col_L  # 60% of the column length
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.dataObj.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.dataObj.plate_thick) + " mm", params)

        # Draw Faint line for Gap Distance
        ptC1 = self.FC
        ptC2 = ptC1 + 40 * np.array([0, 1])
        self.dataObj.draw_faint_line(ptC1,ptC2,dwg)

        ptD1 = self.FB1
        ptD2 = ptD1 + 240 * np.array([0, 1])
        self.dataObj.draw_faint_line(ptD1,ptD2,dwg)

        # ##### Draws faint line to show dimensions #########
        # Faint lines for gauge and edge distances
        pt_one = self.FP - (80 + self.dataObj.D_col) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.FP, pt_one, dwg)

        pt_two = np.array(pt_list[0]) - (80 + self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), pt_two, dwg)

        pt_three = np.array(pt_list[-1]) - (80 + self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[-1]), pt_three, dwg)

        pt_four = self.FU - (80 + self.dataObj.D_col) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.FU, pt_four, dwg)

        # Beam Information
        beam_pt = self.FA2 + self.dataObj.D_beam / 2 * np.array([0, 1])
        theta = 1
        offset = 0.0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # Column Designation

        pt = (self.FH + self.FG) / 2
        theta = 90
        offset = self.dataObj.col_L / 17 + 20
        text_up = ""
        text_down = "Column " + self.dataObj.col_Designation
        self.dataObj.draw_oriented_arrow(dwg, pt, theta, "SW", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.FW + (self.dataObj.weld_thick / 2) * np.array([1, 0])
        theta = 65
        offset = self.dataObj.D_col - 50
        text_up = "                z " + str(int(self.dataObj.weld_thick))
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down, element="weld")

        # Bolt Information
        bolt_pt_x = np.array(pt_list[0])
        theta = 65
        offset = (self.dataObj.D_beam * 3 + 400) / 8
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) +  u'\u00d8'  + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down, element="")

        # Plate Information

        plate_pt = self.FU + (self.dataObj.plate_thick / 2) * np.array([1, 0])
        theta = 55
        offset = (self.dataObj.D_beam + 100) / 2
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + "X" + str(int(self.dataObj.plate_width)) + "X" + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plate_pt, theta, "SE", offset, text_up, text_down, element="")

        # 2D view name
        ptx = self.FC + self.dataObj.col_B/3 * np.array([0, 1])
        dwg.add(dwg.text("Front view (Sec C-C)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = self.FC + (self.dataObj.col_B/3 + 40) * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"########### Column Flange Beam Web Saved ############"

    def call_CWBW_front(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-400 -250 1400 1400'))

        # Cross section A-A
        ptSecA = self.A + (220 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.A2), (self.B), (self.A), (self.D), (self.C), (self.B2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.E), (self.H)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.F), (self.G)).stroke('blue', width=2.5, linecap='square'))

        # Diagonal Hatching to represent WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(4, 4), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))

        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.plate_thick, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.W), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.0))

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
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []

        for i in range(1, (nr + 1)):
            pt = self.ptP - self.dataObj.col_tw * np.array([1, 0]) + self.dataObj.end_dist * np.array([0, 1]) + \
                 (i - 1) * self.dataObj.pitch * np.array([0, 1])

            pt1 = pt - bolt_r * np.array([0, 1])
            rect_length = (self.dataObj.col_tw + self.dataObj.plate_thick)
            rect_width = self.dataObj.bolt_dia

            dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
            B1 = pt + 10 * np.array([-1, 0])
            B2 = pt + (rect_length + 10) * np.array([1, 0])
            dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

            pt_list.append(pt)

        pitch_pts = []
        for row in pt_list:
            if len(row) > 0:
                pitch_pts.append(row[0])

        txt_offset = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80, "textoffset": 150,
                  "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[-1]), str(len(pitch_pts) - 1) + u' \u0040' +
                                                str(int(self.dataObj.pitch)) + "c/c", params)

        # End Distance from the starting point of plate Information
        edgePt = self.P - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), edgePt, str(int(self.dataObj.end_dist)), params)

        # Distance between Beam Flange and Plate
        offset = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick + 80
        params = {"offset": offset , "textoffset": 50, "lineori": "right",
                  "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.A1, self.C1, str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)), params)

        # Draw Faint line for dimensions
        pt_zero =  self.A1 + ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80) * np.array([-1, 0])
        self.dataObj.draw_faint_line(self.A1, pt_zero, dwg)

        pt_one = self.ptP - ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.ptP, pt_one, dwg)

        pt_two = np.array(pt_list[0]) - ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80)  * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), pt_two, dwg)

        pt_three = np.array(pt_list[-1]) - ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80) * np.array([1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[-1]), pt_three, dwg)

        pt_four = self.U - ((self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80) * np.array([1, 0])
        self.dataObj.draw_faint_line(self.U, pt_four, dwg)

        # End Distance from plate end point.
        edgePt1 = self.U - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80,
                  "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[-1]), edgePt1, str(int(self.dataObj.edge_dist)), params)

        # -----------------------------------  Gap Distance - Gap is not required for Endplate -------------------------------------------
        # Draw Faint Lines to representation of Gap distance #
        # dist1 = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam)
        # ptA = self.B1
        # ptB = ptA + (dist1 + 100)* np.array([0,1])
        # self.dataObj.draw_faint_line(ptA,ptB,dwg)
        # ptC = self.G
        # ptD = ptC + (100)*np.array([0,1])
        # self.dataObj.draw_faint_line(ptC,ptD,dwg)
        #
        # ptG1 = self.G + (dist1 + 50)* np.array([0,1])
        # ptG2 = ptG1 - self.dataObj.gap * np.array([-1,0]) + (dist1 + 50)* np.array([0,1])
        # offset = 1
        # params = {"offset": offset, "textoffset": 120, "lineori": "right", "endlinedim":10,"arrowlen":50}
        # self.dataObj.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)
        # -----------------------------------------------------------------------------------------------------------------------------------------------

        # Edge Distance Information
        # ptA = self.ptP + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0])
        # ptB = ptA + self.dataObj.edge_dist * np.array([1, 0])
        # offset_dist = -(self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 120)
        # params = {"offset": offset_dist, "textoffset": 35, "lineori": "right", "endlinedim": 10}
        # self.dataObj.draw_dimension_outer_arrow(dwg,ptA,ptB, str(int(self.dataObj.edge_dist)) + " mm", params)

        # Plate Width Information
        plate_pt = self.U + (self.dataObj.plate_thick / 2) * np.array([1, 0])
        theta = 45
        offset = (self.dataObj.D_beam + 100) / 2
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + "X" + str(int(self.dataObj.plate_width)) + "X" + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plate_pt, theta, "SE", offset, text_up, text_down, element="")

        # Column Designation
        pt = self.D + (self.dataObj.col_B / 3) * np.array([1, 0])
        theta = 90
        offset = 60
        text_up = ""
        text_down = "Column " + self.dataObj.col_Designation
        self.dataObj.draw_oriented_arrow(dwg, pt, theta, "SW", offset, text_up, text_down, element="")

        # Bolt Information
        bolt_pt_x = np.array(pt_list[0])
        theta = 45
        offset = (self.dataObj.D_beam * 3 + 400) / 8
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down, element="")

        # Beam Information
        beam_pt = self.ptB1 + (self.dataObj.beam_L) * np.array([1, 0]) + self.dataObj.D_beam / 2 * np.array([0, -1])
        theta = 1
        offset = 0.0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.W + (self.dataObj.weld_thick / 2) * np.array([1, 0])
        theta = 45
        offset = self.dataObj.col_B - 50
        text_up = "          z " + str(self.dataObj.weld_thick)
        text_down = ""

        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NW", offset, text_up, text_down, element="weld")

        # 2D view name
        ptx = self.D + 100 * np.array([1, 0]) + (self.dataObj.col_B/2) * np.array([0, 1])
        dwg.add(dwg.text("Front view (Sec C-C)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = self.D + 100 * np.array([1, 0]) + (self.dataObj.col_B/2+40) * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"########### Column Web Beam Web Saved ############"


class End2DCreatorTop(object):
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
        self.A7 = self.A + (self.dataObj.col_B / 2 + self.dataObj.col_tw / 2 + self.dataObj.plate_thick) * np.array([1, 0]) + (self.dataObj.D_col / 2 -
                                                                                                                               self.dataObj.beam_tw /
                                                                                                                               2) * np.array([0, 1])

        self.A1 = self.A7 - (self.dataObj.beam_B / 2 - self.dataObj.beam_tw / 2) * np.array([0, 1])
        self.A4 = self.A1 + self.dataObj.beam_B * np.array([0, 1])
        self.A2 = self.A1 + self.dataObj.beam_L * np.array([1, 0])
        self.A3 = self.A2 + self.dataObj.beam_B * np.array([0, 1])
        self.A5 = self.A7 - self.dataObj.plate_thick * np.array([1, 0])
        self.A8 = self.A7 + (self.dataObj.beam_L) * np.array([1, 0])
        self.P1 = self.A7 + (self.dataObj.beam_tw) * np.array([0, 1])
        self.W = self.A7 + (self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2) * np.array([0, -1])
        self.P = self.W - self.dataObj.plate_thick * np.array([1, 0])
        self.X = self.P + (self.dataObj.plate_width) * np.array([0, 1])
        self.A6 = self.P1 + (self.dataObj.beam_L) * np.array([1, 0])
        #         self.P2 = self.P + (self.dataObj.plate_thick) * np.array([1,0])
        #         self.P4 = self.P1 + (self.dataObj.plate_thick)* np.array([0,1])
        #         self.P3 = self.P2 + (self.dataObj.plate_thick)* np.array([0,1])
        #         self.P5 = self.A7 - self.dataObj.plate_thick * np.array([1,0])

        # Weld Triangle
        self.ptP = self.A7 + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.ptO = self.ptP + self.dataObj.weld_thick * np.array([1, 0])
        #         self.ptO = self.O  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.ptR = self.ptP + self.dataObj.weld_thick * np.array([0, -1])
        #         self.ptR = self.R + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])

        self.ptX = self.P1 + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.ptY = self.ptX + (self.dataObj.weld_thick) * np.array([0, 1])
        #         self.ptY = self.Y + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1])
        self.ptZ = self.ptX + (self.dataObj.weld_thick) * np.array([1, 0])
        #         self.ptZ = self.Z + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1])


        # ########################### CFBW connectivity points #######################################################################
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.dataObj.col_T * np.array([1, 0])
        self.FC = self.FB + (self.dataObj.col_B - self.dataObj.col_tw) / 2 * np.array([0, 1])
        self.FD = self.FC + (self.dataObj.D_col - 2 * (self.dataObj.col_T)) * np.array([1, 0])
        self.FE = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.FF = self.FA + self.dataObj.D_col * np.array([1, 0])
        self.FG = self.FF + self.dataObj.col_B * np.array([0, 1])
        self.FH = self.FG + self.dataObj.col_T * np.array([-1, 0])
        self.FI = self.FD + self.dataObj.col_tw * np.array([0, 1])
        self.FJ = self.FC + self.dataObj.col_tw * np.array([0, 1])
        self.FK = self.FB + self.dataObj.col_B * np.array([0, 1])
        self.FL = self.FK + self.dataObj.col_T * np.array([-1, 0])
        self.FA7 = self.FD + (self.dataObj.col_T + self.dataObj.plate_thick) * np.array([1, 0])
        self.FP1 = self.FA7 + (self.dataObj.beam_tw) * np.array([0, 1])
        self.FP6 = self.FA7 - (self.dataObj.plate_width - self.dataObj.beam_tw) / 2 * np.array([0, 1])
        self.FP = self.FP6 + self.dataObj.plate_thick * np.array([-1, 0])
        self.FA1 = self.FA7 + (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([0, -1])
        self.FA2 = self.FA1 + self.dataObj.beam_L * np.array([1, 0])
        self.FA3 = self.FA2 + self.dataObj.beam_B * np.array([0, 1])
        self.FA4 = self.FA1 + self.dataObj.beam_B * np.array([0, 1])
        self.FP2 = self.FP + self.dataObj.plate_width * np.array([0, 1])
        self.FP3 = self.FP2 + self.dataObj.plate_thick * np.array([1, 0])
        self.FA8 = self.FA7 + self.dataObj.beam_L * np.array([1, 0])
        self.FA6 = self.FP1 + self.dataObj.beam_L * np.array([1, 0])
        self.FP5 = self.FA7 + self.dataObj.plate_thick * np.array([-1, 0])
        # Weld Triangle

        self.ptFPW = self.FA7 + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.ptFQ = self.ptFPW + self.dataObj.weld_thick * np.array([1, 0])
        #         self.ptFQ = self.FQ  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.ptFR = self.ptFPW + self.dataObj.weld_thick * np.array([0, -1])
        #         self.ptFR = self.FR + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])

        self.ptFX = self.FP1 + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.ptFY = self.ptFX + (self.dataObj.weld_thick) * np.array([0, 1])
        #         self.ptFY = self.FY + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1])
        self.ptFZ = self.ptFX + (self.dataObj.weld_thick) * np.array([1, 0])
        #         self.ptFZ = self.FZ + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1])


        # ###################################### Beam- Beam ############################################################

        # Points for Beam - Beam connection
        self.beam_beam_length = self.dataObj.beam_B + 200
        # for primary beam
        #self.notch_length = (self.dataObj.col_B - self.dataObj.col_tw) / 2 + 10 - self.dataObj.plate_thick

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
        self.BA1 = self.BA3 - self.dataObj.notch_width * np.array([1, 0])
        self.BA4 = self.BA3 + (self.dataObj.beam_L - self.dataObj.notch_width) * np.array([1, 0])
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

        # Weld Triangle

        self.ptBW = self.BA9 + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.ptBX = self.ptBW + self.dataObj.weld_thick * np.array([1, 0])
        #         self.ptFQ = self.FQ  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.ptBY = self.ptBW + self.dataObj.weld_thick * np.array([0, -1])
        #         self.ptFR = self.FR + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])

        self.ptBW1 = self.BA16 + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.ptBX1 = self.ptBW1 + (self.dataObj.weld_thick) * np.array([0, 1])
        #         self.ptFY = self.FY + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1])
        self.ptBY1 = self.ptBW1 + (self.dataObj.weld_thick) * np.array([1, 0])
        #         self.ptFZ = self.FZ + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1])


        # ################################# for end plate #####################################################################
        self.BP1 = self.BG + (self.beam_beam_length - self.dataObj.plate_width) / 2 * np.array([0, 1])
        self.BP4 = self.BP1 + (self.dataObj.plate_width) * np.array([0, 1])

    def call_BWBW_top(self, filename):

        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-350 -350 1300 1300'))

        ############################################# B-B section #######################################################
        ptSecA = self.BB + ((50 + self.dataObj.plate_thick + self.dataObj.beam_L + 150) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txt_pt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.BC + ((50 + self.dataObj.plate_thick + self.dataObj.beam_L + 150) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ############ C-C section #################
        ptSecA = self.BD + 200 * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.beam_beam_length) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BC), (self.BD), (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BE), (self.BF)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BG), (self.BH)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        #         dwg.add(dwg.line((self.BA2),(self.BA1),(self.BA8),(self.BA7)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))

        #         dwg.add(dwg.line((self.BA2),(self.BA1),(self.BA8),(self.BA7)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))

        dwg.add(dwg.polyline(points=[(self.BA2), (self.BA1), (self.BA8), (self.BA7)], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.BA2), (self.BA3), (self.BA4), (self.BA5), (self.BA6), (self.BA7)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BA3), (self.BA6)).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.line((self.BA9), (self.BA10)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BA16), (self.BA15)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.line((self.BA10), (self.BA11)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BA15), (self.BA14)).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.line((self.BA11), (self.BA12)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BA14), (self.BA13)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline([(self.ptBW), (self.ptBX), (self.ptBY), (self.ptBW)], fill='black', stroke_width=2.5, stroke='black'))
        dwg.add(dwg.polyline([(self.ptBW1), (self.ptBX1), (self.ptBY1), (self.ptBW1)], fill='black', stroke_width=2.5, stroke='black'))

        # end plate
        dwg.add(dwg.rect(insert=(self.BP1), size=(self.dataObj.plate_thick, self.dataObj.plate_width), fill='none', stroke='red',
                         stroke_width=2.5).dasharray(dasharray=([5, 5])))

        #         dwg.add(dwg.line((self.BH1),(self.BG1)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        #         dwg.add(dwg.line((self.BE1),(self.BF1)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        #         dwg.add(dwg.polyline(points=[(self.BJ1),(self.BI1),(self.BL1),(self.BK1),(self.BA)], stroke='red', fill='none',
        #                                                                                         stroke_width=2.5).dasharray(dasharray = ([5,5])))
        #         dwg.add(dwg.line((self.BP4),(self.BP5)).stroke('blue',width = 2.5,linecap = 'square'))
        #         dwg.add(dwg.line((self.BP9),(self.BG1)).stroke('blue',width = 2.5,linecap = 'square'))
        #         dwg.add(dwg.line((self.BQ9),(self.BE1)).stroke('blue',width = 2.5,linecap = 'square'))
        #         dwg.add(dwg.line((self.BQ4),(self.BQ5)).stroke('blue',width = 2.5,linecap = 'square'))
        #         dwg.add(dwg.polyline(points=[(self.BP9),(self.BP10),(self.BP1),(self.BP2),(self.BP3),(self.BP4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        #         dwg.add(dwg.polyline(points=[(self.BQ9),(self.BQ10),(self.BQ1),(self.BQ2),(self.BQ3),(self.BQ4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        #         dwg.add(dwg.line((self.BP10 + self.dataObj.gap * np.array([1,0])),(self.BQ10 + self.dataObj.gap * np.array([1,0]))).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))

        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list1 = []

        if nc >= 1:
            for col in range(nc):
                pt = self.BP1 - self.dataObj.col_tw * np.array([1, 0]) + self.dataObj.edge_dist * np.array([0, 1]) + (col) * self.dataObj.gauge * np.array(
                    [0, 1])
                pt1 = pt - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([-1, 0])
                B2 = pt + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_ref = self.BP4 - self.dataObj.col_tw * np.array([1, 0]) - self.dataObj.edge_dist * np.array([0, 1]) - (col) * self.dataObj.gauge * np.array(
                    [0, 1])
                pt_ref1 = pt_ref - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt_ref1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1_ref = pt_ref + 10 * np.array([-1, 0])
                B2_ref = pt_ref + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_ref), (B2_ref)).stroke('black', width=2.5, linecap='square'))

                pt_list.append(pt)
                pt_list1.append(pt_ref)
                bltdimoffset = self.dataObj.col_B / 2 + 50

                if len(pt_list) > 1:
                    ptblt2 = np.array(pt_list[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])

                    ptblt2_ref = np.array(pt_list[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
                    params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                    params_ref = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list1[0]), np.array(pt_list1[1]), str(int(self.dataObj.gauge)), params_ref)
                    self.dataObj.draw_faint_line(np.array(pt_list[-1]), ptblt2, dwg)
                    self.dataObj.draw_faint_line(np.array(pt_list1[-1]), ptblt2_ref, dwg)

                    # Draw Faint line to represent edge distance
                #         ptB = self.FP + (self.dataObj.col_T) * np.array([-1,0])
                #         ptC = ptB + (bltdimoffset) * np.array([-1,0])
                # #         self.dataObj.draw_faint_line(ptB,ptC,dwg)
                #         ptL = np.array(pt_list[-1])

        # Faint Lines for bolts
        ptblt1 = np.array(pt_list[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        ptblt1_ref = np.array(pt_list1[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), ptblt1, dwg)
        self.dataObj.draw_faint_line(np.array(pt_list1[0]), ptblt1_ref, dwg)

        # Edge Distance
        ptB = self.BP1 - self.dataObj.col_tw * np.array([1, 0])
        pt2 = ptB - bltdimoffset * np.array([1, 0])
        self.dataObj.draw_faint_line(ptB, pt2, dwg)

        ptBD = self.BP4
        pt2 = ptBD - (bltdimoffset + self.dataObj.col_tw) * np.array([1, 0])
        self.dataObj.draw_faint_line(ptBD, pt2, dwg)

        ptB = self.BP1 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptB, np.array(pt_list[0]), str(int(self.dataObj.edge_dist)), params)
        ptB = self.BP4 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptB, np.array(pt_list1[0]), str(int(self.dataObj.edge_dist)), params)

        # Beam Information
        beam_pt = (self.BA4 + self.BA5) / 2
        theta = 1
        offset = 0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # Column Information
        col_pt = (self.BA + self.BB) / 2 + 20 * np.array([1, 0])
        theta = 90
        offset = 100
        text_up = "Beam " + self.dataObj.col_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "NW", offset, text_up, text_down, element="")

        # Plate  Information
        plt_pt = self.BP4 + self.dataObj.plate_thick / 2 * np.array([1, 0])
        theta = 60
        offset = self.dataObj.beam_B / 2 + 60
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, text_up, text_down, element="")

        # Bolt Information
        bltPt = np.array(pt_list[0])
        theta = 75
        offset = (self.beam_beam_length / 2) + 25
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bltPt, theta, "NE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.BA9
        theta = 40
        offset = self.dataObj.beam_B / 2 + 50
        text_up = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down, element="weld")
        #         weldarrow = weld_pt + offset*np.array([0,-1]) + 18*np.array([-1,0])
        #         self.dataObj.draw_weld_arrow(weldarrow , dwg)

        # 2D view name
        ptx = self.BC + 250 * np.array([0, 1])
        dwg.add(dwg.text("Top view (Sec A-A)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = self.BC + 290 * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()
        print "######### Beam Beam Top Saved ############"

    def call_CFBW_top(self, filename):
        v_width = self.dataObj.D_col + 1000
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-330 -350 1400 1400'))

        ############ B-B section #################
        ptSecA = self.FF + ((290 + self.dataObj.plate_thick + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txt_pt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.FG + ((290 + self.dataObj.plate_thick + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ############ C-C section #################
        ptSecA = self.FL + ((self.dataObj.D_beam * 3) / 8 + 100) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.plate_thick + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.FA), (self.FB), (self.FC), (self.FD), (self.FE), (self.FF), (self.FG), (self.FH), (self.FI), (self.FJ), (self.FK),
                                     (self.FL), (self.FA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FA1), size=(self.dataObj.beam_L, self.dataObj.beam_B), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.plate_thick, self.dataObj.plate_width), fill='none', stroke='blue', stroke_width=2.5))

        #         dwg.add(dwg.line((self.FP),(self.FP6)).stroke('blue',width = 2.5,linecap = 'square'))
        #         dwg.add(dwg.line((self.FX),(self.FP4)).stroke('blue',width = 2.5,linecap = 'square'))
        #         dwg.add(dwg.polyline(points=[(self.FP1),(self.FP2),(self.FP3),(self.FP4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FA7), (self.FA8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.FP1), (self.FA6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline([(self.ptFPW), (self.ptFQ), (self.ptFR), (self.ptFPW)], fill='black', stroke_width=2.5, stroke='black'))
        dwg.add(dwg.polyline([(self.ptFX), (self.ptFY), (self.ptFZ), (self.ptFX)], fill='black', stroke_width=2.5, stroke='black'))

        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list1 = []

        if nc >= 1:
            for col in range(nc):
                pt = self.FP + (self.dataObj.edge_dist) * np.array([0, 1]) - self.dataObj.col_T * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array(
                    [0, 1])
                pt1 = pt - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_T + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([-1, 0])
                B2 = pt + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_ref = self.FP2 + (self.dataObj.edge_dist) * np.array([0, -1]) - self.dataObj.col_T * np.array([1, 0]) + (
                                                                                                                           col) * self.dataObj.gauge * np.array(
                    [0, -1])
                pt_ref1 = pt_ref - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_T + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt_ref1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1_ref = pt_ref + 10 * np.array([-1, 0])
                B2_ref = pt_ref + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_ref), (B2_ref)).stroke('black', width=2.5, linecap='square'))

                pt_list.append(pt)
                pt_list1.append(pt_ref)
                bltdimoffset = self.dataObj.D_col + 2 * self.dataObj.col_T + 50

                if len(pt_list) > 1:
                    ptblt2 = np.array(pt_list[-1]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])

                    ptblt2_ref = np.array(pt_list1[-1]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])
                    params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                    params_ref = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list1[0]), np.array(pt_list1[1]), str(int(self.dataObj.gauge)), params_ref)
                    self.dataObj.draw_faint_line(np.array(pt_list[-1]), ptblt2, dwg)
                    self.dataObj.draw_faint_line(np.array(pt_list1[-1]), ptblt2_ref, dwg)

        # Draw Faint line to represent edge distance
        ptB = self.FP + (self.dataObj.col_T) * np.array([-1, 0])
        ptC = ptB + (bltdimoffset) * np.array([-1, 0])
        self.dataObj.draw_faint_line(ptB, ptC, dwg)
        ptB1 = self.FP2 + (self.dataObj.col_T) * np.array([-1, 0])
        ptC1 = ptB1 + (bltdimoffset) * np.array([-1, 0])
        self.dataObj.draw_faint_line(ptB1, ptC1, dwg)

        # Faint Lines for bolts
        ptblt1 = np.array(pt_list[0]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])
        ptblt1_ref = np.array(pt_list1[0]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), ptblt1, dwg)
        self.dataObj.draw_faint_line(np.array(pt_list1[0]), ptblt1_ref, dwg)

        # Edge Distance
        ptL = np.array(pt_list[0])

        ptL1 = np.array(pt_list1[0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptB, ptL, str(int(self.dataObj.edge_dist)), params)
        self.dataObj.draw_dimension_outer_arrow(dwg, ptL1, ptB1, str(int(self.dataObj.edge_dist)), params)

        # Beam Information
        beam_pt = self.FA2 + (self.dataObj.beam_L/2) * np.array([-1, 0])
        theta = 90
        offset = 30
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down, element="")

        # Column Information
        col_pt = self.FL
        theta = 45
        offset = (self.dataObj.D_beam * 3) / 10
        text_up = ""
        text_down = "Column " + self.dataObj.col_Designation
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, text_up, text_down, element="")

        # Plate  Information
        plt_pt = self.FP + self.dataObj.plate_width * np.array([0, 1]) + self.dataObj.plate_thick / 2 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.beam_B / 2 + 50
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, text_up, text_down, element="")

        # Bolt Information
        bltPt = self.FP5 + (50 - self.dataObj.beam_tw / 2) * np.array([0, -1]) - self.dataObj.col_T * np.array([1, 0])
        theta = 85
        offset = (self.dataObj.beam_B) + 100
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bltPt, theta, "NW", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.FA7
        theta = 60
        offset = self.dataObj.weld_thick + self.dataObj.plate_thick + self.dataObj.beam_B / 2 + 100
        text_up = "          z " + str(int(self.dataObj.weld_thick))
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down, element="weld")
        #         weldarrow = weld_pt + offset*np.array([0,-1]) + 18*np.array([-1,0])
        #         self.dataObj.draw_weld_arrow(weldarrow , dwg)

        # 2D view name
        ptx = self.FG + ((self.dataObj.D_beam * 3) / 8 + 200) * np.array([0, 1]) + 120 * np.array([-1,0])
        dwg.add(dwg.text("Top view (Sec A-A)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = self.FG + ((self.dataObj.D_beam * 3) / 8 + 240) * np.array([0, 1]) + 120 * np.array([-1,0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()
        print"$$$$$$$$$ Saved Column Flange Beam Web Top $$$$$$$$$$$$"

    def call_CWBW_top(self, filename):
        v_length = self.dataObj.col_B + 850
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-230 -300 1400 1300' ))

        ############ B-B section #################
        ptSecA = self.B + ((130 + self.dataObj.plate_thick + self.dataObj.beam_L + 100) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txt_pt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.G + ((130 + self.dataObj.plate_thick + self.dataObj.beam_L + 100) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ############ C-C section #################
        # ptx = self.A + 200 * np.array([1, 0]) + (v_length - 370) * np.array([0, 1])

        ptSecA = self.H + 50 * np.array([-1, 0]) + (v_length-800) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col  + self.dataObj.beam_L ) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(
            points=[(self.A), (self.B), (self.C), (self.D), (self.E), (self.F), (self.G), (self.H), (self.I), (self.J), (self.K), (self.L), (self.A)],
            stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A1), size=(self.dataObj.beam_L, self.dataObj.beam_B), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.A7), (self.A8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.P1), (self.A6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.plate_thick, self.dataObj.plate_width), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline([(self.ptP), (self.ptO), (self.ptR), (self.ptP)], fill='black', stroke_width=2.5, stroke='black'))
        dwg.add(dwg.polyline([(self.ptX), (self.ptY), (self.ptZ), (self.ptX)], fill='black', stroke_width=2.5, stroke='black'))

        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pt_list = []
        pt_list1 = []

        if nc >= 1:
            for col in range(nc):
                pt = self.P + (self.dataObj.edge_dist) * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array(
                    [0, 1])
                pt1 = pt - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([-1, 0])
                B2 = pt + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_ref = self.X + (self.dataObj.edge_dist) * np.array([0, -1]) - self.dataObj.col_tw * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array(
                    [0, -1])
                pt_ref1 = pt_ref - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt_ref1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1_ref = pt_ref + 10 * np.array([-1, 0])
                B2_ref = pt_ref + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_ref), (B2_ref)).stroke('black', width=2.5, linecap='square'))

                pt_list.append(pt)
                pt_list1.append(pt_ref)
                bltdimoffset = self.dataObj.D_col / 2 + 50

                if len(pt_list) > 1:
                    ptblt2 = np.array(pt_list[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])

                    ptblt2_ref = np.array(pt_list1[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
                    params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                    params_ref = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list1[0]), np.array(pt_list1[1]), str(int(self.dataObj.gauge)), params_ref)
                    self.dataObj.draw_faint_line(np.array(pt_list[-1]), ptblt2, dwg)
                    self.dataObj.draw_faint_line(np.array(pt_list1[-1]), ptblt2_ref, dwg)

        # Draw Faint line to represent edge distance
        ptB = self.P + self.dataObj.col_tw * np.array([-1, 0])
        ptC = ptB + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.draw_faint_line(ptB, ptC, dwg)
        ptB1 = self.X + self.dataObj.col_tw * np.array([-1, 0])
        ptC1 = ptB1 + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.draw_faint_line(ptB1, ptC1, dwg)

        # Faint Lines for bolts
        ptblt1 = np.array(pt_list[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        ptblt1_ref = np.array(pt_list1[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.draw_faint_line(np.array(pt_list[0]), ptblt1, dwg)
        self.dataObj.draw_faint_line(np.array(pt_list1[0]), ptblt1_ref, dwg)

        # Edge Distance
        ptL = np.array(pt_list[0])
        ptL1 = np.array(pt_list1[0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptB, ptL, str(int(self.dataObj.edge_dist)), params)
        self.dataObj.draw_dimension_outer_arrow(dwg, ptL1, ptB1, str(int(self.dataObj.edge_dist)), params)

        # Beam Information
        beam_pt = self.A6
        theta = 1
        offset = 0
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down, element="")

        # column  Information
        col_pt = self.H + 20 * np.array([1, 0])
        theta = 60
        offset = 110
        text_up = ""
        text_down =  "Column " + self.dataObj.col_Designation
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, text_up, text_down, element="")

        # Plate  Information
        plt_pt = self.X + self.dataObj.plate_thick / 2 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.beam_B / 2 + 70
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, text_up, text_down, element="")

        # Bolt Information
        # bltPt = self.A5 + self.dataObj.edge_dist * np.array([1,0]) + (nc -1) * self.dataObj.gauge * np.array([1,0])
        bltPt = np.array(pt_list[0])
        theta = 60
        offset = (self.dataObj.beam_B) +100
        text_up = str(self.dataObj.no_of_rows) + " rows " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bltPt, theta, "NE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.ptR
        theta = 30
        offset = self.dataObj.D_col * 2 / 4.2
        text_up = "" # u"\u25C1"
        text_down = "          z " + str(int(self.dataObj.weld_thick))
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down, element="weld")

        # 2D view name
        ptx = self.A + 200 * np.array([1, 0]) + (v_length - 370) * np.array([0, 1])
        dwg.add(dwg.text("Top view (Sec A-A)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty =self.A + 200 * np.array([1, 0]) + (v_length - 340) * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"$$$$$$$$$ Saved Column Web Beam Web Top $$$$$$$$$$$"


class End2DCreatorSide(object):
    def __init__(self, fin_common_obj):

        self.dataObj = fin_common_obj

        # CWBW connectivity points
        self.A = np.array([0, 0])
        self.B = self.A + self.dataObj.col_T * np.array([1, 0])
        self.C = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.D = self.A + self.dataObj.D_col * np.array([1, 0])
        self.H = self.C + self.dataObj.col_L * np.array([0, 1])
        self.G = self.B + self.dataObj.col_L * np.array([0, 1])
        self.A1 = self.A + (self.dataObj.D_col / 2 - self.dataObj.beam_B / 2) * np.array((1, 0)) + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array(
            [0, 1])
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
        self.P = self.A11 + (self.dataObj.beam_R1 + 5) * np.array([0, 1]) + self.dataObj.beam_tw / 2 * np.array([1, 0])
        self.Q = self.P + self.dataObj.plate_width / 2 * np.array([-1, 0])
        self.X = self.P + (self.dataObj.weld_thick + self.dataObj.beam_tw / 2 + 2.5) * np.array([-1, 0])
        self.R = self.P + self.dataObj.plate_ht * np.array([0, 1])
        self.Q1 = self.P + self.dataObj.plate_width / 2 * np.array([1, 0])
        self.X1 = self.P + (self.dataObj.beam_tw / 2 + 2.5) * np.array([1, 0])

        # ### CFBW connectivity
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.dataObj.col_B * np.array([1, 0])
        self.ptMid = self.FA + ((self.dataObj.col_B / 2) + (self.dataObj.col_tw / 2)) * np.array([1, 0])
        self.ptMid1 = self.ptMid + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array([0, 1])
        self.FC = self.FB + self.dataObj.col_L * np.array([0, 1])
        self.FD = self.FA + self.dataObj.col_L * np.array([0, 1])
        self.FA1 = self.FA + (self.dataObj.col_B / 2 - self.dataObj.beam_B / 2) * np.array((1, 0)) + (
                                                                                                     (self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array(
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
        #         self.FP = self.FA11 + (self.dataObj.beam_R1 + 3) * np.array([0,1])
        #         self.FQ = self.FP + self.dataObj.plate_thick * np.array([-1,0])
        #         self.FX = self.FQ + self.dataObj.weld_thick * np.array([-1,0])
        #         self.FR = self.FP + self.dataObj.plate_ht * np.array([0,1])
        #         self.FY = self.FX + self.dataObj.plate_ht * np.array([0,1])
        self.FP = self.FA11 + (self.dataObj.beam_R1 + self.dataObj.beam_T + 3) * np.array([0, 1]) + self.dataObj.beam_tw / 2 * np.array([1, 0])
        self.FQ = self.FP + self.dataObj.plate_width / 2 * np.array([-1, 0])
        self.FX = self.FP + (self.dataObj.weld_thick + self.dataObj.beam_tw / 2 + 2.5) * np.array([-1, 0])
        self.FR = self.FP + self.dataObj.plate_ht * np.array([0, 1])
        self.FQ1 = self.FP + self.dataObj.plate_width / 2 * np.array([1, 0])
        self.FX1 = self.FP + (self.dataObj.beam_tw / 2 + 2.5) * np.array([1, 0])

        # #### Points for Beam-Beam connection #####

        self.beam_beam_length = self.dataObj.beam_B + 200  # #beam_B

        # for primary beam
        self.BA = (0, 0)
        self.BB = self.BA + (self.beam_beam_length) * np.array([1, 0])
        self.BC = self.BB + (self.dataObj.col_T) * np.array([0, 1])
        self.BD = self.BC - (self.beam_beam_length - self.dataObj.beam_tw) / 2 * np.array([1, 0])
        self.BE = self.BD - self.dataObj.beam_tw * np.array([1, 0])
        self.BF = self.BA + self.dataObj.col_T * np.array([0, 1])
        self.BG = self.BA + (self.dataObj.D_col - self.dataObj.col_T) * np.array([0, 1])
        self.BH = self.BG + self.beam_beam_length * np.array([1, 0])
        self.BI = self.BH + self.dataObj.col_T * np.array([0, 1])
        self.BJ = self.BG + self.dataObj.col_T * np.array([0, 1])

        # for secondary beam ### changes after importing beam

        self.BA1 = self.BA + (self.beam_beam_length - self.dataObj.beam_B) / 2 * np.array([1, 0])
        self.BB1 = self.BA1 + (self.dataObj.beam_B) * np.array([1, 0])
        self.BC1 = self.BB1 + (self.dataObj.beam_T) * np.array([0, 1])
        self.BD1 = self.BC1 - (self.dataObj.beam_B - self.dataObj.beam_tw) / 2 * np.array([1, 0])
        self.BE1 = self.BD1 + (self.dataObj.D_beam - 2 * self.dataObj.beam_T) * np.array([0, 1])
        self.BF1 = self.BC1 + (self.dataObj.D_beam - 2 * self.dataObj.beam_T) * np.array([0, 1])
        self.BG1 = self.BF1 + (self.dataObj.beam_T) * np.array([0, 1])
        self.BL1 = self.BA1 + (self.dataObj.beam_T) * np.array([0, 1])
        self.BH1 = self.BL1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0, 1])
        self.BI1 = self.BL1 + (self.dataObj.D_beam - 2 * self.dataObj.beam_T) * np.array([0, 1])
        self.BJ1 = self.BE1 - self.dataObj.beam_tw * np.array([1, 0])
        self.BK1 = self.BD1 - self.dataObj.beam_tw * np.array([1, 0])

        # for end plate
        self.BP = self.BD + (self.dataObj.notch_offset - self.dataObj.col_T) * np.array([0, 1])
        self.BQ = self.BP + self.dataObj.weld_thick * np.array([1, 0])
        self.BR = self.BP + (self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2) * np.array([1, 0])
        self.BP1 = self.BP + self.dataObj.plate_ht * np.array([0, 1])
        self.BQ1 = self.BQ + self.dataObj.plate_ht * np.array([0, 1])
        self.BR1 = self.BR + self.dataObj.plate_ht * np.array([0, 1])
        self.BX = self.BP - self.dataObj.beam_tw * np.array([1, 0])
        self.BY = self.BX - self.dataObj.weld_thick * np.array([1, 0])
        self.BZ = self.BX - (self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2) * np.array([1, 0])
        self.BX1 = self.BX + self.dataObj.plate_ht * np.array([0, 1])
        self.BY1 = self.BY + self.dataObj.plate_ht * np.array([0, 1])
        self.BZ1 = self.BZ + self.dataObj.plate_ht * np.array([0, 1])
        self.BV = self.BP + self.dataObj.beam_tw * np.array([-1,0])

    def call_BWBW_side(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-450 -350 1300 1300'))
        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BI), (self.BJ), (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BG), (self.BH)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BF), (self.BE)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BD), (self.BC)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BE), (self.BD)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BP), (self.BX)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BP1), (self.BX1)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.BB1), (self.BC1), (self.BD1), (self.BE1), (self.BF1), (self.BG1), (self.BH1), (self.BI1), (self.BJ1), (self.BK1),
                                     (self.BL1), (self.BA1)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))

        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BY), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2, self.dataObj.plate_ht), fill='none', stroke='blue',
                         stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.BZ), size=((self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2), self.dataObj.plate_ht), fill='none', stroke='blue',
                         stroke_width=2.5))
        dwg.add(dwg.line((self.BP), (self.BV)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([2, 3])))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pitch_pts = []
        pitch_pts1 = []
        for row in range(nr):
            col_list = []
            col_list1 = []
            for col in range(nc):
                pt = self.BZ + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array(
                    [0, 1]) + (col) * self.dataObj.gauge * np.array([1, 0])
                pt_other = self.BR - self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (
                                                                                                                              row) * self.dataObj.pitch * np.array(
                    [0, 1]) - (col) * self.dataObj.gauge * np.array([1, 0])

                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                dwg.add(dwg.circle(center=(pt_other), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))

                blt1 = pt + (bolt_r + 5) * np.array([1, 0])
                blt2 = pt + (bolt_r + 5) * np.array([-1, 0])
                blt3 = pt + (bolt_r + 5) * np.array([0, 1])
                blt4 = pt + (bolt_r + 5) * np.array([0, -1])

                point1 = pt +self.dataObj.edge_dist * np.array([1,0])

                dwg.add(dwg.line((blt1), (blt2)).stroke('red', width=1.5, linecap='square'))
                dwg.add(dwg.line((blt3), (blt4)).stroke('blue', width=1.5, linecap='square').dasharray(dasharray=([20, 5, 1, 5])))

                blt1_o = pt_other + (bolt_r + 5) * np.array([1, 0])
                blt2_o = pt_other + (bolt_r + 5) * np.array([-1, 0])
                blt3_o = pt_other + (bolt_r + 5) * np.array([0, 1])
                blt4_o = pt_other + (bolt_r + 5) * np.array([0, -1])

                dwg.add(dwg.line((blt1_o), (blt2_o)).stroke('red', width=1.5, linecap='square'))
                dwg.add(dwg.line((blt3_o), (blt4_o)).stroke('blue', width=1.5, linecap='square').dasharray(dasharray=([20, 5, 1, 5])))
                col_list.append(pt_other)
                col_list1.append(pt)
            pitch_pts.append(col_list)
            pitch_pts1.append(col_list1)

        if nc > 1:
            gaugept1_other = np.array(pitch_pts[-1][0])
            gaugept2_other = np.array(pitch_pts[-1][1])
            params = {"offset": self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50,
                      "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, gaugept1_other, gaugept2_other, str(int(self.dataObj.gauge)), params)

            faintpt1_other = gaugept1_other
            faintpt1_other1 = gaugept1_other + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht +
                                                self.dataObj.edge_dist + 50) * np.array([0, 1])
            faintpt2_other = gaugept2_other
            faintpt2_other1 = gaugept2_other + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht +
                                                self.dataObj.edge_dist + 50) * np.array([0, 1])
            self.dataObj.draw_faint_line(faintpt1_other, faintpt1_other1, dwg)
            self.dataObj.draw_faint_line(faintpt2_other, faintpt2_other1, dwg)

            gaugept1 = np.array(pitch_pts1[-1][0])
            gaugept2 = np.array(pitch_pts1[-1][1])
            params = {"offset": self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50, "textoffset": 50,
                      "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, gaugept2, gaugept1, str(int(self.dataObj.gauge)), params)
            faintpt1 = gaugept1
            faintpt1_1 = gaugept1 + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50) * np.array([0, 1])
            faintpt2 = gaugept2 + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50) * np.array([0, 1])
            faintpt2_1 = gaugept2
            self.dataObj.draw_faint_line(faintpt1, faintpt1_1, dwg)
            self.dataObj.draw_faint_line(faintpt2, faintpt2_1, dwg)

        pt_list = []
        for row in pitch_pts:
            if len(row) > 0:
                pt_list.append(row[0])

        # End and Pitch Distance Information
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[-1]),
                                                str(len(pt_list) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) +
                                                "c/c", params)
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.BR - self.dataObj.edge_dist * np.array([1, 0]),
                                                np.array(pt_list[0]), str(int(self.dataObj.end_dist)), params)
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[-1]), self.BR - self.dataObj.edge_dist * np.array([1, 0]) +
                                                self.dataObj.plate_ht * np.array([0, 1]), str(int(self.dataObj.end_dist)), params)

        # notch dist
        ptN1 = self.BR - self.dataObj.edge_dist * np.array([1, 0])
        ptN2 = ptN1 - self.dataObj.notch_offset * np.array([0, 1])
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptN2, ptN1, str(int(self.dataObj.notch_offset)), params)

        pt9 = self.BB
        pt10 = pt9 + (self.beam_beam_length / 2 - 20) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt9, pt10, dwg)

        # Draw Faint Line
        pt1 = self.BR
        pt2 = pt1 + (self.beam_beam_length / 2) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt1, pt2, dwg)

        pt3 = np.array(pt_list[0])
        pt4 = pt3 + (self.beam_beam_length / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt3, pt4, dwg)

        pt5 = np.array(pt_list[-1])
        pt6 = pt5 + (self.beam_beam_length / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt5, pt6, dwg)

        pt7 = self.BR + self.dataObj.plate_ht * np.array([0, 1])
        pt8 = pt7 + (self.beam_beam_length / 2) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt7, pt8, dwg)

        # Beam Information
        beam_pt = (self.BG1 + self.BH1) / 2
        theta = 30
        offset = (self.dataObj.col_L/5)
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # column  Information
        col_pt = (self.BA + self.BG) / 3
        theta = 1
        offset = 1
        text_up = "Column " + self.dataObj.col_Designation
        text_down = " "
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "NW", offset, text_up, text_down, element="")

        # Plate  Information
        beam_pt = (self.BX1 + self.BZ1) / 2
        theta = 40
        offset = self.beam_beam_length / 3
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SW", offset, text_up, text_down, element="")

        # Bolt Information
        bolt_pt_x = np.array(pt_list[0])
        theta = 60
        offset = self.dataObj.notch_offset + self.dataObj.end_dist + 70
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.BY + self.dataObj.weld_thick / 2 * np.array([1, 0])
        theta = 90
        offset = self.dataObj.plate_width / 2
        text_up = "          z " + str(int(self.dataObj.weld_thick))
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NW", offset, text_up, text_down, element="weld")

        # 2D view name
        ptx = self.BG + (self.dataObj.beam_B * 1.6) * np.array([0, 1])
        dwg.add(dwg.text("Side view (Sec B-B)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = self.BG + (self.dataObj.beam_B * 1.6 + 40) * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "********* Beam Beam Side Saved ***********"

    def call_CWBW_side(self, filename):
        '''
        :param filename:
        :return:
        '''
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-300 -100 1300 1300'))
        dwg.add(dwg.rect(insert=(self.A), size=(self.dataObj.D_col, self.dataObj.col_L), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.C), (self.H)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.B), (self.G)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.A1), (self.A2), (self.A3), (self.A4), (self.A5), (self.A6), (self.A7), (self.A8), (self.A9), (self.A10), (self.A11),
                                     (self.A12), (self.A1)], stroke='blue', fill='none', stroke_width=2.5))

        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))
        dwg.add(dwg.rect(insert=(self.X), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.Q), size=(self.dataObj.plate_width, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.X1), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col / 2

        bolt_r = self.dataObj.bolt_dia / 2
        pitch_pts = []
        pitch_pts1 = []
        for row in range(nr):
            col_list = []
            col_list1 = []
            for col in range(nc):
                pt = self.Q + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array(
                    [0, 1]) + (col) * self.dataObj.gauge * np.array([1, 0])
                pt_other = self.Q1 - self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (
                                                                                                                              row) * self.dataObj.pitch * np.array(
                    [0, 1]) - (col) * self.dataObj.gauge * np.array([1, 0])

                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                dwg.add(dwg.circle(center=(pt_other), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))

                blt1 = pt + (bolt_r + 5) * np.array([1, 0])
                blt2 = pt + (bolt_r + 5) * np.array([-1, 0])
                blt3 = pt + (bolt_r + 5) * np.array([0, 1])
                blt4 = pt + (bolt_r + 5) * np.array([0, -1])

                dwg.add(dwg.line((blt1), (blt2)).stroke('black', width=1, linecap='square'))
                dwg.add(dwg.line((blt3), (blt4)).stroke('black', width=1, linecap='square'))

                blt1_o = pt_other + (bolt_r + 5) * np.array([1, 0])
                blt2_o = pt_other + (bolt_r + 5) * np.array([-1, 0])
                blt3_o = pt_other + (bolt_r + 5) * np.array([0, 1])
                blt4_o = pt_other + (bolt_r + 5) * np.array([0, -1])

                dwg.add(dwg.line((blt1_o), (blt2_o)).stroke('black', width=1, linecap='square'))
                dwg.add(dwg.line((blt3_o), (blt4_o)).stroke('black', width=1, linecap='square'))
                col_list.append(pt_other)
                col_list1.append(pt)
            pitch_pts.append(col_list)
            pitch_pts1.append(col_list1)

        if nc > 1:
            gaugept1_other = np.array(pitch_pts[-1][0])
            gaugept2_other = np.array(pitch_pts[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, gaugept1_other, gaugept2_other, str(int(self.dataObj.gauge)), params)

            faintpt1_other = gaugept1_other
            faintpt1_other1 = gaugept1_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_other = gaugept2_other
            faintpt2_other1 = gaugept2_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            self.dataObj.draw_faint_line(faintpt1_other, faintpt1_other1, dwg)
            self.dataObj.draw_faint_line(faintpt2_other, faintpt2_other1, dwg)

            gaugept1 = np.array()
            gaugept1 = np.array(pitch_pts1[-1][0])
            gaugept2 = np.array(pitch_pts1[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, gaugept2, gaugept1, str(int(self.dataObj.gauge)), params)
            faintpt1 = gaugept1
            faintpt1_1 = gaugept1 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2 = gaugept2 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_1 = gaugept2
            self.dataObj.draw_faint_line(faintpt1, faintpt1_1, dwg)
            self.dataObj.draw_faint_line(faintpt2, faintpt2_1, dwg)

        pt_list = []
        for row in pitch_pts:
            if len(row) > 0:
                pt_list.append(row[0])

        # End and Pitch Distance Information
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[-1]),
                                                str(len(pt_list) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) + "c/c", params)

        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, self.Q1 - self.dataObj.edge_dist * np.array([1, 0]),
                                                np.array(pt_list[0]), str(int(self.dataObj.end_dist)),
                                                params)

        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[-1]), self.Q1 - self.dataObj.edge_dist * np.array([1, 0])
                                                + self.dataObj.plate_ht *
                                                np.array([0, 1]), str(int(self.dataObj.end_dist)), params)

        # Draw Faint Line
        pt1 = self.Q1
        pt2 = pt1 + (self.dataObj.D_col / 2) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt1, pt2, dwg)

        pt3 = np.array(pt_list[0])
        pt4 = pt3 + (self.dataObj.D_col / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt3, pt4, dwg)

        pt5 = np.array(pt_list[-1])
        pt6 = pt5 + (self.dataObj.D_col / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt5, pt6, dwg)

        pt7 = self.Q1 + self.dataObj.plate_ht * np.array([0, 1])
        pt8 = pt7 + (self.dataObj.D_col / 2) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt7, pt8, dwg)

        # Beam Information
        beam_pt = (self.A8 + self.A7) / 2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam)/2 + 50
        text_up = ""
        text_down = "Beam " + self.dataObj.beam_Designation
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SW", offset, text_up, text_down, element="")

        # column  Information
        col_pt = self.H
        theta = 45
        offset = 70
        text_up = "Column " + self.dataObj.col_Designation
        text_down = " "
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, text_up, text_down, element="")

        # Plate  Information
        beam_pt = self.Q1 + self.dataObj.plate_ht * np.array([0, 1]) - self.dataObj.plate_width / 4 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.plate_thick + self.dataObj.beam_B / 2 + 80
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # Bolt Information
        bolt_pt_x = np.array(pt_list[0])
        theta = 60
        offset = (self.dataObj.D_col - self.dataObj.plate_width) / 2 + self.dataObj.end_dist + 20
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.X + self.dataObj.weld_thick / 2 * np.array([1, 0])
        theta = 60
        offset = self.dataObj.col_L / 5
        text_up = "          z " + str(int(self.dataObj.weld_thick))
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NW", offset, text_up, text_down, element="weld")

        # 2D view name
        ptx = self.G + 100 * np.array([1, 0]) + 200 * np.array([0, 1])
        dwg.add(dwg.text("Side view (Sec B-B)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty =self.G + 100 * np.array([1, 0]) + 240 * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "********* Column Web Beam Web Side Saved ***********"

    def call_CFBW_side(self, filename):
        dwg = svgwrite.Drawing(filename, size=('100%', '100%'), viewBox=('-200 -200 1400 1400'))
        dwg.add(dwg.rect(insert=(self.FA), size=(self.dataObj.col_B, self.dataObj.col_L), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(
            points=[(self.FA1), (self.FA2), (self.FA3), (self.FA4), (self.FA5), (self.FA6), (self.FA7), (self.FA8), (self.FA9), (self.FA10), (self.FA11),
                    (self.FA12), (self.FA1)], stroke='blue', fill='none', stroke_width=2.5))

        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=0.7))
        dwg.add(dwg.rect(insert=(self.FX), size=(self.dataObj.weld_thick, self.dataObj.weld_len), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FQ), size=(self.dataObj.plate_width, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))

        dwg.add(
            dwg.rect(insert=(self.FX1), size=(self.dataObj.weld_thick, self.dataObj.weld_len), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pitch_pts = []
        pitch_pts1 = []
        for row in range(nr):
            col_list = []
            col_list1 = []
            for col in range(nc):
                pt = (self.FQ + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch *
                      np.array([0, 1]) + (col) * self.dataObj.gauge * np.array([1, 0]))
                pt_other = (self.FQ1 - self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch *
                            np.array([0, 1]) - (col) * self.dataObj.gauge * np.array([1, 0]))

                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                dwg.add(dwg.circle(center=(pt_other), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))

                blt1 = pt + (bolt_r + 5) * np.array([1, 0])
                blt2 = pt + (bolt_r + 5) * np.array([-1, 0])
                blt3 = pt + (bolt_r + 5) * np.array([0, 1])
                blt4 = pt + (bolt_r + 5) * np.array([0, -1])

                dwg.add(dwg.line((blt1), (blt2)).stroke('black', width=1, linecap='square'))
                dwg.add(dwg.line((blt3), (blt4)).stroke('black', width=1, linecap='square'))

                blt1_o = pt_other + (bolt_r + 5) * np.array([1, 0])
                blt2_o = pt_other + (bolt_r + 5) * np.array([-1, 0])
                blt3_o = pt_other + (bolt_r + 5) * np.array([0, 1])
                blt4_o = pt_other + (bolt_r + 5) * np.array([0, -1])

                dwg.add(dwg.line((blt1_o), (blt2_o)).stroke('black', width=1, linecap='square'))
                dwg.add(dwg.line((blt3_o), (blt4_o)).stroke('black', width=1, linecap='square'))
                col_list.append(pt_other)
                col_list1.append(pt)
            pitch_pts.append(col_list)
            pitch_pts1.append(col_list1)

        if nc > 1:
            gaugept1_other = np.array(pitch_pts[-1][0])
            gaugept2_other = np.array(pitch_pts[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, gaugept1_other, gaugept2_other, str(int(self.dataObj.gauge)), params)

            faintpt1_other = gaugept1_other
            faintpt1_other1 = gaugept1_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_other = gaugept2_other
            faintpt2_other1 = gaugept2_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            self.dataObj.draw_faint_line(faintpt1_other, faintpt1_other1, dwg)
            self.dataObj.draw_faint_line(faintpt2_other, faintpt2_other1, dwg)

            gaugept1 = np.array(pitch_pts1[-1][0])
            gaugept2 = np.array(pitch_pts1[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outer_arrow(dwg, gaugept2, gaugept1, str(int(self.dataObj.gauge)), params)
            faintpt1 = gaugept1
            faintpt1_1 = gaugept1 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2 = gaugept2 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_1 = gaugept2
            self.dataObj.draw_faint_line(faintpt1, faintpt1_1, dwg)
            self.dataObj.draw_faint_line(faintpt2, faintpt2_1, dwg)

        pt_list = []
        for row in pitch_pts:
            if len(row) > 0:
                pt_list.append(row[0])

        # End and Pitch Distance Information
        pt3 = np.array(pt_list[0])
        pt4 = pt3 + ((self.dataObj.col_B / 2 + 60) + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt3, pt4, dwg)

        pt5 = np.array(pt_list[-1])
        pt6 = pt5 + ((self.dataObj.col_B / 2 + 60)+ self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.draw_faint_line(pt5, pt6, dwg)
        params = {"offset": (self.dataObj.col_B / 2 + 60), "textoffset": 30, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, np.array(pt_list[0]), np.array(pt_list[-1]),
                                                str(len(pt_list) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) + "c/c", params)
        # ------------------------------------------------------------------------------------------------------------------------------------------

        ptx1 = self.FQ1
        pty1 = ptx1 + (self.dataObj.col_B / 2 +30) * np.array([1, 0])
        self.dataObj.draw_faint_line(ptx1, pty1, dwg)

        point = ptx1 - (self.dataObj.end_dist) * np.array([0, -1])
        params = {"offset": (self.dataObj.col_B/2 + 30), "textoffset": 30, "lineori": "left", "endlinedim" : 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptx1, point, str(self.dataObj.end_dist), params)

        # ------------------------------------------------------------------------------------------------------------------------------------------
        ptx2 = self.FQ1 + self.dataObj.plate_ht * np.array([0, 1])
        pty2 = ptx2 + (self.dataObj.col_B / 2 + 30) * np.array([1, 0])
        self.dataObj.draw_faint_line(ptx2, pty2, dwg)

        point1 = ptx2 +(self.dataObj.end_dist) * np.array([0, -1])
        params = {"offset": (self.dataObj.col_B / 2 + 30), "textoffset": 30, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outer_arrow(dwg, ptx2, point1, str(self.dataObj.end_dist), params)

        print "points for end dist:", np.array(pt_list[-1]), self.Q1 - self.dataObj.edge_dist * np.array([1, 0]) + self.dataObj.plate_ht * np.array([0, 1])


        # Beam Information
        beam_pt = (self.FA1 + self.FA2) / 2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam)/2 + 30
        text_up = "Beam " + self.dataObj.beam_Designation
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down, element="")

        # column  Information
        col_pt = self.FD + (self.dataObj.col_B / 2) * np.array([1, 0])
        theta = 90
        offset = 70
        text_up = ""
        text_down = "Column " + self.dataObj.col_Designation
        self.dataObj.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, text_up, text_down, element="")

        # Plate  Information
        beam_pt = self.FQ1 + self.dataObj.plate_ht * np.array([0, 1]) - self.dataObj.plate_width / 4 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.D_col/2 + 50
        text_up = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        text_down = ""
        self.dataObj.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down, element="")

        # Bolt Information
        bolt_pt_x = np.array(pt_list[0])
        theta = 45
        offset = (self.dataObj.col_B - self.dataObj.plate_width) / 2 + self.dataObj.end_dist
        text_up = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.dia_hole) + u'\u00d8' + " holes"

        if str(self.dataObj.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(
                self.dataObj.bolt_type) + " bolts (grade" + " " + str(self.dataObj.bolt_grade) + ")"
        else:
            text_down = "for M" + str(int(self.dataObj.bolt_dia)) + " " + str(self.dataObj.bolt_type) + " " +"(grade" + " " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down, element="")

        # Weld Information
        weld_pt = self.FX + self.dataObj.weld_thick / 2 * np.array([1, 0])
        theta = 45
        offset = ( self.dataObj.D_col/2 + 50)
        text_up = "      z " + str(int(self.dataObj.weld_thick))
        text_down = ""  # u"\u25C1"
        self.dataObj.draw_oriented_arrow(dwg, weld_pt, theta, "NE", offset, text_up, text_down, element="weld")

        # 2D view name
        ptx = (self.FC) + np.array([1, 0]) + (self.dataObj.col_B/2) * np.array([0, 1])
        dwg.add(dwg.text("Side view (Sec B-B)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = (self.FC) + np.array([1, 0]) +  (self.dataObj.col_B/2 + 40) * np.array([0, 1])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        dwg.fit()
        print "********** Column Flange Beam Web Side Saved  *************"
