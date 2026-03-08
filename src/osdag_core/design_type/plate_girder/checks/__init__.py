"""
Plate Girder Design Checks - Skip Configuration

Only checks that are FULLY INDEPENDENT can be skipped:
- Deflection: Does not depend on any other check, nothing depends on it

Usage:
    from ..checks import SKIP_DEFLECTION
    
    # In plate_girder.py, before deflection check:
    if not SKIP_DEFLECTION:
        # run deflection check
    
To skip deflection, set this to True before running design.
"""

# Independent checks that can be safely skipped
SKIP_DEFLECTION: bool = True
