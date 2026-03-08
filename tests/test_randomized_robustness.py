# tests/test_randomized_robustness.py
import sys, pathlib, random
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import Validator, ConnectionValidator

def test_random_weld_lists_do_not_crash():
    cv = ConnectionValidator()
    for _ in range(100):
        welds = [round(random.uniform(0.5, 10.0),2) for _ in range(random.randint(0,10))]
        # patch to safe min/max
        from unittest.mock import patch
        with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=1), \
             patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=8):
            _ = cv.filter_weld_list(welds, 10, 12)
    assert True
