import sys
import os

# Files to save the trace outputs
TRACE_OUTPUT_FILE = "trace_output.txt"
UNIQUE_FUNCTIONS_FILE = "trace_functions.txt"

# Path to ignore (conda environment directory)
CONDA_PATH = os.getenv('CONDA_PREFIX', '')

# Set to store unique function calls
unique_functions = set()

def trace_calls(frame, event, arg):
    # Get the file path of the current frame
    file_path = frame.f_globals.get("__file__", "")
    
    # Ignore calls from files in the conda environment
    if CONDA_PATH and file_path.startswith(CONDA_PATH):
        return
    
    # Log function calls
    if event == "call":
        # Get caller information
        caller_frame = frame.f_back
        caller_file = caller_frame.f_globals.get("__file__", "unknown file")
        caller_line = caller_frame.f_lineno
        
        # Log all calls to trace_output.txt
        with open(TRACE_OUTPUT_FILE, "a") as f:
            f.write(f"Calling function: {frame.f_code.co_name} in {file_path}\n")
            f.write(f"  Called from: {caller_file}, line {caller_line}\n\n")
        
        # Store unique function information
        function_info = f"Function: {frame.f_code.co_name}\nLocation: {file_path}\n"
        if function_info not in unique_functions:
            unique_functions.add(function_info)
            # Write to unique functions file
            with open(UNIQUE_FUNCTIONS_FILE, "a") as f:
                f.write(f"{function_info}\n")
    
    return trace_calls

# Clear both output files before starting
with open(TRACE_OUTPUT_FILE, "w") as f:
    f.write("Trace Log:\n\n")
    
with open(UNIQUE_FUNCTIONS_FILE, "w") as f:
    f.write("Unique Functions Log:\n\n")

# Enable tracing
sys.settrace(trace_calls)

# Import and execute the target script
script_path = "osdag/osdagMainPage.py"
with open(script_path) as f:
    code = f.read()
    exec(code)

# Disable tracing
sys.settrace(None)