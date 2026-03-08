"""
Autogen generator: inspect osdag.utils.validator and write auto_cli + tests.

Usage:
    python -m osdag_validator_cli._autogen_generator
This will generate:
 - osdag_validator_cli/auto_cli.py
 - osdag-validator-cli/tests/test_auto_cli.py
"""

from inspect import isclass, isfunction, signature
import importlib
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]  # package root osdag_validator_cli
OUT_AUTO = ROOT / "auto_cli.py"
OUT_TEST = ROOT.parent / "tests" / "test_auto_cli.py"

def safe_method_name(name: str) -> str:
    return name.replace("-", "_")

def should_expose(callable_obj):
    # Expose only callables that look like validators:
    sig = signature(callable_obj)
    # Only functions with 1 or 2 parameters (simple) are auto-exposed.
    params = [p for p in sig.parameters.values() if p.name != "self"]
    if len(params) > 3:
        return False
    # avoid methods that clearly expect complex objects by name hints
    complex_hints = ("member", "bolt", "plate", "supported", "supporting", "angle")
    for p in params:
        if any(h in p.name.lower() for h in complex_hints):
            # we still expose but with a note that user must pass simple literals
            pass
    return True

def param_parser_code(param_name: str):
    # returns code to attempt int->float->str conversion
    return textwrap.dedent(f"""\
        try:
            {param_name}_val = int({param_name})
        except Exception:
            try:
                {param_name}_val = float({param_name})
            except Exception:
                {param_name}_val = {param_name}
    """)

def main():
    mod = importlib.import_module("osdag.utils.validator")
    lines = []
    lines.append('"""Auto-generated CLI wrappers for simple Validator methods"""')
    lines.append("from __future__ import annotations")
    lines.append("import sys")
    lines.append("def get_validator():\n    from osdag_validator import Validator\n    return Validator()\n")
    lines.append("def print_result(result):\n    if result is True:\n        print('Valid')\n    elif result is False:\n        print('Invalid')\n    elif isinstance(result, str):\n        print(result)\n    else:\n        print('Valid' if result else 'Invalid')\n")

    # iterate classes
    for name, cls in mod.__dict__.items():
        if not isclass(cls):
            continue
        if cls.__module__ != "osdag.utils.validator":
            continue
        # find methods
        for attr_name, attr in cls.__dict__.items():
            if attr_name.startswith("_"):
                continue
            if not callable(attr):
                continue
            if not should_expose(attr):
                continue

            func_name = f"{name}_{attr_name}"
            # build wrapper function
            sig = signature(attr)
            params = [p for p in sig.parameters.values() if p.name != "self"]
            params_list = [p.name for p in params]
            param_args = ", ".join(params_list)
            lines.append(f"def {func_name}({', '.join(params_list)}):")
            # parse args
            if params:
                for p in params_list:
                    lines.append("    " + param_parser_code(p).replace("\n", "\n    ").rstrip())
                call_args = ", ".join(f"{p}_val" for p in params_list)
            else:
                call_args = ""
            lines.append(f"    v = get_validator()")
            lines.append(f"    try:")
            lines.append(f"        result = v.__class__().{attr_name}({call_args})  # instance method call")
            lines.append(f"    except Exception as e:")
            lines.append(f"        raise")
            lines.append(f"    print_result(result)\n")

    # write the auto_cli
    OUT_AUTO.write_text("\n".join(lines))
    print("Wrote", OUT_AUTO)

    # now create a simple pytest file that calls a few wrappers
    test_lines = [
        "import subprocess, sys, os, shlex",
        "HERE = os.path.dirname(__file__)",
        "PY = sys.executable",
        "",
        "def run_cmd(cmd):",
        "    p = subprocess.run([PY, '-c', cmd], capture_output=True, text=True)",
        "    return p",
        "",
        "# Basic smoke tests - ensure wrappers import/execute without crash",
    ]
    # pick a few generated functions to test
    for line in lines:
        if line.startswith("def ") and "(" in line:
            fname = line.split()[1].split("(")[0]
            # produce a simple command that imports and calls function with small args
            test_lines.append(f"def test_{fname}_smoke():")
            # build a tiny invocation based on parameters (all params treated as '1' or '1.0')
            sig_line = line
            # detect number of params
            params_part = line[line.find("(")+1:line.find(")")]
            if params_part.strip() == "":
                args = ""
            else:
                count = len([p.strip() for p in params_part.split(",") if p.strip()])
                # choose '1' for integer-like values
                args = ", ".join(["'1'"] * count)
            test_lines.append(f"    cmd = \"from osdag_validator_cli.auto_cli import {fname}; {fname}({args})\"")
            test_lines.append(f"    p = run_cmd(cmd)")
            test_lines.append(f"    assert p.returncode == 0")
            test_lines.append("")
            # limit tests to 12 wrappers
            if len([l for l in test_lines if l.startswith("def test_")]) > 12:
                break

    OUT_TEST.write_text("\n".join(test_lines))
    print("Wrote", OUT_TEST)

if __name__ == "__main__":
    main()
