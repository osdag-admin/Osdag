# tests/test_stress_and_bounds.py
import sys, pathlib, time
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

from osdag.utils.validator import Validator

def test_bulk_validate_number_speed():
    v = Validator()
    N = 10000
    start = time.perf_counter()
    for i in range(N):
        v.validate_number(str(i))
    duration = time.perf_counter() - start
    # just a soft check: should be fast on modern machine
    assert duration < 2.0
