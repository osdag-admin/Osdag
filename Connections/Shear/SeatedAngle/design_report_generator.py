import time
import math
from seat_angle_calc import SeatAngleCalculation


class ReportGenerator(SeatAngleCalculation):
    """Generate Design Report for Seated Angle Connection.

    Attributes (Inherited from SeatAngleCalculation):
        gamma_mb (float): partial safety factor for material - resistance of connection - bolts
        gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling
        gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress
        beam_col_clear_gap (int): design preference 
        bolt_hole_clearance (float)
        bolt_hole_type (string): "Standard" or "Over-sized"
        bolt_fu_overwrite (float)
        mu_f (float): slip factor for Friction Grip Bolt bolt calculations
        min_edge_multiplier (float): multiplier for min edge distance check - based on edge type
        type_of_edge (string): The type is used in determining the min_edge_distance 
        is_environ_corrosive (string): 'Yes' or 'No'
        design_method (string)
        root_clearance_sa (int): clearance of first bolt from the root of seated angle
        root_clearance_col (int): clearance of first bolt from the root of supporting column

        top_angle (string)
        top_angle_recommended (string)
        connectivity (string)
        beam_section (string)
        column_section (string)
        beam_fu (float)
        beam_fy (float)
        column_fu (float)
        column_fy (float)        
        angle_fy (float)
        angle_fu (float)
        shear_force (float)
        bolt_diameter (int)
        bolt_type (string)
        bolt_grade (float)
        bolt_fu (int)        
        bolt_hole_diameter (int)
        angle_sec (string)
        dict_angle_data (dictionary) = model.get_angledata(angle_sec)
        beam_w_t (float): beam web thickness
        beam_f_t (float): beam flange thickness
        beam_d  (float): beam depth
        beam_w_f  (float): beam width
        beam_R1 (float): beam root radius
        column_f_t (float): column flange thickness
        column_d (float): column depth
        column_w_f (float): column width
        column_R1 (float): column root radius
        angle_t (float): angle thickness
        angle_A  (float): longer leg of unequal angle
        angle_B  (float): shorter leg of unequal angle
        angle_R1 (float)
        angle_l (float)
        thickness_governing_min (float): minimum of angle leg and column web/flange thickness

        safe (Boolean) : status of connection, True if safe

        moment_at_root_angle (float)
        moment_capacity_angle (float): Moment capacity of outstanding leg of seated angle
        is_shear_high (boolean): True if the seated angle leg is in high shear [Cl 8.2.1]
        
        leg_moment_d (float): Moment capacity of outstanding leg of seated angle with low shear
        outstanding_leg_shear_capacity (float)
        outstanding_leg_length_required (float)
        beam_shear_strength (float)
        bolt_shear_capacity (float)
        k_b (float)
        bolt_bearing_capacity (float)
        bolt_value (float)
        bolt_group_capacity (float)
        bolts_required (int)
        num_rows (int)
        num_cols (int)
        pitch (float)
        gauge (float)
        min_end_dist (int)
        min_edge_dist (int)
        min_pitch (int)
        min_gauge (int)
        end_dist (int)
        edge_dist (int)
        max_spacing (int)
        max_edge_dist (int)
        top_angle_end_dist_beam (int)
        top_angle_end_dist_column (int)

        company_name (string)
        company_logo (string)

        group_team_name (string)
        designer (string)
        project_title (string)
        sub_title (string)
        job_number (string)
        method (string)

    """

    def __init__(self, sa_calc_object):
        """
        Args:
            sa_calc_object (SeatAngleCalculation): SeatAngleCalculation class instance

        Returns:
            None
        """
        super(ReportGenerator, self).__init__()
        self.gamma_mb = sa_calc_object.gamma_mb
        self.gamma_m0 = sa_calc_object.gamma_m0
        self.gamma_m1 = sa_calc_object.gamma_m1
        self.beam_col_clear_gap = sa_calc_object.beam_col_clear_gap
        self.bolt_hole_clearance = sa_calc_object.bolt_hole_clearance_value
        self.bolt_hole_type = sa_calc_object.bolt_hole_type
        self.bolt_fu_overwrite = sa_calc_object.bolt_fu_overwrite
        self.mu_f = sa_calc_object.mu_f
        self.min_edge_multiplier = sa_calc_object.min_edge_multiplier
        self.type_of_edge = sa_calc_object.type_of_edge
        self.is_environ_corrosive = sa_calc_object.is_environ_corrosive
        self.design_method = sa_calc_object.design_method
        self.root_clearance_sa = sa_calc_object.root_clearance_sa
        self.root_clearance_col = sa_calc_object.root_clearance_col
        self.is_friction_grip_bolt = sa_calc_object.is_friction_grip_bolt
        self.top_angle = sa_calc_object.top_angle
        self.top_angle_recommended = sa_calc_object.top_angle_recommended
        self.connectivity = sa_calc_object.connectivity
        self.beam_section = sa_calc_object.beam_section
        self.column_section = sa_calc_object.column_section
        self.beam_fu = sa_calc_object.beam_fu
        self.beam_fy = sa_calc_object.beam_fy
        self.column_fu = sa_calc_object.column_fu
        self.column_fy = sa_calc_object.column_fy
        self.angle_fy = sa_calc_object.angle_fy
        self.angle_fu = sa_calc_object.angle_fu
        self.shear_force = sa_calc_object.shear_force
        self.bolt_diameter = sa_calc_object.bolt_diameter
        self.bolt_type = sa_calc_object.bolt_type
        self.bolt_grade = sa_calc_object.bolt_grade
        self.bolt_fu = sa_calc_object.bolt_fu
        self.bolt_hole_diameter = sa_calc_object.bolt_hole_diameter
        self.angle_sec = sa_calc_object.angle_sec
        self.dict_angle_data = sa_calc_object.dict_angle_data
        self.beam_w_t = sa_calc_object.beam_w_t
        self.beam_f_t = sa_calc_object.beam_f_t
        self.beam_d = sa_calc_object.beam_d
        self.beam_w_f = sa_calc_object.beam_b
        self.beam_R1 = sa_calc_object.beam_R1
        self.column_f_t = sa_calc_object.column_f_t
        self.column_d = sa_calc_object.column_d
        self.column_w_f = sa_calc_object.column_b
        self.column_R1 = sa_calc_object.column_R1
        self.angle_t = sa_calc_object.angle_t
        self.angle_A = sa_calc_object.angle_A
        self.angle_B = sa_calc_object.angle_B
        self.angle_R1 = sa_calc_object.angle_R1
        self.angle_l = sa_calc_object.angle_l
        self.thickness_governing_min = sa_calc_object.thickness_governing_min

        self.safe = sa_calc_object.safe
        self.output_dict = sa_calc_object.output_dict

        self.moment_at_root_angle = sa_calc_object.moment_at_root_angle
        self.moment_capacity_angle = sa_calc_object.moment_capacity_angle
        self.is_shear_high = sa_calc_object.is_shear_high
        self.moment_high_shear_beta = sa_calc_object.moment_high_shear_beta
        self.leg_moment_d = sa_calc_object.leg_moment_d
        self.outstanding_leg_shear_capacity = sa_calc_object.outstanding_leg_shear_capacity
        self.outstanding_leg_length_required = sa_calc_object.outstanding_leg_length_required
        self.beam_shear_strength = sa_calc_object.beam_shear_strength
        self.bolt_shear_capacity = sa_calc_object.bolt_shear_capacity
        self.k_b = sa_calc_object.k_b
        self.bolt_bearing_capacity = sa_calc_object.bolt_bearing_capacity
        self.bolt_value = sa_calc_object.bolt_value
        self.bolt_group_capacity = sa_calc_object.bolt_group_capacity
        self.bolts_required = sa_calc_object.bolts_required
        self.bolts_provided = sa_calc_object.bolts_provided
        self.num_rows = sa_calc_object.num_rows
        self.num_cols = sa_calc_object.num_cols
        self.pitch = sa_calc_object.pitch
        self.gauge = sa_calc_object.gauge
        self.min_end_dist = sa_calc_object.min_end_dist
        self.min_edge_dist = sa_calc_object.min_edge_dist
        self.min_pitch = sa_calc_object.min_pitch
        self.min_gauge = sa_calc_object.min_gauge
        self.end_dist = sa_calc_object.end_dist
        self.edge_dist = sa_calc_object.edge_dist
        self.max_spacing = sa_calc_object.max_spacing
        self.max_edge_dist = sa_calc_object.max_edge_dist
        self.top_angle_end_dist_beam = sa_calc_object.top_angle_end_dist_beam
        self.top_angle_end_dist_column = sa_calc_object.top_angle_end_dist_column

        self.company_name = ""
        self.company_logo = ""

        self.group_team_name = ""
        self.designer = ""
        self.project_title = ""
        self.sub_title = ""
        self.job_number = ""
        self.client = ""

    def save_html(self, report_summary, file_name, folder):
        """Create and save html report for Seated angle connection.

        Args:
            report_summary (dict): Structural Engineer details design report
            file_name (string): Name of design report file
            folder (path): Location of folder to save design report

        Returns:
            None
            """
        myfile = open(file_name, "w")
        myfile.write(t('! DOCTYPE html') + nl())
        myfile.write(t('html') + nl())
        myfile.write(t('head') + nl())
        myfile.write(t('link type="text/css" rel="stylesheet" ') + nl())

        myfile.write(html_space(4) + t('style'))
        myfile.write('table{width= 100%; border-collapse:collapse; border:1px solid black collapse}')
        myfile.write('th,td {padding:3px}' + nl())
        myfile.write(html_space(8) + 'td.detail{background-color:#D5DF93; font-size:20; '
                                     'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.detail1{font-size:20; '
                                     'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.detail2{font-size:20;'
                                     ' font-family:Helvetica, Arial, Sans Serif}' + nl())
        myfile.write(html_space(8) + 'td.header0{background-color:#8fac3a; font-size:20;'
                                     ' font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.header1{background-color:#E6E6E6; font-size:20;'
                                     ' font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.header2{font-size:20; width:50%}' + nl())
        myfile.write(html_space(4) + t('/style') + nl())

        myfile.write(t('/head') + nl())
        myfile.write(t('body') + nl())

        # Project summary
        self.company_name = str(report_summary["ProfileSummary"]['CompanyName'])
        self.company_logo = str(report_summary["ProfileSummary"]['CompanyLogo'])

        self.group_team_name = str(report_summary["ProfileSummary"]['Group/TeamName'])
        self.designer = str(report_summary["ProfileSummary"]['Designer'])
        self.project_title = str(report_summary['ProjectTitle'])
        self.sub_title = str(report_summary['Subtitle'])
        self.job_number = str(report_summary['JobNumber'])
        self.client = str(report_summary['Client'])
        additional_comments = str(report_summary['AdditionalComments'])

        # Seated angle design parameters
        connectivity = str(self.connectivity)
        shear_force = str(self.shear_force)
        column_sec = str(self.column_section)
        column_fu = str(self.column_fu)
        beam_sec = str(self.beam_section)
        seated_angle_section = str(self.angle_sec)
        top_angle_section = str(self.top_angle)
        angle_fu = str(self.angle_fu)

        bolt_type = str(self.bolt_type)

        is_friction_grip_bolt = self.is_friction_grip_bolt
        bolt_grade = str(self.bolt_grade)
        bolt_diameter = str(self.bolt_diameter)
        bolt_fu = str(self.bolt_fu)

        # Design Preferences
        beam_col_clear_gap = str(self.beam_col_clear_gap)
        bolt_hole_clearance = str(self.bolt_hole_clearance)
        bolt_hole_type = str(self.bolt_hole_type)
        bolt_fu_overwrite = self.bolt_fu_overwrite
        slip_factor_mu_f = self.mu_f
        min_edge_multiplier = self.min_edge_multiplier
        type_of_edge = self.type_of_edge
        is_environ_corrosive = self.is_environ_corrosive
        design_method = self.design_method

        # Calculation outputs
        bolts_provided = str(self.bolts_provided)
        bolts_required = str(self.bolts_required)

        number_of_rows = str(self.num_rows)
        number_of_cols = str(self.num_cols)
        edge = str(self.edge_dist)
        gauge = str(self.gauge)
        pitch = str(self.pitch)
        end = str(self.end_dist)

        kb = str(self.k_b)
        beam_w_t = str(self.beam_w_t)
        beam_fu = str(self.beam_fu)
        dia_hole = str(self.bolt_hole_diameter)
        shear_capacity = str(self.bolt_shear_capacity)
        bearing_capacity = str(self.bolt_bearing_capacity)

        check_pass = "<p align=left style=color:green><b>Pass</b></p>"
        check_fail = "<p align=left style=color:red><b>Fail</b></p>"

        if self.safe == True:
            remark = check_pass
        elif self.safe == False:
            remark = check_fail

        # -----------------------------------------------------------------------------------
        rstr = self.design_report_header()
        # -----------------------------------------------------------------------------------

        # Design conclusion
        rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ') + nl()

        rstr += design_summary_row(0, "Design Conclusion", "header0", col_span="2")

        row = [1, "Seated Angle", remark]
        rstr += t('tr')
        rstr += html_space(1) + t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail1"') + row[2] + t('/td') + nl()
        # rstr += t('td class="header1 safe"') + row[3] + t('/td')
        rstr += t('/tr')

        rstr += design_summary_row(0, "Seated Angle", "header0", col_span="2")
        rstr += design_summary_row(0, "Connection Properties", "detail", col_span="2")
        rstr += design_summary_row(0, "Connection ", "detail1", col_span="2")
        rstr += design_summary_row(1, "Connection Title", "detail2", text_two=" Seated Angle")
        rstr += design_summary_row(1, "Connection Type", "detail2", text_two=" Shear Connection")
        rstr += design_summary_row(0, "Connection Category", "detail1")
        rstr += design_summary_row(1, "Connectivity", "detail2", text_two=str(connectivity))
        rstr += design_summary_row(1, "Beam Connection", "detail2", text_two="Bolted")
        rstr += design_summary_row(1, "Column Connection", "detail2", text_two="Bolted")
        rstr += design_summary_row(0, "Loading (Factored Load)", "detail1")
        rstr += design_summary_row(1, "Shear Force (kN)", "detail2", text_two=str(shear_force))
        rstr += design_summary_row(0, "Components ", "detail1", col_span="2")
        rstr += design_summary_row(1, "Column Section", "detail1", text_two=str(column_sec), text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(column_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=str(bolt_hole_type))
        rstr += design_summary_row(1, "Beam Section", "detail1", text_two=str(beam_sec), text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(beam_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=str(bolt_hole_type))
        rstr += design_summary_row(1, "Seated Angle Section", "detail1", text_two=str(seated_angle_section),
                                   text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(angle_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=str(bolt_hole_type))
        rstr += design_summary_row(1, "Top Angle Section", "detail1", text_two=str(top_angle_section),
                                   text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(angle_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=bolt_hole_type)
        rstr += design_summary_row(1, "Bolts", "detail1", col_span="2")
        rstr += design_summary_row(2, "Type", "detail2", text_two=bolt_type)
        rstr += design_summary_row(2, "Grade", "detail2", text_two=bolt_grade)
        rstr += design_summary_row(2, "Diameter (mm)", "detail2", text_two=bolt_diameter)
        rstr += design_summary_row(2, "Bolts - Required", "detail2", text_two=bolts_required)
        rstr += design_summary_row(2, "Bolts - Provided", "detail2", text_two=bolts_provided)
        rstr += design_summary_row(2, "Rows", "detail2", text_two=number_of_rows)
        rstr += design_summary_row(2, "Columns", "detail2", text_two=number_of_cols)
        rstr += design_summary_row(2, "Gauge (mm)", "detail2", text_two=gauge)
        rstr += design_summary_row(2, "Pitch (mm)", "detail2", text_two=pitch)
        rstr += design_summary_row(2, "End Distance (mm)", "detail2", text_two=end)
        rstr += design_summary_row(2, "Edge Distance (mm)", "detail2", text_two=edge)
        rstr += design_summary_row(0, "Assembly", "detail1", col_span="2")
        rstr += design_summary_row(1, "Column-Beam Clearance (mm)", "detail2", text_two=beam_col_clear_gap,
                                   text_two_css="detail2")

        rstr += " " + nl() + t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------

        # Design Preferences
        rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ') + nl()

        rstr += design_summary_row(0, "Design Preferences", "detail", col_span="2")
        rstr += design_summary_row(0, "Bolt ", "detail1", col_span="2")
        rstr += design_summary_row(1, "Hole Type", "detail2", text_two=str(bolt_hole_type) + " Hole")
        rstr += design_summary_row(1, "Material Grade Fu (MPa) (overwrite)", "detail2", text_two=str(bolt_fu_overwrite))

        if is_friction_grip_bolt:
            rstr += design_summary_row(1, "Slip Factor", "detail2", text_two=str(slip_factor_mu_f))
        rstr += design_summary_row(0, "Detailing", "detail1", col_span="2")
        rstr += design_summary_row(1, "Type of Edge", "detail2", text_two=str(type_of_edge)[4:])
        rstr += design_summary_row(1, "Minimum Edge Distance check multiplier", "detail2",
                                   text_two=str(min_edge_multiplier) + " * bolt_hole_diameter")
        rstr += design_summary_row(1, "Are members exposed to corrosive influences?", "detail2",
                                   text_two=str(is_environ_corrosive))
        rstr += design_summary_row(1, "Gap between Beam and Column (mm)", "detail2", text_two=str(beam_col_clear_gap))
        rstr += design_summary_row(0, "Design", "detail1", col_span="2")
        rstr += design_summary_row(1, "Design Method", "detail2", text_two=str(design_method))

        rstr += " " + nl() + t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------

        # DESIGN CHECKS
        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black" table-layout:fixed')
        rstr += t('tr')
        rstr += t('td style="width:200px;"')
        rstr += t('td width="50%"')
        rstr += t('td width="50%"')
        rstr += t('td style="width:50px;"')
        rstr += t('/tr')
        rstr += design_check_row("Design Check", "", "", "", col_span="4", text_one_css="detail")

        rstr += design_check_row("Check", "Required", "Provided", "Remark", text_one_css="header1",
                                 text_two_css="header1", text_three_css="header1", text_four_css="header1")

        # Bolt
        rstr += design_check_row("Bolt Checks", "", "", "", col_span="4", text_one_css="detail")

        # Bolt shear capacity (kN)
        const = str(round(math.pi / 4 * 0.78, 4))

        if is_friction_grip_bolt == False:
            req_field = "<i>V</i><sub>dsb</sub> = bolt_fu*(pi*0.78/4)*bolt_diameter^2/(&#8730;3)/" \
                        "<i>gamma<sub>mb</sub></i><br> [cl. 10.3.3]"
            prov_field = "<i>V</i><sub>dsb</sub> = " + bolt_fu + "*(" + const + ")*" + bolt_diameter + "^2/" \
                         + "(&#8730;3)/1.25/1000 <br> " + space(2) + "= " + shear_capacity

        elif is_friction_grip_bolt == True:
            if bolt_hole_type == "Standard":
                K_h = str(1.0)
            elif bolt_hole_type == "Oversized":
                K_h = str(0.85)

            req_field = "Friction Grip Bolt bolt shear capacity:"
            # req_field += "<br> <i>V</i><sub>dsf</sub> = mu_f*n_e*K_h*A_nb*f_0/<i>gamma<sub>mb</sub></i>"
            req_field += "<br> [cl. 10.3.3]"
            prov_field = "<i>V</i><sub>dsf</sub> = ("
            prov_field += str(
                slip_factor_mu_f) + ")*(1)*(" + K_h + ")*(" + const + "*" + bolt_diameter + "^2)<br>" + space(2) + \
                          "*(0.70*" + bolt_fu + ")" + "/1.25/1000 <br> " + space(2) + "= " + shear_capacity
        rstr += design_check_row("Bolt shear capacity (kN)", req_field, prov_field, " ")

        # Bolt bearing capacity (kN)
        # req_field = "<i>V<sub>dpb</sub></i> = 2.5*k<sub>b</sub>*bolt_diameter*critical_thickness" \
        #             +"<br> *<i>f</i><sub>u</sub>/<i>gamma<sub>mb</sub></i><br> [Cl. 10.3.4]"
        req_field = "<i>V<sub>dpb</sub></i>:<br> [Cl. 10.3.4]"

        if is_friction_grip_bolt == False:
            prov_field = "<i>V</i><sub>dpb</sub> = 2.5*" + kb + "*" + bolt_diameter + "*" + beam_w_t + "*" \
                        + beam_fu + "/1.25/1000)  <br>" + space(2) + " = " + bearing_capacity + " kN"
        elif is_friction_grip_bolt == True:
            prov_field = 'N/A'
        rstr += design_check_row("Bolt bearing capacity (kN)", req_field, prov_field, "")

        # Bolt capacity (kN)
        req_field = "min (bolt_shear_capacity, bolt_bearing_capacity)"
        prov_field = "min (" + str(self.bolt_shear_capacity) + ", " + str(self.bolt_bearing_capacity) + ") = " \
                     + str(self.bolt_value)
        rstr += design_check_row("Bolt capacity (kN)", req_field, prov_field, "")

        # No. of bolts
        # bolts = str(round(float(shear_force) / float(str(self.bolt_value)), 1))
        bolts_req_based_on_force = (math.ceil(float(shear_force) / self.bolt_value))
        if bolts_req_based_on_force > self.bolts_provided:
            remark = check_fail
        else:
            remark = check_pass
        # req_field = "shear_force/ bolt_value = " + str(shear_force) + "/" + str(self.bolt_value) + " = " \
        req_field = str(shear_force) + "/" + str(self.bolt_value) + " = " \
                    + str(bolts_req_based_on_force)
        rstr += design_check_row("No. of bolts", req_field, bolts_provided, remark)

        rstr += design_check_row("No. of columns", " ", number_of_cols, " ")
        rstr += design_check_row("No. of row(s)", " &#8804; 2", number_of_rows, " ")

        # Bolt pitch (mm)
        if self.pitch >= self.min_pitch and self.pitch <= self.max_spacing:
            remark = check_pass
            # req_field = " &#8805; 2.5*bolt_diameter ,<br>  &#8804; min(32*thickness_governing_min, 300) "
            req_field = "<br> &#8805; 2.5* " + bolt_diameter + " = " + str(self.min_pitch) + ",<br>  &#8804; min(32*" + \
                         str(self.thickness_governing_min) + ", 300) = " + str(self.max_spacing) + "<br> [cl. 10.2.2] <br>"
            prov_field = pitch
        elif self.pitch < self.min_pitch or self.pitch > self.max_spacing:
            if self.num_rows == 1:
                remark = " "
                req_field = "N/A"
                prov_field = "N/A"
            else:
                remark = check_fail
                # req_field = " &#8805; 2.5*bolt_diameter ,<br>  &#8804; min(32*thickness_governing_min, 300)"
                req_field = "<br> &#8805; 2.5* " + bolt_diameter + " = " + str(
                    self.min_pitch) + ",<br>  &#8804; min(32*" + \
                             str(self.thickness_governing_min) + ", 300) = " + str(self.max_spacing) + "<br> [cl. 10.2.2] <br>"
                prov_field = pitch
        rstr += design_check_row("Bolt pitch (mm)", req_field, prov_field, remark)

        # Bolt gauge (mm)
        if self.gauge >= self.min_gauge and self.gauge <= self.max_spacing:
            remark = check_pass
        elif self.gauge < self.min_gauge or self.gauge > self.max_spacing:
            remark = check_fail
        # req_field = " &#8805; 2.5*bolt_diameter ,<br>  &#8804; min(32*thickness_governing_min, 300)"
        req_field = "<br> &#8805; 2.5*" + bolt_diameter + " = " + str(self.min_gauge) + ",<br> &#8804; min(32*" + \
                     str(self.thickness_governing_min) + ", 300) = " + str(self.max_spacing) + "<br> [cl. 10.2.2] <br>"
        rstr += design_check_row("Bolt gauge (mm)", req_field, gauge, remark)

        # End distance (mm)
        if self.end_dist >= self.min_end_dist:
            remark = check_pass
        elif self.end_dist < self.min_end_dist:
            remark = check_fail
        # req_field = " &#8805;" + str(self.min_edge_multiplier) + "*bolt_hole_diameter" + " [cl. 10.2.4.2]"
        req_field = "<br> &#8805;" + str(self.min_edge_multiplier) + "*" + dia_hole + " = " + str(self.min_end_dist)
        rstr += design_check_row("End distance (mm)", req_field, end, remark)

        # Edge distance (mm)
        if self.edge_dist >= self.min_edge_dist and self.edge_dist <= self.max_edge_dist:
            remark = check_pass
        elif self.edge_dist < self.min_edge_dist or self.edge_dist > self.max_edge_dist:
            remark = check_fail
        # req_field = " &#8805;" + str(self.min_edge_multiplier) + "*bolt_hole_diameter,"
        req_field = " &#8805;" + str(self.min_edge_multiplier) + "*" + dia_hole + " = " + str(self.min_edge_dist) + " [cl. 10.2.4.2]<br>"
        # Cl 10.2.4.3 if members are exposed to corrosive influences
        if is_environ_corrosive == "Yes":
            req_field += "<br><br> As the members are exposed to corrosive influences: "
            # req_field += "<br> &#8804; min(12*thickness_governing_min*sqrt(250/f_y),<br>" + space(
            #     2) + "  40+4*thickness_governing_min)"
            req_field += "<br> [Cl 10.2.4.3]"
            req_field += "<br> &#8804; min(12*" + str(self.thickness_governing_min) + "*sqrt(250/" \
                         + str(self.angle_fy) + "), 40 + 4*" + str(self.thickness_governing_min)\
                         + ") = " + str(self.max_edge_dist)
        elif is_environ_corrosive == "No":
            # req_field += "<br><br> &#8804; 12*thickness_governing_min*sqrt(250/f_y)"
            req_field += "<br> &#8804; 12*" + str(self.thickness_governing_min) + "sqrt(250/" \
                         + str(self.angle_fy) + ") = " + str(self.max_edge_dist) + "[Cl 10.2.4.3]"
        rstr += design_check_row("Edge distance (mm)", req_field, edge, remark)

        # Seated angle
        rstr += design_check_row("Seated Angle " + str(self.angle_sec), "", "", "", col_span="4",
                                 text_one_css="detail")

        # Seated angle length
        if connectivity == "Column flange-Beam flange":
            # req_field = "= min(supported_beam_width,<br>"+space(2)+"supporting_column_width)"
            req_field = " <br> = min(" + str(self.beam_w_f) + ", " + str(self.column_w_f) + ")"
            prov_field = str(self.angle_l)
        elif connectivity == "Column web-Beam flange":
            # limiting_angle_length = self.column_d - 2 * self.column_f_t - 2 * self.column_R1 - self.root_clearance_col
            # self.angle_l = int(math.ceil(min(self.beam_w_f, limiting_angle_length)))
            # req_field = "= min(width of supported beam, <br>" + space(2) + \
            #             "column_depth - 2*column_flange_thickness<br>" + space(2) +\
            #             " - 2*column_R1 - root_clearance_col)"
            req_field = "<br> = min(" + str(self.beam_w_f) \
                        + ", " + str(self.column_d) + " - 2*" + str(self.column_f_t) \
                        + " - 2*" + str(self.column_R1) + " - " + str(self.root_clearance_col) + ")"
            prov_field = str(self.angle_l)
        # As the seated angle length is a determined/calculated parameter, there is no design 'check' remark
        rstr += design_check_row("Length (mm)", req_field, prov_field, " ")

        # Length of outstanding leg
        if self.outstanding_leg_length_required < self.angle_B:
            remark = check_pass
        elif self.outstanding_leg_length_required > self.angle_B:
            remark = check_fail
        # req_field = "b = (R*" + sub("gamma", "m0") + "/(" + sub("f", "yw") +\
        #             "*beam_web_thickness))<br>" + space(2) + "+ beam_column_clear_gap"
        req_field = "<br>[Cl. 8.7.4]"
        req_field += "<br> = (" + str(self.shear_force) + "*1000*" + str(self.gamma_m0) + "/(" + str(self.beam_fy) \
                     + "*" + str(self.beam_w_t) + ")) + " + str(self.beam_col_clear_gap)
        prov_field = str(self.angle_B)
        rstr += design_check_row("Outstanding leg length (mm)", req_field, prov_field, remark)

        # For angle thickness
        # Shear capacity of outstanding leg
        if self.outstanding_leg_shear_capacity > self.shear_force:
            remark = check_pass
        elif self.outstanding_leg_shear_capacity < self.shear_force:
            remark = check_fail
        req_field = sub("V", "dp") + " &#8805 V <br>"
        req_field += sub("V", "dp") + " &#8805 " + str(self.shear_force) + "kN <br> [Cl. 8.4.1]"
        # prov_field = sub("V", "dp") + "=" + sub("A", "v") + sub("f", "yw") + "/ (&#8730 3 *" + sub("gamma", "m0") + ")"
        prov_field = "<br>" + space(1) + "= (" + str(self.angle_l) + "*" + str(self.angle_t)\
                      + ")*" + str(self.angle_fy) + "/ (&#8730 3 *" + str(self.gamma_m0)\
                      + ")<br>" + space(1) + "= " + str(self.outstanding_leg_shear_capacity)
        rstr += design_check_row("Shear capacity of outstanding leg (kN)", req_field, prov_field,
                                 remark)

        # Moment capacity of outstanding leg
        if self.is_shear_high == False:
            req_field = "As V &#8804 0.6 " + sub("V", "d")
            req_field += ",<br>[Cl 8.2.1.2] is applicable <br>"
            req_field += sub("M", "d") + " &#8805 Moment at root of angle"
            req_field += "<br>" + sub("M", "d") + " &#8805 " + str(self.moment_at_root_angle)
            prov_field = sub("M", "d") + " = min(" + sub("beta", "b") + sub("Z", "e") + sub("f", "y")
            prov_field += "/" + sub("gamma", "m0") + ", <br>" + space(1) +\
                          " 1.5" + sub("Z", "e") + sub("f","y") + "/" + sub("gamma", "m0") + ")"
            prov_field += "<br>" + space(1) + " = min(1.0* " + str(self.angle_l) + "*(" + str(self.angle_t) + "^2/6)*"
            prov_field += str(self.angle_fy) + "/" + str(self.gamma_m0) + ",<br>" + space(2) \
                          + " 1.5*" + str(self.angle_l) + "*(" + str(self.angle_t) + "^2/6)*"
            prov_field += str(self.angle_fy) + "/" + str(self.gamma_m0) + ")"
            prov_field += "<br>" + space(1) + "= " + str(self.moment_capacity_angle)

        elif self.is_shear_high == True:
            req_field = "As V &#8805 0.6 " + sub("V", "d")
            req_field += ",<br>[Cl 8.2.1.3] is applicable"
            req_field += "<br>" + sub("M", "dv") + " &#8805 Moment at root of angle"
            req_field += "<br>" + sub("M", "dv") + " &#8805 " + str(self.moment_at_root_angle) + "<br>"
            prov_field = sub("M", "dv") + "= min((1 - beta)" + sub("M", "d") + " , "
            prov_field += "1.2 " + sub("Z", "e") + sub("f", "y") + "/" + sub("gamma", "m0") + ") <br>"
            prov_field += space(1) + "where, <br>" + space(2) + "beta = ((2V/" + sub("V", "d")\
                          + ")-1)^2 = " + str(round(self.moment_high_shear_beta, 4)) + "<br>"
            prov_field += "<br>" + sub("M", "dv") + " = " + "min((1 - " + str(round(self.moment_high_shear_beta, 4))\
                          + ")<br>" + space(1) + "*1.0*(" + str(self.angle_l) + "*" + str(self.angle_t) + "^2/6)*"
            prov_field += str(self.angle_fy) + "/" + str(self.gamma_m0) + " , "
            prov_field += "<br>" + space(1) + "1.2*(" + str(self.angle_l) + "*" + str(self.angle_t) + "^2/6)*"
            prov_field += str(self.angle_fy) + "/" + str(self.gamma_m0) + ")"
            prov_field += "<br>" + space(1) + " = " + str(self.moment_capacity_angle)

        if self.moment_capacity_angle > self.moment_at_root_angle:
            remark = check_pass
        elif self.moment_capacity_angle < self.moment_at_root_angle:
            remark = check_fail
        rstr += design_check_row("Moment capacity of outstanding leg (kN-mm)", req_field,
                                 prov_field, remark)

        # Top angle
        rstr += design_check_row("Top Angle", "", "", "", col_span="4", text_one_css="detail")
        req_field = "Recommended size (based on stability only): " + str(self.top_angle_recommended)
        prov_field = "User selected size: " + str(self.top_angle)
        rstr += design_check_row("Section ", req_field, prov_field, " ")

        # End distance (mm)
        if self.top_angle_end_dist_beam <= self.min_end_dist or \
            self.top_angle_end_dist_column <= self.min_end_dist:
            remark = check_fail
        else:
            remark = check_pass
        req_field = " &#8805;" + str(self.min_edge_multiplier) + "*bolt_hole_diameter" + " [cl. 10.2.4.2]"
        req_field += "<br> &#8805;" + str(self.min_edge_multiplier) + "*" + dia_hole + " = " + str(self.min_end_dist)
        prov_field = " on leg connected to Beam: " + str(self.top_angle_end_dist_beam)
        prov_field += "<br> on leg connected to Column: " + str(self.top_angle_end_dist_column)
        rstr += design_check_row("End distance (mm)", req_field, prov_field, remark)


        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------

        # Connection images (views)
        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

        # row = [0, "Views", " "]
        # rstr += t('tr')
        # rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
        # rstr += t('/tr')
        rstr += design_summary_row(0, "Views", "detail", col_span="2")

        if self.safe is True:
            png = folder + "/images_html/3D_Model.png"
            datapng = '<object type="image/PNG" data= %s width ="450"></object">' % png

            side = folder + "/images_html/seatSide.png"
            dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side

            top = folder + "/images_html/seatTop.png"
            datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top

            front = folder + "/images_html/seatFront.png"
            datafront = '<object type="image/PNG" data= %s width ="450"></object>' % front

            row = [0, datapng, datatop]
            rstr += t('tr') + nl()
            rstr += html_space(4) + t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td') + nl()
            rstr += html_space(4) + t('td  align="center" class=" header2"') + row[2] + t('/td') + nl()
            rstr += t('/tr' + nl())

            row = [0, dataside, datafront]
            rstr += t('tr') + nl()
            rstr += html_space(4) + t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td') + nl()
            rstr += html_space(4) + t('td align="center" class=" header2 "') + row[2] + t('/td') + nl()
            rstr += t('/tr') + nl()

        else:
            pass

        rstr += t('/table') + nl() + " " + nl()
        rstr += t('h1 style="page-break-before:always"')
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------

        rstr += t('hr')
        rstr += t('/hr') + nl() + " " + nl()

        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"') + nl()
        rstr += html_space(1) + t('''col width=30%''')
        rstr += html_space(1) + t('''col width=70%''') + nl()

        rstr += html_space(1) + t('tr') + nl()
        row = [0, "Additional Comments", additional_comments]
        rstr += html_space(2) + t('td class= "detail1"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(2) + t('td class= "detail2" align="justified"') + row[2] + t('/td') + nl()
        rstr += html_space(1) + t('/tr') + nl()

        rstr += t('/table') + nl()

        myfile.write(rstr)
        myfile.write(t('/body'))
        myfile.write(t('/html'))
        myfile.close()

    def design_report_header(self):
        """Create and return html code to display Report Header.

        Args:            

        Returns:
            rstr (str): string containing html code to table (used as Report Header)
        """
        rstr = nl() + " " + nl() + t('table border-collapse= "collapse" border="1px solid black" width=100%') + nl()
        rstr += t('tr') + nl()
        row = [0, '<object type= "image/PNG" data= "cmpylogoSeatAngle.png" height=60 ></object>',
               '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp" "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp"></object>']
        rstr += html_space(1) + t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(1) + t('td colspan="2" align= "center"') + row[2] + t('/td') + nl()
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Company Name", "detail", text_two=self.company_name, is_row=False)
        rstr += design_summary_row(0, "Project Title", "detail", text_two=self.project_title, is_row=False)
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Group/Team Name", "detail", text_two=self.group_team_name, is_row=False)
        rstr += design_summary_row(0, "Subtitle", "detail", text_two=self.sub_title, is_row=False)
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Designer", "detail", text_two=self.designer, is_row=False)
        rstr += design_summary_row(0, "Job Number", "detail", text_two=self.job_number, is_row=False)
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Date", "detail", text_two=time.strftime("%d /%m /%Y"), is_row=False)
        rstr += design_summary_row(0, "Client", "detail", text_two=self.client, is_row=False)
        rstr += t('/tr')
        rstr += t('/table') + nl() + " " + nl()

        rstr += t('hr')
        rstr += t('/hr') + nl() + " " + nl()
        return rstr


def space(n):
    """Create html code to create tab space in html-output.

    Args:
        n (int): number of tab spaces to be created in the html-output.

    Returns:
        rstr (str): html code that creates 'n' number of tab spaces.
    """
    rstr = "&nbsp;" * 4 * n
    return rstr


def t(param):
    """Enclose argument in html tag.

    Args:
        param (str): parameter to be enclosed in html tag <>.

    Returns:
        rstr (str): given param enclosed in html tag <>.
    """
    return '<' + param + '>'


def w(n):
    """Enclose argument in curly brace parenthesis.

    Args:
        n (str): parameter to be enclosed in curly brace parenthesis.

    Returns:
        rstr (str): given param enclosed in curly brace parenthesis.
    """
    return '{' + n + '}'


def quote(m):
    """Enclose argument in double quotes.

    Args:
        m (str): parameter to be enclosed in double quotes

    Returns:
        rstr (str): given param enclosed in double quotes
    """
    return '"' + m + '"'


def nl():
    """Create new line.

    Args:        

    Returns:
        new line tag.

    Note:
        Instead of directly inserting the new line tag '\n' in the code, this function was created,
        to enable custom formatting in future.
    """
    return '\n'


def html_space(n):
    """Create space in html code.

    Args:
        n (int): number of spaces to be created in the html-code.

    Returns:
        (str): specified number_of_spaces
    """
    return " " * n


def sub(string, subscript):
    """Create html code to display subscript.

    Args:
        string (str):
        subscript (str): string to be subscript

    Returns:
        (str): html code with concatenated string and subscript
    """
    return string + "<sub>" + subscript + "</sub>"


def design_summary_row(tab_spaces, text_one, text_one_css, **kwargs):
    """Create formatted html row entry for design summary table.

    Args:
        tab_spaces (int): number of (tab) spaces
        text_one (str): Text entry
        text_one_css (str): Key pointing to table-data css format

    kwargs:
        text_two (str): Text entry
        text_two_css (str): Key pointing to table-data css class
        col_span (str): number of columns in table that the table data spans
        is_row (boolean): key to create separate table row entry

    Returns (str):
        Formatted line of html-code.

    """
    text_two = kwargs.get('text_two', " ")
    text_two_css = kwargs.get('text_two_css', text_one_css)
    col_span = kwargs.get('col_span', "1")
    is_row = kwargs.get('is_row', True)

    row_string = ""  # default
    if is_row == True:
        row_string = t('tr') + nl()

    if col_span != "1":
        row_string = row_string + html_space(4) + t('td colspan=' + col_span + ' class="' + text_one_css + '"') + space(
            tab_spaces) + text_one + t('/td') + nl()
    else:
        row_string = row_string + html_space(4) + t('td class="' + text_one_css + '"') + space(tab_spaces) + text_one \
                     + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + text_two_css + '"') + text_two + t('/td') + nl()

    if is_row == True:
        row_string = row_string + t('/tr') + nl()

    return row_string


def design_check_row(text_one, text_two, text_three, text_four, **kwargs):
    """Create formatted html row entry for design check table.

    Args:
        text_one (str): Detail check name
        text_two (str): Required field
        text_three (str): Provided field
        text_four (str): Remark field

    kwargs:
        col_span (str): number of columns in table that the table data spans
        text_one_css (str): Key pointing to table-data css class
        text_two_css (str): Key pointing to table-data css class
        text_three_css (str): Key pointing to table-data css class
        text_four_css (str): Key pointing to table-data css class

    Returns (str):
        Formatted line of html-code.

    """
    col_span = kwargs.get('col_span', "1")
    t1_css = kwargs.get('text_one_css', "detail1")
    t2_css = kwargs.get('text_two_css', "detail2")
    t3_css = kwargs.get('text_three_css', "detail2")
    t4_css = kwargs.get('text_four_css', "detail1")

    row_string = nl() + t('tr') + nl()

    if col_span == "4":
        row_string = row_string + html_space(4) + t(
            'td colspan=' + col_span + ' class="' + t1_css + '"') + text_one + t('/td') + nl()
    else:
        row_string = row_string + html_space(4) + t('td class="' + t1_css + '"') + text_one + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t2_css + '"') + text_two + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t3_css + '"') + text_three + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t4_css + '"') + text_four + t('/td') + nl()

    row_string = row_string + t('/tr') + nl()

    return row_string
