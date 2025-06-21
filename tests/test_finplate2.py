import pytest
import yaml
from osdag.design_type.connection.fin_plate_connection import FinPlateConnection
import pandas as pd
import glob
import os

# Mock or import these as needed for your environment
# from src.osdag.cad import generate_cad
# from src.osdag.report import generate_report

if not (os.path.exists('FinPlateTest1.osi') and os.path.exists('ExpectedOutputs.xlsx')):

    pytest.skip('Required OSI or Excel file missing, skipping test.', allow_module_level=True)

def get_expected_from_excel(excel_path, osi_filename):
    df = pd.read_excel(excel_path)
    # Find the row matching the OSI file name
    row = df[df['OSI File Name'] == osi_filename].iloc[0]
    # Map Excel columns to output fields (update as needed)
    expected = {
        'Plate.Thickness': row['Gusset Plate Thickness Value'],
        'Plate.Height': row['Gusset Plate Min Height Value'],
        'Plate.Length': row['Gusset Plate Length Value'],
        'Weld.Size': row['Size of Weld Value'],
        'Weld.Strength': row['Weld Strength Value'],
        'Weld.Stress': row['Weld Strength Value'],  # Adjust if different
        # Add more mappings as needed
    }
    return expected

def extract_results_from_output(output):
    # Convert output list of tuples to a dict for easy comparison
    return {k: v for (k, _, _, v, *_) in output if k}

@pytest.mark.parametrize("osi_path", sorted(glob.glob("FinPlateTest*.osi")))

def test_fin_plate_connection_vs_excel(osi_path):
    osi_filename = os.path.basename(osi_path)
    excel_path = "ExpectedOutputs.xlsx"

    osi_data = yaml.safe_load(open(osi_path))
    conn = FinPlateConnection()
    conn.set_input_values(osi_data)
    output = conn.output_values(flag=True)
    results = extract_results_from_output(output)
    expected = get_expected_from_excel(excel_path, osi_filename)
    for key, exp_val in expected.items():
        assert key in results, f"Missing result for {key}"
        # Use tolerance for float comparison
        if isinstance(exp_val, float):
            assert abs(results[key] - exp_val) < 1e-2, f"Mismatch for {key}: {results[key]} != {exp_val}"
        else:
            assert results[key] == exp_val, f"Mismatch for {key}: {results[key]} != {exp_val}"

def test_fin_plate_connection():
    # 1. Load OSI file
    with open('FinPlateTest1.osi', 'r') as f:

        osi_data = yaml.safe_load(f)

    # 2. Create FinPlateConnection instance
    conn = FinPlateConnection()

    # 3. Set input values (mapping is handled in set_input_values)
    conn.set_input_values(osi_data)

    # 4. Run design calculation (simulate pressing 'Design')
    # This is typically done in set_input_values, but you may need to call additional methods if required
    # conn.member_capacity()  # Already called in set_input_values

    # 5. Check calculation values (replace with real expected values from Excel)
    # Example: assert conn.plate.thickness == 8
    # assert conn.bolt.bolt_diameter_provided == 8
    # assert conn.plate.height == 60.0
    # assert conn.plate.length == 40.0
    # assert conn.weld.size == 5
    # assert round(conn.weld.strength, 1) == 662.8
    # assert round(conn.weld.stress, 2) == 347.85

    # 6. Check output fields are populated
    output = conn.output_values(flag=True)
    assert any(o[0] == 'Bolt.Diameter' and o[3] for o in output)
    assert any(o[0] == 'Bolt.Grade_Provided' and o[3] for o in output)
    assert any(o[0] == 'Bolt.Shear' and o[3] for o in output)
    assert any(o[0] == 'Bolt.Bearing' and o[3] for o in output)
    assert any(o[0] == 'Bolt.Capacity' and o[3] for o in output)
    assert any(o[0] == 'Plate.Thickness' and o[3] for o in output)
    assert any(o[0] == 'Plate.Height' and o[3] for o in output)
    assert any(o[0] == 'Plate.Length' and o[3] for o in output)
    assert any(o[0] == 'Weld.Size' and o[3] for o in output)
    assert any(o[0] == 'Weld.Strength' and o[3] for o in output)
    assert any(o[0] == 'Weld.Stress' and o[3] for o in output)

    # 7. Check CAD generation (mocked or real)
    try:
        if hasattr(conn, 'get_3d_components'):
            conn.get_3d_components()
        cad_success = True
    except Exception as e:
        cad_success = False
    assert cad_success, 'CAD generation failed (OCC dependency or other error)'

    # 8. Check report generation (mocked or real)
    try:
        if hasattr(conn, 'save_design'):
            conn.save_design(popup_summary=False)
        report_success = True
    except Exception as e:
        report_success = False
    assert report_success, 'Report generation failed (LaTeX or other error)'

    if not os.path.exists('osi_files/TensionBoltedTest1.osi'):
        pytest.skip("Missing OSI file, skipping test.")

    # ... rest of the test ...