def tab_girder_sec(self, input_dictionary):
        # if not input_dictionary or input_dictionary[KEY_SECSIZE] == 'Select Section' or \
        #         input_dictionary[KEY_MATERIAL] == 'Select Material':
        # if not input_dictionary or input_dictionary[KEY_MATERIAL] == 'Select Material':
        designation = ''
        material_grade = ''
        source = 'Custom'
        fu = ''
        fy = ''
        depth = ''
        flange_width = ''
        flange_thickness = ''
        web_thickness = ''
        flange_slope = ''
        root_radius = ''
        toe_radius = ''
        m_o_e = "200"
        m_o_r = "76.9"
        p_r = "0.3"
        t_e = "12"
        mass = ''
        area = ''
        mom_inertia_z = ''
        mom_inertia_y = ''
        rad_of_gy_z = ''
        rad_of_gy_y = ''
        elast_sec_mod_z = ''
        elast_sec_mod_y = ''
        plast_sec_mod_z = ''
        plast_sec_mod_y = ''
        torsion_const = ''
        warping_const = ''

        image = ''


        # else:
        #     designation = 'NA'
        #     material_grade = str(input_dictionary[KEY_MATERIAL])
        #     m_o_e = "200"
        #     m_o_r = "76.9"
        #     p_r = "0.3"
        #     t_e = "12"
        #     image = VALUES_IMG_BEAM[0]
        #     I_sec_attributes = ISection(designation)
        #     table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
        #     I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
        #     source = str(I_sec_attributes.source)
        #     fu = str(I_sec_attributes.fu)
        #     fy = str(I_sec_attributes.fy)
        #     depth = str(I_sec_attributes.depth)
        #     flange_width = str(I_sec_attributes.flange_width)
        #     flange_thickness = str(I_sec_attributes.flange_thickness)
        #     web_thickness = str(I_sec_attributes.web_thickness)
        #     flange_slope = float(I_sec_attributes.flange_slope)
        #     root_radius = str(I_sec_attributes.root_radius)
        #     toe_radius = str(I_sec_attributes.toe_radius)
        #     mass = str(I_sec_attributes.mass)
        #     area = str(round((I_sec_attributes.area / 10 ** 2), 2))
        #     mom_inertia_z = str(round((I_sec_attributes.mom_inertia_z / 10 ** 4), 2))
        #     mom_inertia_y = str(round((I_sec_attributes.mom_inertia_y / 10 ** 4), 2))
        #     rad_of_gy_z = str(round((I_sec_attributes.rad_of_gy_z / 10), 2))
        #     rad_of_gy_y = str(round((I_sec_attributes.rad_of_gy_y / 10), 2))
        #     elast_sec_mod_z = str(round((I_sec_attributes.elast_sec_mod_z / 10 ** 3), 2))
        #     elast_sec_mod_y = str(round((I_sec_attributes.elast_sec_mod_y / 10 ** 3), 2))
        #     plast_sec_mod_z = str(round((I_sec_attributes.plast_sec_mod_z / 10 ** 3), 2))
        #     plast_sec_mod_y = str(round((I_sec_attributes.plast_sec_mod_y / 10 ** 3), 2))
        #     torsion_const = str(round((I_sec_attributes.It / 10 ** 4), 2))
        #     warping_const = str(round((I_sec_attributes.Iw / 10 ** 6), 2))
        #     if flange_slope != 90:
        #         image = VALUES_IMG_BEAM[0]
        #     else:
        #         image = VALUES_IMG_BEAM[1]
        
        # if KEY_SEC_MATERIAL in input_dictionary.keys():
        #     material_grade = input_dictionary[KEY_SEC_MATERIAL]
        #     material_attributes = Material(material_grade)
        #     fu = material_attributes.fu
        #     fy = material_attributes.fy
        section = []
        # if input_dictionary:
        #     designation_list = input_dictionary[KEY_SECSIZE]
        # else:
        designation_list = []

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_SEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_SEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_23', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Welded'], 'Welded')
        section.append(t14)

        # t13 = (None, None, TYPE_BREAK, None, None)
        # section.append(t13)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        section.append(t5)
        t6 = ('Label_1', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
        section.append(t6)

        t7 = ('Label_2', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, flange_width)
        section.append(t7)

        t8 = ('Label_3', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, flange_thickness)
        section.append(t8)

        t9 = ('Label_4', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, web_thickness)
        section.append(t9)

        t10 = ('Label_5', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
        section.append(t10)

        t11 = ('Label_6', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        section.append(t11)

        # t12 = ('Label_7', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        # section.append(t12)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t18 = ('Label_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        section.append(t18)

        t19 = ('Label_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        section.append(t19)

        t20 = ('Label_13', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        section.append(t20)

        t21 = ('Label_14', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        section.append(t21)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        section.append(t23)

        t24 = ('Label_17', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        section.append(t24)

        t25 = ('Label_18', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        section.append(t25)

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, image)
        section.append(t33)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        section.append(t26)

        t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        section.append(t27)

        t26 = ('Label_21', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        section.append(t26)

        t27 = ('Label_22', KEY_DISP_Iw, TYPE_TEXTBOX, None, warping_const)
        section.append(t27)
        
        return section