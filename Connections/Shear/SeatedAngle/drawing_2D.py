'''
Created on 24-Aug-2015

@author: deepa
'''
import svgwrite
from svgwrite import mm
from PyQt4.QtCore import QString
import numpy as np
from numpy import math
# import cairosvg

class SeatCommonData(object):

    def __init__(self, inputObj, ouputObj, dictBeamdata, dictColumndata, dictangledata, folder):
        '''
        Provide all the data related to Finplate connection
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
        self.D_beam = int(dictBeamdata[QString("D")])
        self.D_col = int(dictColumndata[QString("D")])
        self.col_B = int(dictColumndata[QString("B")])
        self.beam_B = int(dictBeamdata[QString("B")])
        self.col_tw = float(dictColumndata[QString("tw")])
        self.beam_tw = float(dictBeamdata[QString("tw")])
        self.col_Designation = dictColumndata[QString("Designation")]
        self.beam_Designation = dictBeamdata[QString("Designation")]
        self.beam_R1 = float(dictBeamdata[QString("R1")])
        self.col_R1 = float(dictColumndata[QString("R1")])
        
        angle_l = ouputObj['SeatAngle']["Length (mm)"]
        angle_a = int(dictangledata[QString("A")])
        angle_b = int(dictangledata[QString("B")])
        angle_t = float(dictangledata[QString("t")])
        angle_r1 = float(dictangledata[QString("R1")])
        angle_r2 = float(dictangledata[QString("R2")])

        self.bolt_dia = inputObj["Bolt"]["Diameter (mm)"]
        self.grade = inputObj["Bolt"]["Grade"]
        self.connectivity = inputObj['Member']['Connectivity']
        self.pitch = ouputObj['Bolt']["Pitch Distance (mm)"]
        self.gauge = ouputObj['Bolt']["Gauge Distance (mm)"]
        self.end_dist = ouputObj['Bolt']["End Distance (mm)"]
        self.edge_dist = ouputObj['Bolt']["Edge Distance (mm)"]
        self.no_of_rows = ouputObj['Bolt']["No. of Row"]
        self.no_of_col = ouputObj['Bolt']["No. of Column"]
        self.col_L = 700
        self.beam_L = 350
        self.gap = 20  # Clear distance between Column and Beam as per subramanyam's book ,range 15-20 mm
        self.plate_pos_dist = self.beam_T + self.beam_R1 + 5 if self.beam_T + self.beam_R1 + 5 > 50 else  50  # Joints in Steel construction simple connections Publication P212,chapter no4 name: double angle web cleats
        self.beamToBeamDist = 10
        self.notch_L = (self.col_B - (self.col_tw + 40)) / 2.0
        self.notch_ht = self.col_T + self.col_R1

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
        emarker = dwg.marker(insert=(0, 3), size=(30, 20), orient="auto")
        emarker.add(dwg.path(d=" M0,3 L8,6 L5,3 L8,0 L0,3", fill='black'))
        dwg.defs.add(emarker)

        return emarker

    def drawStartArrow(self, line, s_arrow):
        line['marker-start'] = s_arrow.get_funciri()

    def drawEndArrow(self, line, e_arrow):
        line['marker-end'] = e_arrow.get_funciri()

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
        smarker = self.addSMarker(dwg)
        emarker = self.addEMarker(dwg)

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
        self.drawEndArrow(line, smarker)
        # self.drawStartArrow(line, emarker)
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width=2.5, linecap='butt'))
        self.drawEndArrow(line, smarker)
        # self.drawStartArrow(line, emarker)
        if(params["lineori"] == "right"):
            txtPt = B3 + params["textoffset"] * uUnit
        else:
            txtPt = A3 - (params["textoffset"] + 100) * uUnit

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
            txtPtUp = p3 + 0.2 * lengthB * labelVec + txtOffset * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec

        elif(orientation == "SE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - (txtOffset + 15) * offsetVec

        elif(orientation == "SW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + (txtOffset) * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec

        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill='none', stroke='black', stroke_width=2.5))

        emarker = self.addEMarker(dwg)
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

    def saveToSvg(self, fileName, view):

        '''
        It returns the svg drawing depending upon connectivity
        CFBW = Column Flange Beam Web
        CWBW = Column Web Beam Web
        BWBW = Beam Web Beam Web
        '''
        fin2DFront = Seat2DCreatorFront(self)
        fin2DTop = Seat2DCreatorTop(self)
        fin2DSide = Seat2DCreatorSide(self)

        if self.connectivity == 'Column flange-Beam web':
            if view == "Front":
                fin2DFront.callCFBWfront(fileName)
            elif view == "Side":
                fin2DSide.callCFBWSide(fileName)
            elif view == "Top":
                fin2DTop.callCFBWTop(fileName)
            else:
                fileName = str(self.folder) + '/images_html/finFront.svg'
                fin2DFront.callCFBWfront(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finFront.png')

#                 for n in range(1, 100, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/finFrontFB" + str(n) + ".svg"
#                         continue
#                 fin2DFront.callCFBWfront(fileName)
#                 base_front = os.path.basename(str(fileName))

                fileName = str(self.folder) + '/images_html/finSide.svg'
                fin2DSide.callCFBWSide(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finSide.png')

#                 for n in range(1, 100, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/finSideFB" + str(n) + ".svg"
#                         continue
#                 fin2DSide.callCFBWSide(fileName)
#                 base_side = os.path.basename(str(fileName))

                fileName = str(self.folder) + '/images_html/finTop.svg'
                fin2DTop.callCFBWTop(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finTop.png')
#                 for n in range(1, 100, 1):
#                     if (os.path.exists(fileName)):
#                         fileName = str(self.folder) + "/images_html/finTopFB" + str(n) + ".svg"
#                         continue
#                 fin2DTop.callCFBWTop(fileName)
#                 base_top = os.path.basename(str(fileName))

        elif self.connectivity == 'Column web-Beam web':
            if view == "Front":
                fin2DFront.callCWBWfront(fileName)
            elif view == "Side":
                fin2DSide.callCWBWSide(fileName)
            elif view == "Top":
                fin2DTop.callCWBWTop(fileName)
            else:
                fileName = str(self.folder) + '/images_html/finFront.svg'
                fin2DFront.callCWBWfront(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finFront.png')

                fileName = str(self.folder) + '/images_html/finSide.svg'
                fin2DSide.callCWBWSide(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finSide.png')

                fileName = str(self.folder) + '/images_html/finTop.svg'
                fin2DTop.callCWBWTop(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finTop.png')

        else:
            if view == "Front":
                fin2DFront.callBWBWfront(fileName)
            elif view == "Side":
                fin2DSide.callBWBWSide(fileName)
            elif view == "Top":
                fin2DTop.callBWBWTop(fileName)
            else:
                fileName = str(self.folder) + '/images_html/finFront.svg'
                fin2DFront.callBWBWfront(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finFront.png')
                fileName = str(self.folder) + '/images_html/finSide.svg'
                fin2DSide.callBWBWSide(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finSide.png')
                fileName = str(self.folder) + '/images_html/finTop.svg'
                fin2DTop.callBWBWTop(fileName)
                cairosvg.svg2png(file_obj=fileName, write_to=str(self.folder) + '/images_html/finTop.png')



#**************************************************************
class Seat2DCreatorTop(object):
    
    def __init__(self):
        pass


class Seat2DCreatorSide(object):
    
    def __init__(self):
        pass
           
class Seat2DCreatorFront(object):
    
    def __init__(self, seatCommonObj):
        
        self.dataObj = seatCommonObj
        self.beam_T = float(self.dataObj.dictBeamdata[QString("T")])
        self.col_T = float(self.dataObj.dictColumndata[QString("T")])
        self.D_beam = int (self.dataObj.dictBeamdata[QString("D")])
        self.D_col = int (self.dataObj.dictColumndata[QString("D")])
        self.col_B = int(self.dataObj.dictColumndata[QString("B")])
        self.col_tw = float(self.dataObj.dictColumndata[QString("tw")])
        beam_R1 = float(self.dataObj.dictBeamdata[QString("R1")])
        plate_ht= self.dataObj.ouputObj['Plate']['height'] 
        plate_width = self.dataObj.ouputObj['Plate']['width']
        weld_len = self.dataObj.ouputObj['Plate']['height']
        weld_thick =  self.dataObj.ouputObj['Weld']['thickness']
        self.bolt_dia  = self.dataObj.inputObj["Bolt"]["Diameter (mm)"]
        self.connectivity =  self.dataObj.inputObj['Member']['Connectivity']
        self.pitch = self.dataObj.ouputObj['Bolt']["pitch"]
        self.gauge = self.dataObj.ouputObj['Bolt']["gauge"]
        self.end_dist = self.dataObj.ouputObj['Bolt']["enddist"]
        self.edge_dist = self.dataObj.ouputObj['Bolt']["edge"]
        self.no_of_rows = self.dataObj.ouputObj['Bolt']["numofrow"] 
        self.no_of_col = self.dataObj.ouputObj['Bolt']["numofcol"]
        self.col_L = 1000
        self.beam_L = 500
        
        
        self.A2 =(self.col_B,(self.col_L-self.D_beam)/2)
        self.B = (self.col_B,0)
        self.A = (0,0)
        self.D = (0,self.col_L)
        self.C = (self.col_B,self.col_L)
        self.B2 = (self.col_B,(self.D_beam + self.col_L)/2)
        
        ptEx = (self.col_B-self.col_tw)/2
        ptEy = 0.0
        self.E = (ptEx,ptEy)
        ptHx = (self.col_B-self.col_tw)/2
        ptHy = self.col_L
        self.H = (ptHx,ptHy)
        ptFx = (self.col_B + self.col_tw)/2
        ptFy = 0
        self.F = (ptFx,ptFy)
        ptGx = (self.col_B + self.col_tw)/2
        ptGy = self.col_L
        self.G = (ptGx,ptGy)
        
        #Draw rectangle for finPlate PRSU
        ptPx = (self.col_B + self.col_tw)/2
        ptPy = ((self.col_L - self.D_beam)/2) + (self.beam_T + beam_R1 + 3)
        self.P = (ptPx,ptPy) 
        self.ptP = np.array([ptPx,ptPy])
        
        ptRx = ptPx + plate_width
        ptRy = ptPy
        self.R = (ptRx,ptRy)
        
        ptSx = ptRx
        ptSy = ptPy + plate_ht
        self.S = (ptSx,ptSy)
        
        self.plate_ht = plate_ht
        self.plate_width = plate_width
        self.weld_thick = weld_thick
        self.weld_len = weld_len
        # Draw Rectangle for weld
        ptCx1 = ((self.col_B + self.col_tw)/2 + 20)
        ptCy1 = ((self.col_L - self.D_beam)/2) + (self.beam_T + beam_R1 + 3)
        self.C1 =(ptCx1,ptCy1)
        
        ptAx1 = ptCx1
        ptAy1 = ((self.col_L - self.D_beam)/2)
        self.A1 = (ptAx1,ptAy1)
        
        ptAx3 = ptCx1 + self.beam_L
        ptAy3 = ptAy1
        self.A3 = (ptAx3,ptAy3)
        
        ptBx3 = ptAx3
        ptBy3 = ((self.col_L + self.D_beam)/2 ) 
        self.B3 = (ptBx3,ptBy3)
        
        ptBx1 = ptCx1
        ptBy1 = ptBy3
        self.B1 = (ptBx1,ptBy1)
        
        ptC2x= ptCx1
        ptC2y = ptCy1 + plate_ht
        self.C2 = (ptC2x,ptC2y)
        
        ptAx5 = ptAx1
        ptAy5 = ptAy1 + self.beam_T
        self.A5 = ptAx5,ptAy5
        
        ptAx4 = ptAx3
        ptAy4 = ptAy3 + self.beam_T
        self.A4 = (ptAx4,ptAy4)
        
        ptBx4 = ptBx3
        ptBy4 = ptBy3 - self.beam_T  
        self.B4 = (ptBx4,ptBy4)
        
        ptBx5 = ((self.col_B + self.col_tw)/2) + 20
        ptBy5 = ptBy3 - self.beam_T
        self.B5 = (ptBx5,ptBy5)
        
        ptP1x = ((self.col_B + self.col_tw)/2 + self.edge_dist)
        ptP1y = ((self.col_L - self.D_beam)/2 +(self.col_tw + beam_R1 + 3)+ self.end_dist)
        self.P1 = (ptP1x,ptP1y)
        
        ptP2x = ptP1x
        ptP2y = ptP1y + self.pitch
        self.P2 = (ptP1x,ptP1y)
        
        ptP3x = ptP1x
        ptP3y = ptP2y + self.pitch
        self.P3 = (ptP1x,ptP1y)
        
        ##### Column flange points for column flange beam web connectivity #####
        fromPlate_pt = self.D_col + 20 # 20 mm clear distance between colume and beam
        ptFAx = 0
        ptFAy = 0
        self.FA = (ptFAx,ptFAy)
         
        ptFEx = self.col_T
        ptFEy = 0.0
        self.FE =(ptFEx,ptFEy)
         
        ptFFx = self.D_col - self.col_T
        ptFFy = 0.0
        self.FF =(ptFFx,ptFFy)
         
        ptFBx = self.D_col 
        ptFBy = 0.0
        self.FB =(ptFBx,ptFBy)
         
        ptFCx = self.D_col
        ptFCy = self.col_L
        self.FC = (ptFBx,ptFCy)
         
        ptFGx = self.D_col - self.col_T
        ptFGy = self.col_L
        self.FG =(ptFGx,ptFGy)
         
        ptFHx = self.col_T
        ptFHy = self.col_L
        self.FH =(ptFHx,ptFHy)
         
        ptFDx = 0.0
        ptFDy = self.col_L
        self.FD =(ptFDx,ptFDy)
        
        ptFPx = self.D_col
        ptFPy = ((self.col_L - self.D_beam)/2) + (self.beam_T + beam_R1 + 3)
        self.FP = (ptFPx,ptFPy)
        self.ptFP = np.array([ptFPx,ptFPy])
        
        ptFC1x = ptFPx + 20
        ptFC1y = ptFPy
        self.FC1 = (ptFC1x,ptFC1y)
        
        #FC1
        ptFC1x = fromPlate_pt 
        ptFC1y = ((self.col_L - self.D_beam)/2) + (self.beam_T + beam_R1 + 3)
        self.FC1 = (ptFC1x, ptFC1y)
        
        #FC2
        ptFC2x = fromPlate_pt
        ptFC2y = ((self.col_L - self.D_beam)/2) +( self.beam_T + beam_R1 + 3) + self.plate_ht
        self.FC2 = (ptFC2x, ptFC2y)
        
        #FA1
        ptFA1x = fromPlate_pt
        ptFA1y = (self.col_L - self.D_beam)/2
        self.FA1 = ptFA1x, ptFA1y
        
        #FA4
        ptFA4x = fromPlate_pt
        ptFA4y = (self.col_L - self.D_beam)/2  + self.beam_T
        self.FA4 = ptFA4x, ptFA4y
        
        #FA2
        ptFA2x = ptFC1x + self.beam_L
        ptFA2y = ptFA1y
        self.FA2 = ptFA2x, ptFA2y
        
        #FA3
        ptFA3x = fromPlate_pt  + self.beam_L
        ptFA3y = (((self.col_L - self.D_beam)/2 ) + self.beam_T) 
        self.FA3 = ptFA3x, ptFA3y
        
        #FB3
        ptFB3x = fromPlate_pt + self.beam_L
        ptFB3y = ((self.col_L - self.D_beam)/2 + self.D_beam) - self.beam_T
        self.FB3 = (ptFB3x, ptFB3y)
        
        
        #FB2
        ptFB2x = fromPlate_pt + self.beam_L
        ptFB2y = (self.col_L -self.D_beam)/2 +  self.D_beam 
        self.FB2 = ptFB2x, ptFB2y
        
        #FB1
        ptFB1x = self.D_col + 20
        ptFB1y = (self.col_L - self.D_beam)/2 + self.D_beam 
        self.FB1 = ptFB1x, ptFB1y
        
        #FB4
        ptFB4x = fromPlate_pt
        ptFB4y = ((self.col_L - self.D_beam)/2 + self.D_beam) - self.beam_T
        self.FB4 = ptFB4x, ptFB4y
        
        # points for diamension
    
    def callBWBWfront(self):
        pass
            
    def callCFBWfront(self):
        dwg = svgwrite.Drawing('seatfront.svg', profile='full')
        smarker = dwg.marker(insert=(-2.5,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-10,0), (0,-3)], fill='black'))
        
        emarker = dwg.marker(insert=(2.5,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (10,0), (0,-3)], fill='black'))
        dwg.add(dwg.polyline(points = [(self.FA),(self.FB),(self.FC),(self.FD),(self.FA)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.line((self.FE),(self.FH)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FF),(self.FG)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.FC1),(self.FA1),(self.FA2),(self.FB2),(self.FB1),(self.FC2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
        dwg.add(dwg.line((self.FC1),(self.FC2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FA4),(self.FA3)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FB4),(self.FB3)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.plate_width, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.plate_width, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.weld_thick, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.0))
        nr = self.no_of_rows
        nc = self.no_of_col
        bolt_r = self.bolt_dia/2
        ptList = []
        
        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.ptFP + self.edge_dist * np.array([1,0]) + self.end_dist * np.array ([0,1]) + \
                    (i-1) * self.pitch * np.array([0,1]) + (j-1) * self.gauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
                ptE = self.ptFP + self.edge_dist * np.array([1,0]) +(j-1) * self.gauge * np.array([1,0])
                ptF = ptE + self.plate_ht * np.array([0,1])
                dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))   
                colList.append(pt)
            ptList.append(colList)
        
        dwg.save()
        print"Saved CFBWfront"
        
        
        
    def callCWBWfront(self):
        
        dwg = svgwrite.Drawing('seatfront.svg', profile='full')
        smarker = dwg.marker(insert=(-2.5,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-10,0), (0,-3)], fill='black'))
        
        emarker = dwg.marker(insert=(2.5,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (10,0), (0,-3)], fill='black'))
        
        dwg.add(dwg.polyline(points=[(self.A2),(self.B),(self.A),(self.D),(self.C) ,(self.B2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.E),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.F),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.rect(insert=(self.P), size=(self.plate_width, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.P), size=(self.weld_thick, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.0))
        #C1,A1,A3,B3,B1,C2
        dwg.add(dwg.polyline(points=[(self.C1),(self.A1),(self.A3),(self.B3),(self.B1),(self.C2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
        #C1,C2
        dwg.add(dwg.line((self.C1),(self.C2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        #A2,B2
        dwg.add(dwg.line((self.A2),(self.B2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.A5),(self.A4)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.B5),(self.B4)).stroke('blue',width = 2.5,linecap = 'square'))
        nr = self.no_of_rows
        nc = self.no_of_col
        bolt_r = self.bolt_dia/2
        ptList = []
        
        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.ptP + self.edge_dist * np.array([1,0]) + self.end_dist * np.array ([0,1]) + \
                    (i-1) * self.pitch * np.array([0,1]) + (j-1) * self.gauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
                ptE = self.ptP + self.edge_dist * np.array([1,0]) +(j-1) * self.gauge * np.array([1,0])
                ptF = ptE + self.plate_ht * np.array([0,1])
                dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))
                colList.append(pt)
            ptList.append(colList)
            
        pitchPts =[]
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
                
        for i in range (len( pitchPts)-1):
            params = {"offset": self.col_B + 10, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.draw_dimension_outerArrow(dwg, np.array(pitchPts[i]), np.array(pitchPts[i + 1]), str(self.pitch) + "mm", params)
              
                
        gaugePts = ptList[0]   
        for i in range (len( gaugePts)-1):
            params = {"offset": self.col_L + 10, "textoffset": 35, "lineori": "right", "endlinedim":10}
            self.draw_dimension_outerArrow(dwg, np.array(gaugePts[i]), np.array(gaugePts[i + 1]), str(self.gauge) + "mm", params)
                   
        dwg.defs.add(emarker)
        dwg.defs.add(smarker)
        
        ptBeam1 = self.P + 400 * np.array([1,0])
        ptBeam2 = ptBeam1 - 100 * np.array([0,1])
        ptBeam3 = ptBeam2 + 50 * np.array([1,0])
        ptBeam4 = ptBeam3 + 1 * np.array([1,0])
        
        line = dwg.add(dwg.polyline([(ptBeam1), (ptBeam2),(ptBeam3)],stroke='black', fill='none',stroke_width = 1.5))
        dwg.add(dwg.text('ISMB400', insert=(ptBeam4), fill='black'))
        line['marker-start'] = smarker.get_funciri()
        
        params = {"offset": 20, "textoffset": 15, "lineori": "right", "endlinedim":10}
        self.draw_dimension_outerArrow(dwg, np.array(self.B3), np.array(self.A3), str(self.D_beam) + "mm", params)
        
        params["lineori"] = "left"
        params["offset"] = self.col_B + 80
        params["textoffset"] = 60
        self.draw_dimension_outerArrow(dwg, np.array(self.S), np.array(self.R), str(self.plate_ht) + "mm", params)
        
        params = {"offset": 20, "textoffset": 10, "lineori": "right", "endlinedim":10,"arrowlen":50}
        ptA = (np.array(self.B1) + np.array(self.B3)) * 0.5
        ptB = (np.array(self.B5) + np.array(self.B4)) * 0.5
        self.draw_dimension_innerArrow(dwg, ptA, ptB, str(self.beam_T), params)
        
        dwg.save()
        print"Saved"
    
    
    

    
    
    