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
       D: Overall depth of the beam section in mm (float)
       tf: Thickness of flange in mm (float)
       F: Factored axial force in kN (float)
       M: Factored bending moment in kN-m (float)

    Returns:
        Force in flange in kN (float)

    """
    tm = total_moment(beam_d, beam_f_t, axial_force, moment_load)
    return (tm*1000)/(beam_d - beam_f_t)        # kN

########################################################################################################################

# TODO - Detailing checks for flange splice plate

# TODO - Detailing checks for web splice plate

########################################################################################################################
# Thickness of flange splice plate [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)]
def thk_flange_plate(beam_d, beam_f_t, axial_force, moment_load,beam_b,beam_fy,gamma_m0):
    """

    Args:
        D: Overall depth of the beam section in mm (float)
        tf: Thickness of flange in mm (float)
        bf: Width of flange in mm (float)
        fy: Characteristic yield stress in kN/m2 (float)
        gamma_m0: Partial safety factor against yield stress and buckling = 1.10 (float)

    Returns:

    """
    ff = flange_force(beam_d, beam_f_t, axial_force, moment_load)
    flangeplatethickness = ff / (beam_b *(beam_fy/(gamma_m0*1000)))
    # TODO - need to ceil the thickness of plate based on available  plate
    # TODO continued...  thickness in market (better to create dictionary)
    # TODO - the value should be greater than minimum thickness of flange splice plate
    return flangeplatethickness # mm

########################################################################################################################
# Provision of long joints [Reference: Clause 10.3.3.1 page 75, IS 800 : 2007]
def long_joint(bolt_diameter):
    """

    Args:
        bolt_diameter: Nominal diameter of the bolt in mm (float)

    Returns: Reduction factor for calculating bolt capacity (beta_lj) ---> (float)

    """
    # TODO - To calculate this we need lj as input which inturn depends on length of splice plate
    # TODO - This function also requires validation as beta_lj should be between 0.75 and 1.0
    # TODO - Also check if lj > 15d
    lj = 0
    #TODO swathi change the name of lj
    beta_lj = 1.075 - (lj/(200*bolt_diameter))
    return beta_lj

########################################################################################################################
# Capacity of flange [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)]
def flange_capacity(beam_f_t,beam_b,bolt_hole_diameter,beam_fy,gamma_m0):
    """

    Args:
        tf: Thickness of flange in mm (float)
        bf: Width of flange in mm (float)
        bolt_hole_diameter: Diameter of bolt hole in mm
        fy: Characteristic yield stress in kN/m2 (float)
        gamma_m0: Partial safety factor against yield stress and buckling = 1.10 (float)

    Returns: Calculates flange capacity (kN) (float)(

    """

    eff_area =(beam_b - 2 * bolt_hole_diameter) * beam_f_t # eff area = (bf-n*d0)tf ## where n = number of bolts in a row (here it is 2)
    flangecapacity = (eff_area * beam_fy)/(gamma_m0*1000)
    # TODO - write a conditional statement telling that this should be greater than flange force
    return flangecapacity  # kN

########################################################################################################################
# Strength against yielding of gross section [Reference: Clause 6.2 page 32, IS 800 : 2007]
## This is check for flange splice plate
## TODO - This requires dimension of flange splice plate

########################################################################################################################
# Strength against rupture [Reference: Clause 6.3.1 page 32, IS 800 : 2007]
## TODO - An depends on flange plate thickness

########################################################################################################################
# Block shear failure

########################################################################################################################
# Factored resultant shear force (for web splice plate)

########################################################################################################################
# Shear yielding

########################################################################################################################
# Shear rupture

########################################################################################################################
## Height of web splice plate
# Minimum height of web splice plate [Reference: Steel Designer`s Manual - SCI - 6th edition, page 754]
def web_min_h(beam_d):
    """

    Args:
        beam_d: Overall depth of supported beam (float) in mm

    Returns: Minimum height of web splice plate (float)

    """
    minwebh = round((0.5 * beam_d), 3)
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
    maxwebheight = round((beam_d - 2 * beam_f_t - 2 * beam_r1 - 2 * 5), 3)
    return maxwebheight

########################################################################################################################
# Thickness of web splice plate
## Minimum thickness of web splice plate [Reference: N. Subramanian, section 5.7.7 page 373]
def web_min_t(shear_load, beam_fy, web_plate_l):
    """

    Args:
        shear_load: Factored shear force in kN (float)
        beam_fy: Characteristic yield stress of beam N/mm^2 (float)
        web_plate_l: Height of web splice plate in mm (float)

    Returns: Minimum thickness of web splice plate

    """
    min_web_t = (5 * shear_load * 1000) / (beam_fy * web_plate_l)
    return min_web_t

## Maximum thickness of web splice plate [Reference: Handbook on structural steel detailing, INSDAG - Chapter 5, section 5.2.3 page 5.7]
def web_max_t(bolt_diameter):
    """

    Args:
        bolt_dia: Nominal bolt diameter in mm (int)

    Returns: Maximum thickness of web splice plate in mm (float)

    """
    max_web_t = 0.5 * bolt_diameter
    return max_web_t

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

def coverplateboltedconnection(uiObj, desigpre):

    global logger
    global design_status
    design_status = True

    print uiObj
    connectivity = uiObj["Member"]["Connectivity"]
    beam_section = uiObj["Member"]["BeamSection"]
    beam_fu = float(uiObj["Member"]["fu (MPa)"])
    beam_fy = float(uiObj["Member"]["fy (MPa)"])

    shear_load = float(uiObj["Load"]["ShearForce (kN)"] )
    moment_load = float(uiObj["Load"]["Moment (kNm)"] )
    axial_force = float(uiObj["Load"]["AxialForce"])

    bolt_diameter = int(uiObj["Bolt"]["Diameter (mm)"] )
    bolt_grade = float(uiObj["Bolt"]["Grade"] )
    bolt_type = (uiObj["Bolt"]["Type"] )

    gap = float(desigpre["test"]["gap"]) # gap between two beams
    mu_f = float(desigpre["test"]["slip_factor"])
    # gamma_mw = float(desigpre["test"]["safety_factor"])
    dp_bolt_hole_type = str(desigpre["test"]["bolt_hole_type"])
    dia_hole = int(desigpre["test"]["bolt_hole_clrnce"]) + bolt_diameter
    type_edge = str(desigpre["test"]["typeof_edge"])

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

    # TODO : Add old beam section in red colour (code in main file - Reshma)
    # old_beam_section = get_oldbeamcombolist()
    # old_col_section = get_oldcolumncombolist()
    #
    # if beam_section in old_beam_section:
    #     logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")
    # if column_sec in old_col_section:
    #     logger.warning(" : You are using a section (in red color) that is not available in latest version of IS 808")

    ########################################################################################################################
    # Read input values from Beam  database

    # TODO: This requires a function to be written in main file
    if connectivity == "Beam-Beam":
        dictbeamdata = get_beamdata(beam_section)
    else:
        dictbeamdata = get_beamdata(beam_section)

    beam_w_t = float(dictbeamdata["tw"])
    beam_f_t = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_r1 = float(dictbeamdata["R1"])
    beam_B = float(dictbeamdata["B"])

    # return uiObj
    ########################################################################################################################

    # Input for plate dimensions (for optional inputs) and validation

    # Check for web plate thickness
    if web_plate_t < beam_w_t:
        web_plate_t = beam_w_t
        design_status = False
        logger.error(": Chosen web plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of web is %2.2f mm") % beam_w_t

    ########################################################################################################################
    # Bolt design function

    # Bolt fu and fy calculation
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu

    # Minimum pitch and gauge
    min_pitch = int(2.5 * bolt_diameter)
    min_gauge = int(2.5 * bolt_diameter)

    # Minimum and maximum end and edge distance
    if "typeof_edge" == "a - Sheared or hand flame cut":
        min_end_dist = int(float(1.7 * dia_hole))
    else:
        min_end_dist = int(float(1.5 * dia_hole))
    min_edge_dist = min_end_dist

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
        web_bolt_shear_capacity = ConnectionCalculations.bolt_shear(bolt_diameter, web_bolt_planes, bolt_fu)
        web_bolt_bearing_capacity = ConnectionCalculations.bolt_bearing(bolt_diameter,number_of_bolts, web_t_thinner,\
                                                                        kb, web_plate_fu)
        web_bolt_capacity = min(web_bolt_shear_capacity,web_bolt_bearing_capacity)

    elif bolt_type == "HSFG":
        muf = mu_f
        bolt_hole_type = dp_bolt_hole_type  # 1 for standard, 0 for oversize hole
        n_e = 2  # number of effective surfaces offering frictional resistance
        web_bolt_shear_capacity = ConnectionCalculations.bolt_shear_hsfg(bolt_diameter, bolt_fu, muf, n_e, bolt_hole_type)
        web_bolt_bearing_capacity = 'N/A'
        web_bolt_capacity = web_bolt_shear_capacity

        print web_bolt_bearing_capacity, web_bolt_shear_capacity, web_bolt_capacity
    # Bolt capacity calculation for flange splice
        # Bolt capacity calculation for web splice plate

        flange_t_thinner = min(beam_f_t, flange_plate_t.real)
        flange_bolt_planes = 1
        number_of_bolts = 1
        if bolt_type == "Bearing Bolt":
            flange_bolt_shear_capacity = ConnectionCalculations.bolt_shear(bolt_diameter, flange_bolt_planes, bolt_fu)
            flange_bolt_bearing_capacity = ConnectionCalculations.bolt_bearing(bolt_diameter, number_of_bolts, flange_t_thinner, \
                                                                            kb, int(flange_plate_fu))
            flange_bolt_capacity = min(flange_bolt_shear_capacity, flange_bolt_bearing_capacity)

        elif bolt_type == "HSFG":
            muf = mu_f
            bolt_hole_type = dp_bolt_hole_type  # 1 for standard, 0 for oversize hole
            n_e = 2  # number of effective surfaces offering frictional resistance
            flange_bolt_shear_capacity = ConnectionCalculations.bolt_shear_hsfg(bolt_diameter, bolt_fu, muf, n_e,
                                                                             bolt_hole_type)
            flange_bolt_bearing_capacity = 'N/A'
            flange_bolt_capacity = flange_bolt_shear_capacity

            print flange_bolt_bearing_capacity, flange_bolt_shear_capacity, flange_bolt_capacity

        print total_moment(beam_d, beam_f_t, axial_force, moment_load)
        print flange_force(beam_d, beam_f_t, axial_force, moment_load)
