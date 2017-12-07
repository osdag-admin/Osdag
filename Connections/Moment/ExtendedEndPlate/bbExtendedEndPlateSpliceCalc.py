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

#Function for Shear Capacity of bearing bolt (also known as black bolt)
#Reference: Cl 10.3.3 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007
#Assumption: The shear planes are assumed to be passing through the threads of the bolt

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

#Function for Bearing Capacity of bearing bolt (also known as black bolt)
#Reference: Cl 10.3.4 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

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

    Returns: (float)- Minimum required height of extended end plate as per detailing requirements in mm

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
        n: (int)- Number of columns of bolt (assumed to be 2)
        min_gauge: (float)- minimum gauge distance i.e. 2.5*bolt_diameter
        e_2: (float)- minimum edge distance i.e. 1.7*bolt_hole_diameter

    Returns: (float)- Minimum required width of extended end plate as per detailing requirements in mm

    """
    min_end_plate_width = g_1 + (n - 2) * min_gauge + (2 * e_2)
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

    Returns: (float)- Prying force in bolt (in kN)

    """
    prying_force_bolt = (l_v / 2 * l_e) * (T_e - ((beta * eta * f_0 * b_e * t_p ** 4) / 27 * l_e * l_v ** 2))
    return prying_force_bolt

#######################################################################

#Function for calculating Tension capacity of HSFG bolt
#Reference: Cl 10.4.5 - Genereal Construction in Steel - Code of practice (3rd revision) IS 800:2007

def bolt_tension_hsfg(bolt_fu, netArea):
    """

    Args:
        bolt_fu: (float)- Ultimate tensile strength of a bolt
        netArea: (float)- Net tensile stress area as specified in IS 1367 (area at threads)

    Returns: (float)- Tension capacity of HSFG bolt in kN

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

    Returns: (float)- Tension capacity of Bearing bolt in kN

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

    Returns: (float)- Shear yielding capacity of End Plate in kN

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

    bolt_dia = int(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = float(uiObj['Bolt']['Grade'])

    mu_f = 0.30
    gamma_mw = 1.25
    dp_bolt_hole_type = "Standard"
    dia_hole = bolt_dia + 2
    weld_type = "Shop weld"
    dp_bolt_type = "HSFG"
    # mu_f = float(uiObj["bolt"]["slip_factor"])
    # gamma_mw = float(uiObj["weld"]["safety_factor"])
    # dp_bolt_hole_type = str(uiObj['bolt']['bolt_hole_type'])
    # dia_hole = int(uiObj['bolt']['bolt_hole_clrnce']) + bolt_dia
    # weld_type = uiObj['weld']['typeof_weld']
    # dp_bolt_type = uiObj['bolt']['bolt_type']

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

    # t_thinner is the thickness of the thinner plate(s) being connected
    t_thinner = end_plate_thickness

    # min_pitch & max_pitch = Minimum and Maximum pitch distance (mm) [Cl. 10.2.2, IS 800:2007]
    min_pitch = int(2.5 * bolt_dia)
    pitch_dist_min = min_pitch + (5 - min_pitch) % 5  # round off to nearest multiple of five

    max_pitch = int(min(32 * t_thinner, 300))
    pitch_dist_max = max_pitch + (5 - max_pitch) % 5  # round off to nearest multiple of five

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

    end_dist_mini = min_end_distance + (5 - min_end_distance) % 5  # round off to nearest multiple of five

    e = math.sqrt(250 / end_plate_fy)
    max_end_distance = 12 * end_plate_thickness * e

    end_dist_max = max_end_distance + (5 - max_end_distance) % 5  # round off to nearest multiple of five

    # min_edge_distance = Minimum edge distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    edge_dist_mini = end_dist_mini
    edge_dist_max = end_dist_max

    # l_v = Distance between the toe of weld or the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
    # TODO: Implement l_v depending on excomm review
    l_v = 50

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

    end_plate_width_mini = g_1 + (2 * edge_dist_mini)
    end_plate_width_max = max((beam_B + 25), end_plate_width_mini)

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
            # end_plate_height = end_plate_height_mini
            design_status = False
            logger.error(": Height of End Plate is less than/or equal to the depth of the Beam ")
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
            logger.error(": Height of End Plate exceeds the maximum allowed height")
            logger.warning(": Maximum allowed height of End Plate is %2.2f mm" % end_plate_height_max)
            logger.info(": Decrease the Height of End Plate")
    else:
        pass

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
    kb_1 = end_dist_mini / (3 * dia_hole)
    kb_2 = (pitch_dist_min / (3 * dia_hole)) - 0.25
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
    else:
        Vdsb = ConnectionCalculations.bolt_shear(bolt_dia, n_e, bolt_fu)      # 1. Check for Shear capacity of bearing bolt
        if l_j > 15 * bolt_dia:
            V_dsb = Vdsb * long_joint(bolt_dia, l_j)
        else:
            V_dsb = Vdsb
        Vdpb = ConnectionCalculations.bolt_bearing(bolt_dia, factor, sum_plate_thickness, k_b, plate_fu)  # 2. Check for Bearing capacity of bearing bolt
        # Capacity of bearing bolt (V_db) is minimum of V_dsb and Vdpb
        V_db = min(V_dsb, Vdpb)

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
    n = math.sqrt((6 * M_u) / (2 * pitch_dist_min * bolt_shear_capacity))
    n = math.ceil(n)

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
    # TODO : check the working of the below loop
    if number_of_bolts == 8:
        y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
        y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
        y3 = weld_thickness_flange + l_v + (beam_tf/2)
        y = (y1**2 + y2**2 + y3**2)
        T1 = (M_u * y1) / y  # Here, T1 is the tension in the topmost bolt (i.e. critical bolt) starting from the tension flange
        T2 = (M_u * y2) / y
        T3 = (M_u * y3) / y
        T_f = (T1 * (beam_d - beam_tf)) / y1

    elif number_of_bolts == 12:
        y1 = (beam_d - beam_tf/2) + weld_thickness_flange + l_v
        y2 = y1 - ((2 * l_v) + (2 * weld_thickness_flange) + beam_tf)
        y3 = y2 - min_pitch
        y4 = (beam_tf/2) + weld_thickness_flange + l_v + pitch_dist_min
        y5 = y4 - pitch_dist_min
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
        y3 = y2 - pitch_dist_min
        y4 = y3 - pitch_dist_min
        y5 = (beam_tf/2) + weld_thickness_flange + l_v + (2 * pitch_dist_min)
        y6 = y5 - pitch_dist_min
        y7 = y6 - pitch_dist_min
        y = (y1**2 + y2**2 + y3**2 + y4**2 + y5**2 + y6**2 + y7**2)
        T1 = (M_u * y1) / y
        T2 = (M_u * y2) / y
        T3 = (M_u * y3) / y
        T4 = (M_u * y4) / y
        T5 = (M_u * y5) / y
        T6 = (M_u * y6) / y
        T7 = (M_u * y7) / y
        T_f = (T1 * (beam_d - beam_tf)) / y1

    else:
        pass

    #######################################################################
    # Calculating actual required thickness of End Plate (tp_required) as per bending criteria
    b_e = beam_B / 2

    # M_p = Plastic moment capacity of end plate
    # TODO check if T_f value is getting assigned correctly
    tension_flange = T_f
    M_p = (tension_flange * l_v) / 2
    tp_required = math.sqrt((4 * 1.10 * M_p) / (end_plate_fy * b_e))
    tp_required = math.ceil(tp_required)

    if tp_required < end_plate_thickness:
        design_status = False
        logger.error(": Chosen end plate thickness in not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm" % tp_required)
        logger.info(": Increase end plate thickness")
    else:
        pass

    # Calculation of Prying Force at Tension flange
    # TODO : add condition of beta depending on bolt type
    if uiObj['bolt']['bolt_type'] == "pre-tensioned":
        beta = 1
    else:
        beta = 2

    eta = 1.5
    f_0 = 0.7 * bolt_fu
    l_e = min(end_dist_mini, 1.1 * tp_required * math.sqrt((beta * f_0) / bolt_fy))
    T_e = T_f
    t_p = tp_required

    Q = prying_force(T_e, l_v, l_e, beta, eta, f_0, b_e, t_p)
    Q = round(Q.real, 3)

    #######################################################################
    # Check for tension capacities of bolt

    Tdf_1 = (bolt_fy * netarea_shank(bolt_dia) * (1.25/1.10))  # Here, Tdf_1 is the maximum allowed tension capacity of bolt (Cl 10.4.5, IS 800:2007 )

    if bolt_type == "HSFG":
        Tdf = bolt_tension_hsfg(bolt_fu, netArea_thread(bolt_dia))

        if Tdf > Tdf_1:
            design_status = False
            logger.error(": Tension capacity of HSFG bolt exceeds the specified limit (Clause 10.4.5, IS 800:2007)")
            logger.warning(": Maximum allowed tension capacity for selected diameter of bolt is %2.2f kN" % Tdf_1)
            logger.info(": Re-design the connection using bolt of smaller diameter")
    else:
        Tdb = bolt_tension_bearing(bolt_fu, netArea_thread(bolt_dia))

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

    Vsf = factored_shear_load / number_of_bolts
    Vdf = V_dsf
    Tf = T_b

    Vsb = Vsf
    Vdb = V_db
    Tb = T_b

    if bolt_type == "HSFG":
        combined_capacity_hsfg = (Vsf / Vdf) ** 2 + (Tf / Tdf) ** 2

        if combined_capacity_hsfg > 1.0:
            design_status = False
            logger.error(": Load due to combined shear and tension on selected HSFG bolt exceeds the limiting value (Clause 10.4.6, IS 800:2007)")
            logger.warning(": The maximum allowable value is 1.0")
            logger.info(": Re-design the connection using bolt of higher diameter or grade")
    else:
        combined_capacity_bearing = (Vsb / Vdb) ** 2 + (Tb / Tdb) ** 2

        if combined_capacity_bearing > 1.0:
            design_status = False
            logger.error(": Load due to combined shear and tension on selected Bearing bolt exceeds the limiting value (Clause 10.3.6, IS 800:2007)")
            logger.warning(": The maximum allowable value is 1.0")
            logger.info(": Re-design the connection using bolt of higher diameter or grade")

    #######################################################################
    # Check for Shear yielding and shear rupture of end plate

    # 1. Shear yielding of end plate (Clause 8.4.1, IS 800:2007)
    A_v = end_plate_width * end_plate_thickness  # gross shear area of end plate
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
    force_flange = M_u / (beam_d - beam_tf)

    if capacity_beam_flange < force_flange:
        design_status = False
        logger.error(": Force in the flange is greater than its load carrying capacity")
        logger.warning(": The maximum allowable force on beam flange of selected section is %2.2f kN" % capacity_beam_flange)
        logger.info(": Use a higher beam section with wider and/or thicker flange")

    #######################################################################
    # Design of Weld
    # Assumption: The size of weld at flange will be greater than the size of weld at the web
    # Weld at flange resists bending moment whereas the weld at web resists shear + axial load

    # Ultimate and yield strength of welding material is assumed as Fe410 (E41 electrode) (Reference: Design of Steel structures by Dr. N. Subramanian)
    # TODO add condition to retrieve weld fu and fy from design preference
    weld_fu = 410  # Mpa
    weld_fy = 250  # Mpa

    # Minimum weld thickness (mm)
    # Minimum weld thickness at flange (for drop-down list)
    # Minimum weld thickness (tw_minimum) depends on the thickness of the thicker part (Table 21, IS 800:2007)

    t_thicker = max(beam_tf, beam_tw, tp_required)

    if t_thicker <= 10:
        tw_minimum = 3
    elif t_thicker > 10 or t_thicker <= 20:
        tw_minimum = 5
    elif t_thicker > 20 or t_thicker <= 32:
        tw_minimum = 6
    elif t_thicker > 32 or t_thicker <= 50:
        tw_minimum = 8

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
    BS_flange = M_u / Z

    # Resultant (R)
    R = math.sqrt(DS_flange ** 2 + BS_flange ** 2)

    # Actual required size of weld
    t_weld_flange = math.ceil(R / capacity_unit_flange)  # mm

    if t_weld_flange % 2 == 0:
        t_weld_flange = t_weld_flange
    else:
        t_weld_flange += 1

    if weld_thickness_flange < t_weld_flange:
        design_status = False
        logger.error(": Weld thickness at the flange is not sufficient")
        logger.warning(": Minimum weld thickness required is %2.2f mm " % t_weld_flange)
        logger.info(": Increase the weld thickness")

    # Design of weld at web
    t_weld_web = math.ceil(min(beam_tw, tp_required))

    if t_weld_web % 2 == 0:
        t_weld_web = t_weld_web
    else:
        t_weld_web += 1

    if weld_thickness_web < t_weld_web:
        design_status = False
        logger.error(": Weld thickness at the web is not sufficient")
        logger.warning(": Minimum weld thickness required is %2.2f mm" % t_weld_web)
        logger.info(": Increase the weld thickness")

    #######################################################################
    # Weld Checks
    # Check for stresses in weld due to individual force (Clause 10.5.9, IS 800:2007)

    # Weld at flange
    # 1. Check for normal stress

    f_a_flange = force_flange / (3 * L_effective_flange)  # Here, 3 mm is the effective minimum throat thickness

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
    f_a_web = factored_axial_load / (3 * L_effective_web)

    # 2. Check for shear stress
    q_web = factored_shear_load / (3 * L_effective_web)

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
    h_st = (end_plate_height - beam_d) / 2

    # Length of stiffener
    cf = math.pi/180  # conversion factor to convert degree into radian
    l_st = ((h_st - 25) / math.tan(30 * cf)) + 25

    # Thickness of stiffener
    ts1 = beam_tw
    ts2 = (beam_fy / stiffener_fy) * beam_tw
    thickness_stiffener = math.ceil(max(ts1, ts2))

    # Check of stiffener against local buckling
    E = 2 * 10 ** 5  # MPa
    ts_required = 1.79 * h_st * stiffener_fy / E  # mm

    if thickness_stiffener < ts_required:
        design_status = False
        logger.error(": The thickness of stiffener is not sufficient")
        logger.error(": The stiffener might buckle locally (AISC Design guide 16)")
        logger.warning(": Minimum required thickness of stiffener to prevent local bucklimg is % 2.2f mm" % ts_required)
        logger.info(": Increase the thickness of stiffener")








