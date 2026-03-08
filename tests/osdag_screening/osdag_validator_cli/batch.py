# osdag_validator_cli/batch.py
from __future__ import annotations
import os, json, csv
from typing import Any
from .cli import run_batch_file  # reuse CLI batch runner

def run_batch_file_wrapper(path: str, out: str | None = None, out_format: str = "json"):
    """
    Thin wrapper for CLI's run_batch_file to be imported by GUI or other code.
    """
    return run_batch_file(path, out_path=out, out_format=out_format)
