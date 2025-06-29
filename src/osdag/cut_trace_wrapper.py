import sys
import os
import OCC.Core.BRepAlgoAPI
from functools import wraps

# File to save the trace output
TRACE_OUTPUT_FILE = "trace_output_cut.txt"

# Path to ignore (conda environment directory)
CONDA_PATH = os.getenv('CONDA_PREFIX', '')

# Backup original function/class
original_cut_class = OCC.Core.BRepAlgoAPI.BRepAlgoAPI_Cut

# Create a wrapper class that inherits from the original
class TracedCutClass(original_cut_class):
    def __init__(self, *args, **kwargs):
        # Get caller information
        frame = sys._getframe(1)
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        file_path = frame.f_globals.get("__file__", "")
        
        # Ignore calls from conda environment files
        if CONDA_PATH and file_path.startswith(CONDA_PATH):
            super().__init__(*args, **kwargs)
            return
            
        # Call original constructor
        super().__init__(*args, **kwargs)
        
        # Log details
        with open(TRACE_OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"Function Call: BRepAlgoAPI_Cut\n")
            f.write(f"  Called from: {function_name}, line {line_number}, file: {file_path}\n")
            f.write(f"  Arguments count: {len(args)}\n")
            # Safely log argument types without trying to fully stringify them
            arg_types = [type(arg).__name__ for arg in args]
            f.write(f"  Argument types: {arg_types}\n\n")

# Replace the original class with our traced version
OCC.Core.BRepAlgoAPI.BRepAlgoAPI_Cut = TracedCutClass

# Clear output file before starting
with open(TRACE_OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("Trace Log:\n\n")

# Import and execute the target script
script_path = "osdag/osdagMainPage.py"  # Adjust path as needed

# Execute only if this script is run directly
if __name__ == "__main__":
    with open(script_path) as f:
        code = f.read()
        exec(code)

    # Restore original class after execution
    OCC.Core.BRepAlgoAPI.BRepAlgoAPI_Cut = original_cut_class