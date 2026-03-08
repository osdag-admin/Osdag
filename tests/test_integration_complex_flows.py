# tests/test_integration_complex_flows.py
import sys, pathlib
from unittest.mock import patch

repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import Validator, ConnectionValidator, FinPlateConnectionValidator

def test_full_finplate_workflow_mocked():
    v = Validator()
    assert v.validate_fu(420)
    assert v.validate_fy(250)
    assert v.validate_fu_fy(420,250)

    cv = ConnectionValidator()
    weld_sizes = list(range(1,11))
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=3), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=7):
        filt = cv.filter_weld_list(weld_sizes, 10, 12)
        assert filt == [3,4,5,6,7]

    bolt = type("B", (), {"diameter": 28})()
    supported = type("M", (), {"web_thickness": 12})()
    fpv = FinPlateConnectionValidator()
    plates = [10,12,14]
    out = fpv.filter_plate_thickness(plates, bolt, supported)
    assert out == [12,14]
