import yaml
import os

VALID_VALUES = {
    "Bolt.Bolt_Hole_Type": ["Standard", "Oversized", "Slotted"],
    "Bolt.TensionType": ["Pre-tensioned", "Non-pre-tensioned"],
    "Detailing.Corrosive_Influences": ["Yes", "No"],
    "Design.Method": ["Limit State Design", "Working Stress Design"],
}

MISSPELLED_KEYS = {
    "Blt.Diameter": "Bolt.Diameter",
    "Modle": "Module",
    "Standrd": "Standard",
    "Pretensoned": "Pre-tensioned",
    "Maybe": "Yes/No",
}

NUMERIC_KEYS = {
    "Detailing.Gap": (0, 50),
    "Load.Axial": (0, 1000),
    "Load.Shear": (0, 500),
}

def validate_osi_files():
    files = [f for f in os.listdir() if f.endswith(".osi")]
    
    if not files:
        print("No OSI files found in the directory.")
        return

    print(f"Found {len(files)} OSI file(s). Starting validation...\n")

    for file in files:
        validate_osi_file(file)

def validate_osi_file(filename):
    errors = {"Misspelled Keys": [], "Invalid Values": [], "Invalid Numeric Values": []}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not data:
            print(f"\n ERROR: Empty or Corrupted OSI File: {filename}")
            return

        check_misspelled_keys(data, errors)
        check_invalid_values(data, errors)
        check_numeric_values(data, errors)

        if any(errors.values()):
            print(f"\n ERRORS FOUND IN OSI FILE: {filename}")
            for category, issues in errors.items():
                if issues:
                    print(f"\n {category}:")
                    for issue in issues:
                        print(f"  - {issue}")
            print("\n Fix the above errors and try again.")
        else:
            print(f"\n OSI file validation successful for: {filename}")

    except yaml.YAMLError as e:
        print(f"\n YAML Parsing Error in {filename}: {e}")
    except Exception as e:
        print(f"\n Unexpected Error in {filename}: {e}")

def check_misspelled_keys(data, errors):
    def recursive_check(d, parent_key=""):
        if isinstance(d, dict):
            for key in list(d.keys()):
                full_key = f"{parent_key}.{key}" if parent_key else key
                if key in MISSPELLED_KEYS:
                    corrected_key = MISSPELLED_KEYS[key]
                    errors["Misspelled Keys"].append(f"{full_key} -> {corrected_key}")
                recursive_check(d[key], full_key)

    recursive_check(data)

def check_invalid_values(data, errors):
    def recursive_check(d, parent_key=""):
        if isinstance(d, dict):
            for key, value in d.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if full_key in VALID_VALUES:
                    if value not in VALID_VALUES[full_key]:
                        errors["Invalid Values"].append(f"{full_key} = '{value}' (Expected: {VALID_VALUES[full_key]})")
                recursive_check(value, full_key)

    recursive_check(data)

def check_numeric_values(data, errors):
    def recursive_check(d, parent_key=""):
        if isinstance(d, dict):
            for key, value in d.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if full_key in NUMERIC_KEYS:
                    min_val, max_val = NUMERIC_KEYS[full_key]
                    if not isinstance(value, (int, float)):
                        errors["Invalid Numeric Values"].append(f"{full_key} = '{value}' (Expected: Numeric value)")
                    elif not (min_val <= value <= max_val):
                        errors["Invalid Numeric Values"].append(
                            f"{full_key} = {value} (Out of range: {min_val} to {max_val})"
                        )
                recursive_check(value, full_key)

    recursive_check(data)

if __name__ == "__main__":
    validate_osi_files()
