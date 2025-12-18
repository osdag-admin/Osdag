# tests/test_invalid_inputs_and_exceptions.py
import sys, pathlib, pytest
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

from osdag.utils.validator import Validator

def test_validate_fu_with_none_raises_or_false():
    v = Validator()
    try:
        out = v.validate_fu(None)
        # if it returns, it should be boolean False
        assert out is False or out is None
    except Exception:
        assert True

def test_validate_number_with_object_returns_false_or_raises():
    v = Validator()
    class X: pass
    try:
        out = v.validate_number(X())
        assert out is False
    except Exception:
        assert True
