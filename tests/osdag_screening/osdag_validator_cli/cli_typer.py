# osdag_validator_cli/cli_typer.py
"""
Typer-based modern CLI wrapper for osdag_validator.Validator.

Usage examples:
  python -m osdag_validator_cli.cli_typer fu 410
  python -m osdag_validator_cli.cli_typer fy 250
  python -m osdag_validator_cli.cli_typer fu-fy 410 250
  python -m osdag_validator_cli.cli_typer number 12.5
  python -m osdag_validator_cli.cli_typer positive 8
  python -m osdag_validator_cli.cli_typer bolt M20 8.8
  python -m osdag_validator_cli.cli_typer plate 10 250
"""

from typing import Optional
import typer

app = typer.Typer(help="Modern CLI wrapper for osdag_validator (Typer)")

def get_validator():
    try:
        from osdag_validator import Validator
    except Exception as e:
        raise RuntimeError(
            "Failed to import osdag_validator.Validator. Ensure osdag and osdag_validator are installed."
        ) from e
    return Validator()

def print_result_bool(res: bool):
    typer.echo("Valid" if res else "Invalid")

# Base commands
@app.command("fu")
def fu(value: int):
    """Validate fu value (integer)."""
    v = get_validator()
    try:
        res = v.validate_fu(value)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

@app.command("fy")
def fy(value: int):
    """Validate fy value (integer)."""
    v = get_validator()
    try:
        res = v.validate_fy(value)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

@app.command("fu-fy")
def fu_fy(fu: int, fy: int):
    """Validate fu > fy relation."""
    v = get_validator()
    try:
        res = v.validate_fu_fy(fu, fy)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

@app.command("number")
def number(value: str):
    """Check if value is numeric."""
    v = get_validator()
    try:
        res = v.validate_number(value)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

@app.command("positive")
def positive(value: float):
    """Check if value is positive."""
    v = get_validator()
    try:
        res = v.validate_positive_value(value)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

# Optional commands (may or may not be implemented by Validator)
@app.command("tf")
def tf(value: int):
    v = get_validator()
    if not hasattr(v, "validate_tf"):
        typer.echo("Invalid")
        raise typer.Exit(code=0)
    try:
        res = v.validate_tf(value)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

@app.command("bolt")
def bolt(size: str, grade: str):
    v = get_validator()
    if not hasattr(v, "validate_bolt"):
        typer.echo("Invalid")
        raise typer.Exit(code=0)
    try:
        res = v.validate_bolt(size, grade)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

@app.command("plate")
def plate(thickness: float, width: float):
    v = get_validator()
    if not hasattr(v, "validate_plate"):
        typer.echo("Invalid")
        raise typer.Exit(code=0)
    try:
        res = v.validate_plate(thickness, width)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)
    print_result_bool(res)

if __name__ == "__main__":
    app()
