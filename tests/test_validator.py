import os
import pytest
import validator  # Ensure validator.py is in the same folder or PYTHONPATH

# ✅ Updated base path
BASE_PATH = r"C:\Visual Studio Code\FOSSEE OSDAG\Osdag\osdag-conda-recipe\recipe\tests\osi_files"

def run_test(file_name, expected_result):
    file_path = os.path.join(BASE_PATH, file_name)
    result = validator.validate_osi(file_path)
    print(f"Testing {file_name}")
    for key in expected_result:
        assert result[key] == expected_result[key], f"{key} failed: expected {expected_result[key]}, got {result[key]}"
    print(" Passed\n")

def test_tension_bolted_test1():
    expected_result = {
        "Member.Designation": "Pass",
        "Bolt.Grade": "Pass",
        "Bolt.Diameter": ""  # Skipped check
    }
    run_test("TensionBoltedTest1.osi", expected_result)

def test_tension_bolted_test2():
    expected_result = {
        "Member.Designation": "Pass",
        "Bolt.Grade": "Pass",
        "Bolt.Diameter": "Pass"
    }
    run_test("TensionBoltedTest2.osi", expected_result)

def test_tension_bolted_test3():
    expected_result = {
        "Member.Designation": "Pass",
        "Bolt.Grade": "Pass",
        "Bolt.Diameter": "Pass"
    }
    run_test("TensionBoltedTest3.osi", expected_result)

def test_tension_bolted_test4():
    expected_result = {
        "Member.Designation": "Pass",
        "Bolt.Grade": "Pass",
        "Bolt.Diameter": "Pass"
    }
    run_test("TensionBoltedTest4.osi", expected_result)

if __name__ == "__main__":
    pytest.main()

