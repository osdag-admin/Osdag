'''
Created on 17-Mar-2016

@author: Subhrajit
'''
# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from model import *
from Connections.connection_calculations import ConnectionCalculations
import math
import logging
flag = 1
logger = None


def module_setup():
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")
module_setup()

# Function for net area of ordinary bolts
# Source: Subramanian's book, page: 348


def netArea_calc(dia):
    '''

    Args:
        dia (int) diameter of bolt

    Returns:
        Net area of bolts at threaded portion (Ref. Table 5.11 Subramanian's book, page: 358 )

    '''
    netArea = {12:84.5, 16:157, 20:245, 22:303, 24:353, 27:459, 30:561, 36:817};
    return netArea[dia]

# BOLT: determination of shear capacity 


def bolt_shear(dia, n, fu):
    '''

    Args:
        dia (int) diameter of bolt
        n (str) number of shear plane(s) through which bolt is passing
        fu (float) ultimate tensile strength of a bolt

    Returns:
        Shear capacity of bearing type bolt in kN

    '''
    A = netArea_calc(dia)
    root3 = math.sqrt(3)
    Vs = fu * n * A / (root3 * 1.25 * 1000)
    Vs = round(Vs.real, 3)
    return Vs


def bolt_bearing(dia, t, kb, fu):
    '''

    Args:
        dia (int) diameter of bolt
        t (float) summation of thickneses of the connected plates experencing bearing stress in same direction, or if the bolts are countersunk, the thickness of plate minus 1/2 of the depth of countersunk
        kb (float) multiplying factor (Ref: Cl 10.3.4 IS 800:2007)
        fu (float) ultimate tensile strength of a bolt

    Returns:
        Bearing capacity of bearing type bolt in kN

    '''
    Vb = 2.5 * kb * dia * t * fu / (1.25 * 1000)
    Vb = round(Vb.real, 3)
    return Vb


# PLATE HEIGHT: minimum height of fin plate
# [Source: INSDAG detailing manual, page: 5-7] 
def fin_min_h(beam_d):
    '''

    Args:
        beam_d (float) Depth of beam

    Returns:
        Minimum height of fin plate depending on depth of beam

    '''
    min_plate_ht = 0.6 * beam_d;
    return min_plate_ht;

# PLATE THICKNESS: minimum thickness of fin plate
# [Source: Subramanian's book, page: 373]


def fin_min_thk(shear_load, beam_fy, web_plate_l):
    '''

    Args:
        shear_load (float) Factored shear force/load
        beam_fy (float) Yeild stress of beam material
        web_plate_l: Height of fin plate

    Returns:
        Minimum thickness of fin plate based on shear load and fin plate height

    '''
    min_plate_thk = (5 * shear_load * 1000) / (beam_fy * web_plate_l)
    return min_plate_thk;

# PLATE THICKNESS: maximum thickness of fin plate
# [Source: INSDAG detailing manual, page: 5-7]


def fin_max_thk(bolt_dia):
    '''

    Args:
        bolt_dia (int) diameter of bolt

    Returns:
        Maximum thickness of fin plate depending on diameter of bolt

    '''
    max_plate_thk = 0.5 * bolt_dia
    return max_plate_thk

# Function for block shear capacity calculation


def blockshear(numrow, numcol, dia_hole, fy, fu, edge_dist, end_dist, pitch, gauge, thk):
    '''

    Args:
        numrow (str) Number of row(s) of bolts
        numcol (str) Number of column(s) of bolts
        dia_hole (int) diameter of hole (Ref. Table 5.6 Subramanian's book, page: 340)
        fy (float) Yeild stress of material
        fu (float) Ultimate stress of material
        edge_dist (float) edge distance based on diameter of hole
        end_dist (float) end distance based on diameter of hole
        pitch (float) pitch distance based on diameter of bolt
        gauge (float) pitch distance based on diameter of bolt
        thk (float) thickness of plate

    Returns:
        Capacity of fin plate under block shear

    '''
    if numcol == 1:
        Avg = thk * ((numrow - 1) * pitch + end_dist)
        Avn = thk * ((numrow - 1) * pitch + end_dist - (numrow - 1 + 0.5) * dia_hole)
        Atg = thk * edge_dist
        Atn = thk * (edge_dist - 0.5 * dia_hole)

        Tdb1 = (Avg * fy / (math.sqrt(3) * 1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.1)
        Tdb = min(Tdb1, Tdb2)
        Tdb = round(Tdb / 1000, 3)

    elif numcol == 2:
        Avg = thk * ((numrow - 1) * pitch + end_dist)
        Avn = thk * ((numrow - 1) * pitch + end_dist - (numrow - 1 + 0.5) * dia_hole)
        Atg = thk * (edge_dist + gauge)
        Atn = thk * (edge_dist + gauge - 0.5 * dia_hole)

        Tdb1 = (Avg * fy / (math.sqrt(3) * 1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3) * 1.25) + Atg * fy / 1.1)
        Tdb = min(Tdb1, Tdb2)
        Tdb = round(Tdb / 1000, 3)

    return Tdb

### Check for shear yeilding ###

def shear_yeilding_b(A_v, beam_fy):
    '''

    Args:
        A_v (float) Area under shear
        beam_fy (float) Yeild stress of beam material

    Returns:
        Capacity of beam web in shear yeiding

    '''
    V_p = ( 0.6 * A_v * beam_fy ) / ( math.sqrt(3) * 1.10 * 1000 ) # kN
    return V_p

### Check for shear rupture ###

def shear_rupture_b(A_vn, beam_fu ):
    '''

    Args:
        A_vn (float) Net area under shear
        beam_fu (float) Ultimate stress of beam material

    Returns:
        Capacity of beam web in shear rupture

    '''
    R_n = (0.6 * beam_fu * A_vn) / 1000  #kN
    return R_n




def fetchBeamPara(self):
    beam_sec = self.ui.combo_Beam.currentText()
    dictbeamdata = get_beamdata(beam_sec)
    return dictbeamdata


def fetchColumnPara(self):
    column_sec = self.ui.comboColSec.currentText()
    loc = self.ui.comboConnLoc.currentText()
    if loc == "Beam-Beam":
        dictcoldata = get_beamdata(column_sec)
    else:
        dictcoldata = get_columndata(column_sec)
    return dictcoldata
##################################################################################
# Start of main program


def finConn(uiObj):

    global logger
    global design_status
    design_status = True
    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumSection']
    connectivity = uiObj['Member']['Connectivity']
    column_fu = float(uiObj['Member']['fu (MPa)'])
    column_fy = float(uiObj['Member']['fy (MPa)'])
    beam_fu = float(uiObj['Member']['fu (MPa)'])
    beam_fy = float(uiObj['Member']['fy (MPa)'])


    shear_load = float(uiObj['Load']['ShearForce (kN)'])

    bolt_dia = int(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = float(uiObj['Bolt']['Grade'])
    bolt_fu = float(uiObj["bolt"]["bolt_fu"])
    gap = float(uiObj["detailing"]["gap"])
    mu_f = float(uiObj["bolt"]["slip_factor"])
    gamma_mw = float(uiObj["weld"]["safety_factor"])
    dp_bolt_hole_type = str(uiObj['bolt']['bolt_hole_type'])
    dia_hole = int(uiObj['bolt']['bolt_hole_clrnce'])+ bolt_dia
    weld_type = uiObj['weld']['typeof_weld']
    weld_fu = float(uiObj["weld"]["fu_overwrite"])

    web_plate_t = float(uiObj['Plate']['Thickness (mm)'])
    web_plate_w = str(uiObj['Plate']['Width (mm)'])
    if web_plate_w == '':
        web_plate_w  = 0
    else:
        web_plate_w =  float(web_plate_w)

    web_plate_l = str(uiObj['Plate']['Height (mm)'])
    if web_plate_l == '':
        web_plate_l = 0
    else:
        web_plate_l = float(web_plate_l)

    web_plate_fu = float(uiObj['Member']['fu (MPa)'])
    web_plate_fy = float(uiObj['Member']['fy (MPa)'])

    weld_t = float(uiObj["Weld"]['Size (mm)'])

    old_beam_section = get_oldbeamcombolist()
    old_col_section = get_oldcolumncombolist()

    if beam_sec in old_beam_section or column_sec in old_col_section:
        logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")

    if beam_fu < 410 or beam_fy < 230 or column_fu < 410 or column_fy < 230:
        logger.warning(" : You are using a section of grade that is not available in latest version of IS 2062")


    #####################################################################################

# Hard-code input data required to check overall calculation as independent file  
#     beam_sec = 'ISMB300'    # Secondary beam
#     column_sec = 'ISMB500'  # Primary beam
#     connectivity = "Column flange-Beam web"
#     beam_fu = 410
#     beam_fy = 250
#     beam_w_t = 8.9
#     beam_d = 400
#     beam_f_t = 16
#     beam_R1 = 14   #     PBeam_T = 17.2
#     PBeam_R1 = 17
#     shear_load = 140
#     bolt_dia = 20
#     bolt_type  = 'Friction Grip Bolt'
#     bolt_grade = 8.8
#     web_plate_t = 10
#     web_plate_w = 100
#     web_plate_l = 300
#     web_plate_fu = 410
#     web_plate_fy = 250
#     weld_t = 8
#     weld_fu = 410
#     bolt_planes = 1 
##################################################################################
    # Read input values from Beam/Column database

    if connectivity == "Beam-Beam":
        dictbeamdata = get_beamdata(beam_sec)
        dictcolumndata = get_beamdata(column_sec)
    else:
        dictbeamdata = get_beamdata(beam_sec)
        dictcolumndata = get_columndata(column_sec)

    beam_w_t = float(dictbeamdata["tw"])
    beam_f_t = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_R1 = float(dictbeamdata["R1"])
    PBeam_T = float(dictcolumndata["T"])
    PBeam_w_t = float(dictcolumndata["tw"])
    PBeam_R1 = float(dictcolumndata["R1"])
    column_w_t = float(dictcolumndata["tw"])
    column_f_t = float(dictcolumndata["T"])

    if connectivity == "Beam-Beam":
        notch_ht = max([PBeam_T, beam_f_t]) + max([PBeam_R1, beam_R1]) + max([(PBeam_T / 2), (beam_f_t / 2), 10])
        if notch_ht < (beam_d/5):
            pass
        else:
            logger.warning(" : Depth of coping should preferably be less than D/5 (D = Secondary beam depth)")
    ########################################################################
    # INPUT FOR PLATE DIMENSIONS (FOR OPTIONAL INPUTS) AND VALIDATION

    # Plate thickness check
    if web_plate_t < beam_w_t:
        design_status = False
        logger.error(": Chosen fin plate thickness is not sufficient")
        logger.warning(" : Minimum required thickness of fin plate is %2.2f mm" % beam_w_t)
        logger.info(": Increase the thickness of fin plate")

    # # Plate height check

    # Maximum plate height for Column-Beam connectivity (Note: # 5 mm extra gap is provided from top and bottom)
    if connectivity == "Column flange-Beam web" or connectivity == "Column web-Beam web":
        max_plate_height = beam_d - 2 * beam_f_t - 2 * beam_R1 - 2 * 5
    # Maximum plate height for Beam-Beam connectivity
    elif connectivity == "Beam-Beam":
        max_plate_height = beam_d - beam_f_t - beam_R1 - PBeam_T - PBeam_R1 - 5
    max_plate_height = round(max_plate_height, 3)

    # Minimum plate height (valid for all connectivity)
    min_plate_height = fin_min_h(beam_d);
    min_plate_height = round(min_plate_height, 3)

    # Plate height input and check for maximum and minimum values

    if web_plate_l != 0:
        if web_plate_l > max_plate_height :
            if connectivity == "Beam-Beam":
                design_status = False
                logger.error(": Height of the plate is more than the clear depth of the secondary beam")
                logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height)) 
                logger.info(": Reduce the plate height")
            else:
                design_status = False
                logger.error(": Height of the plate is more than the clear depth of the beam")
                logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height)) 
                logger.info(": Reduce the plate height")
                  
        elif min_plate_height > max_plate_height:
            if connectivity == "Beam-Beam":
                design_status = False
                logger.error(": Minimum required plate height is more than the clear depth of the secondary beam")
                logger.warning(": Plate height required should be more than  %2.2f mm " % (min_plate_height))
                logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height))
                logger.info(": Increase the plate height")
            else:
                design_status = False
                logger.error(": Minimum plate height required is more than the clear depth of the beam")
                logger.warning(": Plate height required should be more than  %2.2f mm " % (min_plate_height))
                logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height))
                logger.info(": Increase the plate height")
                
        elif min_plate_height >= web_plate_l:
            design_status = False
            logger.error(": Plate height provided is less than the minimum required ")
            logger.warning(": Plate height required should be more than  %2.2f mm " % (min_plate_height))
            logger.info(": Increase the plate height")
        
    
    ########################################################################
    # Bolt design function
    def boltDesign(web_plate_l):
        # I: Check for number of bolts -------------------
        bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu
         
        # Spacing of bolts for web plate -------------------
        # if bolt_dia == 12 or bolt_dia == 14:
        #     dia_hole = bolt_dia + 1
        # # elif bolt_dia == 16 or bolt_dia == 18 or bolt_dia == 20 or bolt_dia == 22 or bolt_dia == 24:
        # elif bolt_dia == 16 or bolt_dia == 20 or bolt_dia == 24:
        #     dia_hole = bolt_dia + 2
        # else:
        #     dia_hole = bolt_dia + 3
     
        # Minimum spacing
        min_pitch = int(2.5 * bolt_dia)
        min_gauge = int(2.5 * bolt_dia)
        if uiObj["detailing"]["typeof_edge"] == "a - Sheared or hand flame cut":
            min_end_dist = int(float(1.7 * (dia_hole)))
        else:
            min_end_dist = int(1.5 * (dia_hole))
        min_edge_dist = min_end_dist

         
        # Calculation of kb
        kbChk1 = min_end_dist / float(3 * dia_hole)
        kbChk2 = min_pitch / float(3 * dia_hole) - 0.25
        kbChk3 = bolt_fu / float(beam_fu)
        kbChk4 = 1
        kb = min(kbChk1, kbChk2, kbChk3, kbChk4)
        kb = round(kb, 3)
         
        # Bolt capacity calculation
        t_thinner = min(beam_w_t, web_plate_t.real)
        bolt_planes = 1
        if bolt_type == 'Bearing Bolt':
            bolt_shear_capacity = bolt_shear(bolt_dia, bolt_planes,bolt_fu)
            bolt_bearing_capacity = bolt_bearing(bolt_dia, t_thinner, kb, beam_fu)
            bolt_capacity = min(bolt_shear_capacity, bolt_bearing_capacity)

        elif bolt_type == 'Friction Grip Bolt':
            muf = mu_f
            bolt_hole_type = dp_bolt_hole_type # 1 for standard, 0 for oversize hole
            n_e = 1 # number of effective surfaces offering fricitonal resistance
            bolt_shear_capacity = ConnectionCalculations.bolt_shear_friction_grip_bolt(bolt_dia,bolt_fu,muf,n_e,bolt_hole_type)
            bolt_bearing_capacity = 'N/A'
            bolt_capacity = bolt_shear_capacity


        if shear_load != 0:
            bolts_required = int(math.ceil(shear_load / bolt_capacity)) # + 1

        else:
            bolts_required = int(shear_load / bolt_capacity)
            
        if bolts_required > 0 and  bolts_required <= 2 :
            bolts_required = 3
         
        # Bolt group capacity
        bolt_group_capacity = bolts_required * bolt_capacity
         
        if min_pitch % 10 != 0 or min_gauge % 10 != 0:
            min_pitch = (min_pitch / 10) * 10 + 10
            min_gauge = (min_gauge / 10) * 10 + 10
        else:
            min_pitch = min_pitch
            min_gauge = min_gauge

        # clause 10.2.2 is800
        max_spacing = int(min(100 + 4 * t_thinner, 200))  # clause 10.2.3.3 is800

        if min_end_dist % 10 != 0:
            min_end_dist = (min_end_dist / 10) * 10 + 10
            min_edge_dist = min_end_dist
        else:
            min_end_dist = min_end_dist
            min_edge_dist = min_end_dist
            
        # Pitch calculation for a user given finplate height
        if web_plate_l != 0:
            length_avail = (web_plate_l - 2 * min_end_dist)
            pitch = round(length_avail / (bolts_required - 1), 3)
        
        # Calculation of finplate height for optional height input
        elif web_plate_l == 0:
            bolt_line = 1
            web_plate_l_opt = (bolts_required - 1) * min_pitch + 2 * min_end_dist
            length_avail = (web_plate_l_opt - 2 * min_end_dist)
            pitch = min_pitch    
            # Check for maximum/minimum plate height for optional finplate height input
            if web_plate_l_opt > max_plate_height :
                bolt_line = 2
                if bolts_required % 2 == 0:
                    bolts_one_line = bolts_required / 2
                else:
                    bolts_one_line = (bolts_required / 2) + 1
                web_plate_l_opt = (bolts_one_line - 1) * min_pitch + 2 * min_end_dist
                length_avail = (web_plate_l_opt - 2 * min_end_dist)
                if min_plate_height > web_plate_l_opt:
                    web_plate_l_opt = min_plate_height
                    length_avail = (web_plate_l_opt - 2 * min_end_dist);
                    pitch = (web_plate_l_opt - 2 * min_end_dist) / (bolts_one_line - 1)
                    pitch = round(pitch, 3)
                if web_plate_l_opt > max_plate_height :
                    design_status = False
                    logger.error(": Bolt strength is insufficient to carry the shear force")
                    logger.warning(": Maximum plate height allowed is %2.2f mm " % max_plate_height)
                    logger.info(": Increase bolt diameter and/or bolt grade")
                  
            elif min_plate_height > max_plate_height:
                design_status = False
                logger.error(": Minimum plate height required is more than the clear depth of the beam")
                logger.warning(": Plate height required should be more than  %2.2f mm " % (min_plate_height))
                logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height))
                logger.info(": Increase the plate height")
                
            elif min_plate_height > web_plate_l_opt:
                web_plate_l_opt = min_plate_height
                length_avail = (web_plate_l_opt - 2 * min_end_dist);
                pitch = (web_plate_l_opt - 2 * min_end_dist) / (bolts_required - 1)
                pitch = round(pitch, 3) 
        
        # # Calculation of minimum plate thickness and maximum end/edge distance
        if web_plate_l != 0:
            min_plate_thk = (5 * shear_load * 1000) / (beam_fy * web_plate_l)
            max_edge_dist = int((12 * min_plate_thk * math.sqrt(250 / beam_fy)).real) - 1
        elif web_plate_l == 0:
            min_plate_thk = (5 * shear_load * 1000) / (bolt_fy * web_plate_l_opt)
            max_edge_dist = int((12 * min_plate_thk * math.sqrt(250 / beam_fy)).real) - 1
        
        # Moment demand calculation for user defined plate height and width (1st case)
        if web_plate_l != 0 and web_plate_w != 0:
            Ecc = web_plate_w - min_edge_dist
            # Moment due to shear external force
            M1 = shear_load * Ecc;
             
            # Moment demand for single line of bolts due to its shear capacity
            if pitch >= min_pitch:
                bolt_line = 1;
                gauge = 0;
                bolts_one_line = bolts_required;
                K = bolts_one_line / 2;
                M2 = 0;
                if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                    for k in range (0, K):
                        M2 = M2 + 2 * (bolt_shear_capacity * ((length_avail / 2 - k * pitch) ** 2 / (length_avail / 2 - k * pitch)));
                    moment_demand = max(M1, M2);
                    moment_demand = round(moment_demand * 0.001, 3)
              
            # moment demand for multi-line of bolts 
            if pitch < min_pitch:
                bolt_line = 2;
                if bolts_required % 2 == 0:
                    bolts_one_line = bolts_required / 2;
                else:
                    bolts_one_line = (bolts_required / 2) + 1;
                  
                pitch = round(length_avail / (bolts_one_line - 1), 3); 
                gauge = min_gauge
                Ecc = web_plate_w - min_gauge - min_edge_dist        
                # Moment due to external shear force
                M1 = shear_load * Ecc;
                # Moment demand for single line of bolts due to its shear capacity 
                if pitch >= min_pitch:
                    K = bolts_one_line / 2;
                    M2 = 0;
                    if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                        for k in range (0, K):
                            V = length_avail / 2 - k * pitch
                            H = gauge / 2;
                            d = math.sqrt(V ** 2 + H ** 2);
                            M2 = M2 + 2 * (bolt_shear_capacity * (d ** 2 / d));
                        M2 = M2 * 2;
                        moment_demand = max(M1, M2);
                        moment_demand = round(moment_demand * 0.001, 3)
              
                # Design is not safe: iterations required
                else:
                    design_status = False
                    logger.error(": Bolt strength is insufficient to carry the shear force")
                    logger.info(": Increase bolt diameter and/or bolt grade")
                    moment_demand = 0.0
        
        # Moment demand calculation for user defined plate height and optional width input (2nd case)
        if web_plate_l != 0 and web_plate_w == 0:
            Ecc = min_edge_dist + gap
            # Moment due to shear external force
            M1 = shear_load * Ecc;
             
            # Moment demand for single line of bolts due to its shear capacity
            if pitch >= min_pitch:
                bolt_line = 1;
                gauge = 0;
                bolts_one_line = bolts_required;
                K = bolts_one_line / 2;
                M2 = 0;
                if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                    for k in range (0, K):
                        M2 = M2 + 2 * (bolt_shear_capacity * ((length_avail / 2 - k * pitch) ** 2 / (length_avail / 2 - k * pitch)));
                    moment_demand = max(M1, M2);
                    moment_demand = round(moment_demand * 0.001, 3)
              
            # moment demand for multi-line of bolts 
            if pitch < min_pitch:
                bolt_line = 2;
                if bolts_required % 2 == 0:
                    bolts_one_line = bolts_required / 2;
                else:
                    bolts_one_line = (bolts_required / 2) + 1;
                  
                pitch = round(length_avail / (bolts_one_line - 1), 3); 
                gauge = min_gauge
                Ecc = min_edge_dist + min_gauge / 2 + gap
                # Moment due to external shear force
                M1 = shear_load * Ecc;
                # Moment demand for single line of bolts due to its shear capacity 
                if pitch >= min_pitch:
                    K = bolts_one_line / 2;
                    M2 = 0;
                    if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                        for k in range (0, K):
                            V = length_avail / 2 - k * pitch
                            H = gauge / 2;
                            d = math.sqrt(V ** 2 + H ** 2);
                            M2 = M2 + 2 * (bolt_shear_capacity * (d ** 2 / d));
                        M2 = M2 * 2;
                        moment_demand = max(M1, M2);
                        moment_demand = round(moment_demand * 0.001, 3)
              
                # Design is not safe: iterations required
                else:
                    design_status = False
                    logger.error(": Bolt strength is insufficient to carry the shear force")
                    logger.warning (": Increase bolt diameter and/or bolt grade")
                    moment_demand = 0.0
                    
        # Moment demand calculation for optional height and user given width input (3rd case)
        elif web_plate_l == 0 and web_plate_w != 0:
            if bolt_line == 1:
                # Moment due to shear external force
                Ecc = web_plate_w - min_edge_dist
                M1 = shear_load * Ecc; 
                # Moment demand for single line of bolts due to its shear capacity
                gauge = 0;
                bolts_one_line = bolts_required;
                K = bolts_one_line / 2;
                M2 = 0;
                if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                    for k in range (0, K):
                        M2 = M2 + 2 * (bolt_shear_capacity * ((length_avail / 2 - k * pitch) ** 2 / (length_avail / 2 - k * pitch)));
                    moment_demand = max(M1, M2);
                    moment_demand = round(moment_demand * 0.001, 3)
            elif bolt_line == 2:        
                gauge = min_gauge
                Ecc = web_plate_w - min_gauge - min_edge_dist
                # Moment due to external shear force
                M1 = shear_load * Ecc
                # Moment demand for single line of bolts due to its shear capacity 
                K = bolts_one_line / 2
                M2 = 0;
                if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                    for k in range (0, K):
                        V = length_avail / 2 - k * pitch
                        H = gauge / 2;
                        d = math.sqrt(V ** 2 + H ** 2);
                        M2 = M2 + 2 * (bolt_shear_capacity * (d ** 2 / d));
                    M2 = M2 * 2;
                    moment_demand = max(M1, M2);
                    moment_demand = round(moment_demand * 0.001, 3)
        
        # Moment demand calculation for optional height and width input (4th case)
        elif web_plate_l == 0 and web_plate_w == 0:
            if bolt_line == 1:
                # Moment due to shear external force
                Ecc = min_edge_dist + gap # 20
                M1 = shear_load * Ecc; 
                # Moment demand for single line of bolts due to its shear capacity
                gauge = 0;
                bolts_one_line = bolts_required;
                K = bolts_one_line / 2;
                M2 = 0;
                if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                    for k in range (0, K):
                        M2 = M2 + 2 * (bolt_shear_capacity * ((length_avail / 2 - k * pitch) ** 2 / (length_avail / 2 - k * pitch)));
                    moment_demand = max(M1, M2);
                    moment_demand = round(moment_demand * 0.001, 3)
            elif bolt_line == 2:        
                gauge = min_gauge
                Ecc = min_edge_dist + min_gauge / 2 + gap # 20
                # Moment due to external shear force
                M1 = shear_load * Ecc
                # Moment demand for single line of bolts due to its shear capacity 
                K = bolts_one_line / 2
                M2 = 0;
                if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                    for k in range (0, K):
                        V = length_avail / 2 - k * pitch
                        H = gauge / 2;
                        d = math.sqrt(V ** 2 + H ** 2);
                        M2 = M2 + 2 * (bolt_shear_capacity * (d ** 2 / d));
                    M2 = M2 * 2;
                    moment_demand = max(M1, M2);
                    moment_demand = round(moment_demand * 0.001, 3)    
    
        ######################################################################33
        # Fetch bolt design output parameters dictionary
        if web_plate_l == 0:
            boltParam = {}
            boltParam['shearcapacity'] = bolt_shear_capacity
            boltParam['bearingcapacity'] = bolt_bearing_capacity
            boltParam['boltcapacity'] = bolt_capacity
            boltParam['numofbolts'] = bolts_required
            boltParam['boltgrpcapacity'] = bolt_group_capacity
            boltParam['numofrow'] = bolts_one_line
            boltParam['numofcol'] = bolt_line
            boltParam['pitch'] = pitch
            boltParam['minpitch'] = min_pitch
    #         boltParam['edge']= float(edge_dist)
            boltParam['enddist'] = float(min_end_dist)
            boltParam['gauge'] = float(gauge)
            boltParam['moment'] = moment_demand
            boltParam['plateheight'] = web_plate_l
            boltParam['plateheightoptional'] = web_plate_l_opt
            
            # Return bolt design parameters (used for design report)
            boltParam['bolt_fu'] = bolt_fu
            boltParam['bolt_fy'] = bolt_fy
            boltParam['dia_hole'] = dia_hole
            boltParam['kb'] = kb
            return boltParam
        else:
            boltParam = {}
            boltParam['shearcapacity'] = bolt_shear_capacity
            boltParam['bearingcapacity'] = bolt_bearing_capacity
            boltParam['boltcapacity'] = bolt_capacity
            boltParam['numofbolts'] = bolts_required
            boltParam['boltgrpcapacity'] = bolt_group_capacity
            boltParam['numofrow'] = bolts_one_line
            boltParam['numofcol'] = bolt_line
            boltParam['pitch'] = pitch
            boltParam['minpitch'] = min_pitch
    #         boltParam['edge']= float(edge_dist)
            boltParam['enddist'] = float(min_end_dist)
            boltParam['gauge'] = float(gauge)
            boltParam['moment'] = moment_demand
            boltParam['plateheight'] = web_plate_l
            
            # Return bolt design parameters (used for design report)
            boltParam['bolt_fu'] = bolt_fu
            boltParam['bolt_fy'] = bolt_fy
            boltParam['dia_hole'] = dia_hole
            boltParam['kb'] = kb
            return boltParam
    
    # Call function for bolt design output
    boltParameters = boltDesign(web_plate_l)
    
    # Check for long joint connections
    length_joint = (boltParameters['numofrow'] - 1) * boltParameters['pitch']
    if length_joint > 15 * bolt_dia:
        beta_lj = 1.075 - length_joint / (200 * bolt_dia)
        bolt_shear_capacity = beta_lj * boltParameters['shearcapacity']
#         new_bolt_param = boltDesign(bolt_shear_capacity_new)
        new_bolt_param = boltDesign(web_plate_l)
    else:
        new_bolt_param = boltParameters
      
    ####################################################################################
    
    # Design of fin plate  
    # Plate width input (optional) and validation
    # Note: For calculation of edge distance on bean edge side, 20 mm is added for clearance b/w beam edge and column web/flange 
    if web_plate_w != 0:
        if boltParameters['numofcol'] == 1:
            edge_dist = boltParameters['enddist']
            plate_edge = web_plate_w - edge_dist       
            web_plate_w_req = 2 * boltParameters['enddist'] + gap  #20
        if boltParameters['numofcol'] == 2:
            edge_dist = boltParameters['enddist']
            plate_edge = web_plate_w - boltParameters['gauge'] - boltParameters['enddist']    
            web_plate_w_req = boltParameters['gauge'] + 2 * boltParameters['enddist'] + gap  #20
            
            
    if web_plate_w == 0:   
        if boltParameters['numofcol'] == 1:
            edge_dist = boltParameters['enddist']
            plate_edge = edge_dist + gap  #20
            web_plate_w_req = plate_edge + boltParameters['enddist'];
            web_plate_w_opt = web_plate_w_req
        if boltParameters['numofcol'] == 2:
            edge_dist = boltParameters['enddist'] 
            plate_edge = edge_dist + gap   #20
            web_plate_w_req = boltParameters['gauge'] + plate_edge + boltParameters['enddist'];
            web_plate_w_opt = web_plate_w_req;      

    
    # Moment capacity of the fin plate (also known as web-side plate)
    if web_plate_l != 0:
        moment_capacity = 1.2 * (web_plate_fy / 1.1) * (web_plate_t * web_plate_l * web_plate_l) / 6 * 0.001;
        moment_capacity = round(moment_capacity * 0.001, 3);
    elif web_plate_l == 0:
        moment_capacity = 1.2 * (web_plate_fy / 1.1) * (web_plate_t * boltParameters['plateheightoptional'] * boltParameters['plateheightoptional']) / 6 * 0.001;
        moment_capacity = round(moment_capacity * 0.001, 3);
    
    # Plate height calculation based on moment demand
    if web_plate_l == 0:
        if moment_capacity < boltParameters['moment']:
            web_plate_l_mom = math.sqrt(boltParameters['moment'] * 1.1 * 6 * 1000000 / float(1.2 * 250 * web_plate_t)) 
            moment_capacity = boltParameters['moment']
        else:
            web_plate_l_mom = boltParameters['plateheightoptional']
    if web_plate_l != 0:
        if moment_capacity > boltParameters['moment']:
            pass
        else:
            design_status = False
            logger.error(": Plate moment capacity is less than the moment demand [cl. 8.2.1.2]")
            logger.warning(": Re-design with increased plate dimensions")
    
    # Calculation of plate height based on both minimum height and moment criteria (for optional input)
    if web_plate_l == 0:
        web_plate_l_opt = max(web_plate_l_mom, boltParameters['plateheightoptional'])
        if web_plate_l_opt % 10 != 0:
            web_plate_l_opt = (web_plate_l_opt // 10) * 10 + 10
        else:
            web_plate_l_opt = web_plate_l_opt
        if web_plate_l_opt > max_plate_height:
            design_status = False
            logger.error(": Plate height provided is more than the maximum height allowed")
            logger.warning(": Maximum plate height required is %2.2f mm " % (max_plate_height))
            logger.info("Try to increase the plate thickness")
    
    # Calculation for maximum/minimum plate thickness
    max_plate_thk = fin_max_thk(bolt_dia);
    max_plate_thk = round(max_plate_thk, 3);
    if web_plate_l != 0:
        min_plate_thk = fin_min_thk(shear_load, beam_fy, web_plate_l);
        min_plate_thk = round(min_plate_thk, 3);    
    if web_plate_l == 0:
        min_plate_thk = fin_min_thk(shear_load, beam_fy, web_plate_l_opt);
        min_plate_thk = round(min_plate_thk, 3);
        if min_plate_thk > web_plate_t:  # Change
           web_plate_l_opt = 5 * shear_load * 1000 / float(web_plate_t * beam_fy)
           web_plate_l_opt = round(web_plate_l_opt, 3)
           if boltParameters['numofcol'] == 1:
               new_bolt_param['pitch'] = (web_plate_l_opt - 2 * boltParameters['enddist']) / (boltParameters['numofrow'] - 1)
               new_bolt_param['pitch'] = round(new_bolt_param['pitch'], 3)
           elif boltParameters['numofcol'] == 2:
               new_bolt_param['pitch'] = (web_plate_l_opt - 2 * boltParameters['enddist']) / (boltParameters['numofrow'] - 1)
               new_bolt_param['pitch'] = round(new_bolt_param['pitch'], 3)
        if web_plate_l_opt > max_plate_height:
            design_status = False
            logger.error(": Plate height required is more than the maximum height possible")
            logger.warning(": Maximum plate height required is %2.2f mm " % (max_plate_height))
            logger.info("Try to increase the plate thickness")
   ##############
        
    # # Calculation of plate height and thickness and checks for extreme values 
    # Check for maximum and minimum plate thickness
    if web_plate_l != 0:
        if web_plate_t < min_plate_thk:
            design_status = False
            logger.error(": Plate thickness provided is less than the minimum required [Ref. Owens and Cheal, 1989]")
            logger.warning(": Minimum plate thickness required is %2.2f mm " % (min_plate_thk))

    if web_plate_t > max_plate_thk:
        design_status = False
        logger.error(": Plate thickness provided is more than the maximum allowed [Ref. INSDAG detailing manual, 2002]")
        logger.warning(": Maximum plate thickness allowed is half the diameter of bolt")
        logger.info(": Increase the bolt diameter or decrease the plate thickness")
        # logger.warning(": Maximum plate thickness allowed is %2.2f mm " % (max_plate_thk))
        # logger.info(": Select a deeper secondary beam section")

    # Calculation of plate height required (for optional input)
    web_plate_l_req1 = math.sqrt((boltParameters['moment'] * 1000000 * 6 * 1.1) / (1.2 * beam_fy * web_plate_t));
    web_plate_l_req1 = round(web_plate_l_req1, 3)
    # Single line of bolts
    if boltParameters['numofcol'] == 1:
        web_plate_l_req2 = (boltParameters['numofbolts'] - 1) * boltParameters['minpitch'] + 2 * boltParameters['enddist'];
        if web_plate_l == 0 or web_plate_l == min_plate_height or web_plate_l == max_plate_height:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, web_plate_l);
        else:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, min_plate_height);

    # Multi line of bolts
    if boltParameters['numofcol'] == 2:
        web_plate_l_req2 = (boltParameters['numofrow'] - 1) * boltParameters['minpitch'] + 2 * boltParameters['enddist'];
    
        if web_plate_l == 0 or web_plate_l == min_plate_height or web_plate_l == max_plate_height:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, web_plate_l);
        elif web_plate_l > min_plate_height or web_plate_l < max_plate_height:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, min_plate_height);
    
    if web_plate_l >= min_plate_height or web_plate_l <= max_plate_height :
        pass
    else:
        if web_plate_l < web_plate_l_req:
            design_status = False
            logger.error(": Plate height provided is less than the minimum required [cl. 10.2.2/10.2.4]")
            logger.warning(": Minimum plate width required is %2.2f mm " % (web_plate_l_req))
            logger.info(": Increase the plate width")

    if web_plate_w != 0:
        if web_plate_w < web_plate_w_req:
            design_status = False
            logger.error(": Plate width provided is less than the minimum required [cl. 10.2.2/10.2.4]")
            logger.warning(": Minimum plate width required is %2.2f mm " % (web_plate_w_req))
            logger.info(": Increase the plate width")
    else:
        pass
                
    # Block shear capacity of plate
    min_thk = min(web_plate_t,beam_w_t)
    Tdb = blockshear(boltParameters['numofrow'], boltParameters['numofcol'], boltParameters['dia_hole'], \
                     beam_fy, beam_fu, boltParameters['enddist'], \
                     boltParameters['enddist'], boltParameters['pitch'], \
                     boltParameters['gauge'], min_thk)
    if Tdb < shear_load:
        design_status = False
        logger.error(": Block shear capacity of the plate is less than the applied shear force [cl. 6.4.1]")
        logger.warning(": Minimum block shear capacity required is %2.2f kN" % (shear_load))
        logger.info(": Increase the plate thickness")
        
    ##################################################################################
    ### Shear yeilding check ###

    h_0 = beam_d - beam_f_t - beam_R1
    A_v = h_0 * beam_w_t  ## shear area of secondry beam
    V_d = shear_yeilding_b(A_v, beam_fy)
    if connectivity == "Beam-Beam":
        if V_d < shear_load:
            design_status = False
            logger.error(": Secondary beam fails in shear yielding [cl. 8.4.1]/ AISC design manual")
            logger.warning(": Minimum shear yielding capacity required is %2.2f kN" % (shear_load))
            logger.info(": Use a deeper section for the secondary beam")

    #### Check for shear rupture ###

    A_vn = beam_w_t * (h_0 - (boltParameters['numofbolts'] * boltParameters['dia_hole']))
    if A_vn <=  ((beam_fy / beam_fu)*(1.25 / 1.10)*(A_v / 0.9)):
        A_vn =  ((beam_fy / beam_fu)*(1.25 / 1.10)*(A_v / 0.9))
    R_n = shear_rupture_b(A_vn, beam_fu)
    if connectivity == "Beam-Beam":
        if R_n < shear_load:
            design_status = False
            logger.error(": Capacity of the secondary beam in shear rupture is less than the applied shear force [cl. 8.4.1.1; AISC Steel Construction Manual, 14th Edition]")
            logger.warning(": Minimum shear rupture capacity required is %2.2f kN" % (shear_load))
            logger.info(" : Use a deeper section for the secondary beam")


    # # Weld design
    # Assumption: Weld electrode is stronger than parent metal
    weld_fu_govern = min(weld_fu, column_fu)    # cl. 10.5.7.1
#     Effective length of the weld required (Note: Weld is assumed to be provided for full length of the plate)
#     Weld length for user given plate height
    if web_plate_l != 0:
        weld_l = web_plate_l - weld_t * 2
#     Weld length for optional plate height    
    else:
        weld_l = web_plate_l_opt - weld_t * 2
    
    # # Weld shear strength 
    # Direct shear
    Vy1 = shear_load * 1000 / float(2 * weld_l);        
    
    # Shear due to moment (Note: for single line of weld)
    xCritical = 0;                    
    yCritical = weld_l * 0.5;        
    
    Ip = weld_l * weld_l * weld_l / 12;
    
    Vx = boltParameters['moment'] * yCritical * 1000000 / (2 * Ip);
    Vy2 = boltParameters['moment'] * xCritical * 1000000 / (2 * Ip);
    
    # Resultant shear
    Vr = math.sqrt(Vx ** 2 + (Vy1 + Vy2) ** 2);
    Vr = round(Vr, 3);
    
    weld_strength = 0.7 * weld_t * weld_fu_govern / (math.sqrt(3) * gamma_mw);
    weld_strength = round(weld_strength, 3);
    
    weld_t_req_chk1 = (Vr * (math.sqrt(3) * gamma_mw)) / (0.7 * weld_fu_govern);
    weld_t_req_chk2 = 0.8 * web_plate_t;
    weld_t_req = max(weld_t_req_chk1, weld_t_req_chk2);
    
    if weld_t_req != int(weld_t_req):
        weld_t_req = int(weld_t_req) + 1;
    else:
        weld_t_req = weld_t_req;
    
    if weld_t < weld_t_req:
        design_status = False
        logger.error(": Weld thickness is not sufficient [cl. 10.5.7; INSDAG Detailing Manual, 2002]")
        logger.warning(": Minimum weld thickness required is %2.2f mm " % (weld_t_req))
#         logger.sug(": Increase the weld thickness or length of weld/finplate")
        logger.info(": Increase the weld thickness or length of weld/fin plate")

    ############## Check for maximum weld thickness: cl: 10.5.3.1 ; IS 800 ###########

    """ Here t_thinner_beam_plate indicates thickness of thinner part of members
        connected by the fillet weld.
    """
    if connectivity == "Column flange-Beam web":
        t_thinner_col_plate = min(column_f_t.real, web_plate_t.real)

    if connectivity == "Column web-Beam web":
        t_thinner_col_plate = min(column_w_t.real, web_plate_t.real)

    if connectivity == "Beam-Beam":
        t_thinner_col_plate = min(PBeam_w_t.real, web_plate_t.real)

    max_weld_t = t_thinner_col_plate

    if weld_t > max_weld_t:
        design_status = False
        logger.error(": Weld thickness is more than maximum allowed weld thickness [cl. 10.5.3.1]")
        logger.warning(": Maximum weld thickness allowed is %2.2f mm " % (max_weld_t))
        logger.info(": Decrease the weld thickness")

    # End of calculation
    # Output for user given fin plate height
    if web_plate_l != 0 and web_plate_w != 0:
        outputObj = {}
        outputObj['Bolt'] = {}
        outputObj['Bolt']['status'] = design_status
        outputObj['Bolt']['shearcapacity'] = round(new_bolt_param['shearcapacity'], 3)
        outputObj['Bolt']['bearingcapacity'] = new_bolt_param['bearingcapacity']
        outputObj['Bolt']['boltcapacity'] = round(new_bolt_param['boltcapacity'], 3)
        # outputObj['Bolt']['numofbolts'] = new_bolt_param['numofbolts']
        outputObj['Bolt']['numofbolts'] = new_bolt_param['numofrow'] * new_bolt_param['numofcol']
        outputObj['Bolt']['boltgrpcapacity'] = round(new_bolt_param['boltgrpcapacity'], 3)
        outputObj['Bolt']['numofrow'] = new_bolt_param['numofrow']
        outputObj['Bolt']['numofcol'] = new_bolt_param['numofcol']
        outputObj['Bolt']['pitch'] = new_bolt_param['pitch']
        outputObj['Bolt']['edge'] = float(edge_dist)
        outputObj['Bolt']['enddist'] = new_bolt_param['enddist']
        outputObj['Bolt']['gauge'] = new_bolt_param['gauge']
         
        outputObj['Weld'] = {}
        outputObj['Weld']['thickness'] = weld_t_req
        outputObj['Weld']['thicknessprovided'] = weld_t
        outputObj['Weld']['resultantshear'] = Vr
        outputObj['Weld']['weldstrength'] = weld_strength
         
        outputObj['Plate'] = {}
        outputObj['Plate']['minHeight'] = min_plate_height
        outputObj['Plate']['minWidth'] = web_plate_w_req
        outputObj['Plate']['plateedge'] = plate_edge
        outputObj['Plate']['externalmoment'] = new_bolt_param['moment']
        outputObj['Plate']['momentcapacity'] = moment_capacity
        outputObj['Plate']['height'] = float(web_plate_l)
        outputObj['Plate']['width'] = float(web_plate_w)
        outputObj['Plate']['blockshear'] = float(Tdb)
    
    # Output for optional height and user given width of fin plate
    elif web_plate_l == 0 and web_plate_w != 0:
        outputObj = {}
        outputObj['Bolt'] = {}
        outputObj['Bolt']['status'] = design_status
        outputObj['Bolt']['shearcapacity'] = round(new_bolt_param['shearcapacity'], 3)
        outputObj['Bolt']['bearingcapacity'] = new_bolt_param['bearingcapacity']
        outputObj['Bolt']['boltcapacity'] = round(new_bolt_param['boltcapacity'], 3)
        # outputObj['Bolt']['numofbolts'] = new_bolt_param['numofbolts']
        outputObj['Bolt']['numofbolts'] = new_bolt_param['numofrow'] * new_bolt_param['numofcol']
        outputObj['Bolt']['boltgrpcapacity'] = round(new_bolt_param['boltgrpcapacity'], 3)
        outputObj['Bolt']['numofrow'] = new_bolt_param['numofrow']
        outputObj['Bolt']['numofcol'] = new_bolt_param['numofcol']
        outputObj['Bolt']['pitch'] = new_bolt_param['pitch']
        outputObj['Bolt']['edge'] = float(edge_dist)
        outputObj['Bolt']['enddist'] = new_bolt_param['enddist']
        outputObj['Bolt']['gauge'] = new_bolt_param['gauge']
         
        outputObj['Weld'] = {}
        outputObj['Weld']['thickness'] = weld_t_req
        outputObj['Weld']['thicknessprovided'] = weld_t
        outputObj['Weld']['resultantshear'] = Vr
        outputObj['Weld']['weldstrength'] = weld_strength
         
        outputObj['Plate'] = {}
        outputObj['Plate']['minHeight'] = min_plate_height
        outputObj['Plate']['minWidth'] = web_plate_w_req
        outputObj['Plate']['plateedge'] = plate_edge
        outputObj['Plate']['externalmoment'] = new_bolt_param['moment']
        outputObj['Plate']['momentcapacity'] = moment_capacity
        outputObj['Plate']['height'] = float(web_plate_l_opt)
        outputObj['Plate']['width'] = float(web_plate_w)
        outputObj['Plate']['blockshear'] = float(Tdb)
    
    # Output for user given height but optional width of fin plate
    elif web_plate_l != 0 and web_plate_w == 0:
        outputObj = {}
        outputObj['Bolt'] = {}
        outputObj['Bolt']['status'] = design_status
        outputObj['Bolt']['shearcapacity'] = round(new_bolt_param['shearcapacity'], 3)
        outputObj['Bolt']['bearingcapacity'] = new_bolt_param['bearingcapacity']
        outputObj['Bolt']['boltcapacity'] = round(new_bolt_param['boltcapacity'], 3)
        # outputObj['Bolt']['numofbolts'] = new_bolt_param['numofbolts']
        outputObj['Bolt']['numofbolts'] = new_bolt_param['numofrow'] * new_bolt_param['numofcol']
        outputObj['Bolt']['boltgrpcapacity'] = round(new_bolt_param['boltgrpcapacity'], 3)
        outputObj['Bolt']['numofrow'] = new_bolt_param['numofrow']
        outputObj['Bolt']['numofcol'] = new_bolt_param['numofcol']
        outputObj['Bolt']['pitch'] = new_bolt_param['pitch']
        outputObj['Bolt']['edge'] = float(edge_dist)
        outputObj['Bolt']['enddist'] = new_bolt_param['enddist']
        outputObj['Bolt']['gauge'] = new_bolt_param['gauge']
         
        outputObj['Weld'] = {}
        outputObj['Weld']['thickness'] = weld_t_req
        outputObj['Weld']['thicknessprovided'] = weld_t
        outputObj['Weld']['resultantshear'] = Vr
        outputObj['Weld']['weldstrength'] = weld_strength
         
        outputObj['Plate'] = {}
        outputObj['Plate']['minHeight'] = min_plate_height
        outputObj['Plate']['minWidth'] = web_plate_w_req
        outputObj['Plate']['plateedge'] = plate_edge
        outputObj['Plate']['externalmoment'] = new_bolt_param['moment']
        outputObj['Plate']['momentcapacity'] = moment_capacity
        outputObj['Plate']['height'] = float(web_plate_l)
        outputObj['Plate']['width'] = float(web_plate_w_opt)
        outputObj['Plate']['blockshear'] = float(Tdb)
    
    # Output for optional height and width of fin plate
    else:
        outputObj = {}
        outputObj['Bolt'] = {}
        outputObj['Bolt']['status'] = design_status
        outputObj['Bolt']['shearcapacity'] = round(new_bolt_param['shearcapacity'], 3)
        outputObj['Bolt']['bearingcapacity'] = new_bolt_param['bearingcapacity']
        outputObj['Bolt']['boltcapacity'] = round(new_bolt_param['boltcapacity'], 3)
        # outputObj['Bolt']['numofbolts'] = new_bolt_param['numofbolts']
        outputObj['Bolt']['numofbolts'] = new_bolt_param['numofrow'] * new_bolt_param['numofcol']
        outputObj['Bolt']['boltgrpcapacity'] = round(new_bolt_param['boltgrpcapacity'], 3)
        outputObj['Bolt']['numofrow'] = new_bolt_param['numofrow']
        outputObj['Bolt']['numofcol'] = new_bolt_param['numofcol']
        outputObj['Bolt']['pitch'] = new_bolt_param['pitch']
        outputObj['Bolt']['edge'] = float(edge_dist)
        outputObj['Bolt']['enddist'] = new_bolt_param['enddist']
        outputObj['Bolt']['gauge'] = new_bolt_param['gauge']
         
        outputObj['Weld'] = {}
        outputObj['Weld']['thickness'] = weld_t_req
        outputObj['Weld']['thicknessprovided'] = weld_t
        outputObj['Weld']['resultantshear'] = Vr
        outputObj['Weld']['weldstrength'] = weld_strength
         
        outputObj['Plate'] = {}
        outputObj['Plate']['minHeight'] = min_plate_height
        outputObj['Plate']['minWidth'] = web_plate_w_req
        outputObj['Plate']['plateedge'] = plate_edge
        outputObj['Plate']['externalmoment'] = new_bolt_param['moment']
        outputObj['Plate']['momentcapacity'] = moment_capacity
        outputObj['Plate']['height'] = float(web_plate_l_opt)
        outputObj['Plate']['width'] = float(web_plate_w_opt)
        outputObj['Plate']['blockshear'] = float(Tdb)
     
    
    # Parameters dictionary for design report
   
    outputObj['Bolt']['bolt_fu'] = boltParameters['bolt_fu']
    outputObj['Bolt']['bolt_dia'] = bolt_dia
    outputObj['Bolt']['k_b'] = boltParameters['kb']
    outputObj['Bolt']['beam_w_t'] = beam_w_t
    outputObj['Bolt']['web_plate_t'] = web_plate_t
    outputObj['Bolt']['beam_fu'] = beam_fu
    outputObj['Bolt']['shearforce'] = shear_load
    outputObj['Bolt']['dia_hole'] = boltParameters['dia_hole']
    
    outputObj['Plate']['web_plate_fy'] = web_plate_fy
    # $$$$$$$$$$$$$$$$$$$$
    
    outputObj['Plate']['platethk'] = web_plate_t
    outputObj['Plate']['beamdepth'] = beam_d
    outputObj['Plate']['beamrootradius'] = beam_R1
    outputObj['Plate']['colrootradius'] = PBeam_R1
    outputObj['Plate']['beamflangethk'] = beam_f_t
    outputObj['Plate']['colflangethk'] = PBeam_T
 
    # $$$$$$$$$$$$$$$$$$$$$$$$
    
    outputObj['Weld']['weld_fu'] = weld_fu
    outputObj['Weld']['effectiveWeldlength'] = weld_l


# Log message for safe/failed design
    if weld_type == 'Shop weld':
        if weld_t < 6:
            logger.warning(" : Minimum recommended weld thickness for shop weld is 6 mm")
    else:
        if weld_t < 8:
            logger.warning(" : Minimum recommended weld thickness for field weld is 8 mm")


    if  design_status == True:

        logger.info(": Overall fin plate connection design is safe \n")
        logger.debug(" :=========End Of design===========")
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")
    
    return outputObj

