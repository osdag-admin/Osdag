"""
Started on 22nd April, 2019.

@author: ajmalbabums


Module: Beam to column end plate moment connection

Reference:
            1) IS 800: 2007 General construction in steel - Code of practice (Third revision)
            2) Design of Steel structures by Dr. N Subramanian (chapter 5 and 6)
            3) Fundamentals of Structural steel design by M.L Gambhir
            4) AISC Design guide 16 and 4


ASCII diagram


"""

from model import *
from Connections.connection_calculations import ConnectionCalculations
from utilities.is800_2007 import IS800_2007
from utilities.other_standards import IS1363_part_1_2002, IS1363_part_3_2002, IS1367_Part3_2002
from utilities.common_calculation import *
import math
import logging
flag = 1
logger = None


def module_setup():
    global logger
    logger = logging.getLogger("osdag.bc_endplate_calc")


module_setup()

#######################################################################
# Defining functions
#######################################################################


# Function for net area of bolts at threaded portion of bolts
# Reference: Design of steel structures by N. Subramanian, page 348 or 358


def netArea_thread(dia):
    """

    Args:
        dia: (int)- diameter of bolt (Friction Grip Bolt/Bearing bolt)

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
        dia: (int) -  diameter of bolt (Friction Grip Bolt/Bearing bolt)

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
# Start of Main Program

def bc_endplate_design(uiObj):
    global logger
    global design_status
    design_status = True

    conn_type = uiObj['Member']['Connectivity']
    if conn_type == "Extended both ways":
        connectivity = "both_way"
    else:   #TODO : elif for one way and flush
        connectivity = "one_way"
        connectivity = "flush"

    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumnSection']
    beam_fu = float(uiObj['Member']['fu (MPa)'])
    beam_fy = float(uiObj['Member']['fy (MPa)'])
    column_fu = float(uiObj['Member']['fu (MPa)'])
    column_fy = float(uiObj['Member']['fy (MPa)'])
    weld_fu = float(uiObj['weld']['fu_overwrite'])
    weld_fu_govern = min(beam_fu, weld_fu)  # Mpa  (weld_fu_govern is the governing value of weld strength)

    factored_moment = float(uiObj['Load']['Moment (kNm)'])
    factored_shear_load = float(uiObj['Load']['ShearForce (kN)'])
    factored_axial_load = uiObj['Load']['AxialForce (kN)']
    if factored_axial_load == '':
        factored_axial_load = 0
    else:
        factored_axial_load = float(factored_axial_load)

    bolt_dia = int(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = float(uiObj['Bolt']['Grade'])
    bolt_fu = uiObj["bolt"]["bolt_fu"]
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu
    mu_f = float(uiObj["bolt"]["slip_factor"])
    gamma_mw = float(uiObj["weld"]["safety_factor"])
    dp_bolt_hole_type = uiObj["bolt"]["bolt_hole_type"]
    if dp_bolt_hole_type == "Over-sized":
        bolt_hole_type = 'over_size'
    else:
        bolt_hole_type = 'standard'

    dia_hole = bolt_dia + int(uiObj["bolt"]["bolt_hole_clrnce"])

    end_plate_thickness = float(uiObj['Plate']['Thickness (mm)'])

    # TODO implement after excomm review for different grades of plate
    end_plate_fu = float(uiObj['Member']['fu (MPa)'])
    end_plate_fy = float(uiObj['Member']['fy (MPa)'])

    weld_thickness_flange = float(uiObj['Weld']['Flange (mm)'])
    weld_thickness_web = float(uiObj['Weld']['Web (mm)'])

    if uiObj["detailing"]["typeof_edge"] == "a - Sheared or hand flame cut":
        edge_type = 'hand_flame_cut'
    else:
        edge_type = 'machine_flame_cut'
    corrosive_influences = False
    if uiObj['detailing']['is_env_corrosive'] == "Yes":
        corrosive_influences = True

    [bolt_shank_area, bolt_net_area] = IS1367_Part3_2002.bolt_area(bolt_dia)

    old_beam_section = get_oldbeamcombolist()
    old_column_section = get_oldcolumncombolist()

    if beam_sec in old_beam_section or column_sec in old_column_section:
        logger.warning(": You are using a section (in red colour) that is not available in the latest version of IS 808")

    if beam_fu < 410 or beam_fy < 230 or column_fu < 410 or column_fy < 230:
        logger.warning(" : You are using a section of grade that is not available in the latest version of IS 2062")

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
    # Read input values from column database
    # Here,
    #    column_tw - Thickness of column web
    #    column_tf - Thickness of column Flange
    #    column_d  - Depth of column
    #    column_B  - Width of column Flange
    #    column_R1 - Radius of column at root

    dictcolumndata = get_columndata(column_sec)

    column_tw = float(dictcolumndata["tw"])
    column_tf = float(dictcolumndata["T"])
    column_d = float(dictcolumndata["D"])
    column_B = float(dictcolumndata["B"])
    column_R1 = float(dictcolumndata["R1"])

    bolt_plates_tk = [column_tf, end_plate_thickness]

    #######################################################################
    # Calculation of Spacing (Min values rounded to next multiple of 5)

    # t_thinner is the thickness of the thinner plate(s) being bolted
    t_thinner = min(bolt_plates_tk)

    # min_pitch & max_pitch = Minimum and Maximum pitch distance (mm)
    pitch_dist_min = IS800_2007.cl_10_2_2_min_spacing(bolt_dia)
    pitch_dist_max = IS800_2007.cl_10_2_3_1_max_spacing(bolt_plates_tk)
    pitch_dist = round_up(pitch_dist_min, multiplier=5)

    # min_gauge & max_gauge = Minimum and Maximum gauge distance (mm) [Cl. 10.2.3.1, IS 800:2007]
    gauge_dist_min = pitch_dist_min
    gauge_dist_max = pitch_dist_max

    # min_end_distance & max_end_distance = Minimum and Maximum end distance
    #       [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]

    end_dist_min = IS800_2007.cl_10_2_4_2_min_edge_end_dist(d=bolt_dia, bolt_hole_type=bolt_hole_type,
                                                                      edge_type=edge_type)
    end_dist_max = IS800_2007.cl_10_2_4_3_max_edge_dist(plate_thicknesses=bolt_plates_tk, f_y=end_plate_fy,
                                                        corrosive_influences=corrosive_influences)
    end_dist = round_up(end_dist_min, multiplier=5)

    # min_edge_distance = Minimum edge distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    edge_dist_min = end_dist_min
    edge_dist_max = end_dist_max
    edge_dist = edge_dist_min

    #######################################################################
    # l_v = Distance between the toe of weld or the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
    # TODO: Implement l_v depending on excomm review
    l_v = float(50.0)
    flange_projection = 5

    # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge) (Steel designers manual, page 733, 6th edition - 2003)
    # TODO validate g_1 with correct value
    # g_1 = max(90, (l_v + edge_dist_mini))
    g_1 = 100.0


    #######################################################################
    # Calculate bolt capacities

    if bolt_type == "Friction Grip Bolt":
        bolt_shear_capacity = IS800_2007.cl_10_4_3_bolt_slip_resistance(f_ub=bolt_fu, A_nb=bolt_net_area, n_e=1,
                                                                        mu_f=mu_f, bolt_hole_type=bolt_hole_type)
        bolt_tension_capacity = IS800_2007.cl_10_4_5_friction_bolt_tension_resistance(f_ub=bolt_fu,
                                                                                      f_yb=bolt_fy,
                                                                                      A_sb=bolt_shank_area,
                                                                                      A_n=bolt_net_area)
        bearing_capacity = "N/A"
        bolt_capacity = bolt_shear_capacity

    else:
        bolt_shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(f_u=bolt_fu, A_nb=bolt_net_area,
                                                                       A_sb=bolt_shank_area, n_n=1, n_s=0)
        bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(f_u=min(column_fu, end_plate_fu),
                                                                      f_ub=bolt_fu, t=sum(bolt_plates_tk),
                                                                      d=bolt_dia, e=edge_dist, p=pitch_dist,
                                                                      bolt_hole_type=bolt_hole_type)
        bolt_capacity = min(bolt_shear_capacity, bearing_capacity)
        bolt_tension_capacity = IS800_2007.cl_10_3_5_bearing_bolt_tension_resistance(f_ub=bolt_fu,
                                                                                     f_yb=bolt_fy,
                                                                                     A_sb=bolt_shank_area,
                                                                                     A_n=bolt_net_area)

    #######################################################################

    # Calculation for number of bolts around tension flange
    flange_tension = factored_moment / (beam_d - beam_tf) + factored_axial_load / 2
    no_tension_side_rqd = flange_tension / (0.80 * bolt_tension_capacity)
    no_tension_side = round_up(no_tension_side_rqd, multiplier=2, minimum_value=4)
    number_of_bolts = 2 * no_tension_side

    # Prying force
    b_e = beam_B
    prying_force = IS800_2007.cl_10_4_7_bolt_prying_force(T_e=flange_tension/2, l_v=l_v, f_o=0.7*bolt_fu,
                                                          b_e=b_e, t=end_plate_thickness, f_y=end_plate_fy,
                                                          end_dist=end_dist, pre_tensioned=False)
    toe_of_weld_moment = flange_tension/2 * l_v - prying_force * end_dist
    plate_tk_min = math.sqrt(toe_of_weld_moment * 1.10 * 4 / (end_plate_fy * b_e))

    # End Plate Thickness
    # TODO : Is this condition for the main file? EP thickness depends on the plastic capacity of plate
    if end_plate_thickness < max(column_tf, plate_tk_min):
        end_plate_thickness = math.ceil(max(column_tf, plate_tk_min))
        design_status = False
        logger.error(": Chosen end plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm " % end_plate_thickness)
        logger.info(": Increase the thickness of end plate ")

    # Detailing
    bolt_combined_status = False
    while bolt_combined_status is False:
        if connectivity == "both_way":

            if no_tension_side == 4:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
                           'out_compression_flange': 1, 'in_compression_flange': 1}

            elif no_tension_side == 6:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                           'out_compression_flange': 1, 'in_compression_flange': 2}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                               'out_compression_flange': 2, 'in_compression_flange': 1}

            elif no_tension_side == 8:
                no_rows = {'out_tension_flange': 2, 'in_tension_flange': 2,
                           'out_compression_flange': 2, 'in_compression_flange': 2}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                               'out_compression_flange': 3, 'in_compression_flange': 1}
            elif no_tension_side == 10:
                no_rows = {'out_tension_flange': 3, 'in_tension_flange': 2,
                           'out_compression_flange': 3, 'in_compression_flange': 2}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    design_status = False

            else:
                design_status = False
                # logger.error(
                #     ": Detailing Error - Pitch distance is greater than the maximum allowed value (Clause 10.2.3, IS 800:2007)")
                # logger.warning(": Maximum allowed Pitch distance is % 2.2f mm" % pitch_dist_max)
                logger.info(": Re-design the connection using bolt of higher grade or diameter")
                no_rows = {'out_tension_flange': (no_tension_side-4)/2, 'in_tension_flange': 2,
                           'out_compression_flange': (no_tension_side-4)/2, 'in_compression_flange': 2}

            # #######################################################################

        # Plate height and width
        if no_rows['out_tension_flange'] == 0:
            tens_plate_no_pitch = flange_projection
        else:
            tens_plate_no_pitch = end_dist + l_v
        if no_rows['out_compression_flange'] == 0:
            comp_plate_no_pitch = flange_projection
        else:
            comp_plate_no_pitch = end_dist + l_v

        plate_height = (no_rows['out_tension_flange'] + no_rows['out_compression_flange'] - 2) * pitch_dist + \
                       comp_plate_no_pitch + tens_plate_no_pitch
        plate_width = g_1 + 2 * edge_dist
        while plate_width < beam_B:
            edge_dist += 5
            plate_width = g_1 + 2 * edge_dist

        # Tension in bolts
        axial_tension = factored_axial_load / number_of_bolts
        if no_rows['out_tension_flange'] == 0:
            extreme_bolt_dist = beam_d - beam_tf * 3/2 - l_v
        else:
            extreme_bolt_dist = beam_d - beam_tf/2 + l_v + (no_rows['out_tension_flange']-1) * pitch_dist
        sigma_yi_sq = 0
        for bolt_row in range(no_rows['out_tension_flange']):
            sigma_yi_sq += (beam_d - beam_tf/2 + l_v + bolt_row * pitch_dist) ** 2
        for bolt_row in range(no_rows['out_compression_flange']):
            sigma_yi_sq += (beam_d - 3 * beam_tf/2 - l_v - bolt_row * pitch_dist) ** 2

        moment_tension = factored_moment * extreme_bolt_dist / sigma_yi_sq
        tension_in_bolt = axial_tension + moment_tension + prying_force
        shear_in_bolt = factored_shear_load / number_of_bolts
        # Check for combined tension and shear
        if bolt_type == "Friction Grip Bolt":
            bolt_combined_status = IS800_2007.cl_10_4_6_friction_bolt_combined_shear_and_tension(V_sf=shear_in_bolt,
                                                                                            V_df=bolt_capacity,
                                                                                            T_f=tension_in_bolt,
                                                                                            T_df=bolt_tension_capacity)
        else:
            bolt_combined_status = IS800_2007.cl_10_3_6_bearing_bolt_combined_shear_and_tension(V_sb=shear_in_bolt,
                                                                                            V_db=bolt_capacity,
                                                                                            T_b=tension_in_bolt,
                                                                                            T_db=bolt_tension_capacity)

        if bolt_combined_status is False:
            no_tension_side += 2
            number_of_bolts = 2 * no_tension_side




    #######################################################################
    # TODO Check for Shear yielding and shear rupture of end plate
    '''

    # 1. Shear yielding of end plate (Clause 8.4.1, IS 800:2007)
    A_v = plate_width * end_plate_thickness  # gross shear area of end plate
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

    # Minimum weld size (mm)
    # Minimum weld size at flange (for drop-down list)
    # Minimum weld size (tw_minimum) depends on the thickness of the thicker part (Table 21, IS 800:2007)

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

    if weld_thickness_flange < tw_minimum:
        design_status = False
        logger.error(": Selected weld size at flange is less than the minimum required value")
        logger.warning(": Minimum weld size required at flange (as per Table 21, IS 800:2007) is %2.2f mm " % tw_minimum)
        logger.info(": Increase the weld size at flange")

    if weld_thickness_web < tw_minimum:
        design_status = False
        logger.error(": Selected weld size at web is less than the minimum required value")
        logger.warning(": Minimum weld size required at web (as per Table 21, IS 800:2007) is %2.2f mm " % tw_minimum)
        logger.info(": Increase the weld size at web")


    # Design of weld at flange
    # Capacity of unit weld (Clause 10.5.7, IS 800:2007)
    k = 0.7  # constant (Table 22, IS 800:2007)

    # capacity_unit_flange is the capacity of weld of unit throat thickness
    capacity_unit_flange = (k * weld_fu_govern) / (math.sqrt(3) * gamma_mw)  # N/mm**2 or MPa

    # Calculating th effective length of weld at the flange
    L_effective_flange = 2 * ((2 * beam_B) + (2 * (beam_B - beam_tw)) + (4 * beam_tf)) + (2 * weld_thickness_flange)  # mm

    # Calculating the area of weld at flange (a_weld_flange) assuming minimum throat thickness i.e. 3mm (Clause 10.5.3, IS 800:2007)
    a_weld_flange = L_effective_flange * 3  # mm**2

    # Calculating stresses on weld
    # Assumption: The weld at flanges are designed to carry Factored external moment and moment due to axial load,
    # whereas, the weld at beam web are designed to resist factored shear force and axial loads

    # 1. Direct stress (DS)

    # Since there is no direct stress (DS_flange) acting on weld at flange, the value of direct stress will be zero
    DS_flange = 0

    # 2. Bending Stress (BS)
    # Finding section modulus i.e. Z = Izz / y (Reference: Table 6.7, Design of Steel structures by Dr. N. Subramanian)
    Z = (beam_B * beam_d) + (beam_d ** 2 / 3)  # mm **3
    BS_flange = M_u * 10 ** 3 / Z

    # Resultant (R)
    R = math.sqrt(DS_flange ** 2 + BS_flange ** 2)

    # Actual required size of weld
    t_weld_flange_actual = math.ceil((R * 10 ** 3) / capacity_unit_flange)  # mm

    if t_weld_flange_actual % 2 == 0:
        t_weld_flange = t_weld_flange_actual
    else:
        t_weld_flange = t_weld_flange_actual + 1

    if weld_thickness_flange < t_weld_flange:
        design_status = False
        logger.error(": Weld size at the flange is not sufficient")
        logger.warning(": Minimum weld size required is %2.2f mm " % t_weld_flange_actual)
        logger.info(": Increase the weld size at flange")
    if weld_thickness_flange > min(beam_tf, end_plate_thickness):
        design_status = False
        logger.error(": Weld size at the flange exceeds the maximum allowed value")
        logger.warning(": Maximum allowed weld size at the flange is %2.2f mm" % min(beam_tf, end_plate_thickness))
        logger.info(": Decrease the weld size at flange")

    # Design of weld at web

    t_weld_web = int(min(beam_tw, end_plate_thickness))

    if t_weld_web % 2 == 0:
        t_weld_web = t_weld_web
    else:
        t_weld_web -= 1

    if t_weld_web > t_weld_flange:
        t_weld_web = t_weld_flange
    else:
        t_weld_web = t_weld_web

    if weld_thickness_web < t_weld_web:
        design_status = False
        logger.error(": Weld size at the web is not sufficient")
        logger.warning(": Minimum weld size required is %2.2f mm" % t_weld_web)
        logger.info(": Increase the weld size at web")
    if weld_thickness_web > int(min(beam_tw, end_plate_thickness)):
        design_status = False
        logger.error(": Weld size at the web exceeds the maximum allowed value")
        logger.warning(": Maximum allowed weld size at the web is %2.2f mm" % int(min(beam_tw, end_plate_thickness)))
        logger.info(": Decrease the weld size at web")

    #######################################################################
    # Weld Checks
    # Check for stresses in weld due to individual force (Clause 10.5.9, IS 800:2007)

    # Weld at flange
    # 1. Check for normal stress

    f_a_flange = force_flange * 10 ** 3 / (3 * L_effective_flange)  # Here, 3 mm is the effective minimum throat thickness

    # Design strength of fillet weld (Clause 10.5.7.1.1, IS 800:2007)
    f_wd = weld_fu_govern / (math.sqrt(3) * 1.25)
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

    f_e = math.sqrt(f_a_web ** 2 + (3 * q_web ** 2))

    if f_e > f_wd:
        design_status = False
        logger.error(": The stress in weld at web exceeds the limiting value (Clause 10.5.10.1.1, IS 800:2007)")
        logger.warning(": Maximum stress weld can carry is %2.2f N/mm^2" % f_wd)
        logger.info(": Increase the Ultimate strength of weld and/or length of weld")
    
    '''

    #######################################################################
    # Design of Stiffener

    # TODO: add material strengths for below condition (design preference?)
    stiffener_fy = end_plate_fy
    stiffener_fu = end_plate_fu


########################################################################################################################
    # End of Calculation
    # Output dictionary for different cases
        # Case 1: When the height and the width of end plate is not specified by user
    if connectivity == "both_way":
        outputobj = {}
        outputobj['Bolt'] = {}
        outputobj['Bolt']['status'] = design_status
        # outputobj['Bolt']['CriticalTension'] = round(T_b, 3)
        # outputobj['Bolt']['TensionCapacity'] = round(bolt_tension_capacity, 3)
        # outputobj['Bolt']['ShearCapacity'] = round(bolt_shear_capacity, 3)
        # outputobj['Bolt']['BearingCapacity'] = bearing_capacity
        # outputobj['Bolt']['BoltCapacity'] = round(bolt_capacity, 3)
        # outputobj['Bolt']['CombinedCapacity'] = round(combined_capacity, 3)
        # outputobj['Bolt']['NumberOfBolts'] = int(number_of_bolts)
        # outputobj['Bolt']['NumberOfRows'] = int(round(number_rows, 3))
        # outputobj['Bolt']['BoltsPerColumn'] = int(n_c)
        # outputobj['Bolt']['kb'] = float(round(k_b, 3))
        # outputobj['Bolt']['SumPlateThick'] = float(round(sum_plate_thickness, 3))
        # outputobj['Bolt']['BoltFy'] = bolt_fy
        # outputobj['Bolt']['PryingForce'] = round(prying_force, 3)
        # outputobj['Bolt']['TensionCritical'] = round(T1, 3)  # Tension in critical bolt required for report generator
        outputobj['Bolt']['Gauge'] = float(gauge_dist_min)
        outputobj['Bolt']['CrossCentreGauge'] = float(g_1)
        outputobj['Bolt']['End'] = float(end_dist)
        outputobj['Bolt']['Edge'] = float(edge_dist)
        outputobj['Bolt']['Lv'] = float(l_v)
        outputobj['Bolt']['PitchMini'] = pitch_dist_min
        outputobj['Bolt']['PitchMax'] = pitch_dist_max
        outputobj['Bolt']['EndMax'] = end_dist_max
        outputobj['Bolt']['EndMini'] = end_dist
        outputobj['Bolt']['DiaHole'] = int(dia_hole)
        #
        # if bolt_type == "Friction Grip Bolt":
        #     outputobj['Bolt']['Vsf'] = float(round(Vsf, 3))
        #     outputobj['Bolt']['Vdf'] = float(round(Vdf, 3))
        #     outputobj['Bolt']['Tf'] = float(round(Tf, 3))
        #     outputobj['Bolt']['Tdf'] = float(round(Tdf, 3))
        # else:
        #     outputobj['Bolt']['Vsb'] = float(round(Vsb, 3))
        #     outputobj['Bolt']['Vdb'] = float(round(Vdb, 3))
        #     outputobj['Bolt']['Tb'] = float(round(Tb, 3))
        #     outputobj['Bolt']['Tdb'] = float(round(Tdb, 3))



        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = round(pitch_dist, 3)
        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch23'] = pitch_dist
            outputobj['Bolt']['Pitch34'] = beam_d - 2 * (beam_tf + l_v + pitch_dist)
            outputobj['Bolt']['Pitch45'] = pitch_dist
        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch23'] = float(pitch_distance_2_3)
            outputobj['Bolt']['Pitch34'] = float(pitch_distance_3_4)
            outputobj['Bolt']['Pitch45'] = float(pitch_distance_4_5)
            outputobj['Bolt']['Pitch56'] = float(pitch_distance_5_6)
            outputobj['Bolt']['Pitch67'] = float(pitch_distance_6_7)
        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = 0.0
            outputobj['Bolt']['Pitch34'] = 0.0
            outputobj['Bolt']['Pitch45'] = 0.0
            outputobj['Bolt']['Pitch56'] = 0.0
            outputobj['Bolt']['Pitch67'] = 0.0
            outputobj['Bolt']['Pitch78'] = 0.0
            outputobj['Bolt']['Pitch910'] = 0.0

        outputobj['Plate'] = {}
        outputobj['Plate']['Height'] = float(round(plate_height, 3))
        outputobj['Plate']['Width'] = float(round(plate_width, 3))
        outputobj['Plate']['Thickness'] = float(round(end_plate_thickness, 3))
        # # ===================  CAD ===================
        # outputobj['Plate']['MomentDemand'] = round(M_d, 3)
        # outputobj['Plate']['MomentCapacity'] = round(M_c, 3)
        #
        # outputobj['Plate']['ThickRequired'] = float(round(tp_required, 3))
        # outputobj['Plate']['Mp'] = float(round(M_p, 3))

        # outputobj['Weld'] = {}
        # outputobj['Weld']['CriticalStressflange'] = round(f_a_flange, 3)
        # outputobj['Weld']['CriticalStressWeb'] = round(f_e, 3)
        # outputobj['Weld']['WeldStrength'] = round(f_wd, 3)
        # outputobj['Weld']['ForceFlange'] = float(round(force_flange, 3))
        # outputobj['Weld']['LeffectiveFlange'] = float(L_effective_flange)
        # outputobj['Weld']['LeffectiveWeb'] = float(L_effective_web)
        #
        # outputobj['Weld']['FaWeb'] = float(round(f_a_web, 3))
        # outputobj['Weld']['Qweb'] = float(round(q_web, 3))
        # outputobj['Weld']['Resultant'] = float(round(R, 3))
        # outputobj['Weld']['UnitCapacity'] = float(round(capacity_unit_flange, 3))
        # outputobj['Weld']['WeldFuGovern'] = float(weld_fu_govern)

        # outputobj['Stiffener'] = {}
        # outputobj['Stiffener']['Height'] = round(h_st, 3)
        # outputobj['Stiffener']['Length'] = round(l_st, 3)
        # outputobj['Stiffener']['Thickness'] = int(round(thickness_stiffener_provided, 3))

    ###########################################################################
    # End of Output dictionary
    
    if design_status == True:
        logger.info(": Overall extended end plate connection design is safe \n")
        logger.debug(" :=========End Of design===========")
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")

    return outputobj

