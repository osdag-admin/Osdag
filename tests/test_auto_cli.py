import subprocess, sys, os
HERE = os.path.dirname(__file__)
PY = sys.executable

def run_cmd(cmd):
    p = subprocess.run([PY, "-c", cmd], capture_output=True, text=True)
    return p

# ---------------------------------------------------------
# Core Validator smoke tests
# ---------------------------------------------------------

def test_get_validator_smoke():
    cmd = "from osdag_validator_cli.auto_cli import get_validator; get_validator()"
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_print_result_smoke():
    cmd = "from osdag_validator_cli.auto_cli import print_result; print_result('1')"
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_Validator_validate_fu_smoke():
    cmd = "from osdag_validator_cli.auto_cli import Validator_validate_fu; Validator_validate_fu('1')"
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_Validator_validate_fy_smoke():
    cmd = "from osdag_validator_cli.auto_cli import Validator_validate_fy; Validator_validate_fy('1')"
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_Validator_validate_fu_fy_smoke():
    cmd = "from osdag_validator_cli.auto_cli import Validator_validate_fu_fy; Validator_validate_fu_fy('1','1')"
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_Validator_validate_number_smoke():
    cmd = "from osdag_validator_cli.auto_cli import Validator_validate_number; Validator_validate_number('1')"
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_Validator_validate_positive_value_smoke():
    cmd = "from osdag_validator_cli.auto_cli import Validator_validate_positive_value; Validator_validate_positive_value('1')"
    p = run_cmd(cmd)
    assert p.returncode == 0

# ---------------------------------------------------------
# ConnectionValidator tests
# ---------------------------------------------------------

def test_ConnectionValidator_filter_weld_list_smoke():
    cmd = (
        "from osdag_validator_cli.auto_cli import ConnectionValidator_filter_weld_list; "
        "ConnectionValidator_filter_weld_list('1','1','1')"
    )
    p = run_cmd(cmd)
    assert p.returncode == 0

# ---------------------------------------------------------
# ShearConnectionValidator tests
# ---------------------------------------------------------

def test_ShearConnectionValidator_validate_height_min_smoke():
    cmd = (
        "from osdag_validator_cli.auto_cli import ShearConnectionValidator_validate_height_min; "
        "ShearConnectionValidator_validate_height_min('1','1')"
    )
    p = run_cmd(cmd)
    assert p.returncode == 0

# ---------------------------------------------------------
# FinPlateConnectionValidator tests
# ---------------------------------------------------------

def test_FinPlateConnectionValidator_filter_plate_thickness_smoke():
    cmd = (
        "from osdag_validator_cli.auto_cli import FinPlateConnectionValidator_filter_plate_thickness; "
        "FinPlateConnectionValidator_filter_plate_thickness('1','1','1')"
    )
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_FinPlateConnectionValidator_validate_plate_height_min_smoke():
    cmd = (
        "from osdag_validator_cli.auto_cli import FinPlateConnectionValidator_validate_plate_height_min; "
        "FinPlateConnectionValidator_validate_plate_height_min('1','1')"
    )
    p = run_cmd(cmd)
    assert p.returncode == 0

# ---------------------------------------------------------
# EndPlateConnectionValidator tests
# ---------------------------------------------------------

def test_EndPlateConnectionValidator_filter_plate_thickness_smoke():
    cmd = (
        "from osdag_validator_cli.auto_cli import EndPlateConnectionValidator_filter_plate_thickness; "
        "EndPlateConnectionValidator_filter_plate_thickness('1','1')"
    )
    p = run_cmd(cmd)
    assert p.returncode == 0

def test_EndPlateConnectionValidator_validate_plate_width_max_smoke():
    cmd = (
        "from osdag_validator_cli.auto_cli import EndPlateConnectionValidator_validate_plate_width_max; "
        "EndPlateConnectionValidator_validate_plate_width_max('1','1','1')"
    )
    p = run_cmd(cmd)
    assert p.returncode == 0
