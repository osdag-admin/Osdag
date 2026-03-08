# tests/test_cli_helpers.py
from osdag_validator_cli import cli
import os
import json
import tempfile

def test_as_number_if_possible():
    assert cli.as_number_if_possible("10") == 10
    assert cli.as_number_if_possible("3.14") == 3.14
    assert cli.as_number_if_possible("hello") == "hello"
    assert cli.as_number_if_possible(5) == 5

def test_run_batch_file_missing(tmp_path):
    p = tmp_path / "nope.csv"
    try:
        cli.run_batch_file(str(p))
        assert False, "should have raised FileNotFoundError"
    except FileNotFoundError:
        assert True

def test_run_batch_file_csv_roundtrip(tmp_path):
    data = "fu,410\nfy,250\n"
    f = tmp_path / "batch.csv"
    f.write_text(data)
    results = cli.run_batch_file(str(f))
    assert isinstance(results, list)
    assert all("command" in r and "result" in r for r in results)
