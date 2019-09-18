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
from utilities.is800_2007 import IS800_2007
from utilities.other_standards import IS1363_part_1_2002, IS1363_part_3_2002, IS1367_Part3_2002
from utilities.common_calculation import *
import math
import logging
flag = 1
logger = None
beam_d = 0
beam_B = 0




def module_setup():
    global logger
    logger = logging.getLogger("osdag.bc_endplate_calc")


module_setup()

#######################################################################

# Start of Main Program


def bc_endplate_design(uiObj):
    global logger
    global design_status
    design_status = True

    if uiObj['Member']['Connectivity'] == "Column web-Beam web":
        conn_type = 'col_web_connectivity'
    else:   # "Column flange-Beam web"
        conn_type = 'col_flange_connectivity'

    if uiObj['Member']['EndPlate_type'] == "Extended one way":
        endplate_type = "one_way"
    elif uiObj['Member']['EndPlate_type'] == "Flush end plate":
        endplate_type = "flush"
    else:  # uiObj['Member']['EndPlate_type'] == "Extended both ways":
        endplate_type = "both_way"

    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumnSection']
    beam_fu = float(uiObj['Member']['fu (MPa)'])
    beam_fy = float(uiObj['Member']['fy (MPa)'])
    column_fu = float(uiObj['Member']['fu (MPa)'])
    column_fy = float(uiObj['Member']['fy (MPa)'])
    weld_fu = float(uiObj['weld']['fu_overwrite'])

    factored_moment = float(uiObj['Load']['Moment (kNm)']) * 1e6
    factored_shear_load = float(uiObj['Load']['ShearForce (kN)']) * 1e3
    factored_axial_load = uiObj['Load']['AxialForce (kN)']
    if factored_axial_load == '':
        factored_axial_load = 0
    else:
        factored_axial_load = float(factored_axial_load) * 1e3

    bolt_dia = int(uiObj['Bolt']['Diameter (mm)'])
    bolt_type = uiObj["Bolt"]["Type"]
    bolt_grade = float(uiObj['Bolt']['Grade'])
    bolt_fu = uiObj["bolt"]["bolt_fu"]
    bolt_fy = (bolt_grade - int(bolt_grade)) * bolt_fu
    mu_f = float(uiObj["bolt"]["slip_factor"])
    gamma_mw = float(uiObj["weld"]["safety_factor"])
    if gamma_mw == 1.50:
        weld_fabrication = 'field'
    else:
        weld_fabrication = 'shop'

    dp_bolt_hole_type = uiObj["bolt"]["bolt_hole_type"]
    if dp_bolt_hole_type == "Over-sized":
        bolt_hole_type = 'over_size'
    else:   # "Standard"
        bolt_hole_type = 'standard'

    dia_hole = bolt_dia + int(uiObj["bolt"]["bolt_hole_clrnce"])
    end_plate_thickness = float(uiObj['Plate']['Thickness (mm)'])

    # TODO implement after excomm review for different grades of plate
    end_plate_fu = float(uiObj['Member']['fu (MPa)'])
    end_plate_fy = float(uiObj['Member']['fy (MPa)'])

    weld_thickness_flange = 0
    weld_thickness_web = 0
    if uiObj["Weld"]["Method"] == "Fillet Weld":
        weld_method = 'fillet'

        weld_thickness_flange = float(uiObj['Weld']['Flange (mm)'])
        weld_thickness_web = float(uiObj['Weld']['Web (mm)'])

    else:   # "Groove Weld (CJP)"
        weld_method = 'groove'

    if uiObj["detailing"]["typeof_edge"] == "a - Sheared or hand flame cut":
        edge_type = 'hand_flame_cut'
    else:   # "b - Rolled, machine-flame cut, sawn and planed"
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
    global beam_tw
    beam_tw = float(dictbeamdata["tw"])
    global beam_tf
    beam_tf = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_B = float(dictbeamdata["B"])
    beam_R1 = float(dictbeamdata["R1"])
    beam_R2 = float(dictbeamdata["R2"])
    beam_Zz = float(dictbeamdata["Zz"]) * 1e3   # cu. mm




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
    column_clear_d = column_d - 2 * (column_tf + column_R1)

    # Minimum Design Action (Cl. 10.7, IS 800:2007) #TODO:  Correction for plastic moment capacity
    beam_moment = 1.2 * beam_Zz * beam_fy / 1.10
    min_connection_moment = 0.5 * beam_moment
    if factored_moment < min_connection_moment:
        min_connection_moment_kNm = round((min_connection_moment/1e6), 3)
        logger.warning(": The connection is designed for %s kNm (Cl. 10.7, IS 800:2007)" % min_connection_moment_kNm)
        factored_moment = min_connection_moment

    if conn_type == 'col_web_connectivity':
        bolt_plates_tk = [column_tw, end_plate_thickness]
        plate_width_max = column_clear_d

        if beam_B > column_clear_d:
            design_status = False
            logger.error(": Beam is wider than column clear depth")
            logger.warning(": Width of beam should be less than %s mm" % column_clear_d)
            logger.info(": Currently, Osdag doesn't design such connections")

    else:
        bolt_plates_tk = [column_tf, end_plate_thickness]
        plate_width_max = column_B

        if beam_B > column_B:
            design_status = False
            logger.error(": Beam is wider than column width")
            logger.warning(": Width of beam should be less than %s mm" % column_B)
            logger.info(": Currently, Osdag doesn't design such connections")

    web_weld_plates = [end_plate_thickness, beam_tw]
    flange_weld_plates = [end_plate_thickness, beam_tf]

    #######################################################################
    # Calculation of Spacing (Min values rounded to next multiple of 5)

    # min_pitch & max_pitch = Minimum and Maximum pitch distance (mm)
    pitch_dist_min = IS800_2007.cl_10_2_2_min_spacing(bolt_dia)
    pitch_dist_max = IS800_2007.cl_10_2_3_1_max_spacing(bolt_plates_tk)
    pitch_dist = round_up(pitch_dist_min, multiplier=5)

    # min_end_distance & max_end_distance = Minimum and Maximum end distance
    #       [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]

    end_dist_min = IS800_2007.cl_10_2_4_2_min_edge_end_dist(
        d=bolt_dia, bolt_hole_type=bolt_hole_type,edge_type=edge_type)
    end_dist_max = IS800_2007.cl_10_2_4_3_max_edge_dist(
        plate_thicknesses=bolt_plates_tk, f_y=end_plate_fy, corrosive_influences=corrosive_influences)
    end_dist = round_up(end_dist_min, multiplier=5)

    # min_edge_distance = Minimum edge distance (mm) [Cl. 10.2.4.2 & Cl. 10.2.4.3, IS 800:2007]
    edge_dist_min = end_dist_min
    edge_dist_max = end_dist_max
    edge_dist = round_up(edge_dist_min, multiplier=5)

    #######################################################################
    # l_v = Distance from the edge of flange to the centre of the nearer bolt (mm) [AISC design guide 16]
    # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge, Steel designers manual, pp733, 6th edition - 2003)
    if endplate_type == 'flush':
        l_v = 45.0
        g_1 = 90.0
    elif endplate_type == 'one_way':
        l_v = 50.0
        g_1 = 100.0
    else:   # endplate_type == 'both_ways':
        l_v = 50.0
        g_1 = 100.0

    if weld_method == 'fillet':
        flange_projection = round_up(value=weld_thickness_flange + 2, multiplier=5, minimum_value=5)
    else:   # 'groove'
        flange_projection = 5

    #######################################################################
    # Calculate bolt capacities

    if bolt_type == "Friction Grip Bolt":
        bolt_slip_capacity = IS800_2007.cl_10_4_3_bolt_slip_resistance(
            f_ub=bolt_fu, A_nb=bolt_net_area, n_e=1, mu_f=mu_f, bolt_hole_type=bolt_hole_type)
        bolt_tension_capacity = IS800_2007.cl_10_4_5_friction_bolt_tension_resistance(
            f_ub=bolt_fu, f_yb=bolt_fy, A_sb=bolt_shank_area, A_n=bolt_net_area)
        bearing_capacity = 0.0
        bolt_shear_capacity = 0.0
        bolt_capacity = bolt_slip_capacity

    else:
        bolt_shear_capacity = IS800_2007.cl_10_3_3_bolt_shear_capacity(
            f_u=bolt_fu, A_nb=bolt_net_area, A_sb=bolt_shank_area, n_n=1, n_s=0)
        bearing_capacity = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
            f_u=min(column_fu, end_plate_fu), f_ub=bolt_fu, t=sum(bolt_plates_tk), d=bolt_dia, e=edge_dist,
            p=pitch_dist, bolt_hole_type=bolt_hole_type)
        bolt_slip_capacity = 0.0
        bolt_capacity = min(bolt_shear_capacity, bearing_capacity)
        bolt_tension_capacity = IS800_2007.cl_10_3_5_bearing_bolt_tension_resistance(
            f_ub=bolt_fu, f_yb=bolt_fy, A_sb=bolt_shank_area, A_n=bolt_net_area)

    #######################################################################

    # Calculation for number of bolts around tension flange
    flange_tension = factored_moment / (beam_d - beam_tf) + factored_axial_load / 2
    no_tension_side_rqd = flange_tension / (0.80 * bolt_tension_capacity)
    no_tension_side = round_up(no_tension_side_rqd, multiplier=2, minimum_value=2)

    # Prying force
    b_e = beam_B / 2
    prying_force = IS800_2007.cl_10_4_7_bolt_prying_force(
        T_e=flange_tension/4, l_v=l_v, f_o=0.7*bolt_fu, b_e=b_e, t=end_plate_thickness, f_y=end_plate_fy,
        end_dist=end_dist, pre_tensioned=False)
    toe_of_weld_moment = abs(flange_tension/4 * l_v - prying_force * end_dist)
    end_plate_thickness_min = math.sqrt(toe_of_weld_moment * 1.10 * 4 / (end_plate_fy * b_e))

    # End Plate Thickness
    if end_plate_thickness < max(column_tf, end_plate_thickness_min):
        end_plate_thickness_min = math.ceil(max(column_tf, end_plate_thickness_min))
        design_status = False
        logger.error(": Chosen end plate thickness is not sufficient")
        logger.warning(": Minimum required thickness of end plate is %2.2f mm " % end_plate_thickness_min)
        logger.info(": Increase the thickness of end plate ")

    # Detailing
    bolt_combined_status = False
    detailing_status = True
    while bolt_combined_status is False:

        if endplate_type == 'flush':
            number_of_bolts = 2 * no_tension_side

            if no_tension_side == 2:
                no_rows = {'out_tension_flange': 0, 'in_tension_flange': 1,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < pitch_dist:
                    detailing_status = False

            elif no_tension_side == 4:
                no_rows = {'out_tension_flange': 0, 'in_tension_flange': 2,
                           'out_compression_flange': 0, 'in_compression_flange': 2}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # # logger.warning()
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    # TODO Re-detail the connection
                    # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                    #            'out_compression_flange': 2, 'in_compression_flange': 1}

            elif no_tension_side == 6:
                no_rows = {'out_tension_flange': 0, 'in_tension_flange': 3,
                           'out_compression_flange': 0, 'in_compression_flange': 3}
                if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    #  Re-detail the connection
                    # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                    #            'out_compression_flange': 3, 'in_compression_flange': 1}

            else:
                detailing_status = False
                # logger.error("Large number of bolts are required for the connection")
                # logger.info(": Re-design the connection using bolt of higher grade or diameter")
                no_rows = {'out_tension_flange': (no_tension_side-6)/2, 'in_tension_flange': 2,
                           'out_compression_flange': (no_tension_side-6)/2, 'in_compression_flange': 2}

            # #######################################################################

        elif endplate_type == 'one_way':
            number_of_bolts = no_tension_side + 2
            if no_tension_side <= 4:
                no_tension_side = 4
                number_of_bolts = no_tension_side + 2
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # # logger.warning()
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    #  Re-detail the connection
                    # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                    #            'out_compression_flange': 0, 'in_compression_flange': 1}

            elif no_tension_side == 6:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < 2 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # # logger.warning()
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    #  Re-detail the connection
                    # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                    #            'out_compression_flange': 0, 'in_compression_flange': 1}

            elif no_tension_side == 8:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    #  Re-detail the connection
                    # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                    #            'out_compression_flange': 0, 'in_compression_flange': 1}
            elif no_tension_side == 10:
                no_rows = {'out_tension_flange': 2, 'in_tension_flange': 3,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

            else:
                detailing_status = False
                # logger.error("Large number of bolts are required for the connection")
                # logger.info(": Re-design the connection using bolt of higher grade or diameter")
                no_rows = {'out_tension_flange': (no_tension_side-6)/2, 'in_tension_flange': 2,
                           'out_compression_flange': (no_tension_side-6)/2, 'in_compression_flange': 2}

            # #######################################################################

        else:   # endplate_type == "both_way":
            number_of_bolts = 2 * no_tension_side

            if no_tension_side <= 4:
                no_tension_side = 4
                number_of_bolts = 2 * no_tension_side
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 1,
                           'out_compression_flange': 1, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < pitch_dist:
                    detailing_status = False

            elif no_tension_side == 6:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                           'out_compression_flange': 1, 'in_compression_flange': 2}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # # logger.warning()
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    #  Re-detail the connection
                    # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                    #            'out_compression_flange': 2, 'in_compression_flange': 1}

            elif no_tension_side == 8:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
                           'out_compression_flange': 1, 'in_compression_flange': 3}
                if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    #  Re-detail the connection
                    # no_rows = {'out_tension_flange': 3, 'in_tension_flange': 1,
                    #            'out_compression_flange': 3, 'in_compression_flange': 1}
            elif no_tension_side == 10:
                no_rows = {'out_tension_flange': 2, 'in_tension_flange': 3,
                           'out_compression_flange': 2, 'in_compression_flange': 3}
                if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

            else:
                detailing_status = False
                # logger.error("Large number of bolts are required for the connection")
                # logger.info(": Re-design the connection using bolt of higher grade or diameter")
                no_rows = {'out_tension_flange': (no_tension_side-6)/2, 'in_tension_flange': 2,
                           'out_compression_flange': (no_tension_side-6)/2, 'in_compression_flange': 2}

            # #######################################################################

        # Plate height and width
            ''' tens_plate_no_pitch : projection of end plate beyond the beam flange excluding the 
                                        distances b/w bolts on tension side '''
        if no_rows['out_tension_flange'] == 0:
            tens_plate_outer = flange_projection
        else:
            tens_plate_outer = end_dist + l_v + (no_rows['out_tension_flange'] - 1) * pitch_dist
        if no_rows['out_compression_flange'] == 0:
            comp_plate_outer = flange_projection
        else:
            comp_plate_outer = end_dist + l_v + (no_rows['out_compression_flange'] - 1) * pitch_dist

        plate_height = beam_d + comp_plate_outer + tens_plate_outer
        plate_width = g_1 + 2 * edge_dist
        while plate_width < beam_B:
            edge_dist += 5
            plate_width = g_1 + 2 * edge_dist
            if edge_dist > edge_dist_max:
                edge_dist -= 5
                g_1 += 5
                plate_width = g_1 + 2 * edge_dist
                # TODO: Apply max limit for g_1, design fails

        if plate_width > plate_width_max:
            design_status = False
            logger.error(": Required plate width is more than the available width")
            logger.warning(": Width of plate should be less than %s mm" % plate_width_max)
            logger.info(": Currently, Osdag doesn't design such connections")

        # Tension in bolts
        axial_tension = factored_axial_load / number_of_bolts
        if no_rows['out_tension_flange'] == 0:
            extreme_bolt_dist = beam_d - beam_tf * 3/2 - l_v
        else:
            extreme_bolt_dist = beam_d - beam_tf/2 + l_v + (no_rows['out_tension_flange']-1) * pitch_dist
        sigma_yi_sq = 0
        for bolt_row in range(int(no_rows['out_tension_flange'])):
            sigma_yi_sq += (beam_d - beam_tf/2 + l_v + bolt_row * pitch_dist) ** 2
        for bolt_row in range(int(no_rows['in_tension_flange'])):
            sigma_yi_sq += (beam_d - 3 * beam_tf/2 - l_v - bolt_row * pitch_dist) ** 2

        moment_tension = factored_moment * extreme_bolt_dist / sigma_yi_sq / 2
        tension_in_bolt = axial_tension + moment_tension + prying_force
        shear_in_bolt = factored_shear_load / number_of_bolts
        # Check for combined tension and shear
        if bolt_type == "Friction Grip Bolt":
            combined_capacity = IS800_2007.cl_10_4_6_friction_bolt_combined_shear_and_tension(
                V_sf=shear_in_bolt, V_df=bolt_capacity, T_f=tension_in_bolt, T_df=bolt_tension_capacity)
        else:
            combined_capacity = IS800_2007.cl_10_3_6_bearing_bolt_combined_shear_and_tension(
                V_sb=shear_in_bolt, V_db=bolt_capacity, T_b=tension_in_bolt, T_db=bolt_tension_capacity)
        bolt_combined_status = combined_capacity <= 1.0

        if bolt_combined_status is False:
            no_tension_side += 2
        if detailing_status is False:
            design_status = False
            logger.error("Large number of bolts are required for the connection")
            logger.info(": Re-design the connection using bolt of higher grade or diameter")
            break

    #######################################################################
    # WELD DESIGN

    if weld_method == 'fillet':
        # Flange weld
        flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(beam_tf, end_plate_thickness)
        flange_weld_throat_size = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=weld_thickness_flange, fusion_face_angle=90)
        flange_weld_throat_max = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(beam_tf, end_plate_thickness)
        flange_weld_size_max = min(beam_tf, end_plate_thickness)

        # Web welds

        web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(beam_tw, end_plate_thickness)
        web_weld_throat_size = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=weld_thickness_web, fusion_face_angle=90)
        web_weld_throat_max = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(beam_tw, end_plate_thickness)
        web_weld_size_max = min(beam_tw, end_plate_thickness)

        # check min and max weld size

        if weld_thickness_flange < flange_weld_size_min:
            design_status = False
            logger.error(": The weld size at beam flange is less than required")
            logger.warning(": The minimum required weld size at beam flange is %s mm" % flange_weld_size_min)
            logger.info(": Increase the size of weld at beam flanges")

        if weld_thickness_flange > flange_weld_size_max:
            design_status = False
            logger.error(": The weld size at beam flange is more than allowed")
            logger.warning(": The maximum allowed throat size of weld at flanges is %s mm" % flange_weld_size_max)
            logger.info(": Decrease the size of weld at beam flanges")

        if weld_thickness_web < web_weld_size_min:
            design_status = False
            logger.error(": The weld size at beam web is less than required")
            logger.warning(": The minimum required weld size at beam web is %s mm" % web_weld_size_min)
            logger.info(": Increase the size of weld at beam web")

        if weld_thickness_web > web_weld_size_max:
            design_status = False
            logger.error(": The weld size at beam web is more than allowed")
            logger.warning(": The maximum allowed throat size of weld at webs is %s mm" % web_weld_size_max)
            logger.info(": Decrease the size of weld at beam web")

        # Weld lengths - available and effective, long joint reduction factors

        flange_weld_available_length_top = beam_B
        flange_weld_available_length_bottom = (beam_B - beam_tw - 2*beam_R1 - 2*beam_R2) / 2

        flange_weld_effective_length_top = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=weld_thickness_flange, available_length=flange_weld_available_length_top)
        flange_weld_effective_length_bottom = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=weld_thickness_flange, available_length=flange_weld_available_length_bottom)

        flange_weld_long_joint_top = IS800_2007.cl_10_5_7_3_weld_long_joint(
            l_j=flange_weld_effective_length_top, t_t=flange_weld_throat_size)
        flange_weld_long_joint_bottom = IS800_2007.cl_10_5_7_3_weld_long_joint(
            l_j=flange_weld_effective_length_bottom, t_t=flange_weld_throat_size)

        web_weld_available_length = beam_d - 2 * (beam_tf + beam_R1)
        web_weld_effective_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=weld_thickness_web, available_length=web_weld_available_length)
        web_weld_long_joint = IS800_2007.cl_10_5_7_3_weld_long_joint(
            l_j=web_weld_effective_length, t_t=web_weld_throat_size)

        # Weld strength

        flange_weld_strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=[beam_fu, weld_fu], fabrication=weld_fabrication)

        web_weld_strength = IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=[beam_fu, weld_fu], fabrication=weld_fabrication)

        #  Design forces per unit length of welds due to applied loads
        """
        weld_force_axial = factored_axial_load / (
                2 * (flange_weld_effective_length_top * flange_weld_long_joint_top +
                    2 * flange_weld_effective_length_bottom * flange_weld_long_joint_bottom +
                    web_weld_effective_length * web_weld_long_joint))

        flange_tension_moment = factored_moment / (beam_d - beam_tf)
        weld_force_moment = flange_tension_moment / (flange_weld_effective_length_top +
                                                             2 * flange_weld_effective_length_bottom)
        weld_force_shear = factored_shear_load / (2 * web_weld_effective_length * web_weld_long_joint)
        
        # check for weld strength

        flange_weld_stress = (weld_force_moment + weld_force_axial) / flange_weld_throat_size
        flange_weld_throat_reqd = round((weld_force_moment + weld_force_axial) / flange_weld_strength, 3)
        flange_weld_size_reqd = round(flange_weld_throat_reqd / 0.7, 3)

        web_weld_stress = math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / web_weld_throat_size
        web_weld_throat_reqd = round(math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / web_weld_strength, 3)
        web_weld_size_reqd = round(web_weld_throat_reqd / 0.7, 3)

        """
        """
        axial force is taken by flange and web welds = P/(2*lw+ltf+lbf)
        shear force is taken by web welds only = V/(2*lw)
        moment is taken by both flange and web welds = M/Z 
        z = ltf*lw/2 + lbf*lw/2 + d^2/3 
        """
        # Stress for axial load in beam=Axial load/sum of (individual weld length *corresponding weld throat thickness)
        # Total length for flange weld = 2* flange_weld_effective_length_top + 4* flange_weld_effective_length_bottom
        # Weld throat thickness for flange = flange_weld_throat_size
        # Total length for web weld = 2* web_weld_effective_length
        # Weld throat thickness for flange = web_weld_throat_size

        # weld_force_axial = factored_axial_load /
        # (flange_weld_effective_length_top * flange_weld_long_joint_top +
        # flange_weld_effective_length_bottom * flange_weld_long_joint_bottom +
        # 2 *web_weld_effective_length * web_weld_long_joint)

        weld_force_axial_stress = factored_axial_load / ( \
                    2 * flange_weld_effective_length_top * flange_weld_long_joint_top * flange_weld_throat_size + \
                    4 * flange_weld_effective_length_bottom * flange_weld_long_joint_bottom * flange_weld_throat_size + \
                    2 * web_weld_effective_length * web_weld_long_joint * web_weld_throat_size)

        # flange_tension_moment = factored_moment / (beam_d - beam_tf)
        # weld_force_moment = flange_tension_moment / (
        #         flange_weld_effective_length_top * flange_weld_long_joint_top * web_weld_effective_length / 2 +
        #         flange_weld_effective_length_bottom * flange_weld_long_joint_bottom * web_weld_effective_length / 2 +
        #         web_weld_effective_length**2/3)

        # Stresses in extreme weld (top flange) due to applied moment

        weld_Iz = (2 * (web_weld_effective_length ** 3) / 12) * web_weld_throat_size + \
                   (2 * flange_weld_effective_length_top * (beam_d / 2 ) ** 2 + \
                   4 * flange_weld_effective_length_bottom * (beam_d / 2 - beam_tf) ** 2) * flange_weld_throat_size

        flange_weld_Z = weld_Iz / (beam_d / 2)
        web_weld_Z = weld_Iz / (beam_d / 2 - beam_tf - beam_R1)

        flange_weld_stress = factored_moment / flange_weld_Z + weld_force_axial_stress

        weld_force_shear = factored_shear_load / (2 * web_weld_effective_length * web_weld_throat_size * web_weld_long_joint)

        # calculation of required weld size is not accurate since Iz has different web and flange sizes
        # but to get required throat thickness either flange or weld size is multiplied
        flange_weld_throat_reqd = round(flange_weld_stress * flange_weld_throat_size / flange_weld_strength, 3)
        flange_weld_size_reqd = round(flange_weld_throat_reqd / 0.7, 3)

        web_weld_stress = math.sqrt((factored_moment / web_weld_Z + weld_force_axial_stress) ** 2 + \
                          weld_force_shear ** 2)

        web_weld_throat_reqd = round(web_weld_stress * web_weld_throat_size /
                                     web_weld_strength, 3)
        web_weld_size_reqd = round(web_weld_throat_reqd / 0.7, 3)

        if flange_weld_stress >= flange_weld_strength:
            design_status = False
            logger.error(": The weld size at beam flange is less than required")
            if flange_weld_size_reqd > flange_weld_size_max:
                logger.warning(": The connection can not be possible with fillet weld")
                logger.info(": Use groove welds to connect beam and end plate")
            else:
                logger.warning(": The minimum required size of weld at flanges is %s mm" % flange_weld_size_reqd)
                logger.info(": Increase the size of weld at beam flanges")

        if web_weld_stress >= web_weld_strength:
            design_status = False
            logger.error(": The weld size at beam web is less than required")
            if web_weld_size_reqd > web_weld_size_max and flange_weld_size_reqd < flange_weld_size_max:
                logger.warning(": The connection can not be possible with fillet weld")
                logger.info(": Use groove welds to connect beam and end plate")
            else:
                logger.warning(": The minimum required size of weld at web is %s mm" % web_weld_size_reqd)
                logger.info(": Increase the size of weld at beam web")

    else:   # weld_method == 'groove'
        groove_weld_size_flange = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
            beam_tf, end_plate_thickness)
        groove_weld_size_web = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
            beam_tw, end_plate_thickness)

    # Continuity Plates
    cont_plate_fu = beam_fu
    cont_plate_fy = beam_fy
    cont_plate_e = math.sqrt(250/cont_plate_fy)
    gamma_m0 = 1.10
    gamma_m1 = 1.10

    # Continuity Plates on compression side
    p_bf = factored_moment / (beam_d - beam_tf) - factored_axial_load   # Compressive force at beam flanges
    cont_plate_comp_length = column_d - 2 * column_tf
    cont_plate_comp_width = (column_B - column_tw) / 2
    notch_cont_comp = round_up(value=column_R1, multiplier=5, minimum_value=5)
    available_cont_comp_width = cont_plate_comp_width - notch_cont_comp
    available_cont_comp_length = cont_plate_comp_length - 2 * notch_cont_comp

    col_web_capacity_yielding = column_tw * (5 * column_tf + 5 * column_R1 + beam_tf) * column_fy / gamma_m0
    col_web_capacity_crippling = ((300 * column_tw ** 2) / gamma_m1) * (
        1 + 3 * (beam_tf / column_d) * (column_tw / column_tf) ** 1.5) * math.sqrt(column_fy * column_tf / column_tw)
    col_web_capacity_buckling = (10710 * (column_tw ** 3) / column_d) * math.sqrt(column_fy / gamma_m0)
    col_web_capacity = min(col_web_capacity_yielding, col_web_capacity_crippling, col_web_capacity_buckling)
    cont_plate_comp_tk_local_buckling = cont_plate_comp_width / (9.4 * cont_plate_e)
    cont_plate_comp_tk_min = max(cont_plate_comp_tk_local_buckling, beam_tf,
                                 (p_bf - col_web_capacity) / (cont_plate_comp_width * cont_plate_fy / gamma_m0))
    cont_plate_comp_tk = cont_plate_comp_tk_min
    available_plates = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32, 34, 35, 36, 40, 45, 50, 55, 60]
    for plate_tk in available_plates:
        if plate_tk >= cont_plate_comp_tk_min:
            cont_plate_comp_tk = plate_tk
            break

    # Continuity Plates on tension side
    t_bf = factored_moment / (beam_d - beam_tf) + factored_axial_load  # Tensile force at beam flanges
    cont_plate_tens_length = column_d - 2 * column_tf
    cont_plate_tens_width = (column_B - column_tw) / 2
    notch_cont_tens = round_up(value=column_R1, multiplier=5, minimum_value=5)
    available_cont_tens_width = cont_plate_tens_width - notch_cont_tens
    available_cont_tens_length = cont_plate_tens_length - 2 * notch_cont_tens

    col_flange_tens_capacity = (column_tf ** 2) * beam_fy / (0.16 * gamma_m0)
    cont_plate_tens_tk_min = (t_bf - col_flange_tens_capacity) / (cont_plate_tens_width * cont_plate_fy / gamma_m0)
    cont_plate_tens_tk = cont_plate_tens_tk_min
    for plate_tk in available_plates:
        if plate_tk >= cont_plate_tens_tk_min:
            cont_plate_tens_tk = plate_tk
            break

    #conisering both plates thickness as same for practical reasons
    if cont_plate_comp_tk > cont_plate_tens_tk:
        cont_plate_tens_tk = cont_plate_comp_tk
    else:
        cont_plate_comp_tk = cont_plate_tens_tk

    welds_sizes = [3, 4, 5, 6, 8, 10, 12, 14, 16]
    # continuity plate weld design on compression side
    # same is assumed for tension side
    cont_web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(cont_plate_comp_tk, column_tw)
    cont_web_weld_size_max = min(beam_tw, cont_plate_comp_tk)
    available_welds = list(filter(lambda x: (cont_web_weld_size_min <= x <= cont_web_weld_size_max), welds_sizes))
    for cont_web_weld_size in available_welds:
        cont_web_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=cont_web_weld_size, fusion_face_angle=90)
        cont_web_weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=cont_web_weld_size, available_length=available_cont_comp_length)
        if (max(p_bf, t_bf)/2) / (2 * cont_web_weld_eff_length * cont_web_weld_throat) <= \
                IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                    ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
            break

    cont_flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(cont_plate_comp_tk, column_tf)
    cont_flange_weld_size_max = max(column_tf, cont_plate_comp_tk)
    available_welds = list(filter(lambda x: (cont_flange_weld_size_min <= x <= cont_flange_weld_size_max), welds_sizes))
    for cont_flange_weld_size in available_welds:
        cont_flange_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=cont_flange_weld_size, fusion_face_angle=90)
        cont_flange_Weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
            fillet_size=cont_flange_weld_size, available_length=available_cont_comp_width)
        cont_axial_stress = (max(p_bf, t_bf)/2) / (4 * cont_flange_Weld_eff_length * cont_flange_weld_throat)
        cont_moment_stress = (max(p_bf, t_bf)/2) * (l_v + beam_tw / 2) / (
                cont_plate_comp_length * cont_flange_weld_throat * 4 * cont_flange_Weld_eff_length)
        if math.sqrt(
                cont_axial_stress ** 2 + cont_moment_stress ** 2) <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
            ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
            break
    # same weld size is considered for flange and web connectivity of continuity plates
    # TODO: Should we recalculate stresses for common weld thickness?
    # TODO: what if this maximum size exceeds limits of one connection?

    cont_weld_size = max(cont_flange_weld_size, cont_web_weld_size)

    #continuity plate warnings
    if math.sqrt(
            cont_axial_stress ** 2 + cont_moment_stress ** 2) >= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
        ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
        logger.warning("weld between column flange and continuity plates is not safe")

    if (max(p_bf, t_bf)/2) / (2 * cont_web_weld_eff_length * cont_web_weld_throat) >= \
            IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                ultimate_stresses=(weld_fu, column_fu, cont_plate_fu)):
        logger.warning("weld between column web and continuity plates is not safe")

    #Note: for more number of iteration more numbers of  available size should be provided

    # Beam stiffeners
    st_status = False
    if endplate_type == 'flush':
        st_number = 0
    elif endplate_type == 'one_way':
        st_number = 1
        if number_of_bolts >= 12:
            st_status = True
    else:
        st_number = 2
        if number_of_bolts >= 20:
            st_status = True

    st_fu = beam_fu
    st_fy = beam_fy
    st_height = l_v + pitch_dist + end_dist
    for plate_tk in available_plates:
        if plate_tk >= beam_tw:
            st_thickness = plate_tk
            break
    st_length = st_height + 100.0
    st_notch_top = 50.0
    st_notch_bottom = round_up(value=weld_thickness_flange, multiplier=5, minimum_value=5)
    st_eff_length = st_length - st_notch_bottom
    st_beam_weld_min = IS800_2007.cl_10_5_2_3_min_weld_size(st_thickness, beam_tf)
    st_beam_weld_max = max(beam_tf, st_thickness)

    if st_status is True:

        while st_length <= 1000:
            st_eff_length = st_length - st_notch_bottom
            st_force = 4 * tension_in_bolt
            st_moment = st_force * (l_v + pitch_dist / 2)
            st_shear_capacity = st_eff_length * st_thickness * st_fy / (math.sqrt(3) * gamma_m0)
            st_moment_capacity = st_eff_length ** 2 * st_thickness * st_fy / (4 * gamma_m0)
            available_welds = list(filter(lambda x: (st_beam_weld_min <= x <= st_beam_weld_max), welds_sizes))
            for st_beam_weld in available_welds:
                if st_beam_weld <= st_beam_weld_min:
                    st_beam_weld = st_beam_weld_min
                st_beam_weld_throat = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
                    fillet_size=st_beam_weld, fusion_face_angle=90)
                st_beam_weld_eff_length = IS800_2007.cl_10_5_4_1_fillet_weld_effective_length(
                    fillet_size=st_beam_weld, available_length=st_eff_length)
                st_weld_shear_stress = st_force / (2 * st_beam_weld_eff_length * st_beam_weld_throat)
                st_weld_moment_stress = st_moment / (2 * st_beam_weld * st_beam_weld_eff_length ** 2 / 4)
                st_eq_weld_stress = math.sqrt(st_weld_shear_stress ** 2 + st_weld_moment_stress ** 2)
                if st_eq_weld_stress <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                        ultimate_stresses=(weld_fu, beam_fu, st_fu)):
                    break
            if st_moment <= st_moment_capacity and st_force <= st_shear_capacity and \
                    st_eq_weld_stress <= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                    ultimate_stresses=(weld_fu, beam_fu, st_fu)):
                break
            else:
                st_length += 20

        # stiffener warnings

        if st_moment >= st_moment_capacity:
            logger.warning("stiffener cannot take moment, current stiffener length %2.2f" % st_length)
        if st_force >= st_shear_capacity:
            logger.warning("stiffener cannot take shear force, current stiffener length %2.2f" % st_length)
        if st_eq_weld_stress >= IS800_2007.cl_10_5_7_1_1_fillet_weld_design_stress(
                ultimate_stresses=(weld_fu, beam_fu, st_fu)):
            logger.warning("stiffener weld cannot take stiffener loads, current weld thickness is %2.2f" % st_beam_weld)

    # Strength of flange under compression or tension TODO: Get function from IS 800

    A_f = beam_B * beam_tf  # area of beam flange
    capacity_beam_flange = (beam_fy / gamma_m0) * A_f
    force_flange = max(t_bf, p_bf)

    if capacity_beam_flange < force_flange:
        design_status = False
        logger.error(": Forces in the beam flange is greater than its load carrying capacity")
        logger.warning(": The maximum allowable force on beam flange of selected section is %2.2f kN"
                       % (round(capacity_beam_flange/1000, 3)))
        logger.info(": Use a higher beam section with wider and/or thicker flange")

    ######################################
    # End of Calculation, SAMPLE Output dictionary
    outputobj = dict()

    # FOR OUTPUT DOCK
    outputobj['Bolt'] = {}
    outputobj["Weld"] = {}
    outputobj['Plate'] = {}
    outputobj['ContPlateTens'] = {}
    outputobj['ContPlateComp'] = {}
    outputobj['Stiffener'] = {}

    outputobj['Bolt']['status'] = design_status
    outputobj['Bolt']['NumberOfBolts'] = int(number_of_bolts)

    outputobj["Bolt"]["ShearBolt"] = float(round(shear_in_bolt/1000, 3))    # kN
    outputobj["Bolt"]["ShearCapacity"] = float(round(bolt_shear_capacity/1000, 3))
    outputobj["Bolt"]["SlipCapacity"] = float(round(bolt_slip_capacity/1000, 3))
    outputobj["Bolt"]["BearingCapacity"] = float(round(bearing_capacity/1000, 3))
    outputobj["Bolt"]["BoltCapacity"] = float(round(bolt_capacity/1000, 3))

    outputobj["Bolt"]["TensionCapacity"] = float(round(bolt_tension_capacity/1000, 3))
    outputobj["Bolt"]["TensionMoment"] = float(round(moment_tension/1000, 3))
    outputobj["Bolt"]["TensionAxial"] = float(round(axial_tension/1000, 3))
    outputobj["Bolt"]["TensionPrying"] = float(round(prying_force/1000, 3))

    outputobj["Bolt"]["TensionBolt"] = float(round(tension_in_bolt/1000, 3))
    outputobj["Bolt"]["CombinedCapacity"] = float(round(combined_capacity, 3))

    # outputobj['Bolt']['BoltFy'] = 0.0
    # outputobj['Bolt']['NumberOfRows'] = int(no_rows)
    # outputobj['Bolt']['BoltsPerColumn'] = 0.0
    # outputobj['Bolt']['Gauge'] = 0.0
    # outputobj['Bolt']['kb'] = 0.0
    # outputobj['Bolt']['SumPlateThick'] = 0.0

    outputobj['Bolt']['CrossCentreGauge'] = float(round(g_1, 3))
    outputobj['Bolt']['End'] = float(round(end_dist, 3))
    outputobj['Bolt']['Edge'] = float(round(edge_dist, 3))
    outputobj['Bolt']['Lv'] = float(round(l_v, 3))
    outputobj['Bolt']['Pitch'] = float(round(pitch_dist, 3))
    outputobj['Bolt']['PitchMini'] = float(round(pitch_dist_min, 3))
    outputobj['Bolt']['PitchMax'] = float(round(pitch_dist_max, 3))
    outputobj['Bolt']['EndMax'] = float(round(end_dist_max, 3))
    outputobj['Bolt']['EndMini'] = float(round(end_dist_min, 3))
    outputobj['Bolt']['DiaHole'] = int(dia_hole)

    outputobj['Plate']['Height'] = float(round(plate_height, 3))
    outputobj['Plate']['Width'] = float(round(plate_width, 3))
    outputobj['Plate']['WidthMin'] = float(round(beam_B, 3))
    # outputobj['Plate']['WidthMax'] = float(round(plate_width + 25.0, 3))
    outputobj['Plate']['Moment'] = float(round(toe_of_weld_moment, 3))
    outputobj['Plate']['be'] = float(round(beam_B/2, 3))
    outputobj['Plate']['fy'] = float(round(end_plate_fy, 3))
    outputobj['Plate']['Thickness'] = float(round(end_plate_thickness, 3))
    outputobj['Plate']['ThickRequired'] = float(round(end_plate_thickness_min, 3))
    outputobj['Bolt']['projection'] = float(round(flange_projection, 3))

    outputobj['ContPlateComp']['Number'] = 2
    outputobj['ContPlateComp']['Length'] = float(round(cont_plate_comp_length, 3))
    outputobj['ContPlateComp']['Width'] = float(round(cont_plate_comp_width, 3))
    outputobj['ContPlateComp']['Thickness'] = float(round(cont_plate_comp_tk, 3))  #TODO bottom continuity plate thickness Anand
    outputobj['ContPlateComp']['ThicknessMin'] = float(round(cont_plate_comp_tk_min, 3))
    outputobj['ContPlateComp']['NotchSize'] = float(round(notch_cont_comp, 3))
    outputobj['ContPlateComp']['Weld'] = float(round(cont_weld_size, 3))  # TODO: Sourabh give calculated values

    outputobj['ContPlateTens']['Number'] = 2
    outputobj['ContPlateTens']['Length'] = float(round(cont_plate_tens_length, 3))
    outputobj['ContPlateTens']['Width'] = float(round(cont_plate_tens_width, 3))
    outputobj['ContPlateTens']['Thickness'] = float(round(cont_plate_tens_tk, 3))          #TODO uper continuity plate thickness Anand
    outputobj['ContPlateTens']['ThicknessMin'] = float(round(cont_plate_tens_tk_min, 3))
    outputobj['ContPlateTens']['NotchSize'] = float(round(notch_cont_tens, 3))
    outputobj['ContPlateTens']['Weld'] = float(round(cont_weld_size, 3))  # TODO: Sourabh give calculated values

    outputobj['Stiffener']['Status'] = st_status
    outputobj['Stiffener']['Number'] = int(st_number)
    outputobj['Stiffener']['Length'] = float(round(st_length, 3))     # TODO:
    outputobj['Stiffener']['Height'] = float(round(st_height, 3))
    outputobj['Stiffener']['Thickness'] = 10.0  # TODO: Sourabh give calculated values
    outputobj['Stiffener']['NotchBottom'] = float(round(st_notch_bottom, 3))
    outputobj['Stiffener']['NotchTop'] = float(round(st_notch_top, 3))
    outputobj['Stiffener']['Weld'] = 8.0    # TODO: Sourabh give calculated values

    # Detailing
    if endplate_type == 'flush':
        if number_of_bolts == 4:
            outputobj['Bolt']['Pitch12'] = float(round(beam_d - 2 * (beam_tf + l_v), 3))

        elif number_of_bolts == 8:
            outputobj['Bolt']['Pitch12'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch23'] = float(round(beam_d - 2 * (beam_tf + l_v + pitch_dist), 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))

        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch12'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(beam_d - 2 * (beam_tf + l_v + 2 * pitch_dist), 3))
            outputobj['Bolt']['Pitch45'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch56'] = float(round(pitch_dist, 3))

        else:
            pass

    elif endplate_type == 'one_way':

        if number_of_bolts == 6:
            outputobj['Bolt']['Pitch12'] = float(round(2 * l_v + beam_tf, 3))
            outputobj['Bolt']['Pitch23'] = float(round(beam_d - 2 * (beam_tf + l_v), 3))

        elif number_of_bolts == 8:
            outputobj['Bolt']['Pitch12'] = float(round(2 * l_v + beam_tf, 3))
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(beam_d - 2 * (beam_tf + l_v + 0.5 * pitch_dist), 3))

        elif number_of_bolts == 10:
            outputobj['Bolt']['Pitch12'] = float(round(2 * l_v + beam_tf, 3))
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch45'] = float(round(beam_d - 2 * (beam_tf + l_v + pitch_dist), 3))

        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch12'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch23'] = float(round(2 * l_v + beam_tf, 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch45'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch56'] = float(round(beam_d - 2 * (beam_tf + l_v + pitch_dist), 3))

        else:
            pass

    else:   #endplate_type == 'both_way':
        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = float(round(beam_d - 2 * (beam_tf + l_v), 3))
            outputobj['Bolt']['Pitch12'] = float(round((2 * l_v + beam_tf), 3))
            outputobj['Bolt']['Pitch23'] = float(round(beam_d - 2 * (beam_tf + l_v), 3))
            outputobj['Bolt']['Pitch34'] = float(round((2 * l_v + beam_tf), 3))

        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch12'] = float(round((2 * l_v + beam_tf), 3))
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(beam_d - 2 * (beam_tf + l_v + pitch_dist), 3))
            outputobj['Bolt']['Pitch45'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch56'] = float(round((2 * l_v + beam_tf), 3))

        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch12'] = float(round((2 * l_v + beam_tf), 3))
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch45'] = float(round(beam_d - 2 * (beam_tf + l_v + 2 * pitch_dist), 3))
            outputobj['Bolt']['Pitch56'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch67'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch78'] = float(round((2 * l_v + beam_tf), 3))

        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch23'] = float(round((2 * l_v + beam_tf), 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch45'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch56'] = float(round(beam_d - 2 * (beam_tf + l_v + 2 * pitch_dist), 3))
            outputobj['Bolt']['Pitch67'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch78'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch89'] = float(round((2 * l_v + beam_tf), 3))
            outputobj['Bolt']['Pitch910'] = float(round(pitch_dist, 3))
        else:
            pass

    if weld_method == 'fillet':
        outputobj["Weld"]["FlangeSizeMin"] = float(round(flange_weld_size_min, 3))
        outputobj["Weld"]["FlangeSizeMax"] = float(round(flange_weld_size_max, 3))
        outputobj["Weld"]["FlangeLengthTop"] = float(round(flange_weld_effective_length_top, 3))
        outputobj["Weld"]["FlangeLengthBottom"] = float(round(flange_weld_effective_length_bottom, 3))
        outputobj["Weld"]["FlangeThroat"] = float(round(flange_weld_throat_size, 3))
        outputobj["Weld"]["FlangeThroatMin"] = float(round(flange_weld_throat_reqd, 3))
        outputobj["Weld"]["FlangeStress"] = float(round(flange_weld_stress, 3))
        outputobj["Weld"]["FlangeStrength"] = float(round(flange_weld_strength, 3))

        outputobj["Weld"]["WebSizeMin"] = float(round(web_weld_size_min, 3))
        outputobj["Weld"]["WebSizeMax"] = float(round(web_weld_size_max, 3))
        outputobj["Weld"]["WebLength"] = float(round(web_weld_effective_length, 3))
        outputobj["Weld"]["WebThroat"] = float(round(web_weld_throat_size, 3))
        outputobj["Weld"]["WebThroatMin"] = float(round(web_weld_throat_reqd, 3))
        outputobj["Weld"]["WebStress"] = float(round(web_weld_stress, 3))
        outputobj["Weld"]["WebStrength"] = float(round(web_weld_strength, 3))

    else:  # weld_method == 'groove':
        outputobj["Weld"]["Size"] = 3
        outputobj["Weld"]["FlangeSize"] = float(round(groove_weld_size_flange, 3))
        outputobj["Weld"]["WebSize"] = float(round(groove_weld_size_web, 3))


    # End of SAMPLE Output dictionary

    if design_status is True:
        logger.info(": Overall end plate moment connection design is safe \n")
        logger.debug(" :=========End Of design===========")
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")

    return outputobj




