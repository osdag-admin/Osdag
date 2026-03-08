# tests/test_validator_performance.py
import os
import sys
import pathlib
import time

# path setup
repo_root = pathlib.Path(__file__).resolve().parents[1] / "Osdag" / "src"
sys.path.insert(0, str(repo_root))

# dummy injection
from tests import dummy_is800
sys.modules["osdag.utils.common.is800_2007"] = dummy_is800
sys.modules["osdag.Common"] = type("DummyCommon", (), {})()

from osdag.utils.validator import Validator

import pytest

# This test is skipped unless you set environment variable RUN_PERF=1
if os.getenv("RUN_PERF", "0") != "1":
    pytest.skip("Performance tests disabled by default. Set RUN_PERF=1 to enable.", allow_module_level=True)

def test_validate_number_performance():
    v = Validator()
    N = 200_000
    start = time.perf_counter()
    for i in range(N):
        assert v.validate_number(str(i))
    duration = time.perf_counter() - start
    # expect the loop to finish reasonably fast; adjust threshold if your machine is slower
    assert duration < 2.0, f"Performance slow: {duration:.2f}s for {N} iterations"
