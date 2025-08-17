import yaml
import pandas as pd
import os
from osdag.design_type.connection.cleat_angle_connection import CleatAngleConnection

def load_test_data():
    """Load test cases from Excel file"""
    try:
        df = pd.read_excel("ExpectedOutputs.xlsx", sheet_name="Cleat Angle Connection")
        print("✅ Successfully loaded test cases")
        return df
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        exit(1)

def setup_connection(data):
    """Create and configure connection object"""
    connection = CleatAngleConnection()

    try:
        connection.set_input_values(data)  
    except Exception as e:
        print(f" set_input_values failed: {e}")
        raise

    try:
        connection.check_available_cleat_thk()
        connection.create3DModel()  
    except Exception as e:
        print(f"Error during cleat checks or model creation: {e}")

    return connection

def run_single_test(filename, expected):
    """Run test for a single OSI file"""
    print(f"\n Testing: {filename}")
    print(f" Expected: {expected}")

    try:
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            print(" Empty YAML file")
            return "error"

        connection = setup_connection(data)

        
        if not hasattr(connection, "cleat") or not hasattr(connection, "bolt"):
            print(" Missing 'cleat' or 'bolt' attribute")
            return "error"

        actual = {
            "designation": connection.cleat.designation,
            "bolt_dia": connection.bolt.bolt_diameter_provided,
            "bolt_grade": connection.bolt.bolt_PC_provided
        }

        print(f" Actual: {actual}")

        for key in expected:
            if key in actual and expected[key] != actual[key]:
                print(f" Mismatch in {key}: expected {expected[key]}, got {actual[key]}")
                return "failed"

        return "passed"

    except Exception as e:
        print(f" Test failed with error: {type(e).__name__}: {e}")
        return "error"

def main():
    test_cases = load_test_data()

    expected_values = []
    for _, row in test_cases.iterrows():
        if pd.notna(row["Designation"]) and row["Designation"] not in ["Value", "Designation"]:
            expected_values.append({
                "designation": row["Designation"],
                "bolt_dia": row["Bolt Diameter"],
                "bolt_grade": str(row["Property Class"])
            })

    results = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}

    for i, expected in enumerate(expected_values, 1):
        filename = f"CleatAngleTest{i}.osi"

        if not os.path.exists(filename):
            print(f"  Skipping {filename} (file not found)")
            results["skipped"] += 1
            continue

        test_result = run_single_test(filename, expected)

        # Safe update
        if test_result in results:
            results[test_result] += 1
        else:
            results["errors"] += 1

    print("\n" + "=" * 50)
    print(" TEST SUMMARY")
    print("=" * 50)
    print(f" Passed: {results['passed']}")
    print(f" Failed: {results['failed']}")
    print(f"  Errors: {results['errors']}")
    print(f"⏭ Skipped: {results['skipped']}")
    print("=" * 50)

    if results['passed'] == len(expected_values):
        print(" All tests passed!")
    else:
        print(" Some tests failed or errored. See above.")

if __name__ == "__main__":
    main()
