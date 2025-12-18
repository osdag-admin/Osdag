import pytest
import sys, pathlib

# ensure project root is in Python path
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from demo_module.utils import compute_area, parse_profile_string

@pytest.mark.parametrize("w,h,expected", [
    (1, 1, 1),
    (2.5, 4, 10.0),
    (0, 10, 0),
])
def test_compute_area_valid(w, h, expected):
    assert compute_area(w, h) == expected

def test_compute_area_negative():
    with pytest.raises(ValueError):
        compute_area(-1, 5)

def test_compute_area_none():
    with pytest.raises(TypeError):
        compute_area(None, 10)

def test_parse_profile_valid():
    out = parse_profile_string("W100x50")
    assert out["type"] == "W"
    assert out["a"] == 100
    assert out["b"] == 50

@pytest.mark.parametrize("bad", ["", "W100", 123, "X10xY", "W10xx20"])
def test_parse_profile_invalid(bad):
    with pytest.raises((ValueError, TypeError)):
        parse_profile_string(bad)
