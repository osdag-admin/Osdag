# tests/test_geometry_checks.py
import sys
import pathlib

# path setup
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# dummy injection to avoid heavy Common/is800 imports
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import ShearConnectionValidator, FinPlateConnectionValidator, EndPlateConnectionValidator

# Reuse simple dummy objects from conftest via local construction to keep file standalone:
class SimpleMember:
    def __init__(self, depth=300, flange_thickness=15, web_thickness=10, r1=6, flange_width=180):
        self.depth = depth
        self.flange_thickness = flange_thickness
        self.web_thickness = web_thickness
        self.r1 = r1
        self.flange_width = flange_width

class SimplePlate:
    def __init__(self, thickness, height):
        self.thickness = thickness
        self.height = height

def test_validate_height_min_true_false():
    validator = ShearConnectionValidator()
    supported = SimpleMember(depth=300)
    # height must be >= 0.6 * supported.depth
    assert validator.validate_height_min(0.6 * supported.depth, supported) is True
    assert validator.validate_height_min(0.59 * supported.depth, supported) is False

def test_finplate_filter_plate_thickness_limits():
    bolt = type("B", (), {"diameter": 24})()  # bolt diameter 24 -> max plate thickness 12
    supported = SimpleMember(web_thickness=10)
    plate_list = [8, 10, 12, 14]
    fpv = FinPlateConnectionValidator()
    out = fpv.filter_plate_thickness(plate_list, bolt, supported)
    assert out == [10, 12]  # >= web_thickness (10) and <= bolt_diameter/2 (12)

def test_endplate_filter_plate_thickness_limits():
    bolt = type("B", (), {"diameter": 20})()  # max 10
    epv = EndPlateConnectionValidator()
    out = epv.filter_plate_thickness([6, 10, 12], bolt)
    assert out == [6, 10]
