'''
Created on 24-Aug-2015

@author: deepa
'''
import svgwrite
import cmath
import math
from PyQt4.QtCore import QString
import numpy as np
from numpy import math
from model import *
from endPlateCalc import endConn
from cmath import sqrt
from xml.etree.ElementTree import XML, fromstring, tostring
import cairosvg


class EndCommonData(object):

    def __init__(self, inputObj, ouputObj, dictBeamdata, dictColumndata, folder):
        '''
        Provide all the data related to EndPlate connection

        :param inputObj:
        :type inputObj:dictionary(Input parameter dictionary)
        :param outputObj:
        :type ouputObj :dictionary (output parameter dictionary)
        :param dictBeamdata :
        :type dictBeamdata:  dictionary (Beam sectional properties)
        :param dictColumndata :
        :type dictBeamdata: dictionary (Column sectional properties dictionary)

        '''
        self.beam_T = float(dictBeamdata[QString("T")])
        self.col_T = float(dictColumndata[QString("T")])
        self.D_beam = int (dictBeamdata[QString("D")])
        self.D_col = int (dictColumndata[QString("D")])
        self.col_B = int(dictColumndata[QString("B")])
        self.beam_B = int(dictBeamdata[QString("B")])
        self.col_tw = float(dictColumndata[QString("tw")])
        self.beam_tw = float(dictBeamdata[QString("tw")])
        self.col_Designation = dictColumndata[QString("Designation")]
        self.beam_Designation = dictBeamdata[QString("Designation")]
        self.beam_R1 = float(dictBeamdata[QString("R1")])
        self.col_R1 = float(dictColumndata[QString("R1")])
        self.plate_ht = ouputObj['Plate']['Height']
        self.plate_thick = inputObj['Plate']["Thickness (mm)"]
        self.bolt_grade = inputObj['Bolt']['Grade']
        self.plate_width = ouputObj['Plate']['Width']
        self.weld_len = ouputObj['Weld']['weldlength']
        self.weld_thick = inputObj['Weld']['Size (mm)']
        self.bolt_dia = inputObj["Bolt"]["Diameter (mm)"]
        self.connectivity = inputObj['Member']['Connectivity']
        self.pitch = ouputObj['Bolt']["pitch"]
        self.gauge = ouputObj['Bolt']["gauge"]
        self.end_dist = ouputObj['Bolt']["enddist"]
        self.edge_dist = ouputObj['Bolt']["edge"]
        self.no_of_rows = ouputObj['Bolt']["numofrow"]
        self.no_of_col = ouputObj['Bolt']["numofcol"]
        self.sectional_gauge = ouputObj['Plate']['Sectional Gauge']
        self.col_L = 800
        self.beam_L = 350
        self.notch_L = (self.beam_B / 2 - self.beam_tw / 2) + 10
        self.notch_offset = (self.col_T + self.col_R1)

        self.folder = folder

    def addSMarker(self, dwg):
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

    def addSectionMarker(self, dwg):
        '''
        Draws start arrow to given line  -------->

        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)

        '''
        sectionMarker = dwg.marker(insert=(0, 5), size=(10, 10), orient="auto")
        sectionMarker.add(dwg.path(d="M 0 0 L 10 5 L 0 10 z", fill='blue', stroke='black'))
        dwg.defs.add(sectionMarker)

        return sectionMarker

    def addEMarker(self, dwg):
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

    def drawArrow(self, line, s_arrow, e_arrow):
        line['marker-start'] = s_arrow.get_funciri()
        line['marker-end'] = e_arrow.get_funciri()

    def drawStartArrow(self, line, s_arrow):
        line['marker-start'] = s_arrow.get_funciri()

    def drawEndArrow(self, line, e_arrow):
        line['marker-end'] = e_arrow.get_funciri()

    def drawWeldArrow(self, ptweld, dwg):
        ptweld2 = ptweld + (sqrt(3) * 5 / 2) * np.array([1, 0]) + 5 / 2 * np.array([0, 1])
        ptweld3 = ptweld + (sqrt(3) * 5 / 2) * np.array([1, 0]) - 5 / 2 * np.array([0, 1])
        dwg.add(dwg.polyline(points=[ptweld, ptweld2, ptweld3], stroke='black', fill='none', stroke_width=2.5))

    def drawFaintLine(self, ptOne, ptTwo, dwg):
        '''
        Draw faint line to show dimensions.

        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptOne :
        :type NumPy Array
        :param ptTwo :
        :type NumPy Array

        '''
        dwg.add(dwg.line(ptOne, ptTwo).stroke('#D8D8D8', width=2.5, linecap='square', opacity=0.7))

    def draw_dimension_outerArrow(self, dwg, pt1, pt2, text, params):

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
        smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)  
 
        lineVec = pt2 - pt1  # [a, b]
        normalVec = np.array([-lineVec[1], lineVec[0]])  # [-b, a]
        normalUnitVec = self.normalize(normalVec)
        if(params["lineori"] == "left"):
            normalUnitVec = -normalUnitVec

        # Q1 = pt1 + params["offset"] * normalUnitVec
        # Q2 = pt2 + params["offset"] * normalUnitVec
        Q1 = pt1 + params["offset"] * normalUnitVec
        Q2 = pt2 + params["offset"] * normalUnitVec
        line = dwg.add(dwg.line(Q1, Q2).stroke('black', width=2.5, linecap='square'))
        self.drawStartArrow(line, emarker)
        self.drawEndArrow(line, smarker)

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
        a = vec[0]
        b = vec[1]
        mag = math.sqrt(a * a + b * b)
        return vec / mag

    def draw_cross_section(self, dwg, ptA, ptB, txtPt, text):
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param ptA :
        :type ptA : NumPy Array
        :param ptB :
        :type ptB : NumPy Array
        :param txtPt :
        :type txtPt : NumPy Array
        :param text :
        :type text : String

        '''
        line = dwg.add(dwg.line((ptA), (ptB)).stroke('black', width=2.5, linecap='square'))
        sec_arrow = self.addSectionMarker(dwg)
        self.drawEndArrow(line, sec_arrow)
        dwg.add(dwg.text(text, insert=(txtPt), fill='black', font_family="sans-serif", font_size=52))

    def draw_dimension_innerArrow(self, dwg, ptA, ptB, text, params):
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

        # smarker = self.addSMarker(dwg)
        # emarker = self.addEMarker(dwg)
        smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)

        u = ptB - ptA  # [a, b]
        uUnit = self.normalize(u)

        vUnit = np.array([-uUnit[1], uUnit[0]])  # [-b, a]

        A1 = ptA + params["endlinedim"] * vUnit
        A2 = ptA - params["endlinedim"] * (-vUnit)
        dwg.add(dwg.line(A1, A2).stroke('black', width=2.5, linecap='square'))
        B1 = ptB + params["endlinedim"] * vUnit
        B2 = ptB - params["endlinedim"] * (-vUnit)
        dwg.add(dwg.line(B1, B2).stroke('black', width=2.5, linecap='square'))
        A3 = ptA - params["arrowlen"] * uUnit
        B3 = ptB + params["arrowlen"] * uUnit

        line = dwg.add(dwg.line(A3, ptA).stroke('black', width=2.5, linecap='square'))
        self.drawEndArrow(line, smarker)
        # self.drawStartArrow(line, emarker)
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width=2.5, linecap='butt'))
        self.drawEndArrow(line, smarker)
        # self.drawStartArrow(line, emarker)
        txtPt = B3 + params["textoffset"] * uUnit
        dwg.add(dwg.text(text, insert=(txtPt), fill='black', font_family="sans-serif", font_size=28))

    def drawOrientedArrow(self, dwg, pt, theta, orientation, offset, textUp, textDown, element):

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
        :param textUp :
        :type textUp : String
        :param textDown :
        :type textup : String

        '''
        # Right Up.
        theta = math.radians(theta)
        charWidth = 16
        xVec = np.array([1, 0])
        yVec = np.array([0, 1])

        p1 = pt
        lengthA = offset / math.sin(theta)

        arrowVec = None
        if(orientation == "NE"):
            arrowVec = np.array([-math.cos(theta), math.sin(theta)])
        elif(orientation == "NW"):
            arrowVec = np.array([math.cos(theta), math.sin(theta)])
        elif(orientation == "SE"):
            arrowVec = np.array([-math.cos(theta), -math.sin(theta)])
        elif(orientation == "SW"):
            arrowVec = np.array([math.cos(theta), -math.sin(theta)])

        p2 = p1 - lengthA * arrowVec

        text = textDown if len(textDown) > len(textUp) else textUp
        lengthB = len(text) * charWidth

        labelVec = None
        if(orientation == "NE"):
            labelVec = -xVec
        elif(orientation == "NW"):
            labelVec = xVec
        elif(orientation == "SE"):
            labelVec = -xVec
        elif(orientation == "SW"):
            labelVec = xVec

        p3 = p2 + lengthB * (-labelVec)

        txtOffset = 18
        offsetVec = -yVec

        txtPtUp = None
        if(orientation == "NE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - (txtOffset + 15) * offsetVec
        elif(orientation == "NW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + txtOffset * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec
        elif(orientation == "SE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - txtOffset * offsetVec
        elif(orientation == "SW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + (txtOffset) * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill='none', stroke='black', stroke_width=2.5))

        # smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)
        # self.drawStartArrow(line, smarker)
        self.drawStartArrow(line, emarker)

        dwg.add(dwg.text(textUp, insert=(txtPtUp), fill='black', font_family="sans-serif", font_size=28))
        dwg.add(dwg.text(textDown, insert=(txtPtDwn), fill='black', font_family="sans-serif", font_size=28))

        if element == "weld":
            if orientation == "NW":
                self.draw_weld_Marker(dwg, 15, 7.5, line)
            else:
                self.draw_weld_Marker(dwg, 45, 7.5, line)

    def draw_weld_Marker(self, dwg, oriX, oriY, line):

        weldMarker = dwg.marker(insert=(oriX, oriY), size=(15, 15), orient="auto")
        weldMarker.add(dwg.path(d="M 0 0 L 8 7.5 L 0 15 z", fill='none', stroke='black'))
        dwg.defs.add(weldMarker)
        self.drawEndArrow(line, weldMarker)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#     def saveToSvg(self, fileName, view, base_front, base_top, base_side):
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def saveToSvg(self, fileName, view):
        '''
         It returns the svg drawing depending upon connectivity
        CFBW = Column Flange Beam Web
        CWBW = Column Web Beam Web
        BWBW = Beam Web Beam Web

        '''
        end2DFront = End2DCreatorFront(self)
        end2DTop = End2DCreatorTop(self)
        end2DSide = End2DCreatorSide(self)

        if self.connectivity == 'Column flange-Beam web':
            if view == "Front":
                fileName = end2DFront.callCFBWfront(fileName)
            elif view == "Side":
                fileName = end2DSide.callCFBWSide(fileName)
            elif view == "Top":
                fileName = end2DTop.callCFBWTop(fileName)
            else:
                fileName = str(self.folder) + '/images_html/endFront.svg'
                end2DFront.callCFBWfront(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endFront.png')

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endFrontFB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 end2DFront.callCFBWfront(fileName)
#                 base_front = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                fileName = str(self.folder) + '/images_html/endSide.svg'
                end2DSide.callCFBWSide(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endSide.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endSideFB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_side = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                fileName = str(self.folder) + '/images_html/endTop.svg'
                end2DTop.callCFBWTop(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endTop.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/finTopFB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_top = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif self.connectivity == 'Column web-Beam web':
            if view == "Front":
                end2DFront.callCWBWfront(fileName)
            elif view == "Side":
                end2DSide.callCWBWSide(fileName)
            elif view == "Top":
                end2DTop.callCWBWTop(fileName)
            else:
                fileName = str(self.folder) + '/images_html/endFront.svg'
                end2DFront.callCWBWfront(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endFront.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endFrontWB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_front = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                fileName = str(self.folder) + '/images_html/endSide.svg'
                end2DSide.callCWBWSide(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endSide.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endSideWB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_side = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                fileName = str(self.folder) + '/images_html/endTop.svg'
                end2DTop.callCWBWTop(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endTop.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endTopWB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_top = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        else:
            if view == "Front":
                end2DFront.callBWBWfront(fileName)
            elif view == "Side":
                end2DSide.callBWBWSide(fileName)
            elif view == "Top":
                end2DTop.callBWBWTop(fileName)
            else:
                fileName = str(self.folder) + '/images_html/endFront.svg'
                end2DFront.callBWBWfront(fileName)
                cairosvg.svg2png(file_obj = fileName, writ_to = str(self.folder) + '/images_html/endFront.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endFrontBB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_front = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                fileName = str(self.folder) + '/images_html/endSide.svg'
                end2DSide.callBWBWSide(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endSide.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endSideBB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_side = os.path.basename(str(fileName))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                fileName = str(self.folder) + '/images_html/endTop.svg'
                end2DTop.callBWBWTop(fileName)
                cairosvg.svg2png(file_obj = fileName, write_to = str(self.folder) + '/images_html/endTop.png')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% for saving multiple images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 for n in range(1, 5, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/endTopBB" + '(' + str(n) + ')' + ".svg"
#                         continue
#                 base_top = os.path.basename(str(fileName))

#         return base_front, base_top, base_side
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class End2DCreatorFront(object):

    def __init__(self, finCommonObj):

        self.dataObj = finCommonObj

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

        ptRx = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick
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

        fromPlate_pt = self.dataObj.D_col + self.dataObj.plate_thick  # 20 mm clear distance between colume and beam
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
        ptFC1x = fromPlate_pt
        ptFC1y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FC1 = np.array([ptFC1x, ptFC1y])

        # FC2
        ptFC2x = fromPlate_pt
        ptFC2y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
        self.FC2 = (ptFC2x, ptFC2y)

        # FA1
        ptFA1x = fromPlate_pt
        ptFA1y = (self.dataObj.col_L - self.dataObj.D_beam) / 2
        self.FA1 = np.array([ptFA1x, ptFA1y])

        # FA4
        ptFA4x = fromPlate_pt
        ptFA4y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.beam_T
        self.FA4 = ptFA4x, ptFA4y

        # FA2
        ptFA2x = ptFC1x + self.dataObj.beam_L
        ptFA2y = ptFA1y
        self.FA2 = np.array([ptFA2x, ptFA2y])

        # FA3
        ptFA3x = fromPlate_pt + self.dataObj.beam_L
        ptFA3y = (((self.dataObj.col_L - self.dataObj.D_beam) / 2) + self.dataObj.beam_T)
        self.FA3 = ptFA3x, ptFA3y

        # FB3
        ptFB3x = fromPlate_pt + self.dataObj.beam_L
        ptFB3y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB3 = (ptFB3x, ptFB3y)

        # FB2
        ptFB2x = fromPlate_pt + self.dataObj.beam_L
        ptFB2y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam
        self.FB2 = ptFB2x, ptFB2y

        # FB1
        ptFB1x = self.dataObj.D_col + self.dataObj.plate_thick
        ptFB1y = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam
        self.FB1 = np.array([ptFB1x, ptFB1y])

        # FB4
        ptFB4x = fromPlate_pt
        ptFB4y = ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB4 = ptFB4x, ptFB4y

        ######################################### POINTS FOR BEAM BEAM CONNECTION ####################################################

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

        self.BA1 = self.BB + 10 * np.array([1, 0])
        self.BA2 = self.BA1 + (self.dataObj.beam_L - 10 - self.dataObj.col_B / 2 + self.dataObj.col_tw / 2 + self.dataObj.plate_thick) * np.array([1, 0])
        self.BB2 = self.BA2 + self.dataObj.D_beam * np.array([0, 1])
        self.BB1 = self.BB2 - self.dataObj.beam_L * np.array([1, 0])
        self.BA4 = self.BA1 + self.dataObj.beam_T * np.array([0, 1])
        self.BA3 = self.BA2 + self.dataObj.beam_T * np.array([0, 1])
        self.BB3 = self.BB2 - self.dataObj.beam_T * np.array([0, 1])
        self.BB4 = self.BB1 - self.dataObj.beam_T * np.array([0, 1])
        self.BC1 = self.BB1 - (self.dataObj.D_beam - self.dataObj.notch_offset) * np.array([0, 1])
        self.BC2 = self.BC1 + self.dataObj.plate_ht * np.array([0, 1])
        self.BA5 = self.BA1 + self.dataObj.notch_offset * np.array([0, 1])

        # for end plate

        self.BP = self.BC1 - self.dataObj.plate_thick * np.array([1, 0])

    def callBWBWfront(self, fileName):
        v_height = self.dataObj.D_col + 850
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-250 -400 1200 ' + str(v_height)))

        # Cross section A-A
        ptSecA = self.BA + (320 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txtpt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txtpt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))
        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BC), (self.BD), (self.BE), (self.BF), (self.BG), (self.BH), (self.BI), (self.BJ), (self.BK),
                                     (self.BL), (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        pt1 = self.BA5 - self.dataObj.col_R1 * np.array([0, 1])
        pt2 = self.BA5 - self.dataObj.col_R1 * np.array([1, 0])
        dwg.add(dwg.polyline(points=[(pt1), (self.BA1), (self.BA2), (self.BB2), (self.BB1), (self.BB4), (self.BC2), (self.BC1), (pt2)], stroke='blue',
                             fill='none', stroke_width=2.5))
#         dwg.add(dwg.polyline(points = [(self.BC1),(self.BA5),(self.BA1),(self.BA2),(self.BB2),(self.BB1),(self.BB4),(self.BC2),(self.BC1)],stroke = 'blue',
#                 fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.line((self.BA4), (self.BA3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BB4), (self.BB3)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.plate_thick, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))

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

        # Weld hatching to represent WELD.
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(4, 4), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))
        dwg.add(dwg.rect(insert=(self.BC1), size=(self.dataObj.weld_thick, self.dataObj.plate_ht),
                         fill="url(#diagonalHatch)", stroke='white', stroke_width=2.0))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia / 2
        ptList = []

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

            ptList.append(pt)

        pitchPts = []
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        params = {"offset": self.dataObj.col_B / 2 - self.dataObj.col_tw / 2 + 50, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[-1]), str(len(pitchPts) - 1) + u' \u0040' +
                                               str(int(self.dataObj.pitch)) + "c/c", params)

        # Distance between Beam Flange and Plate
        BA_down = self.BA + (self.dataObj.notch_offset) * np.array([0, 1])
        params = {"offset": 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.BA, BA_down, str(int(self.dataObj.notch_offset)), params)
        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        ptOne = self.BA
        ptTwo = self.BA - 50 * np.array([1, 0])
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)

        ptone = self.BP
        pttwo = self.BP - (self.dataObj.col_B + self.dataObj.col_tw + 100) / 2 * np.array([1, 0])
        self.dataObj.drawFaintLine(ptone, pttwo, dwg)

        # End Distance from the starting point of plate Information
        edgPt = self.BP - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": self.dataObj.col_B / 2 - self.dataObj.col_tw / 2 + 50, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), edgPt, str(int(self.dataObj.end_dist)), params)

        # End Distance from plate end point.
        edgPt1 = self.BP + self.dataObj.plate_ht * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": self.dataObj.col_B / 2 - self.dataObj.col_tw / 2 + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[-1]), edgPt1, str(int(self.dataObj.end_dist)), params)
        self.dataObj.drawFaintLine(edgPt1, edgPt1 - (self.dataObj.col_B + self.dataObj.col_tw + 100) / 2 * np.array([1, 0]), dwg)
        ###### Draws faint line to show dimensions #########
        # Faint lines for gauge and edge distances

        ptTwo = np.array(ptList[0]) - (self.dataObj.col_B - self.dataObj.col_tw + 100) / 2 * np.array([1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[0]), ptTwo, dwg)

        ptThree = np.array(ptList[-1]) - (self.dataObj.col_B - self.dataObj.col_tw + 100) / 2 * np.array([1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[-1]), ptThree, dwg)


        # Beam Information
        beam_pt = self.BA2 + self.dataObj.D_beam / 2 * np.array([0, 1])
        theta = 1
        offset = 0.0 
        textUp = "SecondaryBeam " + self.dataObj.beam_Designation
        textDown = ""

        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Column Designation

        pt = (self.BH + self.BG) / 2
        theta = 90
        offset = 100
        textUp = "Primary beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "SE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.BC1 + (self.dataObj.weld_thick / 2) * np.array([1, 0])
        theta = 20
        offset = self.dataObj.col_B 
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown, element="weld")

        # Bolt Information
        bltPtx = np.array(ptList[-1])
        theta = 30
        offset = (self.dataObj.D_beam * 3 + 600) / 8
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "SE", offset, textUp, textDown, element="")

        # Plate Information

        pltPt = self.BC1 - (self.dataObj.plate_thick / 2) * np.array([1, 0])
        theta = 90
        offset = (self.dataObj.notch_offset + 100)
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + "X" + str(int(self.dataObj.plate_width)) + "X" + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "NE", offset, textUp, textDown, element="")

        # 2D view name
        ptx = self.BA + 50 * np.array([1, 0]) + (v_height - 400) * np.array([0, 1])
        dwg.add(dwg.text("Front view (Sec C-C)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "########### Beam web Beam web saved ###########"

    def callCFBWfront(self, fileName):
        v_width = self.dataObj.D_col + 1000
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-340 -280 ' + str(v_width) + ' 1225'))

        # Cross section A-A
        ptSecA = self.FA + (250 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txtpt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txtpt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

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
        ptList = []

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

            ptList.append(pt)

        pitchPts = []
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 50, "textoffset": 150, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[-1]), str(len(pitchPts) - 1) + u' \u0040' +
                                               str(int(self.dataObj.pitch)) + "c/c", params)

        # Distance between Beam Flange and Plate

        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.FA1, self.FC1, str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)), params)
        # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        ptOne = self.FA1
        ptBx = 60 * np.array([-1, 0])
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam) / 2)
        ptTwo = self.FA1 - (60 + self.dataObj.D_col + self.dataObj.plate_thick) * np.array([1, 0])
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)

        # End Distance from the starting point of plate Information
        edgPt = self.FP - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + self.dataObj.plate_thick + 50, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), edgPt, str(int(self.dataObj.end_dist)), params)

        # End Distance from plate end point.
        edgPt1 = self.FU - self.dataObj.col_T * np.array([1, 0])
        params = {"offset": self.dataObj.D_col + self.dataObj.end_dist + 50, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[-1]), edgPt1, str(int(self.dataObj.end_dist)), params)

        # Edge Distance information
        pt1A = self.ptFP + self.dataObj.edge_dist * np.array([1, 0]) + \
                (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0]) + self.dataObj.end_dist * np.array ([0, 1])
        pt1B = self.ptFP + self.dataObj.edge_dist * np.array([1, 0]) + \
               (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0]) + self.dataObj.edge_dist * np.array([1, 0]) + self.dataObj.end_dist * np.array ([0, 1])
        offset = self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3
        params = {"offset": self.dataObj.D_col + self.dataObj.edge_dist , "textoffset": 20, "lineori": "left", "endlinedim": 10}
#         self.dataObj.draw_dimension_outerArrow(dwg, pt1A, pt1B, str(int(self.dataObj.edge_dist)) + " mm" , params)
        # Faint line for Edge distance dimension
        ptB1 = self.ptFP + self.dataObj.edge_dist * np.array([1, 0]) + \
                (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0]) + self.dataObj.edge_dist * np.array([1, 0])
        ptB2 = ptB1 + ((self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 115) * np.array([0, -1])
#         self.dataObj.drawFaintLine(ptB1,ptB2,dwg)

        # Gap Distance
        gapPt = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)) 
        ptG1 = self.ptFP + (gapPt + 30) * np.array([0, 1])
        ptG2 = self.FC1 + (gapPt + 30) * np.array([0, 1])
        offset = self.dataObj.col_L  # 60% of the column length
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10, "arrowlen": 50}
#         self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.plate_thick) + " mm", params)

        # Draw Faint line for Gap Distance
        ptC1 = self.FC
        ptC2 = ptC1 + 40 * np.array([0, 1])
#         self.dataObj.drawFaintLine(ptC1,ptC2,dwg)

        ptD1 = self.FB1
        ptD2 = ptD1 + 240 * np.array([0, 1])
#         self.dataObj.drawFaintLine(ptD1,ptD2,dwg)

        ###### Draws faint line to show dimensions #########
        # Faint lines for gauge and edge distances
        ptOne = self.FP - (60 + self.dataObj.D_col) * np.array([1, 0])
        self.dataObj.drawFaintLine(self.FP, ptOne, dwg)

        ptTwo = np.array(ptList[0]) - (60 + self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[0]), ptTwo, dwg)

        ptThree = np.array(ptList[-1]) - (60 + self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[-1]), ptThree, dwg)

        ptFour = self.FU - (60 + self.dataObj.D_col) * np.array([1, 0])
        self.dataObj.drawFaintLine(self.FU, ptFour, dwg)

        # Beam Information
        beam_pt = self.FA2 + self.dataObj.D_beam / 2 * np.array([0, 1])
        theta = 1
        offset = 0.0 
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Column Designation

        pt = (self.FH + self.FG) / 2
        theta = 30
        offset = self.dataObj.col_L / 10
        textUp = "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "SW", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.FW + (self.dataObj.weld_thick / 2) * np.array([1, 0])
        theta = 45
        offset = self.dataObj.col_B 
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown, element="weld")

        # Bolt Information
        bltPtx = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.D_beam * 3 + 400) / 8
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element="")

        # Plate Information

        pltPt = self.FU + (self.dataObj.plate_thick / 2) * np.array([1, 0])
        theta = 45
        offset = (self.dataObj.D_beam + 100) / 2
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + "X" + str(int(self.dataObj.plate_width)) + "X" + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "SE", offset, textUp, textDown, element="")

        # 2D view name
        ptx = self.FA + 50 * np.array([1, 0]) + 930 * np.array([0, 1])
        dwg.add(dwg.text("Front view (Sec C-C)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"########### Column Flange Beam Web Saved ############"

    def callCWBWfront(self, fileName):
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-400 -250 1250 1250'))

        # Cross section A-A
        ptSecA = self.A + (220 * np.array([0, -1]))
        ptSecB = ptSecA + (50 * np.array([0, 1]))
        txtpt = ptSecB + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        txt = "A"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.dataObj.beam_L) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, 1]))
        txtpt = ptSecD + (10 * np.array([-1, 0])) + (80 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)

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
        ptList = []

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

            ptList.append(pt)

        pitchPts = []
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])

        txtOffset = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80, "textoffset": 150,
                  "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[-1]), str(len(pitchPts) - 1) + u' \u0040' +
                                               str(int(self.dataObj.pitch)) + "c/c", params)

        # End Distance from the starting point of plate Information
        edgePt = self.P - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), edgePt, str(int(self.dataObj.end_dist)), params)

        # Distance between Beam Flange and Plate
        offset = (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick + 50
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.plate_thick + 80, "textoffset": 50, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.A1, self.C1, str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)), params) 

        # Draw Faint line for dimensions

        ptOne = self.ptP - (60 + self.dataObj.col_B / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(self.ptP, ptOne, dwg)

        ptTwo = np.array(ptList[0]) - (60 + self.dataObj.col_B / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[0]), ptTwo, dwg)

        ptThree = np.array(ptList[-1]) - (60 + self.dataObj.col_B / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[-1]), ptThree, dwg)

        ptFour = self.U - (60 + self.dataObj.col_B / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(self.U, ptFour, dwg)

        # End Distance from plate end point.
        edgePt1 = self.U - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw) / 2 + self.dataObj.edge_dist + 80,
                  "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[-1]), edgePt1, str(int(self.dataObj.edge_dist)), params)

        # Gap Distance
        # Draw Faint Lines to representation of Gap distance #
        dist1 = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.D_beam)
#         ptA = self.B1
#         ptB = self.B1 + (dist1 + 100)* np.array([0,1])
#         self.dataObj.drawFaintLine(ptA,ptB,dwg)
#         ptC = self.G
#         ptD = ptC + (100)*np.array([0,1])
#         self.dataObj.drawFaintLine(ptC,ptD,dwg)
#         ptG1 = self.B1 + (dist1 + 50)* np.array([0,1])
#         ptG2 = self.B1 + self.dataObj.gap * np.array([-1,0]) + (dist1 + 50)* np.array([0,1])
#         offset = 1
#         params = {"offset": offset, "textoffset": 120, "lineori": "right", "endlinedim":10,"arrowlen":50}
#         self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)

        # Edge Distance Information
        ptA = self.ptP + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.no_of_col - 1) * self.dataObj.gauge * np.array([1, 0])
        ptB = ptA + self.dataObj.edge_dist * np.array([1, 0])
        offsetDist = -(self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 120)
        params = {"offset": offsetDist, "textoffset": 35, "lineori": "right", "endlinedim": 10}
        # self.dataObj.draw_dimension_outerArrow(dwg,ptA,ptB, str(int(self.dataObj.edge_dist)) + " mm", params)

        # Plate Width Information

        pltPt = self.U + (self.dataObj.plate_thick / 2) * np.array([1, 0])
        theta = 45
        offset = (self.dataObj.D_beam + 100) / 2
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + "X" + str(int(self.dataObj.plate_width)) + "X" + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "SE", offset, textUp, textDown, element="")

        # Column Designation
        pt = self.H
        theta = 30
        offset = self.dataObj.col_L / 10
        textUp = "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "SW", offset, textUp, textDown, element="")

        # Bolt Information
        bltPtx = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.D_beam * 3 + 400) / 8
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element="")

        # Beam Information
        beam_pt = self.ptB1 + (self.dataObj.beam_L) * np.array([1, 0]) + self.dataObj.D_beam / 2 * np.array([0, -1])
        theta = 1
        offset = 0.0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.W + (self.dataObj.weld_thick / 2) * np.array([1, 0])
        theta = 45
        offset = self.dataObj.col_B
        textUp = "          z " + str(self.dataObj.weld_thick)
        textDown = ""

        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown, element="weld")

        # 2D view name
        ptx = self.A + 50 * np.array([1, 0]) + 985 * np.array([0, 1])
        dwg.add(dwg.text("Front view (Sec C-C)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"########### Column Web Beam Web Saved ############"


class End2DCreatorTop(object):

    def __init__(self, finCommonObj):

        self.dataObj = finCommonObj
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
        self.notch_length = (self.dataObj.col_B - self.dataObj.col_tw) / 2 + 10 - self.dataObj.plate_thick

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

    def callBWBWTop(self, fileName):

        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-300 -250 1200 1000'))

        ############################################# B-B section #######################################################
        ptSecA = self.BB + ((50 + self.dataObj.plate_thick + self.dataObj.beam_L + 150) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txtpt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.BC + ((50 + self.dataObj.plate_thick + self.dataObj.beam_L + 150) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txtpt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ############ C-C section #################
        ptSecA = self.BD + 50 * np.array([-1, 0]) + ((self.dataObj.D_beam * 3) / 8) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txtpt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (self.dataObj.col_B + self.beam_beam_length) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txtpt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
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
        ptList = []
        ptList1 = []

        if nc >= 1:
            for col in range(nc):
                pt = self.BP1 - self.dataObj.col_tw * np.array([1, 0]) + self.dataObj.edge_dist * np.array([0, 1]) + (col) * self.dataObj.gauge * np.array([0, 1])
                pt1 = pt - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([-1, 0])
                B2 = pt + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_ref = self.BP4 - self.dataObj.col_tw * np.array([1, 0]) - self.dataObj.edge_dist * np.array([0, 1]) - (col) * self.dataObj.gauge * np.array([0, 1])
                pt_ref1 = pt_ref - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt_ref1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1_ref = pt_ref + 10 * np.array([-1, 0])
                B2_ref = pt_ref + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_ref), (B2_ref)).stroke('black', width=2.5, linecap='square'))

                ptList.append(pt)
                ptList1.append(pt_ref)
                bltdimoffset = self.dataObj.col_B / 2 + 50

                if len(ptList) > 1:
                    ptblt2 = np.array(ptList[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])

                    ptblt2_ref = np.array(ptList1[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
                    params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                    params_ref = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
                    self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList1[0]), np.array(ptList1[1]), str(int(self.dataObj.gauge)), params_ref)
                    self.dataObj.drawFaintLine(np.array(ptList[-1]), ptblt2, dwg)
                    self.dataObj.drawFaintLine(np.array(ptList1[-1]), ptblt2_ref, dwg)

        # Draw Faint line to represent edge distance
#         ptB = self.FP + (self.dataObj.col_T) * np.array([-1,0])
#         ptC = ptB + (bltdimoffset) * np.array([-1,0])
# #         self.dataObj.drawFaintLine(ptB,ptC,dwg)
#         ptL = np.array(ptList[-1])

        # Faint Lines for bolts
        ptblt1 = np.array(ptList[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        ptblt1_ref = np.array(ptList1[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[0]), ptblt1, dwg)
        self.dataObj.drawFaintLine(np.array(ptList1[0]), ptblt1_ref, dwg)

        # Edge Distance
        ptB = self.BP1 - self.dataObj.col_tw * np.array([1, 0])
        pt2 = ptB - bltdimoffset * np.array([1, 0])
        self.dataObj.drawFaintLine(ptB, pt2, dwg)

        ptBD = self.BP4
        pt2 = ptBD - (bltdimoffset + self.dataObj.col_tw) * np.array([1, 0])
        self.dataObj.drawFaintLine(ptBD, pt2, dwg)

        ptB = self.BP1 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, ptB, np.array(ptList[0]), str(int(self.dataObj.edge_dist)), params)
        ptB = self.BP4 - self.dataObj.col_tw * np.array([1, 0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, ptB, np.array(ptList1[0]), str(int(self.dataObj.edge_dist)), params)

        # Beam Information
        beam_pt = (self.BA4 + self.BA5) / 2
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Column Information
        col_pt = (self.BA + self.BB) / 2
        theta = 90
        offset = 100
        textUp = "Beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "NW", offset, textUp, textDown, element="")

        # Plate  Information
        plt_pt = self.BP4 + self.dataObj.plate_thick / 2 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.beam_B / 2 + 50
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown, element="")

        # Bolt Information
        bltPt = np.array(ptList[0])
        theta = 75
        offset = (self.beam_beam_length / 2) + 25
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.BA9
        theta = 40
        offset = self.dataObj.beam_B / 2 + 50
        textUp = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown, element="weld")
#         weldarrow = weldPt + offset*np.array([0,-1]) + 18*np.array([-1,0])
#         self.dataObj.drawWeldArrow(weldarrow , dwg)

        # 2D view name
        ptx = self.BA + 150 * np.array([1, 0]) + 740 * np.array([0, 1])
        dwg.add(dwg.text("Top view (Sec A-A)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()
        print "######### Beam Beam Top Saved ############"

    def callCFBWTop(self, fileName):
        v_width = self.dataObj.D_col + 1000
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-250 -350 ' + str(v_width) + ' 1000'))

        ############ B-B section #################
        ptSecA = self.FF + ((230 + self.dataObj.plate_thick + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txtpt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.FG + ((230 + self.dataObj.plate_thick + self.dataObj.beam_L) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txtpt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ############ C-C section #################
        ptSecA = self.FL + 50 * np.array([-1, 0]) + ((self.dataObj.D_beam * 3) / 8 + 100) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txtpt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.plate_thick + self.dataObj.beam_L + 100) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txtpt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
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
        ptList = []
        ptList1 = []

        if nc >= 1:
            for col in range(nc):
                pt = self.FP + (self.dataObj.edge_dist) * np.array([0, 1]) - self.dataObj.col_T * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array([0, 1])
                pt1 = pt - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_T + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([-1, 0])
                B2 = pt + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_ref = self.FP2 + (self.dataObj.edge_dist) * np.array([0, -1]) - self.dataObj.col_T * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array([0, -1])
                pt_ref1 = pt_ref - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_T + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt_ref1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1_ref = pt_ref + 10 * np.array([-1, 0])
                B2_ref = pt_ref + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_ref), (B2_ref)).stroke('black', width=2.5, linecap='square'))

                ptList.append(pt)
                ptList1.append(pt_ref)
                bltdimoffset = self.dataObj.D_col + 2 * self.dataObj.col_T + 50

                if len(ptList) > 1:
                    ptblt2 = np.array(ptList[-1]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])

                    ptblt2_ref = np.array(ptList1[-1]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])
                    params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                    params_ref = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
                    self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList1[0]), np.array(ptList1[1]), str(int(self.dataObj.gauge)), params_ref)
                    self.dataObj.drawFaintLine(np.array(ptList[-1]), ptblt2, dwg)
                    self.dataObj.drawFaintLine(np.array(ptList1[-1]), ptblt2_ref, dwg)

        # Draw Faint line to represent edge distance
        ptB = self.FP + (self.dataObj.col_T) * np.array([-1, 0])
        ptC = ptB + (bltdimoffset) * np.array([-1, 0])
        self.dataObj.drawFaintLine(ptB, ptC, dwg)
        ptB1 = self.FP2 + (self.dataObj.col_T) * np.array([-1, 0])
        ptC1 = ptB1 + (bltdimoffset) * np.array([-1, 0])
        self.dataObj.drawFaintLine(ptB1, ptC1, dwg)

        # Faint Lines for bolts
        ptblt1 = np.array(ptList[0]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])
        ptblt1_ref = np.array(ptList1[0]) + (self.dataObj.D_col + self.dataObj.col_T + 50) * np.array([-1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[0]), ptblt1, dwg)
        self.dataObj.drawFaintLine(np.array(ptList1[0]), ptblt1_ref, dwg)

        # Edge Distance
        ptL = np.array(ptList[0])

        ptL1 = np.array(ptList1[0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, ptB, ptL, str(int(self.dataObj.edge_dist)), params)
        self.dataObj.draw_dimension_outerArrow(dwg, ptL1, ptB1, str(int(self.dataObj.edge_dist)), params)

        # Beam Information
        beam_pt = self.FA6
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Column Information
        col_pt = self.FL
        theta = 45
        offset = (self.dataObj.D_beam * 3) / 8
        textUp = "Beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown, element="")

        # Plate  Information
        plt_pt = self.FP + self.dataObj.plate_width * np.array([0, 1]) + self.dataObj.plate_thick / 2 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.beam_B / 2 + 50
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown, element="")

        # Bolt Information
        bltPt = self.FP5 + (50 - self.dataObj.beam_tw / 2) * np.array([0, -1]) - self.dataObj.col_T * np.array([1, 0])
        theta = 45
        offset = (self.dataObj.beam_B) + 50
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.FA7
        theta = 40
        offset = self.dataObj.weld_thick + self.dataObj.plate_thick + self.dataObj.beam_B / 2 + 80
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown, element="weld")
#         weldarrow = weldPt + offset*np.array([0,-1]) + 18*np.array([-1,0])
#         self.dataObj.drawWeldArrow(weldarrow , dwg)

        # 2D view name
        ptx = self.FA + 150 * np.array([1, 0]) + 640 * np.array([0, 1])
        dwg.add(dwg.text("Top view (Sec A-A)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))
        dwg.save()
        print"$$$$$$$$$ Saved Column Flange Beam Web Top $$$$$$$$$$$$"

    def callCWBWTop(self, fileName):
        v_length = self.dataObj.col_B + 850
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-230 -300 1200 ' + str(v_length)))

        ############ B-B section #################
        ptSecA = self.B + ((130 + self.dataObj.plate_thick + self.dataObj.beam_L + 100) * np.array([1, 0]))
        ptSecB = ptSecA + (50 * np.array([-1, 0]))
        txtpt = ptSecB + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        txt = "B"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = self.G + ((130 + self.dataObj.plate_thick + self.dataObj.beam_L + 100) * np.array([1, 0]))
        ptSecD = ptSecC + (50 * np.array([-1, 0]))
        txtpt = ptSecD + (80 * np.array([-1, 0])) + (20 * np.array([0, 1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        ############ C-C section #################
        ptSecA = self.H + 50 * np.array([-1, 0]) + ((self.dataObj.D_beam * 3) / 8 + 100) * np.array([0, 1])
        ptSecB = ptSecA + (50 * np.array([0, -1]))
        txtpt = ptSecB + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        txt = "C"
        self.dataObj.draw_cross_section(dwg, ptSecA, ptSecB, txtpt, txt)
        ptSecC = ptSecA + (self.dataObj.D_col + self.dataObj.plate_thick + self.dataObj.beam_L + 100) * np.array([1, 0])
        ptSecD = ptSecC + (50 * np.array([0, -1]))
        txtpt = ptSecD + (20 * np.array([-1, 0])) + (40 * np.array([0, -1]))
        self.dataObj.draw_cross_section(dwg, ptSecC, ptSecD, txtpt, txt)
        dwg.add(dwg.line((ptSecA), (ptSecC)).stroke('#666666', width=1.0, linecap='square'))

        dwg.add(dwg.polyline(points=[(self.A), (self.B), (self.C), (self.D), (self.E), (self.F), (self.G), (self.H), (self.I), (self.J), (self.K), (self.L), (self.A)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A1), size=(self.dataObj.beam_L, self.dataObj.beam_B), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.A7), (self.A8)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.P1), (self.A6)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.plate_thick, self.dataObj.plate_width), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline([(self.ptP), (self.ptO), (self.ptR), (self.ptP)], fill='black', stroke_width=2.5, stroke='black'))
        dwg.add(dwg.polyline([(self.ptX), (self.ptY), (self.ptZ), (self.ptX)], fill='black', stroke_width=2.5, stroke='black'))

        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        ptList = []
        ptList1 = []

        if nc >= 1:
            for col in range(nc):
                pt = self.P + (self.dataObj.edge_dist) * np.array([0, 1]) - self.dataObj.col_tw * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array([0, 1])
                pt1 = pt - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([-1, 0])
                B2 = pt + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1), (B2)).stroke('black', width=2.5, linecap='square'))

                pt_ref = self.X + (self.dataObj.edge_dist) * np.array([0, -1]) - self.dataObj.col_tw * np.array([1, 0]) + (col) * self.dataObj.gauge * np.array([0, -1])
                pt_ref1 = pt_ref - bolt_r * np.array([0, 1])
                rect_width = self.dataObj.bolt_dia
                rect_length = self.dataObj.col_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt_ref1), size=(rect_length, rect_width), fill='black', stroke='black', stroke_width=2.5))
                B1_ref = pt_ref + 10 * np.array([-1, 0])
                B2_ref = pt_ref + (rect_length + 10) * np.array([1, 0])
                dwg.add(dwg.line((B1_ref), (B2_ref)).stroke('black', width=2.5, linecap='square'))

                ptList.append(pt)
                ptList1.append(pt_ref)
                bltdimoffset = self.dataObj.D_col / 2 + 50

                if len(ptList) > 1:

                    ptblt2 = np.array(ptList[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])

                    ptblt2_ref = np.array(ptList1[-1]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
                    params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
                    params_ref = {"offset": bltdimoffset, "textoffset": 50, "lineori": "left", "endlinedim": 10}
                    self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[1]), str(int(self.dataObj.gauge)), params)
                    self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList1[0]), np.array(ptList1[1]), str(int(self.dataObj.gauge)), params_ref)
                    self.dataObj.drawFaintLine(np.array(ptList[-1]), ptblt2, dwg)
                    self.dataObj.drawFaintLine(np.array(ptList1[-1]), ptblt2_ref, dwg)


        # Draw Faint line to represent edge distance
        ptB = self.P + self.dataObj.col_tw * np.array([-1, 0])
        ptC = ptB + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.drawFaintLine(ptB, ptC, dwg)
        ptB1 = self.X + self.dataObj.col_tw * np.array([-1, 0])
        ptC1 = ptB1 + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.drawFaintLine(ptB1, ptC1, dwg)

        # Faint Lines for bolts
        ptblt1 = np.array(ptList[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        ptblt1_ref = np.array(ptList1[0]) + (self.dataObj.col_B / 2 + 50) * np.array([-1, 0])
        self.dataObj.drawFaintLine(np.array(ptList[0]), ptblt1, dwg)
        self.dataObj.drawFaintLine(np.array(ptList1[0]), ptblt1_ref, dwg)

        # Edge Distance
        ptL = np.array(ptList[0])
        ptL1 = np.array(ptList1[0])
        params = {"offset": bltdimoffset, "textoffset": 50, "lineori": "right", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, ptB, ptL, str(int(self.dataObj.edge_dist)), params)
        self.dataObj.draw_dimension_outerArrow(dwg, ptL1, ptB1, str(int(self.dataObj.edge_dist)), params)

        # Beam Information
        beam_pt = self.A6
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown, element="")

        # column  Information
        col_pt = self.H
        theta = 45
        offset = 250
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " "
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown, element="")

        # Plate  Information
        plt_pt = self.X + self.dataObj.plate_thick / 2 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.beam_B / 2 + 50
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown, element="")

        # Bolt Information
        # bltPt = self.A5 + self.dataObj.edge_dist * np.array([1,0]) + (nc -1) * self.dataObj.gauge * np.array([1,0])
        bltPt = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.beam_B) + 75
        textUp = str(self.dataObj.no_of_rows) + " rows " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPt, theta, "NE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.ptR
        theta = 30
        offset = self.dataObj.D_col * 2 / 4
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown, element="weld")

        # 2D view name
        ptx = self.A + 150 * np.array([1, 0]) + (v_length - 330) * np.array([0, 1])
        dwg.add(dwg.text("Top view (Sec A-A)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print"$$$$$$$$$ Saved Column Web Beam Web Top $$$$$$$$$$$"


class End2DCreatorSide(object):
    def __init__(self, finCommonObj):

        self.dataObj = finCommonObj

        # CWBW connectivity points
        self.A = np.array([0, 0])
        self.B = self.A + self.dataObj.col_T * np.array([1, 0])
        self.C = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1, 0])
        self.D = self.A + self.dataObj.D_col * np.array([1, 0])
        self.H = self.C + self.dataObj.col_L * np.array([0, 1])
        self.G = self.B + self.dataObj.col_L * np.array([0, 1])
        self.A1 = self.A + (self.dataObj.D_col / 2 - self.dataObj.beam_B / 2) * np.array((1, 0)) + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array([0, 1])
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

        #### CFBW connectivity
        self.FA = np.array([0, 0])
        self.FB = self.FA + self.dataObj.col_B * np.array([1, 0])
        self.ptMid = self.FA + ((self.dataObj.col_B / 2) + (self.dataObj.col_tw / 2)) * np.array([1, 0])
        self.ptMid1 = self.ptMid + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array([0, 1])
        self.FC = self.FB + self.dataObj.col_L * np.array([0, 1])
        self.FD = self.FA + self.dataObj.col_L * np.array([0, 1])
        self.FA1 = self.FA + (self.dataObj.col_B / 2 - self.dataObj.beam_B / 2) * np.array((1, 0)) + ((self.dataObj.col_L - self.dataObj.D_beam) / 2) * np.array([0, 1])
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

    def callBWBWSide(self, fileName):
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-300 -200 1200 1200'))
        dwg.add(dwg.polyline(points=[(self.BA), (self.BB), (self.BI), (self.BJ), (self.BA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.BG), (self.BH)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BF), (self.BE)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BD), (self.BC)).stroke('blue', width=2.5, linecap='square'))
        dwg.add(dwg.line((self.BE), (self.BD)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BP), (self.BX)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))
        dwg.add(dwg.line((self.BP1), (self.BX1)).stroke('red', width=2.5, linecap='square').dasharray(dasharray=([5, 5])))

        dwg.add(dwg.polyline(points=[(self.BB1), (self.BC1), (self.BD1), (self.BE1), (self.BF1), (self.BG1), (self.BH1), (self.BI1), (self.BJ1), (self.BK1),
                                     (self.BL1), (self.BA1)], stroke='blue', fill='none', stroke_width=2.5))

        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=1.5))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BY), size=(self.dataObj.weld_thick, self.dataObj.plate_ht), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.BP), size=(self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2, self.dataObj.plate_ht), fill='none', stroke='blue',
                         stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.BZ), size=((self.dataObj.plate_width / 2 - self.dataObj.beam_tw / 2), self.dataObj.plate_ht), fill='none', stroke='blue',
                         stroke_width=2.5))

        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pitchPts = []
        pitchPts1 = []
        for row in range(nr):
            colList = []
            colList1 = []
            for col in range(nc):
                pt = self.BZ + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1]) + (col) * self.dataObj.gauge * np.array([1, 0])
                pt_other = self.BR - self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1]) - (col) * self.dataObj.gauge * np.array([1, 0])

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
                colList.append(pt_other)
                colList1.append(pt)
            pitchPts.append(colList)
            pitchPts1.append(colList1)

        if nc > 1:
            gaugept1_other = np.array(pitchPts[-1][0])
            gaugept2_other = np.array(pitchPts[-1][1])
            params = {"offset": self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50,
                      "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outerArrow(dwg, gaugept1_other, gaugept2_other, str(int(self.dataObj.gauge)), params)

            faintpt1_other = gaugept1_other
            faintpt1_other1 = gaugept1_other + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht +
                                                self.dataObj.edge_dist + 50) * np.array([0, 1])
            faintpt2_other = gaugept2_other
            faintpt2_other1 = gaugept2_other + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht +
                                                self.dataObj.edge_dist + 50) * np.array([0, 1])
            self.dataObj.drawFaintLine(faintpt1_other, faintpt1_other1, dwg)
            self.dataObj.drawFaintLine(faintpt2_other, faintpt2_other1, dwg)

            gaugept1 = np.array(pitchPts1[-1][0])
            gaugept2 = np.array(pitchPts1[-1][1])
            params = {"offset": self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50, "textoffset": 50, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg, gaugept2, gaugept1, str(int(self.dataObj.gauge)), params)
            faintpt1 = gaugept1
            faintpt1_1 = gaugept1 + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50) * np.array([0, 1])
            faintpt2 = gaugept2 + (self.dataObj.D_col - self.dataObj.notch_offset - self.dataObj.plate_ht + self.dataObj.edge_dist + 50) * np.array([0, 1])
            faintpt2_1 = gaugept2
            self.dataObj.drawFaintLine(faintpt1, faintpt1_1, dwg)
            self.dataObj.drawFaintLine(faintpt2, faintpt2_1, dwg)

        ptList = []
        for row in pitchPts:
            if len(row) > 0:
                ptList.append(row[0])

        # End and Pitch Distance Information
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[-1]), str(len(ptList) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) +
                                               "c/c", params)
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.BR - self.dataObj.edge_dist * np.array([1, 0]),
                                               np.array(ptList[0]), str(int(self.dataObj.end_dist)), params)
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[-1]), self.BR - self.dataObj.edge_dist * np.array([1, 0]) +
                                               self.dataObj.plate_ht * np.array([0, 1]), str(int(self.dataObj.end_dist)), params)

        # notch dist
        ptN1 = self.BR - self.dataObj.edge_dist * np.array([1, 0])
        ptN2 = ptN1 - self.dataObj.notch_offset * np.array([0, 1])
        params = {"offset": self.beam_beam_length / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, ptN2, ptN1, str(int(self.dataObj.notch_offset)), params)
        pt9 = self.BB
        pt10 = pt9 + (self.beam_beam_length - self.dataObj.plate_width) / 2 * np.array([1, 0])
        self.dataObj.drawFaintLine(pt9, pt10, dwg)

# Draw Faint Line
        pt1 = self.BR
        pt2 = pt1 + (self.beam_beam_length / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
        pt3 = np.array(ptList[0])
        pt4 = pt3 + (self.beam_beam_length / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt3, pt4, dwg)
        pt5 = np.array(ptList[-1])
        pt6 = pt5 + (self.beam_beam_length / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt5, pt6, dwg)
        pt7 = self.BR + self.dataObj.plate_ht * np.array([0, 1])
        pt8 = pt7 + (self.beam_beam_length / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt7, pt8, dwg)

        # Beam Information
        beam_pt = (self.BG1 + self.BH1) / 2
        theta = 30
        offset = (self.dataObj.plate_width - self.dataObj.beam_tw) / 3.46
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # column  Information
        col_pt = (self.BA + self.BG) / 2
        theta = 60
        offset = 70
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "NW", offset, textUp, textDown, element="")

        # Plate  Information
        beam_pt = (self.BX1 + self.BZ1) / 2
        theta = 30
        offset = self.beam_beam_length / 6
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SW", offset, textUp, textDown, element="")

        # Bolt Information
        bltPtx = np.array(ptList[0])
        theta = 45
        offset = self.dataObj.notch_offset + self.dataObj.end_dist + 50
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.BY + self.dataObj.weld_thick / 2 * np.array([1, 0])
        theta = 30
        offset = self.dataObj.plate_width / 2
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown, element="weld")

        # 2D view name
        ptx = self.BA + 10 * np.array([1, 0]) + 950 * np.array([0, 1])
        dwg.add(dwg.text("Side view (Sec B-B)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "********* Beam Beam Side Saved ***********"

    def callCWBWSide(self, fileName):
        '''
        '''
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-200 -100 1000 1200'))
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
        pitchPts = []
        pitchPts1 = []
        for row in range(nr):
            colList = []
            colList1 = []
            for col in range(nc):
                pt = self.Q + self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1]) + (col) * self.dataObj.gauge * np.array([1, 0])
                pt_other = self.Q1 - self.dataObj.edge_dist * np.array([1, 0]) + (self.dataObj.end_dist) * np.array([0, 1]) + (row) * self.dataObj.pitch * np.array([0, 1]) - (col) * self.dataObj.gauge * np.array([1, 0])

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
                colList.append(pt_other)
                colList1.append(pt)
            pitchPts.append(colList)
            pitchPts1.append(colList1)

        if nc > 1:
            gaugept1_other = np.array(pitchPts[-1][0])
            gaugept2_other = np.array(pitchPts[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outerArrow(dwg, gaugept1_other, gaugept2_other, str(int(self.dataObj.gauge)), params)

            faintpt1_other = gaugept1_other
            faintpt1_other1 = gaugept1_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_other = gaugept2_other
            faintpt2_other1 = gaugept2_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            self.dataObj.drawFaintLine(faintpt1_other, faintpt1_other1, dwg)
            self.dataObj.drawFaintLine(faintpt2_other, faintpt2_other1, dwg)

            gaugept1 = np.array(pitchPts1[-1][0])
            gaugept2 = np.array(pitchPts1[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outerArrow(dwg, gaugept2, gaugept1, str(int(self.dataObj.gauge)), params)
            faintpt1 = gaugept1
            faintpt1_1 = gaugept1 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2 = gaugept2 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_1 = gaugept2
            self.dataObj.drawFaintLine(faintpt1, faintpt1_1, dwg)
            self.dataObj.drawFaintLine(faintpt2, faintpt2_1, dwg)

        ptList = []
        for row in pitchPts:
            if len(row) > 0:
                ptList.append(row[0])

        # End and Pitch Distance Information
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[-1]), str(len(ptList) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) + "c/c", params)
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.Q1 - self.dataObj.edge_dist * np.array([1, 0]), np.array(ptList[0]), str(int(self.dataObj.end_dist)), params)
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[-1]), self.Q1 - self.dataObj.edge_dist * np.array([1, 0]) + self.dataObj.plate_ht *
                                               np.array([0, 1]), str(int(self.dataObj.end_dist)), params)

        # Draw Faint Line
        pt1 = self.Q1
        pt2 = pt1 + (self.dataObj.D_col / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
        pt3 = np.array(ptList[0])
        pt4 = pt3 + (self.dataObj.D_col / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt3, pt4, dwg)
        pt5 = np.array(ptList[-1])
        pt6 = pt5 + (self.dataObj.D_col / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt5, pt6, dwg)
        pt7 = self.Q1 + self.dataObj.plate_ht * np.array([0, 1])
        pt8 = pt7 + (self.dataObj.D_col / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt7, pt8, dwg)

        # Beam Information
        beam_pt = (self.A8 + self.A7) / 2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + 50
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SW", offset, textUp, textDown, element="")

        # column  Information
        col_pt = self.H
        theta = 45
        offset = 70
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " "
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown, element="")

        # Plate  Information
        beam_pt = self.Q1 + self.dataObj.plate_ht * np.array([0, 1]) - self.dataObj.plate_width / 4 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.plate_thick + self.dataObj.beam_B / 2 + 80
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Bolt Information
        bltPtx = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.D_col - self.dataObj.plate_width) / 2 + self.dataObj.end_dist + 50
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.X + self.dataObj.weld_thick / 2 * np.array([1, 0])
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.beam_T + self.dataObj.beam_R1 + 50
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown, element="weld")

        # 2D view name
        ptx = self.A + 10 * np.array([1, 0]) + 950 * np.array([0, 1])
        dwg.add(dwg.text("Side view (Sec B-B)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        print "********* Column Web Beam Web Side Saved ***********"

    def callCFBWSide(self, fileName):
        dwg = svgwrite.Drawing(fileName, size=('100%', '100%'), viewBox=('-100 -100 1000 1200'))
        dwg.add(dwg.rect(insert=(self.FA), size=(self.dataObj.col_B, self.dataObj.col_L), fill='none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[(self.FA1), (self.FA2), (self.FA3), (self.FA4), (self.FA5), (self.FA6), (self.FA7), (self.FA8), (self.FA9), (self.FA10), (self.FA11), (self.FA12), (self.FA1)], stroke='blue', fill='none', stroke_width=2.5))

        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id="diagonalHatch", size=(6, 6), patternUnits="userSpaceOnUse", patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d="M -1,2 l 6,0", stroke='#000000', stroke_width=0.7))
        dwg.add(dwg.rect(insert=(self.FX), size=(self.dataObj.weld_thick, self.dataObj.weld_len), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FQ), size=(self.dataObj.plate_width, self.dataObj.plate_ht), fill='none', stroke='blue', stroke_width=2.5))

        dwg.add(dwg.rect(insert=(self.FX1), size=(self.dataObj.weld_thick, self.dataObj.weld_len), fill="url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col / 2
        bolt_r = self.dataObj.bolt_dia / 2
        pitchPts = []
        pitchPts1 = []
        for row in range(nr):
            colList = []
            colList1 = []
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
                colList.append(pt_other)
                colList1.append(pt)
            pitchPts.append(colList)
            pitchPts1.append(colList1)

        if nc > 1:
            gaugept1_other = np.array(pitchPts[-1][0])
            gaugept2_other = np.array(pitchPts[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outerArrow(dwg, gaugept1_other, gaugept2_other, str(int(self.dataObj.gauge)), params)

            faintpt1_other = gaugept1_other
            faintpt1_other1 = gaugept1_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_other = gaugept2_other
            faintpt2_other1 = gaugept2_other + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            self.dataObj.drawFaintLine(faintpt1_other, faintpt1_other1, dwg)
            self.dataObj.drawFaintLine(faintpt2_other, faintpt2_other1, dwg)

            gaugept1 = np.array(pitchPts1[-1][0])
            gaugept2 = np.array(pitchPts1[-1][1])
            params = {"offset": self.dataObj.col_L / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
            self.dataObj.draw_dimension_outerArrow(dwg, gaugept2, gaugept1, str(int(self.dataObj.gauge)), params)
            faintpt1 = gaugept1
            faintpt1_1 = gaugept1 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2 = gaugept2 + (self.dataObj.col_L / 2 + 30) * np.array([0, 1])
            faintpt2_1 = gaugept2
            self.dataObj.drawFaintLine(faintpt1, faintpt1_1, dwg)
            self.dataObj.drawFaintLine(faintpt2, faintpt2_1, dwg)

        ptList = []
        for row in pitchPts:
            if len(row) > 0:
                ptList.append(row[0])

        # End and Pitch Distance Information
        params = {"offset": self.dataObj.col_B / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[0]), np.array(ptList[-1]), str(len(ptList) - 1) + u' \u0040' + str(int(self.dataObj.pitch)) + "c/c", params)
        params = {"offset": self.dataObj.col_B / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.Q1 - self.dataObj.edge_dist * np.array([1, 0]), np.array(ptList[0]), str(int(self.dataObj.end_dist)), params)
        params = {"offset": self.dataObj.col_B / 2 + 30, "textoffset": 50, "lineori": "left", "endlinedim": 10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(ptList[-1]), self.Q1 - self.dataObj.edge_dist * np.array([1, 0]) + self.dataObj.plate_ht *
                                               np.array([0, 1]), str(int(self.dataObj.end_dist)), params)
        print "points for end dist:", np.array(ptList[-1]), self.Q1 - self.dataObj.edge_dist * np.array([1, 0]) + self.dataObj.plate_ht * np.array([0, 1])

        # Draw Faint Line
        pt1 = self.FQ1
        pt2 = pt1 + (self.dataObj.col_B / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
        pt3 = np.array(ptList[0])
        pt4 = pt3 + (self.dataObj.col_B / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt3, pt4, dwg)
        pt5 = np.array(ptList[-1])
        pt6 = pt5 + (self.dataObj.col_B / 2 + self.dataObj.edge_dist) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt5, pt6, dwg)
        pt7 = self.FQ1 + self.dataObj.plate_ht * np.array([0, 1])
        pt8 = pt7 + (self.dataObj.col_B / 2) * np.array([1, 0])
        self.dataObj.drawFaintLine(pt7, pt8, dwg)

        # Beam Information
        beam_pt = (self.FA8 + self.FA7) / 2
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + 50
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SW", offset, textUp, textDown, element="")

        # column  Information
        col_pt = self.FC
        theta = 45
        offset = 70
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " "
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown, element="")

        # Plate  Information
        beam_pt = self.FQ1 + self.dataObj.plate_ht * np.array([0, 1]) - self.dataObj.plate_width / 4 * np.array([1, 0])
        theta = 45
        offset = self.dataObj.plate_thick + self.dataObj.beam_B / 2 + 80
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) + 'x' + str(int(self.dataObj.plate_width)) + 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown, element="")

        # Bolt Information
        bltPtx = np.array(ptList[0])
        theta = 45
        offset = (self.dataObj.col_B - self.dataObj.plate_width) / 2 + self.dataObj.end_dist + 50
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M" + str(self.dataObj.bolt_dia) + " bolts (grade " + str(self.dataObj.bolt_grade) + ")"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp, textDown, element="")

        # Weld Information
        weldPt = self.FX + self.dataObj.weld_thick / 2 * np.array([1, 0])
        theta = 90
        offset = (self.dataObj.col_L - self.dataObj.D_beam) / 2 + self.dataObj.beam_T + self.dataObj.beam_R1 + 50
        textUp = "          z " + str(int(self.dataObj.weld_thick))
        textDown = ""  # u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown, element="weld")

        # 2D view name
        ptx = self.FA + 10 * np.array([1, 0]) + 950 * np.array([0, 1])
        dwg.add(dwg.text("Side view (Sec B-B)", insert=(ptx), fill='black', font_family="sans-serif", font_size=30))
        pty = ptx + 350 * np.array([1, 0])
        dwg.add(dwg.text("(All Dimensions are in mm)", insert=(pty), fill='black', font_family="sans-serif", font_size=30))

        dwg.save()
        dwg.fit()
        print "********** Column Flange Beam Web Side Saved  *************"
