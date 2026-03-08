import sys
import pathlib

# Add Osdag src path
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# Import our dummy module
from tests import dummy_is800

# Patch the heavy modules
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800

class DummyCommon:
    pass

sys.modules["osdag.Common"] = DummyCommon()
import pytest
from osdag.utils.validator import Validator

# --- Tests for Validator simple checks ---

def test_validate_fu_valid_range():
    v = Validator()
    assert v.validate_fu(290) is True
    assert v.validate_fu(780) is True
    assert v.validate_fu(500) is True

def test_validate_fu_out_of_range():
    v = Validator()
    assert v.validate_fu(289) is False
    assert v.validate_fu(781) is False

def test_validate_fy_valid_range():
    v = Validator()
    assert v.validate_fy(165) is True
    assert v.validate_fy(650) is True
    assert v.validate_fy(250) is True

def test_validate_fy_out_of_range():
    v = Validator()
    assert v.validate_fy(164) is False
    assert v.validate_fy(651) is False

def test_validate_fu_fy_relation():
    v = Validator()
    assert v.validate_fu_fy(500, 250) is True
    assert v.validate_fu_fy(250, 250) is False
    assert v.validate_fu_fy(200, 250) is False

def test_validate_number_true_and_false():
    v = Validator()
    assert v.validate_number("12.34") is True
    assert v.validate_number("100") is True
    # non numeric string should return False
    assert v.validate_number("abc") is False

def test_validate_positive_value():
    v = Validator()
    assert v.validate_positive_value(1) is True
    assert v.validate_positive_value(0.0001) is True
    assert v.validate_positive_value(-1) is False
