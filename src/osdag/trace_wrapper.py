import sys
import os

# File to save the trace output
TRACE_OUTPUT_FILE = "trace_output.txt"

# Path to ignore (conda environment directory)
CONDA_PATH = os.getenv('CONDA_PREFIX', '')  # Automatically gets the current conda environment path

def trace_calls(frame, event, arg):
    # Get the file path of the current frame
    file_path = frame.f_globals.get("__file__", "")
    
    # Ignore calls from files in the conda environment
    if CONDA_PATH and file_path.startswith(CONDA_PATH):
        return
    
    # Log the function call to the output file
    if event == "call":
        # Get the caller's frame
        caller_frame = frame.f_back
        caller_file = caller_frame.f_globals.get("__file__", "unknown file")
        caller_line = caller_frame.f_lineno

        with open(TRACE_OUTPUT_FILE, "a") as f:
            f.write(f"Calling function: {frame.f_code.co_name} in {file_path}\n")
            f.write(f"  Called from: {caller_file}, line {caller_line}\n\n")
    return trace_calls

# Clear the output file before starting
with open(TRACE_OUTPUT_FILE, "w") as f:
    f.write("Trace Log:\n\n")

# Enable tracing
sys.settrace(trace_calls)

# Import and execute the target script
script_path = "osdag/osdagMainPage.py"

with open(script_path) as f:
    code = f.read()
    exec(code)

# Disable tracing
sys.settrace(None)
