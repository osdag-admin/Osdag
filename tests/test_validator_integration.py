# tests/test_validator_integration.py
import sys
import pathlib
from unittest.mock import patch

# path setup
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# dummy injection
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import Validator, ConnectionValidator, FinPlateConnectionValidator

# Small integration: validate a small configuration end-to-end
def test_integration_finplate_workflow():
    v = Validator()
    assert v.validate_fu(400)
    assert v.validate_fy(250)
    assert v.validate_fu_fy(400, 250)

    # weld filtering path: mock IS800 to give min=3, max=6
    cv = ConnectionValidator()
    weld_sizes = [1,2,3,4,5,6,7]
    with patch("osdag.utils.validator.IS800_2007.cl_10_5_2_3_min_weld_size", return_value=3), \
         patch("osdag.utils.validator.IS800_2007.cl_10_5_3_1_max_weld_throat_thickness", return_value=6):
        filtered = cv.filter_weld_list(weld_sizes, 8, 10)
        assert filtered == [3,4,5,6]

    # plate thickness integration with bolt/member
    bolt = type("B", (), {"diameter": 26})()
    supported = type("M", (), {"web_thickness": 12})()
    fpv = FinPlateConnectionValidator()
    plates = [10,12,13]
    out = fpv.filter_plate_thickness(plates, bolt, supported)
    assert out == [12, 13]

