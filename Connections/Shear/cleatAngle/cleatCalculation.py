'''
Created on 25-Mar-2016

@author: aravind
'''

import math
from model import *
from PyQt4.Qt import QString
import logging
flag  = 1
logger = None


def module_setup():
    
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")

module_setup()

#All common functions are kept in this module

# Function for net area of ordinary bolts
# Source: Subramanian's book, page: 348
def netArea_calc(dia):
    netArea = {5:15.3, 6:22.04, 8:39.18, 10:61.23, 12:84.5, 16:157, 20:245, 22:303, 24:353, 27:459, 30:561, 36:817};
    return netArea[dia]

#BOLT: determination of shear capacity of black bolt = fu * n * A / (root(3) * Y)
def black_bolt_shear(dia, n, fu):
    A = netArea_calc(dia)
    root3 = math.sqrt(3);
    Vs = fu * n * A / (root3 * 1.25 * 1000)
    Vs = round(Vs,3)
    return Vs


#BOLT: Determination of factored design force of HSFG bolts Vsf = Vnsf / Ymf = uf * ne * Kh * Fo where Vnsf: The nominal shear capacity of bolt
def HSFG_bolt_shear(uf, dia, n, fu):
    Anb = math.pi * dia * dia * 0.25 * 0.78  #threaded area(Anb) = 0.78 x shank area
    Fo = Anb * 0.7 * fu 
    Kh = 1  # Assuming fastners in Clearence hole
    Ymf = 1.25  # Ymf = 1.25 if Slip resistance is designed at ultimate load
    Vsf = uf * n * Kh * Fo / (Ymf * 1000)
    Vsf = round(Vsf,3)
    return Vsf

#BOLT: determination of bearing capacity = 2.5 * kb * d * t * fu / Y
def bearing_capacity(dia, t, fu,beam_fu):
#add code to determine kb if pitch, gauge, edge distance known
    if dia  == 12 or dia == 14:
        dia_hole = dia + 1
    elif dia == 16 or dia == 18 or dia == 20 or dia == 22 or dia == 24:
        dia_hole = dia + 2
    else:
        dia_hole = dia + 3
    #minimum spacing
    min_pitch = int(2.5*dia)
    min_gauge = int(2.5*dia)
    min_end_dist = int(1.7* dia_hole)
    #calculation of kb
    kbchk1 = min_end_dist/float(3*dia_hole)
    kbchk2 = min_pitch/float(3*dia_hole)-0.25
    kbchk3 = fu/float(beam_fu)
    kbchk4 = 1
    kb = min(kbchk1,kbchk2,kbchk3,kbchk4)
    kb = round(kb,3)
    Vb = 2.5 * kb * dia * t * fu / (1.25 * 1000);
    Vb = round(Vb,3);
    return Vb;


def critical_bolt_shear(load,eccentricity,pitch,gauge,bolts_one_line):
    sigma = 0.0
    r_y = 0.0
    r_x = 0.0
    moment = load/2 * eccentricity
    n = int(bolts_one_line / 2)
    bolts_req = bolts_one_line
    if gauge == 0:
        if bolts_one_line % 2 == 0:
            r_y = (n - 0.5) * pitch
            for i in range(n):
                sigma = sigma + 2 * (i+0.5) * (i+0.5)*pitch*pitch
        else:
            r_y = n * pitch
            for i in range(n):
                sigma = sigma + 2 * (i+1) * (i+1)*pitch*pitch 
    else:
        bolts_req = 2 * bolts_one_line
        r_x = gauge / 2.0
        if bolts_one_line % 2 == 0:
            r_y = (n - 0.5) * pitch
            for i in range(n):
                sigma = sigma + 4 * (i+0.5) * (i+0.5)*pitch*pitch + 4 * r_x**2
        else:
            r_y = n * pitch
            for i in range(n):
                sigma = sigma + 4 * (i+1) * (i+1)*pitch*pitch + 4 * r_x**2
    shear_x = (moment * r_y)/sigma
    shear_y = (moment * r_x)/sigma  + load/(2*bolts_req)
    resultant = math.sqrt(shear_x**2 + shear_y**2)
    return resultant  


def column_critical_shear(load,eccentricity,pitch,gauge,bolts_one_line, c_edge_distance):
    resultant_1 = critical_bolt_shear(load,eccentricity,pitch,gauge,bolts_one_line)
    # Assuming centre of pressure 25 mm below the top cleat and again calculating the horizontal force
    # Maximum of force_x and above mentioned horizontal force will be used to check the safety of the bolts
    sigma = 0.0
    r_y = 0.0
    r_x = 0.0
    moment = (load/2) * eccentricity
    bolts_req = bolts_one_line
    r_y = c_edge_distance + (bolts_one_line - 1) * pitch - 25
    if gauge == 0:
        for i in range(1 , bolts_one_line+1):
            r = c_edge_distance + (i - 1) * pitch - 25
            sigma = sigma + r**2
        
    else:
        bolts_req = 2 * bolts_one_line
        r_x = gauge / 2.0
        for i in range(1,bolts_one_line+1):
            r = c_edge_distance + (i - 1) * pitch -25
            sigma = sigma + 2 * (r**2 + r_x**2)
        
    shear_x = (moment * r_y)/sigma
    shear_y = (moment * r_x)/sigma  + load/(2*bolts_req)
    resultant_2 = math.sqrt(shear_x**2 + shear_y**2)
    resultant = max(resultant_1,resultant_2)
    return resultant 
# Block shear capacity of plates/members
def blockshear(numrow,numcol,dia_hole,fy,fu,edge_dist,end_dist,pitch,gauge,platethk):
    Tdb=0.0
    if numcol == 1:
        Avg = platethk * ((numrow-1)*pitch + end_dist)
        Avn = platethk * ((numrow-1)*pitch + end_dist - (numrow-1+0.5)*dia_hole)
        Atg = platethk * edge_dist
        Atn = platethk * (edge_dist - 0.5 * dia_hole)
        
        Tdb1 = (Avg * fy / (math.sqrt(3)*1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3)*1.25) + Atg * fy / 1.1)
        Tdb = min (Tdb1,Tdb2)
        Tdb = round(Tdb/1000,3)
        
    elif numcol == 2:
        Avg = platethk * ((numrow-1)*pitch + end_dist)
        Avn = platethk * ((numrow-1)*pitch + end_dist - (numrow-1+0.5)*dia_hole)
        Atg = platethk * (edge_dist + gauge)
        Atn = platethk * (edge_dist + gauge - 0.5 * dia_hole)
        
        Tdb1 = (Avg * fy / (math.sqrt(3)*1.1) + 0.9 * Atn * fu / 1.25)
        Tdb2 = (0.9 * Avn * fu / (math.sqrt(3)*1.25) + Atg * fy / 1.1)
        Tdb = min (Tdb1,Tdb2)
        Tdb = round(Tdb/1000,3)
        
    return Tdb  

def cleatAngleConn(uiObj):
    global logger
    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumSection']
    connectivity = uiObj['Member']['Connectivity']
    beam_fu = uiObj['Member']['fu (MPa)']
    beam_fy = uiObj['Member']['fy (MPa)']
              
    shear_load = uiObj['Load']['ShearForce (kN)']
                  
    bolt_dia = uiObj['Bolt']['Diameter (mm)']
    bolt_type  = uiObj["Bolt"]["Type"]
    bolt_grade = uiObj['Bolt']['Grade']
   
    cleat_length = uiObj['cleat']['Height (mm)']
    cleat_fu = uiObj['Member']['fu (MPa)']
    cleat_fy = uiObj['Member']['fy (MPa)']
    cleat_sec = uiObj['cleat']['section']
              
    dictbeamdata  = get_beamdata(beam_sec)
    beam_w_t = float(dictbeamdata[QString("tw")])
    beam_f_t = float(dictbeamdata[QString("T")])
    beam_d = float(dictbeamdata[QString("D")])
    beam_R1 =float(dictbeamdata[QString("R1")])
    beam_B =float(dictbeamdata[QString("B")])
    beam_D =float(dictbeamdata[QString("D")])
       
    if connectivity == "Column web-Beam web" or connectivity == "Column flange-Beam web": 
        dictcolumndata = get_columndata(column_sec)
        column_w_t = float(dictcolumndata[QString("tw")])
        column_f_t = float(dictcolumndata[QString("T")])
        column_R1 =float(dictcolumndata[QString("R1")])
        column_D = float(dictcolumndata[QString("D")])
        column_B = float(dictcolumndata[QString("B")])
    else:
        dictcolumndata = get_beamdata(column_sec)
        column_w_t = float(dictcolumndata[QString("tw")])
        column_f_t = float(dictcolumndata[QString("T")])
        column_R1 =float(dictcolumndata[QString("R1")])
        column_D = float(dictcolumndata[QString("D")])
        column_B = float(dictcolumndata[QString("B")])
        
   
    dictCleatData = get_angledata(cleat_sec)
    cleat_legsize= int(dictCleatData[QString("A")])
    cleat_legsize_1 = int(dictCleatData[QString("B")])
    cleat_thk = int(dictCleatData[QString("t")])
#####################Calculation Begins########################
    pitch =0.0
    gauge = 0.0
    eccentricity = 0.0
    dia_hole = 0
    thinner = 0.0
    bolt_shear_capacity = 0.0
    bolt_bearing_capacity_c = 0.0
    bearing_capacity_column = 0.0
    bearing_capacity_cleat_c = 0.0
    bearing_capacity_c =0.0
    

##################################################################
    design_check = True   
    if connectivity == 'Column flange-Beam web':
        avbl_space = column_B 
        required_space = 2 * cleat_legsize_1 + beam_w_t
        maxLegsize = int((avbl_space - beam_w_t)/10) * 5
        if avbl_space < required_space:
            design_check = False
            logger.error(':Column cannot accommodate the given cleat agle due to space restriction  ')
            logger.warning(':Cleat legsize of the cleat angle should be less than or equal to %2.2f mm' %(maxLegsize)) 
            logger.info(':Decrease the cleat legsize')
        
    elif connectivity == 'Column web-Beam web':
        avbl_space = column_D - 2 * (column_f_t + column_R1)
        required_space = 2 * cleat_legsize_1 + beam_w_t
        maxLegsize = int((avbl_space - beam_w_t)/10) * 5
        if avbl_space < required_space:
            design_check = False
            logger.error(':Column cannot accommodate the given cleat agle due to space restriction')
            logger.warning(':Cleat legsize of the cleat angle should be less than or equal to %2.2f mm' %(maxLegsize)) 
            logger.info(':Decrease the cleat legsize')
    else:
        #Always feasible in this case.No checks required
        pass 
    ################################################################################
      
# Bolt design:
#     design_check = True
# I: Check for number of bolts -------------------
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade))*bolt_fu
    
    t_thinner_b = min(beam_w_t.real,cleat_thk.real);
    bolt_shear_capacity = 0
    if bolt_type == 'HSFG':
        bolt_shear_capacity = HSFG_bolt_shear(0.48, bolt_dia, 2, bolt_fu)
    if bolt_type == 'Black Bolt':
        bolt_shear_capacity = black_bolt_shear(bolt_dia, 2, bolt_fu)
        
    bolt_bearing_capacity =  bearing_capacity(bolt_dia, beam_w_t, bolt_fu,beam_fu)
    bearing_capacity_beam =  bearing_capacity(bolt_dia, beam_w_t , beam_fu,beam_fu)
    bearing_capacity_plt =   bearing_capacity(bolt_dia, cleat_thk , cleat_fu,beam_fu)
    bearing_capacity_b =  min(bolt_bearing_capacity, bearing_capacity_beam,bearing_capacity_plt)
    bolt_capacity = min(bolt_shear_capacity, bearing_capacity_b)
    bolt_capacity = bolt_capacity/2.0
    
    
    
#     print "capacity details" ,bolt_bearing_capacity ,bearing_capacity_plt ,bolt_shear_capacity,bearing_capacity_beam
    
    if shear_load !=0:
        bolts_required = int(math.ceil(shear_load/(2*bolt_capacity)))
    else:
        bolts_required = 0
        while  bolts_required == 0:
            design_check = False  
            break
    if bolts_required < 3  and bolts_required > 0 :
        bolts_required = 3
    
    if bolt_dia == 12 or bolt_dia == 14:
        dia_hole = bolt_dia + 1
    elif bolt_dia == 16 or bolt_dia == 18 or bolt_dia == 20 or bolt_dia == 22 or bolt_dia == 24:
        dia_hole = bolt_dia + 2
    else:
        dia_hole = bolt_dia + 3 
          
    min_pitch = int(2.5 * bolt_dia)
    min_gauge = int(2.5 * bolt_dia)
    min_edge_dist = int(1.7 * (dia_hole))
    max_edge_dist = int((12 * t_thinner_b * math.sqrt(250/bolt_fy)))-1
    
    kbchk1 = min_edge_dist/float(3*dia_hole)
    kbchk2 = min_pitch/float(3*dia_hole)-0.25
    kbchk3 = bolt_fu/float(beam_fu)
    kbchk4 = 1
    kb = min(kbchk1,kbchk2,kbchk3,kbchk4)
    kb = round(kb,3)
    ###########################Capacity Details for column bolts #######################################
    bolt_shear_capacity_c = bolt_shear_capacity/2
    if connectivity == 'Column web-Beam web' or connectivity == "Beam-Beam":
        thinner = min(column_w_t,cleat_thk)
        bolt_bearing_capacity_c = bearing_capacity(bolt_dia, thinner, bolt_fu, beam_fu)
        bearing_capacity_column = bearing_capacity(bolt_dia, column_w_t, beam_fu,beam_fu)
        bearing_capacity_cleat_c = bearing_capacity(bolt_dia, cleat_thk, beam_fu, beam_fu)
        bearing_capacity_c = min(bolt_bearing_capacity_c,bearing_capacity_column,bearing_capacity_cleat_c)
    else:
        thinner = min(column_f_t,cleat_thk)
        bolt_bearing_capacity_c = bearing_capacity(bolt_dia, thinner, bolt_fu, beam_fu)
        bearing_capacity_column = bearing_capacity(bolt_dia, column_f_t, beam_fu,beam_fu)
        bearing_capacity_cleat_c = bearing_capacity(bolt_dia, cleat_thk, beam_fu, beam_fu)
        bearing_capacity_c = min(bolt_bearing_capacity_c,bolt_bearing_capacity_c,bearing_capacity_column)

       
    bolt_capacity_c = min(bolt_shear_capacity_c,bearing_capacity_c)
    
    if shear_load != 0:
        bolts_required_c= int(math.ceil(shear_load/(2*bolt_capacity_c)))
    else:
        bolts_required_c = 0
    if bolts_required_c < 3:
        bolts_required_c = 3
    #####################local variable #################
    no_row_b = 0
    no_col_b = 0
    pitch_b = 0.0
    gauge_b = 0.0
    edge_dist_b = 0.0
    end_dist_b = 0.0
    cleat_length_b = 0.0
    
    no_row_c = 0
    no_col_c =0
    pitch_c = 0.0
    gauge_c = 0.0
    edge_dist_c = 0.0 
    end_dist_c = 0.0
    cleat_length_c = 0.0
    c_eccentricity = 0.0
    
#############################Length of the cleat angle given ###################### 
##################Beam Connection #################################################   
    if cleat_length != 0:
        no_row = bolts_required
        no_col = 1
        avbl_length = (cleat_length - 2 * min_edge_dist)
        pitch = avbl_length/(no_row - 1)
        test = True
        if pitch<min_pitch:
            test = False
            no_col = 2
            if no_row % 2 == 0:
                no_row = no_row/2
            else:
                no_row = (no_row+1)/2
            if no_row <= 2:
                no_row = 2
            gauge = min_gauge
            eccentricity = cleat_legsize - (min_edge_dist + gauge/2)
            pitch = avbl_length / (no_row - 1)
        else:
            no_col = 1
            gauge = 0
            eccentricity = cleat_legsize - min_edge_dist
            
        if shear_load != 0 :
            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
            if crit_shear > bolt_capacity :
                if no_col == 1:
                    while crit_shear > bolt_capacity and pitch > min_pitch:
                        no_row = no_row + 1
                        pitch = avbl_length/(no_row - 1)
                        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                    if pitch < min_pitch:
                        no_col = 2
                    elif bolt_capacity > crit_shear and pitch>min_pitch:
                        pass    
                    
                if no_col ==2:#Call math.ceil(x)
                    if test == True:
                        test = False
                        if no_row % 2  == 0:
                            no_row = no_row/2
                        else:
                            no_row = (no_row+1)/2
                    if no_row < 2:
                        no_row = 2
                    pitch = avbl_length/(no_row -1)
                    gauge = min_gauge
                    eccentricity = cleat_legsize - (min_edge_dist + gauge/2)
                    crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row) 
                    if crit_shear > bolt_capacity :
                        
                        while crit_shear > bolt_capacity and pitch > min_pitch:
                            no_row = no_row + 1
                            pitch = avbl_length/(no_row - 1)
                            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                        if pitch < min_pitch:
                            design_check = False
                            logger.error(':Critical shear force on the bolts due to loading is exceeding the bolt capacity')    
                            logger.warning(':Bolt capacity of the critical bolt should be greater than %2.2f KN' %(crit_shear))   
                            logger.info(':Re-design with increased bolt diameter or bolt grade')                        
                        elif bolt_capacity > crit_shear and pitch>min_pitch:
                            pass 
        else:
            crit_shear = 0
            
    ######################################Storing beam results to different variables########################################
        no_row_b = no_row
        no_col_b = no_col
        pitch_b = pitch
        gauge_b = gauge
        edge_dist_b = min_edge_dist 
        end_dist_b = min_edge_dist
        cleat_length_b = cleat_length
        critboltshear_b = crit_shear
        b_eccentricity  = eccentricity
        
    ################################## Column Calculation ###############################################
        no_row = bolts_required_c
        no_col = 1
        avbl_length = (cleat_length - 2 * min_edge_dist)
        pitch = avbl_length/(no_row - 1)
        end_dist = min_edge_dist
        test = True
        if pitch<min_pitch:
            test = False
            no_col = 2
            if no_row % 2 == 0:
                no_row = no_row/2
            else:
                no_row = (no_row+1)/2
            if no_row <= 2:
                no_row = 2
            gauge = min_gauge
            if (cleat_legsize_1 + beam_w_t/2 - end_dist -gauge) > 70:
                eccentricity = 70.0 + gauge/2
                end_dist = (cleat_legsize_1 + beam_w_t/2) - (70.0 + gauge)
            else:    
                eccentricity = (cleat_legsize_1 + beam_w_t/2) - (min_edge_dist + gauge/2)
                end_dist = min_edge_dist
            pitch = avbl_length / (no_row - 1)
        else:
            no_col = 1
            gauge = 0
            if (cleat_legsize_1 + beam_w_t/2 - end_dist - gauge) > 70:
                eccentricity = 70.0 + gauge/2
                end_dist = (cleat_legsize_1 + beam_w_t/2) - (70.0 + gauge)
            else:    
                eccentricity = (cleat_legsize_1 + beam_w_t/2) - (min_edge_dist + gauge/2)
                end_dist = min_edge_dist
            
        crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,min_edge_dist)
        if crit_shear > bolt_capacity_c :
            if no_col == 1:
                while crit_shear > bolt_capacity_c and pitch > min_pitch:
                    no_row = no_row + 1
                    pitch = avbl_length/(no_row - 1)
                    crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,min_edge_dist)
                if pitch < min_pitch:
                    no_col = 2
                elif bolt_capacity_c > crit_shear and pitch>min_pitch:
                    pass    
                
            if no_col ==2:#Call math.ceil(x)
                if test == True:
                    test = False
                    if no_row % 2  == 0:
                        no_row = no_row/2
                    else:
                        no_row = (no_row+1)/2
                if no_row < 2:
                    no_row = 2
                pitch = avbl_length/(no_row -1)
                gauge = min_gauge
                if (cleat_legsize_1 + beam_w_t/2 - end_dist - gauge) > 70:
                    eccentricity = 70.0 + gauge/2
                    end_dist = (cleat_legsize_1 + beam_w_t/2) - (70.0 + gauge)
                else:    
                    eccentricity = (cleat_legsize_1 + beam_w_t/2) - (min_edge_dist + gauge/2)
                    end_dist = min_edge_dist
        
                crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,min_edge_dist)
                if crit_shear > bolt_capacity_c :
                    
                    while crit_shear > bolt_capacity_c and pitch > min_pitch:
                        no_row = no_row + 1
                        pitch = avbl_length/(no_row - 1)
                        crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,min_edge_dist)
                    if pitch < min_pitch:
                        design_check = False
                        logger.error(':Critical shear force on the bolts due to loading is exceeding the bolt capacity')    
                        logger.warning(':Bolt capacity of the critical bolt should be greater than %2.2f KN' %(crit_shear))   
                        logger.info(':Re-design with increased bolt diameter or bolt grade')        
                    elif bolt_capacity_c > crit_shear and pitch>min_pitch:
                        pass 
    ##########################################################################
        no_row_c = no_row
        no_col_c = no_col
        pitch_c = pitch
        gauge_c = gauge
        edge_dist_c = min_edge_dist 
        end_dist_c = end_dist
        cleat_length_c = cleat_length
        c_eccentricity = eccentricity     
        critboltshear_c = crit_shear
 
########################################### length of the cleat angle not given #########################
    else:
        no_row = bolts_required
        no_col = 1
        cleat_length = (no_row - 1) * min_pitch + 2 * min_edge_dist
        pitch = min_pitch
        max_cleat_length = beam_D - 2 *(beam_f_t + beam_R1)
        edge_dist = min_edge_dist
        test = True
        if cleat_length > max_cleat_length:
            test = False
            no_col = 2
            if no_row % 2 == 0:
                no_row = no_row/2
            else:
                no_row = (no_row+1)/2
            if no_row < 2:
                no_row = 2
                
            gauge = min_gauge
            eccentricity = cleat_legsize - (gauge/2 + min_edge_dist)
        else:
            no_col = 1
            gauge = 0
            eccentricity = cleat_legsize - (gauge/2 + min_edge_dist)
        if shear_load != 0:
            
            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
            if crit_shear > bolt_capacity :
                if no_col == 1:
                    while crit_shear > bolt_capacity and cleat_length <  max_cleat_length:
                        no_row = no_row + 1
                        cleat_length = cleat_length + pitch
                        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                    if cleat_length > max_cleat_length:
                        no_col = 2
                    elif bolt_capacity > crit_shear and cleat_length < max_cleat_length:
                        pass    
                     
                if no_col ==2:#Call math.ceil(x)
                    if test == True:
                        test = False
                        if no_row % 2  == 0:
                            no_row = no_row/2
                        else:
                            no_row = (no_row+1)/2
                    if no_row <= 2:
                        no_row = 2
                        
                    cleat_length = (no_row - 1) * min_pitch + 2 * min_edge_dist
    #                 if cleat_length < 0.6 * beam_D:
    #                     cleat_length = 0.6 * beam_D
    #                     edge_dist = (cleat_length - (no_row -1) * pitch)/2
    #                 else:
    #                     edge_dist = min_edge_dist
                    gauge = min_gauge
                    eccentricity = cleat_legsize - (gauge/2 + min_edge_dist)
                    crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row) 
                    if crit_shear > bolt_capacity :
                         
                        while crit_shear > bolt_capacity and cleat_length <  max_cleat_length:
                            no_row = no_row + 1
                            cleat_length = cleat_length + pitch
                            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                        if cleat_length > max_cleat_length:
                            design_check = False
                            logger.error(':Critical shear force on the bolts due to loading is exceeding the bolt capacity')    
                            logger.warning(':Bolt capacity of the critical bolt should be greater than %2.2f KN' %(crit_shear))   
                            logger.info(':Re-design with increased bolt diameter or bolt grade')        
                        elif bolt_capacity > crit_shear and cleat_length <= max_cleat_length:
                            pass       
            #             if end_dist > min_edge_dist and cleat_length > 0.6 * beam_D :
            #                 end_dist = min_edge_dist
            #                 cleat_length = (no_row -1) * pitch + 2 * min_edge_dist
        
            if cleat_length < 0.6 * beam_D:
                cleat_length = 0.6 * beam_D
                edge_dist = (cleat_length - (no_row -1) * pitch)/2
        else:
            crit_shear = 0
        
    ######################################Storing beam results to different variables######################
        no_row_b = no_row
        no_col_b = no_col
        pitch_b = pitch
        gauge_b = gauge
        edge_dist_b = edge_dist
        end_dist_b = min_edge_dist
        cleat_length_b = cleat_length
        critboltshear_b = crit_shear
        b_eccentricity  = eccentricity
    ################################## Column Calculation ###############################################
        no_row = bolts_required_c
        no_col = 1
        cleat_length = (no_row - 1) * min_pitch + 2 * min_edge_dist
        pitch = min_pitch
        max_cleat_length = beam_D - 2 *(beam_f_t + beam_R1)
        edge_dist = min_edge_dist
        end_dist = min_edge_dist
        test = True
        if cleat_length > max_cleat_length:
            test = False
            no_col = 2
            if no_row % 2 == 0:
                no_row = no_row/2
            else:
                no_row = (no_row+1)/2
            if no_row < 2:
                no_row = 2
                
            gauge = min_gauge
            if (cleat_legsize_1 + beam_w_t/2 - end_dist - gauge) > 70:
                eccentricity = 70.0 + gauge/2
                end_dist = (cleat_legsize_1 + beam_w_t/2) - (70.0 + gauge)
            else:    
                eccentricity = (cleat_legsize_1 + beam_w_t/2) - (min_edge_dist + gauge/2)
                end_dist = min_edge_dist
            
        else:
            no_col = 1
            gauge = 0
            if (cleat_legsize_1 + beam_w_t/2 - end_dist -gauge) > 70:
                eccentricity = 70.0 + gauge/2
                end_dist = (cleat_legsize_1 + beam_w_t/2) - (70.0 + gauge)
            else:    
                eccentricity = (cleat_legsize_1 + beam_w_t/2) - (min_edge_dist + gauge/2)
                end_dist = min_edge_dist
           
             
        crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,edge_dist)
        if crit_shear > bolt_capacity_c :
            if no_col == 1:
                while crit_shear > bolt_capacity_c and cleat_length <  max_cleat_length:
                    no_row = no_row + 1
                    cleat_length = cleat_length + pitch
                    crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,edge_dist)
                if cleat_length > max_cleat_length:
                    no_col = 2
                elif bolt_capacity_c > crit_shear and cleat_length < max_cleat_length:
                    pass    
                 
            if no_col ==2:#Call math.ceil(x)
                if test == True:
                    test = False
                    if no_row % 2  == 0:
                        no_row = no_row/2
                    else:
                        no_row = (no_row+1)/2
                if no_row < 2:
                    no_row = 2
                    
                cleat_length = (no_row - 1) * min_pitch + 2 * min_edge_dist
#                 if cleat_length < 0.6 * beam_D:
#                     cleat_length = 0.6 * beam_D
#                     edge_dist = (cleat_length - (no_row -1) * pitch)/2
#                 else:
#                 edge_dist = min_edge_dist
                gauge = min_gauge
                if (cleat_legsize_1 + beam_w_t/2 - end_dist -gauge) > 70:
                    eccentricity = 70.0 + gauge/2
                    end_dist = (cleat_legsize_1 + beam_w_t/2) - (70.0 + gauge)
                else:    
                    eccentricity = (cleat_legsize_1 + beam_w_t/2) - (min_edge_dist + gauge/2)
                    end_dist = min_edge_dist
                    
                crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,edge_dist) 
                if crit_shear > bolt_capacity_c :
                     
                    while crit_shear > bolt_capacity_c and cleat_length <  max_cleat_length:
                        no_row = no_row + 1
                        cleat_length = cleat_length + pitch
                        crit_shear = column_critical_shear(shear_load, eccentricity, pitch, gauge, no_row,edge_dist)
                    if cleat_length > max_cleat_length:
                        design_check = False
                        logger.error(':Shear force on the critical bolt due to external load is exceeding the bolt capacity') 
                        logger.warning(':Bolt capacity of the critical bolt should be greater than %2.2f KN' %(crit_shear))   
                        logger.info(':Re-design with increased bolt diameter or bolt grade')        
                    elif bolt_capacity_c > crit_shear and cleat_length <= max_cleat_length:
                        pass       
        #             if end_dist > min_edge_dist and cleat_length > 0.6 * beam_D :
        #                 end_dist = min_edge_dist
        #                 cleat_length = (no_row -1) * pitch + 2 * min_edge_dist
        if cleat_length < 0.6 * beam_D:
            cleat_length = 0.6 * beam_D
            edge_dist = (cleat_length - (no_row -1) * pitch)/2
    ####################################Storing to a Seperate Variables######################################
        no_row_c = no_row
        no_col_c = no_col
        pitch_c = pitch
        gauge_c = gauge
        edge_dist_c = edge_dist
        end_dist_c = end_dist
        cleat_length_c = cleat_length
        c_eccentricity = eccentricity 
        critboltshear_c = crit_shear
    #################################################Deciding final Design outcomes based on column and beam connectivity design #######
    if cleat_length_b > cleat_length_c:
        cleat_length = cleat_length_b
        edge_dist_c = (cleat_length - (no_row_c -1) * pitch_c)/2
    else:
        cleat_length = cleat_length_c
        edge_dist_b = (cleat_length - (no_row_b -1) * pitch_b)/2
        
    ############################################All the checks########################################################
    b_end_distance = cleat_legsize-(20 + min_edge_dist + gauge_b) 
    if b_end_distance < min_edge_dist:#is it neccessary to treat single and double line seperately?
        design_check = False
        logger.error(':Edge distance in the beam web is less than the minimum edge distance as per IS 800:2007[cl.10.2.4.2]')    
        logger.warning(':Minimum leg size of the cleat Angle required is %s mm' %(str(2*min_edge_dist + 20 + gauge_b)))
        logger.info(':Increase the cleat leg size')#change reference
    b_gauge  = (2 * cleat_legsize_1 + beam_w_t) - 2*(end_dist_c + gauge_c)
    connection = "column"
    if connectivity == "Beam-Beam":
        connection = "primary beam"

    if b_gauge < 90:
        
        design_check = False
        logger.error(':Cross center distance between bolt lines in %s on either side of the supported beam is less than the specified gauge [reference-JSC:ch.4 check-1]' %(str(connection)))
        logger.warning(':Minimum specified cross center gauge is 90 mm')
        logger.info(':Increase the cleat leg size')
    if b_gauge > 140:
        design_check = False
        logger.error(':Cross center distance between bolt lines in %s on either side of supported the beam is greater than the specified gauge[reference-JSC:ch.4 check-1]' %(str(connection)))
        logger.warning(':Maximum specified cross center gauge is 140 mm')
        logger.info(':Decrease the cleat leg size')
        
    #block shear
    Tdb_B = blockshear(no_row_b, no_col_b, dia_hole, beam_fy, beam_fu, end_dist_b, edge_dist_b, pitch_b, gauge_b, cleat_thk)
    Tdb_C = blockshear(no_row_c, no_col_c, dia_hole, beam_fy, beam_fu, end_dist_c, edge_dist_c, pitch_c, gauge_c, cleat_thk)  
    
    Tdb = min(Tdb_B,Tdb_C)
    if Tdb_B <= shear_load or Tdb_C <= shear_load :
        design_check = False
        logger.error(": The block shear capacity of the cleat Angle is lass than the applied shear force [cl. 6.4.1]")
        logger.warning(": Minimum block shear capacity required is %2.2f KN " %(shear_load))
        logger.info(":Block shear capacity of the cleat angle is %2.2f KN" %(Tdb))
        logger.info(": Increase the cleat angle thickness")  
    ###############Moment Demand and Moment Capacity ##################
    moment_demand_c = 0.5 * shear_load * c_eccentricity / 1000
    moment_capacity_c = 1.2 * cleat_fy * cleat_thk * cleat_length * cleat_length / 1000000
    if moment_capacity_c < moment_demand_c:
        design_check = False
        logger.error(":Moment capacity of the cleat angle leg  is less than the moment demand [cl. 8.2.1.2]")
        logger.info(":Re-design with increased plate dimensions")
    moment_demand_b = 0.5 * shear_load * b_eccentricity / 1000
    moment_capacity_b = 1.2 * cleat_fy * cleat_thk * cleat_length * cleat_length / 1000000
    if moment_capacity_b < moment_demand_b:
        design_check = False
        logger.error(":Moment capacity of the cleat angle leg  is less than the moment demand [cl. 8.2.1.2]")
        logger.info(":Re-design with increased plate dimensions")
    #########################feeding output to array ###############
    outputObj = {}
    outputObj['Bolt'] ={}
    outputObj['Bolt']['status'] = True
    outputObj['Bolt']['shearcapacity'] = round(bolt_shear_capacity,3)
    outputObj['Bolt']['bearingcapacity'] = round(bearing_capacity_b,3)
    outputObj['Bolt']['bearingcapacitybeam'] = round(bearing_capacity_beam,3)
    outputObj['Bolt']['bearingcapacitycleat'] = round(bearing_capacity_plt,3)
    outputObj['Bolt']['boltcapacity'] = round(2 * bolt_capacity,3)
    outputObj['Bolt']['boltbearingcapacity'] = round(bolt_bearing_capacity,3)
    outputObj['Bolt']['externalmoment'] = round(moment_demand_b,3)
    outputObj['Bolt']['momentcapacity'] = round(moment_capacity_b,3)

    outputObj['Bolt']['blockshear'] = round(Tdb_B,3)
    outputObj['Bolt']['critshear'] = round(critboltshear_b,3)
    
    outputObj['Bolt']['numofbolts'] = no_row_b * no_col_b
    outputObj['Bolt']['boltgrpcapacity'] = round(2 * bolt_capacity * no_row_b * no_col_b,3)
    outputObj['Bolt']['numofrow'] = int(no_row_b)
    outputObj['Bolt']['numofcol'] = int(no_col_b) 
    outputObj['Bolt']['pitch'] = int(pitch_b)
    outputObj['Bolt']['enddist'] = int(end_dist_b)
    outputObj['Bolt']['edge'] = int(edge_dist_b)
    outputObj['Bolt']['gauge'] =int(gauge_b)
    outputObj['Bolt']['thinner'] = float(t_thinner_b)
    outputObj['Bolt']['diahole'] = float(dia_hole)
    outputObj['Bolt']['kb'] = float(kb)
    
#     outputObj['Bolt']['grade'] = bolt_grade

      
     
    outputObj['cleat'] = {}
    outputObj['cleat']['numofbolts'] = 2*no_row_c * no_col_c
    outputObj['cleat']['height'] = int(cleat_length)
    outputObj['cleat']['externalmoment'] = round(moment_demand_c ,3)
    outputObj['cleat']['momentcapacity'] = round(moment_capacity_c,3)
    outputObj['cleat']['numofrow'] = no_row_c
    outputObj['cleat']['numofcol'] = no_col_c
    
    outputObj['cleat']['pitch'] = int(pitch_c)
    outputObj['cleat']['guage'] = int(gauge_c)
    outputObj['cleat']['edge'] = edge_dist_c
    outputObj['cleat']['end'] = end_dist_c
    outputObj['cleat']['legsize'] = cleat_legsize_1
    outputObj['cleat']['thinner'] = float(thinner)
 
    outputObj['cleat']['shearcapacity'] = round(bolt_shear_capacity_c,3)
    outputObj['cleat']['bearingcapacity'] = round(bearing_capacity_c,3)
    outputObj['cleat']['boltcapacity'] = round(bolt_capacity_c,3)
    outputObj['cleat']['bearingcapacitycolumn'] = round(bearing_capacity_column,3)
    outputObj['cleat']['bearingcapacitycleat'] = round(bearing_capacity_cleat_c,3)
    outputObj['cleat']['boltgrpcapacity'] = round(2 * bolt_capacity_c * no_row_c * no_col_c,3)
    outputObj['cleat']['boltbearingcapacity'] = round(bolt_bearing_capacity_c,3)
    outputObj['cleat']['blockshear'] = round(Tdb_C,3)     
    outputObj['cleat']['critshear'] = round(critboltshear_c,3)

          

    if bolts_required == 0 or bolts_required_c == 0:
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                outputObj[k][key] = ""
                
    if design_check == False:
        for k in outputObj.keys():
            for key in outputObj[k].keys():
                outputObj[k][key] = ""
                
    
                    
    if design_check == True:  
        logger.info(": Overall cleat Angle connection design is safe \n")
        logger.debug(" :=========End Of design===========")
          
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")
     
    return outputObj                          
    



