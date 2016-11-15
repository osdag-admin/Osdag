'''
Created on 08-Nov-2016
@author: jayant patil
'''
import svgwrite
from PyQt4.QtCore import QString
import numpy as np
from numpy import math
import cairosvg


class SeatCommonData(object):
    """Contain common data and functions for use in generating different views.
    Attributes:


    """

    def __init__(self, input_dict, output_dict, beam_data, column_data, folder):
        """Initialise seated angle connection's geometric properties as class attributes.

        Args:
            input_dict (dictionary): input parameters from GUI
            output_dict (dictionary): output parameters based on calculation
            beam_data (dictionary): geometric properties of beam
            column_data (dictionary): geometric properties of column
            folder (str): path to save the generated images

        Returns:
            None

        """
        self.beam_flange_thk = float(beam_data[QString("T")])
        self.col_flange_thk = float(column_data[QString("T")])
        self.beam_depth = int(beam_data[QString("D")])
        self.col_depth = int(column_data[QString("D")])
        self.col_width = int(column_data[QString("B")])
        self.beam_width = int(beam_data[QString("B")])
        self.col_web_thk = float(column_data[QString("tw")])
        self.beam_web_thk = float(beam_data[QString("tw")])
        self.col_designation = column_data[QString("Designation")]
        self.beam_designation = beam_data[QString("Designation")]
        self.beam_R1 = float(beam_data[QString("R1")])
        self.col_R1 = float(column_data[QString("R1")])
        self.bolt_dia = input_dict["Bolt"]["Diameter (mm)"]
        self.grade = input_dict["Bolt"]["Grade"]
        self.connectivity = input_dict['Member']['Connectivity']
        self.pitch = output_dict['Bolt']["pitch"]
        self.gauge = output_dict['Bolt']["gauge"]
        self.end_dist = output_dict['Bolt']["enddist"]
        self.edge_dist = output_dict['Bolt']["edge"]
        self.no_of_rows = output_dict['Bolt']["numofrow"]
        self.no_of_col = output_dict['Bolt']["numofcol"]
        self.col_length = 700
        self.beam_length = 350
        self.gap = 10  # Clear distance between column and beam
        self.notch_L = (self.col_width - (self.col_web_thk + 40)) / 2.0
        self.notch_ht = self.col_flange_thk + self.col_R1

        self.folder = folder

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

    def draw_end_line(self, line, e_arrow):
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
        dwg.add(dwg.line(ptOne, ptTwo).stroke('#D8D8D8', width=2.5, linecap='square', opacity=0.7))

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
        normalVec = np.array([-lineVec[1], lineVec[0]])  # [-b, a]
        normalUnitVec = self.normalize(normalVec)
        if (params["lineori"] == "left"):
            normalUnitVec = -normalUnitVec

        Q1 = pt1 + params["offset"] * normalUnitVec
        Q2 = pt2 + params["offset"] * normalUnitVec
        line = dwg.add(dwg.line(Q1, Q2).stroke('black', width=2.5, linecap='square'))
        self.draw_start_arrow(line, emarker)
        self.draw_end_line(line, smarker)

        Q12mid = 0.5 * (Q1 + Q2)
        txtPt = Q12mid + params["textoffset"] * normalUnitVec
        dwg.add(dwg.text(text, insert=(txtPt), fill='black', font_family="sans-serif", font_size=28))

        L1 = Q1 + params["endlinedim"] * normalUnitVec
        L2 = Q1 + params["endlinedim"] * (-normalUnitVec)
        dwg.add(dwg.line(L1, L2).stroke('black', width=2.5, linecap='square', opacity=1.0))
        L3 = Q2 + params["endlinedim"] * normalUnitVec
        L4 = Q2 + params["endlinedim"] * (-normalUnitVec)

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

    def draw_cross_section(self, dwg, ptA, ptB, txtPt, text):
        '''Draw cross section.

        Args:
            dwg (svgwrite object): Container for all svg elements
            ptA (NumPy array): start point
            ptB (NumPy array): end point
            txtPt (NumPy array): location of point to insert text
            text (string):

        Return:
            None
        '''
        line = dwg.add(dwg.line((ptA), (ptB)).stroke('black', width=2.5, linecap='square'))
        sec_arrow = self.add_section_marker(dwg)
        self.draw_end_line(line, sec_arrow)
        dwg.add(dwg.text(text, insert=(txtPt), fill='black', font_family="sans-serif", font_size=52))

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
        uUnit = self.normalize(u)

        vUnit = np.array([-uUnit[1], uUnit[0]])  # [-b, a]

        A1 = ptA + params["endlinedim"] * vUnit
        A2 = ptA + params["endlinedim"] * (-vUnit)
        dwg.add(dwg.line(A1, A2).stroke('black', width=2.5, linecap='square'))
        B1 = ptB + params["endlinedim"] * vUnit
        B2 = ptB + params["endlinedim"] * (-vUnit)
        dwg.add(dwg.line(B1, B2).stroke('black', width=2.5, linecap='square'))
        A3 = ptA - params["arrowlen"] * uUnit
        B3 = ptB + params["arrowlen"] * uUnit

        line = dwg.add(dwg.line(A3, ptA).stroke('black', width=2.5, linecap='square'))
        self.draw_end_line(line, smarker)
        # self.draw_start_arrow(line, emarker)
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width=2.5, linecap='butt'))
        self.draw_end_line(line, smarker)
        # self.draw_start_arrow(line, emarker)
        if (params["lineori"] == "right"):
            txtPt = B3 + params["textoffset"] * uUnit
        else:
            txtPt = A3 - (params["textoffset"] + 100) * uUnit

        dwg.add(dwg.text(text, insert=(txtPt), fill='black', font_family="sans-serif", font_size=28))

    def draw_oriented_arrow(self, dwg, pt, theta, orientation, offset, textUp, textDown, element):
        '''Drawing an arrow in given direction.

         Args:
            dwg (svgwrite object): Container for all svg elements
            pt (NumPy array): start point
            theta (int):
            orientation (string):
            offset (float): offset of the dimension line
            textUp (float):
            textDown (float):

        Return:
            None
        '''
        # Right Up.
        theta = math.radians(theta)
        charWidth = 16
        xVec = np.array([1, 0])
        yVec = np.array([0, 1])

        p1 = pt
        lengthA = offset / math.sin(theta)

        arrowVec = None
        if (orientation == "NE"):
            arrowVec = np.array([-math.cos(theta), math.sin(theta)])
        elif (orientation == "NW"):
            arrowVec = np.array([math.cos(theta), math.sin(theta)])
        elif (orientation == "SE"):
            arrowVec = np.array([-math.cos(theta), -math.sin(theta)])
        elif (orientation == "SW"):
            arrowVec = np.array([math.cos(theta), -math.sin(theta)])

        p2 = p1 - lengthA * arrowVec

        text = textDown if len(textDown) > len(textUp) else textUp
        lengthB = len(text) * charWidth

        labelVec = None
        if (orientation == "NE"):
            labelVec = -xVec
        elif (orientation == "NW"):
            labelVec = xVec
        elif (orientation == "SE"):
            labelVec = -xVec
        elif (orientation == "SW"):
            labelVec = xVec

        p3 = p2 + lengthB * (-labelVec)

        txtOffset = 18
        offsetVec = -yVec

        txtPtUp = None
        if (orientation == "NE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - (txtOffset + 15) * offsetVec
        elif (orientation == "NW"):
            txtPtUp = p3 + 0.2 * lengthB * labelVec + txtOffset * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec

        elif (orientation == "SE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - (txtOffset + 15) * offsetVec

        elif (orientation == "SW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + (txtOffset) * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill='none', stroke='black', stroke_width=2.5))

        emarker = self.add_end_marker(dwg)
        self.draw_start_arrow(line, emarker)

        dwg.add(dwg.text(textUp, insert=(txtPtUp), fill='black', font_family="sans-serif", font_size=28))
        dwg.add(dwg.text(textDown, insert=(txtPtDwn), fill='black', font_family="sans-serif", font_size=28))

        if element == "weld":
            if orientation == "NW":
                self.draw_weld_marker(dwg, 15, 7.5, line)
            else:
                self.draw_weld_marker(dwg, 45, 7.5, line)

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
        seat2DFront = Seat2DCreatorFront(self)
        seat2DTop = Seat2DCreatorTop(self)
        seat2DSide = Seat2DCreatorSide(self)

        if self.connectivity == 'Column flange-Beam flange':
            if view == "Front":
                seat2DFront.callCFBFfront(file_name)
            elif view == "Side":
                seat2DSide.callCFBFSide(file_name)
            elif view == "Top":
                seat2DTop.callCFBFTop(file_name)
            else:
                file_name = str(self.folder) + '/images_html/seatFront.svg'
                seat2DFront.callCFBFfront(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=str(self.folder) + '/images_html/seatFront.png')

                file_name = str(self.folder) + '/images_html/seatSide.svg'
                seat2DSide.callCFBFSide(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=str(self.folder) + '/images_html/seatSide.png')

                file_name = str(self.folder) + '/images_html/seatTop.svg'
                seat2DSide.callCFBFTop(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=str(self.folder) + '/images_html/seatTop.png')

        elif self.connectivity == 'Column web-Beam flange':
            if view == "Front":
                seat2DFront.callCWBFfront(file_name)
            elif view == "Side":
                seat2DSide.callCWBFSide(file_name)
            elif view == "Top":
                seat2DSide.callCWBFTop(file_name)
            else:
                file_name = str(self.folder) + '/images_html/seatFront.svg'
                seat2DFront.callCWBFfront(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=str(self.folder) + '/images_html/seatFront.png')

                file_name = str(self.folder) + '/images_html/seatSide.svg'
                seat2DSide.callCWBFSide(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=str(self.folder) + '/images_html/seatSide.png')

                file_name = str(self.folder) + '/images_html/seatTop.svg'
                seat2DSide.callCWBFTop(file_name)
                cairosvg.svg2png(file_obj=file_name, write_to=str(self.folder) + '/images_html/seatTop.png')

                #         return base_front, base_top, base_side


class Seat2DCreatorFront(object):
    """Contains functions for generating the front view of the seated angle connection.
        Attributes:


    """
    def __init__(self, seat_common_object):

        self.data_object = seat_common_object
        # ------------------------------------------------------------------------------
        #              COLUMN WEB BEAM FLANGE CONNECTIVITY (FRONT VIEW)
        # ------------------------------------------------------------------------------

        self.A2 = (self.data_object.col_width, (self.data_object.col_length - self.data_object.beam_depth) / 2)
        self.B = (self.data_object.col_width, 0)
        self.A = (0, 0)
        self.D = (0, self.data_object.col_length)
        self.C = (self.data_object.col_width, self.data_object.col_length)
        self.B2 = (self.data_object.col_width, (self.data_object.beam_depth + self.data_object.col_length) / 2)

        ptEx = (self.data_object.col_width - self.data_object.col_web_thk) / 2
        ptEy = 0.0
        self.E = (ptEx, ptEy)

        ptHx = (self.data_object.col_width - self.data_object.col_web_thk) / 2
        ptHy = self.data_object.col_length
        self.H = (ptHx, ptHy)

        ptFx = (self.data_object.col_width + self.data_object.col_web_thk) / 2
        ptFy = 0
        self.F = (ptFx, ptFy)

        ptGx = (self.data_object.col_width + self.data_object.col_web_thk) / 2
        ptGy = self.data_object.col_length
        self.G = np.array([ptGx, ptGy])

        # Draw rectangle for seatPlate PRSU
        ptPx = (self.data_object.col_width + self.data_object.col_web_thk) / 2
        ptPy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        self.P = (ptPx, ptPy)
        self.ptP = np.array([ptPx, ptPy])

        self.U = self.ptP + (self.data_object.plate_ht) * np.array([0, 1])

        ptRx = (self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plate_width
        ptRy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        self.R = (ptRx, ptRy)

        ptSx = ptRx
        ptSy = ptPy + self.data_object.plate_ht
        self.S = (ptSx, ptSy)

        ptC1x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap)
        ptC1y = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        self.C1 = np.array([ptC1x, ptC1y])

        ptA1x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap)
        ptA1y = ((self.data_object.col_length - self.data_object.beam_depth) / 2)
        self.A1 = np.array([ptA1x, ptA1y])

        ptA3x = ((
                 self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap) + self.data_object.beam_length
        ptA3y = ((self.data_object.col_length - self.data_object.beam_depth) / 2)
        self.A3 = (ptA3x, ptA3y)

        ptB3x = ((
                 self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap) + self.data_object.beam_length
        ptB3y = ((self.data_object.col_length + self.data_object.beam_depth) / 2)
        self.B3 = (ptB3x, ptB3y)

        ptB1x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap)
        ptB1y = ((self.data_object.col_length + self.data_object.beam_depth) / 2)
        # self.B1 = np.array([ptB1x,ptB1y])
        self.ptB1 = np.array([ptB1x, ptB1y])

        ptC2x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + 20)
        ptC2y = ptC1y + self.data_object.plate_ht
        self.C2 = (ptC2x, ptC2y)

        ptA5x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + 20)
        ptA5y = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + self.data_object.beam_flange_thk
        self.A5 = ptA5x, ptA5y

        ptA4x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + 20) + self.data_object.beam_length
        ptA4y = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + self.data_object.beam_flange_thk
        self.A4 = (ptA4x, ptA4y)

        ptB4x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + 20) + self.data_object.beam_length
        ptB4y = ((self.data_object.col_length + self.data_object.beam_depth) / 2) - self.data_object.beam_flange_thk
        self.B4 = (ptB4x, ptB4y)

        ptBx5 = ((self.data_object.col_width + self.data_object.col_web_thk) / 2) + 20
        ptBy5 = ((self.data_object.col_length + self.data_object.beam_depth) / 2) - self.data_object.beam_flange_thk
        self.B5 = (ptBx5, ptBy5)

        ptP1x = ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plateEdge_dist)
        ptP1y = ((self.data_object.col_length - self.data_object.beam_depth) / 2 + (
            self.data_object.col_web_thk + self.data_object.beam_R1 + 3) + self.data_object.end_dist)
        self.P1 = (ptP1x, ptP1y)

        # =======================================================================
        #              COLUMN FLANGE BEAM FLANGE CONNECTIVITY (FRONT VIEW)
        # =======================================================================
        fromPlate_pt = self.data_object.col_depth + self.data_object.gap  # 20 mm clear distance between colume and beam
        ptFAx = 0
        ptFAy = 0
        self.FA = np.array([ptFAx, ptFAy])

        ptFEx = self.data_object.col_flange_thk
        ptFEy = 0.0
        self.FE = (ptFEx, ptFEy)

        ptFFx = self.data_object.col_depth - self.data_object.col_flange_thk
        ptFFy = 0.0
        self.FF = (ptFFx, ptFFy)

        ptFBx = self.data_object.col_depth
        ptFBy = 0.0
        self.FB = (ptFBx, ptFBy)

        ptFCx = self.data_object.col_depth
        ptFCy = self.data_object.col_length
        self.FC = np.array([ptFBx, ptFCy])

        ptFGx = self.data_object.col_depth - self.data_object.col_flange_thk
        ptFGy = self.data_object.col_length
        self.FG = (ptFGx, ptFGy)

        ptFHx = self.data_object.col_flange_thk
        ptFHy = self.data_object.col_length
        self.FH = (ptFHx, ptFHy)

        ptFDx = 0.0
        ptFDy = self.data_object.col_length
        self.FD = (ptFDx, ptFDy)

        ptFPx = self.data_object.col_depth
        ptFPy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        self.FP = (ptFPx, ptFPy)
        self.ptFP = np.array([ptFPx, ptFPy])

        ptFUx = self.data_object.col_depth
        ptFUy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.plate_ht
        self.FU = (ptFUx, ptFUy)

        # FC1
        ptFC1x = fromPlate_pt
        ptFC1y = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        self.FC1 = np.array([ptFC1x, ptFC1y])

        # FC2
        ptFC2x = fromPlate_pt
        ptFC2y = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.plate_ht
        self.FC2 = (ptFC2x, ptFC2y)

        # FA1
        ptFA1x = fromPlate_pt
        ptFA1y = (self.data_object.col_length - self.data_object.beam_depth) / 2
        self.FA1 = np.array([ptFA1x, ptFA1y])

        # FA4
        ptFA4x = fromPlate_pt
        ptFA4y = (self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_flange_thk
        self.FA4 = ptFA4x, ptFA4y

        # FA2
        ptFA2x = ptFC1x + self.data_object.beam_length
        ptFA2y = ptFA1y
        self.FA2 = np.array([ptFA2x, ptFA2y])

        # FA3
        ptFA3x = fromPlate_pt + self.data_object.beam_length
        ptFA3y = (((self.data_object.col_length - self.data_object.beam_depth) / 2) + self.data_object.beam_flange_thk)
        self.FA3 = ptFA3x, ptFA3y

        # FB3
        ptFB3x = fromPlate_pt + self.data_object.beam_length
        ptFB3y = ((
                      self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_depth) - self.data_object.beam_flange_thk
        self.FB3 = (ptFB3x, ptFB3y)

        # FB2
        ptFB2x = fromPlate_pt + self.data_object.beam_length
        ptFB2y = (self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_depth
        self.FB2 = ptFB2x, ptFB2y

        # FB1
        ptFB1x = self.data_object.col_depth + self.data_object.gap
        ptFB1y = (self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_depth
        self.FB1 = np.array([ptFB1x, ptFB1y])

        # FB4
        ptFB4x = fromPlate_pt
        ptFB4y = ((
                      self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_depth) - self.data_object.beam_flange_thk
        self.FB4 = ptFB4x, ptFB4y

    def callCFBFfront(self, file_name):
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-340 -350 1200 1300'))

        dwg.add(dwg.polyline(points=[(self.FA), (self.FB), (self.FC), (self.FD), (self.FA)], stroke='blue', fill='none',
                             stroke_width=2.5))
        dwg.add(dwg.line((self.FE), (self.FH)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FF), (self.FG)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(
            dwg.polyline(points=[(self.FC1), (self.FA1), (self.FA2), (self.FB2), (self.FB1), (self.FC2)], stroke='blue',
                         fill='none', stroke_width=2.5))
        dwg.add(
            dwg.line((self.FC1), (self.FC2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.FA4), (self.FA3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FB4), (self.FB3)).stroke('blue', width=2.5, linecap='square'))

        # Weld hatching to represent WELD.
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 8), patternUnits="userSpaceOnUse",
                                           patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(
            dwg.rect(insert=(self.FP), size=(12, self.data_object.plate_ht), fill="url(#diagonalHatch)", stroke='white',
                     stroke_width=2.0))

        dwg.add(dwg.rect(insert=(self.FP), size=(self.data_object.plate_width, self.data_object.plate_ht), fill='none',
                         stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.data_object.plate_width, self.data_object.plate_ht), fill='none',
                         stroke='blue', stroke_width=2.5))

        nr = self.data_object.no_of_rows
        nc = self.data_object.no_of_col
        bolt_r = self.data_object.bolt_dia / 2
        ptList = []

        for i in range(1, (nr + 1)):
            colList = []
            for j in range(1, (nc + 1)):
                pt = self.ptFP + self.data_object.plateEdge_dist * np.array(
                    [1, 0]) + self.data_object.end_dist * np.array(
                    [0, 1]) + \
                     (i - 1) * self.data_object.pitch * np.array([0, 1]) + (j - 1) * self.data_object.gauge * np.array(
                    [1, 0])
                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1, 0])
                PtD = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line((ptC), (PtD)).stroke('red', width=2.0, linecap='square'))
                ptE = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + (
                                                                                           j - 1) * self.data_object.gauge * np.array(
                    [1, 0])
                ptF = ptE + self.data_object.plate_ht * np.array([0, 1])
                dwg.add(dwg.line((ptE), (ptF)).stroke('blue', width=1.5, linecap='square').dasharray(
                    dasharray=([20, 5, 1, 5])))
                colList.append(pt)
            ptList.append(colList)

        pitchPts = []
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        params = {"offset": self.data_object.col_depth + self.data_object.plateEdge_dist + 50, "textoffset": 235,
                  "lineori": "right", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len(pitchPts) - 1]),
                                                    str(len(pitchPts) - 1) + u' \u0040' + str(
                                                        int(self.data_object.pitch)) + " mm c/c", params)

        # Cross section A-A
        ptSecA = self.FA + (320 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txtpt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.FA2 + (472 * np.array([0, -1]))
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txtpt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        # Distance between Beam Flange and Plate

        params = {"offset": self.data_object.col_depth + self.data_object.gap + 50, "textoffset": 125,
                  "lineori": "right",
                  "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, self.FA1, self.FC1, str(
            int(self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)) + " mm", params)
        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        ptOne = self.FA1
        ptBx = -30
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2)
        ptTwo = (ptBx, ptBy)
        self.data_object.draw_faint_line(ptOne, ptTwo, dwg)

        # End Distance from the starting point of plate Information
        edgPtx = (self.data_object.col_depth) + self.data_object.plateEdge_dist
        edgPty = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        edgPt = (edgPtx, edgPty)
        params = {"offset": self.data_object.col_depth + self.data_object.plateEdge_dist + 50, "textoffset": 125,
                  "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[0]), np.array([edgPtx, edgPty]),
                                                    str(int(self.data_object.end_dist)) + " mm", params)

        # End Distance from plate end point.
        edgPt1x = edgPtx
        edgPt1y = edgPty + self.data_object.plate_ht
        edgPt1 = (edgPt1x, edgPt1y)
        params = {"offset": self.data_object.col_depth + self.data_object.plateEdge_dist + 50, "textoffset": 125,
                  "lineori": "right", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[len(pitchPts) - 1]),
                                                    np.array([edgPt1x, edgPt1y]),
                                                    str(int(self.data_object.end_dist)) + " mm", params)

        # Edge Distance information
        pt1A = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + \
               (self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
                   [1, 0]) + self.data_object.end_dist * np.array(
            [0, 1])
        pt1B = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + \
               (self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
                   [1, 0]) + self.data_object.edge_dist * np.array(
            [1, 0]) + self.data_object.end_dist * np.array([0, 1])
        offset = self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3
        params = {"offset": self.data_object.col_depth + self.data_object.plateEdge_dist, "textoffset": 20,
                  "lineori": "left",
                  "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, pt1A, pt1B, str(int(self.data_object.edge_dist)) + " mm",
                                                    params)

        # Faint line for Edge distance dimension
        ptB1 = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + \
               (self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
                   [1, 0]) + self.data_object.edge_dist * np.array(
            [1, 0])
        ptB2 = ptB1 + ((
                           self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + 115) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptB1, ptB2, dwg)

        # Gauge Distance

        if self.data_object.no_of_col > 1:
            A = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + self.data_object.end_dist * np.array(
                [0, 1])
            B = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + \
                (self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
                    [1, 0]) + self.data_object.end_dist * np.array(
                [0, 1])
            offset = (self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + 130
            params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
            self.data_object.draw_dimension_outer_arrow(dwg, A, B, str(int(self.data_object.gauge)) + " mm", params)
            FA = self.FP + self.data_object.plateEdge_dist * np.array([1, 0])
            FB = self.FP + self.data_object.plateEdge_dist * np.array([1, 0]) + ((
                                                                                     self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + 70) * np.array(
                [0, -1])
            self.data_object.draw_faint_line(FA, FB, dwg)

        # Gap Distance
        gapPt = self.data_object.col_length - ((self.data_object.col_length - self.data_object.beam_depth) / 2 + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3))
        ptG1 = self.ptFP + (gapPt + 30) * np.array([0, 1])
        ptG2 = self.FC1 + (gapPt + 30) * np.array([0, 1])
        offset = self.data_object.col_length  # 60% of the column length
        params = {"offset": offset, "textoffset": 20, "lineori": "right", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.data_object.gap) + " mm", params)

        # Draw Faint line for Gap Distance
        ptC1 = self.FC
        ptC2 = ptC1 + 20 * np.array([0, 1])
        self.data_object.draw_faint_line(ptC1, ptC2, dwg)

        ptD1 = self.FB1
        ptD2 = ptD1 + 70 * np.array([0, 1])
        self.data_object.draw_faint_line(ptD1, ptD2, dwg)

        # Draws faint line to show dimensions
        # Faint lines for gauge and edge distances
        ptA1 = self.ptFP + self.data_object.plateEdge_dist * np.array([1, 0]) + \
               (self.data_object.no_of_col - 1) * self.data_object.gauge * np.array([1, 0])
        ptA2 = ptA1 + ((
                           self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + 115) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptA1, ptA2, dwg)

        ptA = self.FP
        ptBx = -30
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        ptB = (ptBx, ptBy)
        self.data_object.draw_faint_line(ptA, ptB, dwg)

        pt1 = np.array(pitchPts[0]) - 20 * np.array([1, 0])
        ptBx = -30
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.end_dist
        pt2 = (ptBx, ptBy)
        self.data_object.draw_faint_line(pt1, pt2, dwg)

        ptOne = np.array(pitchPts[len(pitchPts) - 1])
        ptBx = -30
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + (
               self.data_object.plate_ht - self.data_object.end_dist)
        ptTwo = (ptBx, ptBy)
        self.data_object.draw_faint_line(ptOne, ptTwo, dwg)

        ptOne = self.FU
        ptBx = -30
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.plate_ht
        ptTwo = (ptBx, ptBy)
        self.data_object.draw_faint_line(ptOne, ptTwo, dwg)

        # Beam Information
        beam_pt = self.FA2 + self.data_object.beam_depth / 2 * np.array([0, 1])
        theta = 1
        offset = 0.0
        textUp = "Beam " + self.data_object.beam_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element)

        # Column Designation
        ptx = self.data_object.col_depth / 2
        pty = 0
        pt = self.FA + 10 * np.array([1, 0])  # np.array([ptx,pty])
        theta = 30
        offset = 40  # self.data_object.col_length /7
        textUp = "Column " + self.data_object.col_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, pt, theta, "NW", offset, textUp, textDown, element)

        # Weld Information
        #         weldPtx = (self.data_object.col_depth)
        #         weldPty = ((self.data_object.col_length - self.data_object.beam_depth)/2) + (self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        weldPt = self.ptFP + 6 * np.array([1, 0]) + self.data_object.end_dist * np.array([0, 1])
        theta = 45
        offset = self.data_object.col_width
        textUp = "         z " + str(int(self.data_object.weld_thick)) + " mm"
        textDown = ""  # u"\u25C1"
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, weldPt, theta, "NW", offset, textUp, textDown, element)

        # Bolt Information
        bltPtx = self.FP + self.data_object.plateEdge_dist * np.array([1, 0]) + self.data_object.end_dist * np.array(
            [0, 1]) + (
                          self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
            [1, 0])
        theta = 45
        offset = (self.data_object.beam_depth * 3) / 8
        textUp = str(self.data_object.no_of_rows) + " nos " + str(int(self.data_object.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(int(self.data_object.bolt_dia)) + " bolts (grade" + str(self.data_object.grade) + ")"
        element = ""
        self.data_object.draw_oriented_arrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element)

        # Plate Information
        pltPtx = self.data_object.col_depth + self.data_object.plate_width / 2
        pltPty = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.plate_ht
        pltPt = np.array([pltPtx, pltPty])
        theta = 45
        offset = (self.data_object.beam_depth) / 2
        textUp = "PLT. " + str(int(self.data_object.plate_ht)) + "X" + str(
            int(self.data_object.plate_width)) + "X" + str(
            int(self.data_object.plate_thick))
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, pltPt, theta, "SE", offset, textUp, textDown, element)

        # 2D view name
        ptx = self.FG + (self.data_object.col_length / 5) * np.array([0, 1]) + 50 * np.array([-1, 0])
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"########### Column Flange Beam Flange Saved ############"

    def callCWBFfront(self, file_name):

        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-410 -350 1250 1280'))

        ptSecA = self.A + (320 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txtpt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.A3 + (472 * np.array([0, -1]))
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txtpt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.A2), (self.B), (self.A), (self.D), (self.C), (self.B2)], stroke='blue',
                             fill='none', stroke_width=2.5))
        # dwg.add(dwg.line((self.E),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
        # dwg.add(dwg.line((self.F),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(
            dwg.rect(insert=(self.E), size=(self.data_object.col_web_thk, self.data_object.col_length), fill='#E0E0E0',
                     stroke='blue', stroke_width=2.5))

        # Diagonal Hatching to represent WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 8), patternUnits="userSpaceOnUse",
                                           patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(
            dwg.rect(insert=(self.P), size=(12, self.data_object.plate_ht), fill="url(#diagonalHatch)", stroke='white',
                     stroke_width=2.0))

        dwg.add(dwg.rect(insert=(self.P), size=(self.data_object.plate_width, self.data_object.plate_ht), fill='none',
                         stroke='blue', stroke_width=2.5))

        # C1,A1,A3,B3,B1,C2
        dwg.add(dwg.polyline(points=[(self.C1), (self.A1), (self.A3), (self.B3), (self.ptB1), (self.C2)], stroke='blue',
                             fill='none', stroke_width=2.5))
        # C1,C2
        dwg.add(dwg.line((self.C1), (self.C2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        # A2,B2
        dwg.add(dwg.line((self.A2), (self.B2)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.A5), (self.A4)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.B5), (self.B4)).stroke('blue', width=2.5, linecap='square'))
        nr = self.data_object.no_of_rows
        nc = self.data_object.no_of_col
        bolt_r = self.data_object.bolt_dia / 2
        ptList = []

        for i in range(1, (nr + 1)):
            colList = []
            for j in range(1, (nc + 1)):
                pt = self.ptP + self.data_object.plateEdge_dist * np.array(
                    [1, 0]) + self.data_object.end_dist * np.array(
                    [0, 1]) + \
                     (i - 1) * self.data_object.pitch * np.array([0, 1]) + (j - 1) * self.data_object.gauge * np.array(
                    [1, 0])
                dwg.add(dwg.circle(center=(pt), r=bolt_r, stroke='blue', fill='none', stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1, 0])
                PtD = pt + (bolt_r + 4) * np.array([1, 0])
                dwg.add(dwg.line((ptC), (PtD)).stroke('red', width=2.0, linecap='square'))
                ptE = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0]) + (
                                                                                          j - 1) * self.data_object.gauge * np.array(
                    [1, 0])
                ptF = ptE + self.data_object.plate_ht * np.array([0, 1])
                dwg.add(dwg.line((ptE), (ptF)).stroke('blue', width=1.5, linecap='square').dasharray(
                    dasharray=([20, 5, 1, 5])))
                colList.append(pt)
            ptList.append(colList)

        pitchPts = []
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        txtOffset = (
                    self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plateEdge_dist + 80
        params = {"offset": (
                            self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plateEdge_dist + 80,
                  "textoffset": txtOffset, "lineori": "right", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len(pitchPts) - 1]),
                                                    str(len(pitchPts) - 1) + u' \u0040' + str(
                                                        int(self.data_object.pitch)) + " mm c/c", params)

        # End Distance from the starting point of plate Information
        edgPtx = (self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plateEdge_dist
        edgPty = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        edgPt = (edgPtx, edgPty)
        params = {"offset": (
                            self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plateEdge_dist + 80,
                  "textoffset": 120, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[0]), np.array([edgPtx, edgPty]),
                                                    str(int(self.data_object.end_dist)) + " mm", params)

        # Distance between Beam Flange and Plate
        offset = (self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap + 50
        params = {"offset": (self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap + 80,
                  "textoffset": 125, "lineori": "right", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, self.A1, self.C1, str(
            int(self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)) + " mm", params)

        # Draw Faint line for dimensions
        ptOne = self.P
        ptTwox = -60
        ptTwoy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3)
        ptTwo = (ptTwox, ptTwoy)
        self.data_object.draw_faint_line(ptOne, ptTwo, dwg)

        pt1 = np.array(pitchPts[0])
        ptTwox = -60
        ptTwoy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.end_dist
        pt2 = (ptTwox, ptTwoy)
        self.data_object.draw_faint_line(pt1, pt2, dwg)

        ptA = np.array(pitchPts[len(pitchPts) - 1])
        ptBx = -60
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + (
               self.data_object.plate_ht - self.data_object.end_dist)
        ptB = (ptBx, ptBy)
        self.data_object.draw_faint_line(ptA, ptB, dwg)

        ptOne = self.U
        ptBx = -60
        ptBy = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.plate_ht
        ptTwo = (ptBx, ptBy)
        self.data_object.draw_faint_line(ptOne, ptTwo, dwg)

        # End Distance from plate end point.
        edgPt1x = edgPtx
        edgPt1y = edgPty + self.data_object.plate_ht
        edgPt1 = (edgPt1x, edgPt1y)
        params = {"offset": (
                            self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plateEdge_dist + 80,
                  "textoffset": 120, "lineori": "right", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[len(pitchPts) - 1]),
                                                    np.array([edgPt1x, edgPt1y]),
                                                    str(int(self.data_object.end_dist)) + " mm", params)

        # Gap Distance
        # Draw Faint Lines to representation of Gap distance #
        dist1 = self.data_object.col_length - (
            (self.data_object.col_length - self.data_object.beam_depth) / 2 + self.data_object.beam_depth)
        ptA = self.ptB1
        ptB = self.ptB1 + (dist1 + 100) * np.array([0, 1])
        self.data_object.draw_faint_line(ptA, ptB, dwg)
        ptC = self.G
        ptD = ptC + (100) * np.array([0, 1])
        self.data_object.draw_faint_line(ptC, ptD, dwg)
        ptG1 = self.ptB1 + (dist1 + 50) * np.array([0, 1])
        ptG2 = self.ptB1 + self.data_object.gap * np.array([-1, 0]) + (dist1 + 50) * np.array([0, 1])
        offset = 1
        params = {"offset": offset, "textoffset": 120, "lineori": "right", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.data_object.gap) + " mm", params)

        # Gauge Distance Information
        gaugePts = ptList[0]
        for i in range(len(gaugePts) - 1):
            offset_dist = -(
                self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3 + dist1 + 100)
            params = {"offset": offset_dist, "textoffset": 35, "lineori": "right", "endlinedim": 10}
            ptP = np.array(gaugePts[i])
            ptQ = np.array(gaugePts[i + 1])
            self.data_object.draw_dimension_outer_arrow(dwg, ptP, ptQ, str(int(self.data_object.gauge)) + " mm", params)

        if len(ptList[(len(ptList) - 1)]) > 1:
            ptA = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0])
            ptB = ptA + (
                            self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3 + dist1 + 50) * np.array(
                [0, -1])
            self.data_object.draw_faint_line(ptA, ptB, dwg)

            ptC = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0]) + self.data_object.gauge * np.array(
                [1, 0])
            ptD = ptC + (
                            self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3 + dist1 + 50) * np.array(
                [0, -1])
            # self.data_object.draw_faint_line(ptC, ptD, dwg)

        # Edge Distance Information
        ptA = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0]) + (
                                                                                  self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
            [1, 0])
        ptB = ptA + self.data_object.edge_dist * np.array([1, 0])
        offsetDist = -(
        self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3 + dist1 + 120)
        params = {"offset": offsetDist, "textoffset": 35, "lineori": "right", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, ptA, ptB, str(int(self.data_object.edge_dist)) + " mm", params)
        # Draw Faint line for Edge distance
        ptC = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0]) + (
                                                                                  self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
            [1, 0])
        ptD = ptC + (
                        self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3 + dist1 + 100) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptC, ptD, dwg)
        ptE = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0]) + (
                                                                                  self.data_object.no_of_col - 1) * self.data_object.gauge * np.array(
            [1, 0]) + self.data_object.edge_dist * np.array([1, 0])
        ptF = ptE + (
                        self.data_object.end_dist + self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3 + dist1 + 100) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptE, ptF, dwg)

        # Plate Width Information
        pltPtx = (self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.plate_width / 2
        pltPty = ((self.data_object.col_length - self.data_object.beam_depth) / 2) + (
            self.data_object.beam_flange_thk + self.data_object.beam_R1 + 3) + self.data_object.plate_ht
        pltPt = np.array([pltPtx, pltPty])
        theta = 45
        offset = (self.data_object.beam_depth) / 2
        textUp = "PLT. " + str(int(self.data_object.plate_ht)) + "X" + str(
            int(self.data_object.plate_width)) + "X" + str(
            int(self.data_object.plate_thick))
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, pltPt, theta, "SE", offset, textUp, textDown, element)

        # Column Designation

        pt = self.D + 20 * np.array([0, -1])
        theta = 1
        offset = 1
        textUp = "Column " + self.data_object.col_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, pt, theta, "NW", offset, textUp, textDown, element)

        # Bolt Information
        bltPtx = self.ptP + self.data_object.plateEdge_dist * np.array([1, 0]) + self.data_object.end_dist * np.array(
            [0, 1]) + (self.data_object.no_of_col - 1) * self.data_object.gauge * np.array([1, 0])
        theta = 45
        offset = (self.data_object.beam_depth * 3) / 8
        textUp = str(self.data_object.no_of_rows) + " nos " + str(self.data_object.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M " + str(self.data_object.bolt_dia) + " bolts (grade " + str(self.data_object.grade) + ")"
        element = ""
        self.data_object.draw_oriented_arrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element)

        # Beam Information
        beam_pt = self.ptB1 + (self.data_object.beam_length) * np.array(
            [1, 0]) + self.data_object.beam_depth / 2 * np.array(
            [0, -1])
        theta = 1
        offset = 0.0
        textUp = "Beam " + self.data_object.beam_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element)

        # Weld Information
        weldPt = self.ptP + 6 * np.array([1, 0]) + self.data_object.end_dist / 2 * np.array([0, 1])
        theta = 45
        offset = self.data_object.col_width
        textUp = "          z " + str(self.data_object.weld_thick) + " mm"
        textDown = ""
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, weldPt, theta, "NW", offset, textUp, textDown, element)

        # 2D view name
        ptx = self.H + (self.data_object.col_length / 3.5) * np.array([0, 1]) + 30 * np.array([-1, 0])
        dwg.add(dwg.text('Front view (Sec C-C)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"########### Column Web Beam Flange Saved ############"


class Seat2DCreatorTop(object):
    def __init__(self, seat_common_object):

        self.data_object = seat_common_object
        # =======================================================================
        #          COLUMN WEB BEAM FLANGE CONNECTIVITY (TOP VIEW)
        # =======================================================================
        self.A = np.array([0, 0])
        self.B = np.array([0, 0]) + (self.data_object.col_width) * np.array([1, 0])
        self.C = self.B + (self.data_object.col_flange_thk) * np.array([0, 1])
        self.D = self.A + (self.data_object.col_width + self.data_object.col_web_thk) / 2 * np.array([1, 0]) + (
                                                                                                           self.data_object.col_flange_thk) * np.array(
            [0, 1])
        self.E = self.A + (self.data_object.col_width + self.data_object.col_web_thk) / 2 * np.array([1, 0]) + (
                                                                                                                   self.data_object.col_depth - self.data_object.col_flange_thk) * np.array(
            [0, 1])
        self.F = self.B + (self.data_object.col_depth - self.data_object.col_flange_thk) * np.array([0, 1])
        self.G = self.B + (self.data_object.col_depth) * np.array([0, 1])
        self.H = self.A + (self.data_object.col_depth) * np.array([0, 1])
        self.I = self.A + (self.data_object.col_depth - self.data_object.col_flange_thk) * np.array([0, 1])
        self.J = self.E - (self.data_object.col_web_thk) * np.array([1, 0])
        self.K = self.D - (self.data_object.col_web_thk) * np.array([1, 0])
        self.L = self.A + (self.data_object.col_flange_thk) * np.array([0, 1])
        self.A1 = self.A + ((self.data_object.col_width + self.data_object.col_web_thk) / 2 + self.data_object.gap) * np.array(
            [1, 0]) + ((self.data_object.col_flange_thk) + (10)) * np.array([0, 1])
        self.A4 = self.A1 + self.data_object.beam_width * np.array([0, 1])
        self.A7 = self.A1 + (self.data_object.beam_width - self.data_object.beam_web_thk) / 2 * np.array([0, 1])
        self.A5 = self.A7 - 20 * np.array([1, 0])
        self.A8 = self.A7 + (self.data_object.beam_length) * np.array([1, 0])
        self.P1 = self.A1 + (self.data_object.beam_width + self.data_object.beam_web_thk) / 2 * np.array([0, 1])
        self.A6 = self.P1 + (self.data_object.beam_length) * np.array([1, 0])
        self.P = self.P1 - 20 * np.array([1, 0])
        self.P2 = self.P + (self.data_object.plate_width) * np.array([1, 0])
        self.P4 = self.P1 + (self.data_object.plate_thick) * np.array([0, 1])
        self.P3 = self.P2 + (self.data_object.plate_thick) * np.array([0, 1])

        # Weld Triangle

        self.ptP = self.P + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.O = self.P + self.data_object.weld_thick * np.array([1, 0])
        self.ptO = self.O + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.R = self.P + self.data_object.weld_thick * np.array([0, -1])
        self.ptR = self.R + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])

        self.X = self.P + (self.data_object.plate_thick) * np.array([0, 1])
        self.ptX = self.X + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.Y = self.X + (self.data_object.weld_thick) * np.array([0, 1])
        self.ptY = self.Y + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.Z = self.X + (self.data_object.weld_thick) * np.array([1, 0])
        self.ptZ = self.Z + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])

        # =======================================================================
        #            COLUMN FLANGE BEAM FLANGE CONNECTIVITY (TOP VIEW)
        # =======================================================================
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.data_object.col_flange_thk * np.array([1, 0])
        self.FC = self.FB + (self.data_object.col_width - self.data_object.col_web_thk) / 2 * np.array([0, 1])
        self.FD = self.FC + (self.data_object.col_depth - 2 * (self.data_object.col_flange_thk)) * np.array([1, 0])
        self.FE = self.A + (self.data_object.col_depth - self.data_object.col_flange_thk) * np.array([1, 0])
        self.FF = self.FA + self.data_object.col_depth * np.array([1, 0])
        self.FG = self.FF + self.data_object.col_width * np.array([0, 1])
        self.FH = self.FG + self.data_object.col_flange_thk * np.array([-1, 0])
        self.FI = self.FD + self.data_object.col_web_thk * np.array([0, 1])
        self.FJ = self.FC + self.data_object.col_web_thk * np.array([0, 1])
        self.FK = self.FB + self.data_object.col_width * np.array([0, 1])
        self.FL = self.FK + self.data_object.col_flange_thk * np.array([-1, 0])
        self.FA7 = self.FD + (self.data_object.col_flange_thk + self.data_object.gap) * np.array([1, 0])
        self.FP1 = self.FA7 + self.data_object.beam_web_thk * np.array([0, 1])
        self.FP = self.FP1 + self.data_object.gap * np.array([-1, 0])
        self.FA1 = self.FA7 + (self.data_object.beam_width - self.data_object.beam_web_thk) / 2 * np.array([0, -1])
        self.FA2 = self.FA1 + self.data_object.beam_length * np.array([1, 0])
        self.FA3 = self.FA2 + self.data_object.beam_width * np.array([0, 1])
        self.FA4 = self.FA1 + self.data_object.beam_width * np.array([0, 1])
        self.FX = self.FP + self.data_object.plate_thick * np.array([0, 1])
        self.FP2 = self.FP + self.data_object.plate_width * np.array([1, 0])
        self.FP3 = self.FP2 + self.data_object.plate_thick * np.array([0, 1])
        self.FP4 = self.FX + self.data_object.gap * np.array([1, 0])
        self.FA8 = self.FA7 + self.data_object.beam_length * np.array([1, 0])
        self.FA6 = self.FP1 + self.data_object.beam_length * np.array([1, 0])
        self.FP5 = self.FA7 + self.data_object.gap * np.array([-1, 0])
        # Weld Triangle

        self.ptFP = self.FP + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.FQ = self.FP + self.data_object.weld_thick * np.array([1, 0])
        self.ptFQ = self.FQ + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])
        self.FR = self.FP + self.data_object.weld_thick * np.array([0, -1])
        self.ptFR = self.FR + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, -1])

        self.FX = self.FP + (self.data_object.plate_thick) * np.array([0, 1])
        self.ptFX = self.FX + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.FY = self.FX + (self.data_object.weld_thick) * np.array([0, 1])
        self.ptFY = self.FY + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])
        self.FZ = self.FX + (self.data_object.weld_thick) * np.array([1, 0])
        self.ptFZ = self.FZ + 2.5 * np.array([1, 0]) + 2.5 * np.array([0, 1])

    def callCFBFTop(self, file_name):
        vb_width = str(int(self.data_object.col_depth) + 750)
        vb_ht = str(800)
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-50 -250 ' + vb_width + ' ' + vb_ht))

        ptSecA = self.FF + ((230 + self.data_object.gap + self.data_object.beam_length) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txtpt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.FG + ((230 + self.data_object.gap + self.data_object.beam_length) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txtpt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        #  C-C section
        ptSecA = self.FA4 + ((self.data_object.gap + self.data_object.col_depth) * np.array([-1, 0])) + 230 * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txtpt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.FA3 + (230 * np.array([0, 1])) + 100 * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txtpt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(
            points=[(self.FA), (self.FB), (self.FC), (self.FD), (self.FE), (self.FF), (self.FG), (self.FH), (self.FI),
                    (self.FJ), (self.FK), (self.FL), (self.FA)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FA1), size=(self.data_object.beam_length, self.data_object.beam_width), fill='none',
                         stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.FP), (self.FP1)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.FX), (self.FP4)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.FP1), (self.FP2), (self.FP3), (self.FP4)], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([5, 5])))
        dwg.add(
            dwg.line((self.FA7), (self.FA8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(
            dwg.line((self.FP1), (self.FA6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline([(self.ptFP), (self.ptFQ), (self.ptFR), (self.ptFP)], fill='black', stroke_width=2.5,
                             stroke='black'))
        dwg.add(dwg.polyline([(self.ptFX), (self.ptFY), (self.ptFZ), (self.ptFX)], fill='black', stroke_width=2.5,
                             stroke='black'))

        nc = self.data_object.no_of_col
        bolt_r = self.data_object.bolt_dia / 2
        ptList = []
        if nc >= 1:
            for col in range(nc):
                pt = self.FP5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (col) * self.data_object.gauge * np.array(
                    [1, 0])
                pt1 = pt - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_ht = self.data_object.beam_web_thk + self.data_object.plate_thick
                dwg.add(
                    dwg.rect(insert=(pt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0, -1])
                B2 = pt + (rect_ht + 10) * np.array([0, 1])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                ptList.append(pt)
                dimOffset = self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 150
                # Draw Faint line between edge and gauge distance
                ptA = B1 + (dimOffset) * np.array([0, -1])
                self.data_object.draw_faint_line(B1, ptA, dwg)

                if len(ptList) > 1:
                    params = {"offset": dimOffset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
                    self.data_object.draw_dimension_outer_arrow(dwg, np.array(ptList[0]), np.array(ptList[1]),
                                                                str(int(self.data_object.gauge)) + " mm", params)

        # Draw Faint line to represent edge distance
        ptB = self.FP5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (col) * self.data_object.gauge * np.array(
            [1, 0]) + self.data_object.edge_dist * np.array([1, 0])
        ptC = ptB + (self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 90) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptB, ptC, dwg)

        ptx = self.FP5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (col) * self.data_object.gauge * np.array([1, 0])
        ptY = ptx + self.data_object.edge_dist * np.array([1, 0])
        offset = self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 100
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx, ptY, str(int(self.data_object.edge_dist)) + " mm", params)

        # Beam Information
        beam_pt = self.FA1 + (self.data_object.beam_length / 2) * np.array([1, 0])
        theta = 55
        offset = 80
        textUp = "Beam " + self.data_object.beam_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown, element)

        # Column Information

        ptSecA = self.FJ + ((self.data_object.col_depth / 2.5) * np.array([1, 0]))
        ptSecB = ptSecA + (120 * np.array([0, 1]))
        txtpt = ptSecB + (120 * np.array([-1, 0])) + (30 * np.array([0, 1]))
        line = dwg.add(dwg.line((ptSecA), (ptSecB)).stroke('black', width=2.5, linecap='square'))
        start_arrow = self.data_object.add_end_marker(dwg)
        self.data_object.draw_start_arrow(line, start_arrow)
        text = "Column " + self.data_object.col_designation
        dwg.add(dwg.text(text, insert=(txtpt), fill='black', font_family="sans-serif", font_size=28))

        # Plate  Information
        plt_pt = self.FP3
        theta = 60
        offset = self.data_object.beam_width / 2 + 50
        textUp = "PLT. " + str(int(self.data_object.plate_ht)) + 'x' + str(int(self.data_object.plate_width)) + 'x' + str(
            int(self.data_object.plate_thick))
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown, element)

        # Bolt Information
        bltPt = self.FP5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (nc - 1) * self.data_object.gauge * np.array(
            [1, 0])
        theta = 55
        offset = (self.data_object.beam_width) + 130
        textUp = str(self.data_object.no_of_rows) + " nos " + str(self.data_object.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.data_object.bolt_dia) + " bolts (grade " + str(self.data_object.grade) + ")"
        element = ""
        self.data_object.draw_oriented_arrow(dwg, bltPt, theta, "NE", offset, textUp, textDown, element)

        # Weld Information
        weldPt = self.FY
        theta = 60
        offset = self.data_object.weld_thick + self.data_object.plate_thick + self.data_object.beam_width / 2 + 80
        textUp = "          z " + str(int(self.data_object.weld_thick)) + " mm"
        textDown = ""  # u"\u25C1"
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, weldPt, theta, "SE", offset, textUp, textDown, element)

        # Gap Informatoin
        ptG1 = self.FF + 50 * np.array([0, -1])
        ptG2 = ptG1 + 20 * np.array([1, 0])
        offset = 1
        params = {"offset": offset, "textoffset": 10, "lineori": "left", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.data_object.gap) + " mm", params)
        # Draw Faint Lines to representation of Gap distance #
        ptA = self.FF
        ptB = ptG1
        self.data_object.draw_faint_line(ptA, ptB, dwg)
        ptC = self.FA1
        ptD = ptG2
        self.data_object.draw_faint_line(ptC, ptD, dwg)

        # 2D view name
        ptx = self.FG + 270 * np.array([0, 1])
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()
        print"$$$$$$$$$ Saved Column Flange Beam Flange Top $$$$$$$$$$$$"

    def callCWBFTop(self, file_name):
        vb_ht = str(float(self.data_object.col_depth) + 750)
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-50 -300 850 ' + vb_ht))

        dwg.add(dwg.polyline(
            points=[(self.A), (self.B), (self.C), (self.D), (self.E), (self.F), (self.G), (self.H), (self.I), (self.J),
                    (self.K), (self.L), (self.A)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A1), size=(self.data_object.beam_length, self.data_object.beam_width), fill='none',
                         stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.A7), (self.A8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.P1), (self.A6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.P), (self.P1)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.X), (self.P4)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.P1), (self.P2), (self.P3), (self.P4)], stroke='red', fill='none',
                             stroke_width=2.5).dasharray(dasharray=([5, 5])))
        dwg.add(dwg.polyline([(self.ptP), (self.ptO), (self.ptR), (self.ptP)], fill='black', stroke_width=2.5,
                             stroke='black'))
        dwg.add(dwg.polyline([(self.ptX), (self.ptY), (self.ptZ), (self.ptX)], fill='black', stroke_width=2.5,
                             stroke='black'))

        nc = self.data_object.no_of_col
        bolt_r = self.data_object.bolt_dia / 2
        ptList = []
        if nc >= 1:
            for col in range(nc):
                pt = self.A5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (col) * self.data_object.gauge * np.array(
                    [1, 0])

                pt1 = pt - bolt_r * np.array([1, 0])
                rect_width = self.data_object.bolt_dia
                rect_ht = self.data_object.beam_web_thk + self.data_object.plate_thick
                dwg.add(
                    dwg.rect(insert=(pt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0, -1])
                B2 = pt + (rect_ht + 10) * np.array([0, 1])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))
                ptList.append(pt)
                if len(ptList) > 1:
                    dimOffset = self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 50
                    params = {"offset": dimOffset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
                    self.data_object.draw_dimension_outer_arrow(dwg, np.array(ptList[0]), np.array(ptList[1]),
                                                                str(int(self.data_object.gauge)) + "mm", params)

        # Cross section B-B and C-C
        ptSecA = self.B + (20 * np.array([0, -1])) + (500 * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txtpt = ptSecB + (70 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.G + (20 * np.array([0, 1])) + (500 * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txtpt = ptSecD + (70 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ptSecA = self.I + (07 * np.array([0, -1])) + (0 * np.array([-1, 0]))
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txtpt = ptSecB + (50 * np.array([0, -1])) + (15 * np.array([-1, 0]))
        txt = "C"
        self.data_object.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (530 * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txtpt = ptSecD + (50 * np.array([0, -1])) + (25 * np.array([-1, 0]))
        self.data_object.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        # Draw Faint line to represent edge distance
        ptB = self.A5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (nc - 1) * self.data_object.gauge * np.array(
            [1, 0]) + self.data_object.edge_dist * np.array([1, 0])
        ptC = ptB + (self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 150) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptB, ptC, dwg)
        ptL = self.A5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (nc - 1) * self.data_object.gauge * np.array(
            [1, 0])
        ptM = ptL + (self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 150) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptL, ptM, dwg)

        # Edge Distance
        ptx = self.A5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (nc - 1) * self.data_object.gauge * np.array(
            [1, 0])
        ptY = ptx + self.data_object.edge_dist * np.array([1, 0])
        offset = self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 150
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, ptx, ptY, str(int(self.data_object.edge_dist)) + " mm", params)

        #  Draws Faint line to represent Gauge Distance
        ptK = self.A5 + self.data_object.plateEdge_dist * np.array([1, 0])
        ptM = ptK + (self.data_object.beam_width / 2 + self.data_object.col_flange_thk + self.data_object.col_R1 + 50) * np.array(
            [0, -1])
        self.data_object.draw_faint_line(ptK, ptM, dwg)

        # Beam Information
        beam_pt = self.A1 + self.data_object.beam_length / 2 * np.array([1, 0])
        theta = 60
        offset = 100
        textUp = "Beam " + self.data_object.beam_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown, element)

        # column  Information
        col_pt = self.H
        theta = 70
        offset = 270
        textUp = "Column " + self.data_object.col_designation
        textDown = " "
        element = ""
        self.data_object.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, textUp, textDown, element)

        # Plate  Information
        plt_pt = self.P3
        theta = 70
        offset = self.data_object.beam_width / 2 + 130
        textUp = "PLT. " + str(int(self.data_object.plate_ht)) + 'x' + str(int(self.data_object.plate_width)) + 'x' + str(
            int(self.data_object.plate_thick))
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown, element)

        # Bolt Information
        bltPt = self.A5 + self.data_object.plateEdge_dist * np.array([1, 0]) + (nc - 1) * self.data_object.gauge * np.array(
            [1, 0])
        theta = 60
        offset = (self.data_object.beam_width) + 160
        textUp = str(self.data_object.no_of_rows) + " nos " + str(self.data_object.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.data_object.bolt_dia) + " bolts (grade " + str(self.data_object.grade) + ")"
        element = ""
        self.data_object.draw_oriented_arrow(dwg, bltPt, theta, "NE", offset, textUp, textDown, element)

        # Weld Information
        weldPt = self.Y
        theta = 70
        offset = self.data_object.col_depth * 3 / 4 + 100
        textUp = "          z " + str(int(self.data_object.weld_thick)) + " mm"
        textDown = ""  # u"\u25C1"
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, weldPt, theta, "SE", offset, textUp, textDown, element)

        # Gap Informatoin
        ptG1 = self.D + 250 * np.array([0, -1])
        ptG2 = ptG1 + self.data_object.gap * np.array([1, 0])
        offset = 100
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim": 10, "arrowlen": 50}
        self.data_object.draw_dimension_inner_arrow(dwg, ptG1, ptG2, str(self.data_object.gap) + " mm", params)
        # Draw Faint Lines to representation of Gap distance #
        ptA = self.D
        ptB = ptA + (285) * np.array([0, -1])
        self.data_object.draw_faint_line(ptA, ptB, dwg)
        ptC = self.A1
        ptD = ptC + (300) * np.array([0, -1])
        self.data_object.draw_faint_line(ptC, ptD, dwg)

        # 2D view name
        ptx = self.G + (30) * np.array([1, 0]) + (400) * np.array([0, 1])
        dwg.add(dwg.text('Top view (Sec A-A)', insert=(ptx), fill='black', font_family="sans-serif", font_size=32))

        dwg.save()
        print"$$$$$$$$$ Saved Column Web Beam Flange Top $$$$$$$$$$$"


class Seat2DCreatorSide(object):
    def __init__(self, seat_common_object):

        self.data_object = seat_common_object
        # =======================================================================
        # # COLUMN WEB BEAM FLANGE Side Connectivity Points
        # =======================================================================
        self.A = np.array([0, 0])
        self.B = self.A + self.data_object.col_flange_thk * np.array([1, 0])
        self.E = self.B + self.data_object.col_length * np.array([0, 1])
        self.C = self.A + (self.data_object.col_depth - self.data_object.col_flange_thk) * np.array([1, 0])
        self.D = self.A + self.data_object.col_depth * np.array([1, 0])
        self.H = self.C + self.data_object.col_length * np.array([0, 1])
        self.G = self.B + self.data_object.col_length * np.array([0, 1])
        self.A1 = (self.data_object.col_flange_thk + self.data_object.col_R1) * np.array((1, 0)) + ((
                                                                                                        self.data_object.col_length - self.data_object.beam_depth) / 2) * np.array(
            [0, 1])
        self.A2 = self.A1 + self.data_object.beam_width * np.array([1, 0])
        self.A3 = self.A2 + self.data_object.beam_flange_thk * np.array([0, 1])
        self.A12 = self.A1 + self.data_object.beam_flange_thk * np.array([0, 1])
        self.A11 = self.A12 + (self.data_object.beam_width - self.data_object.beam_web_thk) / 2 * np.array([1, 0])
        self.A4 = self.A11 + self.data_object.beam_web_thk * np.array([1, 0])
        self.A5 = self.A4 + (self.data_object.beam_depth - (2 * self.data_object.beam_flange_thk)) * np.array([0, 1])
        self.A6 = self.A2 + (self.data_object.beam_depth - self.data_object.beam_flange_thk) * np.array([0, 1])
        self.A7 = self.A2 + self.data_object.beam_depth * np.array([0, 1])
        self.A8 = self.A1 + self.data_object.beam_depth * np.array([0, 1])
        self.A9 = self.A1 + (self.data_object.beam_depth - self.data_object.beam_flange_thk) * np.array([0, 1])
        self.A10 = self.A11 + (self.data_object.beam_depth - (2 * self.data_object.beam_flange_thk)) * np.array([0, 1])
        self.P = self.A11 + (self.data_object.beam_R1 + 3) * np.array([0, 1])
        self.P1 = self.P + (self.data_object.end_dist) * np.array([0, 1])
        self.Q = self.P + self.data_object.plate_thick * np.array([-1, 0])
        # Hashing for weld is 8mm so self.X shfited in 8mm distance in -X axis direction
        self.X = self.Q + 8 * np.array([-1, 0])
        self.R = self.P + self.data_object.plate_ht * np.array([0, 1])
        self.Y = self.R + (self.data_object.plate_thick + self.data_object.weld_thick) * np.array([-1, 0])

        # =======================================================================
        # COLUMN FLANGE BEAM FLANGE Side Connectivity Points
        # =======================================================================
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.data_object.col_width * np.array([1, 0])
        self.ptMid = self.FA + ((self.data_object.col_width / 2) + (self.data_object.col_web_thk / 2)) * np.array([1, 0])
        self.ptMid1 = self.ptMid + ((self.data_object.col_length - self.data_object.beam_depth) / 2) * np.array([0, 1])
        self.FC = self.FB + self.data_object.col_length * np.array([0, 1])
        self.FD = self.FA + self.data_object.col_length * np.array([0, 1])
        self.FA1 = self.ptMid1 + (self.data_object.beam_web_thk / 2) * np.array(
            [-1, 0]) + self.data_object.beam_width / 2 * np.array([-1, 0])
        self.FA2 = self.FA1 + self.data_object.beam_width * np.array([1, 0])
        self.FA3 = self.FA2 + self.data_object.beam_flange_thk * np.array([0, 1])
        self.FA12 = self.FA1 + self.data_object.beam_flange_thk * np.array([0, 1])
        self.FA11 = self.FA12 + (self.data_object.beam_width - self.data_object.beam_web_thk) / 2 * np.array([1, 0])
        self.FA4 = self.FA11 + self.data_object.beam_web_thk * np.array([1, 0])
        self.FA5 = self.FA4 + (self.data_object.beam_depth - (2 * self.data_object.beam_flange_thk)) * np.array([0, 1])
        self.FA6 = self.FA2 + (self.data_object.beam_depth - self.data_object.beam_flange_thk) * np.array([0, 1])
        self.FA7 = self.FA2 + self.data_object.beam_depth * np.array([0, 1])
        self.FA8 = self.FA1 + self.data_object.beam_depth * np.array([0, 1])
        self.FA9 = self.FA1 + (self.data_object.beam_depth - self.data_object.beam_flange_thk) * np.array([0, 1])
        self.FA10 = self.FA11 + (self.data_object.beam_depth - (2 * self.data_object.beam_flange_thk)) * np.array([0, 1])
        self.FP = self.FA11 + (self.data_object.beam_R1 + 3) * np.array([0, 1])
        self.FP = self.FA4 + (self.data_object.beam_R1 + 3) * np.array([0, 1])
        self.FP1 = self.FP + (self.data_object.end_dist) * np.array([0, 1])
        self.FQ = self.FP + self.data_object.plate_thick * np.array([-1, 0])
        self.FX = self.FQ + 8 * np.array([-1, 0])
        self.FR = self.FP + self.data_object.plate_ht * np.array([0, 1])
        self.FY = self.FX + self.data_object.plate_ht * np.array([0, 1])

    def callCWBFSide(self, file_name):
        vb_width = str(float(3.5 * self.data_object.col_depth))
        vb_ht = str(float(1.4 * self.data_object.col_length))

        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-10 -100 ' + vb_width + ' ' + vb_ht))
        dwg.add(dwg.rect(insert=(self.A), size=(self.data_object.col_depth, self.data_object.col_length), fill='none',
                         stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.C), (self.H)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.B), (self.G)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.polyline(
            points=[(self.A1), (self.A2), (self.A3), (self.A4), (self.A5), (self.A6), (self.A7), (self.A8), (self.A9),
                    (self.A10), (self.A11), (self.A12), (self.A1)], stroke='blue', fill='#E0E0E0', stroke_width=2.5))

        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 8), patternUnits="userSpaceOnUse",
                                           patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.X), size=(8, self.data_object.plate_ht), fill="url(#diagonalHatch)", stroke='white',
                         stroke_width=1.0))

        dwg.add(dwg.rect(insert=(self.Q), size=(self.data_object.plate_thick, self.data_object.plate_ht), fill='none',
                         stroke='blue', stroke_width=2.5))

        nr = self.data_object.no_of_rows
        pitchPts = []
        for row in range(nr):
            pt = self.P + self.data_object.end_dist * np.array([0, 1]) + (row) * self.data_object.pitch * np.array([0, 1])
            ptOne = pt + 20 * np.array([1, 0])
            ptTwo = pt + 30 * np.array([-1, 0])
            dwg.add(dwg.circle(center=(pt), r=1.5, stroke='red', fill='none', stroke_width=1.5))
            dwg.add(dwg.line((ptOne), (ptTwo)).stroke('red', width=1.5, linecap='square').dasharray(
                dasharray=([10, 5, 1, 5])))
            bltPt1 = pt + self.data_object.bolt_dia / 2 * np.array([0, -1]) + self.data_object.plate_thick * np.array([-1, 0])
            bltPt2 = pt + self.data_object.bolt_dia / 2 * np.array([0, -1]) + self.data_object.beam_web_thk * np.array([1, 0])
            rect_width = self.data_object.bolt_dia
            rect_ht = self.data_object.beam_web_thk + self.data_object.plate_thick
            dwg.add(
                dwg.rect(insert=(bltPt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))
            bltPt3 = pt + self.data_object.bolt_dia / 2 * np.array([0, 1]) + self.data_object.plate_thick * np.array([-1, 0])
            bltPt4 = pt + self.data_object.bolt_dia / 2 * np.array([0, 1]) + self.data_object.beam_web_thk * np.array([1, 0])
            dwg.add(dwg.line((bltPt1), (bltPt2)).stroke('black', width=1.5, linecap='square'))
            dwg.add(dwg.line((bltPt3), (bltPt4)).stroke('black', width=1.5, linecap='square'))
            pitchPts.append(pt)

        # End and Pitch Distance Information
        params = {"offset": self.data_object.col_depth / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len(pitchPts) - 1]),
                                                    str(len(pitchPts) - 1) + u' \u0040' + str(
                                                    int(self.data_object.pitch)) + " mm c/c", params)
        params = {"offset": self.data_object.col_depth / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, self.P, np.array(pitchPts[0]),
                                                    str(int(self.data_object.end_dist)) + " mm ", params)
        params = {"offset": self.data_object.col_depth / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[len(pitchPts) - 1]), self.R,
                                                    str(int(self.data_object.end_dist)) + " mm", params)

        # Draw Faint Line
        pt2 = self.P + ((self.data_object.col_depth / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(self.P, pt2, dwg)
        pt1 = np.array(pitchPts[0]) + ((self.data_object.col_depth / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(np.array(pitchPts[0]), pt1, dwg)
        ptA = self.R + ((self.data_object.col_depth / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(self.R, ptA, dwg)
        ptB = np.array(pitchPts[len(pitchPts) - 1]) + ((self.data_object.col_depth / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(np.array(pitchPts[len(pitchPts) - 1]), ptB, dwg)

        # Column Information
        beam_pt = self.G + self.data_object.beam_width / 2 * np.array([1, 0])
        theta = 30
        offset = 50
        textUp = "Column " + self.data_object.col_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element)

        # Beam  Information
        col_pt = self.A2 + self.data_object.beam_width / 2 * np.array([-1, 0])
        theta = 45
        offset = self.data_object.col_length / 4
        textUp = "Beam " + self.data_object.beam_designation
        textDown = " "
        element = ""
        self.data_object.draw_oriented_arrow(dwg, col_pt, theta, "NE", offset, textUp, textDown, element)

        # Plate  Information
        beam_pt = self.R + self.data_object.plate_thick / 2 * np.array([-1, 0])
        theta = 45
        offset = self.data_object.col_length / 4
        textUp = "PLT. " + str(int(self.data_object.plate_ht)) + 'x' + str(int(self.data_object.plate_width)) + 'x' + str(
            int(self.data_object.plate_thick))
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element)

        # Bolt Information
        boltPt = self.P1
        theta = 45
        offset = self.data_object.weld_thick + self.data_object.plate_thick + self.data_object.beam_width / 2 + 80
        textUp = str(self.data_object.no_of_rows) + " nos " + str(self.data_object.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M " + str(self.data_object.bolt_dia) + " bolts (grade " + str(self.data_object.grade) + ")"
        element = ""
        self.data_object.draw_oriented_arrow(dwg, boltPt, theta, "NE", offset, textUp, textDown, element)

        # Weld Information
        weldPt = np.array(pitchPts[len(pitchPts) - 1]) + self.data_object.pitch / 2 * np.array([0, -1]) + (
                                                                                                              self.data_object.plate_thick + 4) * np.array(
            [-1, 0])
        theta = 45
        offset = self.data_object.col_length / 5
        textUp = "          z " + str(int(self.data_object.weld_thick)) + " mm"
        textDown = ""  # u"\u25C1"
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, weldPt, theta, "SE", offset, textUp, textDown, element)

        # 2D view name
        ptx = self.H + (self.data_object.col_length / 5.5) * np.array([0, 1]) + 50 * np.array([-1, 0])
        dwg.add(dwg.text('Side view (Sec B-B)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "********* Column Web Beam Flange Side Saved ***********"

    def callCFBFSide(self, file_name):
        vb_width = str(float(3.5 * self.data_object.col_depth))
        vb_ht = str(float(1.4 * self.data_object.col_length))
        dwg = svgwrite.Drawing(file_name, size=('100%', '100%'), viewBox=('-10 -100 ' + vb_width + ' ' + vb_ht))
        dwg.add(dwg.rect(insert=(self.FA), size=(self.data_object.col_width, self.data_object.col_length), fill='none',
                         stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(
            points=[(self.FA1), (self.FA2), (self.FA3), (self.FA4), (self.FA5), (self.FA6), (self.FA7), (self.FA8),
                    (self.FA9), (self.FA10), (self.FA11), (self.FA12), (self.FA1)], stroke='blue', fill='#E0E0E0',
            stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FQ), size=(self.data_object.plate_thick, self.data_object.plate_ht), fill='none',
                         stroke='blue',
                         stroke_width=2.5))  # dwg.add(dwg.line((self.ptMid),(self.ptMid1)).stroke('green',width = 2.5,linecap = 'square'))
        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 8), patternUnits="userSpaceOnUse",
                                           patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=2.5))
        # 12 mm thickness is provided for weld to get clear visibility of weld hashed lines
        dwg.add(dwg.rect(insert=(self.FX), size=(8, self.data_object.plate_ht), fill="url(#diagonalHatch)", stroke='white',
                         stroke_width=1.0))

        nr = self.data_object.no_of_rows
        pitchPts = []
        for row in range(nr):
            pt = self.FP + self.data_object.end_dist * np.array([0, 1]) + (row) * self.data_object.pitch * np.array([0, 1])
            ptOne = pt + 20 * np.array([1, 0])
            ptTwo = pt + 30 * np.array([-1, 0])
            dwg.add(dwg.line((ptOne), (ptTwo)).stroke('red', width=1.5, linecap='square').dasharray(
                dasharray=([10, 5, 1, 5])))
            bltPt1 = pt + self.data_object.bolt_dia / 2 * np.array([0, -1]) + self.data_object.plate_thick * np.array([-1, 0])
            bltPt2 = pt + self.data_object.bolt_dia / 2 * np.array([0, -1]) + self.data_object.beam_web_thk * np.array([1, 0])

            bltPt2 = pt + self.data_object.bolt_dia / 2 * np.array([0, -1]) + self.data_object.beam_web_thk * np.array([1, 0])
            rect_width = self.data_object.bolt_dia
            rect_ht = self.data_object.beam_web_thk + self.data_object.plate_thick
            dwg.add(
                dwg.rect(insert=(bltPt1), size=(rect_width, rect_ht), fill='black', stroke='black', stroke_width=2.5))

            bltPt3 = pt + self.data_object.bolt_dia / 2 * np.array([0, 1]) + self.data_object.plate_thick * np.array([-1, 0])
            bltPt4 = pt + self.data_object.bolt_dia / 2 * np.array([0, 1]) + self.data_object.beam_web_thk * np.array([1, 0])
            dwg.add(dwg.line((bltPt1), (bltPt2)).stroke('black', width=1.5, linecap='square'))
            dwg.add(dwg.line((bltPt3), (bltPt4)).stroke('black', width=1.5, linecap='square'))
            pitchPts.append(pt)

        params = {"offset": self.data_object.col_width / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len(pitchPts) - 1]),
                                                    str(len(pitchPts) - 1) + u' \u0040' + str(
                                                    int(self.data_object.pitch)) + "mm c/c", params)
        params = {"offset": self.data_object.col_width / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, self.FP, np.array(pitchPts[0]),
                                                    str(int(self.data_object.end_dist)) + " mm ", params)
        params = {"offset": self.data_object.col_width / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim": 10}
        self.data_object.draw_dimension_outer_arrow(dwg, np.array(pitchPts[len(pitchPts) - 1]), self.FR,
                                                    str(int(self.data_object.end_dist)) + " mm", params)

        # Draw Faint Line
        pt2 = self.FP + ((self.data_object.col_width / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(self.FP, pt2, dwg)
        pt1 = np.array(pitchPts[0]) + ((self.data_object.col_width / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(np.array(pitchPts[0]), pt1, dwg)
        ptA = self.FR + ((self.data_object.col_width / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(self.FR, ptA, dwg)
        ptB = np.array(pitchPts[len(pitchPts) - 1]) + ((self.data_object.col_width / 2) + 15) * np.array([1, 0])
        self.data_object.draw_faint_line(np.array(pitchPts[len(pitchPts) - 1]), ptB, dwg)

        # Beam Information
        beam_pt = self.FA1 + self.data_object.beam_width / 2 * np.array([1, 0])
        theta = 45
        offset = self.data_object.col_length / 4
        textUp = "Beam " + self.data_object.beam_designation
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown, element)

        # column  Information
        col_pt = self.FC + self.data_object.col_width / 2 * np.array([-1, 0])
        theta = 30
        offset = 50
        textUp = "Column " + self.data_object.col_designation
        textDown = " "
        element = ""
        self.data_object.draw_oriented_arrow(dwg, col_pt, theta, "SE", offset, textUp, textDown, element)

        # Plate  Information
        beam_pt = self.FR + self.data_object.plate_thick / 2 * np.array([-1, 0])
        theta = 45
        offset = self.data_object.col_length / 4
        textUp = "PLT. " + str(int(self.data_object.plate_ht)) + 'x' + str(int(self.data_object.plate_width)) + 'x' + str(
            int(self.data_object.plate_thick))
        textDown = ""
        element = ""
        self.data_object.draw_oriented_arrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element)

        # Bolt Information
        boltPt = self.FP1
        theta = 45
        offset = (self.data_object.beam_depth * 3) / 8
        textUp = str(self.data_object.no_of_rows) + " nos " + str(self.data_object.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M " + str(self.data_object.bolt_dia) + " bolts (grade " + str(self.data_object.grade) + ")"
        element = ""
        self.data_object.draw_oriented_arrow(dwg, boltPt, theta, "NE", offset, textUp, textDown, element)

        # Weld Information
        weldPt = np.array(pitchPts[len(pitchPts) - 1]) + self.data_object.pitch / 2 * np.array([0, -1]) + (
                                                                                                              self.data_object.plate_thick + 4) * np.array(
            [-1, 0])
        theta = 45
        offset = self.data_object.col_length / 5
        textUp = "          z " + str(int(self.data_object.weld_thick)) + " mm"
        textDown = ""
        element = "weld"
        self.data_object.draw_oriented_arrow(dwg, weldPt, theta, "SE", offset, textUp, textDown, element)

        # 2D view name
        ptx = self.FC + (self.data_object.col_length / 5.5) * np.array([0, 1]) + 50 * np.array([-1, 0])
        dwg.add(dwg.text('Side view (Sec B-B)', insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        dwg.fit()
        dwg.save()

        print "********** Column Flange Beam Flange Side Saved  *************"