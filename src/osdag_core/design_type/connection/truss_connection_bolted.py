from .truss_connection import TrussConnection
from ...design_report.reportGenerator_latex import CreateLatex
from ...utils.common.component import *
from ...utils.common.material import *
from ...Report_functions import *
import logging


class TrussConnectionBolted(TrussConnection):

    def __init__(self):
        super(TrussConnectionBolted, self).__init__()



    def tab_list(self):
        tabs = []

        return tabs

    def tab_value_changed(self):
        change_tab = []

        return change_tab

    def input_dictionary_design_pref(self):
        design_input = []

        return design_input

    def input_dictionary_without_design_pref(self):
        design_input = []

        return design_input

    # Setting up logger and Input and Output Docks
    ####################################

    def set_osdaglogger(key):

        global logger
        logger = logging.getLogger('Osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def module_name(self):
        return KEY_DISP_TRUSS_BOLTED

    def member(self, status):
        member = []

        return member

    def input_values(self):

        '''
        Fuction to return a list of tuples to be displayed as the UI.(Input Dock)

        e.g.
        t = (Key, Key_display, Type, existing_val, Current_Value, enabled/disabled, Validator_type)
        '''


        self.module = KEY_DISP_TRUSS_BOLTED

        options_list = []

        t16 = (KEY_MODULE, KEY_DISP_TRUSS_BOLTED, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t16)

        t0 = (KEY_MEMBERS, KEY_DISP_MEMBERS, TYPE_COMBOBOX_CUSTOMIZED, VALUES_MEMBERS, True, 'No Validator')
        options_list.append(t0)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t1)

        t00 = (KEY_TABLE, '', TYPE_TABLE_IN, None, True, 'No Validator')
        options_list.append(t00)

        t9 = (None, DISP_TITLE_BOLT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_D, KEY_DISP_D, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, VALUES_TYP, True, 'No Validator')
        options_list.append(t11)

        t15 = (KEY_COF, KEY_DISP_COF, TYPE_TEXTBOX, None, True, 'No Validator')
        options_list.append(t15)

        t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, VALUES_GRD, True, 'No Validator')
        options_list.append(t12)

        t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, VALUES_D, True, 'No Validator')
        options_list.append(t14)

        return options_list



    def spacing(self, status):

        spacing = []

        return spacing

    def summary(self, status):
        summary = []

        t1 = (KEY_TABLE, '', TYPE_TABLE_OU, '')
        summary.append(t1)

        return summary




    def output_values(self, flag):
        '''
        Fuction to return a list of tuples to be displayed as the UI.(Output Dock)
        '''

        # @author: Umair

        out_list = []

        t1 = (None, "Bolt Design Summary", TYPE_TITLE, None, True)
        out_list.append(t1)

        t00 = (KEY_TABLE, '', TYPE_TABLE_OU, None, True, 'No Validator')
        out_list.append(t00)

        t2 = (KEY_OUT_SPACING, KEY_OUT_DISP_SPACING, TYPE_OUT_BUTTON, ['Spacing Details', self.spacing], True)
        out_list.append(t2)

        t3= (None, "Gusset Plate Detail", TYPE_TITLE, None, True)
        out_list.append(t3)

        t4 = (KEY_TABLE, '', TYPE_TABLE_GUS, None, True, 'No Validator')
        out_list.append(t4)

        return out_list


    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('Truss Connection Bolted', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Truss Connection Bolted':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        #ui.commLogicObj.display_3DModel("Plate", bgcolor)




# # Author: Devesh Kumar
#
# from utils.common.component import Bolt
# import copy
# from utils.common.common_calculation import *
# import math
# from utils.common.is800_2007 import IS800_2007
#
# """ ======The input values start here====== """
#
# """ These values are to be extracted from the input provided by the users """
# no_of_members = 4
# """ this number of members info is not being used directly in the code """
#
# """ List of details of members
# i.e.[section_profile, conn_part_width(mm), conn_part_t(mm), fu_memb(MPa), fy_memb(MPa), member_type,
#      angle from x-axis(in deg), gross area(mm2), h1(mm)]
#      here h1(mm) is the width available for bolt accommodation = conn_part_width - t_flanges - root_radi
# starting from 1st member and proceeding one by one.
# member_type means 'tension' or 'compression' or 'compression_butting' (str) """
# # be careful while connecting the input values of gross area of back to back members (2Area) and star-angles(1 Area with
# # halved load)
# member_details = [['Back to Back Angles', 80, 10, 410, 250, 'tension', 0, 3000, 62],
#                   ['Back to Back Angles', 70, 10, 410, 250, 'tension', 180, 2600, 53],
#                   ['Angles', 75, 8, 410, 250, 'tension', 240, 1140, 55],
#                   ['Angles', 60, 6, 410, 250, 'tension', 270, 684, 47.5],
#                   ]
#
#                   #['Angles', 75, 8, 410, 250, 'compression', 180, 938, 55.5],
#                   #['Angles', 65, 6, 410, 250, 'compression', 225, 625, 53],
#                   #['Angles', 80, 8, 410, 250, 'tension', 270, 978, 65],
#                   #['Angles', 65, 8, 410, 250, 'tension', 315, 817, 51],
#                   #]
#
# """ here type of bolt may be 'Bearing' or 'Friction'. It is also mandatory to connect the input values such that
#  the values inside the 'grade' and the 'Diameter'(mm) key are in ascending order to avoid any unforeseen error
# here grade can be like [4.6, 4.8, 6.8], Diameter like [8, 10, 12, 20, 32] """
# bolts_details = {'type': 'Bearing', 'grade': [4.6], 'Diameter': [10, 12], 'mu_f': 0.2}
#
# """List of the input of the [thickness, fu_plate, fy_plate] of gusset plate"""
# """ Note that currently at least one plate should be having thickness grater than the thickness of any of the members
# in the input """
# plate_details = [[6, 410, 250],
#                  [8, 410, 250],
#                  [12, 410, 250]
#                  ]
#
#
# """ List of axial load (in KN)  on the members starting from 1st member and proceeding one by one """
# # beware of connecting the load inputs of star angles. the load should be divided by 2 because further design will be
# # done considering one of the angles of star angle as a single angle but whitmore width will consider both angles
# load_details = [225, 180, 110, 75]
#
# """ ======The input values end here====== """
#
#
# class bolt_general():
#     def __init__(self, grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail):
#         self.grade = grade
#         self.bolt_dia = bolt_dia
#         """ conn_plates_t_fu_fy - List of tuples with plate thicknesses in mm, fu in MPa, fy in MPa (list of tuples)"""
#         self.connection_plates_t_fu_fy = connection_plates_t_fu_fy
#         """ connection_plates_t - List or tuple of thicknesses in mm of connected plates, the first entry being the
#         thickness of gusset plate"""
#         self.connection_plates_t = connection_plates_t
#         """ example of member_detail - ['Angles', 70, 8, 410, 250, 'tension', 0, 858, 55.5] """
#         self.member_detail = member_detail
#         self.bolt_hole_dia = IS800_2007.cl_10_2_1_bolt_hole_size(bolt_dia, 'Standard')
#         self.fu_b = bolt_general.f_u_bolt(grade=grade, bolt_dia=bolt_dia)
#         self.min_edge_dist = IS800_2007.cl_10_2_4_2_min_edge_end_dist(d=self.bolt_dia, bolt_hole_type='Standard',
#                                                                       edge_type='Sheared or hand flame cut')
#         self.max_edge_dist = IS800_2007.cl_10_2_4_3_max_edge_dist(self.connection_plates_t_fu_fy, False)
#         self.max_spacing = IS800_2007.cl_10_2_3_1_max_spacing(self.connection_plates_t)
#         self.min_pitch = IS800_2007.cl_10_2_2_min_spacing(d=bolt_dia)
#         self.max_pitch = IS800_2007.cl_10_2_3_2_max_pitch_tension_compression(d=bolt_dia,
#                                                                               plate_thicknesses=self.connection_plates_t,
#                                                                               member_type=self.member_detail[5])
#         self.pitch_provided = min(round_up(self.min_pitch, 5), round_down(self.max_pitch, 5))
#         self.edge_dist_provided = min(round_up(self.min_edge_dist, 5), round_down(self.max_edge_dist, 5))
#         self.n_n = bolt_general.get_n_n(section_profile=self.member_detail[0])
#         self.a_nb = bolt_general.get_a_nb(bolt_dia=self.bolt_dia)
#         self.a_sb = round(math.pi / 4 * bolt_dia ** 2)
#
#
#     @staticmethod
#     def get_n_n(section_profile):
#         """This will provide the number of shear planes intercepting the bolt.
#            the connection location will be specified by the user in each of the member case"""
#         if section_profile in ['Angles', 'Channels', 'Star Angles']:
#             return 1
#         elif section_profile in ['Back to Back Angles', 'Back to Back Channels']:
#             return 2
#
#     @staticmethod
#     def get_a_nb(bolt_dia):
#         return round(0.78 * math.pi / 4 * bolt_dia ** 2, 2)
#
#     @staticmethod
#     def f_u_bolt(grade, bolt_dia):
#         """returns the ultimate strength of the bolt as per Table -1 of IS 800: 2007"""
#         grade = float(grade)
#         bolt_dia = float(bolt_dia)
#
#         if grade == 8.8 and bolt_dia <= 16:
#             return 800
#         elif grade == 8.8:
#             return 830
#         else:
#             fu_data = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 9.8: 900, 10.9: 1040, 12.9: 1220}
#             return fu_data[grade]
#
#     @staticmethod
#     def cl_10_2_1_bolt_hole_size(d, bolt_hole_type='Standard'):
#         """Calculate bolt hole diameter as per Table 19 of IS 800:2007
#         Args:
#              d - Nominal diameter of fastener in mm (float)
#              bolt_hole_type - Either 'Standard' or 'Over-sized' or 'short_slot' or 'long_slot' (str)
#         Returns:
#             bolt_hole_size -  Diameter of the bolt hole in mm (float)
#         Note:
#             Reference:
#             IS 800, Table 19 (Cl 10.2.1)
#         TODO:ADD KEY_DISP for for Standard/oversize etc and replace these strings
#         """
#         table_19 = {
#             "12-14": {'Standard': 1.0, 'Over-sized': 3.0, 'short_slot': 4.0, 'long_slot': 2.5},
#             "16-22": {'Standard': 2.0, 'Over-sized': 4.0, 'short_slot': 6.0, 'long_slot': 2.5},
#             "24": {'Standard': 2.0, 'Over-sized': 6.0, 'short_slot': 8.0, 'long_slot': 2.5},
#             "24+": {'Standard': 3.0, 'Over-sized': 8.0, 'short_slot': 10.0, 'long_slot': 2.5}
#         }
#
#         d = int(d)
#
#         if d < 12:
#             clearance = 0
#         elif d <= 14:
#             clearance = table_19["12-14"][bolt_hole_type]
#         elif d <= 22:
#             clearance = table_19["16-22"][bolt_hole_type]
#         elif d <= 24:
#             clearance = table_19["24"][bolt_hole_type]
#         else:
#             clearance = table_19["24+"][bolt_hole_type]
#         if bolt_hole_type == 'long_slot':
#             bolt_hole_size = (clearance + 1) * d
#         else:
#             bolt_hole_size = clearance + d
#         return bolt_hole_size
#
#
# class bearing_bolt(bolt_general):
#     def __init__(self, grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail, joint_length=0):
#         super().__init__(grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail)
#         # joint_length(lj) is the distance between the first and the last row of joint in the direction of load
#         self.joint_length = joint_length
#         self.beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(d=self.bolt_dia, l_j=self.joint_length)
#         # considering no packing plates to be used in the gusset connection, taking beta_pkg = 1
#         self.beta_pkg = 1
#         self.grip_length = sum(self.connection_plates_t)
#         self.beta_lg = IS800_2007.cl_10_3_3_2_bolt_large_grip(d=self.bolt_dia, l_g=self.grip_length,
#                                                               l_j=self.joint_length)
#         self.t_bearing = min(self.connection_plates_t[0], (sum(self.connection_plates_t) - self.connection_plates_t[0]))
#
#     def bearing_bolt_design_capacity(self):
#         v_dsb = self.beta_lj * self.beta_lg * self.beta_pkg * \
#                 IS800_2007.cl_10_3_3_bolt_shear_capacity(f_ub=self.fu_b, A_nb=self.a_nb, A_sb=self.a_sb, n_n=self.n_n)
#         v_dpb = IS800_2007.cl_10_3_4_bolt_bearing_capacity(f_u=self.member_detail[3], f_ub=self.fu_b, t=self.t_bearing,
#                                                            d=self.bolt_dia, e=self.edge_dist_provided,
#                                                            p=self.pitch_provided, bolt_hole_type='Standard')
#
#         v_db = min(v_dsb, v_dpb)
#         return round(v_db/1000, 3)
#
#
# class friction_bolt(bolt_general):
#     def __init__(self, grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail, mu_f=0.2):
#         super().__init__(grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail)
#         self.mu_f = mu_f
#
#     def friction_bolt_design_capacity(self):
#         v_dsf = IS800_2007.cl_10_4_3_bolt_slip_resistance(f_ub=self.fu_b, A_nb=self.a_nb, n_e=self.n_n,
#                                                           mu_f=self.mu_f, bolt_hole_type='Standard',
#                                                           slip_resistance='ultimate_load')
#         return round(v_dsf[0]/1000, 3)
#
#
# """ creating some miscellaneous functions to be used in this module """
# def sort_abs_desc(lst):
#     """
#     Sort a list of integers in descending order of their absolute values.
#     Return two lists: the sorted list of absolute values, and the corresponding indexes in the input list.
#     """
#     # Create a list of tuples (value, index) to keep track of the original indexes
#     lst_with_index = [(abs(xy), ij) for ij, xy in enumerate(lst)]
#     # Sort the list of tuples in descending order of the absolute values
#     sorted_lst_with_index = sorted(lst_with_index, reverse=True)
#     # Create the two output lists by extracting the values and indexes from the sorted tuples
#     sorted_abs_lst = [xy[0] for xy in sorted_lst_with_index]
#     sorted_index_lst = [xy[1] for xy in sorted_lst_with_index]
#     return sorted_abs_lst, sorted_index_lst
#
#
# """ function to sort two list w.r.t first list by parallel iteration """
# def sort_two_lists(list1, list2):
#     """
#     Sort the first list in ascending order and return the corresponding
#     values in the second list.
#     """
#     sorted_list1, sorted_list2 = zip(*sorted(zip(list1, list2)))
#     return list(sorted_list1), list(sorted_list2)
#
# """ function to sort 5 lists w.r.t the first one"""
# def sort_five_lists(list1, list2, list3, list4, list5):
#     """
#     Sort the first list in ascending order and return the corresponding
#     values in the second, third, fourth, and fifth lists.
#     """
#     sorted_lists = sorted(zip(list1, list2, list3, list4, list5))
#     sorted_list1, sorted_list2, sorted_list3, sorted_list4, sorted_list5 = zip(*sorted_lists)
#     return list(sorted_list1), list(sorted_list2), list(sorted_list3), list(sorted_list4), list(sorted_list5)
#
#
# """ creating a function to get the clearance distance d from the origin of any member """
# def get_clearance_d(alpha ,p0 , p1):
#     if alpha == 180:
#         return 2.5
#     elif alpha < 180:
#         alpha = math.radians(alpha)
#         c = p0/p1
#         c1 = (c*math.sin(alpha))/(1+c*math.cos(alpha))
#         beta = math.atan(c1)
#         d = p0/math.tan(beta)
#         return round_up(d, 5)
#         # increased the calculated value by 5mm to provide some space between members on the plate
#     elif alpha > 180:
#         return
#
#
# """ function to get quadrant from a given angle """
# def get_quadrant(angle):
#     if 0 <= angle <= 90:
#         return 1
#     elif 90 < angle <= 180:
#         return 2
#     elif 180 < angle < 270:
#         return 3
#     elif 270 <= angle <= 360:  # actually 360 = 0 therefore input should not accept 360 instead that 0 should be input
#         return 4
#
#
# """function to get included angle where included angle is the angle less than 180degrees between two lines. no need to
# worry about the sequence of the angles. the angles should be positive and not greater than 360 """
#
#
# def get_included_angle(theta1, theta2):
#     if abs(theta1-theta2) <= 180:
#         return abs(theta1-theta2)
#     elif abs(theta1-theta2) > 180:
#         return 360-abs(theta1-theta2)
#
#
# """ function to get the value of d - the clearance for all members"""
# # defining a function which take lists [a,b,angle] for previous and the current member respectively and return p,p1
# def get_d(prev_memb_a_b_angle, current_memb_a_b_angle):
#     quad1 = get_quadrant(prev_memb_a_b_angle[2])
#     quad2 = get_quadrant(current_memb_a_b_angle[2])
#     angle1 = prev_memb_a_b_angle[2]
#     angle2 = current_memb_a_b_angle[2]
#     a1 = prev_memb_a_b_angle[0]
#     b1 = prev_memb_a_b_angle[1]
#     a2 = current_memb_a_b_angle[0]
#     b2 = current_memb_a_b_angle[1]
#     inc_angle = get_included_angle(current_memb_a_b_angle[2], prev_memb_a_b_angle[2])
#
#     """ initialising and assigning p0 and p1 """
#     p0 = 1
#     p1 = 1
#
#     if quad1 == 1 and quad2 == 1:
#         if angle1 < angle2:
#             p0 = b2
#             p1 = a1
#         elif angle1 > angle2:
#             p0 = a2
#             p1 = b1
#     elif quad1 == 2 and quad2 == 2:
#         if angle1 < angle2:
#             p0 = a2
#             p1 = b1
#         elif angle1 > angle2:
#             p0 = b2
#             p1 = a1
#     elif quad1 == 3 and quad2 == 3:
#         if angle1 < angle2:
#             p0 = a2
#             p1 = b1
#         elif angle1 > angle2:
#             p0 = b2
#             p1 = a1
#     elif quad1 == 4 and quad2 == 4:
#         if angle1 < angle2:
#             p0 = b2
#             p1 = a1
#         elif angle1 > angle2:
#             p0 = a2
#             p1 = b1
#     elif quad1 == 1 and quad2 == 2:
#         p0 = a2
#         p1 = a1
#     elif quad1 == 2 and quad2 == 3:
#         p0 = a2
#         p1 = b1
#     elif quad1 == 3 and quad2 == 4:
#         p0 = b2
#         p1 = b1
#     elif quad1 == 4 and quad2 == 1:
#         p0 = b2
#         p1 = a1
#     elif quad1 == 1 and quad2 == 3:
#         if abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) < 180:
#             p0 = a2
#             p1 = a1
#         elif abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) > 180:
#             p0 = b2
#             p1 = b1
#     elif quad1 == 2 and quad2 == 4:
#         if abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) < 180:
#             p0 = b2
#             p1 = b1
#         elif abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) > 180:
#             p0 = a2
#             p1 = a1
#     elif quad1 == 3 and quad2 == 1:
#         if abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) < 180:
#             p0 = b2
#             p1 = b1
#         elif abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) > 180:
#             p0 = a2
#             p1 = a1
#     elif quad1 == 4 and quad2 == 2:
#         if abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) < 180:
#             p0 = a2
#             p1 = a1
#         elif abs(current_memb_a_b_angle[2] - prev_memb_a_b_angle[2]) > 180:
#             p0 = b2
#             p1 = b1
#     elif quad1 == 1 and quad2 == 4:
#         p0 = a2
#         p1 = b1
#     elif quad1 == 2 and quad2 == 1:
#         p0 = a2
#         p1 = a1
#     elif quad1 == 3 and quad2 == 2:
#         p0 = b2
#         p1 = a1
#     elif quad1 == 4 and quad2 == 3:
#         p0 = b2
#         p1 = b1
#
#     return get_clearance_d(inc_angle, p0, p1)
#
#
# """ function for rotation of angles. input will be list of tuples (x,y) which is to be rotated with same angle in
# anti-clock wise direction """
# def rotate_points(points, angle):
#     # Convert angle from degrees to radians
#     angle = math.radians(angle)
#     # Initialize empty list to store rotated points
#     rotated_points = []
#     # Loop over input points
#     for x, y in points:
#         # Apply rotation formula to each point
#         x_rotated = round((x * math.cos(angle) - y * math.sin(angle)), 2)
#         y_rotated = round(x * math.sin(angle) + y * math.cos(angle), 2)
#         # Add rotated point to list
#         rotated_points.append((x_rotated, y_rotated))
#     # Return list of rotated points
#     return rotated_points
#
#
# """ function to give sides of a polynomial"""
# def polygon_side_lengths(vertices):
#     """
#     Takes a list of vertices of a polygon in the form of tuples and returns
#     the length of each side of the polygon.
#     """
#     side_lengths = []
#     n = len(vertices)
#     for ijk in range(n):
#         x__1, y__1 = vertices[ijk]
#         x__2, y__2 = vertices[(ijk+1) % n]
#         side_length = round(math.sqrt((x__2 - x__1)**2 + (y__2 - y__1)**2), 1)
#         side_lengths.append(side_length)
#     return side_lengths
#
#
# """ defining a function to get the design compressive strength of a gusset plate """
#
#
# def gusset_design_comp_strength(whitmore_width_guss, sec_thick, clearance_d, fy_guss):
#     """ radius of gyration taken as 0.2887*thickness considering buckling of rectangle section with
#     whitmore_width and  sec_thick(gusset plate thickness) as its dimension """
#     rad_gyr = 0.2887*sec_thick
#     k_l = 2*clearance_d
#     # here clearance_d is offset from origin and k is taken 2 considering 1st case of table 11(IS800:2007)
#     mod_elasticity = 2*10**5  # Modulus of elasticity in MPa
#     """ f_cc is Euler buckling stress """
#     f_cc = (math.pi**2*mod_elasticity)/((k_l/rad_gyr)**2)
#     lembda_guss = (fy_guss/f_cc)**0.5
#     """ considering the section as the buckling class c as per table 10 of IS800:2007 and hence alpha = 0.49 """
#     alpha_guss = 0.49
#     phi_guss = 0.5*(1+alpha_guss*(lembda_guss-0.2)+lembda_guss**2)
#     gamma_m0_guss = 1.1
#     f_cd = min((fy_guss/gamma_m0_guss)/(phi_guss+(phi_guss**2-lembda_guss**2)**0.5), fy_guss/gamma_m0_guss)
#     p_d = round((f_cd * whitmore_width_guss * sec_thick)/1000, 3)  # divided by 1000 to convert to KN
#     return p_d
#
#
# def calculate_side_lengths(A):
#     # Select every odd-numbered point starting from the third point
#     odd_points = A[2:(len(A) - 2):2]
#
#     # Select every even-numbered point starting from the fourth point
#     even_points = A[3:(len(A) - 2):2]
#
#     # Pair the odd-numbered points with the next even-numbered point
#     pairs = zip(odd_points, even_points)
#
#     # Calculate the distance between each pair of points and store them in a list
#     lengths = [math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) for ((x1, y1), (x2, y2)) in pairs]
#
#     return lengths
#
#
# def calculate_even_side_lengths(poly):
#     # Calculate the total number of vertices
#     n = len(poly)
#
#     # Initialize an empty list to store the side lengths
#     side_lengths = []
#
#     # Loop over every even-numbered vertex and calculate the distance to the next vertex
#     for i in range(0, n, 2):
#         x1, y1 = poly[i]
#         x2, y2 = poly[(i + 1) % n]
#         side_length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
#         side_lengths.append(side_length)
#
#     return side_lengths
#
#
# """ starting the loop for the truss connection design. starting with selecting a thickness of a gusset plate and
# then for the same thickness all the joining members are designed for the available bolts. In the available bolts the
# bolts that can be suitably used will be stored and later the bolts common to all the members or most suitable
# bolt design will be selected"""
#
# """ starting with selecting and deciding the thicknesses of the gusset plate for which the loop has to run """
#
# """ selecting the thickness of thickest connected member and for that first creating the list of thickness
# of all the connected members named member_thickness_iter """
# member_thickness_iter = []
# for i in range(len(member_details)):
#     member_thickness_iter.append(member_details[i][2])
#
#
# """Creating a list of input plate thickness having thickness greater than the max of thickness of all the members as it
# is a thumb rule to take the thickness of the gusset plate greater than the thickness of any connecting member
# plate_details_iter is a list - [gusset thickness, fu of gusset plate, fy of gusset plate]
# member_detail_iter - [section_profile, conn_part_width, conn_part_t, fu_memb, fy_memb, member_type, angle, A_g, h1]
#  here h1(mm) is the width available for bolt accommodation = conn_part_width - t_flanges - root_radius """
# plate_details_iter = []
# for i in range(len(plate_details)):
#     if plate_details[i][0] > max(tuple(member_thickness_iter)):
#         plate_details_iter.append(plate_details[i])
#
# large_grip1 = False
# safe_whitmore_section = True
# gusset_block_shear_failure = False
# mem_width_too_large = False
# """ Starting the loop of gusset plate """
# for i in range(len(plate_details_iter)):
#     selected_gusset = plate_details_iter[i]
#     """ defining candidate_bolts_all to store the eligible bolts for all the members. it is as follows:
#     candidate_bolts_all = [[candidate_bolt1 of member1],[candidate_bolt1 of member2],[candidate_bolt1 of member3]]"""
#     candidate_bolts_all = []
#
#     """gusset_plate_t_fu_fy - [thickness, fu_plate, fy_plate] of gusset plate"""
#     gusset_plate_t_fu_fy = plate_details_iter[i]
#
#     design_load_all = []
#
#     for j in range(len(member_details)):
#         """ candidate_bolts1 is the list which will store all the combination of diameter and grade of bolt which can
#         be used for the connection of that member. It will be empty for every value of j. the assignment of this
#         variable to an empty list will be done after adding this list to another list which stores such list for all
#         the members. it will look as follows:
#         candidate_bolts1 = [[recommended_bolt of 1st dia-grade combination],
#         [recommended_bolt of 2nd dia-grade combination],[recommended_bolt of 3rd dia-grade combination],....]"""
#         candidate_bolts1 = []
#
#         """ member_detail_iter is the variable having detail of that member
#         e.g ['Angles', 70, 8, 410, 250, 'tension', 0, 858, 55.5]
#         for which the iteration of the bolt design is to run """
#         member_detail_iter = member_details[j]
#
#         """ member_t_fu_fy is the list of tuples of t, fu, fy of the member under consideration """
#         if member_detail_iter[0] in ['Angles', 'Channels', 'Star Angles']:
#             member_t_fu_fy = [(member_detail_iter[2], member_detail_iter[3], member_detail_iter[4])]
#         elif member_detail_iter[0] in ['Back to Back Angles', 'Back to Back Channels']:
#             member_t_fu_fy = [(member_detail_iter[2], member_detail_iter[3], member_detail_iter[4])] * 2
#
#         """connection_plates_t_fu_fy_iter is the list of tuples of the   plate and members containing
#         their (thickness,fu,fy) like [(12, 410, 250), (8, 410, 250)]. The first tuple should be the detail of the
#         gusset plate and the following are the member detail. Number of tuples will be 3 for back to back conn"""
#         connection_plates_t_fu_fy_iter = [tuple(gusset_plate_t_fu_fy)] + member_t_fu_fy
#
#         """note that the first entry i.e. the 0th index is the thickness of gusset and the subsequent are
#          member e.g. thickness_connection_plates_t_iter = [12, 8]"""
#         if member_detail_iter[0] in ['Angles', 'Channels', 'Star Angles']:
#             thickness_connection_plates_t_iter = [connection_plates_t_fu_fy_iter[0][0],
#                                                   connection_plates_t_fu_fy_iter[1][0]]
#         elif member_detail_iter[0] in ['Back to Back Angles', 'Back to Back Channels']:
#             thickness_connection_plates_t_iter = [connection_plates_t_fu_fy_iter[0][0],
#                                                   connection_plates_t_fu_fy_iter[1][0],
#                                                   connection_plates_t_fu_fy_iter[2][0]]
#
#         """ design_load_all is the list of load for which the members are being designed and design_load_iter is the
#          load for which the member under the current loop has to be designed """
#
#         design_load_iter = round(max(abs(load_details[j]), (
#                     0.3 * IS800_2007.cl_6_2_tension_yielding_strength(member_detail_iter[7],
#                                                                       member_detail_iter[4])/1000)), 3)
#
#         design_load_all = design_load_all + [design_load_iter]
#
#         """ bolt_dia_iter is a list having all the input bolt diameter e.g [8, 10, 12, 20, 32] """
#         bolt_dia_iter = bolts_details['Diameter']
#         bolt_grade_iter = bolts_details['grade']
#         for k in range(len(bolt_dia_iter)):
#             bolt_dia1 = bolt_dia_iter[k]
#
#             """ Now running a loop for every grade of bolts in the list of input grades of the bolt """
#             for l in range(len(bolt_grade_iter)):
#                 bolt_grade1 = bolt_grade_iter[l]
#
#                 """ creating an instance named bolt1 from the bearing bolt class or friction bolt class
#                 depending upon the input """
#                 joint_len = 0
#                 mu_f1 = 0.2
#                 if bolts_details['type'] == 'Bearing':
#                     bolt1 = bearing_bolt(grade=bolt_grade1, bolt_dia=bolt_dia1,
#                                          connection_plates_t_fu_fy=connection_plates_t_fu_fy_iter,
#                                          connection_plates_t=thickness_connection_plates_t_iter,
#                                          member_detail=member_detail_iter, joint_length=joint_len)
#                 else:
#                     bolt1 = friction_bolt(grade=bolt_grade1, bolt_dia=bolt_dia1,
#                                           connection_plates_t_fu_fy=connection_plates_t_fu_fy_iter,
#                                           connection_plates_t=thickness_connection_plates_t_iter,
#                                           member_detail=member_detail_iter, mu_f=mu_f1)
#
#                 """ using large grip criteria as per Cl 10.3.3.2 of IS800:2007, ensuring the minimum dia bolt for which
#                  the loop should run """
#                 large_grip1 = False
#                 if bolt_dia1 <= sum(thickness_connection_plates_t_iter) / 8:
#                     large_grip1 = True
#                     """ coming out of the bolt grade loop """
#                     break
#
#                 """ Condition to ensure that the bolt dia selected will be able to be accommodated in the connected
#                 part of the member. number of bolt lines(no_rows) possible** = round_down((h1 - 2e_min)/gauge_dist) + 1
#                 here for simplicity gauge dist has been taken as the pitch.
#                 Note - rows means bolt lines along the direction of load applied
#                     columns means bolt line perpendicular to the direction of load applied """
#                 no_rows = round_down((member_detail_iter[8] - 2 * bolt1.edge_dist_provided) / bolt1.pitch_provided + 1)
#                 if no_rows < 1:
#                     """ coming out of the bolt grade loop """
#                     break
#
#                 """ the edge distance, gauge and pitch used are represented as follows by edge_dist1, gauge1
#                 and pitch1 . edge_dist2 is the distance towards the toe side of an angle"""
#                 edge_dist1 = bolt1.edge_dist_provided
#                 edge_dist2 = edge_dist1
#                 if no_rows == 1:
#                     gauge1 = 0
#                 else:
#                     gauge1 = min((member_detail_iter[8] - 2 * edge_dist1) / (no_rows - 1), bolt1.max_spacing)
#
#                 pitch1 = bolt1.pitch_provided
#
#
#                 """ finding the bolt capacity (bolt_capacity1) of the selected bolt and grade """
#                 bolt_capacity1 = 0
#                 if bolts_details['type'] == 'Bearing':
#                     bolt_capacity1 = bolt1.bearing_bolt_design_capacity()
#                 else:
#                     bolt_capacity1 = bolt1.friction_bolt_design_capacity()
#
#                 no_bolts1 = round_up((design_load_iter/bolt_capacity1), 1)
#                 """ there should at least be two numbers of bolts in a connection. if number of bolts are less than 2
#                 then the grade loop has to be broken because one bolt may not resist the rotation of member and in turn
#                 make the line of action of axial forces non-concurrent.
#                 For this it is mandatory that the list of grade is in ascending order """
#                 if no_bolts1 < 2:
#                     break
#
#                 for o in range(no_rows):
#                     no_rows1 = o+1
#                     no_column1 = round_up((no_bolts1/no_rows1), 1)
#                     """ Note - The arrangement of the bolts are in chain pattern not in staggered or diamond pattern
#                     therefore the number of bolts = rows*columns
#                     rows means bolt lines along the direction of load applied
#                     columns means bolt line perpendicular to the direction of load applied """
#                     no_bolts2 = no_rows1*no_column1
#                     """ now joint length = (columns - 1)*pitch """
#                     joint_len = (no_column1-1)*pitch1
#                     """if it is found that the joint length is less than 15d then that number of row is selected and
#                     the loop is broken. if the joint length exceeds 15d even after accommodating the bolts in the
#                     maximum possible number of rows then that maximum possible number of rows will be the selected
#                     number of rows"""
#                     if joint_len < 15*bolt_dia1:
#                         break
#
#                 """ calculating the total bolt capacity"""
#                 bolt_group_capacity1 = 0
#                 if bolts_details['type'] == 'Bearing':
#                     bolt_group_capacity1 = no_bolts2*bolt1.bearing_bolt_design_capacity()
#                 else:
#                     bolt_group_capacity1 = no_bolts2*bolt1.friction_bolt_design_capacity()
#
#                 """ increasing the number of bolts by increasing one one column in case the bolt group capacity is
#                 less than the design load. the no. of times the while loop iterates is limited to 10 in order to escape
#                 from entering into an infinite loop in any case """
#                 count1 = 1
#                 while bolt_group_capacity1 < design_load_iter and count1 < 10:
#                     count1 = count1+1
#                     no_column1 = no_column1 + 1
#                     no_bolts2 = no_rows1 * no_column1
#                     joint_len = (no_column1 - 1) * pitch1
#                     if bolts_details['type'] == 'Bearing':
#                         bolt_group_capacity1 = no_bolts2 * bolt1.bearing_bolt_design_capacity()
#                     else:
#                         bolt_group_capacity1 = no_bolts2 * bolt1.friction_bolt_design_capacity()
#
#                 """ ensuring that the member is not so much big that the bolt's end distance becomes grater than the
#                 maximum edge distance. here we are using the whole width of the connected member because we are looking
#                 on the maximum side of the edge distance not the minimum (we provide minimum spacing so that we
#                 get space to work ). edge_dist1 is the spacing from the end of the root radius to the center of the
#                 bolthole. whereas edge_dist2 is the distance from the bolt hole center to the end of the toe."""
#                 if no_rows1 == 1:
#                     if member_detail_iter[0] in ['Angles', 'Star Angles', 'Back to Back Angles']:
#                         edge_dist2 = member_detail_iter[8] - edge_dist1
#                         if edge_dist2 > bolt1.max_edge_dist:
#                             edge_dist2 = bolt1.max_edge_dist
#                             edge_dist1 = member_detail_iter[8] - edge_dist2
#
#                             if edge_dist1 > (bolt1.max_edge_dist - (member_detail_iter[1] - member_detail_iter[8])):
#                                 print('edge distance exceeds the maximum edge distance')
#                                 mem_width_too_large = True
#                                 break
#                     elif member_detail_iter[0] in ['Channels', 'Back to Back Channels']:
#                         edge_dist1 = member_detail_iter[8] / 2
#
#                         if edge_dist1 > (bolt1.max_edge_dist - (member_detail_iter[1] - member_detail_iter[8]) / 2):
#                             print('edge distance exceeds the maximum edge distance')
#                             mem_width_too_large = True
#                             break
#                 else:
#                     if gauge1 >= bolt1.max_spacing:
#                         edge_dist1 = min(((member_detail_iter[8] - (no_rows - 1) * gauge1) / 2),
#                                          bolt1.max_edge_dist)
#
#                     if (2 * edge_dist1 + (no_rows - 1) * gauge1) < member_detail_iter[8]:
#                         print('edge distance exceeds the maximum edge distance')
#                         mem_width_too_large = True
#                         break
#
#                 """ overlap_length is the length required from the end of the plate to accommodate the member """
#                 overlap_length = 2*edge_dist1 + (no_column1 - 1) * pitch1
#
#                 """ now we need to check for the tension or compression yielding capacity of the gusset plate on the
#                  area corresponding to the whitmore width. It is the width obtained by connecting the ends of two
#                  line segments extending from the first bolt towards the load side to the last bolt, making an angle
#                  of 30 degree or pi/6 radian from the direction of load on either side of the load direction.
#                  If the capacity thus obtained is less than the design action then a flag named safe_whitmore_section
#                  is generated. if flag is no, then the loop will be broken from grade, diameter, member loop and the
#                  iteration should continue for the plate loop with the next plate size. """
#                 whitmore_width = round((no_rows1-1)*gauge1 + 2*(joint_len*(math.tan(math.pi/6))), 2)
#                 whitmore_eff_width = round(whitmore_width - no_rows1*bolt1.bolt_hole_dia, 2)
#                 whitmore_area = round(whitmore_width*gusset_plate_t_fu_fy[0], 2)
#                 whitmore_eff_area = round(whitmore_eff_width*gusset_plate_t_fu_fy[0], 2)
#
#                 if member_detail_iter[5] == 'tension':
#                     gusset_yield_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g=whitmore_area,
#                                                                                         f_y=gusset_plate_t_fu_fy[2])/1000
#
#                     gusset_rupture_capacity = IS800_2007.cl_6_3_1_tension_rupture_strength(A_n=whitmore_eff_area,
#                                                                                            f_u=gusset_plate_t_fu_fy[1])/1000
#
#                     if gusset_yield_capacity > design_load_iter and gusset_rupture_capacity > design_load_iter:
#                         safe_whitmore_section = True
#                     else:
#                         safe_whitmore_section = False
#                         """ coming out of grade of bolt loop """
#                         break
#                 elif member_detail_iter[5] == 'compression':
#                     """ here we are trying to find the factored design compression considering the stress reduction
#                     factor (kai) as 1 as per cl 7.1.2 of IS800:2007. It is equal to (eff. area * fy/gamma_m0) """
#                     gusset_yield_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g=whitmore_eff_area,
#                                                                                         f_y=gusset_plate_t_fu_fy[2])/(0.9*1000)
#                     if gusset_yield_capacity > design_load_iter:
#                         safe_whitmore_section = True
#                     else:
#                         safe_whitmore_section = False
#                         """ coming out of grade of bolt loop """
#                         break
#
#                 """ now checking for block shear failure of members. t_db = block shear strength. If block shear failure
#                  can happen then the variable, block_shear_failure = True """
#                 block_shear_failure = False
#                 if member_detail_iter[0] in ['Angles', 'Star Angles', 'Back to Back Angles']:
#                     if member_detail_iter[0] in ['Angles', 'Star Angles']:
#                         if no_rows1 == 1:
#                             a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2]
#                             a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#                             a_tg = (edge_dist2 + (no_rows1 - 1) * gauge1) * member_detail_iter[2]
#                             a_tn = (edge_dist2 + (no_rows1 - 1) * gauge1 - (no_rows1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#                         else:
#                             a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2]
#                             a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#                             a_tg = (edge_dist1 + (no_rows1 - 1) * gauge1) * member_detail_iter[2]
#                             a_tn = (edge_dist1 + (no_rows1 - 1) * gauge1 - (no_rows1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#
#                         t_db = IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg, A_tn=a_tn,
#                                                                         f_u=member_detail_iter[3],
#                                                                         f_y=member_detail_iter[4])/1000
#                     elif member_detail_iter[0] == 'Back to Back Angles':
#                         if no_rows1 == 1:
#                             a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2]
#                             a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#                             a_tg = (edge_dist2 + (no_rows1 - 1) * gauge1) * member_detail_iter[2]
#                             a_tn = (edge_dist2 + (no_rows1 - 1) * gauge1 - (no_rows1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#                         else:
#                             a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2]
#                             a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#                             a_tg = (edge_dist1 + (no_rows1 - 1) * gauge1) * member_detail_iter[2]
#                             a_tn = (edge_dist1 + (no_rows1 - 1) * gauge1 - (no_rows1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#
#                         t_db = 2 * IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg,
#                                                                             A_tn=a_tn,
#                                                                             f_u=member_detail_iter[3],
#                                                                             f_y=member_detail_iter[4])/1000
#                     if t_db < design_load_iter:
#                         block_shear_failure = True
#                         continue
#                     elif t_db > design_load_iter:
#                         block_shear_failure = False
#                 elif member_detail_iter[0] in ['Channels', 'Back to Back Channels']:
#                     if no_rows1 > 1:
#                         if member_detail_iter[0] == 'Channels':
#                             a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2] * 2
#                             a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                     member_detail_iter[2] * 2
#                             a_tg = (no_rows1 - 1) * gauge1 * member_detail_iter[2]
#                             a_tn = ((no_rows1 - 1) * gauge1 - (no_rows1 - 1) * bolt1.bolt_hole_dia) * \
#                                     member_detail_iter[2]
#
#                             t_db = IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg,
#                                                                             A_tn=a_tn,
#                                                                             f_u=member_detail_iter[3],
#                                                                             f_y=member_detail_iter[4])/1000
#
#                         elif member_detail_iter[0] == 'Back to Back Channels':
#                             a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2] * 2
#                             a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2] * 2
#                             a_tg = (no_rows1 - 1) * gauge1 * member_detail_iter[2]
#                             a_tn = ((no_rows1 - 1) * gauge1 - (no_rows1 - 1) * bolt1.bolt_hole_dia) * \
#                                    member_detail_iter[2]
#
#                             t_db = 2 * IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg,
#                                                                                 A_tn=a_tn,
#                                                                                 f_u=member_detail_iter[3],
#                                                                                 f_y=member_detail_iter[4])/1000
#                         if t_db < design_load_iter:
#                             block_shear_failure = True
#                             continue
#                         elif t_db > design_load_iter:
#                             block_shear_failure = False
#                     elif no_rows1 == 1:
#                         block_shear_failure = False
#
#                 """ now checking block shear failure for the gusset plate. gusset_t_db = gusset block shear strength """
#                 gusset_block_shear_failure = False
#                 gusset_a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * gusset_plate_t_fu_fy[0] * 2
#                 gusset_a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
#                                gusset_plate_t_fu_fy[0] * 2
#                 gusset_a_tg = (no_rows1 - 1) * gauge1 * gusset_plate_t_fu_fy[0]
#                 gusset_a_tn = ((no_rows1 - 1) * gauge1 - (no_rows1 - 1) * bolt1.bolt_hole_dia) * \
#                                gusset_plate_t_fu_fy[0]
#
#                 gusset_t_db = IS800_2007.cl_6_4_1_block_shear_strength(A_vg=gusset_a_vg, A_vn=gusset_a_vn,
#                                                                        A_tg=gusset_a_tg,
#                                                                        A_tn=gusset_a_tn,
#                                                                        f_u=gusset_plate_t_fu_fy[1],
#                                                                        f_y=gusset_plate_t_fu_fy[2])/1000
#                 if gusset_t_db < design_load_iter:
#                     gusset_block_shear_failure = True
#                     """ coming out of bolt grade loop """
#                     break
#                 elif gusset_t_db > design_load_iter:
#                     gusset_block_shear_failure = False
#
#                 """ now storing the design data in a list called recommended_bolt which looks as follows:
#                  recommended_bolt = [dia, grade, num_bolts, rows, columns, group_capacity, block_shear_status,
#                                      overlap_length, e1, e2, p, g, whitmore_width]"""
#                 recommended_bolt = [bolt_dia1, bolt_grade1, no_bolts2, no_rows1, no_column1, bolt_group_capacity1,
#                                     block_shear_failure, overlap_length, edge_dist1, edge_dist2, pitch1, gauge1,
#                                     whitmore_width]
#
#                 candidate_bolts1 = candidate_bolts1 + [recommended_bolt]
#                 recommended_bolt = []
#
#             if large_grip1:
#                 """ going for the next diameter in the diameter loop """
#                 continue
#
#             if no_rows < 1:
#                 """ coming out of the bolt loop because the bolt dia is in ascending order and next bolts will certainly
#                  not qualify this criteria. """
#                 break
#
#             if mem_width_too_large:
#                 """ going for the next diameter in the diameter loop """
#                 continue
#
#             if no_bolts1 < 2:
#                 """ going for the next diameter in the diameter loop """
#                 continue
#
#             if not safe_whitmore_section:
#                 """ coming out of bolt dia loop """
#                 break
#             else:
#                 pass
#
#             if gusset_block_shear_failure:
#                 """ coming out of bolt dia loop """
#                 break
#         if not safe_whitmore_section:
#             """ coming out of members loop """
#             break
#         else:
#             pass
#
#         if gusset_block_shear_failure:
#             """ coming out of member loop """
#             break
#
#         """ storing the bolts eligible for each member """
#         candidate_bolts_all = candidate_bolts_all + [candidate_bolts1]
#         candidate_bolts1 = []
#     if not safe_whitmore_section:
#         """ going for the next thickness of the plate """
#         continue
#
#     if gusset_block_shear_failure:
#         """ going for the next thickness of the plate """
#         continue
#
#     """ now selecting the final bolts for each member """
#     """ first of we will check if the bolt_dia and grade of all the members are same then those will be selected.
#     It will look like as follows:
#     final_selected_bolts = [[final recommended_bolt for member1], [final recommended_bolt for member2],
#                             [final recommended_bolt for member3],.....] """
#     final_selected_bolts = []
#     for p in reversed(candidate_bolts_all[0]):
#         final_selected_bolts = final_selected_bolts + [p]
#         for q in candidate_bolts_all[1:len(candidate_bolts_all)]:  # range(1, (len(candidate_bolts_all)-1)):
#             for r in reversed(q):
#                 if p[0] == r[0] and p[1] == r[1]:
#                     final_selected_bolts = final_selected_bolts + [r]
#                     break
#                 else:
#                     continue
#
#         if len(final_selected_bolts) == len(member_details):
#             break
#         else:
#             continue
#
#     """ if no common bolt_dia and grade is found then going to select those with common grade but with different
#     diameter """
#     if len(final_selected_bolts) != len(member_details):
#         final_selected_bolts = []
#         for p in reversed(candidate_bolts_all[0]):
#             final_selected_bolts = final_selected_bolts + [p]
#             for q in candidate_bolts_all[1:len(candidate_bolts_all)]:
#                 for r in reversed(q):
#                     if p[1] == r[1]:
#                         final_selected_bolts = final_selected_bolts + [r]
#                         break
#                     else:
#                         continue
#
#             if len(final_selected_bolts) == len(member_details):
#                 break
#             else:
#                 continue
#
#     """if no bolts with common diameter and grade are there then go for the first entries from the last """
#     if len(final_selected_bolts) != len(member_details):
#         final_selected_bolts = []
#         for p in candidate_bolts_all:
#             final_selected_bolts += [p[len(p)-1]]
#
#     """ now we need to position the members such that they do not overlap with each other. for that if we get the
#     coordinates of all the corners of gusset plates and the shift of the members from the origin then we will be able
#     to place the members as planned """
#     """ first we will find the shift or the clearance(d)of the members from the origin. for that we will start placing
#     the members carrying larger loads as much closer to the origin as possible. the next coming member should have the
#     clearance such that it does not overlap with any of the previously placed member """
#
#     """ arranging the absolute loads in descending order """
#     sorted_load, sorted_index = sort_abs_desc(design_load_all)
#
#     """ creating a list of a and b corresponding to the sorted_index. here a is distance from the bolt centroid to the
#     edge towards the out-stand and b is the distance from the centroid to the end of the toe in case of angles and
#     in case of channel a and b both are the distance from the bolt centroid to the edge towards the out-stand on
#     either side.The edge might be the physical edge of the member or the end tip of whitmore width whichever is greater """
#     sorted_a = []
#     sorted_b = []
#     sorted_angle = []
#     sorted_lap_length = []
#     for x1 in sorted_index:
#         if member_details[x1][0] in ['Angles', 'Star Angles', 'Back to Back Angles']:
#             if final_selected_bolts[x1][3] == 1:
#                 a_1 = max((final_selected_bolts[x1][8] + (member_details[x1][1] - member_details[x1][8]) + 2),
#                           (final_selected_bolts[x1][12]/2))  # added 2 mm for clearance for member accommodation
#             elif final_selected_bolts[x1][3] > 1:
#                 a_1 = max((final_selected_bolts[x1][8] + (member_details[x1][1] - member_details[x1][8]) +
#                           (final_selected_bolts[x1][3]-1)*final_selected_bolts[x1][11]/2 + 2),
#                           (final_selected_bolts[x1][12] / 2))
#         elif member_details[x1][0] in ['Channels', 'Back to Back Channels']:
#             if final_selected_bolts[x1][3] == 1:
#                 a_1 = max((final_selected_bolts[x1][8] + (member_details[x1][1] - member_details[x1][8])/2 + 2),
#                           (final_selected_bolts[x1][12]/2))
#             elif final_selected_bolts[x1][3] > 1:
#                 a_1 = max((final_selected_bolts[x1][8] + (member_details[x1][1] - member_details[x1][8])/2 +
#                           (final_selected_bolts[x1][3]-1)*final_selected_bolts[x1][11]/2 + 2),
#                           (final_selected_bolts[x1][12] / 2))
#
#         if member_details[x1][0] in ['Angles', 'Star Angles', 'Back to Back Angles']:
#             if final_selected_bolts[x1][3] == 1:
#                 b_1 = max((final_selected_bolts[x1][9] + 2),
#                           (final_selected_bolts[x1][12]/2))
#             elif final_selected_bolts[x1][3] > 1:
#                 b_1 = max((final_selected_bolts[x1][9] +
#                           (final_selected_bolts[x1][3]-1)*final_selected_bolts[x1][11]/2 + 2),
#                           (final_selected_bolts[x1][12] / 2))
#         elif member_details[x1][0] in ['Channels', 'Back to Back Channels']:
#             if final_selected_bolts[x1][3] == 1:
#                 b_1 = max((final_selected_bolts[x1][8] + (member_details[x1][1] - member_details[x1][8])/2 + 2),
#                           (final_selected_bolts[x1][12]/2))
#             elif final_selected_bolts[x1][3] > 1:
#                 b_1 = max((final_selected_bolts[x1][8] + (member_details[x1][1] - member_details[x1][8])/2 +
#                           (final_selected_bolts[x1][3]-1)*final_selected_bolts[x1][11]/2 + 2),
#                           (final_selected_bolts[x1][12] / 2))
#
#         sorted_a = sorted_a + [a_1]
#         sorted_b = sorted_b + [b_1]
#         sorted_angle = sorted_angle + [member_details[x1][6]]
#         sorted_lap_length = sorted_lap_length + [final_selected_bolts[x1][7]]
#
#     """ now we want to get the list of spacing(d) from the origin for all the member's end """
#     sorted_d = []
#     counter_x2 = 0
#     for x2 in sorted_index:
#         if counter_x2 == 0:
#             sorted_d = sorted_d + [2.5]
#         else:
#             d_all_possible = []
#             for x3 in range(counter_x2):
#                 prev_a_b_angle = [sorted_a[x3], sorted_b[x3], sorted_angle[x3]]
#                 curr_a_b_angle = [sorted_a[counter_x2], sorted_b[counter_x2], sorted_angle[counter_x2]]
#                 d_all_possible = d_all_possible + [get_d(prev_memb_a_b_angle=prev_a_b_angle,
#                                                          current_memb_a_b_angle=curr_a_b_angle)]
#
#             sorted_d = sorted_d + [max(tuple(d_all_possible))]
#         counter_x2 = counter_x2 + 1
#
#     """ now creating the co-ordinates of the vertices of the polynomial in the shape of which the gusset plate has to
#     be cut """
#     """ for this, creating ascending order of angles and the index corresponding to it """
#     asc_angle, asc_a, asc_b, asc_d, asc_lap_length = sort_five_lists(list1=sorted_angle, list2=sorted_a,
#                                                                      list3=sorted_b, list4=sorted_d,
#                                                                      list5=sorted_lap_length)
#     """the coordinate is stored in a list of tuples in an order which when joined, takes the shape of the gusset plate"""
#     guss_coord = []
#     origin_offset = []
#     for x4 in range(len(asc_angle)):
#         """ included angle between the first and the last entry of the asc_angle """
#         included_angle_min_max = asc_angle[len(asc_angle)-1] - asc_angle[0]  # get_included_angle(theta1=asc_angle[0],
#                                                     # theta2=asc_angle[len(asc_angle)-1])
#         if included_angle_min_max <= 180:
#             if x4 == 0:
#                 absc1 = 0
#                 ordn1 = -1*asc_b[x4]
#                 absc2 = asc_d[x4]+asc_lap_length[x4]
#                 ordn2 = -1 * asc_b[x4]
#                 absc3 = asc_d[x4] + asc_lap_length[x4]
#                 ordn3 = asc_a[x4]
#                 guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                         angle=asc_angle[x4])
#             elif x4 == (len(asc_angle)-1):
#                 absc3 = 0
#                 ordn3 = asc_a[x4]
#                 absc1 = asc_d[x4] + asc_lap_length[x4]
#                 ordn1 = -1 * asc_b[x4]
#                 absc2 = asc_d[x4] + asc_lap_length[x4]
#                 ordn2 = asc_a[x4]
#                 guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                         angle=asc_angle[x4])
#             else:
#                 absc1 = asc_d[x4] + asc_lap_length[x4]
#                 ordn1 = -1 * asc_b[x4]
#                 absc2 = asc_d[x4] + asc_lap_length[x4]
#                 ordn2 = asc_a[x4]
#                 guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2)],
#                                                         angle=asc_angle[x4])
#         elif asc_angle[1] - asc_angle[0] >= 180:
#             if x4 == 1:
#                 absc1 = 0
#                 ordn1 = -1*asc_b[x4]
#                 absc2 = asc_d[x4]+asc_lap_length[x4]
#                 ordn2 = -1 * asc_b[x4]
#                 absc3 = asc_d[x4] + asc_lap_length[x4]
#                 ordn3 = asc_a[x4]
#                 guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                         angle=asc_angle[x4])
#             elif x4 == 0:
#                 absc3 = 0
#                 ordn3 = asc_a[x4]
#                 absc1 = asc_d[x4] + asc_lap_length[x4]
#                 ordn1 = -1 * asc_b[x4]
#                 absc2 = asc_d[x4] + asc_lap_length[x4]
#                 ordn2 = asc_a[x4]
#                 guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                         angle=asc_angle[x4])
#             else:
#                 absc1 = asc_d[x4] + asc_lap_length[x4]
#                 ordn1 = -1 * asc_b[x4]
#                 absc2 = asc_d[x4] + asc_lap_length[x4]
#                 ordn2 = asc_a[x4]
#                 guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2)],
#                                                         angle=asc_angle[x4])
#         else:
#             absc1 = asc_d[x4] + asc_lap_length[x4]
#             ordn1 = -1 * asc_b[x4]
#             absc2 = asc_d[x4] + asc_lap_length[x4]
#             ordn2 = asc_a[x4]
#             guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2)],
#                                                     angle=asc_angle[x4])
#
#         """origin_offset = distance of the edge of the gusset from the assumed origin"""
#         origin_offset = origin_offset + [asc_d[x4] + asc_lap_length[x4]]
#
#     offset_excess_min_max = (max(tuple(origin_offset)) - min(tuple(origin_offset)))/ min(tuple(origin_offset))
#
#     if (included_angle_min_max <= 180 and offset_excess_min_max >= 1.5) or \
#             (asc_angle[1] - asc_angle[0] > 180 and offset_excess_min_max >= 1.5):
#         guss_coord = []
#         for x5 in range(len(asc_angle)):
#             if included_angle_min_max <= 180:
#                 if x5 == 0:
#                     absc1 = 0
#                     ordn1 = -1 * asc_b[x5]
#                     absc2 = asc_d[x5] + asc_lap_length[x5]
#                     ordn2 = -1 * asc_b[x5]
#                     absc3 = asc_d[x5] + asc_lap_length[x5]
#                     ordn3 = asc_a[x5]
#                     if (max(tuple(origin_offset)) - origin_offset[x5]) / origin_offset[x5] >= 1.5:
#                         absc2 = max(tuple(asc_d))  # [] + asc_lap_length[x4]
#                         absc3 = max(tuple(asc_d))
#                         ind1 = sorted_angle.index(asc_angle[x5])
#                         ind2 = sorted_index[sorted_angle.index(asc_angle[x5])]
#                         sorted_d[ind1] = absc2 - final_selected_bolts[ind2][7]
#                     guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                             angle=asc_angle[x5])
#                 elif x5 == (len(asc_angle) - 1):
#                     absc3 = 0
#                     ordn3 = asc_a[x5]
#                     absc1 = asc_d[x5] + asc_lap_length[x5]
#                     ordn1 = -1 * asc_b[x5]
#                     absc2 = asc_d[x5] + asc_lap_length[x5]
#                     ordn2 = asc_a[x5]
#                     if (max(tuple(origin_offset)) - origin_offset[x5]) / origin_offset[x5] >= 1.5:
#                         absc2 = max(tuple(asc_d))  # [] + asc_lap_length[x4]
#                         absc1 = max(tuple(asc_d))
#                         ind1 = sorted_angle.index(asc_angle[x5])
#                         ind2 = sorted_index[sorted_angle.index(asc_angle[x5])]
#                         sorted_d[ind1] = absc2 - final_selected_bolts[ind2][7]
#                     guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                             angle=asc_angle[x5])
#                 else:
#                     absc1 = asc_d[x5] + asc_lap_length[x5]
#                     ordn1 = -1 * asc_b[x5]
#                     absc2 = asc_d[x5] + asc_lap_length[x5]
#                     ordn2 = asc_a[x5]
#                     if (max(tuple(origin_offset)) - origin_offset[x5]) / origin_offset[x5] >= 1.5:
#                         absc1 = max(tuple(asc_d))  # [] + asc_lap_length[x4]
#                         absc2 = max(tuple(asc_d))
#                         ind1 = sorted_angle.index(asc_angle[x5])
#                         ind2 = sorted_index[sorted_angle.index(asc_angle[x5])]
#                         sorted_d[ind1] = absc2 - final_selected_bolts[ind2][7]
#                     guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2)],
#                                                             angle=asc_angle[x5])
#             elif asc_angle[1] - asc_angle[0] >= 180:
#                 if x5 == 1:
#                     absc1 = 0
#                     ordn1 = -1 * asc_b[x5]
#                     absc2 = asc_d[x5] + asc_lap_length[x5]
#                     ordn2 = -1 * asc_b[x5]
#                     absc3 = asc_d[x5] + asc_lap_length[x5]
#                     ordn3 = asc_a[x5]
#                     if (max(tuple(origin_offset)) - origin_offset[x5]) / origin_offset[x5] >= 1.5:
#                         absc2 = max(tuple(asc_d))  # [] + asc_lap_length[x4]
#                         absc3 = max(tuple(asc_d))
#                         ind1 = sorted_angle.index(asc_angle[x5])
#                         ind2 = sorted_index[sorted_angle.index(asc_angle[x5])]
#                         sorted_d[ind1] = absc2 - final_selected_bolts[ind2][7]
#                     guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                             angle=asc_angle[x5])
#                 elif x5 == 0:
#                     absc3 = 0
#                     ordn3 = asc_a[x5]
#                     absc1 = asc_d[x5] + asc_lap_length[x5]
#                     ordn1 = -1 * asc_b[x5]
#                     absc2 = asc_d[x5] + asc_lap_length[x5]
#                     ordn2 = asc_a[x5]
#                     if (max(tuple(origin_offset)) - origin_offset[x5]) / origin_offset[x5] >= 1.5:
#                         absc2 = max(tuple(asc_d))  # [] + asc_lap_length[x4]
#                         absc1 = max(tuple(asc_d))
#                         ind1 = sorted_angle.index(asc_angle[x5])
#                         ind2 = sorted_index[sorted_angle.index(asc_angle[x5])]
#                         sorted_d[ind1] = absc2 - final_selected_bolts[ind2][7]
#                     guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2), (absc3, ordn3)],
#                                                             angle=asc_angle[x5])
#                 else:
#                     absc1 = asc_d[x5] + asc_lap_length[x5]
#                     ordn1 = -1 * asc_b[x5]
#                     absc2 = asc_d[x5] + asc_lap_length[x5]
#                     ordn2 = asc_a[x5]
#                     if (max(tuple(origin_offset)) - origin_offset[x5]) / origin_offset[x5] >= 1.5:
#                         absc1 = max(tuple(asc_d))  # [] + asc_lap_length[x4]
#                         absc2 = max(tuple(asc_d))
#                         ind1 = sorted_angle.index(asc_angle[x5])
#                         ind2 = sorted_index[sorted_angle.index(asc_angle[x5])]
#                         sorted_d[ind1] = absc2 - final_selected_bolts[ind2][7]
#                     guss_coord = guss_coord + rotate_points(points=[(absc1, ordn1), (absc2, ordn2)],
#                                                             angle=asc_angle[x5])
#
#     """ Getting the co-ordinates of the center of bolt holes member by member """
#     coord_bolt_holes_all = []
#     for x6 in range(len(member_details)):
#         n_r = final_selected_bolts[x6][3]
#         n_c = final_selected_bolts[x6][4]
#         e1 = final_selected_bolts[x6][8]
#         p1 = final_selected_bolts[x6][10]
#         g1 = final_selected_bolts[x6][11]
#         d1 = sorted_d[sorted_index.index(x6)]
#         angle1 = member_details[x6][6]
#         y_max = (n_r - 1)/2 * g1
#         """ here n_r and n_c are the number of rows and number of columns respectively for member under iteration """
#         coord_bolt_holes = []
#         for x7 in range(n_r):
#
#             for x8 in range(n_c):
#                 absc_x = d1 + e1 + x8*p1
#                 ordn_y = y_max - x7*g1
#
#                 coord_bolt_holes += [(absc_x, ordn_y)]
#         coord_bolt_holes = rotate_points(coord_bolt_holes, angle=angle1)
#
#         coord_bolt_holes_all += [coord_bolt_holes]
#
#     """ finding the edge length of the gusset plate to find its tendency towards local buckling """
#     gusset_side_length = polygon_side_lengths(guss_coord)
#
#     if included_angle_min_max <= 180 or asc_angle[1] - asc_angle[0] > 180:
#         gusset_free_side_length = calculate_side_lengths(A=guss_coord)
#     else:
#         gusset_free_side_length = calculate_even_side_lengths(poly=guss_coord)
#
#     """ Local buckling may be prevented if the unsupported edge of a gusset plate is restricted to
#     42*epsilon times the thickness (Gaylord et al. 1992), where epsilon = (250/fy)^0.5 """
#     epsilon_guss = (250/gusset_plate_t_fu_fy[2])**0.5
#     local_buckling1 = False
#     if max(tuple(gusset_free_side_length)) > 42*epsilon_guss*gusset_plate_t_fu_fy[0]:
#         local_buckling1 = True
#         continue
#
#     """ now checking for local buckling of gusset plate due to the compression members. Therefore checking for the
#     compression member with highest load. if local_buckling2 is found to be True then go for next thickness of plate"""
#     negative_list = [x for x in load_details if x < 0]
#
#     local_buckling2 = False
#     if len(negative_list) > 0:
#         max_comp_load = min(tuple(negative_list))
#         for x9 in negative_list:
#             # guss_max_comp = design_load_all[load_details.index(x9)]
#             d_comp = sorted_d[sorted_index.index(load_details.index(x9))]
#             whitmore_width_comp = final_selected_bolts[load_details.index(x9)][12]
#             if design_load_all[load_details.index(x9)] > \
#                     gusset_design_comp_strength(whitmore_width_guss=whitmore_width_comp,
#                                                 sec_thick=gusset_plate_t_fu_fy[0],
#                                                 clearance_d=d_comp,
#                                                 fy_guss=gusset_plate_t_fu_fy[2]):
#                 local_buckling2 = True
#                 break
#         if local_buckling2:
#             continue
#
#     """ now breaking the loop if all the local buckling checks are found to be true """
#     if not local_buckling1 and not local_buckling2:
#         break
#
#
#
# """ completion of the main loop """
#
#
# """ printing warning and suggestion log """
#
#
#
# """check"""
# print(final_selected_bolts)
# print(guss_coord)
# print(coord_bolt_holes_all)
# print(selected_gusset)
# print(local_buckling2, local_buckling1)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
