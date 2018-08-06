
from numpy import float
import cmath
import math
import sys
from Connections.connection_calculations import ConnectionCalculations

from model import *
import logging
flag = 1
logger = None


def module_setup():
    
    global logger
    logger = logging.getLogger("osdag.endPlateCalc")

module_setup()

def net_area_calc(dia):
    '''

    Args:
        dia (int) diameter of bolt

    Returns
        Net area of bolts at threaded portion (Ref. Table 5.11 Subramanian's book, page: 358 )

    '''
    net_area = {5: 15.3, 6: 22.04, 8: 39.18, 10: 61.23, 12: 84.5, 16: 157, 20: 245, 22: 303, 24: 353, 27: 459, 30: 561, 36: 817}
    return net_area[dia]



# BOLT: determination of shear capacity of black bolt = fu * n * A / (root(3) * Y)
def black_bolt_shear(dia, n, fu):
    '''

    Args:
        dia (int) diameter of bolt
        n (str) number of shear plane(s) through which bolt is passing
        fu (float) ultimate tensile strength of a bolt

    Returns:
        Shear capacity of bearing type bolt in kN

    '''
    A = net_area_calc(dia)
    root3 = math.sqrt(3)
    Vs = fu * n * A / (root3 * 1.25 * 1000)
    Vs = round(Vs.real, 3)
    return Vs

# NOT present in CAD_notchB-B branch
############ REDUCTION FACTORS FOR BOLTS ############
# Check added by Danish Ansari on 13th June 2017
# Check for Long joints & Large grip lengths, IS 800:2007 Cl 10.3.3.1 & Cl 10.3.3.2

def get_reduction_factor(bolt_shear_capacity, connectivity, bolt_dia, bolts_required, pitch, end_plate_t, column_f_t,column_w_t, beam_w_t):
    '''

    Args:
        bolt_shear_capacity (float)
        connectivity
        bolt_dia (int) diameter of bolt
        bolts_required (str)
        pitch (float)
        end_plate_t (float)
        column_f_t (float)
        column_w_t (float)
        beam_w_t (float)

    Returns:
        Shear capacity of bolt after multiplying the reduction factors (i.e beta_lg & beta_lj. Ref. IS 800:2007 Cl 10.3.3.2 & Cl 10.3.3.1)

    '''

    l_j = ((bolts_required/2) - 1) * pitch  # length of joint in direction of load transfer
    if l_j > 15 * bolt_dia:
        beta_long_joints = 1.075 - 0.005 * (l_j / bolt_dia)
        if beta_long_joints <= 0.75 or beta_long_joints >= 1.0:
            beta_long_joints = 0.875  # assuming the value of beta_long_joints is average of 0.75 and 1.0
        else:
            beta_long_joints = 1.075 - 0.005 * (l_j / bolt_dia)
    else:
        beta_long_joints = int(1)

    beta_l_j = beta_long_joints

    # Check for Large grip lengths
    # Function for Large grip length, beta_lg (reduction factor to be multiplied to shear capacity of bearing bolt)
    # Ref: IS 800:2007 Cl 10.3.3.2

    if connectivity == "Column flange-Beam web":
        l_g = column_f_t + end_plate_t
        if l_g > (5 * bolt_dia):
            beta_lg = 8 / (3 + (l_g / bolt_dia))
        else:
            beta_lg = int(1)
    elif connectivity == "Column web-Beam web":
        l_g = column_w_t + end_plate_t
        if l_g > (5 * bolt_dia):
            beta_lg = 8 / (3 + (l_g / bolt_dia))
        else:
            beta_lg = int(1)
    else:
        l_g = beam_w_t + end_plate_t
        if l_g > (5 * bolt_dia):
            beta_lg = 8 / (3 + (l_g / bolt_dia))
        else:
            beta_lg = int(1)

    beta_l_g = beta_lg
    bolt_shear_capa = bolt_shear_capacity * beta_l_g *beta_l_j
    return bolt_shear_capa
#######################################################################

# BOLT: determination of bearing capacity = 2.5 * kb * d * t * fu / Y
def bolt_bearing(dia, t, fu, kb):
    '''

    Args:
        dia (int) diameter of bolt
        t (float) summation of thickneses of the connected plates experencing bearing stress in same direction, or if the bolts are countersunk, the thickness of plate minus 1/2 of the depth of countersunk
        fu  (float) ultimate tensile strength of a bolt
        kb  (float) multiplying factor (Ref: Cl 10.3.4 IS 800:2007)

    Returns:
        Bearing capacity of bearing type bolt in kN

    '''
    Vb = 2.5 * kb * dia * t * fu / (1.25 * 1000)
    Vb = round(Vb.real, 3)
    return Vb


def end_plate_t_max(beam_depth, grade_bolt, dia):
    #TODO: Check on maximum endplate thickness with bolt diameter [Ref: INSDAG Teaching materials, pp 34-4]
    '''

    Args:
        beam_depth (float)
        grade_bolt (float)
        dia (int) Diameter of bolt

    Returns:
        Minimum thickness of end plate based on beam depth and grade of bolt (Ref. Subramanian's book page no 372 )

    '''
    if beam_depth < 450:
        max_endplate = 10
        # if grade_bolt <= 4.6:
        #     max_endplate = min(8, int(dia) / 3)
        # else:
        #     max_endplate = min(8, int(dia) / 2)
    else:
        max_endplate = 12
        # if grade_bolt <= 4.6:
        #     max_endplate = min(10, int(dia) / 3)
        # else:
        #     max_endplate = min(10, int(dia) / 2)
    return max_endplate

# ############ CRITICAL BOLT SHEAR CAPACITY ###################


def critical_bolt_shear(load, eccentricity, pitch, gauge, bolts_one_line):
    '''

    Args:
        load (float) Factored shear force/load
        eccentricity (float)
        pitch (float)
        gauge (float)
        bolts_one_line (str) number of bolts in one line

    Returns:
        Resultant shear load for type1 effect

    '''
    sigma = 0.0
    r_y = 0.0
    r_x = 0.0
    moment = load / (2 * eccentricity)
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


# #################### Block shear capacity of plates/members ##########################333

def blockshear(numrow, numcol, dia_hole, fy, fu, edge_dist, end_dist, pitch, gauge, thk):
    '''

    Args:
        numrow (str) Number of row(s) of bolts
        numcol (str) Number of column(s) of bolts
        dia_hole  (int) diameter of hole (Ref. Table 5.6 Subramanian's book, page: 340)
        fy (float) Yeild stress of material
        fu  (float) Ultimate stress of material
        edge_dist  (float) edge distance based on diameter of hole
        end_dist (float) end distance based on diameter of hole
        pitch (float) pitch distance based on diameter of bolt
        gauge  (float) pitch distance based on diameter of bolt
        thk (float) thickness of plate

    Returns:
        Capacity of fin plate under block shear

    '''
    if numcol == 1:
        area_shear_gross = thk * ((numrow - 1) * pitch + end_dist)
        area_shear_net = thk * ((numrow - 1) * pitch + end_dist - (numrow - 1 + 0.5) * dia_hole)
        area_tension_gross = thk * edge_dist
        area_tension_net = thk * (edge_dist - 0.5 * dia_hole)
        
        Tdb1 = (area_shear_gross * fy / (math.sqrt(3) * 1.1) + 0.9 * area_tension_net * fu / 1.25)
        Tdb2 = (0.9 * area_shear_net * fu / (math.sqrt(3) * 1.25) + area_tension_gross * fy / 1.1)
        Tdb = min (Tdb1, Tdb2)
        Tdb = round(Tdb / 1000, 3)
        
    elif numcol == 2:
        area_shear_gross = thk * ((numrow - 1) * pitch + end_dist)
        area_shear_net = thk * ((numrow - 1) * pitch + end_dist - (numrow - 1 + 0.5) * dia_hole)
        area_tension_gross = thk * (edge_dist + gauge)
        area_tension_net = thk * (edge_dist + gauge - 0.5 * dia_hole)
        
        Tdb1 = (area_shear_gross * fy / (math.sqrt(3) * 1.1) + 0.9 * area_tension_net * fu / 1.25)
        Tdb2 = (0.9 * area_shear_net * fu / (math.sqrt(3) * 1.25) + area_tension_gross * fy / 1.1)
        Tdb = min (Tdb1, Tdb2)
        Tdb = round(Tdb / 1000, 3)
        
    return Tdb


def end_connection(ui_obj):
    
    global logger
    beam_sec = ui_obj['Member']['BeamSection']
    column_sec = ui_obj['Member']['ColumSection']
    connectivity = ui_obj['Member']['Connectivity']
    beam_fu = float(ui_obj['Member']['fu (MPa)'])
    beam_fy = float(ui_obj['Member']['fy (MPa)'])
    column_fu = float(ui_obj['Member']['fu (MPa)'])
    column_fy = float(ui_obj['Member']['fy (MPa)'])
              
    shear_load = float(str(ui_obj['Load']['ShearForce (kN)']))

    bolt_dia = int(ui_obj['Bolt']['Diameter (mm)'])
    bolt_type = ui_obj["Bolt"]["Type"]
    bolt_grade = float(ui_obj['Bolt']['Grade'])
    bolt_fu = float(ui_obj["bolt"]["bolt_fu"])
    mu_f = float(ui_obj["bolt"]["slip_factor"])
    dp_bolt_hole_type = str(ui_obj['bolt']['bolt_hole_type'])
    gamma_mw = float(ui_obj["weld"]["safety_factor"])
    weld_type = ui_obj['weld']['typeof_weld']

    end_plate_t = float(ui_obj['Plate']['Thickness (mm)'])
    end_plate_w = str(ui_obj['Plate']['Width (mm)'])
    if end_plate_w == '':
        end_plate_w = 0
    else:
        end_plate_w = float(end_plate_w)

    end_plate_l = str(ui_obj['Plate']['Height (mm)'])
    if end_plate_l == '':
        end_plate_l = 0
    else:
        end_plate_l = float(end_plate_l)
        
    web_plate_fu = float(ui_obj['Member']['fu (MPa)'])
    web_plate_fy = float(ui_obj['Member']['fy (MPa)'])
    
    user_height = end_plate_l 
    user_width = end_plate_w
    
    weld_t = float(ui_obj["Weld"]['Size (mm)'])
    weld_fu = float(ui_obj["weld"]["weld_fu"])

    bolt_planes = 1
    # check input database required or not?
    dictbeamdata = get_beamdata(beam_sec)
    beam_w_t = float(dictbeamdata["tw"])
    beam_f_t = float(dictbeamdata["T"])
    beam_depth = float(dictbeamdata["D"])
    beam_R1 = float(dictbeamdata["R1"])

    old_beam_section = get_oldbeamcombolist()
    old_col_section = get_oldcolumncombolist()

    if beam_sec in old_beam_section or column_sec in old_col_section:
        logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")

    if beam_fu < 410 or beam_fy < 230 or column_fu < 410 or column_fy < 230:
        logger.warning(" : You are using a section of grade that is not available in latest version of IS 2062")


    if connectivity == "Column web-Beam web" or connectivity == "Column flange-Beam web":
        dictcolumndata = get_columndata(column_sec)
        column_w_t = float(dictcolumndata["tw"])
        column_f_t = float(dictcolumndata["T"])
        column_R1 = float(dictcolumndata["R1"])
        column_d = float(dictcolumndata["D"])
        column_b = float(dictcolumndata["B"])
    else:
        dictcolumndata = get_beamdata(column_sec)
        column_w_t = float(dictcolumndata["tw"])
        column_f_t = float(dictcolumndata["T"])
        column_R1 = float(dictcolumndata["R1"])
        column_d = float(dictcolumndata["D"])
        column_b = float(dictcolumndata["B"])

    if connectivity == "Beam-Beam":
        notch_ht = max([column_f_t, beam_f_t]) + max([column_R1, beam_R1]) + max([(column_f_t / 2), (beam_f_t / 2), 10])
        if notch_ht < (beam_depth/5):
            pass
        else:
            logger.warning(" : Depth of coping should preferably be less than D/5 (D: Secondary beam depth)")
    
    design_check = True

    sectional_gauge = 0.0
    gauge = 0.0
    pitch = 0.0
    eccentricity = 0.0
    dia_hole = 0
    bolt_shear_capacity = 0.0
    
# Plate thickness check
    max_end_plate_t = end_plate_t_max(beam_depth, bolt_grade, bolt_dia)
    if end_plate_t > max_end_plate_t:
        design_check = False
        logger.error(": Chosen end plate thickness is more than the maximum allowed [DoSS, N. Subramanian, page 372]")
        logger.warning(" : Maximum allowed plate thickness is %2.2f mm" % max_end_plate_t)
        logger.info(" : Decrease the end plate thickness")

# ############# BOLT CAPACITY ###############
#    0 def boltDesign(end_plate_l):
# I: Check for number of bolts -------------------

    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu

    if connectivity == "Column web-Beam web":
        t_thinner = min(column_w_t.real, end_plate_t.real)
    elif connectivity == "Column flange-Beam web":
        t_thinner = min(column_f_t.real, end_plate_t.real)
    else:
        t_thinner = min(column_w_t.real, end_plate_t.real)

    # Spacing of bolts for web plate -------------------
    # ######## According to IS 800 - 2007, table 9, clause no. 10.2.1 ##########################

    dia_hole = ui_obj["bolt"]["bolt_hole_clrnce"] + bolt_dia

        # Minimum/maximum pitch and gauge
    min_pitch = int(2.5 * bolt_dia)
    min_gauge = int(2.5 * bolt_dia)
    if min_pitch % 10 != 0 or min_gauge % 10 != 0:
        min_pitch = (min_pitch / 10) * 10 + 10
        min_gauge = (min_gauge / 10) * 10 + 10
    else:
        min_pitch = min_pitch
        min_gauge = min_gauge

    # ########## MAX SPACING BETWEEN BOLTS #####################
    max_spacing = int(min(100 + 4 * end_plate_t, 200))  # clause 10.2.3.3 is800

    # ############ END AND EDGE DISTANCES ###################
    if ui_obj["detailing"]["typeof_edge"] == "a - Sheared or hand flame cut":
        min_end_dist = int(float(1.7 * (dia_hole)))
    else:
        min_end_dist = int(1.5 * (dia_hole))
    min_edge_dist = min_end_dist

    kbchk1 = min_end_dist / float(3 * dia_hole)
    kbchk2 = min_pitch / float(3 * dia_hole) - 0.25
    kbchk3 = bolt_fu / float(beam_fu)
    kbchk4 = 1
    kb = min(kbchk1, kbchk2, kbchk3, kbchk4)
    kb = round(kb, 3)

    max_edge_dist = int((12 * end_plate_t * cmath.sqrt(250 / beam_fy)).real) - 1
    max_end_dist = int((12 * end_plate_t * cmath.sqrt(250 / beam_fy)).real) - 1

    if bolt_type == 'Friction Grip Bolt':
        muf = mu_f
        n_e = 1 # number of effective interfaces offering frictional resistance
        bolt_hole_type = dp_bolt_hole_type # 1 - standard hole, 0.85 - oversize hole
        bolt_shear_capacity = ConnectionCalculations.bolt_shear_friction_grip_bolt(bolt_dia, bolt_fu, muf, n_e, bolt_hole_type)
        bolt_bearing_capacity = 'N/A'
        bolt_capacity = bolt_shear_capacity

    elif bolt_type == "Bearing Bolt" :
        bolt_shear_capacity = black_bolt_shear(bolt_dia, bolt_planes, bolt_fu)
        bolt_bearing_capacity = bolt_bearing(bolt_dia, t_thinner, kb, beam_fu).real
        bolt_capacity = min(bolt_shear_capacity, bolt_bearing_capacity)

    # def bolt_bearing(dia, t, fu, kb):

    if shear_load != 0:
        #                 bolts_required = int(math.ceil(shear_load/(2*bolt_capacity)))
        bolts_required = float(math.ceil(shear_load / bolt_capacity))  # changing no of bolts into multiple of 4
        if bolts_required <= 3:
            bolts_required = 4
        elif bolts_required % 2 == 0:
            bolts_required = bolts_required
        elif bolts_required % 2 != 0:
            bolts_required = bolts_required + 1
    else:
        bolts_required = 0
        while bolts_required == 0:
            design_check = False
            break


    # ###################################################### CHECK 1: DETAILING PRACTICE ###############################################################
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
        # ########################### check critical bolt shear capacity #######################

        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
        if crit_shear > bolt_capacity:
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
                if test is True:
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
                if crit_shear > bolt_capacity:

                    while crit_shear > bolt_capacity and pitch > min_pitch:
                        no_row = no_row + 1
                        pitch = avbl_length / (no_row - 1)
                        crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                    if pitch < min_pitch:
                        design_check = False
                        logger.error(": Shear force on the critical bolt due to external load is more than the bolt capacity")
                        logger.warning(": Bolt capacity of the critical bolt is %2.2f" % (bolt_capacity))
                        logger.info(": Increase the diameter of the bolt or bolt grade")

                    elif bolt_capacity > crit_shear and pitch > min_pitch:
                        pass

        min_end_plate_l = 2 * min_end_dist + (no_row - 1) * min_pitch

        max_end_plate_l = beam_depth - (2 * (beam_f_t + beam_R1 + 5))  # 5mm is the gap

        if connectivity == "Column web-Beam web":
            max_end_plate_w = column_d - 2 * (column_f_t + column_R1)
        elif connectivity == "Column flange-Beam web":
            max_end_plate_w = column_b
        else:
            pass
        if end_plate_w != 0:
            if no_col == 1:
                sectional_gauge = end_plate_w - (2 * min_edge_dist)
                min_end_plate_w = 100 + (2 * min_edge_dist)
            else:
                sectional_gauge = end_plate_w - 2 * (min_edge_dist + gauge)
                min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            if connectivity == "Column flange-Beam web":
                if sectional_gauge < max(90, (column_w_t + (2 * column_R1) + (2*min_edge_dist))):
                    design_check = False
                    logger.error(": Cross center distance between the vertical bolt lines on either side of the beam is less than "
                             "specified gauge [reference JSC : chap. 5 check 1]")
                    logger.warning(": Minimum required cross center gauge is %2.2f mm" % (max(90,(column_w_t + (2* column_R1) + (2* min_edge_dist)) )))
                    logger.info(": Increase the plate width")
                else:
                    pass
            else:
                if sectional_gauge < 90:
                    design_check = False
                    logger.error(": Cross center distance between the bolt lines on either side of the beam is less than "
                            "specified gauge [reference JSC : chap. 5 check 1]")
                    logger.warning(": Minimum required cross center gauge is 90 mm")
                    logger.info(": Increase the plate width")
                else:
                    pass

            if sectional_gauge > 140:
                design_check = False
                logger.error(": Cross center distance between the vertical bolt lines on either side of the beam is greater than "
                             "specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Maximum permissible cross center gauge is 140 mm")
                logger.info(": Decrease the plate width")

        if end_plate_w == 0:
            min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            end_plate_w = min_end_plate_w
            sectional_gauge = 100

            if connectivity != "Beam-Beam":
                if min_end_plate_w > max_end_plate_w:
                    design_check = False
                    logger.error(": Calculated width of the end plate exceeds the width of the column")
                    logger.warning(": Minimum end plate width is %2.2f" % (min_end_plate_w))

        if end_plate_l < (0.6 * beam_depth):
            design_check = False
            logger.error(": The height of end plate is less than the minimum required height")
            logger.warning(": The minimum required height of end plate is %2.2f" % (0.6 * beam_depth))
            logger.info(": Increase the height of end plate")

        if end_plate_l > max_end_plate_l:
            design_check = False
            logger.error(": The height of end plate exceeds the maximum allowed value")
            logger.warning(": The maximum allowed height of end plate is %2.2f" % max_end_plate_l)
            logger.info(": Decrease the height of end plate")

    else:

        no_row = bolts_required / 2
        no_col = 1
        min_end_plate_l = 0.6 * beam_depth
        max_end_plate_l = beam_depth - 2 * (beam_f_t + beam_R1)
        req_end_plate_l = ((no_row-1) * min_pitch + 2 * min_end_dist)
        end_plate_l = max(0.6 * beam_depth, req_end_plate_l)
        avbl_length = (end_plate_l - 2 * min_end_dist)
        pitch = avbl_length / (no_row - 1)
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

# ############################################### check critical bolt shear capacity ################################################3
        if shear_load != 0:
            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)

            if crit_shear > bolt_capacity:
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
                    if test is True:
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
                    if crit_shear > bolt_capacity:

                        while crit_shear > bolt_capacity and end_plate_l < max_end_plate_l:
                            no_row = no_row + 1
                            end_plate_l = end_plate_l + pitch
                            crit_shear = critical_bolt_shear(shear_load, eccentricity, pitch, gauge, no_row)
                        if end_plate_l > max_end_plate_l:
                            design_check = False
                            logger.error(": Shear force on the critical bolt due to external load is more than the bolt capacity")
                            logger.warning(": Capacity of the critical bolt is %2.2f" % (bolt_capacity))
                            logger.info(": Increase the diameter of the bolt or bolt grade")
                        elif bolt_capacity > crit_shear and end_plate_l <= max_end_plate_l:
                            pass
        else:
            crit_shear = 0

# ############################ check end plate length ##########################################

        if end_plate_l < 0.6 * beam_depth:
            end_plate_l = 0.6 * beam_depth
            end_dist = (end_plate_l - (no_row - 1) * pitch) / 2

# ############################ check end plate height ##########################################
        if end_plate_l < min_end_plate_l:
            design_check = False
            logger.error(": The height of end plate is less than the minimum required height")
            logger.warning(": The minimum required height of end plate is %2.2f" % min_end_plate_l)
            logger.info(": Increase the height of end plate ")

        if end_plate_l > max_end_plate_l:
            design_check = False
            logger.error(": The height of end plate exceeds the maximum allowed value")
            logger.warning(": The maximum allowed height of end plate is %2.2f" % max_end_plate_l)
            logger.info(": Decrease the height of end plate ")


            # ############################ check end plate width ##########################################
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
                logger.error(": Cross center distance between the vertical bolt lines on either side of the beam is less than"
                             " specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Minimum required cross center gauge is 90 mm")
                logger.info(": Increase the plate width")

            if sectional_gauge > 140:
                design_check = False
                logger.error(": Cross center distance between the vertical bolt lines on either side of the beam is greater than "
                             "specified gauge [reference JSC : chap. 5 check 1]")
                logger.warning(": Maximum allowed cross center gauge is 140 mm")
                logger.info(": Decrease the plate width")
        if end_plate_w == 0:
            min_end_plate_w = 100 + 2 * (min_edge_dist + gauge)
            end_plate_w = min_end_plate_w
            sectional_gauge = 100
            if connectivity != "Beam-Beam":

                if min_end_plate_w > max_end_plate_w:
                    design_check = False
                    logger.error(": Calculated width of the end plate exceeds the width of the column")
                    logger.warning(": Minimum end plate width is %2.2f mm" % (min_end_plate_w))

######### Check for shear capacity of bolt after multiplying the reduction factors (beta_l_g and beta_l_j) #####

    bolt_shear_capacity = get_reduction_factor(bolt_shear_capacity, connectivity, bolt_dia, bolts_required, pitch,
                                               end_plate_t, column_f_t, column_w_t, beam_w_t)                                                           

# ################ CHECK 2: SHEAR CAPACITY OF BEAM WEB ####################

    shear_capacity_beam = 0.6 * beam_fy * 0.9 * end_plate_l * beam_w_t / 1000

    if shear_load > shear_capacity_beam:
        design_check = False
        logger.error(": Shear capacity of the beam web at the end plate is less than the external load")
        logger.warning(": Shear capacity of the beam web is %2.2f kN" % (shear_capacity_beam))
        logger.info(": Increase the end plate height if possible, else select a deeper beam section")

# ################ CHECK 3: BLOCK SHEAR ####################
#     min_thk = min(end_plate_t,beam_w_t)
    min_thk = end_plate_t
    Tdb = 2 * blockshear(no_row, no_col, dia_hole, beam_fy, beam_fy, min_edge_dist, end_dist, pitch, gauge, min_thk)

    if Tdb < shear_load:
        design_check = False
        logger.error(": Block shear capacity of the plate is less than the applied shear force [cl. 6.4.1]")
        # logger.warning(": Minimum block shear capacity required is % 2.2f kN" % shear_load)
        logger.warning(
            ": Available block shear capacity is %2.2f kN which is less than required %2.2f kN" % (Tdb, shear_load))
        logger.info(": Increase the plate thickness or the plate height")

# ################ CHECK 4: FILLET WELD ###################

    # Assumption: Weld electrode is stronger than parent metal
    weld_fu_govern = min(weld_fu, beam_fu)    # cl. 10.5.7.1
    weld_l = end_plate_l - 2 * weld_t
    Vy1 = (shear_load) / float(2 * weld_l)
    Vy1 = round(Vy1, 3)
    weld_strength = 0.7 * weld_t * weld_fu_govern / (math.sqrt(3) * 1000 * gamma_mw)
    weld_strength = round(weld_strength, 3);
    if Vy1 > weld_strength:
        design_check = False
        logger.error(": Weld strength is less than the shear demand [cl. 10.5.9]")
        logger.warning(": Weld strength should be greater than %2.2f kN/mm" % (weld_strength))
        logger.info(": Increase the weld size")

    ############## Check for minimum weld thickness: Table 21; IS 800 ###########
    # Here t_thicker indicates thickness of thicker part

    t_thicker = max(beam_w_t.real, end_plate_t.real)

    if float(t_thicker) > 0 and float(t_thicker) <= 10:
        weld_t_min = int(3)
    elif float(t_thicker) > 10 and float(t_thicker) <= 20:
        weld_t_min = int(5)
    elif float(t_thicker) >= 20 and float(t_thicker) <= 32:
        weld_t_min = int(6)
    else:
        weld_t_min = int(10)

    weld_t_req = weld_t_min

    if weld_t < weld_t_req:
        design_check = False
        logger.error(": Weld thickness is not sufficient [cl. 10.5.2.3 and Table 21]")
        logger.warning(": Minimum weld thickness required is %2.2f mm " % (weld_t_req))
        logger.info(": Increase the weld thickness or the length of weld/end plate")

    ############## Check for maximum weld thickness: cl: 10.5.3.1 ; IS 800 ###########

    """ Here t_thinner_beam_plate indicates thickness of thinner part of members
        connected by the fillet weld. ie., Beam web and End plate
    """
    t_thinner_beam_plate = min(beam_w_t.real, end_plate_t.real)

    max_weld_t = t_thinner_beam_plate

    if weld_t > max_weld_t:
        design_check = False
        logger.error(": Weld thickness is more than maximum allowed weld thickness [cl. 10.5.3.1]")
        logger.warning(": Maximum weld thickness allowed is %2.2f mm " % (max_weld_t))
        logger.info(": Decrease the weld thickness")

    # End of calculation
    output_obj = {}
    output_obj['Bolt'] = {}
    output_obj['Bolt']['status'] = design_check
    output_obj['Bolt']['shearcapacity'] = round(bolt_shear_capacity, 2)
    output_obj['Bolt']['bearingcapacity'] = bolt_bearing_capacity
    output_obj['Bolt']['boltcapacity'] = round(bolt_capacity, 2)
    output_obj['Bolt']['numofbolts'] = int(2 * no_col * no_row)
    output_obj['Bolt']['boltgrpcapacity'] = float(round((bolt_capacity * 2 * no_col * no_row), 2))
    output_obj['Bolt']['numofrow'] = int(no_row)
    output_obj['Bolt']['numofcol'] = int(2 * no_col)
    output_obj['Bolt']['pitch'] = round(float(pitch), 2)
    output_obj['Bolt']['enddist'] = float(end_dist)
    output_obj['Bolt']['edge'] = float(edge_dist)
    output_obj['Bolt']['gauge'] = round(float(gauge), 2)
    output_obj['Bolt']['thinner'] = float(t_thinner)
    output_obj['Bolt']['dia_hole'] = float(dia_hole)
    output_obj['Bolt']['bolt_fu'] = float(bolt_fu)
    output_obj['Bolt']['bolt_fy'] = float(bolt_fy)
    output_obj['Bolt']['critshear'] = float(round(crit_shear, 2))
    output_obj['Bolt']['kb'] = round(float(kb), 2)

    output_obj['Weld'] = {}
    output_obj['Weld']['weldshear'] = Vy1
    output_obj['Weld']['weldlength'] = weld_l
    output_obj['Weld']['weldstrength'] = weld_strength
    output_obj['Weld']['thickness'] = weld_t_req
    output_obj['Weld']['thicknessprovided'] = weld_t

    output_obj['Plate'] = {}
    output_obj['Plate']['height'] = float(end_plate_l)
    output_obj['Plate']['width'] = float(end_plate_w)
    output_obj['Plate']['MaxThick'] = float(max_end_plate_t)
    output_obj['Plate']['MinWidth'] = float(min_end_plate_w)
    output_obj['Plate']['blockshear'] = float(Tdb)
    output_obj['Plate']['Sectional Gauge'] = float(sectional_gauge)

    if weld_type == 'Shop weld':
        if weld_t < 6:
            logger.warning(" : Minimum recommended weld thickness for shop weld is 6 mm")
    else:
        if weld_t < 8:
            logger.warning(" : Minimum recommended weld thickness for field weld is 8 mm")

    if end_plate_t < 8:
        logger.warning(
            " : Minimum recommended wend plate thickness is 8 mm to avoid weld distortion during fabrication and"
            " damage during transportation [Reference: SCI Steel Designers' Manual - 7th Edition (2012)")

    if output_obj['Bolt']['status'] is True:

        logger.info(": Overall end plate connection design is safe \n")
        logger.debug(" :=========End Of design===========")

    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")
    return output_obj
