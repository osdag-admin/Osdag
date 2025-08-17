import sqlite3
from design_type.connection.fin_plate_connection import FinPlateConnection
from utils.common.Common import connectdb, connectdb1, MaterialValidator, VALUES_CONN, VALUES_TYP, VALUES_GRD_CUSTOMIZED, VALUES_PLATETHK_CUSTOMIZED
from utils.common.component import PATH_TO_DATABASE

# function to get ultimate (fu) and yield (fy) strengths for a material grade
def get_fy_fu(material_grade, thickness=None):
    """return fu and fy for a material grade, considering thickness for plates."""
    # handle standard material grade e 250 (fe 410 w)a
    if material_grade == "E 250 (Fe 410 W)A":
        # if no thickness provided, return default fu, fy
        if thickness is None:
            return 410, 250
        else:
            # convert thickness to float for comparison
            thickness = float(thickness)
            # return fu, fy based on thickness ranges
            if thickness <= 20:
                return 410, 250, 250, 250
            elif thickness <= 40:
                return 410, 250, 240, 240
            else:
                return 410, 250, 240, 230
    # handle custom material grades starting with "cus_"
    elif material_grade.startswith("Cus_"):
        validator = MaterialValidator(material_grade)
        # check if custom material is valid
        if validator.is_valid_custom():
            parts = material_grade.split('_')
            # extract fu and fy from custom grade name
            fu, fy = float(parts[-1]), float(parts[-2])
            # return fu, fy based on thickness
            if thickness is None:
                return fu, fy
            else:
                return fu, fy, fy, fy
    # default fu, fy if material grade is unknown
    return 410, 250

# function to mimic gui input for fin plate connection
def mimic_fin_plate_inputs(test_case_data):
    """mimic gui input collection for fin plate connection, creating a design_dictionary."""
    # copy input data to avoid modifying original
    design_dictionary = test_case_data.copy()
    
    # connect to database to fetch valid values
    conn = sqlite3.connect(PATH_TO_DATABASE)
    cursor = conn.cursor()
    
    # define input fields for fin plate connection
    input_fields = [
        {"key": "KEY_MODULE", "type": "TYPE_MODULE", "value": "Fin Plate Connection"},
        {"key": "KEY_CONN", "type": "TYPE_COMBOBOX", "values": VALUES_CONN},
        # fetch beams or columns based on connection type
        {"key": "KEY_SUPTNGSEC", "type": "TYPE_COMBOBOX", 
         "values": connectdb("Beams") if test_case_data.get("KEY_CONN") == "Beam-Beam" else connectdb("Columns")},
        {"key": "KEY_SUPTNGSEC_MATERIAL", "type": "TYPE_COMBOBOX", "values": connectdb("Material")},
        {"key": "KEY_SUPTDSEC", "type": "TYPE_COMBOBOX", "values": connectdb("Beams")},
        {"key": "KEY_SUPTDSEC_MATERIAL", "type": "TYPE_COMBOBOX", "values": connectdb("Material")},
        {"key": "KEY_SHEAR", "type": "TYPE_TEXTBOX", "validator": "Int Validator"},
        {"key": "KEY_AXIAL", "type": "TYPE_TEXTBOX", "validator": "Int Validator"},
        {"key": "KEY_D", "type": "TYPE_COMBOBOX_CUSTOMIZED", "values": connectdb1()},
        {"key": "KEY_TYP", "type": "TYPE_COMBOBOX", "values": VALUES_TYP},
        {"key": "KEY_GRD", "type": "TYPE_COMBOBOX_CUSTOMIZED", "values": VALUES_GRD_CUSTOMIZED},
        {"key": "KEY_PLATETHK", "type": "TYPE_COMBOBOX_CUSTOMIZED", "values": VALUES_PLATETHK_CUSTOMIZED},
        {"key": "KEY_CONNECTOR_MATERIAL", "type": "TYPE_COMBOBOX", "values": connectdb("Material")},
    ]
    
    # define design preference fields
    design_pref_fields = [
        {"key": "KEY_DP_BOLT_TYPE", "type": "TYPE_COMBOBOX", "values": ["Pretensioned", "Non pre-tensioned"]},
        {"key": "KEY_DP_BOLT_HOLE_TYPE", "type": "TYPE_COMBOBOX", "values": ["Standard", "Over-sized"]},
        {"key": "KEY_DP_BOLT_SLIP_FACTOR", "type": "TYPE_TEXTBOX", "value": "0.3"},
        {"key": "KEY_DP_WELD_FAB", "type": "TYPE_COMBOBOX", "values": ["Shop Weld", "Field Weld"]},
        {"key": "KEY_DP_WELD_MATERIAL_G_O", "type": "TYPE_TEXTBOX", "value": "410"},
        {"key": "KEY_DP_DETAILING_EDGE_TYPE", "type": "TYPE_COMBOBOX", 
         "values": ["Sheared or hand flame cut", "Rolled, machine-flame cut, sawn and planed"]},
        {"key": "KEY_DP_DETAILING_GAP", "type": "TYPE_TEXTBOX", "value": "10"},
        {"key": "KEY_DP_DETAILING_CORROSIVE_INFLUENCES", "type": "TYPE_COMBOBOX", "values": ["No", "Yes"]},
        {"key": "KEY_DP_DESIGN_METHOD", "type": "TYPE_COMBOBOX", "values": ["Limit State Design"]},
    ]
    
    # validate each input field
    for field in input_fields:
        key = field["key"]
        input_type = field["type"]
        valid_values = field.get("values", [])
        
        value = design_dictionary.get(key)
        
        # check combobox values are valid
        if input_type == "TYPE_COMBOBOX":
            if value not in valid_values and value not in ["", None]:
                raise ValueError(f"Invalid value '{value}' for {key}. Valid: {valid_values}")
        # check customized combobox values
        elif input_type == "TYPE_COMBOBOX_CUSTOMIZED":
            if isinstance(valid_values, list) and valid_values and isinstance(valid_values[0], list):
                valid_values = valid_values[0]
            if value not in valid_values and value not in ["", None]:
                raise ValueError(f"Invalid value '{value}' for {key}. Valid: {valid_values}")
        # validate textbox inputs as integers
        elif input_type == "TYPE_TEXTBOX" and field.get("validator") == "Int Validator":
            try:
                if value not in ["", None]:
                    int_value = int(value)
                    if int_value <= 0:
                        print(f"Warning: {key} must be positive. Using default: 1")
                        design_dictionary[key] = "1"
                else:
                    design_dictionary[key] = ""
            except ValueError:
                print(f"Error: Invalid {key}: '{value}'. Using default: 1")
                design_dictionary[key] = "1"
        
        # validate custom material grades
        if key.endswith("_MATERIAL") and value and value.startswith("Cus_"):
            validator = MaterialValidator(value)
            if not validator.is_valid_custom():
                print(f"Warning: Invalid custom material '{value}' for {key}. Using default: E 250 (Fe 410 W)A")
                design_dictionary[key] = "E 250 (Fe 410 W)A"
        
        # convert specific keys to float or string
        if key == "KEY_GRD":
            design_dictionary[key] = float(value) if value else 8.8
        elif key == "KEY_D":
            design_dictionary[key] = float(value) if value else 20.0
        else:
            design_dictionary[key] = str(value) if value is not None else ""
    
    # validate design preference fields
    for field in design_pref_fields:
        key = field["key"]
        input_type = field["type"]
        valid_values = field.get("values", [])
        default_value = field.get("value", valid_values[0] if valid_values else "")
        
        value = design_dictionary.get(key, default_value)
        
        # check design preference combobox values
        if input_type == "TYPE_COMBOBOX":
            if value not in valid_values:
                print(f"Warning: Invalid value '{value}' for {key}. Using default: {default_value}")
                design_dictionary[key] = default_value
        # validate textbox inputs as floats
        elif input_type == "TYPE_TEXTBOX":
            try:
                float(value)
            except ValueError:
                print(f"Warning: Invalid value '{value}' for {key}. Using default: {default_value}")
                design_dictionary[key] = default_value
    
    # add compatibility keys for legacy support
    compatibility_keys = {
        "Connectivity *": "KEY_CONN",
        "Member.Supporting_Section.Designation" : "KEY_SUPTNGSEC",
        "Member.Supported_Section.Designation": "KEY_SUPTDSEC",
        "Member.Supporting_Section.Material": "KEY_SUPTNGSEC_MATERIAL",
        "Member.Supported_Section.Material": "KEY_SUPTDSEC_MATERIAL",
        "Load.Shear": "KEY_SHEAR",
        "Load.Axial": "KEY_AXIAL",
        "Bolt.Diameter": "KEY_D",
        "Bolt.Grade": "KEY_GRD",
        "Bolt.Type": "KEY_TYP",
        "Bolt.Bolt_Hole_Type": "KEY_DP_BOLT_HOLE_TYPE",
        "Bolt.TensionType": "KEY_DP_BOLT_TYPE",
        "Detailing.Bolt_Slip_Factor": "KEY_DP_BOLT_SLIP_FACTOR",
        "Detailing.Edge_type": "KEY_DP_DETAILING_EDGE_TYPE",
        "Detailing.Corrosive_Influences": "KEY_DP_DETAILING_CORROSIVE_INFLUENCES",
        "Detailing.Gap": "KEY_DP_DETAILING_GAP",
        "Design.Method": "KEY_DP_DESIGN_METHOD",
        "Material": "KEY_CONNECTOR_MATERIAL",
        "Module": "KEY_MODULE",
        "Plate.Thickness": "KEY_PLATETHK",
        "Plate.Material_Grade": "KEY_CONNECTOR_MATERIAL",
        "Connector.Material": "KEY_CONNECTOR_MATERIAL",
        "Shear_Force": "KEY_SHEAR",
        "Axial_Force": "KEY_AXIAL",
        "Weld.Material": "KEY_DP_WELD_MATERIAL_G_O",
        "Weld.Material_Grade_OverWrite": "KEY_DP_WELD_MATERIAL_G_O",
        "Weld.Fab": "KEY_DP_WELD_FAB",
        "Weld.Fabrication": "KEY_DP_WELD_FAB",
        "Weld.Fu": "KEY_DP_WELD_MATERIAL_G_O",
    }
    
    # map compatibility keys to design dictionary
    for dest_key, src_key in compatibility_keys.items():
        design_dictionary[dest_key] = design_dictionary.get(src_key, "")
    
    # calculate material properties for supporting, supported, and connector
    material_keys = [
        ("KEY_SUPTNGSEC_FU", "KEY_SUPTNGSEC_FY", "KEY_SUPTNGSEC_MATERIAL", None),
        ("KEY_SUPTDSEC_FU", "KEY_SUPTDSEC_FY", "KEY_SUPTDSEC_MATERIAL", None),
        ("KEY_CONNECTOR_FU", "KEY_CONNECTOR_FY_20", "KEY_CONNECTOR_MATERIAL", design_dictionary.get('KEY_PLATETHK', 10)),
    ]
    
    # assign fu and fy based on material and thickness
    for fu_key, fy_key, mat_key, thickness in material_keys:
        material = design_dictionary.get(mat_key, "E 250 (Fe 410 W)A")
        if thickness is None:
            fu, fy = get_fy_fu(material)
            design_dictionary[fu_key] = str(fu)
            design_dictionary[fy_key] = str(fy)
        else:
            fu, fy_20, fy_20_40, fy_40 = get_fy_fu(material, float(thickness))
            design_dictionary[fu_key] = str(fu)
            design_dictionary[fy_key] = str(fy_20)
            design_dictionary['KEY_CONNECTOR_FY_20_40'] = str(fy_20_40)
            design_dictionary['KEY_CONNECTOR_FY_40'] = str(fy_40)
    
    # close database connection
    conn.close()
    return design_dictionary

# function to test fin plate input mimicry with four test cases
def test_mimic_fin_plate_inputs():
    """test the mimicry function with four osi file test cases."""
    # define four test cases based on osi files
    test_cases = [
        # finplatetest1.osi
        {
            "KEY_MODULE": "Fin Plate Connection",
            "KEY_CONN": "Column Flange-Beam Web",
            "KEY_SUPTNGSEC": "HB 300",
            "KEY_SUPTNGSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SUPTDSEC": "MB 200",
            "KEY_SUPTDSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SHEAR": "5",
            "KEY_AXIAL": "",
            "KEY_D": "20",
            "KEY_GRD": "10.9",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "10",
            "KEY_CONNECTOR_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_DP_BOLT_TYPE": "Pretensioned",
            "KEY_DP_BOLT_HOLE_TYPE": "Standard",
            "KEY_DP_BOLT_SLIP_FACTOR": "0.3",
            "KEY_DP_WELD_FAB": "Shop Weld",
            "KEY_DP_WELD_MATERIAL_G_O": "410",
            "KEY_DP_DETAILING_EDGE_TYPE": "Sheared or hand flame cut",
            "KEY_DP_DETAILING_GAP": "10",
            "KEY_DP_DETAILING_CORROSIVE_INFLUENCES": "No",
            "KEY_DP_DESIGN_METHOD": "Limit State Design"
        },
        # finplatetest2.osi
        {
            "KEY_MODULE": "Fin Plate Connection",
            "KEY_CONN": "Column Web-Beam Web",
            "KEY_SUPTNGSEC": "HB 200",
            "KEY_SUPTNGSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SUPTDSEC": "MB 200",
            "KEY_SUPTDSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SHEAR": "5",
            "KEY_AXIAL": "",
            "KEY_D": "20",
            "KEY_GRD": "8.8",
            "KEY_TYP": "Friction Grip Bolt",
            "KEY_PLATETHK": "16",
            "KEY_CONNECTOR_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_DP_BOLT_TYPE": "Pretensioned",
            "KEY_DP_BOLT_HOLE_TYPE": "Standard",
            "KEY_DP_BOLT_SLIP_FACTOR": "0.3",
            "KEY_DP_WELD_FAB": "Shop Weld",
            "KEY_DP_WELD_MATERIAL_G_O": "410",
            "KEY_DP_DETAILING_EDGE_TYPE": "Sheared or hand flame cut",
            "KEY_DP_DETAILING_GAP": "10",
            "KEY_DP_DETAILING_CORROSIVE_INFLUENCES": "No",
            "KEY_DP_DESIGN_METHOD": "Limit State Design"
        },
        # finplatetest3.osi
        {
            "KEY_MODULE": "Fin Plate Connection",
            "KEY_CONN": "Beam-Beam",
            "KEY_SUPTNGSEC": "MB 200",
            "KEY_SUPTNGSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SUPTDSEC": "MB 300",
            "KEY_SUPTDSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SHEAR": "50",
            "KEY_AXIAL": "8",
            "KEY_D": "20",
            "KEY_GRD": "8.8",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "12",
            "KEY_CONNECTOR_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_DP_BOLT_TYPE": "Pretensioned",
            "KEY_DP_BOLT_HOLE_TYPE": "Standard",
            "KEY_DP_BOLT_SLIP_FACTOR": "0.3",
            "KEY_DP_WELD_FAB": "Shop Weld",
            "KEY_DP_WELD_MATERIAL_G_O": "410",
            "KEY_DP_DETAILING_EDGE_TYPE": "Sheared or hand flame cut",
            "KEY_DP_DETAILING_GAP": "10",
            "KEY_DP_DETAILING_CORROSIVE_INFLUENCES": "No",
            "KEY_DP_DESIGN_METHOD": "Limit State Design"
        },
        # finplatetest4.osi
        {
            "KEY_MODULE": "Fin Plate Connection",
            "KEY_CONN": "Beam-Beam",
            "KEY_SUPTNGSEC": "MB 300",
            "KEY_SUPTNGSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SUPTDSEC": "MB 200",
            "KEY_SUPTDSEC_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_SHEAR": "50",
            "KEY_AXIAL": "8",
            "KEY_D": "20",
            "KEY_GRD": "8.8",
            "KEY_TYP": "Bearing Bolt",
            "KEY_PLATETHK": "20",
            "KEY_CONNECTOR_MATERIAL": "E 250 (Fe 410 W)A",
            "KEY_DP_BOLT_TYPE": "Non pre-tensioned",
            "KEY_DP_BOLT_HOLE_TYPE": "Over-sized",
            "KEY_DP_BOLT_SLIP_FACTOR": "0.3",
            "KEY_DP_WELD_FAB": "Field Weld",
            "KEY_DP_WELD_MATERIAL_G_O": "410",
            "KEY_DP_DETAILING_EDGE_TYPE": "Rolled, machine-flame cut, sawn and planed",
            "KEY_DP_DETAILING_GAP": "10",
            "KEY_DP_DETAILING_CORROSIVE_INFLUENCES": "No",
            "KEY_DP_DESIGN_METHOD": "Limit State Design"
        }
    ]
    
    # run each test case and validate
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nRunning Test Case {i} (FinPlateTest{i}.osi)")
        try:
            design_dict = mimic_fin_plate_inputs(test_case)
            print("Design Dictionary:")
            for key, value in sorted(design_dict.items()):
                print(f"  {key}: {value}")
            # create fin plate connection object and set inputs
            fin_plate = FinPlateConnection()
            fin_plate.set_input_values(design_dict)
            print(f"Test Case {i}: Validation Successful")
        except Exception as e:
            print(f"Test Case {i}: Validation Failed - {str(e)}")
            raise

# run tests if script is executed directly
if __name__ == "__main__":
    test_mimic_fin_plate_inputs()