#!/usr/bin/env python3
# osdag_validator_cli/cli.py
"""
Robust CLI helpers for osdag-validator.

This file exposes:
 - get_validator() -> Validator() instance (raises ImportError if missing)
 - as_number_if_possible(s) -> int/float/str conversion helper
 - format_output / print_result for CLI output
 - cmd_* functions used by the console script
 - run_command(cmd, args) -> dict result (safe for programmatic use)
 - run_batch_file(path, out_path=None, out_format="json")
 - main(argv=None) -> exit code for CLI invocation

Designed to be safely called from:
 - subprocess/python -m osdag_validator_cli.cli ...
 - FastAPI (import programmatic helpers)
 - batch runners / tests
"""

from __future__ import annotations
import sys
import argparse
import json
import csv
import os
from typing import Any

# -------------------------
# Validator import helper
# -------------------------
def get_validator():
    """
    Return an instance of osdag_validator.Validator.

    Raises ImportError with a helpful message if the package is missing.
    """
    try:
        from osdag_validator import Validator  # type: ignore
    except Exception as e:
        raise ImportError(
            "Failed to import osdag_validator.Validator. Make sure osdag and osdag_validator are installed. "
            f"Original error: {e!r}"
        )
    return Validator()

# -------------------------
# small helpers
# -------------------------
def as_number_if_possible(s: Any) -> Any:
    """
    Convert string to int/float where possible; otherwise return original.

    Safe to call on already-parsed values (non-strings) — returns them unchanged.
    """
    if not isinstance(s, str):
        return s
    v = s.strip()
    if v == "":
        return v
    try:
        return int(v)
    except Exception:
        pass
    try:
        return float(v)
    except Exception:
        pass
    return v

def format_output(value: Any, fmt: str = "text") -> str:
    """Serialize result value according to requested format."""
    fmt = (fmt or "text").lower()
    if fmt == "json":
        try:
            return json.dumps({"result": value}, ensure_ascii=False)
        except Exception:
            return json.dumps({"result": str(value)})
    if fmt == "csv":
        if isinstance(value, (list, tuple)):
            out_lines = ["value"]
            out_lines += [str(x) for x in value]
            return "\n".join(out_lines)
        if isinstance(value, dict):
            keys = ",".join(map(str, value.keys()))
            vals = ",".join(map(str, value.values()))
            return keys + "\n" + vals
        return str(value)
    # default: plain text
    if isinstance(value, bool):
        return "Valid" if value else "Invalid"
    return str(value)

def print_result(result: Any, fmt: str = "text"):
    """Print to stdout according to format. Keeps CLI behaviour backward-compatible."""
    if fmt == "text":
        if result is True:
            print("Valid")
            return
        if result is False:
            print("Invalid")
            return
    print(format_output(result, fmt))

# -------------------------
# core command handlers (return exit codes)
# -------------------------
def cmd_validate_fu(args):
    v = get_validator()
    try:
        val = as_number_if_possible(args.value)
        result = v.validate_fu(val)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print_result(result, args.format)
    return 0

def cmd_validate_fy(args):
    v = get_validator()
    try:
        val = as_number_if_possible(args.value)
        result = v.validate_fy(val)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print_result(result, args.format)
    return 0

def cmd_validate_tf(args):
    v = get_validator()
    try:
        val = as_number_if_possible(args.value)
        result = getattr(v, "validate_tf", lambda x: False)(val)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print_result(result, args.format)
    return 0

def cmd_validate_bolt(args):
    v = get_validator()
    try:
        result = getattr(v, "validate_bolt", lambda s,g: False)(args.size, args.grade)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print_result(result, args.format)
    return 0

def cmd_validate_plate(args):
    v = get_validator()
    try:
        thickness = as_number_if_possible(args.thickness)
        width = as_number_if_possible(args.width)
        result = getattr(v, "validate_plate", lambda t,w: False)(thickness, width)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print_result(result, args.format)
    return 0

# -------------------------
# batch helper + CLI runner
# -------------------------
def _run_command_by_name(cmd: str, args: list[str]):
    """Internal runner used by batch and run_command."""
    v = get_validator()
    cmd = (cmd or "").strip()
    try:
        if cmd == "fu":
            val = as_number_if_possible(args[0]) if args else None
            res = v.validate_fu(val)
        elif cmd == "fy":
            val = as_number_if_possible(args[0]) if args else None
            res = v.validate_fy(val)
        elif cmd == "tf":
            val = as_number_if_possible(args[0]) if args else None
            res = getattr(v, "validate_tf", lambda x: False)(val)
        elif cmd == "bolt":
            res = getattr(v, "validate_bolt", lambda s,g: False)(args[0] if args else "", args[1] if len(args)>1 else "")
        elif cmd == "plate":
            t = as_number_if_possible(args[0]) if args else 0
            w = as_number_if_possible(args[1]) if len(args)>1 else 0
            res = getattr(v, "validate_plate", lambda a,b: False)(t, w)
        else:
            res = {"error": f"Unknown command '{cmd}'"}
    except Exception as e:
        res = {"error": str(e)}
    return {"command": cmd, "args": args, "result": res}

def run_command(cmd: str, args: list[str]):
    """Public wrapper returning a result dict (no printing)."""
    return _run_command_by_name(cmd, args)

def run_batch_file(path: str, out_path: str | None = None, out_format: str = "json"):
    """
    Reads CSV or JSON batch file and runs commands.
    CSV format: each row -> command, arg1, arg2, ...
    JSON format: a list of {"command": "fu", "args": ["410"]}
    """
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    results = []
    if path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            if not isinstance(items, list):
                raise ValueError("JSON batch file must contain a list of commands")
            for it in items:
                cmd = it.get("command")
                args = it.get("args", [])
                results.append(_run_command_by_name(cmd, args))
    else:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                cmd = row[0].strip()
                args = [c.strip() for c in row[1:]]
                results.append(_run_command_by_name(cmd, args))
    if out_path:
        out_path = os.path.expanduser(out_path)
        if out_format == "json":
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        elif out_format == "csv":
            with open(out_path, "w", encoding="utf-8", newline='') as f:
                w = csv.writer(f)
                for r in results:
                    w.writerow([r.get("command")] + list(map(str, r.get("args", []))) + [r.get("result")])
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(str(results))
    return results

def cmd_batch(args):
    try:
        results = run_batch_file(args.path, out_path=args.out, out_format=args.format)
    except Exception as e:
        print(f"Batch error: {e}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "csv":
        import io
        buf = io.StringIO()
        w = csv.writer(buf)
        for r in results:
            w.writerow([r.get("command")] + list(map(str, r.get("args", []))) + [r.get("result")])
        print(buf.getvalue())
    else:
        print(results)
    return 0

# ---------- CLI entry ----------
def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(prog="osdag-val", description="CLI for osdag_validator with JSON/CSV and batch")
    sub = parser.add_subparsers(dest="command")

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--format", "-f", choices=("text","json","csv"), default="text",
                               help="Output format")

    p_fu = sub.add_parser("fu", parents=[common_parser])
    p_fu.add_argument("value")
    p_fu.set_defaults(func=cmd_validate_fu)

    p_fy = sub.add_parser("fy", parents=[common_parser])
    p_fy.add_argument("value")
    p_fy.set_defaults(func=cmd_validate_fy)

    p_tf = sub.add_parser("tf", parents=[common_parser])
    p_tf.add_argument("value")
    p_tf.set_defaults(func=cmd_validate_tf)

    p_bolt = sub.add_parser("bolt", parents=[common_parser])
    p_bolt.add_argument("size")
    p_bolt.add_argument("grade")
    p_bolt.set_defaults(func=cmd_validate_bolt)

    p_plate = sub.add_parser("plate", parents=[common_parser])
    p_plate.add_argument("thickness")
    p_plate.add_argument("width")
    p_plate.set_defaults(func=cmd_validate_plate)

    p_batch = sub.add_parser("batch")
    p_batch.add_argument("path", help="CSV or JSON file containing commands")
    p_batch.add_argument("--out", "-o", help="Output file to write results")
    p_batch.add_argument("--format", choices=("json","csv","text"), default="json", help="Output format for batch")
    p_batch.set_defaults(func=cmd_batch)

    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        return args.func(args)
    except ImportError as ie:
        print(str(ie), file=sys.stderr)
        return 4
    except Exception as e:
        print(f"Unhandled error: {e}", file=sys.stderr)
        return 5

if __name__ == "__main__":
    raise SystemExit(main())

# Exports
__all__ = [
    "get_validator",
    "as_number_if_possible",
    "run_command",
    "run_batch_file",
    "format_output",
    "print_result",
]
