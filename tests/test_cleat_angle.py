import sys
import os
import builtins
import yaml
import pytest

# Add Osdag source path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Inject missing constants before Osdag loads
builtins.KEY_DP_FAB_SHOP = "fab_shop"
builtins.KEY_DP_FAB_FIELD = "fab_field"

# Import CleatAngleConnection safely
from osdag.design_type.connection.cleat_angle_connection import CleatAngleConnection

import osdag.design_type.connection.cleat_angle_connection as cleat_mod
import logging

# Patch missing logger
cleat_mod.logger = logging.getLogger("dummy_logger")
cleat_mod.logger.addHandler(logging.NullHandler())


# Patch set_input_values to fix argument issue
def patched_set_input_values(self, design_dictionary):
    CleatAngleConnection.__bases__[0].set_input_values(self, design_dictionary)

CleatAngleConnection.set_input_values = patched_set_input_values

# Patch connectdb after import (mock DB access)
class DummyCursor:
    def execute(self, query):
        if "Bolt" in query:
            return [(10,), (8,), (12,)]
        return []
    def fetchall(self):
        return [(10,), (8,), (12,)]

class DummyConnection:
    def execute(self, q): return DummyCursor()
    def cursor(self): return DummyCursor()
    def commit(self): pass
    def close(self): pass

if "osdag.Common" in sys.modules:
    sys.modules["osdag.Common"].connectdb = lambda name: DummyConnection()

# Load YAML file
def load_osi_file(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

# Run design logic
def run_design(filepath):
    data = load_osi_file(filepath)
    obj = CleatAngleConnection()
    obj.set_input_values(data)

    connector = data.get("Connector", {})  # Safe access
    obj.angle_list = connector.get("Angle_List", [])
    obj.cleat_list = obj.angle_list.copy()
    obj.cleat_material_grade = connector.get("Material", "")
    obj.check_available_cleat_thk()

    return obj

# Test case from Excel
test_cases = [
    (
        "CleatAngleTest1.osi",
        {
            "designation": "50x50x3",
            "height": 115,
            "shear_yielding_capacity": 90.54,
            "block_shear_capacity": 101.36,
            "moment_capacity": 4.51,
            "bolt_diameter": 10,
            "property_class": "5.6"
        }
    ),
    (
        "CleatAngleTest2.osi",
        {
            "designation": "60x60x4",
            "height": 130,
            "shear_yielding_capacity": 136.46,
            "block_shear_capacity": 124.08,
            "moment_capacity": 7.68,
            "bolt_diameter": 8,
            "property_class": "6.8"
        }
    ),
    (
        "CleatAngleTest3.osi",
        {
            "designation": "65x65x8",
            "height": 150,
            "shear_yielding_capacity": 314.92,
            "block_shear_capacity": 353.61,
            "moment_capacity": 20.45,
            "bolt_diameter": 8,
            "property_class": "12.9"
        }
    ),
    (
        "CleatAngleTest4.osi",
        {
            "designation": "50x50x3",
            "height": 150,
            "shear_yielding_capacity": 118.09,
            "block_shear_capacity": 125.77,
            "moment_capacity": 7.67,
            "bolt_diameter": 8,
            "property_class": "4.8"
        }
    )
]

# Pytest test function
@pytest.mark.parametrize("filename, expected", test_cases)
def test_cleat_angle_output(filename, expected):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    assert os.path.exists(filepath), f"Missing OSI file: {filepath}"

    obj = run_design(filepath)

    assert hasattr(obj, "cleat"), f"No cleat selected for {filename}"
    assert obj.cleat.designation == expected["designation"]
    assert obj.cleat.height == expected["height"]
    assert round(obj.shear_yielding_capacity, 2) == expected["shear_yielding_capacity"]
    assert round(obj.block_shear_capacity, 2) == expected["block_shear_capacity"]
    assert round(obj.moment_capacity, 2) == expected["moment_capacity"]
    assert obj.bolt.bolt_diameter_provided == expected["bolt_diameter"]
    assert obj.bolt.bolt_PC_provided == expected["property_class"]
