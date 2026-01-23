"""
Module: latex_report.py
Description: DDCL-COMPLIANT Design Report Generator for Plate Girder (Updated)
Author: Roushan Raj
Date: 2026-01-16
"""

import logging
from pylatex import Math
from pylatex.utils import NoEscape
from ....design_report.reportGenerator_latex import CreateLatex
from ....Common import KEY_DISP_SEC_PROFILE
from ....utils.common.Unsymmetrical_Section_Properties import Unsymmetrical_I_Section_Properties
import os
import math
from ..checks.shear import tension_field_unequal_I_corrected, calc_K_v
from ....utils.common.is800_2007 import IS800_2007

def save_design(popup_summary):
    """Generate LaTeX design report for Plate Girder module"""
    unique_logger_name = 'Osdag_plate_girder_flexure'
    logger = logging.getLogger(unique_logger_name)
    logger.info(" :=========Start of design report generation===========")

    try:
        pg_obj = popup_summary.get('plate_girder_object')
        if pg_obj is None:
            logger.error("Plate Girder Object is None")
            return False
            
        if not pg_obj.design_status:
            logger.warning("Design is not complete/failed checks. Generating report with failures.")

        report_input = prepare_report_input(pg_obj, logger)
        report_check = prepare_design_checks(pg_obj, logger)

        # Prepare report summary
        report_summary = popup_summary.copy()
        if 'ProfileSummary' not in report_summary:
            report_summary['ProfileSummary'] = {
                'CompanyName': report_summary.get('CompanyName', ''),
                'CompanyLogo': report_summary.get('CompanyLogo', ''),
                'Group/TeamName': report_summary.get('Group/TeamName', ''),
                'Designer': report_summary.get('Designer', '')
            }
        
        report_summary.setdefault('ProjectTitle', 'Plate Girder Design')
        report_summary.setdefault('Subtitle', 'Welded Plate Girder')
        report_summary.setdefault('JobNumber', '')
        report_summary.setdefault('Client', '')
        report_summary['does_design_exist'] = pg_obj.design_status
        report_summary.setdefault('logger_messages', '')
        
        # Image paths
        Disp_2d_image = []
        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = os.path.abspath(".").replace("\\", "/")
        fname_no_ext = popup_summary.get("filename", "ButtJointWeldedReport")
        folder = popup_summary.get('folder', './reports')
        os.makedirs(folder, exist_ok=True)
                
        CreateLatex.save_latex(
            CreateLatex(), report_input, report_check,
            popup_summary, fname_no_ext, rel_path, Disp_2d_image, Disp_3D_image,
            module="Plate Girder"
        )
        logger.info(f"Report generated successfully: {fname_no_ext}.pdf")
                
        pdf_file_path = os.path.join(folder, f"{fname_no_ext}.pdf")
        if os.path.exists(pdf_file_path):
            file_size = os.path.getsize(pdf_file_path)
            print(f"SUCCESS: Report generated: {pdf_file_path} ({file_size} bytes)")
            return True
        else:
            print("ERROR: PDF not found")
            return False

    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        return False


def prepare_report_input(pg_obj, logger):
    """
    Prepare input section - ONLY user inputs, NO calculations
    """
    report_input = {}

    try:
        report_input['Module'] = 'PLATE GIRDER'
        report_input['Main Module'] = 'Flexural Member'
        # ==================== 1. General Inputs ====================
        report_input['General Inputs'] = 'TITLE'
        
        # Material
        material = getattr(pg_obj, 'material', None)
        report_input['Material Grade'] = getattr(material, 'designation', 'E 250') if material else 'E 250'
        
        # Structure Type
        # Try to get from attributes, fallback to reasonable default if missing
        report_input['Type of Structure'] = getattr(pg_obj, 'structure_type', 'Industrial Structure')
        
        # Torsional Restraint
        report_input['Torsional Restraint'] = getattr(pg_obj, 'torsional_restraint', 'Fully Restrained')
        
        # Warping Restraint
        report_input['Warping Restraint'] = getattr(pg_obj, 'warping_restraint', 'No Restraint')
        
        # Span
        report_input['Span (mm)'] = round(getattr(pg_obj, 'length', 0), 1)
        
        if hasattr(pg_obj, 'max_deflection'):
             report_input['Maximum deflection observed (mm)'] = getattr(pg_obj, 'max_deflection', '-')

        # ==================== Girder Properties ====================
        girder_props = {}
        girder_props[KEY_DISP_SEC_PROFILE] = 'ISection'

        # Material Properties
        if material:
            girder_props['Material'] = getattr(material, 'designation', 'E 250')
            girder_props['Ultimate Strength (MPa)'] = getattr(material, 'fu', 410)
            girder_props['Yield Strength (MPa)'] = getattr(material, 'fy', 250)
            E = getattr(material, 'modulus_of_elasticity', 200000)
            girder_props['Modulus of Elasticity (MPa)'] = E
            mu = getattr(material, 'poisson_ratio', 0.3)
            girder_props["Poisson's Ratio"] = mu
            # Calculate G if not present
            if hasattr(material, 'shear_modulus'):
                 girder_props['Modulus of Rigidity (MPa)'] = getattr(material, 'shear_modulus')
            else:
                 girder_props['Modulus of Rigidity (MPa)'] = round(E / (2 * (1 + mu)), 2)
            
            girder_props['Thermal Expansion'] = getattr(material, 'coeff_thermal_expansion', 12e-6)

        girder_props['Type'] = 'Welded'

        # Geometry for Calculation
        D = getattr(pg_obj, 'total_depth', 0)
        bf_top = getattr(pg_obj, 'top_flange_width', 0)
        bf_bot = getattr(pg_obj, 'bottom_flange_width', 0)
        tw = getattr(pg_obj, 'web_thickness', 0)
        tf_top = getattr(pg_obj, 'top_flange_thickness', 0)
        tf_bot = getattr(pg_obj, 'bottom_flange_thickness', 0)

        # Section Properties Calculations
        girder_props['Mass (kg/m)'] = Unsymmetrical_I_Section_Properties.calc_mass(D, bf_top, bf_bot, tw, tf_top, tf_bot)
        girder_props['Area (cm$^2$)' ] = round(Unsymmetrical_I_Section_Properties.calc_area(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 100, 2)
        
        girder_props['Moment of Area, $I_z$ (cm$^4$)' ] = round(Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 10000, 2)
        girder_props['Moment of Area, $I_y$ (cm$^4$)' ] = round(Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 10000, 2)
        
        girder_props['Radius of Gyration, $r_z$ (cm)'] = round(Unsymmetrical_I_Section_Properties.calc_RadiusOfGyrationZ(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 10, 2)
        girder_props['Radius of Gyration, $r_y$ (cm)'] = round(Unsymmetrical_I_Section_Properties.calc_RadiusOfGyrationY(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 10, 2)
        
        girder_props['Elastic Modulus, $Z_{ez}$ (cm$^3$)' ] = round(Unsymmetrical_I_Section_Properties.calc_ElasticModulusZz(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 1000, 2)
        girder_props['Elastic Modulus, $Z_{ey}$ (cm$^3$)' ] = round(Unsymmetrical_I_Section_Properties.calc_ElasticModulusZy(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 1000, 2)
        
        girder_props['Plastic Modulus, $Z_{pz}$ (cm$^3$)' ] = round(Unsymmetrical_I_Section_Properties.calc_PlasticModulusZ(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 1000, 2)
        girder_props['Plastic Modulus, $Z_{py}$ (cm$^3$)' ] = round(Unsymmetrical_I_Section_Properties.calc_PlasticModulusY(D, bf_top, bf_bot, tw, tf_top, tf_bot) / 1000, 2)

        report_input['Girder Properties'] = girder_props
        
        # ==================== 2. Dimensions Inputs ====================
        report_input['Dimensions Inputs'] = 'TITLE'
        
        report_input['Top Flange Width (mm)'] = round(getattr(pg_obj, 'top_flange_width', 0), 1)
        report_input['Top Flange Thickness (mm)'] = round(getattr(pg_obj, 'top_flange_thickness', 0), 1)
        report_input['Bottom Flange Width (mm)'] = round(getattr(pg_obj, 'bottom_flange_width', 0), 1)
        report_input['Bottom Flange Thickness (mm)'] = round(getattr(pg_obj, 'bottom_flange_thickness', 0), 1)
        report_input['Depth of Section (mm)'] = round(getattr(pg_obj, 'total_depth', 0), 1)
        report_input['Web Thickness (mm)'] = round(getattr(pg_obj, 'web_thickness', 0), 1)

        # ==================== 3. Load Inputs ====================
        report_input['Load Inputs'] = 'TITLE'
        
        load = getattr(pg_obj, 'load', None)
        if load:
            report_input['Maximum Bending Moment (kNm)'] = round(getattr(load, 'moment', 0) * 1e-6, 2)
            report_input['Maximum Shear Force (kN)'] = round(getattr(load, 'shear_force', 0) * 1e-3, 2)
        else:
            report_input['Maximum Bending Moment (kNm)'] = 0
            report_input['Maximum Shear Force (kN)'] = 0
            
        report_input['Bending moment diagram shape'] = getattr(pg_obj, 'moment_diagram_type', 'Uniform Loading')

        # ==================== 4. Support Condition Inputs ====================
        report_input['Support Condition Inputs'] = 'TITLE'
        
        report_input['Support Condition'] = getattr(pg_obj, 'support_type', 'Major Laterally Supported')

        # ==================== 5. Web Philosophy Inputs ====================
        report_input['Web Philosophy Inputs'] = 'TITLE'
        
        report_input['Web Type'] = getattr(pg_obj, 'web_philosophy', 'Thick Web without ITS')

        # Additional Material Details (Standard)
        if material:
            report_input['Yield Strength, $f_y$ (MPa)'] = round(getattr(material, 'fy', 0), 1)
            report_input['Ultimate Strength, $f_u$ (MPa)'] = round(getattr(material, 'fu', 0), 1)

    except Exception as e:
        logger.error(f"Error preparing report input: {str(e)}")

    return report_input

def prepare_design_checks(pg_obj, logger):
    """
    Prepare design checks - DDCL compliant with multi-line equations
    All equations formatted per lap_joint_bolted.py pattern
    """
    report_check = []
    table_format = '|p{4cm}|p{4.5cm}|p{6cm}|p{1.5cm}|'

    try:
        # ==================== GET VALUES FROM PG_OBJ ====================
        # Material
        material = getattr(pg_obj, 'material', None)
        fy = round(material.fy, 1) if material else 250
        fu = round(material.fu, 1) if material else 410
        E = getattr(material, 'modulus_of_elasticity', 200000) if material else 200000

        # Loads
        load = getattr(pg_obj, 'load', None)
        M_applied = round(getattr(load, 'moment', 0) * 1e-6, 2) if load else 0
        V_applied = round(getattr(load, 'shear_force', 0) * 1e-3, 2) if load else 0

        # Dimensions
        D = getattr(pg_obj, 'total_depth', 0)
        d = getattr(pg_obj, 'eff_depth', 0)
        tw = getattr(pg_obj, 'web_thickness', 0)
        tf_top = getattr(pg_obj, 'top_flange_thickness', 0)
        tf_bot = getattr(pg_obj, 'bottom_flange_thickness', 0)
        bf_top = getattr(pg_obj, 'top_flange_width', 0)
        bf_bot = getattr(pg_obj, 'bottom_flange_width', 0)
        L = getattr(pg_obj, 'length', 0)

        # Design parameters
        gamma_m0 = getattr(pg_obj, 'gamma_m0', 1.1)
        epsilon = getattr(pg_obj, 'epsilon', 1.0)

        # Design decisions from pg_obj
        section_class = getattr(pg_obj, 'section_class', None)
        if section_class is None:
            section_class = getattr(pg_obj, 'section_classification_val', 'NA')

        design_status = getattr(pg_obj, 'design_status', False)
        shear_flag1 = getattr(pg_obj, 'shearflag1', False)
        shear_flag2 = getattr(pg_obj, 'shearflag2', False)
        shear_flag3 = getattr(pg_obj, 'shearflag3', False)
        moment_checks = getattr(pg_obj, 'momentchecks', False)
        defl_check = getattr(pg_obj, 'defl_check', False)
        web_philosophy = getattr(pg_obj, 'web_philosophy', '')

        # ==================== SECTION CLASSIFICATION ====================
        report_check.append(['SubSection', 'Section Classification', table_format])

        # Top flange slenderness
        if bf_top > 0 and tf_top > 0:
            btf_top = round((bf_top - tw) / (2 * tf_top), 2)

            btf_eq = Math(inline=True)
            btf_eq.append(NoEscape(r'\begin{aligned}\\'))
            btf_eq.append(NoEscape(rf'\dfrac{{b_f - t_w}}{{2 t_f}} &= \dfrac{{{bf_top:.1f} - {tw:.1f}}}{{2 \times {tf_top:.1f}}}\\'))
            btf_eq.append(NoEscape(rf'&= {btf_top:.2f}\\'))
            btf_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 2]}\\'))
            btf_eq.append(NoEscape(r'\end{aligned}'))

            # Determine Class
            outstand_top = (bf_top - tw) / 2
            class_top = IS800_2007.Table2_i(outstand_top, tf_top, fy, 'Welded')[0]

            report_check.append([
                'Top Flange Slenderness Ratio',
                '',
                btf_eq,
                class_top
            ])

        # Bottom flange slenderness
        if bf_bot > 0 and tf_bot > 0:
            btf_bot = round((bf_bot - tw) / (2 * tf_bot), 2)

            btf_bot_eq = Math(inline=True)
            btf_bot_eq.append(NoEscape(r'\begin{aligned}\\'))
            btf_bot_eq.append(NoEscape(rf'\dfrac{{b_f - t_w}}{{2 t_f}} &= \dfrac{{{bf_bot:.1f} - {tw:.1f}}}{{2 \times {tf_bot:.1f}}}\\'))
            btf_bot_eq.append(NoEscape(rf'&= {btf_bot:.2f}\\'))
            btf_bot_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 2]}\\'))
            btf_bot_eq.append(NoEscape(r'\end{aligned}'))

            # Determine Class
            outstand_bot = (bf_bot - tw) / 2
            class_bot = IS800_2007.Table2_i(outstand_bot, tf_bot, fy, 'Welded')[0]

            report_check.append([
                'Bottom Flange Slenderness Ratio',
                '',
                btf_bot_eq,
                class_bot
            ])

        # Web slenderness
        d_tw_ratio = round(d / tw, 2) if tw > 0 else 0

        dtw_eq = Math(inline=True)
        dtw_eq.append(NoEscape(r'\begin{aligned}\\'))
        dtw_eq.append(NoEscape(rf'\dfrac{{d}}{{t_w}} &= \dfrac{{{d:.1f}}}{{{tw:.1f}}}\\'))
        dtw_eq.append(NoEscape(rf'&= {d_tw_ratio:.2f}\\'))
        dtw_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 2]}\\'))
        dtw_eq.append(NoEscape(r'\end{aligned}'))

        web_depth = d
        class_web = IS800_2007.Table2_iii(web_depth, tw, fy)

        report_check.append([
            'Web Slenderness Ratio',
            '',
            dtw_eq,
            class_web
        ])

        # Overall section classification
        overall_eq = Math(inline=True)
        overall_eq.append(NoEscape(r'\begin{aligned}\\'))
        overall_eq.append(NoEscape(r'&\text{Governing classification based on}\\'))
        overall_eq.append(NoEscape(r'&\text{most critical element}\\'))
        overall_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 2]}\\'))
        overall_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Overall Section Classification',
            overall_eq,
            str(section_class), 
            ''
        ])

        # ==================== SHEAR CAPACITY CHECK ====================
        report_check.append(['SubSection', 'Shear Capacity Check', table_format])

        V_d_N = getattr(pg_obj, 'V_d', 0)
        V_d = round(V_d_N / 1000, 2) if V_d_N else 0

        # Shear area
        Avw = round(d * tw, 2)

        avw_eq = Math(inline=True)
        avw_eq.append(NoEscape(r'\begin{aligned}\\'))
        avw_eq.append(NoEscape(rf'A_{{vw}} &= d \times t_w\\'))
        avw_eq.append(NoEscape(rf'&= {d:.1f} \times {tw:.1f}\\'))
        avw_eq.append(NoEscape(rf'&= {Avw:.2f} \text{{ mm}}^2\\'))
        avw_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4]}\\'))
        avw_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            NoEscape(r'Shear Area'),
            '',
            avw_eq,
            ''
        ])

        # Design shear strength
        if web_philosophy == 'Thick Web without ITS':
            vd_eq = Math(inline=True)
            vd_eq.append(NoEscape(r'\begin{aligned}\\'))
            vd_eq.append(NoEscape(r'V_d &= \dfrac{A_{vw} f_y}{\sqrt{3} \gamma_{m0} \times 10^3}\\'))
            vd_eq.append(NoEscape(rf'&= \dfrac{{{Avw:.2f} \times {fy:.1f}}}{{\sqrt{{3}} \times {gamma_m0} \times 1000}}\\'))
            vd_eq.append(NoEscape(rf'&= {V_d:.2f} \text{{ kN}}\\'))
            vd_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.1]}\\'))
            vd_eq.append(NoEscape(r'\end{aligned}'))

            shear_status = 'Pass' if shear_flag1 else 'Fail'

            report_check.append([
                NoEscape(r'Design Shear Strength'),
                f'{V_applied:.2f}',
                vd_eq, 
                shear_status
            ])

            # Shear Buckling Resistance (same as Shear Capacity for thick web)
            vcr_thk_eq = Math(inline=True)
            vcr_thk_eq.append(NoEscape(r'\begin{aligned}\\'))
            vcr_thk_eq.append(NoEscape(r'V_{cr} &= V_d \text{ (Yielding governs)}\\\\'))
            vcr_thk_eq.append(NoEscape(rf'&= {V_d:.2f} \text{{ kN}}\\'))
            vcr_thk_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.1]}\\'))
            vcr_thk_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                'Shear Buckling Resistance',
                '',
                vcr_thk_eq,
                ''
            ])
        else:
            # Thin web - Check if Tension Field or Simple Post Critical
            shear_method = getattr(pg_obj, 'x', 'Simple Post Critical')
            
            # Common parameters for both methods
            d_eff = getattr(pg_obj, 'eff_depth', 0)
            c_val = getattr(pg_obj, 'c', 0)
            if c_val == 'NA': c_val = 0 
            
            kv = calc_K_v(c_val, d_eff, web_philosophy)
            
            kv_nm = 5.35
            kv_m = 4.0
            a_ratio = c_val / d_eff if d_eff != 0 else 0
            
            kv_calc_eq = Math(inline=True)
            kv_calc_eq.append(NoEscape(r'\begin{aligned}\\'))
            kv_calc_eq.append(NoEscape(rf'\dfrac{{c}}{{d}} &= \dfrac{{{c_val:.1f}}}{{{d_eff:.1f}}} = {a_ratio:.2f}\\\\'))
            
            if a_ratio < 1.0:
                 kv_calc_eq.append(NoEscape(r'k_v &= 4.0 + \dfrac{5.35}{(c/d)^2}\\\\'))
                 kv_calc_eq.append(NoEscape(rf'&= 4.0 + \dfrac{{5.35}}{{({a_ratio:.2f})^2}} = {kv:.3f}\\'))
            else:
                 kv_calc_eq.append(NoEscape(r'k_v &= 5.35 + \dfrac{4.0}{(c/d)^2}\\\\'))
                 kv_calc_eq.append(NoEscape(rf'&= 5.35 + \dfrac{{4.0}}{{({a_ratio:.2f})^2}} = {kv:.3f}\\'))
            
            kv_calc_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2]}\\'))
            kv_calc_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                NoEscape(r'Buckling Coefficient'),
                '',
                kv_calc_eq,
                ''
            ])
            
            # Calculate Tau_crc, Lambda_w, Tau_b generically first using IS800 module logic 
            # (replicating shear.py logic for consistency)
            mu = 0.3
            tau_crc = IS800_2007.cl_8_4_2_2_tau_crc_Simple_postcritical(kv, E, mu, d_eff, tw)
            lambda_w = IS800_2007.cl_8_4_2_2_lambda_w_Simple_postcritical(fy, tau_crc)
            tau_b = IS800_2007.cl_8_4_2_2_tau_b_Simple_postcritical(lambda_w, fy)
            
            # Display Lambda_w
            lambda_eq = Math(inline=True)
            lambda_eq.append(NoEscape(r'\begin{aligned}\\'))
            lambda_eq.append(NoEscape(r'\lambda_w &= \sqrt{\dfrac{f_{yw}}{\sqrt{3} \tau_{cr,e}}}\\\\'))
            lambda_eq.append(NoEscape(rf'&= \sqrt{{\dfrac{{{fy:.2f}}}{{\sqrt{{3}} \times {tau_crc:.2f}}}}}\\\\'))
            lambda_eq.append(NoEscape(rf'&= {lambda_w:.3f}\\'))
            lambda_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2]}\\'))
            lambda_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                NoEscape(r'Web Slenderness'),
                '',
                lambda_eq,
                ''
            ])
            
            if lambda_w <= 0.8:
                tau_b = round(fy / (3**0.5), 2)
                tau_b_eq = Math(inline=True)
                tau_b_eq.append(NoEscape(r'\begin{aligned}\\'))
                tau_b_eq.append(NoEscape(rf'\lambda_w \leq 0.8: \quad \tau_b &= \dfrac{{f_{{yw}}}}{{\sqrt{{3}}}}\\\\'))
                tau_b_eq.append(NoEscape(rf'&= \dfrac{{{fy:.1f}}}{{\sqrt{{3}}}}\\\\'))
                tau_b_eq.append(NoEscape(rf'&= {tau_b:.2f} \text{{ MPa}}\\\\'))
                tau_b_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2, Eq. 1.21]}\\'))
                tau_b_eq.append(NoEscape(r'\end{aligned}'))
            elif 0.8 < lambda_w < 1.2:
                tau_b = round((1 - 0.8 * (lambda_w - 0.8)) * (fy / (3**0.5)), 2)
                tau_b_eq = Math(inline=True)
                tau_b_eq.append(NoEscape(r'\begin{aligned}\\'))
                tau_b_eq.append(NoEscape(r'0.8 < \lambda_w < 1.2: \quad \tau_b &= [1 - 0.8(\lambda_w - 0.8)]\dfrac{f_{yw}}{\sqrt{3}}\\\\'))
                tau_b_eq.append(NoEscape(rf'&= [1 - 0.8({lambda_w:.3f} - 0.8)] \times \dfrac{{{fy:.1f}}}{{\sqrt{{3}}}}\\\\'))
                tau_b_eq.append(NoEscape(rf'&= {tau_b:.2f} \text{{ MPa}}\\\\'))
                tau_b_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2, Eq. 1.21]}\\'))
                tau_b_eq.append(NoEscape(r'\end{aligned}'))
            else:
                tau_b = round(fy / (3**0.5 * lambda_w), 2)
                tau_b_eq = Math(inline=True)
                tau_b_eq.append(NoEscape(r'\begin{aligned}\\'))
                tau_b_eq.append(NoEscape(r'\lambda_w \geq 1.2: \quad \tau_b &= \dfrac{f_{yw}}{\sqrt{3}\lambda_w}\\\\'))
                tau_b_eq.append(NoEscape(rf'&= \dfrac{{{fy:.1f}}}{{\sqrt{{3}} \times {lambda_w:.3f}}}\\\\'))
                tau_b_eq.append(NoEscape(rf'&= {tau_b:.2f} \text{{ MPa}}\\\\'))
                tau_b_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2]}\\'))
                tau_b_eq.append(NoEscape(r'\end{aligned}'))
            
            report_check.append([
                'Design Shear Stress',
                '',
                tau_b_eq,
                ''
            ])
            
            V_cr_val = round(Avw * tau_b / 1000, 2)
            
            Vcr_eq = Math(inline=True)
            Vcr_eq.append(NoEscape(r'\begin{aligned}\\'))
            Vcr_eq.append(NoEscape(r'V_{cr} &= A_{vw} \times \tau_b\\\\'))
            Vcr_eq.append(NoEscape(rf'&= {Avw:.2f} \times {tau_b:.2f}\\\\'))
            Vcr_eq.append(NoEscape(rf'&= {V_cr_val:.2f} \text{{ kN}}\\\\'))
            Vcr_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.1]}\\'))
            Vcr_eq.append(NoEscape(r'\end{aligned}'))
            
            report_check.append([
                'Shear Buckling Resistance',
                '',
                Vcr_eq,
                ''
            ])

            if shear_method == 'Tension Field Action':
                # --- TENSION FIELD ACTION REPORTING ---
                
                # Recalculate Tension Field parameters
                V_cr = IS800_2007.cl_8_4_2_2_Vcr_Simple_postcritical(tau_b, Avw)
                
                # We need M_applied (calculated/user) but for calculation of N_f, shear.py uses load.moment (N-mm)
                # Ensure units are correct. M_applied earlier is in kNm.
                # tension_field_unequal_I_corrected expects M in N-mm
                M_design_Nmm = M_applied * 1e6 
                
                Nf_val = M_design_Nmm / (d_eff + (tf_top + tf_bot) / 2)
                
                phi, Mfr_t, Mfr_b, s_t, s_b, w_tf, psi, fv, V_tf_val = tension_field_unequal_I_corrected(
                    c_val, d_eff, tw, fy, bf_top, tf_top, bf_bot, tf_bot, Nf_val, gamma_m0, Avw, tau_b
                )
                
                V_tf_final = round(V_tf_val / 1000, 2)
                
                # 1. Tension Field Angle (phi) - DDCL Eq 1.29
                phi_eq = Math(inline=True)
                phi_eq.append(NoEscape(r'\begin{aligned}\\'))
                phi_eq.append(NoEscape(r'\phi &= \tan^{-1} \left( \dfrac{d}{c} \right)\\\\'))
                phi_eq.append(NoEscape(rf'&= \tan^{{-1}} \left( \dfrac{{{d_eff:.1f}}}{{{c_val:.1f}}} \right)\\\\'))
                phi_eq.append(NoEscape(rf'&= {phi:.2f}^\circ\\'))
                phi_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2a]}\\'))
                phi_eq.append(NoEscape(r'\end{aligned}'))
                
                report_check.append([
                    NoEscape(r'Tension Field Angle'),
                    '',
                    phi_eq,
                    ''
                ])
                
                # 2. Width of Tension Field (w_tf) - DDCL Eq 1.30
                # w_tf = d*cos(phi) + (c - sc - st)*sin(phi)
                # Note: 'sc' in code is 's_b' (anchor length bottom/compression?) or s_t/s_b generically
                # The function returns s_t (top) and s_b (bottom). DDCL uses sc and st.
                # Just show the formula with values.
                
                wtf_eq = Math(inline=True)
                wtf_eq.append(NoEscape(r'\begin{aligned}\\'))
                wtf_eq.append(NoEscape(r'w_{tf} &= d \cos \phi + (c - s_c - s_t) \sin \phi\\\\'))
                wtf_eq.append(NoEscape(rf'&= {d_eff:.1f} \cos({phi:.2f}) + ({c_val:.1f} - {s_b:.1f} - {s_t:.1f}) \sin({phi:.2f})\\\\'))
                wtf_eq.append(NoEscape(rf'&= {w_tf:.2f} \text{{ mm}}\\'))
                wtf_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2a]}\\'))
                wtf_eq.append(NoEscape(r'\end{aligned}'))
                
                report_check.append([
                    NoEscape(r'Width of Tension Field'),
                    '',
                    wtf_eq,
                    ''
                ])
                
                # 3. Yield Strength of Tension Field (fv) - DDCL Eq 1.31
                # fv = sqrt(fy^2 - 3*tau_b^2 + psi^2) - psi
                # psi = 1.5 * tau_b * sin(2phi)
                
                fv_eq = Math(inline=True)
                fv_eq.append(NoEscape(r'\begin{aligned}\\'))
                fv_eq.append(NoEscape(r'\psi &= 1.5 \tau_b \sin(2\phi)\\\\'))
                fv_eq.append(NoEscape(rf'&= 1.5 \times {tau_b:.2f} \times \sin(2 \times {phi:.2f}) = {psi:.2f}\\\\'))
                fv_eq.append(NoEscape(r'f_v &= \sqrt{f_{yw}^2 - 3 \tau_b^2 + \psi^2} - \psi\\\\'))
                fv_eq.append(NoEscape(rf'&= \sqrt{{{fy:.1f}^2 - 3({tau_b:.2f})^2 + ({psi:.2f})^2}} - {psi:.2f}\\\\'))
                fv_eq.append(NoEscape(rf'&= {fv:.2f} \text{{ MPa}}\\'))
                fv_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2a]}\\'))
                fv_eq.append(NoEscape(r'\end{aligned}'))
                
                report_check.append([
                    NoEscape(r'Yield Strength of Web'),
                    '',
                    fv_eq,
                    ''
                ])
                
                # 4. Design Shear Strength (V_tf) - DDCL Eq 1.28
                vtf_eq = Math(inline=True)
                vtf_eq.append(NoEscape(r'\begin{aligned}\\'))
                vtf_eq.append(NoEscape(r'V_{tf} &= [A_{vm} \tau_b + 0.9 w_{tf} t_w f_v \sin \phi] \times 10^{-3}\\\\'))
                vtf_eq.append(NoEscape(rf'&= [{Avw:.2f} \times {tau_b:.2f} + 0.9 \times {w_tf:.2f} \times {tw:.1f} \times {fv:.2f} \times \sin({phi:.2f})] \times 10^{{-3}}\\\\')) 
                vtf_eq.append(NoEscape(rf'&= {V_tf_final:.2f} \text{{ kN}}\\'))
                vtf_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2a]}\\'))
                vtf_eq.append(NoEscape(r'\end{aligned}'))
                
                shear_status = 'Pass' if shear_flag1 else 'Fail'
                
                report_check.append([
                    NoEscape(r'Design Shear Strength'),
                    f'{V_applied:.2f}', # Applied Load
                    vtf_eq,
                    shear_status
                ])

        # Web crippling
        if hasattr(pg_obj, 'F_q') and pg_obj.F_q not in [None, 'NA', 0]:
            Fq = round(pg_obj.F_q / 1000, 2)
            b1 = getattr(pg_obj, 'b1', 0)
            bearing_note = ""
            if b1 <= 0 or b1 < pg_obj.web_thickness * 2:
                bearing_note = " (min. assumed)"

            fq_eq = Math(inline=True)
            fq_eq.append(NoEscape(r'\begin{aligned}\\'))
            
            # Calculate n2 for display purpose if not explicitly available, based on Fq equation
            # Fq = (b1 + n2) * tw * fy / gamma_m0
            # (b1 + n2) = Fq * gamma_m0 / (tw * fy)
            # n2 = [Fq * 1000 * gamma_m0 / (tw * fy)] - b1
            # Note: Fq in pg_obj is in N. b1 in mm.
            
            n2_disp = 0
            if tw > 0 and fy > 0:
                try:
                    n2_disp = (pg_obj.F_q * gamma_m0) / (tw * fy) - b1
                except Exception:
                    n2_disp = 0
            
            fq_eq.append(NoEscape(r'F_w &= \dfrac{(b_1 + n_2) t_w f_y}{\gamma_{m0} \times 10^3}\\'))
            fq_eq.append(NoEscape(rf'&= \dfrac{{({b1:.1f} + {n2_disp:.1f}) \times {tw:.1f} \times {fy:.1f}}}{{{gamma_m0} \times 1000}}\\\\'))
            fq_eq.append(NoEscape(rf'&= {Fq:.2f} \text{{ kN}}\\'))
            fq_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.7.4]}\\'))
            fq_eq.append(NoEscape(r'\end{aligned}'))

            fq_status = 'Pass' if shear_flag3 else 'Fail'

            report_check.append([
                NoEscape(r'Web Crippling Strength'),
                '',
                fq_eq,
                fq_status
            ])

        # ==================== MOMENT CAPACITY CHECK ====================
        try:
            report_check.append(['SubSection', 'Moment Capacity Check', table_format])

            # READ Md from pg_obj
            Md_val = getattr(pg_obj, 'Md', 0)
            Md = round(Md_val * 1e-6, 2) if Md_val and Md_val > 0 else 0

            Zp_val = getattr(pg_obj, 'plast_sec_mod_z', 0)
            Zp = round(Zp_val * 1e-3, 2) if Zp_val and Zp_val > 0 else 0

            Ze_val = getattr(pg_obj, 'elast_sec_mod_z', 0)
            Ze = round(Ze_val * 1e-3, 2) if Ze_val and Ze_val > 0 else 0

            beta_b_val = getattr(pg_obj, 'betab', 1.0)
            beta_b = round(beta_b_val, 3) if beta_b_val else 1.0

            if section_class in ['Plastic', 'Compact']:
                Z_used = Zp
                Z_label = 'Z_p'
            else:
                Z_used = Ze
                Z_label = 'Z_e'

            # Beta_b
            beta_eq = Math(inline=True)
            beta_eq.append(NoEscape(r'\begin{aligned}\\'))
            beta_eq.append(NoEscape(rf'\beta_b &= {beta_b:.2f}\\'))
            beta_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                NoEscape(r'Beta b Factor'),
                '',
                beta_eq,
                ''
            ])

            # ==================== LATERAL TORSIONAL BUCKLING (Integrated) ====================
            support_type = getattr(pg_obj, 'support_type', '')
            if support_type in ['Major Laterally Unsupported', 'Minor Laterally Unsupported']:
                # No SubSection header - listed as rows in Moment Capacity Check

                L_eff = getattr(pg_obj, 'effective_length', 0)
                Mcr_val = getattr(pg_obj, 'M_cr', 0)
                Mcr = round(Mcr_val * 1e-6, 2) if Mcr_val and Mcr_val > 0 else 'NA'
                val_lam = getattr(pg_obj, 'lambda_lt', None)
                lambda_LT = round(val_lam, 3) if isinstance(val_lam, (int, float)) else 'NA'
                
                val_chi = getattr(pg_obj, 'X_lt', None)
                chi_LT = round(val_chi, 3) if isinstance(val_chi, (int, float)) else 'NA'

                val_fbd = getattr(pg_obj, 'fbd_lt', None)
                fbd = round(val_fbd, 2) if isinstance(val_fbd, (int, float)) else 'NA'

                # Effective length
                L_total = getattr(pg_obj, 'length', 0)
                lefactor = getattr(pg_obj, 'lefactor', 1.0)
                
                leff_eq = Math(inline=True)
                leff_eq.append(NoEscape(r'\begin{aligned}\\'))
                leff_eq.append(NoEscape(r'L_{LT} &= K \times L\\'))
                leff_eq.append(NoEscape(rf'&= {lefactor:.2f} \times {L_total:.1f} = {L_eff:.1f} \text{{ mm}}\\'))
                leff_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl. 8.3 / Table 15]}\\'))
                leff_eq.append(NoEscape(r'\end{aligned}'))

                report_check.append([
                    NoEscape(r'Effective Length'),
                    '',
                    leff_eq,
                    ''
                ])

                # Critical moment
                if Mcr != 'NA':
                    # Calculate properties for Mcr breakdown
                    try:
                        Iy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(D, bf_top, bf_bot, tw, tf_top, tf_bot)
                        # Mcr,z (Euler) in kNm
                        # Mcr_z = (pi^2 * E * Iy) / L_LT^2
                        if L_eff > 0:
                            Mcr_z_Nmm = (math.pi**2 * E * Iy) / (L_eff**2)
                            Mcr_z = Mcr_z_Nmm * 1e-6
                        else:
                            Mcr_z = 0

                        # Back-calculate Mcr,T -> Mcr = sqrt(Mcr_z * Mcr_T) => Mcr_T = Mcr^2 / Mcr_z
                        if Mcr_z > 0:
                             Mcr_T = (Mcr)**2 / Mcr_z
                        else:
                             Mcr_T = 0
                    except Exception as m_e:
                        # Fallback if calc fails
                        Mcr_z = 0
                        Mcr_T = 0
                    
                    mcr_eq = Math(inline=True)
                    mcr_eq.append(NoEscape(r'\begin{aligned}\\'))
                    mcr_eq.append(NoEscape(r'M_{cr} &= \sqrt{M_{cr,z} \times M_{cr,T}}\\'))
                    if Mcr_z > 0 and Mcr_T > 0:
                         mcr_eq.append(NoEscape(rf'&= \sqrt{{{Mcr_z:.2f} \times {Mcr_T:.2f}}}\\'))
                    mcr_eq.append(NoEscape(rf'&= {Mcr:.2f} \text{{ kNm}}\\'))
                    mcr_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Annex E]}\\'))
                    mcr_eq.append(NoEscape(r'\end{aligned}'))

                    report_check.append([
                        NoEscape(r'Elastic Critical Moment'),
                        '',
                        mcr_eq,
                        ''
                    ])

                # Lambda_LT
                if lambda_LT != 'NA':
                    lambda_eq = Math(inline=True)
                    lambda_eq.append(NoEscape(r'\begin{aligned}\\'))
                    lambda_eq.append(NoEscape(rf'\lambda_{{LT}} &= {lambda_LT:.3f}\\'))
                    lambda_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.2.2]}\\'))
                    lambda_eq.append(NoEscape(r'\end{aligned}'))

                    report_check.append([
                        NoEscape(r'Slenderness Ratio'),
                        '',
                        lambda_eq,
                        ''
                    ])

                # f_bd
                if fbd != 'NA' and chi_LT != 'NA':
                    fbd_eq = Math(inline=True)
                    fbd_eq.append(NoEscape(r'\begin{aligned}\\'))
                    fbd_eq.append(NoEscape(r'f_{bd} &= \dfrac{\chi_{LT} \times f_y}{\gamma_{m0}}\\'))
                    fbd_eq.append(NoEscape(rf'&= \dfrac{{{chi_LT:.3f} \times {fy}}}{{{gamma_m0}}}\\\\'))
                    fbd_eq.append(NoEscape(rf'&= {fbd:.2f} \text{{ MPa}}\\\\'))
                    fbd_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.2.2]}\\'))
                    fbd_eq.append(NoEscape(r'\end{aligned}'))

                    report_check.append([
                        NoEscape(r'Design Bending Strength'),
                        '',
                        fbd_eq,
                        ''
                    ])

            # Design moment capacity
            md_eq = Math(inline=True)
            md_eq.append(NoEscape(r'\begin{aligned}\\'))

            support_type = getattr(pg_obj, 'support_type', '')
            if support_type == 'Major Laterally Unsupported':
                md_eq.append(NoEscape(rf'M_d &= \beta_b {Z_label} f_{{bd}}\\\\'))
                md_eq.append(NoEscape(rf'&= {beta_b} \times {Z_used:.2f} \times f_{{bd}}\\\\'))
            else:
                md_eq.append(NoEscape(rf'M_d &= \dfrac{{\beta_b {Z_label} f_y}}{{\gamma_{{m0}}}}\\\\'))
                md_eq.append(NoEscape(rf'&= \dfrac{{{beta_b} \times {Z_used:.2f} \times {fy}}}{{{gamma_m0}}}\\\\'))

            md_eq.append(NoEscape(rf'&= {Md:.2f} \text{{ kNm}}\\\\'))

            if support_type == 'Major Laterally Unsupported':
                md_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.2.2]}\\'))
            else:
                md_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.2.1]}\\'))

            md_eq.append(NoEscape(r'\end{aligned}'))

            moment_status = 'Pass' if moment_checks else 'Fail'

            report_check.append([
                NoEscape(r'Design Moment Capacity'),
                NoEscape(rf'{M_applied:.2f}\text{{ kNm}}'),
                md_eq,
                moment_status
            ])
        except Exception as e:
            logger.error(f"Error in Moment Capacity Check: {str(e)}")
            report_check.append(['Error', 'Moment Capacity Check Failed', str(e), 'Fail'])



        # ==================== DEFLECTION CHECK ====================
        report_check.append(['SubSection', 'Deflection Check', table_format])

        defl_val = getattr(pg_obj, 'deflection_criteria', 600)
        try:
             defl_limit_ratio = float(defl_val)
             if defl_limit_ratio <= 0:
                 defl_limit_ratio = 600
        except (ValueError, TypeError):
             defl_limit_ratio = 600

        if L > 0:

            # Allowable deflection
            delta_allow = round(L / defl_limit_ratio, 2)

            allow_eq = Math(inline=True)
            allow_eq.append(NoEscape(r'\begin{aligned}\\'))
            allow_eq.append(NoEscape(rf'\delta_{{allow}} &= \dfrac{{L}}{{{defl_limit_ratio}}}\\\\'))
            allow_eq.append(NoEscape(rf'&= \dfrac{{{L:.1f}}}{{{defl_limit_ratio}}}\\\\'))
            allow_eq.append(NoEscape(rf'&= {delta_allow:.2f} \text{{ mm}}\\\\'))
            allow_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 6]}\\'))
            allow_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                NoEscape(r'Allowable Deflection'),
                '',
                allow_eq,
                ''
            ])

            # Actual deflection
            delta_actual_str = getattr(pg_obj, 'calculated_deflection', 'NA')
            if delta_actual_str not in ['NA', 'Skipped']:
                try:
                    delta_actual = round(float(delta_actual_str), 2)

                    # Calculate Iz for formula display
                    try:
                        Iz_mm4 = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(
                            D, bf_top, bf_bot, tw, tf_top, tf_bot
                        )
                    except:
                        Iz_mm4 = 1

                    # Calculate w (N/mm) from M_applied (kNm) assuming UDL
                    # M = w L^2 / 8 => w = 8 M / L^2
                    if L > 0:
                         M_Nmm = M_applied * 1e6
                         w_udl = 8 * M_Nmm / (L**2)
                    else:
                         w_udl = 0

                    actual_eq = Math(inline=True)
                    actual_eq.append(NoEscape(r'\begin{aligned}\\'))
                    actual_eq.append(NoEscape(r'\delta &= \dfrac{5 w L^4}{384 E I_{z}}\\\\'))
                    actual_eq.append(NoEscape(rf'&= \dfrac{{5 \times {w_udl:.2f} \times {L:.1f}^4}}{{384 \times {E} \times {Iz_mm4:.2e}}}\\\\'))
                    actual_eq.append(NoEscape(rf'&= {delta_actual:.2f} \text{{ mm}}\\\\'))
                    actual_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 6]}'))
                    actual_eq.append(NoEscape(r'\end{aligned}'))

                    defl_status = 'Pass' if defl_check else 'Fail'
                    report_check.append([
                        'Actual Deflection',
                        NoEscape(rf'{delta_allow:.2f} \text{{ mm}}'), 
                        actual_eq,
                        defl_status
                    ])
                except (ValueError, TypeError):
                    pass

        # ==================== WELD DESIGN ====================
        report_check.append(['SubSection', 'Weld Design', table_format])

        weld_top = getattr(pg_obj, 'atop', 0)
        weld_bot = getattr(pg_obj, 'abot', 0)
        t_min = min(tw, tf_top, tf_bot) if tw > 0 and tf_top > 0 and tf_bot > 0 else 0
        weld_stiff = getattr(pg_obj, 'weld_stiff', None)

        # Minimum weld size per IS 800:2007 Table 21
        if t_min < 10:
            s_min = 3
        elif t_min <= 20:
            s_min = 5
        else:
            s_min = 6

        minweld_eq = Math(inline=True)
        minweld_eq.append(NoEscape(r'\begin{aligned}\\'))
        minweld_eq.append(NoEscape(rf's_{{min}} &= {s_min:.1f} \text{{ mm}}\\'))
        minweld_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Table 21]}\\'))
        minweld_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Minimum Weld Size',
            '',
            minweld_eq,
            ''
        ])

        # Weld sizes - design outputs
        if weld_top > 0:
            wtop_eq = Math(inline=True)
            wtop_eq.append(NoEscape(r'\begin{aligned}\\'))
            wtop_eq.append(NoEscape(rf's_{{top}} &= {round(weld_top, 1):.1f} \text{{ mm}}\\'))
            wtop_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.10.5.7]}\\'))
            wtop_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                'Weld Size - Web to Top Flange',
                '',
                wtop_eq,
                ''
            ])

        if weld_bot > 0:
            wbot_eq = Math(inline=True)
            wbot_eq.append(NoEscape(r'\begin{aligned}\\'))
            wbot_eq.append(NoEscape(rf's_{{bot}} &= {round(weld_bot, 1):.1f} \text{{ mm}}\\'))
            wbot_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.10.5.7]}\\'))
            wbot_eq.append(NoEscape(r'\end{aligned}'))

            report_check.append([
                'Weld Size - Web to Bottom Flange',
                '',
                wbot_eq,
                ''
            ])

        if weld_stiff and weld_stiff not in [None, 'NA', 0, '']:
            weld_stiff_val = float(weld_stiff)
            if weld_stiff_val > 0:
                wstiff_eq = Math(inline=True)
                wstiff_eq.append(NoEscape(r'\begin{aligned}'))
                wstiff_eq.append(NoEscape(rf's_{{stiff}} &= {round(weld_stiff_val, 1):.1f} \text{{ mm}}\\'))
                wstiff_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.10.5.7]}\\'))
                wstiff_eq.append(NoEscape(r'\end{aligned}'))

                report_check.append([
                    'Weld Size - Stiffener to Web',
                    '',
                    wstiff_eq,
                    ''
                ])




        # ==================== INTERMEDIATE STIFFENER - SECTION 1.5.1 ====================
        report_check.append(['SubSection', 'Intermediate Stiffener', table_format])

        c = getattr(pg_obj, 'c', 0)

        if web_philosophy == 'Thick Web without ITS':
             report_check.append([
                'Minimum Moment of Inertia',
                '',
                'Not Required',
                ''
            ])
             
             report_check.append([
                'Critical Buckling Stress',
                '',
                'Not Required',
                ''
            ])
        else:
            if d > 0:
                c_d_ratio = round(c / d, 3)
                sqrt_2 = 1.414
                
                if c_d_ratio >= sqrt_2:
                    I_s_min = round(0.75 * d * (tw**3), 2)
                    
                    I_s_eq = Math(inline=True)
                    I_s_eq.append(NoEscape(r'\begin{aligned}\\'))
                    I_s_eq.append(NoEscape(rf'\text{{Since }} \dfrac{{c}}{{d}} &= {c_d_ratio:.3f} \geq \sqrt{{2}}\\\\'))
                    I_s_eq.append(NoEscape(r'I_s &\geq 0.75 \, d \, t_w^3\\\\'))
                    I_s_eq.append(NoEscape(rf'&\geq 0.75 \times {d:.1f} \times ({tw:.1f})^3\\\\'))
                    I_s_eq.append(NoEscape(rf'&\geq {I_s_min:.2f} \text{{ mm}}^4\\\\'))
                    I_s_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.7.1.2, Eq. 1.17]}\\'))
                    I_s_eq.append(NoEscape(r'\end{aligned}'))
                else:
                    # condition_status = rf'Since \dfrac{{c}}{{d}} = {c_d_ratio:.3f} < \sqrt{{2}}'
                    I_s_min = round((1.5 * (d**3) * (tw**3)) / (c**2), 2)
                    
                    I_s_eq = Math(inline=True)
                    I_s_eq.append(NoEscape(r'\begin{aligned}\\'))
                    I_s_eq.append(NoEscape(rf'\text{{Since }} \dfrac{{c}}{{d}} &= {c_d_ratio:.3f} < \sqrt{{2}}\\\\'))
                    I_s_eq.append(NoEscape(r'I_s &\geq 1.5 \, \dfrac{d^3 t_w^3}{c^2}\\\\'))
                    I_s_eq.append(NoEscape(rf'&\geq 1.5 \times \dfrac{{({d:.1f})^3 \times ({tw:.1f})^3}}{{({c:.1f})^2}}\\\\'))
                    I_s_eq.append(NoEscape(rf'&\geq {I_s_min:.2f} \text{{ mm}}^4\\\\'))
                    I_s_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.7.1.2, Eq. 1.18]}\\'))
                    I_s_eq.append(NoEscape(r'\end{aligned}'))
                
                report_check.append([
                    'Minimum Moment of Inertia',
                    '',
                    I_s_eq,
                    ''
                ])
                
                mu = 0.3
                tau_crc = round((kv * (3.14159**2) * E) / (12 * (1 - mu**2) * ((d/tw)**2)), 2)
                
                tau_crc_eq = Math(inline=True)
                tau_crc_eq.append(NoEscape(r'\begin{aligned}\\'))
                tau_crc_eq.append(NoEscape(r'\tau_{cr,e} &= \dfrac{K_v \pi^2 E}{12(1-\mu^2)(d/t_w)^2}\\\\'))
                tau_crc_eq.append(NoEscape(rf'&= \dfrac{{{kv:.3f} \times \pi^2 \times {E}}}{{12(1-{mu}^2)({d:.1f}/{tw:.1f})^2}}\\\\'))
                tau_crc_eq.append(NoEscape(rf'&= {tau_crc:.2f} \text{{ MPa}}\\\\'))
                tau_crc_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2, Eq. 1.23]}\\'))
                tau_crc_eq.append(NoEscape(r'\end{aligned}'))
                
                report_check.append([
                    'Critical Buckling Stress',  
                    NoEscape(rf'$\mu = {mu}$'),
                    tau_crc_eq,
                    ''
                ])
            

        # ==================== END PANEL STIFFENER - SECTION 1.5.2 ====================
        report_check.append(['SubSection', 'End Panel Stiffener', table_format])

        # Vertical Anchor Force
        Vp = round((d * tw * fy) / (3**0.5), 2)
        Vp_kN = round(Vp / 1000, 2)

        Vp_eq = Math(inline=True)
        Vp_eq.append(NoEscape(r'\begin{aligned}\\'))
        Vp_eq.append(NoEscape(r'V_p &= \dfrac{d \cdot t_w \cdot f_y}{\sqrt{3}}\\\\'))
        Vp_eq.append(NoEscape(rf'&= \dfrac{{{d:.1f} \times {tw:.1f} \times {fy:.1f}}}{{\sqrt{{3}}}}\\\\'))
        Vp_eq.append(NoEscape(rf'&= {Vp_kN:.2f} \text{{ kN}}\\\\'))
        Vp_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2]}\\'))
        Vp_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Vertical Anchor Force',
            '',
            Vp_eq,
            ''
        ])

        # Tension Flange Reaction
        Rtf = round(Vp_kN / 2, 2)

        Rtf_eq = Math(inline=True)
        Rtf_eq.append(NoEscape(r'\begin{aligned}\\'))
        Rtf_eq.append(NoEscape(r'R_{tf} &= \dfrac{V_p}{2}\\\\'))
        Rtf_eq.append(NoEscape(rf'&= \dfrac{{{Vp_kN:.2f}}}{{2}}\\\\'))
        Rtf_eq.append(NoEscape(rf'&= {Rtf:.2f} \text{{ kN}}\\\\'))
        Rtf_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2]}\\'))
        Rtf_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Tension Flange Reaction',
            '',
            Rtf_eq,
            ''
        ])

        # Tension Flange Moment
        Mtf = round(Vp_kN * d / 10, 2)

        Mtf_eq = Math(inline=True)
        Mtf_eq.append(NoEscape(r'\begin{aligned}\\'))
        Mtf_eq.append(NoEscape(r'M_{tf} &= \dfrac{V_p \cdot d}{10}\\\\'))
        Mtf_eq.append(NoEscape(rf'&= \dfrac{{{Vp_kN:.2f} \times {d:.1f}}}{{10}}\\\\'))
        Mtf_eq.append(NoEscape(rf'&= {Mtf:.2f} \text{{ kNmm}}\\\\'))
        Mtf_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.4.2.2]}\\'))
        Mtf_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Tension Flange Moment',
            '',
            Mtf_eq,
            ''
        ])

        if web_philosophy != "Thick Web without ITS":
            # Calculate end panel stiffener thickness based on tension flange reaction
            Vp = (d * tw * fy) / math.sqrt(3)
            Rtf = Vp / 2  # Tension flange reaction
            
            # Design stiffener for Rtf
            # Assume stiffener is a pair on both sides of web
            endstiffwidth = getattr(pg_obj, 'end_stiffwidth', 0)
            stiff_width = endstiffwidth 
            
            # Required thickness based on bearing stress
            # σ_bearing = Rtf / (2 × stiff_width × t_stiff) ≤ fy / γm0
            # Solving for t_stiff: t_stiff ≥ (Rtf × γm0) / (2 × stiff_width × fy)
            
            if stiff_width > 0:
                t_req = (Rtf * gamma_m0) / (2 * stiff_width * fy)
                
                # Use thickness from pg_obj if available (Optimization source of truth)
                t_provided_obj = getattr(pg_obj, 'end_stiffthickness', 0)
                
                if t_provided_obj and t_provided_obj > 0:
                    pg_obj.endstiffthickness = float(t_provided_obj)
                else:
                    # Fallback design logic if not provided
                    available_thk = [8, 10, 12, 16, 20, 25, 32, 40, 50]
                    
                    endstiffthickness = None
                    for thk in available_thk:
                        if float(thk) >= t_req:
                            pg_obj.endstiffthickness = float(thk)
                            break
                    
                    if pg_obj.endstiffthickness is None:
                        pg_obj.endstiffthickness = float(available_thk[-1])  # Use maximum if all fail
                        logger.warning(f"End stiffener thickness {pg_obj.endstiffthickness}mm may be insufficient")
            else:
                pg_obj.endstiffthickness = 50.0
            
            pg_obj.endpanelstiffenerthickness = pg_obj.endstiffthickness
            logger.info(f"End Panel Stiffener Thickness: {pg_obj.endpanelstiffenerthickness} mm")
        else:
            # Thick web without stiffeners
            pg_obj.endpanelstiffenerthickness = "NA"
            pg_obj.endstiffthickness = 0

        # ==================== LONGITUDINAL STIFFENER - SECTION 1.5.3 ====================
        report_check.append(['SubSection', 'Longitudinal Stiffener', table_format])

        # Calculate epsilon and limits
        epsilon_w = round((250 / fy)**0.5, 3)
        limit_200_eps = round(200 * epsilon_w, 2)
        limit_250_eps = round(250 * epsilon_w, 2)
        limit_400_eps = round(400 * epsilon_w, 2)
        
        d_tw_ratio = round(d / tw, 2)

        # Row 1: Web Thickness Limits (Check for Longitudinal Stiffener Requirement)
        req_check_eq = Math(inline=True)
        req_check_eq.append(NoEscape(r'\begin{aligned}\\'))
        req_check_eq.append(NoEscape(rf'1.&\text{{Transverse Stiffeners only: }}\\'))
        req_check_eq.append(NoEscape((rf'&\dfrac{{d}}{{t_w}} \leq 200 \epsilon_w = {limit_200_eps:.2f}\\\\')))
        req_check_eq.append(NoEscape(rf'2.&\text{{With 1st Longitudinal Stiffener: }}\\'))
        req_check_eq.append(NoEscape(rf'&\dfrac{{d}}{{t_w}} \leq 250 \epsilon_w = {limit_250_eps:.2f}\\\\'))    
        req_check_eq.append(NoEscape(rf'3.&\text{{With 2nd Longitudinal Stiffener: }}\\'))
        req_check_eq.append(NoEscape(rf'&\dfrac{{d}}{{t_w}} \leq 400 \epsilon_w = {limit_400_eps:.2f}\\\\'))
        req_check_eq.append(NoEscape(rf'4.&\text{{Actual Web Slenderness: }}\\\\'))
        req_check_eq.append(NoEscape(rf'&\dfrac{{d}}{{t_w}} = {d_tw_ratio:.2f}\\\\'))
        
        long_stiff_required = False
        second_stiff_required = False

        if d_tw_ratio <= limit_200_eps:
             req_check_eq.append(NoEscape(rf'&\text{{Since }} {d_tw_ratio:.2f} \leq {limit_200_eps:.2f}, \text{{ Limit Satsified.}}\\\\'))
             req_check_eq.append(NoEscape(r'&\text{Longitudinal Stiffeners NOT Required.}\\'))
             req_check_eq.append(NoEscape(r'\end{aligned}'))
             
             report_check.append([
                'Web Thickness Limits',
                '',
                req_check_eq,
                ''
            ])
             
             # Add placeholder rows for consistency
             report_check.append(['First Stiffener Placement', '', 'Not Required', ''])
             report_check.append(['First Stiffener - Moment of Inertia', '', 'Not Required', ''])
             report_check.append(['Second Stiffener (Neutral Axis)', '', 'Not Required', ''])

        else:
             long_stiff_required = True
             req_check_eq.append(NoEscape(rf'&\text{{Since }} {d_tw_ratio:.2f} > {limit_200_eps:.2f}, \text{{ Limit NOT Satsified.}}\\\\'))
             req_check_eq.append(NoEscape(r'&\text{Longitudinal Stiffeners REQUIRED.}\\\\'))
             req_check_eq.append(NoEscape(r'\end{aligned}'))
             
             report_check.append([
                'Web Thickness Limits',
                '',
                req_check_eq,
                ''
            ])

             # First Stiffener Placement
             y_comp = round((D - tf_top - tf_bot) / 5, 2)

             y_comp_eq = Math(inline=True)
             y_comp_eq.append(NoEscape(r'\begin{aligned}\\'))
             y_comp_eq.append(NoEscape(r'y &= \dfrac{1}{5}(D - t_f - t_f)\\\\'))
             y_comp_eq.append(NoEscape(rf'&= \dfrac{{1}}{{5}}({D:.1f} - {tf_top:.1f} - {tf_bot:.1f})\\\\'))
             y_comp_eq.append(NoEscape(rf'&= {y_comp:.2f} \text{{ mm}}\\\\'))
             y_comp_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.7.1.3]}\\'))
             y_comp_eq.append(NoEscape(r'\end{aligned}'))

             report_check.append([
                'First Stiffener Placement',
                'Distance from compression flange',
                y_comp_eq,
                ''
             ])

             # First Stiffener Design (Is_1 calculation)
             Is_1 = round(4 * c * (tw**3), 2)

             Is1_eq = Math(inline=True)
             Is1_eq.append(NoEscape(r'\begin{aligned}\\'))
             Is1_eq.append(NoEscape(r'I_s &\geq 4 c t_w^3\\\\'))
             Is1_eq.append(NoEscape(rf'&\geq 4 \times {c:.1f} \times ({tw:.1f})^3\\\\'))
             Is1_eq.append(NoEscape(rf'&\geq {Is_1:.2f} \text{{ mm}}^4\\\\'))
             Is1_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.7.2.4]}\\'))
             Is1_eq.append(NoEscape(r'\end{aligned}'))

             report_check.append([
                 'First Stiffener - Moment of Inertia',
                 '',
                 Is1_eq,
                 ''
             ])

             # Check for Second Stiffener Requirement
             Is2_check_eq = Math(inline=True)
             Is2_check_eq.append(NoEscape(r'\begin{aligned}\\'))
             Is2_check_eq.append(NoEscape(r'\text{Limit for single longitudinal stiffener:}\\\\'))
             Is2_check_eq.append(NoEscape(rf'\dfrac{{d}}{{t_w}} \leq 250 \epsilon_w = {limit_250_eps:.2f}\\\\'))
             Is2_check_eq.append(NoEscape(r'\text{Actual Web Slenderness:}\\\\'))
             Is2_check_eq.append(NoEscape(rf'\dfrac{{d}}{{t_w}} &= {d_tw_ratio:.2f}\\\\'))
             
             if d_tw_ratio > limit_250_eps:
                 second_stiff_required = True
                 Is2_check_eq.append(NoEscape(rf'\text{{Since }} {d_tw_ratio:.2f} > {limit_250_eps:.2f}, \text{{ Limit NOT Satsified.}}\\\\'))
                 Is2_check_eq.append(NoEscape(r'\text{Second Stiffener at N.A. REQUIRED.}\\'))
                 
                 # Add 2nd stiffener calculation to the same block or next
                 d_2 = round(D - tf_top - tf_bot, 2)
                 Is_2 = round(d_2 * (tw**3), 2)
                 Is2_check_eq.append(NoEscape(r'I_s &\geq d_2 \times t_w^3\\\\'))
                 Is2_check_eq.append(NoEscape(rf'&\geq {d_2:.2f} \times ({tw:.1f})^3\\\\'))
                 Is2_check_eq.append(NoEscape(rf'&\geq {Is_2:.2f} \text{{ mm}}^4\\\\'))
                 Is2_check_eq.append(NoEscape(r'&\text{[Ref: IS 800:2007, Cl.8.7.13.2, Eq. 1.42]}\\'))
                 Is2_check_eq.append(NoEscape(r'\end{aligned}'))
                 
                 report_check.append([
                    'Second Stiffener (Neutral Axis)',
                    '',
                    Is2_check_eq,
                    ''
                 ])
             else:
                 Is2_check_eq.append(NoEscape(rf'\text{{Since }} {d_tw_ratio:.2f} \leq {limit_250_eps:.2f}, \text{{ Limit Satsified.}}\\\\'))
                 Is2_check_eq.append(NoEscape(r'\text{NOT Required.}\\'))
                 Is2_check_eq.append(NoEscape(r'\end{aligned}'))
                 
                 report_check.append([
                    'Second Stiffener (Neutral Axis)',
                    '',
                    Is2_check_eq,
                    ''
                 ])


        # ==================== STIFFENER DESIGN SUMMARY ====================
        report_check.append(['SubSection', 'Stiffener Design Summary', table_format])

        # Get all stiffener parameters from pg_obj
        t_int_stiff = getattr(pg_obj, 'IntStiffThickness', 0)
        t_end_stiff = getattr(pg_obj, 'endstiffthickness', 0)
        
        # Override for Thick Web without ITS
        if web_philosophy == 'Thick Web without ITS':
             t_int_stiff = "N/A"
             t_end_stiff = "N/A"
             method_name = "N/A"
             int_spacing = "N/A"
             num_end = "0"
        else:
             method_name = getattr(pg_obj, 'x', 'Simple Post Critical')
             int_spacing = getattr(pg_obj, 'c', 0)
             # Calculate number of end panel stiffeners
             if isinstance(t_end_stiff, (int, float)) and t_end_stiff > 0:
                 num_end = "2 (Pair)"
             else:
                 num_end = "0"
        
        # Determine Longitudinal Stiffener values based on requirement
        if long_stiff_required:
            t_long_stiff = getattr(pg_obj, 'longstiffenerthk', 'NA')
            num_long = getattr(pg_obj, 'longstiffenerno', 'Not Required')
            stiff_1_pos = getattr(pg_obj, 'x1', 'Not Required')
            stiff_2_pos = getattr(pg_obj, 'x2', 'Not Required')
        else:
            t_long_stiff = 'Not Required'
            num_long = 'Not Required'
            stiff_1_pos = 'Not Required'
            stiff_2_pos = 'Not Required'

        summary_data = [
            ['Method', str(method_name)],
            ['End Panel Stiffener Thickness (mm)', f'{t_end_stiff:.1f}' if isinstance(t_end_stiff, (int, float)) else str(t_end_stiff)],
            ['Number of End Panel Stiffeners', num_end],
            ['Intermediate Stiffener Thickness (mm)', f'{t_int_stiff:.1f}' if isinstance(t_int_stiff, (int, float)) else str(t_int_stiff)],
            ['Intermediate Stiffener Spacing (mm)', f'{int_spacing:.1f}' if isinstance(int_spacing, (int, float)) else str(int_spacing)],
            ['Longitudinal Stiffener Thickness (mm)', f'{t_long_stiff:.1f}' if isinstance(t_long_stiff, (int, float)) else str(t_long_stiff)],
            ['Number of Longitudinal Stiffeners', str(num_long)],
            ['Stiffener 1 Pos. from Comp. Flange (mm)', f'{stiff_1_pos:.2f}' if isinstance(stiff_1_pos, (int, float)) else str(stiff_1_pos)],
            ['Stiffener 2 Pos. from Comp. Flange (mm)', f'{stiff_2_pos:.2f}' if isinstance(stiff_2_pos, (int, float)) else str(stiff_2_pos)]
        ]

        # Create formatted table
        for item in summary_data:
            param_name = item[0]
            param_value = item[1]
            
            summary_eq = Math(inline=True)
            summary_eq.append(NoEscape(r'\begin{aligned}\\'))
            summary_eq.append(NoEscape(rf'\text{{{param_value}}}'))
            summary_eq.append(NoEscape(r'\end{aligned}'))
            
            report_check.append([
                param_name,
                '',
                summary_eq,
                ''
            ])


        # ==================== OVERALL DESIGN CHECK ====================
        report_check.append(['SubSection', 'Overall Design Check', table_format])

        # READ utilization ratios from pg_obj
        ur_moment = round(getattr(pg_obj, 'moment_ratio', 0), 3)
        ur_shear = round(getattr(pg_obj, 'shear_ratio', 0), 3)
        ur_deflection = round(getattr(pg_obj, 'deflection_ratio', 0), 3)

        # Moment utilization - show calculation
        moment_ur_eq = Math(inline=True)
        moment_ur_eq.append(NoEscape(r'\begin{aligned}\\'))
        moment_ur_eq.append(NoEscape(r'UR_M &= \dfrac{M_{applied}}{M_d}\\'))
        if Md > 0:
            moment_ur_eq.append(NoEscape(rf'&= \dfrac{{{M_applied:.2f}}}{{{Md:.2f}}}\\\\'))
        moment_ur_eq.append(NoEscape(rf'&= {ur_moment:.3f}\\\\'))
        moment_ur_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Moment Utilization Ratio',
            moment_ur_eq,
            f'{ur_moment:.3f}',
            ''
        ])

        # Shear utilization - show calculation
        shear_ur_eq = Math(inline=True)
        shear_ur_eq.append(NoEscape(r'\begin{aligned}\\'))
        shear_ur_eq.append(NoEscape(r'UR_V &= \dfrac{V_{applied}}{V_d}\\\\'))
        if V_d > 0:
            shear_ur_eq.append(NoEscape(rf'&= \dfrac{{{V_applied:.2f}}}{{{V_d:.2f}}}\\\\'))
        shear_ur_eq.append(NoEscape(rf'&= {ur_shear:.3f}\\\\'))
        shear_ur_eq.append(NoEscape(r'\end{aligned}'))

        report_check.append([
            'Shear Utilization Ratio',
            shear_ur_eq,
            f'{ur_shear:.3f}',
            ''
        ])

        # Deflection utilization - show calculation if applicable
        if ur_deflection > 0:
            delta_actual_str = getattr(pg_obj, 'calculated_deflection', 'NA')
            if delta_actual_str not in ['NA', 'Skipped']:
                try:
                    delta_actual = round(float(delta_actual_str), 2)
                    delta_allow = round(L / defl_limit_ratio, 2)

                    defl_ur_eq = Math(inline=True)
                    defl_ur_eq.append(NoEscape(r'\begin{aligned}\\'))
                    defl_ur_eq.append(NoEscape(r'UR_{\delta} &= \dfrac{\delta_{actual}}{\delta_{allowable}}\\\\'))
                    if delta_allow > 0:
                        defl_ur_eq.append(NoEscape(rf'&= \dfrac{{{delta_actual:.2f}}}{{{delta_allow:.2f}}}\\\\'))
                    defl_ur_eq.append(NoEscape(rf'&= {ur_deflection:.3f}\\\\'))
                    defl_ur_eq.append(NoEscape(r'\end{aligned}'))

                    report_check.append([
                        'Deflection Utilization Ratio',
                        defl_ur_eq,
                        f'{ur_deflection:.3f}',
                        ''
                    ])
                except (ValueError, TypeError):
                    pass

        # Overall design status - calculate and display
        overall_ur = max(ur_moment, ur_shear, ur_deflection)

        overall_eq = Math(inline=True)
        overall_eq.append(NoEscape(r'\begin{aligned}\\'))
        overall_eq.append(NoEscape(r'UR_{overall} &= \max(UR_M, UR_V, UR_{\delta})\\\\'))
        overall_eq.append(NoEscape(rf'&= \max({ur_moment:.3f}, {ur_shear:.3f}, {ur_deflection:.3f})\\\\'))
        overall_eq.append(NoEscape(rf'&= {round(overall_ur, 3):.3f}\\'))
        overall_eq.append(NoEscape(r'\end{aligned}'))

        final_status = 'Pass' if design_status else 'Fail'

        ur_text = "< 1" if overall_ur < 1 else "> 1"
        report_check.append([
            'Overall Design Status',
            overall_eq,
            NoEscape(rf'{round(overall_ur, 3):.3f}\text{{ {ur_text}}}'),
            final_status
        ])

        logger.info("DDCL-compliant design checks prepared successfully")

    except Exception as e:
        logger.error(f"Error preparing design checks: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")

    return report_check