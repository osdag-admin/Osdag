# tests/test_plate_and_connection_limits.py
import sys, pathlib

repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import ShearConnectionValidator, EndPlateConnectionValidator, FinPlateConnectionValidator

# simple dummies (we can also reuse conftest fixtures)
class Member:
    def __init__(self, depth=300, flange_thickness=15, web_thickness=10, flange_width=180, r1=6):
        self.depth = depth
        self.flange_thickness = flange_thickness
        self.web_thickness = web_thickness
        self.flange_width = flange_width
        self.r1 = r1

class Plate:
    def __init__(self, thickness, height):
        self.thickness = thickness
        self.height = height

def test_validate_plate_width_max_various_connectivities():
    epv = EndPlateConnectionValidator()
    # connectivity: column_flange_beam_web uses supporting_member.flange_width
    sup = Member(flange_width=200, flange_thickness=20, web_thickness=12)
    assert epv.validate_plate_width_max(200, "column_flange_beam_web", sup) is True
    # narrow width should also return True
    assert epv.validate_plate_width_max(100, "column_flange_beam_web", sup) is True
    # For column_web_beam_web, width uses depth - 2*(flange_thickness + r1 + 5)
    sup2 = Member(depth=300, flange_thickness=10, r1=4)
    max_w = sup2.depth - 2 * (sup2.flange_thickness + sup2.r1 + 5)
    assert epv.validate_plate_width_max(max_w, "column_web_beam_web", sup2) is True
    # If connectivity unknown, should return True (per code)
    assert epv.validate_plate_width_max(1000, "unknown_conn", sup) is True

def test_height_min_max_behavior_for_shear_connection():
    scv = ShearConnectionValidator()
    supported = Member(depth=250, flange_thickness=12, r1=5)
    supporting = Member(flange_thickness=10, r1=5)
    # min height
    min_h = 0.6 * supported.depth
    assert scv.validate_height_min(min_h, supported) is True
    assert scv.validate_height_min(min_h - 1, supported) is False
    # For beam_beam connectivity, validate_height_max should return a numeric comparison
    # We'll call it and ensure it returns a boolean (not an exception)
    val = scv.validate_height_max(100, "beam_beam", supporting, supported)
    assert isinstance(val, bool)
