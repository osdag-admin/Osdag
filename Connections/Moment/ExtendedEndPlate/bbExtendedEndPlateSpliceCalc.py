'''
Created on 16th October, 2017.

@author: Danish Ansari


Module: Beam to beam extended end plate splice connection (Moment connection)

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel structures by Dr. N Subramanian (chapter 5 and 6)
            3) Fundamentals of Structural steel design by M.L Gambhir
            4) AISC Design guide 16 and 4


ASCII diagram
                                      end plate (extended)

                                        +-+-+
                                        | | |
                                     +---------+ bolt
                                        | | |
+---------------------------------------+ | +-----------------------------------+
|                                       | | |                                   |
|                                       | | |                                   |
|                                    +---------+                                |
|                                       | | |                                   |
|                                       | | |                                   |
|                                       | | |                                   |
|              Beam section             | | |              Beam section         |
|                                       | | |                                   |
|                                       | | |                                   |
|                                    +---------+                                |
|                                       | | |                                   |
|                                       | | |                                   |
+---------------------------------------+ | +-----------------------------------+
                                        | | |
                                     +---------+
                                        | | |
                                        +-+-+


'''

from model import *
from Connections.connection_calculations import ConnectionCalculations
import math
import logging
flag = 1
logger = None


def module_setup():
    global logger
    logger = logging.getLogger("osdag.bbExtendedEndPlateSpliceCalc")
module_setup()

#######################################################################
# Defining functions
#######################################################################


# Function for net area of bolts
# Reference: Design of steel structures by N. Subramanian, page 348 or 358


def netArea_calc(dia):
    """

    Args:
        dia: (int)- diameter of bolt (HSFG/Bearing bolt)

    Returns: Net area of bolts at threaded portion (Ref. Table 5.11 Subramanian's book, page: 358 )

    """

    netArea = {12: 84.5, 16: 157, 20: 245, 22: 303, 24: 353, 27: 459, 30: 561, 36: 817}
    return netArea[dia]

#######################################################################

#Function for long joints (beta_lj)
#Source: Cl 10.3.3.1
#Reference: Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def long_joint(dia, l_j):
    """

    Args:
        dia: (int)- diameter of bolt
        l_j: length of joint i.e. distance between first and last bolt in the joint measured in the direction of load transfer

    Returns: reduction factor beta_lj

    """

    beta_lj = 1.075 - (0.005 * (l_j/dia))
    return beta_lj



#######################################################################

#Function for Shear Capacity of bearing bolt (also known as black bolt)
#Reference: Cl 10.3.3 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007
#Assumption: The shear planes are assumed to be passing through the threads of the bolt

def bolt_shear(dia, n, bolt_fu):
    """

    Args:
        dia: (int)- diameter of bolt
        n: (str)- number of shear plane(s) through which bolt is passing
        bolt_fu: (float)- Ultimate tensile strength of a bolt

    Returns: Shear capacity of bearing type bolt in kN

    """

    A = netArea_calc(dia)
    V_dsb = bolt_fu * n * A / (math.sqrt(3) * 1.25 * 1000)
    V_dsb = round(V_dsb.real, 3)
    return V_dsb



#######################################################################

#Function for Bearing Capacity of bearing bolt (also known as black bolt)
#Reference: Cl 10.3.4 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def bolt_bearing(dia, t, k_b, bolt_fu):
    """

    Args:
        dia: (int)- diameter of bolt
        t:(float)- summation of thickneses of the connected plates experencing bearing stress in same direction, or if the bolts are countersunk, the thickness of plate minus 1/2 of the depth of countersunk
        k_b: (float)- multiplying factor (Ref: Cl 10.3.4 IS 800:2007)
        bolt_fu: (float)- Ultimate tensile strength of a bolt

    Returns: Bearing capacity of bearing type bolt in kN

    """

    V_dpb = 2.5 * k_b * dia * t * bolt_fu / (1.25 * 1000)
    V_dpb  = round(V_dpb.real, 3)
    return V_dpb


#######################################################################

#Function for minimum height of end plate
#Reference: Based on reasoning

def min_plate_height(beam_D, l_v, n_r, min_pitch, e_1):
    """

    Args:
        beam_D: (float) - Depth of beam
        l_v: (float)- Distance between the toe of weld or flange to the centre of the nearer bolt
        n_r: (int)- number of row(s) above or below the beam flange
        min_pitch: (float)- minimum pitch distance i.e. 2.5*bolt_diameter
        e_1: (float)- minimum end distance i.e. 1.7*bolt_hole_diameter

    Returns: Minimum required height of extended end plate as per detailing requirements in mm

    """
    min_end_plate_height = beam_D + (2 * l_v) + (2 * (n_r-1) * min_pitch) + (2 * e_1)
    return min_end_plate_height


#######################################################################

#Function for minimum width of end plate
#Reference: Based on reasoning

def min_plate_width(g_1, n, min_gauge, e_2):
    """

    Args:
        g_1: (float)- Cross-centre gauge distance
        min_gauge: (float)- minimum gauge distance i.e. 2.5*bolt_diameter
        e_2: (float)- minimum edge distance i.e. 1.7*bolt_hole_diameter

    Returns: Minimum required width of extended end plate as per detailing requirements in mm

    """
    min_end_plate_width = g_1 + (n - 2)* min_gauge + 2 * e_2
    return min_end_plate_width


#######################################################################

#Function for calculation of Prying Force in bolts
#Reference: Cl 10.4.7 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def prying_force(T_e, l_v, l_e, beta, eta, f_0, b_e, t_p):
    """

    Args:
        T_e: (float): Tension acting on beam flange
        l_v: (float)- Distance between the toe of weld or flange to the centre of the nearer bolt
        l_e: (float)- Distance between prying force and bolt centreline
        beta: (int)- multiplying factor
        eta: (float)- multiplying factor
        f_0: (float)- proof stress in consistent units
        b_e: (float)- effective width of flange per pair of bolts
        t_p: (float)- thickness of end plate

    Returns: Prying force in bolt

    """
    prying_force_bolt = (l_v / 2 * l_e) * (T_e - ((beta * eta * f_0 * b_e * t_p ^ 4) / 27 * l_e * l_v ^ 2))
    return prying_force_bolt


#######################################################################

#Function for calculating Tension capacity of HSFG bolt
#Reference: Cl 10.4.5 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def bolt_tension_hsfg(bolt_fu, netArea):
    """

    Args:
        bolt_fu: (float)- Ultimate tensile strength of a bolt
        netArea: (float)- Net tensile stress area as specified in IS 1367 (area at threads)

    Returns: Tension capacity of HSFG bolt in kN

    """
    T_df = 0.9 * bolt_fu * netArea / 1.25 * 1000
    return T_df


#######################################################################

#Function for calculating Tension capacity of bearing bolt (also known as black bolt)
#Reference: Cl 10.3.5 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def bolt_tension_bearing(bolt_fu, netArea):
    """

    Args:
        bolt_fu: (float)- Ultimate tensile strength of a bolt
        netArea: (float)- Net tensile stress area as specified in IS 1367 (area at threads)

    Returns: Tension capacity of Bearing bolt in kN

    """
    T_db = 0.9 * bolt_fu * netArea / 1.25 * 1000
    return T_db


#######################################################################

#Function for calculating Shear yielding capacity of End Plate
#Reference: Cl 8.4.1 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def shear_yielding(A_v, plate_fy):
    """

    Args:
        A_v: (float)- Gross shear area of end plate
        plate_fy: (float)- Yield stress of plate material

    Returns: Shear yielding capacity of End Plate in kN

    """
    V_d = 0.6 * A_v * plate_fy / (math.sqrt(3) * 1.10 * 1000)
    return V_d


#######################################################################

#Function for calculating Shear rupture capacity of End Plate
#Reference: Cl 8.4.1 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def shear_rupture(A_vn, plate_fu):
    """

    Args:
        A_vn: (float)- Net shear area of end plate
        plate_fu: (float)- Ultimate stress of plate material

    Returns: Shear rupture capacity of End Plate in kN

    """
    R_n = 0.6 * A_vn * plate_fu / 1000
    return R_n


#######################################################################

#Function for fetching beam parameters from the database

def fetchBeamPara(self):
    beam_sec = self.ui.combo_Beam.currentText()
    dictbeamdata = get_beamdata(beam_sec)
    return dictbeamdata


#######################################################################
#######################################################################
# Start of Main Program

def bbExtendedEndPlateSplice(uiObj):
    global logger
    global design_status
    design_status = True

    connectivity = uiObj ['Member']['Connectivity']
    beam_sec = uiObj['Member']['BeamSection']
    beam_fu = float(uiObj['Member']['fu (MPa)'])
    beam_fy = float(uiObj['Member']['fy (MPa)'])

    factored_moment = float(uiObj['Load']['Moment (kNm)'])
    factored_shear_load = float(uiObj['Load']['ShearForce (kN)'])
    factored_axial_load = float(uiObj['Load']['AxialForce (kN)'])

    bolt_dia = int(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = float(uiObj['Bolt']['Grade'])

    mu_f = float(uiObj["bolt"]["slip_factor"])
    gamma_mw = float(uiObj["weld"]["safety_factor"])
    dp_bolt_hole_type = str(uiObj['bolt']['bolt_hole_type'])
    dia_hole = int(uiObj['bolt']['bolt_hole_clrnce']) + bolt_dia
    weld_type = uiObj['weld']['typeof_weld']
    dp_bolt_type = uiObj['bolt']['bolt_type']


    end_plate_thickness = float(uiObj['Plate']['Thickness (mm)'])

    end_plate_width = str(uiObj['Plate']['Width (mm)'])
    if end_plate_width == '':
        end_plate_width = 0
    else:
        end_plate_width = int(end_plate_width)

    end_plate_height = str(uiObj['Plate']['Height (mm)'])
    if end_plate_height == '':
        end_plate_height = 0
    else:
        end_plate_height = int(end_plate_height)

    # TODO implement after erxcomm review for different grades of plate
    end_plate_fu = float(uiObj['Member']['fu (MPa)'])
    end_plate_fy = float(uiObj['Member']['fy (MPa)'])

    weld_thickness_flange = float(uiObj['Weld']['Size (mm)'])
    weld_thickness_web = float(uiObj['Weld']['Size (mm)'])

    old_beam_section = get_oldbeamcombolist()

    if beam_sec in old_beam_section:
        logger.warning(": You are using a section (in red colour) that is not available in the latest version of IS 808")

    #######################################################################
    # Read input values from Beam database
    # Here,
    #    beam_tw - Thickness of beam web
    #    beam_tf - Thickness of beam Flange
    #    beam_d  - Depth of beam
    #    beam_B  - Width of beam Flange
    #    beam_R1 - Radius of beam at root

    dictbeamdata = get_beamdata(beam_sec)

    beam_tw = float(dictbeamdata["tw"])
    beam_tf = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_B = float(dictbeamdata["B"])
    beam_R1 = float(dictbeamdata["R1"])

    #######################################################################
    # Calculation of Bolt strength in MPa
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu

    #######################################################################
    # Calculation of Spacing

    # t_thinner is the thickness of the thinner plate
    t_thinner = end_plate_thickness

    # min_pitch & max_pitch = Minimum and Maximum pitch distance (mm) [Cl. 10.2.2, IS 800:2007]
    min_pitch = int(2.5 * bolt_dia)
    max_pitch = max(int(32 * t_thinner, 300))

    # min_gauge & max_gauge = Minimum and Maximum gauge distance (mm) [Cl. 10.2.3.1, IS 800:2007]
    min_gauge = min_pitch
    max_gauge = max_pitch

    # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge)
    # TODO validate g_1 with correct value
    g_1 = 90

    # min_end_distance & max_end_distance = Minimum and Maximum end distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    if uiObj["detailing"]["typeof_edge"] == "a - Sheared or hand flame cut":
        min_end_distance = int(float(1.7 * dia_hole))
    else:
        min_end_distance = int(float(1.5 * dia_hole))

    e = math.sqrt(250 / end_plate_fy)
    max_end_distance = 12 * end_plate_thickness * e

    # min_edge_distance = Minimum edge distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    min_edge_distance = min_end_distance
    max_edge_distance = max_end_distance

    # l_v = Distance between the toe of weld or the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
    # TODO: Implement l_v depending on excomm review
    l_v = 50

    #######################################################################
    # Validation of Input Dock

    # End Plate Thickness

    if end_plate_thickness < max(beam_tf, beam_tw):
        end_plate_thickness = max(beam_tf, beam_tw)
        design_status = False
        logger.error(": Chosen end plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm " % end_plate_thickness)

    # End Plate Height [Ref: Based on reasoning]

    # Minimum and Maximum Plate Height
    # TODO: Validate end_plate_height_mini after excomm review (currently used value of l_v is 50mm)
    end_plate_height_mini = beam_d + 50 + (2 * min_end_distance)

    # TODO: Validate end_plate_height_max after excomm review
    # Note: The distance between the toe of weld or the flange edge to the centre of the nearer bolt is 62.5mm (assumed to be maximum)

    end_plate_height_max = beam_d + 50 + (2 * max_end_distance)

    # End Plate Width

    # Minimum and Maximum width of End Plate [Ref: Based on reasoning and AISC Design guide 16]
    # TODO check for mini width as per AISC after excomm review
    end_plate_width_mini = g_1 + (2 * min_edge_distance)

    end_plate_width_max = max((beam_B + 25), end_plate_width_mini)


    # Check for Minimum and Maximum values of End Plate Height from user input

    if end_plate_height != 0:
        if end_plate_height <= beam_d:
            # end_plate_height = end_plate_height_mini
            design_status = False
            logger.error(": Height of End Plate is less than the depth of the Beam ")
            logger.warning(": Minimum End Plate height required is %2.2f mm" % end_plate_height_mini)
            logger.info(": Increase the Height of End Plate")
        elif end_plate_height <= end_plate_height_mini:
            # end_plate_height = end_plate_height_mini
            design_status = False
            logger.error(": Height of End Plate is less than the minimum required height")
            logger.warning(": Minimum End Plate height required is %2.2f mm" % end_plate_height_mini)
            logger.info(": Increase the Height of End Plate")
    else:
        pass

    if end_plate_height != 0:
        if end_plate_height > end_plate_height_max:
            # end_plate_height = end_plate_height_max
            design_status = False
            logger.error(": Height of End Plate exceeds the maximum required height")
            logger.warning(": Maximum End Plate height required is %2.2f mm" % end_plate_height_max)
            logger.info(": Decrease the Height of End Plate")
    else:
        pass

    #######################################################################
    # Calculation for number of bolts in each column

    # M_u = Total bending moment in kN i.e. (External factored moment + Moment due to axial force )
    M_u = factored_moment + ((factored_axial_load * (beam_d/2 - beam_tf/2)) / 1000)

    # Number of bolts in each column
    # Here, we assume number of columns (n_c) of bolt to be 2
    # TODO Implement/check n_c after excomm review
    n_c = 2
    bolt_shear_capacity = bolt_shear(bolt_dia, n_c, bolt_fu)
    n = math.sqrt((6 * M_u) / (2 * min_pitch * bolt_shear_capacity))
    n = round(n.real)

    # number_of_bolts = Total number of bolts in the configuration
    number_of_bolts = 2 * n

    if number_of_bolts <= 8:
        number_of_bolts = 8
    elif number_of_bolts > 8 or number_of_bolts <= 12:
        number_of_bolts = 12
    elif number_of_bolts > 12 or number_of_bolts <= 16:
        number_of_bolts = 16
    # TODO : validate else statement. (Discuss with sir)
    else:
        logger.error(": The number of bolts exceeds 16")
        logger.warning(": Maximum number of bolts that can be accommodated in Extended End plate configuration is 16")
        logger.info(": Use Bolted cover plate splice connection for higher moments")

    #######################################################################
    # Calculation of Tension in bolts
    # Assuming the Neutral axis to pass through the centre of the bottom flange
    # T1, T2, ..., Tn are the Tension in the bolts starting from top of the end plate and y1, y2, ..., yn are its corresponding distances from N.A
    # TODO : check the working of the loop below
    if number_of_bolts == 8:
        y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
        y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
        y3 = weld_thickness_flange + l_v + (beam_tf/2)
        y = (y1**2 + y2**2 + y3**2)
        T1 = (M_u * y1) / y
        T2 = (M_u * y2) / y
        T3 = (M_u * y3) / y
        T_f = (T1 * (beam_d - beam_tf)) / y1

    elif number_of_bolts == 12:
        y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
        y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
        y3 = y2 - min_pitch
        y4 = (beam_tf/2) + weld_thickness_flange + l_v + min_pitch
        y5 = y4 - min_pitch
        y = (y1**2 + y2**2 + y3**2 + y4**2 + y5**2)
        T1 = (M_u * y1) / y
        T2 = (M_u * y2) / y
        T3 = (M_u * y3) / y
        T4 = (M_u * y4) / y
        T5 = (M_u * y5) / y
        T_f = (T1 * (beam_d - beam_tf)) / y1

    elif number_of_bolts == 16:
        y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
        y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
        y3 = y2 - min_pitch
        y4 = y3 - min_pitch
        y5 = (beam_tf/2) + weld_thickness_flange + l_v + (2 * min_pitch)
        y6 = y5 - min_pitch
        y7 = y6 - min_pitch
        y = (y1**2 + y2**2 + y3**2 + y4**2 + y5**2 + y6**2 + y7**2)
        T1 = (M_u * y1) / y
        T2 = (M_u * y2) /y
        T3 = (M_u * y3) /y
        T4 = (M_u * y4) /y
        T5 = (M_u * y5) /y
        T6 = (M_u * y6) /y
        T7 = (M_u * y7) /y
        T_f = (T1 * (beam_d - beam_tf)) / y1

    else:
        pass

    #######################################################################
    # Calculating actual required thickness of End Plate (tp_required) as per bending criteria
    b_e = beam_B / 2

    # M_p = Plastic moment capacity of end plate
    tension_flange = T_f
    M_p = (tension_flange * l_v) / 2
    tp_required = math.sqrt((4 * 1.10 * M_p) / (end_plate_fy * b_e))
    tp_required = round(tp_required)

    if tp_required < end_plate_thickness:
        design_status = False
        logger.error(": Chosen end plate thickness in not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm" % tp_required)
        logger.info(": Increase end plate thickness")
    else:
        pass

    # Calculation of Prying Force at Tension flange
    # TODO : add condition of beta depending on bolt type

    beta = 2
    eta = 1.5
    f_0 = 0.7 * bolt_fu
    l_e = min(min_end_distance, 1.1 * tp_required * math.sqrt((beta * f_0) / bolt_fy))

    Q = (l_v / (2 * l_e)) * (T_f - ((beta * eta * f_0 * b_e * tp_required ** 4) / (27 * l_e * l_v ** 2)))
    Q = round(Q.real, 3)

















































