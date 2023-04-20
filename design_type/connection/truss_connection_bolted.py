# Author: Devesh Kumar
from utils.common.is800_2007 import IS800_2007
from utils.common.component import Bolt
import copy
from utils.common.other_standards import *
from utils.common.common_calculation import *
import math

""" ======The input values start here====== """

""" These values are to be extracted from the input provided by the users """
no_of_members = 3

""" List of details of members 
i.e.[section_profile, conn_part_width(mm), conn_part_t(mm), fu_memb(MPa), fy_memb(MPa), member_type,  
     angle from x-axis(in deg), gross area(mm2), h1(mm)]
     here h1(mm) is the width available for bolt accommodation = conn_part_width - t_flanges - root_radi
starting from 1st member and proceeding one by one.
member_type means 'tension' or 'compression' or 'compression_butting' (str) """
# be careful while connecting the input values of gross area of back to back members and star-angles
member_details = [['Angles', 70, 8, 410, 250, 'tension', 0, 858, 55.5],
                  ['Angles', 75, 10, 410, 250, 'compression', 45, 1152, 58.5],
                  ['Angles', 80, 8, 410, 250, 'tension', 90, 978, 65]
                  ]

""" here type of bolt may be 'Bearing' or 'Friction'. It is also mandatory to connect the input values such that
 the values inside the 'grade' and the 'Diameter' key are in ascending order to avoid any unforeseen error """
bolts_details = {'type': 'Bearing', 'grade': [4.6, 4.8, 6.8], 'Diameter': [8, 10, 12, 20, 32], 'mu_f': 0.2}

"""List of the input of the [thickness, fu_plate, fy_plate] of gusset plate"""
plate_details = [[6, 410, 250],
                 [8, 410, 250],
                 [10, 410, 250],
                 [12, 410, 250]
                 ]

""" List of axial load (in KN)  on the members starting from 1st member and proceeding one by one """
# beware of connecting the load inputs of star angles. the load should be divided by 2 because further design will be
# done considering one of the angles of star angle as a single angle but whitmore width will consider both angles
load_details = [20, 25, 30]

""" ======The input values end here====== """


# input_Conn_Location = 'Angles'
# input_dia_list = [8,10,12,16]
# input_bolt_grades = [4.6,4.8,8.8]


class bolt_general():
    def __init__(self, grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail):
        self.grade = grade
        self.bolt_dia = bolt_dia
        """ conn_plates_t_fu_fy - List of tuples with plate thicknesses in mm, fu in MPa, fy in MPa (list of tuples)"""
        self.connection_plates_t_fu_fy = connection_plates_t_fu_fy
        """ connection_plates_t - List of thicknesses in mm of connected plates (list or tuple)"""
        self.connection_plates_t = connection_plates_t
        """ member_detail - 'Angles','Channels','Star Angles', 'Back to Back Angles','Back to Back Channels' """
        self.member_detail = member_detail
        self.bolt_hole_dia = IS800_2007.cl_10_2_1_bolt_hole_size(bolt_dia, 'Standard')
        self.fu_b = bolt_general.f_u_bolt(grade=grade, bolt_dia=bolt_dia)
        self.min_edge_dist = IS800_2007.cl_10_2_4_2_min_edge_end_dist(d=self.bolt_dia, bolt_hole_type='Standard',
                                                                      edge_type='Sheared or hand flame cut')
        # in the below variable global variable (connection_plates_t_fu_fy) is being used so care has to be taken that
        # the global variable changes respectively for respective loop
        self.max_edge_dist = IS800_2007.cl_10_2_4_3_max_edge_dist(self.connection_plates_t_fu_fy, False)
        self.max_spacing = IS800_2007.cl_10_2_3_1_max_spacing(self.connection_plates_t)
        self.min_pitch = IS800_2007.cl_10_2_2_min_spacing(d=bolt_dia)
        self.max_pitch = IS800_2007.cl_10_2_3_2_max_pitch_tension_compression(d=bolt_dia,
                                                                              plate_thicknesses=self.connection_plates_t,
                                                                              member_type=self.member_detail[5])
        self.pitch_provided = min(round_up(self.min_pitch, 5), round_down(self.max_pitch, 5))
        self.edge_dist_provided = min(round_up(self.min_edge_dist, 5), round_down(self.max_edge_dist, 5))
        self.n_n = bolt_general.get_n_n(section_profile=member_detail)
        self.a_nb = bolt_general.get_a_nb(bolt_dia=self.bolt_dia)
        self.a_sb = round(math.pi / 4 * bolt_dia ** 2)

    def bolt_dia_number_bearing(self, conn_loc_t, guss_plate_t, diam=None, bolt_gr=None):
        """will return the diameter and the no. of such bearing bolts required for a given member thickness
        gusset thickness and given load"""

        if diam == None or bolt_gr == None:
            diam = self.dia_list
            bolt_gr = self.bolt_grade

        'selecting the min dia and removing the dia of bolt below that, required for a given member and '
        'gusset thickness keeping large grip provision in mind'
        m = len(diam)
        for i in range(m):

            if diam[i] <= (conn_loc_t + guss_plate_t) / 8:
                trimmed_dia = copy.copy(diam)
                del trimmed_dia[i]

    @staticmethod
    def get_n_n(section_profile):
        """This will provide the number of shear planes intercepting the bolt.
           the connection location will be specified by the user in each of the member case"""
        if section_profile in ['Angles', 'Channels', 'Star Angles']:
            return 1
        elif section_profile in ['Back to Back Angles', 'Back to Back Channels']:
            return 2

    @staticmethod
    def get_a_nb(bolt_dia):
        return round(0.78 * math.pi / 4 * bolt_dia ** 2)

    @staticmethod
    def f_u_bolt(grade, bolt_dia):
        'returns the ultimate strength of the bolt as per Table -1 of IS 800: 2007'
        grade = float(grade)
        bolt_dia = float(bolt_dia)

        if grade == 8.8 and bolt_dia <= 16:
            return 800
        elif grade == 8.8:
            return 830
        else:
            fu_data = {3.6: 330, 4.6: 400, 4.8: 420, 5.6: 500, 5.8: 520, 6.8: 600, 9.8: 900, 10.9: 1040, 12.9: 1220}
            return fu_data[grade]

    @staticmethod
    def cl_10_2_1_bolt_hole_size(d, bolt_hole_type='Standard'):
        """Calculate bolt hole diameter as per Table 19 of IS 800:2007
        Args:
             d - Nominal diameter of fastener in mm (float)
             bolt_hole_type - Either 'Standard' or 'Over-sized' or 'short_slot' or 'long_slot' (str)
        Returns:
            bolt_hole_size -  Diameter of the bolt hole in mm (float)
        Note:
            Reference:
            IS 800, Table 19 (Cl 10.2.1)
        TODO:ADD KEY_DISP for for Standard/oversize etc and replace these strings
        """
        table_19 = {
            "12-14": {'Standard': 1.0, 'Over-sized': 3.0, 'short_slot': 4.0, 'long_slot': 2.5},
            "16-22": {'Standard': 2.0, 'Over-sized': 4.0, 'short_slot': 6.0, 'long_slot': 2.5},
            "24": {'Standard': 2.0, 'Over-sized': 6.0, 'short_slot': 8.0, 'long_slot': 2.5},
            "24+": {'Standard': 3.0, 'Over-sized': 8.0, 'short_slot': 10.0, 'long_slot': 2.5}
        }

        d = int(d)

        if d < 12:
            clearance = 0
        elif d <= 14:
            clearance = table_19["12-14"][bolt_hole_type]
        elif d <= 22:
            clearance = table_19["16-22"][bolt_hole_type]
        elif d <= 24:
            clearance = table_19["24"][bolt_hole_type]
        else:
            clearance = table_19["24+"][bolt_hole_type]
        if bolt_hole_type == 'long_slot':
            bolt_hole_size = (clearance + 1) * d
        else:
            bolt_hole_size = clearance + d
        return bolt_hole_size


class bearing_bolt(bolt_general):
    def __init__(self, grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail, joint_length=0):
        super().__init__(grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail)
        # joint_length(lj) is the distance between the first and the last row of joint in the direction of load
        self.joint_length = joint_length
        self.beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(d=self.bolt_dia, l_j=self.joint_length)
        # if self.joint_length is not None:
        # self.beta_lj = IS800_2007.cl_10_3_3_1_bolt_long_joint(d=self.bolt_dia, l_j=self.joint_length)
        # considering no packing plates to be used in the gusset connection, taking beta_pkg = 1
        self.beta_pkg = 1
        self.grip_length = sum(self.connection_plates_t)
        self.beta_lg = IS800_2007.cl_10_3_3_2_bolt_large_grip(d=self.bolt_dia, l_g=self.grip_length,
                                                              l_j=self.joint_length)
        self.t_bearing = min(self.connection_plates_t[0], (sum(self.connection_plates_t) - self.connection_plates_t[0]))

    def bearing_bolt_design_capacity(self):
        v_dsb = self.beta_lj * self.beta_lg * self.beta_pkg * \
                IS800_2007.cl_10_3_3_bolt_shear_capacity(f_ub=self.fu_b, A_nb=self.a_nb, A_sb=self.a_sb, n_n=self.n_n)
        v_dpb = IS800_2007.cl_10_3_4_bolt_bearing_capacity(f_u=self.member_detail[3], f_ub=self.fu_b, t=self.t_bearing,
                                                           d=self.bolt_dia, e=self.edge_dist_provided,
                                                           p=self.pitch_provided, bolt_hole_type='Standard',
                                                           safety_factor_parameter='Field weld')
        v_db = min(v_dsb, v_dpb)
        return v_db


class friction_bolt(bolt_general):
    def __init__(self, grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail, mu_f=0.2):
        super().__init__(grade, bolt_dia, connection_plates_t_fu_fy, connection_plates_t, member_detail)
        self.mu_f = mu_f

    def friction_bolt_design_capacity(self):
        v_dsf = IS800_2007.cl_10_4_3_bolt_slip_resistance(f_ub=self.fu_b, A_nb=self.a_nb, n_e=self.n_n,
                                                          mu_f=self.mu_f, bolt_hole_type='Standard',
                                                          slip_resistance='ultimate_load')
        return v_dsf[0]


""" starting the loop for the truss connection design. starting with selecting a thickness of a gusset plate and
then for the same thickness all the joining members are designed for the available bolts. In the available bolts the 
bolts that can be suitably used will be stored and later some common or most suitable bolt design will be selected"""

""" starting with selecting and deciding the thicknesses of the gusset plate for which the loop has to run """

""" selecting the thickness of thickest connected member and for that first creating the list of thickness 
of all the connected members named member_thickness_iter """
member_thickness_iter = []
for i in len(member_details):
    member_thickness_iter.append(member_details[i][2])

"""Creating a list of input plate thickness having thickness greater than the max of thickness of all the members as it
is a thumb rule to take the thickness of the gusset plate greater than the thickness of any connecting member
plate_details_iter is a list - 
[section_profile, conn_part_width, conn_part_t, fu_memb, fy_memb, member_type, angle, A_g, h1]
 here h1(mm) is the width available for bolt accommodation = conn_part_width - t_flanges - root_radi """
plate_details_iter = []
for i in len(plate_details):
    if plate_details[i][0] > max(tuple(member_thickness_iter)):
        plate_details_iter.append(plate_details[i])

""" Starting the loop of gusset plate """
for i in len(plate_details_iter):
    """ defining candidate_bolts_all to store the eligible bolts for all the members"""
    candidate_bolts_all = []

    """gusset_plate_t_fu_fy - [thickness, fu_plate, fy_plate] of gusset plate"""
    gusset_plate_t_fu_fy = plate_details_iter[i]

    for j in len(member_details):
        """ candidate_bolts1 is the list which will store all the combination of diameter and grade of bolt which can
        be used for the connection of that member. It will be empty for every value of j. the assignment of this 
        variable to an empty list will be done after adding this list to another list which stores such list for all 
        the members """
        candidate_bolts1 = []

        """ member_detail_iter is the variable having detail of that member 
        e.g ['Angles', 70, 8, 410, 250, 'tension', 0, 858, 55.5]
        for which the iteration of the bolt design is to run """
        member_detail_iter = member_details[j]

        """ member_t_fu_fy is the list of tuples of t, fu, fy of the member under consideration """
        if member_detail_iter[0] in ['Angles', 'Channels', 'Star Angles']:
            member_t_fu_fy = [(member_detail_iter[2], member_detail_iter[3], member_detail_iter[4])]
        elif member_detail_iter[0] in ['Back to Back Angles', 'Back to Back Channels']:
            member_t_fu_fy = [(member_detail_iter[2], member_detail_iter[3], member_detail_iter[4])] * 2

        """connection_plates_t_fu_fy_iter is the list of tuples of the   plate and members containing 
        their (thickness,fu,fy) like [(12, 410, 250), (8, 410, 250)]. The first tuple should be the detail of the 
        gusset plate and the following are the member detail. Number of tuples will be 3 for back to back conn"""
        connection_plates_t_fu_fy_iter = [tuple(gusset_plate_t_fu_fy)] + member_t_fu_fy

        """note that the first entry i.e. the 0th index is the thickness of gusset and the subsequent are
         member e.g. thickness_connection_plates_t_iter = [12, 8]"""
        if member_detail_iter[0] in ['Angles', 'Channels', 'Star Angles']:
            thickness_connection_plates_t_iter = [connection_plates_t_fu_fy_iter[0][0],
                                                  connection_plates_t_fu_fy_iter[1][0]]
        elif member_detail_iter[0] in ['Back to Back Angles', 'Back to Back Channels']:
            thickness_connection_plates_t_iter = [connection_plates_t_fu_fy_iter[0][0],
                                                  connection_plates_t_fu_fy_iter[1][0],
                                                  connection_plates_t_fu_fy_iter[2][0]]

        design_load_iter = min(abs(load_details[j]), (
                    0.3 * IS800_2007.cl_6_2_tension_yielding_strength(member_detail_iter[7], member_detail_iter[4])))

        """ bolt_dia_iter is a list having all the input bolt diameter e.g [8, 10, 12, 20, 32] """
        bolt_dia_iter = bolts_details['Diameter']
        bolt_grade_iter = bolts_details['grade']
        for k in len(bolt_dia_iter):
            bolt_dia1 = bolt_dia_iter[k]

            """ Now running a loop for every grade of bolts in the list of input grades of the bolt """
            for l in len(bolt_grade_iter):
                bolt_grade1 = bolt_grade_iter[l]

                """ creating an instance named bolt1 from the bearing bolt class or friction bolt class 
                depending upon the input """
                joint_len = 0
                mu_f1 = 0.2
                if bolts_details['type'] == 'Bearing':
                    bolt1 = bearing_bolt(grade=bolt_grade1, bolt_dia=bolt_dia1,
                                         connection_plates_t_fu_fy=connection_plates_t_fu_fy_iter,
                                         connection_plates_t=thickness_connection_plates_t_iter,
                                         member_detail=member_detail_iter[0], joint_length=joint_len)
                else:
                    bolt1 = friction_bolt(grade=bolt_grade1, bolt_dia=bolt_dia1,
                                          connection_plates_t_fu_fy=connection_plates_t_fu_fy_iter,
                                          connection_plates_t=thickness_connection_plates_t_iter,
                                          member_detail=member_detail_iter[0], mu_f=mu_f1)

                """ using large grip criteria as per Cl 10.3.3.2 of IS800:2007, ensuring the min dia bolt for which
                 the loop should run """
                large_grip1 = False
                if bolt_dia_iter <= sum(thickness_connection_plates_t_iter) / 8:
                    large_grip1 = True
                    """ coming out of the bolt grade loop """
                    break

                """ Condition to ensure that the bolt dia selected will be able to be accommodated in the connected 
                part of the member. number of bolt lines(no_rows) possible** = round_down((h1 - 2e_min)/gauge_dist) + 1
                here for simplicity gauge dist has been taken as the pitch. 
                Note - rows means bolt lines along the direction of load applied
                    columns means bolt line perpendicular to the direction of load applied """
                no_rows = round_down((member_detail_iter[8] - 2 * bolt1.edge_dist_provided) / bolt1.pitch_provided) + 1
                if no_rows < 1:
                    """ coming out of the bolt grade loop """
                    break

                """ the edge distance, gauge and pitch used are represented as follows by edge_dist1, gauge1 
                and pitch1 """
                edge_dist1 = bolt1.edge_dist_provided
                gauge1 = min((member_detail_iter[8] - 2 * edge_dist1) / (no_rows - 1), bolt1.max_spacing)
                pitch1 = bolt1.pitch_provided

                """ finding the bolt capacity (bolt_capacity1) of the selected bolt and grade """
                bolt_capacity1 = 0
                if bolts_details['type'] == 'Bearing':
                    bolt_capacity1 = bolt1.bearing_bolt_design_capacity()
                else:
                    bolt_capacity1 = bolt1.friction_bolt_design_capacity()

                no_bolts1 = round_up((design_load_iter/bolt_capacity1), 1)
                """ there should at least be two numbers of bolts in a connection. if number of bolts are less than 2
                then the grade loop has to be broken because one bolt may not resist the rotation of member and in turn
                make the line of action of axial forces non-concurrent.  
                For this it is mandatory that the list of grade is in ascending order """
                if no_bolts1 < 2:
                    break

                for o in range(no_rows):
                    no_rows1 = o+1
                    no_column1 = round_up((no_bolts1/no_rows1), 1)
                    """ Note - The arrangement of the bolts are in chain pattern not in staggered or diamond pattern 
                    therefore the number of bolts = rows*columns
                    rows means bolt lines along the direction of load applied
                    columns means bolt line perpendicular to the direction of load applied """
                    no_bolts2 = no_rows1*no_column1
                    """ now joint length = (columns - 1)*pitch """
                    joint_len = (no_column1-1)*pitch1
                    """if it is found that the joint length is less than 15d then that number of row is selected and 
                    the loop is broken. if the joint length exceeds 15d even after accommodating the bolts in the 
                    maximum possible number of rows then that maximum possible number of rows will be the selected
                    number of rows"""
                    if joint_len < 15*bolt_dia1:
                        break

                """ calculating the total bolt capacity"""
                bolt_group_capacity1 = 0
                if bolts_details['type'] == 'Bearing':
                    bolt_group_capacity1 = no_bolts2*bolt1.bearing_bolt_design_capacity()
                else:
                    bolt_group_capacity1 = no_bolts2*bolt1.friction_bolt_design_capacity()

                """ increasing the number of bolts by increasing one one column in case the bolt group capacity is
                less than the design load. the no. of times the while loop iterates is limited to 10 in order to escape
                from entering into an infinite loop in any case """
                count1 = 1
                while bolt_group_capacity1 < design_load_iter and count1 < 10:
                    count1 = count1+1
                    no_column1 = no_column1 + 1
                    no_bolts2 = no_rows1 * no_column1
                    joint_len = (no_column1 - 1) * pitch1
                    if bolts_details['type'] == 'Bearing':
                        bolt_group_capacity1 = no_bolts2 * bolt1.bearing_bolt_design_capacity()
                    else:
                        bolt_group_capacity1 = no_bolts2 * bolt1.friction_bolt_design_capacity()

                """ overlap_length is the length required from the end of the plate to accommodate the member """
                overlap_length = edge_dist1 + (no_column1 - 1) * pitch1

                """ now we need to check for the tension or compression yielding capacity of the gusset plate on the 
                 area corresponding to the whitmore width. It is the width obtained by connecting the ends of two
                 line segments extending from the first bolt towards the load side to the last bolt, making an angle
                 of 30 degree or pi/6 radian from the direction of load on either side of the load direction. 
                 If the capacity thus obtained is less than the design action then a flag named safe_whitmore_section 
                 is generated. if flag is no, then the loop will be broken from grade, diameter, member loop and the
                 iteration should continue for the plate loop with the next plate size. """
                whitmore_width = (no_rows1-1)*gauge1 + 2*(joint_len*(math.tan(math.pi/6)))
                whitmore_eff_width = whitmore_width - no_rows1*bolt1.bolt_hole_dia
                whitmore_area = whitmore_width*gusset_plate_t_fu_fy[0]
                whitmore_eff_area = whitmore_eff_width*gusset_plate_t_fu_fy[0]

                if member_detail_iter[5] == 'tension':
                    gusset_yield_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g=whitmore_area,
                                                                                        f_y=gusset_plate_t_fu_fy[2])

                    gusset_rupture_capacity = IS800_2007.cl_6_3_1_tension_rupture_strength(A_n=whitmore_eff_area,
                                                                                           f_u=gusset_plate_t_fu_fy[1])

                    if gusset_yield_capacity > design_load_iter and gusset_rupture_capacity > design_load_iter:
                        safe_whitmore_section = True
                    else:
                        safe_whitmore_section = False
                        """ coming out of grade of bolt loop """
                        break
                elif member_detail_iter[5] == 'compression':
                    """ here we are trying to find the factored design compression considering the stress reduction
                    factor (kai) as 1 as per cl 7.1.2 of IS800:2007. It is equal to (eff. area * fy/gamma_m0) """
                    gusset_yield_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g=whitmore_eff_area,
                                                                                        f_y=gusset_plate_t_fu_fy[2])
                    if gusset_yield_capacity > design_load_iter:
                        safe_whitmore_section = True
                    else:
                        safe_whitmore_section = False
                        """ coming out of grade of bolt loop """
                        break

                """ now checking for block shear failure of members. t_db = block shear strength. If block shear failure
                 can happen then the variable block_shear_failure = True """
                block_shear_failure = False
                if member_detail_iter[0] in ['Angles', 'Star Angles', 'Back to Back Angles']:
                    if member_detail_iter[0] in ['Angles', 'Star Angles']:
                        a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2]
                        a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
                               member_detail_iter[2]
                        a_tg = (edge_dist1 + (no_rows1 - 1) * gauge1) * member_detail_iter[2]
                        a_tn = (edge_dist1 + (no_rows1 - 1) * gauge1 - (no_rows1 - 0.5) * bolt1.bolt_hole_dia) * \
                               member_detail_iter[2]

                        t_db = IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg, A_tn=a_tn,
                                                                        f_u=member_detail_iter[3],
                                                                        f_y=member_detail_iter[4])
                    elif member_detail_iter[0] == 'Back to Back Angles':
                        a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2]
                        a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
                               member_detail_iter[2]
                        a_tg = (edge_dist1 + (no_rows1 - 1) * gauge1) * member_detail_iter[2]
                        a_tn = (edge_dist1 + (no_rows1 - 1) * gauge1 - (no_rows1 - 0.5) * bolt1.bolt_hole_dia) * \
                               member_detail_iter[2]

                        t_db = 2 * IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg,
                                                                            A_tn=a_tn,
                                                                            f_u=member_detail_iter[3],
                                                                            f_y=member_detail_iter[4])
                    if t_db < design_load_iter:
                        block_shear_failure = True
                    elif t_db > design_load_iter:
                        block_shear_failure = False
                elif member_detail_iter[0] in ['Channels', 'Back to Back Channels']:
                    if no_rows1 > 1:
                        if member_detail_iter[0] == 'Channels':
                            a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2] * 2
                            a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
                                    member_detail_iter[2] * 2
                            a_tg = (no_rows1 - 1) * gauge1 * member_detail_iter[2]
                            a_tn = ((no_rows1 - 1) * gauge1 - (no_rows1 - 1) * bolt1.bolt_hole_dia) * \
                                    member_detail_iter[2]

                            t_db = IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg,
                                                                            A_tn=a_tn,
                                                                            f_u=member_detail_iter[3],
                                                                            f_y=member_detail_iter[4])

                        elif member_detail_iter[0] == 'Back to Back Channels':
                            a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * member_detail_iter[2] * 2
                            a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
                                   member_detail_iter[2] * 2
                            a_tg = (no_rows1 - 1) * gauge1 * member_detail_iter[2]
                            a_tn = ((no_rows1 - 1) * gauge1 - (no_rows1 - 1) * bolt1.bolt_hole_dia) * \
                                   member_detail_iter[2]

                            t_db = 2 * IS800_2007.cl_6_4_1_block_shear_strength(A_vg=a_vg, A_vn=a_vn, A_tg=a_tg,
                                                                                A_tn=a_tn,
                                                                                f_u=member_detail_iter[3],
                                                                                f_y=member_detail_iter[4])
                        if t_db < design_load_iter:
                            block_shear_failure = True
                        elif t_db > design_load_iter:
                            block_shear_failure = False
                    elif no_rows1 == 1:
                        block_shear_failure = False

                """ now checking block shear failure for the gusset plate. gusset_t_db = gusset block shear strength """
                gusset_block_shear_failure = False
                gusset_a_vg = (edge_dist1 + (no_column1 - 1) * pitch1) * gusset_plate_t_fu_fy[0] * 2
                gusset_a_vn = (edge_dist1 + (no_column1 - 1) * pitch1 - (no_column1 - 0.5) * bolt1.bolt_hole_dia) * \
                       gusset_plate_t_fu_fy[0] * 2
                gusset_a_tg = (no_rows1 - 1) * gauge1 * gusset_plate_t_fu_fy[0]
                gusset_a_tn = ((no_rows1 - 1) * gauge1 - (no_rows1 - 1) * bolt1.bolt_hole_dia) * \
                       gusset_plate_t_fu_fy[0]

                gusset_t_db = IS800_2007.cl_6_4_1_block_shear_strength(A_vg=gusset_a_vg, A_vn=gusset_a_vn,
                                                                       A_tg=gusset_a_tg,
                                                                       A_tn=gusset_a_tn,
                                                                       f_u=gusset_plate_t_fu_fy[1],
                                                                       f_y=gusset_plate_t_fu_fy[2])
                if gusset_t_db < design_load_iter:
                    block_shear_failure = True
                    """ coming out of bolt grade loop """
                    break
                elif gusset_t_db > design_load_iter:
                    block_shear_failure = False

                """ now storing the design data in a list called recommended_bolt which looks as follows:
                 [dia, grade, num_bolts, rows, columns, group_capacity, block_shear_status, overlap_length, e, p, g ]"""
                recommended_bolt = [bolt_dia1, bolt_grade1, no_bolts2, no_rows1, no_column1, bolt_group_capacity1,
                                    block_shear_failure, overlap_length, edge_dist1, pitch1, gauge1]

                candidate_bolts1 = candidate_bolts1 + [recommended_bolt]
                recommended_bolt = []




            if large_grip1:
                """ going for the next diameter in the diameter loop """
                continue

            if no_rows < 1:
                """ going for the next diameter in the diameter loop """
                continue

            if no_bolts1 < 2:
                """ going for the next diameter in the diameter loop """
                continue

            if safe_whitmore_section == False:
                """ coming out of bolt dia loop """
                break
            else:
                pass

            if gusset_block_shear_failure == True:
                """ coming out of bolt dia loop """
                break
        if safe_whitmore_section == False:
            """ coming out of members loop """
            break
        else:
            pass

        if gusset_block_shear_failure == True:
            """ coming out of member loop """
            break

        """ storing the bolts eligible for each member """
        candidate_bolts_all = candidate_bolts_all + candidate_bolts1
        candidate_bolts1 = []
    if safe_whitmore_section == False:
        """ going for the next thickness of the plate """
        continue

    if gusset_block_shear_failure == True:
        """ going for the next thickness of the plate """
        continue

    """ now selecting the final bolts for each member """
    """ first of we will check if the bolt_dia and grade of all the members are same then those will be selected """
    final_selected_bolts = []
    for p in reversed(candidate_bolts_all[0]):
        final_selected_bolts = final_selected_bolts + [p]
        for q in range(1, (len(candidate_bolts_all-1))):
            for r in reversed(q):
                if p[0] == r[0] and p[1] == r[1]:
                    final_selected_bolts = final_selected_bolts + [r]
                else:
                    continue

        if len(final_selected_bolts) == len(member_details):
            break
        else:
            continue

    """ if no common bolt_dia and grade is found then going to selected those with common grade but with different 
    diameter """
    if len(final_selected_bolts) != len(member_details):
        final_selected_bolts = []
        for p in reversed(candidate_bolts_all[0]):
            final_selected_bolts = final_selected_bolts + [p]
            for q in range(1, (len(candidate_bolts_all - 1))):
                for r in reversed(q):
                    if p[1] == r[1]:
                        final_selected_bolts = final_selected_bolts + [r]
                    else:
                        continue

            if len(final_selected_bolts) == len(member_details):
                break
            else:
                continue

    """if no bolts with common diameter and grade are there then go for the first entries from the last """
    if len(final_selected_bolts) != len(member_details):
        final_selected_bolts = []
        for p in candidate_bolts_all:
            final_selected_bolts += [p[len(p)-1]]













print(bolt_general.cl_10_2_1_bolt_hole_size(22))
print(Bolt().calculate_kb(40, 30, 12, 400, 410))
print(IS800_2007.cl_10_2_1_bolt_hole_size(22))
print(bolt_general(4.6, 22).bolt_hole_dia)
print(str(bolt_general(4.6, 20).fu_b))
# print(Bolt().calculate_bolt_capacity(20, 4.6, [[8,410,250],[6,410,250]],1))
# print(IS1367_Part3_2002.get_bolt_fu_fy(4.6, 12))
