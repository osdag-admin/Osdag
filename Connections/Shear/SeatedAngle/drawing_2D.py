'''
Created on 08-Nov-2016
@author: jayant patil
'''
import svgwrite
import numpy as np
from numpy import math
import cairosvg
import os


class SeatCommonData(object):
    """Contain common data and functions for use in generating different views.
    Attributes:
    """

    def __init__(self, input_dict, output_dict, beam_data, column_data, angle_data, dicttopangledata,folder):
        """Initialise seated angle connection's geometric properties as class attributes.

        Args:
            input_dict (dictionary): input parameters from GUI
            output_dict (dictionary): output parameters based on calculation
            beam_data (dictionary): geometric properties of beam
            column_data (dictionary): geometric properties of column
            folder (str): path to save the generated images
            angle_data (dictionary):
            top_angle_data (dictionary):

        Returns:
            None

        """
        self.beam_flange_thk = float(beam_data["T"])
        self.col_flange_thk = float(column_data["T"])
        self.beam_depth = int(beam_data["D"])
        self.col_depth = int(column_data["D"])
        self.col_width = int(column_data["B"])
        self.beam_width = int(beam_data["B"])
        self.col_web_thk = float(column_data["tw"])
        self.beam_web_thk = float(beam_data["tw"])
        self.col_designation = column_data["Designation"]
        self.beam_designation = beam_data["Designation"]
        self.beam_R1 = float(beam_data["R1"])
        self.col_R1 = float(column_data["R1"])
        self.bolt_dia = str(input_dict["Bolt"]["Diameter (mm)"])
        self.bolt_hole_diameter = int(output_dict["Bolt"]["hole_dia"])
        self.bolt_type = str(input_dict["Bolt"]["Type"])
        self.grade = input_dict["Bolt"]["Grade"]
        self.connectivity = input_dict['Member']['Connectivity']
        self.pitch = output_dict['Bolt']["Pitch Distance (mm)"]
        self.gauge = output_dict['Bolt']["Gauge Distance (mm)"]
        self.gauge_two_bolt = output_dict["Bolt"]["Gauge Two Bolt (mm)"]
        self.end_dist = output_dict['Bolt']["End Distance (mm)"]
        self.edge_dist = output_dict['Bolt']["Edge Distance (mm)"]

        self.top_angle_end_dist_column = output_dict['Bolt']["top_angle_end_dist_column"]
        self.top_angle_end_dist_beam = output_dict['Bolt']["top_angle_end_dist_beam"]
        self.seat_angle_end_dist_beam = output_dict['Bolt']["seat_angle_end_dist_beam"]

        self.no_of_rows = output_dict['Bolt']["No. of Row"]
        self.no_of_col = output_dict['Bolt']["No. of Column"]

        self.bolts_top_column_col = 2                                       #bolts attached to column top angle in no. of column
        self.bolts_top_column_row = 1                                       #bolts attached to column top angle in no. of rows
        self.bolts_top_beam_col = 2                                         #bolts attached to beam top angle in no. of column
        self.bolts_top_beam_row = 1                                         #bolts attached to beam top angle in no. of rows

        self.bolts_seat_column_col = output_dict['Bolt']["No. of Column"]   #bolts attached to column top angle in no.of column
        self.bolts_seat_column_row = output_dict['Bolt']["No. of Row"]      #bolts attached to column top angle in no. of rows
        self.bolts_seat_beam_col = 2                                        #bolts attached to beam top angle in no. of column
        self.bolts_seat_beam_row = 1                                        #bolts attached to beam top angle in no. of rows

        self.angle_length = output_dict['SeatAngle']['Length (mm)']
        self.col_length = 1000
        self.beam_length = 500
        self.gap = input_dict["detailing"]["gap"] # Clear distance between column and beam

        # ================  seat angle  ==============================
        seat_legsizes = str(angle_data["AXB"])
        self.seat_angle_legsize_vertical = int(seat_legsizes.split('x')[0])
        self.seat_angle_legsize_horizontal = int(seat_legsizes.split('x')[1])
        self.seat_angle_thickness = int(angle_data["t"])
        # self.seat_angle_R1 = int(angle_data["R1"])
        # self.seat_angle_R2 = float(angle_data["R2"])

        # ================  top angle  ================================
        seat_legsizes = str(dicttopangledata["AXB"])
        self.top_angle_legsize_vertical = int(seat_legsizes.split('x')[0])
        self.top_angle_legsize_horizontal = int(seat_legsizes.split('x')[1])

        self.top_angle_thickness = int(dicttopangledata["t"])
        # self.top_angle_R1 = int(top_angle_data["R1"])
        # self.top_angle_R2 = float(top_angle_data["R2"])

        self.folder = folder

    def arc_for_angle(self, dwg):
        '''

        :param dwg:
        :return:
        '''

        arch = dwg.marker(insert=(0, 3), size=(30, 20), orient="auto")
        arch.add(dwg.path(d=" M0,3 L8,6 L5,3 L8,0 L0,3", fill='blue'))

    def add_start_marker(self, dwg):
        '''Draw start arrow to given line.  -------->

        Args:
            dwg (svgwrite object): Container for all svg elements

        Return:
            smarker (svgwrite object)
        '''
        smarker = dwg.marker(insert=(8, 3), size=(30, 30), orient="auto")

        smarker.add(dwg.path(d=" M0,0 L3,3 L0,6 L8,3 L0,0", fill='black'))
        dwg.defs.add(smarker)

        return smarker

    def add_section_marker(self, dwg):
        '''Draw section marking arrow to given line.  -------->

        Args:
            dwg (svgwrite object): Container for all svg elements

        Return:
            section_marker (svgwrite object)
        '''
        section_marker = dwg.marker(insert=(0, 5), size=(10, 10), orient="auto")
        section_marker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill='blue', stroke='black'))
        dwg.defs.add(section_marker)

        return section_marker

    def add_end_marker(self, dwg):
        '''Draw end arrow.  <---------

        Args:
            dwg (svgwrite object): Container for all svg elements

        Return:
            emarker (svgwrite object)
        '''
        emarker = dwg.marker(insert=(0, 3), size=(30, 20), orient="auto")
        emarker.add(dwg.path(d=" M0,3 L8,6 L5,3 L8,0 L0,3", fill='black'))
        dwg.defs.add(emarker)

        return emarker

    def draw_start_arrow(self, line, s_arrow):
        line['marker-start'] = s_arrow.get_funciri()

    def draw_end_arrow(self, line, e_arrow):
        line['marker-end'] = e_arrow.get_funciri()

    def draw_faint_line(self, ptOne, ptTwo, dwg):
        '''Draw faint line to show dimensions.

        Args:
            dwg (svgwrite object): Container for all svg elements
            ptOne (NumPy array): start point
            ptTwo (NumPy array): end point

        Return:
            None
        '''
        dwg.add(dwg.line(ptOne, ptTwo).stroke('#D8D8D8', width=2.5, linecap='square', opacity=0.7))          # #D8D8D8 = grey color

    def draw_dimension_outer_arrow(self, dwg, pt1, pt2, text, params):
        '''Draw outer arrow of dimension line.

        Args:
            dwg (svgwrite object): Container for all svg elements
            pt1 (NumPy array): start point
            pt2 (NumPy array): end point
            text (string): dimension length
            params (dictionary):
                params["offset"] (float): offset of the dimension line
                params["textoffset"] (float): offset of text from dimension line
                params["lineori"] (float): orientation of line [right/left]
                params["endlinedim"] (float): dimension line at the end of the outer arrow

        Return:
            None
        '''
        smarker = self.add_start_marker(dwg)
        emarker = self.add_end_marker(dwg)

        lineVec = pt2 - pt1  # [a, b]
        normal_vector = np.array([-lineVec[1], lineVec[0]])  # [-b, a]
        normal_unit_vector = self.normalize(normal_vector)
        if (params["lineori"] == "left"):
            normal_unit_vector = -normal_unit_vector

        Q1 = pt1 + params["offset"] * normal_unit_vector
        Q2 = pt2 + params["offset"] * normal_unit_vector
        line = dwg.add(dwg.line(Q1, Q2).stroke('black', width=2.5, linecap='square'))
        self.draw_start_arrow(line, emarker)
        self.draw_end_arrow(line, smarker)

        Q12mid = 0.5 * (Q1 + Q2)
        txt_pt = Q12mid + params["textoffset"] * normal_unit_vector
        dwg.add(dwg.text(text, insert=txt_pt, fill='black', font_family="sans-serif", font_size=28))

        L1 = Q1 + params["endlinedim"] * normal_unit_vector
        L2 = Q1 + params["endlinedim"] * (-normal_unit_vector)
        dwg.add(dwg.line(L1, L2).stroke('black', width=2.5, linecap='square', opacity=1.0))
        L3 = Q2 + params["endlinedim"] * normal_unit_vector
        L4 = Q2 + params["endlinedim"] * (-normal_unit_vector)

        dwg.add(dwg.line(L3, L4).stroke('black', width=2.5, linecap='square', opacity=1.0))

    def normalize(self, vec):
        '''Normalize given vecto.

        Args:
            vec (list of floats): list containing X, Y ordinates of vector

        Return:
            vector containing normalized X and Y ordinates
        '''
        a = vec[0]
        b = vec[1]
        mag = math.sqrt(a * a + b * b)
        return vec / mag

    def draw_cross_section(self, dwg, ptA, ptB, txt_pt, text):
        '''Draw cross section.

        Args:
            dwg (svgwrite object): Container for all svg elements
            ptA (NumPy array): start point
            ptB (NumPy array): end point
            txt_pt (NumPy array): location of point to insert text
            text (string):

        Return:
            None
        '''
        line = dwg.add(dwg.line((ptA), (ptB)).stroke('black', width=2.5, linecap='square'))
        sec_arrow = self.add_section_marker(dwg)
        self.draw_end_arrow(line, sec_arrow)
        dwg.add(dwg.text(text, insert=(txt_pt), fill='black', font_family="sans-serif", font_size=52))

    def draw_dimension_inner_arrow(self, dwg, ptA, ptB, text, params):
        '''Draw inner arrow of dimension line.

         Args:
            dwg (svgwrite object): Container for all svg elements
            ptA (NumPy array): start point
            ptB (NumPy array): end point
            text (string): dimension length
            params (dictionary):
                params["offset"] (float): offset of the dimension line
                params["textoffset"] (float): offset of text from dimension line
                params["lineori"] (float): orientation of line [right/left]
                params["endlinedim"] (float): dimension line at the end of the outer arrow
                params["arrowlen"] (float): size of the arrow

        Return:
            None
        '''
        smarker = self.add_start_marker(dwg)
        emarker = self.add_end_marker(dwg)

        u = ptB - ptA  # [a, b]
        u_unit_vector = self.normalize(u)

        v_unit_vector = np.array([-u_unit_vector[1], u_unit_vector[0]])  # [-b, a]

        A1 = ptA + params["endlinedim"] * v_unit_vector
        A2 = ptA + params["endlinedim"] * (-v_unit_vector)
        dwg.add(dwg.line(A1, A2).stroke('black', width=2.5, linecap='square'))
        B1 = ptB + params["endlinedim"] * v_unit_vector
        B2 = ptB + params["endlinedim"] * (-v_unit_vector)
        dwg.add(dwg.line(B1, B2).stroke('black', width=2.5, linecap='square'))
        A3 = ptA - params["arrowlen"] * u_unit_vector
        B3 = ptB + params["arrowlen"] * u_unit_vector

        line = dwg.add(dwg.line(A3, ptA).stroke('black', width=2.5, linecap='square'))
        self.draw_end_arrow(line, smarker)
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width=2.5, linecap='butt'))
        self.draw_end_arrow(line, smarker)
        if (params["lineori"] == "right"):
            txt_pt = B3 + params["textoffset"] * u_unit_vector
        else:
            txt_pt = A3 - (params["textoffset"] + 100) * u_unit_vector

        dwg.add(dwg.text(text, insert=(txt_pt), fill='black', font_family="sans-serif", font_size=28))

    def draw_oriented_arrow(self, dwg, pt, theta, orientation, offset, text_up, text_down):   #, element):
        '''Drawing an arrow in given direction.

         Args:
            dwg (svgwrite object): Container for all svg elements
            pt (NumPy array): start point
            theta (int):
            orientation (string):
            offset (float): offset of the dimension line
            text_up (float):
            text_down (float):
            element :

        Return:
            None
        '''
        # Right Up.
        theta = math.radians(theta)
        char_width = 16
        x_vector = np.array([1, 0])
        y_vector = np.array([0, 1])
        p1 = pt
        lengthA = offset / math.sin(theta)

        arrow_vector = None
        if orientation == "NE":
            arrow_vector = np.array([-math.cos(theta), math.sin(theta)])
        elif orientation == "NW":
            arrow_vector = np.array([math.cos(theta), math.sin(theta)])
        elif orientation == "SE":
            arrow_vector = np.array([-math.cos(theta), -math.sin(theta)])
        elif orientation == "SW":
            arrow_vector = np.array([math.cos(theta), -math.sin(theta)])

        p2 = p1 - lengthA * arrow_vector

        text = text_down if len(text_down) > len(text_up) else text_up
        lengthB = len(text) * char_width

        label_vector = None
        if orientation == "NE":
            label_vector = -x_vector
        elif orientation == "NW":
            label_vector = x_vector
        elif orientation == "SE":
            label_vector = -x_vector
        elif orientation == "SW":
            label_vector = x_vector

        p3 = p2 + lengthB * (-label_vector)

        txt_offset = 18
        offset_vector = -y_vector

        txt_pt_up = None
        if orientation == "NE":
            txt_pt_up = p2 + 0.2 * lengthB * (-label_vector) + txt_offset * offset_vector
            txt_pt_down = p2 - 0.2 * lengthB * label_vector - (txt_offset + 15) * offset_vector
        elif orientation == "NW":
            txt_pt_up = p3 + 0.1 * lengthB * label_vector + txt_offset * offset_vector
            txt_pt_down = p3 - 0.00001 * lengthB * label_vector - (txt_offset + 15) * offset_vector

        elif orientation == "SE":
            txt_pt_up = p2 + 0.1 * lengthB * (-label_vector) + txt_offset * offset_vector
            txt_pt_down = p2 - 0.1 * lengthB * label_vector - (txt_offset + 15) * offset_vector

        elif orientation == "SW":
            txt_pt_up = p3 + 0.2 * lengthB * label_vector + txt_offset * offset_vector
            txt_pt_down = p3 - 0.01 * lengthB * label_vector - (txt_offset + 15) * offset_vector

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill='none', stroke='black', stroke_width=2.5))

        emarker = self.add_end_marker(dwg)
        self.draw_start_arrow(line, emarker)

        dwg.add(dwg.text(text_up, insert=(txt_pt_up), fill='black', font_family="sans-serif", font_size=28))
        dwg.add(dwg.text(text_down, insert=(txt_pt_down), fill='black', font_family="sans-serif", font_size=28))

    def save_to_svg(self, file_name, view):
        '''Create and return svg drawings.

        Args:
            file_name (str):
            view (str): view(s) of drawings to be generated

        Return:
            None

        Note:
            CFBF = Column Flange Beam Flange
            CWBF = Column Web Beam Flange
        '''
        seat_2d_front = Seat2DCreatorFront(self)
        seat_2d_top = Seat2DCreatorTop(self)
        seat_2d_side = Seat2DCreatorSide(self)

        if self.connectivity == 'Column flange-Beam flange':
            if view == "Front":
                seat_2d_front.call_CFBF_front(file_name)
            elif view == "Side":
                seat_2d_side.call_CFBF_side(file_name)
            elif view == "Top":
                seat_2d_top.call_CFBF_top(file_name)
            else:
                file_name = os.path.join(str(self.folder), "images_html", "seatFront.svg")
                seat_2d_front.call_CFBF_front(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=os.path.join(str(self.folder), "images_html", "seatFront.png"))

                file_name = os.path.join(str(self.folder), "images_html", "seatSide.svg")
                seat_2d_side.call_CFBF_side(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=os.path.join(str(self.folder), "images_html", "seatSide.png"))

                file_name = os.path.join(str(self.folder), "images_html", "seatTop.svg")
                seat_2d_top.call_CFBF_top(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=os.path.join(str(self.folder), "images_html", "seatTop.png"))

        elif self.connectivity == 'Column web-Beam flange':
            if view == "Front":
                seat_2d_front.call_CWBF_front(file_name)
            elif view == "Side":
                seat_2d_side.call_CWBF_side(file_name)
            elif view == "Top":
                seat_2d_top.call_CWBF_top(file_name)
            else:
                file_name = os.path.join(str(self.folder), "images_html", "seatFront.svg")
                seat_2d_front.call_CWBF_front(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=os.path.join(str(self.folder), "images_html", "seatFront.png"))

                file_name = os.path.join(str(self.folder), "images_html", "seatSide.svg")
                seat_2d_side.call_CWBF_side(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=os.path.join(str(self.folder), "images_html", "seatSide.png"))

                file_name = os.path.join(str(self.folder), "images_html", "seatTop.svg")
                seat_2d_top.call_CWBF_top(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=os.path.join(str(self.folder), "images_html", "seatTop.png"))


class Seat2DCreatorFront(object):
    """Contains functions for generating the front view of the seated angle connection.
        Attributes:

    """

    def __init__(self, seat_common_object):

        self.data_object = seat_common_object
        # -----------------------------------------------------------------------------------------------
        #              COLUMN FLANGE BEAM FLANGE CONNECTIVITY (FRONT VIEW)
        # -----------------------------------------------------------------------------------------------
        # =================  Column plotting  ===================================

        beam_start_X = self.data_object.col_depth + self.data_object.gap  # 20 mm clear distance between column and beam
        ptSAx = 0
        ptSAy = 0
        self.SA = np.array([ptSAx, ptSAy])

        ptSEx = self.data_object.col_flange_thk
        ptSEy = 0.0
        self.SE = np.array([ptSEx, ptSEy])

        ptSFx = self.data_object.col_depth - self.data_object.col_flange_thk
        ptSFy = 0.0
        self.SF = np.array([ptSFx, ptSFy])

        ptSBx = self.data_object.col_depth
        ptSBy = 0.0
        self.SB = np.array([ptSBx, ptSBy])

        ptSCx = self.data_object.col_depth
        ptSCy = self.data_object.col_length
        self.SC = np.array([ptSCx, ptSCy])

        ptSGx = self.data_object.col_depth - self.data_object.col_flange_thk
        ptSGy = self.data_object.col_length
        self.SG = np.array([ptSGx, ptSGy])

        ptSHx = self.data_object.col_flange_thk
        ptSHy = self.data_object.col_length
        self.SH = np.array([ptSHx, ptSHy])

        ptSDx = 0.0
        ptSDy = self.data_object.col_length
        self.SD = np.array([ptSDx, ptSDy])

        ptSPx = self.data_object.col_depth
        ptSPy = (self.data_object.col_length - self.data_object.beam_depth)/2 + self.data_object.beam_flange_thk
        self.SP = np.array([ptSPx, ptSPy])

        # =================  Beam plotting  ===================================
        # SA1
        ptSA1x = beam_start_X
        ptSA1y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SA1 = np.array([ptSA1x, ptSA1y])

        # SA2
        ptSA2x = ptSA1x + self.data_object.beam_length
        ptSA2y = ptSA1y
        self.SA2 = np.array([ptSA2x, ptSA2y])

        # SA3
        ptSA3x = ptSA1x + self.data_object.beam_length
        ptSA3y = ptSA1y + self.data_object.beam_flange_thk
        self.SA3 = np.array([ptSA3x, ptSA3y])

        # SA4
        ptSA4x = ptSA1x
        ptSA4y = ptSA1y + self.data_object.beam_flange_thk
        self.SA4 = np.array([ptSA4x, ptSA4y])

        # SB1
        ptSB1x = ptSA1x
        ptSB1y = ptSA1y + self.data_object.beam_depth
        self.SB1 = np.array([ptSB1x, ptSB1y])

        # SB2
        ptSB2x = ptSA1x + self.data_object.beam_length
        ptSB2y = ptSA1y + self.data_object.beam_depth
        self.SB2 = np.array([ptSB2x, ptSB2y])

        # SB3
        ptSB3x = ptSA1x + self.data_object.beam_length
        ptSB3y = ptSA1y + self.data_object.beam_depth - self.data_object.beam_flange_thk
        self.SB3 = np.array([ptSB3x, ptSB3y])

        # SB4
        ptSB4x = ptSA1x
        ptSB4y = ptSA1y + self.data_object.beam_depth - self.data_object.beam_flange_thk
        self.SB4 = np.array([ptSB4x, ptSB4y])

        # ============================  Top Angle  ===================================
        ptSC5x = self.data_object.col_depth
        ptSC5y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SC5 = (ptSC5x, ptSC5y)

        ptSC1x = self.data_object.col_depth
        ptSC1y = ptSC5y - self.data_object.top_angle_legsize_vertical
        self.SC1 = (ptSC1x, ptSC1y)

        ptSC4x = ptSC5x + self.data_object.top_angle_legsize_horizontal
        ptSC4y = ptSC5y
        self.SC4 = (ptSC4x, ptSC4y)

        ptSC2x = ptSC1x + self.data_object.top_angle_thickness
        ptSC2y = ptSC5y - self.data_object.top_angle_legsize_vertical
        self.SC2 = (ptSC2x, ptSC2y)

        ptSC3x = ptSC4x
        ptSC3y = ptSC5y - self.data_object.top_angle_thickness
        self.SC3 = (ptSC3x, ptSC3y)

        ptSC6x = ptSC2x
        ptSC6y = ptSC5y # ptSC2y - self.data_object.top_angle_thickness
        self.SC6 = np.array([ptSC6x, ptSC6y])

        ptSC7x = ptSC5x
        ptSC7y = ptSC5y - self.data_object.top_angle_thickness
        self.SC7 = np.array([ptSC7x, ptSC7y])

        ptSCTx = ptSC7x + self.data_object.top_angle_thickness
        ptSCTy = ptSC6y - self.data_object.top_angle_thickness
        self.SCT = np.array([ptSCTx, ptSCTy])

        # ============================  Seat Angle  ===================================
        ptSD5x = self.data_object.col_depth
        ptSD5y = (self.data_object.col_length + self.data_object.beam_depth)/2
        self.SD5 = (ptSD5x, ptSD5y)

        ptSD1x = self.data_object.col_depth
        ptSD1y = ptSD5y + self.data_object.seat_angle_legsize_vertical
        self.SD1 = (ptSD1x, ptSD1y)

        ptSD4x = self.data_object.col_depth + self.data_object.seat_angle_legsize_horizontal
        ptSD4y = ptSD5y
        self.SD4 = (ptSD4x, ptSD4y)

        ptSD2x = ptSD1x + self.data_object.seat_angle_thickness
        ptSD2y = ptSD5y + self.data_object.seat_angle_legsize_vertical
        self.SD2 = (ptSD2x, ptSD2y)

        ptSD3x = ptSD4x
        ptSD3y = ptSD4y + self.data_object.seat_angle_thickness
        self.SD3 = (ptSD3x, ptSD3y)

        ptSD6x = ptSD2x
        ptSD6y = ptSD5y
        self.SD6 = np.array([ptSD6x, ptSD6y])

        ptSD7x = ptSD5x
        ptSD7y = ptSD5y + self.data_object.seat_angle_thickness
        self.SD7 = np.array([ptSD7x, ptSD7y])

        ptSDTx = ptSD7x + self.data_object.seat_angle_thickness
        ptSDTy = ptSD6y + self.data_object.seat_angle_thickness
        self.SDT = np.array([ptSDTx, ptSDTy])
        # -----------------------------------------------------------------------------------------------
        #              COLUMN WEB BEAM FLANGE CONNECTIVITY (FRONT VIEW)
        # -----------------------------------------------------------------------------------------------
        # ========================  Column plotting  ===================================

        ptSWAx = 0
        ptSWAy = 0
        self.SWA = np.array([ptSWAx, ptSWAy])

        ptSWBx = ptSWAx + self.data_object.col_width
        ptSWBy = 0
        self.SWB = np.array([ptSWBx, ptSWBy])

        ptSWCx = ptSWBx
        ptSWCy = ptSWBy + self.data_object.col_length
        self.SWC = np.array([ptSWCx, ptSWCy])

        ptSWDx = ptSWAx
        ptSWDy = ptSWAy + self.data_object.col_length
        self.SWD = np.array([ptSWDx, ptSWDy])

        ptSWEx = self.data_object.col_width / 2 - self.data_object.col_web_thk / 2
        ptSWEy = 0.0
        self.SWE = np.array([ptSWEx, ptSWEy])

        ptSWFx = self.data_object.col_width / 2 + self.data_object.col_web_thk / 2
        ptSWFy = 0
        self.SWF = np.array([ptSWFx, ptSWFy])

        ptSWGx = self.data_object.col_width / 2 + self.data_object.col_web_thk / 2
        ptSWGy = self.data_object.col_length
        self.SWG = np.array([ptSWGx, ptSWGy])

        ptSWHx = self.data_object.col_width / 2 - self.data_object.col_web_thk / 2
        ptSWHy = self.data_object.col_length
        self.SWH = np.array([ptSWHx, ptSWHy])

        ptSWPx = self.data_object.col_width / 2 + self.data_object.col_flange_thk / 2
        ptSWPy = (self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_flange_thk
        self.SWP = np.array([ptSWPx, ptSWPy])

        # =========================  Beam plotting  ===================================

        ptSWA6x = (self.data_object.col_width + self.data_object.col_flange_thk) / 2 + self.data_object.gap
        ptSWA6y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SWA6 = np.array([ptSWA6x, ptSWA6y])

        ptSWA1x = self.data_object.col_width
        ptSWA1y = ptSWA6y
        self.SWA1 = np.array([ptSWA1x, ptSWA1y])

        ptSWA2x = ptSWA6x + self.data_object.beam_length
        ptSWA2y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SWA2 = np.array([ptSWA2x, ptSWA2y])

        ptSWA3x = ptSWA6x + self.data_object.beam_length
        ptSWA3y = ptSWA6y + self.data_object.beam_flange_thk
        self.SWA3 = np.array([ptSWA3x, ptSWA3y])

        ptSWA4x = ptSWA1x
        ptSWA4y = ptSWA1y + self.data_object.beam_flange_thk
        self.SWA4 = np.array([ptSWA4x, ptSWA4y])

        ptSWA5x = ptSWA6x
        ptSWA5y = ptSWA4y
        self.SWA5 = np.array([ptSWA5x, ptSWA5y])

        ptSWB6x = (self.data_object.col_width + self.data_object.col_flange_thk) / 2 + self.data_object.gap
        ptSWB6y = (self.data_object.col_length + self.data_object.beam_depth) / 2 - self.data_object.beam_flange_thk
        self.SWB6 = np.array([ptSWB6x, ptSWB6y])

        ptSWB1x = ptSWA1x
        ptSWB1y = (self.data_object.col_length + self.data_object.beam_depth) / 2 - self.data_object.beam_flange_thk
        self.SWB1 = np.array([ptSWB1x, ptSWB1y])

        ptSWB2x = ptSWB6x +self.data_object.beam_length
        ptSWB2y = (self.data_object.col_length + self.data_object.beam_depth) / 2 - self.data_object.beam_flange_thk
        self.SWB2 = np.array([ptSWB2x, ptSWB2y])

        ptSWB3x = ptSWB6x +self.data_object.beam_length
        ptSWB3y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SWB3 = np.array([ptSWB3x, ptSWB3y])

        ptSWB4x = ptSWA1x
        ptSWB4y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SWB4 = np.array([ptSWB4x, ptSWB4y])

        ptSWB5x = ptSWB6x
        ptSWB5y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SWB5 = np.array([ptSWB5x, ptSWB5y])

        # ============================  Top Angle  ===================================
        ptSWC5x = (self.data_object.col_width + self.data_object.col_web_thk) / 2
        ptSWC5y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SWC5 = (ptSWC5x, ptSWC5y)

        ptSWC1x = ptSWC5x
        ptSWC1y = ptSC5y - self.data_object.top_angle_legsize_vertical
        self.SWC1 = (ptSWC1x, ptSWC1y)

        ptSWC4x = ptSWC5x + self.data_object.top_angle_legsize_horizontal
        ptSWC4y = ptSWC5y
        self.SWC4 = (ptSWC4x, ptSWC4y)

        ptSWC2x = ptSWC1x + self.data_object.top_angle_thickness
        ptSWC2y = ptSWC5y - self.data_object.top_angle_legsize_vertical
        self.SWC2 = (ptSWC2x, ptSWC2y)

        ptSWC3x = ptSWC4x
        ptSWC3y = ptSWC5y - self.data_object.top_angle_thickness
        self.SWC3 = (ptSWC3x, ptSWC3y)

        ptSWC6x = ptSWC2x
        ptSWC6y = ptSWC5y  # ptSC2y - self.data_object.top_angle_thickness
        self.SWC6 = np.array([ptSWC6x, ptSWC6y])

        ptSWC7x = ptSWC5x
        ptSWC7y = ptSWC5y - self.data_object.top_angle_thickness
        self.SWC7 = np.array([ptSWC7x, ptSWC7y])

        ptSWCTx = ptSWC7x + self.data_object.top_angle_thickness
        ptSWCTy = ptSWC6y - self.data_object.top_angle_thickness
        self.SWCT = np.array([ptSWCTx, ptSWCTy])

        # ============================  Seat Angle  ===================================
        ptSWD5x = (self.data_object.col_width + self.data_object.col_web_thk) / 2
        ptSWD5y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SWD5 = (ptSWD5x, ptSWD5y)

        ptSWD1x = ptSWD5x
        ptSWD1y = ptSD5y + self.data_object.seat_angle_legsize_vertical
        self.SWD1 = (ptSWD1x, ptSWD1y)

        ptSWD4x = ptSWD5x + self.data_object.seat_angle_legsize_horizontal
        ptSWD4y = ptSWD5y
        self.SWD4 = (ptSWD4x, ptSWD4y)

        ptSWD2x = ptSWD1x + self.data_object.seat_angle_thickness
        ptSWD2y = ptSWD5y + self.data_object.seat_angle_legsize_vertical
        self.SWD2 = (ptSWD2x, ptSWD2y)

        ptSWD3x = ptSWD4x
        ptSWD3y = ptSWD4y + self.data_object.seat_angle_thickness
        self.SWD3 = (ptSWD3x, ptSWD3y)

        ptSWD6x = ptSWD2x
        ptSWD6y = ptSWD5y
        self.SWD6 = np.array([ptSWD6x, ptSWD6y])

        ptSWD7x = ptSWD5x
        ptSWD7y = ptSWD5y + self.data_object.seat_angle_thickness
        self.SWD7 = np.array([ptSWD7x, ptSWD7y])

        ptSWDTx = ptSWD7x + self.data_object.seat_angle_thickness
        ptSWDTy = ptSWD6y + self.data_object.seat_angle_thickness
        self.SWDT = np.array([ptSWDTx, ptSWDTy])
        # ------------------------------------------------------------------------------------------------------------

    def call_CFBF_front(self, file_name):

        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-280 -370 1500 1700'))
        dwg.add(dwg.polyline(points=[self.SA, self.SB, self.SC, self.SD, self.SA], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SE, self.SH).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.SF, self.SG).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points =[self.SA1, self.SA2, self.SB2, self.SB1, self.SA1], stroke = 'blue', fill = 'none', stroke_width =2.5))
        dwg.add(dwg.line(self.SA4, self.SA3).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.SB4, self.SB3).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.SCT, self.SC2, self.SC1, self.SC5, self.SC4, self.SC3, self.SCT], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SDT, self.SD2, self.SD1, self.SD5, self.SD4, self.SD3, self.SDT], stroke='blue', fill='none', stroke_width=2.5))

        # ===============================  Top angle Bolts plotting  ========================================
        btcr = self.data_object.bolts_top_column_row
        btbr = self.data_object.bolts_top_beam_row

        pt_top_column_list = []
        pt_top_beam_list = []
        bolt_r = float(self.data_object.bolt_dia) / 2

        # ---------------------------------  column bolts --------------------------------------
        if btcr >= 1:
            for column in range(btcr):
                ptx = self.SC5 + (self.data_object.top_angle_legsize_vertical - self.data_object.top_angle_end_dist_column) * np.array([0, -1]) - \
                      self.data_object.col_flange_thk * np.array([1, 0]) + column * self.data_object.gauge_two_bolt * np.array([0, 1])
                ptx1 = ptx - bolt_r * np.array([0, 1])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.col_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx + 10 * np.array([1, 0 ])
                pt_Dx = ptx + (rect_length + 9) * np.array([1, 0])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_column_list.append(ptx)

                pt_Cx1 = ptx + np.array([-1, 0])
                pt_Dx1 = ptx + (rect_length - 9) * np.array([-1, 0])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_column_list.append(ptx)

        # -----------------------------------  beam bolts --------------------------------------
        if btbr >= 1:
            for column in range(btbr):
                pty = self.SC5 + (self.data_object.top_angle_legsize_horizontal - self.data_object.top_angle_end_dist_beam) * np.array([1, 0]) - \
                      self.data_object.beam_flange_thk * np.array([0, 1]) + column * self.data_object.gauge_two_bolt * np.array([1, 0])
                pty1 = pty - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=pty1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = pty + np.array([0, -1])
                pt_Dx = pty + (rect_length - 6) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(pty)

                pt_Cx1 = pty + 15 * np.array([0, 1])
                pt_Dx1 = pty + (rect_length + 15) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(pty)

        # ===============================  Seat angle Bolts plotting  ========================================
        bscr = self.data_object.bolts_seat_column_row
        bsbr = self.data_object.bolts_seat_beam_row
        bscc = self.data_object.bolts_seat_column_col
        pt_seat_column_list = []
        pt_seat_beam_list = []

        # ---------------------------------  column bolts --------------------------------------
        if bscr >= 1:
            for column in range(bscr):
                ptx = self.SD5 + (self.data_object.seat_angle_legsize_vertical - self.data_object.end_dist) * np.array([0, 1]) - \
                      self.data_object.col_flange_thk * np.array([1, 0]) + column * self.data_object.pitch * np.array([0, -1])
                ptx1 = ptx - bolt_r * np.array([0, 1])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.col_flange_thk + self.data_object.seat_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx + 10 * np.array([1, 0])
                pt_Dx = ptx + (rect_length + 9) * np.array([1, 0])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_seat_column_list.append(ptx)

                pt_Cx1 = ptx + np.array([-1, 0])
                pt_Dx1 = ptx + (rect_length - 9) * np.array([-1, 0])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_seat_column_list.append(ptx)

            if bscr >1:
                params = {"offset": (self.data_object.col_depth + 20), "textoffset": 60, "lineori": "left", "endlinedim": 10}
                self.data_object.draw_dimension_outer_arrow(dwg, np.array(pt_seat_column_list[0]),
                                                            np.array(pt_seat_column_list[len(pt_seat_column_list) - 1]), str(int(self.data_object.pitch)), params)
            else:
                pass

        # -----------------------------------  beam bolts --------------------------------------
        if bsbr >= 1:
            for column in range(bsbr):
                pty = self.SD5 + (self.data_object.seat_angle_legsize_horizontal - self.data_object.seat_angle_end_dist_beam) * np.array([1, 0]) - \
                      self.data_object.beam_flange_thk * np.array([0, 1]) + column * self.data_object.gauge_two_bolt * np.array([1, 0])
                pty1 = pty - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.seat_angle_thickness
                dwg.add(dwg.rect(insert=pty1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = pty + np.array([0, -1])
                pt_Dx = pty + (rect_length - 6) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_seat_beam_list.append(pty)

                pt_Cx1 = pty + 5 * np.array([0, 1])
                pt_Dx1 = pty + (rect_length + 15) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_seat_beam_list.append(pty)

        # ===============================  Beam Top angle Bolts Information  ========================================
        no_of_bolts_beam = self.data_object.bolts_top_beam_row * self.data_object.bolts_top_beam_col
        bolt_pt = np.array(pt_top_beam_list[1])
        theta = 60
        offset = self.data_object.beam_depth /1.5
        text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"

        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # ===============================  Column Top angle Bolts Information  ========================================
        no_of_bolts_column = self.data_object.bolts_top_column_row * self.data_object.bolts_top_column_col
        bolt_pt = np.array(pt_top_column_list[0])
        theta = 60
        offset = self.data_object.beam_depth
        text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # ===============================  Beam Seat angle Bolts Information  ========================================
        no_of_bolts_beam = self.data_object.bolts_seat_beam_row * self.data_object.bolts_seat_beam_col
        bolt_pt = np.array(pt_seat_beam_list[0])
        theta = 60
        offset = self.data_object.beam_depth - 30
        text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "SE", offset, text_up, text_down)

        # ===============================  Column Seat angle Bolts Information  ========================================
        no_of_bolts_column = self.data_object.bolts_seat_column_row * self.data_object.bolts_seat_column_col
        bolt_pt = np.array(pt_seat_column_list[0])
        theta = 60
        offset = self.data_object.beam_depth +20
        text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "SE", offset, text_up, text_down)


        # ===============================  Cross section A-A  ===============================================
        ptSecA = self.SA + (50 * np.array([0, -1])) + ((self.data_object.beam_depth - 20) * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))                                       # here 50 is the length of arrow vertically
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)

        ptSecC = ptSecA+ (self.data_object.col_width / 2 + self.data_object.beam_length + 60) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))                                         # here 50 is the length of arrow vertically
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))  # #666666 is red color

        # ===============================  Label Gap Distance  ===============================
        gap_pt = self.data_object.col_length - ((self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_flange_thk)
        # ------------------------  here "gap_pt" represents labelling of [ ___  ___20 ] & "30" represents move 'gap_pt'vertically  ------------------------
        ptG1 = self.SP + (gap_pt + 50) * np.array([0, 1])
        ptG2 = self.SA4 + (gap_pt + 50) * np.array([0, 1])
        offset = self.data_object.col_length  # 60% of the column length
        params = {"offset": offset, "textoffset": -30, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.data_object.gap), params)

        # ===============================  Draw Faint line for Gap Distance  ===============================
        # ------------------------  here "40" represents length of the faint line vertically(left)  ------------------------
        pt_L_G1x = self.SC
        pt_L_G1y = pt_L_G1x + 45 * np.array([0, 1])
        self.data_object.draw_faint_line(pt_L_G1x, pt_L_G1y, dwg)

        # ------------------------  here "70" represents length of the faint line vertically(right)  ------------------------
        pt_R_G2x = self.SB1
        pt_R_G2y = pt_R_G2x + 400 * np.array([0, 1])
        self.data_object.draw_faint_line(pt_R_G2x, pt_R_G2y, dwg)

        # ===============================   Beam Information   ===============================
        beam_pt = self.SA2 + (self.data_object.beam_depth / 2) * np.array([0, 1])
        theta = 1
        offset = 0.01
        text_up = "Beam " + self.data_object.beam_designation
        text_down = ""       # text_down shows empty
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # ===============================   Column Designation  ===============================
        pt = self.SA
        theta = 45
        offset = 30
        pt = self.SA + (self.data_object.col_width/2.5)  * np.array([1, 0])
        theta = 90
        offset = 30
        text_up = "Column " + self.data_object.col_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, pt, theta, "NW", offset, text_up, text_down)

        # ===============================   Seat angle information  ===============================
        seat_angle_pt = self.SD3
        theta = 55
        offset = self.data_object.beam_depth/ 2 - 20
        text_up = "ISA." + str(int(self.data_object.seat_angle_legsize_vertical)) + "X" + str(int(self.data_object.seat_angle_legsize_horizontal)) +\
                  "X" + str(int(self.data_object.seat_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, seat_angle_pt, theta, "SE", offset, text_up, text_down)

        # ===============================   Top angle information  ===============================
        top_angle_pt = self.SC3
        theta = 55
        offset = self.data_object.beam_depth/2 -15
        text_up = ""
        text_down =  "ISA." + str(int(self.data_object.top_angle_legsize_vertical)) + "X" + str(int(self.data_object.top_angle_legsize_horizontal)) +\
                  "X" + str(int(self.data_object.top_angle_thickness))
        self.data_object.draw_oriented_arrow(dwg, top_angle_pt, theta, "NE", offset, text_up, text_down)

        # ======================================  Faint line for TOp angle bolts distances  ================================================
        pt_top_anglex = self.SC2
        pt_top_angley = pt_top_anglex + (self.data_object.col_depth + 20) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglex, pt_top_angley, dwg)

        pt_top_anglex1 = np.array(pt_top_column_list[0])
        pt_top_angley1 = pt_top_anglex1 + (self.data_object.col_depth + 20)* np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglex1, pt_top_angley1, dwg)

        point = pt_top_anglex1 - self.data_object.top_angle_end_dist_column * np.array([0, 1])
        params = {"offset": (self.data_object.col_depth + 20), "textoffset": 60, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglex1, point, str(self.data_object.top_angle_end_dist_column), params)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        pt_top_anglexx = self.SC3
        pt_top_angleyy = pt_top_anglexx + ((self.data_object.col_length - self.data_object.beam_depth)/2 + 50) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_top_anglexx, pt_top_angleyy, dwg)

        pt_top_anglexx1 = np.array(pt_top_beam_list[1])
        pt_top_angleyy1 = pt_top_anglexx1 + (self.data_object.beam_length - 100) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_top_anglexx1, pt_top_angleyy1, dwg)

        point1 = pt_top_anglexx1 +  self.data_object.top_angle_end_dist_beam * np.array([1, 0])
        params = {"offset": ((self.data_object.col_length - self.data_object.beam_depth)/2 + 50) , "textoffset": 20, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglexx1, point1, str(self.data_object.top_angle_end_dist_beam), params)

        # ======================================  Faint line for Seat angle bolts distances  ================================================
        pt_seat_anglex = self.SD2
        pt_seat_angley = pt_seat_anglex + (self.data_object.col_depth + 20) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglex, pt_seat_angley, dwg)

        pt_seat_anglex1 = np.array(pt_seat_column_list[1])
        pt_seat_angley1 = pt_seat_anglex1 + (self.data_object.col_depth + 20) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglex1, pt_seat_angley1, dwg)

        point2 = pt_seat_anglex1 - self.data_object.end_dist * np.array([0, -1])
        params = {"offset": (self.data_object.col_depth + 20), "textoffset": 60, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_seat_anglex1, point2, str(self.data_object.end_dist) , params)
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        pt_seat_anglexx1 = np.array(pt_seat_column_list[0]) - self.data_object.pitch
        pt_seat_angleyy1 = pt_seat_anglexx1 + (self.data_object.col_depth + 20) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglexx1, pt_seat_angleyy1, dwg)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        pt_seat_anglexx = self.SD3
        pt_seat_angleyy = pt_seat_anglexx + ((self.data_object.col_length - self.data_object.beam_depth)/2) * np.array([0, 1])
        self.data_object.draw_faint_line(pt_seat_anglexx, pt_seat_angleyy, dwg)

        pt_seat_anglexx1 = np.array(pt_seat_beam_list[1])
        pt_seat_angleyy1 = pt_seat_anglexx1 + (self.data_object.beam_length - 170) * np.array([0, 1])
        self.data_object.draw_faint_line(pt_seat_anglexx1, pt_seat_angleyy1, dwg)

        point3 = pt_seat_anglexx1 - self.data_object.seat_angle_end_dist_beam * np.array([-1, 0])
        params = {"offset": ((self.data_object.col_length - self.data_object.beam_depth)/2), "textoffset": 35, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_seat_anglexx1, point3, str(self.data_object.seat_angle_end_dist_beam), params)

        # =================================    2D view name   ==================================
        ptx = self.SA + self.data_object.col_depth * np.array([1, 0]) + (self.data_object.col_length + 160) * np.array([0, 1])
        dwg.add(dwg.text('Front view (Sec C-C) ', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 =self.SA + self.data_object.col_depth * np.array([1, 0]) + (self.data_object.col_length + 200) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CWBF_front(self, file_name):

        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-340 -400 1400 1600'))
        dwg.add(dwg.polyline(points=[self.SWA, self.SWB, self.SWC, self.SWD, self.SWA], stroke='blue', fill='none', stroke_width=2.5))
        # ------------------------  here "[5,5]" represents hatching of line  ------------------------
        dwg.add(dwg.line(self.SWE, self.SWH).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line(self.SWF, self.SWG).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline(points=[self.SWA1, self.SWA2, self.SWB3, self.SWB4, self.SWA1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SWA4, self.SWA3).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.SWB1, self.SWB2).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.SWA1, self.SWA6, self.SWB5, self.SWB4], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line(self.SWA5, self.SWA4).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line(self.SWB6, self.SWB1).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline(points=[self.SWCT, self.SWC2, self.SWC1, self.SWC5, self.SWC4, self.SWC3, self.SWCT], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([2, 2])))
        dwg.add(dwg.polyline(points=[self.SWDT, self.SWD2, self.SWD1, self.SWD5, self.SWD4, self.SWD3, self.SWDT], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([2, 2])))

        # ===============================  Cross section A-A  ===============================================
        ptSecA = self.SWA + (50 * np.array([0, -1])) + ((self.data_object.beam_depth - 50) * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))                                       # here 50 is the length of arrow vertically
        txt_pt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)

        ptSecC = ptSecA+ (self.data_object.col_width / 2 + self.data_object.beam_length + 60) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))                                         # here 50 is the length of arrow vertically
        txt_pt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))  # #666666 is red color

        # ===============================  Label Gap Distance  ===============================
        gap_pt = ((self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_flange_thk)
        # ------------------------  here "gap_pt" represents labelling of [ ___  ___20 ] & "600" represents move 'gap_pt'vertically  ------------------------
        ptG1 = self.SWP + (gap_pt + (self.data_object.beam_depth+10)) * np.array([0, 1])
        ptG2 = self.SWA5 + (gap_pt + (self.data_object.beam_depth+10)) * np.array([0, 1])
        offset = self.data_object.col_length  # 60% of the column length
        params = {"offset": offset, "textoffset": -30, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.data_object.gap), params)

        # ===============================  Draw Faint line for Gap Distance  ===============================
        # ------------------------  here "40" represents length of the faint line vertically(left)  ------------------------
        pt_L_G1x = self.SWG
        pt_L_G1y = pt_L_G1x + 45 * np.array([0, 1])
        self.data_object.draw_faint_line(pt_L_G1x, pt_L_G1y, dwg)
        # ------------------------  here "70" represents length of the faint line vertically(right)  ------------------------
        pt_R_G2x = self.SWB5
        pt_R_G2y = pt_R_G2x + 400 * np.array([0, 1])
        self.data_object.draw_faint_line(pt_R_G2x, pt_R_G2y, dwg)

        # ===============================  Top angle Bolts plotting  ========================================
        btcr = self.data_object.bolts_top_column_row
        btbr = self.data_object.bolts_top_beam_row

        bolt_r = int(self.data_object.bolt_dia )/ 2
        pt_top_column_list = []
        pt_top_beam_list = []

        # ---------------------------------  column bolts --------------------------------------
        for i in range(1, (btcr + 1)):
            ptx = self.SWC5 + (self.data_object.top_angle_legsize_vertical - self.data_object.top_angle_end_dist_column) * np.array([0, -1]) - \
                  self.data_object.col_web_thk * np.array([1, 0]) #+ column * self.data_object.gauge * np.array([0, 1])
            ptx1 = ptx - bolt_r * np.array([0, 1])
            rect_width = self.data_object.bolt_dia
            rect_length = self.data_object.col_web_thk + self.data_object.top_angle_thickness
            dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

            pt_Cx = ptx + 10 * np.array([1, 0])
            pt_Dx = ptx + (rect_length + 9) * np.array([1, 0])
            dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
            pt_top_column_list.append(ptx)

            pt_Cx1 = ptx + np.array([-1, 0])
            pt_Dx1 = ptx + (rect_length - 9) * np.array([-1, 0])
            dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
            pt_top_column_list.append(ptx)

        # -----------------------------------  beam bolts --------------------------------------
        if btbr >= 1:
            for column in range(btbr):
                pty = self.SWC5 + (self.data_object.top_angle_legsize_horizontal - self.data_object.top_angle_end_dist_beam) * np.array([1, 0]) - self.data_object.beam_flange_thk * np.array([0, 1]) + column * self.data_object.gauge_two_bolt * np.array([1, 0])
                pty1 = pty - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=pty1, size=(rect_width, rect_length), fill='black', stroke='black',stroke_width=2.5))

                pt_Cx = pty + np.array([0, -1])
                pt_Dx = pty + (rect_length - 6) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(pty)

                pt_Cx1 = pty + 15 * np.array([0, 1])
                pt_Dx1 = pty + (rect_length + 15) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(pty)

        # ===============================  Seat angle Bolts plotting  ========================================
        bscr = self.data_object.bolts_seat_column_row
        bsbr = self.data_object.bolts_seat_beam_row
        pt_seat_column_list = []
        pt_seat_beam_list = []
        # ---------------------------------  column bolts --------------------------------------
        if bscr >= 1:
            for column in range(bscr):
                ptx = self.SWD5 + (self.data_object.seat_angle_legsize_vertical - self.data_object.end_dist) * np.array([0, 1]) - \
                      self.data_object.col_web_thk * np.array([1, 0]) + column * self.data_object.pitch * np.array([0, -1])
                ptx1 = ptx - bolt_r * np.array([0, 1])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.col_web_thk + self.data_object.seat_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx + 10 * np.array([1, 0])
                pt_Dx = ptx + (rect_length + 9) * np.array([1, 0])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_seat_column_list.append(ptx)

                pt_Cx1 = ptx + np.array([-1, 0])
                pt_Dx1 = ptx + (rect_length - 9) * np.array([-1, 0])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_seat_column_list.append(ptx)

        if bscr > 1:
            params = {"offset":(self.data_object.col_width + 10), "textoffset": 60, "lineori": "left", "endlinedim": 10}
            self.data_object.draw_dimension_outer_arrow(dwg, np.array(pt_seat_column_list[0]),
                                                        np.array(pt_seat_column_list[len(pt_seat_column_list)-1]),  str(int(self.data_object.pitch)) , params)
        else:
            pass

        # -----------------------------------  beam bolts --------------------------------------
        if bsbr >= 1:
            for column in range(bsbr):
                pty = self.SWD5 + (self.data_object.seat_angle_legsize_horizontal - self.data_object.seat_angle_end_dist_beam) * np.array([1, 0]) - \
                          self.data_object.beam_flange_thk * np.array([0, 1])  + column * self.data_object.gauge_two_bolt * np.array([1, 0])
                pty1 = pty - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.seat_angle_thickness
                dwg.add(dwg.rect(insert=pty1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = pty + np.array([0, -1])
                pt_Dx = pty + (rect_length - 6) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_seat_beam_list.append(pty)

                pt_Cx1 = pty + 5 * np.array([0, 1])
                pt_Dx1 = pty + (rect_length + 15) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_seat_beam_list.append(pty)

        # ===============================   Beam Information   ===============================
        beam_pt = self.SWA2 + (self.data_object.beam_depth/2) * np.array([0, 1])
        theta = 1
        offset = 1
        text_up = ""    # text_down shows empty
        text_down = "Beam " + self.data_object.beam_designation
        element = ""    # elements shows empty
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # ===============================   Column Designation  ===============================
        pt = self.SWA + (self.data_object.col_width/2.5)  * np.array([1, 0])
        theta = 90
        offset = self.data_object.col_width/2.5
        text_up = "Column " + self.data_object.col_designation
        text_down = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, pt, theta, "NW", offset, text_up, text_down)

        # ===============================   Seat angle information  ===============================
        seat_angle_pt = self.SWD3
        theta = 55
        offset = self.data_object.beam_depth / 4
        text_up = "ISA." + str(int(self.data_object.seat_angle_legsize_vertical)) + "X" + str(int(self.data_object.seat_angle_legsize_horizontal)) +\
                  "X" + str(int(self.data_object.seat_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, seat_angle_pt, theta, "SE", offset, text_up, text_down)

        # ===============================   Top angle information  ===============================
        top_angle_pt = self.SWC3
        theta = 55
        offset = self.data_object.beam_depth / 3
        text_up = ""
        text_down = "ISA." + str(int(self.data_object.top_angle_legsize_vertical)) + "X" + str(int(self.data_object.top_angle_legsize_horizontal)) +\
                  "X" + str(int(self.data_object.top_angle_thickness))
        self.data_object.draw_oriented_arrow(dwg, top_angle_pt, theta, "NE", offset, text_up, text_down)

        # ===============================   Bolts - Top angle Beam part information  ===============================
        no_of_bolts = self.data_object.bolts_top_beam_row * self.data_object.bolts_top_beam_col
        bolt_pt_x = np.array(pt_top_beam_list[1])
        theta = 60
        offset = self.data_object.beam_depth / 1.6
        text_up = str(no_of_bolts) + "nos " + str(int(self.data_object.bolt_hole_diameter)) + u'\u00d8' + "holes "

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down)

        # ===============================   Bolts - Top angle Column part information  ===============================
        no_of_bolts = self.data_object.bolts_top_column_row * self.data_object.bolts_top_column_col
        bolt_pt_x = np.array(pt_top_column_list[0])
        theta = 60
        offset = self.data_object.beam_depth
        text_up = str(no_of_bolts) + "nos " + str(int(self.data_object.bolt_hole_diameter)) + u'\u00d8' + "holes "

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt_x, theta, "NE", offset, text_up, text_down)

        # ===============================   Bolts - Seat angle Beam part information  ===============================
        no_of_bolts = self.data_object.bolts_seat_beam_row * self.data_object.bolts_seat_beam_col
        bolt_pt_x = np.array(pt_seat_beam_list[0])
        theta = 60
        offset = self.data_object.beam_depth/1.8
        text_up = str(no_of_bolts) + "nos " + str(int(self.data_object.bolt_hole_diameter)) + u'\u00d8' + "holes "


        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt_x, theta, "SE", offset, text_up, text_down)

        # ===============================   Bolts - Seat angle Column part information  ===============================
        no_of_bolts = self.data_object.bolts_seat_column_row * self.data_object.bolts_seat_column_col
        bolt_pt_x = np.array(pt_seat_column_list[0])
        theta = 55
        offset = self.data_object.beam_depth/2 + 20
        text_up = str(no_of_bolts) + "nos " + str(int(self.data_object.bolt_hole_diameter)) + u'\u00d8' + "holes "

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt_x, theta, "SE", offset, text_up, text_down)

        # ======================================  Faint line for TOp angle bolts distances  ================================================
        pt_top_anglex = self.SWC2
        pt_top_angley = pt_top_anglex + (self.data_object.col_width + 10) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglex, pt_top_angley, dwg)

        pt_top_anglex1 = np.array(pt_top_column_list[0])
        pt_top_angley1 = pt_top_anglex1 + (self.data_object.col_width + 10) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglex1, pt_top_angley1, dwg)

        point = pt_top_anglex1 - self.data_object.top_angle_end_dist_column * np.array([0, 1])
        params = {"offset": (self.data_object.col_width + 10) , "textoffset": 60, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglex1, point, str(self.data_object.top_angle_end_dist_column), params)
        # -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        pt_top_anglexx = self.SWC3
        pt_top_angleyy = pt_top_anglexx + ((self.data_object.col_length - self.data_object.beam_depth)/2 + 30)  * np.array([0, -1])
        self.data_object.draw_faint_line(pt_top_anglexx, pt_top_angleyy, dwg)

        pt_top_anglexx1 = np.array(pt_top_beam_list[1])
        pt_top_angleyy1 = pt_top_anglexx1 + ((self.data_object.col_length - self.data_object.beam_depth)/2 + 30)  * np.array([0, -1])
        self.data_object.draw_faint_line(pt_top_anglexx1, pt_top_angleyy1, dwg)

        point1 = pt_top_anglexx1 +  self.data_object.top_angle_end_dist_beam * np.array([1, 0])
        params = {"offset": ((self.data_object.col_length - self.data_object.beam_depth)/2 + 30), "textoffset": 20, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglexx1, point1, str(self.data_object.top_angle_end_dist_beam), params)

        # ======================================  Faint line for Seat angle bolts distances  ================================================
        pt_seat_anglex = self.SWD2
        pt_seat_angley = pt_seat_anglex + (self.data_object.col_width + 10)  * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglex, pt_seat_angley, dwg)

        pt_seat_anglex1 = np.array(pt_seat_column_list[1])
        pt_seat_angley1 = pt_seat_anglex1 + (self.data_object.col_width + 10) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglex1, pt_seat_angley1, dwg)

        point2 = pt_seat_anglex1 - self.data_object.end_dist * np.array([0, -1])
        params = {"offset": (self.data_object.col_width + 10), "textoffset": 60, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_seat_anglex1, point2, str(self.data_object.end_dist) , params)
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        pt_seat_anglexx1 = np.array(pt_seat_column_list[-1])
        pt_seat_angleyy1 = pt_seat_anglexx1 + (self.data_object.col_width + 10) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglexx1, pt_seat_angleyy1, dwg)

        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        pt_seat_anglexx = self.SWD3
        pt_seat_angleyy = pt_seat_anglexx + ((self.data_object.col_length - self.data_object.beam_depth)/2 + 20) * np.array([0, 1])
        self.data_object.draw_faint_line(pt_seat_anglexx, pt_seat_angleyy, dwg)

        pt_seat_anglexx1 = np.array(pt_seat_beam_list[1])
        pt_seat_angleyy1 = pt_seat_anglexx1 + ((self.data_object.col_length - self.data_object.beam_depth)/2 + 20) * np.array([0, 1])
        self.data_object.draw_faint_line(pt_seat_anglexx1, pt_seat_angleyy1, dwg)

        point3 = pt_seat_anglexx1 - self.data_object.seat_angle_end_dist_beam * np.array([-1, 0])
        params = {"offset": ((self.data_object.col_length - self.data_object.beam_depth)/2 + 20), "textoffset": 30, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_seat_anglexx1, point3, str(self.data_object.seat_angle_end_dist_beam), params)

         # ======================================   2D view name  =======================================
        ptx = self.SWA + np.array([1, 0]) + (self.data_object.col_length +130) * np.array([0, 1])
        dwg.add(dwg.text('Front view (Sec C-C)', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = self.SWA + np.array([1, 0]) + (self.data_object.col_length + 170) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))
        dwg.save()


class Seat2DCreatorTop(object):
    def __init__(self, seat_common_object):

        self.data_object = seat_common_object
        # --------------------------------------------------------------------------------------------------------------
        #                           COLUMN FLANGE BEAM FLANGE (TOP VIEW)
        # --------------------------------------------------------------------------------------------------------------
        # ========================  Column plotting  ===================================

        ptSAx = 0
        ptSAy = 0
        self.SA = np.array([ptSAx, ptSAy])

        ptSBx = ptSAy + self.data_object.col_flange_thk
        ptSBy = 0
        self.SB = np.array([ptSBx, ptSBy])

        ptSCx = ptSBx
        ptSCy = ptSBy + self.data_object.col_width / 2 - self.data_object.col_web_thk / 2
        self.SC = np.array([ptSCx, ptSCy])

        ptSDx = (self.data_object.col_depth - self.data_object.col_flange_thk)
        ptSDy = ptSCy
        self.SD = np.array([ptSDx, ptSDy])

        ptSEx = ptSDx
        ptSEy = ptSBy
        self.SE = np.array([ptSEx, ptSEy])

        ptSFx = ptSEx + self.data_object.col_flange_thk
        ptSFy = ptSEy
        self.SF = np.array([ptSFx, ptSFy])

        ptSGx = ptSFx
        ptSGy = ptSFy + self.data_object.col_width
        self.SG = np.array([ptSGx, ptSGy])

        ptSHx = ptSDx
        ptSHy = ptSGy
        self.SH = np.array([ptSHx, ptSHy])

        ptSIx = ptSDx
        ptSIy = ptSDy + self.data_object.col_web_thk
        self.SI = np.array([ptSIx, ptSIy])

        ptSJx = ptSCx
        ptSJy = ptSIy
        self.SJ = np.array([ptSJx, ptSJy])

        ptSKx = ptSBx
        ptSKy = ptSBy + self.data_object.col_width
        self.SK = np.array([ptSKx, ptSKy])

        ptSLx = 0
        ptSLy = ptSAx + self.data_object.col_width
        self.SL = np.array([ptSLx, ptSLy])

        ptSPx = self.data_object.col_depth
        ptSPy = self.data_object.col_width / 2
        self.SP = np.array([ptSPx, ptSPy])

        ptSQx = ptSPx
        ptSQy = self.data_object.angle_length / 2
        self.SQ = np.array([ptSQx, ptSQy])

        # ========================  Beam plotting  ===================================

        ptSB1x = ptSPx + self.data_object.gap
        ptSB1y = (self.data_object.col_width - self.data_object.beam_width ) / 2
        self.SB1 = np.array([ptSB1x, ptSB1y])

        ptSB2x = ptSB1x + self.data_object.beam_length
        ptSB2y = ptSB1y
        self.SB2 = np.array([ptSB2x, ptSB2y])

        ptSB3x = ptSB2x
        ptSB3y = ptSB2y + self.data_object.beam_width
        self.SB3 = np.array([ptSB3x, ptSB3y])

        ptSB4x = ptSB1x
        ptSB4y = (self.data_object.col_width + self.data_object.beam_width ) / 2
        self.SB4 = np.array([ptSB4x, ptSB4y])

        # ========================  Top Angle plotting  ===================================
        ptSA1x = ptSPx
        ptSA1y = (self.data_object.col_width - self.data_object.angle_length ) / 2
        self.SA1 = np.array([ptSA1x, ptSA1y])

        ptSA2x = ptSA1x + self.data_object.top_angle_thickness
        ptSA2y = ptSA1y
        self.SA2 = np.array([ptSA2x, ptSA2y])

        ptSA3x = ptSA1x + self.data_object.top_angle_legsize_horizontal
        ptSA3y = ptSA1y
        self.SA3 = np.array([ptSA3x, ptSA3y])

        ptSA4x = ptSA3x
        ptSA4y = ptSA3y + self.data_object.angle_length
        self.SA4 = np.array([ptSA4x, ptSA4y])

        ptSA5x = ptSA2x
        ptSA5y = ptSA2y + self.data_object.angle_length
        self.SA5 = np.array([ptSA5x, ptSA5y])

        ptSA6x = ptSA1x
        ptSA6y = ptSA1y + self.data_object.angle_length
        self.SA6 = np.array([ptSA6x, ptSA6y])

        # --------------------------------------------------------------------------------------------------------------
        #          COLUMN WEB BEAM FLANGE CONNECTIVITY (TOP VIEW)
        # --------------------------------------------------------------------------------------------------------------
        # ========================  Column plotting  ===================================

        ptSWAx = 0
        ptSWAy = 0
        self.SWA = np.array([ptSWAx, ptSWAy])

        ptSWBx = 0
        ptSWBy = ptSWAy + self.data_object.col_flange_thk
        self.SWB = np.array([ptSWBx, ptSWBy])

        ptSWCx = ptSWBx + self.data_object.col_width / 2 - self.data_object.col_web_thk / 2
        ptSWCy = ptSWBy
        self.SWC = np.array([ptSWCx, ptSWCy])

        ptSWDx = ptSWCx
        ptSWDy = (self.data_object.col_depth - self.data_object.col_flange_thk)
        self.SWD = np.array([ptSWDx, ptSWDy])

        ptSWEx = ptSWBx
        ptSWEy = ptSWDy
        self.SWE = np.array([ptSWEx, ptSWEy])

        ptSWFx = ptSWEx
        ptSWFy = ptSWEy + self.data_object.col_flange_thk
        self.SWF = np.array([ptSWFx, ptSWFy])

        ptSWGx = ptSWFx + self.data_object.col_width
        ptSWGy = ptSWFy
        self.SWG = np.array([ptSWGx, ptSWGy])

        ptSWHx = ptSWGx
        ptSWHy = ptSWDy
        self.SWH = np.array([ptSWHx, ptSWHy])

        ptSWIx = ptSWDx + self.data_object.col_web_thk
        ptSWIy = ptSWDy
        self.SWI = np.array([ptSWIx, ptSWIy])

        ptSWJx = ptSWIx
        ptSWJy = ptSWCy
        self.SWJ = np.array([ptSWJx, ptSWJy])

        ptSWKx = ptSWBx + self.data_object.col_width
        ptSWKy = ptSWBy
        self.SWK = np.array([ptSWKx, ptSWKy])

        ptSWLx = ptSWAx + self.data_object.col_width
        ptSWLy = 0
        self.SWL = np.array([ptSWLx, ptSWLy])

        ptSWPx = (self.data_object.col_width + self.data_object.col_web_thk) / 2
        ptSWPy = self.data_object.col_depth / 2
        self.SWP = np.array([ptSWPx, ptSWPy])

        ptSWQx = ptSWPx
        ptSWQy = self.data_object.angle_length / 2
        self.SWQ = np.array([ptSWQx, ptSWQy])

        # ========================  Beam plotting  ===================================
        ptSWB1x = ptSWPx + self.data_object.gap
        ptSWB1y = (self.data_object.col_depth - self.data_object.beam_width) / 2
        self.SWB1 = np.array([ptSWB1x, ptSWB1y])

        ptSWB2x = ptSWB1x + self.data_object.beam_length
        ptSWB2y = ptSWB1y
        self.SWB2 = np.array([ptSWB2x, ptSWB2y])

        ptSWB3x = ptSWB2x
        ptSWB3y = ptSWB2y + self.data_object.beam_width
        self.SWB3 = np.array([ptSWB3x, ptSWB3y])

        ptSWB4x = ptSWB1x
        ptSWB4y = ptSWB1y + self.data_object.beam_width
        self.SWB4 = np.array([ptSWB4x, ptSWB4y])

        ptSWB6x = ptSWB1x
        ptSWB6y = ptSWB1y + (self.data_object.beam_width - self.data_object.angle_length) / 2
        self.SWB6 = np.array([ptSWB6x, ptSWB6y])

        ptSWB5x = ptSWB1x
        ptSWB5y = ptSWB1y + (self.data_object.beam_width + self.data_object.angle_length) / 2
        self.SWB5 = np.array([ptSWB5x, ptSWB5y])

        # ========================  Top Angle plotting  ===================================
        ptSWA1x = ptSWQx
        ptSWA1y = (self.data_object.col_depth - self.data_object.angle_length ) / 2
        self.SWA1 = np.array([ptSWA1x, ptSWA1y])

        ptSWA2x = ptSWA1x + self.data_object.top_angle_thickness
        ptSWA2y = ptSWA1y
        self.SWA2 = np.array([ptSWA2x, ptSWA2y])

        ptSWA3x = ptSWA1x + self.data_object.top_angle_legsize_horizontal
        ptSWA3y = ptSWA1y
        self.SWA3 = np.array([ptSWA3x, ptSWA3y])

        ptSWA4x = ptSWA3x
        ptSWA4y = ptSWA3y + self.data_object.angle_length
        self.SWA4 = np.array([ptSWA4x, ptSWA4y])

        ptSWA5x = ptSWA2x
        ptSWA5y = ptSWA2y + self.data_object.angle_length
        self.SWA5 = np.array([ptSWA5x, ptSWA5y])

        ptSWA6x = ptSWA1x
        ptSWA6y = ptSWA1y + self.data_object.angle_length
        self.SWA6 = np.array([ptSWA6x, ptSWA6y])
        # ------------------------------------------------------------------------------------------------------------

    def call_CFBF_top(self, file_name):
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-400 -400 1500 1300'))
        dwg.add(dwg.polyline(points=[self.SA, self.SB, self.SC, self.SD, self.SE, self.SF, self.SG, self.SH, self.SI, self.SJ, self.SK,
                                     self.SL, self.SA], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SB1, self.SB2, self.SB3, self.SB4], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SB1, self.SB4).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line(self.SA2, self.SA5).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.SA1, self.SA2, self.SA3, self.SA4, self.SA5, self.SA6,
                                     self.SA1], stroke='blue',fill='none', stroke_width=2.5))

        # ===============================  Cross section B-B  ===============================================

        ptSecA = self.SF + (230 + self.data_object.gap + self.data_object.beam_length) * np.array([1, 0])
        ptSecB = ptSecA + 50 * np.array([-1, 0])
        txt_pt = ptSecB + 80 * np.array([-1, 0]) + (20 * np.array([0, 1]))
        txt = "B"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.SG + (230 + self.data_object.gap + self.data_object.beam_length) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))

        #  ===============================  C-C section  ====================================================
        ptSecA = self.SL + 50 * np.array([-1, 0]) + (self.data_object.beam_width * 2.5) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.data_object.col_depth + self.data_object.gap + self.data_object.beam_length + 100) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))

        # ===============================  Top angle Bolts plotting  ========================================
        btbc = self.data_object.bolts_top_beam_col
        btbr = self.data_object.bolts_top_beam_row
        btcc = self.data_object.bolts_top_column_col

        bolt_r = int(self.data_object.bolt_dia )/ 2
        pt_top_column_list = []
        pt_top_beam_list = []

        # --------------------------------  beam bolts -----------------------------
        for i in range(1, (btbr + 1)):
            col_list = []
            for j in range(1, (btbc+ 1)):
                pt = self.SA1 + (self.data_object.top_angle_legsize_horizontal - self.data_object.top_angle_end_dist_beam) * np.array([1, 0]) + \
                     self.data_object.edge_dist * np.array([0, 1]) + (i-1) * self.data_object.pitch * np.array([0, 1]) + (j-1) * self.data_object.gauge_two_bolt * np.array([0, 1])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_list.append(pt)
            pt_top_beam_list.append(col_list)

        # --------------------------------  column bolts -----------------------------
        if btcc >= 1:
            for column in range(btcc):
                ptx = self.SA6 + (self.data_object.angle_length - self.data_object.edge_dist) * np.array([0, -1]) - self.data_object.col_flange_thk *\
                                                                                                                    np.array([1, 0]) + column * self.data_object.gauge_two_bolt * np.array([0, 1])
                ptx1 = ptx - bolt_r * np.array([0, 1])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.col_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx + 10 * np.array([1, 0])
                pt_Dx = ptx + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_column_list.append(ptx)

                pt_Cx1 = ptx + 1 * np.array([-1, 0])
                pt_Dx1 = ptx + (rect_length - 14) * np.array([-1, 0])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_column_list.append(ptx)

        # ===============================  Beam Bolts Information  ========================================
        no_of_bolts_beam = self.data_object.bolts_top_beam_col * self.data_object.bolts_top_beam_row
        bolt_pt = np.array(pt_top_beam_list[0][0])
        theta = 60
        offset = self.data_object.beam_depth/1.5 + 60
        text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # ===============================  Column Bolts Information  ========================================
        no_of_bolts_column = self.data_object.bolts_top_column_col * self.data_object.bolts_top_column_row
        bolt_pt = np.array(pt_top_column_list[0])
        theta = 70
        offset = self.data_object.beam_depth/2 + 50
        text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ===============================  Beam Information  ========================================
        beam_pt = self.SB1 + (self.data_object.beam_length / 2) * np.array([1, 0])
        theta = 60
        offset = 50
        text_up = "Beam " + self.data_object.beam_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # =================================  Column Information  ========================================
        column_pt = self.SG + np.array([1, 0])
        theta = 40
        offset = 130
        text_up = ""
        text_down = "Column " + self.data_object.col_designation
        self.data_object.draw_oriented_arrow(dwg, column_pt, theta, "SE", offset, text_up, text_down)

        # ===============================  Top Angle Information  ========================================
        beam_pt = self.SA3 + (self.data_object.angle_length / 2  + 10) * np.array([0, 1])
        theta = 40
        offset = 130
        text_up = "ISA " + str(int(self.data_object.top_angle_legsize_vertical)) + 'x' + str(int(self.data_object.top_angle_legsize_horizontal)) + 'x' + \
                  str(int(self.data_object.top_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # ======================================  Faint line for TOp angle bolts distances  ================================================
        pt_leftx = self.SA1
        pt_lefty = pt_leftx + (self.data_object.col_depth + 60) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_leftx, pt_lefty, dwg)

        pt_top_anglex1 = np.array(pt_top_column_list[1])
        pt_top_angley1 = pt_top_anglex1 + (self.data_object.col_depth + 60) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglex1, pt_top_angley1, dwg)

        point1 = pt_top_anglex1 - self.data_object.edge_dist * np.array([0, 1])
        params = {"offset": (self.data_object.col_depth + 60), "textoffset": 50, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglex1, point1, str(self.data_object.edge_dist), params)

        # -----------------------------------------------------------------------------------------------------------------------------
        pt_rightx = self.SA6
        pt_righty = pt_rightx + (self.data_object.col_depth + 60) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_rightx, pt_righty, dwg)

        pt_top_anglexx1 = np.array(pt_top_column_list[1]) + self.data_object.gauge_two_bolt * np.array([0, 1])
        pt_top_angleyy1 = pt_top_anglexx1 + (self.data_object.col_depth + 60) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglexx1, pt_top_angleyy1, dwg)

        point2 = pt_top_anglexx1 - self.data_object.edge_dist * np.array([0, -1])
        params = {"offset": (self.data_object.col_depth + 60), "textoffset": 50, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglexx1, point2, str(self.data_object.edge_dist), params)

        params = {"offset": (self.data_object.col_depth + 60), "textoffset": 50, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, point1, point2, str(self.data_object.gauge_two_bolt), params)

        # -----------------------------------------------------------------------------------------------------------------------------
        pt_leftx1 = self.SA3
        pt_lefty1 = pt_leftx1 + (self.data_object.col_depth - 40) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_leftx1, pt_lefty1, dwg)

        pt_beamx = np.array(pt_top_beam_list[0][0]) -  np.array([0, -1])
        pt_beamy = pt_beamx + (self.data_object.col_depth) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_beamx, pt_beamy, dwg)

        point3 = pt_beamx + self.data_object.top_angle_end_dist_beam * np.array([ 1, 0])
        params = {"offset": self.data_object.col_depth, "textoffset": 20, "lineori": "left", "endlinedim":10, "arrowlen":20}
        self.data_object.draw_dimension_outer_arrow(dwg,  pt_beamx, point3,  str(self.data_object.top_angle_end_dist_beam), params)

        # ====================================  Label & Draw Faint line for  Gap Distance  =======================================
        ptGx1 = self.SG
        ptGy1 = ptGx1 + 100 * np.array([0, 1])
        self.data_object.draw_faint_line(ptGx1, ptGy1, dwg)

        ptGx2 = self.SB4
        ptGy2 = ptGx2 + 150 * np.array([0, 1])
        self.data_object.draw_faint_line(ptGx2, ptGy2, dwg)

        point = ptGx2 + self.data_object.gap * np.array([-1, 0])
        params = {"offset": 150, "textoffset": 35, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_outer_arrow(dwg, ptGx2, point,  str(self.data_object.gap), params)

        # ================================  2D view name  ==============================================
        ptx = self.SG + 50 * np.array([-1, 0]) + (self.data_object.beam_length/1.5 + 50) * np.array([0, 1])
        dwg.add(dwg.text('Top view (Sec A-A)', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = self.SG + 50 * np.array([-1, 0]) + (self.data_object.beam_length/1.5 +90) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CWBF_top(self, file_name):
        # vb_ht = str(float(self.data_object.col_depth) + 750)
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-450 -300 1500 1200'))
        dwg.add(dwg.polyline(points=[self.SWA, self.SWB, self.SWC, self.SWD, self.SWE, self.SWF, self.SWG, self.SWH, self.SWI, self.SWJ, self.SWK, self.SWL,
                                     self.SWA], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SWA1, self.SWA3, self.SWA4, self.SWA6, self.SWA1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SWA2, self.SWA5).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.line(self.SWB6, self.SWB5).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line(self.SWB1, self.SWB6).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.SWB4, self.SWB5).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.SWB1, self.SWB2, self.SWB3, self.SWB4], stroke='blue', fill='none', stroke_width=2.5))

        # ===============================  Cross section B-B  ===============================================

        ptSecA = self.SWF + (430 + self.data_object.gap + self.data_object.beam_length) * np.array([1, 0])
        ptSecB = ptSecA + 50 * np.array([-1, 0])
        txt_pt = ptSecB + 80 * np.array([-1, 0]) + (20 * np.array([0, 1]))
        txt = "B"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = self.SWA + (430 + self.data_object.gap + self.data_object.beam_length) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txt_pt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))

        #  ===============================  Cross section C-C  ====================================================
        ptSecA = self.SWA + 50 * np.array([-1, 0]) + (self.data_object.beam_width * 3.5)  * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txt_pt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txt_pt, txt)
        ptSecC = ptSecA + (self.data_object.col_width + self.data_object.gap + self.data_object.beam_length + 100) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txt_pt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txt_pt, txt)
        dwg.add(dwg.line(ptSecA, ptSecC).stroke('#666666', width=1.0, linecap='square'))

        # ===============================  Top angle Bolts plotting  ========================================

        btcc = self.data_object.bolts_top_column_col
        btbc = self.data_object.bolts_top_beam_col
        btbr = self.data_object.bolts_top_beam_row

        bolt_r = int(self.data_object.bolt_dia) / 2
        pt_top_column_list = []
        pt_top_beam_list = []
        # --------------------------------  beam bolts -----------------------------
        for i in range(1, (btbr + 1)):
            col_list = []
            for j in range(1, (btbc + 1)):
                pt = self.SWA1 + (self.data_object.top_angle_legsize_horizontal - self.data_object.seat_angle_end_dist_beam) * np.array([1, 0]) + \
                     self.data_object.edge_dist * np.array([0, 1]) + (i - 1) * self.data_object.pitch * np.array([0, 1]) + (j - 1) * self.data_object.gauge_two_bolt * np.array([0, 1])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_list.append(pt)
            pt_top_beam_list.append(col_list)

            # --------------------------------  column bolts -----------------------------
            if btcc >= 1:
                for column in range(btcc):
                    ptx = self.SWA6 + (self.data_object.angle_length - self.data_object.edge_dist) * np.array([0, -1]) -\
                          self.data_object.col_web_thk * np.array([1, 0]) + column * self.data_object.gauge_two_bolt * np.array([0, 1])
                    ptx1 = ptx - bolt_r * np.array([0, 1])
                    rect_width = self.data_object.bolt_dia
                    rect_length = self.data_object.col_web_thk + self.data_object.top_angle_thickness
                    dwg.add(dwg.rect(insert=ptx1, size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))

                    pt_Cx = ptx + 10 * np.array([1, 0])
                    pt_Dx = ptx + (rect_length + 9) * np.array([1, 0])
                    dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                    pt_top_column_list.append(ptx)

                    pt_Cx1 = ptx +  np.array([-1, 0])
                    pt_Dx1 = ptx + (rect_length - 9) * np.array([-1, 0])
                    dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                    pt_top_column_list.append(ptx)

        # ===============================  Beam Bolts Information  ========================================
        no_of_bolts_beam = self.data_object.bolts_top_beam_col * self.data_object.bolts_top_beam_row
        bolt_pt = np.array(pt_top_beam_list[0][0])
        theta = 60
        offset = self.data_object.beam_width + 50
        text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NE", offset, text_up, text_down)

        # ===============================  Column Bolts Information  ========================================
        no_of_bolts_column = self.data_object.bolts_top_column_col * self.data_object.bolts_top_column_row
        bolt_pt = np.array(pt_top_column_list[0])
        theta = 90
        offset = (self.data_object.col_depth - self.data_object.beam_width)/ 2 + 50
        text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ===============================  Beam Information  ========================================
        beam_pt = self.SWB1 + (self.data_object.beam_length / 2) * np.array([1, 0])
        theta = 50
        offset = 30
        text_up = "Beam " + self.data_object.beam_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # =================================  Column Information  ========================================
        column_pt = self.SWG - 30 * np.array([1, 0])
        theta = 40
        offset = 130
        text_up = ""
        text_down = "Column " + self.data_object.col_designation
        self.data_object.draw_oriented_arrow(dwg, column_pt, theta, "SE", offset, text_up, text_down)

        # ===============================  Top Angle Information  ========================================
        beam_pt = self.SWA3 + ((self.data_object.angle_length / 2) + 20) * np.array([0, 1])
        theta = 40
        offset = 130
        text_up = ""
        text_down = "ISA " + str(int(self.data_object.top_angle_legsize_vertical)) + 'x' + str(int(self.data_object.top_angle_legsize_horizontal)) + 'x' + \
                  str(int(self.data_object.top_angle_thickness))
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # ======================================  Faint line for TOp angle bolts distances  ================================================
        pt_leftx = self.SWA1
        pt_lefty = pt_leftx + self.data_object.col_depth * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_leftx, pt_lefty, dwg)

        pt_top_anglex1 = np.array(pt_top_column_list[1])
        pt_top_angley1 = pt_top_anglex1 + self.data_object.col_depth * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglex1, pt_top_angley1, dwg)

        point1 = pt_top_anglex1 - self.data_object.edge_dist * np.array([0, 1])
        params = {"offset": self.data_object.col_depth, "textoffset": 50, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglex1, point1, str(self.data_object.edge_dist), params)

        # -----------------------------------------------------------------------------------------------------------------------------
        pt_rightx = self.SWA6
        pt_righty = pt_rightx + self.data_object.col_depth * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_rightx, pt_righty, dwg)

        pt_top_anglexx1 = np.array(pt_top_column_list[1]) + self.data_object.gauge_two_bolt * np.array([0, 1])
        pt_top_angleyy1 = pt_top_anglexx1 + self.data_object.col_depth * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_top_anglexx1, pt_top_angleyy1, dwg)

        point2 = pt_top_anglexx1 - self.data_object.edge_dist * np.array([0, -1])
        params = {"offset": self.data_object.col_depth, "textoffset": 50, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglexx1, point2, str(self.data_object.edge_dist), params)

        params = {"offset": self.data_object.col_depth, "textoffset": 50, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, point1, point2, str(self.data_object.gauge_two_bolt), params)

        # -----------------------------------------------------------------------------------------------------------------------------
        pt_leftx1 = self.SWA3
        pt_lefty1 = pt_leftx1 + (self.data_object.col_depth - 40) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_leftx1, pt_lefty1, dwg)

        pt_beamx = np.array(pt_top_beam_list[0][0]) -  np.array([0, -1])
        pt_beamy = pt_beamx + (self.data_object.col_depth) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_beamx, pt_beamy, dwg)

        point3 = pt_beamx + self.data_object.top_angle_end_dist_beam * np.array([ 1, 0])
        params = {"offset": self.data_object.col_depth, "textoffset": 25, "lineori": "left", "endlinedim":10, "arrowlen":20}
        self.data_object.draw_dimension_outer_arrow(dwg,  pt_beamx, point3,  str(self.data_object.top_angle_end_dist_beam), params)

        # ====================================  Label & Draw Faint line for Gap Distance  =======================================
        ptGx1 = self.SWI
        ptGy1 = ptGx1 + 100 * np.array([0, 1])
        self.data_object.draw_faint_line(ptGx1, ptGy1, dwg)

        ptGx2 = self.SWB4
        ptGy2 = ptGx2 + 150 * np.array([0, 1])
        self.data_object.draw_faint_line(ptGx2, ptGy2, dwg)

        point = ptGx2 + self.data_object.gap * np.array([-1, 0])
        params = {"offset": 150, "textoffset": 35, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_outer_arrow(dwg, ptGx2, point,  str(self.data_object.gap), params)


        # ================================  2D view name  ==============================================
        ptx = self.SWC + (self.data_object.beam_length + 40) * np.array([0, 1])
        dwg.add(dwg.text('Top view (Sec A-A)', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = self.SWC + (self.data_object.beam_length + 80) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black', font_family="sans-serif", font_size=30))
        dwg.save()


class Seat2DCreatorSide(object):
    def __init__(self, seat_common_object):

        self.data_object = seat_common_object
        # --------------------------------------------------------------------------------------------------------------
        #                           COLUMN FLANGE BEAM FLANGE (SIDE VIEW)
        # --------------------------------------------------------------------------------------------------------------
        # ========================  Column plotting  ===================================

        self.SA = np.array([0, 0])

        ptSBx = self.data_object.col_width
        ptSBy = 0
        self.SB = np.array([ptSBx, ptSBy])

        ptSCx = self.data_object.col_width
        ptSCy = self.data_object.col_length
        self.SC = np.array([ptSCx, ptSCy])

        ptSDx = 0
        ptSDy = self.data_object.col_length
        self.SD = np.array([ptSDx, ptSDy])

        self.pt_mid_horizontal = self.SA + ((self.data_object.col_width / 2) + (self.data_object.col_web_thk / 2)) * np.array([1, 0])
        self.pt_mid_vertical = self.pt_mid_horizontal + ((self.data_object.col_length - self.data_object.beam_depth) / 2) * np.array([0, 1])

        # ========================  Beam plotting  ===================================

        ptSA1x = (self.data_object.col_depth - self.data_object.beam_width) / 2
        ptSA1y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SA1 = np.array([ptSA1x, ptSA1y])

        ptSA2x = ptSA1x + self.data_object.beam_width
        ptSA2y = ptSA1y
        self.SA2 = np.array([ptSA2x, ptSA2y])

        ptSA3x = ptSA2x
        ptSA3y = ptSA2y + self.data_object.beam_flange_thk
        self.SA3 = np.array([ptSA3x, ptSA3y])

        ptSA12x = ptSA1x
        ptSA12y = ptSA1y + self.data_object.beam_flange_thk
        self.SA12 = np.array([ptSA12x, ptSA12y])

        ptSA4x = ptSA12x + (self.data_object.beam_width / 2 + self.data_object.beam_web_thk / 2)
        ptSA4y = ptSA3y
        self.SA4 = np.array([ptSA4x, ptSA4y])

        ptSA8x = ptSA1x
        ptSA8y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SA8 = np.array([ptSA8x, ptSA8y])

        ptSA9x = ptSA1x
        ptSA9y = ptSA8y - self.data_object.beam_flange_thk
        self.SA9 = np.array([ptSA9x, ptSA9y])

        ptSA7x = ptSA8x + self.data_object.beam_width
        ptSA7y = ptSA8y
        self.SA7 = np.array([ptSA7x, ptSA7y])

        ptSA6x = ptSA7x
        ptSA6y = ptSA7y - self.data_object.beam_flange_thk
        self.SA6 = np.array([ptSA6x, ptSA6y])

        ptSA5x = ptSA4x
        ptSA5y = ptSA6y
        self.SA5 = np.array([ptSA5x, ptSA5y])

        ptSA11x = ptSA12x + (self.data_object.beam_width / 2 - self.data_object.beam_web_thk / 2)
        ptSA11y = ptSA12y
        self.SA11 = np.array([ptSA11x, ptSA11y])

        ptSA10x = ptSA11x
        ptSA10y = ptSA9y
        self.SA10 = np.array([ptSA10x, ptSA10y])

        ptSPx = self.data_object.beam_width / 2
        ptSPy = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SP = (ptSPx, ptSPy)

        ptSQx = self.data_object.angle_length / 2
        ptSQy = ptSPy
        self.SQ = (ptSQx, ptSQy)

        # ============================  Top Angle  ===================================

        ptSB6x = (self.data_object.col_depth - self.data_object.angle_length) / 2
        ptSB6y = ptSQy
        self.SB6 = (ptSB6x, ptSB6y)

        ptSB1x = ptSB6x
        ptSB1y = ptSQy - self.data_object.top_angle_thickness
        self.SB1 = np.array([ptSB1x, ptSB1y])

        ptSB2x = ptSB6x
        ptSB2y = ptSQy - self.data_object.top_angle_legsize_vertical
        self.SB2 = np.array([ptSB2x, ptSB2y])

        ptSB3x = ptSB6x + self.data_object.angle_length
        ptSB3y = ptSB2y
        self.SB3 = np.array([ptSB3x, ptSB3y])

        ptSB4x = ptSB3x
        ptSB4y = ptSB1y
        self.SB4 = np.array([ptSB4x, ptSB4y])

        ptSB5x = ptSB6x + self.data_object.angle_length
        ptSB5y = ptSB6y
        self.SB5 = (ptSB5x, ptSB5y)

        # ============================  Seat Angle  ===================================

        ptSB11x = ptSB6x
        ptSB11y = ptSQy + self.data_object.beam_depth
        self.SB11 = (ptSB11x, ptSB11y)

        ptSB10x = ptSB11x
        ptSB10y = ptSB11y + self.data_object.seat_angle_thickness
        self.SB10 = np.array([ptSB10x, ptSB10y])

        ptSB9x = ptSB11x
        ptSB9y = ptSB11y + self.data_object.seat_angle_legsize_vertical
        self.SB9 = np.array([ptSB9x, ptSB9y])

        ptSB8x = ptSB9x + self.data_object.angle_length
        ptSB8y = ptSB9y
        self.SB8 = np.array([ptSB8x, ptSB8y])

        ptSB7x = ptSB10x + self.data_object.angle_length
        ptSB7y = ptSB10y
        self.SB7 = np.array([ptSB7x, ptSB7y])

        ptSB12x = ptSB11x + self.data_object.angle_length
        ptSB12y = ptSB11y
        self.SB12 = (ptSB12x, ptSB12y)

        # --------------------------------------------------------------------------------------------------------------
        #                           COLUMN WEB BEAM FLANGE (SIDE VIEW)
        # --------------------------------------------------------------------------------------------------------------
        # ========================  Column plotting  ===================================

        ptSWAx = 0
        ptSWAy = 0
        self.SWA = np.array([ptSWAx, ptSWAy])

        ptSWBx = ptSWAx + self.data_object.col_depth
        ptSWBy = 0
        self.SWB = np.array([ptSWBx, ptSWBy])

        ptSWCx = ptSWBx
        ptSWCy = self.data_object.col_length
        self.SWC = np.array([ptSWCx, ptSWCy])

        ptSWDx = 0
        ptSWDy = self.data_object.col_length
        self.SWD = np.array([ptSWDx, ptSWDy])

        ptSWEx = ptSWAx + self.data_object.col_flange_thk
        ptSWEy = 0
        self.SWE = np.array([ptSWEx, ptSWEy])

        ptSWFx = ptSWAx + (self.data_object.col_depth -  self.data_object.col_flange_thk)
        ptSWFy = 0
        self.SWF = np.array([ptSWFx, ptSWFy])

        ptSWGx = ptSWFx
        ptSWGy = self.data_object.col_length
        self.SWG = np.array([ptSWGx, ptSWGy])

        ptSWHx = ptSWEx
        ptSWHy = self.data_object.col_length
        self.SWH = np.array([ptSWHx, ptSWHy])

        self.pt_mid_horizontal = ptSWAx + ((self.data_object.col_depth / 2) + (self.data_object.col_web_thk / 2)) * np.array([1, 0])
        self.pt_mid_vertical = self.pt_mid_horizontal + ((self.data_object.col_length - self.data_object.beam_depth) / 2) * np.array([0, 1])

        # ========================  Beam plotting  ===================================

        ptSWA1x = (self.data_object.col_depth - self.data_object.beam_width) / 2
        ptSWA1y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SWA1 = np.array([ptSWA1x, ptSWA1y])

        ptSWA2x = ptSWA1x + self.data_object.beam_width
        ptSWA2y = ptSWA1y
        self.SWA2 = np.array([ptSWA2x, ptSWA2y])

        ptSWA3x = ptSA2x
        ptSWA3y = ptSWA2y + self.data_object.beam_flange_thk
        self.SWA3 = np.array([ptSWA3x, ptSWA3y])

        ptSWA12x = ptSWA1x
        ptSWA12y = ptSWA1y+ self.data_object.beam_flange_thk
        self.SWA12 = np.array([ptSWA12x, ptSWA12y])

        ptSWA4x = ptSWA12x + (self.data_object.beam_width / 2 + self.data_object.beam_web_thk / 2)
        ptSWA4y = ptSWA3y
        self.SWA4 = np.array([ptSWA4x, ptSWA4y])

        ptSWA8x = ptSWA1x
        ptSWA8y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SWA8 = np.array([ptSWA8x, ptSWA8y])

        ptSWA9x = ptSWA1x
        ptSWA9y = ptSWA8y - self.data_object.beam_flange_thk
        self.SWA9 = np.array([ptSWA9x, ptSWA9y])

        ptSWA7x = ptSWA8x + self.data_object.beam_width
        ptSWA7y = ptSWA8y
        self.SWA7 = np.array([ptSWA7x, ptSWA7y])

        ptSWA6x = ptSWA7x
        ptSWA6y = ptSWA7y - self.data_object.beam_flange_thk
        self.SWA6 = np.array([ptSWA6x, ptSWA6y])

        ptSWA5x = ptSWA4x
        ptSWA5y = ptSWA6y
        self.SWA5 = np.array([ptSWA5x, ptSWA5y])

        ptSWA11x = ptSWA12x + (self.data_object.beam_width / 2 - self.data_object.beam_web_thk / 2)
        ptSWA11y = ptSWA12y
        self.SWA11 = np.array([ptSWA11x, ptSWA11y])

        ptSWA10x = ptSWA11x
        ptSWA10y = ptSWA9y
        self.SWA10 = np.array([ptSWA10x, ptSWA10y])

        ptSWPx = self.data_object.beam_width / 2
        ptSWPy = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.SWP = (ptSWPx, ptSWPy)

        ptSWQx = self.data_object.angle_length / 2
        ptSWQy = ptSWPy
        self.SWQ = (ptSWQx, ptSWQy)

        ptSWQ1x = self.data_object.angle_length / 2
        ptSWQ1y = (self.data_object.col_length + self.data_object.beam_depth) / 2
        self.SWQ1 = (ptSWQ1x, ptSWQ1y)

        # ============================  Top Angle  ===================================
        ptSWB6x = (self.data_object.col_depth - self.data_object.angle_length) / 2
        ptSWB6y = ptSWQy
        self.SWB6 = (ptSWB6x, ptSWB6y)

        ptSWB1x = ptSWB6x
        ptSWB1y = ptSWQy - self.data_object.top_angle_thickness
        self.SWB1 = np.array([ptSWB1x, ptSWB1y])

        ptSWB2x = ptSWB6x
        ptSWB2y = ptSWQy - self.data_object.top_angle_legsize_vertical
        self.SWB2 = np.array([ptSWB2x, ptSWB2y])

        ptSWB3x = ptSWB6x + self.data_object.angle_length
        ptSWB3y = ptSWB2y
        self.SWB3 = np.array([ptSWB3x, ptSWB3y])

        ptSWB4x = ptSWB3x
        ptSWB4y = ptSWB1y
        self.SWB4 = np.array([ptSWB4x, ptSWB4y])

        ptSWB5x = ptSWB6x + self.data_object.angle_length
        ptSWB5y = ptSWB6y
        self.SWB5 = (ptSWB5x, ptSWB5y)

        # ============================  Seat Angle  ===================================
        ptSWB11x = ptSWB6x
        ptSWB11y = ptSWQy + self.data_object.beam_depth
        self.SWB11 = (ptSWB11x, ptSWB11y)

        ptSWB10x = ptSWB11x
        ptSWB10y = ptSWB11y + self.data_object.seat_angle_thickness
        self.SWB10 = np.array([ptSWB10x, ptSWB10y])

        ptSWB9x = ptSWB11x
        ptSWB9y = ptSWB11y + self.data_object.seat_angle_legsize_vertical
        self.SWB9 = np.array([ptSWB9x, ptSWB9y])

        ptSWB8x = ptSWB9x + self.data_object.angle_length
        ptSWB8y = ptSWB9y
        self.SWB8 = np.array([ptSWB8x, ptSWB8y])

        ptSWB7x = ptSWB10x + self.data_object.angle_length
        ptSWB7y = ptSWB10y
        self.SWB7 = np.array([ptSWB7x, ptSWB7y])

        ptSWB12x = ptSWB11x + self.data_object.angle_length
        ptSWB12y = ptSWB11y
        self.SWB12 = (ptSWB12x, ptSWB12y)

    # ------------------------------------------------------------------------------------------------------------

    def call_CWBF_side(self, file_name):
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-550 -350 1200 1500'))
        dwg.add(dwg.polyline(points=[self.SWA, self.SWB, self.SWC, self.SWD, self.SWA], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SWE, self.SWH).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.SWF, self.SWG).stroke('blue', width=2.5, linecap='square'))

        dwg.add(dwg.polyline(points=[self.SWA1, self.SWA2, self.SWA3, self.SWA4, self.SWA5, self.SWA6, self.SWA7, self.SWA8, self.SWA9, self.SWA10,
                                     self.SWA11, self.SWA12, self.SWA1], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SWB6, self.SWB2, self.SWB3, self.SWB5, self.SWB6], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SWB1, self.SWB4).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[self.SWB12, self.SWB8, self.SWB9, self.SWB11, self.SWB12], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SWB10, self.SWB7).stroke('blue', width=2.5, linecap='square'))

        # ===============================  Beam Information  ========================================
        beam_pt = self.SWA3 + np.array([1, 0])
        theta = 65
        offset = self.data_object.beam_depth/3
        text_up = "Beam " + self.data_object.beam_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # =================================  Column Information  ========================================
        beam_pt = self.SWA * np.array([1, 0])
        theta = 90
        offset = 30
        text_up = "Column " + self.data_object.col_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NW", offset, text_up, text_down)

        # ====================================  Top Angle Information  =========================================
        beam_pt = self.SWB3
        theta = 65
        offset =  self.data_object.beam_depth/3
        text_up = "ISA " + str(int(self.data_object.top_angle_legsize_vertical)) + 'x' + str(int(self.data_object.top_angle_legsize_horizontal)) + 'x' + \
                  str(int(self.data_object.top_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # ====================================  Seat Angle Information  =========================================
        beam_pt = self.SWB8
        theta = 65
        offset =  self.data_object.beam_depth/3
        text_up = "ISA " + str(int(self.data_object.seat_angle_legsize_vertical)) + 'x' + str(int(self.data_object.seat_angle_legsize_horizontal)) + 'x' + \
                  str(int(self.data_object.seat_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)


        # ===============================  Top angle Bolts plotting  ========================================
        btcr = self.data_object.bolts_top_column_row
        btcc = self.data_object.bolts_top_column_col
        btbc = self.data_object.bolts_top_beam_col

        bolt_r = int(self.data_object.bolt_dia )/ 2
        pt_top_column_list = []
        pt_top_beam_list = []

        # ---------------------------------  column bolts --------------------------------------
        for i in range(1, (btcr + 1)):
            col_list_top = []
            for j in range(1, (btcc + 1)):
                pt = self.SWB6 + (self.data_object.top_angle_legsize_vertical - self.data_object.top_angle_end_dist_column) * np.array([0, -1]) + \
                     self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch * np.array([0, 1]) + (j - 1) * self.data_object.gauge_two_bolt * np.array([1, 0])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_list_top.append(pt)
            pt_top_column_list.append(col_list_top)

        # ---------------------------------  beam bolts --------------------------------------
        if btbc >= 1:
            for column in range(btbc):
                ptx = self.SWB5 - (self.data_object.angle_length - self.data_object.edge_dist) * np.array( [1, 0]) - self.data_object.beam_flange_thk * np.array([0, 1]) + column * self.data_object.gauge_two_bolt * np.array([1, 0])  # + 20
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black',stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 4) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(ptx)

                pt_Cx1 = ptx +  np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 9) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(ptx)

        # ===============================  Seat angle Bolts plotting  ========================================

        bscr = self.data_object.bolts_seat_column_row
        bscc = self.data_object.bolts_seat_column_col
        bsbc = self.data_object.bolts_seat_beam_col
        pt_seat_column_list = []
        pt_seat_beam_list = []
        # ---------------------------------  column bolts --------------------------------------
        for i in range(1, (bscr + 1)):
            col_list_seat = []
            for j in range(1, (bscc + 1)):
                pt = self.SWB11 + (self.data_object.seat_angle_legsize_vertical - self.data_object.end_dist) * np.array([0, 1]) +\
                     self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch * np.array([0, -1]) + (j - 1) * self.data_object.gauge * np.array([1, 0])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_list_seat.append(pt)
            pt_seat_column_list.append(col_list_seat)

        # ---------------------------------  beam bolts --------------------------------------
        if bsbc >= 1:
            for column in range(bsbc):
                ptx = self.SWB12 - (self.data_object.angle_length - self.data_object.edge_dist) * np.array( [1, 0]) - self.data_object.beam_flange_thk * np.array([0, 1]) + column * self.data_object.gauge_two_bolt * np.array([1, 0])  # + 20
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black',stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 4) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_seat_beam_list.append(ptx)

                pt_Cx1 = ptx +  np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 9) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_seat_beam_list.append(ptx)

        # ===============================  Beam Top angle Bolts Information  ========================================
        no_of_bolts_beam = self.data_object.bolts_top_beam_row * self.data_object.bolts_top_beam_col
        bolt_pt = np.array(pt_top_beam_list[0])
        theta = 55
        offset =  self.data_object.beam_depth/3
        text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ===============================  Column Top angle Bolts Information  ========================================
        no_of_bolts_column = self.data_object.bolts_top_column_row * self.data_object.bolts_top_column_col
        bolt_pt = np.array(pt_top_column_list[0][0])
        theta = 65
        offset =  self.data_object.beam_depth/1.5
        text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ===============================  Beam Seat angle Bolts Information  ========================================
        no_of_bolts_beam = self.data_object.bolts_seat_beam_row * self.data_object.bolts_seat_beam_col
        bolt_pt = np.array(pt_seat_beam_list[0])

        theta = 65
        offset =  self.data_object.beam_depth/1.5
        text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ===============================  Column Seat angle Bolts Information  ========================================
        no_of_bolts_column = self.data_object.bolts_seat_column_row * self.data_object.bolts_seat_column_col
        bolt_pt = np.array(pt_seat_column_list[0][0])
        theta = 55
        offset =  self.data_object.beam_depth/3
        text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

        if str(self.data_object.bolt_type) == "Friction Grip Bolt":
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
        else:
            text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
        self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ======================================  Faint line for TOp angle bolts distances  ================================================
        pt_leftx = self.SWB2
        pt_lefty = pt_leftx + (self.data_object.col_depth+140) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_leftx, pt_lefty, dwg)

        pt_top_anglex1 = np.array(pt_top_column_list[0][0])
        pt_top_angley1 = pt_top_anglex1 + (self.data_object.col_depth + 140) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_top_anglex1, pt_top_angley1, dwg)

        point1 = pt_top_anglex1 + self.data_object.edge_dist * np.array([-1, 0])
        params = {"offset": (self.data_object.col_depth + 140), "textoffset": 10, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglex1, point1, str(self.data_object.edge_dist), params)

        # -----------------------------------------------------------------------------------------------------------------------------
        pt_rightx = self.SWB3
        pt_righty = pt_rightx + (self.data_object.col_depth+140)  * np.array([0, -1])
        self.data_object.draw_faint_line(pt_rightx, pt_righty, dwg)

        pt_top_anglexx1 = np.array(pt_top_column_list[0][0]) + self.data_object.gauge_two_bolt * np.array([1, 0])
        pt_top_angleyy1 = pt_top_anglexx1 - (self.data_object.col_depth + 70) * np.array([0, 1])
        self.data_object.draw_faint_line(pt_top_anglexx1, pt_top_angleyy1, dwg)

        point2 = pt_top_anglexx1 + self.data_object.edge_dist * np.array([1, 0])
        params = {"offset": (self.data_object.col_depth + 140), "textoffset": 10, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglexx1, point2, str(self.data_object.edge_dist), params)

        params = {"offset": (self.data_object.col_depth + 140), "textoffset": 10, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, point1, point2, str(self.data_object.gauge_two_bolt), params)

        # ======================================  Faint line for Seat angle bolts distances  ================================================

        pt_leftx1 = self.SWB9
        pt_lefty1 = pt_leftx1 + self.data_object.col_depth * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_leftx1, pt_lefty1, dwg)

        pt_seat_anglex2 = np.array(pt_seat_column_list[0][0])
        pt_seat_angley2 = pt_seat_anglex2 + (self.data_object.col_depth + 50) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglex2, pt_seat_angley2, dwg)

        point3 = pt_seat_anglex2 + self.data_object.end_dist * np.array([0, 1])
        params = {"offset": (self.data_object.col_depth + 50), "textoffset": 60, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_seat_anglex2, point3, str(self.data_object.end_dist), params)

        pt_seat_anglexx2 = np.array(pt_seat_column_list[0][1])
        pt_seat_angleyy2 = pt_seat_anglexx2 + (self.data_object.col_depth + 50) * np.array([-1,0])
        self.data_object.draw_faint_line(pt_seat_anglexx2, pt_seat_angleyy2, dwg)


        # ======================================  2D view name  ================================================
        ptx = self.SWA +  np.array([1, 0]) + (self.data_object.col_length + 50) * np.array([0, 1])
        dwg.add(dwg.text('Side view (Sec B-B)', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = self.SWA +  np.array([1, 0]) + (self.data_object.col_length + 90) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black',
                         font_family="sans-serif", font_size=30))
        dwg.save()

    def call_CFBF_side(self, file_name):
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-600 -350 1400 1500'))
        dwg.add(dwg.rect(insert=self.SA, size=(self.data_object.col_width, self.data_object.col_length), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SA1, self.SA2, self.SA3, self.SA4, self.SA5, self.SA6, self.SA7, self.SA8, self.SA9, self.SA10, self.SA11,
                                     self.SA12, self.SA1], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SB1, self.SB2, self.SB3, self.SB4, self.SB5, self.SB6, self.SB1], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[self.SB7, self.SB8, self.SB9, self.SB10, self.SB11, self.SB12, self.SB7], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line(self.SB1, self.SB4).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line(self.SB10, self.SB7).stroke('blue', width=2.5, linecap='square'))

        # ===============================  Beam Information  ========================================
        beam_pt = self.SA3 + np.array([1, 0])
        theta = 45
        offset = self.data_object.beam_depth/4
        text_up = "Beam " + self.data_object.beam_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # =================================  Column Information  ========================================
        beam_pt = self.SA + (self.data_object.col_width/5) * np.array([1, 0])
        theta = 90
        offset = self.data_object.col_depth/3
        text_up = "Column " + self.data_object.col_designation
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NW", offset, text_up, text_down)

        # ===============================  Top angle Bolts plotting  ========================================
        btcc = self.data_object.bolts_top_column_col
        btcr = self.data_object.bolts_top_column_row
        btbc = self.data_object.bolts_top_beam_col
        bolt_r = int(self.data_object.bolt_dia )/ 2

        pt_top_column_list = []
        pt_top_beam_list = []

        # ---------------------------------  column bolts --------------------------------------
        for i in range(1, (btcr + 1)):
            col_list_top = []
            for j in range(1, (btcc + 1)):
                pt = self.SB6 + (self.data_object.top_angle_legsize_vertical - self.data_object.top_angle_end_dist_column) * np.array([0, -1]) + \
                     self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch * np.array([0, 1]) + (j - 1) * self.data_object.gauge_two_bolt * np.array([1, 0])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_list_top.append(pt)
            pt_top_column_list.append(col_list_top)

        # ---------------------------------  beam bolts --------------------------------------
        if btbc >= 1:
            for column in range(btbc):
                ptx = self.SB5 - (self.data_object.angle_length - self.data_object.edge_dist) * np.array([1, 0]) - self.data_object.beam_flange_thk * np.array([0, 1]) +\
                      column * self.data_object.gauge_two_bolt * np.array([1, 0]) #+ 20
                ptx1 = ptx - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_length = self.data_object.beam_flange_thk + self.data_object.top_angle_thickness
                dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                pt_Cx = ptx +  np.array([0, -1])
                pt_Dx = ptx + (rect_length - 4) * np.array([0, -1])
                dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(ptx)

                pt_Cx1 = ptx + 10 * np.array([0, 1])
                pt_Dx1 = ptx + (rect_length + 9) * np.array([0, 1])
                dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                pt_top_beam_list.append(ptx)

        # ===============================  Seat angle Bolts plotting  ========================================
        bscc = self.data_object.bolts_seat_column_col
        bscr = self.data_object.bolts_seat_column_row
        bsbc = self.data_object.bolts_seat_beam_col

        pt_seat_column_list = []
        pt_seat_beam_list = []

        # ---------------------------------  column bolts --------------------------------------
        for i in range(1, (bscr + 1)):
            col_list_seat = []
            for j in range(1, (bscc + 1)):
                pt = self.SB11 + (self.data_object.seat_angle_legsize_vertical - self.data_object.end_dist) * np.array([0, 1]) + \
                     self.data_object.edge_dist * np.array([1, 0]) + (i - 1) * self.data_object.pitch * np.array([0, -1]) + (j - 1) * self.data_object.gauge * np.array([1, 0])
                dwg.add(dwg.circle(center=pt, r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                pt_C = pt - (bolt_r + 4) * np.array([1, 0])
                pt_D = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line(pt_C, pt_D).stroke('red', width=1.0, linecap='square'))

                pt_C1 = pt - (bolt_r + 4) * np.array([0, 1])
                pt_D1 = pt + (bolt_r + 4) * np.array([0, 1])
                dwg.add(dwg.line(pt_C1, pt_D1).stroke('red', width=1.0, linecap='square'))

                col_list_seat.append(pt)
            pt_seat_column_list.append(col_list_seat)

            # ---------------------------------  beam bolts --------------------------------------
            if bsbc >= 1:
                for column in range(bsbc):
                    ptx = self.SB12 - (self.data_object.angle_length - self.data_object.edge_dist) * np.array([1, 0]) - self.data_object.beam_flange_thk * np.array([0, 1]) + \
                          column * self.data_object.gauge_two_bolt * np.array([1, 0]) #+ 20
                    ptx1 = ptx - bolt_r * np.array([1, 0])
                    rect_width = self.data_object.bolt_dia
                    rect_length = self.data_object.beam_flange_thk + self.data_object.top_angle_thickness
                    dwg.add(dwg.rect(insert=ptx1, size=(rect_width, rect_length), fill='black', stroke='black', stroke_width=2.5))

                    pt_Cx = ptx + np.array([0, -1])
                    pt_Dx = ptx + (rect_length - 4) * np.array([0, -1])
                    dwg.add(dwg.line(pt_Cx, pt_Dx).stroke('black', width=2.0, linecap='square'))
                    pt_seat_beam_list.append(ptx)

                    pt_Cx1 = ptx + 10 * np.array([0, 1])
                    pt_Dx1 = ptx + (rect_length + 9) * np.array([0, 1])
                    dwg.add(dwg.line(pt_Cx1, pt_Dx1).stroke('black', width=2.0, linecap='square'))
                    pt_seat_beam_list.append(ptx)

            # ===============================  Beam Top angle Bolts Information  ========================================
            no_of_bolts_beam = self.data_object.bolts_top_beam_col * self.data_object.bolts_top_beam_row
            bolt_pt = np.array(pt_top_beam_list[0])
            theta = 70
            offset = self.data_object.beam_depth/4
            text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

            if str(self.data_object.bolt_type) == "Friction Grip Bolt":
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
            else:
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
            self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

            # ===============================  Column Top angle Bolts Information  ========================================
            no_of_bolts_column = self.data_object.bolts_top_column_col * self.data_object.bolts_top_column_row
            bolt_pt = np.array(pt_top_column_list[0][0])
            theta = 70
            offset = self.data_object.beam_depth/2
            text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

            if str(self.data_object.bolt_type) == "Friction Grip Bolt":
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
            else:
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
            self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

            # ===============================  Beam Seat angle Bolts Information  ========================================
            no_of_bolts_beam = self.data_object.bolts_seat_beam_col * self.data_object.bolts_seat_beam_row
            bolt_pt = np.array(pt_seat_beam_list[0])
            theta = 70
            offset = self.data_object.beam_depth/2
            text_up = str(no_of_bolts_beam) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

            if str(self.data_object.bolt_type) == "Friction Grip Bolt":
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
            else:
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
            self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

            # ===============================  Column Seat angle Bolts Information  ========================================
            no_of_bolts_column = self.data_object.bolts_seat_column_col * self.data_object.bolts_seat_column_row
            bolt_pt = np.array(pt_seat_column_list[0][0])
            theta = 70
            offset = self.data_object.beam_depth/3
            text_up = str(no_of_bolts_column) + " nos " + str(self.data_object.bolt_hole_diameter) + u'\u00d8' + " holes"

            if str(self.data_object.bolt_type) == "Friction Grip Bolt":
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " bolts (grade " + str(self.data_object.grade) + ")"
            else:
                text_down = "for M" + str(self.data_object.bolt_dia) + " " + str(
                    self.data_object.bolt_type) + " " + "(grade " + str(self.data_object.grade) + ")"
            self.data_object.draw_oriented_arrow(dwg, bolt_pt, theta, "NW", offset, text_up, text_down)

        # ====================================  Top Angle Information  =========================================
        beam_pt = self.SB3
        theta = 45
        offset = self.data_object.beam_depth/4
        text_up = "ISA " + str(int(self.data_object.top_angle_legsize_vertical)) + 'x' + str(int(self.data_object.top_angle_legsize_horizontal)) + 'x' + \
                  str(int(self.data_object.top_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, text_up, text_down)

        # ====================================  Seat Angle Information  =========================================
        beam_pt = self.SB8
        theta = 45
        offset = self.data_object.beam_depth/4
        text_up = "ISA " + str(int(self.data_object.seat_angle_legsize_vertical)) + 'x' + str(int(self.data_object.seat_angle_legsize_horizontal)) + 'x' + \
                  str(int(self.data_object.seat_angle_thickness))
        text_down = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, text_up, text_down)

        # ======================================  Faint line for TOp angle bolts distances  ================================================
        pt_leftx = self.SB2
        pt_lefty = pt_leftx + (self.data_object.col_depth + 120) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_leftx, pt_lefty, dwg)

        pt_top_anglex1 = np.array(pt_top_column_list[0][0])
        pt_top_angley1 = pt_top_anglex1 + (self.data_object.col_depth + 170) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_top_anglex1, pt_top_angley1, dwg)

        point1 = pt_top_anglex1 + self.data_object.edge_dist * np.array([-1, 0])
        params = {"offset": (self.data_object.col_depth + 170), "textoffset": 20, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglex1, point1, str(self.data_object.edge_dist), params)

        # -----------------------------------------------------------------------------------------------------------------------------
        pt_rightx = self.SB3
        pt_righty = pt_rightx + (self.data_object.col_depth + 120) * np.array([0, -1])
        self.data_object.draw_faint_line(pt_rightx, pt_righty, dwg)

        pt_top_anglexx1 = np.array(pt_top_column_list[0][0]) + self.data_object.gauge_two_bolt * np.array([1, 0])
        pt_top_angleyy1 = pt_top_anglexx1 - (self.data_object.col_depth + 170) * np.array([0, 1])
        self.data_object.draw_faint_line(pt_top_anglexx1, pt_top_angleyy1, dwg)

        point2 = pt_top_anglexx1 + self.data_object.edge_dist * np.array([1, 0])
        params = {"offset": (self.data_object.col_depth + 170), "textoffset": 20, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_top_anglexx1, point2, str(self.data_object.edge_dist), params)

        params = {"offset": (self.data_object.col_depth + 170), "textoffset": 20, "lineori": "left", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, point1, point2, str(self.data_object.gauge_two_bolt), params)


        # ======================================  Faint line for Seat angle bolts distances  ================================================
        pt_leftx1 = self.SB9
        pt_lefty1 = pt_leftx1 + self.data_object.col_depth * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_leftx1, pt_lefty1, dwg)

        pt_seat_anglex2 = np.array(pt_seat_column_list[0][0])
        pt_seat_angley2 = pt_seat_anglex2 + (self.data_object.col_depth + 50) * np.array([-1, 0])
        self.data_object.draw_faint_line(pt_seat_anglex2, pt_seat_angley2, dwg)

        point3 = pt_seat_anglex2 + self.data_object.end_dist * np.array([0, 1])
        params = {"offset": (self.data_object.col_depth + 50), "textoffset": 60, "lineori": "right", "endlinedim": 10, "arrowlen": 20}
        self.data_object.draw_dimension_outer_arrow(dwg, pt_seat_anglex2, point3, str(self.data_object.end_dist), params)

        pt_seat_anglexx2 = np.array(pt_seat_column_list[0][1])
        pt_seat_angleyy2 = pt_seat_anglexx2 + (self.data_object.col_depth + 50) * np.array([-1,0])
        self.data_object.draw_faint_line(pt_seat_anglexx2, pt_seat_angleyy2, dwg)

        # ======================================  2D view name ====================================
        ptx = self.SA + np.array([1, 0]) + (self.data_object.col_length + 50) * np.array([0, 1])
        dwg.add(dwg.text('Side view (Sec B-B)', insert=ptx, fill='black', font_family="sans-serif", font_size=30))
        ptx1 = self.SA + np.array([1, 0]) + (self.data_object.col_length + 90) * np.array([0, 1])

        dwg.add(dwg.text('(All dimensions are in "mm")', insert=ptx1, fill='black',
                         font_family="sans-serif", font_size=30))
        dwg.fit()
        dwg.save()
