import os

#Valid entries per file
valid_designations = {
    "TensionBoltedTest1": ["40 x 20 x 3"],
    "TensionBoltedTest2": ["JC 100"],
    "TensionBoltedTest3": ["40 x 40 x 3"],
    "TensionBoltedTest4": ["JC175"],
}
valid_bolt_grades = ["3.6", "12.9", "4.6", "5.6"]
valid_bolt_diameters = {
    "TensionBoltedTest1": [""],     # skip check
    "TensionBoltedTest2": ["12"],
    "TensionBoltedTest3": ["10"],
    "TensionBoltedTest4": ["20"],
}

def normalize(val):
    return val.strip().strip("'").strip('"').lower()

def extract_multiple_values(file_path):
    values = {"Member.Designation": [], "Bolt.Grade": [], "Bolt.Diameter": []}
    with open(file_path, "r") as f:
        current_key = None
        for line in f:
            line = line.strip()
            if ":" in line:
                key, _ = line.split(":", 1)
                current_key = key.strip()
                if current_key in values:
                    values[current_key] = []
            elif current_key and current_key in values and line.startswith("-"):
                values[current_key].append(line.strip("- ").strip())
    return values

def validate_osi(file_path):
    filename = os.path.splitext(os.path.basename(file_path))[0]
    data = extract_multiple_values(file_path)

    normalized_data = {
        "Member.Designation": [normalize(d) for d in data["Member.Designation"]],
        "Bolt.Grade": [normalize(g) for g in data["Bolt.Grade"]],
        "Bolt.Diameter": [normalize(d) for d in data["Bolt.Diameter"]],
    }

    # Get file-specific valid bolt diameters
    bolt_dia_check = valid_bolt_diameters.get(filename, [])
    bolt_dia_check_normalized = [normalize(val) for val in bolt_dia_check if normalize(val) != ""]

    results = {}

    # Check Member.Designation
    valid_desig = [normalize(val) for val in valid_designations.get(filename, [])]
    results["Member.Designation"] = "Pass" if any(d in valid_desig for d in normalized_data["Member.Designation"]) else "Fail"

    # Check Bolt.Grade
    valid_grades = [normalize(val) for val in valid_bolt_grades]
    results["Bolt.Grade"] = "Pass" if any(g in valid_grades for g in normalized_data["Bolt.Grade"]) else "Fail"

    # Check Bolt.Diameter
    if not bolt_dia_check or "" in bolt_dia_check:
        results["Bolt.Diameter"] = ""  # Leave blank
    else:
        results["Bolt.Diameter"] = (
            "Pass" if any(d in bolt_dia_check_normalized for d in normalized_data["Bolt.Diameter"]) else "Fail"
        )

    return results

#Run validator
folder_path = "./osi_files"
print("Running OSI File Validator...\n")
for file in os.listdir(folder_path):
    if file.endswith(".osi"):
        path = os.path.join(folder_path, file)
        result = validate_osi(path)
        print(f"Results for {file}:")
        for key, status in result.items():
            print(f"  {key}: {status}")
        print()
