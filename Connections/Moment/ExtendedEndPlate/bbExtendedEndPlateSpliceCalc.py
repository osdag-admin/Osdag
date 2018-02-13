"""
Created on 16th October, 2017.

@author: Danish Ansari


Module: Beam to beam extended end plate splice connection (Moment connection)

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel structures by Dr. N Subramanian (chapter 5 and 6)
            3) Fundamentals of Structural steel design by M.L Gambhir
            4) AISC Design guide 16 and 4


ASCII diagram
                                      End plate
                                     +---+
                                 +----------+ Bolt
                                     | | |
+------------------------------------+ | +-------------------------------+
+------------------------------------| | |-------------------------------+
|                                   || | ||                              |
|                                +----------+                            |
|                                   || | ||   Bolt                       |
|                                +----------+                            |
|                                   || | ||                              |
|           Beam Section            || | ||            Beam Section      |
|                                   || | ||                              |
|                                +-----------+                           |
|                                   || | ||     Bolt                     |
|                                +-----------+                           |
|                                   || | ||                              |
+------------------------------------| | |-------------------------------+
+------------------------------------+ | +-------------------------------+
                                     | | |
                                 +----------+  Bolt
                                     +---+

                                      End plate
Note: The above ASCII diagram does not show details of weld


"""

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


# Function for net area of bolts at threaded portion of bolts
# Reference: Design of steel structures by N. Subramanian, page 348 or 358


def netArea_thread(dia):
    """

    Args:
        dia: (int)- diameter of bolt (HSFG/Bearing bolt)

    Returns: (float)- Net area of bolts at threaded portion (Ref. Table 5.11 Subramanian's book, page: 358 )

    """
    netArea = {12: 84.3, 16: 157, 20: 245, 22: 303, 24: 353, 27: 459, 30: 561, 36: 817}
    return netArea[dia]

#######################################################################

# Function for net area of bolts at threaded portion of bolts
# Reference: Design of steel structures by N. Subramanian, page 348 or 358


def netarea_shank(dia):
    """

    Args:
        dia: (int) -  diameter of bolt (HSFG/Bearing bolt)

    Returns: (int)- Net area of bolts at shank portion (Ref. Table 5.11 Subramanian's book, page: 358 )

    """
    net_area = {12: 113, 16: 201, 20: 314, 22: 380, 24: 452, 27: 572, 30: 706, 36: 1017}
    return net_area[dia]

#######################################################################

#Function for long joints (beta_lj)
#Source: Cl 10.3.3.1
#Reference: Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007


def long_joint(dia, l_j):
    """

    Args:
        dia: (int)- diameter of bolt
        l_j: (float)- length of joint i.e. distance between first and last bolt in the joint measured in the direction of load transfer

    Returns: (float)- reduction factor beta_lj

    """
    beta_lj = 1.075 - (0.005 * (l_j/dia))
    return beta_lj


#######################################################################

# Function for Shear Capacity of bearing bolt (also known as black bolt)
# Reference: Cl 10.3.3 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007
# Assumption: The shear planes are assumed to be passing through the threads of the bolt

def bolt_shear(dia, n, bolt_fu):
    """

    Args:
        dia: (int)- diameter of bolt
        n: (str)- number of shear plane(s) through which bolt is passing
        bolt_fu: (float)- Ultimate tensile strength of a bolt

    Returns: (float)- Shear capacity of bearing type bolt in kN

    """
    A = netArea_thread(dia)
    V_dsb = bolt_fu * n * A / (math.sqrt(3) * 1.25 * 1000)
    V_dsb = round(V_dsb.real, 3)
    return V_dsb


#######################################################################

# Function for Bearing Capacity of bearing bolt (also known as black bolt)
# Reference: Cl 10.3.4 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def bolt_bearing(dia, t, k_b, bolt_fu):
    """

    Args:
        dia: (int)- diameter of bolt
        t: (float)- summation of thickneses of the connected plates experencing bearing stress in same direction, or if the bolts are countersunk, the thickness of plate minus 1/2 of the depth of countersunk
        k_b: (float)- multiplying factor (Ref: Cl 10.3.4 IS 800:2007)
        bolt_fu: (float)- Ultimate tensile strength of a bolt

    Returns: (float)- Bearing capacity of bearing type bolt in kN

    """
    V_dpb = 2.5 * k_b * dia * t * bolt_fu / (1.25 * 1000)
    V_dpb  = round(V_dpb.real, 3)
    return V_dpb


#######################################################################

# Function for minimum height of end plate
# Reference: Based on reasoning

def min_plate_height(beam_D, l_v, n_r, min_pitch, e_1):
    """

    Args:
        beam_D: (float) - Depth of beam
        l_v: (float)- Distance between the toe of weld or flange to the centre of the nearer bolt
        n_r: (int)- number of row(s) above or below the beam flange
        min_pitch: (float)- minimum pitch distance i.e. 2.5*bolt_diameter
        e_1: (float)- minimum end distance i.e. 1.7*bolt_hole_diameter

    Returns: (float)- Minimum required height of extended end plate as per detailing requirements in mm

    """
    min_end_plate_height = beam_D + (2 * l_v) + (2 * (n_r-1) * min_pitch) + (2 * e_1)
    return min_end_plate_height


#######################################################################

# Function for minimum width of end plate
# Reference: Based on reasoning

def min_plate_width(g_1, n, min_gauge, e_2):
    """

    Args:
        g_1: (float)- Cross-centre gauge distance
        n: (int)- Number of columns of bolt (assumed to be 2)
        min_gauge: (float)- minimum gauge distance i.e. 2.5*bolt_diameter
        e_2: (float)- minimum edge distance i.e. 1.7*bolt_hole_diameter

    Returns: (float)- Minimum required width of extended end plate as per detailing requirements in mm

    """
    min_end_plate_width = g_1 + (n - 2) * min_gauge + (2 * e_2)
    return min_end_plate_width


#######################################################################

# Function for calculation of Prying Force in bolts
# Reference: Cl 10.4.7 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

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

    Returns: (float)- Prying force in bolt (in kN)

    """
    prying_force_bolt = (l_v * (2 * l_e) ** -1) * (T_e - ((beta * eta * f_0 * b_e * t_p ** 4) * (27 * l_e * l_v ** 2) ** -1))
    return prying_force_bolt

#######################################################################

# Function for calculating Tension capacity of HSFG bolt
# Reference: Cl 10.4.5 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007


def bolt_tension_hsfg(bolt_fu, netArea):
    """

    Args:
        bolt_fu: (float)- Ultimate tensile strength of a bolt
        netArea: (float)- Net tensile stress area as specified in IS 1367 (area at threads)

    Returns: (float)- Tension capacity of HSFG bolt in kN

    """
    T_df = 0.9 * bolt_fu * netArea * (1.25 * 1000) ** -1
    return T_df


#######################################################################

# Function for calculating Tension capacity of bearing bolt (also known as black bolt)
# Reference: Cl 10.3.5 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def bolt_tension_bearing(bolt_fu, netArea):
    """

    Args:
        bolt_fu: (float)- Ultimate tensile strength of a bolt
        netArea: (float)- Net tensile stress area as specified in IS 1367 (area at threads)

    Returns: (float)- Tension capacity of Bearing bolt in kN

    """
    T_db = 0.9 * bolt_fu * netArea / 1.25 * 1000
    return T_db


#######################################################################

# Function for calculating Shear yielding capacity of End Plate
# Reference: Cl 8.4.1 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def shear_yielding(A_v, plate_fy):
    """

    Args:
        A_v: (float)- Gross shear area of end plate
        plate_fy: (float)- Yield stress of plate material

    Returns: (float)- Shear yielding capacity of End Plate in kN

    """
    V_d = 0.6 * A_v * plate_fy / (math.sqrt(3) * 1.10 * 1000)
    return V_d


#######################################################################

# Function for calculating Shear rupture capacity of End Plate
# Reference: Cl 8.4.1 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def shear_rupture(A_vn, plate_fu):
    """

    Args:
        A_vn: (float)- Net shear area of end plate
        plate_fu: (float)- Ultimate stress of plate material

    Returns: (float)- Shear rupture capacity of End Plate in kN

    """
    R_n = 0.6 * A_vn * plate_fu / 1000
    return R_n


#######################################################################
# Function for fetching beam parameters from the database

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

    connectivity = uiObj['Member']['Connectivity']
    beam_sec = uiObj['Member']['BeamSection']
    beam_fu = float(uiObj['Member']['fu (MPa)'])
    beam_fy = float(uiObj['Member']['fy (MPa)'])

    factored_moment = float(uiObj['Load']['Moment (kNm)'])
    factored_shear_load = float(uiObj['Load']['ShearForce (kN)'])
    factored_axial_load = float(uiObj['Load']['AxialForce (kN)'])
    if factored_axial_load == '':
        factored_axial_load = 0
    else:
        factored_axial_load = float(factored_axial_load)

    bolt_dia = int(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = float(uiObj['Bolt']['Grade'])

    mu_f = float(uiObj["bolt"]["slip_factor"])
    gamma_mw = float(uiObj["weld"]["safety_factor"])
    dp_bolt_hole_type = uiObj["bolt"]["bolt_hole_type"]
    dia_hole = bolt_dia + int(uiObj["bolt"]["bolt_hole_clrnce"])
    weld_type = uiObj["weld"]["typeof_weld"]
    dp_bolt_type = uiObj["Bolt"]["Grade"]

    end_plate_thickness = float(uiObj['Plate']['Thickness (mm)'])

    end_plate_width = str(uiObj['Plate']['Width (mm)'])
    if end_plate_width == '':
        end_plate_width = 0
    else:
        end_plate_width = float(end_plate_width)

    end_plate_height = str(uiObj['Plate']['Height (mm)'])
    if end_plate_height == '':
        end_plate_height = 0
    else:
        end_plate_height = float(end_plate_height)

    # TODO implement after excomm review for different grades of plate
    end_plate_fu = float(uiObj['Member']['fu (MPa)'])
    end_plate_fy = float(uiObj['Member']['fy (MPa)'])

    weld_thickness_flange = float(uiObj['Weld']['Flange (mm)'])
    weld_thickness_web = float(uiObj['Weld']['Web (mm)'])

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

    # global dictbeamdata
    dictbeamdata = get_beamdata(beam_sec)

    beam_tw = float(dictbeamdata["tw"])
    beam_tf = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_B = float(dictbeamdata["B"])
    beam_R1 = float(dictbeamdata["R1"])
    beam_R2 = float(dictbeamdata["R2"])
    alpha = float(dictbeamdata["FlangeSlope"])
    beam_length = 800.0

    #######################################################################
    # Calculation of Bolt strength in MPa
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu

    #######################################################################
    # Calculation of Spacing

    # t_thinner is the thickness of the thinner plate(s) being connected
    t_thinner = end_plate_thickness

    # min_pitch & max_pitch = Minimum and Maximum pitch distance (mm) [Cl. 10.2.2, IS 800:2007]
    min_pitch = int(math.ceil(2.5 * bolt_dia))
    pitch_dist_min = min_pitch + (5 - min_pitch) % 5  # round off to nearest greater multiple of five

    max_pitch = int(min(math.ceil(32 * t_thinner), 300))
    pitch_dist_max = max_pitch + (5 - max_pitch) % 5  # round off to nearest greater multiple of five

    # min_gauge & max_gauge = Minimum and Maximum gauge distance (mm) [Cl. 10.2.3.1, IS 800:2007]

    gauge_dist_min = pitch_dist_min
    gauge_dist_max = pitch_dist_max

    # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge) (Steel designers manual, page 733, 6th edition - 2003)
    # TODO validate g_1 with correct value
    g_1 = 90

    # min_end_distance & max_end_distance = Minimum and Maximum end distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    if uiObj["detailing"]["typeof_edge"] == "a - Sheared or hand flame cut":
        min_end_distance = int(math.ceil(1.7 * dia_hole))
    else:
        min_end_distance = int(float(1.5 * dia_hole))

    end_dist_mini = min_end_distance + (5 - min_end_distance) % 5  # round off to nearest greater multiple of five

    e = math.sqrt(250 / end_plate_fy)
    max_end_distance = math.ceil(12 * end_plate_thickness * e)

    end_dist_max = max_end_distance + (5 - max_end_distance) % 5  # round off to nearest greater multiple of five

    # min_edge_distance = Minimum edge distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    edge_dist_mini = end_dist_mini
    edge_dist_max = end_dist_max

    # l_v = Distance between the toe of weld or the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
    # TODO: Implement l_v depending on excomm review
    l_v = float(50)

    #######################################################################
    # Validation of Input Dock

    # End Plate Thickness

    # TODO : Is this condition for the main file? EP thickness depends on the plastic capacity of plate
    if end_plate_thickness < max(beam_tf, beam_tw):
        end_plate_thickness = max(math.ceil(beam_tf, beam_tw))
        design_status = False
        logger.error(": Chosen end plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm " % end_plate_thickness)

    # End Plate Height [Ref: Based on reasoning]

    # Minimum and Maximum Plate Height
    # TODO: Validate end_plate_height_mini after excomm review (currently used value of l_v is 50mm)
    end_plate_height_mini = beam_d + 50 + (2 * end_dist_mini)

    # TODO: Validate end_plate_height_max after excomm review
    # Note: The distance between the toe of weld or the flange edge to the centre of the nearer bolt is 62.5mm (assumed to be maximum)

    end_plate_height_max = beam_d + 50 + (2 * end_dist_max)

    # End Plate Width

    # Minimum and Maximum width of End Plate [Ref: Based on reasoning and AISC Design guide 16]
    # TODO check for mini width as per AISC after excomm review

    end_plate_width_mini = max(g_1 + (2 * edge_dist_mini), beam_B)
    end_plate_width_max = max((beam_B + 25), end_plate_width_mini)

    if end_plate_width != 0:
        if end_plate_width < end_plate_width_mini:
            design_status = False
            logger.error(": Width of the End Plate is less than the minimum required value ")
            logger.warning(": Minimum End Plate width required is %2.2f mm" % end_plate_width_mini)
            logger.info(": Increase the width of End Plate")
        if end_plate_width > end_plate_width_max:
            design_status = False
            logger.error(": Width of the End Plate exceeds the maximum allowed width ")
            logger.warning(": Maximum allowed width of End Plate is %2.2f mm" % end_plate_width_max)
            logger.info(": Decrease the width of End Plate")

    # Check for Minimum and Maximum values of End Plate Height from user input

    if end_plate_height != 0:
        if end_plate_height <= beam_d:
            design_status = False
            logger.error(": Height of End Plate is less than/or equal to the depth of the Beam ")
            logger.warning(": Minimum End Plate height required is %2.2f mm" % end_plate_height_mini)
            logger.info(": Increase the Height of End Plate")
        elif end_plate_height <= end_plate_height_mini:
            design_status = False
            logger.error(": Height of End Plate is less than the minimum required height")
            logger.warning(": Minimum End Plate height required is %2.2f mm" % end_plate_height_mini)
            logger.info(": Increase the Height of End Plate")

        if end_plate_height > end_plate_height_max:
            design_status = False
            logger.error(": Height of End Plate exceeds the maximum allowed height")
            logger.warning(": Maximum allowed height of End Plate is %2.2f mm" % end_plate_height_max)
            logger.info(": Decrease the Height of End Plate")

    #######################################################################
    # Check for shear capacity of HSFG bolt (Cl. 10.4.3, IS 800:2007)
    # Check for shear and bearing capacities of Bearing bolt (Cl. 10.3.3 and Cl. 10.3.4, IS 800:2007)
    # Here,
    # Vdsf = nominal shear capacity of HSFG bolt
    # V_dsf = nominal shear capacity of HSFG bolt after multiplying the correction factor(s)
    # Vdsb = nominal shear capacity of Bearing bolt
    # V_dsb = nominal shear capacity of Bearing bolt after multiplying the correction factor(s)

    n_e = 1  # number of effective interfaces offering resistance to shear
    factor = 1
    sum_plate_thickness = 2 * end_plate_thickness

    # Calculation of k_b
    kb_1 = float(end_dist_mini) / (3 * dia_hole)
    kb_2 = (float(pitch_dist_min) / (3 * dia_hole)) - 0.25
    kb_3 = bolt_fu / end_plate_fu
    kb_4 = 1.0
    k_b = min(kb_1, kb_2, kb_3, kb_4)

    plate_fu = int(end_plate_fu)

    # Check for long joints (Cl. 10.3.3.1, IS 800:2007)
    l_j = beam_d - (2 * beam_tf) - (2 * weld_thickness_flange) - (2 * l_v)

    if bolt_type == "HSFG":
        Vdsf = ConnectionCalculations.bolt_shear_hsfg(bolt_dia, bolt_fu, mu_f, n_e, dp_bolt_hole_type)

        if l_j > 15 * bolt_dia:
            V_dsf = Vdsf * long_joint(bolt_dia, l_j)
        else:
            V_dsf = Vdsf
        bolt_capacity = V_dsf  # Capacity of HSFG bolt
        bearing_capacity = "N/A"
    else:
        Vdsb = ConnectionCalculations.bolt_shear(bolt_dia, n_e, bolt_fu)      # 1. Check for Shear capacity of bearing bolt

        if l_j > 15 * bolt_dia:
            V_dsb = Vdsb * long_joint(bolt_dia, l_j)
        else:
            V_dsb = Vdsb

        Vdpb = ConnectionCalculations.bolt_bearing(bolt_dia, factor, sum_plate_thickness, k_b, plate_fu)  # 2. Check for Bearing capacity of bearing bolt

        V_db = min(V_dsb, Vdpb)   # Capacity of bearing bolt (V_db) is minimum of V_dsb and Vdpb
        bolt_capacity = V_db
        bearing_capacity = Vdpb

    #######################################################################
    # Calculation for number of bolts in each column

    # M_u = Total bending moment in kNm i.e. (External factored moment + Moment due to axial force )
    M_u = factored_moment + ((factored_axial_load * (beam_d/2 - beam_tf/2)) / 1000)  # kN-m

    # Number of bolts in each column

    if bolt_type == "HSFG":
        bolt_shear_capacity = V_dsf
    else:
        bolt_shear_capacity = V_dsb

    # TODO : Here 2 is the number of columns of bolt (Check for implementation with excomm)
    n = math.sqrt((6 * M_u * 10 ** 3) / (2 * pitch_dist_min * bolt_shear_capacity))
    n = math.ceil(n)

    # number_of_bolts = Total number of bolts in the configuration
    # TODO: Update number of bolts after review
    number_of_bolts = n

    if number_of_bolts <= 8:
        number_of_bolts = 8
    elif number_of_bolts > 8 and number_of_bolts <= 12:
        number_of_bolts = 12
    elif number_of_bolts > 12 and number_of_bolts <= 16:
        number_of_bolts = 16
    elif number_of_bolts > 16 and number_of_bolts <= 20:
        number_of_bolts = 20
    # TODO : validate else statement. (Discuss with sir)
    else:
        logger.error(": The number of bolts exceeds 16")
        logger.warning(": Maximum number of bolts that can be accommodated in Extended End plate configuration is 16")
        logger.info(": Use Bolted cover plate splice connection for higher moments")

    # Number of rows of bolt
    if number_of_bolts == 8:
        number_rows = 4
    elif number_of_bolts == 12:
        number_rows = 6
    elif number_of_bolts == 16:
        number_rows = 8
    elif number_of_bolts == 20:
        number_rows = 10

    #######################################################################
    minimum_pitch_distance = pitch_dist_min
    maximum_pitch_distance = pitch_dist_max

    minimum_gauge_distance = gauge_dist_min
    maximum_gauge_distance = gauge_dist_max

    minimum_end_distance = end_dist_mini
    maximum_end_distance = end_dist_max

    minimum_edge_distance = edge_dist_mini
    maximum_edge_distance = edge_dist_max

    # Calculating pitch, gauge, end and edge distances for different cases

    # Case 1: When the height and the width of end plate is not specified by user
    if end_plate_height == 0 and end_plate_width == 0:

        if number_of_bolts == 8:
            pitch_distance = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v))

            if pitch_distance < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if pitch_distance > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 12:
            pitch_distance_2_3 = pitch_distance_4_5 = pitch_dist_min  # Distance between 2nd and 3rd bolt and 4th and 5th bolt from top
            pitch_distance_3_4 = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v) + pitch_distance_2_3 + pitch_distance_4_5)

            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 16:
            pitch_distance_2_3 = pitch_distance_3_4 = pitch_distance_5_6 = pitch_distance_6_7 = pitch_dist_min
            pitch_distance_4_5 = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v) + pitch_distance_2_3 + pitch_distance_3_4 + pitch_distance_5_6 + pitch_distance_6_7)

            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 20:
            pitch_distance_1_2 = pitch_distance_9_10 = pitch_dist_min
            pitch_distance_3_4 = pitch_distance_4_5 = pitch_distance_6_7 = pitch_distance_7_8 = pitch_dist_min
            pitch_distance_5_6 = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v) + (4 * pitch_dist_min))

            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        if number_of_bolts == 8 or number_of_bolts == 12 or number_of_bolts == 16:
            end_plate_height_provided = beam_d + ((2 * weld_thickness_flange) + (2 * l_v) + (2 * minimum_end_distance))
        else:
            end_plate_height_provided = beam_d + ((2 * weld_thickness_flange) + (2 * l_v) + (2 * minimum_pitch_distance) + (2 * minimum_end_distance))

        end_plate_width_provided = max(beam_B + 25, g_1 + (2 * minimum_edge_distance))

    # Case 2: When the height of end plate is specified but the width is not specified by the user
    elif end_plate_height != 0 and end_plate_width == 0:
        height_available = end_plate_height  # available height of end plate

        if number_of_bolts == 8:
            pitch_distance = height_available - ((2 * minimum_end_distance) + (2 * l_v) + (4 * weld_thickness_flange) + (2 * beam_tf) + (2 * l_v))

            if pitch_distance < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if pitch_distance > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 12:
            pitch_distance_2_3 = pitch_distance_4_5 = pitch_dist_min
            pitch_distance_3_4 = height_available - ((2 * minimum_end_distance) + (2 * l_v) + (4 * weld_thickness_flange) + (2 * beam_tf) + (2 * l_v) + pitch_distance_2_3 + pitch_distance_4_5)

            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 16:
            pitch_distance_2_3 = pitch_distance_3_4 = pitch_distance_5_6 = pitch_distance_6_7 = pitch_dist_min
            pitch_distance_4_5 = height_available - ((2 * minimum_end_distance) + (4 * l_v) + (4 * weld_thickness_flange) + (4 * pitch_dist_min))

            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 20:
            pitch_distance_1_2 = pitch_distance_9_10 = pitch_dist_min
            pitch_distance_3_4 = pitch_distance_4_5 = pitch_distance_6_7 = pitch_distance_7_8 = pitch_dist_min
            pitch_distance_5_6 = height_available - ((2 * minimum_end_distance) + (4 * l_v) + (2 * beam_tf) + (4 * weld_thickness_flange) + (4 * pitch_dist_min))

            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        end_plate_height_provided = height_available
        end_plate_width_provided = max(beam_B + 25, g_1 + (2 * minimum_edge_distance))

    # Case 3: When the height of end plate is not specified but the width is specified by the user
    elif end_plate_height == 0 and end_plate_width != 0:

        if number_of_bolts == 8:
            pitch_distance = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v))

            if pitch_distance < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if pitch_distance > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 12:
            pitch_distance_2_3 = pitch_distance_4_5 = pitch_dist_min
            pitch_distance_3_4 = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v) + pitch_distance_2_3 + pitch_distance_4_5)

            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 16:
            pitch_distance_2_3 = pitch_distance_3_4 = pitch_distance_5_6 = pitch_distance_6_7 = pitch_dist_min
            pitch_distance_4_5 = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v) + pitch_distance_2_3 + pitch_distance_3_4 + pitch_distance_5_6 + pitch_distance_6_7)

            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 20:
            pitch_distance_1_2 = pitch_distance_9_10 = pitch_dist_min
            pitch_distance_3_4 = pitch_distance_4_5 = pitch_distance_6_7 = pitch_distance_7_8 = pitch_dist_min
            pitch_distance_5_6 = beam_d - ((2 * beam_tf) + (2 * weld_thickness_flange) + (2 * l_v) + (4 * pitch_dist_min))

            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        if number_of_bolts == 8 or number_of_bolts == 12 or number_of_bolts == 16:
            end_plate_height_provided = beam_d + ((2 * weld_thickness_flange) + (2 * l_v) + (2 * minimum_end_distance))
        else:
            end_plate_height_provided = beam_d + ((2 * weld_thickness_flange) + (2 * l_v) + (2 * minimum_pitch_distance) + (2 * minimum_end_distance))

        width_available = end_plate_width
        end_plate_width_provided = width_available

    # Case 4: When the height and the width of End Plate is specified by the user
    elif end_plate_height != 0 and end_plate_width != 0:

        height_available = end_plate_height

        if number_of_bolts == 8:
            pitch_distance = height_available - ((2 * minimum_end_distance) + (2 * l_v) + (4 * weld_thickness_flange) + (2 * beam_tf) + (2 * l_v))

            if pitch_distance < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if pitch_distance > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 12:
            pitch_distance_2_3 = pitch_distance_4_5 = pitch_dist_min
            pitch_distance_3_4 = height_available - ((2 * minimum_end_distance) + (2 * l_v) + (4 * weld_thickness_flange) + (2 * beam_tf) + (2 * l_v) + pitch_distance_2_3 + pitch_distance_4_5)

            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_4_5 or pitch_distance_3_4) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 16:
            pitch_distance_2_3 = pitch_distance_3_4 = pitch_distance_5_6 = pitch_distance_6_7 = pitch_dist_min
            pitch_distance_4_5 = height_available - ((2 * minimum_end_distance) + (4 * l_v) + (4 * weld_thickness_flange) + (4 * pitch_dist_min))

            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_2_3 or pitch_distance_3_4 or pitch_distance_5_6 or pitch_distance_6_7 or pitch_distance_4_5) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        elif number_of_bolts == 20:
            pitch_distance_1_2 = pitch_distance_9_10 = pitch_dist_min
            pitch_distance_3_4 = pitch_distance_4_5 = pitch_distance_6_7 = pitch_distance_7_8 = pitch_dist_min
            pitch_distance_5_6 = height_available - ((2 * minimum_end_distance) + (4 * l_v) + (2 * beam_tf) + (4 * weld_thickness_flange) + (4 * pitch_dist_min))

            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) < pitch_dist_min:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is smaller than the minimum required value (Clause 10.2.2, IS 800:2007)")
                logger.warning(": Minimum required Pitch distance is % 2.2f mm" % pitch_dist_min)
                logger.info(": Re-design the connection using bolt of smaller diameter")
            if (pitch_distance_1_2 or pitch_distance_3_4 or pitch_distance_4_5 or pitch_distance_6_7 or pitch_distance_7_8 or pitch_distance_9_10 or pitch_distance_5_6) > pitch_dist_max:
                design_status = False
                logger.error(": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher diameter")

        end_plate_height_provided = height_available

        width_available = end_plate_width
        end_plate_width_provided = width_available

    #######################################################################
    # Validation of calculated Height and Width of End Plate

    if number_of_bolts == 8 or number_of_bolts == 12 or number_of_bolts == 16:
        if end_plate_height_provided < end_plate_height_mini:
            design_status = False
            logger.error(": Height of End Plate is less than the minimum required height")
            logger.warning(": Minimum End Plate height required is %2.2f mm" % end_plate_height_mini)
            logger.info(": Increase the Height of End Plate")
        if end_plate_height_provided > end_plate_height_max:
            design_status = False
            logger.error(": Height of End Plate exceeds the maximum allowed height")
            logger.warning(": Maximum allowed height of End Plate is %2.2f mm" % end_plate_height_max)
            logger.info(": Decrease the Height of End Plate")

    elif number_of_bolts == 20:
        if end_plate_height_provided < (end_plate_height_mini + (2 * pitch_dist_min)):
            design_status = False
            logger.error(": Height of End Plate is less than the minimum required height")
            logger.warning(": Minimum End Plate height required is %2.2f mm" % end_plate_height_mini)
            logger.info(": Increase the Height of End Plate")
        if end_plate_height_provided > (end_plate_height_max + (2 * pitch_dist_min)):
            design_status = False
            logger.error(": Height of End Plate exceeds the maximum allowed height")
            logger.warning(": Maximum allowed height of End Plate is %2.2f mm" % end_plate_height_max)
            logger.info(": Decrease the Height of End Plate")

    if end_plate_width_provided < end_plate_width_mini:
        design_status = False
        logger.error(": Width of the End Plate is less than the minimum required value ")
        logger.warning(": Minimum End Plate width required is %2.2f mm" % end_plate_width_mini)
        logger.info(": Increase the width of End Plate")

    if end_plate_width_provided > end_plate_width_max:
        design_status = False
        logger.error(": Width of the End Plate exceeds the maximum allowed width ")
        logger.warning(": Maximum allowed width of End Plate is %2.2f mm" % end_plate_width_max)
        logger.info(": Decrease the width of End Plate")

    #######################################################################
    # Calculation of Tension in bolts
    # Assuming the Neutral axis to pass through the centre of the bottom flange
    # T1, T2, ..., Tn are the Tension in the bolts starting from top of the end plate and y1, y2, ..., yn are its corresponding distances from N.A
    # TODO : check the working of the below loop

    # Case 1: When the height and the width of end plate is not specified by user
    if end_plate_height == 0 and end_plate_width == 0:
        if number_of_bolts == 8:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = weld_thickness_flange + l_v + (beam_tf/2)
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y  # Here, T1 is the tension in the topmost bolt (i.e. critical bolt) starting from the tension flange
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 12:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = (beam_tf/2) + weld_thickness_flange + l_v + pitch_dist_min
            y5 = y4 - pitch_distance_4_5
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 16:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = y3 - pitch_distance_3_4
            y5 = (beam_tf/2) + weld_thickness_flange + l_v + (2 * pitch_dist_min)
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 20:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v + pitch_distance_1_2
            y2 = y1 - pitch_distance_1_2
            y3 = y2 - (beam_tf + (2 * l_v) + (2 * weld_thickness_flange))
            y4 = y3 - pitch_distance_3_4
            y5 = y4 - pitch_distance_4_5
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y8 = y7 - pitch_distance_7_8
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2 + y8 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y
            T8 = (M_u * 10 ** 3 * y8) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

    # Case 2: When the height of end plate is specified but the width is not specified by the user
    elif end_plate_height != 0 and end_plate_width == 0:
        if number_of_bolts == 8:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = weld_thickness_flange + l_v + (beam_tf/2)
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y  # Here, T1 is the tension in the topmost bolt (i.e. critical bolt) starting from the tension flange
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 12:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = (beam_tf/2) + weld_thickness_flange + l_v + pitch_dist_min
            y5 = y4 - pitch_distance_4_5
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 16:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = y3 - pitch_distance_3_4
            y5 = (beam_tf/2) + weld_thickness_flange + l_v + (2 * pitch_dist_min)
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 20:
            y1 = (beam_d - beam_tf / 2) + weld_thickness_flange + l_v + pitch_distance_1_2
            y2 = y1 - pitch_distance_1_2
            y3 = y2 - (beam_tf + (2 * l_v) + (2 * weld_thickness_flange))
            y4 = y3 - pitch_distance_3_4
            y5 = y4 - pitch_distance_4_5
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y8 = y7 - pitch_distance_7_8
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2 + y8 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y
            T8 = (M_u * 10 ** 3 * y8) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

    # Case 3: When the height of end plate is not specified but the width is specified by the user
    elif end_plate_height == 0 and end_plate_width != 0:
        if number_of_bolts == 8:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = weld_thickness_flange + l_v + (beam_tf/2)
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y  # Here, T1 is the tension in the topmost bolt (i.e. critical bolt) starting from the tension flange
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 12:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = (beam_tf/2) + weld_thickness_flange + l_v + pitch_dist_min
            y5 = y4 - pitch_distance_4_5
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 16:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = y3 - pitch_distance_3_4
            y5 = (beam_tf/2) + weld_thickness_flange + l_v + (2 * pitch_dist_min)
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 20:
            y1 = (beam_d - beam_tf / 2) + weld_thickness_flange + l_v + pitch_distance_1_2
            y2 = y1 - pitch_distance_1_2
            y3 = y2 - (beam_tf + (2 * l_v) + (2 * weld_thickness_flange))
            y4 = y3 - pitch_distance_3_4
            y5 = y4 - pitch_distance_4_5
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y8 = y7 - pitch_distance_7_8
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2 + y8 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y
            T8 = (M_u * 10 ** 3 * y8) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

    # Case 4: When the height and the width of End Plate is specified by the user
    elif end_plate_height != 0 and end_plate_width != 0:
        if number_of_bolts == 8:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = weld_thickness_flange + l_v + (beam_tf/2)
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y  # Here, T1 is the tension in the topmost bolt (i.e. critical bolt) starting from the tension flange
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 12:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = (beam_tf/2) + weld_thickness_flange + l_v + pitch_dist_min
            y5 = y4 - pitch_distance_4_5
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 16:
            y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
            y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
            y3 = y2 - pitch_distance_2_3
            y4 = y3 - pitch_distance_3_4
            y5 = (beam_tf/2) + weld_thickness_flange + l_v + (2 * pitch_dist_min)
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

        elif number_of_bolts == 20:
            y1 = (beam_d - beam_tf / 2) + weld_thickness_flange + l_v + pitch_distance_1_2
            y2 = y1 - pitch_distance_1_2
            y3 = y2 - (beam_tf + (2 * l_v) + (2 * weld_thickness_flange))
            y4 = y3 - pitch_distance_3_4
            y5 = y4 - pitch_distance_4_5
            y6 = y5 - pitch_distance_5_6
            y7 = y6 - pitch_distance_6_7
            y8 = y7 - pitch_distance_7_8
            y = (y1 ** 2 + y2 ** 2 + y3 ** 2 + y4 ** 2 + y5 ** 2 + y6 ** 2 + y7 ** 2 + y8 ** 2)

            T1 = (M_u * 10 ** 3 * y1) / y
            T2 = (M_u * 10 ** 3 * y2) / y
            T3 = (M_u * 10 ** 3 * y3) / y
            T4 = (M_u * 10 ** 3 * y4) / y
            T5 = (M_u * 10 ** 3 * y5) / y
            T6 = (M_u * 10 ** 3 * y6) / y
            T7 = (M_u * 10 ** 3 * y7) / y
            T8 = (M_u * 10 ** 3 * y8) / y

            T_f = (T1 * (beam_d - beam_tf)) / y1

    #######################################################################
    # Calculating actual required thickness of End Plate (tp_required) as per bending criteria
    b_e = beam_B / 2

    # M_p = Plastic moment capacity of end plate
    # TODO check if T_f value is getting assigned correctly
    tension_flange = T_f
    M_p = (tension_flange * l_v) / 2  # kN-mm
    tp_required = math.sqrt((4 * 1.10 * M_p * 10 ** 3) / (end_plate_fy * b_e))
    tp_required = math.ceil(tp_required)

    tp_provided = math.ceil(tp_required / 2.) * 2  # rounding off to nearest (higher) even number

    if end_plate_thickness < tp_provided:
        design_status = False
        logger.error(": Chosen end plate thickness in not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm" % tp_required)
        logger.info(": Increase end plate thickness")
    else:
        pass

    # Moment demand of End Plate
    M_d = ((tp_required ** 2 * end_plate_fy * b_e) / 4.4 * 1000) * 10 ** -6  # kN-m

    # Moment Capacity of End Plate
    M_c = ((tp_provided ** 2 * end_plate_fy * b_e) / 4.4 * 1000) * 10 ** -6  # kN-m

    if M_d > M_c:
        design_status = False
        logger.error(": The moment demand on end plate exceeds its moment carrying capacity")
        logger.warning(": The moment carrying capacity of end plate is %2.2f kNm" % M_c)
        logger.info(": Increase end plate thickness")

    # Calculation of Prying Force at Tension flange
    # TODO : add condition of beta depending on bolt type
    if uiObj['bolt']['bolt_type'] == "pre-tensioned":
        beta = float(1)
    else:
        beta = float(2)

    eta = 1.5
    f_0 = 0.7 * bolt_fu / 1000  # kN/mm**2
    l_e = min(end_dist_mini, 1.1 * tp_required * math.sqrt((beta * f_0 * 10 ** 3) / bolt_fy))
    T_e = T_f
    t_p = tp_required

    Q = prying_force(T_e, l_v, l_e, beta, eta, f_0, b_e, t_p)
    Q = round(Q.real, 3)

    #######################################################################
    # Check for tension capacities of bolt

    Tdf_1 = (bolt_fy * netarea_shank(bolt_dia) * (1.25/1.10)) / 1000 # Here, Tdf_1 is the maximum allowed tension capacity of bolt (Cl 10.4.5, IS 800:2007 )

    if bolt_type == "HSFG":
        Tdf = bolt_tension_hsfg(bolt_fu, netArea_thread(bolt_dia))
        bolt_tension_capacity = Tdf
        if Tdf > Tdf_1:
            design_status = False
            logger.error(": Tension capacity of HSFG bolt exceeds the specified limit (Clause 10.4.5, IS 800:2007)")
            logger.warning(": Maximum allowed tension capacity for selected diameter of bolt is %2.2f kN" % Tdf_1)
            logger.info(": Re-design the connection using bolt of smaller diameter")
    else:
        Tdb = bolt_tension_bearing(bolt_fu, netArea_thread(bolt_dia))
        bolt_tension_capacity = Tdb

        if Tdb > Tdf_1:
            design_status = False
            logger.error(": Tension capacity of Bearing bolt exceeds the specified limit (Clause 10.3.5, IS 800:2007)")
            logger.warning(": Maximum allowed tension capacity for selected diameter of bolt is %2.2f kN" % Tdf_1)
            logger.info(": Re-design the connection using bolt of smaller diameter")

    # Finding tension in critical bolt (T_b)
    # Here, the critical bolt is the bolt which will be farthest from the top/bottom flange
    T_b = T1 + Q

    if bolt_type == "HSFG":
        if T_b >= Tdf:
            design_status = False
            logger.error(": Tension acting on the critical bolt exceeds its tension carrying capacity (Clause 10.4.5, IS 800:2007)")
            logger.warning(": Maximum allowed tension on HSFG bolt of selected diameter is %2.2f kN" % Tdf)
            logger.info(": Re-design the connection using bolt of higher diameter or grade")
    else:
        if T_b >= Tdb:
            design_status = False
            logger.error(": Tension acting on the critical bolt exceeds its tension carrying capacity (Clause 10.3.5, IS 800:2007)")
            logger.warning(": Maximum allowed tension on Bearing bolt of selected diameter is %2.2f kN" % Tdb)
            logger.info(": Re-design the connection using bolt of higher diameter or grade")

    #######################################################################
    # Check for Combined shear and tension capacity of bolt

    # 1. HSFG bolt (Cl. 10.4.6, IS 800:2007)
    # Here, Vsf = Factored shear load acting on single bolt, Vdf = shear capacity of single HSFG bolt
    # Tf = External factored tension acting on a single HSFG bolt, Tdf = Tension capacity of single HSFG bolt

    # 2. Bearing bolt (Cl. 10.3.6, IS 800:2007)
    # Here, Vsb = Factored shear load acting on single bolt, Vdb = shear capacity of single bearing bolt
    # Tb = External factored tension acting on single bearing bolt, Tdb = Tension capacity of single bearing bolt

    if bolt_type == "HSFG":
        Vsf = factored_shear_load / number_of_bolts
        Vdf = V_dsf
        Tf = T_b
    else:
        Vsb = factored_shear_load / number_of_bolts
        Vdb = V_db
        Tb = T_b

    if bolt_type == "HSFG":
        combined_capacity = (Vsf / Vdf) ** 2 + (Tf / Tdf) ** 2

        if combined_capacity > 1.0:
            design_status = False
            logger.error(": Load due to combined shear and tension on selected HSFG bolt exceeds the limiting value (Clause 10.4.6, IS 800:2007)")
            logger.warning(": The maximum allowable value is 1.0")
            logger.info(": Re-design the connection using bolt of higher diameter or grade")
    else:
        combined_capacity = (Vsb / Vdb) ** 2 + (Tb / Tdb) ** 2

        if combined_capacity > 1.0:
            design_status = False
            logger.error(": Load due to combined shear and tension on selected Bearing bolt exceeds the limiting value (Clause 10.3.6, IS 800:2007)")
            logger.warning(": The maximum allowable value is 1.0")
            logger.info(": Re-design the connection using bolt of higher diameter or grade")

    #######################################################################
    # Check for Shear yielding and shear rupture of end plate

    # 1. Shear yielding of end plate (Clause 8.4.1, IS 800:2007)
    if end_plate_width != 0:
        A_v = end_plate_width_provided * tp_provided  # gross shear area of end plate
    else:
        A_v = end_plate_width_provided * tp_provided  # gross shear area of end plate
    V_d = shear_yielding(A_v, end_plate_fy)

    if V_d < factored_shear_load:
        design_status = False
        logger.error(": The End Plate might yield due to Shear")
        logger.warning(": The minimum required shear yielding capacity is %2.2f kN" % factored_shear_load)
        logger.info(": Increase the thickness of End Plate")

    # 2. Shear rupture of end plate (Clause 8.4.1, IS 800:2007)
    A_vn = A_v - (number_of_bolts * dia_hole)
    R_n = shear_rupture(A_vn, end_plate_fu)

    if R_n < factored_shear_load:
        design_status = False
        logger.error(": The End Plate might rupture due to Shear")
        logger.warning(": The minimum shear rupture capacity required is %2.2f kN" % factored_shear_load)
        logger.info(": Increase the thickness of End Plate")

    # TODO add block shear check

    #######################################################################
    # Member Checks
    # Strength of flange under Compression (Reference: Example 5.23 & 5.27, Design of Steel structures by Dr. N. Subramanian)

    A_f = beam_B * beam_tf  # area of beam flange
    capacity_beam_flange = ((beam_fy / 1.10) * A_f) / 1000  # kN
    force_flange = M_u * 10 ** 3 / (beam_d - beam_tf)

    if capacity_beam_flange < force_flange:
        design_status = False
        logger.error(": Force in the flange is greater than its load carrying capacity")
        logger.warning(": The maximum allowable force on beam flange of selected section is %2.2f kN" % capacity_beam_flange)
        logger.info(": Use a higher beam section with wider and/or thicker flange")

    #######################################################################
    # Design of Weld
    # Assumption: The size of weld at flange will be greater than the size of weld at the web
    # Weld at flange resists bending moment whereas the weld at web resists shear + axial load

    # Ultimate and yield strength of welding material is assumed as Fe410 (E41 electrode)
    # (Reference: Design of Steel structures by Dr. N. Subramanian)
    # TODO add condition to retrieve weld fu and fy from design preference
    weld_fu = 410  # Mpa
    weld_fy = 250  # Mpa

    # Minimum weld thickness (mm)
    # Minimum weld thickness at flange (for drop-down list)
    # Minimum weld thickness (tw_minimum) depends on the thickness of the thicker part (Table 21, IS 800:2007)

    t_thicker = max(beam_tf, beam_tw, tp_required)

    if t_thicker <= 10.0:
        tw_minimum = 3
    elif t_thicker > 10.0 and t_thicker <= 20.0:
        tw_minimum = 5
    elif t_thicker > 20.0 and t_thicker <= 32.0:
        tw_minimum = 6
    elif t_thicker > 32.0 and t_thicker <= 50.0:
        tw_minimum = 8
    # TODO: If tw_minimum is required in calc file?

    # Design of weld at flange
    # Capacity of unit weld (Clause 10.5.7, IS 800:2007)
    k = 0.7  # constant (Table 22, IS 800:2007)

    # capacity_unit_flange is the capacity of weld of unit throat thickness
    capacity_unit_flange = (k * weld_fu) / (math.sqrt(3) * gamma_mw)  # N/mm**2 or MPa

    # Calculating th effective length of weld at the flange
    L_effective_flange = 2 * ((2 * beam_B) + (2 * (beam_B - beam_tw)) + (4 * beam_tf)) + (2 * weld_thickness_flange)  # mm

    # Calculating the area of weld at flange (a_weld_flange) assuming minimum throat thickness i.e. 3mm (Clause 10.5.3, IS 800:2007)
    a_weld_flange = L_effective_flange * 3  # mm**2

    # Calculating stresses on weld
    # Assumption: The weld at flanges are designed to carry Factored external moment and moment due to axial load,
    # whereas, the weld at beam web are designed to resist factored shear force and axial loads

    # 1. Direct stress (DS)
    # Since there is no direct stress (DS_flange) acting on weld at flange, the value od direct stress will be zero
    DS_flange = 0

    # 2. Bending Stress (BS)
    # Finding section modulus i.e. Z = Izz / y (Reference: Table 6.7, Design of Steel structures by Dr. N. Subramanian)
    Z = (beam_B * beam_d) + (beam_d ** 2 / 3)  # mm **3
    BS_flange = M_u * 10 ** 3 / Z

    # Resultant (R)
    R = math.sqrt(DS_flange ** 2 + BS_flange ** 2)

    # Actual required size of weld
    t_weld_flange = math.ceil((R * 10 ** 3) / capacity_unit_flange)  # mm

    if t_weld_flange % 2 == 0:
        t_weld_flange = t_weld_flange
    else:
        t_weld_flange += 1

    if weld_thickness_flange < t_weld_flange:
        design_status = False
        logger.error(": Weld thickness at the flange is not sufficient")
        logger.warning(": Minimum weld thickness required is %2.2f mm " % t_weld_flange)
        logger.info(": Increase the weld thickness at flange")
    if weld_thickness_flange > min(beam_tf, tp_provided):
        design_status = False
        logger.error(": Weld thickness at the flange exceeds the maximum allowed value")
        logger.warning(": Maximum allowed weld thickness at the flange is %2.2f mm" % min(beam_tf, tp_provided))
        logger.info(": Decrease the weld thickness at flange")

    # Design of weld at web
    t_weld_web = int(min(beam_tw, tp_required))
    if t_weld_web > t_weld_flange:
        t_weld_web = t_weld_flange
    else:
        t_weld_web = t_weld_web

    if t_weld_web % 2 == 0:
        t_weld_web = t_weld_web
    else:
        t_weld_web -= 1

    if weld_thickness_web < t_weld_web:
        design_status = False
        logger.error(": Weld thickness at the web is not sufficient")
        logger.warning(": Minimum weld thickness required is %2.2f mm" % t_weld_web)
        logger.info(": Increase the weld thickness at web")
    if weld_thickness_web > int(min(beam_tw, tp_required)):
        design_status = False
        logger.error(": Weld thickness at the web exceeds the maximum allowed value")
        logger.warning(": Maximum allowed weld thickness at the web is %2.2f mm" % t_weld_web)
        logger.info(": Decrease the weld thickness at web")

    #######################################################################
    # Weld Checks
    # Check for stresses in weld due to individual force (Clause 10.5.9, IS 800:2007)

    # Weld at flange
    # 1. Check for normal stress

    f_a_flange = force_flange * 10 ** 3 / (3 * L_effective_flange)  # Here, 3 mm is the effective minimum throat thickness

    # Design strength of fillet weld (Clause 10.5.7.1.1, IS 800:2007)
    f_wd = weld_fu / (math.sqrt(3) * 1.25)
    # TODO: call appropriate factor of safety for weld from main file

    if f_a_flange > f_wd:
        design_status = False
        logger.error(": The stress in weld at flange exceeds the limiting value (Clause 10.5.7.1.1, IS 800:2007)")
        logger.warning(": Maximum stress weld can carry is %2.2f N/mm^2" % f_wd)
        logger.info(": Increase the Ultimate strength of weld and/or length of weld")

    # Weld at web
    L_effective_web = 4 * (beam_d - (2 * beam_tf))

    # 1. Check for normal stress (Clause 10.5.9, IS 800:2007)
    f_a_web = factored_axial_load * 10 ** 3 / (3 * L_effective_web)

    # 2. Check for shear stress
    q_web = factored_shear_load * 10 ** 3 / (3 * L_effective_web)

    # 3. Combination of stress (Clause 10.5.10.1.1, IS 800:2007)
    f_e = math.sqrt(f_a_web ** 2 + (3 * q_web) ** 2)

    if f_e > f_wd:
        design_status = False
        logger.error(": The stress in weld at web exceeds the limiting value (Clause 10.5.10.1.1, IS 800:2007)")
        logger.warning(": Maximum stress weld can carry is %2.2f N/mm^2" % f_wd)
        logger.info(": Increase the Ultimate strength of weld and/or length of weld")

    #######################################################################
    # Design of Stiffener

    # TODO: add material strengths for below condition (design preference?)
    stiffener_fy = beam_fy
    stiffener_fu = beam_fu

    # Height of stiffener (mm) (AISC Design guide 4, page 16)
    # TODO: Do calculation for actual height of end plate above
    h_st = math.ceil((end_plate_height_provided - beam_d) / 2)

    # Length of stiffener
    cf = math.pi/180  # conversion factor to convert degree into radian
    l_st = math.ceil(((h_st - 25) / math.tan(30 * cf)) + 25)

    # Thickness of stiffener
    ts1 = beam_tw
    ts2 = (beam_fy / stiffener_fy) * beam_tw
    thickness_stiffener = math.ceil(max(ts1, ts2))

    thickness_stiffener_provided = math.ceil(thickness_stiffener / 2.) * 2  # round off to the nearest higher multiple of two

    # Check of stiffener against local buckling
    E = 2 * 10 ** 5  # MPa
    ts_required = 1.79 * h_st * stiffener_fy / E  # mm

    if thickness_stiffener_provided < ts_required:
        design_status = False
        logger.error(": The thickness of stiffener is not sufficient")
        logger.error(": The stiffener might buckle locally (AISC Design guide 16)")
        logger.warning(": Minimum required thickness of stiffener to prevent local bucklimg is % 2.2f mm" % ts_required)
        logger.info(": Increase the thickness of stiffener")

    # End of Calculation
    # Output dictionary for different cases

    # Case 1: When the height and the width of end plate is not specified by user
    if end_plate_height == 0 and end_plate_width == 0:
        outputobj = {}
        outputobj['Bolt'] = {}
        outputobj['Bolt']['status'] = design_status
        outputobj['Bolt']['CriticalTension'] = round(T_b, 3)
        outputobj['Bolt']['TensionCapacity'] = round(bolt_tension_capacity, 3)
        outputobj['Bolt']['ShearCapacity'] = round(bolt_shear_capacity, 3)
        outputobj['Bolt']['BearingCapacity'] = bearing_capacity
        outputobj['Bolt']['BoltCapacity'] = round(bolt_capacity, 3)
        outputobj['Bolt']['CombinedCapacity'] = round(combined_capacity, 3)
        outputobj['Bolt']['NumberOfBolts'] = int(round(number_of_bolts, 3))
        outputobj['Bolt']['NumberOfRows'] = int(round(number_rows, 3))
        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = float(pitch_distance)
        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = float(pitch_distance_1_2)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
            outputobj['Bolt']['Pitch78'] = float(pitch_distance_7_8)
            outputobj['Bolt']['Pitch910'] = float(pitch_distance_9_10)

        outputobj['Bolt']['Gauge'] = float(minimum_gauge_distance)
        outputobj['Bolt']['CrossCentreGauge'] = float(g_1)
        outputobj['Bolt']['End'] = float(minimum_end_distance)
        outputobj['Bolt']['Edge'] = float(minimum_edge_distance)
        outputobj['Bolt']['Lv'] = float(l_v)

        outputobj['Plate'] = {}
        outputobj['Plate']['Height'] = round(end_plate_height_provided, 3)
        outputobj['Plate']['Width'] = round(end_plate_width_provided, 3)
        outputobj['Plate']['Thickness'] = round(end_plate_thickness, 3)
        outputobj['Plate']['MomentDemand'] = round(M_d, 3)
        outputobj['Plate']['MomentCapacity'] = round(M_c, 3)

        outputobj['Weld'] = {}
        outputobj['Weld']['CriticalStressflange'] = round(f_a_flange, 3)
        outputobj['Weld']['CriticalStressWeb'] = round(f_e, 3)

        outputobj['Stiffener'] = {}
        outputobj['Stiffener']['Height'] = round(h_st, 3)
        outputobj['Stiffener']['Length'] = round(l_st, 3)
        outputobj['Stiffener']['Thickness'] = int(round(thickness_stiffener_provided, 3))

    # Case 2: When the height of end plate is specified but the width is not specified by the user
    elif end_plate_height != 0 and end_plate_width == 0:
        outputobj = {}
        outputobj['Bolt'] = {}
        outputobj['Bolt']['status'] = design_status
        outputobj['Bolt']['CriticalTension'] = round(T_b, 3)
        outputobj['Bolt']['TensionCapacity'] = round(bolt_tension_capacity, 3)
        outputobj['Bolt']['ShearCapacity'] = round(bolt_shear_capacity, 3)
        outputobj['Bolt']['BearingCapacity'] = bearing_capacity
        outputobj['Bolt']['BoltCapacity'] = round(bolt_capacity, 3)
        outputobj['Bolt']['CombinedCapacity'] = round(combined_capacity, 3)
        outputobj['Bolt']['NumberOfBolts'] = int(round(number_of_bolts, 3))
        outputobj['Bolt']['NumberOfRows'] = int(round(number_rows, 3))
        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = float(pitch_distance)
        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = float(pitch_distance_1_2)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
            outputobj['Bolt']['Pitch78'] = float(pitch_distance_7_8)
            outputobj['Bolt']['Pitch910'] = float(pitch_distance_9_10)

        outputobj['Bolt']['Gauge'] = float(minimum_gauge_distance)
        outputobj['Bolt']['CrossCentreGauge'] = float(g_1)
        outputobj['Bolt']['End'] = float(minimum_end_distance)
        outputobj['Bolt']['Edge'] = float(minimum_edge_distance)

        outputobj['Plate'] = {}
        outputobj['Plate']['Height'] = round(end_plate_height_provided, 3)
        outputobj['Plate']['Width'] = round(end_plate_width_provided, 3)
        outputobj['Plate']['MomentDemand'] = round(M_d, 3)
        outputobj['Plate']['MomentCapacity'] = round(M_c, 3)

        outputobj['Weld'] = {}
        outputobj['Weld']['CriticalStressflange'] = round(f_a_flange, 3)
        outputobj['Weld']['CriticalStressWeb'] = round(f_e, 3)

        outputobj['Stiffener'] = {}
        outputobj['Stiffener']['Height'] = round(h_st, 3)
        outputobj['Stiffener']['Length'] = round(l_st, 3)
        outputobj['Stiffener']['Thickness'] = int(round(thickness_stiffener_provided, 3))

    # Case 3: When the height of end plate is not specified but the width is specified by the user
    elif end_plate_height == 0 and end_plate_width != 0:
        outputobj = {}
        outputobj['Bolt'] = {}
        outputobj['Bolt']['status'] = design_status
        outputobj['Bolt']['CriticalTension'] = round(T_b, 3)
        outputobj['Bolt']['TensionCapacity'] = round(bolt_tension_capacity, 3)
        outputobj['Bolt']['ShearCapacity'] = round(bolt_shear_capacity, 3)
        outputobj['Bolt']['BearingCapacity'] = bearing_capacity
        outputobj['Bolt']['BoltCapacity'] = round(bolt_capacity, 3)
        outputobj['Bolt']['CombinedCapacity'] = round(combined_capacity, 3)
        outputobj['Bolt']['NumberOfBolts'] = int(round(number_of_bolts, 3))
        outputobj['Bolt']['NumberOfRows'] = int(round(number_rows, 3))
        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = float(pitch_distance)
        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = float(pitch_distance_1_2)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
            outputobj['Bolt']['Pitch78'] = float(pitch_distance_7_8)
            outputobj['Bolt']['Pitch910'] = float(pitch_distance_9_10)

        outputobj['Bolt']['Gauge'] = float(minimum_gauge_distance)
        outputobj['Bolt']['CrossCentreGauge'] = float(g_1)
        outputobj['Bolt']['End'] = float(minimum_end_distance)
        outputobj['Bolt']['Edge'] = float(minimum_edge_distance)

        outputobj['Plate'] = {}
        outputobj['Plate']['Height'] = round(end_plate_height_provided, 3)
        outputobj['Plate']['Width'] = round(end_plate_width_provided, 3)
        outputobj['Plate']['MomentDemand'] = round(M_d, 3)
        outputobj['Plate']['MomentCapacity'] = round(M_c, 3)

        outputobj['Weld'] = {}
        outputobj['Weld']['CriticalStressflange'] = round(f_a_flange, 3)
        outputobj['Weld']['CriticalStressWeb'] = round(f_e, 3)

        outputobj['Stiffener'] = {}
        outputobj['Stiffener']['Height'] = round(h_st, 3)
        outputobj['Stiffener']['Length'] = round(l_st, 3)
        outputobj['Stiffener']['Thickness'] = int(round(thickness_stiffener_provided, 3))

    # Case 4: When the height and the width of End Plate is specified by the user
    elif end_plate_height != 0 and end_plate_width != 0:
        outputobj = {}
        outputobj['Bolt'] = {}
        outputobj['Bolt']['status'] = design_status
        outputobj['Bolt']['CriticalTension'] = round(T_b, 3)
        outputobj['Bolt']['TensionCapacity'] = round(bolt_tension_capacity, 3)
        outputobj['Bolt']['ShearCapacity'] = round(bolt_shear_capacity, 3)
        outputobj['Bolt']['BearingCapacity'] = bearing_capacity
        outputobj['Bolt']['BoltCapacity'] = round(bolt_capacity, 3)
        outputobj['Bolt']['CombinedCapacity'] = round(combined_capacity, 3)
        outputobj['Bolt']['NumberOfBolts'] = int(round(number_of_bolts, 3))
        outputobj['Bolt']['NumberOfRows'] = int(round(number_rows, 3))
        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = float(pitch_distance)
        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = float(pitch_distance_1_2)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
            outputobj['Bolt']['Pitch78'] = float(pitch_distance_7_8)
            outputobj['Bolt']['Pitch910'] = float(pitch_distance_9_10)

        outputobj['Bolt']['Gauge'] = float(minimum_gauge_distance)
        outputobj['Bolt']['CrossCentreGauge'] = float(g_1)
        outputobj['Bolt']['End'] = float(minimum_end_distance)
        outputobj['Bolt']['Edge'] = float(minimum_edge_distance)

        outputobj['Plate'] = {}
        outputobj['Plate']['Height'] = round(end_plate_height_provided, 3)
        outputobj['Plate']['Width'] = round(end_plate_width_provided, 3)
        outputobj['Plate']['MomentDemand'] = round(M_d, 3)
        outputobj['Plate']['MomentCapacity'] = round(M_c, 3)

        outputobj['Weld'] = {}
        outputobj['Weld']['CriticalStressflange'] = round(f_a_flange, 3)
        outputobj['Weld']['CriticalStressWeb'] = round(f_e, 3)

        outputobj['Stiffener'] = {}
        outputobj['Stiffener']['Height'] = round(h_st, 3)
        outputobj['Stiffener']['Length'] = round(l_st, 3)
        outputobj['Stiffener']['Thickness'] = int(round(thickness_stiffener_provided, 3))

    ###########################################################################
    # End of Output dictionary
    
    if design_status == True:
        logger.info(": Overall extended end plate connection design is safe \n")
        logger.debug(" :=========End Of design===========")
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")

    return outputobj