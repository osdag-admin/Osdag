# tests/test_validator_parametrics.py
import sys, pathlib
from itertools import product

# path setup
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# dummy injection
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import Validator

@pytest.mark.parametrize("fu,expected", [
    (290, True), (780, True), (289.9, False), (780.1, False),
    (400, True), (1000, False)
])
def test_validate_fu_param(fu, expected):
    v = Validator()
    assert v.validate_fu(fu) is expected

@pytest.mark.parametrize("fy,expected", [
    (165, True), (650, True), (164.9, False), (650.1, False),
    (250, True)
])
def test_validate_fy_param(fy, expected):
    v = Validator()
    assert v.validate_fy(fy) is expected

@pytest.mark.parametrize("a,b", [
    (300, 299), (300, 300), (301,300)
])
def test_validate_fu_fy_relations(a,b):
    v = Validator()
    expect = a > b
    assert v.validate_fu_fy(a,b) is expect

def test_validate_number_various_types():
    v = Validator()
    assert v.validate_number("123.45") is True
    assert v.validate_number(123) is True
    assert v.validate_number(12.34) is True
    assert v.validate_number("notnum") is False
