# tests/test_validator_edgecases.py
import sys
import pathlib
from unittest.mock import patch

# --- path setup: make osdag importable ---
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# --- inject dummy modules used earlier to avoid heavy imports ---
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800

class DummyCommon:
    pass

sys.modules["osdag.Common"] = DummyCommon()

import pytest
from osdag.utils.validator import Validator, ConnectionValidator, FinPlateConnectionValidator, EndPlateConnectionValidator

# ---------- Boundary / edge tests for numeric validators ----------

def test_fu_boundary_values():
    v = Validator()
    assert v.validate_fu(290) is True   # min allowed
    assert v.validate_fu(780) is True   # max allowed
    assert v.validate_fu(289.9999) is False
    assert v.validate_fu(780.0001) is False

def test_fy_boundary_values():
    v = Validator()
    assert v.validate_fy(165) is True
    assert v.validate_fy(650) is True
    assert v.validate_fy(164.9) is False
    assert v.validate_fy(650.1) is False

def test_fu_fy_equal_and_less():
    v = Validator()
    assert v.validate_fu_fy(300, 300) is False  # equal not allowed
    assert v.validate_fu_fy(299, 300) is False  # fu < fy not allowed
    assert v.validate_fu_fy(301, 300) is True

def test_validate_number_non_numeric_and_numeric():
    v = Validator()
    assert v.validate_number("123.45") is True
    assert v.validate_number("0") is True
    assert v.validate_number("not-a-number") is False
    # ensure ints/floats pass through
    assert v.validate_number(123) is True
    assert v.validate_number(12.34) is True

def test_validate_positive_value_edge():
    v = Validator()
    assert v.validate_positive_value(1e-9) is True
    assert v.validate_positive_value(0) is False
    assert v.validate_positive_value(-1e-9) is False

# ---------- ConnectionValidator weld filtering edge cases (with mocking) ----------

def test_connection_filter_weld_list_inclusive_bounds():
    cv = ConnectionValidator()
    weld_sizes = [1, 2, 3, 4, 5]
    # patch min/max to exact boundaries 2 and 4
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=2), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=4):
        out = cv.filter_weld_list(weld_sizes, 10, 12)
        assert out == [2, 3, 4]
