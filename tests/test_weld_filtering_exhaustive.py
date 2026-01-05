# tests/test_weld_filtering_exhaustive.py
import sys, pathlib
from unittest.mock import patch

repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import ConnectionValidator

@pytest.mark.parametrize("min_w,max_w,weld_sizes,expected", [
    (1, 3, [0.5,1,2,3,4], [1,2,3]),
    (2, 4, [1,2,3,4,5], [2,3,4]),
    (0, 10, [], []),
    (3, 3, [1,2,3,4], [3])
])
def test_weld_filter_with_various_bounds(min_w, max_w, weld_sizes, expected):
    cv = ConnectionValidator()
    # patch the calls where the validator uses IS800_2007
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=min_w), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=max_w):
        out = cv.filter_weld_list(weld_sizes, 10, 12)
        assert out == expected
