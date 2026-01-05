# tests/test_performance_sanity.py
import os, sys, time, pathlib
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

import pytest
from osdag.utils.validator import Validator

# Skip unless RUN_PERF=1
if os.getenv("RUN_PERF", "0") != "1":
    pytest.skip("Performance tests are disabled by default.", allow_module_level=True)

def test_bulk_validate_number():
    v = Validator()
    N = 200000
    t0 = time.perf_counter()
    for i in range(N):
        v.validate_number(str(i))
    dur = time.perf_counter() - t0
    assert dur < 5.0  # adjust if needed for slow machines
