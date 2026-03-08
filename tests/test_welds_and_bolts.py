# tests/test_welds_and_bolts.py
import sys, pathlib
from unittest.mock import patch

# path setup
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# dummy injection (prevents heavy imports)
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import ConnectionValidator, FinPlateConnectionValidator, EndPlateConnectionValidator

# Use fixtures from conftest (bolt, supported_member)
def test_weld_filter_uses_is800_min_max_patch():
    cv = ConnectionValidator()
    weld_sizes = [0.5, 1, 2, 3, 4, 5, 6, 7]
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=1), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=5):
        out = cv.filter_weld_list(weld_sizes, 5, 6)
        assert out == [1, 2, 3, 4, 5]

def test_finplate_bolt_plate_relation(bolt, supported_member):
    fpv = FinPlateConnectionValidator()
    # bolt diameter 20 -> max plate thickness 10; supported_member.web_thickness uses fixture
    plate_list = [6, 9, 10, 11, 12]
    out = fpv.filter_plate_thickness(plate_list, bolt, supported_member)
    assert out == [t for t in plate_list if supported_member.web_thickness <= t <= bolt.diameter / 2]

def test_endplate_plate_filter(bolt):
    epv = EndPlateConnectionValidator()
    plates = [4, 6, 9, 11]
    # bolt fixture diameter gives max plate thickness = bolt.diameter/2
    out = epv.filter_plate_thickness(plates, bolt)
    assert all(isinstance(x, (int, float)) for x in out)
    assert all(x <= bolt.diameter / 2 for x in out)
