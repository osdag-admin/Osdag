import sys
import os
import runpy

TRACE_OUTPUT_FILE = "trace_output.txt"
CONDA_PATH = os.getenv('CONDA_PREFIX', '')

def trace_calls(frame, event, arg):
    file_path = frame.f_globals.get("__file__", "")
    if CONDA_PATH and file_path.startswith(CONDA_PATH):
        return
    if event == "call":
        caller_frame = frame.f_back
        caller_file = caller_frame.f_globals.get("__file__", "unknown file")
        caller_line = caller_frame.f_lineno
        with open(TRACE_OUTPUT_FILE, "a") as f:
            f.write(f"Calling function: {frame.f_code.co_name} in {file_path}\n")
            f.write(f"  Called from: {caller_file}, line {caller_line}\n\n")
    return trace_calls

# Clear log
with open(TRACE_OUTPUT_FILE, "w") as f:
    f.write("Trace Log:\n\n")

# Set trace
sys.settrace(trace_calls)

# Run osdagMainPage as a module
runpy.run_module("osdag.osdagMainPage", run_name="__main__")

# Clear trace
sys.settrace(None)
