'''
Created on Oct 21, 2016

@author: Jayant Patil
'''
import time
import math
from PyQt4.QtCore import QString
from seat_angle_calc import SeatAngleCalculation


class ReportGenerator(SeatAngleCalculation):
    """Generate Design Report for Seated Angle Connection.

    Attributes (Inherited from SeatAngleCalculation):
        gamma_mb (float): partial safety factor for material - resistance of connection - bolts
        gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling
        gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress
        bolt_hole_type (boolean): bolt hole type - 1 for standard; 0 for oversize
        custom_hole_clearance (float): user defined hole clearance, if any
        beam_col_clear_gap (int): clearance + tolerance
        min_edge_multiplier (float): multipler for min edge distance check - based on edge type
        root_clearance (int): clearance of bolt row from the root of seated angle

        top_angle (string)
        connectivity (string)
        beam_section (string)
        column_section (string)
        beam_fu (float)
        beam_fy (float)
        angle_fy (float)
        angle_fu (float)
        shear_force (float)
        bolt_diameter (int)
        bolt_type (string)
        bolt_grade (float)
        bolt_fu (int)
        bolt_diameter (int)
        bolt_hole_diameter (int)
        angle_sec
        dict_angle_data = model.get_angledata(angle_sec)
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

        safe (Boolean) : status of connection, True if safe
        output_dict (dictionary)

        moment_at_root_angle (float)
        moment_capacity_angle (float): Moment capacity of outstanding lege of the seated angle
        outstanding_leg_shear_capacity (float)
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
        pitch (float)
        gauge (float)
        max_spacing (int)
        max_edge_dist (int)

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
        self.max_spacing = sa_calc_object.max_spacing
        self.gamma_mb = sa_calc_object.gamma_mb
        self.gamma_m0 = sa_calc_object.gamma_m0
        self.gamma_m1 = sa_calc_object.gamma_m1
        self.bolt_hole_type = sa_calc_object.bolt_hole_type
        self.custom_hole_clearance = sa_calc_object.custom_hole_clearance
        self.beam_col_clear_gap = sa_calc_object.beam_col_clear_gap
        self.min_edge_multiplier = sa_calc_object.min_edge_multiplier
        self.root_clearance = sa_calc_object.root_clearance
        self.top_angle = sa_calc_object.top_angle
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
        self.bolt_diameter = sa_calc_object.bolt_diameter
        self.bolt_hole_diameter = sa_calc_object.bolt_hole_diameter
        self.angle_sec = sa_calc_object.angle_sec
        self.dict_angle_data = sa_calc_object.dict_angle_data
        self.beam_w_t = sa_calc_object.beam_w_t
        self.beam_f_t = sa_calc_object.beam_f_t
        self.beam_d = sa_calc_object.beam_d
        self.beam_w_f = sa_calc_object.beam_w_f
        self.beam_R1 = sa_calc_object.beam_R1
        self.column_f_t = sa_calc_object.column_f_t
        self.column_d = sa_calc_object.column_d
        self.column_w_f = sa_calc_object.column_w_f
        self.column_R1 = sa_calc_object.column_R1
        self.angle_t = sa_calc_object.angle_t
        self.angle_A = sa_calc_object.angle_A
        self.angle_B = sa_calc_object.angle_B
        self.angle_R1 = sa_calc_object.angle_R1
        self.angle_l = sa_calc_object.angle_l

        self.safe = sa_calc_object.safe
        self.output_dict = sa_calc_object.output_dict

        self.moment_at_root_angle = sa_calc_object.moment_at_root_angle
        self.moment_capacity_angle = sa_calc_object.moment_capacity_angle
        self.outstanding_leg_shear_capacity = sa_calc_object.outstanding_leg_shear_capacity
        self.beam_shear_strength = sa_calc_object.beam_shear_strength
        self.bolt_shear_capacity = sa_calc_object.bolt_shear_capacity
        if sa_calc_object.bolt_hole_type == 1:
            self.bolt_hole_type = "STD"
        elif sa_calc_object.bolt_hole_type == 0:
            self.bolt_hole_type = "OVS"
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
        self.pitch = sa_calc_object.pitch
        self.gauge = sa_calc_object.gauge
        self.max_spacing = sa_calc_object.max_spacing
        self.max_edge_dist = sa_calc_object.max_edge_dist

        self.company_name = ""
        self.company_logo = ""

        self.group_team_name = ""
        self.designer = ""
        self.project_title = ""
        self.sub_title = ""
        self.job_number = ""
        self.method = ""

    def save_html(self, output_object, input_object, report_summary, file_name, folder, base,
                  base_front, base_top, base_side):
        """Create and save html report for Seated angle connection.

        Args:
            output_object (dict): Calculated output parameters of connection
            input_object (dict): User input parameters of connection
            report_summary (dict): Structural Engineer details design report
            file_name (string): Name of design report file
            folder (path): Location of folder to save design report
            base (path): Location of folder to save design report dependencies
            base_front (string): Location to save design report dependency (front view image)
            base_top  (string): Location to save design report dependency (top view image)
            base_side (string): Location to save design report dependency (side view image)

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
        self.method = str(report_summary['Method'])
        additional_comments = str(report_summary['AdditionalComments'])

        # Seated angle design parameters
        connectivity = str(self.connectivity)
        shear_force = str(self.shear_force)
        column_sec = str(self.column_section)
        column_fu = str(self.column_fu)
        beam_sec = str(self.beam_section)
        beam_col_clear_gap = str(self.beam_col_clear_gap)

        boltGrade = str(self.bolt_grade)
        bolt_diameter = str(self.bolt_diameter)
        bolt_hole_type = str(self.bolt_hole_type)

        beam_depth = str(self.beam_d)
        beam_flange_thickness = str(self.beam_f_t)
        beam_root_radius = str(self.beam_R1)
        col_flange_thickness = str(self.column_f_t)
        col_root_radius = str(self.column_R1)

        seated_angle_section = str(self.angle_sec)
        top_angle_section = str(self.top_angle)
        angle_fu = str(self.angle_fu)
        angle_fy = str(self.angle_fy)

        bolts_provided = str(self.bolts_provided)
        bolts_required = str(self.bolts_required)

        number_of_rows = str(self.num_rows)
        number_of_cols = str(self.num_cols)
        edge = str(self.edge_dist)
        gauge = str(self.gauge)
        pitch = str(self.pitch)
        end = str(self.end_dist)
        moment_demand = str(self.moment_at_root_angle)
        gap = '20'
        # TODO replace hardcoded gap value

        bolt_fu = str(self.bolt_fu)
        bolt_type = str(self.bolt_type)
        bolt_dia = str(self.bolt_diameter)
        kb = str(self.k_b)
        beam_w_t = str(self.beam_w_t)
        beam_fu = str(self.beam_fu)
        dia_hole = str(self.bolt_hole_diameter)
        shear_capacity = str(self.bolt_shear_capacity)
        bearing_capacity = str(self.bolt_bearing_capacity)
        if self.safe == True:
            design_conclusion = "Pass"
        elif self.safe == False:
            design_conclusion = "Fail"

        # -----------------------------------------------------------------------------------
        rstr = self.design_report_header()
        # -----------------------------------------------------------------------------------

        # Design conclusion
        rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ') + nl()

        rstr += design_summary_row(0, "Design Conclusion", "header0", col_span="2")

        row = [1, "Seated Angle", "<p align=left style=color:green><b>" + design_conclusion + "</b></p>"]
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
        rstr += design_summary_row(2, "Grade", "detail2", text_two=boltGrade)
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
        # DESIGN CHECK
        # TODO IMPORTANT Remove calculations from below lines of code

        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
        rstr += design_check_row("Design Check", "", "", "", col_span="4", text_one_css="detail")

        rstr += design_check_row("Check", "Required", "Provided", "Remark", text_one_css="header1",
                                 text_two_css="header1", text_three_css="header1", text_four_css="header1")

        check_pass = "<p align=left style=color:green><b>Pass</b></p>"

        # Bolt
        rstr += design_check_row("Bolt", "","","",col_span="4",text_one_css="detail1")

        # Bolt shear capacity (kN)
        const = str(round(math.pi / 4 * 0.78, 4))
        req_field = " "
        prov_field = "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + const + "*" + bolt_dia + "*" \
                     + bolt_dia + ")/ <br>(&#8730;3*1.25*1000) = " + shear_capacity + "<br> [cl. 10.3.3]"
        rstr += design_check_row("Bolt shear capacity (kN)", req_field, prov_field, " ")

        # Bolt bearing capacity (kN)
        req_field = "<i>V<sub>dpb</sub></i> = 2.5 * k<sub>b</sub> * bolt_diameter * critical_thickness * <br>"\
                    +space(3)+" <i>f</i><sub>u</sub>/<i>gamma<sub>mb</sub></i> <br> "\
                    +"[Cl. 10.3.4]"
        prov_field = "<i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_dia + "*" + beam_w_t + "*" \
                     + beam_fu + ")/(1.25*1000)  <br>"+space(2) +" ="+ bearing_capacity + " kN"
        # TODO incorrect value of bolt_bearing capacity
        rstr += design_check_row("Bolt bearing capacity (kN)", req_field, prov_field, "")

        # Bolt capacity (kN)
        prov_field = "Min (" + str(self.bolt_shear_capacity) + ", " + str(self.bolt_bearing_capacity) + ") = " \
                     + str(self.bolt_value)
        rstr += design_check_row("Bolt capacity (kN)", " ", prov_field, "")

        # No. of bolts
        bolts = str(round(float(shear_force) / float(str(self.bolt_value)), 1))
        req_field = shear_force + "/" + str(self.bolt_value) + " = " + bolts
        rstr += design_check_row("No. of bolts", req_field, bolts_provided, check_pass)

        rstr += design_check_row("No. of columns", " ", number_of_cols, check_pass)
        rstr += design_check_row("No. of row(s)", " &#8804; 2", number_of_rows, check_pass)

        # Bolt pitch (mm)
        minPitch = str(int(2.5 * float(bolt_dia)))
        maxPitch = str(300) if 32 * float(beam_w_t) > 300 else str(int(math.ceil(32 * float(beam_w_t))))
        req_field = " &#8805; 2.5* " + bolt_dia + " = " + minPitch + ",  &#8804; Min(32*" + beam_w_t + \
                    ", 300) = " + maxPitch + "<br> [cl. 10.2.2]"
        rstr += design_check_row("Bolt pitch (mm)", req_field, pitch, check_pass)

        # Bolt gauge (mm)
        minGauge = str(int(2.5 * float(bolt_dia)))
        maxGauge = str(300) if 32 * float(beam_w_t) > 300 else str(int(math.ceil(32 * float(beam_w_t))))
        req_field = " &#8805; 2.5*" + bolt_dia + " = " + minGauge + ", &#8804; Min(32*" + beam_w_t + ", 300) = " + maxGauge + " <br> [cl. 10.2.2]"
        rstr += design_check_row("Bolt gauge (mm)", req_field, gauge, check_pass)

        # End distance (mm)
        minEnd = str(1.7 * float(dia_hole))
        maxEnd = str(12 * float(beam_w_t))
        req_field = " &#8805; 1.7*" + dia_hole + " = " + minEnd + ", &#8804; 12*" + beam_w_t + " = " + maxEnd + " <br> [cl. 10.2.4]"
        rstr += design_check_row("End distance (mm)", req_field, end, check_pass)

        # Edge distance (mm)
        minEdge = str(1.7 * float(dia_hole))
        maxEdge = str(12 * float(beam_w_t))
        req_field = " &#8805; 1.7*" + dia_hole + " = " + minEdge + ", &#8804; 12*" + beam_w_t + " = " + maxEdge + "<br> [cl. 10.2.4]"
        rstr += design_check_row("Edge distance (mm)", req_field, edge, check_pass)

        # Seated angle
        rstr += design_check_row("Seated Angle", "","","",col_span="4",text_one_css="detail1")

        # Seated angle length
        if connectivity ==  "Column flange-Beam web":
            req_field = "= min(supported_beam_width, supporting_column_width) <br> = min(" + str(self.beam_w_f) + ", " + str(self.column_w_f)+")"
            prov_field = str(self.angle_l)
        elif connectivity == "Column web-Beam web":
            req_field = "=width of supported beam <br> ="+str(self.beam_w_f)
            prov_field = str(self.angle_l)
        rstr += design_check_row("length", req_field, prov_field, check_pass)

        # Length of oustanding leg
        req_field = "b = R/"+sub("t", "w")+"("+sub("f","yw")+"/"+sub("&gamma","m0")+")"
        # TODO Add other checks to the list

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')
        rstr += t('/h1')

        # TODO IMPORTANT Remove calculations from above lines of code
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

        png = folder + "/css/" + base
        datapng = '<object type="image/PNG" data= %s width ="450"></object">' % png

        side = folder + "/css/" + base_side
        dataside = '<object type="image/svg+xml" data= %s width ="400"></object>' % side

        top = folder + "/css/" + base_top
        datatop = '<object type="image/svg+xml" data= %s width ="400"></object>' % top

        front = folder + "/css/" + base_front
        datafront = '<object type="image/svg+xml" data= %s width ="450"></object>' % front

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
            None

        Returns:
            rstr (str): string containing html code to table (used as Report Header)
        """
        rstr = nl() + " " + nl() + t('table border-collapse= "collapse" border="1px solid black" width=100%') + nl()
        rstr += t('tr') + nl()
        row = [0, '<object type= "image/PNG" data= "css/cmpylogoSeatAngle.png" height=60 ></object>',
               '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>'' &nbsp'
               '<object type= "image/PNG" data= "css/Osdag_header.png" height=60 ''&nbsp></object>']
        rstr += html_space(1) + t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(1) + t('td colspan="2" align= "right"') + row[2] + t('/td') + nl()
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
        rstr += design_summary_row(0, "Method", "detail", text_two=self.method, is_row=False)
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


def w(param):
    """Enclose argument in curly brace parenthesis.

    Args:
        param (str): parameter to be enclosed in curly brace parenthesis.

    Returns:
        rstr (str): given param enclosed in curly brace parenthesis.
    """
    return '{' + n + '}'


def quote(m):
    """Enclose argument in double quotes.

    Args:
        param (str): parameter to be enclosed in double quotes

    Returns:
        rstr (str): given param enclosed in double quotes
    """
    return '"' + m + '"'


def nl():
    """Create new line.

    Args:
        None

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
        subscript (str): string to be subscripted.

    Returns:
        (str): html code with concatenated string and subscript
    """
    return string+"<sub>"+subscript+"</sub>"


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

    if is_row == True:
        row_string = t('tr') + nl()
    elif is_row == False:
        row_string = ""

    if col_span != "1":
        row_string = row_string + html_space(4) + t('td colspan=' + col_span + ' class="' + text_one_css + '"') + space(
            tab_spaces) + text_one + t('/td') + nl()
    else:
        row_string = row_string + html_space(4) + t('td class="' + text_one_css + '"') + space(tab_spaces) + text_one \
                     + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + text_two_css + '"') + text_two + t('/td') + nl()

    if is_row is True:
        row_string = row_string + t('/tr') + nl()
    elif is_row is False:
        pass

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
        row_string = row_string + html_space(4) + t('td class="' + t1_css + '"') + space(1)+text_one + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t2_css + '"') + text_two + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t3_css + '"') + text_three + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t4_css + '"') + text_four + t('/td') + nl()

    row_string = row_string + t('/tr') + nl()

    return row_string
