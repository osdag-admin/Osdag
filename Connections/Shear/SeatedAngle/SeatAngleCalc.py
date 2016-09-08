
'''
Created on 2-Sept-2016
@author: jayant patil
'''

''' 
References:

Design of Steel Structures (DoSS) - N. Subramanian
First published 2008, 14th impression 2014
    Chapter 5: Bolted Connections
    Example 5.14, Page 406

IS 800: 2007
    General construction in steel - Code of practice (Third revision)
'''

'''
ASCII diagram

            +-+-------------+-+   +-------------------------+
            | |             | |   |-------------------------|
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |                         |
            | |             | |   |-------------------------|
            | |             | |   +-------------------------+
            | |             | |+-----------+
            | |             | || +---------+
            | |             | || |
            | |         +---|-||-|---+
            | |         +---|-||-|---+
            | |             | || |
            | |         +---|-||-|---+
            | |         +---|-||-|---+
            | |             | ||_|
            | |             | |
            | |             | |
            +-+-------------+-+

'''


import math
import logging
import model

from PyQt4.Qt import QString

logger = logging.getLogger("osdag.SeatAngleCalc")

'''

List of assumptions:
Bolts:
# for all bolts, shear plane passes through threaded area
# for all bolts, tensile stress area equals the threaded area

'''


# Bolt calculations
# Bolt factored shear capacity = f_u * number_of_bolts * Area_bolt_net_tensile / (square_root(3) * gamma_mb)
# IS 800, Cl 10.3.3
# Reduction factors for long joints, large grip lengths, and packing plates
def bolt_shear(bolt_diameter, number_of_bolts, f_u):
    gamma_mb = 1.25 # partial safety factor for bolt
    # assumption: for all bolts, shear plane passes through threaded area
    # assumption: for all bolts, tensile stress area equals the threaded area
    # values for tensile stress area (mm^2) from Table 5.9 DoSS - N. Subramanian
    # TODO area of bolts for lower diameters
        # 5, 6, 8, 10 - either omit these from inputs or add to below dictionary
    bolt_area = {
        '12': 84.3,
        '16': 157,
        '20': 245,
        '22': 303,
        '24': 353,
        '27': 459,
        '30': 561,
        '36': 817
    }[str(bolt_diameter)]
    # bolt_area_approx = math.pi * bolt_diameter * bolt_diameter * 0.25 * 0.78
    bolt_nominal_shear_capacity = f_u * number_of_bolts * bolt_area / math.sqrt(3)/ 1000
    return round(bolt_nominal_shear_capacity /gamma_mb, 3)


# Bolt factored bearing capacity = 2.5 * k_b * bolt_diameter * sum_thickness_of_connecting_plates * f_u / gamma_mb
# IS 800, Cl 10.3.4
def bolt_bearing(bolt_diameter, thickness_plate, f_u):
    # currently assuming k_b = 0.5
    # TODO calculate k_b
    # given pitch, gauge, edge distance
    k_b = 0.5
    bolt_nominal_bearing_capacity = 2.5 * k_b * bolt_diameter * thickness_plate * f_u / (1000)
    return round(bolt_nominal_bearing_capacity / 1.25, 3)


# TODO check code block for min ply thk
#  ***********************************************
# # Minimum thickness of ply for bolt bearing = Vnpb/(d*vnpb)
# # vnpb = bearing capacity = 2.5 * kb * d * t * fu / Y
# # Vnpb=
# # ***********************************************
# def ply_min_thickness(shear, f_y, thk):
#     min_ply_thickness = 5 * shear * 1000 / (fy * thk);
#     return min_ply_thickness;


def SeatAngleConn(inputObj):

    connectivity = inputObj['Member']['Connectivity']
    beam_section = inputObj['Member']['BeamSection']
    column_section = inputObj['Member']['ColumnSection']
    beam_fu = inputObj['Member']['fu (MPa)']
    beam_fy = inputObj['Member']['fy (MPa)']

    shear_force = inputObj['Load']['ShearForce (kN)']

    bolt_diameter = inputObj['Bolt']['Diameter (mm)']
    bolt_type = inputObj['Bolt']['Type']
    bolt_grade = inputObj['Bolt']['Grade']
    # bolt_planes = 1

    # angle_sec = 'ISA 15075'
    # TODO rework angle section name
    angle_sec = inputObj['Angle']["AngleSection"]
    # angle_t = 12

    dict_beam_data = model.get_beamdata(beam_section)
    beam_w_t = float(dict_beam_data[QString("tw")]) # beam web thickness
    beam_f_t = float(dict_beam_data[QString("T")]) # beam flange thickness
    beam_d = float(dict_beam_data[QString("D")]) # beam depth
    beam_w_f = float(dict_beam_data[QString("B")]) # beam width
    beam_R1 = float(dict_beam_data[QString("R1")]) # beam root radius

    dict_column_data = model.get_columndata(column_section)
    column_f_t = float(dict_column_data[QString("T")]) # column flange thickness
    # columnt_f_t = 15

    dict_angle_data = model.get_angledata(angle_sec)
    angle_t = float(dict_angle_data[QString("t")]) # angle thickness
    # angle_t = 12
    # intentional PEP8 violation in variable naming for angle parameters below
    angle_A = float(dict_angle_data[QString("A")])
    angle_B = float(dict_angle_data[QString("B")])
    angle_R1 = float(dict_angle_data[QString("R1")])

    safe = True

    # -----------------------------------------------------------------------------------------------------------
    # Design Preferences:

    bolt_hole_type = 1 # standard bolt hole
    # bolt_hole_type = 0  # oversize bolt hole
    # bolt hole clearance - user overwrite
    custom_hole_clearance = None # set this to user defined hole clearance, in case
    # assumption: end clearance of beam from face of column = 5mm
    # and tolerance = 5mm
    clearance = 5
    tolerance = 5
    clear_gap = clearance + tolerance
    gamma_m0 = 1.1  # material safety factor for bolts
    # min edge distance multiplier based on edge type Cl 10.2.4.2
    min_edge_multiplier = 1.5  # machine flame cut edges
    # min_edge_multiplier = 1.7  # sheared or hand flame cut edges

    # -----------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------
    #  BOLT DESIGN

    bolt_fu = int(bolt_grade) * 100 # Table 1 of IS 800
    # bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu;    # Bolt f_y is not required in calculations

    thickness_governing = min(beam_w_t.real, angle_t.real)
    bolt_shear_capacity = bolt_shear(bolt_diameter, 1, bolt_fu).real
    bolt_bearing_capacity = bolt_bearing(bolt_diameter, column_f_t, beam_fu).real
    bolt_value = min(bolt_shear_capacity, bolt_bearing_capacity)

    bolts_required = math.ceil(shear_force / bolt_value)

    # TODO SCI minimum 3 bolts
        # assumption: provide minimum 3 bolts based on SCI guidelines
        # check if odd number of bolts can be allowed
    if bolts_required <= 2:
        bolts_required = 3
    print "Number of bolts required = " + str(bolts_required)

    # TODO bolt group capacity
        # check applicable reduction factors
    bolt_group_capacity = bolts_required * bolt_value
    # print "bolt group capacity = " + str(bolt_group_capacity)

    # Bolt hole clearance
    # IS 800, Table 19 Clearances for Fastener HOles
    # TODO Bolt hole clearance
        # update clearance dictionary for other bolt diameters
        # update clearance dictionary for oversized holes

    def bolt_hole_clearance(bolt_hole_type, bolt_diameter):
        if bolt_hole_type == 1: # standard hole
            hole_clearance = {
                12: 1,
                14: 1,
                16: 2,
                18: 2,
                20: 2,
                22: 2,
                24: 2,
                30: 3,
                36: 3
            }[bolt_diameter]
        elif bolt_hole_type == 0: # over size hole
            hole_clearance = {
                12: 3,
                14: 3,
                16: 4,
                18: 4,
                20: 4,
                22: 4,
                24: 6,
                30: 8,
                36: 8
            }[bolt_diameter]

        if custom_hole_clearance is not None:
            hole_clearance = custom_hole_clearance # units: mm
        return hole_clearance  # units: mm

    bolt_hole_diameter = bolt_diameter + bolt_hole_clearance(bolt_hole_type, bolt_diameter)

    # Minimum pitch and gauge IS 800 Cl 10.2.2
    # TODO minimum spacing
        # check with thickness of connected members <= 32t, 300
    min_pitch = int(2.5 * bolt_diameter)
    min_gauge = int(2.5 * bolt_diameter)

    # assumption: rounding off min pitch and gauge distances to upper multiple of 10
    if min_pitch % 10 != 0 or min_gauge % 10 != 0:
        min_pitch = (min_pitch / 10) * 10 + 10
        min_gauge = (min_gauge / 10) * 10 + 10

    print "Minimum pitch = " + str(min_pitch)
    print "Minimum gauge = " + str(min_gauge)

    # Max spacing IS 800 Cl 10.2.3.3
    max_spacing = int(min(100 + 4 * thickness_governing, 200))
    print "Max spacing=" + str(max_spacing)

    # Max spacing IS 800 Cl 10.2.4.2
    min_edge_dist = int(min_edge_multiplier * (bolt_hole_diameter))
    if min_edge_dist % 10 != 0:
        min_edge_dist = (min_edge_dist / 10) * 10 + 10

    # Max spacing IS 800 Cl 10.2.4.3
    max_edge_dist = int((12 * thickness_governing * math.sqrt(250 / beam_fy)).real)

    # in case of corrosive influences, the maximum edge distance shall not exceed
    # 40mm plus 4t, where t is the thickness of the thinner connected plate.
    # max_edge_dist = min(max_edge_dist, 40 + 4*thickness_governing)

    # Determine single or double line of bolts
    length_avail = (angle_A - 2 * min_edge_dist)
    pitch = round(length_avail / (bolts_required - 1), 1)
    # -----------------------------------------------------------------------------------------------------------

    # Seating Angle Design and Check
    # TODO : additional Moment check
        # check moment demand based on shear capacity too?

    # length of angle = beam flange width
    angle_l = beam_w_f
    print "Length of angle = " + str(angle_l)

    # length of bearing required at the root line of beam (b) = R*gamma_m0/t_w*f_yw
    # Changed form of Equation from Cl 8.7.4
    bearing_length = (shear_force * 1000) * gamma_m0 / (beam_w_t * beam_fy)
    bearing_length = round(bearing_length, 3)
    print "Length of bearing required at the root line of beam = " + str(bearing_length)

    # Required length of outstanding leg = bearing length + clearance + tolerance,
    # clear_gap = clearance + tolerance
    outstanding_leg_length_required = bearing_length + clear_gap
    print "Outstanding leg length =" + str(outstanding_leg_length_required)

    if outstanding_leg_length_required > angle_B:
        logger.error(": Connection is not safe")
        logger.warning(": Outstanding leg length of seated angle should be more than " + str(outstanding_leg_length_required))
        safe = False
        print "Error: Seated angle's outstanding leg length needs to be increased"

    # based on 45 degree dispersion Cl 8.7.1.3, stiff bearing length (b1) is calculated as
    # (stiff) bearing length on cleat (b1) = b - T_f (beam flange thickness) - r_b (root radius of beam flange)

    b1 = bearing_length - beam_f_t - beam_R1
    print "Length of bearing on cleat" + str(b1)

    # Distance from the end of bearing on cleat to root angle OR A TO B =b2
    b2 = b1 + clear_gap - angle_t - angle_R1
    print "Distance A to B = " + str(b2)

    # Moment capacity check
    # assumption: load is uniform on length b1
    # moment at root of angle (at B) due to load to the right of B
    moment_at_root_angle = round(shear_force * (b2 / b1) * (b2 / 2), 3)
    print "Moment at root angle = " + str(moment_at_root_angle)

    # Moment capacity = 1.2*Z*f_y/gamma_m0
    # assumption: using elastic moment capacity of the outstanding leg
    moment_capacity_angle = round( 1.2 * (beam_fy / gamma_m0) * angle_l * (angle_t ** 2) * 0.001 / 6, 3)
    print "Moment capacity =" + str(moment_capacity_angle)

    if moment_capacity_angle < moment_at_root_angle:
        logger.error(": Connection is not safe")
        logger.warning(": Moment capacity should be at least " + str(moment_at_root_angle))
        safe = False
        print "Error: Connection not safe"

    # TODO current bookmark
    # Shear capacity check Cl 8.4.1
    # shear capacity of the outstanding leg of cleat = A_v * f_yw / root_3 / gamma_m0
    # = w*t*fy/gamma_m0/root_3
    root_3 = math.sqrt(3);
    outstanding_leg_shear_strength = round(angle_l * angle_t * beam_fy * 0.001 / (gamma_m0 * root_3), 3) #kN
    print "Shear strength of outstanding leg of Seated Anlge = " + str(outstanding_leg_shear_strength)

    if outstanding_leg_shear_strength < shear_force:
        logger.error(": Shear capacity is insufficient")
        logger.warning(": Shear capacity should be at least " + str(shear_force))
        safe = False
        print "Error: Shear capacity is insufficient"

    # shear capacity of beam, Vd = A_v*F_yw/root_3/gamma_m0
    beam_shear_capacity = round(beam_d * beam_w_t * beam_fy / root_3 /gamma_m0/ 1000, 3)
    print "Beam shear capacity = " + str(beam_shear_capacity)

    if beam_shear_capacity < shear_force:
        logger.error(": Beam shear capacity is insufficient")
        logger.warning(": Beam shear capacity should be at least " + str(shear_force + "kN"))
        logger.warning(": Beam design is outside the scope of this module")
        safe = False


        # End of calculation

    outputObj = {}
    outputObj['SeatAngle'] = {
        "Length (mm)": angle_l,
        "Moment Demand (kNm)": moment_at_root_angle,
        "Moment Capacity (kNm)": moment_capacity_angle,
        "Shear Demand (kN/mm)": shear_force,
        "Shear Capacity (kN/mm)": outstanding_leg_shear_strength,
        "Beam Shear Strength (kN/mm)": beam_shear_capacity
        }

    outputObj['Bolt'] = {
        "status": safe,
        "Shear Capacity (kN)": bolt_shear_capacity,
        "Bearing Capacity (kN)": bolt_bearing_capacity,
        "Capacity Of Bolt (kN)": bolt_value,
        "Bolt group capacity (kN)": bolt_group_capacity,
        "No Of Bolts": bolts_required,
        # "No.Of Row": bolts_one_line,
        # "No.Of Column": bolt_line,
        "Pitch Distance (mm)": pitch,
        # "Guage Distance (mm)": gauge,
        # "End Distance (mm)": end_dist,
        "Edge Distance (mm)": min_edge_dist
        }

    if outputObj['Bolt']['status'] == True:

        logger.info(": Overall Seat Angle connection design is safe \n")
        logger.debug(": =========End Of design===========")

    else:
        logger.error(": Design is not safe \n ")
        logger.debug(": =========End Of design===========")

    return outputObj
