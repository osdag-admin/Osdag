# osdag_validator_cli/entry.py
"""
Tiny launcher used by PyInstaller. Keeps CLI entrypoint explicit and small.
"""

from __future__ import annotations
import sys

# Import the module-level main() from your CLI wrapper
# (this matches the module you already tested: osdag_validator_cli.cli)
from osdag_validator_cli.cli import main

def run():
    # main() expects argv similar to sys.argv[1:]
    # We call it and exit with its return code.
    try:
        return_code = main()
        # If main returned None, convert to 0
        if return_code is None:
            return_code = 0
        # Ensure an int return code
        sys.exit(int(return_code))
    except SystemExit as se:
        # allow SystemExit to propagate properly
        raise
    except Exception as exc:
        # Show a helpful error for users running the exe
        print("Error running osdag-val:", exc, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run()
