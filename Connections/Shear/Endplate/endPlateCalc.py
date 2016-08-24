
from numpy import float
import cmath;
import math
import sys;

from model import *
from PyQt4.Qt import QString
import logging
flag = 1
logger = None

def module_setup():
    
    global logger
    logger = logging.getLogger("osdag.endPlateCalc")

module_setup()

#FUNCTION DEFINITIONS---------------
# Function for net area of ordinary bolts
# Source: Subramanian's book, page: 348
def netArea_calc(dia):
    netArea = {5:15.3, 6:22.04, 8:39.18, 10:61.23, 12:84.5, 16:157, 20:245, 22:303, 24:353, 27:459, 30:561, 36:817};
    return netArea[dia]

# BOLT: determination of shear capacity of black bolt = fu * n * A / (root(3) * Y)
def black_bolt_shear(dia, n, fu):
    A = netArea_calc(dia)
    root3 = math.sqrt(3);
    Vs = fu * n * A / (root3 * 1.25 * 1000)
    Vs = round(Vs, 3)
    return Vs
    
# BOLT: determination of bearing capacity = 2.5 * kb * d * t * fu / Y
def bolt_bearing(dia, t, fu, beam_fu):
    # add code to determine kb if pitch, gauge, edge distance known
    if dia == 12 or dia == 14:
        dia_hole = dia + 1
    elif dia == 16 or dia == 18 or dia == 20 or dia == 22 or dia == 24:
        dia_hole = dia + 2
    else:
        dia_hole = dia + 3
    # minimum spacing
    min_pitch = int(2.5 * dia)
    min_gauge = int(2.5 * dia)
    min_end_dist = int(1.7 * dia_hole)
    # calculation of kb
    kbchk1 = min_end_dist / float(3 * dia_hole)
    kbchk2 = min_pitch / float(3 * dia_hole) - 0.25
    kbchk3 = fu / float(beam_fu)
    kbchk4 = 1
    kb = min(kbchk1, kbchk2, kbchk3, kbchk4)
    kb = round(kb, 3)
    Vb = 2.5 * kb * dia * t * fu / (1.25 * 1000);
    Vb = round(Vb, 3);
    return Vb;
# According to subramanyam page no 372
def end_plate_t_min(beam_depth, grade_bolt, dia):
    if beam_depth < 450:
        if grade_bolt <= 4.6:
            min_endplate = min(8, dia / 3)
        else:
            min_endplate = min(8, dia / 2)
    else:
        if grade_bolt <= 4.6:
            min_endplate = min(10, dia / 3)
        else:
            min_endplate = min(10, dia / 2)
    return min_endplate;

# BOLT: determination of shear capacity of black bolt = fu * n * A / (root(3) * Y)
# def black_bolt_shear(dia, n, fu):
#     A = math.pi * dia * dia * 0.25 * 0.78; #threaded area = 0.78 x shank area
#     root3 = math.sqrt(3);
#     Vs = fu * n * A / (root3 * 1.25 * 1000)
#     Vs = round(Vs,3)
#     return Vs


# BOLT: Determination of factored design force of HSFG bolts Vsf = Vnsf / Ymf = uf * ne * Kh * Fo where Vnsf: The nominal shear capacity of bolt
def HSFG_bolt_shear(uf, dia, n, fu):
    Anb = math.pi * dia * dia * 0.25 * 0.78  # threaded area(Anb) = 0.78 x shank area
    Fo = Anb * 0.7 * fu 
    Kh = 1  # Assuming fastners in Clearence hole
    Ymf = 1.25  # Ymf = 1.25 if Slip resistance is designed at ultimate load
    Vsf = uf * n * Kh * Fo / (Ymf * 1000)
    Vsf = round(Vsf, 3)
    return Vsf

############# CRITICAL BOLT SHEAR CAPACITY ###################
def critical_bolt_shear(load, eccentricity, pitch, gauge, bolts_one_line):
    sigma = 0.0
    r_y = 0.0
    r_x = 0.0
    moment = load / 2 * eccentricity
    n = int(bolts_one_line / 2)
    bolts_req = bolts_one_line
    if gauge == 0:
        if bolts_one_line % 2 == 0:
            r_y = (n - 0.5) * pitch
            for i in range(n):
                sigma = sigma + 2 * (i + 0.5) * (i + 0.5) * pitch * pitch
        else:
            r_y = n * pitch
            for i in range(n):
                sigma = sigma + 2 * (i + 1) * (i + 1) * pitch * pitch 
    else:
        bolts_req = 2 * bolts_one_line
        r_x = gauge / 2.0
        if bolts_one_line % 2 == 0:
            r_y = (n - 0.5) * pitch
            for i in range(n):
                sigma = sigma + 4 * (i + 0.5) * (i + 0.5) * pitch * pitch + 4 * r_x ** 2
        else:
            r_y = n * pitch
            for i in range(n):
                sigma = sigma + 4 * (i + 1) * (i + 1) * pitch * pitch + 4 * r_x ** 2
    shear_x = (moment * r_y) / sigma
    shear_y = (moment * r_x) / sigma + load / (2 * bolts_req)
    resultant = math.sqrt(shear_x ** 2 + shear_y ** 2)
    return resultant  


##################### Block shear capacity of plates/members ##########################333

def blockshear(numrow, numcol, dia_hole, fy, fu, edge_dist, end_dist, pitch, gauge, platethk):
    if numcol == 1:
        Avg = platethk * ((numrow - 1) * pitch + end_dist)
        Avn = platethk * ((numrow - 1) * pitch + end_dist - (numrow - 1 + 0.5) * dia_hole)
        Atg = platethk * edge_dist
        Atn = platethk * (edge_dist - 0.5 * dia_hole)
        
        Tdb1 = (Avg * fy / (math.sqrt(3) * 1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.1)
        Tdb = min (Tdb1, Tdb2)
        Tdb = round(Tdb / 1000, 3)
        
    elif numcol == 2:
        Avg = platethk * ((numrow - 1) * pitch + end_dist)
        Avn = platethk * ((numrow - 1) * pitch + end_dist - (numrow - 1 + 0.5) * dia_hole)
        Atg = platethk * (edge_dist + gauge)
        Atn = platethk * (edge_dist + gauge - 0.5 * dia_hole)
        
        Tdb1 = (Avg * fy / (math.sqrt(3) * 1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.1)
        Tdb = min (Tdb1, Tdb2)
        Tdb = round(Tdb / 1000, 3)
        
    return Tdb  






def endConn(uiObj):
    global logger
    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumSection']
    connectivity = uiObj['Member']['Connectivity']
    beam_fu = uiObj['Member']['fu (MPa)']
    beam_fy = uiObj['Member']['fy (MPa)']
              
    shear_load = uiObj['Load']['ShearForce (kN)']
                  
    bolt_dia = uiObj['Bolt']['Diameter (mm)']
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = uiObj['Bolt']['Grade']
              
    end_plate_t = uiObj['Plate']['Thickness (mm)']
    end_plate_w = uiObj['Plate']['Width (mm)']
    end_plate_l = uiObj['Plate']['Height (mm)']
    web_plate_fu = uiObj['Member']['fu (MPa)']
    web_plate_fy = uiObj['Member']['fy (MPa)']
    user_height = end_plate_l 
    user_width = end_plate_w      
    weld_t = uiObj["Weld"]['Size (mm)']
    weld_fu = 410

    bolt_planes = 1 
    dictbeamdata = get_beamdata(beam_sec)
    beam_w_t = float(dictbeamdata[QString("tw")])
    beam_f_t = float(dictbeamdata[QString("T")])
    beam_d = float(dictbeamdata[QString("D")])
    beam_R1 = float(dictbeamdata[QString("R1")])

    if connectivity == "Column web-Beam web" or connectivity == "Column flange-Beam web":
        dictcolumndata = get_columndata(column_sec)
        column_w_t = float(dictcolumndata[QString("tw")])
        column_f_t = float(dictcolumndata[QString("T")])
        column_R1 = float(dictcolumndata[QString("R1")])
        column_d = float(dictcolumndata[QString("D")])
        column_b = float(dictcolumndata[QString("B")])
    else:
        dictcolumndata = get_beamdata(column_sec)
        column_w_t = float(dictcolumndata[QString("tw")])
        column_f_t = float(dictcolumndata[QString("T")])
        column_R1 = float(dictcolumndata[QString("R1")])
        column_d = float(dictcolumndata[QString("D")])
        column_b = float(dictcolumndata[QString("B")])
    
    design_check = True

    
    sectional_gauge = 0.0
    gauge = 0.0
    pitch = 0.0
    eccentricity = 0.0
    dia_hole = 0
    bolt_shear_capacity = 0.0
     # Plate thickness check
    min_end_plate_t = end_plate_t_min(beam_d, bolt_grade, bolt_dia)
    if end_plate_t < min_end_plate_t:
        end_plate_t = min_end_plate_t
        design_check = False  
        logger.error(": Chosen end plate thickness is less than the minimum plate thickness [Refer Subramanyam page no. 372]")
        logger.warning(" : Minimum required thickness %2.2f mm" % (min_end_plate_t))
        logger.info(" : Increase Plate Thickness")
    
    
    ############## BOLT CAPACITY ###############
    
    # I: Check for number of bolts -------------------
    
    
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu;
    
    if connectivity == "Column web-Beam web":
        t_thinner = min(column_w_t.real, end_plate_t.real);
    elif connectivity == "Column flange-Beam web":
        t_thinner = min(column_f_t.real, end_plate_t.real);
    else:
        t_thinner = min(column_w_t.real, end_plate_t.real);
    
    if bolt_type == 'HSFG':
        
        bolt_shear_capacity = HSFG_bolt_shear(0.48, bolt_dia, 1, bolt_fu)
    else:
        bolt_shear_capacity = black_bolt_shear(bolt_dia, 1, bolt_fu)
    bolt_bearing_capacity = bolt_bearing(bolt_dia, t_thinner, beam_fu, beam_fu).real;
    
    bolt_capacity = min(bolt_shear_capacity, bolt_bearing_capacity);
    
    if shear_load != 0:
#                 bolts_required = int(math.ceil(shear_load/(2*bolt_capacity)))

        bolts_required = float(math.ceil(shear_load / bolt_capacity));  # changing no of bolts into multiple of 4
        if bolts_required <= 3:
            bolts_required = 4;
        elif bolts_required % 2 == 0:
            bolts_required = bolts_required;
        elif bolts_required % 2 != 0:
            bolts_required = bolts_required + 1
    else:
        bolts_required = 0
        while  bolts_required == 0:
            design_check = False  
            break
        
        
        
    
    # Spacing of bolts for web plate -------------------
    ######### According to IS 800 - 2007, table 9, clause no. 10.2.1 ##########################
    
    if bolt_dia == 12 or bolt_dia == 14:
        dia_hole = bolt_dia + 1
    elif bolt_dia == 16 or bolt_dia == 18 or bolt_dia == 20 or bolt_dia == 22 or bolt_dia == 24:
        dia_hole = bolt_dia + 2
    else:
        dia_hole = bolt_dia + 3    

    # Minimum/maximum pitch and gauge
    min_pitch = int(2.5 * bolt_dia);
    min_gauge = int(2.5 * bolt_dia);
    
    ########### MAX SPACING BETWEEN BOLTS #####################
    max_spacing = int(min(100 + 4 * end_plate_t, 200))  # clause 10.2.3.3 is800
    
    
    ############# END AND EDGE DISTANCES ###################
    min_edge_dist = int(1.7 * (dia_hole))
    min_end_dist = int(1.7 * (dia_hole))
    
    kbchk1 = min_end_dist / float(3 * dia_hole)
    kbchk2 = min_pitch / float(3 * dia_hole) - 0.25
    kbchk3 = bolt_fu / float(beam_fu)
    kbchk4 = 1
    kb = min(kbchk1, kbchk2, kbchk3, kbchk4)
    kb = round(kb, 3)
        
    max_edge_dist = int((12 * end_plate_t * cmath.sqrt(250 / beam_fy)).real) - 1;
    max_end_dist = int((12 * end_plate_t * cmath.sqrt(250 / beam_fy)).real) - 1;
    
    
    ####################################################### CHECK 1: DETAILING PRACTICE ###############################################################
    if end_plate_l != 0:
        no_row = (bolts_required / 2)
        no_col = 1
        avbl_length = (end_plate_l - 2 * min_end_dist)
        pitch = avbl_length / (no_row - 1)
        end_dist = min_end_dist
        edge_dist = min_edge_dist
        
        test = True
        if pitch < min_pitch:
            test = False
            no_col = 2
            if no_row % 2 == 0:
                no_row = no_row / 2
            else:
                no_row = (no_row + 1) / 2
            if no_row < 3:
                no_row = 2
            gauge = min_gauge
            if end_plate_w != 0:
                if (end_plate_w / 2 - edge_dist - gauge) > 70:
                    eccentricity = gauge / 2 + 70
                    edge_dist = end_plate_w / 2 - (70 + gauge)
                else:
                    eccentricity = (end_plate_w / 2 - edge_dist - gauge / 2)
            else:
                eccentricity = gauge / 2 + 50
                
            pitch = avbl_length / (no_row - 1)
        else:
            gauge = 0
            if end_plate_w != 0:
                if (end_plate_w / 2 - edge_dist - gauge) > 70:
                    eccentricity = gauge / 2 + 70
                    edge_dist = end_plate_w / 2 - (70 + gauge)
                else:
                    eccentricity = (end_plate_w / 2 - edge_dist - gauge / 2)
            else:
                eccentricity = gauge / 2 + 50            
                
            no_col = 1            
        ############################ check critical bolt shear capacity #######################
                      
        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
        if crit_shear > bolt_capacity :
            if no_col == 1:
                while crit_shear > bolt_capacity and pitch > min_pitch:
                    no_row = no_row + 1
                    pitch = avbl_length / (no_row - 1)
                    crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                if pitch < min_pitch:
                    no_col = 2
                elif bolt_capacity > crit_shear and pitch > min_pitch:
                    pass    
                
            if no_col == 2:  # Call math.ceil(x)
                if test == True:
                    if no_row % 2 == 0:
                        no_row = no_row / 2
                    else:
                        no_row = (no_row + 1) / 2
                if no_row == 1:
                    no_row = 2
                pitch = avbl_length / (no_row - 1)
                gauge = min_gauge
                if end_plate_w != 0:
                    if (end_plate_w / 2 - edge_dist - gauge) > 70:
                        eccentricity = gauge / 2 + 70
                        edge_dist = end_plate_w / 2 - (70 + gauge)
                    else:
                        eccentricity = (end_plate_w / 2 - edge_dist - gauge / 2)
                else:
                    eccentricity = gauge / 2 + 50
                crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row) 
                if crit_shear > bolt_capacity :
                    
                    while crit_shear > bolt_capacity and pitch > min_pitch:
                        no_row = no_row + 1
                        pitch = avbl_length / (no_row - 1)
                        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                    if pitch < min_pitch:
                        design_check = False
                        logger.error(": Shear force on critical bolt due to external load is more than bolt capacity")
                        logger.warning(": Bolt capacity of the critical bolt is %2.2f" % (bolt_capacity))
                        logger.info(": Increase the diameter of the bolt or bolt grade")
            
                    elif bolt_capacity > crit_shear and pitch > min_pitch:
                        pass       
        
        min_end_plate_l = 2 * min_end_dist + (no_row - 1) * min_pitch
        max_end_plate_l = beam_d - 2 * (beam_f_t + beam_R1)
        ############# check end plate length #################
#         if end_plate_l > max_end_plate_l:
#             design_check = False
#             logger.error(": Given end plate length exceeds the depth of the beam")
#             logger.warning(": The maximum permissible end plate length is %2.2f" %(max_end_plate_l))
#             logger.info(": Increase the beam Section or decrease length of end plate")
#         if end_plate_l < min_end_plate_l:
#             design_check = False
#             logger.error(": Given end plate length is less than minimum end plate length")
#             logger.warning(": The minimum end plate length is %2.2f" %(min_end_plate_l))
#             logger.info(": Increase the beam Section or decrease length of end plate")
            
        ############ check end plate width ###################
        
        if connectivity == "Column web-Beam web":
            max_end_plate_w = column_d - 2 * (column_f_t + column_R1)
        elif connectivity == "Column flange-Beam web":
            max_end_plate_w = column_b
        else:
            pass
        if end_plate_w != 0:
            sectional_gauge = end_plate_w - 2 * (min_edge_dist + gauge)
            min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            if sectional_gauge < 90:
                design_check = False
                logger.error(": Cross center distance between the bolt lines on either side of the beam is less than specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Minimum required cross center gauge is 90 mm")
                logger.info(": Increase the plate width")
                
            if sectional_gauge > 140:
                design_check = False
                logger.error(": Cross center distance between the bolt lines on either side of the beam is greater than specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Maximum required cross center gauge is 140 mm")
                logger.info(": Decrease the plate width")
                
#             if end_plate_w > max_end_plate_w:
#                 design_check = False
#                 logger.error(": Width of plate exceeds the width of column")
                
            
        if end_plate_w == 0:
            min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            end_plate_w = min_end_plate_w
            sectional_gauge = 100
            
            if connectivity != "Beam-Beam":
                if min_end_plate_w > max_end_plate_w:
                    design_check = False
                    logger.error(": Calculated width of end plate exceeds the width of the column")
                    logger.warning(": Minimum end plate width is %2.2f" % (min_end_plate_w))
                
                
    else:
        
        
        no_row = bolts_required / 2
        no_col = 1
         
        end_plate_l = (no_row - 1) * min_pitch + 2 * min_end_dist
        pitch = min_pitch
        max_end_plate_l = beam_d - 2 * (beam_f_t + beam_R1)
        end_dist = min_end_dist
        edge_dist = min_edge_dist
        test = True
        if end_plate_l > max_end_plate_l:
            test = False
            no_col = 2
            if no_row % 2 == 0:
                no_row = no_row / 2
            else:
                no_row = (no_row + 1) / 2
            if no_row < 2:
                no_row = 2
                
            if end_plate_w != 0:
                if (end_plate_w / 2 - edge_dist - gauge) > 70:
                    eccentricity = gauge / 2 + 70
                    edge_dist = end_plate_w / 2 - (70 + gauge)
                else:
                    eccentricity = (end_plate_w / 2 - edge_dist - gauge / 2)
            else:
                eccentricity = gauge / 2 + 50
        else:
            no_col = 1
            gauge = 0
            if end_plate_w != 0:
                if (end_plate_w / 2 - edge_dist - gauge) > 70:
                    eccentricity = gauge / 2 + 70
                    edge_dist = end_plate_w / 2 - (70 + gauge)
                else:
                    eccentricity = (end_plate_w / 2 - edge_dist - gauge / 2)
            else:
                eccentricity = gauge / 2 + 50 
     ################################################ check critical bolt shear capacity ################################################3
        if shear_load != 0:
            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)

            if crit_shear > bolt_capacity :
                if no_col == 1:
                    while crit_shear > bolt_capacity and end_plate_l < max_end_plate_l:
                        no_row = no_row + 1
                        end_plate_l = end_plate_l + pitch
                        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                    if end_plate_l > max_end_plate_l:
                        no_col = 2
                    elif bolt_capacity > crit_shear and end_plate_l < max_end_plate_l:
                        pass   
                     
                if no_col == 2:  # Call math.ceil(x)
                    if test == True:
                        test = False
                        if no_row % 2 == 0:
                            no_row = no_row / 2
                        else:
                            no_row = (no_row + 1) / 2
                    if no_row == 1:
                        no_row = 2
                        
                    end_plate_l = (no_row - 1) * min_pitch + 2 * min_end_dist
                    gauge = min_gauge
                    if end_plate_w != 0:
                        if (end_plate_w / 2 - edge_dist - gauge) > 70:
                            eccentricity = gauge / 2 + 70
                            edge_dist = end_plate_w / 2 - (70 + gauge)
                        else:
                            eccentricity = (end_plate_w / 2 - edge_dist - gauge / 2)
                    else:
                        eccentricity = gauge / 2 + 50
                    crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                    if crit_shear > bolt_capacity :
                         
                        while crit_shear > bolt_capacity and end_plate_l < max_end_plate_l:
                            no_row = no_row + 1
                            end_plate_l = end_plate_l + pitch
                            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                        if end_plate_l > max_end_plate_l:
                            design_check = False
                            logger.error(": Shear force on critical bolt due to external load is more than bolt capacity")
                            logger.warning(": Bolt capacity of the critical bolt is %2.2f" % (bolt_capacity))
                            logger.info(": Increase the diameter of the bolt or bolt grade")
                        elif bolt_capacity > crit_shear and end_plate_l <= max_end_plate_l:
                            pass      
        else:
            crit_shear = 0  
                    
        ############################# check end plate length ##########################################
        
        if end_plate_l < 0.6 * beam_d:
            end_plate_l = 0.6 * beam_d
            end_dist = (end_plate_l - (no_row - 1) * pitch) / 2
    
        ############################# check end plate width ##########################################
        if connectivity == "Column web-Beam web":
            max_end_plate_w = column_d - 2 * (column_f_t + column_R1)
        elif connectivity == "Column flange-Beam web":
            max_end_plate_w = column_b
        else:
            pass
        if end_plate_w != 0:
            sectional_gauge = end_plate_w - 2 * (min_edge_dist + gauge)
            min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            if sectional_gauge < 90:
                design_check = False
                logger.error(": Cross center distance between the bolt lines on either side of the beam is less than specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Minimum required cross center gauge is 90 mm")
                logger.info(": Increase the plate width")
                
            if sectional_gauge > 140:
                design_check = False
                logger.error(": Cross center distance between the bolt lines on either side of the beam is greater than specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Maximum required cross center gauge is 140 mm")
#                 
#             if end_plate_w > max_end_plate_w:
#                 design_check = False
#                 logger.error(": Width of plate exceeds the width of column")
                
            
        if end_plate_w == 0:
            min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            end_plate_w = min_end_plate_w
            sectional_gauge = 100
            if connectivity != "Beam-Beam":
            
                if min_end_plate_w > max_end_plate_w:
                    design_check = False
                    logger.error(": Calculated width of end plate exceeds the width of the column")
                    logger.warning(": Minimum end plate width is %2.2f mm" % (min_end_plate_w))      
        
    ################# CHECK 2: SHEAR CAPACITY OF BEAM WEB ####################
    
    shear_capacity_beam = 0.6 * beam_fy * 0.9 * end_plate_l * beam_w_t / 1000
    
    if shear_load > shear_capacity_beam:
        design_check = False
        logger.error(": Shear capacity of the beam web at the end plate is less than the external load")
        logger.warning(": The shear capacity of the beam web is %2.2f KN" % (shear_capacity_beam))
        logger.info(": Increase the end plate height if given else increase the beam section")
    
    ################# CHECK 3: BLOCK SHEAR ####################
    
    Tdb = blockshear(no_row, no_col, dia_hole, beam_fy, beam_fy, min_edge_dist, end_dist, pitch, gauge, end_plate_t)
    
    if Tdb < shear_load:
        design_check = False
        logger.error(": The block shear capacity of the plate is less than the applied shear force [cl. 6.4.1]")
        logger.warning(": Minimum block shear capacity required is % 2.2f KN" % (shear_load))
        logger.info(": Increase the plate thickness")
    
    ################# CHECK 4: FILLET WELD ####################
    
    # V: Weld shear strength -------------------
#     weld_l = (shear_load* 1000)/float(158*2*weld_t);
#     weld_l = round(weld_l,3)
#     if weld_l > end_plate_l:
#         weld_l = end_plate_l
#     else:
#         None
    weld_l = end_plate_l - 2 * weld_t
    Vy1 = (shear_load) / float(2 * weld_l);
    Vy1 = round(Vy1, 3)
    weld_strength = 0.7 * weld_t * weld_fu / (math.sqrt(3) * 1250);
    weld_strength = round(weld_strength, 3); 
    if Vy1 > weld_strength:
        design_check = False
        logger.error(": Weld Strength is less than the Shear Demand [cl. 10.5.9]")
        logger.warning(": Weld Strength should be greater than %2.2f KN/mm" % (weld_strength))
        logger.info(": Increase the Weld Size")
    
    # End of calculation
    outputObj = {}
    outputObj['Bolt'] = {}
    outputObj['Bolt']['status'] = True
    outputObj['Bolt']['shearcapacity'] = bolt_shear_capacity
    outputObj['Bolt']['bearingcapacity'] = bolt_bearing_capacity
    outputObj['Bolt']['boltcapacity'] = bolt_capacity
    outputObj['Bolt']['numofbolts'] = int(2 * no_col * no_row)
    outputObj['Bolt']['boltgrpcapacity'] = float(bolt_capacity * 2 * no_col * no_row)
    outputObj['Bolt']['numofrow'] = int(no_row)
    outputObj['Bolt']['numofcol'] = int(2 * no_col)
    outputObj['Bolt']['pitch'] = float(pitch)
    outputObj['Bolt']['enddist'] = float(end_dist)
    outputObj['Bolt']['edge'] = float(edge_dist)
    outputObj['Bolt']['gauge'] = float(gauge)
    outputObj['Bolt']['thinner'] = float(t_thinner)
    outputObj['Bolt']['dia_hole'] = float(dia_hole)
    outputObj['Bolt']['bolt_fu'] = float(bolt_fu)
    outputObj['Bolt']['bolt_fy'] = float(bolt_fy)
    outputObj['Bolt']['critshear'] = round(crit_shear, 3)
    outputObj['Bolt']['kb'] = float(kb)

    
     
    outputObj['Weld'] = {}
    outputObj['Weld']['weldshear'] = Vy1
    outputObj['Weld']['weldlength'] = weld_l
    outputObj['Weld']['weldstrength'] = weld_strength
     
    outputObj['Plate'] = {}
    outputObj['Plate']['Height'] = float(end_plate_l)
    outputObj['Plate']['Width'] = float(end_plate_w)
    outputObj['Plate']['MinThick'] = float(min_end_plate_t)
    outputObj['Plate']['MinWidth'] = float(min_end_plate_w)
    outputObj['Plate']['blockshear'] = float(Tdb)
    outputObj['Plate']['Sectional Gauge'] = float(sectional_gauge)
    
    
    # return outputObj
    
    if bolts_required == 0 :
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                outputObj[k][key] = ""
                
    if design_check == False:
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                outputObj[k][key] = ""   
                        
#     outputObj = {}
    if  outputObj['Bolt']['status'] == True:
        
        logger.info(": Overall endplate connection design is safe \n")
        logger.debug(" :=========End Of design===========")
        
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")
    
    return outputObj
    




