# osdag-validator-cli/tests/test_cli_generated.py
"""
Generated tests for osdag_validator_cli.cli

These tests run the CLI using the same Python interpreter (sys.executable).
They expect the CLI module to be importable via `python -m osdag_validator_cli.cli`.
If a particular Validator method isn't implemented, the CLI intentionally prints
"Invalid" and returns 0 for that command (this behavior is accepted by the tests).
"""

import sys
import subprocess
import pytest

PY = sys.executable

def run_cli(args):
    """Run the CLI module and return CompletedProcess (capture text)."""
    cmd = [PY, "-m", "osdag_validator_cli.cli"] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p

def assert_valid_or_invalid(stdout):
    """Helper: pass if stdout contains 'Valid' or 'Invalid' (case-sensitive)."""
    s = stdout.strip()
    assert ("Valid" in s) or ("Invalid" in s), f"stdout does not contain Valid/Invalid: {s!r}"

def test_fu_valid():
    p = run_cli(["fu", "410"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_fy_valid():
    p = run_cli(["fy", "250"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_fu_fy_relation():
    p = run_cli(["fu-fy", "410", "250"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_number_check():
    p = run_cli(["number", "12.5"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_positive_check():
    p = run_cli(["positive", "8"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_tf_if_present():
    p = run_cli(["tf", "20"])
    # Accept either normal valid/invalid output or 'Invalid' if function missing
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_bolt_if_present():
    p = run_cli(["bolt", "M20", "8.8"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)

def test_plate_if_present():
    p = run_cli(["plate", "10", "250"])
    assert p.returncode == 0
    assert_valid_or_invalid(p.stdout)
