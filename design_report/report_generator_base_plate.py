"""
Design report generator for the Base Plate Connection Module

@Author:    Danish Ansari - Osdag Team, IIT Bombay

 Module - Base Plate Connection
           - Pinned Base Plate (welded and bolted) [Axial + Shear]
           - Gusseted Base Plate [Moment (major and minor axis) + Axial + Shear]
           - Base Plate for hollow sections [Moment (major and minor axis) + Axial + Shear]


 Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) IS 2062: 2011, Hot rolled medium and high tensile structural steel - specification
               4) IS 5624: 1993, Foundation bolts
               5) IS 456: 2000, Plain and reinforced concrete - code of practice
               6) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               7) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

     other     8)  Column Bases - Omer Blodgett (chapter 3)
  references   9) AISC Design Guide 1 - Base Plate and Anchor Rod Design

  Note: This file refers to the BasePlateConnection class of the base_plate_connection file

"""

# Import modules and classes
from design_type.connection.base_plate_connection import BasePlateConnection
# from design_type.connection.base_plate_connection import *
from Common import *
self = BasePlateConnection

# Start of the design report


# r'/ResourceFiles/images/ColumnsBeams".png'
class SaveDesignBP(BasePlateConnection):

# def save_design(self, popup_summary):
#     """ create design report for the base plate module
#
#     Args:
#         self
#         popup_summary
#
#     Returns:
#
#     """

    self.supported_section = {
        KEY_DISP_SEC_PROFILE: "ISection",
        KEY_DISP_SUPTNGSEC: self.,
        KEY_DISP_MATERIAL: self.material,
        KEY_DISP_FU: self.column_fu,
        KEY_DISP_FY: self.supporting_section.fy,
        'Mass': self.supporting_section.mass,
        'Area(cm2) - A': self.supporting_section.area,
        'D(mm)': self.supporting_section.depth,
        'B(mm)': self.supporting_section.flange_width,
        't(mm)': self.supporting_section.web_thickness,
        'T(mm)': self.supporting_section.flange_thickness,
        'FlangeSlope': self.supporting_section.flange_slope,
        'R1(mm)': self.supporting_section.root_radius,
        'R2(mm)': self.supporting_section.toe_radius,
        'Iz(cm4)': self.supporting_section.mom_inertia_z,
        'Iy(cm4)': self.supporting_section.mom_inertia_y,
        'rz(cm)': self.supporting_section.rad_of_gy_z,
        'ry(cm)': self.supporting_section.rad_of_gy_y,
        'Zz(cm3)': self.supporting_section.elast_sec_mod_z,
        'Zy(cm3)': self.supporting_section.elast_sec_mod_y,
        'Zpz(cm3)': self.supporting_section.plast_sec_mod_z,
        'Zpy(cm3)': self.supporting_section.elast_sec_mod_y
    }

    # bolt_list = str(*self.bolt.bolt_diameter, sep=", ")
    self.report_supporting = {KEY_DISP_SEC_PROFILE:"ISection",
                              KEY_DISP_SUPTNGSEC: self.supporting_section.designation,
                              KEY_DISP_MATERIAL: self.supporting_section.material,
                              KEY_DISP_FU: self.supporting_section.fu,
                              KEY_DISP_FY: self.supporting_section.fy,
                              'Mass': self.supporting_section.mass,
                              'Area(cm2) - A': self.supporting_section.area,
                              'D(mm)': self.supporting_section.depth,
                              'B(mm)': self.supporting_section.flange_width,
                              't(mm)': self.supporting_section.web_thickness,
                              'T(mm)': self.supporting_section.flange_thickness,
                              'FlangeSlope': self.supporting_section.flange_slope,
                              'R1(mm)': self.supporting_section.root_radius,
                              'R2(mm)': self.supporting_section.toe_radius,
                              'Iz(cm4)': self.supporting_section.mom_inertia_z,
                              'Iy(cm4)': self.supporting_section.mom_inertia_y,
                              'rz(cm)': self.supporting_section.rad_of_gy_z,
                              'ry(cm)': self.supporting_section.rad_of_gy_y,
                              'Zz(cm3)': self.supporting_section.elast_sec_mod_z,
                              'Zy(cm3)': self.supporting_section.elast_sec_mod_y,
                              'Zpz(cm3)': self.supporting_section.plast_sec_mod_z,
                              'Zpy(cm3)': self.supporting_section.elast_sec_mod_y}

    self.report_supported = {
        KEY_DISP_SEC_PROFILE:"ISection", #Image shall be save with this name.png in resource files
        KEY_DISP_SUPTDSEC: self.supported_section.designation,
        KEY_DISP_MATERIAL: self.supported_section.material,
        KEY_DISP_FU: self.supported_section.fu,
        KEY_DISP_FY: self.supported_section.fy,
        'Mass': self.supported_section.mass,
        'Area(cm2) - A': round(self.supported_section.area, 2),
        'D(mm)': self.supported_section.depth,
        'B(mm)': self.supported_section.flange_width,
        't(mm)': self.supported_section.web_thickness,
        'T(mm)': self.supported_section.flange_thickness,
        'FlangeSlope': self.supported_section.flange_slope,
        'R1(mm)': self.supported_section.root_radius,
        'R2(mm)': self.supported_section.toe_radius,
        'Iz(cm4)': self.supported_section.mom_inertia_z,
        'Iy(cm4)': self.supported_section.mom_inertia_y,
        'rz(cm)': self.supported_section.rad_of_gy_z,
        'ry(cm)': self.supported_section.rad_of_gy_y,
        'Zz(cm3)': self.supported_section.elast_sec_mod_z,
        'Zy(cm3)': self.supported_section.elast_sec_mod_y,
        'Zpz(cm3)': self.supported_section.plast_sec_mod_z,
        'Zpy(cm3)': self.supported_section.elast_sec_mod_y}

    self.report_input = \
        {KEY_MODULE: self.module,
        KEY_MAIN_MODULE: self.mainmodule,
        KEY_CONN: self.connectivity,
        KEY_DISP_SHEAR: self.load.shear_force,
        "Supporting Section":"TITLE",
        "Supporting Section Details": self.report_supporting,
        "Supported Section":"TITLE",
        "Supported Section Details": self.report_supported,
        "Bolt Details":"TITLE",
        KEY_DISP_D: str(self.bolt.bolt_diameter),
        KEY_DISP_GRD: str(self.bolt.bolt_grade),
        KEY_DISP_TYP: self.bolt.bolt_type,
        KEY_DISP_DP_BOLT_HOLE_TYPE: self.bolt.bolt_hole_type,
        KEY_DISP_DP_BOLT_SLIP_FACTOR: self.bolt.mu_f,
        KEY_DISP_DP_DETAILING_EDGE_TYPE: self.bolt.edge_type,
        KEY_DISP_DP_DETAILING_GAP: self.plate.gap,
        KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES: self.bolt.corrosive_influences,
        "Weld Details":"TITLE",
        KEY_DISP_DP_WELD_TYPE: "Fillet",
        KEY_DISP_DP_WELD_FAB: self.weld.fabrication,
        KEY_DISP_DP_WELD_MATERIAL_G_O: self.weld.fu}

    self.report_check = []
    connecting_plates = [self.plate.thickness_provided,self.supported_section.web_thickness]

    bolt_shear_capacity_kn = round(self.bolt.bolt_capacity/1000,2)
    bolt_bearing_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
    bolt_capacity_kn = round(self.bolt.bolt_capacity / 1000, 2)
    kb_disp= round(self.bolt.kb,2)
    kh_disp = round(self.bolt.kh, 2)
    bolt_force_kn=round(self.plate.bolt_force,2)
    bolt_capacity_red_kn=round(self.plate.bolt_capacity_red,2)

    t1 = ('SubSection', 'Bolt Design Checks','|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
    self.report_check.append(t1)

    if self.bolt.bolt_type == TYP_BEARING:
        t1 = (KEY_OUT_DISP_BOLT_SHEAR, '', bolt_shear_prov(self.bolt.fu,1,self.bolt.bolt_net_area,
                                                           self.bolt.gamma_mb,bolt_shear_capacity_kn), '')
        self.report_check.append(t1)
        t2 = (KEY_OUT_DISP_BOLT_BEARING, '', bolt_bearing_prov(kb_disp,self.bolt.bolt_diameter_provided,
                                                               self.bolt_conn_plates_t_fu_fy,self.bolt.gamma_mb,
                                                               bolt_bearing_capacity_kn), '')
        self.report_check.append(t2)
        t3 = (KEY_OUT_DISP_BOLT_CAPACITY, '',
              bolt_capacity_prov(bolt_shear_capacity_kn,bolt_bearing_capacity_kn,bolt_capacity_kn),
              '')
        self.report_check.append(t3)
    else:

        t4 = (KEY_OUT_DISP_BOLT_SLIP, '',
              HSFG_bolt_capacity_prov(mu_f=self.bolt.mu_f,n_e=1,K_h=kh_disp,fub = self.bolt.fu,
                                      Anb= self.bolt.bolt_net_area,gamma_mf=self.bolt.gamma_mf,
                                      capacity=bolt_capacity_kn),'')
        self.report_check.append(t4)

    t5 = (DISP_NUM_OF_BOLTS, get_trial_bolts(self.load.shear_force,self.load.axial_force,bolt_capacity_kn), self.plate.bolts_required, '')
    self.report_check.append(t5)
    t6 = (DISP_NUM_OF_COLUMNS, '', self.plate.bolt_line, '')
    self.report_check.append(t6)
    t7 = (DISP_NUM_OF_ROWS, '', self.plate.bolts_one_line, '')
    self.report_check.append(t7)
    t1 = (DISP_MIN_PITCH, min_pitch(self.bolt.bolt_diameter_provided),
          self.plate.pitch_provided, get_pass_fail(self.bolt.min_pitch, self.plate.pitch_provided,relation='lesser'))
    self.report_check.append(t1)
    t1 = (DISP_MAX_PITCH, max_pitch(connecting_plates),
          self.plate.pitch_provided, get_pass_fail(self.bolt.max_spacing, self.plate.pitch_provided,relation='greater'))
    self.report_check.append(t1)
    t2 = (DISP_MIN_GAUGE, min_pitch(self.bolt.bolt_diameter_provided),
          self.plate.gauge_provided, get_pass_fail(self.bolt.min_gauge, self.plate.gauge_provided,relation="lesser"))
    self.report_check.append(t2)
    t2 = (DISP_MAX_GAUGE, max_pitch(connecting_plates),
          self.plate.gauge_provided, get_pass_fail(self.bolt.max_spacing, self.plate.gauge_provided,relation="greater"))
    self.report_check.append(t2)
    t3 = (DISP_MIN_END, min_edge_end(self.bolt.d_0, self.bolt.edge_type),
          self.plate.end_dist_provided, get_pass_fail(self.bolt.min_end_dist, self.plate.end_dist_provided,relation='lesser'))
    self.report_check.append(t3)
    t4 = (DISP_MAX_END, max_edge_end(self.plate.fy, self.plate.thickness_provided),
          self.plate.end_dist_provided, get_pass_fail(self.bolt.max_end_dist, self.plate.end_dist_provided,relation='greater'))
    self.report_check.append(t4)
    t3 = (DISP_MIN_EDGE, min_edge_end(self.bolt.d_0, self.bolt.edge_type),
          self.plate.edge_dist_provided, get_pass_fail(self.bolt.min_edge_dist, self.plate.edge_dist_provided,relation='lesser'))
    self.report_check.append(t3)
    t4 = (DISP_MAX_EDGE, max_edge_end(self.plate.fy, self.plate.thickness_provided),
          self.plate.edge_dist_provided, get_pass_fail(self.bolt.max_edge_dist, self.plate.edge_dist_provided,relation="greater"))
    self.report_check.append(t4)
    t5=(KEY_OUT_DISP_BOLT_CAPACITY, bolt_force_kn,bolt_capacity_red_kn,
        get_pass_fail(bolt_force_kn,bolt_capacity_red_kn,relation="lesser"))
    self.report_check.append(t5)

    t1 = ('SubSection','Plate Design Checks','|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
    self.report_check.append(t1)

    t1 = (DISP_MIN_PLATE_HEIGHT, min_plate_ht_req(self.supported_section.depth,self.min_plate_height), self.plate.height,
          get_pass_fail(self.min_plate_height, self.plate.height,relation="lesser"))
    self.report_check.append(t1)
    t1 = (DISP_MAX_PLATE_HEIGHT, max_plate_ht_req(self.connectivity,self.supported_section.depth,
                                                  self.supported_section.flange_thickness,
                                                  self.supported_section.root_radius, self.supported_section.notch_ht,
                                                  self.max_plate_height), self.plate.height,
          get_pass_fail(self.max_plate_height, self.plate.height,relation="greater"))
    self.report_check.append(t1)
    min_plate_length = self.plate.gap +2*self.bolt.min_end_dist+(self.plate.bolt_line-1)*self.bolt.min_pitch
    t1 = (DISP_MIN_PLATE_LENGTH, min_plate_length_req(self.bolt.min_pitch, self.bolt.min_end_dist,
                                                  self.plate.bolt_line,min_plate_length), self.plate.length,
          get_pass_fail(min_plate_length, self.plate.length, relation="lesser"))
    self.report_check.append(t1)
    t1 = (DISP_MIN_PLATE_THICK, min_plate_thk_req(self.supported_section.web_thickness), self.plate.thickness_provided,
          get_pass_fail(self.supported_section.web_thickness, self.plate.thickness_provided, relation="lesser"))
    self.report_check.append(t1)
    ###################
    #Plate Shear Capacities
    ###################
    gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
    A_v = self.plate.height*self.plate.thickness_provided
    t1 = (KEY_DISP_SHEAR_YLD, '', shear_yield_prov(self.plate.height,self.plate.thickness_provided,
                                                       self.plate.fy,gamma_m0,round(self.plate.shear_yielding_capacity/1000,2)),
          '')
    self.report_check.append(t1)

    t1 = (KEY_DISP_SHEAR_RUP, '', shear_rupture_prov(self.plate.height, self.plate.thickness_provided,
                                                                       self.plate.bolts_one_line, self.bolt.dia_hole,
                                                                       self.plate.fu,round(self.plate.shear_rupture_capacity/1000,2)),
          '')
    self.report_check.append(t1)

    t1 = (KEY_DISP_PLATE_BLK_SHEAR_SHEAR, '', round(self.plate.block_shear_capacity/1000,2),'')
    self.report_check.append(t1)

    t1 = (KEY_DISP_SHEAR_CAPACITY, self.load.shear_force, shear_capacity_prov(round(self.plate.shear_yielding_capacity/1000,2),
                                                                             round(self.plate.shear_rupture_capacity/1000,2),
                                                                             round(self.plate.block_shear_capacity/1000,2)),
          get_pass_fail(self.load.shear_force, round(self.plate.shear_capacity / 1000, 2), relation="lesser"))
    self.report_check.append(t1)
    ############
    # Plate Tension Capacities
    ##############
    gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
    A_g = self.plate.length * self.plate.thickness_provided
    t1 = (KEY_DISP_TENSION_YIELDCAPACITY, '', tension_yield_prov(self.plate.length,self.plate.thickness_provided, self.plate.fy, gamma_m0,
                                                         round(self.plate.tension_yielding_capacity / 1000, 2)),'')
    self.report_check.append(t1)

    t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '', tension_rupture_bolted_prov(self.plate.length, self.plate.thickness_provided,
                                                    self.plate.bolts_one_line, self.bolt.dia_hole,
                                                    self.plate.fu,gamma_m1,
                                                    round(self.plate.tension_rupture_capacity / 1000, 2)),'')
    self.report_check.append(t1)

    t1 = (KEY_DISP_PLATE_BLK_SHEAR_TENSION, '', round(self.plate.block_shear_capacity/1000,2),'')
    self.report_check.append(t1)

    t1 = (KEY_DISP_TENSION_CAPACITY, self.load.axial_force, tensile_capacity_prov(round(self.plate.tension_yielding_capacity/1000,2),
                                                                              round(self.plate.tension_rupture_capacity/1000,2),
                                                                              round(self.plate.block_shear_capacity/1000,2)),
    get_pass_fail(self.load.axial_force, round(self.plate.tension_capacity / 1000, 2), relation="lesser"))
    self.report_check.append(t1)

    #############
    #Plate Moment Capacity
    ##############

    t1 = (KEY_OUT_DISP_PLATE_MOM_CAPACITY, round(self.plate.moment_demand/1000000,2),
          round(self.plate.moment_capacity/1000000,2),
          get_pass_fail(self.plate.moment_demand, self.plate.moment_capacity, relation="lesser"))
    self.report_check.append(t1)

    t1 = (KEY_DISP_IR, IR_req(IR = 1),
          mom_axial_IR_prov(round(self.plate.moment_demand/1000000,2),round(self.plate.moment_capacity/1000000,2),
                            self.load.axial_force,round(self.plate.tension_capacity/1000,2),self.plate.IR),
          get_pass_fail(1, self.plate.IR, relation="greater"))
    self.report_check.append(t1)

    ##################
    # Weld Checks
    ##################
    t1 = ('SubSection', 'Weld Checks', '|p{4cm}|p{7.0cm}|p{3.5cm}|p{1.5cm}|')
    self.report_check.append(t1)

    t1 = (DISP_MIN_WELD_SIZE, min_weld_size_req(self.weld_connecting_plates,self.weld_size_min), self.weld.size,
          get_pass_fail(self.weld_size_min, self.weld.size, relation="leq"))
    self.report_check.append(t1)
    t1 = (DISP_MAX_WELD_SIZE, max_weld_size_req(self.weld_connecting_plates, self.weld_size_max), self.weld.size,
          get_pass_fail(self.weld_size_min, self.weld.size, relation="geq"))
    self.report_check.append(t1)
    Ip_weld = round(2 * self.weld.eff_length ** 3 / 12,2)
    weld_conn_plates_fu = [self.supporting_section.fu, self.plate.fu]
    gamma_mw = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.weld.fabrication]
    t1 = (DISP_WELD_STRENGTH, weld_strength_req(V=self.load.shear_force*1000,A=self.load.axial_force*1000,
                                                M=self.plate.moment_demand,Ip_w=Ip_weld,
                                                y_max= self.weld.eff_length/2,x_max=0.0,l_w=2*self.weld.eff_length,
                                                R_w=self.weld.stress),
          weld_strength_prov(weld_conn_plates_fu, gamma_mw, self.weld.throat_tk,self.weld.strength),
          get_pass_fail(self.weld.stress, self.weld.strength, relation="lesser"))
    self.report_check.append(t1)

    Disp_3D_image = "./ResourceFiles/images/3d.png"

    # config = configparser.ConfigParser()
    # config.read_file(open(r'Osdag.config'))
    # desktop_path = config.get("desktop_path", "path1")
    # print("desk:", desktop_path)
    #print(sys.path[0])
    rel_path = str(sys.path[0])
    rel_path = rel_path.replace("\\", "/")

    #file_type = "PDF (*.pdf)"
    #filename = QFileDialog.getSaveFileName(QFileDialog(), "Save File As", os.path.join(str(' '), "untitled.pdf"), file_type)
    # filename = os.path.join(str(folder), "images_html", "TexReport")
    #file_name = str(filename)
    fname_no_ext = popup_summary['filename']

    CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, Disp_3D_image)


# For Command Line


# from ast import literal_eval
#
# path = input("Enter the file location: ")
# with open(path, 'r') as f:
#     data = f.read()
#     d = literal_eval(data)
#     FinPlateConnection.set_input_values(FinPlateConnection(), d, False)
