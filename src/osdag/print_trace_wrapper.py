import sys
import os
import builtins

# File to save the trace output
TRACE_OUTPUT_FILE = "trace_output.txt"

# Path to ignore (conda environment directory)
CONDA_PATH = os.getenv('CONDA_PREFIX', '')  # Automatically gets the current conda environment path

# Backup original print function
original_print = builtins.print

def traced_print(*args, **kwargs):
    # Get the current frame
    frame = sys._getframe(1)
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    file_path = frame.f_globals.get("__file__", "")
    
    # Ignore printing from files in the conda environment
    if CONDA_PATH and file_path.startswith(CONDA_PATH):
        original_print(*args, **kwargs)
        return
    
    # Log the print statement with UTF-8 encoding
    with open(TRACE_OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"Print in function: {function_name}, line {line_number}, file: {file_path}\n")
        f.write(f"  Output: {' '.join(map(str, args))}\n\n")
    
    # Call the original print function
    original_print(*args, **kwargs)

# Clear the output file before starting
with open(TRACE_OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("Trace Log:\n\n")

# Override built-in print
builtins.print = traced_print

# Import and execute the target script
script_path = "osdag/osdagMainPage.py"

with open(script_path) as f:
    code = f.read()
    exec(code)

# Restore original print
builtins.print = original_print
