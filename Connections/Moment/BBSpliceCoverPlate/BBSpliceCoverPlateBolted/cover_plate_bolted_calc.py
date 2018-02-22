'''
Created on 30-Oct-2017

@author: Swathi M.
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
    logger = logging.getLogger("osdag.coverPlateBoltedCalc")
module_setup()

########################################################################################################################
# Reference:
########################################################################################################################
### 1. Example 10.14 - M.L. Gambhir (page 10.83)
### 2. Example 5.27 - N. Subramanian (page 427)
### 3. IS 800 : 2007
### 4. 30 good rules for connection design, AISC
### 5. Steel Designer's Manual - 6th Edition (2003)
### 6. Bolted field splices for steel bridge flexural members AISC - overview and design example: Design example 3.1
### 7. INSDAG design example
### 8. Structural steel work connections - Graham Owens (Design Examples)


'''

ASCII diagram - Beam-Beam Bolted Splice Connection with Cover Plates

                                                           +-----+ Flange splice plate
                                                           |
                      ++         ++        ++          ++  |      ++        ++
                 +----||---------||--------||----++----||--v------||--------||----+
    +------------+----||---------||--------||----++----||---------||--------||----+------------+
    +-----------------||---------||--------||----++----||---------||--------||-----------------+
    |                 ++         ++        ++    ||    ++         ++        ++                 |
    |                                            ||                                            |
    |   BEAM                            +------------------+                                   |
    |                                   |        ||        |                                   |
    |                                   |   x    ||    x   |                                   |
    |                                   |        ||        |                                   |
    |                                   |        ||        <------+ Web splice plate           |
    |                                   |   x    ||    x   |                                   |
    |                                   |        ||        |                                   |
    |                                   |        ||        |                                   |
    |                                   |   x    ||    x   |                                   |
    |                                   |        ||        |                                   |
    |                                   +------------------+                                   |
    |                                            ||                                            |
    |                 ++         ++        ++    ||    ++         ++         ++                |
    +-----------------||---------||--------||----++----||---------||---------||----------------+
    +-----------------||---------||--------||----++----||---------||---------||----------------+
                 +----||---------||--------||----++----||---------||---------||---+
                      ++         ++        ++          ++         ++         ++
'''

########################################################################################################################
# Total moment acting on the section (kN-m)
def total_moment(beam_d, beam_f_t, axial_force, moment_load):
    """

    Args:
        beam_d: Overall depth of the beam section in mm (float)
        beam_f_t: Thickness of flange in mm (float)
        axial_force: Factored axial force in kN (float)
        moment_load: Factored bending moment in kN-m (float)

    Returns:
        Total moment acting on the section in kN-m (float)

    """
    cg = (beam_d/2)-(beam_f_t/2)  # Assumption: Axial force acts exactly at the center of the section
    moment_axial_force = (axial_force * cg)/1000  # Moment due to factored axial force = F * centroidal distance  (kN-m)
    total_moment = moment_load + moment_axial_force
    return round(total_moment, 1)  # kN-m

########################################################################################################################
# Force in flange (kN)  [Reference: M.L. Gambhir (page 10.83), N. Subramanian (page 427)]
def flange_force(beam_d, beam_f_t, axial_force, moment_load):
    """

    Args:
       beam_d: Overall depth of the beam section in mm (float)
       beam_f_t: Thickness of flange in mm (float)
       axial_force: Factored axial force in kN (float)
       moment_load: Factored bending moment in kN-m (float)

    Returns:
        Force in flange in kN (float)

    """
    tm = total_moment(beam_d, beam_f_t, axial_force, moment_load)
    return round((tm*1000)/(beam_d - beam_f_t), 2)        # kN

########################################################################################################################
# Thickness of flange splice plate [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)]
def thk_flange_plate(beam_d, beam_f_t, axial_force, moment_load,beam_b,beam_fy, dia_hole):
    """

    Args:
        beam_d: Overall depth of the beam section in mm (float)
        beam_f_t: Thickness of flange in mm (float)
        axial_force: Factored axial force in kN (float)
        moment_load: Factored bending moment in kN-m (float)
        beam_b: Width of flange in mm (float)
        beam_fy: Characteristic yield stress in N/mm^2 (float)

    Returns:

    """
    n = 2 # number of bolts along flange width
    gamma_m0 = 1.10 # Partial safety factor against yield stress and buckling = 1.10 (float)
    ff = flange_force(beam_d, beam_f_t, axial_force, moment_load)
    flangeplatethickness = ff / ((beam_b - n * dia_hole) * (beam_fy / (gamma_m0 * 1000)))

    return round(flangeplatethickness, 2) # mm


########################################################################################################################
# Capacity of flange [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)]
def flange_capacity(beam_f_t,beam_b,dia_hole,beam_fy):
    """

    Args:
        tf: Thickness of flange in mm (float)
        bf: Width of flange in mm (float)
        bolt_hole_diameter: Diameter of bolt hole in mm
        fy: Characteristic yield stress in kN/m2 (float)

    Returns: Calculates flange capacity (kN) (float)(

    """
    gamma_m0 = 1.10 # Partial safety factor against yield stress and buckling = 1.10 (float)
    eff_area =(beam_b - 2 * dia_hole) * beam_f_t # eff area = (bf-n*d0)tf ## where n = number of bolts in a row (here it is 2)
    flangecapacity = (eff_area * beam_fy)/(gamma_m0*1000)
    return round(flangecapacity, 2)  # kN

########################################################################################################################
## Height of web splice plate
# Minimum height of web splice plate [Reference: Steel Designer`s Manual - SCI - 6th edition, page 754]
def web_min_h(beam_d):
    """

    Args:
        beam_d: Overall depth of supported beam (float) in mm

    Returns: Minimum height of web splice plate (float)

    """
    minwebh = round((0.5 * beam_d), 2)
    return minwebh

# Maximum height of web splice plate [Reference: Previous DDCL] assumed gap clearance is 5mm based on reasoning
def web_max_h(beam_d, beam_f_t, beam_r1):
    """

    Args:
        beam_d: Overall depth of supported beam (float) in mm
        beam_f_t: Thickness of flange in mm (float)
        beam_R1: Root radius of the beam section in mm (float)

    Returns: Maximum height of web splice plate in mm (float)

    """
    maxwebheight = round((beam_d - 2 * beam_f_t - 2 * beam_r1 - 2 * 5), 2)
    return maxwebheight

########################################################################################################################
# # Thickness of web splice plate
# ## Minimum thickness of web splice plate [Reference: N. Subramanian, section 5.7.7 page 373]
# def web_min_t(shear_load, beam_fy, web_plate_l):
#     """
#
#     Args:
#         shear_load: Factored shear force in kN (float)
#         beam_fy: Characteristic yield stress of beam N/mm^2 (float)
#         web_plate_l: Height of web splice plate in mm (float)
#
#     Returns: Minimum thickness of web splice plate
#
#     """
#     min_web_t = (5 * shear_load * 1000) / (beam_fy * web_plate_l)
#     return min_web_t

## Maximum thickness of web splice plate [Reference: Handbook on structural steel detailing, INSDAG - Chapter 5, section 5.2.3 page 5.7]
def web_max_t(bolt_diameter):
    """

    Args:
        bolt_dia: Nominal bolt diameter in mm (int)

    Returns: Maximum thickness of web splice plate in mm (float)

    """
    max_web_t = round(0.5 * bolt_diameter, 2)
    return max_web_t

########################################################################################################################
# Calculation of block shear capacity of web splice plate
def web_block_shear(web_plate_l, edge_dist, thk, n_bolts, dia_hole, fy, fu):
    """

    Args:
        web_plate_l: Height of web splice plate in mm (float)
        edge_dist: Edge/end distance in mm (Assumption: edge distance = end distance) (float)
        thk: Thickness of web splice plate in mm (float)
        n_bolts: Number of bolts in web splice plate (int)
        dia_hole: Diameter of bolt hole in mm (int)
        fy: Characteristic yield stress in N/mm^2 (float)
        fu: Ultimate tensile stress of the material in N/mm^2 (float)

    Returns: Block shear capacity of web splice plate in kN

    """
    gamma_m0 = 1.10
    gamma_m1 = 1.25
    Avg = (web_plate_l - edge_dist) * thk
    Avn = (web_plate_l - edge_dist - (n_bolts - 1 + 0.5) * dia_hole) * thk
    Atg = edge_dist * thk
    Atn = (edge_dist - 0.5 * dia_hole) * thk

    Tdb1 = ((Avg * fy)/(math.sqrt(3) * gamma_m0)) + ((0.9 * Atn * fu) / (gamma_m1))
    Tdb2 = ((0.9 * Avn * fu) / (math.sqrt(3))) + ((Atg * fy) / gamma_m0)
    Tdb = min(Tdb1, Tdb2)

    return round((Tdb / 1000), 2)

########################################################################################################################
# Calculation of block shear capacity of flange splice plate
def flange_block_shear(Ltp, edge_dist, thk, n_bolts, dia_hole, flange_width, flange_gauge, fy, fu):
    """

    Args:
        Ltp: ((Length of flange splice plate - gap) / 2) in mm (float)
        edge_dist: Edge/end distance in mm (Assumption: edge distance = end distance) (float)
        thk: Thickness of flange splice plate in mm (float)
        n_bolts: Number of bolts in half part of flange splice plate (int)
        dia_hole: Diameter of bolt hole in mm
        flange_width: Width of flange in mm (float)
        flange_gauge: Gauge distance between bolts in flange in mm (float)
        fy: Characteristic yield stress in N/mm^2 (float)
        fu: Ultimate tensile stress of the material in N/mm^2 (float)

    Returns: Block shear capacity of flange splice plate in mm

    """

    gamma_m0 = 1.10
    gamma_m1 = 1.25
    Avg = (Ltp - edge_dist) * thk
    Avn = (Ltp - edge_dist - (n_bolts - 1 + 0.5) * dia_hole) * thk
    Atg = ((flange_width - flange_gauge) / 2)  * thk
    Atn = (((flange_width - flange_gauge) / 2) - 0.5 * dia_hole) * thk

    Tdb1 = 2 * (((Avg * fy)/(math.sqrt(3) * gamma_m0)) + ((0.9 * Atn * fu) / (gamma_m1)))
    Tdb2 = 2 * (((0.9 * Avn * fu) / (math.sqrt(3))) + ((Atg * fy) / gamma_m0))
    Tdb_flange = min(Tdb1, Tdb2)

    return round((Tdb_flange / 1000), 2)

########################################################################################################################
# Check for shear yielding of web splice plate (Clause 8.4.1, IS 800 : 2007)
def shear_yielding(A_v, beam_fy):
    """

    Args:
        A_v: Total cross sectional area in shear in mm^2 (float)
        beam_fy: Characteristic yield stress in N/mm^2 (float)

    Returns: Strength of web splice plate under shear yielding (kN) ----> (float)

    """
    gamma_m0 = 1.10
    V_p = (0.6 * A_v * beam_fy) / (math.sqrt(3) * gamma_m0 * 1000) # kN
    return round(V_p, 2)

########################################################################################################################
# Check for shear rupture of web splice plate (Clause 8.4.1, IS 800 : 2007)
def shear_rupture(A_vn, beam_fu):
    """

    Args:
        A_vn: Net area of the total cross section in shear mm^2 (float)
        beam_fu: Ultimate tensile stress of the material in N/mm^2 (float)

    Returns: Strength of web splice plate under shear rupture (kN) ----> (float)

    """
    R_n = (0.6 * beam_fu * A_vn) / 1000 # kN
    return round(R_n, 2)

########################################################################################################################
def fetchBeamPara(self):
    beam_section = self.ui.combo_Beam.currentText()
    dictbeamdata = get_beamdata(beam_section)
    return dictbeamdata

# def fetchColumnPara(self):
#     column_sec = self.ui.comboColSec.currentText()
#     loc = self.ui.comboConnLoc.currentText()
#     if loc == "Beam-Beam":
#         dictcoldata = get_beamdata(column_sec)
#     else:
#         dictcoldata = get_columndata(column_sec)
#     return dictcoldata
########################################################################################################################
# Start of main program

def coverplateboltedconnection(uiObj):

    global logger
    global design_status
    design_status = True

    print uiObj
    connectivity = uiObj["Member"]["Connectivity"]
    beam_section = uiObj["Member"]["BeamSection"]
    beam_fu = float(uiObj["Member"]["fu (MPa)"])
    beam_fy = float(uiObj["Member"]["fy (MPa)"])

    shear_load = float(uiObj["Load"]["ShearForce (kN)"])
    moment_load = float(uiObj["Load"]["Moment (kNm)"])
    axial_force = float(uiObj["Load"]["AxialForce"])

    bolt_diameter = int(uiObj["Bolt"]["Diameter (mm)"])
    bolt_grade = float(uiObj["Bolt"]["Grade"])
    bolt_type = (uiObj["Bolt"]["Type"])

    gap = float(uiObj["detailing"]["gap"]) # gap between two beams
    mu_f = float(uiObj["bolt"]["slip_factor"])
    dp_bolt_hole_type = str(uiObj["bolt"]["bolt_hole_type"])
    dia_hole = int(uiObj["bolt"]["bolt_hole_clrnce"]) + bolt_diameter
    type_edge = str(uiObj["detailing"]["typeof_edge"])

    flange_plate_t = float(uiObj["FlangePlate"]["Thickness (mm)"])
    flange_plate_w = str(uiObj["FlangePlate"]["Width (mm)"])
    if flange_plate_w == '':
        flange_plate_w = 0
    else:
        flange_plate_w = int(flange_plate_w)

    flange_plate_l = str(uiObj["FlangePlate"]["Height (mm)"])
    if flange_plate_l == '':
        flange_plate_l = 0
    else:
        flange_plate_l = int(flange_plate_l)

    # flange_plate_fu = float(uiObj["Member"]["fu (Mpa)"])
    # flange_plate_fy = float(uiObj["Member"]["fy (MPa)"])
    flange_plate_fu = beam_fu
    flange_plate_fy = beam_fy

    web_plate_t = float(uiObj["WebPlate"]["Thickness (mm)"])
    web_plate_w = str(uiObj["WebPlate"]["Width (mm)"])
    if web_plate_w == '':
        web_plate_w = 0
    else:
        web_plate_w = int(web_plate_w)

    web_plate_l = str(uiObj["WebPlate"]["Height (mm)"])
    if web_plate_l == '':
        web_plate_l = 0
    else:
        web_plate_l = int(web_plate_l)

    web_plate_fu = int(beam_fu)
    web_plate_fy = int(beam_fy)

    old_beam_section = get_oldbeamcombolist()
    # old_col_section = get_oldcolumncombolist()
    #
    if beam_section in old_beam_section:
        logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
    # if column_sec in old_col_section:
    #     logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")

    ########################################################################################################################
    # Read input values from Beam  database

    if connectivity == "Beam-Beam":
        dictbeamdata = get_beamdata(beam_section)
    else:
        pass

    beam_w_t = float(dictbeamdata["tw"])
    beam_f_t = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])

    beam_r1 = float(dictbeamdata["R1"])
    beam_b = float(dictbeamdata["B"])

    # return uiObj
    ########################################################################################################################

    # Input for plate dimensions (for optional inputs) and validation

    # Check for web plate thickness
    if web_plate_t < beam_w_t:
        web_plate_t = beam_w_t
        design_status = False
        logger.error(": Chosen web splice plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of web splice plate is %2.2f mm" % (beam_w_t))
        logger.info(": Increase thickness of web splice plate")

    # elif web_plate_t < web_min_t(shear_load,beam_fy, web_plate_l):
    #     design_status = False
    #     logger.error(": Chosen web splice plate thickness is not sufficient")
    #     logger.warning(": Minimum required thickness of web splice plate is %2.2f mm" % (web_min_t))
    #     logger.info(": Increase the thickness of web splice plate")

    elif web_plate_t > web_max_t:
        design_status = False
        logger.error(": Thickness of web splice plate is greater than the maximum thickness")
        logger.warning(": Maximum allowed thickness of web splice plate is %2.2f mm" % (web_max_t))
        logger.info(": Decrease the thickness of web splice plate")

    else:
        pass


    # Input for flange splice plate dimensions (for optional inputs) and validation

    # Check for thickness of flange splice plate
    # if flange_plate_t < beam_f_t: # TODO: Yet to be finalized
    #     flange_plate_t = thk_flange_plate
    #     design_status = False
    #     logger.error(": Chosen flange splice plate thickness is not sufficient")
    #     logger.warning(": Minimum required thickness of flange splice plate is %2.2f mm" % (thk_flange_plate))
    #     logger.info(": Increase thickness of flange splice plate")
    thkflangeplate = thk_flange_plate(beam_d, beam_f_t, axial_force, moment_load, beam_b, beam_fy, dia_hole)
    if thkflangeplate < min((beam_f_t / 2), 10):
        thkflangeplate = max((beam_f_t / 2), 10)
    else:
        pass

    if flange_plate_t < (beam_f_t / 2):
        flange_plate_t = thkflangeplate
        design_status = False
        logger.error(": Chosen flange splice plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of flange splice plate is %2.2f mm" % (thkflangeplate))
        logger.info(": Increase thickness of flange splice plate")


    elif flange_plate_t < 10: # 10 mm
        flange_plate_t = thkflangeplate
        logger.error(": Chosen flange splice plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of flange splice plate is %2.2f mm" % (thkflangeplate))
        logger.info(": Increase thickness of flange splice plate")

    else:
        pass

    # Web splice plate height input and check for maximum and minimum values
    webmaxh = web_max_h(beam_d, beam_f_t, beam_r1)
    webminh = web_min_h(beam_d)
    if web_plate_l != 0:
        if web_plate_l > web_max_h:
            if connectivity =="Beam-Beam":
                design_status = False
                logger.error(": Height of web splice plate is greater than the clear depth of beam")
                logger.warning(": Maximum web splice plate height allowed is %2.2f mm" % (webmaxh))
                logger.info(": Reduce the height of web splice plate")
            # else:
            #     pass

        elif webminh > webmaxh:
            if connectivity == "Beam-Beam":
                design_status = False
                logger.error(": Minimum height of web splice plate is more than the clear depth of the beam")
                logger.warning(": Height of web splice plate should be more than %2.2f mm" % (webminh))
                logger.warning(": Allowed height of web splice plate is %2.2f mm" % (webmaxh))
                logger.info(": Increase the height of web splice plate")

        elif web_plate_l < web_min_h:
                design_status = False
                logger.error(": Height of web splice plate is less than the required minimum height as specified in Steel Designer's Manual")
                logger.warning(": Height of web splice plate should be more than %2.2f mm" % (webminh))
                logger.info(": Increase the height of web splice plate")
        else:
            pass

    # Width of flange splice plate (maximum and minimum values)
    if flange_plate_w != 0:
        if flange_plate_w < (beam_b - 2 * 12.7): # AISC Essential detailing requirements for a splice --> B - Half inch on both sides
            # Note: half inch (0.5 inch) = 12.7 mm
            flangeplatewidth = beam_b - (2 * 12.7)
            design_status = False
            logger.error(": Width of flange splice plate is not sufficient")
            logger.warning(": Minimum width of flange splice plate is restricted to %2.2f mm" % (flangeplatewidth))
            logger.info(": Increase the width of flange splice plate")

        elif flange_plate_w > beam_b:
            flangeplatewidth = beam_b
            design_status = False
            logger.error(": Width of flange splice plate is greater than the maximum width as mentioned in AISC")
            logger.warning(": Maximum width of flange splice plate is restricted to %2.2f mm" % (flangeplatewidth))
            logger.info(": Decrease the width of flange splice plate")

        else:
            pass



    ########################################################################################################################
    def boltdesignweb (web_plate_l, flange_plate_w, flange_plate_l):
        # Bolt fu and fy calculation
        bolt_fu = int(bolt_grade) * 100
        bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu
        print bolt_fu
        # Minimum pitch and gauge
        min_pitch = int(2.5 * bolt_diameter)
        min_gauge = int(2.5 * bolt_diameter)

        # Minimum and maximum end and edge distance
        if uiObj["detailing"]["typeof_edge"] == str("a - Sheared or hand flame cut"):
            min_end_dist = int(float(1.7 * dia_hole))
        else:
            min_end_dist = int(float(1.5 * dia_hole))
        min_edge_dist = min_end_dist

        # min_end_dist = 1.7 * dia_hole
        # min_edge_dist = min_end_dist

        # max_end_distance  = 12 * web_t_thinner * (fy/25)^0.5

        # Calculation of kb
        kbChk1 = min_end_dist / float(3 * dia_hole)
        kbChk2 = min_pitch / float(3 * dia_hole) - 0.25
        kbChk3 = bolt_fu / float(beam_fu)
        kbChk4 = 1
        kb = min(kbChk1, kbChk2, kbChk3, kbChk4)
        kb = round(kb, 3)

        # Bolt capacity calculation for web splice
        web_t_thinner = min(beam_w_t, web_plate_t.real)
        web_bolt_planes = 1
        number_of_bolts = 1
        if bolt_type == "Bearing Bolt":
            web_bolt_shear_capacity = round(ConnectionCalculations.bolt_shear(bolt_diameter, web_bolt_planes, bolt_fu), 2)
            web_bolt_bearing_capacity = round(ConnectionCalculations.bolt_bearing(bolt_diameter,number_of_bolts, web_t_thinner,\
                                                                            kb, web_plate_fu), 2)
            web_bolt_capacity = min(web_bolt_shear_capacity,web_bolt_bearing_capacity)

        elif bolt_type == "HSFG":
            muf = mu_f
            bolt_hole_type = dp_bolt_hole_type  # 1 for standard, 0 for oversize hole
            n_e = 2  # number of effective surfaces offering frictional resistance
            web_bolt_shear_capacity = round(ConnectionCalculations.bolt_shear_hsfg(bolt_diameter, bolt_fu, muf, n_e, bolt_hole_type), 2)
            web_bolt_bearing_capacity = 'N/A'
            web_bolt_capacity = web_bolt_shear_capacity

            print web_bolt_bearing_capacity, web_bolt_shear_capacity, web_bolt_capacity

        # Bolt capacity calculation for flange splice

            flange_t_thinner = min(beam_f_t, flange_plate_t.real)
            flange_bolt_planes = 1
            number_of_bolts = 1
            if bolt_type == "Bearing Bolt":
                flange_bolt_shear_capacity = round(ConnectionCalculations.bolt_shear(bolt_diameter, number_of_bolts, bolt_fu), 2)
                flange_bolt_bearing_capacity = round(ConnectionCalculations.bolt_bearing(bolt_diameter, number_of_bolts, flange_t_thinner, \
                                                                                kb, int(flange_plate_fu)), 2)
                flange_bolt_capacity = min(flange_bolt_shear_capacity, flange_bolt_bearing_capacity)

            elif bolt_type == "HSFG":
                muf = mu_f
                bolt_hole_type = dp_bolt_hole_type  # 1 for standard, 0 for oversize hole
                n_e = 1  # number of effective surfaces offering frictional resistance
                flange_bolt_shear_capacity = round(ConnectionCalculations.bolt_shear_hsfg(bolt_diameter, bolt_fu, muf, n_e,
                                                                                 bolt_hole_type), 2)
                flange_bolt_bearing_capacity = 'N/A'
                flange_bolt_capacity = flange_bolt_shear_capacity

                print flange_bolt_bearing_capacity, flange_bolt_shear_capacity, flange_bolt_capacity

    # Maximum pitch and gauge distance for web splice plate
        max_pitch = int(min((32 * web_t_thinner), 300))
        max_gauge = int(min((32 * web_t_thinner), 300))

    # Maximim pitch and gauge distance for flange splice plate
        max_pitch_flange = int(min((32.0 * flange_t_thinner), 300))
        max_gauge_flange = int(min((32 * flange_t_thinner), 300))

    # Calculation of number of bolts required for web splice plate
        if shear_load != 0:
            web_bolts_required = int(math.ceil(shear_load/ web_bolt_capacity))
        else:
            web_bolts_required = 0

    # Calculation of number of bolts required for flange splice plate
        ff = flange_force(beam_d, beam_f_t, axial_force, moment_load)
        if ff != 0:
            flange_bolts_required = int(math.ceil(ff/ flange_bolt_capacity))
        else:
            flange_bolts_required = 0

    # From practical considerations, minimum number of bolts required for web splice plate is 3 [Reference: ML Gambhir page 10.84]
        if web_bolts_required > 0 and web_bolts_required <=2:
            web_bolts_required = 3

    # Number of bolts in even number (for design of flange splice plate)
        if flange_bolts_required % 2 == 0:
            flange_bolts_required = flange_bolts_required
        else:
            flange_bolts_required = flange_bolts_required + 1

    # Number of rows of bolts in flange splice


            '''

            ASCII Diagram to represent flange splice plate
                            row 1                 row 4   Gap between beams
                          +---->                  +-->   ++-----+
                          |                       |      ||
            +--------+----|-----------------------|------||-----------------------------------+---------+
            |        |    +                       |      vv                                   |         |
            |        |                            |      ||                                   |         |
            |        |    +       +       +       +      ||    +       +       +       +      |         |
            |        |                                   ||                                   |         |
            |        |                                   ||                                   |         |
            |        |                                   ||                   ++-+            |         |
            |        |    +       +       +       +      ||    +       +      |+ |     +      |         |
            |        |                                   ||                   +--v            |         |
            |   ^    |            ^                      ||                      |            |         |
            +---|----+------------|--------------- ------++----------------------|------------+---------+
                |                 |                                              | Bolt
                | Beam            |Flange splice plate                           +------+
                +-----+           +--------+

                                   In the above diagram total number of bolts along one side of beam is 8

                                     number of rows = 8/2 = 4
            '''
        number_of_rows_flange = flange_bolts_required / 2

    # Calculation of bolt group capacity for web splice plate
        web_bolt_group_capcity = web_bolts_required * web_bolt_capacity

    # Calculation of bolt group capacity for flange splice plate
        flange_bolt_group_capacity = flange_bolts_required * flange_bolt_capacity


    # Roundup pitch and end distances as a whole number in the multiples of 10
        if min_pitch % 10 != 0 or min_gauge % 10 != 0:
            min_pitch = int(min_pitch / 10) * 10 + 10
            min_gauge = int(min_pitch / 10) * 10 + 10
        else:
            min_pitch = min_pitch + 10
            min_gauge = min_gauge + 10

    # Roundup end and edge distances as a whole number in the multiples of 10
        if min_end_dist % 10 != 0:
            min_end_dist = int(min_end_dist / 10) * 10 + 10
            min_edge_dist = int(min_edge_dist / 10) * 10 + 10
        else:
            min_end_dist = min_end_dist
            min_edge_dist = min_end_dist

    # Pitch calculation for a user given height of web splice plate
        if web_plate_l != 0:
            length_avail = (web_plate_l - 2 * min_end_dist)
            web_pitch = round(length_avail / (web_bolts_required - 1), 3)

    # Case : When there is no user input for height of web splice plate
        elif web_plate_l == 0:
            # Consider web splice plate equal to minimum required height of web splice plate & calc pitch
            web_plate_l_opt = web_min_h(beam_d)
            web_pitch = (web_plate_l_opt - (2 * min_end_dist)) / (web_bolts_required - 1)
            web_plate_l = web_plate_l_opt
            ## In the above case if "pitch < required min pitch" then recalculate height of web splice plate
            if web_pitch <= min_pitch:
                web_plate_l_opt = (web_bolts_required - 1) * min_pitch + 2 * min_end_dist
                web_pitch = min_pitch
                # Recalculate pitch if height of web splice plate is greater than maximum height of web splice plate
                if web_plate_l > web_max_h:
                    web_plate_l_opt = web_max_h(beam_d,beam_f_t, beam_r1)
                    web_pitch = (web_plate_l_opt - 2 * min_end_dist) / (web_bolts_required - 1)
                else:
                    pass
                web_plate_l = web_plate_l_opt

            elif web_pitch >= max_pitch:
                web_plate_l_opt = (web_bolts_required - 1) * max_pitch + 2 * min_end_dist
                web_pitch = max_pitch
                web_plate_l = web_plate_l_opt

            else:
                pass

        else:
            pass

    # Calculation of width of flange splice plate (When user doesn't specify the value)

        '''
        ASCII Diagram to represent length and height of flange splice plate

                 <----------------length = (2 * Ltp) + Gap------------------>
                 +----------------------------++----------------------------+  ^
                 |                            ||                            |  |
                 |   +        +       +       ||    +         +       +     |
                 |                            ||                            | width
                 |   +        +       +       ||    +         +       +     |
                 |                            ||                            |  |
                 +----------------------------++----------------------------+  v
                                              ||
                 <---------+  Ltp  +--------->||<---------+  Ltp  +--------->
                                             Gap
                                              vv
        '''
        if flange_plate_w == 0:
            flange_plate_w = beam_b
        elif flange_plate_w != 0:
            flange_plate_w = flange_plate_w
        else:
            pass

    # Calculation of length of flange splice plate (optional input)
        Ltp = (2 * min_end_dist) + (min_pitch * (number_of_rows_flange - 1))
        if Ltp < max(beam_b, 225): # Note: Ltp > 225 mm and Ltp > width of beam
            Ltp = max(beam_b, 225)
        else:
            pass
        flange_plate_l_opt = 2 * Ltp + gap
    #### 1. Check if Ltp > width of beam (beam_b) and 225 mm ; Note: refer above ASCII diagram
        ## Reference: Steel Designer's Manual - SCI - 6th edition, page 754
        if flange_plate_l != 0:
            Ltp_input = (flange_plate_l - gap) / 2
            if Ltp_input < Ltp:
                design_status = False
                logger.error(": Chosen length of flange splice plate is not sufficient")
                logger.warning(": Minimum required length of flange splice plate is %2.2f" % (flange_plate_l_opt))
                logger.info(": Increase the length of flange splice plate")
            else:
                pass
            flange_plate_l = flange_plate_l
            flange_pitch = (Ltp_input - (2 * min_end_dist)) /(number_of_rows_flange - 1)

        elif flange_plate_l == 0:
            flange_plate_l = flange_plate_l_opt
            flange_pitch = (Ltp - (2 * min_end_dist)) /(number_of_rows_flange - 1)

        else:
            pass


    # Calculation of minimum web plate thickness and maximum end/edge distance
        if web_plate_l != 0:
            web_min_t = (5 * shear_load * 1000) / (beam_fy * web_plate_l)
            max_end_distance = int((12 * web_min_t * math.sqrt(250 / beam_fy)).real)
            max_edge_distance = max_end_distance
            if web_plate_t < web_min_t:
                design_status = False
                logger.error(": Chosen web splice plate thickness is not sufficient")
                logger.warning(": Minimum required thickness of web splice plate is %2.2f mm" % (web_min_t))
                logger.info(": Increase the thickness of web splice plate")

        elif web_plate_l == 0:
            web_min_t = (5 * shear_load * 1000) / (beam_fy * web_plate_l_opt)
            max_end_distance = int((12 * web_min_t * math.sqrt(250 / beam_fy)).real)
            max_edge_distance = max_end_distance

        ################################################################################################################
        # Fetch bolt design output parameters dictionary
        if web_plate_l == 0 and flange_plate_l == 0 and flange_plate_w == 0:
            boltParam = {}
            boltParam["ShearCapacity"] = web_bolt_shear_capacity
            boltParam["BearingCapacity"] = web_bolt_bearing_capacity
            boltParam["CapacityBolt"] = web_bolt_capacity
            boltParam["BoltsRequired"] = web_bolts_required
            boltParam["Pitch"] = web_pitch
            boltParam["End"] = min_end_dist
            boltParam["Edge"] = min_edge_dist
            boltParam["WebPlateHeight"] = web_plate_l
            boltParam["WebGauge"] = min_gauge
            boltParam["WebGaugeMax"] = max_gauge
            boltParam["webPlateDemand"] = shear_load

            boltParam["ShearCapacityF"] = flange_bolt_shear_capacity
            boltParam["BearingCapacityF"] = flange_bolt_bearing_capacity
            boltParam["CapacityBoltF"] = flange_bolt_capacity
            boltParam["BoltsRequiredF"] = flange_bolts_required # Note: This outputs number of bolts required in one side of splice
            boltParam["PitchF"] = flange_pitch
            boltParam["EndF"] = min_end_dist
            boltParam["EdgeF"] = min_edge_dist
            boltParam["FlangePlateHeight"] = flange_plate_l
            boltParam["FlangePlateWidth"] = flange_plate_w
            boltParam["FlangeGauge"] = 90 # TODO: Need to fetch values
            boltParam["FlangePlateDemand"] = flange_force(beam_d, beam_f_t, axial_force, moment_load)

            # bolt parameters required for calculation
            boltParam["bolt_fu"] = bolt_fu
            boltParam["bolt_fy"] = bolt_fy
            boltParam["dia_hole"] = dia_hole
            boltParam["kb"] = kb
            return boltParam
        else:
            boltParam = {}
            boltParam["ShearCapacity"] = web_bolt_shear_capacity
            boltParam["BearingCapacity"] = web_bolt_bearing_capacity
            boltParam["CapacityBolt"] = web_bolt_capacity
            boltParam["BoltsRequired"] = web_bolts_required
            boltParam["Pitch"] = web_pitch
            boltParam["End"] = min_end_dist
            boltParam["Edge"] = min_edge_dist
            boltParam["WebPlateHeight"] = web_plate_l
            boltParam["WebGauge"] = min_gauge
            boltParam["WebGaugeMax"] = max_gauge
            boltParam["webPlateDemand"] = shear_load

            boltParam["ShearCapacityF"] = flange_bolt_shear_capacity
            boltParam["BearingCapacityF"] = flange_bolt_bearing_capacity
            boltParam["CapacityBoltF"] = flange_bolt_capacity
            boltParam["BoltsRequiredF"] = flange_bolts_required  # Note: This outputs number of bolts required in one side of splice
            boltParam["PitchF"] = flange_pitch
            boltParam["EndF"] = min_end_dist
            boltParam["EdgeF"] = min_edge_dist
            boltParam["FlangePlateHeight"] = flange_plate_l
            boltParam["FlangePlateWidth"] = flange_plate_w
            boltParam["FlangeGauge"] = 90  # TODO: Need to fetch values
            boltParam["FlangePlateDemand"] = flange_force(beam_d, beam_f_t, axial_force, moment_load)

            # bolt parameters required for calculation
            boltParam["bolt_fu"] = bolt_fu
            boltParam["bolt_fy"] = bolt_fy
            boltParam["dia_hole"] = dia_hole
            boltParam["kb"] = kb
            return boltParam
        # Call function for bolt design output
    boltparameters = boltdesignweb(web_plate_l, flange_plate_w, flange_plate_l)
    print "boltparmameters", boltparameters

    # check for long joint provisions for web splice plate [Reference: Clause 10.3.3.1, page 75, IS 800 : 2007]
    length_joint_web = (boltparameters["BoltsRequired"] - 1) * boltparameters["Pitch"]
    if length_joint_web > 15 * bolt_diameter:
        beta_lj = (1.075 - length_joint_web) / (200 * bolt_diameter)
        web_bolt_shear_capacity = beta_lj * boltparameters["ShearCapacity"]
        new_bolt_param = boltdesignweb(web_plate_l, flange_plate_w, flange_plate_l)
    else:
        new_bolt_param = boltparameters

    # check for long joint provisions for flange splice plate
    length_joint_flange = ((boltparameters["BoltsRequiredF"] / 2) - 1) * boltparameters["PitchF"]
    if length_joint_flange > 15 * bolt_diameter:
        beta_lj = (1.075 - length_joint_flange) / (200 * bolt_diameter)
        flange_bolt_shear_capacity = beta_lj * boltparameters["ShearCapacityF"]
        new_bolt_param = boltdesignweb(web_plate_l, flange_plate_w, flange_plate_l)
    else:
        new_bolt_param = boltparameters
    #####################################################################################################################
    ## Web plate width input (optional) and validation
    if web_plate_w != 0:
        edge_distance = boltparameters["Edge"]
        min_gauge = boltparameters["WebGauge"]
        gauge_web = web_plate_w - 2 * edge_distance
        max_gauge = boltparameters["WebGaugeMax"]
        # calculation of total width of web splice plate
        ## Case 1: width is sufficient
        web_plate_w_req = gauge_web + 2 * boltparameters["Edge"] + gap
        ## Case 2: when gauge is less than the minimum gauge
        min_web_w_gauge = min_gauge + 2 * boltparameters["Edge"] + gap
        ## Case 3: when gauge distance is less than 2 times the end distance
        ### Note: gauge_web > (End distance of one beam + end distance of other beam)
        web_plate_w_3 = 2 * edge_distance + 2 * edge_distance + gap
        ## Case 4: when gauge distance is less than 90 mm TODO: To be reviewed
        web_plate_w_4 = 90 + 2 * edge_distance + gap
        ## Case 5: when gauge distance is greater than 140 mm TODO: To be reviewed
        web_plate_w_5 = 140 + 2 * edge_distance + gap
        ## Case 6: when gauge distance is greater than maximum gauge [min(32t, 300)]
        web_plate_w_6 = max_gauge + 2 * edge_distance + gap

        ## Case 2
        if gauge_web < min_gauge:
            web_plate_w_req = min_web_w_gauge
            design_status = False
            logger.error(": Chosen width for web splice plate is not sufficient")
            logger.warning(": Minimum width of web splice plate required is %2.2f mm" % (min_web_w_gauge))
            logger.info(": Increase the width of web splice plate")
        ## Case 3
        elif gauge_web < ((2 * edge_distance) + gap):
            web_plate_w_req = web_plate_w_3
            design_status = False
            logger.error(": Chosen width of web splice plate is not sufficient")
            logger.warning(": Minimum width of web splice plate required is %2.2f mm" % (web_plate_w_3))
            logger.info(": Increase the width of web splice plate")
        ## Case 4
        elif gauge_web < (90 + gap):
            web_plate_w_req = web_plate_w_4
            design_status = False
            logger.error(": Chosen width of web splice plate is not sufficient")
            logger.warning(": Minimum width of web splice plate required is %2.2f mm" % (web_plate_w_4))
            logger.info(": Increase the width of web splice plate")
        ## Case 5
        elif gauge_web > (140 + gap):
            web_plate_w_req = web_plate_w_5
            design_status = False
            logger.error(": Width is greater than the maximum allowed width of web splice plate")
            logger.warning(": Maximum width of web splice plate allowed is %2.2f mm" % (web_plate_w_5))
            logger.info(": Decrease the width of web splice plate")
        ## Case 6
        elif gauge_web > (max_gauge + gap):
            web_plate_w_req = web_plate_w_6
            design_status = False
            logger.error(": Width is greater than the maximum allowed width of web splice plate")
            logger.warning(": Maximum width of web splice plate allowed is %2.2f mm" % (web_plate_w_6))
            logger.info(": Decrease the width of web splice plate")

    elif web_plate_w == 0:
        edge_distance = boltparameters["Edge"]
        min_gauge = boltparameters["WebGauge"]
        max_gauge = boltparameters["WebGaugeMax"]
        web_plate_w_req = 4 * edge_distance + gap
        if (2 * edge_distance) < min_gauge:
            web_plate_w_req = min_gauge + (2 * edge_distance) + gap
        elif (2 * edge_distance) < 90:
            web_plate_w_req = 100 + (2 * edge_distance) + gap
        elif (2 * edge_distance) > 140:
            web_plate_w_req = 140 + (2 * edge_distance) + gap
        elif (2 * edge_distance) > max_gauge:
            web_plate_w_req = max_gauge + (2 * edge_distance) + gap
        else:
            pass

    #####################################################################################################################
    # Check for block shear capacity of web splice plate
    min_thk = min(web_plate_t, beam_w_t)
    Tdb = web_block_shear(boltparameters["WebPlateHeight"], boltparameters["Edge"], min_thk, boltparameters["BoltsRequired"],\
                          boltparameters["dia_hole"], beam_fy, beam_fu)

    if Tdb < shear_load:
        design_status = False
        logger.error(": Block shear capacity of web splice plate is less than applied shear force [cl. 6.4.1]")
        logger.warning(": Minimum block shear capacity required is %2.2f kN" % (shear_load))
        logger.info(": Increase the thickness of web splice plate")
    else:
        pass

    #####################################################################################################################
    # Check for shear yielding of web splice plate
    web_plate_l = boltparameters["WebPlateHeight"]
    A_v = web_plate_l * web_plate_t
    V_d = shear_yielding(A_v, beam_fy)
    if V_d < shear_load:
        design_status = False
        logger.error(": Web splice plate fails in shear yielding [cl. 8.4.1] / AISC design manual")
        logger.warning(": Minimum shear yielding capacity required is  %2.2f kN" % (shear_load))
        logger.info(": Increase thickness and height of web splice plate")
    else:
        pass

    #####################################################################################################################
    # Check for shear rupture of web splice plate
    web_plate_l = boltparameters["WebPlateHeight"]
    n_bolts = boltparameters["BoltsRequired"]
    A_vn = (web_plate_l -  n_bolts * 2 * dia_hole) * web_plate_t
    R_n = shear_rupture(A_vn, beam_fu)
    if R_n < shear_load:
        design_status = False
        logger.error(": Web splice plate fails due to shear rupture")
        logger.warning(": Minimum shear yielding capacity required is  %2.2f kN" % (shear_load))
        logger.info(": Increase thickness and height of web splice plate")
    else:
        pass

    #####################################################################################################################
    # Capacity of web splice plate
    web_splice_capacity = min(Tdb, V_d, R_n)


    #####################################################################################################################
    # Check for capacity of flange splice plate
    flangecapacity = flange_capacity(beam_f_t, beam_b, dia_hole, beam_fy)
    ff = flange_force(beam_d, beam_f_t, axial_force, moment_load)
    if flangecapacity < ff:
        design_status = False
        logger.error(": Flange capacity is less than force in flange")
        logger.warning(": Minimum flange capacity required is %2.2f kN" %(ff))
        logger.info(": Increase the size of beam section")
    else:
        pass

    #####################################################################################################################
    # Strength against yielding of gross section (flange splice plate)
    flangeplatewidth = boltparameters["FlangePlateWidth"]
    flangeplatethickness = flange_plate_t
    gamma_m0 = 1.10
    Tdg_flange_plate = ((flangeplatewidth * flangeplatethickness * beam_fy) / gamma_m0)
    if Tdg_flange_plate < ff:
        design_status = False
        logger.error(": Flange splice plate fails due to yielding of gross section")
        logger.warning(": Minimum flange splice plate capacity required is %2.2f kN" % (ff))
        logger.info(": Increase the thickness of flange splice plate")

    #####################################################################################################################
    # Strength against rupture (flange splice plate)
    net_area = (flangeplatewidth - 2 * dia_hole) * flangeplatethickness
    gamma_m1 = 1.25
    Tdn_flange_plate = (0.9 * net_area * flange_plate_fu) / (gamma_m1 * 1000)
    if Tdn_flange_plate < ff:
        design_status = False
        logger.error(": Flange splice plate fails due to rupture")
        logger.warning(": Minimum flange splice plate capacity required is %2.2f kN" % (ff))
        logger.info(": Increase the thickness of flange splice plate")

    #####################################################################################################################
    # Check for block shear capacity of flange splice plate
    min_thk = min(flange_plate_t, beam_f_t)
    n_bolts = boltparameters["BoltsRequiredF"] / 2
    Ltp = (boltparameters["FlangePlateHeight"] - gap) / 2
    Tdb_flange = flange_block_shear(Ltp, boltparameters["EdgeF"], min_thk, n_bolts, dia_hole,
                                    boltparameters["FlangePlateWidth"], boltparameters["FlangeGauge"],
                                    flange_plate_fy, flange_plate_fu)

    if Tdb_flange < ff:
        design_status = False
        logger.error(": Block shear capacity of flange splice plate is less than force in flange [cl. 6.4.1]")
        logger.warning(": Minimum block shear capacity required is %2.2f kN" % (ff))
        logger.info(": Increase the thickness of flange splice plate")
    else:
        pass

    # Capacity of flange splice plate
    flange_splice_capacity = min(Tdg_flange_plate, Tdn_flange_plate, Tdb_flange)

    #####################################################################################################################
    # End of calculation for design of web splice plate
    # Output
    ## When height and width of web splice plate are zero
    if web_plate_l == 0 and web_plate_w == 0 and flange_plate_l == 0 and flange_plate_w == 0:
        outputObj = {}
        outputObj["WebBolt"] = {}
        outputObj["WebBolt"]["ShearCapacity"] = new_bolt_param["ShearCapacity"]
        outputObj["WebBolt"]["BearingCapacity"] = new_bolt_param["BearingCapacity"]
        outputObj["WebBolt"]["CapacityBolt"] = new_bolt_param["CapacityBolt"]
        outputObj["WebBolt"]["BoltsRequired"] = new_bolt_param["BoltsRequired"]
        outputObj["WebBolt"]["Pitch"] = new_bolt_param["Pitch"]
        outputObj["WebBolt"]["End"] = new_bolt_param["End"]
        outputObj["WebBolt"]["Edge"] = new_bolt_param["Edge"]
        outputObj["WebBolt"]["WebPlateHeight"] = new_bolt_param["WebPlateHeight"]
        outputObj["WebBolt"]["WebGauge"] = new_bolt_param["WebGauge"]
        outputObj["WebBolt"]["WebGaugeMax"] = new_bolt_param["WebGaugeMax"]
        outputObj["WebBolt"]["webPlateDemand"] = new_bolt_param["webPlateDemand"]
        outputObj["WebBolt"]["WebPlateWidth"] = web_plate_w_req
        outputObj["WebBolt"]["WebPlateCapacity"] = web_splice_capacity

        outputObj["FlangeBolt"] = {}
        outputObj["FlangeBolt"]["ShearCapacityF"] = new_bolt_param["ShearCapacityF"]
        outputObj["FlangeBolt"]["BearingCapacityF"] = new_bolt_param["BearingCapacityF"]
        outputObj["FlangeBolt"]["CapacityBoltF"] = new_bolt_param["CapacityBoltF"]
        outputObj["FlangeBolt"]["BoltsRequiredF"] = new_bolt_param["BoltsRequiredF"]  # Note: This outputs number of bolts required in one side of splice
        outputObj["FlangeBolt"]["PitchF"] = new_bolt_param["PitchF"]
        outputObj["FlangeBolt"]["EndF"] = new_bolt_param["EndF"]
        outputObj["FlangeBolt"]["EdgeF"] = new_bolt_param["EdgeF"]
        outputObj["FlangeBolt"]["FlangePlateHeight"] = new_bolt_param["FlangePlateHeight"]
        outputObj["FlangeBolt"]["FlangePlateWidth"] = new_bolt_param["FlangePlateWidth"]
        outputObj["FlangeBolt"]["FlangeGauge"] = 90  # TODO: Need to fetch values
        outputObj["FlangeBolt"]["FlangePlateDemand"] = new_bolt_param["FlangePlateDemand"]
        outputObj["FlangeBolt"]["FlangeCapacity"] = flange_splice_capacity

        ####### For reference and validation
        outputObj["WebBolt"]["WebBlockShear"] = Tdb
        outputObj["WebBolt"]["ShearYielding"] = V_d
        outputObj["WebBolt"]["ShearRupture"] = R_n
        outputObj["FlangeBolt"]["FlangeCapacity"] = flangecapacity
        outputObj["FlangeBolt"]["Yielding"] = Tdg_flange_plate
        outputObj["FlangeBolt"]["Rupture"] = Tdn_flange_plate
        outputObj["FlangeBolt"]["FlangeBlockShear"] = Tdb_flange

    else:
        outputObj = {}
        outputObj["WebBolt"] = {}
        outputObj["WebBolt"]["ShearCapacity"] = new_bolt_param["ShearCapacity"]
        outputObj["WebBolt"]["BearingCapacity"] = new_bolt_param["BearingCapacity"]
        outputObj["WebBolt"]["CapacityBolt"] = new_bolt_param["CapacityBolt"]
        outputObj["WebBolt"]["BoltsRequired"] = new_bolt_param["BoltsRequired"]
        outputObj["WebBolt"]["Pitch"] = new_bolt_param["Pitch"]
        outputObj["WebBolt"]["End"] = new_bolt_param["End"]
        outputObj["WebBolt"]["Edge"] = new_bolt_param["Edge"]
        outputObj["WebBolt"]["WebPlateHeight"] = new_bolt_param["WebPlateHeight"]
        outputObj["WebBolt"]["WebGauge"] = new_bolt_param["WebGauge"]
        outputObj["WebBolt"]["WebGaugeMax"] = new_bolt_param["WebGaugeMax"]
        outputObj["WebBolt"]["webPlateDemand"] = new_bolt_param["webPlateDemand"]
        outputObj["WebBolt"]["WebPlateWidth"] = web_plate_w_req
        outputObj["WebBolt"]["WebPlateCapacity"] = web_splice_capacity

        outputObj["FlangeBolt"] = {}
        outputObj["FlangeBolt"]["ShearCapacityF"] = new_bolt_param["ShearCapacityF"]
        outputObj["FlangeBolt"]["BearingCapacityF"] = new_bolt_param["BearingCapacityF"]
        outputObj["FlangeBolt"]["CapacityBoltF"] = new_bolt_param["CapacityBoltF"]
        outputObj["FlangeBolt"]["BoltsRequiredF"] = new_bolt_param["BoltsRequiredF"]  # Note: This outputs number of bolts required in one side of splice
        outputObj["FlangeBolt"]["PitchF"] = new_bolt_param["PitchF"]
        outputObj["FlangeBolt"]["EndF"] = new_bolt_param["EndF"]
        outputObj["FlangeBolt"]["EdgeF"] = new_bolt_param["EdgeF"]
        outputObj["FlangeBolt"]["FlangePlateHeight"] = new_bolt_param["FlangePlateHeight"]
        outputObj["FlangeBolt"]["FlangePlateWidth"] = new_bolt_param["FlangePlateWidth"]
        outputObj["FlangeBolt"]["FlangeGauge"] = 90  # TODO: Need to fetch values
        outputObj["FlangeBolt"]["FlangePlateDemand"] = new_bolt_param["FlangePlateDemand"]
        outputObj["FlangeBolt"]["FlangeCapacity"] = flange_splice_capacity

        ####### For reference and validation
        outputObj["WebBolt"]["WebBlockShear"] = Tdb
        outputObj["WebBolt"]["ShearYielding"] = V_d
        outputObj["WebBolt"]["ShearRupture"] = R_n
        outputObj["FlangeBolt"]["FlangeCapacity"] = flangecapacity
        outputObj["FlangeBolt"]["Yielding"] = Tdg_flange_plate
        outputObj["FlangeBolt"]["Rupture"] = Tdn_flange_plate
        outputObj["FlangeBolt"]["FlangeBlockShear"] = Tdb_flange

    if design_status == True:

        logger.info(": Overall bolted cover plate splice connection design is safe \n")
        logger.debug(" :=========End Of design===========")
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")

    return outputObj


########################################### End of Design ################################################





















