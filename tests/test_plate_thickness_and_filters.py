# tests/test_plate_thickness_and_filters.py
import sys, pathlib

repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import FinPlateConnectionValidator, EndPlateConnectionValidator

def test_finplate_plate_thickness_edge_cases():
    bolt = type("B", (), {"diameter": 26})()  # max plate thickness 13
    supported = type("M", (), {"web_thickness": 10})()
    fpv = FinPlateConnectionValidator()
    plates = [9,10,12,13,14]
    out = fpv.filter_plate_thickness(plates, bolt, supported)
    assert out == [10,12,13]

def test_endplate_plate_thickness_edge_cases():
    bolt = type("B", (), {"diameter": 20})()
    epv = EndPlateConnectionValidator()
    in_list = [5,9,10,11,15]
    out = epv.filter_plate_thickness(in_list, bolt)
    # endplate logic in Osdag allows <= bolt/2
    assert all(x <= bolt.diameter/2 for x in out)
