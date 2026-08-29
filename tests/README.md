Osdag Testing Suite – tests/
This directory contains testing and validation scripts built to ensure the correctness, consistency, and structure of .osi design files used in Osdag. These tests primarily focus on validating file formats, parameter values, and GUI input mimicry for automated and regression testing.

File Descriptions
1. test_validator.py
This is a unit test suite that verifies the .osi files exported by the Tension Member Design – Bolted to End Gusset module.

Asserts specific key-value pairs such as:

Member.Designation

Bolt.Grade

Bolt.Diameter

The test compares these values against expected results and flags any mismatches.

Uses validator.py as the backend validation engine.

Usage Tip: To skip checking a particular key, just use an empty string "" in the expected_result.

2. validator.py
A utility script that performs field-level validation for .osi files.

Extracts and normalizes values from .osi files.

Validates keys using known correct values (e.g., valid bolt grades, valid designations).

Returns a Pass/Fail result per key for use in testing.

Helps maintain data consistency early in the test pipeline.

3. test_tension_bolted_mock.py
This script automates the testing of .osi file structure and content for the Tension Member module.

Meant for mock runs to simulate how actual .osi values will be verified post-design.

Aims to catch incorrect data early during development.

Useful for quickly validating new or modified .osi test cases before pushing to production.

4. test_fin_plate_mimicry.py
This script tests GUI-mimicked input flows for the Fin Plate Connection module.

Mimics how a user would fill in GUI inputs programmatically, including handling:

Combo boxes

Text fields with validation

Material-specific logic for fy, fu

Automatically generates a design_dictionary from raw input.

Ensures values conform to expected database-driven options (like sections, grades, plate thickness).

Final output is passed to the actual Osdag design logic to verify input compatibility.

This file is especially useful for ensuring that test .osi files align with what the GUI would generate in a real user scenario.

How to Run
Each file can be run using Python or pytest where applicable.

# Run all pytest-based validations
pytest test_validator.py

# Run GUI-mimicked design input tests
python test_fin_plate_mimicry.py
Ensure dependencies and database paths are correctly set before execution.

Purpose
This folder serves as a foundational test layer to:

Detect errors in .osi files early.

Verify GUI-input compatibility.

Automate structural checks on design outputs.

Serve as a baseline for regression testing during ongoing development.

Each script here is modular and can be extended or reused across other modules with minimal changes.

