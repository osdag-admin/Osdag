# tests/test_combined_edgecases.py
import sys, pathlib
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import FinPlateConnectionValidator, Validator

def test_combined_plate_and_number_edgecases():
    v = Validator()
    fpv = FinPlateConnectionValidator()
    # sanity: validator shouldn't crash with weird numeric strings
    assert isinstance(v.validate_number("  12.3  "), bool)
    # plate thickness with weird types
    bolt = type("B", (), {"diameter": 24})()
    supported = type("M", (), {"web_thickness": 10})()
    # Provide string - test robustness
    res = fpv.filter_plate_thickness([10, "12", 13], bolt, supported)
    # result should filter numeric values; ensure it returns a list
    assert isinstance(res, list)
