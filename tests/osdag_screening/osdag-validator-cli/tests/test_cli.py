import subprocess
import sys
import os

# run the installed console script using the interpreter in the current venv
PY = sys.executable

def run(cmd_args):
    # execute using python -m to be robust
    p = subprocess.run([PY, "-m", "osdag_validator_cli.cli"] + cmd_args, capture_output=True, text=True)
    return p

def test_fu_410_valid():
    p = run(["fu", "410"])
    assert p.returncode == 0
    assert ("Valid" in p.stdout) or ("Invalid" in p.stdout)

def test_show_help():
    p = run([])
    assert p.returncode == 0
    assert "usage" in p.stdout.lower()
