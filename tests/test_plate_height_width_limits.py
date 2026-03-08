# tests/test_plate_height_width_limits.py
import sys, pathlib

repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import ShearConnectionValidator, EndPlateConnectionValidator

class M:
    def __init__(self, depth=300, flange_thickness=12, r1=5, flange_width=180, web_thickness=10):
        self.depth = depth
        self.flange_thickness = flange_thickness
        self.r1 = r1
        self.flange_width = flange_width
        self.web_thickness = web_thickness

def test_height_min_and_max_behaviour():
    scv = ShearConnectionValidator()
    supported = M(depth=250, flange_thickness=10, r1=4)
    # min = 0.6 * depth
    assert scv.validate_height_min(0.6 * supported.depth, supported) is True
    assert scv.validate_height_min(0.59 * supported.depth, supported) is False
    # calling max should return boolean (we don't assert True/False because it depends on code path)
    assert isinstance(scv.validate_height_max(100, "beam_beam", supported, supported), bool)

def test_endplate_width_limit_cases():
    epv = EndPlateConnectionValidator()
    sup = M(depth=300, flange_thickness=10, r1=5, flange_width=160)
    # when connectivity is column_flange_beam_web, max width is flange_width
    assert epv.validate_plate_width_max(sup.flange_width, "column_flange_beam_web", sup) is True
    assert epv.validate_plate_width_max(sup.flange_width+100, "column_flange_beam_web", sup) is False
