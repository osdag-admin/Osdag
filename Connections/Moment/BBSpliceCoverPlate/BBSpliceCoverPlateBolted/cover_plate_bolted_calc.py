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
    logger = logging.getLogger("osdag.BBSpliceCoverPlateBolted")
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
def total_moment(D,tf,F,M):
    """

    Args:
        D: Overall depth of the beam section in mm (float)
        tf: Thickness of flange in mm (float)
        F: Factored axial force in kN (float)
        M: Factored bending moment in kN-m (float)

    Returns:
        Total moment acting on the section in kN-m (float)

    """
    cg = (D/2)-(tf/2)  # Assumption: Axial force acts exactly at the center of the section
    moment_axialF = (F * cg)/1000  # Moment due to factored axial force = F * centroidal distance  (kN-m)
    total_moment = M + moment_axialF
    return total_moment  # kN-m

########################################################################################################################
# Force in flange (kN)  [Reference: M.L. Gambhir (page 10.83), N. Subramanian (page 427)]
def flange_force(D,tf,F,M):
    """

    Args:
       D: Overall depth of the beam section in mm (float)
       tf: Thickness of flange in mm (float)
       F: Factored axial force in kN (float)
       M: Factored bending moment in kN-m (float)

    Returns:
        Force in flange in kN (float)

    """
    Mt = total_moment(D,tf,F,M)
    return (Mt*1000)/(D-tf)        # kN

########################################################################################################################

# TODO - Detailing checks for flange splice plate

# TODO - Detailing checks for web splice plate

########################################################################################################################
# Thickness of flange splice plate [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)]
def thk_flange_plate(D,tf,F,M,bf,fy,gamma_m0):
    """

    Args:
        D: Overall depth of the beam section in mm (float)
        tf: Thickness of flange in mm (float)
        bf: Width of flange in mm (float)
        fy: Characteristic yield stress in kN/m2 (float)
        gamma_m0: Partial safety factor against yield stress and buckling = 1.10 (float)

    Returns:

    """
    FF = flange_force(D,tf,F,M)
    TFP = FF / (bf *(fy/(gamma_m0*1000)))
    # TODO - need to ceil the thickness of plate based on available  plate
    # TODO continued...  thickness in market (better to create dictionary)
    # TODO - the value should be greater than minimum thickness of flange splice plate
    return TFP # mm

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
def flange_capacity(tf,bf,bolt_hole_diameter,fy,gamma_m0):
    """

    Args:
        tf: Thickness of flange in mm (float)
        bf: Width of flange in mm (float)
        bolt_hole_diameter: Diameter of bolt hole in mm
        fy: Characteristic yield stress in kN/m2 (float)
        gamma_m0: Partial safety factor against yield stress and buckling = 1.10 (float)

    Returns: Calculates flange capacity (kN) (float)(

    """

    eff_area =(bf - 2 * bolt_hole_diameter) * tf # eff area = (bf-n*d0)tf ## where n = number of bolts in a row (here it is 2)
    FC = (eff_area * fy)/(gamma_m0*1000)
    # TODO - write a conditional statement telling that this should be greater than flange force
    return FC  # kN

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
# Minimum and maximum web splice plate dimensions

########################################################################################################################
# Factored resultant shear force (for web splice plate)

########################################################################################################################
# Shear yielding

########################################################################################################################
# Shear rupture

def coverplateboltedconnection(uiObj):
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

    flange_plate_t = float(uiObj["FlangePlate"]["Thickness (mm)"] )
    flange_plate_h = str(uiObj["FlangePlate"]["Height (mm)"] )
    flange_plate_w = str(uiObj["FlangePlate"]["Width (mm)"] )

    web_plate_t = float(uiObj["WebPlate"]["Thickness (mm)"] )
    web_plate_h = str(uiObj["WebPlate"]["Height (mm)"] )
    web_plate_w = str(uiObj["WebPlate"]["Width (mm)"] )
