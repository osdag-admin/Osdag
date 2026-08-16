import os
import sys
import yaml
import pandas as pd
import pytest

# Setup path to import from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from osdag.design_type.connection.fin_plate_connection import FinPlateConnection

# ----------------- MONKEY PATCH ---------------------
# If you cannot change fin_plate_connection.py
def patched_set_input_values(self, design_dictionary):
    super(type(self), self).set_input_values(design_dictionary)
    self.fin_plate_thickness = design_dictionary.get("FinPlateThickness")
    self.edge_distance = design_dictionary.get("EdgeDistance")
    self.fin_plate_material = design_dictionary.get("FinPlateMaterial")
    self.connectivity = design_dictionary.get("Connectivity")
    self.bolt_dia = design_dictionary.get("BoltDia")
    self.bolt_type = design_dictionary.get("BoltType")
    self.bolt_grade = design_dictionary.get("BoltGrade")
    self.no_of_rows = design_dictionary.get("NumberOfRows")
    self.no_of_columns = design_dictionary.get("NumberOfColumns")
    self.pitch = design_dictionary.get("Pitch")
    self.gauge = design_dictionary.get("Gauge")
    self.weld_size = design_dictionary.get("WeldSize")
    self.member_type = design_dictionary.get("MemberType")
    self.end_distance = design_dictionary.get("EndDistance")
    self.safety_factor = design_dictionary.get("SafetyFactor")
    self.material_grade = design_dictionary.get("MaterialGrade")
    self.load = design_dictionary.get("Load")

# Apply patch
FinPlateConnection.set_input_values = patched_set_input_values
# -----------------------------------------------------


# Load expected values from Excel
def load_expected_values(path):
    df = pd.read_excel(path, sheet_name="Fin Plate Connection", header=None)

    expected = {}
    for _, row in df.iterrows():
        try:
            test_id = str(row[1]).strip()

            # Skip unwanted rows
            if not test_id.startswith("FinPlateTest"):
                continue

            filename = f"{test_id}.osi"
            expected[filename] = {
                "weld_size": float(row[3]),
                "shear_capacity": float(row[5]),
                "bearing_capacity": float(row[7]),
                "bolt_shear": float(row[9]),
                "weld_stress": float(row[19]),
                "moment_capacity": float(row[21])
            }

        except Exception as e:
            print(f"Skipping row due to error: {e}")
            continue

    print("✅ Loaded expected data for:", list(expected.keys()))
    return expected



# Run the full design
def run_design(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    obj = FinPlateConnection()
    obj.set_input_values(data)
    obj.design_finplate_connection()
    return obj


# Parametrize based on all FinPlateTest*.osi files in current folder
@pytest.mark.parametrize("filename", [
    f for f in os.listdir(os.path.dirname(__file__))
    if f.startswith("FinPlateTest") and f.endswith(".osi")
])
def test_fin_plate_outputs(filename):
    expected_path = os.path.join(os.path.dirname(__file__), "ExpectedOutputs.xlsx")
    expected_data = load_expected_values(expected_path)

    assert filename in expected_data, f"{filename} not found in Excel sheet"
    expected = expected_data[filename]

    filepath = os.path.join(os.path.dirname(__file__), filename)
    assert os.path.exists(filepath), f"Missing OSI file: {filepath}"

    obj = run_design(filepath)

    assert round(obj.weld.weld_size, 2) == expected["weld_size"]
    assert round(obj.shear_capacity, 2) == expected["shear_capacity"]
    assert round(obj.bearing_capacity, 2) == expected["bearing_capacity"]
    assert round(obj.bolt_shear_capacity, 2) == expected["bolt_shear"]
    assert round(obj.weld_stress, 2) == expected["weld_stress"]
    assert round(obj.moment_capacity, 2) == expected["moment_capacity"]

