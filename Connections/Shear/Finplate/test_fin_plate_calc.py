# TODO Update the following functions with appropriate UI inputs for fin plate connection.
# Danish, please delete this note once the function is updated.


def create_sample_ui_input_fp(fp_connection_id):
    input_dict = {'Member': {}, 'Load': {}, 'Bolt': {}, 'bolt': {}, 'Plate': {}, 'Weld': {}, 'weld': {}}

    if fp_connection_id == "FP_0":
        input_dict['Member'] = {
            'Connectivity': "Column flange-Beam web",
            'BeamSection': "MB 400",
            'ColumSection': "UC 254 x 254 x 167",
            'fu (MPa)': 410,
            'fy (MPa)': 250}
        input_dict['Load']['ShearForce (kN)'] = 120
        input_dict['Bolt'] = {
            'Diameter (mm)': 16,
            'Type': "Friction Grip Bolt",
            'Grade': "8.8"}
        input_dict['Plate'] = {
            'Thickness (mm)': 10,
            'Width (mm)': '',
            'Height (mm)': ''}
        input_dict['Weld']['Size (mm)'] = 8
        input_dict['bolt'] = {
            'bolt_hole_clrnce': 2.0,
            'slip_factor': 0.55,
            'bolt_fu': 800,
            'bolt_hole_type': 'Standard'}
        input_dict['weld'] = {
            'typeof_weld': 'Shop weld',
            'safety_factor': 1.25}
        input_dict['design'] = {'design_method': 'Limit State Design'}
        input_dict['detailing'] = {
            'typeof_edge': 'a - Sheared or hand flame cut',
            'min_edgend_dist': 1.7,
            'gap': 20}
    elif fp_connection_id == "FP_2":
        # TODO : update the following FP parameters
        input_dict['Member'] = {
            'Connectivity': "Column flange-Beam web",
            'BeamSection': "MB 400",
            'ColumSection': "UC 254 x 254 x 167",
            'fu (MPa)': 410,
            'fy (MPa)': 250}
        input_dict['Load']['ShearForce (kN)'] = 120
        input_dict['Bolt'] = {
            'Diameter (mm)': 16,
            'Type': "Friction Grip Bolt",
            'Grade': "8.8"}
        input_dict['Plate'] = {
            'Thickness (mm)': 10,
            'Width (mm)': '',
            'Height (mm)': ''}
        input_dict['Weld']['Size (mm)'] = 8
        input_dict['bolt'] = {
            'bolt_hole_clrnce': 2.0,
            'slip_factor': 0.55,
            'bolt_fu': 800,
            'bolt_hole_type': 'Standard'}
        input_dict['weld'] = {
            'typeof_weld': 'Shop weld',
            'safety_factor': 1.25}
        input_dict['design'] = {'design_method': 'Limit State Design'}
        input_dict['detailing'] = {
            'typeof_edge': 'a - Sheared or hand flame cut',
            'min_edgend_dist': 1.7,
            'gap': 20}
    elif fp_connection_id == "FP_3":
        input_dict['Member'] = {
            'Connectivity': "Column flange-Beam web",
            'BeamSection': "MB 400",
            'ColumSection': "UC 254 x 254 x 167",
            'fu (MPa)': 410,
            'fy (MPa)': 250}
        input_dict['Load']['ShearForce (kN)'] = 120
        input_dict['Bolt'] = {
            'Diameter (mm)': 16,
            'Type': "Friction Grip Bolt",
            'Grade': "8.8"}
        input_dict['Plate'] = {
            'Thickness (mm)': 10,
            'Width (mm)': '',
            'Height (mm)': ''}
        input_dict['Weld']['Size (mm)'] = 8
        input_dict['bolt'] = {
            'bolt_hole_clrnce': 2.0,
            'slip_factor': 0.55,
            'bolt_fu': 800,
            'bolt_hole_type': 'Standard'}
        input_dict['weld'] = {
            'typeof_weld': 'Shop weld',
            'safety_factor': 1.25}
        input_dict['design'] = {'design_method': 'Limit State Design'}
        input_dict['detailing'] = {
            'typeof_edge': 'a - Sheared or hand flame cut',
            'min_edgend_dist': 1.7,
            'gap': 20}
    elif fp_connection_id == "FP_4":
        input_dict['Member'] = {
            'Connectivity': "Column flange-Beam web",
            'BeamSection': "MB 400",
            'ColumSection': "UC 254 x 254 x 167",
            'fu (MPa)': 410,
            'fy (MPa)': 250}
        input_dict['Load']['ShearForce (kN)'] = 120
        input_dict['Bolt'] = {
            'Diameter (mm)': 16,
            'Type': "Friction Grip Bolt",
            'Grade': "8.8"}
        input_dict['Plate'] = {
            'Thickness (mm)': 10,
            'Width (mm)': '',
            'Height (mm)': ''}
        input_dict['Weld']['Size (mm)'] = 8
        input_dict['bolt'] = {
            'bolt_hole_clrnce': 2.0,
            'slip_factor': 0.55,
            'bolt_fu': 800,
            'bolt_hole_type': 'Standard'}
        input_dict['weld'] = {
            'typeof_weld': 'Shop weld',
            'safety_factor': 1.25}
        input_dict['design'] = {'design_method': 'Limit State Design'}
        input_dict['detailing'] = {
            'typeof_edge': 'a - Sheared or hand flame cut',
            'min_edgend_dist': 1.7,
            'gap': 20}
    elif fp_connection_id == "FP_6":
        input_dict['Member'] = {
            'Connectivity': "Column flange-Beam web",
            'BeamSection': "MB 400",
            'ColumSection': "UC 254 x 254 x 167",
            'fu (MPa)': 410,
            'fy (MPa)': 250}
        input_dict['Load']['ShearForce (kN)'] = 120
        input_dict['Bolt'] = {
            'Diameter (mm)': 16,
            'Type': "Friction Grip Bolt",
            'Grade': "8.8"}
        input_dict['Plate'] = {
            'Thickness (mm)': 10,
            'Width (mm)': '',
            'Height (mm)': ''}
        input_dict['Weld']['Size (mm)'] = 8
        input_dict['bolt'] = {
            'bolt_hole_clrnce': 2.0,
            'slip_factor': 0.55,
            'bolt_fu': 800,
            'bolt_hole_type': 'Standard'}
        input_dict['weld'] = {
            'typeof_weld': 'Shop weld',
            'safety_factor': 1.25}
        input_dict['design'] = {'design_method': 'Limit State Design'}
        input_dict['detailing'] = {
            'typeof_edge': 'a - Sheared or hand flame cut',
            'min_edgend_dist': 1.7,
            'gap': 20}
    return input_dict


def create_sample_ui_output_fp():
    output_dict = {'SeatAngle': {}, 'Bolt': {}}
    output_dict['SeatAngle'] = {
        "Length (mm)": 140,
        "Moment Demand (kNm)": 542,
        "Moment Capacity (kNm)": 916,
        "Shear Demand (kN/mm)": 100,
        "Shear Capacity (kN/mm)": 220,
        "Beam Shear Strength (kN/mm)": 303,
        "Top Angle": "60 60X6"
    }
    output_dict['Bolt'] = {
        "status": True,
        "Shear Capacity (kN)": 45.3,
        "Bearing Capacity (kN)": 96,
        "Capacity of Bolt (kN)": 45.3,
        "Bolt group capacity (kN)": 181.2,
        "No. of Bolts": 4,
        "No. of Row": 2,
        "No. of Column": 2,
        "Pitch Distance (mm)": 50,
        "Gauge Distance (mm)": 40,
        "End Distance (mm)": 50,
        "Edge Distance (mm)": 50,

        "bolt_fu": 400,
        "bolt_dia": 20,
        "k_b": 0.5,
        "beam_w_t": 7.7,
        "beam_fu": 410,
        "shearforce": 100,
        "hole_dia": 22
    }
    return output_dict
