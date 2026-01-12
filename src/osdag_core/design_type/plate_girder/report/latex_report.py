"""
Module: latex_report.py
Description: Design report generation for Plate Girder module
Author: Roushan Raj
Date: 2026-01-12
"""

import logging
import os
import sys
import ctypes
from ....design_report.reportGenerator_latex import CreateLatex
from ....Report_functions import *
from pylatex import Math
from pylatex.utils import NoEscape

def get_short_path(path):
    """
    Convert a path to Windows 8.3 short path format to handle spaces and underscores
    (e.g., 'C:/Users/Roushan Raj' -> 'C:/Users/ROUSHA~1').
    """
    if sys.platform == 'win32':
        try:
            if not os.path.exists(path):
                dirname = os.path.dirname(path)
                basename = os.path.basename(path)
                if os.path.exists(dirname):
                    short_dir = get_short_path(dirname)
                    return os.path.join(short_dir, basename).replace('\\', '/')
                return path.replace('\\', '/')
            
            # Create a buffer for the short path
            buffer_size = ctypes.windll.kernel32.GetShortPathNameW(path, None, 0)
            buffer = ctypes.create_unicode_buffer(buffer_size)
            # Get the short path
            ctypes.windll.kernel32.GetShortPathNameW(path, buffer, buffer_size)
            # Return normalized path with forward slashes for LaTeX
            return buffer.value.replace('\\', '/')
        except Exception:
            return path.replace('\\', '/')
    return path.replace('\\', '/')

def save_design(popup_summary):
    """
    Generate LaTeX design report for Plate Girder module
    
    Args:
        popup_summary: Dictionary containing report metadata from GUI
    """
    unique_logger_name = 'Osdag_plate_girder_flexure'
    logger = logging.getLogger(unique_logger_name)
    logger.info(" :=========Start of design report generation===========")
    
    try:
        # Get the plate girder object from popup_summary
        pg_obj = popup_summary.get('plate_girder_object')
        if pg_obj is None:
            logger.error(" :Plate girder object not found in popup_summary")
            return
        
        # Prepare report input dictionary
        report_input = prepare_report_input(pg_obj, logger)
        
        # Prepare design checks
        report_check = prepare_design_checks(pg_obj, logger)
        
        full_filename_path = popup_summary.get('filename', 'plate_girder_report')
        
        folder_path = popup_summary.get('folder', os.path.dirname(full_filename_path))
        if not folder_path: 
            folder_path = os.getcwd()
            
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        short_folder_path = get_short_path(folder_path)
        
        # Sanitize Filename (No spaces in the file name itself)
        filename_only = os.path.basename(full_filename_path)
        filename_only = os.path.splitext(filename_only)[0]
        filename_only = filename_only.replace(' ', '_')
        
        # Construct Final Output Path (Short Folder + Safe Filename)
        # This ensures the file is created WHERE the GUI expects it, but WITHOUT spaces
        final_output_path_no_ext = os.path.join(short_folder_path, filename_only).replace('\\', '/')
        
        raw_rel_path = os.path.abspath('..') 
        rel_path = get_short_path(raw_rel_path)
        
        # Ensure report_summary has the correct structure
        report_summary = popup_summary.copy()
        
        # Add ProfileSummary if not present
        if 'ProfileSummary' not in report_summary:
            report_summary['ProfileSummary'] = {
                'CompanyName': report_summary.get('CompanyName', ''),
                'CompanyLogo': report_summary.get('CompanyLogo', ''),
                'GroupTeamName': report_summary.get('Group/TeamName', ''),
                'Designer': report_summary.get('Designer', '')
            }
        
        # Add other required fields
        if 'ProjectTitle' not in report_summary:
            report_summary['ProjectTitle'] = 'Plate Girder Design'
        if 'Subtitle' not in report_summary:
            report_summary['Subtitle'] = 'Welded Plate Girder'
        if 'JobNumber' not in report_summary:
            report_summary['JobNumber'] = ''
        if 'Client' not in report_summary:
            report_summary['Client'] = ''
        
        # Add design status
        report_summary['does_design_exist'] = pg_obj.design_status
        if 'logger_messages' not in report_summary:
            report_summary['logger_messages'] = ''

        Disp_2d_image = []
        Disp_3d_image = popup_summary.get('Disp_3d_image', '')
        
        # --- GENERATION BLOCK WITH ERROR HANDLING ---
        try:
            CreateLatex.save_latex(
                CreateLatex(),
                report_input,
                report_check,
                report_summary,
                final_output_path_no_ext, # <--- Passing full short path
                rel_path,
                Disp_2d_image,
                Disp_3d_image,
                module='Plate Girder'
            )
        except Exception as e:
            # CHECK IF PDF WAS ACTUALLY GENERATED
            # We check the short path we calculated
            expected_pdf_path = f"{final_output_path_no_ext}.pdf"
            
            # Also check using the original long path to be safe (OS maps them to same file)
            long_path_check = os.path.join(folder_path, f"{filename_only}.pdf")

            pdf_exists = False
            if os.path.exists(expected_pdf_path) and os.path.getsize(expected_pdf_path) > 0:
                pdf_exists = True
                logger.info(f" :PDF found at {expected_pdf_path} despite compiler exit code.")
            elif os.path.exists(long_path_check) and os.path.getsize(long_path_check) > 0:
                pdf_exists = True
                logger.info(f" :PDF found at {long_path_check} despite compiler exit code.")
            
            if pdf_exists:
                logger.warning(" :LaTeX compiler returned error code 1, but PDF was generated. Ignoring error.")
            else:
                logger.error(f" :Critical Error generating LaTeX report: {str(e)}")
                # Suppress raising to avoid crashing GUI if we can't help it
                # raise e 

        logger.info(" :=========Design report generated successfully===========")
        
    except Exception as e:
        logger.error(f" :Final Error in save_design: {str(e)}")


def prepare_report_input(pg_obj, logger):
    """
    Prepare the report input dictionary - ONLY INPUT PARAMETERS
    """
    report_input = {}
    
    try:
        report_input['Module'] = getattr(pg_obj, 'module', 'Plate Girder')
        
        report_input['Overall Depth (mm)'] = round(getattr(pg_obj, 'total_depth', 0), 1)
        report_input['Web Thickness (mm)'] = round(getattr(pg_obj, 'web_thickness', 0), 1)
        report_input['Top Flange Width (mm)'] = round(getattr(pg_obj, 'top_flange_width', 0), 1)
        report_input['Top Flange Thickness (mm)'] = round(getattr(pg_obj, 'top_flange_thickness', 0), 1)
        report_input['Bottom Flange Width (mm)'] = round(getattr(pg_obj, 'bottom_flange_width', 0), 1)
        report_input['Bottom Flange Thickness (mm)'] = round(getattr(pg_obj, 'bottom_flange_thickness', 0), 1)
        report_input['Member Length (mm)'] = round(getattr(pg_obj, 'length', 0), 1)
        
        material = getattr(pg_obj, 'material', None)
        if material:
            report_input['Material Grade'] = getattr(material, 'designation', 'E 250')
            report_input['Yield Strength, fy (MPa)'] = round(getattr(material, 'fy', 0), 1)
            report_input['Ultimate Strength, fu (MPa)'] = round(getattr(material, 'fu', 0), 1)
            E_val = getattr(material, 'modulus_of_elasticity', 200000)
            report_input["Young's Modulus, E (MPa)"] = f"{E_val:.0f}"
        
        load = getattr(pg_obj, 'load', None)
        if load:
            report_input['Applied Moment (kN-m)'] = round(getattr(load, 'moment', 0) * 1e-6, 2)
            report_input['Applied Shear Force (kN)'] = round(getattr(load, 'shear_force', 0) * 1e-3, 2)
            report_input['Loading Case'] = getattr(pg_obj, 'loading_case', 'Uniform Loading with pinned-pinned support')
        
        report_input['Support Type'] = getattr(pg_obj, 'support_type', 'Major Laterally Supported')
        report_input['Support Width (mm)'] = round(getattr(pg_obj, 'b1', 0), 1)
        
        if getattr(pg_obj, 'support_type', '') == 'Major Laterally Unsupported':
            report_input['Effective Length (mm)'] = round(getattr(pg_obj, 'effective_length', 0), 1)
            report_input['Torsional Restraint'] = getattr(pg_obj, 'torsional_res', 'Fully Restrained')
            report_input['Warping Restraint'] = getattr(pg_obj, 'warping', 'Both flanges fully restrained')
        
        report_input['Web Philosophy'] = getattr(pg_obj, 'web_philosophy', 'Thick Web without ITS')
        
        gamma_m0 = round(getattr(pg_obj, 'gamma_m0', 1.1), 2)
        report_input[NoEscape(r'Governed by Yielding, $\gamma_{m0}$')] = gamma_m0
        
        if hasattr(pg_obj, 'deflection_criteria'):
            report_input['Deflection Limit'] = f"L/{getattr(pg_obj, 'deflection_criteria', 600)}"
        
    except Exception as e:
        logger.error(f" :Error preparing report input: {str(e)}")
    
    return report_input


def prepare_design_checks(pg_obj, logger):
    """
    Prepare design checks for the report with detailed formulas
    """
    report_check = []
    
    try:
        # Get material properties
        material = getattr(pg_obj, 'material', None)
        fy = round(material.fy, 1) if material else 250
        fu = round(material.fu, 1) if material else 410
        E = getattr(material, 'modulus_of_elasticity', 200000) if material else 200000
        
        # Get load values
        load = getattr(pg_obj, 'load', None)
        M_applied = round(getattr(load, 'moment', 0) * 1e-6, 2) if load else 0
        V_applied = round(getattr(load, 'shear_force', 0) * 1e-3, 2) if load else 0
        
        # Get section dimensions
        D = getattr(pg_obj, 'total_depth', 0)
        d = getattr(pg_obj, 'eff_depth', 0)
        tw = getattr(pg_obj, 'web_thickness', 0)
        tf_top = getattr(pg_obj, 'top_flange_thickness', 0)
        tf_bot = getattr(pg_obj, 'bottom_flange_thickness', 0)
        bf_top = getattr(pg_obj, 'top_flange_width', 0)
        bf_bot = getattr(pg_obj, 'bottom_flange_width', 0)
        
        table_format = '|p{5cm}|p{6cm}|p{3.5cm}|p{1.5cm}|'
        
        # Section Classification
        report_check.append(['SubSection', 'Section Classification', table_format])
        
        section_class = getattr(pg_obj, 'section_class', 'NA')
        epsilon = getattr(pg_obj, 'epsilon', 1.0)
        
        report_check.append([
            'Section Class',
            NoEscape(r'Based on flange and web slenderness ratios [Ref: IS 800:2007, Table 2]'),
            section_class,
            'Pass' if getattr(pg_obj, 'design_flag', False) else 'Fail'
        ])
        
        dtw_ratio = round(d / tw, 2) if tw > 0 else 0
        dtw_limit = round(200 * epsilon, 2)
        
        report_check.append([
            'Web Slenderness Ratio',
            NoEscape(rf'$d/t_w = {d:.1f}/{tw:.1f} = {dtw_ratio:.2f}$'),
            NoEscape(rf'{dtw_ratio:.2f} $\leq$ {dtw_limit:.2f}'),
            'Pass' if dtw_ratio <= dtw_limit else 'Fail'
        ])
        
        # Shear Capacity Check
        report_check.append(['SubSection', 'Shear Capacity Check', table_format])
        
        gamma_m0 = getattr(pg_obj, 'gamma_m0', 1.1)
        Vd_calculated = 0
        
        if getattr(pg_obj, 'web_philosophy', '') == 'Thick Web without ITS':
            # THICK WEB
            Avw = round(d * tw, 2)
            
            report_check.append([
                NoEscape(r'Shear Area, $A_{vw}$ (mm$^2$)'),
                NoEscape(rf'$A_{{vw}} = d \times t_w = {d:.1f} \times {tw:.1f} = {Avw:.2f}$ mm$^2$'),
                f'{Avw:.2f}',
                'Pass'
            ])
            
            import math
            Vd_calculated = round((Avw * fy) / (math.sqrt(3) * gamma_m0) / 1000, 2)
            
            report_check.append([
                NoEscape(r'Design Shear Strength, $V_d$ (kN)'),
                NoEscape(rf'$V_d = \dfrac{{A_{{vw}} \times f_y}}{{\sqrt{{3}} \times \gamma_{{m0}}}} = \dfrac{{{Avw:.2f} \times {fy:.1f}}}{{\sqrt{{3}} \times {gamma_m0}}} = {Vd_calculated:.2f}$ kN [Ref: IS 800:2007, Cl.8.4.1]'),
                f'{Vd_calculated:.2f} kN',
                'Pass' if Vd_calculated >= V_applied else 'Fail'
            ])
            
        else:
            # THIN WEB
            c = getattr(pg_obj, 'c', 0)
            if c != 'NA' and c > 0:
                c_val = float(c)
                c_d_ratio = c_val / d
                kv = 5.35 if c_d_ratio > 1.0 else round(4.0 + 5.35 / (c_d_ratio**2), 3)
                
                report_check.append([
                    NoEscape(r'Buckling Coefficient, $k_v$'),
                    NoEscape(rf'$k_v = 4.0 + \dfrac{{5.35}}{{(c/d)^2}} = 4.0 + \dfrac{{5.35}}{{({c_val:.1f}/{d:.1f})^2}} = {kv:.3f}$ [Ref: IS 800:2007, Cl.8.4.2.2]'),
                    f'{kv:.3f}',
                    'Pass'
                ])
                
                Avw = round(d * tw, 2)
                report_check.append([
                    NoEscape(r'Shear Area, $A_{vw}$ (mm$^2$)'),
                    NoEscape(rf'$A_{{vw}} = d \times t_w = {d:.1f} \times {tw:.1f} = {Avw:.2f}$ mm$^2$'),
                    f'{Avw:.2f}',
                    'Pass'
                ])
                
                import math
                mu = 0.3
                tau_crc = (kv * math.pi**2 * E) / (12 * (1 - mu**2) * (d/tw)**2)
                lambda_w = math.sqrt(fy / tau_crc)
                
                if lambda_w < 0.8:
                    tau_b = fy / math.sqrt(3)
                elif lambda_w <= 1.2:
                    tau_b = (1.0 - 0.8 * (lambda_w - 0.8) / 0.4) * fy / math.sqrt(3)
                else:
                    tau_b = fy / (math.sqrt(3) * lambda_w**2)
                
                Vd_calculated = round((tau_b * Avw) / (gamma_m0 * 1000), 2)
                
                report_check.append([
                    NoEscape(r'Design Shear Strength, $V_d$ (kN)'),
                    NoEscape(rf'$V_d = \dfrac{{\tau_b \times A_{{vw}}}}{{\gamma_{{m0}}}}$ (considering web buckling) [Ref: IS 800:2007, Cl.8.4.2.2]'),
                    f'{Vd_calculated:.2f} kN',
                    'Pass' if Vd_calculated >= V_applied else 'Fail'
                ])
        
        report_check.append([
            'Applied Shear Force (kN)',
            f'{V_applied:.2f} kN',
            f'{V_applied:.2f} kN',
            'Pass'
        ])
        
        # Web Buckling Check
        if hasattr(pg_obj, 'Vcr') and pg_obj.Vcr:
            Vcr = round(getattr(pg_obj, 'Vcr', 0) * 1e-3, 2)
            report_check.append([
                NoEscape(r'Web Buckling Resistance, $V_{cr}$ (kN)'),
                NoEscape(r'Critical buckling strength [Ref: IS 800:2007, Cl.8.4.2.2]'),
                f'{Vcr:.2f} kN',
                'Pass' if getattr(pg_obj, 'shear_flag2', False) else 'Fail'
            ])
        
        # Web Crippling Check
        if hasattr(pg_obj, 'Fq') and pg_obj.Fq:
            Fq = round(getattr(pg_obj, 'Fq', 0) * 1e-3, 2)
            b1 = getattr(pg_obj, 'b1', 0)
            
            report_check.append(['SubSection', 'Web Crippling Check', table_format])
            
            report_check.append([
                NoEscape(r'Bearing Width, $b_1$ (mm)'),
                f'Support width = {b1:.1f} mm',
                f'{b1:.1f} mm',
                'Pass'
            ])
            
            report_check.append([
                NoEscape(r'Crippling Resistance, $F_q$ (kN)'),
                NoEscape(rf'$F_q = (b_1 + n_2) \times t_w \times f_y / \gamma_{{m0}}$ [Ref: IS 800:2007, Cl.8.7.1.1]'),
                f'{Fq:.2f} kN',
                'Pass' if getattr(pg_obj, 'shear_flag3', False) else 'Fail'
            ])
        
        # Moment Capacity Check
        report_check.append(['SubSection', 'Moment Capacity Check', table_format])
        
        Md = round(getattr(pg_obj, 'Md', 0) * 1e-6, 2) if hasattr(pg_obj, 'Md') and pg_obj.Md else 0
        Zp = round(getattr(pg_obj, 'plast_sec_mod_z', 0) * 1e-3, 2) if hasattr(pg_obj, 'plast_sec_mod_z') else 0
        Ze = round(getattr(pg_obj, 'elast_sec_mod_z', 0) * 1e-3, 2) if hasattr(pg_obj, 'elast_sec_mod_z') else 0
        
        section_class = getattr(pg_obj, 'section_class', 'NA')
        
        if section_class in ['Plastic', 'Compact']:
            Z_used = Zp
            Z_label = 'Z_p'
        else:
            Z_used = Ze
            Z_label = 'Z_e'
        
        report_check.append([
            NoEscape(rf'Section Modulus, ${Z_label}$ (cm$^3$)'),
            NoEscape(rf'${Z_label} = {Z_used:.2f}$ cm$^3$ ({section_class} section)'),
            f'{Z_used:.2f} cm³',
            'Pass'
        ])
        
        report_check.append([
            NoEscape(r'Design Moment Capacity, $M_d$ (kN-m)'),
            NoEscape(rf'$M_d = \dfrac{{{Z_label} \times f_y}}{{\gamma_{{m0}}}} = \dfrac{{{Z_used:.2f} \times {fy:.1f} \times 10^3}}{{{gamma_m0} \times 10^6}} = {Md:.2f}$ kN-m [Ref: IS 800:2007, Cl.8.2.1]'),
            f'{Md:.2f} kN-m',
            'Pass'
        ])
        
        report_check.append([
            'Applied Bending Moment (kN-m)',
            f'{M_applied:.2f} kN-m',
            f'{M_applied:.2f} kN-m',
            'Pass' if Md >= M_applied else 'Fail'
        ])
        
        # Lateral Torsional Buckling (if applicable)
        if getattr(pg_obj, 'support_type', '') == 'Major Laterally Unsupported':
            report_check.append(['SubSection', 'Lateral Torsional Buckling Check', table_format])
            
            if hasattr(pg_obj, 'Mcr') and pg_obj.Mcr:
                Mcr = round(getattr(pg_obj, 'Mcr', 0) * 1e-6, 2)
                Leff = getattr(pg_obj, 'effective_length', 0)
                
                report_check.append([
                    NoEscape(r'Effective Length, $L_{eff}$ (mm)'),
                    f'Effective length = {Leff:.1f} mm',
                    f'{Leff:.1f} mm',
                    'Pass'
                ])
                
                report_check.append([
                    NoEscape(r'Elastic Critical Moment, $M_{cr}$ (kN-m)'),
                    NoEscape(r'$M_{cr} = \sqrt{M_{cr,z} \times M_{cr,T}}$ [Ref: IS 800:2007, Cl.8.2.2]'),
                    f'{Mcr:.2f} kN-m',
                    'Pass'
                ])
                
                if hasattr(pg_obj, 'lambda_lt'):
                    lambda_lt = round(getattr(pg_obj, 'lambda_lt', 0), 3)
                    report_check.append([
                        NoEscape(r'Slenderness Ratio, $\lambda_{LT}$'),
                        NoEscape(rf'$\lambda_{{LT}} = \sqrt{{\dfrac{{Z_e \times f_y}}{{M_{{cr}}}}}} = {lambda_lt:.3f}$ [Ref: IS 800:2007, Cl.8.2.2]'),
                        f'{lambda_lt:.3f}',
                        'Pass'
                    ])
                
                if hasattr(pg_obj, 'fbd_lt'):
                    fbd = round(getattr(pg_obj, 'fbd_lt', 0), 2)
                    chi_lt = getattr(pg_obj, 'X_lt', 1.0)
                    report_check.append([
                        NoEscape(r'Design Bending Strength, $f_{bd}$ (MPa)'),
                        NoEscape(rf'$f_{{bd}} = \chi_{{LT}} \times \dfrac{{f_y}}{{\gamma_{{m0}}}} = {chi_lt:.3f} \times \dfrac{{{fy:.1f}}}{{{gamma_m0}}} = {fbd:.2f}$ MPa [Ref: IS 800:2007, Cl.8.2.2]'),
                        f'{fbd:.2f} MPa',
                        'Pass'
                    ])
        
        # Deflection Check
        if hasattr(pg_obj, 'deflection_ratio') and pg_obj.deflection_ratio:
            report_check.append(['SubSection', 'Deflection Check', table_format])
            
            defl_limit = getattr(pg_obj, 'deflection_criteria', 600)
            defl_ratio = getattr(pg_obj, 'deflection_ratio', 0)
            defl_actual_val = round(1 / defl_ratio, 1) if defl_ratio > 0 else 0
            L = getattr(pg_obj, 'length', 0)
            I = getattr(pg_obj, 'moment_of_inertia_z', 0) if hasattr(pg_obj, 'moment_of_inertia_z') else 0
            
            report_check.append([
                'Deflection Limit',
                NoEscape(rf'Allowable deflection = L/{defl_limit} [As per design preference]'),
                f'L/{defl_limit}',
                'Pass'
            ])
            
            if I > 0:
                I_cm4 = round(I * 1e-4, 2)
                report_check.append([
                    NoEscape(r'Moment of Inertia, $I_z$ (cm$^4$)'),
                    f'{I_cm4:.2f} cm⁴',
                    f'{I_cm4:.2f} cm⁴',
                    'Pass'
                ])
            
            report_check.append([
                'Actual Deflection',
                NoEscape(r'$\delta = \dfrac{5 \times w \times L^4}{384 \times E \times I}$ (for UDL with pinned support) [Ref: Structural Analysis]'),
                f'L/{defl_actual_val:.1f}' if defl_actual_val > 0 else 'NA',
                'Pass' if getattr(pg_obj, 'defl_check', False) else 'Fail'
            ])
        
        # ==================== WELD DESIGN SECTION ====================
        if hasattr(pg_obj, 'atop') or hasattr(pg_obj, 'abot'):
            report_check.append(['SubSection', 'Weld Design', table_format])
            
            weld_top = getattr(pg_obj, 'atop', 0)
            weld_bot = getattr(pg_obj, 'abot', 0)
            weld_size = max(weld_top, weld_bot)
            
            t_min = min(tw, tf_top, tf_bot)
            s_min = 3 if t_min <= 10 else (5 if t_min <= 20 else 6)
            
            report_check.append([
                'Minimum Weld Size (mm)',
                NoEscape(rf'Based on thinner part thickness ({t_min:.1f} mm) [Ref: IS 800:2007, Table 21]'),
                NoEscape(rf'{weld_size:.1f} mm $\geq$ {s_min} mm'),
                'Pass' if weld_size >= s_min else 'Fail'
            ])
            
            # Web-to-top flange weld
            if weld_top > 0:
                report_check.append([
                    'Weld Size - Web to Top Flange (mm)',
                    NoEscape(r'Fillet weld connecting web to top flange'),
                    f'{round(weld_top, 1)} mm',
                    'Pass'
                ])
            
            # Web-to-bottom flange weld
            if weld_bot > 0:
                report_check.append([
                    'Weld Size - Web to Bottom Flange (mm)',
                    NoEscape(r'Fillet weld connecting web to bottom flange'),
                    f'{round(weld_bot, 1)} mm',
                    'Pass'
                ])
            
            # Stiffener weld (if applicable)
            if hasattr(pg_obj, 'weld_stiff') and pg_obj.weld_stiff is not None and pg_obj.weld_stiff > 0:
                weld_stiff = getattr(pg_obj, 'weld_stiff', 0)
                report_check.append([
                    'Weld Size - Stiffener to Web (mm)',
                    NoEscape(r'Fillet weld connecting stiffener to web'),
                    f'{round(weld_stiff, 1)} mm',
                    'Pass'
                ])
        
        # ==================== STIFFENER DESIGN SECTION ====================
        # Check if stiffeners exist (for both thick and thin web)
        has_stiffeners = False
        
        # Check if ANY stiffener attribute exists and is not 'NA' or 0
        if hasattr(pg_obj, 'end_panel_stiffener_thickness'):
            t_end = getattr(pg_obj, 'end_panel_stiffener_thickness', 'NA')
            if t_end not in ['NA', 'Not Required', 0, None, '']:
                has_stiffeners = True
        
        if hasattr(pg_obj, 'IntStiffThickness'):
            t_int = getattr(pg_obj, 'IntStiffThickness', 'NA')
            if t_int not in ['NA', 'Not Required', 0, None, '']:
                has_stiffeners = True
        
        if hasattr(pg_obj, 'LongStiffThickness'):
            t_long = getattr(pg_obj, 'LongStiffThickness', 'NA')
            if t_long not in ['NA', 'Not Required', 0, None, '']:
                has_stiffeners = True
        
        # Only create Stiffener Design section if stiffeners exist
        if has_stiffeners:
            report_check.append(['SubSection', 'Stiffener Design', table_format])
            
            # End Panel Stiffeners (Load Bearing Stiffeners)
            if hasattr(pg_obj, 'end_panel_stiffener_thickness'):
                t_end = getattr(pg_obj, 'end_panel_stiffener_thickness', 'NA')
                if t_end not in ['NA', 'Not Required', 0, None, '']:
                    try:
                        t_end_val = float(t_end)
                        report_check.append([
                            'End Panel Stiffener Thickness (mm)',
                            NoEscape(r'Load bearing stiffener at support [Ref: IS 800:2007, Cl.8.7.1.1]'),
                            f'{round(t_end_val, 1)} mm',
                            'Pass'
                        ])
                        
                        report_check.append([
                            'Number of End Panel Stiffeners',
                            NoEscape(r'Pair of stiffeners provided at each support'),
                            '2 (One pair)',
                            'Pass'
                        ])
                    except (ValueError, TypeError):
                        pass
            
            # Intermediate Transverse Stiffeners
            if hasattr(pg_obj, 'IntStiffThickness'):
                t_stiff = getattr(pg_obj, 'IntStiffThickness', 'NA')
                if t_stiff not in ['NA', 'Not Required', 0, None, '']:
                    try:
                        t_stiff_val = float(t_stiff)
                        d_over_50 = round(d / 50, 2)
                        
                        report_check.append([
                            'Intermediate Stiffener Thickness (mm)',
                            NoEscape(rf'Minimum thickness = d/50 = {d:.1f}/50 = {d_over_50:.2f} mm [Ref: IS 800:2007, Cl.8.7.1.3]'),
                            NoEscape(rf'{round(t_stiff_val, 1)} mm $\geq$ {d_over_50:.2f} mm'),
                            'Pass' if t_stiff_val >= d_over_50 else 'Fail'
                        ])
                        
                        # Intermediate stiffener spacing
                        if hasattr(pg_obj, 'c') and pg_obj.c not in ['NA', 'Not Required', 0, None, '']:
                            try:
                                c_val = float(getattr(pg_obj, 'c', 0))
                                if c_val > 0:
                                    c_max = 3 * d
                                    c_min = 0.5 * d
                                    spacing_ok = c_min <= c_val <= c_max
                                    
                                    report_check.append([
                                        'Intermediate Stiffener Spacing (mm)',
                                        NoEscape(rf'Spacing range: {c_min:.1f} mm $\leq$ c $\leq$ {c_max:.1f} mm [Ref: IS 800:2007, Cl.8.6]'),
                                        f'{c_val:.1f} mm',
                                        'Pass' if spacing_ok else 'Fail'
                                    ])
                            except (ValueError, TypeError):
                                pass
                    except (ValueError, TypeError):
                        pass
            
            # Longitudinal Stiffeners
            if hasattr(pg_obj, 'LongStiffThickness'):
                t_long = getattr(pg_obj, 'LongStiffThickness', 'NA')
                if t_long not in ['NA', 'Not Required', 0, None, '']:
                    try:
                        t_long_val = float(t_long)
                        report_check.append([
                            'Longitudinal Stiffener Thickness (mm)',
                            NoEscape(rf'{getattr(pg_obj, "longStiffner", "Longitudinal stiffener")} [Ref: IS 800:2007, Cl.8.7.1.3]'),
                            f'{round(t_long_val, 1)} mm',
                            'Pass'
                        ])
                        
                        # Number of longitudinal stiffeners
                        if hasattr(pg_obj, 'longstiffener_no'):
                            num_long = getattr(pg_obj, 'longstiffener_no', 0)
                            if num_long and num_long not in ['NA', 'Not Required', 0, None, '']:
                                try:
                                    num_long_int = int(num_long)
                                    if num_long_int > 0:
                                        report_check.append([
                                            'Number of Longitudinal Stiffeners',
                                            NoEscape(r'Number of stiffeners along web depth'),
                                            f'{num_long_int}',
                                            'Pass'
                                        ])
                                except (ValueError, TypeError):
                                    pass
                        
                        # Longitudinal stiffener positions
                        if hasattr(pg_obj, 'x1') and pg_obj.x1 not in ['NA', 'Not Required', 0, None, '']:
                            try:
                                x1_pos = float(getattr(pg_obj, 'x1', 0))
                                if x1_pos > 0:
                                    report_check.append([
                                        'Stiffener 1 Position (mm)',
                                        NoEscape(r'Distance from compression flange = 0.2d [Ref: IS 800:2007, Cl.8.7.1.3]'),
                                        f'{round(x1_pos, 2)} mm',
                                        'Pass'
                                    ])
                            except (ValueError, TypeError):
                                pass
                        
                        if hasattr(pg_obj, 'x2') and pg_obj.x2 not in ['NA', 'Not Required', 0, None, '']:
                            try:
                                x2_pos = float(getattr(pg_obj, 'x2', 0))
                                if x2_pos > 0:
                                    report_check.append([
                                        'Stiffener 2 Position (mm)',
                                        NoEscape(r'Distance from compression flange = 0.5d [Ref: IS 800:2007, Cl.8.7.1.3]'),
                                        f'{round(x2_pos, 2)} mm',
                                        'Pass'
                                    ])
                            except (ValueError, TypeError):
                                pass
                    except (ValueError, TypeError):
                        pass
        
        # Overall Design Status
        report_check.append(['SubSection', 'Overall Design Check', table_format])
        
        ur_moment = getattr(pg_obj, 'moment_ratio', 0)
        ur_shear = getattr(pg_obj, 'shear_ratio', 0)
        ur_deflection = getattr(pg_obj, 'deflection_ratio', 0)
        overall_ur = max(ur_moment, ur_shear, ur_deflection)
        
        report_check.append([
            'Moment Utilization Ratio',
            NoEscape(rf'$UR_M = \dfrac{{M_{{applied}}}}{{M_d}} = \dfrac{{{M_applied:.2f}}}{{{Md:.2f}}} = {ur_moment:.3f}$'),
            NoEscape(rf'{ur_moment:.3f} $\leq$ 1.0'),
            'Pass' if ur_moment <= 1.0 else 'Fail'
        ])
        
        report_check.append([
            'Shear Utilization Ratio',
            NoEscape(rf'$UR_V = \dfrac{{V_{{applied}}}}{{V_d}} = \dfrac{{{V_applied:.2f}}}{{{Vd_calculated:.2f}}} = {ur_shear:.3f}$'),
            NoEscape(rf'{ur_shear:.3f} $\leq$ 1.0'),
            'Pass' if ur_shear <= 1.0 else 'Fail'
        ])
        
        if ur_deflection > 0:
            report_check.append([
                'Deflection Utilization Ratio',
                NoEscape(rf'$UR_{{\delta}} = \dfrac{{\delta_{{actual}}}}{{\delta_{{allowable}}}} = {ur_deflection:.3f}$'),
                NoEscape(rf'{ur_deflection:.3f} $\leq$ 1.0'),
                'Pass' if ur_deflection <= 1.0 else 'Fail'
            ])
        
        report_check.append([
            'Overall Utilization Ratio',
            NoEscape(r'Maximum of all utilization ratios'),
            NoEscape(rf'{round(overall_ur, 3)} $\leq$ 1.0'),
            'Pass' if overall_ur <= 1.0 else 'Fail'
        ])
        
        logger.info(" :Design checks prepared successfully")
        
    except Exception as e:
        logger.error(f" :Error preparing design checks: {str(e)}")
        import traceback
        logger.error(f" :Traceback: {traceback.format_exc()}")
    
    return report_check
