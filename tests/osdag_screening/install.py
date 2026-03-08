import os
import shutil
import sys
from pathlib import Path
import stat

print("\n=== Installing osdag-validator-cli ===")

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "osdag_validator_cli"

def remove_readonly(func, path, exc):
    """Make read-only files writable and retry delete."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def safe_rmtree(path: Path):
    """Remove a directory even if __pycache__ is locked or read-only."""
    if path.exists():
        shutil.rmtree(path, onerror=remove_readonly)

def install_package():
    venv_site = Path(sys.executable).parent.parent / "Lib" / "site-packages"
    dst = venv_site / "osdag_validator_cli"

    if not SRC.exists():
        print("ERROR: osdag_validator_cli/ not found beside install.py")
        sys.exit(1)

    print(f"Source: {SRC}")
    print(f"Target: {dst}")

    # 1 — Remove existing installation (safe)
    if dst.exists():
        print("Removing old installation...")
        safe_rmtree(dst)

    # 2 — Copy fresh package
    print("Copying new package...")
    shutil.copytree(SRC, dst)

    print("\nSUCCESS: osdag-validator-cli installed.")
    print("You can now run:")
    print("  python -m osdag_validator_cli.auto_cli")
    print("  python -m osdag_validator_cli.cli_typer")
    print("  python -m osdag_validator_cli.cli")

def main():
    install_package()

if __name__ == "__main__":
    main()
