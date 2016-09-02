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

'''
import math
import logging

from model import *
from PyQt4.Qt import QString

# flag = 1
# logger = None

logger = logging.getLogger("osdag.SeatAngleCalc")

'''

List of assumptions:

'''


# Bolt calculations
# Bolt factored shear capacity = f_u * number_of_bolts * Area_bolt_net_tensile / (square_root(3) * gamma_mb)
# Reduction factors for long joints, large grip lengths, and packing plates
def bolt_shear(bolt_diameter, number_of_bolts, f_u):
    # assuming shear plane passes through threaded area of all bolts
    # assuming the tensile stress area equal to the threaded area
    # values for tensile stress area (mm^2) from Table 5.9 DoSS - N. Subramanian
    # TODO area of bolts for lower diameters
        # 5, 6, 8, 10 - either omit these from inputs or add to below dictionary
    area_bolts = {'12': 84.3, '16': 157, '20': 245, '22': 303, '24': 353, '27': 459, '30': 561, '36': 817}
    bolt_area = area_bolts[str(bolt_diameter)]
    # bolt_area_approx = math.pi * bolt_diameter * bolt_diameter * 0.25 * 0.78
    bolt_nominal_shear_capacity = f_u * number_of_bolts * bolt_area / (math.sqrt(3) * 1000)
    return round(bolt_nominal_shear_capacity / 1.25, 3)  # gamma_mb = 1.25


# Bolt factored bearing capacity = 2.5 * k_b * bolt_diameter * sum_thickness_of_connecting_plates * f_u / gamma_mb
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
    bolt_planes = 1

    # angle_sec = 'ISA 15075'
    # TODO rework
    angle_sec = inputObj['Angle']["AngleSection"]
    # angle_t = 12

    dictbeamdata = get_beamdata(beam_section)
    beam_w_t = float(dictbeamdata[QString("tw")])
    beam_f_t = float(dictbeamdata[QString("T")])
    beam_d = float(dictbeamdata[QString("D")])
    beam_w_f = float(dictbeamdata[QString("B")])
    beam_R1 = float(dictbeamdata[QString("R1")])

    dictcolumndata = get_columndata(column_section)
    column_f_t = float(dictcolumndata[QString("T")])
    columnt_f_t = 15

    dictangledata = get_angledata(angle_sec)
    angle_t = float(dictangledata[QString("t")])
    # angle_t = 12
    angle_a = float(dictangledata[QString("A")])
    angle_b = float(dictangledata[QString("B")])
    angle_ra = float(dictangledata[QString("R1")])

    safe = True

    ########################################################################
    # Bolt design:

    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu;

    # I: Check for number of bolts -------------------
    t_thinner = min(beam_w_t.real, angle_t.real);
    bolt_shear_capacity = bolt_shear(bolt_diameter, bolt_planes, bolt_fu).real;
    bolt_bearing_capacity = bolt_bearing(bolt_diameter, column_f_t, beam_fu).real;

    bolt_capacity = min(bolt_shear_capacity, bolt_bearing_capacity);

    bolts_required = int(shear_force / bolt_capacity) + 1;
    if bolts_required <= 2:
        bolts_required = 3;

    # even number of bolts -- confirm with sir(doubt)
    else:
        if bolts_required % 2 == 1:
            bolts_required = bolts_required + 1;

    print "no of bolts required =" + str(bolts_required)

    bolt_group_capacity = bolts_required * bolt_capacity;
    print "bolt group capacity =" + str(bolt_group_capacity)

    # Spacing of bolts for web plate -------------------
    if bolt_diameter == 12 or bolt_diameter == 14:
        dia_hole = bolt_diameter + 1
    elif bolt_diameter == 16 or bolt_diameter == 18 or bolt_diameter == 20 or bolt_diameter == 22 or bolt_diameter == 24:
        dia_hole = bolt_diameter + 2
    else:
        dia_hole = bolt_diameter + 3

        # Minimum/maximum pitch and gauge
    min_pitch = int(2.5 * bolt_diameter);
    min_gauge = int(2.5 * bolt_diameter);

    if min_pitch % 10 != 0 or min_gauge % 10 != 0:
        min_pitch = (min_pitch / 10) * 10 + 10;
        min_gauge = (min_gauge / 10) * 10 + 10;
    else:
        min_pitch = min_pitch;
        min_gauge = min_gauge;
        # clause 10.2.2 is800
    print "minimum pitch =" + str(min_pitch)
    print "minimum gauge =" + str(min_gauge)

    max_spacing = int(min(100 + 4 * t_thinner, 200));  # clause 10.2.3.3 is800
    print "max spacing=" + str(max_spacing)

    min_edge_dist = int(1.5 * (dia_hole)) + 10;  # 10 mm added than min. value
    if min_edge_dist % 10 != 0:
        min_edge_dist = (min_edge_dist / 10) * 10 + 10;
    else:
        min_edge_dist = min_edge_dist;

    max_edge_dist = int((12 * t_thinner * math.sqrt(250 / beam_fy)).real) - 1;

    # Determine single or double line of bolts

    length_avail = (angle_a - 2 * min_edge_dist);
    pitch = round(length_avail / (bolts_required - 1), 3);

    ## Calculation of moment demand

    M1 = bolt_shear_capacity * (20 + min_edge_dist / 2);
    # Single line of bolts
    if pitch >= min_pitch:
        bolt_line = 1;
        gauge = 0;
        bolts_one_line = bolts_required;
        K = bolts_one_line / 2;
        M2 = 0;
        if bolts_required % 2 == 0 or bolts_required % 2 != 0:
            for k in range(0, K):
                M2 = M2 + 2 * (
                bolt_shear_capacity * ((length_avail / 2 - k * pitch) ** 2 / (length_avail / 2 - k * pitch)));
            moment_demand = max(M1, M2);
            moment_demand = round(moment_demand * 0.001, 3)

    # Multi-line of bolts
    if pitch < min_pitch:
        bolt_line = 2;
        if bolts_required % 2 == 0:
            bolts_one_line = bolts_required / 2;
        else:
            bolts_one_line = (bolts_required / 2) + 1;

        pitch = round(length_avail / (bolts_one_line - 1), 3);
        gauge = min_gauge;
        M1 = bolt_shear_capacity * (20 + min_edge_dist + gauge / 2);

        if pitch >= min_pitch:
            K = bolts_one_line / 2;
            M2 = 0;
            if bolts_required % 2 == 0 or bolts_required % 2 != 0:
                for k in range(0, K):
                    V = length_avail / 2 - k * pitch
                    H = gauge / 2;
                    d = math.sqrt(V ** 2 + H ** 2);
                    M2 = M2 + 2 * (bolt_shear_capacity * (d ** 2 / d));
                M2 = M2 * 2;
                moment_demand = max(M1, M2);
                moment_demand = round(moment_demand * 0.001, 3)

                # Needs discussion with Sir
        else:
            logger.error(": Bolt strength is insufficient to carry the shear force")
            safe = False
            logger.warning(": Increase bolt diameter and/or bolt grade")
            moment_demand = 0.0

    if bolt_line == 1:
        angle_b_req = 2 * min_edge_dist
        end_dist = angle_b / 2
    if bolt_line == 2:
        angle_b_req = gauge + 2 * min_edge_dist
        end_dist = (angle_b - gauge) / 2

    # *************************************
    # Seating Angle Design and Check
    # *************************************
    # length of angle = beam flange width
    angle_l = beam_w_f
    print "length of angle =" + str(angle_l)

    # length of bearing required at the root line of beam = R*Y0/tw*fyw
    #
    bearing_length = shear_force * 1.1 * 1000 / (beam_w_t * beam_fy)
    bearing_length = round(bearing_length, 3)
    print "length of bearing required at the root line of beam=" + str(bearing_length)

    # assuming end clearance of beam from face of column as 5mm and tolerance of 5mm
    clearance = 5
    tolerance = 5
    # Required length of outstanding leg = bearing length + clearance + tolerance
    outstanding_leg_length = bearing_length + tolerance + clearance
    print "outstanding leg length =" + str(outstanding_leg_length)

    if outstanding_leg_length > angle_b:
        logger.error(": Assumed angle outstanding leg length need to be changed")
        logger.warning(": Outstanding leg length should be less than " + str(angle_b))
        safe = False
        print "error: assumed angle outstanding leg length is not sufficient"

    # length of bearing on cleat = b1
    bearing_length_on_cleat = bearing_length - (beam_f_t + beam_R1)  # find out what these values are DOUBT
    b1 = bearing_length_on_cleat
    print "length of bearing on cleat" + str(bearing_length_on_cleat)

    # for ISA 150*75*12, distance from the end of bearing on cleat to root angle OR A TO B =b2
    b2 = b1 + clearance + tolerance - angle_t - angle_ra
    print "distance A to B = " + str(b2)

    # **************************************
    # Moment Calculation
    # **************************************
    # assuming uniformly distributed load on length b1
    # moment at root of angle, that is , at B due to load to the right of B
    moment_at_root_angle = shear_force * (b2 / b1) * (b2 / 2)
    moment_at_root_angle = round(moment_at_root_angle, 3)
    print "moment at root angle =" + str(moment_at_root_angle)

    # Moment capacity = 1.2*Z*fy/Y0
    moment_capacity = 1.2 * (beam_fy / 1.1) * angle_l * (angle_t ** 2) * 0.001 / 6
    moment_capacity = round(moment_capacity, 3)
    print "Moment capacity =" + str(moment_capacity)

    if moment_capacity < moment_at_root_angle:
        logger.error(": Connection is not safe")
        logger.warning(": Moment Capacity should be at least " + str(moment_at_root_angle))
        safe = False
        print "error: connection not safe"

    # **************************************
    # Shear capacity calculation
    # **************************************
    # shear capacity of the outstanding leg of cleat = w*t*fy/(y0*(root 3))
    root3 = math.sqrt(3);
    outstanding_leg_shear_strength = beam_w_f * angle_t * beam_fy * 0.001 / (1.1 * root3)
    outstanding_leg_shear_strength = round(outstanding_leg_shear_strength, 3)
    print "outstanding leg shear strength =" + str(outstanding_leg_shear_strength)

    if outstanding_leg_shear_strength < shear_force:
        logger.error(": Shear capacity is insufficient")
        logger.warning(": Shear Capacity should be at least " + str(shear_force)
        safe = False
        print "error: shear capacity is insufficient"

    # shear capacity of beam, Vd = Av*Fyw/root3*y0
    beam_shear_capacity = beam_d * beam_w_t * beam_fy / (root3 * 1.10 * 1000)
    beam_shear_capacity = round(beam_shear_capacity, 3)
    print "beam shear strength = " + str(beam_shear_capacity)

    if beam_shear_capacity < shear_force:
        logger.error(": Beam Shear Capacity is insufficient")
        logger.warning(": Beam Shear Capacity should be at least " + str(shear_force + "kN/mm")
        safe = False






        # End of calculation
    #     outputObj = {}
    #     outputObj['Bolt'] ={}

    #     outputObj['Bolt']['shearcapacity'] = bolt_shear_capacity
    #     outputObj['Bolt']['bearingcapacity'] = bolt_bearing_capacity
    #     outputObj['Bolt']['boltcapacity'] = bolt_capacity
    #     outputObj['Bolt']['numofbolts'] = bolts_required
    #     outputObj['Bolt']['boltgrpcapacity'] = bolt_group_capacity
    #     outputObj['Bolt'][''] = bolts_one_line
    #     outputObj['Bolt']['numofcol'] = bolt_line
    #     outputObj['Bolt']['pitch'] = pitch
    #     outputObj['Bolt']['enddist'] = float(end_dist)
    #     outputObj['Bolt']['edge'] = float(min_edge_dist)
    #     outputObj['Bolt']['gauge'] = float(gauge)
    #

    outputObj = {}
    outputObj['SeatAngle'] = {}

    outputObj['SeatAngle']["Length (mm)"] = angle_l
    outputObj['SeatAngle']["Moment Demand (kNm)"] = moment_at_root_angle
    outputObj['SeatAngle']["Moment Capacity (kNm)"] = moment_capacity
    outputObj['SeatAngle']["Shear Demand (kN/mm)"] = shear_force
    outputObj['SeatAngle']["Shear Capacity (kN/mm)"] = outstanding_leg_shear_strength
    outputObj['SeatAngle']["Beam Shear Strength (kN/mm)"] = beam_shear_capacity

    outputObj['Bolt'] = {}
    outputObj['Bolt']['status'] = safe
    outputObj['Bolt']["Shear Capacity (kN)"] = bolt_shear_capacity
    outputObj['Bolt']["Bearing Capacity (kN)"] = bolt_bearing_capacity
    outputObj['Bolt']["Capacity Of Bolt (kN)"] = bolt_capacity
    outputObj['Bolt']["Bolt group capacity (kN)"] = bolt_group_capacity
    outputObj['Bolt']["No Of Bolts"] = bolts_required
    outputObj['Bolt']["No.Of Row"] = bolts_one_line
    outputObj['Bolt']["No.Of Column"] = bolt_line
    outputObj['Bolt']["Pitch Distance (mm)"] = pitch
    outputObj['Bolt']["Guage Distance (mm)"] = gauge
    outputObj['Bolt']["End Distance (mm)"] = end_dist
    outputObj['Bolt']["Edge Distance (mm)"] = min_edge_dist

    if outputObj['Bolt']['status'] == True:

        logger.info(": Overall Seat Angle connection design is safe \n")
        logger.debug(" :=========End Of design===========")

    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")

    return outputObj
