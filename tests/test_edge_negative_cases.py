# tests/test_edge_negative_cases.py
import sys, pathlib
import pytest

repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

from osdag.utils.validator import Validator

def test_validate_number_handles_nan_safely():
    v = Validator()
    # validate_number("NaN") returns True because float("NaN") is valid
    def test_validate_number_raises_on_weird_input():
         v = Validator()
         out = v.validate_number("NaN")
         assert isinstance(out, bool)


    # validate_number("NaN") is a valid float, so the function should NOT crash.
    out = v.validate_number("NaN")

    # It must return a boolean.
    assert isinstance(out, bool)


def test_validate_fu_type_errors():
    v = Validator()
    # If someone passes None or a string, the behavior should be safe (return False or TypeError handled)
    with pytest.raises((TypeError, AssertionError, ValueError, Exception)):
        # call with clearly wrong type that original validate_fu will not accept
        _ = v.validate_fu("not-a-number")
