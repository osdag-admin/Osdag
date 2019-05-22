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


# #######################################################################
# # Function for fetching column and beam parameters from the database
#
# def fetchColumnPara(self):
#     column_sec = self.ui.combo_Column.currentText()
#     dictcolumndata = get_beamdata(column_sec)
#     return dictcolumndata
#
# def fetchBeamPara(self):
#     beam_sec = self.ui.combo_Beam.currentText()
#     dictbeamdata = get_beamdata(beam_sec)
#     return dictbeamdata
#

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

    if uiObj["Weld"]["Method"] == "Fillet Weld":
        weld_method = 'fillet'
    else:   # "Groove Weld (CJP)"
        weld_method = 'groove'

    weld_thickness_flange = float(uiObj['Weld']['Flange (mm)'])
    weld_thickness_web = float(uiObj['Weld']['Web (mm)'])

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

    beam_tw = float(dictbeamdata["tw"])
    beam_tf = float(dictbeamdata["T"])
    beam_d = float(dictbeamdata["D"])
    beam_B = float(dictbeamdata["B"])
    beam_R1 = float(dictbeamdata["R1"])
    beam_R2 = float(dictbeamdata["R2"])


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

    if conn_type == 'col_web_connectivity':
        bolt_plates_tk = [column_tw, end_plate_thickness]
    else:
        bolt_plates_tk = [column_tf, end_plate_thickness]

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
    l_v = float(50.0)
    flange_projection = 5

    # g_1 = Gauge 1 distance (mm) (also known as cross-centre gauge, Steel designers manual, pp733, 6th edition - 2003)
    g_1 = 100.0

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

                    # TODO Re-detail the connection
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

            elif no_tension_side == 6:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < 2 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # # logger.warning()
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    # TODO Re-detail the connection
                    # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                    #            'out_compression_flange': 0, 'in_compression_flange': 1}

            elif no_tension_side == 8:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
                           'out_compression_flange': 0, 'in_compression_flange': 1}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    # TODO Re-detail the connection
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

            elif no_tension_side == 6:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 2,
                           'out_compression_flange': 1, 'in_compression_flange': 2}
                if beam_d - 2 * beam_tf - 2 * l_v < 3 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # # logger.warning()
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    # TODO Re-detail the connection
                    # no_rows = {'out_tension_flange': 2, 'in_tension_flange': 1,
                    #            'out_compression_flange': 2, 'in_compression_flange': 1}

            elif no_tension_side == 8:
                no_rows = {'out_tension_flange': 1, 'in_tension_flange': 3,
                           'out_compression_flange': 1, 'in_compression_flange': 3}
                if beam_d - 2 * beam_tf - 2 * l_v < 5 * pitch_dist:
                    detailing_status = False
                    # logger.error("Large number of bolts are required for the connection")
                    # logger.info(": Re-design the connection using bolt of higher grade or diameter")

                    # TODO Re-detail the connection
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
            tens_plate_no_pitch = flange_projection
        else:
            tens_plate_no_pitch = end_dist + l_v
        if no_rows['out_compression_flange'] == 0:
            comp_plate_no_pitch = flange_projection
        else:
            comp_plate_no_pitch = end_dist + l_v

        plate_height = (no_rows['out_tension_flange'] + no_rows['out_compression_flange'] - 2) * pitch_dist + \
                       beam_d + comp_plate_no_pitch + tens_plate_no_pitch
        plate_width = g_1 + 2 * edge_dist
        while plate_width < beam_B:
            edge_dist += 5
            plate_width = g_1 + 2 * edge_dist
            if edge_dist > edge_dist_max:
                edge_dist -= 5
                g_1 += 5
                plate_width = g_1 + 2 * edge_dist
                # TODO: Apply max limit for g_1, design fails

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

        moment_tension = factored_moment * extreme_bolt_dist / sigma_yi_sq
        tension_in_bolt = axial_tension + moment_tension + prying_force
        shear_in_bolt = factored_shear_load / number_of_bolts
        # Check for combined tension and shear
        if bolt_type == "Friction Grip Bolt":
            bolt_combined_status = IS800_2007.cl_10_4_6_friction_bolt_combined_shear_and_tension(
                V_sf=shear_in_bolt, V_df=bolt_capacity, T_f=tension_in_bolt, T_df=bolt_tension_capacity) <= 1.0
        else:
            bolt_combined_status = IS800_2007.cl_10_3_6_bearing_bolt_combined_shear_and_tension(
                V_sb=shear_in_bolt, V_db=bolt_capacity, T_b=tension_in_bolt, T_db=bolt_tension_capacity) <= 1.0

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

        # Web welds

        web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(beam_tw, end_plate_thickness)
        web_weld_throat_size = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness(
            fillet_size=weld_thickness_web, fusion_face_angle=90)
        web_weld_throat_max = IS800_2007.cl_10_5_3_1_max_weld_throat_thickness(beam_tw, end_plate_thickness)

        # check min and max weld size

        if weld_thickness_flange <= flange_weld_size_min:
            design_status = False
            logger.error(": The weld size at beam flange is less than required")
            logger.warning(": The minimum required weld size at beam flange is %s mm" % flange_weld_size_min)
            logger.info(": Increase the size of weld at beam flanges")

        if flange_weld_throat_size >= flange_weld_throat_max:
            design_status = False
            logger.error(": The weld size at beam flange is more than allowed")
            logger.warning(": The maximum allowed throat size of weld at flanges is %s mm" % flange_weld_throat_max)
            logger.info(": Decrease the size of weld at beam flanges")

        if weld_thickness_web <= web_weld_size_min:
            design_status = False
            logger.error(": The weld size at beam web is less than required")
            logger.warning(": The minimum required weld size at beam web is %s mm" % web_weld_size_min)
            logger.info(": Increase the size of weld at beam web")

        if web_weld_throat_size >= web_weld_throat_max:
            design_status = False
            logger.error(": The weld size at beam web is more than allowed")
            logger.warning(": The maximum allowed throat size of weld at webs is %s mm" % web_weld_throat_max)
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

        #  Design forces at welds due to loads

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

        web_weld_stress = math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / web_weld_throat_size

        web_weld_throat_reqd = round(math.sqrt(weld_force_axial ** 2 + weld_force_shear ** 2) / web_weld_strength, 3)

        if flange_weld_stress >= flange_weld_strength:
            design_status = False
            logger.error(": The weld size at beam flange is less than required")
            logger.warning(": The minimum required throat size of weld flanges is %s mm" % flange_weld_throat_reqd)
            logger.info(": Increase the size of weld at beam flanges")

        if web_weld_stress >= web_weld_strength:
            design_status = False
            logger.error(": The weld size at beam web is less than required")
            logger.warning(": The minimum required throat size of weld web is %s mm" % web_weld_throat_reqd)
            logger.info(": Increase the size of weld at beam web")

    else:   # weld_method == 'groove'
        groove_weld_size = IS800_2007.cl_10_5_3_3_groove_weld_effective_throat_thickness(
            beam_tf, beam_tw, end_plate_thickness)

    # Continuity Plates on compression side
    cont_plate_fu = beam_fu
    cont_plate_fy = beam_fy
    cont_plate_e = math.sqrt(250/cont_plate_fy)
    gamma_m0 = 1.10
    gamma_m1 = 1.10
    p_bf = factored_moment / (beam_d - beam_tf) - factored_axial_load   # Compressive force at beam flanges

    cont_plate_comp_length = column_d - 2 * column_tf
    cont_plate_comp_width = (column_B - column_tw) / 2
    available_plates = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30]
    for plate_tk in available_plates:
        if plate_tk >= beam_tf:
            cont_plate_tk_flange = plate_tk
            break

    col_web_capacity_yielding = column_tw * (5 * column_tf + 5 * column_R1 + beam_tf) * column_fy / gamma_m0

    col_web_capacity_crippling = ((300 * column_tw ** 2) / gamma_m1) * (
        1 + 3 * (beam_tf / column_d) * (column_tw / column_tf) ** 1.5) * math.sqrt(column_fy * column_tf / column_tw)
    col_web_capacity_buckling = (10710 * (column_tw ** 3) / column_d) * math.sqrt(column_fy / gamma_m0)
    col_web_capacity = max(col_web_capacity_yielding, col_web_capacity_crippling, col_web_capacity_buckling)

    cont_plate_comp_tk_local_buckling = cont_plate_comp_length / (9.4 * cont_plate_e)
    cont_plate_comp_tk_min = max(cont_plate_comp_tk_local_buckling, cont_plate_tk_flange,
                                 (p_bf - col_web_capacity) / (cont_plate_fy / gamma_m0))

    # Continuity Plates on compression side
    cont_plate_tens_length = column_d - 2 * column_tf
    cont_plate_tens_width = (column_B - column_tw) / 2

    t_bf = factored_moment / (beam_d - beam_tf) + factored_axial_load   # Tensile force at beam flanges
    col_flange_tens_capacity = (column_tf ** 2) * beam_fy / (0.16 * gamma_m0)
    cont_plate_tens_tk_min = max(cont_plate_tk_flange, (t_bf - col_flange_tens_capacity) / (cont_plate_fy / gamma_m0))

    # Beam stiffeners
    st_fu = beam_fu
    st_fy = beam_fy
    st_height = l_v + pitch_dist + end_dist
    for plate_tk in available_plates:
        if plate_tk >= beam_tw:
            st_thickness = plate_tk
            break
    st_width = st_height + 100.0
    st_notch_top = 50.0
    st_notch_bottom = round_up(value=weld_thickness_flange, multiplier=5)
    st_beam_weld = 1.0
    st_plate_weld = 10.0

    st_force = 4 * tension_in_bolt
    st_moment = st_force * (l_v + pitch_dist / 2)
    st_eff_length = st_width - st_notch_bottom

    st_shear_capacity = st_eff_length * st_thickness * st_fy / (math.sqrt(3) * gamma_m0)
    st_moment_capacity = st_eff_length ** 2 * st_thickness * st_fy / (4 * gamma_m0)

    st_weld_eff = st_eff_length - 2 * st_beam_weld
    st_weld_shear_capacity = 2 * st_weld_eff * 0.7 * st_beam_weld * st_fu / (math.sqrt(3) * gamma_mw)

    st_shear_stress = st_force / (2 * st_weld_eff * 0.7 * st_beam_weld)

    st_moment_stress = st_moment / (2 * st_beam_weld ** 2 / 4)

    st_eq_weld_stress = math.sqrt(st_shear_stress ** 2 + st_moment_stress ** 2)

    st_weld_fu_gov = min(st_fu, beam_fu, weld_fu)

    st_weld_status = st_eq_weld_stress <= st_weld_fu_gov / (math.sqrt(3) * gamma_mw)


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
      '''

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

    outputobj["Bolt"]["ShearBolt"] = float(round(shear_in_bolt, 3))
    outputobj["Bolt"]["ShearCapacity"] = float(round(bolt_shear_capacity, 3))
    outputobj["Bolt"]["SlipCapacity"] = float(round(bolt_slip_capacity, 3))
    outputobj["Bolt"]["BearingCapacity"] = float(round(bearing_capacity, 3))
    outputobj["Bolt"]["BoltCapacity"] = float(round(bolt_capacity, 3))

    outputobj["Bolt"]["TensionCapacity"] = float(round(bolt_tension_capacity, 3))
    outputobj["Bolt"]["TensionBolt"] = float(round(tension_in_bolt, 3))
    outputobj["Bolt"]["CombinedCapacity"] = float(round(bolt_combined_status, 3))

    outputobj['Bolt']['CrossCentreGauge'] = float(round(g_1, 3))
    outputobj['Bolt']['End'] = float(round(end_dist, 3))
    outputobj['Bolt']['Edge'] = float(round(edge_dist, 3))
    outputobj['Bolt']['Lv'] = float(round(l_v, 3))
    outputobj['Bolt']['PitchMini'] = float(round(pitch_dist_min, 3))
    outputobj['Bolt']['PitchMax'] = float(round(pitch_dist_max, 3))
    outputobj['Bolt']['EndMax'] = float(round(end_dist_max, 3))
    outputobj['Bolt']['EndMini'] = float(round(end_dist_min, 3))
    outputobj['Bolt']['DiaHole'] = int(dia_hole)

    outputobj['Plate']['Height'] = float(round(plate_height, 3))
    outputobj['Plate']['Width'] = float(round(plate_width, 3))
    outputobj['Plate']['Thickness'] = float(round(end_plate_thickness, 3))
    outputobj['Plate']['ThickRequired'] = float(round(end_plate_thickness_min, 3))
    outputobj['Bolt']['projection'] = float(round(flange_projection, 3))

    outputobj['ContPlateComp']['Length'] = cont_plate_comp_length
    outputobj['ContPlateComp']['Width'] = cont_plate_comp_width
    outputobj['ContPlateComp']['Thickness'] = cont_plate_tk_flange  #TODO bottom continuity plate thickness Anand
    outputobj['ContPlateComp']['ThicknessMin'] = cont_plate_comp_tk_min

    outputobj['ContPlateTens']['Length'] = cont_plate_tens_length
    outputobj['ContPlateTens']['Width'] = cont_plate_tens_width
    outputobj['ContPlateTens']['Thickness'] = cont_plate_tk_flange          #TODO uper continuity plate thickness Anand
    outputobj['ContPlateTens']['ThicknessMin'] = cont_plate_tens_tk_min

    outputobj['Stiffener']['Length'] = 300.0     # TODO:
    outputobj['Stiffener']['Height'] = 100.0
    outputobj['Stiffener']['Thickness'] = 10.0
    outputobj['Stiffener']['NotchBottom'] = 15.0
    outputobj['Stiffener']['NotchTop'] = 50.0


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

    else:   # endplate_type == 'both_way':
        if number_of_bolts == 8:
            outputobj['Bolt']['Pitch'] = float(round(beam_d - 2 * (beam_tf + l_v), 3))
        elif number_of_bolts == 12:
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(beam_d - 2 * (beam_tf + l_v + pitch_dist), 3))
            outputobj['Bolt']['Pitch45'] = float(round(pitch_dist, 3))
        elif number_of_bolts == 16:
            outputobj['Bolt']['Pitch23'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch45'] = float(round(beam_d - 2 * (beam_tf + l_v + 2 * pitch_dist), 3))
            outputobj['Bolt']['Pitch56'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch67'] = float(round(pitch_dist, 3))
        elif number_of_bolts == 20:
            outputobj['Bolt']['Pitch12'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch34'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch45'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch56'] = float(round(beam_d - 2 * (beam_tf + l_v + 2 * pitch_dist), 3))
            outputobj['Bolt']['Pitch67'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch78'] = float(round(pitch_dist, 3))
            outputobj['Bolt']['Pitch910'] = float(round(pitch_dist, 3))
        else:
            pass

    if weld_method == 'fillet':
        outputobj["Weld"]["FlangeSizeMin"] = float(round(flange_weld_size_min, 3))
        outputobj["Weld"]["FlangeSizeMax"] = float(round(flange_weld_throat_max, 3))
        outputobj["Weld"]["FlangeLengthTop"] = float(round(flange_weld_effective_length_top, 3))
        outputobj["Weld"]["FlangeLengthBottom"] = float(round(flange_weld_effective_length_bottom, 3))
        outputobj["Weld"]["FlangeThroat"] = float(round(flange_weld_throat_size, 3))
        outputobj["Weld"]["FlangeThroatMin"] = float(round(flange_weld_throat_reqd, 3))
        outputobj["Weld"]["FlangeStress"] = float(round(flange_weld_stress, 3))
        outputobj["Weld"]["FlangeStrength"] = float(round(flange_weld_strength, 3))

        outputobj["Weld"]["WebSizeMin"] = float(round(web_weld_size_min, 3))
        outputobj["Weld"]["WebSizeMax"] = float(round(web_weld_throat_max, 3))
        outputobj["Weld"]["WebLength"] = float(round(web_weld_effective_length, 3))
        outputobj["Weld"]["WebThroat"] = float(round(web_weld_throat_size, 3))
        outputobj["Weld"]["WebThroatMin"] = float(round(web_weld_throat_reqd, 3))
        outputobj["Weld"]["WebStress"] = float(round(web_weld_stress, 3))
        outputobj["Weld"]["WebStrength"] = float(round(web_weld_strength, 3))

    else:  # weld_method == 'groove':
        outputobj["Weld"]["Size"] = float(round(groove_weld_size, 3))

    # End of SAMPLE Output dictionary
    
    if design_status is True:
        logger.info(": Overall extended end plate connection design is safe \n")
        logger.debug(" :=========End Of design===========")
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")

    return outputobj
