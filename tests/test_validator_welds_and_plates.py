import sys
import pathlib
from unittest.mock import patch   # ← ADD THIS LINE

# Add Osdag src path
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800

sys.modules["osdag.utils.common.is800_2007"] = dummy_is800

class DummyCommon:
    pass

sys.modules["osdag.Common"] = DummyCommon()

import pytest
from osdag.utils.validator import ConnectionValidator, FinPlateConnectionValidator, EndPlateConnectionValidator

# --- Test ConnectionValidator.filter_weld_list with mocked IS800 values --------
def test_connection_filter_weld_list_mock_min_max():
    cv = ConnectionValidator()
    # Make a simple weld sizes list
    weld_sizes = [1, 2, 3, 4, 5, 6]

    # Patch the IS800_2007 functions used inside filter_weld_list to define min/max
    # We patch where they are referenced inside validator module's import path:
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=2), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=4):
        filtered = cv.filter_weld_list(weld_sizes, part1_thickness=10, part2_thickness=12)
        # expected to keep values in [2,4]
        assert filtered == [2, 3, 4]

# --- Tests for FinPlateConnectionValidator.filter_plate_thickness ----------
def test_finplate_filter_plate_thickness(bolt, supported_member):
    fpv = FinPlateConnectionValidator()
    plate_list = [6, 8, 10, 12, 15]  # mm
    # supported_member_web_thickness = supported_member.web_thickness (from fixture)
    # min_plate_thickness = supported_member_web_thickness
    # max_plate_thickness = bolt.diameter / 2
    out = fpv.filter_plate_thickness(plate_list, bolt, supported_member)
    expected = [t for t in plate_list if supported_member.web_thickness <= t <= bolt.diameter / 2]
    assert out == expected

# --- Tests for EndPlateConnectionValidator.filter_plate_thickness ----------
def test_endplate_filter_plate_thickness(bolt):
    epv = EndPlateConnectionValidator()
    plate_list = [4, 8, 10, 12, 16]
    out = epv.filter_plate_thickness(plate_list, bolt)
    expected = [t for t in plate_list if t <= bolt.diameter / 2]
    assert out == expected
