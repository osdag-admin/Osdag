# tests/test_weld_length_zero_empty.py
import sys, pathlib
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

from osdag.utils.validator import ConnectionValidator

def test_empty_weld_list_returns_empty():
    cv = ConnectionValidator()
    from unittest.mock import patch
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=1), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=4):
        assert cv.filter_weld_list([], 10, 12) == []
